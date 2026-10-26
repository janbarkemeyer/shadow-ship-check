# Yi Peng 3 - BCS East-West Interlink and C-Lion1, Baltic Sea (before the incident)

**Score: 5/100 (LOW)**  
Analysis window: 2024-11-16 12:00 - 2024-11-17 08:00 UTC  
Data cut-off: 2024-11-17 08:00 UTC - only what GFW had recorded before this time  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| AVRA | GRC | 240583000 | 9224984 | 2012-01-09 | 2015-07-30 | self-reported AIS only |
| AVRA | LBR | 636017118 | 9224984 | 2015-07-30 | 2016-12-02 | registry + AIS |
| YI PENG 3 | CHN | 414270000 | 9224984 | 2020-06-30 | 2024-11-17 | self-reported AIS only |

## Red flags

### 3 identities linked to the same hull (1 in the 5 years before 2024-11-17)  `MULTI_IDENTITY` (+0)
-   AVRA / GRC / MMSI 240583000 (2012-01-09 - 2015-07-30, self-reported AIS only)
-   AVRA / LBR / MMSI 636017118 (2015-07-30 - 2016-12-02, registry + AIS)
- * YI PENG 3 / CHN / MMSI 414270000 (2020-06-30 - 2024-11-17, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+0)
- 2015-07-30: GRC -> LBR (Paris MoU white, ITF flag of convenience)  [AVRA -> AVRA]

> Scored: changes in the 3 years before 2024-11-17 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

### Registry confirmation lost - identity in use is self-reported only  `REGISTRY_LOST` (+5)
- last confirmed: AVRA / LBR / MMSI 636017118 (2015-07-30 - 2016-12-02, registry + AIS)
- in use at 2024-11-17: YI PENG 3 / CHN / MMSI 414270000 (2020-06-30 - 2024-11-17, self-reported AIS only)

> Confirmation was lost more than 5 years before the reference date.

## Notes

- 13 track points inside the analysis window (118 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
