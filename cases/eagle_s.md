# Case file: Eagle S: Estlink 2 and telecom cables, Gulf of Finland, 25 December 2024

| | |
|---|---|
| Incident | Estlink 2 power cable (Finland–Estonia) failed at 12:26 EET (10:26 UTC); telecom cables in the area were damaged too |
| Status | Suspected involvement. The Helsinki District Court declined jurisdiction on 3 Oct 2025. On 27 Aug 2026, the Helsinki Court of Appeal overturned that decision and returned the case to the district court. That ruling concerns jurisdiction, not guilt. |
| Hull | IMO 9329760, oil products tanker, Cook Islands flag, linked to Russia's "shadow fleet" in reporting |
| Tool result | 50 HIGH before the incident, 55 HIGH with full data ([report](../reports/eagle_s.md)) |

## Identities in Global Fishing Watch

| Name | Flag | MMSI | AIS period | Registry-confirmed |
|---|---|---|---|---|
| NORSTAR INTREPID | Marshall Islands | 538003031 | 2012 to 22 Jul 2023 | yes |
| EAGLE-S | Cook Islands | 518998865 | 22 Jul 2023 to Mar 2026 | no |

The switch happened on a single day. After it, the ship trades only between the Baltic, the
Mediterranean, West Africa and India (GFW map, full period).

## What the track shows

* The bundled GFW track has no position between 11 Dec 2024 02:26 UTC and 7 Mar 2025 00:00 UTC. The last
  position is in the eastern Gulf of Finland off the Russian coast (59.92 N, 28.67 E), the next one in
  the North Sea (53.64 N, 3.63 E). The ship's departure from Ust-Luga, the crossing of Estlink 2, the
  U-turn reported by Finnish media, the boarding and the whole detention are missing.
* Media and investigators reconstructed the route from AIS data of other providers. So this is most
  likely a gap in GFW's public data, not proof that the ship switched AIS off. The tool reports
  the gap (`AIS_GAP`, "no track points inside the analysis window"), but the case shows why a second
  AIS source is needed for incident reconstruction.
* In Nov / early Dec 2024 GFW shows many 6–71 h breaks without movement while the ship lay off the
  Russian coast; typical for sparse coverage at anchor and not scored.

## Warning signals (tool)

`MULTI_IDENTITY` (2), `FLAG_CHANGE` (Marshall Islands, Paris MoU white list → Cook Islands, grey list),
`REGISTRY_LOST` (registry confirmation ended with the flag change), `AIS_GAP` (window empty).
`SANCTIONED` is listed with 0 points: the UK designated the ship in July 2025, after the incident.
Before the incident the gap since 11 Dec still counts (+15); without it the ship would score 35 (MEDIUM).

## Open questions

1. Why are Eagle S positions missing from the bundled snapshot from mid-December 2024 to March 2025?
   Check a second AIS source and the datasets available with authorised GFW access. A token alone
   does not establish that the missing positions are available.
2. Track data around 25 Dec: Estlink 2 and the Finland–Estonia telecom cables are in the bundled cable
   layer, but GFW has no positions to test `CABLE_CROSSING_SLOW` against.
3. Ownership changes in July 2023 (registry data beyond GFW, e.g. Equasis).

## Sources

* GFW vessel search and tracks (fixture `data/fixtures/eagle_s.json`, fetched 26 Oct 2026)
* [Wikipedia: 2024 Estlink 2 incident](https://en.wikipedia.org/wiki/2024_Estlink_2_incident): times, route, legal case
* [ERR, 26 Dec 2024](https://news.err.ee/1609560763/finnish-police-ship-at-the-site-of-estlink-2-s-breakage-missing-anchor): missing anchor
* [Helsinki Court of Appeal, 27 Aug 2026](https://www.tuomioistuimet.fi/ajankohtaista/tiedotteet/tiedote-hovioikeuden-paatoksesta-ns-eagle-s-aluksen-asiassa-r-16-2025-2572/): jurisdiction decision overturned and case returned to the district court
