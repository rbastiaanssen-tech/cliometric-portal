#!/usr/bin/env python3
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT_PDF = Path("manuscript/figure1_corridor_maps.pdf")
OUT_PNG = Path("manuscript/figure1_corridor_maps.png")

# Clean high-contrast schematic coastlines & political outlines (lon, lat)
EU_COAST = [
    (-4.5, 48.4), (-1.8, 49.6), (1.8, 51.0), (4.3, 52.0), (6.5, 53.5), (8.6, 54.0), (9.5, 54.8),
    (11.0, 54.4), (14.2, 53.9), (16.5, 54.5)
]
ITALY_COAST = [
    (7.5, 43.8), (8.9, 44.4), (10.2, 43.9), (11.2, 42.4), (13.6, 41.2), (15.6, 38.2),
    (16.2, 38.9), (18.4, 40.2), (16.0, 41.9), (14.2, 42.5), (12.3, 44.5), (12.3, 45.4), (13.7, 45.6)
]
UK_COAST = [
    (-5.5, 50.1), (-2.0, 50.6), (1.3, 51.2), (1.7, 52.6), (0.2, 53.0), (-0.4, 54.1),
    (-1.6, 55.6), (-3.1, 56.0), (-2.1, 57.5), (-4.8, 58.5), (-5.8, 56.8), (-4.8, 55.0),
    (-3.2, 54.5), (-3.1, 53.4), (-4.5, 53.2), (-5.1, 51.7), (-3.2, 51.4), (-5.5, 50.1)
]
IRELAND_COAST = [
    (-10.2, 51.8), (-9.8, 53.5), (-8.2, 55.2), (-6.0, 55.0), (-6.2, 53.3), (-6.5, 52.2), (-10.2, 51.8)
]

ALPINE_NODES = [
    ("Antwerp", 4.40, 51.22, (-38, 6)),
    ("Brussels", 4.35, 50.85, (-42, -10)),
    ("Cologne", 6.96, 50.94, (6, 4)),
    ("Augsburg", 10.90, 48.37, (6, 3)),
    ("Munich", 11.58, 48.14, (7, -6)),
    ("Innsbruck", 11.40, 47.26, (-48, -4)),
    ("Brenner Pass", 11.50, 47.00, (7, -3)),
    ("Verona", 10.99, 45.44, (-36, -6)),
    ("Venice", 12.32, 45.44, (7, -3)),
]

UK_NODES = [
    ("London", -0.12, 51.51, (7, -4)),
    ("Bristol", -2.59, 51.45, (-34, -6)),
    ("Cambridge", 0.12, 52.21, (7, -2)),
    ("Norwich", 1.30, 52.63, (7, -2)),
    ("Manchester", -2.24, 53.48, (-52, 2)),
    ("Liverpool", -2.99, 53.41, (-46, -9)),
    ("Leeds", -1.55, 53.80, (7, 1)),
    ("Hull", -0.34, 53.74, (7, -4)),
    ("Newcastle", -1.62, 54.98, (7, -2)),
    ("Edinburgh", -3.19, 55.95, (7, 1)),
    ("Glasgow", -4.25, 55.86, (-44, -2)),
]

def build_maps():
    plt.rcParams.update({"font.family": "serif", "font.size": 8.5, "axes.titlesize": 9.8})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.6), gridspec_kw={"wspace": 0.16})

    # Panel A: Antwerp-Venice Alpine Corridor
    ax1.set_facecolor("#f4f6f8")
    ax1.plot([x for x, _ in EU_COAST], [y for _, y in EU_COAST], color="#7b8794", lw=1.0)
    ax1.plot([x for x, _ in ITALY_COAST], [y for _, y in ITALY_COAST], color="#7b8794", lw=1.0)
    ax1.fill_between([6.5, 14.5], 45.8, 47.7, color="#d9e2ec", alpha=0.55, label="Alpine Barrier")
    ax1.text(8.4, 46.7, "A L P S", fontsize=8, color="#486581", style="italic", fontweight="bold")

    ax1.plot([n[1] for n in ALPINE_NODES], [n[2] for n in ALPINE_NODES], color="#b83227", lw=2.0, ls="--", zorder=4)
    for name, lon, lat, (dx, dy) in ALPINE_NODES:
        is_end = name in ("Antwerp", "Venice")
        ax1.scatter(lon, lat, color="#b83227" if is_end else "#1f2933", s=46 if is_end else 22, edgecolor="white", lw=0.7, zorder=5)
        ax1.annotate(name, (lon, lat), xytext=(dx, dy), textcoords="offset points",
                     fontsize=7.6, fontweight="bold" if is_end else "normal", color="#102a43")

    ax1.set_xlim(1.5, 15.5)
    ax1.set_ylim(43.8, 53.2)
    ax1.set_xlabel("Longitude (°E)")
    ax1.set_ylabel("Latitude (°N)")
    ax1.set_title("A. Antwerp–Venice Transalpine Corridor (~1,150 km)", fontweight="bold", pad=8)
    ax1.grid(True, ls=":", lw=0.5, color="#bcccdc")

    # Panel B: British Research Network & Transatlantic Cablehead
    ax2.set_facecolor("#f4f6f8")
    ax2.fill([x for x, _ in UK_COAST], [y for _, y in UK_COAST], facecolor="#e4e7eb", edgecolor="#7b8794", lw=1.0)
    ax2.fill([x for x, _ in IRELAND_COAST], [y for _, y in IRELAND_COAST], facecolor="#e4e7eb", edgecolor="#7b8794", lw=1.0)

    spine = ["London", "Cambridge", "Leeds", "Newcastle", "Edinburgh", "Glasgow"]
    spine_pts = [next(n for n in UK_NODES if n[0] == s) for s in spine]
    ax2.plot([n[1] for n in spine_pts], [n[2] for n in spine_pts], color="#1b4965", lw=2.0, ls="--", zorder=4)

    for name, lon, lat, (dx, dy) in UK_NODES:
        is_hub = name in ("London", "Liverpool", "Manchester", "Glasgow")
        ax2.scatter(lon, lat, color="#1b4965" if is_hub else "#334e68", s=42 if is_hub else 24, edgecolor="white", lw=0.7, zorder=5)
        ax2.annotate(name, (lon, lat), xytext=(dx, dy), textcoords="offset points",
                     fontsize=7.5, fontweight="bold" if is_hub else "normal", color="#102a43")

    # Valentia Island (Transatlantic Cablehead 1866)
    ax2.scatter(-10.35, 51.93, color="#b83227", marker="D", s=42, edgecolor="white", lw=0.7, zorder=6)
    ax2.annotate("Valentia (1866\nCablehead)", (-10.35, 51.93), xytext=(6, -10), textcoords="offset points", fontsize=7.2, color="#b83227", fontweight="bold")
    ax2.annotate("", xy=(-11.4, 51.93), xytext=(-10.35, 51.93), arrowprops=dict(arrowstyle="->", color="#b83227", lw=1.5))
    ax2.text(-11.3, 52.35, "To Heart's Content &\nNew York (5,570 km)", fontsize=7.0, color="#b83227")

    ax2.set_xlim(-11.5, 2.8)
    ax2.set_ylim(49.8, 58.6)
    ax2.set_xlabel("Longitude (°W / °E)")
    ax2.set_title("B. British Network & Transatlantic Cablehead", fontweight="bold", pad=8)
    ax2.grid(True, ls=":", lw=0.5, color="#bcccdc")

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated:", OUT_PDF)

if __name__ == "__main__":
    build_maps()
