"""Minimal client for the Global Fishing Watch (GFW) API.

* Vessel search uses the public v3 endpoint ``/vessels/search``.
* Tracks use ``/vessels/{id}/tracks`` in the compact binary ``VALUE_ARRAY``
  format used by the GFW map. The bundled snapshots were collected without a
  token and contain simplified tracks. The client supports ``GFW_API_TOKEN``,
  but neither anonymous access nor higher resolution with a token is guaranteed.
  Documented API access: https://globalfishingwatch.org/our-apis/.

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

from . import __version__
from .models import Identity, TrackPoint, normalize_name, parse_ts

BASE_URL = "https://gateway.api.globalfishingwatch.org/v3"
IDENTITY_DATASET = "public-global-vessel-identity:v5.0"
TRACK_DATASET = "public-global-all-tracks:v4.0"
USER_AGENT = f"shadow-ship-check/{__version__}"
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
        entries, offset = [], 0
        while True:
            body = self._get(
                "/vessels/search",
                [("query", query), ("datasets[0]", IDENTITY_DATASET), ("limit", 50), ("offset", offset)],
            )
            page = json.loads(body)
            if not isinstance(page, dict) or not isinstance(page.get("entries"), list):
                raise ValueError("Invalid vessel search response: missing entries")
            entries.extend(page["entries"])
            following = page.get("nextOffset")
            if following is None:
                if page.get("total", len(entries)) > len(entries):
                    raise ValueError("Vessel search response is incomplete: no nextOffset")
                return entries
            if page.get("total") is not None and len(entries) >= page["total"]:
                return entries
            if type(following) is not int or following <= offset or not page["entries"]:
                raise ValueError("Invalid vessel search pagination")
            offset = following

    def search(self, query: str) -> List[Identity]:
        return identities_from_entries(self.search_raw(query))

    # -- Tracks -------------------------------------------------------------
    def track(self, vessel_id: str, start: datetime, end: datetime) -> List[TrackPoint]:
        body = self._get(
            f"/vessels/{urllib.parse.quote(vessel_id, safe='')}/tracks",
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
    also carries a registry record with the same non-empty MMSI and no conflicting known IMO.
    """
    out: dict = {}
    raw: List[Identity] = []
    if not isinstance(entries, list):
        raise ValueError("Vessel search entries must be a list")
    for entry in entries:
        if not isinstance(entry, dict):
            raise ValueError("Vessel search entries must be objects")
        if not any(field in entry for field in ("registryInfo", "selfReportedInfo")):
            raise ValueError("Vessel search entry has no recognised identity fields")
        for field in ("registryInfo", "selfReportedInfo"):
            rows = entry.get(field) if entry.get(field) is not None else []
            if not isinstance(rows, list) or any(not isinstance(r, dict) for r in rows):
                raise ValueError(f"Invalid vessel identity field {field}")
            for row in rows:
                for name in (
                    "shipname",
                    "flag",
                    "ssvid",
                    "imo",
                    "callsign",
                    "id",
                    "transmissionDateFrom",
                    "transmissionDateTo",
                ):
                    if row.get(name) is not None and not isinstance(row[name], str):
                        raise ValueError(f"Vessel identity field {name} must be a string or null")
        registry = entry.get("registryInfo") or []
        for s in entry.get("selfReportedInfo") or []:
            ident = Identity(
                name=(s.get("shipname") or "").strip(),
                flag=s.get("flag") or None,
                mmsi=s.get("ssvid") or None,
                imo=s.get("imo") or None,
                callsign=s.get("callsign") or None,
                start=parse_ts(s.get("transmissionDateFrom")),
                end=parse_ts(s.get("transmissionDateTo")),
                registry_confirmed=bool(s.get("ssvid"))
                and any(
                    r.get("ssvid") == s["ssvid"] and not (s.get("imo") and r.get("imo") and s["imo"] != r["imo"])
                    for r in registry
                ),
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
            if any(
                (_norm(s.get("shipname")), s.get("ssvid")) == (_norm(r.get("shipname")), r.get("ssvid"))
                and (not r.get("imo") or s.get("imo") == r["imo"])
                for s in entry.get("selfReportedInfo") or []
            ):
                continue
            raw.append(ident)
            _merge(out, replace(ident))
    if not dedupe:
        return sorted(raw, key=lambda i: i.start or _EPOCH)
    return sorted(out.values(), key=lambda i: i.start or _EPOCH)


def hull_identities(entries: list, query: str, dedupe: bool = True) -> List[Identity]:
    """Identities of the hull behind an IMO/MMSI query (search results are fuzzy).

    Selection works per GFW entry. An entry with a hull IMO keeps its rows without an IMO, because
    GFW groups a hull's earlier names in the same entry; rows with another IMO are dropped. An entry
    that matches the query but carries only other IMOs belongs to another ship: only its IMO-less
    rows with the queried MMSI stay (MMSI reuse), and its registry rows cannot confirm them.
    """
    identities_from_entries(entries, dedupe=False)  # validate every entry, kept or not
    q = (query or "").strip()

    def rows(entry):
        return [*(entry.get("selfReportedInfo") or []), *(entry.get("registryInfo") or [])]

    matched = [e for e in entries if any(q in (r.get("imo"), r.get("ssvid")) for r in rows(e))]
    imos = {r.get("imo") for e in matched for r in rows(e) if r.get("imo") and q in (r.get("imo"), r.get("ssvid"))}
    if len(imos) > 1:
        raise ValueError(
            f"This identifier matches multiple IMO numbers: {', '.join(sorted(imos))}; check each IMO separately"
        )
    kept = []
    for entry in entries:
        entry_imos = {r.get("imo") for r in rows(entry) if r.get("imo")}
        if entry_imos & imos:

            def keep(r):
                return not r.get("imo") or r.get("imo") in imos
        elif any(entry is m for m in matched) and not entry_imos:

            def keep(r):
                return True
        elif any(entry is m for m in matched):

            def keep(r):
                return not r.get("imo") and r.get("ssvid") == q
        else:
            continue
        foreign_entry = not entry_imos & imos and bool(entry_imos)
        kept.append(
            {
                **entry,
                "selfReportedInfo": [r for r in entry.get("selfReportedInfo") or [] if keep(r)],
                # another ship's registry rows never confirm the rows kept from its entry
                "registryInfo": [] if foreign_entry else [r for r in entry.get("registryInfo") or [] if keep(r)],
            }
        )
    return [i for i in identities_from_entries(kept, dedupe=dedupe) if not i.imo or i.imo in imos]


def _norm(name) -> str:
    return normalize_name(name)


def _merge(out: dict, ident: Identity) -> None:
    # Preserve conflicting IMO claims and separate episodes. First/last dates
    # still describe an envelope within an episode, not continuous use.
    matches = []
    for key, prev in out.items():
        if prev.key != ident.key or prev.imo != ident.imo:
            continue
        dates = (prev.start, prev.end, ident.start, ident.end)
        if all(dates):
            overlap = prev.start <= ident.end and ident.start <= prev.end
        else:
            overlap = (prev.start, prev.end) == (ident.start, ident.end)
        if overlap:
            matches.append(key)
    if not matches:
        out[(ident.key, ident.imo, ident.start, ident.end)] = ident
        return
    prev = out[matches[0]]
    for key in matches[1:]:
        other = out.pop(key)
        if other.start and (not prev.start or other.start < prev.start):
            prev.start = other.start
        if other.end and (not prev.end or other.end > prev.end):
            prev.end = other.end
        prev.registry_confirmed |= other.registry_confirmed
        prev.messages = (prev.messages or 0) + (other.messages or 0)
        prev.source = "ais" if "ais" in (prev.source, other.source) else "registry"
    # same name/flag/MMSI split over several GFW ids -> widen the time span
    if ident.start and (not prev.start or ident.start < prev.start):
        prev.start = ident.start
    if ident.end and (not prev.end or ident.end > prev.end):
        prev.end = ident.end
    prev.registry_confirmed = prev.registry_confirmed or ident.registry_confirmed
    prev.source = "ais" if "ais" in (prev.source, ident.source) else "registry"
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
        while shift < 70:
            if i >= len(buf):
                raise ValueError("Truncated protobuf varint")
            b = buf[i]
            i += 1
            result |= (b & 0x7F) << shift
            shift += 7
            if not b & 0x80:
                return result
        raise ValueError("Protobuf varint exceeds 64 bits")

    while i < len(buf):
        key = varint()
        field = key >> 3
        if not field:
            raise ValueError("Invalid protobuf field number")
        wire = key & 7
        if wire == 2:
            length = varint()
            end = i + length
            if end > len(buf):
                raise ValueError("Truncated protobuf field")
            if field == 1:
                while i < end:
                    value = varint()
                    if i > end or value > 0xFFFFFFFF:
                        raise ValueError("Invalid packed sint32 value")
                    vals.append(_zigzag(value))
            else:
                i = end
        elif wire == 0:
            varint()
        elif wire in (1, 5):
            i += 8 if wire == 1 else 4
            if i > len(buf):
                raise ValueError("Truncated protobuf field")
        else:
            raise ValueError(f"Unsupported protobuf wire type {wire}")
    return vals


def decode_value_array(buf: bytes) -> List[TrackPoint]:
    """Turn GFW's binary VALUE_ARRAY track into TrackPoints.

    Layout (fields LONLAT, TIMESTAMP, SPEED): ``[sentinel, n_segments,
    offset_1..offset_n, lon*1e6, lat*1e6, unix_ts, speed*1e6, ...]`` where the
    offsets are indices into the value list that start each segment.
    """
    vals = decode_varints(buf)
    if buf and not vals and buf != b"\x0a\x00":
        raise ValueError("Non-empty track response contains no recognised value field")
    return points_from_values(vals)


def points_from_values(vals: List[int]) -> List[TrackPoint]:
    if not vals:
        return []
    if len(vals) < 2 or vals[0] != -2147483648 or not 0 <= vals[1] <= len(vals) - 2:
        raise ValueError("Invalid VALUE_ARRAY header")
    n = vals[1]
    offsets = vals[2 : 2 + n]
    data = vals[2 + n :]
    if (
        len(data) % 4
        or (not n and data)
        or (n and (offsets[0] != 0 or any(a > b for a, b in zip(offsets, offsets[1:]))))
        or any(o < 0 or o > len(data) or o % 4 for o in offsets)
    ):
        raise ValueError("Invalid VALUE_ARRAY segment offsets or point data")
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
