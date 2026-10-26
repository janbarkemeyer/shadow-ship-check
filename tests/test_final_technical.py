"""Boundary tests for live identity matching and user supplied source data."""

import json
from datetime import datetime, timedelta, timezone

import pytest

from shadow_ship_check import cli
from shadow_ship_check.geo import CableLayer
from shadow_ship_check.gfw import identities_from_entries
from shadow_ship_check.models import TrackPoint


@pytest.mark.parametrize(
    "lookup_imo,include_track,metadata_variant,manual",
    [
        ("9000002", False, False, False),
        ("9000002", False, True, False),
        (None, True, False, False),
        (None, True, True, False),
        ("9000002", True, False, True),
    ],
)
def test_live_tracks_respect_hull_linking(monkeypatch, tmp_path, lookup_imo, include_track, metadata_variant, manual):
    now = datetime(2025, 1, 1, tzinfo=timezone.utc)
    own = {
        "shipname": "SHIP",
        "flag": "DEU",
        "ssvid": "211000001",
        "imo": "9000001",
        "id": "own",
        "transmissionDateFrom": "2024-01-01T00:00:00Z",
        "transmissionDateTo": "2025-01-02T00:00:00Z",
    }
    other = {**own, "imo": lookup_imo, "id": "other"}
    requested = []

    query_id = "211000001" if metadata_variant else "9000001"

    class Client:
        first = True

        def search_raw(self, query):
            if self.first:
                self.first = False
                rows = [own, {**own, "imo": None}] if metadata_variant else [own]
            else:
                rows = [other] if query == "9000002" else [own, other]
            return [{"selfReportedInfo": rows}]

        def track(self, vid, start, end):
            requested.append(vid)
            return [TrackPoint(now + timedelta(hours=h), 0, 0 if vid == "own" else 10, 10) for h in range(12)]

    monkeypatch.setattr(cli, "GFWClient", Client)
    path = tmp_path / "report.json"
    assert (
        cli.main(
            [
                "check",
                query_id,
                *(["--also", "9000002"] if manual else []),
                "--start",
                "2025-01-01",
                "--end",
                "2025-01-02",
                "--no-cables",
                "--no-sanctions",
                "--json",
                str(path),
            ]
        )
        == 0
    )
    data = json.loads(path.read_text())
    assert ("other" in requested) == include_track
    codes = {s["code"] for s in data["signals"]}
    assert ("PARALLEL_TRACKS" in codes) == include_track
    if lookup_imo and not manual:
        assert "MMSI_REUSE" in codes
    if manual:
        assert any("linked manually" in note for note in data["notes"])


@pytest.mark.parametrize(
    "field,value",
    [
        ("shipname", 42),
        ("flag", {}),
        ("ssvid", 211000001),
        ("imo", 9000001),
        ("callsign", []),
        ("id", 42),
        ("transmissionDateFrom", 0),
    ],
)
def test_identity_string_fields_reject_wrong_source_types(field, value):
    with pytest.raises(ValueError, match=field):
        identities_from_entries([{"selfReportedInfo": [{field: value}]}])


def test_missing_identity_strings_remain_valid():
    records = identities_from_entries([{"selfReportedInfo": [{"shipname": None, "flag": None}]}])
    assert len(records) == 1 and records[0].name == ""


@pytest.mark.parametrize(
    "body",
    [
        [],
        {"type": "FeatureCollection", "features": {}},
        {"type": "FeatureCollection", "features": [42]},
        {"type": "FeatureCollection", "features": [{"properties": [], "geometry": None}]},
        {"type": "FeatureCollection", "features": [{"geometry": []}]},
        {"type": "FeatureCollection", "features": [{"geometry": {"type": "LineString", "coordinates": [[0], [1, 2]]}}]},
    ],
)
def test_invalid_geojson_shapes_raise_input_error(tmp_path, body):
    path = tmp_path / "routes.geojson"
    path.write_text(json.dumps(body))
    with pytest.raises(ValueError, match="GeoJSON|cable|Cable"):
        CableLayer.from_geojson(path)


def test_geojson_keeps_lines_among_other_features_and_accepts_empty_layer(tmp_path):
    path = tmp_path / "routes.geojson"
    path.write_text(
        json.dumps(
            {
                "type": "FeatureCollection",
                "features": [
                    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [0, 0]}},
                    {
                        "type": "Feature",
                        "properties": {"name": "TEST"},
                        "geometry": {"type": "LineString", "coordinates": [[0, 0, 10], [1, 1, 20]]},
                    },
                ],
            }
        )
    )
    assert CableLayer.from_geojson(path).lines == [("TEST", [(0, 0), (1, 1)])]
    path.write_text('{"type": "FeatureCollection", "features": []}')
    assert CableLayer.from_geojson(path).lines == []


def test_cli_reports_invalid_geojson_without_traceback(tmp_path, capsys):
    path = tmp_path / "routes.geojson"
    path.write_text("[]")
    assert cli.main(["case", "eagle_s", "--cables", str(path)]) == 2
    assert "GeoJSON" in capsys.readouterr().err


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("from_lookup", [False, True])
def test_later_metadata_episode_cannot_hide_an_earlier_track(monkeypatch, tmp_path, reverse, from_lookup):
    old = {
        "shipname": "SHIP",
        "flag": "DEU",
        "ssvid": "211000001",
        "imo": "9000001",
        "id": "same-id",
        "transmissionDateFrom": "2024-01-01T00:00:00Z",
        "transmissionDateTo": "2025-01-03T00:00:00Z",
    }
    later = {**old, "transmissionDateFrom": "2026-01-01T00:00:00Z", "transmissionDateTo": "2026-01-03T00:00:00Z"}
    requested = []

    class Client:
        first = True

        def search_raw(self, query):
            rows = [old] if self.first and from_lookup else [old, later]
            self.first = False
            return [{"selfReportedInfo": list(reversed(rows)) if reverse else rows}]

        def track(self, vid, start, end):
            requested.append(vid)
            return [TrackPoint(datetime(2025, 1, 1, 12, tzinfo=timezone.utc), 0, 0, 2)]

    monkeypatch.setattr(cli, "GFWClient", Client)
    output = tmp_path / "report.json"
    assert (
        cli.main(
            [
                "check",
                "9000001",
                "--start",
                "2025-01-01",
                "--as-of",
                "2025-01-02",
                "--no-cables",
                "--no-sanctions",
                "--json",
                str(output),
            ]
        )
        == 0
    )
    assert requested == ["same-id"]
    assert json.loads(output.read_text())["notes"][0].startswith("1 track points")


def test_identity_without_last_seen_date_still_fetches_its_track(monkeypatch):
    requested = []

    class Client:
        def search_raw(self, query):
            return [
                {
                    "selfReportedInfo": [
                        {
                            "shipname": "SHIP",
                            "imo": "9000001",
                            "id": "still-open",
                            "transmissionDateFrom": "2025-01-01T00:00:00Z",
                        }
                    ]
                }
            ]

        def track(self, vid, start, end):
            requested.append(vid)
            return [TrackPoint(datetime(2025, 1, 1, 12, tzinfo=timezone.utc), 0, 0, 2)]

    monkeypatch.setattr(cli, "GFWClient", Client)
    assert (
        cli.main(
            [
                "check",
                "9000001",
                "--start",
                "2025-01-01",
                "--as-of",
                "2025-01-02",
                "--no-mmsi-lookup",
                "--no-cables",
                "--no-sanctions",
            ]
        )
        == 0
    )
    assert requested == ["still-open"]


def test_all_cases_summary_preserves_score_and_cutoff_interpretation(capsys):
    from shadow_ship_check.report import DISCLAIMER

    assert cli.main(["case", "all", "--no-cables", "--no-sanctions"]) == 0
    text = capsys.readouterr().out
    assert DISCLAIMER in text
    assert "do not reconstruct an advance warning" in text


@pytest.mark.parametrize("status", [401, 403])
def test_live_access_denial_explains_authentication_and_offline_alternative(monkeypatch, capsys, status):
    import urllib.error

    from shadow_ship_check import gfw

    def denied(request, timeout):
        raise urllib.error.HTTPError(request.full_url, status, "Access denied", None, None)

    monkeypatch.setattr(gfw.urllib.request, "urlopen", denied)
    assert cli.main(["check", "9000001"]) == 2
    error = capsys.readouterr().err
    assert f"denied access (HTTP {status})" in error
    assert "GFW_API_TOKEN" in error and "not guaranteed" in error
    assert "ssc case all" in error and "ssc eval" in error
    assert "No vessel found" not in error
