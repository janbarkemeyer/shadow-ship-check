# Control: Finlandia (Helsinki-Tallinn ferry), Gulf of Finland

| | Score | Identity | Flag & registry | Behaviour |
|---|---|---|---|---|
| Window-end cut-off | 0 LOW | 0 | 0 | 0 |
| Full data | 0 LOW | 0 | 0 | 0 |

Timestamp cut-off: 2024-12-28 23:59 UTC.<br>
Analysis window: 2024-12-23 00:00 - 2024-12-28 23:59 UTC.  
_Heuristic research indicators only. The score is not a probability or evidence of intent or responsibility for damage. LOW may reflect limited data. Overlapping rules can add points for the same event. The combined score is capped at 100; group totals are uncapped. Bundled sources: Global Fishing Watch (CC BY-NC 4.0); cable routes © OpenStreetMap contributors (ODbL); UK Sanctions List (OGL v3) via OpenSanctions (CC BY-NC 4.0)._

## Window-end cut-off

Retrospective timestamp filter of the bundled snapshot. Current identity links, registry matches, manual associations and fixed 2025 flag weights remain; this does not reconstruct an advance warning.

This control has no incident time. Its cut-off is the end of its analysis window.

No scored signals.

### Notes

- 302 track points inside the analysis window (753 loaded, 1 identity track(s)).
- Timestamp filtering retains current identity links, registry matches and fixed 2025 flag weights; it does not reconstruct what was known at the cut-off.

## Full data

### Identities

| Name | Flag | MMSI | IMO | First seen | Last seen | Source |
|---|---|---|---|---|---|---|
| MOBY FREEDOM | ITA | 247034500 | 9214379 | 2012-01-01 | 2012-03-08 | self-reported AIS only |
| FINLANDIA | FIN | 230628000 | 9214379 | 2012-03-08 | 2026-10-23 | registry + AIS |

### Signals

#### Identity (+0)

##### 1 distinct name/flag combinations in the 5 years before 2024-12-28 (2 linked records in total) (`MULTI_IDENTITY`, +0)

-   MOBY FREEDOM / ITA / MMSI 247034500 (2012-01-01 - 2012-03-08, self-reported AIS only)
- \* FINLANDIA / FIN / MMSI 230628000 (2012-03-08 - 2026-10-23, registry + AIS)

\* = dated use during the look-back period (scored); other records are outside it or undated.

#### Flag & registry (+0)

##### 1 flag change(s) (`FLAG_CHANGE`, +0)

- 2012-03-08: ITA -&gt; FIN (Paris MoU white)  \[MOBY FREEDOM -&gt; FINLANDIA\]

Scored: changes in the 3 years before 2024-12-28 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

#### Behaviour (+0)

##### Low speed (&lt;= 3 kn) for 2 h or more (`SLOW_LOITERING`, +0)

- 2024-12-23 01:19 UTC -&gt; 2024-12-23 03:40 UTC: 2.3 h stationary (anchored or drifting), mean AIS speed 0.8 kn, path 0.1 nm, net 0.1 nm, at 59.445,24.763
- 2024-12-23 22:00 UTC -&gt; 2024-12-24 03:40 UTC: 5.7 h stationary (anchored or drifting), mean AIS speed 0.7 kn, path 0.2 nm, net 0.0 nm, at 59.446,24.766
- 2024-12-24 12:06 UTC -&gt; 2024-12-26 06:42 UTC: 42.6 h stationary (anchored or drifting), mean AIS speed 0.2 kn, path 0.2 nm, net 0.2 nm, at 60.147,24.908
- 2024-12-26 22:00 UTC -&gt; 2024-12-27 03:38 UTC: 5.6 h stationary (anchored or drifting), mean AIS speed 0.7 kn, path 0.2 nm, net 0.1 nm, at 59.446,24.767
- 2024-12-27 22:00 UTC -&gt; 2024-12-28 03:37 UTC: 5.6 h stationary (anchored or drifting), mean AIS speed 0.7 kn, path 0.2 nm, net 0.1 nm, at 59.446,24.767
- 2024-12-28 18:55 UTC -&gt; 2024-12-28 23:30 UTC: 4.6 h stationary (anchored or drifting), mean AIS speed 0.0 kn, path 0.0 nm, net 0.0 nm, at 60.149,24.912

Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

### Notes

- 302 track points inside the analysis window (1093 loaded, 1 identity track(s)).
