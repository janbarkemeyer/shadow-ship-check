# Control: Yi Peng 5 (sister ship of Yi Peng 3, same operator)

**Score: 5/100 (LOW)**  
Analysis window: 2024-11-16 12:00 - 2024-11-18 18:00 UTC  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| ELEFTHERIA | GRC | 239850000 | 9221190 | 2012-01-01 | 2018-05-19 | registry + AIS |
| YI PENG 5 | CHN | 414388000 | 9221190 | 2018-05-16 | 2026-10-23 | self-reported AIS only |

## Red flags

### 2 identities linked to the same hull (1 in the 5 years before 2024-11-18)  `MULTI_IDENTITY` (+0)
-   ELEFTHERIA / GRC / MMSI 239850000 (2012-01-01 - 2018-05-19, registry + AIS)
- * YI PENG 5 / CHN / MMSI 414388000 (2018-05-16 - 2026-10-23, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+0)
- 2018-05-16: GRC -> CHN  [ELEFTHERIA -> YI PENG 5]

> Scored: changes in the 3 years before 2024-11-18 (+15 into a flag of convenience, +5 otherwise) and after it (+5). Sales also cause flag changes.

### Registry confirmation lost - identity in use is self-reported only  `REGISTRY_LOST` (+5)
- last confirmed: ELEFTHERIA / GRC / MMSI 239850000 (2012-01-01 - 2018-05-19, registry + AIS)
- in use at 2024-11-18: YI PENG 5 / CHN / MMSI 414388000 (2018-05-16 - 2026-10-23, self-reported AIS only)

> Confirmation was lost more than 5 years before the reference date.

### Low speed (<= 3 kn) for 2 h or more  `SLOW_LOITERING` (+0)
- 2024-11-16 12:10 UTC -> 2024-11-18 06:31 UTC: 42.3 h stationary (anchored or drifting), mean AIS speed 0.4 kn, path 4.2 nm, net 0.1 nm, at 26.468,120.002
- 2024-11-18 07:10 UTC -> 2024-11-18 17:58 UTC: 10.8 h stationary (anchored or drifting), mean AIS speed 0.6 kn, path 0.9 nm, net 0.0 nm, at 26.467,120.003

> Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

## Notes

- 355 track points inside the analysis window (1345 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
