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
import matplotlib.ticker

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from shadow_ship_check.models import TrackPoint  # noqa: E402
from shadow_ship_check.signals import connected  # noqa: E402

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


def track_xy(points):
    """Break plotted lines at segment boundaries and gaps over three hours."""
    xs, ys = [], []
    for n, p in enumerate(points):
        if n and not connected(points[n - 1], p):
            xs.append(float("nan"))
            ys.append(float("nan"))
        xs.append(p.lon)
        ys.append(p.lat)
    return xs, ys


def fig_xingshun(polys):
    a = pts("xingshun_39", "xingshun_39", utc(2024, 12, 28), utc(2025, 1, 4, 6))
    b = pts("xingshun_39", "shunxing39_cmr", utc(2024, 12, 28), utc(2025, 1, 4, 6))
    fig, ax = plt.subplots(figsize=(7.2, 6.4), dpi=160)
    base(ax, polys, (121.45, 122.25, 25.0, 26.2))
    cables(ax, (121.45, 122.25, 25.0, 26.2), ("unnamed telecom (OSM way 1334156416)",))
    ax.plot(
        *track_xy(b),
        color=C2,
        lw=1.4,
        zorder=3,
        label="SHUNXING39 · Cameroon · MMSI 613003889 · no IMO",
    )
    ax.plot(
        *track_xy(a),
        color=C1,
        lw=1.4,
        zorder=4,
        label="XINGSHUN39 · Tanzania · MMSI 677087200 · IMO 8358427",
    )
    off = [x for x in a if x.t <= utc(2024, 12, 29)][-1]
    last_b = [x for x in b if x.t <= utc(2025, 1, 3, 9)][-1]
    ax.scatter([off.lon], [off.lat], s=30, color=C1, zorder=5, edgecolor="white")
    ax.annotate(
        "XINGSHUN39: last GFW position\nbefore gap, 28 Dec 22:11 UTC",
        (off.lon, off.lat),
        (121.84, 25.08),
        fontsize=8,
        color=INK,
        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8),
    )
    ax.scatter([last_b.lon], [last_b.lat], s=46, facecolor="none", edgecolor=INK, lw=1.2, zorder=6)
    ax.annotate(
        "Possible handover: last SHUNXING39 position 08:19 UTC,\nXINGSHUN39 recorded 08:52 UTC, 0.2 nm away (3 Jan)",
        (last_b.lon, last_b.lat),
        (121.48, 25.55),
        fontsize=8,
        color=INK,
        arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8),
    )
    ax.text(121.505, 25.135, "Keelung", fontsize=8, color=MUTED)
    ax.set_title("Xingshun 39: linked AIS identities (28 Dec 2024 – 4 Jan 2025)", fontsize=10, color=INK, loc="left")
    ax.legend(loc="upper left", fontsize=7.5, frameon=False)
    ax.plot([], [], color=INK, lw=1.1, label="telecom cable, unnamed in OpenStreetMap")
    ax.legend(loc="upper left", fontsize=7.5, frameon=False)
    fig.text(0.01, 0.01, "Data: Global Fishing Watch (CC BY-NC 4.0); cables: © OpenStreetMap contributors (ODbL); "
             "land: Natural Earth", fontsize=6, color=MUTED)  # fmt: skip
    fig.tight_layout()
    fig.savefig(OUT / "xingshun39_handover.png")


def cables(ax, extent, highlight=(), label_all=False):
    from shadow_ship_check.geo import CableLayer

    for name, cs in CableLayer.bundled().lines:
        xs, ys = zip(*cs)
        if max(xs) < extent[0] or min(xs) > extent[1] or max(ys) < extent[2] or min(ys) > extent[3]:
            continue
        hi = name in highlight
        ax.plot(xs, ys, color=INK if hi else "#b8c0c8", lw=1.1 if hi else 0.5, zorder=2, alpha=1 if hi else 0.8)


def fig_yipeng(polys):
    from statistics import median

    from shadow_ship_check.geo import CableLayer, haversine_nm

    a = pts("yi_peng_3", "yi_peng_3", utc(2024, 11, 16, 12), utc(2024, 11, 18, 18))
    ext = (14.6, 21.4, 54.75, 58.3)
    fig, ax = plt.subplots(figsize=(6.8, 6.4), dpi=160)
    base(ax, polys, ext)
    hi = ("BCS East-West Interlink", "C-Lion 1")
    cables(ax, ext, hi)
    ref = median(p.speed for p in pts("yi_peng_3", "yi_peng_3") if p.speed >= 5)
    for p, q in zip(a, a[1:]):
        if not connected(p, q):
            continue
        rate = haversine_nm(p.lat, p.lon, q.lat, q.lon) / max((q.t - p.t).total_seconds() / 3600, 1e-6)
        ax.plot([p.lon, q.lon], [p.lat, q.lat], color=C2 if rate <= 0.7 * ref else C1, lw=1.8, zorder=3)
    layer = CableLayer.bundled()
    notes = {
        "BCS East-West Interlink": (
            "crosses BCS East-West Interlink\n17 Nov 07:15-08:46 UTC, 6.7 kn\n(cut reported ~08:00 UTC)",
            (19.0, 57.75),
        ),
        "C-Lion 1": ("crosses C-Lion1\n18 Nov 01:39-03:10 UTC, 6.2 kn\n(failure 02:00 UTC)", (14.75, 56.55)),
    }  # fmt: skip
    for p, q in zip(a, a[1:]):
        if not connected(p, q):
            continue
        for name in layer.crossed((p.lon, p.lat), (q.lon, q.lat)):
            if name in notes:
                text, xy = notes.pop(name)
                mid = ((p.lon + q.lon) / 2, (p.lat + q.lat) / 2)
                ax.scatter(*mid, s=40, facecolor="none", edgecolor=INK, lw=1.2, zorder=6)
                ax.annotate(
                    text, mid, xy, fontsize=7.5, color=INK, arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8)
                )
    ax.plot([], [], color=C1, lw=1.8, label=f"> 70 % of median speed ({ref:.1f} kn)")
    ax.plot([], [], color=C2, lw=1.8, label="<= 70 % of median speed (over ground)")
    ax.plot([], [], color=INK, lw=1.1, label="damaged cables (OpenStreetMap)")
    ax.plot([], [], color="#b8c0c8", lw=0.6, label="other cables and pipelines")
    ax.set_title("Yi Peng 3, 16-18 Nov 2024: reduced speed across two cables", fontsize=10, color=INK, loc="left")
    ax.legend(loc="lower right", fontsize=7, frameon=True, facecolor="white", edgecolor="none")
    fig.text(0.01, 0.01, "Data: Global Fishing Watch (CC BY-NC 4.0); cables: © OpenStreetMap contributors (ODbL); "
             "land: Natural Earth", fontsize=6, color=MUTED)  # fmt: skip
    fig.tight_layout()
    fig.savefig(OUT / "yipeng3_cables.png")


def fig_hongtai(polys):
    a = pts("hong_tai_58", "hong_tai_58", utc(2025, 2, 20), utc(2025, 2, 26))
    fig, ax = plt.subplots(figsize=(6.4, 6.4), dpi=160)
    base(ax, polys, (119.85, 120.35, 22.6, 23.4))
    ax.plot(*track_xy(a), color=C1, lw=1.3, zorder=3)
    anch = [x for x in a if utc(2025, 2, 22, 10, 40) <= x.t <= utc(2025, 2, 24, 18, 57) and x.speed <= 3]
    ax.scatter(
        [x.lon for x in anch],
        [x.lat for x in anch],
        s=4,
        color=C2,
        zorder=4,
        label="AIS speed <= 3 kn, 22–24 Feb (positions only)",
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


def fig_evaluation():
    from shadow_ship_check import evaluate

    if not evaluate.BUNDLED.exists():
        return
    data = evaluate.load()
    groups = {"sanctioned": [], "control": []}
    for rec in data["records"]:
        if rec["identities"]:
            groups["sanctioned" if rec["label"] == "sanctioned" else "control"].append(evaluate.score_record(rec)[0])
    bins = list(range(0, 101, 10))
    fig, ax = plt.subplots(figsize=(6.6, 3.2), dpi=160)
    width = 3.6
    for off, (key, color, label) in zip(
        (-width / 2, width / 2),
        (("control", MUTED, "sampled controls"), ("sanctioned", C2, "UK-sanctioned (Russia), at designation date")),
    ):
        vals = groups[key]
        counts = [sum(1 for v in vals if b <= v < b + 10 or (b == 90 and v == 100)) / len(vals) for b in bins[:-1]]
        ax.bar([b + 5 + off for b in bins[:-1]], counts, width=width, color=color, label=f"{label} (n={len(vals)})")
    for x, lab in ((20, "MEDIUM"), (50, "HIGH")):
        ax.axvline(x, color="#cbd2d9", lw=0.8, zorder=0, ls="--")
        ax.text(x + 1, ax.get_ylim()[1] * 0.92, lab, fontsize=7, color=MUTED)
    ax.set_xticks(bins)
    ax.set_xlabel("identity score (0-100)", fontsize=8, color=INK)
    ax.set_ylabel("share of ships", fontsize=8, color=INK)
    ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(1.0, decimals=0))
    ax.tick_params(colors=INK, labelsize=8)
    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)
    ax.legend(fontsize=7.5, frameon=False, loc="upper right", bbox_to_anchor=(1.0, 0.86))
    ax.set_title("Identity score: UK-sanctioned ships vs. sampled controls", fontsize=9.5, color=INK, loc="left")
    fig.text(0.01, 0.01, "Data: Global Fishing Watch (CC BY-NC 4.0); UK Sanctions List via OpenSanctions",
             fontsize=6, color=MUTED)  # fmt: skip
    fig.tight_layout()
    fig.savefig(OUT / "evaluation.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    polys = land_polygons(sys.argv[1])
    fig_xingshun(polys)
    fig_hongtai(polys)
    fig_yipeng(polys)
    fig_evaluation()
    print("written:", ", ".join(p.name for p in OUT.glob("*.png")))
