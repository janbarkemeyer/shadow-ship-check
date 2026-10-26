"""Re-download the reference fixtures from Global Fishing Watch.

    python scripts/refresh_fixtures.py            # all cases
    python scripts/refresh_fixtures.py eagle_s    # one case

Needs network access to gateway.api.globalfishingwatch.org. Track requests use
the same endpoint as the GFW map; set GFW_API_TOKEN if you have one.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from shadow_ship_check.gfw import GFWClient  # noqa: E402

OUT = Path(__file__).resolve().parents[1] / "data" / "fixtures"


@dataclass
class T:
    key: str
    vessel_id: str
    start: str
    end: str


SPEC = {
    "eagle_s": ("9329760", [T("eagle_s", "0d4db6d94-4ad5-9991-5c80-7b0e71df60d1", "2024-11-01", "2025-03-15")], []),
    "xingshun_39": (
        "8358427",
        [
            T("xingshun_39", "015aaed2a-abb2-12e0-7c7f-7b25909991ab", "2024-12-28", "2025-01-06"),
            # second AIS identity without IMO, found by name search ("SHUNXING39")
            T("shunxing39_cmr", "668c5bda6-65bf-eb02-e8b6-8d081cca1a96", "2024-12-28", "2025-01-06"),
        ],
        ["677087200", "613003889", "750342000", "613003836"],
    ),
    "hong_tai_58": (
        "8357069",
        [
            T("hong_tai_58", "0a93f9cd6-6923-76bb-da5c-7214b017deda", "2025-02-20", "2025-02-26"),
            T("hong_tai_58_dec", "0a93f9cd6-6923-76bb-da5c-7214b017deda", "2024-11-15", "2025-01-15"),
            T("hong_tai_58_imo_identity", "a94da05a1-1beb-f515-bba2-9e616bdfecd3", "2024-11-15", "2024-12-16"),
            T("hongta_8", "5d833022a-a0aa-ee63-532d-80343081c344", "2024-12-14", "2025-01-03"),
            T("hongta8_noimo", "03c114022-24a5-d2a7-f21f-3993a12a567e", "2025-01-04", "2025-02-06"),
        ],
        ["671756000", "677082100", "671666000", "671280000"],
    ),
    "yi_peng_3": ("9224984", [T("yi_peng_3", "c06f00160-0d09-c8e2-4c8a-d81527e023fb", "2024-11-15", "2024-11-21")], []),
    "newnew_polar_bear": (
        "9313204",
        [T("newnew_polar_bear", "39f75936d-d697-c8f5-7603-962fa0c0ad0b", "2023-10-05", "2023-10-10")],
        [],
    ),
    "control_finlandia": (
        "9214379",
        [T("control_finlandia", "728fcd1d9-9227-2f42-3fbc-ada70d3b2fd4", "2024-12-16", "2025-01-04")],
        ["230628000"],
    ),
    "control_yi_peng_5": (
        "9221190",
        [T("control_yi_peng_5", "4c06b7116-6776-2cb2-096c-baf666353141", "2024-11-10", "2024-11-25")],
        ["414388000"],
    ),
    "control_ever_liven": (
        "9595527",
        [T("control_ever_liven", "aa19f9526-605a-c978-0156-a7d02d7599a2", "2025-02-15", "2025-03-05")],
        ["416481000"],
    ),
}


def _day(s: str) -> datetime:
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


def refresh(name: str, client: GFWClient) -> None:
    imo, tracks, mmsis = SPEC[name]
    out = {
        "source": "Global Fishing Watch API (gateway.api.globalfishingwatch.org)",
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "license": "GFW data: CC BY-NC 4.0 - attribution required, non-commercial",
        "query": imo,
        # keep only entries that carry the IMO (search results are fuzzy)
        "identities": [
            e
            for e in client.search_raw(imo)
            if any(x.get("imo") == imo for x in (e.get("selfReportedInfo") or []) + (e.get("registryInfo") or []))
        ],
        "tracks": {},
    }
    for t in tracks:
        pts = client.track(t.vessel_id, _day(t.start), _day(t.end))
        out["tracks"][t.key] = {
            "vessel_id": t.vessel_id,
            "start": t.start,
            "end": t.end,
            "points": [
                [int(p.t.timestamp()), round(p.lat, 5), round(p.lon, 5), round(p.speed, 2), p.segment] for p in pts
            ],
        }
    if mmsis:
        out["mmsi_lookups"] = {m: client.search_raw(m) for m in mmsis}
    (OUT / f"{name}.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"{name}: {sum(len(v['points']) for v in out['tracks'].values())} points")


if __name__ == "__main__":
    client = GFWClient()
    for n in sys.argv[1:] or list(SPEC):
        refresh(n, client)
