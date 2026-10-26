"""Run all checks for one hull and build a :class:`Report`."""

from __future__ import annotations

import json
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Tuple

from . import signals as S
from .geo import CableLayer
from .gfw import _merge, identities_from_entries
from .models import Identity, Report, TrackPoint


def merge_lookup_identities(identities: List[Identity], lookups: Optional[Dict[str, List[Identity]]]) -> List[Identity]:
    """Fold MMSI-search hits that are the *same* identity (same name, flag and
    MMSI, just without IMO) into the identity list, widening its time span."""
    if not lookups:
        return list(identities)
    out = {i.key: replace(i) for i in identities}
    for others in lookups.values():
        for o in others:
            if o.key in out:
                _merge(out, replace(o))
    return sorted(out.values(), key=lambda i: i.start.timestamp() if i.start else 0)


def _merge_signals(groups: List[List]) -> List:
    """Combine per-track results: one signal per code, max points, all evidence."""
    out: Dict[str, object] = {}
    for label, sigs in groups:
        for s in sigs:
            ev = [f"[{label}] {e}" for e in s.evidence] if label else list(s.evidence)
            if s.code not in out:
                out[s.code] = replace(s, evidence=ev)
            else:
                cur = out[s.code]
                cur.evidence += ev
                if s.points > cur.points:
                    cur.points, cur.title = s.points, s.title
    return list(out.values())


def clip_identities(identities: List[Identity], as_of: datetime) -> List[Identity]:
    """Only what was observable at ``as_of``: identities that had started, with
    their last-seen date cut at ``as_of``."""
    out = []
    for i in identities:
        if i.start and i.start > as_of:
            continue
        out.append(replace(i, end=min(i.end, as_of) if i.end else i.end))
    return out


def analyze(
    query: str,
    identities: List[Identity],
    track: List[TrackPoint],
    window: Optional[Tuple[datetime, datetime]] = None,
    mmsi_lookups: Optional[Dict[str, List[Identity]]] = None,
    parallel: Optional[Dict[str, List[TrackPoint]]] = None,
    cables: Optional[CableLayer] = None,
    incident_time: Optional[datetime] = None,
    excerpt_hours: float = 3.0,
    fetched: Optional[Dict[str, Tuple[datetime, datetime]]] = None,
    primary_label: str = "",
    extra_tracks: Optional[Dict[str, List[TrackPoint]]] = None,
    as_of: Optional[datetime] = None,
) -> Report:
    """Run every check.

    ``track`` is the main AIS identity in use around the window. ``extra_tracks``
    are other identities of the same hull whose movements should be checked
    too (each separately, so two clones are never stitched into one path).
    ``parallel`` holds all identity tracks for the handover / parallel checks.
    """
    if as_of:
        # pre-incident view: drop everything GFW recorded after ``as_of``
        identities = clip_identities(identities, as_of)
        mmsi_lookups = {m: clip_identities(v, as_of) for m, v in (mmsi_lookups or {}).items()}
        track = [p for p in track if p.t <= as_of]
        extra_tracks = {k: [p for p in v if p.t <= as_of] for k, v in (extra_tracks or {}).items()}
        parallel = {k: [p for p in v if p.t <= as_of] for k, v in (parallel or {}).items()}
        fetched = {k: (a, min(b, as_of)) for k, (a, b) in (fetched or {}).items()}
        start = window[0] if window and window[0] < as_of else as_of - timedelta(days=3)
        window = (start, as_of)
        incident_time = None
    ref = window[1] if window else as_of
    sigs = []
    sigs += S.imo_hidden(identities, mmsi_lookups)
    identities = merge_lookup_identities(identities, mmsi_lookups)
    sigs += S.multiple_identities(identities, ref)
    sigs += S.flag_changes(identities, ref)
    sigs += S.registry_confirmation(identities, ref)
    sigs += S.mmsi_flag_mismatch(identities)
    sigs += S.mmsi_reuse(identities, mmsi_lookups)
    sigs += S.name_on_other_mmsi(identities, mmsi_lookups)
    sigs += S.concurrent_identities(identities, ref)
    if parallel and len(parallel) > 1:
        sigs += S.identity_handover(parallel, fetched)
        sigs += S.parallel_tracks(parallel)

    movement = {primary_label: sorted(track, key=lambda p: p.t)}
    for k, v in (extra_tracks or {}).items():
        movement[k] = sorted(v, key=lambda p: p.t)
    multi = len(movement) > 1
    groups = []
    n_window = 0
    for label, pts in movement.items():
        in_window = [p for p in pts if not window or window[0] <= p.t <= window[1]]
        n_window += len(in_window)
        others = {k: v for k, v in movement.items() if k != label}
        found = []
        found += S.ais_gaps(pts, window=window, cover=others)
        found += S.slow_movement(in_window)
        found += S.speed_drop(in_window, reference=pts)
        found += S.zigzag(in_window)
        found += S.near_cables(in_window, cables)
        groups.append((label if multi else "", found))
    sigs += _merge_signals(groups)

    order = {c: n for n, c in enumerate(S.ALL_CODES)}
    sigs.sort(key=lambda s: order.get(s.code, 99))
    total = sum(len(v) for v in movement.values())
    notes = [f"{n_window} track points inside the analysis window ({total} loaded, {len(movement)} identity track(s))."]
    if not cables:
        notes.append("No cable layer given (--cables): proximity to cable routes was not checked.")
    excerpt = []
    if incident_time:
        pad = timedelta(hours=excerpt_hours)
        for label, pts in movement.items():
            excerpt += [(label, p) for p in pts if incident_time - pad <= p.t <= incident_time + pad]
        excerpt.sort(key=lambda lp: lp[1].t)
    return Report(
        query=query,
        identities=identities,
        signals=sigs,
        window=window,
        notes=notes,
        incident_time=incident_time,
        excerpt=excerpt,
        as_of=as_of,
    )


# ---------------------------------------------------------------------------
# Offline use with the fixtures in data/fixtures
# ---------------------------------------------------------------------------
def load_fixture(path: str | Path) -> dict:
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _day(s: str) -> datetime:
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def analyze_fixture(
    case: dict, fixture: dict, cables: Optional[CableLayer] = None, before_incident: bool = False
) -> Report:
    """Re-run a reference case. ``before_incident`` limits the data to what GFW
    had recorded up to the case's ``as_of`` time (start of the incident)."""
    identities = identities_from_entries(fixture["identities"])
    tracks = {k: [TrackPoint.from_row(r) for r in v["points"]] for k, v in fixture["tracks"].items()}
    lookups = {m: identities_from_entries(e, dedupe=False) for m, e in (fixture.get("mmsi_lookups") or {}).items()}
    # identities linked to the hull by hand (no IMO in GFW, found via name search)
    for m in case.get("linked_mmsis", []):
        identities += [i for i in identities_from_entries(fixture["mmsi_lookups"][m]) if i.mmsi == m]
    labels = case.get("track_labels", {})
    parallel = {labels.get(k, k): tracks[k] for k in case.get("parallel", []) if k in tracks}
    fetched = {labels.get(k, k): (_day(v["start"]), _day(v["end"])) for k, v in fixture["tracks"].items()}
    primary = case["primary_track"]
    extra = {labels.get(k, k): tracks[k] for k in case.get("movement_tracks", []) if k != primary}
    return analyze(
        query=f"IMO {case['imo']}",
        identities=identities,
        track=tracks[primary],
        primary_label=labels.get(primary, primary),
        extra_tracks=extra,
        fetched=fetched,
        window=case.get("window"),
        mmsi_lookups=lookups,
        parallel=parallel,
        cables=cables,
        incident_time=case.get("incident_time"),
        as_of=(case.get("as_of") or case["window"][1]) if before_incident else None,
    )
