# Eagle S - Estlink 2 and telecom cables, Gulf of Finland (before the incident)

**Score: 50/100 (HIGH)**  
Analysis window: 2024-12-23 00:00 - 2024-12-25 10:26 UTC  
Data cut-off: 2024-12-25 10:26 UTC - only what GFW had recorded before this time  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| NORSTAR INTREPID | MHL | 538003031 | 9329760 | 2012-01-26 | 2023-07-22 | registry + AIS |
| EAGLE-S | COK | 518998865 | 9329760 | 2023-07-22 | 2024-12-25 | self-reported AIS only |

## Red flags

### 2 identities linked to the same hull (2 in the 5 years before 2024-12-25)  `MULTI_IDENTITY` (+10)
- * NORSTAR INTREPID / MHL / MMSI 538003031 (2012-01-26 - 2023-07-22, registry + AIS)
- * EAGLE-S / COK / MMSI 518998865 (2023-07-22 - 2024-12-25, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+10)
- 2023-07-22: MHL -> COK (Paris MoU grey, ITF flag of convenience)  [NORSTAR INTREPID -> EAGLE-S]  (recent)

> Scored: changes in the 3 years before 2024-12-25 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

### Registry confirmation lost - identity in use is self-reported only  `REGISTRY_LOST` (+15)
- last confirmed: NORSTAR INTREPID / MHL / MMSI 538003031 (2012-01-26 - 2023-07-22, registry + AIS)
- in use at 2024-12-25: EAGLE-S / COK / MMSI 518998865 (2023-07-22 - 2024-12-25, self-reported AIS only)

### AIS gaps  `AIS_GAP` (+15)
- no track points at all inside the analysis window

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

## Notes

- 0 track points inside the analysis window (1686 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
