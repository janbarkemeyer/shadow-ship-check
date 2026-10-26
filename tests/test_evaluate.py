import gzip
import json

from shadow_ship_check import evaluate


def _info(name, flag, mmsi, imo, start, end):
    return {
        "shipname": name,
        "flag": flag,
        "ssvid": mmsi,
        "imo": imo,
        "callsign": None,
        "transmissionDateFrom": start,
        "transmissionDateTo": end,
    }


def _record(label, infos, as_of="2025-06-01"):
    return {"imo": "1", "as_of": as_of, "label": label, "identities": [{"registryInfo": [], "selfReportedInfo": infos}]}


def test_auc():
    assert evaluate.auc([3, 4], [1, 2]) == 1.0
    assert evaluate.auc([1], [1]) == 0.5


def test_score_uses_only_history_before_the_reference_date():
    rec = _record(
        "sanctioned",
        [
            _info("A", "GRC", "240000001", "9000001", "2015-01-01T00:00:00Z", "2024-01-01T00:00:00Z"),
            _info("B", "CMR", "613000001", "9000001", "2024-01-01T00:00:00Z", "2026-01-01T00:00:00Z"),
            _info("C", "TGO", "671000001", "9000001", "2025-07-01T00:00:00Z", "2026-01-01T00:00:00Z"),  # later
        ],
    )
    score, points = evaluate.score_record(rec)
    assert points["MULTI_IDENTITY"] == 10  # A and B only
    assert "SANCTIONED" not in points
    assert score == sum(points.values())


def test_evaluate_end_to_end(tmp_path):
    hopper = [
        _info("A", "GRC", "240000001", "9000001", "2015-01-01T00:00:00Z", "2024-01-01T00:00:00Z"),
        _info("B", "CMR", "613000001", "9000001", "2024-01-01T00:00:00Z", "2026-01-01T00:00:00Z"),
    ]
    plain = [_info("P", "DEU", "211000001", "9000002", "2015-01-01T00:00:00Z", "2026-01-01T00:00:00Z")]
    data = {"meta": {"title": "test"}, "records": [_record("sanctioned", hopper), _record("control", plain)]}
    path = tmp_path / "e.json.gz"
    with gzip.open(path, "wt", encoding="utf-8") as fh:
        json.dump(data, fh)
    r = evaluate.evaluate(evaluate.load(path))
    assert r["auc"] == 1.0 and r["n"] == {"sanctioned": 1, "control": 1}
    assert "AUC 1.00" in evaluate.to_text(r, data["meta"])


def test_bundled_evaluation_set():
    """Regression guard: rule changes that wreck the out-of-sample separation show up here."""
    data = evaluate.load()
    r = evaluate.evaluate(data)
    assert r["n"] == {"sanctioned": 300, "control": 300}
    assert r["auc"] > 0.75
    assert r["levels"]["HIGH"]["sanctioned_flagged"] > 4 * r["levels"]["HIGH"]["controls_flagged"]


def test_name_lookup_keeps_all_rows_for_a_new_mmsi():
    own = _info("A", "PLW", "511000001", "9000001", "2024-01-01T00:00:00Z", "2025-06-01T00:00:00Z")
    other = _info("A", "PLW", "511000002", "9000002", "2024-01-01T00:00:00Z", "2025-06-01T00:00:00Z")
    missing_imo = {**other, "imo": None}
    rec = _record("sanctioned", [own])
    rec["name_lookups"] = {"A": [{"selfReportedInfo": [other, missing_imo]}]}
    score, points = evaluate.score_record(rec)
    assert points["NAME_ON_OTHER_MMSI"] == 15
    rec["name_lookups"]["A"][0]["selfReportedInfo"].reverse()
    assert evaluate.score_record(rec) == (score, points)


def test_evaluation_reference_converts_timezone():
    from datetime import datetime, timezone

    assert evaluate._ref("2025-01-02T20:00+08:00") == datetime(2025, 1, 2, 12, tzinfo=timezone.utc)
