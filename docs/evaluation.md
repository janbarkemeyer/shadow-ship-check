# Evaluation: sanctioned shadow-fleet vessels vs. random ships

The five reference incidents are too few to test the rules, and the rules were written with them in
mind. This evaluation asks a narrower question on data the rules have not seen:

> Does the identity history of a ship, *as it stood before anyone officially called it a shadow-fleet
> vessel*, separate such ships from ordinary ones?

```
ssc eval
```

## Design

| | Sanctioned | Control |
|---|---|---|
| Who | 300 vessels drawn at random (seed 20261026) from the 645 designated under the UK Russia sanctions regime – all designated between 31 Jul 2024 and 8 Oct 2026 | 300 random valid IMO numbers with the same mix of IMO prefixes (first three digits, a rough proxy for build year), not on the UK list, known to GFW |
| Reference date | Designation date | A designation date drawn from the sanctioned sample |
| Data | GFW identity search by IMO, by every MMSI and by the latest name – what `ssc check` collects | same |

* Only identity history recorded **before the reference date** counts (`clip_identities`, the same
  mechanism as the pre-incident view of the cases).
* Only the identity checks run: there are no tracks, so the behaviour group is empty.
* The `SANCTIONED` check is switched off – otherwise the test would be circular.
* The thresholds were not changed after the control vessels were scored. One rule
  (`NAME_ON_OTHER_MMSI`) was fixed while building the evaluation, after looking at sanctioned
  vessels only – see [methodology.md](methodology.md#calibration-and-validation).
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

**AUC 0.83** (95 % bootstrap interval 0.80–0.87): a randomly chosen sanctioned vessel scores higher
than a randomly chosen control in 83 % of pairs.

Share of ships with each signal:

| Signal | Sanctioned | Random ships |
|---|---|---|
| `MULTI_IDENTITY` | 87 % | 39 % |
| `FLAG_CHANGE` | 79 % | 17 % |
| `REGISTRY_LOST` | 73 % | 28 % |
| `MMSI_REUSE` | 23 % | 16 % |
| `CONCURRENT_IDENTITIES` | 8 % | 3 % |
| `IMO_HIDDEN` | 4 % | 8 % |
| `NAME_ON_OTHER_MMSI` | 3 % | 5 % |
| `MMSI_FLAG_MISMATCH` | 2 % | 0 % |
| `NO_REGISTRY` | 1 % | 7 % |

Flag in use at the reference date: the sanctioned ships fly Russia (68), Panama (57), Comoros (27),
Gabon (27), Sierra Leone (21), Barbados (19), Guinea (15), Cameroon (13) …; the controls Panama (36),
Liberia (27), Marshall Islands (16), China (14), Malta, Japan, Singapore (11 each) … On the Paris MoU
list, 50 % of the sanctioned ships were under a grey or black flag, against 10 % of the controls.

## What this shows – and what it does not

* **The flag and registry rules carry the result.** On their own they reach an AUC of 0.83, the same
  as the full score. The identity group alone reaches 0.79, mostly through `MULTI_IDENTITY`, which
  is largely the same sale-and-reflag event seen from another angle.
* **The elaborate tricks are rare in the shadow fleet.** Borrowed MMSIs, hidden IMO numbers and
  parallel identities – the patterns that make Xingshun 39 and Hong Tai 58 stand out – occur in a few
  percent of sanctioned tankers, no more often than among random ships. They are worth keeping for the
  cable cases, but this test gives no evidence that they help in general.
* **This is not a test of sabotage prediction.** Sanctioned tankers are a proxy population; none of
  them is known to have damaged a cable. And the UK designates ships partly *because* of frequent
  reflagging and false flags, so part of the separation is built into the label.
* **The controls are not all clean.** 9 controls are on the US OFAC list (OpenSanctions `us_ofac_sdn`,
  26 Oct 2026), 4 of them among the 24 controls that score HIGH. Without those 9 the AUC is 0.84.
  Other high-scoring controls include government vessels with messy AIS set-ups (a Royal Navy patrol
  ship, an Indian coast guard ship) – realistic false positives.
* **Hindsight remains.** GFW links AIS identities to IMO numbers with today's knowledge; a live
  system at the designation date would have seen fewer links.
* Random IMO numbers sample *the world fleet*, not ships in the Baltic or the Taiwan Strait. A
  regional control group would be a harder test.

## Reproduce

`ssc eval --json metrics.json` recomputes everything from the bundled file. The collection itself ran
in a browser session against the GFW API; the record format matches what `ssc check` gathers, so a
new sample can be scored the same way (`ssc eval --data my_sample.json.gz`).
