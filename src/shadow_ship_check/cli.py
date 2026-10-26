"""Command line interface: ``ssc search | check | case``."""

from __future__ import annotations

import argparse
import http.client
import sys
import urllib.error
from dataclasses import replace
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

from .analyze import analyze, analyze_fixture, load_fixture
from .cases import ALL
from .geo import CableLayer
from .gfw import GFWClient, identities_from_entries
from .models import Identity, normalize_name
from .report import to_json, to_markdown, to_text

DEFAULT_FIXTURES = Path(__file__).resolve().parents[2] / "data" / "fixtures"


def _date(s: str) -> datetime:
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def _emit(report, args, title=None) -> None:
    if args.json:
        Path(args.json).write_text(to_json(report), encoding="utf-8")
    if args.md:
        Path(args.md).write_text(to_markdown(report, title), encoding="utf-8")
    print(to_text(report))


def cmd_search(args) -> int:
    for i in GFWClient().search(args.query):
        print(f"{i.vessel_id or '(registry)':40} {i.label()}  IMO {i.imo or '-'}")
    return 0


def _same_hull(identities: List[Identity], query: str) -> List[Identity]:
    """Keep identities that share the queried IMO/MMSI (search results are fuzzy)."""
    q = query.strip()
    imos = {i.imo for i in identities if q in (i.imo, i.mmsi) and i.imo}
    return [i for i in identities if q in (i.imo, i.mmsi) or (i.imo and i.imo in imos)]


def _label(i: Identity) -> str:
    return f"{i.name}/{i.flag}/{i.mmsi}" + ("" if i.imo else " (no IMO)")


def cmd_check(args) -> int:
    client = GFWClient()
    raw = _same_hull(identities_from_entries(client.search_raw(args.query), dedupe=False), args.query)
    if not raw:
        print(f"No vessel found for {args.query!r} (search by IMO or MMSI for exact matches).", file=sys.stderr)
        return 1
    end = _date(args.end) if args.end else datetime.now(timezone.utc)
    start = _date(args.start) if args.start else end - timedelta(days=30)
    pad = timedelta(days=args.context_days)

    # MMSI look-ups: reuse by other ships, and IMO-less copies of the hull's identities
    lookups = {}
    if not args.no_mmsi_lookup:
        for m in sorted({i.mmsi for i in raw if i.mmsi}):
            lookups[m] = [i for i in identities_from_entries(client.search_raw(m), dedupe=False) if i.mmsi == m]
        # the hull's recent names: does the name also appear under other MMSIs?
        for name in sorted({i.name for i in raw if i.name and i.end and i.end >= start - 3 * 365 * timedelta(days=1)})[
            :3
        ]:
            hits = [
                i
                for i in identities_from_entries(client.search_raw(name), dedupe=False)
                if i.key[0] == normalize_name(name)
            ]
            for m in {i.mmsi for i in hits if i.mmsi} - set(lookups):
                lookups[m] = [i for i in identities_from_entries(client.search_raw(m), dedupe=False) if i.mmsi == m]
    keys = {i.key for i in raw}
    gfw_ids = {i.vessel_id: i for i in raw if i.vessel_id}
    for found in lookups.values():
        gfw_ids.update({i.vessel_id: i for i in found if i.vessel_id and i.key in keys})
    # identities linked by hand (e.g. a name variant without IMO)
    linked = []
    for q in args.also or []:
        hits = [
            i
            for i in identities_from_entries(client.search_raw(q), dedupe=False)
            if q in (i.mmsi, i.imo) or i.key[0] == q.upper().replace(" ", "")
        ]
        linked += hits
        gfw_ids.update({i.vessel_id: i for i in hits if i.vessel_id})

    tracks = {}
    for vid, ident in gfw_ids.items():
        if not ident.end or ident.end < start - pad or (ident.start and ident.start > end + pad):
            continue
        pts = client.track(vid, start - pad, end + pad)
        if pts:
            tracks.setdefault(_label(ident), []).extend(pts)
    for v in tracks.values():
        v.sort(key=lambda p: p.t)
    if not tracks:
        print("No AIS positions in the requested period.", file=sys.stderr)
    in_win = {k: sum(1 for p in v if start <= p.t <= end) for k, v in tracks.items()}
    primary = max(in_win, key=in_win.get) if tracks else ""
    extra = {k: v for k, v in tracks.items() if k != primary and in_win[k]}
    fetched = {k: (start - pad, end + pad) for k in tracks}

    cables = CableLayer.from_geojson(args.cables) if args.cables else None
    report = analyze(
        args.query,
        _dedupe(raw + linked),
        tracks.get(primary, []),
        window=(start, end),
        mmsi_lookups=lookups,
        parallel=tracks if len(tracks) > 1 else None,
        cables=cables,
        incident_time=_date(args.at) if args.at else None,
        fetched=fetched,
        primary_label=primary if extra else "",
        extra_tracks=extra,
    )
    _emit(report, args)
    return 0


def _dedupe(identities: List[Identity]) -> List[Identity]:
    from .gfw import _merge

    out: dict = {}
    for i in identities:
        _merge(out, replace(i))
    return sorted(out.values(), key=lambda i: i.start.timestamp() if i.start else 0)


def cmd_case(args) -> int:
    names = list(ALL) if args.name == "all" else [args.name]
    cables = CableLayer.from_geojson(args.cables) if args.cables else None
    for n in names:
        if n not in ALL:
            print(f"Unknown case {n!r}. Available: {', '.join(ALL)}", file=sys.stderr)
            return 1
        case = ALL[n]
        report = analyze_fixture(case, load_fixture(Path(args.fixtures) / f"{n}.json"), cables)
        if len(names) > 1:
            if args.md:
                Path(args.md).mkdir(parents=True, exist_ok=True)
                Path(args.md, f"{n}.md").write_text(to_markdown(report, case["title"]), encoding="utf-8")
            scored = ", ".join(f"{s.code}+{s.points}" for s in report.signals if s.points)
            print(f"{n:20} score {report.score:>3} {report.level:6} {scored}")
        else:
            _emit(report, args, case["title"])
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(
        prog="ssc", description="Check ships for camouflage patterns seen before subsea cable incidents."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="list identities matching a name / IMO / MMSI")
    s.add_argument("query")
    s.set_defaults(func=cmd_search)

    c = sub.add_parser("check", help="run all checks for one vessel (live data from GFW)")
    c.add_argument("query", help="IMO or MMSI (exact match recommended)")
    c.add_argument("--start", help="window start, YYYY-MM-DD (default: 30 days before --end)")
    c.add_argument("--end", help="window end, YYYY-MM-DD (default: now)")
    c.add_argument("--context-days", type=int, default=3, help="extra days of track loaded around the window")
    c.add_argument("--at", help="incident time (UTC, e.g. 2025-02-24T19:00) - prints the track +/- 3 h")
    c.add_argument("--cables", help="GeoJSON with cable routes (LineString features)")
    c.add_argument("--no-mmsi-lookup", action="store_true", help="skip the extra search for MMSI reuse")
    c.add_argument(
        "--also",
        action="append",
        metavar="MMSI_OR_NAME",
        help="link another identity to this hull by hand (repeatable), e.g. a name variant without IMO",
    )
    c.add_argument("--md", help="write a Markdown report to this path")
    c.add_argument("--json", help="write a JSON report to this path")
    c.set_defaults(func=cmd_check)

    k = sub.add_parser("case", help="re-run a reference case from the bundled fixtures (offline)")
    k.add_argument("name", help=f"one of: {', '.join(ALL)}, or 'all'")
    k.add_argument("--fixtures", default=str(DEFAULT_FIXTURES))
    k.add_argument("--cables")
    k.add_argument("--md", help="Markdown output file (a directory when name is 'all')")
    k.add_argument("--json")
    k.set_defaults(func=cmd_case)

    args = p.parse_args(argv)
    try:
        return args.func(args)
    except (urllib.error.URLError, http.client.HTTPException, TimeoutError) as exc:
        print(f"Could not reach Global Fishing Watch: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
