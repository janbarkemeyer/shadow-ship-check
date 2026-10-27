"""Sample comparison of the identity rules: sanctioned vessels vs. sampled controls.

Each record in the evaluation file holds the raw GFW identity search results for one hull
(plus the MMSI and name look-ups that ``ssc check`` would make) and a reference date:

* ``sanctioned`` - vessels designated under the UK Russia sanctions regime; reference date =
  designation date, so only identity history recorded *before* the designation counts;
* ``control`` - random IMO numbers drawn with the same IMO-prefix (≈ build year) mix, not on
  the UK list, each with a reference date drawn from the positives' designation dates.

Only the identity checks run (there is no track). The ``SANCTIONED`` watchlist check is off -
otherwise the test would be circular. NAME_ON_OTHER_MMSI was revised after
inspecting sanctioned vessels; this is not an untouched validation set.
"""

from __future__ import annotations

import gzip
import json
import random
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Dict, List, Sequence, Tuple

from . import data_path
from .analyze import clip_identities, identity_signals
from .gfw import identities_from_entries
from .models import CATEGORIES, CATEGORY_OF, normalize_name

BUNDLED = data_path() / "eval" / "uk_sanctions_vs_random.json.gz"
LEVELS = (("HIGH", 50), ("MEDIUM", 20))
INTERPRETATION = (
    "This compares identity-rule scores for the supplied labels; it does not predict cable incidents. "
    "The SANCTIONED check is off. Timestamp filtering retains snapshot identity links, registry matches "
    "and fixed flag weights; it does not reconstruct past knowledge. "
    "The bootstrap interval does not account for selection bias or dependence between related vessels."
)
REVIEWED_SAMPLE_NOTE = "The bundled sample was reviewed during development and is not an untouched holdout."
CONTEXT_FIELDS = ("title", "collected", "source", "licence")


def load(path: Path = BUNDLED) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def _ref(s: str) -> datetime:
    if not isinstance(s, str) or not s.strip():
        raise ValueError("Evaluation as_of must be an ISO date or timestamp string")
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def _validate_record(rec: dict) -> None:
    if not isinstance(rec, dict):
        raise ValueError("Evaluation records must be objects")
    if not isinstance(rec.get("imo"), str) or not re.fullmatch(r"[0-9]{7}", rec["imo"]):
        raise ValueError("Evaluation IMO must be a seven-digit string")
    _ref(rec.get("as_of"))
    if not isinstance(rec.get("identities"), list):
        raise ValueError("Evaluation identities must be a list")
    for field in ("mmsi_lookups", "name_lookups"):
        value = rec.get(field)
        if value is not None and (
            not isinstance(value, dict) or any(not isinstance(key, str) or not key.strip() for key in value)
        ):
            raise ValueError(f"Evaluation {field} must be an object with non-empty string keys")


def _entries(entries: list, dedupe: bool = True) -> list:
    identities = identities_from_entries(entries, dedupe=dedupe)
    if entries and not any(i.name or i.mmsi or i.imo for i in identities):
        raise ValueError("Non-empty evaluation response contains no recognized identity records")
    return identities


def _score_record(rec: dict) -> Tuple[int, Dict[str, int], bool]:
    _validate_record(rec)
    ref = _ref(rec["as_of"])
    own = [i for i in _entries(rec["identities"]) if not i.imo or i.imo == rec["imo"]]
    if rec["identities"] and not own:
        raise ValueError("Evaluation response has no identity compatible with the requested IMO")
    identities = clip_identities(own, ref)
    unavailable_at_reference = not identities
    lookups = {
        m: [i for i in _entries(e, dedupe=False) if i.mmsi == m] for m, e in (rec.get("mmsi_lookups") or {}).items()
    }
    # Name lookups can reveal MMSIs that were not looked up directly.
    direct_mmsis = set(lookups)
    for name, entries in (rec.get("name_lookups") or {}).items():
        for i in _entries(entries, dedupe=False):
            if i.mmsi and i.mmsi not in direct_mmsis and i.key[0] == normalize_name(name):
                lookups.setdefault(i.mmsi, []).append(i)
    lookups = {m: clip_identities(v, ref) for m, v in lookups.items()}
    _, sigs = identity_signals(identities, lookups, ref, sanctions_list=None)
    points: Dict[str, int] = Counter()
    for signal in sigs:
        points[signal.code] += signal.points
    return min(100, sum(points.values())), dict(points), unavailable_at_reference


def score_record(rec: dict) -> Tuple[int, Dict[str, int]]:
    """Identity-only score at the reference date; returns score and points by code."""
    score, points, _ = _score_record(rec)
    return score, points


def auc(pos: Sequence[float], neg: Sequence[float]) -> float:
    """Probability that a random positive scores higher than a random negative (ties count half).

    Computed from ranks (Mann-Whitney U), so the bootstrap stays fast."""
    if not pos or not neg:
        raise ValueError("AUC requires observations in both groups")
    values = sorted([(v, 1) for v in pos] + [(v, 0) for v in neg])
    rank_sum, i = 0.0, 0
    while i < len(values):
        j = i
        while j < len(values) and values[j][0] == values[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2  # ranks i+1 .. j share their average
        rank_sum += avg_rank * sum(flag for _, flag in values[i:j])
        i = j
    n_p, n_n = len(pos), len(neg)
    return (rank_sum - n_p * (n_p + 1) / 2) / (n_p * n_n)


def bootstrap_auc(
    pos: Sequence[float], neg: Sequence[float], n: int = 1000, seed: int = 20261026
) -> Tuple[float, float]:
    if n < 40:
        raise ValueError("At least 40 bootstrap samples are required")
    rnd = random.Random(seed)
    vals = sorted(auc([rnd.choice(pos) for _ in pos], [rnd.choice(neg) for _ in neg]) for _ in range(n))
    return vals[int(0.025 * n)], vals[int(0.975 * n) - 1]


def evaluate(data: dict, *, reviewed_sample: bool = False) -> dict:
    if not isinstance(data, dict) or not isinstance(data.get("records"), list):
        raise ValueError("Evaluation data must be an object with a records list")
    if "meta" in data and (
        not isinstance(data["meta"], dict)
        or any(field in data["meta"] and not isinstance(data["meta"][field], str) for field in CONTEXT_FIELDS)
    ):
        raise ValueError("Evaluation meta must be an object; title, collected, source and licence must be strings")
    groups: Dict[str, List[Tuple[int, Dict[str, int]]]] = {"sanctioned": [], "control": []}
    seen = set()
    for rec in data["records"]:
        if not isinstance(rec, dict):
            raise ValueError("Evaluation records must be objects")
        if not isinstance(rec.get("label"), str) or rec["label"] not in groups:
            raise ValueError(f"Unknown evaluation label: {rec.get('label')!r}")
        if not isinstance(rec.get("imo"), str):
            raise ValueError("Evaluation IMO must be a seven-digit string")
        if rec["imo"] in seen:
            raise ValueError(f"Duplicate IMO in evaluation: {rec['imo']}")
        seen.add(rec["imo"])
    missing = 0
    unavailable = {label: 0 for label in groups}
    for rec in data["records"]:
        score, points, no_identity_at_reference = _score_record(rec)
        if not rec["identities"]:
            missing += 1
            continue
        groups[rec["label"]].append((score, points))
        unavailable[rec["label"]] += int(no_identity_at_reference)
    pos = [s for s, _ in groups["sanctioned"]]
    neg = [s for s, _ in groups["control"]]
    out = {
        "n": {k: len(v) for k, v in groups.items()},
        "missing": missing,
        "unavailable_at_reference": unavailable,
        "interpretation": INTERPRETATION + (" " + REVIEWED_SAMPLE_NOTE if reviewed_sample else ""),
        "auc": auc(pos, neg),
        "auc_ci95": bootstrap_auc(pos, neg),
        "median": {"sanctioned": median(pos), "control": median(neg)},
        "levels": {},
        "signals": {},
        "categories": {},
    }
    context = {field: data["meta"][field] for field in CONTEXT_FIELDS if field in data.get("meta", {})}
    if context:
        out["dataset_context"] = {"description": "Input snapshot metadata, not independently verified", **context}
    for name, cut in LEVELS:
        tp = sum(s >= cut for s in pos)
        fp = sum(s >= cut for s in neg)
        out["levels"][name] = {
            "threshold": cut,
            "sanctioned_flagged": tp / len(pos),
            "controls_flagged": fp / len(neg),
        }
    codes = sorted({c for g in groups.values() for _, p in g for c, v in p.items() if v}, key=_code_order)
    for c in codes:
        out["signals"][c] = {k: sum(1 for _, p in g if p.get(c)) / len(g) for k, g in groups.items()}
    for cat in ("identity", "registry"):  # no tracks here, so no behaviour signals

        def sub(points, cat=cat):
            return min(100, sum(v for c, v in points.items() if CATEGORY_OF.get(c) == cat))

        out["categories"][cat] = {
            **{k: sum(1 for _, p in g if sub(p)) / len(g) for k, g in groups.items()},
            "auc": auc([sub(p) for _, p in groups["sanctioned"]], [sub(p) for _, p in groups["control"]]),
        }
    return out


def _code_order(code: str) -> int:
    from .signals import ALL_CODES

    return ALL_CODES.index(code) if code in ALL_CODES else 99


def to_text(r: dict, meta: dict) -> str:
    pct = "{:.0%}".format
    lines = [
        f"Evaluation: {meta.get('title', '')}",
        f"  {r['n']['sanctioned']} sanctioned vessels, {r['n']['control']} controls"
        + (f" ({r['missing']} records without GFW identity skipped)" if r["missing"] else ""),
        "  identity checks only, at each vessel's reference date; SANCTIONED check off",
        "",
        f"AUC {r['auc']:.2f} (95% CI {r['auc_ci95'][0]:.2f}-{r['auc_ci95'][1]:.2f}); "
        f"median score {r['median']['sanctioned']:g} vs {r['median']['control']:g}",
        "",
        f"{'':28}{'sanctioned':>12}{'controls':>10}",
    ]

    def row(label, a, b):
        lines.append(f"{label:28}{pct(a):>12}{pct(b):>10}")

    for name, v in r["levels"].items():
        row(f"score >= {v['threshold']} ({name})", v["sanctioned_flagged"], v["controls_flagged"])
    lines.append("")
    for cat, v in r["categories"].items():
        row(f"any {CATEGORIES[cat][0].lower()} signal", v["sanctioned"], v["control"])
        lines[-1] += f"   (AUC of this group alone {v['auc']:.2f})"
    lines.append("")
    for code, v in r["signals"].items():
        row(code, v["sanctioned"], v["control"])
    if any(r["unavailable_at_reference"].values()):
        missing_at_ref = r["unavailable_at_reference"]
        lines += [
            "",
            "No compatible identity remains after timestamp filtering: "
            f"{missing_at_ref['sanctioned']} sanctioned, {missing_at_ref['control']} control. "
            "These records remain in the sample with score 0; this is a data gap, not an ordinary-history finding.",
        ]
    if r.get("dataset_context"):
        context = r["dataset_context"]
        lines += ["", context["description"] + ":"]
        lines += [f"  {field}: {context[field]}" for field in CONTEXT_FIELDS if field in context]
    lines += ["", r["interpretation"]]
    return "\n".join(lines)
