"""Counterexamples for identity linking, incomplete tracks and invalid inputs."""

from dataclasses import replace
from datetime import datetime, timedelta, timezone
from itertools import permutations

import pytest

from shadow_ship_check import evaluate, signals
from shadow_ship_check.analyze import merge_lookup_identities
from shadow_ship_check.geo import CableLayer
from shadow_ship_check.gfw import decode_varints, identities_from_entries, points_from_values
from shadow_ship_check.models import Identity, Report, Signal, TrackPoint, parse_ts
from shadow_ship_check.report import to_markdown, to_text

T = datetime(2025, 1, 1, tzinfo=timezone.utc)


def identity(**kwargs):
    base = Identity("SHIP", "DEU", "211000001", "9000001", None, T, T + timedelta(days=10), False, "ais")
    return replace(base, **kwargs)


def point(hours, lon=0, speed=2, segment=0):
    return TrackPoint(T + timedelta(hours=hours), 0, lon, speed, segment)


def test_registry_selection_is_independent_of_input_order():
    old = identity(name="OLD", start=T - timedelta(days=100), end=T, registry_confirmed=True)
    new = identity(name="NEW", start=T - timedelta(days=5), end=T)
    for order in permutations([old, new]):
        assert signals.active_at(order, T).name == "NEW"
        assert [(s.code, s.points) for s in signals.registry_confirmation(order, T)] == [("REGISTRY_LOST", 15)]


def test_foreign_imo_cannot_extend_or_confirm_hull_identity():
    own = identity()
    foreign = identity(imo="9000002", end=T + timedelta(days=100), registry_confirmed=True)
    result = merge_lookup_identities([own], {own.mmsi: [foreign]})
    assert len(result) == 1
    assert result[0] == own


def test_foreign_imo_registry_match_is_not_confirmation():
    entries = [
        {
            "selfReportedInfo": [{"shipname": "SHIP", "ssvid": "211000001", "imo": "9000001"}],
            "registryInfo": [{"shipname": "SHIP", "ssvid": "211000001", "imo": "9000002"}],
        }
    ]
    ais = next(i for i in identities_from_entries(entries) if i.source == "ais")
    assert not ais.registry_confirmed


def test_registry_imo_is_retained_when_same_named_ais_record_omits_it():
    entries = [
        {
            "selfReportedInfo": [{"shipname": "SHIP", "flag": "DEU", "ssvid": "211000001"}],
            "registryInfo": [{"shipname": "SHIP", "flag": "DEU", "ssvid": "211000001", "imo": "9000001"}],
        }
    ]
    records = identities_from_entries(entries)
    assert any(i.imo == "9000001" and i.source == "registry" for i in records)
    assert any(i.imo is None and i.source == "ais" for i in records)


def test_flattening_preserves_conflicting_hulls_and_disjoint_periods():
    from shadow_ship_check.gfw import _merge

    rows = [identity(), identity(imo="9000002"), identity(start=T + timedelta(days=30), end=T + timedelta(days=40))]
    for order in permutations(rows):
        merged = {}
        for i in order:
            _merge(merged, replace(i))
        assert len(merged) == 3
        assert {i.imo for i in merged.values()} == {"9000001", "9000002"}


def test_overlapping_fragments_merge_transitively_in_any_order():
    from shadow_ship_check.gfw import _merge

    rows = [
        identity(end=T + timedelta(days=2)),
        identity(start=T + timedelta(days=1), end=T + timedelta(days=4)),
        identity(start=T + timedelta(days=3), end=T + timedelta(days=5)),
    ]
    for order in permutations(rows):
        merged = {}
        for i in order:
            _merge(merged, replace(i))
        assert len(merged) == 1
        record = next(iter(merged.values()))
        assert (record.start, record.end) == (T, T + timedelta(days=5))


def test_imo_less_later_episode_is_kept_without_bridging_the_gap():
    own = identity(end=T + timedelta(days=2))
    later = identity(imo=None, start=T + timedelta(days=4), end=T + timedelta(days=40))
    result = merge_lookup_identities([own], {own.mmsi: [later]})
    assert len(result) == 2
    assert result[0].end == own.end
    assert result[1].start == later.start


def test_merging_a_bridge_cannot_overwrite_a_later_episode():
    from shadow_ship_check.gfw import _merge

    rows = [
        identity(end=T + timedelta(days=2)),
        identity(start=T + timedelta(days=3), end=T + timedelta(days=5)),
        identity(start=T + timedelta(days=10), end=T + timedelta(days=12)),
        identity(start=T + timedelta(days=1), end=T + timedelta(days=4)),
        identity(start=T + timedelta(days=20), end=T + timedelta(days=22)),
    ]
    merged = {}
    for i in rows:
        _merge(merged, replace(i))
    assert len(merged) == 3
    assert sorted(i.end for i in merged.values()) == [T + timedelta(days=d) for d in (5, 12, 22)]


def test_search_follows_pagination_and_rejects_silent_truncation(monkeypatch):
    import json

    from shadow_ship_check.gfw import GFWClient

    client = GFWClient()
    calls = []

    def get(path, params):
        offset = dict(params)["offset"]
        calls.append(offset)
        return json.dumps({"entries": [{"id": offset}], "total": 2, "nextOffset": offset + 1}).encode()

    monkeypatch.setattr(client, "_get", get)
    assert client.search_raw("SHIP") == [{"id": 0}, {"id": 1}]
    assert calls == [0, 1]
    monkeypatch.setattr(client, "_get", lambda *a: b'{"entries": [{}], "total": 2}')
    with pytest.raises(ValueError, match="incomplete"):
        client.search_raw("SHIP")


def test_reused_mmsi_is_not_silently_treated_as_one_hull():
    from shadow_ship_check.gfw import hull_identities

    rows = [{"shipname": "SHIP", "ssvid": "211000001", "imo": imo} for imo in ("9000001", "9000002")]
    with pytest.raises(ValueError, match="multiple IMO"):
        hull_identities([{"selfReportedInfo": rows}], "211000001")


def test_case_all_does_not_silently_ignore_json_output(tmp_path, capsys):
    from shadow_ship_check.cli import main

    output = tmp_path / "all.json"
    assert main(["case", "all", "--json", str(output)]) == 2
    assert not output.exists()
    assert "one case" in capsys.readouterr().err


def test_matching_labels_do_not_join_different_live_track_ids(monkeypatch, tmp_path):
    import json

    from shadow_ship_check import cli

    rows = [
        {
            "shipname": "SHIP",
            "flag": "DEU",
            "ssvid": "211000001",
            "imo": "9000001",
            "id": str(n),
            "transmissionDateFrom": "2025-01-01T00:00:00Z",
            "transmissionDateTo": "2025-01-02T00:00:00Z",
        }
        for n in range(2)
    ]

    class Client:
        def search_raw(self, query):
            return [{"selfReportedInfo": rows}]

        def track(self, vid, start, end):
            return [point(int(vid) * 2, int(vid) * 0.04)]

    monkeypatch.setattr(cli, "GFWClient", Client)
    output = tmp_path / "report.json"
    assert (
        cli.main(
            [
                "check",
                "9000001",
                "--start",
                "2025-01-01",
                "--end",
                "2025-01-02",
                "--no-mmsi-lookup",
                "--no-cables",
                "--no-sanctions",
                "--json",
                str(output),
            ]
        )
        == 0
    )
    report = json.loads(output.read_text())
    assert not any(s["code"] == "SLOW_LOITERING" for s in report["signals"])
    assert "2 identity track(s)" in report["notes"][0]


def test_explicit_window_is_not_silently_replaced_at_cutoff():
    from shadow_ship_check.analyze import analyze

    with pytest.raises(ValueError, match="window"):
        analyze("q", [], [], window=(T, T + timedelta(days=1)), as_of=T)


def test_json_and_markdown_preserve_custom_excerpt_window():
    import json

    from shadow_ship_check.analyze import analyze
    from shadow_ship_check.report import to_json

    report = analyze("q", [], [point(0)], incident_time=T, excerpt_hours=1)
    assert "+/- 1 h" in to_markdown(report)
    data = json.loads(to_json(report))
    assert data["incident_time"] == T.isoformat()
    assert data["excerpt_hours"] == 1
    assert len(data["excerpt"]) == 1


def test_parallel_detection_matches_exhaustive_pairs():
    import random

    from shadow_ship_check.geo import haversine_nm

    rnd = random.Random(20261027)
    for _ in range(100):
        a = sorted([point(rnd.uniform(0, 5), rnd.uniform(0, 4)) for _ in range(7)], key=lambda p: p.t)
        b = sorted([point(rnd.uniform(0, 5), rnd.uniform(0, 4)) for _ in range(19)], key=lambda p: p.t)
        expected = any(
            abs(p.t - q.t) <= timedelta(hours=1) and haversine_nm(p.lat, p.lon, q.lat, q.lon) >= 100
            for p in a
            for q in b
        )
        assert bool(signals.parallel_tracks({"a": a, "b": b})) == expected


def test_unrelated_name_lookup_does_not_imply_own_mmsi_reuse():
    own = identity()
    other = identity(name="OTHER", mmsi="211000002", imo="9000002")
    assert not signals.mmsi_reuse([own], {other.mmsi: [other]})


def test_known_foreign_imo_with_same_name_can_reuse_mmsi():
    own = identity()
    other = identity(imo="9000002")
    assert signals.mmsi_reuse([own], {own.mmsi: [other]})[0].points == 15


def test_unknown_flags_do_not_establish_name_and_flag_match():
    own = identity(flag=None)
    other = identity(flag=None, mmsi="211000002", imo=None)
    assert not signals.name_on_other_mmsi([own], {other.mmsi: [other]})


def test_missing_imo_requires_matching_period_and_flag():
    own = identity()
    old = identity(imo=None, start=T - timedelta(days=100), end=T - timedelta(days=90))
    foreign_flag = identity(imo=None, flag="GBR")
    assert not signals.imo_hidden([own], {own.mmsi: [old, foreign_flag]})
    assert signals.imo_hidden([own], {own.mmsi: [identity(imo=None)]})


@pytest.mark.parametrize(
    "points",
    [
        [point(0), point(48, 1)],
        [point(0), point(1, 0.02), point(2, 0.04, segment=1), point(3, 0.06, segment=1)],
    ],
)
def test_slow_movement_does_not_bridge_missing_periods(points):
    assert not signals.slow_movement(points)


def test_speed_drop_does_not_bridge_missing_periods():
    cruise = [point(-n, speed=12) for n in range(1, 6)]
    assert not signals.speed_drop([point(0, speed=4), point(48, 4, speed=4)], reference=cruise)


def test_zigzag_does_not_join_disconnected_segments():
    pts = [point(0), point(1, 0.05), point(2, 0.1, segment=1), point(3, 0, segment=1)]
    assert not signals.zigzag(pts)


def test_cable_crossing_requires_a_connected_track_segment():
    layer = CableLayer([("test", [(0, -1), (0, 1)])])
    assert not signals.cable_crossings([point(0, -0.02), point(1, 0.02, segment=1)], layer)
    assert signals.cable_crossings([point(0, -0.02), point(1, 0.02)], layer)


def test_inserting_a_cable_vertex_keeps_a_crossing_but_touching_does_not():
    p, q = (-0.02, 0), (0.02, 0)
    straight = CableLayer([("test", [(0, -1), (0, 1)])])
    split = CableLayer([("test", [(0, -1), (0, 0), (0, 1)])])
    touch = CableLayer([("test", [(-0.01, 1), (0, 0), (0.01, 1)])])
    assert straight.crossed(p, q) == split.crossed(p, q) == ["test"]
    assert not touch.crossed(p, q)


def test_date_line_is_rejected_instead_of_using_a_false_planar_crossing():
    layer = CableLayer([("test", [(0, -1), (0, 1)])])
    with pytest.raises(ValueError, match="date line"):
        layer.crossed((179, 0), (-179, 0))


def test_invalid_cable_coordinates_are_rejected():
    with pytest.raises(ValueError, match="coordinates"):
        CableLayer([("test", [(0, 0), (0, float("nan"))])])


def test_parallel_tracks_checks_entire_time_tolerance():
    other = [point(-0.9, 3), point(-0.8), point(-0.7), point(-0.6), point(-0.5), point(0.1)]
    assert signals.parallel_tracks({"a": [point(0)], "b": other})


@pytest.mark.parametrize("buf", [b"\x0a\x02\x80", b"\x0a\x03\x02", b"\x0a\x01\x80", b"\x0b"])
def test_truncated_or_unsupported_protobuf_fails_explicitly(buf):
    with pytest.raises(ValueError):
        decode_varints(buf)


def test_unknown_protobuf_field_is_not_track_values():
    assert decode_varints(b"\x12\x01\x02") == []


def test_unknown_track_schema_is_not_reported_as_no_ais_positions():
    from shadow_ship_check.gfw import decode_value_array

    assert decode_value_array(b"\x0a\x00") == []
    with pytest.raises(ValueError, match="recognised"):
        decode_value_array(b"\x12\x01\x02")


@pytest.mark.parametrize(
    "values", [[-2147483648, 2, 0], [0, 0], [-2147483648, -1], [-2147483648, 1, -1], [-2147483648, 1, 0, 1]]
)
def test_bad_track_layout_fails_explicitly(values):
    with pytest.raises(ValueError):
        points_from_values(values)


@pytest.mark.parametrize("lat,lon,speed", [(91, 0, 2), (0, 181, 2), (float("nan"), 0, 2), (0, 0, -1), (0, 0, 102.3)])
def test_unusable_track_values_are_not_scored(lat, lon, speed):
    with pytest.raises(ValueError):
        TrackPoint.from_row([int(T.timestamp()), lat, lon, speed])


def test_timestamp_without_zone_is_utc():
    assert parse_ts("2025-01-01T00:00:00") == T


def test_non_numeric_mmsi_does_not_establish_a_country():
    from shadow_ship_check.registries import flag_from_mmsi

    assert flag_from_mmsi("211ABCDEF") is None


def test_undated_identity_does_not_establish_recent_use():
    rows = [identity(name="A", start=None, end=None), identity(name="B", start=None, end=None)]
    assert all(s.points == 0 for s in signals.multiple_identities(rows, T))


def test_imo_metadata_variants_are_not_concurrent_ais_identities():
    own = identity(end=T + timedelta(days=50))
    assert not signals.concurrent_identities([own, replace(own, imo=None)], T + timedelta(days=40))


def test_metadata_variants_do_not_multiply_a_concurrent_pair():
    own = identity(end=T + timedelta(days=50))
    other = replace(own, mmsi="211000002")
    result = signals.concurrent_identities([own, replace(own, imo=None), other], T + timedelta(days=40))
    assert result[0].points == 5


def test_metadata_variants_do_not_multiply_mmsi_mismatch():
    own = identity(flag="FRA")
    assert signals.mmsi_flag_mismatch([own, replace(own, imo=None)])[0].points == 10


def test_metadata_variants_do_not_multiply_same_dated_flag_transition():
    previous = identity(flag="GBR", start=T - timedelta(days=100), end=T)
    current = identity(flag="CMR", end=T + timedelta(days=100))
    result = signals.flag_changes([previous, current, replace(current, imo=None)], T + timedelta(days=10))
    assert result[0].points == 15


def test_cutoff_does_not_invent_an_earlier_observation_for_unknown_start():
    from shadow_ship_check.analyze import clip_identities

    row = identity(start=None, end=T + timedelta(days=10))
    clipped = clip_identities([row], T)[0]
    assert clipped.start is None and clipped.end is None


def test_terminal_keeps_missing_data_notes_and_signal_caveats():
    report = Report("q", [], [Signal("AIS_GAP", "gap", 15, [], "Incomplete coverage")], notes=["No positions"])
    text = to_text(report)
    assert "No positions" in text
    assert "Incomplete coverage" in text


def test_external_names_cannot_break_markdown_table_or_inject_html():
    report = Report("q", [identity(name="A|B\n<img src=x>")], [])
    md = to_markdown(report)
    assert "<img src=x>" not in md
    assert "A\\|B<br>&lt;img src=x&gt;" in md


def test_auc_rejects_missing_comparison_group():
    with pytest.raises(ValueError, match="both groups"):
        evaluate.auc([], [1])


def test_evaluation_rejects_unknown_labels():
    with pytest.raises(ValueError, match="label"):
        evaluate.evaluate({"records": [{"label": "typo", "imo": "1", "identities": []}]})


def test_evaluation_rejects_duplicate_hulls_before_scoring():
    record = {"label": "sanctioned", "imo": "1", "identities": []}
    with pytest.raises(ValueError, match="Duplicate IMO"):
        evaluate.evaluate({"records": [record, {**record, "label": "control"}]})
