"""Regression tests on the reference incidents (offline fixtures)."""

import pytest

from shadow_ship_check.analyze import analyze_fixture, load_fixture
from shadow_ship_check.cases import ALL, CASES, CONTROLS
from shadow_ship_check.cli import main
from shadow_ship_check.geo import CableLayer


def run(name, fixtures_dir):
    return analyze_fixture(CASES[name], load_fixture(fixtures_dir / f"{name}.json"))


def codes(report, min_points=1):
    return {s.code for s in report.signals if s.points >= min_points}


def test_eagle_s(fixtures_dir):
    r = run("eagle_s", fixtures_dir)
    assert {"FLAG_CHANGE", "REGISTRY_LOST", "AIS_GAP"} <= codes(r)
    gap = next(s for s in r.signals if s.code == "AIS_GAP")
    assert any("overlaps the analysis window" in e for e in gap.evidence)
    assert r.excerpt == []  # GFW has no positions around the Estlink 2 failure


def test_xingshun_39(fixtures_dir):
    r = run("xingshun_39", fixtures_dir)
    assert {
        "MULTI_IDENTITY",
        "FLAG_CHANGE",
        "NO_REGISTRY",
        "ZIGZAG",
        "SLOW_LOITERING",
        "CONCURRENT_IDENTITIES",
        "IDENTITY_HANDOVER",
    } <= codes(r)
    handover = next(s for s in r.signals if s.code == "IDENTITY_HANDOVER")
    # the Cameroon identity hands back to the Tanzania identity within the hour, same spot
    assert any("SHUNXING39" in e and "-> XINGSHUN39" in e and "0.2 nm" in e for e in handover.evidence)


def test_hong_tai_58(fixtures_dir):
    r = run("hong_tai_58", fixtures_dir)
    assert {
        "MULTI_IDENTITY",
        "FLAG_CHANGE",
        "REGISTRY_LOST",
        "MMSI_REUSE",
        "IMO_HIDDEN",
        "PARALLEL_TRACKS",
        "CONCURRENT_IDENTITIES",
        "IDENTITY_HANDOVER",
    } <= codes(r)
    slow = next(s for s in r.signals if s.code == "SLOW_LOITERING")
    assert any("43.5 h stationary" in e for e in slow.evidence)  # anchored next to the cable for ~2 days
    # ship leaves its anchorage right around the reported cable break
    assert max(p.speed for _, p in r.excerpt) >= 4.5


def test_yi_peng_3_has_no_identity_camouflage(fixtures_dir):
    r = run("yi_peng_3", fixtures_dir)
    assert "MULTI_IDENTITY" not in codes(r) and "FLAG_CHANGE" not in codes(r)
    assert "SPEED_DROP" in codes(r)


def test_newnew_polar_bear(fixtures_dir):
    r = run("newnew_polar_bear", fixtures_dir)
    assert {"REGISTRY_LOST", "FLAG_CHANGE"} <= codes(r)
    assert r.level in {"MEDIUM", "HIGH"}


@pytest.mark.parametrize("name", list(CASES))
def test_score_bounds(name, fixtures_dir):
    r = run(name, fixtures_dir)
    assert 0 <= r.score <= 100


def test_cli_case_all(tmp_path, fixtures_dir, capsys):
    assert main(["case", "all", "--fixtures", str(fixtures_dir), "--md", str(tmp_path)]) == 0
    assert len(list(tmp_path.glob("*.md"))) == len(ALL)  # one combined report per case
    text = (tmp_path / "hong_tai_58.md").read_text()
    assert "Before the incident" in text and "Full data" in text


@pytest.mark.parametrize("name", list(CONTROLS))
def test_controls_stay_low(name, fixtures_dir):
    """Ordinary ships in the same waters must not be flagged."""
    r = analyze_fixture(CONTROLS[name], load_fixture(fixtures_dir / f"{name}.json"), CableLayer.bundled())
    assert r.level == "LOW", [(s.code, s.points) for s in r.signals]


def test_incidents_score_above_controls(fixtures_dir):
    worst_control = max(analyze_fixture(c, load_fixture(fixtures_dir / f"{n}.json")).score for n, c in CONTROLS.items())
    flagged = [n for n in CASES if run(n, fixtures_dir).score > worst_control]
    assert set(flagged) >= {"eagle_s", "xingshun_39", "hong_tai_58", "newnew_polar_bear"}


def before(name, fixtures_dir):
    return analyze_fixture(CASES[name], load_fixture(fixtures_dir / f"{name}.json"), before_incident=True)


def test_cutoff_removes_later_identity_timestamps(fixtures_dir):
    r = before("newnew_polar_bear", fixtures_dir)
    assert "BELLE ARIES" not in {i.name for i in r.identities}  # renamed only in 2025
    assert all(i.end <= CASES["newnew_polar_bear"]["as_of"] for i in r.identities if i.end)


def test_timestamp_filtered_cases_keep_their_documented_signals(fixtures_dir):
    """Current links remain: these assertions do not test an advance warning."""
    xs = before("xingshun_39", fixtures_dir)
    assert {"CONCURRENT_IDENTITIES", "IDENTITY_HANDOVER"} <= codes(xs) and xs.level == "HIGH"
    ht = before("hong_tai_58", fixtures_dir)
    assert {"PARALLEL_TRACKS", "IDENTITY_HANDOVER", "NAME_ON_OTHER_MMSI"} <= codes(ht) and ht.level == "HIGH"
    assert before("yi_peng_3", fixtures_dir).level == "LOW"


def test_bundled_cables_slow_crossings(fixtures_dir):
    """With the OpenStreetMap cable layer: Yi Peng 3 crosses C-Lion1 at reduced speed around the
    reported failure time, the Helsinki-Tallinn ferry crosses cables only at cruising speed."""
    cables = CableLayer.bundled()

    def signals(name):
        r = analyze_fixture(ALL[name], load_fixture(fixtures_dir / f"{name}.json"), cables)
        return {s.code: s for s in r.signals}

    yp = signals("yi_peng_3")["CABLE_CROSSING_SLOW"]
    assert any("C-Lion 1" in e and "2024-11-18 01:39" in e for e in yp.evidence)
    assert "CABLE_CROSSING_SLOW" not in signals("control_finlandia")
    assert "CABLE_CROSSING_SLOW" in signals("xingshun_39")
