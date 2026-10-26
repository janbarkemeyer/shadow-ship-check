# Case file: NewNew Polar Bear: Balticconnector, Gulf of Finland, 7–8 October 2023

| | |
|---|---|
| Incident | Balticconnector gas pipeline (Finland–Estonia) ruptured in the night of 7 to 8 Oct 2023 |
| Status | Suspected. Finland's National Bureau of Investigation matched the anchor recovered at the rupture to the ship. In Aug 2024 a Chinese investigation acknowledged the damage but called it an accident caused by a storm. |
| Hull | IMO 9313204, container ship, Hong Kong flag at the time, Chinese operator |
| Tool result | 30 MEDIUM before the incident, 35 MEDIUM with full data ([report](../reports/newnew_polar_bear.md)) |

## Identities in Global Fishing Watch

| Name | Flag | MMSI | AIS period | Registry-confirmed |
|---|---|---|---|---|
| REINBEK | Liberia / Malta / Liberia | 636091998, 229739000, 636092694 | 2012 to May 2017 | no |
| BALTIC FULMAR | Cyprus | 210925000 | Apr 2017 to 20 Jun 2023 | yes |
| NEWNEW POLAR BEAR | Hong Kong | 477893800 | 20 Jun 2023 to 11 Mar 2025 | no |
| BELLE ARIES | Panama | 352005308 | since 11 Mar 2025 | no |

Bought and renamed less than four months before the incident; registry confirmation ended with the
sale. Renamed and reflagged again (Panama) in March 2025.

## What the track shows

* GFW positions roughly every 90 minutes. Between 22:15 and 23:48 UTC on 7 Oct the track crosses the
  Balticconnector route (OpenStreetMap) at a steady 11–12 kn; the rupture is dated to about 22:20 UTC.
* No slowdown, no loop, no gap around the incident in GFW. The damage pattern (anchor dragged along the
  seabed) is not visible in a position track at this resolution.
* 4-hour gap on 7 Oct (13:16–17:16 UTC, 37 nm at a plausible speed); most likely reception, not scored.

## Warning signals (tool)

`MULTI_IDENTITY`, `FLAG_CHANGE` (Cyprus → Hong Kong 2023, Hong Kong → Panama after the incident),
`REGISTRY_LOST`. `CABLE_CROSSING_SLOW` does not fire: the ship crossed the pipeline at cruising speed.
A speed-based rule can miss an anchor drag at normal cruising speed; the absence of a signal does
not rule out damage.

## Open questions

1. The exact time of the rupture (we use ~22:20 UTC as an approximation) and the exact crossing point.
2. Why did the Panama reflagging happen in March 2025, and who owns BELLE ARIES?

## Sources

* GFW vessel search and tracks (fixture `data/fixtures/newnew_polar_bear.json`, fetched 26 Oct 2026)
* [Offshore Magazine, 30 Oct 2023](https://www.offshore-mag.com/regional-reports/north-sea-europe/article/14300839/chinese-ships-anchor-caused-damage-to-baltic-gas-pipeline-finland-suggests): anchor, seabed trail
* [Yle, 10 Nov 2023](https://yle.fi/a/74-20059680): anchor confirmed as the ship's
* [The Baltic Times: China admits ship damaged Balticconnector "by accident"](https://www.baltictimes.com/china_admits_hong_kong-flagged_ship_damaged_balticconnector_gas_pipeline__by_accident_)
