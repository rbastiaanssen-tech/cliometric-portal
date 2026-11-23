#!/usr/bin/env python3
import json
import urllib.request
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

NE_URL = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_50m_admin_0_countries.geojson"
CACHE_GEOJSON = Path("scripts/ne_50m_admin_0_countries.geojson")
OUT_PDF = Path("manuscript/figure1_corridor_maps.pdf")
OUT_PNG = Path("manuscript/figure1_corridor_maps.png")

ALPINE_NODES = [
    ("Antwerp", 4.40, 51.22, (-44, 5), True),
    ("Brussels", 4.35, 50.85, (-44, -9), False),
    ("Cologne", 6.96, 50.94, (6, 2), False),
    ("Augsburg", 10.90, 48.37, (-48, 3), False),
    ("Munich", 11.58, 48.14, (7, -3), False),
    ("Innsbruck", 11.40, 47.26, (-52, 1), False),
    ("Brenner Pass", 11.50, 47.00, (7, -3), False),
    ("Verona", 10.99, 45.44, (-40, -6), False),
    ("Venice", 12.32, 45.44, (7, -3), True),
]

UK_NODES = [
    ("London", -0.12, 51.51, (7, -3), True),
    ("Bristol", -2.59, 51.45, (-34, -5), False),
    ("Cambridge", 0.12, 52.21, (7, -2), False),
    ("Norwich", 1.30, 52.63, (6, -2), False),
    ("Manchester", -2.24, 53.48, (-54, 4), False),
    ("Liverpool", -2.99, 53.41, (-48, -7), True),
    ("Leeds", -1.55, 53.80, (7, 4), False),
    ("Hull", -0.34, 53.74, (7, -5), False),
    ("Newcastle", -1.62, 54.98, (7, -2), False),
    ("Edinburgh", -3.19, 55.95, (7, 2), False),
    ("Glasgow", -4.25, 55.86, (-45, -2), False),
]

def load_geojson():
    if not CACHE_GEOJSON.exists():
        print("Downloading Natural Earth 1:50m boundaries...")
        urllib.request.urlretrieve(NE_URL, CACHE_GEOJSON)
    return json.loads(CACHE_GEOJSON.read_text(encoding="utf-8"))

def draw_countries(ax, geo, xlim, ylim):
    for feat in geo["features"]:
        geom = feat["geometry"]
        polys = [geom["coordinates"]] if geom["type"] == "Polygon" else geom["coordinates"]
        for poly in polys:
            ring = poly[0]
            xs = [pt[0] for pt in ring]
            ys = [pt[1] for pt in ring]
            if max(xs) < xlim[0] or min(xs) > xlim[1] or max(ys) < ylim[0] or min(ys) > ylim[1]:
                continue
            ax.add_patch(Polygon(ring, closed=True, facecolor="#F3F0E8", edgecolor="#8E98A2", lw=0.65, zorder=1))

def add_scale_bar(ax, x0, y0, deg_len, label):
    ax.plot([x0, x0 + deg_len], [y0, y0], color="#101828", lw=1.6, zorder=10)
    ax.plot([x0, x0], [y0 - 0.08, y0 + 0.08], color="#101828", lw=1.2, zorder=10)
    ax.plot([x0 + deg_len, x0 + deg_len], [y0 - 0.08, y0 + 0.08], color="#101828", lw=1.2, zorder=10)
    ax.text(x0 + deg_len / 2, y0 + 0.14, label, ha="center", va="bottom", fontsize=7.0, color="#101828", fontweight="bold", zorder=10)

def build_maps():
    geo = load_geojson()
    plt.rcParams.update({"font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"], "font.family": "sans-serif"})
    fig = plt.figure(figsize=(7.4, 4.2))
    fig.patch.set_facecolor("white")

    fig.lines.append(plt.Line2D([0.02, 0.98], [0.985, 0.985], transform=fig.transFigure, color="#C8372D", lw=2.2))
    fig.text(0.02, 0.935, "Two corridors anchor four millennia of communication benchmarks", fontsize=10.8, fontweight="bold", color="#101828")
    fig.text(0.02, 0.896, "Primary empirical routes across the Alpine barrier and the North Atlantic (Natural Earth 1:50m)", fontsize=8.1, color="#475467")

    gs = fig.add_gridspec(1, 2, left=0.02, right=0.98, top=0.81, bottom=0.04, wspace=0.06)
    ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    # Panel A: Antwerp-Venice
    xlim1, ylim1 = (1.5, 15.5), (43.8, 52.8)
    ax1.set_facecolor("#D6E4EE")
    draw_countries(ax1, geo, xlim1, ylim1)
    ax1.fill_between([6.0, 14.8], 45.85, 47.65, color="#DFD9CE", alpha=0.65, zorder=2)
    ax1.text(6.6, 46.45, "A L P I N E   B A R R I E R", fontsize=6.6, color="#5C6672", fontweight="bold", zorder=2)

    ax1.plot([n[1] for n in ALPINE_NODES], [n[2] for n in ALPINE_NODES], color="#C8372D", lw=1.8, ls="--", zorder=4)
    for name, lon, lat, (dx, dy), is_end in ALPINE_NODES:
        ax1.scatter(lon, lat, color="#C8372D" if is_end else "#1D2939", s=38 if is_end else 18, edgecolor="white", lw=0.7, zorder=5)
        ax1.annotate(name, (lon, lat), xytext=(dx, dy), textcoords="offset points",
                     fontsize=7.0, fontweight="bold" if is_end else "normal", color="#101828",
                     bbox=dict(boxstyle="round,pad=0.08", fc="#F3F0E8", ec="none", alpha=0.82), zorder=6)
    ax1.set_xlim(*xlim1)
    ax1.set_ylim(*ylim1)
    ax1.set_title("A. Transalpine corridor (~1,150 km)", loc="left", fontsize=8.6, fontweight="bold", color="#101828", pad=5)
    add_scale_bar(ax1, 2.2, 44.3, 2.7, "200 km")

    # Panel B: British Network & Transatlantic Cablehead
    xlim2, ylim2 = (-11.8, 3.2), (49.7, 58.6)
    ax2.set_facecolor("#D6E4EE")
    draw_countries(ax2, geo, xlim2, ylim2)

    spine = ["London", "Cambridge", "Leeds", "Newcastle", "Edinburgh", "Glasgow"]
    spine_pts = [next(n for n in UK_NODES if n[0] == s) for s in spine]
    ax2.plot([n[1] for n in spine_pts], [n[2] for n in spine_pts], color="#0F3D5E", lw=1.8, ls="--", zorder=4)

    for name, lon, lat, (dx, dy), is_hub in UK_NODES:
        ax2.scatter(lon, lat, color="#0F3D5E" if is_hub else "#344054", s=36 if is_hub else 18, edgecolor="white", lw=0.7, zorder=5)
        ax2.annotate(name, (lon, lat), xytext=(dx, dy), textcoords="offset points",
                     fontsize=6.9, fontweight="bold" if is_hub else "normal", color="#101828",
                     bbox=dict(boxstyle="round,pad=0.07", fc="#F3F0E8", ec="none", alpha=0.8), zorder=6)

    ax2.scatter(-10.35, 51.93, color="#C8372D", marker="D", s=34, edgecolor="white", lw=0.7, zorder=6)
    ax2.annotate("Valentia Island\n(1866 cablehead)", (-10.35, 51.93), xytext=(6, -13), textcoords="offset points",
                 fontsize=6.7, color="#C8372D", fontweight="bold", zorder=6)
    ax2.annotate("", xy=(-11.6, 51.93), xytext=(-10.35, 51.93), arrowprops=dict(arrowstyle="->", color="#C8372D", lw=1.4))
    ax2.text(-11.5, 52.50, "To Heart's Content &\nNew York (5,570 km)", fontsize=6.7, color="#0F3D5E", fontweight="bold")

    ax2.set_xlim(*xlim2)
    ax2.set_ylim(*ylim2)
    ax2.set_title("B. British network & transatlantic cablehead", loc="left", fontsize=8.6, fontweight="bold", color="#101828", pad=5)
    add_scale_bar(ax2, -11.1, 50.2, 2.35, "150 km")

    for ax in (ax1, ax2):
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor("#CBD5E1")
            sp.set_linewidth(0.8)

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated real Natural Earth map:", OUT_PDF)

if __name__ == "__main__":
    build_maps()
