# NewNew Polar Bear - Balticconnector gas pipeline and telecom cables

Case file with context and sources: [newnew_polar_bear.md](../cases/newnew_polar_bear.md)

| | Score | Identity | Flag & registry | Behaviour |
|---|---|---|---|---|
| Before the incident | 30 MEDIUM | 10 | 20 | 0 |
| Full data | 35 MEDIUM | 10 | 25 | 0 |

Pre-incident data cut-off: 2023-10-07 20:00 UTC.  
Analysis window: 2023-10-07 12:00 - 2023-10-08 06:00 UTC.  
_Research indicators only. The score is not a probability or evidence of intent or responsibility for damage. LOW may reflect limited data. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Before the incident

Retrospective timestamp filter of the bundled snapshot. Current identity links, registry matches, manual associations and fixed 2025 flag weights remain; this does not reconstruct an advance warning.

- Selected AIS identity has no registry match in GFW; an earlier identity did (+15): last confirmed: BALTIC FULMAR / CYP / MMSI 210925000 (2017-04-28 - 2023-06-20, registry + AIS)
- 5 identities linked to the same hull (2 in the 5 years before 2023-10-07) (+10):   REINBEK / LBR / MMSI 636091998 (2012-01-03 - 2014-03-13, self-reported AIS only)
- 4 flag change(s) (+5): 2014-03-13: LBR -> MLT (Paris MoU white, ITF flag of convenience)  [REINBEK -> REINBEK]

## Full data

### Identities

| Name | Flag | MMSI | IMO | First seen | Last seen | Source |
|---|---|---|---|---|---|---|
| REINBEK | LBR | 636091998 | 9313204 | 2012-01-03 | 2014-03-13 | self-reported AIS only |
| REINBEK | MLT | 229739000 | 9313204 | 2014-03-13 | 2016-03-07 | self-reported AIS only |
| REINBEK | LBR | 636092694 | 9313204 | 2016-03-07 | 2017-05-20 | self-reported AIS only |
| BALTIC FULMAR | CYP | 210925000 | 9313204 | 2017-04-28 | 2023-06-20 | registry + AIS |
| NEWNEW POLAR BEAR | HKG | 477893800 | 9313204 | 2023-06-20 | 2025-03-11 | self-reported AIS only |
| BELLE ARIES | PAN | 352005308 | 9313204 | 2025-03-11 | 2026-10-23 | self-reported AIS only |

### Signals

#### Identity (+10)

##### 6 identities linked to the same hull (2 in the 5 years before 2023-10-08) (`MULTI_IDENTITY`, +10)

-   REINBEK / LBR / MMSI 636091998 (2012-01-03 - 2014-03-13, self-reported AIS only)
-   REINBEK / MLT / MMSI 229739000 (2014-03-13 - 2016-03-07, self-reported AIS only)
-   REINBEK / LBR / MMSI 636092694 (2016-03-07 - 2017-05-20, self-reported AIS only)
- * BALTIC FULMAR / CYP / MMSI 210925000 (2017-04-28 - 2023-06-20, registry + AIS)
- * NEWNEW POLAR BEAR / HKG / MMSI 477893800 (2023-06-20 - 2025-03-11, self-reported AIS only)
-   BELLE ARIES / PAN / MMSI 352005308 (2025-03-11 - 2026-10-23, self-reported AIS only)

* = in use during the look-back period (scored); others are history.

#### Flag & registry (+25)

##### 5 flag change(s) (`FLAG_CHANGE`, +10)

- 2014-03-13: LBR -> MLT (Paris MoU white, ITF flag of convenience)  [REINBEK -> REINBEK]
- 2016-03-07: MLT -> LBR (Paris MoU white, ITF flag of convenience)  [REINBEK -> REINBEK]
- 2017-04-28: LBR -> CYP (Paris MoU white, ITF flag of convenience)  [REINBEK -> BALTIC FULMAR]
- 2023-06-20: CYP -> HKG (Paris MoU white)  [BALTIC FULMAR -> NEWNEW POLAR BEAR]  (recent)
- 2025-03-11: HKG -> PAN (Paris MoU white, ITF flag of convenience)  [NEWNEW POLAR BEAR -> BELLE ARIES]  (after reference date)

Scored: changes in the 3 years before 2023-10-08 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

##### Selected AIS identity has no registry match in GFW; an earlier identity did (`REGISTRY_LOST`, +15)

- last confirmed: BALTIC FULMAR / CYP / MMSI 210925000 (2017-04-28 - 2023-06-20, registry + AIS)
- in use at 2023-10-08: NEWNEW POLAR BEAR / HKG / MMSI 477893800 (2023-06-20 - 2025-03-11, self-reported AIS only)

GFW registry coverage is incomplete; a missing match does not establish invalid registration.

### Track around the reported incident time

Reported time (approximate): 2023-10-07 22:20 UTC. Points within +/- 3 h:

| Time (UTC) | Identity | Lat | Lon | AIS speed (kn) |
|---|---|---|---|---|
| 2023-10-07 20:17 | newnew_polar_bear | 59.5540 | 23.4093 | 10.6 |
| 2023-10-07 21:48 | newnew_polar_bear | 59.6452 | 23.8912 | 10.9 |
| 2023-10-07 22:15 | newnew_polar_bear | 59.6722 | 24.0483 | 11.2 |
| 2023-10-07 23:48 | newnew_polar_bear | 59.7462 | 24.6219 | 11.9 |

### Notes

- 11 track points inside the analysis window (255 loaded, 1 identity track(s)).
