# Methodology

Shadow Ship Check turns the patterns seen before known cable incidents into explicit, testable rules.
Each rule produces a signal with a fixed number of points and the evidence behind it. The score is the
sum of all points, capped at 100: **LOW < 20 ≤ MEDIUM < 50 ≤ HIGH**.

The score is a prioritisation aid for a human analyst. It is not a probability, and a high score is
not evidence of sabotage.

Each signal belongs to one of three groups, reported as sub-scores so that one kind of evidence
cannot hide behind another:

| Group | Signals |
|---|---|
| Identity | `MULTI_IDENTITY`, `MMSI_FLAG_MISMATCH`, `MMSI_REUSE`, `NAME_ON_OTHER_MMSI`, `IMO_HIDDEN`, `CONCURRENT_IDENTITIES`, `IDENTITY_HANDOVER`, `PARALLEL_TRACKS` |
| Flag & registry | `FLAG_CHANGE`, `REGISTRY_LOST`, `NO_REGISTRY`, `SANCTIONED` |
| Behaviour | `AIS_GAP`, `SLOW_LOITERING`, `SPEED_DROP`, `ZIGZAG`, `CABLE_CROSSING_SLOW` |

## Reference date and look-back

Every check runs against a reference date: the end of the analysis window (usually the incident).
Identity history is weighed by how close it is to that date:

* identity changes in the **3 years** (flags) or **5 years** (identities, registry) before the reference
  date score full points;
* older history is listed for context but scores nothing;
* renaming or reflagging **after** the reference date scores a little (+5), because it is a common
  reaction after an incident.

## Identity checks

| Code | Rule | Points | Why it matters | Typical false positive |
|---|---|---|---|---|
| `MULTI_IDENTITY` | Distinct name/flag combinations under one IMO in the look-back period | +10 per extra identity, max 30 | Name changes break the link to a ship's history | Ordinary sales; a new MMSI under the same name does not count |
| `FLAG_CHANGE` | Successive identities with different flags | By the new flag's Paris MoU 2025 rating: black +15, grey +10, white +5; not listed +10 if an ITF flag of convenience, else +5; max 30. +5 per change after the reference date | Poorly performing registries are where shadow fleets go | Ordinary sales – most of the world fleet sails under white-listed open registries (Liberia, Panama, Marshall Islands), which is why they score only 5 |
| `REGISTRY_LOST` / `NO_REGISTRY` | The identity in use is only self-reported AIS, while earlier ones were registry-confirmed (or none ever was) | +15 (+5 if lost > 5 years ago) / +10 | Without a registry match nobody vouches for the identity | GFW's public registry coverage is incomplete; logged-in users see 11 more sources |
| `MMSI_FLAG_MISMATCH` | MMSI country prefix (MID) does not match the broadcast flag | +10 each, max 20 | Self-assigned or copied MMSIs | Second registers (e.g. German GIS) |
| `MMSI_REUSE` | The hull's MMSI was also used by unrelated ships | +15 if within 2 years, else +5 | Recycled or fraudulent numbers from small registries | Legitimate re-assignment after many years |
| `NAME_ON_OTHER_MMSI` | The hull's name broadcast under an MMSI outside its known identities - with no IMO (or the hull's), the same flag, while the hull itself used that name | +15 | Borrowing other ships' MMSIs | Typos during transponder set-up; small craft with the same name and flag |
| `SANCTIONED` | Hull IMO on the bundled UK sanctions list, designated before the reference date | +20 (later designations listed with 0) | An official finding, not an indicator - included so a check is not blind to it | - |
| `IMO_HIDDEN` | A known name + MMSI also broadcast without IMO | +10 | Cuts the AIS identity off from the hull history | Transponders that simply omit the IMO field |
| `CONCURRENT_IDENTITIES` | Two identities of the same hull active for ≥ 30 days at the same time | +20 (different name/flag), +5 (same name and flag) | Two transponders, two identities – switch as needed | Second transponder; first/last-message dates overstate overlap |

## Track checks

Track checks run separately for each AIS identity of the hull (so two clones are never stitched into
one path) and are restricted to the analysis window. The window is padded by 7 days for gap checks.

| Code | Rule | Points | Notes |
|---|---|---|---|
| `IDENTITY_HANDOVER` | One identity stops and another starts within 6 h at a reachable position (≤ 10 nm + 15 kn × elapsed time) | +20 | Ignores starts/stops at the edge of the requested period |
| `PARALLEL_TRACKS` | Two identities of the same hull report positions ≥ 100 nm apart within one hour | +20 | Two hulls share identity data – or GFW linked identities wrongly |
| `AIS_GAP` | ≥ 6 h without position and a jump ≥ 5 nm, or ≥ 48 h, or no data in the window | +5 (6–24 h), +10 (≥ 24 h), +10 if it overlaps the window, +15 for an empty window; max 30 | Gaps while another identity of the hull is broadcasting are listed but scored under `IDENTITY_HANDOVER` |
| `SLOW_LOITERING` | ≥ 2 h at ≤ 3 kn; "slow moving" if the path rate is ≥ 0.5 nm/h | +10 per slow-moving run, max 20; stationary runs 0 | Anchoring is not scored because ports and anchorages look the same; a slow crossing of a mapped cable is scored by `CABLE_CROSSING_SLOW` |
| `SPEED_DROP` | ≥ 1.5 h underway at 2 kn to 60 % of the ship's own median cruising speed, with real movement (≥ 1 nm/h) | +10 | Catches dragging-anchor behaviour only when the drop is strong |
| `ZIGZAG` | Within 6 h: path ≥ 5 nm, path ≥ 2.5 × net displacement, average ≤ 6 kn | +10 | The speed cap keeps shuttle ferries out |
| `CABLE_CROSSING_SLOW` | The straight line between two positions (≤ 3 h apart) crosses a mapped cable or pipeline while the speed over ground is ≤ 70 % of the ship's median cruising speed (5 kn if unknown); lying still (< 1 kn) does not count | +20 | Uses the bundled OpenStreetMap layer; ships cross cables constantly, only slow crossings are listed |

## Calibration and validation

Thresholds were first set from the problem description, then adjusted once against three control
vessels sailing in the same waters and time windows as the incident ships:

* *Finlandia* (Helsinki–Tallinn ferry) – originally flagged for zig-zag and port stays → zig-zag got a
  speed cap, stationary periods stopped scoring.
* *Ever Liven* (Taiwanese container ship) – a second MMSI under the same name counted as a new identity
  → `MULTI_IDENTITY` now counts name/flag combinations, and same-name concurrency scores only 5.
* *Yi Peng 5* (sister ship of Yi Peng 3) – unchanged.

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

The tool can cut off all data recorded after a given time (`--as-of`, or `ssc case … --before-incident`
with the cut-off stored per case). Identities that started later are dropped, last-seen dates are
clipped, tracks end at the cut-off. This is the relevant test of the idea – a check is only useful if it
flags the ship before the damage. One kind of hindsight remains: GFW linked AIS identities to hulls
with today's knowledge.

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

**Caveat.** Eight ships are a sanity check, not a validation. The rules were written with these incidents
in mind and the controls were used to tune them, so neither is an independent test set. The
out-of-sample test of the identity rules is in [evaluation.md](evaluation.md).

Yi Peng 3 is the honest miss: no identity camouflage at all. With the cable layer, its track crosses
C-Lion1 at reduced speed around the reported failure time (full data: 35 MEDIUM) – useful after the
fact, but nothing points at the ship beforehand.
