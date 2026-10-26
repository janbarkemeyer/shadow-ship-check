"""Minimal client for the Global Fishing Watch (GFW) API.

* Vessel search uses the public v3 endpoint ``/vessels/search``.
* Tracks use ``/vessels/{id}/tracks`` in the compact binary ``VALUE_ARRAY``
  format - the same request the GFW map makes in the browser. Without a token
  GFW serves a simplified track (roughly one point every 60-90 minutes on open
  water, denser near the coast). With a token (``GFW_API_TOKEN``, free for
  non-commercial use at https://globalfishingwatch.org/our-apis/) more data
  may be available.

The track endpoint is not part of GFW's documented public API and may change.
Data licence: CC BY-NC 4.0 - credit Global Fishing Watch, no commercial use
without an agreement with GFW.
"""

from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request
from dataclasses import replace
from datetime import datetime, timezone
from typing import Iterable, List, Optional

from .models import Identity, TrackPoint, normalize_name, parse_ts

BASE_URL = "https://gateway.api.globalfishingwatch.org/v3"
IDENTITY_DATASET = "public-global-vessel-identity:v5.0"
TRACK_DATASET = "public-global-all-tracks:v4.0"
USER_AGENT = "shadow-ship-check/0.1"
_EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


class GFWClient:
    def __init__(self, token: Optional[str] = None, base_url: str = BASE_URL, timeout: int = 60):
        self.token = token if token is not None else os.environ.get("GFW_API_TOKEN")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    # -- HTTP ---------------------------------------------------------------
    def _get(self, path: str, params: Iterable[tuple]) -> bytes:
        url = f"{self.base_url}{path}?{urllib.parse.urlencode(list(params))}"
        headers = {"User-Agent": USER_AGENT}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return resp.read()

    # -- Search -------------------------------------------------------------
    def search_raw(self, query: str) -> list:
        body = self._get(
            "/vessels/search",
            [("query", query), ("datasets[0]", IDENTITY_DATASET)],
        )
        return json.loads(body).get("entries", [])

    def search(self, query: str) -> List[Identity]:
        return identities_from_entries(self.search_raw(query))

    # -- Tracks -------------------------------------------------------------
    def track(self, vessel_id: str, start: datetime, end: datetime) -> List[TrackPoint]:
        body = self._get(
            f"/vessels/{vessel_id}/tracks",
            [
                ("dataset", TRACK_DATASET),
                ("fields[0]", "LONLAT"),
                ("fields[1]", "TIMESTAMP"),
                ("fields[2]", "SPEED"),
                ("format", "VALUE_ARRAY"),
                ("binary", "true"),
                ("start-date", start.strftime("%Y-%m-%dT%H:%M:%S.000Z")),
                ("end-date", end.strftime("%Y-%m-%dT%H:%M:%S.000Z")),
            ],
        )
        return decode_value_array(body)


# ---------------------------------------------------------------------------
# Parsing helpers (pure functions, unit tested)
# ---------------------------------------------------------------------------
def identities_from_entries(entries: list, dedupe: bool = True) -> List[Identity]:
    """Flatten GFW search entries into a de-duplicated list of identities.

    An AIS identity counts as *registry confirmed* when the same GFW entry
    also carries a registry record with the same MMSI.
    """
    out: dict = {}
    raw: List[Identity] = []
    for entry in entries:
        registry = entry.get("registryInfo") or []
        reg_mmsis = {r.get("ssvid") for r in registry}
        for s in entry.get("selfReportedInfo") or []:
            ident = Identity(
                name=(s.get("shipname") or "").strip(),
                flag=s.get("flag") or None,
                mmsi=s.get("ssvid") or None,
                imo=s.get("imo") or None,
                callsign=s.get("callsign") or None,
                start=parse_ts(s.get("transmissionDateFrom")),
                end=parse_ts(s.get("transmissionDateTo")),
                registry_confirmed=s.get("ssvid") in reg_mmsis,
                source="ais",
                vessel_id=s.get("id"),
                messages=s.get("messagesCounter"),
            )
            raw.append(ident)
            _merge(out, replace(ident))
        for r in registry:
            ident = Identity(
                name=(r.get("shipname") or "").strip(),
                flag=r.get("flag") or None,
                mmsi=r.get("ssvid") or None,
                imo=r.get("imo") or None,
                callsign=r.get("callsign") or None,
                start=parse_ts(r.get("transmissionDateFrom")),
                end=parse_ts(r.get("transmissionDateTo")),
                registry_confirmed=True,
                source="registry",
            )
            # Registry records whose MMSI is already covered by an AIS identity
            # only confirm it (their flag field is sometimes the owner's or a
            # second register's). Registry-only identities are kept.
            ais_keys = {(_norm(s.get("shipname")), s.get("ssvid")) for s in entry.get("selfReportedInfo") or []}
            if (_norm(r.get("shipname")), r.get("ssvid")) in ais_keys:
                continue
            if ident.key not in out:
                raw.append(ident)
                _merge(out, replace(ident))
    if not dedupe:
        return sorted(raw, key=lambda i: i.start or _EPOCH)
    return sorted(out.values(), key=lambda i: i.start or _EPOCH)


def _norm(name) -> str:
    return normalize_name(name)


def _merge(out: dict, ident: Identity) -> None:
    prev = out.get(ident.key)
    if prev is None:
        out[ident.key] = ident
        return
    # same name/flag/MMSI split over several GFW ids -> widen the time span
    if ident.start and (not prev.start or ident.start < prev.start):
        prev.start = ident.start
    if ident.end and (not prev.end or ident.end > prev.end):
        prev.end = ident.end
    prev.registry_confirmed = prev.registry_confirmed or ident.registry_confirmed
    prev.imo = prev.imo or ident.imo
    prev.messages = (prev.messages or 0) + (ident.messages or 0)


def _zigzag(n: int) -> int:
    return (n >> 1) ^ -(n & 1)


def decode_varints(buf: bytes) -> List[int]:
    """Decode a protobuf message holding packed sint32 values (field 1)."""
    vals: List[int] = []
    i = 0

    def varint() -> int:
        nonlocal i
        result = shift = 0
        while True:
            b = buf[i]
            i += 1
            result |= (b & 0x7F) << shift
            shift += 7
            if not b & 0x80:
                return result

    while i < len(buf):
        key = varint()
        wire = key & 7
        if wire == 2:
            length = varint()
            end = i + length
            while i < end:
                vals.append(_zigzag(varint()))
        elif wire == 0:
            varint()
        else:  # unexpected wire type - stop rather than mis-parse
            break
    return vals


def decode_value_array(buf: bytes) -> List[TrackPoint]:
    """Turn GFW's binary VALUE_ARRAY track into TrackPoints.

    Layout (fields LONLAT, TIMESTAMP, SPEED): ``[sentinel, n_segments,
    offset_1..offset_n, lon*1e6, lat*1e6, unix_ts, speed*1e6, ...]`` where the
    offsets are indices into the value list that start each segment.
    """
    vals = decode_varints(buf)
    return points_from_values(vals)


def points_from_values(vals: List[int]) -> List[TrackPoint]:
    if len(vals) < 2:
        return []
    n = vals[1]
    offsets = vals[2 : 2 + n]
    data = vals[2 + n :]
    pts: List[TrackPoint] = []
    for s in range(n):
        a = offsets[s]
        b = offsets[s + 1] if s + 1 < n else len(data)
        for i in range(a, b - 3, 4):
            pts.append(
                TrackPoint(
                    t=datetime.fromtimestamp(data[i + 2], tz=timezone.utc),
                    lat=data[i + 1] / 1e6,
                    lon=data[i] / 1e6,
                    speed=data[i + 3] / 1e6,
                    segment=s,
                )
            )
    pts.sort(key=lambda p: p.t)
    return pts
