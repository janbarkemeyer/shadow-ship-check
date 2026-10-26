"""Plain data classes used across the package."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional


def normalize_name(name: Optional[str]) -> str:
    """Upper-case, drop "NO." before numbers and all non-alphanumerics:
    "Xing Shun No.39" -> "XINGSHUN39"."""
    n = re.sub(r"NO\.\s*(?=\d)|\bNO\s+(?=\d)", "", (name or "").upper())
    return "".join(ch for ch in n if ch.isalnum())


def parse_ts(value: Optional[str]) -> Optional[datetime]:
    """Parse an ISO timestamp as returned by GFW ("2023-07-22T10:15:56Z", also
    with 1-6 fractional digits). Python 3.10's fromisoformat only accepts 3 or 6."""
    if not value:
        return None
    value = value.replace("Z", "+00:00")
    m = re.match(r"^(.*T\d{2}:\d{2}:\d{2})\.(\d+)(.*)$", value)
    if m:
        value = f"{m.group(1)}.{m.group(2)[:6].ljust(6, '0')}{m.group(3)}"
    return datetime.fromisoformat(value)


@dataclass
class Identity:
    """One AIS / registry identity a hull has used (name + flag + MMSI)."""

    name: str
    flag: Optional[str]
    mmsi: Optional[str]
    imo: Optional[str]
    callsign: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]
    registry_confirmed: bool
    source: str  # "ais" (self reported) or "registry"
    vessel_id: Optional[str] = None
    messages: Optional[int] = None

    @property
    def key(self) -> tuple:
        return (normalize_name(self.name), self.flag or "", self.mmsi or "")

    @property
    def source_label(self) -> str:
        if self.source == "registry":
            return "registry record"
        return "registry + AIS" if self.registry_confirmed else "self-reported AIS only"

    def label(self) -> str:
        span = f"{_d(self.start)} - {_d(self.end)}"
        src = self.source_label
        return f"{self.name or '(no name)'} / {self.flag or '?'} / MMSI {self.mmsi or '?'} ({span}, {src})"


def _d(dt: Optional[datetime]) -> str:
    return dt.strftime("%Y-%m-%d") if dt else "?"


@dataclass
class TrackPoint:
    t: datetime
    lat: float
    lon: float
    speed: float  # knots, as reported by AIS
    segment: int = 0

    @staticmethod
    def from_row(row: list) -> "TrackPoint":
        ts, lat, lon, sp, *rest = row
        return TrackPoint(
            t=datetime.fromtimestamp(ts, tz=timezone.utc),
            lat=lat,
            lon=lon,
            speed=sp,
            segment=rest[0] if rest else 0,
        )


@dataclass
class Signal:
    """A red flag found by one of the checks."""

    code: str
    title: str
    points: int
    evidence: List[str] = field(default_factory=list)
    caveat: Optional[str] = None


@dataclass
class Report:
    query: str
    identities: List[Identity]
    signals: List[Signal]
    window: Optional[tuple] = None
    notes: List[str] = field(default_factory=list)
    incident_time: Optional[datetime] = None
    excerpt: List[tuple] = field(default_factory=list)  # (identity label, TrackPoint)
    as_of: Optional[datetime] = None  # data cut-off for a pre-incident view

    @property
    def score(self) -> int:
        return min(100, sum(s.points for s in self.signals))

    @property
    def level(self) -> str:
        if self.score >= 50:
            return "HIGH"
        if self.score >= 20:
            return "MEDIUM"
        return "LOW"
