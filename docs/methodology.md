# Methodology

I use explicit rules to describe AIS identity changes and movements in known cable cases.
Each rule produces a signal with a fixed number of points and the evidence behind it. The score is the
sum of all points, capped at 100: LOW < 20 ≤ MEDIUM < 50 ≤ HIGH.

The score is a prioritisation aid for a human analyst. It is not a probability or evidence of
intent or responsibility for damage. LOW may reflect missing data rather than an ordinary history.

Each signal belongs to one of three groups. Sub-scores show their contributions, but the total still
adds correlated signals together:

| Group | Signals |
|---|---|
| Identity | `MULTI_IDENTITY`, `MMSI_FLAG_MISMATCH`, `MMSI_REUSE`, `NAME_ON_OTHER_MMSI`, `IMO_HIDDEN`, `CONCURRENT_IDENTITIES`, `IDENTITY_HANDOVER`, `PARALLEL_TRACKS` |
| Flag & registry | `FLAG_CHANGE`, `REGISTRY_LOST`, `NO_REGISTRY`, `SANCTIONED` |
| Behaviour | `AIS_GAP`, `SLOW_LOITERING`, `SPEED_DROP`, `ZIGZAG`, `CABLE_CROSSING_SLOW` |

## Reference date and look-back

Every check runs against a reference date: the end of the analysis window (usually the incident).
Identity history is weighed by how close it is to that date:

* identity changes in the 3 years (flags) or 5 years (identities, registry) before the reference
  date score full points;
* older name/flag changes are listed without recent-change points. Old registry matches and MMSI
  reuse can still contribute 5 points under their respective rules;
* flag changes after the reference date score +5 each, capped at 10 additional points, in the full
  report. This is a descriptive choice, not evidence that a change was a reaction to the incident.

The Paris MoU 2025 performance list was published on 1 July 2026. The same fixed list is used for all
reference dates, including earlier incidents. Its inspection and detention statistics measure flag
performance in port-state control, not a ship's intent. Source:
[Paris MoU performance lists](https://parismou.org/year-report/year-report-2025/performance-lists/).

## Identity checks

| Code | Rule | Points | Why it matters | Typical false positive |
|---|---|---|---|---|
| `MULTI_IDENTITY` | Distinct name/flag combinations under one IMO in the look-back period | +10 per extra identity, max 30 | Name changes break the link to a ship's history | Ordinary sales; a new MMSI under the same name does not count |
| `FLAG_CHANGE` | Successive identities with different flags | By the new flag's Paris MoU 2025 rating: black +15, grey +10, white +5; not listed +10 if an ITF flag of convenience, else +5; max 30 recent plus max 10 after the reference date | Flag performance provides context; it does not establish concealment | Ordinary sales and legitimate reflagging, including moves to open registries |
| `REGISTRY_LOST` / `NO_REGISTRY` | The selected identity has no matching registry MMSI in GFW, while an earlier one did (or none ever did) | +15 (+5 if last match ended > 5 years ago) / +10 | A change in the available registry match | GFW registry coverage varies by flag; this does not establish that a registration is missing or invalid |
| `MMSI_FLAG_MISMATCH` | MMSI country prefix (MID) does not match the broadcast flag | +10 each, max 20 | Self-assigned or copied MMSIs | Second registers (e.g. German GIS) |
| `MMSI_REUSE` | The hull's MMSI was also reported under another name without its IMO | +15 if within 2 years, else +5 | Possible reassignment or identity conflict | Legitimate reassignment, missing dates and incorrect links |
| `NAME_ON_OTHER_MMSI` | The known name appears under an additional MMSI, without a foreign IMO, matching the flag and overlapping the same usage period | +15 | Possible additional identity | Typos during transponder set-up; small craft with the same name and flag |
| `SANCTIONED` | Hull IMO on the bundled UK sanctions list, designated on or before the reference date | +20 (later designations listed with 0) | A recorded designation, not a finding about a cable incident | The snapshot can be outdated; date-only designations are treated as 00:00 UTC |
| `IMO_HIDDEN` | A known name + MMSI also broadcast without IMO | +10 | Cuts the AIS identity off from the hull history | Transponders that simply omit the IMO field |
| `CONCURRENT_IDENTITIES` | Linked AIS identity envelopes overlap for ≥ 30 days within the 5-year period ending at the reference date | +20 (different name/flag), +5 (same name and flag), max 20 | Possible multiple identities; continuous simultaneous use is not established | Second transponder; first/last-message dates overstate overlap |

## Track checks

Track checks run separately for each AIS identity of the hull (so two clones are never stitched into
one path). Movement checks use positions inside the analysis window, with loaded context used for
cruising-speed baselines. Gap checks inspect up to 7 days around the window if those positions are
loaded; the live command fetches 3 days of context by default (`--context-days`). Handover and parallel
checks use the supplied identity tracks, which can include longer historical periods in case fixtures.

| Code | Rule | Points | Notes |
|---|---|---|---|
| `IDENTITY_HANDOVER` | One identity stops and another starts within 6 h at a reachable position (≤ 10 nm + 15 kn × elapsed time) | +20 | Ignores starts/stops at the edge of the requested period |
| `PARALLEL_TRACKS` | Linked identities report positions ≥ 100 nm apart within one hour | +20 | Possible shared identity data, incorrect GFW links or erroneous positions |
| `AIS_GAP` | ≥ 6 h without position, unless a short stationary gap lies outside the window; also reports when all loaded positions lie outside the window | +5 (6–24 h), +10 (≥ 24 h), +10 if overlapping the window, +15 when all loaded points are outside it; max 30 | An entirely empty track yields no gap signal. Any position from another supplied identity inside a gap suppresses its points; this does not require a confirmed handover |
| `SLOW_LOITERING` | ≥ 2 h at ≤ 3 kn; "slow moving" if the path rate is ≥ 0.5 nm/h | +10 per slow-moving run, max 20; stationary runs 0 | Anchoring is not scored because ports and anchorages look the same; a slow crossing of a mapped cable is scored by `CABLE_CROSSING_SLOW` |
| `SPEED_DROP` | ≥ 1.5 h underway above 2 kn and below 60 % of the median of loaded AIS speeds ≥ 5 kn, with real movement (≥ 1 nm/h); needs ≥ 5 baseline points | +10 | A relative speed change; it does not identify the cause |
| `ZIGZAG` | ≥ 4 positions within 6 h: path ≥ 5 nm, path ≥ 2.5 × net displacement, average ≤ 6 kn | +10 | Filters out fast ferry crossings; ordinary waiting and manoeuvring can still qualify |
| `CABLE_CROSSING_SLOW` | The straight line between two positions (≤ 3 h apart) crosses a mapped cable or pipeline while the speed over ground is ≤ 70 % of the ship's median cruising speed (5 kn if unknown); lying still (< 1 kn) does not count | +20 | Uses the bundled OpenStreetMap layer; ships cross cables constantly, only slow crossings are listed |

## Calibration and validation

Thresholds were first set from the problem description, then adjusted once against three control
vessels sailing in the same waters and time windows as the incident ships:

* *Finlandia* (Helsinki–Tallinn ferry); originally flagged for zig-zag and port stays → zig-zag got a
  speed cap, stationary periods stopped scoring.
* *Ever Liven* (Taiwanese container ship); a second MMSI under the same name counted as a new identity
  → `MULTI_IDENTITY` now counts name/flag combinations, and same-name concurrency scores only 5.
* *Yi Peng 5* (sister ship of Yi Peng 3); unchanged.

A fourth adjustment came from a review of the whole project: flag changes were first scored by the ITF
"flag of convenience" list alone. That list includes Liberia, Panama and the Marshall Islands, which
carry a large share of the world fleet, so an ordinary sale scored as high as a move to Togo. Flags are
now weighted by the Paris MoU performance list (detentions in European ports); a unit test checks that
an ordinary Greek-to-Liberia sale stays LOW.

Two more changes came with version 0.2:

* *Cable check.* The first rule ("≤ 5 kn within 2 nm of a cable") flagged the Finlandia ferry at its
  Helsinki berth as soon as real cable routes were loaded. It was replaced by `CABLE_CROSSING_SLOW`,
  which needs the ship to move across the route at reduced speed. This rule was designed after seeing
  the control vessel and the incident tracks, so its case results are in-sample.
* *Namesakes.* While preparing the evaluation, `NAME_ON_OTHER_MMSI` turned out to fire for any ship
  with a common name ("VLADIMIR", "RAGNAR"): other ships of that name, with their own IMO numbers,
  counted as "borrowed" MMSIs. The rule now requires an identity without a foreign IMO, with the same
  flag, active while the hull used the name. This was fixed after looking at sanctioned vessels only,
  before any control vessel was scored.

## Before the incident vs. full data

The tool filters the current snapshot by timestamps (`--as-of`, or `ssc case … --before-incident`
with the cut-off stored per case). Identities that started later are dropped, last-seen dates are
clipped, and tracks end at the cut-off. `ssc check --as-of` without a start/end window loads the
preceding 30 days. If both `--end` and `--as-of` are supplied, their earlier value is the effective
cut-off for tracks and identities. An earlier end is never extended by `--as-of`.

This does not reconstruct the information available at that time. Identity links and registry
matches come from the current GFW snapshot; the flag list was published in 2026; names and manually
linked MMSIs may have been found after the incident. An identity with no start date cannot be dated
reliably and is retained. A later sanctions designation can still appear with zero points for context.
The result is a retrospective timestamp filter, not proof of an advance warning.

Result (`ssc case all`):

| Ship | Role | Before incident | Full data |
|---|---|---|---|
| Xingshun 39 | incident | 100 HIGH | 100 HIGH |
| Hong Tai 58 | incident | 100 HIGH | 100 HIGH |
| Eagle S | incident | 50 HIGH | 55 HIGH |
| NewNew Polar Bear | incident | 30 MEDIUM | 35 MEDIUM |
| Yi Peng 3 | incident | 5 LOW | 35 MEDIUM |
| Ever Liven | control | 5 LOW | 5 LOW |
| Yi Peng 5 | control | 5 LOW | 5 LOW |
| Finlandia | control | 0 LOW | 0 LOW |

Eagle S keeps an `AIS_GAP` before the incident because GFW has no positions after 11 Dec 2024. That is
most likely a coverage gap, not a switched-off transponder (see the case file); without it the ship
would score 35 (MEDIUM).

Eight ships are a sanity check, not a validation. The rules were written with these incidents
in mind and the controls were used to tune them, so neither is an independent test set. The
separate comparison of the identity rules is in [evaluation.md](evaluation.md).

Yi Peng 3 has no scored recent identity changes. With the cable layer, its track crosses C-Lion1 at
reduced speed around the reported failure time (full data: 35 MEDIUM). The earlier score is 5 LOW.
This limits the use of identity history for identifying candidates around cable damage.

## Dependencies and unresolved validation

One sale can produce `MULTI_IDENTITY`, `FLAG_CHANGE` and `REGISTRY_LOST` together. A slow passage can
also trigger several movement checks. The score sums these contributions; it is not an independent
evidence count. The 100-point cap can hide differences between high-scoring cases, so group totals
and individual signals should be read alongside it.

First/last identity dates describe an envelope, not continuous transmissions. Merging repeated uses
of the same name/flag/MMSI can bridge an unobserved interval. Handover candidates can be up to 100 nm
apart at the six-hour limit; proximity alone does not establish that they are the same hull.
The MMSI-country mapping covers a subset of prefixes; an unlisted prefix produces no mismatch
signal. Missing dates and incomplete source coverage also limit interpretation of identity signals.

Low-speed runs and speed-drop runs can bridge missing positions. Track segments and long gaps are
not yet used to split every movement calculation. Straight-line cable intersections between sparse
points are reconstructed candidates, not observed contact with a cable or an anchor. No independent
normal-traffic sample has measured these rules' false-positive rates.

I have not recalibrated the weights on the existing 600 records. A revision would need a separate
development set and an untouched test set, with comparable ship types, regions and observation
periods. It would also need to account for data coverage and for related ships sharing an operator.
