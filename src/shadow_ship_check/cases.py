"""Metadata for the reference incidents (case files live in /cases)."""

from __future__ import annotations

from datetime import datetime, timezone


def _utc(s: str) -> datetime:
    return datetime.fromisoformat(s).replace(tzinfo=timezone.utc)


CASES = {
    "eagle_s": {
        "title": "Eagle S - Estlink 2 and telecom cables, Gulf of Finland",
        "imo": "9329760",
        "incident": "2024-12-25",
        "region": "Baltic Sea (Gulf of Finland)",
        "status": "Suspected. Finland charged the captain and two officers; in Oct 2025 the "
        "Helsinki District Court dismissed the case for lack of jurisdiction (appeal possible).",
        "window": (_utc("2024-12-23T00:00"), _utc("2024-12-28T23:59")),
        "primary_track": "eagle_s",
        "incident_time": _utc("2024-12-25T10:26"),
        "parallel": [],
    },
    "xingshun_39": {
        "title": "Xingshun 39 (Shunxing 39) - TPE cable north of Keelung",
        "imo": "8358427",
        "incident": "2025-01-03",
        "region": "Taiwan (north coast, Keelung)",
        "status": "Suspected. Taiwan's coast guard intercepted the ship but could not board it in rough seas; "
        "it was then allowed to continue to South Korea.",
        "window": (_utc("2025-01-02T00:00"), _utc("2025-01-05T00:00")),
        "primary_track": "xingshun_39",
        "parallel": ["xingshun_39", "shunxing39_cmr"],
        "movement_tracks": ["shunxing39_cmr"],
        # CGA: ship had left the damage area ~9 h before the 16:40 (UTC+8) interception
        # on 3 Jan -> damage around 07:40 local = 23:40 UTC on 2 Jan (approximate)
        "incident_time": _utc("2025-01-02T23:40"),
        "linked_mmsis": ["613003889"],
        "track_labels": {
            "xingshun_39": "XINGSHUN39/TZA/677087200",
            "shunxing39_cmr": "SHUNXING39/CMR/613003889 (no IMO)",
        },
    },
    "hong_tai_58": {
        "title": "Hong Tai 58 - TPKM-3 cable Taiwan-Penghu",
        "imo": "8357069",
        "incident": "2025-02-25",
        "region": "Taiwan Strait (Taiwan-Penghu)",
        "status": "Captain convicted by the Tainan District Court (June 2025, 3 years) for "
        "intentionally damaging the cable (first instance).",
        "window": (_utc("2025-02-22T00:00"), _utc("2025-02-26T00:00")),
        "primary_track": "hong_tai_58",
        "incident_time": _utc("2025-02-24T19:03"),
        "parallel": ["hong_tai_58_dec", "hong_tai_58_imo_identity", "hongta_8", "hongta8_noimo"],
        "track_labels": {
            "hong_tai_58_dec": "HONGTAI58/671756000 (no IMO)",
            "hong_tai_58_imo_identity": "HONGTAI58/671756000 (IMO 8357069)",
            "hongta_8": "HONGTA 8/677082100 (IMO 8357069)",
            "hongta8_noimo": "HONGTA8/677082100 (no IMO)",
        },
    },
    "yi_peng_3": {
        "title": "Yi Peng 3 - BCS East-West Interlink and C-Lion1, Baltic Sea",
        "imo": "9224984",
        "incident": "2024-11-17/18",
        "region": "Baltic Sea (Gotland - Bornholm)",
        "status": "Suspected. No charges; Swedish prosecutors were not allowed on board, and US officials "
        "were reported to assess the damage as accidental.",
        "window": (_utc("2024-11-16T12:00"), _utc("2024-11-18T18:00")),
        "primary_track": "yi_peng_3",
        "incident_time": _utc("2024-11-18T02:00"),
        "parallel": [],
    },
    "newnew_polar_bear": {
        "title": "NewNew Polar Bear - Balticconnector gas pipeline and telecom cables",
        "imo": "9313204",
        "incident": "2023-10-08",
        "region": "Baltic Sea (Gulf of Finland)",
        "status": "Suspected. Finnish investigators matched the recovered anchor to the ship; in Aug 2024 a "
        "Chinese investigation acknowledged the damage but called it an accident in a storm.",
        "window": (_utc("2023-10-07T12:00"), _utc("2023-10-08T06:00")),
        "primary_track": "newnew_polar_bear",
        "incident_time": _utc("2023-10-07T22:20"),
        "parallel": [],
    },
}


# Control vessels: ordinary ships in the same waters and time windows. They are
# used to check that the score does not simply flag every ship.
CONTROLS = {
    "control_finlandia": {
        "title": "Control: Finlandia (Helsinki-Tallinn ferry), Gulf of Finland",
        "imo": "9214379",
        "region": "Baltic Sea (Gulf of Finland)",
        "window": (_utc("2024-12-23T00:00"), _utc("2024-12-28T23:59")),
        "primary_track": "control_finlandia",
        "parallel": [],
    },
    "control_yi_peng_5": {
        "title": "Control: Yi Peng 5 (sister ship of Yi Peng 3, same operator)",
        "imo": "9221190",
        "region": "varies",
        "window": (_utc("2024-11-16T12:00"), _utc("2024-11-18T18:00")),
        "primary_track": "control_yi_peng_5",
        "parallel": [],
    },
    "control_ever_liven": {
        "title": "Control: Ever Liven (Taiwan-flagged container ship)",
        "imo": "9595527",
        "region": "varies",
        "window": (_utc("2025-02-22T00:00"), _utc("2025-02-26T00:00")),
        "primary_track": "control_ever_liven",
        "parallel": [],
    },
}

ALL = {**CASES, **CONTROLS}
