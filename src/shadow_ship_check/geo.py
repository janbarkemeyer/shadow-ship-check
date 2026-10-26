"""Small geometry helpers (no external dependencies)."""

from __future__ import annotations

import json
import math
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


class CableLayer:
    """Cable routes loaded from GeoJSON (LineString / MultiLineString features).

    No cable geometry ships with this project: public cable maps are usually
    not openly licensed. Bring your own file (e.g. digitised from official
    notices) and pass it with ``--cables``.
    """

    def __init__(self, lines: List[Tuple[str, List[Tuple[float, float]]]]):
        self.lines = lines

    @classmethod
    def from_geojson(cls, path: str) -> "CableLayer":
        with open(path, encoding="utf-8") as fh:
            gj = json.load(fh)
        lines = []
        for feat in gj.get("features", []):
            name = (feat.get("properties") or {}).get("name", "cable")
            geom = feat.get("geometry") or {}
            if geom.get("type") == "LineString":
                lines.append((name, [tuple(c[:2]) for c in geom["coordinates"]]))
            elif geom.get("type") == "MultiLineString":
                for part in geom["coordinates"]:
                    lines.append((name, [tuple(c[:2]) for c in part]))
        return cls(lines)

    def nearest(self, lat: float, lon: float) -> Tuple[str, float]:
        best = ("", float("inf"))
        for name, coords in self.lines:
            for a, b in zip(coords, coords[1:]):
                d = point_segment_nm(lat, lon, a, b)
                if d < best[1]:
                    best = (name, d)
        return best


def path_length_nm(points: Iterable) -> float:
    pts = list(points)
    return sum(haversine_nm(p.lat, p.lon, q.lat, q.lon) for p, q in zip(pts, pts[1:]))
