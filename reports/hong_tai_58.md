# Hong Tai 58 - TPKM-3 cable Taiwan-Penghu

Case file with context and sources: [hong_tai_58.md](../cases/hong_tai_58.md)

| | Score | Identity | Flag & registry | Behaviour |
|---|---|---|---|---|
| Before the incident | 100 HIGH | 130 | 30 | 20 |
| Full data | 100 HIGH | 130 | 30 | 30 |

Timestamp cut-off: 2025-02-24 16:00 UTC.<br>
Analysis window: 2025-02-22 00:00 - 2025-02-26 00:00 UTC.  
_Heuristic research indicators only. The score is not a probability or evidence of intent or responsibility for damage. LOW may reflect limited data. Overlapping rules can add points for the same event. The combined score is capped at 100; group totals are uncapped. Bundled sources: Global Fishing Watch (CC BY-NC 4.0); cable routes © OpenStreetMap contributors (ODbL); UK Sanctions List (OGL v3) via OpenSanctions (CC BY-NC 4.0)._

## Before the incident

Retrospective timestamp filter of the bundled snapshot. Current identity links, registry matches, manual associations and fixed 2025 flag weights remain; this does not reconstruct an advance warning.

- 4 distinct name/flag combinations in the 5 years before 2025-02-24 (5 linked records in total) (+30): \* JIN LONG 389 / CHN / MMSI 413762751 (2012-08-23 - 2022-10-09, registry + AIS)
- Overlapping first/last dates for linked AIS identities (+20): 2025-01-05 - 2025-02-05: HONGTAI58/TGO/671756000 and HONGTA8/TZA/677082100
- Possible identity handover (one AIS track stops, another starts nearby) (+20): HONGTAI58/671756000 (IMO 8357069) stops 2024-12-15 02:01 UTC at 34.278,128.456 -&gt; HONGTA 8/677082100 (IMO 8357069) starts 2024-12-15 03:17 UTC at 34.278,128.456 (76 min, 0.0 nm)
- Linked identities report distant positions within one hour (+20): HONGTAI58/671756000 (no IMO) at 25.98,120.91 (2024-12-17 21:30 UTC) vs HONGTA 8/677082100 (IMO 8357069) at 34.69,128.88 (2024-12-17 20:37 UTC): 666 nm apart
- Crossed a mapped cable or pipeline at reduced speed (+20): 2025-02-22 03:49 UTC -&gt; 05:20: crosses unnamed pipeline (OSM way 1357665582) at 4.0 kn over ground, around 23.045,119.979
- 1 flag change(s) (+15): 2023-07-31: CHN -&gt; TGO (Paris MoU black, ITF flag of convenience)  \[DONGSHUN3 -&gt; HONGTAI58\]  (recent)
- Selected AIS identity has no registry match in GFW; an earlier identity did (+15): last confirmed: DONGSHUN3 / CHN / MMSI 413762751 (2022-10-27 - 2023-09-05, registry record)
- MMSI shared with other vessels (2 within 2 years, 4 outside or undated) (+15): MMSI 677082100 also used by YEKTA 3 / TZA / MMSI 677082100 (2020-09-14 - 2024-07-19, self-reported AIS only), IMO 8889842  (within 2 years)
- Known name reported under an additional MMSI (+15): HONGTAI58 / TGO / MMSI 671666000 (2024-11-27 - 2024-12-04, self-reported AIS only) - MMSI also used by KARAM
- Identity also used without its IMO number (+10): HONGTAI58 / TGO / MMSI 671756000 (2023-11-21 - 2025-02-24, self-reported AIS only) - same name and MMSI, but no IMO number broadcast

### Notes

- 180 track points inside the analysis window (431 loaded, 1 identity track(s)).
- Timestamp filtering retains current identity links, registry matches and fixed 2025 flag weights; it does not reconstruct what was known at the cut-off.
- Linked identities may belong to multiple physical hulls; the score describes an identity cluster.

## Full data

### Identities

| Name | Flag | MMSI | IMO | First seen | Last seen | Source |
|---|---|---|---|---|---|---|
| JIN LONG 389 | CHN | 413762751 | - | 2012-08-23 | 2022-10-09 | registry + AIS |
| DONGSHUN3 | CHN | 413762751 | 8357069 | 2022-10-27 | 2023-09-05 | registry record |
| HONGTAI58 | TGO | 671756000 | 8357069 | 2023-07-31 | 2025-02-27 | self-reported AIS only |
| HONGTA 8 | TZA | 677082100 | 8357069 | 2024-12-15 | 2025-01-02 | self-reported AIS only |
| HONGTA8 | TZA | 677082100 | - | 2025-01-05 | 2025-02-05 | self-reported AIS only |

### Signals

#### Identity (+130)

##### 4 distinct name/flag combinations in the 5 years before 2025-02-26 (5 linked records in total) (`MULTI_IDENTITY`, +30)

- \* JIN LONG 389 / CHN / MMSI 413762751 (2012-08-23 - 2022-10-09, registry + AIS)
- \* DONGSHUN3 / CHN / MMSI 413762751 (2022-10-27 - 2023-09-05, registry record)
- \* HONGTAI58 / TGO / MMSI 671756000 (2023-07-31 - 2025-02-27, self-reported AIS only)
- \* HONGTA 8 / TZA / MMSI 677082100 (2024-12-15 - 2025-01-02, self-reported AIS only)
- \* HONGTA8 / TZA / MMSI 677082100 (2025-01-05 - 2025-02-05, self-reported AIS only)

\* = dated use during the look-back period (scored); other records are outside it or undated.

##### MMSI shared with other vessels (2 within 2 years, 4 outside or undated) (`MMSI_REUSE`, +15)

- MMSI 677082100 also used by YEKTA 3 / TZA / MMSI 677082100 (2020-09-14 - 2024-07-19, self-reported AIS only), IMO 8889842  (within 2 years)
- MMSI 677082100 also used by LADY EMERALD / TZA / MMSI 677082100 (2024-06-29 - 2024-11-07, self-reported AIS only)  (within 2 years)
- MMSI 671756000 also used by STEEL DEVELOPER / TGO / MMSI 671756000 (2016-05-10 - 2016-05-28, registry + AIS), IMO 9171424
- MMSI 677082100 also used by A DAL 3 / TZA / MMSI 677082100 (2016-01-19 - 2016-05-25, registry + AIS)
- MMSI 677082100 also used by A DAL 3 / TZA / MMSI 677082100 (2016-05-28 - 2016-11-10, registry + AIS), IMO 8713299
- MMSI 677082100 also used by GOLDEN SEA / TZA / MMSI 677082100 (2017-11-27 - 2018-11-07, registry + AIS), IMO 8800298

Legitimate MMSI reassignment and errors in identity linking are possible.

##### Known name reported under an additional MMSI (`NAME_ON_OTHER_MMSI`, +15)

- HONGTAI58 / TGO / MMSI 671666000 (2024-11-27 - 2024-12-04, self-reported AIS only) - MMSI also used by KARAM
- HONGTAI58 / TGO / MMSI 671280000 (2023-12-25 - 2023-12-26, self-reported AIS only) - MMSI also used by XINJINLIN6

Short episodes can also be typing errors in the AIS set-up; repeated use is the signal.

##### Identity also used without its IMO number (`IMO_HIDDEN`, +10)

- HONGTAI58 / TGO / MMSI 671756000 (2023-11-21 - 2025-02-27, self-reported AIS only) - same name and MMSI, but no IMO number broadcast

A missing IMO can reflect incomplete AIS configuration; it does not establish deliberate concealment.

##### Overlapping first/last dates for linked AIS identities (`CONCURRENT_IDENTITIES`, +20)

- 2025-01-05 - 2025-02-05: HONGTAI58/TGO/671756000 and HONGTA8/TZA/677082100

Overlap is computed from first/last AIS message per identity; check the tracks (handover / parallel signals).

##### Possible identity handover (one AIS track stops, another starts nearby) (`IDENTITY_HANDOVER`, +20)

- HONGTAI58/671756000 (IMO 8357069) stops 2024-12-15 02:01 UTC at 34.278,128.456 -&gt; HONGTA 8/677082100 (IMO 8357069) starts 2024-12-15 03:17 UTC at 34.278,128.456 (76 min, 0.0 nm)

A reachable position is not proof of the same hull. Coverage gaps, ports and incorrect links can produce similar candidates.

##### Linked identities report distant positions within one hour (`PARALLEL_TRACKS`, +20)

- HONGTAI58/671756000 (no IMO) at 25.98,120.91 (2024-12-17 21:30 UTC) vs HONGTA 8/677082100 (IMO 8357069) at 34.69,128.88 (2024-12-17 20:37 UTC): 666 nm apart
- HONGTAI58/671756000 (no IMO) at 25.59,120.24 (2025-01-12 12:56 UTC) vs HONGTA8/677082100 (no IMO) at 35.08,129.00 (2025-01-12 12:45 UTC): 728 nm apart

Possible shared identity data, incorrect GFW links or erroneous positions; this does not establish that multiple physical hulls were present.

#### Flag & registry (+30)

##### 1 flag change(s) (`FLAG_CHANGE`, +15)

- 2023-07-31: CHN -&gt; TGO (Paris MoU black, ITF flag of convenience)  \[DONGSHUN3 -&gt; HONGTAI58\]  (recent)

Scored: changes in the 3 years before 2025-02-26 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

##### Selected AIS identity has no registry match in GFW; an earlier identity did (`REGISTRY_LOST`, +15)

- last confirmed: DONGSHUN3 / CHN / MMSI 413762751 (2022-10-27 - 2023-09-05, registry record)
- selected for 2025-02-26: HONGTAI58 / TGO / MMSI 671756000 (2023-07-31 - 2025-02-27, self-reported AIS only)

GFW registry coverage is incomplete; a missing match does not establish invalid registration.

#### Behaviour (+30)

##### AIS gaps (not scored) (`AIS_GAP`, +0)

- 1 further gap(s) &gt;= 6 h without movement (port / anchorage / sparse data) - not scored

Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

##### Low speed (&lt;= 3 kn) for 2 h or more (`SLOW_LOITERING`, +0)

- 2025-02-22 10:40 UTC -&gt; 2025-02-24 06:11 UTC: 43.5 h stationary (anchored or drifting), mean AIS speed 1.3 kn, path 2.3 nm, net 0.8 nm, at 23.304,120.016
- 2025-02-24 07:21 UTC -&gt; 2025-02-24 19:06 UTC: 11.8 h stationary (anchored or drifting), mean AIS speed 1.2 kn, path 0.8 nm, net 0.2 nm, at 23.291,120.016

Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

##### Sustained speed drop while underway (`SPEED_DROP`, +10)

- 2025-02-24 20:44 UTC -&gt; 2025-02-24 22:15 UTC: 1.5 h at 2.2-3.5 kn (cruising median 6.3 kn), from 23.308,119.990

Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

##### Crossed a mapped cable or pipeline at reduced speed (`CABLE_CROSSING_SLOW`, +20)

- 2025-02-22 03:49 UTC -&gt; 05:20: crosses unnamed pipeline (OSM way 1357665582) at 4.0 kn over ground, cruising median 6.3 kn, around 23.045,119.979

Straight-line crossings reconstructed between sparse positions. OpenStreetMap routes are approximate and incomplete. This does not establish contact with a cable, anchor use or intent.

### Track around the reported incident time

Reported time (approximate): 2025-02-24 19:03 UTC. Points within +/- 3 h:

| Time (UTC) | Identity | Lat | Lon | AIS speed (kn) |
|---|---|---|---|---|
| 2025-02-24 16:35 | hong\_tai\_58 | 23.2901 | 120.0161 | 2.1 |
| 2025-02-24 16:43 | hong\_tai\_58 | 23.2901 | 120.0161 | 1.1 |
| 2025-02-24 17:38 | hong\_tai\_58 | 23.2901 | 120.0163 | 0.0 |
| 2025-02-24 17:40 | hong\_tai\_58 | 23.2901 | 120.0162 | 0.2 |
| 2025-02-24 17:56 | hong\_tai\_58 | 23.2901 | 120.0164 | 0.4 |
| 2025-02-24 17:58 | hong\_tai\_58 | 23.2901 | 120.0162 | 0.3 |
| 2025-02-24 18:14 | hong\_tai\_58 | 23.2901 | 120.0163 | 0.9 |
| 2025-02-24 18:15 | hong\_tai\_58 | 23.2901 | 120.0162 | 0.9 |
| 2025-02-24 18:17 | hong\_tai\_58 | 23.2901 | 120.0161 | 0.0 |
| 2025-02-24 18:19 | hong\_tai\_58 | 23.2901 | 120.0162 | 1.4 |
| 2025-02-24 18:57 | hong\_tai\_58 | 23.2925 | 120.0155 | 2.9 |
| 2025-02-24 19:02 | hong\_tai\_58 | 23.2932 | 120.0131 | 0.5 |
| 2025-02-24 19:05 | hong\_tai\_58 | 23.2931 | 120.0127 | 2.2 |
| 2025-02-24 19:06 | hong\_tai\_58 | 23.2928 | 120.0130 | 2.4 |
| 2025-02-24 19:10 | hong\_tai\_58 | 23.2935 | 120.0163 | 4.5 |
| 2025-02-24 19:12 | hong\_tai\_58 | 23.2960 | 120.0171 | 5.2 |
| 2025-02-24 20:30 | hong\_tai\_58 | 23.3118 | 119.9874 | 2.7 |
| 2025-02-24 20:33 | hong\_tai\_58 | 23.3120 | 119.9882 | 0.4 |
| 2025-02-24 20:34 | hong\_tai\_58 | 23.3121 | 119.9883 | 0.4 |
| 2025-02-24 20:44 | hong\_tai\_58 | 23.3076 | 119.9899 | 2.4 |
| 2025-02-24 20:45 | hong\_tai\_58 | 23.3073 | 119.9900 | 2.2 |

### Notes

- 218 track points inside the analysis window (469 loaded, 1 identity track(s)).
- Linked identities may belong to multiple physical hulls; the score describes an identity cluster.
