# Xingshun 39 (Shunxing 39) - TPE cable north of Keelung (before the incident)

**Score: 100/100 (HIGH)**  
Analysis window: 2025-01-02 00:00 - 2025-01-02 12:00 UTC  
Data cut-off: 2025-01-02 12:00 UTC - only what GFW had recorded before this time  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| BAOLONG36 | GUY | 750342000 | 8358427 | 2022-11-17 | 2023-05-12 | self-reported AIS only |
| BAOLONG36 | CMR | 613003836 | 8358427 | 2022-11-24 | 2023-09-11 | self-reported AIS only |
| XINGSHUN39 | TZA | 677087200 | 8358427 | 2024-03-04 | 2025-01-02 | self-reported AIS only |
| SHUNXING39 | CMR | 613003889 | - | 2024-09-28 | 2025-01-02 | self-reported AIS only |

## Red flags

### 4 identities linked to the same hull (4 in the 5 years before 2025-01-02)  `MULTI_IDENTITY` (+30)
- * BAOLONG36 / GUY / MMSI 750342000 (2022-11-17 - 2023-05-12, self-reported AIS only)
- * BAOLONG36 / CMR / MMSI 613003836 (2022-11-24 - 2023-09-11, self-reported AIS only)
- * XINGSHUN39 / TZA / MMSI 677087200 (2024-03-04 - 2025-01-02, self-reported AIS only)
- * SHUNXING39 / CMR / MMSI 613003889 (2024-09-28 - 2025-01-02, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+15)
- 2024-03-04: CMR -> TZA (Paris MoU black, ITF flag of convenience)  [BAOLONG36 -> XINGSHUN39]  (recent)

> Scored: changes in the 3 years before 2025-01-02 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

### No identity of this hull is confirmed by a registry in GFW  `NO_REGISTRY` (+10)
- in use at 2025-01-02: XINGSHUN39 / TZA / MMSI 677087200 (2024-03-04 - 2025-01-02, self-reported AIS only)

> Logged-in GFW users see 11 additional registry sources.

### Identity also used without its IMO number  `IMO_HIDDEN` (+10)
- BAOLONG36 / CMR / MMSI 613003836 (2022-11-24 - 2023-02-10, self-reported AIS only) - same name and MMSI, but no IMO number broadcast
- XINGSHUN39 / TZA / MMSI 677087200 (2024-06-16 - 2024-09-29, self-reported AIS only) - same name and MMSI, but no IMO number broadcast
- BAOLONG36 / GUY / MMSI 750342000 (2022-11-17 - 2022-11-24, self-reported AIS only) - same name and MMSI, but no IMO number broadcast

> Without an IMO the AIS identity is not tied to the hull's history.

### Two identities of the same hull in use at the same time  `CONCURRENT_IDENTITIES` (+20)
- 2022-11-24 - 2023-05-12: BAOLONG36/GUY/750342000 and BAOLONG36/CMR/613003836
- 2024-09-28 - 2025-01-02: XINGSHUN39/TZA/677087200 and SHUNXING39/CMR/613003889

> Overlap is computed from first/last AIS message per identity; check the tracks (handover / parallel signals).

### Identity swap at sea (one AIS identity stops, another starts nearby)  `IDENTITY_HANDOVER` (+20)
- XINGSHUN39/TZA/677087200 stops 2024-12-28 22:11 UTC at 25.163,121.753 -> SHUNXING39/CMR/613003889 (no IMO) starts 2024-12-29 02:44 UTC at 25.588,121.803 (273 min, 25.7 nm)

### AIS gaps  `AIS_GAP` (+15)
- [XINGSHUN39/TZA/677087200] no track points at all inside the analysis window
- [SHUNXING39/CMR/613003889 (no IMO)] 2024-12-29 05:55 UTC -> 2024-12-29 19:49 UTC: 13.9 h without position, 11 nm straight-line jump (implied 0.8 kn), 25.922,121.823 -> 26.104,121.783
- [SHUNXING39/CMR/613003889 (no IMO)] 2024-12-29 20:07 UTC -> 2024-12-31 14:07 UTC: 42.0 h without position, 10 nm straight-line jump (implied 0.2 kn), 26.104,121.783 -> 25.972,121.894
- [SHUNXING39/CMR/613003889 (no IMO)] 1 further gap(s) >= 6 h without movement (port / anchorage / sparse data) - not scored

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

### Low speed (<= 3 kn) for 2 h or more  `SLOW_LOITERING` (+0)
- [SHUNXING39/CMR/613003889 (no IMO)] 2025-01-02 06:13 UTC -> 2025-01-02 11:49 UTC: 5.6 h stationary (anchored or drifting), mean AIS speed 0.4 kn, path 1.1 nm, net 0.8 nm, at 25.663,122.057

> Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

## Notes

- 51 track points inside the analysis window (101 loaded, 2 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
