# Shadow Ship Check

[![tests](https://github.com/janbarkemeyer/shadow-ship-check/actions/workflows/tests.yml/badge.svg)](https://github.com/janbarkemeyer/shadow-ship-check/actions/workflows/tests.yml)
[![project page](https://img.shields.io/badge/project%20page-online-2f6fdf)](https://janbarkemeyer.github.io/shadow-ship-check/)

**Checks a ship's AIS history for the camouflage patterns seen before subsea cable incidents in
Taiwan and the Baltic Sea – changing names, flag hopping, borrowed MMSIs, identity swaps at sea and
slow crossings of cable routes.**

Since 2023, subsea cables and a gas pipeline around Taiwan and in the Baltic Sea have repeatedly been
damaged by ships dragging their anchors. Several of the suspected ships had changed name and flag
shortly before and broadcast inconsistent AIS data. Shadow Ship Check turns those patterns into
transparent rules, runs them on free data from [Global Fishing Watch](https://globalfishingwatch.org),
and tests them on five incidents and on 300 sanctioned shadow-fleet vessels.

> The output is a list of indicators with evidence, for a human analyst to follow up. A high score
> is not evidence of sabotage. Most incidents here are officially unresolved and are described as
> *suspected*.

![Xingshun 39: two AIS identities, one ship](docs/img/xingshun39_handover.png)

*Xingshun 39 broadcast as two ships – a Tanzania identity with IMO number and a Cameroon identity
without one – and switched between them at sea. A search by IMO number shows only the first.*

## Results

**Reference incidents.** Each case is scored twice: with only the data GFW had recorded *before the
incident*, and with all data available today. The first score tests the idea – could the ship have
been flagged in advance?

| Ship | Incident | Before | Full data | What stands out before the incident |
|---|---|---|---|---|
| [Xingshun 39](cases/xingshun_39.md) | Keelung cable, Jan 2025 | **100** | 100 | A second AIS identity without IMO, used in parallel; identity swap off Keelung |
| [Hong Tai 58](cases/hong_tai_58.md) | Taiwan–Penghu cable, Feb 2025 | **100** | 100 | Identity data used by two hulls at once; swap at sea; borrowed MMSIs |
| [Eagle S](cases/eagle_s.md) | Estlink 2, Dec 2024 | **50** | 55 | Renamed and moved to a grey-listed flag in 2023; no GFW positions since 11 Dec |
| [NewNew Polar Bear](cases/newnew_polar_bear.md) | Balticconnector, Oct 2023 | **30** | 35 | Bought, renamed and reflagged < 4 months before |
| [Yi Peng 3](cases/yi_peng_3.md) | BCS / C-Lion1, Nov 2024 | **5** | 35 | Nothing beforehand; during the incident it crosses C-Lion1 at reduced speed |
| Finlandia, Yi Peng 5, Ever Liven | controls | 0–5 | 0–5 | Ordinary ships in the same waters and windows |

Per-case reports: [reports/](reports/). Matsu (2023) is documented as the case without any published
ship identifier ([cases/matsu_2023.md](cases/matsu_2023.md)).

**Out-of-sample test.** 300 vessels sanctioned by the UK for carrying Russian oil, scored on their
identity history as it stood on the day they were designated, against 300 random ships of similar
age. Median score 50 vs. 10; 54 % vs. 8 % reach HIGH; AUC 0.83 (95 % CI 0.80–0.87). Reflagging and
lost registry confirmation carry the result – the elaborate tricks seen in the Taiwan cases are rare
among sanctioned tankers. Details and caveats: [docs/evaluation.md](docs/evaluation.md).

![Identity score of sanctioned vessels vs. random ships](docs/img/evaluation.png)

## Quick start

```bash
git clone https://github.com/janbarkemeyer/shadow-ship-check && cd shadow-ship-check
pip install -e ".[dev]"      # standard library only; pytest/ruff for development

ssc case all                 # the reference cases, offline from bundled data
ssc case yi_peng_3           # one case with all evidence
ssc eval                     # the out-of-sample test, offline

# any ship, live from GFW (IMO or MMSI); --as-of gives the view before a given time
ssc check 8358427 --start 2025-01-02 --end 2025-01-04 --also SHUNXING39 --md report.md
ssc check 8358427 --as-of 2025-01-02T12:00 --also SHUNXING39
```

Example (`ssc case xingshun_39 --before-incident`, evidence shortened):

```
Shadow Ship Check - IMO 8358427
Score 100/100 (HIGH) (data until 2025-01-02 12:00 UTC)
  Identity 80 · Flag & registry 25 · Behaviour 15
...
[+15] FLAG_CHANGE: 1 flag change(s)
        2024-03-04: CMR -> TZA (Paris MoU black, ITF flag of convenience)  [BAOLONG36 -> XINGSHUN39]  (recent)
...
[+20] CONCURRENT_IDENTITIES: Two identities of the same hull in use at the same time
        2022-11-24 - 2023-05-12: BAOLONG36/GUY/750342000 and BAOLONG36/CMR/613003836
        2024-09-28 - 2025-01-02: XINGSHUN39/TZA/677087200 and SHUNXING39/CMR/613003889
[+20] IDENTITY_HANDOVER: Identity swap at sea (one AIS identity stops, another starts nearby)
        XINGSHUN39/TZA/677087200 stops 2024-12-28 22:11 UTC at 25.163,121.753 -> SHUNXING39/CMR/613003889
        (no IMO) starts 2024-12-29 02:44 UTC at 25.588,121.803 (273 min, 25.7 nm)
...
```

## How it works

1. **Collect.** `ssc check` searches GFW for the hull's identities, every MMSI it used and its recent
   names (identities without IMO are only found that way), then loads the AIS track of each identity.
2. **Check.** 17 signal types in three groups – *identity* (several names, borrowed or reused MMSIs, two
   identities at once, swaps at sea), *flag & registry* (reflagging weighted by the Paris MoU
   performance list, lost registry confirmation, UK sanctions list) and *behaviour* (AIS gaps,
   loitering, speed drops, slow crossings of cable routes from OpenStreetMap). Each rule produces
   points and the evidence behind them.
3. **Score.** Points add up to a score from 0 to 100 (LOW < 20 ≤ MEDIUM < 50 ≤ HIGH), reported with
   sub-scores per group. `--as-of` cuts off everything recorded after a given time.

Rules, thresholds and their typical false positives: [docs/methodology.md](docs/methodology.md).
Data sources and formats: [docs/data.md](docs/data.md).

## Limitations

* **Public GFW tracks are simplified** (often one point per 60–90 min on open water). Short manoeuvres
  disappear; gaps can be coverage, not a switched-off transponder (see Eagle S).
* **Hindsight in the data.** The pre-incident score cuts off everything recorded later, but GFW
  linked identities to hulls with today's knowledge.
* **The case scores are in-sample.** The rules were written with these incidents in mind and tuned
  against three control vessels. The evaluation tests the identity rules out of sample; the behaviour
  rules have no such test yet.
* **Cable routes are incomplete.** OpenStreetMap has C-Lion1, BCS, Balticconnector and Estlink, but
  not TPKM-3 or the named trans-Pacific cables off Taiwan.
* **Points are simple and partly overlap.** One sale usually triggers `MULTI_IDENTITY`, `FLAG_CHANGE`
  and `REGISTRY_LOST` together. Read the evidence, not just the number.
* Incident times are approximate and taken from public reporting.

## Repository layout

```
src/shadow_ship_check/   cli · gfw (API client, binary track decoder) · signals · watchlist
                         analyze · evaluate · report · cases · registries · geo
cases/                   case files with timelines, sources and open questions
reports/                 generated per-case reports (ssc case all --md reports; checked in CI)
data/                    GFW fixtures and evaluation set · OSM cable routes · UK sanctions list
docs/                    methodology, data, evaluation, figures
scripts/                 refresh_fixtures.py · make_figures.py · build_site.py
tests/                   unit, regression (cases + controls), evaluation, mocked end-to-end
```

## Roadmap

1. Area search: all ships moving slowly across a cable route in a time window (the Matsu case).
2. Automatic name variants (XINGSHUN ↔ SHUNXING) with track evidence before linking.
3. An out-of-sample test for the behaviour rules: tracks of ordinary ships crossing the same cables.
4. A second AIS source to separate coverage gaps from real AIS silence.

## Data and licences

Code: MIT. Vessel data: © Global Fishing Watch,
[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) – non-commercial use with attribution.
Cable routes: © OpenStreetMap contributors, [ODbL](https://www.openstreetmap.org/copyright).
Sanctions list: UK Sanctions List (Open Government Licence v3.0) via OpenSanctions (CC BY-NC 4.0).
Land outlines in the figures: Natural Earth (public domain). Details in [docs/data.md](docs/data.md).
