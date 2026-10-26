"""Red-flag checks.

Every check returns zero or more :class:`Signal` objects with a point value
and human-readable evidence. Points are deliberately simple and transparent;
they are *indicators* for further research, not proof of wrongdoing.

Most identity checks take a reference date ``ref`` (normally the end of the
analysis window / the incident date). Changes in the ``lookback`` years before
``ref`` score full points; older history is listed for context only, and
changes after ``ref`` (renaming / reflagging after an incident) score a little.
"""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from statistics import median
from typing import Dict, List, Optional, Sequence, Tuple

from .geo import CableLayer, haversine_nm, path_length_nm
from .models import Identity, Signal, TrackPoint
from .registries import flag_from_mmsi, flag_tier, is_foc

SPARSE_TRACK_CAVEAT = (
    "Public GFW tracks are simplified (often one point every 60-90 min on open "
    "water). Short gaps and brief manoeuvres can be invisible or exaggerated."
)
YEAR = timedelta(days=365)
TIER_POINTS = {"black": 15, "grey": 10, "white": 5}


def _fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%d %H:%M UTC")


def _ref(ref: Optional[datetime]) -> datetime:
    return ref or datetime.now(timezone.utc)


def _overlaps(a: Identity, start: datetime, end: datetime) -> bool:
    if a.start and a.end:
        return a.start <= end and a.end >= start
    # One dated observation can establish presence at that time. An unknown
    # boundary cannot establish presence throughout the scoring period.
    return any(start <= d <= end for d in (a.start, a.end) if d)


def active_at(identities: Sequence[Identity], ref: datetime) -> Optional[Identity]:
    """Identity in use at ``ref`` (or the last one before it)."""
    dated = [i for i in identities if i.start and i.start <= ref]
    if not dated:
        return None
    covering = [i for i in dated if i.end and i.end >= ref]
    # Prefer the latest start among covering records. Clipping at a cut-off
    # makes their end dates equal, so end-only selection depends on input order.
    return max(
        covering or dated,
        key=lambda i: (
            i.start if covering else (i.end or i.start),
            i.start,
            i.key,
            i.imo or "",
            i.source,
            i.registry_confirmed,
        ),
    )


# ---------------------------------------------------------------------------
# Identity checks
# ---------------------------------------------------------------------------
def multiple_identities(
    identities: Sequence[Identity], ref: Optional[datetime] = None, lookback_years: int = 5
) -> List[Signal]:
    ref = _ref(ref)
    named = [i for i in identities if i.name]
    recent = [i for i in named if _overlaps(i, ref - lookback_years * YEAR, ref)]
    if len(named) < 2:
        return []
    ev = [("* " if i in recent else "  ") + i.label() for i in named]
    # a new MMSI under the same name and flag is not a new identity for scoring
    distinct = {(i.key[0], i.flag) for i in recent}
    pts = min(30, 10 * (len(distinct) - 1)) if len(distinct) >= 2 else 0
    return [
        Signal(
            code="MULTI_IDENTITY",
            title=f"{len(named)} identities linked to the same hull ({len(recent)} in the "
            f"{lookback_years} years before {ref:%Y-%m-%d})",
            points=pts,
            evidence=ev,
            caveat="* = dated use during the look-back period (scored); other records are outside it or undated.",
        )
    ]


def flag_changes(
    identities: Sequence[Identity], ref: Optional[datetime] = None, lookback_years: int = 3
) -> List[Signal]:
    ref = _ref(ref)
    ordered = sorted([i for i in identities if i.flag and i.start and i.end], key=lambda i: i.start)
    pts_recent, pts_after, ev = 0, 0, []
    seen = set()
    for cur in ordered:
        # predecessor = the identity that stopped shortly before (or just after) this one started
        cands = [
            p
            for p in ordered
            if p is not cur
            and p.start < cur.start
            and cur.start - timedelta(days=180) <= p.end <= cur.start + timedelta(days=60)
        ]
        if not cands:
            continue
        prev = max(cands, key=lambda p: (p.end, p.start, p.key, p.imo or "", p.source))
        if prev.flag == cur.flag:
            continue
        if prev.source == cur.source == "ais" and prev.end - cur.start >= timedelta(days=30):
            continue  # used at the same time -> reported by CONCURRENT_IDENTITIES
        event = (prev.flag, cur.flag, cur.start)
        if event in seen:
            continue
        seen.add(event)
        tier = flag_tier(cur.flag)
        tags = [f"Paris MoU {tier}" if tier != "unlisted" else "not on Paris MoU lists"]
        if is_foc(cur.flag):
            tags.append("ITF flag of convenience")
        line = f"{cur.start:%Y-%m-%d}: {prev.flag} -> {cur.flag} ({', '.join(tags)})  [{prev.name} -> {cur.name}]"
        if cur.start > ref:
            line += "  (after reference date)"
            pts_after += 5
        elif cur.start >= ref - lookback_years * YEAR:
            line += "  (recent)"
            pts_recent += TIER_POINTS[tier] if tier != "unlisted" else (10 if is_foc(cur.flag) else 5)
        ev.append(line)
    if not ev:
        return []
    return [
        Signal(
            code="FLAG_CHANGE",
            title=f"{len(ev)} flag change(s)",
            points=min(30, pts_recent) + min(10, pts_after),
            evidence=ev,
            caveat=f"Scored: changes in the {lookback_years} years before {ref:%Y-%m-%d} by the new flag's Paris MoU "
            "rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes "
            "after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed "
            "open registries.",
        )
    ]


def registry_confirmation(
    identities: Sequence[Identity], ref: Optional[datetime] = None, lookback_years: int = 5
) -> List[Signal]:
    ref = _ref(ref)
    current = active_at(identities, ref)
    if not current or current.registry_confirmed:
        return []
    confirmed = [i for i in identities if i.registry_confirmed and i.start and i.start <= ref]
    if confirmed:
        last = max(confirmed, key=lambda i: i.end or i.start)
        recent = last.end and last.end >= ref - lookback_years * YEAR
        return [
            Signal(
                code="REGISTRY_LOST",
                title="Selected AIS identity has no registry match in GFW; an earlier identity did",
                points=15 if recent else 5,
                evidence=[f"last confirmed: {last.label()}", f"selected for {ref:%Y-%m-%d}: {current.label()}"],
                caveat="GFW registry coverage is incomplete; a missing match does not establish invalid registration."
                + (
                    ""
                    if recent
                    else f" The last match ended more than {lookback_years} years before the reference date."
                ),
            )
        ]
    return [
        Signal(
            code="NO_REGISTRY",
            title="No identity of this hull is confirmed by a registry in GFW",
            points=10,
            evidence=[f"selected for {ref:%Y-%m-%d}: {current.label()}"],
            caveat="GFW registry coverage varies by flag and access level; "
            "a missing match is not proof of non-registration.",
        )
    ]


def mmsi_flag_mismatch(identities: Sequence[Identity]) -> List[Signal]:
    ev, seen = [], set()
    for i in identities:
        if i.source != "ais":
            continue
        mid_flag = flag_from_mmsi(i.mmsi)
        if mid_flag and i.flag and mid_flag != i.flag:
            if i.key in seen:
                continue
            seen.add(i.key)
            ev.append(f"{i.name}: MMSI {i.mmsi} belongs to {mid_flag}, but broadcasts flag {i.flag}")
    if not ev:
        return []
    return [Signal("MMSI_FLAG_MISMATCH", "MMSI country code does not match broadcast flag", min(20, 10 * len(ev)), ev)]


def mmsi_reuse(
    identities: Sequence[Identity], lookups: Optional[Dict[str, List[Identity]]], near_years: int = 2
) -> List[Signal]:
    """Same MMSI also used by vessels with a different name / IMO."""
    if not lookups:
        return []
    own_names = {i.key[0] for i in identities}
    own_imos = {i.imo for i in identities if i.imo}
    close, far = [], []
    for mmsi, others in lookups.items():
        if not any(i.mmsi == mmsi for i in identities):
            continue
        users = [i for i in identities if i.mmsi == mmsi and i.start and i.end]
        for o in others:
            if o.mmsi != mmsi or not o.name or (o.imo and o.imo in own_imos) or (o.key[0] in own_names and not o.imo):
                continue
            line = f"MMSI {mmsi} also used by {o.label()}" + (f", IMO {o.imo}" if o.imo else "")
            near = any(_overlaps(o, u.start - near_years * YEAR, u.end + near_years * YEAR) for u in users)
            (close if near else far).append(line + ("  (within %d years)" % near_years if near else ""))
    if not close and not far:
        return []
    ev = (
        close
        + far[:5]
        + ([f"... {len(far) - 5} further uses outside the dated proximity check"] if len(far) > 5 else [])
    )
    return [
        Signal(
            code="MMSI_REUSE",
            title=f"MMSI shared with other vessels ({len(close)} within {near_years} years, "
            f"{len(far)} outside or undated)",
            points=15 if close else 5,
            evidence=ev,
            caveat="Legitimate MMSI reassignment and errors in identity linking are possible.",
        )
    ]


def name_on_other_mmsi(identities: Sequence[Identity], lookups: Optional[Dict[str, List[Identity]]]) -> List[Signal]:
    """The hull's name broadcast under MMSIs that are not part of its known
    identities - often MMSIs that belong to other ships.

    Only counts an identity that (a) carries no IMO number or the hull's own, (b) was
    active while the hull itself used that name and (c) broadcast the same flag - a ship
    that merely shares a common name ("VLADIMIR") has its own IMO, period or flag."""
    if not lookups:
        return []
    own_mmsis = {i.mmsi for i in identities if i.mmsi}
    own_imos = {i.imo for i in identities if i.imo}
    usage: Dict[str, List[Identity]] = {}
    for i in identities:
        if i.key[0] and i.start and i.end:
            usage.setdefault(i.key[0], []).append(i)
    seen, ev = set(), []
    for found in lookups.values():
        for o in found:
            if not (o.key[0] in usage and o.mmsi and o.mmsi not in own_mmsis and o.key not in seen):
                continue
            if o.imo and o.imo not in own_imos:
                continue
            if not (
                o.start
                and o.end
                and o.flag
                and any(i.flag == o.flag and o.start <= i.end and o.end >= i.start for i in usage[o.key[0]])
            ):
                continue
            seen.add(o.key)
            owners = sorted(
                {x.name for f in lookups.values() for x in f if x.mmsi == o.mmsi and x.name and x.key[0] not in usage}
            )
            ev.append(f"{o.label()}" + (f" - MMSI also used by {', '.join(owners)}" if owners else ""))
    if not ev:
        return []
    return [
        Signal(
            "NAME_ON_OTHER_MMSI",
            "Known name reported under an additional MMSI",
            15,
            ev,
            "Short episodes can also be typing errors in the AIS set-up; repeated use is the signal.",
        )
    ]


def imo_hidden(identities: Sequence[Identity], lookups: Optional[Dict[str, List[Identity]]]) -> List[Signal]:
    """The hull's known name/MMSI also broadcast without an IMO number."""
    if not lookups:
        return []
    own = [i for i in identities if i.imo and i.flag and i.start and i.end]
    ev = []
    for others in lookups.values():
        for o in others:
            if (
                o.imo
                or not o.start
                or not o.end
                or not any(i.key == o.key and o.start <= i.end and o.end >= i.start for i in own)
            ):
                continue
            ev.append(f"{o.label()} - same name and MMSI, but no IMO number broadcast")
    if not ev:
        return []
    return [
        Signal(
            "IMO_HIDDEN",
            "Identity also used without its IMO number",
            10,
            ev,
            "A missing IMO can reflect incomplete AIS configuration; it does not establish deliberate concealment.",
        )
    ]


def concurrent_identities(
    identities: Sequence[Identity],
    ref: Optional[datetime] = None,
    min_overlap_days: float = 30,
    lookback_years: int = 5,
) -> List[Signal]:
    """Two identities of the same hull in use during the same period.

    A second MMSI under the *same* name and flag is usually a second
    transponder or a configuration error (+5); a different name or flag at the
    same time is the camouflage pattern (+20). Only overlaps in the look-back
    period before ``ref`` are scored."""
    ref = _ref(ref)
    lo_limit = ref - lookback_years * YEAR
    named = [i for i in identities if i.name and i.start and i.end and i.source == "ais"]
    ev, score, scored_pairs = [], 0, set()
    for a_i in range(len(named)):
        for b_i in range(a_i + 1, len(named)):
            a, b = named[a_i], named[b_i]
            if a.key == b.key:
                continue  # IMO metadata variants are not distinct AIS identities
            lo, hi = max(a.start, b.start), min(a.end, b.end)
            if (hi - lo) < timedelta(days=min_overlap_days):
                continue
            same = a.key[0] == b.key[0] and a.flag == b.flag
            recent = min(hi, ref) - max(lo, lo_limit) >= timedelta(days=min_overlap_days)
            line = f"{lo:%Y-%m-%d} - {hi:%Y-%m-%d}: {a.name}/{a.flag}/{a.mmsi} and {b.name}/{b.flag}/{b.mmsi}"
            if same:
                line += "  (same name and flag - likely a second transponder)"
            if not recent:
                line += f"  (less than {min_overlap_days:g} days inside the scoring period, not scored)"
            else:
                pair = tuple(sorted((a.key, b.key)))
                if pair not in scored_pairs:
                    score += 5 if same else 20
                    scored_pairs.add(pair)
            ev.append(line)
    if not ev:
        return []
    return [
        Signal(
            code="CONCURRENT_IDENTITIES",
            title="Overlapping first/last dates for linked AIS identities",
            points=min(20, score),
            evidence=list(dict.fromkeys(ev)),
            caveat="Overlap is computed from first/last AIS message per identity; check the tracks "
            "(handover / parallel signals).",
        )
    ]


def _activity_edges(points: Sequence[TrackPoint], fetched: Optional[Tuple[datetime, datetime]], gap: timedelta):
    """'off' and 'on' events of one identity: ends/starts of broadcast periods,
    ignoring the edges of the requested time range."""
    pts = sorted(points, key=lambda p: p.t)
    if not pts:
        return [], []
    offs, ons = [], []
    if not fetched or pts[0].t - fetched[0] > gap:
        ons.append(pts[0])
    for p, q in zip(pts, pts[1:]):
        if q.t - p.t >= gap:
            offs.append(p)
            ons.append(q)
    if not fetched or fetched[1] - pts[-1].t > gap:
        offs.append(pts[-1])
    return offs, ons


def identity_handover(
    tracks: Dict[str, List[TrackPoint]],
    fetched: Optional[Dict[str, Tuple[datetime, datetime]]] = None,
    gap: timedelta = timedelta(hours=6),
    max_dt: timedelta = timedelta(hours=6),
    base_nm: float = 10.0,
    max_kn: float = 15.0,
) -> List[Signal]:
    """One identity of the hull goes silent and another one starts at a
    physically reachable position shortly after - an identity swap at sea."""
    edges = {k: _activity_edges(v, (fetched or {}).get(k), gap) for k, v in tracks.items()}
    ev = []
    for a, (offs, _) in edges.items():
        for b, (_, ons) in edges.items():
            if a == b:
                continue
            for off in offs:
                for on in ons:
                    dt = on.t - off.t
                    if timedelta(0) <= dt <= max_dt:
                        d = haversine_nm(off.lat, off.lon, on.lat, on.lon)
                        if d <= base_nm + max_kn * dt.total_seconds() / 3600:
                            ev.append(
                                f"{a} stops {_fmt(off.t)} at {off.lat:.3f},{off.lon:.3f} -> {b} starts "
                                f"{_fmt(on.t)} at {on.lat:.3f},{on.lon:.3f} "
                                f"({dt.total_seconds() / 60:.0f} min, {d:.1f} nm)"
                            )
    if not ev:
        return []
    return [
        Signal(
            code="IDENTITY_HANDOVER",
            title="Possible identity handover (one AIS track stops, another starts nearby)",
            points=20,
            evidence=sorted(set(ev)),
            caveat="A reachable position is not proof of the same hull. Coverage gaps, ports and incorrect links "
            "can produce similar candidates.",
        )
    ]


def parallel_tracks(
    tracks: Dict[str, List[TrackPoint]], max_dt: timedelta = timedelta(hours=1), min_nm: float = 100
) -> List[Signal]:
    """Two identities of the same claimed hull broadcasting at the same time far apart."""
    labels = list(tracks)
    ev = []
    for ai in range(len(labels)):
        for bi in range(ai + 1, len(labels)):
            a = sorted(tracks[labels[ai]], key=lambda p: p.t)
            b = sorted(tracks[labels[bi]], key=lambda p: p.t)
            hit = _first_parallel(a, b, max_dt, min_nm)
            if hit:
                pa, pb, d = hit
                ev.append(
                    f"{labels[ai]} at {pa.lat:.2f},{pa.lon:.2f} ({_fmt(pa.t)}) vs {labels[bi]} at "
                    f"{pb.lat:.2f},{pb.lon:.2f} ({_fmt(pb.t)}): {d:.0f} nm apart"
                )
    if not ev:
        return []
    return [
        Signal(
            code="PARALLEL_TRACKS",
            title="Linked identities report distant positions within one hour",
            points=20,
            evidence=ev,
            caveat="Either two hulls share identity data (spoofing / cloning) or GFW linked identities wrongly.",
        )
    ]


def _first_parallel(a, b, max_dt, min_nm) -> Optional[Tuple[TrackPoint, TrackPoint, float]]:
    j = 0
    for p in a:
        while j < len(b) and b[j].t < p.t - max_dt:
            j += 1
        k = j
        while k < len(b) and b[k].t <= p.t + max_dt:
            q = b[k]
            d = haversine_nm(p.lat, p.lon, q.lat, q.lon)
            if d >= min_nm:
                return p, q, d
            k += 1
    return None


# ---------------------------------------------------------------------------
# Track checks
# ---------------------------------------------------------------------------
def ais_gaps(
    points: Sequence[TrackPoint],
    window: Optional[Tuple[datetime, datetime]] = None,
    min_hours: float = 6,
    context: timedelta = timedelta(days=7),
    min_jump_nm: float = 5,
    cover: Optional[Dict[str, List[TrackPoint]]] = None,
) -> List[Signal]:
    """Missing positions. Gaps touching the window (+/- ``context``) are
    reported; gaps where the ship did not move (< ``min_jump_nm``) and that
    are shorter than 48 h are typical for ports / sparse coverage and are only
    counted, not scored."""
    pts = sorted(points, key=lambda p: p.t)
    if window:
        lo, hi = window[0] - context, window[1] + context
    ev, quiet, score = [], 0, 0
    for p, q in zip(pts, pts[1:]):
        h = (q.t - p.t).total_seconds() / 3600
        if h < min_hours or (window and (q.t < lo or p.t > hi)):
            continue
        d = haversine_nm(p.lat, p.lon, q.lat, q.lon)
        covers = bool(window and p.t <= window[1] and q.t >= window[0])
        if d < min_jump_nm and h < 48 and not covers:
            quiet += 1
            continue
        line = (
            f"{_fmt(p.t)} -> {_fmt(q.t)}: {h:.1f} h without position, {d:.0f} nm straight-line jump "
            f"(implied {d / h:.1f} kn), {p.lat:.3f},{p.lon:.3f} -> {q.lat:.3f},{q.lon:.3f}"
        )
        covering = {k: sum(1 for x in v if p.t < x.t < q.t) for k, v in (cover or {}).items()}
        covering = {k: n for k, n in covering.items() if n}
        if covering:
            who = ", ".join(f"{k} ({n} positions)" for k, n in covering.items())
            ev.append(line + f"; meanwhile GFW records linked track(s): {who}; no additional gap points")
            continue
        score += 10 if h >= 24 else 5
        if covers:
            line += "  <-- overlaps the analysis window"
            score += 10
        ev.append(line)
    if window and pts and (pts[-1].t < window[0] or pts[0].t > window[1]):
        ev.append("no track points at all inside the analysis window")
        score += 15
    scored = score > 0
    if quiet:
        ev.append(
            f"{quiet} further gap(s) >= {min_hours:g} h without movement (port / anchorage / sparse data) - not scored"
        )
    if not ev:
        return []
    title = "AIS gaps" if scored else "Only short stationary AIS gaps (not scored)"
    return [Signal("AIS_GAP", title, min(30, score), ev, SPARSE_TRACK_CAVEAT)]


def connected(p: TrackPoint, q: TrackPoint, max_gap_h: float = 3.0) -> bool:
    """Interpolation guard, not a claim of continuous observation."""
    return p.segment == q.segment and timedelta(0) < q.t - p.t <= timedelta(hours=max_gap_h)


def _runs(points: Sequence[TrackPoint], pred) -> List[List[TrackPoint]]:
    runs, cur = [], []
    for p in points:
        if cur and not connected(cur[-1], p):
            runs.append(cur)
            cur = []
        if pred(p):
            cur.append(p)
        else:
            if cur:
                runs.append(cur)
            cur = []
    if cur:
        runs.append(cur)
    return runs


def slow_movement(
    points: Sequence[TrackPoint], max_kn: float = 3.0, min_hours: float = 2.0, moving_rate_nm_h: float = 0.5
) -> List[Signal]:
    """Long stretches at low speed, split into 'stationary' (anchored /
    drifting on the spot) and 'slow moving' (crawling or circling)."""
    pts = sorted(points, key=lambda p: p.t)
    ev, score = [], 0
    for run in _runs(pts, lambda p: p.speed <= max_kn):
        hours = (run[-1].t - run[0].t).total_seconds() / 3600
        if hours < min_hours:
            continue
        path = path_length_nm(run)
        net = haversine_nm(run[0].lat, run[0].lon, run[-1].lat, run[-1].lon)
        moving = path / hours >= moving_rate_nm_h
        kind = "slow moving" if moving else "stationary (anchored or drifting)"
        mean = sum(p.speed for p in run) / len(run)
        ev.append(
            f"{_fmt(run[0].t)} -> {_fmt(run[-1].t)}: {hours:.1f} h {kind}, mean AIS speed {mean:.1f} kn, "
            f"path {path:.1f} nm, net {net:.1f} nm, at {run[0].lat:.3f},{run[0].lon:.3f}"
        )
        score += 10 if moving else 0
    if not ev:
        return []
    return [
        Signal(
            "SLOW_LOITERING",
            f"Low speed (<= {max_kn:g} kn) for {min_hours:g} h or more",
            min(20, score),
            ev,
            "Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a "
            "cable layer the tool cannot tell a port from an anchorage over a cable.",
        )
    ]


def speed_drop(
    points: Sequence[TrackPoint],
    reference: Optional[Sequence[TrackPoint]] = None,
    factor: float = 0.6,
    min_hours: float = 1.5,
    cruise_min_kn: float = 5.0,
) -> List[Signal]:
    """Underway but clearly slower than the ship's own cruising speed
    (e.g. dragging an anchor). Cruising speed is the median of ``reference``
    points >= ``cruise_min_kn`` (defaults to ``points``)."""
    pts = sorted(points, key=lambda p: p.t)
    cruise = [p.speed for p in (reference or pts) if p.speed >= cruise_min_kn]
    if len(cruise) < 5:
        return []
    ref = median(cruise)
    limit = ref * factor
    ev = []
    for run in _runs(pts, lambda p: 2.0 < p.speed < limit):
        hours = (run[-1].t - run[0].t).total_seconds() / 3600
        # require real movement: AIS speed jitters around 2 kn at anchor
        if len(run) >= 2 and hours >= min_hours and path_length_nm(run) / hours >= 1.0:
            ev.append(
                f"{_fmt(run[0].t)} -> {_fmt(run[-1].t)}: {hours:.1f} h at {min(p.speed for p in run):.1f}-"
                f"{max(p.speed for p in run):.1f} kn (cruising median {ref:.1f} kn), from "
                f"{run[0].lat:.3f},{run[0].lon:.3f}"
            )
    if not ev:
        return []
    return [Signal("SPEED_DROP", "Sustained speed drop while underway", 10, ev, SPARSE_TRACK_CAVEAT)]


def zigzag(
    points: Sequence[TrackPoint],
    window_hours: float = 6,
    min_path_nm: float = 5,
    ratio: float = 2.5,
    max_mean_kn: float = 6.0,
) -> List[Signal]:
    """Path much longer than net displacement at low average speed:
    zig-zagging, loops, circling. The speed limit keeps shuttle ferries out."""
    pts = sorted(points, key=lambda p: p.t)
    ev, last_end = [], None
    for i, p in enumerate(pts):
        if last_end and p.t < last_end:
            continue
        j = i
        while (
            j + 1 < len(pts) and connected(pts[j], pts[j + 1]) and (pts[j + 1].t - p.t) <= timedelta(hours=window_hours)
        ):
            j += 1
        seg = pts[i : j + 1]
        if len(seg) < 4:
            continue
        path = path_length_nm(seg)
        net = haversine_nm(seg[0].lat, seg[0].lon, seg[-1].lat, seg[-1].lon)
        hours = max((seg[-1].t - seg[0].t).total_seconds() / 3600, 1e-6)
        if path >= min_path_nm and path >= ratio * max(net, 0.1) and path / hours <= max_mean_kn:
            ev.append(
                f"{_fmt(seg[0].t)} -> {_fmt(seg[-1].t)}: {path:.1f} nm sailed, only {net:.1f} nm net, "
                f"at {seg[0].lat:.3f},{seg[0].lon:.3f}"
            )
            last_end = seg[-1].t
    if not ev:
        return []
    return [Signal("ZIGZAG", "Zig-zag / looping movement", 10, ev, SPARSE_TRACK_CAVEAT)]


def cable_crossings(
    points: Sequence[TrackPoint],
    cables: Optional[CableLayer],
    reference: Optional[Sequence[TrackPoint]] = None,
    factor: float = 0.7,
    fallback_kn: float = 5.0,
    max_gap_h: float = 3.0,
    cruise_min_kn: float = 5.0,
) -> List[Signal]:
    """The track crosses a mapped cable or pipeline while the ship moves clearly slower
    than its own cruising speed - the pattern of an anchor dragged across a cable.

    Speed is measured over ground between the two positions (AIS speed jitters).
    Crossings while lying still (both AIS speeds and the rate < 1 kn) are ignored:
    at a berth a cable can run under a ship that does not move."""
    if not cables:
        return []
    pts = sorted(points, key=lambda p: p.t)
    cruise = [p.speed for p in (reference or pts) if p.speed >= cruise_min_kn]
    ref = median(cruise) if len(cruise) >= 5 else None
    limit = ref * factor if ref else fallback_kn
    ev = []
    for p, q in zip(pts, pts[1:]):
        hours = (q.t - p.t).total_seconds() / 3600
        if not connected(p, q, max_gap_h):
            continue
        rate = haversine_nm(p.lat, p.lon, q.lat, q.lon) / hours
        if rate > limit or (rate < 1.0 and max(p.speed, q.speed) < 1.0):
            continue
        names = cables.crossed((p.lon, p.lat), (q.lon, q.lat))
        if names:
            base = f", cruising median {ref:.1f} kn" if ref else ""
            ev.append(
                f"{_fmt(p.t)} -> {q.t:%H:%M}: crosses {', '.join(names)} at {rate:.1f} kn over ground{base}, "
                f"around {(p.lat + q.lat) / 2:.3f},{(p.lon + q.lon) / 2:.3f}"
            )
    if not ev:
        return []
    return [
        Signal(
            "CABLE_CROSSING_SLOW",
            "Crossed a mapped cable or pipeline at reduced speed",
            20,
            ev,
            "Straight-line crossings reconstructed between sparse positions. OpenStreetMap routes are approximate "
            "and incomplete. This does not establish contact with a cable, anchor use or intent.",
        )
    ]


ALL_CODES = [
    "MULTI_IDENTITY",
    "FLAG_CHANGE",
    "REGISTRY_LOST",
    "NO_REGISTRY",
    "SANCTIONED",
    "MMSI_FLAG_MISMATCH",
    "MMSI_REUSE",
    "NAME_ON_OTHER_MMSI",
    "IMO_HIDDEN",
    "CONCURRENT_IDENTITIES",
    "IDENTITY_HANDOVER",
    "PARALLEL_TRACKS",
    "AIS_GAP",
    "SLOW_LOITERING",
    "SPEED_DROP",
    "ZIGZAG",
    "CABLE_CROSSING_SLOW",
]
