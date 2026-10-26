# Control: Finlandia (Helsinki-Tallinn ferry), Gulf of Finland (before the incident)

**Score: 0/100 (LOW)**  
Analysis window: 2024-12-23 00:00 - 2024-12-28 23:59 UTC  
Data cut-off: 2024-12-28 23:59 UTC - only what GFW had recorded before this time  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| MOBY FREEDOM | ITA | 247034500 | 9214379 | 2012-01-01 | 2012-03-08 | self-reported AIS only |
| FINLANDIA | FIN | 230628000 | 9214379 | 2012-03-08 | 2024-12-28 | registry + AIS |

## Red flags

### 2 identities linked to the same hull (1 in the 5 years before 2024-12-28)  `MULTI_IDENTITY` (+0)
-   MOBY FREEDOM / ITA / MMSI 247034500 (2012-01-01 - 2012-03-08, self-reported AIS only)
- * FINLANDIA / FIN / MMSI 230628000 (2012-03-08 - 2024-12-28, registry + AIS)

> * = in use during the look-back period (scored); others are history.

### 1 flag change(s)  `FLAG_CHANGE` (+0)
- 2012-03-08: ITA -> FIN (Paris MoU white)  [MOBY FREEDOM -> FINLANDIA]

> Scored: changes in the 3 years before 2024-12-28 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

### Low speed (<= 3 kn) for 2 h or more  `SLOW_LOITERING` (+0)
- 2024-12-23 01:19 UTC -> 2024-12-23 03:40 UTC: 2.3 h stationary (anchored or drifting), mean AIS speed 0.8 kn, path 0.1 nm, net 0.1 nm, at 59.445,24.763
- 2024-12-23 22:00 UTC -> 2024-12-24 03:40 UTC: 5.7 h stationary (anchored or drifting), mean AIS speed 0.7 kn, path 0.2 nm, net 0.0 nm, at 59.446,24.766
- 2024-12-24 12:06 UTC -> 2024-12-26 06:42 UTC: 42.6 h stationary (anchored or drifting), mean AIS speed 0.2 kn, path 0.2 nm, net 0.2 nm, at 60.147,24.908
- 2024-12-26 22:00 UTC -> 2024-12-27 03:38 UTC: 5.6 h stationary (anchored or drifting), mean AIS speed 0.7 kn, path 0.2 nm, net 0.1 nm, at 59.446,24.767
- 2024-12-27 22:00 UTC -> 2024-12-28 03:37 UTC: 5.6 h stationary (anchored or drifting), mean AIS speed 0.7 kn, path 0.2 nm, net 0.1 nm, at 59.446,24.767
- 2024-12-28 18:55 UTC -> 2024-12-28 23:30 UTC: 4.6 h stationary (anchored or drifting), mean AIS speed 0.0 kn, path 0.0 nm, net 0.0 nm, at 60.149,24.912

> Only 'slow moving' scores. Stationary periods are normal in ports and anchorages; without a cable layer the tool cannot tell a port from an anchorage over a cable.

## Notes

- 302 track points inside the analysis window (753 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
