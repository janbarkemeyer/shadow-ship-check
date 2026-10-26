import json
from datetime import datetime, timedelta, timezone

from shadow_ship_check.geo import CableLayer, haversine_nm, point_segment_nm
from shadow_ship_check.models import TrackPoint
from shadow_ship_check.registries import flag_from_mmsi, is_foc
from shadow_ship_check.signals import cable_crossings, slow_movement, zigzag


def test_haversine_one_degree_latitude():
    assert abs(haversine_nm(0, 0, 1, 0) - 60.04) < 0.1


def test_point_segment_distance():
    # point 0.1 deg north of an east-west segment at the equator -> ~6 nm
    assert abs(point_segment_nm(0.1, 0.5, (0, 0), (1, 0)) - 6.0) < 0.05


def test_registries():
    assert is_foc("COK") and is_foc("TGO") and is_foc("tza")
    assert not is_foc("CHN") and not is_foc(None)
    assert flag_from_mmsi("518998865") == "COK"
    assert flag_from_mmsi("677087200") == "TZA"
    assert flag_from_mmsi("123") is None


def _pts(coords, start=datetime(2025, 1, 1, tzinfo=timezone.utc), step_min=30, speed=1.0):
    return [TrackPoint(start + timedelta(minutes=step_min * i), lat, lon, speed) for i, (lat, lon) in enumerate(coords)]


def _layer(tmp_path):
    gj = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "TEST-1"},
                "geometry": {"type": "LineString", "coordinates": [[121.0, 25.0], [122.0, 25.0]]},
            }
        ],
    }
    path = tmp_path / "cables.geojson"
    path.write_text(json.dumps(gj))
    return CableLayer.from_geojson(path)


def test_cable_crossing_slow(tmp_path):
    layer = _layer(tmp_path)
    # 0.1 deg (6 nm) per hour across the cable: 6 kn, against a cruising speed of 12 kn
    cruising = _pts([(24.0, 121.5 + 0.01 * i) for i in range(6)], step_min=60, speed=12.0)
    slow = _pts([(24.95, 121.5), (25.05, 121.5)], start=datetime(2025, 1, 2, tzinfo=timezone.utc), step_min=60)
    sigs = cable_crossings(slow, layer, reference=cruising + slow)
    assert sigs and sigs[0].code == "CABLE_CROSSING_SLOW" and "TEST-1" in sigs[0].evidence[0]


def test_cable_crossing_at_cruising_speed_is_ignored(tmp_path):
    layer = _layer(tmp_path)
    fast = _pts([(24.9, 121.5), (25.1, 121.5)], step_min=60, speed=12.0)  # 12 kn
    assert cable_crossings(fast, layer, reference=fast * 3) == []


def test_bundled_cables_load():
    layer = CableLayer.bundled()
    names = {n for n, _ in layer.lines}
    assert {"C-Lion 1", "BCS East-West Interlink", "Baltic Connector", "HVDC Estlink 2"} <= names


def test_zigzag_and_slow():
    back_and_forth = [
        (25.0, 121.0),
        (25.05, 121.0),
        (25.0, 121.0),
        (25.05, 121.0),
        (25.0, 121.0),
        (25.05, 121.0),
        (25.0, 121.0),
    ]
    pts = _pts(back_and_forth, step_min=60, speed=2.0)  # ~3 kn average
    assert zigzag(pts)[0].code == "ZIGZAG"
    slow = slow_movement(pts)
    assert slow and "slow moving" in slow[0].evidence[0] and slow[0].points == 10
    ferry = _pts(back_and_forth, step_min=15, speed=2.0)  # same shape at ~12 kn: a shuttle, not loitering
    assert zigzag(ferry) == []
