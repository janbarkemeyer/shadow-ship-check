# Yi Peng 3 - BCS East-West Interlink and C-Lion1, Baltic Sea

Case file with context and sources: [yi_peng_3.md](../cases/yi_peng_3.md)

| | Score | Identity | Flag & registry | Behaviour |
|---|---|---|---|---|
| Before the incident | 5 LOW | 0 | 5 | 0 |
| Full data | 35 MEDIUM | 0 | 5 | 30 |

Timestamp cut-off: 2024-11-17 08:00 UTC.<br>
Analysis window: 2024-11-16 12:00 - 2024-11-18 18:00 UTC.  
_Heuristic research indicators only. The score is not a probability or evidence of intent or responsibility for damage. LOW may reflect limited data. Overlapping rules can add points for the same event. The combined score is capped at 100; group totals are uncapped. Bundled sources: Global Fishing Watch (CC BY-NC 4.0); cable routes © OpenStreetMap contributors (ODbL); UK Sanctions List (OGL v3) via OpenSanctions (CC BY-NC 4.0)._

## Before the incident

Retrospective timestamp filter of the bundled snapshot. Current identity links, registry matches, manual associations and fixed 2025 flag weights remain; this does not reconstruct an advance warning.

- Selected AIS identity has no registry match in GFW; an earlier identity did (+5): last confirmed: AVRA / LBR / MMSI 636017118 (2015-07-30 - 2016-12-02, registry + AIS)

### Notes

- 13 track points inside the analysis window (118 loaded, 1 identity track(s)).
- Timestamp filtering retains current identity links, registry matches and fixed 2025 flag weights; it does not reconstruct what was known at the cut-off.
- Incident excerpt omitted: the reported time is after the timestamp cut-off.

## Full data

### Identities

| Name | Flag | MMSI | IMO | First seen | Last seen | Source |
|---|---|---|---|---|---|---|
| AVRA | GRC | 240583000 | 9224984 | 2012-01-09 | 2015-07-30 | self-reported AIS only |
| AVRA | LBR | 636017118 | 9224984 | 2015-07-30 | 2016-12-02 | registry + AIS |
| YI PENG 3 | CHN | 414270000 | 9224984 | 2020-06-30 | 2026-10-23 | self-reported AIS only |

### Signals

#### Identity (+0)

##### 1 distinct name/flag combinations in the 5 years before 2024-11-18 (3 linked records in total) (`MULTI_IDENTITY`, +0)

-   AVRA / GRC / MMSI 240583000 (2012-01-09 - 2015-07-30, self-reported AIS only)
-   AVRA / LBR / MMSI 636017118 (2015-07-30 - 2016-12-02, registry + AIS)
- \* YI PENG 3 / CHN / MMSI 414270000 (2020-06-30 - 2026-10-23, self-reported AIS only)

\* = dated use during the look-back period (scored); other records are outside it or undated.

#### Flag & registry (+5)

##### 1 flag change(s) (`FLAG_CHANGE`, +0)

- 2015-07-30: GRC -&gt; LBR (Paris MoU white, ITF flag of convenience)  \[AVRA -&gt; AVRA\]

Scored: changes in the 3 years before 2024-11-18 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

##### Selected AIS identity has no registry match in GFW; an earlier identity did (`REGISTRY_LOST`, +5)

- last confirmed: AVRA / LBR / MMSI 636017118 (2015-07-30 - 2016-12-02, registry + AIS)
- selected for 2024-11-18: YI PENG 3 / CHN / MMSI 414270000 (2020-06-30 - 2026-10-23, self-reported AIS only)

GFW registry coverage is incomplete; a missing match does not establish invalid registration. The last dated match was more than 5 years before the reference date.

#### Behaviour (+30)

##### Sustained speed drop while underway (`SPEED_DROP`, +10)

- 2024-11-17 17:59 UTC -&gt; 2024-11-17 19:30 UTC: 1.5 h at 3.9-4.3 kn (cruising median 8.9 kn), from 56.164,18.226

Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

##### Crossed a mapped cable or pipeline at reduced speed (`CABLE_CROSSING_SLOW`, +20)

- 2024-11-18 01:39 UTC -&gt; 03:10: crosses Nord Stream 1, Nord Stream 2, C-Lion 1 at 6.2 kn over ground, cruising median 8.9 kn, around 55.860,16.944

Straight-line crossings reconstructed between sparse positions. OpenStreetMap routes are approximate and incomplete. This does not establish contact with a cable, anchor use or intent.

### Track around the reported incident time

Reported time (approximate): 2024-11-18 02:00 UTC. Points within +/- 3 h:

| Time (UTC) | Identity | Lat | Lon | AIS speed (kn) |
|---|---|---|---|---|
| 2024-11-18 00:01 | yi\_peng\_3 | 55.9262 | 17.3880 | 6.7 |
| 2024-11-18 01:39 | yi\_peng\_3 | 55.8791 | 17.0784 | 6.0 |
| 2024-11-18 03:10 | yi\_peng\_3 | 55.8407 | 16.8104 | 5.1 |
| 2024-11-18 04:40 | yi\_peng\_3 | 55.8050 | 16.5361 | 7.0 |

### Notes

- 50 track points inside the analysis window (324 loaded, 1 identity track(s)).
