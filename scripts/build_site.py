"""Build the project page (GitHub Pages) from the same data as the README.

    python scripts/build_site.py            # writes site/index.html and site/img/

Every number on the page is computed here from the bundled fixtures and the evaluation set,
so the page cannot drift from the code.
"""

from __future__ import annotations

import html
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from shadow_ship_check import evaluate, watchlist  # noqa: E402
from shadow_ship_check.analyze import analyze_fixture, load_fixture  # noqa: E402
from shadow_ship_check.cases import ALL, CASES  # noqa: E402
from shadow_ship_check.geo import CableLayer  # noqa: E402

REPO = "https://github.com/janbarkemeyer/shadow-ship-check"
OUT = ROOT / "site"
NAMES = {
    "eagle_s": ("Eagle S", "Estlink 2, Dec 2024"),
    "xingshun_39": ("Xingshun 39", "Keelung cable, Jan 2025"),
    "hong_tai_58": ("Hong Tai 58", "Taiwan–Penghu cable, Feb 2025"),
    "yi_peng_3": ("Yi Peng 3", "BCS / C-Lion1, Nov 2024"),
    "newnew_polar_bear": ("NewNew Polar Bear", "Balticconnector, Oct 2023"),
    "control_finlandia": ("Finlandia", "control: Helsinki–Tallinn ferry"),
    "control_yi_peng_5": ("Yi Peng 5", "control: sister ship of Yi Peng 3"),
    "control_ever_liven": ("Ever Liven", "control: container ship"),
}

CSS = """
:root{--bg:#fbfbfa;--fg:#1f2933;--muted:#616e7c;--line:#e4e7eb;--accent:#2f6fdf;--warn:#c2410c;--card:#fff}
@media (prefers-color-scheme:dark){:root{--bg:#121417;--fg:#e4e7eb;--muted:#9aa5b1;--line:#2d3339;--accent:#7aa7f5;--warn:#f0905e;--card:#1a1d21}
 img.fig{background:#fff;border-radius:6px}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif}
main{max-width:860px;margin:0 auto;padding:48px 16px 80px}
h1{font-size:2rem;line-height:1.2;margin:0 0 .4rem;letter-spacing:-.01em}
h2{font-size:1.25rem;margin:3rem 0 .8rem}
p.lead{font-size:1.1rem;color:var(--muted);margin:0 0 1.5rem}
a{color:var(--accent)}
.note{border-left:3px solid var(--line);padding:.2rem 0 .2rem 1rem;color:var(--muted)}
.wrap{overflow-x:auto}
table{border-collapse:collapse;width:100%;font-size:.92rem}
th,td{text-align:left;padding:.45rem .6rem;border-bottom:1px solid var(--line);vertical-align:top}
th{font-weight:600;color:var(--muted)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
.lvl{font-size:.75rem;font-weight:600;letter-spacing:.03em;padding:.1rem .4rem;border-radius:4px;border:1px solid var(--line)}
.HIGH{color:var(--warn);border-color:var(--warn)}
.MEDIUM{color:var(--accent);border-color:var(--accent)}
img.fig{width:100%;height:auto;margin:1rem 0 .3rem}
.cap{font-size:.85rem;color:var(--muted);margin:0 0 1rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:1rem 0}
.stat{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:.8rem 1rem}
.stat b{display:block;font-size:1.6rem;font-variant-numeric:tabular-nums}
.stat span{font-size:.85rem;color:var(--muted)}
pre{background:var(--card);border:1px solid var(--line);border-radius:8px;padding:1rem;overflow-x:auto;font-size:.85rem}
@media (max-width:600px){.hide-sm{display:none}code{font-size:.8rem}}
footer{margin-top:4rem;font-size:.85rem;color:var(--muted)}
"""


def esc(s) -> str:
    return html.escape(str(s))


def level(score: int, lvl: str) -> str:
    return f'{score} <span class="lvl {lvl}">{lvl}</span>'


def cases_table() -> str:
    cab, sl = CableLayer.bundled(), watchlist.load()
    rows = []
    for key, case in ALL.items():
        fx = load_fixture(ROOT / "data" / "fixtures" / f"{key}.json")
        before = analyze_fixture(case, fx, cab, True, sl)
        full = analyze_fixture(case, fx, cab, False, sl)
        name, what = NAMES[key]
        link = f'<a href="{REPO}/blob/main/cases/{key}.md">{esc(name)}</a>' if key in CASES else esc(name)
        rows.append(
            f"<tr><td>{link}<br><span class=cap>{esc(what)}</span></td>"
            f'<td class="num">{level(before.score, before.level)}</td><td class="num">{level(full.score, full.level)}</td>'
            f"<td class=hide-sm>{', '.join(f'<code>{s.code}</code>' for s in before.signals if s.points) or '–'}</td></tr>"
        )
    return (
        '<div class="wrap"><table><thead><tr><th>Ship</th><th class="num">Before the incident</th>'
        '<th class="num">Full data</th><th class=hide-sm>Scored before the incident</th></tr></thead><tbody>'
        + "".join(rows)
        + "</tbody></table></div>"
    )


def eval_block() -> str:
    if not evaluate.BUNDLED.exists():
        return ""
    data = evaluate.load()
    r = evaluate.evaluate(data)
    pct = "{:.0%}".format
    hi, med = r["levels"]["HIGH"], r["levels"]["MEDIUM"]
    stats = [
        (f"{r['auc']:.2f}", f"AUC (95% CI {r['auc_ci95'][0]:.2f}–{r['auc_ci95'][1]:.2f})"),
        (f"{r['median']['sanctioned']:g} vs {r['median']['control']:g}", "median score, sanctioned vs. random"),
        (f"{pct(med['sanctioned_flagged'])} vs {pct(med['controls_flagged'])}", "score ≥ 20 (MEDIUM or HIGH)"),
        (f"{pct(hi['sanctioned_flagged'])} vs {pct(hi['controls_flagged'])}", "score ≥ 50 (HIGH)"),
    ]
    rows = "".join(
        f'<tr><td><code>{esc(c)}</code></td><td class="num">{pct(v["sanctioned"])}</td><td class="num">{pct(v["control"])}</td></tr>'
        for c, v in r["signals"].items()
    )
    return f"""
<h2>UK-sanctioned vessels and sampled controls</h2>
<p>{r["n"]["sanctioned"]} vessels designated under the UK Russia sanctions regime, compared with
{r["n"]["control"]} sampled valid IMO numbers with a similar prefix distribution. Identity timestamps are filtered
at each reference date; current links and registry matches remain. Only identity checks run, with sanctions
points switched off. One rule was revised while preparing the sanctioned sample, so this is not an untouched
validation set. The comparison measures separation of these groups, not prediction of cable incidents.</p>
<div class="stats">{"".join(f"<div class=stat><b>{a}</b><span>{esc(b)}</span></div>" for a, b in stats)}</div>
<img class="fig" src="img/evaluation.png" alt="Score distribution of sanctioned vessels and random ships">
<div class="wrap"><table><thead><tr><th>Signal</th><th class="num">sanctioned</th><th class="num">random ships</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<p class="cap">Share of ships in each group with the signal. Details and caveats:
<a href="{REPO}/blob/main/docs/evaluation.md">docs/evaluation.md</a>.</p>
<p>The 8 % HIGH share applies to these 300 controls, not the world fleet or false alarms for cable incidents.
Flag and registry signals alone reach almost the same AUC as the combined score. The bootstrap interval does
not include sampling bias, uncertain labels or hindsight in the source data.</p>
"""


def page() -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shadow Ship Check</title>
<meta name="description" content="Inspect AIS identity changes and tracks around reported subsea cable incidents.">
<style>{CSS}</style></head><body><main>
<h1>Shadow Ship Check</h1>
<p class="lead">I use this Python CLI to examine changes in ships' AIS identities and their tracks around reported
subsea cable incidents in Taiwan and the Baltic Sea.</p>
<p>I am a politics and economics student based in Taipei. I built Shadow Ship Check to investigate identity changes
reported around cable incidents. It runs explicit rules on data from Global Fishing Watch and lists the records
behind each result. <a href="{REPO}">Code and documentation on GitHub</a>.</p>
<p>The results help prioritise research into a known ship or identity cluster. They do not establish intent,
responsibility for damage or a probability of a future incident. HIGH means several rules fired; LOW can also
reflect limited data.</p>

<img class="fig" src="img/xingshun39_handover.png" alt="Map of two AIS identities of Xingshun 39 north of Keelung">
<p class="cap">The Xingshun 39 case links a Tanzania identity with an IMO number and a Cameroon identity without
one. Their tracks show a possible handover at sea. Searching GFW by IMO alone misses the second identity;
this case links it manually by name and track evidence.</p>

<h2>Reference incidents</h2>
<p>Each case is scored twice: with a timestamp cut-off before the incident, and with the full bundled snapshot.
Current identity links, registry matches and manual associations remain. Flag weights use the 2025 Paris MoU list,
published in July 2026. These are retrospective comparisons, not demonstrated advance warnings. One sale can
trigger several signals, and movement checks have no independent validation. See the
<a href="{REPO}/blob/main/docs/methodology.md">methodology</a> for thresholds and limitations.</p>
{cases_table()}
<img class="fig" src="img/yipeng3_cables.png" alt="Yi Peng 3 track crossing two Baltic cables at reduced speed">
<p class="cap">Yi Peng 3 has no scored recent identity changes. Straight-line track segments cross both cable
routes within intervals containing the reported failure times. Only the C-Lion1 crossing meets the scoring
threshold; these reconstructed crossings do not establish anchor use or responsibility.</p>
{eval_block()}
<h2>Try it</h2>
<pre>git clone {REPO} && cd shadow-ship-check
pip install -e .
ssc case all                 # reference cases, offline
ssc eval                     # sanctioned-vessel comparison, offline
ssc check 9224984 --start 2024-11-16 --end 2024-11-19   # any ship, live from GFW</pre>
<footer>Vessel data © Global Fishing Watch (CC BY-NC 4.0) · cable routes © OpenStreetMap contributors (ODbL) ·
sanctions: UK Sanctions List (OGL v3) via OpenSanctions (CC BY-NC 4.0) · land: Natural Earth · code: MIT ·
<a href="{REPO}">{REPO.removeprefix("https://")}</a></footer>
</main></body></html>
"""


if __name__ == "__main__":
    (OUT / "img").mkdir(parents=True, exist_ok=True)
    for png in (ROOT / "docs" / "img").glob("*.png"):
        shutil.copy(png, OUT / "img" / png.name)
    (OUT / "index.html").write_text(page(), encoding="utf-8")
    print("written:", OUT / "index.html")
