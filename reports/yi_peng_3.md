# Yi Peng 3 - BCS East-West Interlink and C-Lion1, Baltic Sea

**Score: 15/100 (LOW)**  
Analysis window: 2024-11-16 12:00 - 2024-11-18 18:00 UTC  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| AVRA | GRC | 240583000 | 9224984 | 2012-01-09 | 2015-07-30 | self-reported AIS only |
| AVRA | LBR | 636017118 | 9224984 | 2015-07-30 | 2016-12-02 | registry + AIS |
| YI PENG 3 | CHN | 414270000 | 9224984 | 2020-06-30 | 2026-10-23 | self-reported AIS only |

## Red flags

### 3 identities linked to the same hull (1 in the 5 years before 2024-11-18)  `MULTI_IDENTITY` (+0)
-   AVRA / GRC / MMSI 240583000 (2012-01-09 - 2015-07-30, self-reported AIS only)
-   AVRA / LBR / MMSI 636017118 (2015-07-30 - 2016-12-02, registry + AIS)
- * YI PENG 3 / CHN / MMSI 414270000 (2020-06-30 - 2026-10-23, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+0)
- 2015-07-30: GRC -> LBR (flag of convenience)  [AVRA -> AVRA]

> Scored: changes in the 3 years before 2024-11-18 (+15 into a flag of convenience, +5 otherwise) and after it (+5). Sales also cause flag changes.

### Registry confirmation lost - identity in use is self-reported only  `REGISTRY_LOST` (+5)
- last confirmed: AVRA / LBR / MMSI 636017118 (2015-07-30 - 2016-12-02, registry + AIS)
- in use at 2024-11-18: YI PENG 3 / CHN / MMSI 414270000 (2020-06-30 - 2026-10-23, self-reported AIS only)

> Confirmation was lost more than 5 years before the reference date.

### Sustained speed drop while underway  `SPEED_DROP` (+10)
- 2024-11-17 17:59 UTC -> 2024-11-17 19:30 UTC: 1.5 h at 3.9-4.3 kn (cruising median 8.9 kn), from 56.164,18.226

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

## Track around the reported incident time

Reported time (approximate): 2024-11-18 02:00 UTC. Points within +/- 3 h:

| Time (UTC) | Identity | Lat | Lon | AIS speed (kn) |
|---|---|---|---|---|
| 2024-11-18 00:01 | yi_peng_3 | 55.9262 | 17.3880 | 6.7 |
| 2024-11-18 01:39 | yi_peng_3 | 55.8791 | 17.0784 | 6.0 |
| 2024-11-18 03:10 | yi_peng_3 | 55.8407 | 16.8104 | 5.1 |
| 2024-11-18 04:40 | yi_peng_3 | 55.8050 | 16.5361 | 7.0 |

## Notes

- 50 track points inside the analysis window (324 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
