# Eagle S - Estlink 2 and telecom cables, Gulf of Finland

Case file with context and sources: [eagle_s.md](../cases/eagle_s.md)

| | Score | Identity | Flag & registry | Behaviour |
|---|---|---|---|---|
| Before the incident | **50 HIGH** | 10 | 25 | 15 |
| Full data | **55 HIGH** | 10 | 25 | 20 |

Pre-incident data cut-off: 2024-12-25 10:26 UTC.  
Analysis window: 2024-12-23 00:00 - 2024-12-28 23:59 UTC.  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Before the incident

What the checks flag using only data recorded before the cut-off:

- **Registry confirmation lost - identity in use is self-reported only** (+15): last confirmed: NORSTAR INTREPID / MHL / MMSI 538003031 (2012-01-26 - 2023-07-22, registry + AIS)
- **AIS gaps** (+15): no track points at all inside the analysis window
- **2 identities linked to the same hull (2 in the 5 years before 2024-12-25)** (+10): * NORSTAR INTREPID / MHL / MMSI 538003031 (2012-01-26 - 2023-07-22, registry + AIS)
- **1 flag change(s)** (+10): 2023-07-22: MHL -> COK (Paris MoU grey, ITF flag of convenience)  [NORSTAR INTREPID -> EAGLE-S]  (recent)

## Full data

### Identities

| Name | Flag | MMSI | IMO | First seen | Last seen | Source |
|---|---|---|---|---|---|---|
| NORSTAR INTREPID | MHL | 538003031 | 9329760 | 2012-01-26 | 2023-07-22 | registry + AIS |
| EAGLE-S | COK | 518998865 | 9329760 | 2023-07-22 | 2026-03-28 | self-reported AIS only |

### Signals

#### Identity (+10)

**2 identities linked to the same hull (2 in the 5 years before 2024-12-28)** `MULTI_IDENTITY` +10

- * NORSTAR INTREPID / MHL / MMSI 538003031 (2012-01-26 - 2023-07-22, registry + AIS)
- * EAGLE-S / COK / MMSI 518998865 (2023-07-22 - 2026-03-28, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

#### Flag & registry (+25)

**1 flag change(s)** `FLAG_CHANGE` +10

- 2023-07-22: MHL -> COK (Paris MoU grey, ITF flag of convenience)  [NORSTAR INTREPID -> EAGLE-S]  (recent)

> Scored: changes in the 3 years before 2024-12-28 by the new flag's Paris MoU rating (black +15, grey +10, white +5; unlisted +10 if an ITF flag of convenience, else +5) and changes after it (+5). Sales also cause flag changes; most of the world fleet sails under white-listed open registries.

**Registry confirmation lost - identity in use is self-reported only** `REGISTRY_LOST` +15

- last confirmed: NORSTAR INTREPID / MHL / MMSI 538003031 (2012-01-26 - 2023-07-22, registry + AIS)
- in use at 2024-12-28: EAGLE-S / COK / MMSI 518998865 (2023-07-22 - 2026-03-28, self-reported AIS only)

**Hull added to the UK sanctions list after the reference date** `SANCTIONED` +0

- IMO 9329760 (EAGLE S): UK designation 2025-07-21, Russia regime

> Listed for context only: the designation was not known at the reference date.

#### Behaviour (+20)

**AIS gaps** `AIS_GAP` +20

- 2024-12-11 02:26 UTC -> 2025-03-07 00:00 UTC: 2061.6 h without position, 899 nm straight-line jump (implied 0.4 kn), 59.921,28.665 -> 53.635,3.633  <-- overlaps the analysis window

> Public GFW tracks are simplified (often one point every 60-90 min on open water). Short gaps and brief manoeuvres can be invisible or exaggerated.

### Track around the reported incident time

Reported time (approximate): 2024-12-25 10:26 UTC. Points within +/- 3 h:

No AIS positions in GFW for this period.

### Notes

- 0 track points inside the analysis window (1814 loaded, 1 identity track(s)).
