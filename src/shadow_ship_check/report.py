"""Render a Report as Markdown, plain text or JSON."""

from __future__ import annotations

import json
from dataclasses import asdict

from .models import Report

DISCLAIMER = (
    "Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)."
)


def to_markdown(r: Report, title: str | None = None) -> str:
    out = [f"# {title or 'Shadow Ship Check: ' + r.query}", ""]
    out.append(f"**Score: {r.score}/100 ({r.level})**  ")
    if r.window:
        out.append(f"Analysis window: {r.window[0]:%Y-%m-%d %H:%M} - {r.window[1]:%Y-%m-%d %H:%M} UTC  ")
    out.append(f"_{DISCLAIMER}_")
    out += [
        "",
        "## Identities",
        "",
        "| Name | Flag | MMSI | IMO | From | To | Source |",
        "|---|---|---|---|---|---|---|",
    ]
    for i in r.identities:
        out.append(
            f"| {i.name or '-'} | {i.flag or '-'} | {i.mmsi or '-'} | {i.imo or '-'} | "
            f"{i.start:%Y-%m-%d} | {i.end:%Y-%m-%d} | {i.source_label} |"
            if i.start and i.end
            else f"| {i.name or '-'} | {i.flag or '-'} | {i.mmsi or '-'} | {i.imo or '-'} | ? | ? | {i.source_label} |"
        )
    out += ["", "## Red flags", ""]
    if not r.signals:
        out.append("None of the checks fired.")
    for s in r.signals:
        out.append(f"### {s.title}  `{s.code}` (+{s.points})")
        out += [f"- {e}" for e in s.evidence]
        if s.caveat:
            out.append(f"\n> {s.caveat}")
        out.append("")
    if r.incident_time:
        out += [
            "## Track around the reported incident time",
            "",
            f"Reported time (approximate): {r.incident_time:%Y-%m-%d %H:%M} UTC. Points within +/- 3 h:",
            "",
        ]
        if r.excerpt:
            out += ["| Time (UTC) | Identity | Lat | Lon | AIS speed (kn) |", "|---|---|---|---|---|"]
            out += [
                f"| {p.t:%Y-%m-%d %H:%M} | {lab or '-'} | {p.lat:.4f} | {p.lon:.4f} | {p.speed:.1f} |"
                for lab, p in r.excerpt
            ]
        else:
            out.append("No AIS positions in GFW for this period.")
        out.append("")
    if r.notes:
        out += ["## Notes", ""] + [f"- {n}" for n in r.notes]
    return "\n".join(out) + "\n"


def to_text(r: Report) -> str:
    lines = [f"Shadow Ship Check - {r.query}", f"Score {r.score}/100 ({r.level})", ""]
    lines.append("Identities:")
    lines += [f"  - {i.label()}" for i in r.identities]
    lines.append("")
    for s in r.signals:
        lines.append(f"[+{s.points:>2}] {s.code}: {s.title}")
        lines += [f"        {e}" for e in s.evidence[:8]]
        if len(s.evidence) > 8:
            lines.append(f"        ... {len(s.evidence) - 8} more")
    lines += ["", DISCLAIMER]
    return "\n".join(lines)


def to_json(r: Report) -> str:
    d = {
        "query": r.query,
        "score": r.score,
        "level": r.level,
        "window": [w.isoformat() for w in r.window] if r.window else None,
        "identities": [asdict(i) for i in r.identities],
        "signals": [asdict(s) for s in r.signals],
        "notes": r.notes,
    }
    return json.dumps(d, indent=2, default=str)
