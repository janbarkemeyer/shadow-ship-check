"""Render a Report as Markdown, plain text or JSON."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import List, Optional

from .models import CATEGORIES, CATEGORY_OF, Report

DISCLAIMER = (
    "Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)."
)


def _sub(r: Report) -> str:
    return " · ".join(f"{CATEGORIES[c][0]} {p}" for c, p in r.subscores.items())


def _header(r: Report) -> List[str]:
    out = [f"**Score: {r.score}/100 ({r.level})** - {_sub(r)}  "]
    if r.window:
        out.append(f"Analysis window: {r.window[0]:%Y-%m-%d %H:%M} - {r.window[1]:%Y-%m-%d %H:%M} UTC  ")
    if r.as_of:
        out.append(f"Data cut-off: {r.as_of:%Y-%m-%d %H:%M} UTC - only what GFW had recorded before this time  ")
    return out


def _identity_table(r: Report) -> List[str]:
    out = ["| Name | Flag | MMSI | IMO | First seen | Last seen | Source |", "|---|---|---|---|---|---|---|"]
    for i in r.identities:
        a = f"{i.start:%Y-%m-%d}" if i.start else "?"
        b = f"{i.end:%Y-%m-%d}" if i.end else "?"
        out.append(
            f"| {i.name or '-'} | {i.flag or '-'} | {i.mmsi or '-'} | {i.imo or '-'} | {a} | {b} | {i.source_label} |"
        )
    return out


def _signals(r: Report, h: str = "##") -> List[str]:
    if not r.signals:
        return ["None of the checks fired.", ""]
    out: List[str] = []
    for cat, (label, _) in CATEGORIES.items():
        sigs = [s for s in r.signals if CATEGORY_OF.get(s.code, "behaviour") == cat]
        if not sigs:
            continue
        out += [f"{h}# {label} (+{sum(s.points for s in sigs)})", ""]
        for s in sigs:
            out.append(f"**{s.title}** `{s.code}` +{s.points}")
            out.append("")
            out += [f"- {e}" for e in s.evidence]
            if s.caveat:
                out += ["", f"> {s.caveat}"]
            out.append("")
    return out


def _excerpt(r: Report, h: str = "##") -> List[str]:
    if not r.incident_time:
        return []
    out = [
        f"{h} Track around the reported incident time",
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
    return out + [""]


def _summary(r: Report, n: int = 3) -> List[str]:
    top = sorted((s for s in r.signals if s.points), key=lambda s: -s.points)[:n]
    if not top:
        return ["No scored signals.", ""]
    return [f"- **{s.title}** (+{s.points}): {s.evidence[0] if s.evidence else ''}" for s in top] + [""]


def _notes(r: Report, h: str = "##") -> List[str]:
    return [f"{h} Notes", ""] + [f"- {n}" for n in r.notes] + [""] if r.notes else []


def to_markdown(r: Report, title: Optional[str] = None) -> str:
    out = [f"# {title or 'Shadow Ship Check: ' + r.query}", ""] + _header(r) + [f"_{DISCLAIMER}_", ""]
    out += ["## Strongest signals", ""] + _summary(r)
    out += ["## Identities", ""] + _identity_table(r) + [""]
    out += ["## Signals", ""] + _signals(r)
    out += _excerpt(r) + _notes(r)
    return "\n".join(out).rstrip() + "\n"


def to_markdown_case(full: Report, before: Report, title: str, case_file: Optional[str] = None) -> str:
    """One report per reference case: the pre-incident view first, then the full data."""
    cats = list(CATEGORIES)
    out = [f"# {title}", ""]
    if case_file:
        out += [f"Case file with context and sources: [{case_file.rsplit('/', 1)[-1]}]({case_file})", ""]
    out += [
        "| | Score | " + " | ".join(CATEGORIES[c][0] for c in cats) + " |",
        "|---|---|" + "---|" * len(cats),
    ]
    for name, r in (("Before the incident", before), ("Full data", full)):
        out.append(f"| {name} | **{r.score} {r.level}** | " + " | ".join(str(r.subscores[c]) for c in cats) + " |")
    out += [""]
    if before.as_of:
        out.append(f"Pre-incident data cut-off: {before.as_of:%Y-%m-%d %H:%M} UTC.  ")
    if full.window:
        out.append(f"Analysis window: {full.window[0]:%Y-%m-%d %H:%M} - {full.window[1]:%Y-%m-%d %H:%M} UTC.  ")
    out += [f"_{DISCLAIMER}_", ""]
    out += ["## Before the incident", "", "What the checks flag using only data recorded before the cut-off:", ""]
    out += _summary(before, 10)
    out += ["## Full data", "", "### Identities", ""] + _identity_table(full) + [""]
    out += ["### Signals", ""] + _signals(full, "###") + _excerpt(full, "###") + _notes(full, "###")
    return "\n".join(out).rstrip() + "\n"


def to_text(r: Report) -> str:
    cut = f" (data until {r.as_of:%Y-%m-%d %H:%M} UTC)" if r.as_of else ""
    lines = [f"Shadow Ship Check - {r.query}", f"Score {r.score}/100 ({r.level}){cut}", f"  {_sub(r)}", ""]
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
        "subscores": r.subscores,
        "window": [w.isoformat() for w in r.window] if r.window else None,
        "as_of": r.as_of.isoformat() if r.as_of else None,
        "identities": [asdict(i) for i in r.identities],
        "signals": [asdict(s) for s in r.signals],
        "notes": r.notes,
    }
    return json.dumps(d, indent=2, default=str)
