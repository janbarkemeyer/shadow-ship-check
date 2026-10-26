"""Sanctions watchlist: vessels designated under the UK sanctions regimes.

The bundled list (``data/sanctions/uk_vessels.csv``) comes from the UK Sanctions List
(FCDO, Open Government Licence v3.0) via OpenSanctions (CC BY-NC 4.0). A designation is
an official decision, not an indicator - but only designations made *before* the
reference date count, so a pre-incident view never sees later listings.
"""

from __future__ import annotations

import csv
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional

from . import data_path
from .models import Identity, Signal

BUNDLED = data_path() / "sanctions" / "uk_vessels.csv"
REGIME = {"Russia": "Russia regime", "DPRK": "DPRK regime", "Libya": "Libya regime"}


def load(path: Path = BUNDLED) -> Dict[str, dict]:
    with open(path, encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out: Dict[str, dict] = {}
    for r in rows:
        r["designated"] = datetime.fromisoformat(r["designated"]).replace(tzinfo=timezone.utc)
        if r["imo"] not in out or r["designated"] < out[r["imo"]]["designated"]:
            out[r["imo"]] = r
    return out


def sanctions(identities: List[Identity], ref: Optional[datetime], listing: Optional[Dict[str, dict]]) -> List[Signal]:
    if not listing:
        return []
    imos = sorted({i.imo for i in identities if i.imo})
    hits = [listing[m] for m in imos if m in listing]
    if not hits:
        return []
    before = [h for h in hits if ref is None or h["designated"] <= ref]
    later = [h for h in hits if h not in before]

    def line(h):
        regime = REGIME.get(h["regime"], h["regime"])
        return f"IMO {h['imo']} ({h['name']}): UK designation {h['designated']:%Y-%m-%d}, {regime}"

    sigs = []
    if before:
        sigs.append(Signal("SANCTIONED", "Hull on the UK sanctions list", 20, [line(h) for h in before]))
    if later:
        sigs.append(
            Signal(
                "SANCTIONED",
                "Hull added to the UK sanctions list after the reference date",
                0,
                [line(h) for h in later],
                "Listed for context only: the designation was not known at the reference date.",
            )
        )
    return sigs
