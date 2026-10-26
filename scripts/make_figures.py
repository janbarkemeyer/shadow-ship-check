"""Draw the README figures from the fixtures.

    npm pack world-atlas@2.0.2 && tar xzf world-atlas-2.0.2.tgz   # Natural Earth land, public domain
    python scripts/make_figures.py package/land-10m.json

Needs matplotlib. Output: docs/img/*.png
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from shadow_ship_check.models import TrackPoint  # noqa: E402

OUT = ROOT / "docs" / "img"
INK, MUTED, GRID = "#1f2933", "#7b8794", "#e4e7eb"
C1, C2, LAND, SEA = "#2f6fdf", "#e0613a", "#d9d4c7", "#f4f7fa"


def land_polygons(path: str):
    """Minimal TopoJSON decoder for world-atlas land-*.json (delta-encoded, quantized arcs)."""
    topo = json.loads(Path(path).read_text())
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcs = []
    for arc in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcs.append(pts)

    def ring(idx):
        out = []
        for i in idx:
            seg = arcs[i] if i >= 0 else arcs[~i][::-1]
            out.extend(seg if not out else seg[1:])
        return out

    polys = []
    for geom in topo["objects"]["land"]["geometries"]:
        parts = geom["arcs"] if geom["type"] == "MultiPolygon" else [geom["arcs"]]
        for poly in parts:
            polys.append([ring(r) for r in poly])
    return polys


def base(ax, polys, extent):
    ax.set_facecolor(SEA)
    for poly in polys:
        outer = poly[0]
        xs, ys = zip(*outer)
        if max(xs) < extent[0] or min(xs) > extent[1] or max(ys) < extent[2] or min(ys) > extent[3]:
            continue
        ax.fill(xs, ys, color=LAND, lw=0, zorder=1)
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_aspect(1 / abs(__import__("math").cos(__import__("math").radians((extent[2] + extent[3]) / 2))))
    ax.tick_params(colors=MUTED, labelsize=8)
    for s in ax.spines.values():
        s.set_color(GRID)
    ax.grid(color="white", lw=0.6, zorder=0)


def pts(fixture, key, start=None, end=None):
    fx = json.loads((ROOT / "data" / "fixtures" / f"{fixture}.json").read_text())
    p = [TrackPoint.from_row(r) for r in fx["tracks"][key]["points"]]
    return [x for x in p if (not start or x.t >= start) and (not end or x.t <= end)]


def utc(*a):
    return datetime(*a, tzinfo=timezone.utc)


def fig_xingshun(polys):
    a = pts("xingshun_39", "xingshun_39", utc(2024, 12, 28), utc(2025, 1, 4, 6))
    b = pts("xingshun_39", "shunxing39_cmr", utc(2024, 12, 28), utc(2025, 1, 4, 6))
    fig, ax = plt.subplots(figsize=(7.2, 6.4), dpi=160)
    base(ax, polys, (121.45, 122.25, 25.0, 26.2))
    ax.plot(
        [x.lon for x in b],
        [x.lat for x in b],
        color=C2,
        lw=1.4,
        zorder=3,
        label="SHUNXING39 · Cameroon · MMSI 613003889 · no IMO",
    )
    ax.plot(
        [x.lon for x in a],
        [x.lat for x in a],
        color=C1,
        lw=1.4,
        zorder=4,
        label="XINGSHUN39 · Tanzania · MMSI 677087200 · IMO 8358427",
    )
    off = [x for x in a if x.t <= utc(2024, 12, 29)][-1]
    last_b = [x for x in b if x.t <= utc(2025, 1, 3, 9)][-1]
    ax.scatter([off.lon], [off.lat], s=30, color=C1, zorder=5, edgecolor="white")
    ax.annotate(
        "XINGSHUN39 goes silent\n28 Dec 22:11 UTC",
        (off.lon, off.lat),
        (121.50, 25.08),
        fontsize=8,
        color=INK,
        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8),
    )
    ax.scatter([last_b.lon], [last_b.lat], s=46, facecolor="none", edgecolor=INK, lw=1.2, zorder=6)
    ax.annotate(
        "Handover: SHUNXING39 last position 08:19 UTC,\nXINGSHUN39 back at 08:52 UTC, 0.2 nm away (3 Jan)",
        (last_b.lon, last_b.lat),
        (121.48, 25.55),
        fontsize=8,
        color=INK,
        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8),
    )
    ax.text(121.505, 25.135, "Keelung", fontsize=8, color=MUTED)
    ax.set_title(
        "Xingshun 39: two AIS identities, one ship (28 Dec 2024 – 4 Jan 2025)", fontsize=10, color=INK, loc="left"
    )
    ax.legend(loc="upper left", fontsize=7.5, frameon=False)
    fig.text(0.01, 0.01, "Data: Global Fishing Watch (CC BY-NC 4.0); land: Natural Earth", fontsize=6.5, color=MUTED)
    fig.tight_layout()
    fig.savefig(OUT / "xingshun39_handover.png")


def fig_hongtai(polys):
    a = pts("hong_tai_58", "hong_tai_58", utc(2025, 2, 20), utc(2025, 2, 26))
    fig, ax = plt.subplots(figsize=(6.4, 6.4), dpi=160)
    base(ax, polys, (119.85, 120.35, 22.6, 23.4))
    ax.plot([x.lon for x in a], [x.lat for x in a], color=C1, lw=1.3, zorder=3)
    anch = [x for x in a if utc(2025, 2, 22, 10, 40) <= x.t <= utc(2025, 2, 24, 18, 57)]
    ax.scatter(
        [x.lon for x in anch],
        [x.lat for x in anch],
        s=4,
        color=C2,
        zorder=4,
        label="stationary 22 Feb 10:40 – 24 Feb 18:57 UTC (~56 h)",
    )
    dep = [x for x in a if x.t >= utc(2025, 2, 24, 19, 10)][0]
    ax.annotate(
        "departs 24 Feb ~19:00 UTC (03:00 local)\n4.5–5.2 kn, then 78 min without position",
        (dep.lon, dep.lat),
        (119.865, 23.355),
        fontsize=8,
        color=INK,
        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8),
    )
    end = a[-1]
    ax.annotate(
        "last position 25 Feb 04:18 UTC\n(detained)",
        (end.lon, end.lat),
        (119.88, 22.85),
        fontsize=8,
        color=INK,
        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8),
    )
    ax.annotate("from Kaohsiung", (a[0].lon, a[0].lat), (120.0, 22.64), fontsize=8, color=MUTED)
    ax.set_title("Hong Tai 58 (HONGTAI58 · Togo · no IMO), 20–25 Feb 2025", fontsize=10, color=INK, loc="left")
    ax.legend(loc="lower left", fontsize=7.5, frameon=False)
    fig.text(0.01, 0.01, "Data: Global Fishing Watch (CC BY-NC 4.0); land: Natural Earth", fontsize=6.5, color=MUTED)
    fig.tight_layout()
    fig.savefig(OUT / "hongtai58_anchorage.png")


def fig_scores():
    import subprocess

    rows = subprocess.run(
        [sys.executable, "-m", "shadow_ship_check", "case", "all", "--md", "/tmp/ssc_fig"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        env={"PYTHONPATH": str(ROOT / "src")},
    ).stdout
    data = [(line.split()[0], int(line.split()[2])) for line in rows.splitlines() if " score " in line]
    names = {
        "eagle_s": "Eagle S",
        "xingshun_39": "Xingshun 39",
        "hong_tai_58": "Hong Tai 58",
        "yi_peng_3": "Yi Peng 3",
        "newnew_polar_bear": "NewNew Polar Bear",
        "control_finlandia": "Finlandia (control)",
        "control_yi_peng_5": "Yi Peng 5 (control)",
        "control_ever_liven": "Ever Liven (control)",
    }
    data.sort(key=lambda r: r[1])
    fig, ax = plt.subplots(figsize=(6.4, 3.2), dpi=160)
    colors = [MUTED if n.startswith("control") else C1 for n, _ in data]
    ax.barh([names[n] for n, _ in data], [s for _, s in data], color=colors, height=0.6)
    for i, (_, s) in enumerate(data):
        ax.text(s + 1.5, i, str(s), va="center", fontsize=8, color=INK)
    for x, lab in ((20, "MEDIUM"), (50, "HIGH")):
        ax.axvline(x, color=GRID, lw=1, zorder=0)
        ax.text(x + 1, len(data) - 0.4, lab, fontsize=7, color=MUTED)
    ax.set_xlim(0, 110)
    ax.tick_params(colors=INK, labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Score per ship (incident ships blue, controls grey)", fontsize=10, color=INK, loc="left")
    fig.tight_layout()
    fig.savefig(OUT / "scores.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    polys = land_polygons(sys.argv[1])
    fig_xingshun(polys)
    fig_hongtai(polys)
    fig_scores()
    print("written:", ", ".join(p.name for p in OUT.glob("*.png")))
