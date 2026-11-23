#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

OUT_PDF = Path("manuscript/figure2_gvk_distance_latency.pdf")
OUT_PNG = Path("manuscript/figure2_gvk_distance_latency.png")

POINTS = [
    ("1895 BC · Assur–Kültepe", 1000, 2.419e6, "Ancient", (8, 4)),
    ("301 AD · Rome–Brundisium", 530, 6.912e5, "Ancient", (-78, -11)),
    ("750 AD · Chang'an–Guangzhou", 2250, 8.640e5, "Ancient", (-52, -13)),
    ("1395 · Antwerp–Venice", 1150, 1.382e6, "Antwerp-Venice", (8, 3)),
    ("1635 · Antwerp–Venice", 1150, 1.037e6, "Antwerp-Venice", (8, -6)),
    ("1825 · London–New York", 5570, 2.333e6, "London-New York", (-88, 5)),
    ("1855 · London–New York", 5570, 1.054e6, "London-New York", (-88, -10)),
    ("1866 · Atlantic cable", 5570, 1.20, "London-New York", (-85, 6)),
    ("1872 · Alpine telegraph", 1150, 0.050, "Antwerp-Venice", (8, 4)),
    ("1935 · Telephone", 1150, 0.015, "Antwerp-Venice", (8, -7)),
    ("1956 · TAT-1", 5570, 0.035, "London-New York", (-65, 7)),
    ("2026 · EU Fibre", 1150, 0.00575, "Antwerp-Venice", (-66, 6)),
    ("2026 · Atlantic Fibre", 5570, 0.02785, "London-New York", (-82, -11)),
]

COLORS = {"London-New York": "#1b4965", "Antwerp-Venice": "#b83227", "Ancient": "#8c6d1f"}

def build_gvk_dist():
    plt.rcParams.update({"font.family": "serif", "font.size": 8.8, "axes.labelsize": 9.5, "axes.titlesize": 10})
    fig, ax = plt.subplots(figsize=(9.5, 5.2))

    d_grid = np.logspace(0, 4.35, 300)

    # Diagonal iso-velocity rays: L = d / v
    rays = [
        (2.0 / 3.6, "Caravan (2 km/h)", 1.3, 1.45),
        (25.0 / 3.6, "Steam packet (25 km/h)", 12.0, 0.55),
        (200000.0, "Guided-wave fibre (200,000 km/s)", 85.0, 1.35),
        (299792.458, "Vacuum light bound c (299,792 km/s)", 240.0, 0.58),
    ]
    for v_kms, lbl, x_pos, mult in rays:
        l_ray = d_grid / v_kms
        ax.plot(d_grid, l_ray, color="#486581" if v_kms > 1000 else "#627d98", ls="--", lw=1.0, alpha=0.75, zorder=1)
        y_pos = (x_pos / v_kms) * mult
        ax.text(x_pos, y_pos, lbl, fontsize=7.5, color="#334e68", rotation=23.5, rotation_mode="anchor")

    # Shade forbidden superluminal zone
    ax.fill_between(d_grid, 1e-6, d_grid / 299792.458, color="#d9e2ec", alpha=0.65, zorder=0)

    # Reference vertical line at 1,000 km
    ax.axvline(1000, color="#b83227", ls=":", lw=1.3, zorder=2)
    ax.text(1050, 1.6e-3, "Reference slice: d = 1,000 km", fontsize=7.8, color="#b83227", fontweight="bold")

    for lbl, dist, lat, corr, (dx, dy) in POINTS:
        c = COLORS[corr]
        ax.scatter(dist, lat, color=c, s=48, edgecolor="white", lw=0.8, zorder=5)
        ax.annotate(lbl, (dist, lat), xytext=(dx, dy), textcoords="offset points", fontsize=7.6, color="#102a43")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 20000)
    ax.set_ylim(1e-3, 1e7)
    ax.set_xlabel("Corridor Distance d (km, Log Scale)")
    ax.set_ylabel("Observed First-Signal Latency L (Log Scale)")
    ax.set_yticks([1e-3, 1.0, 60.0, 3600.0, 86400.0, 1e7])
    ax.set_yticklabels(["1.0 ms", "1.0 s", "1.0 min", "1.0 h", "1.0 day", "115.7 days"])
    ax.grid(True, which="major", ls="-", lw=0.5, color="#d9e2ec")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    handles = [
        mlines.Line2D([], [], color="#1b4965", marker="o", ls="None", ms=6.5, label="London–New York Corridor"),
        mlines.Line2D([], [], color="#b83227", marker="o", ls="None", ms=6.5, label="Antwerp–Venice Corridor"),
        mlines.Line2D([], [], color="#8c6d1f", marker="o", ls="None", ms=6.5, label="Ancient & Tang Anchors"),
    ]
    ax.legend(handles=handles, loc="upper left", frameon=True, facecolor="white", edgecolor="#bcccdc", fontsize=8)

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated:", OUT_PDF)

if __name__ == "__main__":
    build_gvk_dist()
