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
    ("301 AD · Rome-Brundisium", 530, 6.912e5, "Ancient", -10, -2, "right"),
    ("1895 BC · Assur-Kultepe", 1000, 2.419e6, "Ancient", -10, 7, "right"),
    ("1395 · Antwerp-Venice", 1150, 1.382e6, "Antwerp-Venice", 10, 6, "left"),
    ("1635 · Antwerp-Venice", 1150, 1.037e6, "Antwerp-Venice", 10, -5, "left"),
    ("750 AD · Chang'an-Guangzhou", 2250, 8.640e5, "Ancient", 0, -15, "center"),
    ("1825 · Sailing packet", 5570, 2.333e6, "London-New York", 9, 5, "left"),
    ("1855 · Steam packet", 5570, 1.054e6, "London-New York", 9, -5, "left"),
    ("1866 · Atlantic cable", 5570, 1.20, "London-New York", 9, 2, "left"),
    ("1965 · Intelsat I (250 ms)", 5570, 0.250, "London-New York", -10, 7, "right"),
    ("1872 · Alpine telegraph", 1150, 0.050, "Antwerp-Venice", -10, 8, "right"),
    ("1956 · TAT-1 coaxial", 5570, 0.035, "London-New York", 9, 6, "left"),
    ("1988 · TAT-8 & 2026 fibre", 5570, 0.02785, "London-New York", 9, -7, "left"),
    ("1935 · Telephone", 1150, 0.015, "Antwerp-Venice", -10, 0, "right"),
    ("2026 · EU fibre", 1150, 0.00575, "Antwerp-Venice", -10, -8, "right"),
]

COLORS = {"London-New York": "#0F3D5E", "Antwerp-Venice": "#C8372D", "Ancient": "#B47B14"}

def build_gvk_dist():
    plt.rcParams.update({"font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"], "font.family": "sans-serif"})
    fig = plt.figure(figsize=(7.4, 4.6))
    fig.patch.set_facecolor("white")

    fig.lines.append(plt.Line2D([0.02, 0.98], [0.985, 0.985], transform=fig.transFigure, color="#C8372D", lw=2.2))
    fig.text(0.02, 0.935, "Eight orders of magnitude separate physical transport from electromagnetic signals", fontsize=10.4, fontweight="bold", color="#101828")
    fig.text(0.02, 0.896, "Corridor distance (km) vs. observed first-signal latency, log scales", fontsize=8.2, color="#475467")

    handles = [
        mlines.Line2D([], [], color="#0F3D5E", marker="o", ls="None", ms=6, label="London-New York"),
        mlines.Line2D([], [], color="#C8372D", marker="o", ls="None", ms=6, label="Antwerp-Venice"),
        mlines.Line2D([], [], color="#B47B14", marker="o", ls="None", ms=6, label="Ancient & Tang anchors"),
    ]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.012, 0.88), ncol=3, frameon=False, fontsize=7.8)

    ax = fig.add_axes([0.11, 0.12, 0.86, 0.67])
    d_grid = np.logspace(0, 4.7, 300)

    rays = [
        (2.0 / 3.6, "Caravan (2 km/h)", 1.5, 1.55),
        (25.0 / 3.6, "Steam packet (25 km/h)", 8.0, 0.46),
        (200000.0, "Silica fibre (200,000 km/s)", 14.0, 1.65),
        (299792.458, "Speed of light c (299,792 km/s)", 38.0, 0.44),
    ]
    for v_kms, lbl, x_pos, mult in rays:
        ax.plot(d_grid, d_grid / v_kms, color="#64748B", ls="--", lw=0.9, alpha=0.75, zorder=1)
        ax.text(x_pos, (x_pos / v_kms) * mult, lbl, fontsize=6.8, color="#475467", rotation=20.0, rotation_mode="anchor")

    ax.axhline(0.250, color="#0F3D5E", ls=":", lw=0.95, alpha=0.75, zorder=2)
    ax.text(1.3, 0.34, "Geostationary satellite latency ceiling (250 ms)", fontsize=6.6, color="#0F3D5E")

    ax.fill_between(d_grid, 5e-4, d_grid / 299792.458, color="#E2E8F0", alpha=0.75, zorder=0)
    ax.text(1.3, 1.1e-3, "Physically unreachable (faster than light)", fontsize=6.6, color="#64748B", style="italic")

    ax.axvline(1000, color="#C8372D", ls=":", lw=1.1, zorder=2)
    ax.text(920, 45.0, "1,000 km slice", ha="right", fontsize=6.9, color="#C8372D", fontweight="bold")

    for lbl, dist, lat, corr, dx, dy, ha in POINTS:
        c = COLORS[corr]
        ax.scatter(dist, lat, color=c, s=40, edgecolor="white", lw=0.75, zorder=5)
        ax.annotate(lbl, (dist, lat), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center",
                    fontsize=6.6, color="#101828",
                    arrowprops=dict(arrowstyle="-", color="#94A3B8", lw=0.55, shrinkA=0, shrinkB=2),
                    bbox=dict(boxstyle="round,pad=0.05", fc="white", ec="none", alpha=0.9), zorder=6)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1, 55000)
    ax.set_ylim(6e-4, 2.5e7)
    ax.set_xlabel("Corridor distance (km, log scale)", fontsize=8.4, color="#1E293B")
    ax.set_ylabel("First-signal latency (log scale)", fontsize=8.4, color="#1E293B")
    ax.set_yticks([1e-3, 1.0, 60.0, 3600.0, 86400.0, 1e7])
    ax.set_yticklabels(["1 ms", "1 sec", "1 min", "1 hour", "1 day", "116 days"], fontsize=7.6)
    ax.tick_params(axis="x", labelsize=7.6)
    ax.grid(True, which="major", axis="y", ls="-", lw=0.55, color="#E2E8F0")
    for sp in ["top", "right", "left"]: ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated clean Figure 2:", OUT_PDF)

if __name__ == "__main__":
    build_gvk_dist()
