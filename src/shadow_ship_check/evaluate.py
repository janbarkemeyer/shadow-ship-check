"""Out-of-sample check of the identity rules: sanctioned shadow-fleet vessels vs. random ships.

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
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from typing import Dict, List, Sequence, Tuple

from .analyze import clip_identities, identity_signals
from .gfw import identities_from_entries
from .models import CATEGORIES, CATEGORY_OF, normalize_name

BUNDLED = Path(__file__).resolve().parents[2] / "data" / "eval" / "uk_sanctions_vs_random.json.gz"
LEVELS = (("HIGH", 50), ("MEDIUM", 20))


def load(path: Path = BUNDLED) -> dict:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        return json.load(fh)


def _ref(s: str) -> datetime:
    dt = datetime.fromisoformat(s.replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc) if dt.tzinfo else dt.replace(tzinfo=timezone.utc)


def score_record(rec: dict) -> Tuple[int, Dict[str, int]]:
    """Identity-only score of one hull at its reference date; returns (score, points per signal code)."""
    ref = _ref(rec["as_of"])
    identities = clip_identities(identities_from_entries(rec["identities"]), ref)
    lookups = {
        m: [i for i in identities_from_entries(e, dedupe=False) if i.mmsi == m]
        for m, e in (rec.get("mmsi_lookups") or {}).items()
    }
    # name look-ups: the hull's names broadcast under MMSIs that were not looked up directly
    direct_mmsis = set(lookups)
    for name, entries in (rec.get("name_lookups") or {}).items():
        for i in identities_from_entries(entries, dedupe=False):
            if i.mmsi and i.mmsi not in direct_mmsis and i.key[0] == normalize_name(name):
                lookups.setdefault(i.mmsi, []).append(i)
    lookups = {m: clip_identities(v, ref) for m, v in lookups.items()}
    _, sigs = identity_signals(identities, lookups, ref, sanctions_list=None)
    points: Dict[str, int] = Counter()
    for s in sigs:
        points[s.code] += s.points
    return min(100, sum(points.values())), dict(points)


def auc(pos: Sequence[float], neg: Sequence[float]) -> float:
    """Probability that a random positive scores higher than a random negative (ties count half).

    Computed from ranks (Mann-Whitney U), so the bootstrap stays fast."""
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
    rnd = random.Random(seed)
    vals = sorted(auc([rnd.choice(pos) for _ in pos], [rnd.choice(neg) for _ in neg]) for _ in range(n))
    return vals[int(0.025 * n)], vals[int(0.975 * n) - 1]


def evaluate(data: dict) -> dict:
    groups: Dict[str, List[Tuple[int, Dict[str, int]]]] = {"sanctioned": [], "control": []}
    for rec in data["records"]:
        if rec["identities"]:
            groups["sanctioned" if rec["label"] == "sanctioned" else "control"].append(score_record(rec))
    pos = [s for s, _ in groups["sanctioned"]]
    neg = [s for s, _ in groups["control"]]
    out = {
        "n": {k: len(v) for k, v in groups.items()},
        "missing": sum(1 for r in data["records"] if not r["identities"]),
        "auc": auc(pos, neg),
        "auc_ci95": bootstrap_auc(pos, neg),
        "median": {"sanctioned": median(pos), "control": median(neg)},
        "levels": {},
        "signals": {},
        "categories": {},
    }
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
        f"  {r['n']['sanctioned']} sanctioned vessels, {r['n']['control']} random controls"
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
    return "\n".join(lines)
