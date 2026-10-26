# NewNew Polar Bear - Balticconnector gas pipeline and telecom cables (before the incident)

**Score: 30/100 (MEDIUM)**  
Analysis window: 2023-10-07 12:00 - 2023-10-07 20:00 UTC  
Data cut-off: 2023-10-07 20:00 UTC - only what GFW had recorded before this time  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| REINBEK | LBR | 636091998 | 9313204 | 2012-01-03 | 2014-03-13 | self-reported AIS only |
| REINBEK | MLT | 229739000 | 9313204 | 2014-03-13 | 2016-03-07 | self-reported AIS only |
| REINBEK | LBR | 636092694 | 9313204 | 2016-03-07 | 2017-05-20 | self-reported AIS only |
| BALTIC FULMAR | CYP | 210925000 | 9313204 | 2017-04-28 | 2023-06-20 | registry + AIS |
| NEWNEW POLAR BEAR | HKG | 477893800 | 9313204 | 2023-06-20 | 2023-10-07 | self-reported AIS only |

## Red flags

### 5 identities linked to the same hull (2 in the 5 years before 2023-10-07)  `MULTI_IDENTITY` (+10)
-   REINBEK / LBR / MMSI 636091998 (2012-01-03 - 2014-03-13, self-reported AIS only)
-   REINBEK / MLT / MMSI 229739000 (2014-03-13 - 2016-03-07, self-reported AIS only)
-   REINBEK / LBR / MMSI 636092694 (2016-03-07 - 2017-05-20, self-reported AIS only)
- * BALTIC FULMAR / CYP / MMSI 210925000 (2017-04-28 - 2023-06-20, registry + AIS)
- * NEWNEW POLAR BEAR / HKG / MMSI 477893800 (2023-06-20 - 2023-10-07, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 4 flag change(s)  `FLAG_CHANGE` (+5)
- 2014-03-13: LBR -> MLT (Paris MoU white, ITF flag of convenience)  [REINBEK -> REINBEK]
- 2016-03-07: MLT -> LBR (Paris MoU white, ITF flag of convenience)  [REINBEK -> REINBEK]
- 2017-04-28: LBR -> CYP (Paris MoU white, ITF flag of convenience)  [REINBEK -> BALTIC FULMAR]
- 2023-06-20: CYP -> HKG (Paris MoU white)  [BALTIC FULMAR -> NEWNEW POLAR BEAR]  (recent)

> Scored: changes in the 3 years before 2023-10-07 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

### Registry confirmation lost - identity in use is self-reported only  `REGISTRY_LOST` (+15)
- last confirmed: BALTIC FULMAR / CYP / MMSI 210925000 (2017-04-28 - 2023-06-20, registry + AIS)
- in use at 2023-10-07: NEWNEW POLAR BEAR / HKG / MMSI 477893800 (2023-06-20 - 2023-10-07, self-reported AIS only)

## Notes

- 3 track points inside the analysis window (49 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
