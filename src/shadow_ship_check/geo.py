"""Small geometry helpers (no external dependencies)."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Iterable, List, Tuple

EARTH_RADIUS_NM = 3440.065


def haversine_nm(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = math.radians
    dlat = r(lat2 - lat1)
    dlon = r(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(r(lat1)) * math.cos(r(lat2)) * math.sin(dlon / 2) ** 2
    return 2 * EARTH_RADIUS_NM * math.asin(math.sqrt(a))


def point_segment_nm(lat: float, lon: float, a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Distance from a point to a segment a-b (each (lon, lat)), in nautical miles.

    Uses a local equirectangular projection, accurate enough for distances of
    a few dozen nautical miles.
    """
    k = math.cos(math.radians(lat))
    ax, ay = (a[0] - lon) * k, a[1] - lat
    bx, by = (b[0] - lon) * k, b[1] - lat
    dx, dy = bx - ax, by - ay
    seg2 = dx * dx + dy * dy
    t = 0.0 if seg2 == 0 else max(0.0, min(1.0, -(ax * dx + ay * dy) / seg2))
    px, py = ax + t * dx, ay + t * dy
    return math.hypot(px, py) * 60.0  # 1 degree latitude ~ 60 nm


BUNDLED_CABLES = Path(__file__).resolve().parents[2] / "data" / "cables"


class CableLayer:
    """Cable and pipeline routes loaded from GeoJSON (LineString / MultiLineString features).

    The project bundles submarine cables and gas/oil pipelines for the Baltic Sea and
    Taiwan from OpenStreetMap (``data/cables``, ODbL). OSM coverage is incomplete:
    a missing route means "not mapped", not "no cable".
    """

    def __init__(self, lines: List[Tuple[str, List[Tuple[float, float]]]]):
        self.lines = lines
        self._boxes = [
            (min(c[1] for c in cs), max(c[1] for c in cs), min(c[0] for c in cs), max(c[0] for c in cs))
            for _, cs in lines
        ]

    @classmethod
    def from_geojson(cls, *paths) -> "CableLayer":
        """Load one or more GeoJSON files, or every ``*.geojson`` in a directory."""
        files: List[Path] = []
        for p in map(Path, paths):
            files += sorted(p.glob("*.geojson")) if p.is_dir() else [p]
        lines = []
        for f in files:
            gj = json.loads(f.read_text(encoding="utf-8"))
            for feat in gj.get("features", []):
                props = feat.get("properties") or {}
                name = props.get("name") or (
                    f"unnamed {props.get('kind', 'cable')} (OSM way {props['osm_way']})"
                    if props.get("osm_way")
                    else "cable"
                )
                geom = feat.get("geometry") or {}
                parts = [geom["coordinates"]] if geom.get("type") == "LineString" else geom.get("coordinates", [])
                if geom.get("type") in ("LineString", "MultiLineString"):
                    lines += [(name, [tuple(c[:2]) for c in part]) for part in parts if len(part) > 1]
        return cls(lines)

    @classmethod
    def bundled(cls) -> "CableLayer":
        return cls.from_geojson(BUNDLED_CABLES)

    def nearest(self, lat: float, lon: float, within_nm: float = 30.0) -> Tuple[str, float]:
        """Nearest route and its distance; routes further than ``within_nm`` are skipped."""
        dlat = within_nm / 60.0
        dlon = dlat / max(0.05, math.cos(math.radians(lat)))
        best = ("", float("inf"))
        for (name, coords), (la0, la1, lo0, lo1) in zip(self.lines, self._boxes):
            if lat < la0 - dlat or lat > la1 + dlat or lon < lo0 - dlon or lon > lo1 + dlon:
                continue
            for a, b in zip(coords, coords[1:]):
                d = point_segment_nm(lat, lon, a, b)
                if d < best[1]:
                    best = (name, d)
        return best

    def crossed(self, p: Tuple[float, float], q: Tuple[float, float]) -> List[str]:
        """Names of the routes crossed by the straight line p-q (each (lon, lat))."""
        lo0, lo1, la0, la1 = min(p[0], q[0]), max(p[0], q[0]), min(p[1], q[1]), max(p[1], q[1])
        out = []
        for (name, coords), (b0, b1, c0, c1) in zip(self.lines, self._boxes):
            if la1 < b0 or la0 > b1 or lo1 < c0 or lo0 > c1 or name in out:
                continue
            if any(segments_cross(p, q, a, b) for a, b in zip(coords, coords[1:])):
                out.append(name)
        return out


def _orient(a, b, c) -> float:
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def segments_cross(p, q, a, b) -> bool:
    """True if segment p-q properly crosses segment a-b (points as (lon, lat))."""
    return _orient(p, q, a) * _orient(p, q, b) < 0 and _orient(a, b, p) * _orient(a, b, q) < 0


def path_length_nm(points: Iterable) -> float:
    pts = list(points)
    return sum(haversine_nm(p.lat, p.lon, q.lat, q.lon) for p, q in zip(pts, pts[1:]))
