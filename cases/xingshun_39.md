# Case file: Xingshun 39 / Shunxing 39: Keelung, 3 January 2025

| | |
|---|---|
| Incident | Damage to an international telecom cable north of Keelung / Yehliu, Taiwan |
| Reported | 3 Jan 2025, 12:40 (UTC+8), Chunghwa Telecom to the Coast Guard Administration (CGA) |
| Status | Suspected. The CGA intercepted the ship but could not board in rough seas; it continued to Busan, and Taiwan asked South Korea for help collecting evidence. |
| Hull | IMO 8358427, cargo ship, Hong Kong-based owner (per CGA) |
| Tool result | 100 HIGH before the incident, 100 with full data ([report](../reports/xingshun_39.md)) |

## Identities in Global Fishing Watch

| Name | Flag | MMSI | AIS period | Registry-confirmed |
|---|---|---|---|---|
| BAOLONG36 | Guyana | 750342000 | 17–24 Nov 2022; 29 Nov 2022 to 12 May 2023 | no |
| BAOLONG36 | Cameroon | 613003836 | 24 Nov 2022 to 10 Feb 2023; 20 Jul to 11 Sep 2023 | no |
| XINGSHUN39 | Tanzania | 677087200 | Mar 2024 to Jan 2025 (one more message Aug 2025) | no |
| SHUNXING39 | Cameroon | 613003889 | Sep 2024 to 3 Jan 2025 | no, no IMO broadcast |

The fourth identity is not linked to the IMO in the bundled GFW search. It turns up in a separate
name search because the two syllables are swapped (XING-SHUN / SHUN-XING). The case links it manually;
the CLI does not discover that spelling variant automatically. Taiwan News reported the CGA's
description of registrations as "Shun Xing 39" in Cameroon and "Xing Shun 39" in Tanzania, with two AIS
systems ([7 Jan 2025](https://www.taiwannews.com.tw/news/6009265)). This later account supports the
association but would not have been available for a warning before the incident.

## What the tracks show

* The last GFW position for XINGSHUN39 (Tanzania) before a gap is on 28 Dec 2024 at 22:11 UTC just off
  Keelung (25.16 N, 121.75 E). 4.5 hours later SHUNXING39 (Cameroon, no IMO) sends its first position after more than
  a day of silence, 26 nm further north. On 3 Jan 2025 SHUNXING39 sends its last position at 08:19 UTC at 25.334 N, 121.712 E;
  at 08:52 UTC GFW records XINGSHUN39 again, 0.2 nm from the same spot. The sequence is consistent
  with a handover but does not independently establish the physical hull or transponder settings.
* The damage was reported on 3 Jan at 04:40 UTC (12:40 local). The bundled Tanzania-identity track has
  no positions from 28 Dec 22:11 until 3 Jan 08:52 UTC. GFW records the IMO-less SHUNXING39 during
  parts of that interval; this does not establish continuous transmission or the exact damage time.
  On 2 Jan that identity lay almost still at 25.66 N, 122.06 E (06:13–13:51 UTC),
  then moved south-west towards Keelung in short legs of up to 5 kn, and from 22:57 UTC on 2 Jan to
  05:07 UTC on 3 Jan crept 5.8 nm at a mean 1.0 kn (from 25.40 N, 121.81 E). On the way it crossed a
  telecom cable mapped in OpenStreetMap (unnamed there) between 23:42 UTC on 2 Jan and 00:04 UTC on 3 Jan at
  1.9 kn, about 14 nm north of Keelung. Whether this is the damaged cable is not known.
* After XINGSHUN39 reappears in GFW, its track zig-zags north of Keelung for hours (15.2 nm sailed for 3.1 nm net
  between 08:52 and 14:32 UTC), mostly at 0–5 kn; around 21:00 UTC it was making 1–2.5 kn.
* GFW has no position for either identity between 29 Dec 20:07 UTC and 31 Dec 14:07 UTC (42 h).
* BAOLONG36 has overlapping first/last dates under Guyana and Cameroon flags from 29 Nov 2022 to 10 Feb 2023
  in 2022/23. Those dates alone do not establish continuous parallel use.

My initial manual search found no GFW loitering events for this ship. I have not established which
model settings or data coverage explain the difference. This tool's slow-movement and zig-zag
checks use separate rules and have no distance-from-shore limit.

## Warning signals (tool)

`MULTI_IDENTITY` (four name/flag combinations), `FLAG_CHANGE` (Guyana → Cameroon and Cameroon → Tanzania), `NO_REGISTRY`,
`IMO_HIDDEN`, `CONCURRENT_IDENTITIES` (twice), `IDENTITY_HANDOVER`, `AIS_GAP`, `SLOW_LOITERING`, `ZIGZAG`,
`CABLE_CROSSING_SLOW` (the crossing above, and four more by XINGSHUN39 on 3 Jan).

## Open questions

1. Exact time and position of the cable fault. The 23:40 UTC reference in the report is inferred from
   "had left about nine hours earlier" in CGA statements and may be off by hours; the conclusion above
   does not depend on it.
2. Which cable was damaged (reports mention the TPE cable and a four-core cable near Yehliu), and is it
   the unnamed route in OpenStreetMap?
3. Is the Cameroon registration of SHUNXING39 real or fraudulent? Check the Cameroon registry / IMO GISIS.
4. Check the overlapping BAOLONG36 records under Guyana and Cameroon flags in 2022/23 against tracks
   or registration records; the name is the same and the flags differ.

## Sources

* GFW vessel search and tracks (fixture `data/fixtures/xingshun_39.json`, fetched 26 Oct 2026)
* [Taiwan News, 7 Jan 2025](https://www.taiwannews.com.tw/news/6009265): two registrations, two AIS systems, boarding not possible
* [CNA via GlobalSecurity, 4 Jan 2025](https://www.globalsecurity.org/wmd/library/news/taiwan/2025/taiwan-250104-cna01.htm): report time, interception 7 nm north of Yehliu
