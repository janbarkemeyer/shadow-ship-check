# Xingshun 39 (Shunxing 39) - cable damage north of Keelung

Case file with context and sources: [xingshun_39.md](../cases/xingshun_39.md)

| | Score | Identity | Flag & registry | Behaviour |
|---|---|---|---|---|
| Before the incident | 100 HIGH | 80 | 40 | 15 |
| Full data | 100 HIGH | 80 | 40 | 65 |

Timestamp cut-off: 2025-01-02 12:00 UTC.<br>
Analysis window: 2025-01-02 00:00 - 2025-01-05 00:00 UTC.  
_Heuristic research indicators only. The score is not a probability or evidence of intent or responsibility for damage. LOW may reflect limited data. Overlapping rules can add points for the same event. The combined score is capped at 100; group totals are uncapped. Bundled sources: Global Fishing Watch (CC BY-NC 4.0); cable routes © OpenStreetMap contributors (ODbL); UK Sanctions List (OGL v3) via OpenSanctions (CC BY-NC 4.0)._

## Before the incident

Retrospective timestamp filter of the bundled snapshot. Current identity links, registry matches, manual associations and fixed 2025 flag weights remain; this does not reconstruct an advance warning.

- 4 distinct name/flag combinations in the 5 years before 2025-01-02 (6 linked records in total) (+30): \* BAOLONG36 / GUY / MMSI 750342000 (2022-11-17 - 2022-11-24, self-reported AIS only)
- 3 flag change(s) (+30): 2022-11-24: GUY -&gt; CMR (Paris MoU black, ITF flag of convenience)  \[BAOLONG36 -&gt; BAOLONG36\]  (recent)
- Overlapping first/last dates for linked AIS identities (+20): 2022-11-29 - 2023-02-10: BAOLONG36/CMR/613003836 and BAOLONG36/GUY/750342000
- Possible identity handover (one AIS track stops, another starts nearby) (+20): XINGSHUN39/TZA/677087200 stops 2024-12-28 22:11 UTC at 25.163,121.753 -&gt; SHUNXING39/CMR/613003889 (no IMO) starts 2024-12-29 02:44 UTC at 25.588,121.803 (273 min, 25.7 nm)
- AIS gaps (+15): \[XINGSHUN39/TZA/677087200\] no positions of this identity inside the analysis window; reachable linked observations exist, so no additional absence points (this does not establish continuous coverage)
- No dated registry match at or before the reference date in GFW (+10): selected for 2025-01-02: SHUNXING39 / CMR / MMSI 613003889 (2024-09-28 - 2025-01-02, self-reported AIS only)
- Identity also used without its IMO number (+10): XINGSHUN39 / TZA / MMSI 677087200 (2024-06-16 - 2024-09-29, self-reported AIS only) - same name and MMSI, but no IMO number broadcast

### Notes

- 51 track points inside the analysis window (101 loaded, 2 identity track(s)).
- Timestamp filtering retains current identity links, registry matches and fixed 2025 flag weights; it does not reconstruct what was known at the cut-off.
- SHUNXING39 without IMO is linked manually using later name and track evidence.

## Full data

### Identities

| Name | Flag | MMSI | IMO | First seen | Last seen | Source |
|---|---|---|---|---|---|---|
| BAOLONG36 | GUY | 750342000 | - | 2022-11-17 | 2022-11-24 | self-reported AIS only |
| BAOLONG36 | CMR | 613003836 | - | 2022-11-24 | 2023-02-10 | self-reported AIS only |
| BAOLONG36 | GUY | 750342000 | 8358427 | 2022-11-29 | 2023-05-12 | self-reported AIS only |
| BAOLONG36 | CMR | 613003836 | 8358427 | 2023-07-20 | 2023-09-11 | self-reported AIS only |
| XINGSHUN39 | TZA | 677087200 | 8358427 | 2024-03-04 | 2025-01-04 | self-reported AIS only |
| SHUNXING39 | CMR | 613003889 | - | 2024-09-28 | 2025-01-03 | self-reported AIS only |
| XINGSHUNNO.39 | TZA | 677087200 | - | 2025-08-14 | 2025-08-14 | self-reported AIS only |

### Signals

#### Identity (+80)

##### 4 distinct name/flag combinations in the 5 years before 2025-01-05 (7 linked records in total) (`MULTI_IDENTITY`, +30)

- \* BAOLONG36 / GUY / MMSI 750342000 (2022-11-17 - 2022-11-24, self-reported AIS only)
- \* BAOLONG36 / CMR / MMSI 613003836 (2022-11-24 - 2023-02-10, self-reported AIS only)
- \* BAOLONG36 / GUY / MMSI 750342000 (2022-11-29 - 2023-05-12, self-reported AIS only)
- \* BAOLONG36 / CMR / MMSI 613003836 (2023-07-20 - 2023-09-11, self-reported AIS only)
- \* XINGSHUN39 / TZA / MMSI 677087200 (2024-03-04 - 2025-01-04, self-reported AIS only)
- \* SHUNXING39 / CMR / MMSI 613003889 (2024-09-28 - 2025-01-03, self-reported AIS only)
-   XINGSHUNNO.39 / TZA / MMSI 677087200 (2025-08-14 - 2025-08-14, self-reported AIS only)

\* = dated use during the look-back period (scored); other records are outside it or undated.

##### Identity also used without its IMO number (`IMO_HIDDEN`, +10)

- XINGSHUN39 / TZA / MMSI 677087200 (2024-06-16 - 2024-09-29, self-reported AIS only) - same name and MMSI, but no IMO number broadcast

A missing IMO can reflect incomplete AIS configuration; it does not establish deliberate concealment.

##### Overlapping first/last dates for linked AIS identities (`CONCURRENT_IDENTITIES`, +20)

- 2022-11-29 - 2023-02-10: BAOLONG36/CMR/613003836 and BAOLONG36/GUY/750342000
- 2024-09-28 - 2025-01-03: XINGSHUN39/TZA/677087200 and SHUNXING39/CMR/613003889

Overlap is computed from first/last AIS message per identity; check the tracks (handover / parallel signals).

##### Possible identity handover (one AIS track stops, another starts nearby) (`IDENTITY_HANDOVER`, +20)

- SHUNXING39/CMR/613003889 (no IMO) stops 2025-01-03 08:19 UTC at 25.334,121.712 -&gt; XINGSHUN39/TZA/677087200 starts 2025-01-03 08:52 UTC at 25.335,121.707 (33 min, 0.2 nm)
- XINGSHUN39/TZA/677087200 stops 2024-12-28 22:11 UTC at 25.163,121.753 -&gt; SHUNXING39/CMR/613003889 (no IMO) starts 2024-12-29 02:44 UTC at 25.588,121.803 (273 min, 25.7 nm)

A reachable position is not proof of the same hull. Coverage gaps, ports and incorrect links can produce similar candidates.

#### Flag & registry (+40)

##### 3 flag change(s) (`FLAG_CHANGE`, +30)

- 2022-11-24: GUY -&gt; CMR (Paris MoU black, ITF flag of convenience)  \[BAOLONG36 -&gt; BAOLONG36\]  (recent)
- 2023-07-20: GUY -&gt; CMR (Paris MoU black, ITF flag of convenience)  \[BAOLONG36 -&gt; BAOLONG36\]  (recent)
- 2024-03-04: CMR -&gt; TZA (Paris MoU black, ITF flag of convenience)  \[BAOLONG36 -&gt; XINGSHUN39\]  (recent)

Scored: changes in the 3 years before 2025-01-05 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

##### No dated registry match at or before the reference date in GFW (`NO_REGISTRY`, +10)

- selected for 2025-01-05: XINGSHUN39 / TZA / MMSI 677087200 (2024-03-04 - 2025-01-04, self-reported AIS only)

GFW registry coverage varies by flag and access level; a missing or undated match is not proof of non-registration.

#### Behaviour (+65)

##### AIS gaps (`AIS_GAP`, +15)

- \[XINGSHUN39/TZA/677087200\] 2024-12-28 22:11 UTC -&gt; 2025-01-03 08:52 UTC: 130.7 h without position, 11 nm straight-line jump (implied 0.1 kn), 25.163,121.753 -&gt; 25.335,121.707; plausible linked positions reduce gap points from 20 to 10  &lt;-- overlaps the analysis window
- \[SHUNXING39/CMR/613003889 (no IMO)\] 2024-12-29 05:55 UTC -&gt; 2024-12-29 19:49 UTC: 13.9 h without position, 11 nm straight-line jump (implied 0.8 kn), 25.922,121.823 -&gt; 26.104,121.783
- \[SHUNXING39/CMR/613003889 (no IMO)\] 2024-12-29 20:07 UTC -&gt; 2024-12-31 14:07 UTC: 42.0 h without position, 10 nm straight-line jump (implied 0.2 kn), 26.104,121.783 -&gt; 25.972,121.894
- \[SHUNXING39/CMR/613003889 (no IMO)\] 1 further gap(s) &gt;= 6 h without movement (port / anchorage / sparse data) - not scored

Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

##### Low speed (&lt;= 3 kn) for 2 h or more (`SLOW_LOITERING`, +20)

- \[XINGSHUN39/TZA/677087200\] 2025-01-03 17:49 UTC -&gt; 2025-01-03 21:01 UTC: 3.2 h slow moving, mean AIS speed 1.7 kn, path 5.7 nm, net 1.1 nm, at 25.374,121.750
- \[SHUNXING39/CMR/613003889 (no IMO)\] 2025-01-02 06:13 UTC -&gt; 2025-01-02 13:51 UTC: 7.6 h stationary (anchored or drifting), mean AIS speed 0.5 kn, path 2.3 nm, net 1.9 nm, at 25.663,122.057
- \[SHUNXING39/CMR/613003889 (no IMO)\] 2025-01-02 15:17 UTC -&gt; 2025-01-02 17:47 UTC: 2.5 h slow moving, mean AIS speed 1.3 kn, path 2.2 nm, net 2.1 nm, at 25.580,121.938
- \[SHUNXING39/CMR/613003889 (no IMO)\] 2025-01-02 22:57 UTC -&gt; 2025-01-03 05:07 UTC: 6.2 h slow moving, mean AIS speed 1.0 kn, path 5.8 nm, net 5.4 nm, at 25.403,121.807

Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

##### Zig-zag / looping movement (`ZIGZAG`, +10)

- \[XINGSHUN39/TZA/677087200\] 2025-01-03 08:52 UTC -&gt; 2025-01-03 14:32 UTC: 15.2 nm sailed, only 3.1 nm net, at 25.335,121.707
- \[XINGSHUN39/TZA/677087200\] 2025-01-03 16:02 UTC -&gt; 2025-01-03 21:57 UTC: 10.7 nm sailed, only 1.1 nm net, at 25.350,121.747

Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

##### Crossed a mapped cable or pipeline at reduced speed (`CABLE_CROSSING_SLOW`, +20)

- \[XINGSHUN39/TZA/677087200\] 2025-01-03 17:49 UTC -&gt; 18:45: crosses unnamed telecom (OSM way 1334156416) at 3.3 kn over ground, around 25.397,121.763
- \[XINGSHUN39/TZA/677087200\] 2025-01-03 20:26 UTC -&gt; 20:49: crosses unnamed telecom (OSM way 1334156416) at 0.9 kn over ground, around 25.381,121.773
- \[XINGSHUN39/TZA/677087200\] 2025-01-03 23:13 UTC -&gt; 00:06: crosses unnamed telecom (OSM way 1334156416) at 2.1 kn over ground, around 25.372,121.758
- \[XINGSHUN39/TZA/677087200\] 2025-01-04 00:06 UTC -&gt; 01:37: crosses unnamed telecom (OSM way 1334156416) at 3.1 kn over ground, around 25.385,121.722
- \[SHUNXING39/CMR/613003889 (no IMO)\] 2025-01-02 23:42 UTC -&gt; 00:04: crosses unnamed telecom (OSM way 1334156416) at 1.9 kn over ground, cruising median 5.8 kn, around 25.382,121.780
- \[SHUNXING39/CMR/613003889 (no IMO)\] 2025-01-03 01:09 UTC -&gt; 01:12: crosses unnamed telecom (OSM way 1334156416) at 0.5 kn over ground, cruising median 5.8 kn, around 25.381,121.771

Straight-line crossings reconstructed between sparse positions. OpenStreetMap routes are approximate and incomplete. This does not establish contact with a cable, anchor use or intent.

### Track around the reported incident time

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

### Notes

- 276 track points inside the analysis window (326 loaded, 2 identity track(s)).
- SHUNXING39 without IMO is linked manually using later name and track evidence.
