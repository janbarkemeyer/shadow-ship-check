# Control: Yi Peng 5 (comparison vessel near Taiwan)

| | Score | Identity | Flag & registry | Behaviour |
|---|---|---|---|---|
| Window-end cut-off | 5 LOW | 0 | 5 | 0 |
| Full data | 5 LOW | 0 | 5 | 0 |

Timestamp cut-off: 2024-11-18 18:00 UTC.<br>
Analysis window: 2024-11-16 12:00 - 2024-11-18 18:00 UTC.  
_Heuristic research indicators only. The score is not a probability or evidence of intent or responsibility for damage. LOW may reflect limited data. Overlapping rules can add points for the same event. The combined score is capped at 100; group totals are uncapped. Bundled sources: Global Fishing Watch (CC BY-NC 4.0); cable routes © OpenStreetMap contributors (ODbL); UK Sanctions List (OGL v3) via OpenSanctions (CC BY-NC 4.0)._

## Window-end cut-off

Retrospective timestamp filter of the bundled snapshot. Current identity links, registry matches, manual associations and fixed 2025 flag weights remain; this does not reconstruct an advance warning.

This control has no incident time. Its cut-off is the end of its analysis window.

- Selected AIS identity has no registry match in GFW; an earlier identity did (+5): last confirmed: ELEFTHERIA / GRC / MMSI 239850000 (2012-01-01 - 2018-05-19, registry + AIS)

### Notes

- 355 track points inside the analysis window (1004 loaded, 1 identity track(s)).
- Timestamp filtering retains current identity links, registry matches and fixed 2025 flag weights; it does not reconstruct what was known at the cut-off.
- This control is near Taiwan, outside the Baltic incident region; its cut-off is the window end.

## Full data

### Identities

| Name | Flag | MMSI | IMO | First seen | Last seen | Source |
|---|---|---|---|---|---|---|
| ELEFTHERIA | GRC | 239850000 | 9221190 | 2012-01-01 | 2018-05-19 | registry + AIS |
| YI PENG 5 | CHN | 414388000 | 9221190 | 2018-05-16 | 2026-10-23 | self-reported AIS only |

### Signals

#### Identity (+0)

##### 1 distinct name/flag combinations in the 5 years before 2024-11-18 (2 linked records in total) (`MULTI_IDENTITY`, +0)

-   ELEFTHERIA / GRC / MMSI 239850000 (2012-01-01 - 2018-05-19, registry + AIS)
- \* YI PENG 5 / CHN / MMSI 414388000 (2018-05-16 - 2026-10-23, self-reported AIS only)

\* = dated use during the look-back period (scored); other records are outside it or undated.

#### Flag & registry (+5)

##### 1 flag change(s) (`FLAG_CHANGE`, +0)

- 2018-05-16: GRC -&gt; CHN (Paris MoU white)  \[ELEFTHERIA -&gt; YI PENG 5\]

Scored: changes in the 3 years before 2024-11-18 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

##### Selected AIS identity has no registry match in GFW; an earlier identity did (`REGISTRY_LOST`, +5)

- last confirmed: ELEFTHERIA / GRC / MMSI 239850000 (2012-01-01 - 2018-05-19, registry + AIS)
- selected for 2024-11-18: YI PENG 5 / CHN / MMSI 414388000 (2018-05-16 - 2026-10-23, self-reported AIS only)

GFW registry coverage is incomplete; a missing match does not establish invalid registration. The last dated match was more than 5 years before the reference date.

#### Behaviour (+0)

##### Low speed (&lt;= 3 kn) for 2 h or more (`SLOW_LOITERING`, +0)

- 2024-11-16 12:10 UTC -&gt; 2024-11-18 06:31 UTC: 42.3 h stationary (anchored or drifting), mean AIS speed 0.4 kn, path 4.2 nm, net 0.1 nm, at 26.468,120.002
- 2024-11-18 07:10 UTC -&gt; 2024-11-18 17:58 UTC: 10.8 h stationary (anchored or drifting), mean AIS speed 0.6 kn, path 0.9 nm, net 0.0 nm, at 26.467,120.003

Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

### Notes

- 355 track points inside the analysis window (1345 loaded, 1 identity track(s)).
- This control is near Taiwan, outside the Baltic incident region; its cut-off is the window end.
