"""Checks across lookup matching, missing data and report interpretation."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone

from shadow_ship_check.analyze import analyze, merge_lookup_identities
from shadow_ship_check.geo import CableLayer
from shadow_ship_check.models import Identity

T = datetime(2025, 1, 1, tzinfo=timezone.utc)


def test_missing_imo_variant_cannot_import_a_known_foreign_hull():
    own = Identity("SHIP", "DEU", "211000001", "9000001", None, T, T + timedelta(days=10), False, "ais")
    unknown = replace(own, imo=None)
    foreign = replace(own, imo="9000002", registry_confirmed=True)
    result = merge_lookup_identities([own, unknown], {own.mmsi: [foreign]})
    assert {i.imo for i in result} == {"9000001", None}
    assert not any(i.registry_confirmed for i in result)


def test_empty_data_and_empty_cable_layer_are_explicit():
    report = analyze("9000001", [], [], window=(T, T + timedelta(days=1)), cables=CableLayer([]))
    assert report.score == 0
    assert any("No identity records" in n for n in report.notes)
    assert any("No positions" in n for n in report.notes)
    assert any("cable crossings were not checked" in n for n in report.notes)


def test_fixture_rejects_foreign_imo_but_keeps_conflict_lookup():
    from shadow_ship_check.analyze import analyze_fixture

    def entry(imo, flag, mmsi):
        return {
            "selfReportedInfo": [
                {
                    "shipname": "SHIP",
                    "flag": flag,
                    "ssvid": mmsi,
                    "imo": imo,
                    "transmissionDateFrom": "2025-01-01T00:00:00Z",
                    "transmissionDateTo": "2025-01-10T00:00:00Z",
                }
            ]
        }

    case = {"imo": "9000001", "window": (T, T + timedelta(days=1)), "primary_track": "own"}
    fixture = {
        "identities": [entry("9000001", "DEU", "211000001"), entry("9000002", "CMR", "613000001")],
        "tracks": {"own": {"start": "2025-01-01", "end": "2025-01-02", "points": []}},
        "mmsi_lookups": {"211000001": [entry("9000002", "DEU", "211000001")]},
    }
    r = analyze_fixture(case, fixture)
    assert {i.imo for i in r.identities} == {"9000001"}
    assert any(s.code == "MMSI_REUSE" for s in r.signals)


def test_malformed_fixture_mapping_is_a_cli_error(tmp_path, capsys):
    import json

    from shadow_ship_check.cli import main

    (tmp_path / "eagle_s.json").write_text(json.dumps({"identities": [], "tracks": []}))
    assert main(["case", "eagle_s", "--fixtures", str(tmp_path)]) == 2
    assert "Fixture tracks" in capsys.readouterr().err
