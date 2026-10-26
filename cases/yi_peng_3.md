# Case file: Yi Peng 3 – BCS East-West Interlink and C-Lion1, Baltic Sea, 17–18 November 2024

| | |
|---|---|
| Incident | BCS East-West Interlink (Lithuania–Gotland) cut around 10:00 local time on 17 Nov; C-Lion1 (Finland–Germany) lost traffic at 02:00 UTC on 18 Nov |
| Status | **Suspected.** No charges. Swedish accident investigators said it "cannot be determined with certainty" whether the anchor was dropped deliberately; the ship dragged it for about 180 nm. Swedish prosecutors were not allowed on board. |
| Hull | IMO 9224984, bulk carrier, China flag, Chinese operator |
| Tool result | `ssc case yi_peng_3` → **15/100 LOW** ([full report](../reports/yi_peng_3.md)) |

## Identities in Global Fishing Watch

| Name | Flag | MMSI | AIS period | Registry-confirmed |
|---|---|---|---|---|
| AVRA | Greece | 240583000 | 2012 – Jul 2015 | no |
| AVRA | Liberia | 636017118 | Jul 2015 – Dec 2016 | yes |
| YI PENG 3 | China | 414270000 | since 2016 (with IMO since Jun 2020) | no |

One sale and reflagging to China eight years before the incident – **no camouflage pattern**. The
sister ship Yi Peng 5 (control vessel) has the same profile.

## What the track shows

* Speed drops from about 9 kn on 16 Nov to 6–7 kn from around 00:00 UTC on 17 Nov and stays there
  until the next morning – consistent with the ~1.5 days of anchor dragging described by Swedish
  investigators. The tool only flags the strongest part (3.9–4.3 kn, 17:59–19:30 UTC on 17 Nov, around
  56.16 N, 18.23 E); a 9 → 6.5 kn drop is within normal variation for its threshold.
* At 02:00 UTC on 18 Nov (C-Lion1 failure) the ship is at about 55.88 N, 17.08 E making 6 kn.
* 08:25–09:35 UTC on 18 Nov: stop east of Bornholm (55.69 N, 15.80 E), then 9–10.5 kn.
* **Contradiction to check:** media reported that the ship's AIS was off for about 7.5 hours after
  Gotland and came back at 22:41 UTC south of Öland. GFW shows positions every ~90 minutes through that
  whole period. Possible explanations: satellite AIS received what coastal stations missed, GFW's
  simplified public track, or an error in the reporting. Needs full-resolution data before any claim.

## Warning signals (tool)

`SPEED_DROP`, `REGISTRY_LOST` (only 5 points – confirmation lost in 2016). Identity checks stay silent.

**Lesson:** identity camouflage is not a necessary condition. Yi Peng 3 would only be caught by
behaviour checks – and those need denser data and cable routes.

## Open questions

1. AIS-off period: GFW vs. media reports (see above).
2. Cable routes of BCS and C-Lion1 to measure the crossings (`--cables`).
3. A better speed-drop baseline (same ship, same route, previous voyages) instead of a fixed threshold.

## Sources

* GFW vessel search and tracks (fixture `data/fixtures/yi_peng_3.json`, fetched 26 Oct 2026)
* [Wikipedia: 2024 Baltic Sea submarine cable disruptions](https://en.wikipedia.org/wiki/2024_Baltic_Sea_submarine_cable_disruptions) – times, AIS reports, investigations
* [The Maritime Executive: Swedish report fails to find evidence of sabotage](https://maritime-executive.com/article/swedish-report-fails-to-find-evidence-of-sabotage-by-chinese-bulker)
