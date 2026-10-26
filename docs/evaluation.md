# Evaluation: UK-sanctioned vessels vs. sampled controls

The five reference incidents are too few to test the rules, and the rules were written with them in
mind. I use a separate sample to ask a narrower question:

Do the timestamp-filtered identity records distinguish the sampled UK-sanctioned ships from the
sampled controls? Current identity links, registry matches and fixed flag weights are retained.

```
ssc eval
```

## Design

| | Sanctioned | Control |
|---|---|---|
| Who | 300 vessels drawn at random (seed 20261026) from the 645 designated under the UK Russia sanctions regime; sample designation dates between 31 Jul 2024 and 8 Oct 2026 | 300 random valid IMO numbers with the same mix of IMO prefixes (first three digits, a rough proxy for build year), not on the UK list, known to GFW |
| Reference date | Designation date | A designation date drawn from the sanctioned sample |
| Data | GFW identity search by IMO, by every MMSI and by the latest name | same |

* Only identity history recorded before the reference date counts (`clip_identities`, the same
  mechanism as the pre-incident view of the cases).
* Only the identity checks run: there are no tracks, so the behaviour group is empty.
* The `SANCTIONED` check is switched off; otherwise the test would be circular.
* The thresholds were not changed after the control vessels were scored. One rule
  (`NAME_ON_OTHER_MMSI`) was fixed while building the evaluation, after looking at sanctioned
  vessels only; see [methodology.md](methodology.md#calibration-and-validation).
* Data: `data/eval/uk_sanctions_vs_random.json.gz` (GFW, CC BY-NC 4.0), collected on 26 Oct 2026; 391
  random IMO numbers were tried to find 300 that GFW knows; one search (IMO 9289594) failed and is not in
  the set.

## Results

![Score distribution](img/evaluation.png)

| | Sanctioned (n = 300) | Random ships (n = 300) |
|---|---|---|
| Median score | 50 | 10 |
| Score ≥ 20 (MEDIUM or HIGH) | 83 % | 32 % |
| Score ≥ 50 (HIGH) | 54 % | 8 % |

AUC 0.83 (95 % bootstrap interval 0.80–0.87) measures how often a sanctioned vessel ranks above a
control, counting tied scores as half a win. The bootstrap resamples vessels within each group
1,000 times with seed 20261026. It does not account for operator clusters, selection bias, uncertain
labels or hindsight in the source data.

Share of ships with each signal:

| Signal | Sanctioned | Random ships |
|---|---|---|
| `MULTI_IDENTITY` | 87 % | 39 % |
| `FLAG_CHANGE` | 79 % | 17 % |
| `REGISTRY_LOST` | 73 % | 28 % |
| `MMSI_REUSE` | 23 % | 16 % |
| `CONCURRENT_IDENTITIES` | 8 % | 3 % |
| `IMO_HIDDEN` | 4 % | 8 % |
| `NAME_ON_OTHER_MMSI` | 4 % | 5 % |
| `MMSI_FLAG_MISMATCH` | 2 % | 0 % |
| `NO_REGISTRY` | 1 % | 7 % |

Flag in use at the reference date: the sanctioned ships fly Russia (68), Panama (57), Comoros (27),
Gabon (27), Sierra Leone (21), Barbados (19), Guinea (15), Cameroon (13) …; the controls Panama (36),
Liberia (27), Marshall Islands (16), China (14), Malta, Japan, Singapore (11 each) … On the Paris MoU
list, 50 % of the sanctioned ships were under a grey or black flag, against 10 % of the controls.

## Interpretation and limitations

* Flag and registry rules alone reach an AUC of 0.83, the same
  as the full score. The identity group alone reaches 0.79, mostly through `MULTI_IDENTITY`, which
  is largely the same sale-and-reflag event seen from another angle.
* Missing IMO fields and names under additional MMSIs occur in only a few percent of the sampled
  sanctioned vessels, with no higher observed shares than among controls. Overlapping identity
  dates occur in 8 % vs. 3 %. Track-based handovers and parallel tracks are not tested here because
  the sample has no positions. These results do not establish the general value of the Taiwan patterns.
* This does not test prediction of cable incidents. The labels are UK sanctions designations,
  not confirmed cable damage or deliberate AIS manipulation. Designation criteria can themselves
  include identity and flag practices, so the score and label are not independent descriptions.
* The controls exclude UK-listed vessels, not every sanctioned or unusual ship. The earlier manual
  OFAC cross-check reported nine matches, four among HIGH controls, but its raw results are not
  bundled and that count cannot be reproduced from this repository. I do not use the claimed
  adjusted AUC as a validated result. Government vessels with incomplete AIS records can also score
  HIGH; that alone does not establish a false positive for any single underlying record.
* GFW links identities and registry matches with current knowledge. The most recent name used to
  collect records may be later than the reference date. The fixed Paris MoU list was published in
  July 2026. Timestamp filtering does not remove these sources of hindsight.
* The controls are GFW-known ships reached through sampled valid IMO numbers. They do not represent
  every ship or regional traffic near the cables. Matching IMO prefixes is a rough age proxy, not
  a match on build year, ship type, size, owner, region or observation length.
* The 24 HIGH controls out of 300 give an 8 % sample share. This is not a measured false-positive
  rate for cable incidents. Predictive value would also depend on the prevalence of the target
  behaviour in the population being searched, which this balanced comparison does not estimate.
* `NAME_ON_OTHER_MMSI` was revised during sample preparation, and the records have now also been
  inspected for implementation errors. This dataset must not be presented as an untouched holdout
  for further rule development. A new independent sample is needed to evaluate revised weights.

## Reproduce

`ssc eval --json metrics.json` recomputes the reported metrics from the bundled file. The collection itself ran
in a browser session against the GFW API; the record format matches what `ssc check` gathers, so a
new sample can be scored the same way (`ssc eval --data my_sample.json.gz`). The collection script
and full request log are not bundled, so the acquisition and sampling cannot be rerun from the
repository alone. The current live command searches up to three recent names; this sample searched
the latest name.

An implementation correction retains all matching name-search rows for an additional MMSI, rather
than only the first row. With the same raw sample, AUC changes from 0.834017 to 0.834239 and HIGH
sanctioned vessels from 161 to 162; HIGH controls remain 24. Rounded headline results are unchanged.
`NAME_ON_OTHER_MMSI` changes from 3 % to 4 % among sanctioned vessels. These are corrected calculations,
not an improvement demonstrated on new data.
