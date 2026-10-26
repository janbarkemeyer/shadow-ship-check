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
        "status": "Suspected involvement. On 27 Aug 2026, the Helsinki Court of Appeal overturned "
        "the jurisdiction dismissal and returned the case to the district court. This was not a finding of guilt.",
        "window": (_utc("2024-12-23T00:00"), _utc("2024-12-28T23:59")),
        "primary_track": "eagle_s",
        # data cut-off for the pre-incident score: Estlink 2 failure
        "as_of": _utc("2024-12-25T10:26"),
        "incident_time": _utc("2024-12-25T10:26"),
        "parallel": [],
    },
    "xingshun_39": {
        "title": "Xingshun 39 (Shunxing 39) - cable damage north of Keelung",
        "imo": "8358427",
        "incident": "2025-01-03",
        "region": "Taiwan (north coast, Keelung)",
        "status": "Suspected. Taiwan's coast guard intercepted the ship but could not board it in rough seas; "
        "it was then allowed to continue to South Korea.",
        "window": (_utc("2025-01-02T00:00"), _utc("2025-01-05T00:00")),
        "primary_track": "xingshun_39",
        # Conservative comparison cut-off, earlier than the report and approximate incident time.
        # The CGA received the damage report at 04:40 UTC on 3 Jan; it is not the damage time.
        "as_of": _utc("2025-01-02T12:00"),
        "parallel": ["xingshun_39", "shunxing39_cmr"],
        "movement_tracks": ["shunxing39_cmr"],
        # CGA: ship had left the damage area ~9 h before the 16:40 (UTC+8) interception
        # on 3 Jan -> damage around 07:40 local = 23:40 UTC on 2 Jan (approximate)
        "incident_time": _utc("2025-01-02T23:40"),
        "linked_mmsis": ["613003889"],
        "notes": ["SHUNXING39 without IMO is linked manually using later name and track evidence."],
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
        "status": "The Tainan District Court's first-instance judgment of 12 Jun 2025 imposed a three-year "
        "sentence for damaging the cable with conditional intent. "
        "On 29 Aug 2025, the Tainan Branch of the Taiwan High Court dismissed the prosecution's sentence appeal "
        "and upheld the sentence. Further appeal was allowed; later finality is not established here.",
        "window": (_utc("2025-02-22T00:00"), _utc("2025-02-26T00:00")),
        "primary_track": "hong_tai_58",
        # data cut-off for the pre-incident score: 00:00 local on 25 Feb; the break was reported for the early morning
        "as_of": _utc("2025-02-24T16:00"),
        "incident_time": _utc("2025-02-24T19:03"),
        "notes": ["Linked identities may belong to multiple physical hulls; the score describes an identity cluster."],
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
        "status": "Suspected involvement. Public reporting on the Swedish investigation does not establish "
        "whether an anchor drag was deliberate. Swedish prosecutors were not allowed on board.",
        "window": (_utc("2024-11-16T12:00"), _utc("2024-11-18T18:00")),
        "primary_track": "yi_peng_3",
        # data cut-off for the pre-incident score: BCS East-West Interlink cut around 10:00 local (EET)
        "as_of": _utc("2024-11-17T08:00"),
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
        # data cut-off for the pre-incident score: about two hours before the approximate rupture time
        "as_of": _utc("2023-10-07T20:00"),
        "incident_time": _utc("2023-10-07T22:20"),
        "parallel": [],
    },
}


# Illustrative controls in the incident time windows. Only Finlandia is in its
# incident comparison region; these are not matched passages over the same cables.
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
        "title": "Control: Yi Peng 5 (comparison vessel near Taiwan)",
        "imo": "9221190",
        "region": "Taiwan Strait (near Fujian)",
        "notes": ["This control is near Taiwan, outside the Baltic incident region; its cut-off is the window end."],
        "window": (_utc("2024-11-16T12:00"), _utc("2024-11-18T18:00")),
        "primary_track": "control_yi_peng_5",
        "parallel": [],
    },
    "control_ever_liven": {
        "title": "Control: Ever Liven (Taiwan-flagged container ship)",
        "imo": "9595527",
        "region": "Western Pacific",
        "notes": [
            "This control is in the western Pacific, outside the Taiwan incident region; its cut-off is the window end."
        ],
        "window": (_utc("2025-02-22T00:00"), _utc("2025-02-26T00:00")),
        "primary_track": "control_ever_liven",
        "parallel": [],
    },
}

ALL = {**CASES, **CONTROLS}
