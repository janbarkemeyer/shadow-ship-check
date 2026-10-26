# NewNew Polar Bear - Balticconnector gas pipeline and telecom cables

**Score: 35/100 (MEDIUM)**  
Analysis window: 2023-10-07 12:00 - 2023-10-08 06:00 UTC  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| REINBEK | LBR | 636091998 | 9313204 | 2012-01-03 | 2014-03-13 | self-reported AIS only |
| REINBEK | MLT | 229739000 | 9313204 | 2014-03-13 | 2016-03-07 | self-reported AIS only |
| REINBEK | LBR | 636092694 | 9313204 | 2016-03-07 | 2017-05-20 | self-reported AIS only |
| BALTIC FULMAR | CYP | 210925000 | 9313204 | 2017-04-28 | 2023-06-20 | registry + AIS |
| NEWNEW POLAR BEAR | HKG | 477893800 | 9313204 | 2023-06-20 | 2025-03-11 | self-reported AIS only |
| BELLE ARIES | PAN | 352005308 | 9313204 | 2025-03-11 | 2026-10-23 | self-reported AIS only |

## Red flags

### 6 identities linked to the same hull (2 in the 5 years before 2023-10-08)  `MULTI_IDENTITY` (+10)
-   REINBEK / LBR / MMSI 636091998 (2012-01-03 - 2014-03-13, self-reported AIS only)
-   REINBEK / MLT / MMSI 229739000 (2014-03-13 - 2016-03-07, self-reported AIS only)
-   REINBEK / LBR / MMSI 636092694 (2016-03-07 - 2017-05-20, self-reported AIS only)
- * BALTIC FULMAR / CYP / MMSI 210925000 (2017-04-28 - 2023-06-20, registry + AIS)
- * NEWNEW POLAR BEAR / HKG / MMSI 477893800 (2023-06-20 - 2025-03-11, self-reported AIS only)
-   BELLE ARIES / PAN / MMSI 352005308 (2025-03-11 - 2026-10-23, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 5 flag change(s)  `FLAG_CHANGE` (+10)
- 2014-03-13: LBR -> MLT (flag of convenience)  [REINBEK -> REINBEK]
- 2016-03-07: MLT -> LBR (flag of convenience)  [REINBEK -> REINBEK]
- 2017-04-28: LBR -> CYP (flag of convenience)  [REINBEK -> BALTIC FULMAR]
- 2023-06-20: CYP -> HKG  [BALTIC FULMAR -> NEWNEW POLAR BEAR]  (recent)
- 2025-03-11: HKG -> PAN (flag of convenience)  [NEWNEW POLAR BEAR -> BELLE ARIES]  (after reference date)

> Scored: changes in the 3 years before 2023-10-08 (+15 into a flag of convenience, +5 otherwise) and after it (+5). Sales also cause flag changes.

### Registry confirmation lost - identity in use is self-reported only  `REGISTRY_LOST` (+15)
- last confirmed: BALTIC FULMAR / CYP / MMSI 210925000 (2017-04-28 - 2023-06-20, registry + AIS)
- in use at 2023-10-08: NEWNEW POLAR BEAR / HKG / MMSI 477893800 (2023-06-20 - 2025-03-11, self-reported AIS only)

## Track around the reported incident time

Reported time (approximate): 2023-10-07 22:20 UTC. Points within +/- 3 h:

| Time (UTC) | Identity | Lat | Lon | AIS speed (kn) |
|---|---|---|---|---|
| 2023-10-07 20:17 | newnew_polar_bear | 59.5540 | 23.4093 | 10.6 |
| 2023-10-07 21:48 | newnew_polar_bear | 59.6452 | 23.8912 | 10.9 |
| 2023-10-07 22:15 | newnew_polar_bear | 59.6722 | 24.0483 | 11.2 |
| 2023-10-07 23:48 | newnew_polar_bear | 59.7462 | 24.6219 | 11.9 |

## Notes

- 11 track points inside the analysis window (255 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
