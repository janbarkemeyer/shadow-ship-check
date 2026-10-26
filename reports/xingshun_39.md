# Xingshun 39 (Shunxing 39) - TPE cable north of Keelung

**Score: 100/100 (HIGH)**  
Analysis window: 2025-01-02 00:00 - 2025-01-05 00:00 UTC  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| BAOLONG36 | GUY | 750342000 | 8358427 | 2022-11-17 | 2023-05-12 | self-reported AIS only |
| BAOLONG36 | CMR | 613003836 | 8358427 | 2022-11-24 | 2023-09-11 | self-reported AIS only |
| XINGSHUN39 | TZA | 677087200 | 8358427 | 2024-03-04 | 2025-08-14 | self-reported AIS only |
| SHUNXING39 | CMR | 613003889 | - | 2024-09-28 | 2025-01-03 | self-reported AIS only |

## Red flags

### 4 identities linked to the same hull (4 in the 5 years before 2025-01-05)  `MULTI_IDENTITY` (+30)
- * BAOLONG36 / GUY / MMSI 750342000 (2022-11-17 - 2023-05-12, self-reported AIS only)
- * BAOLONG36 / CMR / MMSI 613003836 (2022-11-24 - 2023-09-11, self-reported AIS only)
- * XINGSHUN39 / TZA / MMSI 677087200 (2024-03-04 - 2025-08-14, self-reported AIS only)
- * SHUNXING39 / CMR / MMSI 613003889 (2024-09-28 - 2025-01-03, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+15)
- 2024-03-04: CMR -> TZA (Paris MoU black, ITF flag of convenience)  [BAOLONG36 -> XINGSHUN39]  (recent)

> Scored: changes in the 3 years before 2025-01-05 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

### No identity of this hull is confirmed by a registry in GFW  `NO_REGISTRY` (+10)
- in use at 2025-01-05: XINGSHUN39 / TZA / MMSI 677087200 (2024-03-04 - 2025-08-14, self-reported AIS only)

> Logged-in GFW users see 11 additional registry sources.

### Identity also used without its IMO number  `IMO_HIDDEN` (+10)
- BAOLONG36 / CMR / MMSI 613003836 (2022-11-24 - 2023-02-10, self-reported AIS only) - same name and MMSI, but no IMO number broadcast
- XINGSHUN39 / TZA / MMSI 677087200 (2024-06-16 - 2024-09-29, self-reported AIS only) - same name and MMSI, but no IMO number broadcast
- XINGSHUNNO.39 / TZA / MMSI 677087200 (2025-08-14 - 2025-08-14, self-reported AIS only) - same name and MMSI, but no IMO number broadcast
- BAOLONG36 / GUY / MMSI 750342000 (2022-11-17 - 2022-11-24, self-reported AIS only) - same name and MMSI, but no IMO number broadcast

> Without an IMO the AIS identity is not tied to the hull's history.

### Two identities of the same hull in use at the same time  `CONCURRENT_IDENTITIES` (+20)
- 2022-11-24 - 2023-05-12: BAOLONG36/GUY/750342000 and BAOLONG36/CMR/613003836
- 2024-09-28 - 2025-01-03: XINGSHUN39/TZA/677087200 and SHUNXING39/CMR/613003889

> Overlap is computed from first/last AIS message per identity; check the tracks (handover / parallel signals).

### Identity swap at sea (one AIS identity stops, another starts nearby)  `IDENTITY_HANDOVER` (+20)
- SHUNXING39/CMR/613003889 (no IMO) stops 2025-01-03 08:19 UTC at 25.334,121.712 -> XINGSHUN39/TZA/677087200 starts 2025-01-03 08:52 UTC at 25.335,121.707 (33 min, 0.2 nm)
- XINGSHUN39/TZA/677087200 stops 2024-12-28 22:11 UTC at 25.163,121.753 -> SHUNXING39/CMR/613003889 (no IMO) starts 2024-12-29 02:44 UTC at 25.588,121.803 (273 min, 25.7 nm)

### AIS gaps  `AIS_GAP` (+15)
- [XINGSHUN39/TZA/677087200] 2024-12-28 22:11 UTC -> 2025-01-03 08:52 UTC: 130.7 h without position, 11 nm straight-line jump (implied 0.1 kn), 25.163,121.753 -> 25.335,121.707  - meanwhile broadcasting as SHUNXING39/CMR/613003889 (no IMO) (253 positions); scored under IDENTITY_HANDOVER
- [SHUNXING39/CMR/613003889 (no IMO)] 2024-12-29 05:55 UTC -> 2024-12-29 19:49 UTC: 13.9 h without position, 11 nm straight-line jump (implied 0.8 kn), 25.922,121.823 -> 26.104,121.783
- [SHUNXING39/CMR/613003889 (no IMO)] 2024-12-29 20:07 UTC -> 2024-12-31 14:07 UTC: 42.0 h without position, 10 nm straight-line jump (implied 0.2 kn), 26.104,121.783 -> 25.972,121.894
- [SHUNXING39/CMR/613003889 (no IMO)] 1 further gap(s) >= 6 h without movement (port / anchorage / sparse data) - not scored

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

### Low speed (<= 3 kn) for 2 h or more  `SLOW_LOITERING` (+20)
- [XINGSHUN39/TZA/677087200] 2025-01-03 17:49 UTC -> 2025-01-03 21:01 UTC: 3.2 h slow moving, mean AIS speed 1.7 kn, path 5.7 nm, net 1.1 nm, at 25.374,121.750
- [SHUNXING39/CMR/613003889 (no IMO)] 2025-01-02 06:13 UTC -> 2025-01-02 13:51 UTC: 7.6 h stationary (anchored or drifting), mean AIS speed 0.5 kn, path 2.3 nm, net 1.9 nm, at 25.663,122.057
- [SHUNXING39/CMR/613003889 (no IMO)] 2025-01-02 15:17 UTC -> 2025-01-02 17:47 UTC: 2.5 h slow moving, mean AIS speed 1.3 kn, path 2.2 nm, net 2.1 nm, at 25.580,121.938
- [SHUNXING39/CMR/613003889 (no IMO)] 2025-01-02 22:57 UTC -> 2025-01-03 05:07 UTC: 6.2 h slow moving, mean AIS speed 1.0 kn, path 5.8 nm, net 5.4 nm, at 25.403,121.807

> Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

### Zig-zag / looping movement  `ZIGZAG` (+10)
- [XINGSHUN39/TZA/677087200] 2025-01-03 08:52 UTC -> 2025-01-03 14:32 UTC: 15.2 nm sailed, only 3.1 nm net, at 25.335,121.707
- [XINGSHUN39/TZA/677087200] 2025-01-03 16:02 UTC -> 2025-01-03 21:57 UTC: 10.7 nm sailed, only 1.1 nm net, at 25.350,121.747

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

## Track around the reported incident time

Reported time (approximate): 2025-01-02 23:40 UTC. Points within +/- 3 h:

| Time (UTC) | Identity | Lat | Lon | AIS speed (kn) |
|---|---|---|---|---|
| 2025-01-02 20:41 | SHUNXING39/CMR/613003889 (no IMO) | 25.4911 | 121.9173 | 0.6 |
| 2025-01-02 20:42 | SHUNXING39/CMR/613003889 (no IMO) | 25.4908 | 121.9175 | 1.3 |
| 2025-01-02 20:44 | SHUNXING39/CMR/613003889 (no IMO) | 25.4902 | 121.9177 | 1.1 |
| 2025-01-02 20:45 | SHUNXING39/CMR/613003889 (no IMO) | 25.4897 | 121.9178 | 2.2 |
| 2025-01-02 20:46 | SHUNXING39/CMR/613003889 (no IMO) | 25.4892 | 121.9178 | 1.5 |
| 2025-01-02 20:54 | SHUNXING39/CMR/613003889 (no IMO) | 25.4849 | 121.9162 | 3.9 |
| 2025-01-02 20:55 | SHUNXING39/CMR/613003889 (no IMO) | 25.4843 | 121.9158 | 4.5 |
| 2025-01-02 22:25 | SHUNXING39/CMR/613003889 (no IMO) | 25.4234 | 121.8304 | 5.4 |
| 2025-01-02 22:57 | SHUNXING39/CMR/613003889 (no IMO) | 25.4028 | 121.8065 | 0.8 |
| 2025-01-02 22:58 | SHUNXING39/CMR/613003889 (no IMO) | 25.4026 | 121.8063 | 2.0 |
| 2025-01-02 23:00 | SHUNXING39/CMR/613003889 (no IMO) | 25.4021 | 121.8057 | 0.2 |
| 2025-01-02 23:01 | SHUNXING39/CMR/613003889 (no IMO) | 25.4017 | 121.8054 | 2.0 |
| 2025-01-02 23:20 | SHUNXING39/CMR/613003889 (no IMO) | 25.3939 | 121.7971 | 0.2 |
| 2025-01-02 23:23 | SHUNXING39/CMR/613003889 (no IMO) | 25.3931 | 121.7958 | 3.0 |
| 2025-01-02 23:41 | SHUNXING39/CMR/613003889 (no IMO) | 25.3857 | 121.7861 | 0.5 |
| 2025-01-02 23:42 | SHUNXING39/CMR/613003889 (no IMO) | 25.3854 | 121.7857 | 2.6 |
| 2025-01-03 00:04 | SHUNXING39/CMR/613003889 (no IMO) | 25.3789 | 121.7745 | 0.2 |
| 2025-01-03 00:06 | SHUNXING39/CMR/613003889 (no IMO) | 25.3790 | 121.7740 | 0.4 |
| 2025-01-03 00:09 | SHUNXING39/CMR/613003889 (no IMO) | 25.3792 | 121.7737 | 0.8 |
| 2025-01-03 00:11 | SHUNXING39/CMR/613003889 (no IMO) | 25.3795 | 121.7736 | 0.9 |
| 2025-01-03 00:12 | SHUNXING39/CMR/613003889 (no IMO) | 25.3795 | 121.7736 | 0.0 |
| 2025-01-03 00:14 | SHUNXING39/CMR/613003889 (no IMO) | 25.3795 | 121.7734 | 0.3 |
| 2025-01-03 00:17 | SHUNXING39/CMR/613003889 (no IMO) | 25.3797 | 121.7732 | 1.2 |
| 2025-01-03 00:18 | SHUNXING39/CMR/613003889 (no IMO) | 25.3799 | 121.7730 | 0.5 |
| 2025-01-03 00:28 | SHUNXING39/CMR/613003889 (no IMO) | 25.3806 | 121.7727 | 0.0 |
| 2025-01-03 00:30 | SHUNXING39/CMR/613003889 (no IMO) | 25.3806 | 121.7726 | 0.3 |
| 2025-01-03 00:31 | SHUNXING39/CMR/613003889 (no IMO) | 25.3805 | 121.7726 | 0.6 |
| 2025-01-03 00:33 | SHUNXING39/CMR/613003889 (no IMO) | 25.3805 | 121.7727 | 0.0 |
| 2025-01-03 00:34 | SHUNXING39/CMR/613003889 (no IMO) | 25.3806 | 121.7727 | 0.4 |
| 2025-01-03 00:36 | SHUNXING39/CMR/613003889 (no IMO) | 25.3806 | 121.7727 | 0.4 |
| 2025-01-03 00:51 | SHUNXING39/CMR/613003889 (no IMO) | 25.3810 | 121.7724 | 0.8 |
| 2025-01-03 00:53 | SHUNXING39/CMR/613003889 (no IMO) | 25.3809 | 121.7725 | 0.2 |
| 2025-01-03 00:54 | SHUNXING39/CMR/613003889 (no IMO) | 25.3809 | 121.7725 | 0.5 |
| 2025-01-03 00:57 | SHUNXING39/CMR/613003889 (no IMO) | 25.3814 | 121.7723 | 0.4 |
| 2025-01-03 00:58 | SHUNXING39/CMR/613003889 (no IMO) | 25.3815 | 121.7722 | 1.5 |
| 2025-01-03 00:59 | SHUNXING39/CMR/613003889 (no IMO) | 25.3816 | 121.7723 | 0.2 |
| 2025-01-03 01:02 | SHUNXING39/CMR/613003889 (no IMO) | 25.3817 | 121.7723 | 0.4 |
| 2025-01-03 01:04 | SHUNXING39/CMR/613003889 (no IMO) | 25.3816 | 121.7722 | 0.6 |
| 2025-01-03 01:08 | SHUNXING39/CMR/613003889 (no IMO) | 25.3814 | 121.7715 | 1.4 |
| 2025-01-03 01:09 | SHUNXING39/CMR/613003889 (no IMO) | 25.3812 | 121.7709 | 2.0 |
| 2025-01-03 01:12 | SHUNXING39/CMR/613003889 (no IMO) | 25.3812 | 121.7704 | 0.3 |
| 2025-01-03 01:14 | SHUNXING39/CMR/613003889 (no IMO) | 25.3811 | 121.7700 | 1.0 |

## Notes

- 276 track points inside the analysis window (326 loaded, 2 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
