# Methodology

Shadow Ship Check turns the patterns seen before known cable incidents into explicit, testable rules.
Each rule produces a signal with a fixed number of points and the evidence behind it. The score is the
sum of all points, capped at 100: **LOW < 20 ≤ MEDIUM < 50 ≤ HIGH**.

The score is a prioritisation aid for a human analyst. It is not a probability, and a high score is
not evidence of sabotage.

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
| `FLAG_CHANGE` | Successive identities with different flags | +15 into a flag of convenience, +5 otherwise, max 30; +5 after the reference date | Open registries are where shadow fleets go | Sales to owners who use open registries for normal business |
| `REGISTRY_LOST` / `NO_REGISTRY` | The identity in use is only self-reported AIS, while earlier ones were registry-confirmed (or none ever was) | +15 (+5 if lost > 5 years ago) / +10 | Without a registry match nobody vouches for the identity | GFW's public registry coverage is incomplete; logged-in users see 11 more sources |
| `MMSI_FLAG_MISMATCH` | MMSI country prefix (MID) does not match the broadcast flag | +10 each, max 20 | Self-assigned or copied MMSIs | Second registers (e.g. German GIS) |
| `MMSI_REUSE` | The hull's MMSI was also used by unrelated ships | +15 if within 2 years, else +5 | Recycled or fraudulent numbers from small registries | Legitimate re-assignment after many years |
| `NAME_ON_OTHER_MMSI` | The hull's name broadcast under MMSIs outside its known identities | +15 | Borrowing other ships' MMSIs | Typos during transponder set-up |
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
| `SLOW_LOITERING` | ≥ 2 h at ≤ 3 kn; "slow moving" if the path rate is ≥ 0.5 nm/h | +10 per slow-moving run, max 20; stationary runs 0 | Anchoring is only scored via `NEAR_CABLE_SLOW` because ports and anchorages look the same |
| `SPEED_DROP` | ≥ 1.5 h underway at 2 kn to 60 % of the ship's own median cruising speed, with real movement (≥ 1 nm/h) | +10 | Catches dragging-anchor behaviour only when the drop is strong |
| `ZIGZAG` | Within 6 h: path ≥ 5 nm, path ≥ 2.5 × net displacement, average ≤ 6 kn | +10 | The speed cap keeps shuttle ferries out |
| `NEAR_CABLE_SLOW` | ≤ 5 kn within 2 nm of a cable route (needs `--cables`) | +20 | No cable geometry ships with the project |

## Calibration and validation

Thresholds were first set from the problem description, then adjusted once against three control
vessels sailing in the same waters and time windows as the incident ships:

* *Finlandia* (Helsinki–Tallinn ferry) – originally flagged for zig-zag and port stays → zig-zag got a
  speed cap, stationary periods stopped scoring.
* *Ever Liven* (Taiwanese container ship) – a second MMSI under the same name counted as a new identity
  → `MULTI_IDENTITY` now counts name/flag combinations, and same-name concurrency scores only 5.
* *Yi Peng 5* (sister ship of Yi Peng 3) – unchanged.

Result after calibration (`ssc case all`):

| Ship | Role | Score | Level |
|---|---|---|---|
| Xingshun 39 | incident | 100 | HIGH |
| Hong Tai 58 | incident | 100 | HIGH |
| Eagle S | incident | 60 | HIGH |
| NewNew Polar Bear | incident | 35 | MEDIUM |
| Yi Peng 3 | incident | 15 | LOW |
| Ever Liven | control | 5 | LOW |
| Yi Peng 5 | control | 5 | LOW |
| Finlandia | control | 0 | LOW |

**Caveat.** Eight ships are a sanity check, not a validation. The controls were used to tune the rules,
so they are not an independent test set. A real evaluation needs a few hundred ordinary ships in the
same regions (expected: mostly LOW) and more incident ships, scored without further tuning.

Yi Peng 3 is the honest miss: no identity camouflage at all. Its behaviour (≈ 1.5 days of reduced speed
while dragging the anchor) is only partly visible in the public track.
