# Hong Tai 58 - TPKM-3 cable Taiwan-Penghu

**Score: 100/100 (HIGH)**  
Analysis window: 2025-02-22 00:00 - 2025-02-26 00:00 UTC  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| JIN LONG 389 | CHN | 413762751 | - | 2012-08-23 | 2022-10-09 | registry + AIS |
| DONGSHUN3 | CHN | 413762751 | 8357069 | 2022-10-27 | 2023-09-05 | registry record |
| HONGTAI58 | TGO | 671756000 | 8357069 | 2023-07-31 | 2025-02-27 | self-reported AIS only |
| HONGTA 8 | TZA | 677082100 | 8357069 | 2024-12-15 | 2025-02-05 | self-reported AIS only |

## Red flags

### 4 identities linked to the same hull (4 in the 5 years before 2025-02-26)  `MULTI_IDENTITY` (+30)
- * JIN LONG 389 / CHN / MMSI 413762751 (2012-08-23 - 2022-10-09, registry + AIS)
- * DONGSHUN3 / CHN / MMSI 413762751 (2022-10-27 - 2023-09-05, registry record)
- * HONGTAI58 / TGO / MMSI 671756000 (2023-07-31 - 2025-02-27, self-reported AIS only)
- * HONGTA 8 / TZA / MMSI 677082100 (2024-12-15 - 2025-02-05, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+15)
- 2023-07-31: CHN -> TGO (Paris MoU black, ITF flag of convenience)  [DONGSHUN3 -> HONGTAI58]  (recent)

> Scored: changes in the 3 years before 2025-02-26 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

### Registry confirmation lost - identity in use is self-reported only  `REGISTRY_LOST` (+15)
- last confirmed: DONGSHUN3 / CHN / MMSI 413762751 (2022-10-27 - 2023-09-05, registry record)
- in use at 2025-02-26: HONGTAI58 / TGO / MMSI 671756000 (2023-07-31 - 2025-02-27, self-reported AIS only)

### MMSI shared with other vessels (2 within 2 years, 6 older)  `MMSI_REUSE` (+15)
- MMSI 677082100 also used by YEKTA 3 / TZA / MMSI 677082100 (2020-09-14 - 2024-07-19, self-reported AIS only), IMO 8889842  (within 2 years)
- MMSI 677082100 also used by LADY EMERALD / TZA / MMSI 677082100 (2024-06-29 - 2024-11-07, self-reported AIS only)  (within 2 years)
- MMSI 671756000 also used by STEEL DEVELOPER / TGO / MMSI 671756000 (2016-05-10 - 2016-05-28, registry + AIS), IMO 9171424
- MMSI 677082100 also used by A DAL 3 / TZA / MMSI 677082100 (2016-01-19 - 2016-05-25, registry + AIS)
- MMSI 677082100 also used by A DAL 3 / TZA / MMSI 677082100 (2016-05-28 - 2016-11-10, registry + AIS), IMO 8713299
- MMSI 677082100 also used by GOLDEN SEA / TZA / MMSI 677082100 (2017-11-27 - 2018-11-07, registry + AIS), IMO 8800298
- MMSI 671666000 also used by KARAM / TGO / MMSI 671666000 (2015-12-02 - 2021-06-20, registry + AIS), IMO 8116180
- ... 1 older uses

> Small registries sometimes recycle MMSIs; use close in time is the strong signal.

### Hull's name broadcast under other ships' MMSIs  `NAME_ON_OTHER_MMSI` (+15)
- HONGTAI58 / TGO / MMSI 671666000 (2024-11-27 - 2024-12-04, self-reported AIS only) - MMSI also used by KARAM
- HONGTAI58 / TGO / MMSI 671280000 (2023-12-25 - 2023-12-26, self-reported AIS only) - MMSI also used by XINJINLIN6

> Short episodes can also be typing errors in the AIS set-up; repeated use is the signal.

### Identity also used without its IMO number  `IMO_HIDDEN` (+10)
- HONGTAI58 / TGO / MMSI 671756000 (2023-11-21 - 2025-02-27, self-reported AIS only) - same name and MMSI, but no IMO number broadcast
- HONGTA8 / TZA / MMSI 677082100 (2025-01-05 - 2025-02-05, self-reported AIS only) - same name and MMSI, but no IMO number broadcast

> Without an IMO the AIS identity is not tied to the hull's history.

### Two identities of the same hull in use at the same time  `CONCURRENT_IDENTITIES` (+20)
- 2024-12-15 - 2025-02-05: HONGTAI58/TGO/671756000 and HONGTA 8/TZA/677082100

> Overlap is computed from first/last AIS message per identity; check the tracks (handover / parallel signals).

### Identity swap at sea (one AIS identity stops, another starts nearby)  `IDENTITY_HANDOVER` (+20)
- HONGTAI58/671756000 (IMO 8357069) stops 2024-12-15 02:01 UTC at 34.278,128.456 -> HONGTA 8/677082100 (IMO 8357069) starts 2024-12-15 03:17 UTC at 34.278,128.456 (76 min, 0.0 nm)

### Identities of the same hull broadcast from two places at once  `PARALLEL_TRACKS` (+20)
- HONGTAI58/671756000 (no IMO) at 25.98,120.91 (2024-12-17 21:30 UTC) vs HONGTA 8/677082100 (IMO 8357069) at 34.69,128.88 (2024-12-17 20:37 UTC): 666 nm apart
- HONGTAI58/671756000 (no IMO) at 25.59,120.24 (2025-01-12 12:56 UTC) vs HONGTA8/677082100 (no IMO) at 35.08,129.00 (2025-01-12 12:45 UTC): 728 nm apart

> Either two hulls share identity data (spoofing / cloning) or GFW linked identities wrongly.

### Only short stationary AIS gaps (not scored)  `AIS_GAP` (+0)
- 1 further gap(s) >= 6 h without movement (port / anchorage / sparse data) - not scored

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

### Low speed (<= 3 kn) for 2 h or more  `SLOW_LOITERING` (+0)
- 2025-02-22 10:40 UTC -> 2025-02-24 06:11 UTC: 43.5 h stationary (anchored or drifting), mean AIS speed 1.3 kn, path 2.3 nm, net 0.8 nm, at 23.304,120.016
- 2025-02-24 07:21 UTC -> 2025-02-24 19:06 UTC: 11.8 h stationary (anchored or drifting), mean AIS speed 1.2 kn, path 0.8 nm, net 0.2 nm, at 23.291,120.016

> Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

### Sustained speed drop while underway  `SPEED_DROP` (+10)
- 2025-02-24 20:44 UTC -> 2025-02-24 22:15 UTC: 1.5 h at 2.2-3.5 kn (cruising median 6.3 kn), from 23.308,119.990

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

## Track around the reported incident time

Reported time (approximate): 2025-02-24 19:03 UTC. Points within +/- 3 h:

| Time (UTC) | Identity | Lat | Lon | AIS speed (kn) |
|---|---|---|---|---|
| 2025-02-24 16:35 | hong_tai_58 | 23.2901 | 120.0161 | 2.1 |
| 2025-02-24 16:43 | hong_tai_58 | 23.2901 | 120.0161 | 1.1 |
| 2025-02-24 17:38 | hong_tai_58 | 23.2901 | 120.0163 | 0.0 |
| 2025-02-24 17:40 | hong_tai_58 | 23.2901 | 120.0162 | 0.2 |
| 2025-02-24 17:56 | hong_tai_58 | 23.2901 | 120.0164 | 0.4 |
| 2025-02-24 17:58 | hong_tai_58 | 23.2901 | 120.0162 | 0.3 |
| 2025-02-24 18:14 | hong_tai_58 | 23.2901 | 120.0163 | 0.9 |
| 2025-02-24 18:15 | hong_tai_58 | 23.2901 | 120.0162 | 0.9 |
| 2025-02-24 18:17 | hong_tai_58 | 23.2901 | 120.0161 | 0.0 |
| 2025-02-24 18:19 | hong_tai_58 | 23.2901 | 120.0162 | 1.4 |
| 2025-02-24 18:57 | hong_tai_58 | 23.2925 | 120.0155 | 2.9 |
| 2025-02-24 19:02 | hong_tai_58 | 23.2932 | 120.0131 | 0.5 |
| 2025-02-24 19:05 | hong_tai_58 | 23.2931 | 120.0127 | 2.2 |
| 2025-02-24 19:06 | hong_tai_58 | 23.2928 | 120.0130 | 2.4 |
| 2025-02-24 19:10 | hong_tai_58 | 23.2935 | 120.0163 | 4.5 |
| 2025-02-24 19:12 | hong_tai_58 | 23.2960 | 120.0171 | 5.2 |
| 2025-02-24 20:30 | hong_tai_58 | 23.3118 | 119.9874 | 2.7 |
| 2025-02-24 20:33 | hong_tai_58 | 23.3120 | 119.9882 | 0.4 |
| 2025-02-24 20:34 | hong_tai_58 | 23.3121 | 119.9883 | 0.4 |
| 2025-02-24 20:44 | hong_tai_58 | 23.3076 | 119.9899 | 2.4 |
| 2025-02-24 20:45 | hong_tai_58 | 23.3073 | 119.9900 | 2.2 |

## Notes

- 218 track points inside the analysis window (469 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
