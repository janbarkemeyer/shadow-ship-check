# Control: Ever Liven (Taiwan-flagged container ship)

**Score: 5/100 (LOW)**  
Analysis window: 2025-02-22 00:00 - 2025-02-26 00:00 UTC  
_Indicators only - not evidence of sabotage or any other wrongdoing. Data: Global Fishing Watch (CC BY-NC 4.0)._

## Identities

| Name | Flag | MMSI | IMO | From | To | Source |
|---|---|---|---|---|---|---|
| EVER LIVEN | TWN | 416481000 | 9595527 | 2013-04-06 | 2026-10-23 | registry + AIS |
| JIRENYU  00085 | CHN | 412286696 | 9595527 | 2015-04-11 | 2015-10-15 | self-reported AIS only |
| EVER LIVEN | TWN | 416481100 | 9595527 | 2022-06-15 | 2022-08-10 | self-reported AIS only |

## Red flags

### 3 identities linked to the same hull (2 in the 5 years before 2025-02-26)  `MULTI_IDENTITY` (+0)
- * EVER LIVEN / TWN / MMSI 416481000 (2013-04-06 - 2026-10-23, registry + AIS)
-   JIRENYU  00085 / CHN / MMSI 412286696 (2015-04-11 - 2015-10-15, self-reported AIS only)
- * EVER LIVEN / TWN / MMSI 416481100 (2022-06-15 - 2022-08-10, self-reported AIS only)

> * = in use during the look-back period (scored); others are history.

### Two identities of the same hull in use at the same time  `CONCURRENT_IDENTITIES` (+5)
- 2015-04-11 - 2015-10-15: EVER LIVEN/TWN/416481000 and JIRENYU  00085/CHN/412286696  (outside look-back, not scored)
- 2022-06-15 - 2022-08-10: EVER LIVEN/TWN/416481000 and EVER LIVEN/TWN/416481100  (same name and flag - likely a second transponder)

> Overlap is computed from first/last AIS message per identity; check the tracks (handover / parallel signals).

## Notes

- 63 track points inside the analysis window (390 loaded, 1 identity track(s)).
- No cable layer given (--cables): proximity to cable routes was not checked.
