# Case file: Xingshun 39 / Shunxing 39 – Keelung, 3 January 2025

| | |
|---|---|
| Incident | Damage to an international telecom cable north of Keelung / Yehliu, Taiwan |
| Reported | 3 Jan 2025, 12:40 (UTC+8), Chunghwa Telecom to the Coast Guard Administration (CGA) |
| Status | **Suspected**. The CGA intercepted the ship but could not board in rough seas; it continued to Busan, and Taiwan asked South Korea for help collecting evidence. |
| Hull | IMO 8358427, cargo ship, Hong Kong-based owner (per CGA) |
| Tool result | **100 HIGH before the incident**, 100 with full data ([report](../reports/xingshun_39.md)) |

## Identities in Global Fishing Watch

| Name | Flag | MMSI | AIS period | Registry-confirmed |
|---|---|---|---|---|
| BAOLONG36 | Guyana | 750342000 | Nov 2022 – May 2023 | no |
| BAOLONG36 | Cameroon | 613003836 | Nov 2022 – Sep 2023 | no |
| XINGSHUN39 | Tanzania | 677087200 | Mar 2024 – Jan 2025 (one more message Aug 2025) | no |
| **SHUNXING39** | **Cameroon** | **613003889** | **Sep 2024 – 3 Jan 2025** | no, **no IMO broadcast** |

The fourth identity is not linked to the IMO in GFW. It turns up in a name search because the
two syllables are simply swapped (XING-SHUN / SHUN-XING). The CGA confirmed afterwards that the
ship was registered as "Shun Xing 39" in Cameroon and "Xing Shun 39" in Tanzania and used two AIS
systems ([Taiwan News, 7 Jan 2025](https://www.taiwannews.com.tw/news/6009265)).

## What the tracks show

* **Identity swap at sea.** XINGSHUN39 (Tanzania) goes silent on 28 Dec 2024 at 22:11 UTC just off
  Keelung (25.16 N, 121.75 E). 4.5 hours later SHUNXING39 (Cameroon, no IMO) sends its first position after more than
  a day of silence, 26 nm further north. On 3 Jan 2025 SHUNXING39 sends its last position at 08:19 UTC at 25.334 N, 121.712 E;
  at 08:52 UTC XINGSHUN39 is back on air **0.2 nm from the same spot**.
* **Around the damage, only the IMO-less identity was transmitting.** The damage was reported on 3 Jan at
  04:40 UTC (12:40 local). The Tanzania identity was silent from 28 Dec 22:11 until 3 Jan 08:52 UTC, so
  whenever exactly the cable was hit in those days, the ship was either dark or visible only as the
  IMO-less SHUNXING39. On 2 Jan that identity lay almost still at 25.66 N, 122.06 E (06:13–13:51 UTC),
  then moved south-west towards Keelung in short legs of up to 5 kn, and from 22:57 UTC on 2 Jan to
  05:07 UTC on 3 Jan crept 5.8 nm at a mean 1.0 kn (from 25.40 N, 121.81 E). On the way it crossed a
  telecom cable mapped in OpenStreetMap (unnamed there) between 23:42 UTC on 2 Jan and 00:04 UTC on 3 Jan at
  1.9 kn, about 14 nm north of Keelung. Whether this is the damaged cable is not known.
* After the swap back, XINGSHUN39 zig-zags north of Keelung for hours (15.2 nm sailed for 3.1 nm net
  between 08:52 and 14:32 UTC), mostly at 0–5 kn; around 21:00 UTC it was making 1–2.5 kn.
* Neither identity sent a position between 29 Dec 20:07 UTC and 31 Dec 14:07 UTC (42 h).
* The same pattern existed in 2022/23: BAOLONG36 broadcast as Guyana and Cameroon in parallel for five
  months.

Our first manual check found 0 loitering events in GFW for this ship; GFW's loitering model only
looks at activity more than 20 nm from shore (to be confirmed in GFW's documentation). The tool's
slow-movement and zig-zag checks have no distance limit.

## Warning signals (tool)

`MULTI_IDENTITY` (4), `FLAG_CHANGE` (Cameroon → Tanzania, both on the Paris MoU black list), `NO_REGISTRY`,
`IMO_HIDDEN`, `CONCURRENT_IDENTITIES` (twice), `IDENTITY_HANDOVER`, `AIS_GAP`, `SLOW_LOITERING`, `ZIGZAG`,
`CABLE_CROSSING_SLOW` (the crossing above, and four more by XINGSHUN39 on 3 Jan).

## Open questions

1. Exact time and position of the cable fault. The 23:40 UTC reference in the report is inferred from
   "had left about nine hours earlier" in CGA statements and may be off by hours; the conclusion above
   does not depend on it.
2. Which cable was damaged (reports mention the TPE cable and a four-core cable near Yehliu), and is it
   the unnamed route in OpenStreetMap?
3. Is the Cameroon registration of SHUNXING39 real or fraudulent? Check the Cameroon registry / IMO GISIS.
4. GFW lists BAOLONG36 under both Guyana and Cameroon flags in 2022/23 – same pattern, different names.

## Sources

* GFW vessel search and tracks (fixture `data/fixtures/xingshun_39.json`, fetched 26 Oct 2026)
* [Taiwan News, 7 Jan 2025](https://www.taiwannews.com.tw/news/6009265) – two registrations, two AIS systems, boarding not possible
* [CNA via GlobalSecurity, 4 Jan 2025](https://www.globalsecurity.org/wmd/library/news/taiwan/2025/taiwan-250104-cna01.htm) – report time, interception 7 nm north of Yehliu
