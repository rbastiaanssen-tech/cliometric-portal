#!/usr/bin/env python3
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

OUT_PDF = Path("manuscript/figure1_corridor_maps.pdf")
OUT_PNG = Path("manuscript/figure1_corridor_maps.png")

# Detailed coastlines (lon, lat) for NYT-style cartographic locator panels
CONT_EUROPE = [
    (-4.7, 48.4), (-3.5, 48.8), (-1.9, 49.7), (-1.2, 49.4), (0.1, 49.5), (1.6, 50.9),
    (2.2, 51.1), (3.4, 51.4), (4.1, 51.9), (4.8, 52.9), (5.4, 53.4), (7.1, 53.6),
    (8.6, 53.9), (8.9, 54.8), (9.8, 54.8), (10.2, 54.4), (11.1, 54.4), (12.1, 54.2),
    (13.8, 53.9), (14.8, 54.2), (16.5, 54.6), (16.5, 45.2), (13.8, 45.6), (12.3, 45.4),
    (12.3, 44.5), (13.5, 43.6), (14.2, 42.5), (15.8, 41.9), (18.4, 40.2), (16.2, 38.9),
    (15.6, 38.2), (15.1, 39.8), (13.6, 41.2), (12.2, 41.8), (11.1, 42.5), (10.3, 43.7),
    (9.0, 44.4), (7.5, 43.8), (6.5, 43.1), (4.8, 43.4), (3.1, 42.5), (-4.7, 43.4), (-4.7, 48.4)
]

GREAT_BRITAIN = [
    (-5.6, 50.1), (-4.2, 50.3), (-2.5, 50.6), (-1.1, 50.8), (0.3, 50.8), (1.4, 51.2),
    (1.1, 51.5), (1.7, 52.5), (1.3, 52.9), (0.3, 52.9), (0.1, 53.5), (-0.4, 54.1),
    (-1.2, 54.7), (-1.6, 55.5), (-2.1, 55.9), (-3.1, 56.0), (-2.6, 56.3), (-2.1, 57.1),
    (-1.8, 57.6), (-3.5, 57.6), (-4.0, 58.0), (-3.1, 58.6), (-4.9, 58.5), (-5.4, 57.8),
    (-5.8, 56.8), (-5.2, 55.8), (-4.8, 55.0), (-4.9, 54.7), (-3.6, 54.9), (-3.5, 54.4),
    (-3.0, 53.9), (-3.1, 53.4), (-4.4, 53.3), (-4.7, 52.9), (-4.1, 52.5), (-5.2, 51.9),
    (-5.0, 51.6), (-3.2, 51.4), (-4.2, 51.1), (-5.6, 50.1)
]

IRELAND = [
    (-10.3, 51.8), (-9.9, 52.5), (-9.1, 53.2), (-10.1, 53.9), (-9.6, 54.3), (-8.3, 54.6),
    (-7.6, 55.2), (-6.1, 55.1), (-5.5, 54.4), (-6.2, 53.9), (-6.1, 53.3), (-6.2, 52.3),
    (-7.6, 52.1), (-8.5, 51.7), (-10.3, 51.8)
]

ALPINE_NODES = [
    ("Antwerp", 4.40, 51.22, (-46, 5), True),
    ("Brussels", 4.35, 50.85, (-46, -10), False),
    ("Cologne", 6.96, 50.94, (6, 3), False),
    ("Augsburg", 10.90, 48.37, (6, 3), False),
    ("Munich", 11.58, 48.14, (7, -6), False),
    ("Innsbruck", 11.40, 47.26, (-52, 2), False),
    ("Brenner Pass", 11.50, 47.00, (7, -4), False),
    ("Verona", 10.99, 45.44, (-40, -6), False),
    ("Venice", 12.32, 45.44, (7, -3), True),
]

UK_NODES = [
    ("London", -0.12, 51.51, (7, -3), True),
    ("Bristol", -2.59, 51.45, (-34, -6), False),
    ("Cambridge", 0.12, 52.21, (7, -2), False),
    ("Norwich", 1.30, 52.63, (6, -2), False),
    ("Manchester", -2.24, 53.48, (7, 2), False),
    ("Liverpool", -2.99, 53.41, (-48, -4), True),
    ("Leeds", -1.55, 53.80, (7, 2), False),
    ("Hull", -0.34, 53.74, (6, -4), False),
    ("Newcastle", -1.62, 54.98, (7, -2), False),
    ("Edinburgh", -3.19, 55.95, (7, 1), False),
    ("Glasgow", -4.25, 55.86, (-44, -2), False),
]

def add_scale_bar(ax, x0, y0, length_deg, label):
    ax.plot([x0, x0 + length_deg], [y0, y0], color="#1D2939", lw=1.6, zorder=10)
    ax.plot([x0, x0], [y0 - 0.08, y0 + 0.08], color="#1D2939", lw=1.2, zorder=10)
    ax.plot([x0 + length_deg, x0 + length_deg], [y0 - 0.08, y0 + 0.08], color="#1D2939", lw=1.2, zorder=10)
    ax.text(x0 + length_deg / 2, y0 + 0.16, label, ha="center", va="bottom", fontsize=7.2, color="#1D2939", fontweight="bold")

def build_maps():
    plt.rcParams.update({"font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"], "font.family": "sans-serif"})
    fig = plt.figure(figsize=(7.4, 4.1))
    fig.patch.set_facecolor("white")

    # Economist-style top crimson rule & headline
    fig.lines.append(plt.Line2D([0.02, 0.98], [0.985, 0.985], transform=fig.transFigure, color="#C8372D", lw=2.2))
    fig.text(0.02, 0.935, "Two corridors anchor four millennia of communication benchmarks", fontsize=11, fontweight="bold", color="#101828")
    fig.text(0.02, 0.895, "Primary empirical routes across the Alpine barrier and the North Atlantic", fontsize=8.5, color="#475467")

    gs = fig.add_gridspec(1, 2, left=0.02, right=0.98, top=0.81, bottom=0.04, wspace=0.06)
    ax1, ax2 = fig.add_subplot(gs[0]), fig.add_subplot(gs[1])

    # Panel A: Antwerp-Venice
    ax1.set_facecolor("#DCE6EE")
    ax1.add_patch(Polygon(CONT_EUROPE, closed=True, facecolor="#F2EFE9", edgecolor="#8C969E", lw=0.75, zorder=1))
    ax1.fill_between([6.2, 14.5], 45.85, 47.65, color="#E2DDD2", alpha=0.85, zorder=2)
    ax1.text(7.3, 46.55, "A L P I N E   B A R R I E R", fontsize=6.8, color="#667085", fontweight="bold", zorder=2)

    ax1.plot([n[1] for n in ALPINE_NODES], [n[2] for n in ALPINE_NODES], color="#C8372D", lw=1.8, ls="--", zorder=4)
    for name, lon, lat, (dx, dy), is_end in ALPINE_NODES:
        ax1.scatter(lon, lat, color="#C8372D" if is_end else "#1D2939", s=38 if is_end else 18, edgecolor="white", lw=0.7, zorder=5)
        ax1.annotate(name, (lon, lat), xytext=(dx, dy), textcoords="offset points",
                     fontsize=7.2, fontweight="bold" if is_end else "normal", color="#101828",
                     bbox=dict(boxstyle="round,pad=0.1", fc="#F2EFE9", ec="none", alpha=0.75), zorder=6)

    ax1.set_xlim(1.8, 15.2)
    ax1.set_ylim(43.8, 52.8)
    ax1.set_title("A. Transalpine corridor (~1,150 km)", loc="left", fontsize=8.8, fontweight="bold", color="#101828", pad=5)
    add_scale_bar(ax1, 2.4, 44.3, 2.7, "200 km")

    # Panel B: British Network & Transatlantic Cablehead
    ax2.set_facecolor("#DCE6EE")
    ax2.add_patch(Polygon(GREAT_BRITAIN, closed=True, facecolor="#F2EFE9", edgecolor="#8C969E", lw=0.75, zorder=1))
    ax2.add_patch(Polygon(IRELAND, closed=True, facecolor="#F2EFE9", edgecolor="#8C969E", lw=0.75, zorder=1))

    spine = ["London", "Cambridge", "Leeds", "Newcastle", "Edinburgh", "Glasgow"]
    spine_pts = [next(n for n in UK_NODES if n[0] == s) for s in spine]
    ax2.plot([n[1] for n in spine_pts], [n[2] for n in spine_pts], color="#0F3D5E", lw=1.8, ls="--", zorder=4)

    for name, lon, lat, (dx, dy), is_hub in UK_NODES:
        ax2.scatter(lon, lat, color="#0F3D5E" if is_hub else "#344054", s=36 if is_hub else 18, edgecolor="white", lw=0.7, zorder=5)
        ax2.annotate(name, (lon, lat), xytext=(dx, dy), textcoords="offset points",
                     fontsize=7.0, fontweight="bold" if is_hub else "normal", color="#101828",
                     bbox=dict(boxstyle="round,pad=0.08", fc="#F2EFE9", ec="none", alpha=0.7), zorder=6)

    ax2.scatter(-10.35, 51.93, color="#C8372D", marker="D", s=34, edgecolor="white", lw=0.7, zorder=6)
    ax2.annotate("Valentia Island\n(1866 cablehead)", (-10.35, 51.93), xytext=(6, -12), textcoords="offset points",
                 fontsize=6.8, color="#C8372D", fontweight="bold", zorder=6)
    ax2.annotate("", xy=(-11.5, 51.93), xytext=(-10.35, 51.93), arrowprops=dict(arrowstyle="->", color="#C8372D", lw=1.4))
    ax2.text(-11.4, 52.45, "To Heart's Content &\nNew York (5,570 km)", fontsize=6.8, color="#0F3D5E", fontweight="bold")

    ax2.set_xlim(-11.7, 3.2)
    ax2.set_ylim(49.7, 58.6)
    ax2.set_title("B. British network & transatlantic cablehead", loc="left", fontsize=8.8, fontweight="bold", color="#101828", pad=5)
    add_scale_bar(ax2, -11.0, 50.2, 2.35, "150 km")

    for ax in (ax1, ax2):
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_edgecolor("#CBD5E1")
            sp.set_linewidth(0.8)

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated:", OUT_PDF)

if __name__ == "__main__":
    build_maps()
