# Eagle S - Estlink 2 and telecom cables, Gulf of Finland

**Score: 60/100 (HIGH)**  
Analysis window: 2024-12-23 00:00 - 2024-12-28 23:59 UTC  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| NORSTAR INTREPID | MHL | 538003031 | 9329760 | 2012-01-26 | 2023-07-22 | registry + AIS |
| EAGLE-S | COK | 518998865 | 9329760 | 2023-07-22 | 2026-03-28 | self-reported AIS only |

## Red flags

### 2 identities linked to the same hull (2 in the 5 years before 2024-12-28)  `MULTI_IDENTITY` (+10)
- * NORSTAR INTREPID / MHL / MMSI 538003031 (2012-01-26 - 2023-07-22, registry + AIS)
- * EAGLE-S / COK / MMSI 518998865 (2023-07-22 - 2026-03-28, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+15)
- 2023-07-22: MHL -> COK (flag of convenience)  [NORSTAR INTREPID -> EAGLE-S]  (recent)

> Scored: changes in the 3 years before 2024-12-28 (+15 into a flag of convenience, +5 otherwise) and after it (+5). Sales also cause flag changes.

### Registry confirmation lost - identity in use is self-reported only  `REGISTRY_LOST` (+15)
- last confirmed: NORSTAR INTREPID / MHL / MMSI 538003031 (2012-01-26 - 2023-07-22, registry + AIS)
- in use at 2024-12-28: EAGLE-S / COK / MMSI 518998865 (2023-07-22 - 2026-03-28, self-reported AIS only)

### AIS gaps  `AIS_GAP` (+20)
- 2024-12-11 02:26 UTC -> 2025-03-07 00:00 UTC: 2061.6 h without position, 899 nm straight-line jump (implied 0.4 kn), 59.921,28.665 -> 53.635,3.633  <-- overlaps the analysis window

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

## Track around the reported incident time

Reported time (approximate): 2024-12-25 10:26 UTC. Points within +/- 3 h:

No AIS positions in GFW for this period.

## Notes

- 0 track points inside the analysis window (1814 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
