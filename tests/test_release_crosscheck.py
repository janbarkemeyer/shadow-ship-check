"""Cross-layer counterexamples: hull selection, cut-off views, edge rules and output wording."""

import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from shadow_ship_check import cli, evaluate, signals
from shadow_ship_check.analyze import analyze
from shadow_ship_check.geo import CableLayer
from shadow_ship_check.gfw import hull_identities
from shadow_ship_check.models import Identity, Report, Signal, TrackPoint
from shadow_ship_check.report import _key_evidence

T = datetime(2025, 1, 1, tzinfo=timezone.utc)


def ident(name="SHIP", flag="PAN", mmsi="351000001", imo="9000001", start=(2015, 1, 1), end=(2025, 1, 1), reg=False):
    return Identity(
        name,
        flag,
        mmsi,
        imo,
        None,
        datetime(*start, tzinfo=timezone.utc),
        datetime(*end, tzinfo=timezone.utc),
        reg,
        "ais",
    )


def tp(hours, lat=60.0, lon=25.0, kn=10.0, segment=0):
    return TrackPoint(T + timedelta(hours=hours), lat, lon, kn, segment)


def row(**kw):
    base = {
        "shipname": "SHIP",
        "flag": "PAN",
        "ssvid": "351000001",
        "imo": "9000001",
        "id": "own",
        "transmissionDateFrom": "2024-01-01T00:00:00Z",
        "transmissionDateTo": "2025-01-02T00:00:00Z",
    }
    return {**base, **kw}


# --- hull selection is the same for live checks, fixtures and the evaluation ------------------------


def test_hull_keeps_earlier_names_grouped_in_the_same_entry():
    entries = [{"selfReportedInfo": [row(), row(shipname="OLD NAME", ssvid="412000001", imo=None, id="old")]}]
    names = {i.name for i in hull_identities(entries, "9000001")}
    assert names == {"SHIP", "OLD NAME"}


def test_hull_drops_fuzzy_entries_and_foreign_imo_rows():
    entries = [
        {"selfReportedInfo": [row(), row(shipname="OTHER", imo="9000002", id="x")]},
        {"selfReportedInfo": [row(shipname="NAMESAKE", ssvid="999000001", imo=None, id="y")]},
    ]
    assert [i.name for i in hull_identities(entries, "9000001")] == ["SHIP"]


def test_evaluation_and_fixture_selection_share_the_hull_rule():
    rec = {
        "imo": "9000001",
        "label": "control",
        "as_of": "2025-01-01",
        "identities": [{"selfReportedInfo": [row(), row(shipname="OTHER", imo="9000002", id="x")]}],
    }
    score, points = evaluate.score_record(rec)
    assert "MULTI_IDENTITY" not in points or points["MULTI_IDENTITY"] == 0


# --- foreign IMOs cannot enter through a name link or a cut-off -------------------------------------


class _Client:
    def __init__(self, also_rows):
        self.also_rows = also_rows

    def search_raw(self, query):
        if query == "9000001":
            return [{"selfReportedInfo": [row()]}]
        if query == "SHIPX":
            return [{"selfReportedInfo": self.also_rows}]
        return [{"selfReportedInfo": [row()]}]

    def track(self, vid, start, end):
        return [TrackPoint(T + timedelta(hours=h), 0, 0, 10) for h in range(12)]


def _check(monkeypatch, tmp_path, also_rows):
    monkeypatch.setattr(cli, "GFWClient", lambda: _Client(also_rows))
    out = tmp_path / "r.json"
    code = cli.main(
        ["check", "9000001", "--also", "SHIPX", "--start", "2025-01-01", "--end", "2025-01-02", "--json", str(out)]
    )
    return code, (json.loads(out.read_text()) if out.exists() else None)


def test_also_name_link_ignores_namesakes_with_other_imos(monkeypatch, tmp_path):
    rows = [
        row(shipname="SHIPX", ssvid="351000009", imo=None, id="ok"),
        row(shipname="SHIPX", ssvid="352000001", imo="8518780", id="foreign"),
    ]
    code, report = _check(monkeypatch, tmp_path, rows)
    assert code == 0
    assert {i.get("imo") for i in report["identities"]} <= {"9000001", None}


def test_also_name_link_with_only_foreign_imos_stops(monkeypatch, tmp_path, capsys):
    code, _ = _check(monkeypatch, tmp_path, [row(shipname="SHIPX", ssvid="352000001", imo="8518780", id="f")])
    assert code == 2
    assert "8518780" in capsys.readouterr().err


def test_cut_off_cannot_adopt_a_foreign_imo_from_lookups():
    own_old = ident(imo=None, start=(2021, 1, 1), end=(2021, 6, 1))
    own_new = ident(start=(2023, 1, 1), end=(2024, 1, 1))
    foreign = ident(imo="8518780", start=(2021, 1, 1), end=(2021, 6, 1), reg=True)
    report = analyze(
        "x",
        [own_old, own_new],
        [],
        window=(datetime(2022, 11, 1, tzinfo=timezone.utc), datetime(2022, 12, 1, tzinfo=timezone.utc)),
        mmsi_lookups={"351000001": [foreign]},
        as_of=datetime(2022, 12, 1, tzinfo=timezone.utc),
    )
    assert "8518780" not in {i.imo for i in report.identities}
    assert "REGISTRY_LOST" not in {s.code for s in report.signals}


# --- identity rules ------------------------------------------------------------------------------


def test_registry_lost_not_scored_while_a_confirmed_identity_is_still_in_use():
    confirmed = ident(reg=True)
    second = ident(mmsi="351000002", start=(2024, 6, 1))
    assert signals.registry_confirmation([confirmed, second], T) == []


def test_missing_flag_is_not_a_different_flag():
    a = ident(reg=True)
    blank = ident(flag=None, start=(2023, 1, 1), end=(2023, 6, 1))
    multi = signals.multiple_identities([a, blank], T)
    assert multi and multi[0].points == 0
    concurrent = signals.concurrent_identities([a, replace(blank, mmsi="351000002")], T)
    assert concurrent and concurrent[0].points == 5


# --- movement rules ------------------------------------------------------------------------------


def test_duplicate_timestamp_does_not_split_a_slow_run():
    run = [tp(i / 2, lon=25 + i / 2 * 4 / 60, kn=2.0) for i in range(13)]
    duplicate = run[:7] + [replace(run[6])] + run[7:]
    assert signals.slow_movement(run)[0].points == signals.slow_movement(duplicate)[0].points == 10


def test_date_line_track_does_not_abort_cable_check():
    track = [tp(h, lat=0, lon=lon, kn=3) for h, lon in enumerate([179.9, 179.95, 180.0, -179.95, -179.9])]
    report = analyze("x", [], track, window=(T, T + timedelta(hours=10)), cables=CableLayer.bundled())
    assert report.score >= 0


def test_silence_at_the_window_end_is_described_not_scored():
    track = [tp(h, lon=25 + 0.2 * h, kn=12) for h in range(-24, 21)]
    gaps = signals.ais_gaps(track, window=(T, T + timedelta(hours=48)))
    assert gaps and gaps[0].points == 0
    assert any("window end/cut-off" in e and "not scored" in e for e in gaps[0].evidence)


# --- outputs -------------------------------------------------------------------------------------


def test_summary_line_prefers_scored_recent_evidence():
    s = Signal(
        "FLAG_CHANGE",
        "2 flag change(s)",
        15,
        ["2010-01-01: A -> B (x)  [N -> N]", "2024-03-04: B -> C (y)  [N -> M]  (recent)"],
    )
    assert "(recent)" in _key_evidence(s)
    gap = Signal(
        "AIS_GAP", "AIS gaps", 15, ["no positions ... so no additional absence points", "13.9 h without position"]
    )
    assert _key_evidence(gap) == "13.9 h without position"


def test_eval_reports_the_documented_extra_figures():
    result = evaluate.evaluate(evaluate.load())
    assert round(result["single_rule_auc"]["FLAG_CHANGE"], 2) == 0.84
    lo, hi = result["flag_change_minus_total_ci95"]
    assert lo < 0 < hi
    assert round(result["grey_or_black_flag_share"]["sanctioned"], 2) == 0.51
    assert result["reference_flags"]["sanctioned"]["RUS"] == 68


def test_eval_text_names_the_labels_not_a_shadow_fleet(capsys):
    assert cli.main(["eval"]) == 0
    text = capsys.readouterr().out
    assert "shadow-fleet" not in text.splitlines()[0] and "MEDIUM or HIGH" in text


def test_broken_pipe_exits_quietly(monkeypatch, capsys):
    def boom(args):
        raise BrokenPipeError

    monkeypatch.setattr(cli, "cmd_eval", boom)
    assert cli.main(["eval"]) == 0
    assert "Broken pipe" not in capsys.readouterr().err


@pytest.mark.parametrize("empty", [None, {}])
def test_missing_mmsi_lookups_are_stated(empty):
    report = analyze("x", [ident()], [], window=(T - timedelta(days=1), T), mmsi_lookups=empty)
    assert any("MMSI look-ups" in n for n in report.notes)
    assert isinstance(report, Report)


def test_short_overlap_at_the_cut_off_still_counts_as_registry_lost():
    confirmed = ident(reg=True, end=(2025, 3, 1))
    new = ident(name="NEW", flag="BES", mmsi="351000009", start=(2024, 12, 10), end=(2025, 3, 1))
    report = analyze(
        "x",
        [confirmed, new],
        [],
        window=(T - timedelta(days=3), T),
        mmsi_lookups={"x": []},
        as_of=T,
    )
    assert ("REGISTRY_LOST", 15) in [(s.code, s.points) for s in report.signals]


def test_missing_flag_with_an_unknown_foreign_mmsi_prefix_stays_different():
    a = ident(flag="RUS", mmsi="273258960", reg=True)
    blank = ident(flag=None, mmsi="442303030", start=(2024, 6, 1))
    concurrent = signals.concurrent_identities([a, blank], T)
    assert concurrent[0].points == 20


def test_mmsi_query_does_not_adopt_another_ships_entry():
    hull = {"selfReportedInfo": [row()], "registryInfo": [row(id=None)]}
    other = {
        "selfReportedInfo": [
            row(shipname="OTHER", imo=None, id="o1"),
            row(shipname="OTHER", ssvid="671000002", imo=None, id="o2"),
        ],
        "registryInfo": [row(shipname="OTHER", ssvid="671000002", imo="9000002", id=None)],
    }
    found = hull_identities([hull, other], "351000001")
    assert {(i.name, i.mmsi) for i in found} == {("SHIP", "351000001"), ("OTHER", "351000001")}
    assert not any(i.registry_confirmed for i in found if i.name == "OTHER")


def test_foreign_entry_registry_rows_never_confirm_kept_rows():
    hull = {"selfReportedInfo": [row()]}
    other = {
        "selfReportedInfo": [
            row(shipname="OTHER", imo=None, id="o1"),
            row(shipname="OTHER", ssvid="671000002", imo="9111111", id="o2"),
        ],
        "registryInfo": [row(shipname="OTHER", imo=None, id=None)],
    }
    found = [i for i in hull_identities([hull, other], "351000001") if i.name == "OTHER"]
    assert found and not any(i.registry_confirmed for i in found)


def test_registry_lost_overlap_counts_only_up_to_the_reference_date():
    older = ident(name="OLDEST", mmsi="352000001", start=(2010, 1, 1), end=(2014, 1, 1), reg=True)
    conf = ident(name="CONF", mmsi="352000002", start=(2024, 3, 1), end=(2025, 4, 1), reg=True)
    cur = ident(name="NEW", flag="CMR", mmsi="613000003", start=(2024, 12, 27), end=(2025, 3, 1))
    codes = [s.code for s in signals.registry_confirmation([older, conf, cur], T)]
    assert codes == ["REGISTRY_LOST"]
