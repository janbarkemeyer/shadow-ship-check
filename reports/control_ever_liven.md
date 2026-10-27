# Control: Ever Liven (Taiwan-flagged container ship)

| | Score | Identity | Flag & registry | Behaviour |
|---|---|---|---|---|
| Window-end cut-off | 5 LOW | 5 | 0 | 0 |
| Full data | 5 LOW | 5 | 0 | 0 |

Timestamp cut-off: 2025-02-26 00:00 UTC.<br>
Analysis window: 2025-02-22 00:00 - 2025-02-26 00:00 UTC.  
_Heuristic research indicators only. The score is not a probability or evidence of intent or responsibility for damage. LOW may reflect limited data. Overlapping rules can add points for the same event. The combined score is capped at 100; group totals are uncapped. Bundled sources: Global Fishing Watch (CC BY-NC 4.0); cable routes © OpenStreetMap contributors (ODbL); UK Sanctions List (OGL v3) via OpenSanctions (CC BY-NC 4.0)._

## Window-end cut-off

Retrospective timestamp filter of the bundled snapshot. Current identity links, registry matches, manual associations and fixed 2025 flag weights remain; this does not reconstruct an advance warning.

This control has no incident time. Its cut-off is the end of its analysis window.

- Overlapping first/last dates for linked AIS identities (+5): 2022-06-15 - 2022-08-10: EVER LIVEN/TWN/416481000 and EVER LIVEN/TWN/416481100  (same name and flag - likely a second transponder)

### Notes

- 63 track points inside the analysis window (177 loaded, 1 identity track(s)).
- Timestamp filtering retains current identity links, registry matches and fixed 2025 flag weights; it does not reconstruct what was known at the cut-off.
- This control is in the western Pacific, outside the Taiwan incident region; its cut-off is the window end.

## Full data

### Identities

| Name | Flag | MMSI | IMO | First seen | Last seen | Source |
|---|---|---|---|---|---|---|
| EVER LIVEN | TWN | 416481000 | 9595527 | 2013-04-06 | 2026-10-23 | registry + AIS |
| JIRENYU  00085 | CHN | 412286696 | 9595527 | 2015-04-11 | 2015-10-15 | self-reported AIS only |
| EVER LIVEN | TWN | 416481100 | 9595527 | 2022-06-15 | 2022-08-10 | self-reported AIS only |

### Signals

#### Identity (+5)

##### 1 distinct name/flag combinations in the 5 years before 2025-02-26 (3 linked records in total) (`MULTI_IDENTITY`, +0)

- \* EVER LIVEN / TWN / MMSI 416481000 (2013-04-06 - 2026-10-23, registry + AIS)
-   JIRENYU  00085 / CHN / MMSI 412286696 (2015-04-11 - 2015-10-15, self-reported AIS only)
- \* EVER LIVEN / TWN / MMSI 416481100 (2022-06-15 - 2022-08-10, self-reported AIS only)

\* = dated use during the look-back period (scored); other records are outside it or undated.

##### Overlapping first/last dates for linked AIS identities (`CONCURRENT_IDENTITIES`, +5)

- 2015-04-11 - 2015-10-15: EVER LIVEN/TWN/416481000 and JIRENYU  00085/CHN/412286696  (less than 30 days inside the scoring period, not scored)
- 2022-06-15 - 2022-08-10: EVER LIVEN/TWN/416481000 and EVER LIVEN/TWN/416481100  (same name and flag - likely a second transponder)

Overlap is computed from first/last AIS message per identity; check the tracks (handover / parallel signals).

### Notes

- 63 track points inside the analysis window (390 loaded, 1 identity track(s)).
- This control is in the western Pacific, outside the Taiwan incident region; its cut-off is the window end.
