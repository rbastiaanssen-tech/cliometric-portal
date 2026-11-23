#!/usr/bin/env python3
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

OUT_PDF = Path("manuscript/figure3_gvk_bandwidth_latency.pdf")
OUT_PNG = Path("manuscript/figure3_gvk_bandwidth_latency.png")

POINTS = [
    ("1895 BC · Assur–Kültepe", 0.00198, 2.419e6, "Ancient", (7, 3)),
    ("301 AD · Rome", 0.00694, 1.304e6, "Ancient", (-38, -11)),
    ("750 AD · Chang'an", 0.00556, 3.840e5, "Ancient", (-45, -11)),
    ("1395 · Datini", 0.01389, 1.202e6, "Antwerp-Venice", (7, 4)),
    ("1635 · Thurn & Taxis", 0.01852, 9.016e5, "Antwerp-Venice", (7, -7)),
    ("1825 · Sailing packet", 0.00823, 4.188e5, "London-New York", (-72, 4)),
    ("1855 · Steam packet", 0.01821, 1.892e5, "London-New York", (-72, -10)),
    ("1866 · Atlantic cable (17 wpm)", 1.417, 0.2154, "London-New York", (8, 3)),
    ("1872 · Alpine telegraph", 2.50, 0.0435, "Antwerp-Venice", (8, 4)),
    ("1935 · Telephone", 1200.0, 0.0130, "Antwerp-Venice", (8, 4)),
    ("1956 · TAT-1", 4800.0, 0.00628, "London-New York", (8, 5)),
    ("2026 · EU Fibre", 1e13, 0.0050, "Antwerp-Venice", (-56, 7)),
    ("2026 · Atlantic Fibre", 1e14, 0.0050, "London-New York", (-65, -12)),
]

COLORS = {"London-New York": "#1b4965", "Antwerp-Venice": "#b83227", "Ancient": "#8c6d1f"}

def build_gvk_bw():
    plt.rcParams.update({"font.family": "serif", "font.size": 8.8, "axes.labelsize": 9.5, "axes.titlesize": 10})
    fig, ax = plt.subplots(figsize=(9.5, 5.4))

    b_grid = np.logspace(-6, 15, 600)
    # Iso-delivery contours for 1 MB payload (M = 8e6 bits): T = L_1000 + M / B -> L_1000 = T - M / B
    M_1MB = 8.0e6
    contours = [
        (86400.0, "T = 1 day (1 MB)", 3e12),
        (3600.0, "T = 1 hour", 3e12),
        (60.0, "T = 1 min", 3e12),
        (1.0, "T = 1 s", 3e12),
    ]
    for T_sec, lbl, x_lbl in contours:
        b_valid = b_grid[b_grid > (M_1MB / T_sec) * 1.002]
        l_curve = T_sec - (M_1MB / b_valid)
        ax.plot(b_valid, l_curve, color="#829ab1", ls="--", lw=0.95, zorder=1)
        ax.text(x_lbl, T_sec * 1.28, lbl, fontsize=7.4, color="#486581")

    # Physical lower bounds at 1,000 km
    ax.axhline(0.005, color="#b83227", ls=":", lw=1.2, zorder=2)
    ax.text(2e-6, 0.0065, "Guided-wave silica floor (5.0 ms / 1,000 km)", fontsize=7.5, color="#b83227", fontweight="bold")
    ax.axhline(0.00333, color="#102a43", ls="--", lw=1.1, zorder=2)
    ax.text(2e-6, 0.0017, "Vacuum speed-of-light bound (3.33 ms / 1,000 km)", fontsize=7.5, color="#102a43")
    ax.fill_between([1e-6, 1e15], 1e-3, 0.00333, color="#d9e2ec", alpha=0.75, zorder=0)

    # Trajectory arrows for London-New York & Antwerp-Venice
    atl_pts = [p for p in POINTS if p[3] == "London-New York"]
    eu_pts = [p for p in POINTS if p[3] == "Antwerp-Venice"]
    for seq, c in [(atl_pts, "#1b4965"), (eu_pts, "#b83227")]:
        ax.plot([p[1] for p in seq], [p[2] for p in seq], color=c, lw=1.5, alpha=0.8, zorder=3)

    for lbl, bps, l1000, corr, (dx, dy) in POINTS:
        c = COLORS[corr]
        is_1866 = "1866" in lbl
        ax.scatter(bps, l1000, facecolor="white" if is_1866 else c, edgecolor=c, s=72 if is_1866 else 44, lw=1.8 if is_1866 else 0.8, zorder=5)
        ax.annotate(lbl, (bps, l1000), xytext=(dx, dy), textcoords="offset points", fontsize=7.5,
                    fontweight="bold" if is_1866 else "normal", color="#102a43")

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-6, 1e15)
    ax.set_ylim(1e-3, 1e7)
    ax.set_xlabel("Channel Sending Rate B (Bits per Second, Log Scale)")
    ax.set_ylabel("Distance-Normalized Latency L (per 1,000 km, Log Scale)")
    ax.set_xticks([1e-6, 1e-3, 1, 1e3, 1e6, 1e9, 1e12, 1e15])
    ax.set_yticks([1e-3, 1.0, 60.0, 3600.0, 86400.0, 1e7])
    ax.set_yticklabels(["1.0 ms", "1.0 s", "1.0 min", "1.0 h", "1.0 day", "115.7 days"])
    ax.grid(True, which="major", ls="-", lw=0.5, color="#d9e2ec")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    handles = [
        mlines.Line2D([], [], color="#1b4965", lw=1.6, marker="o", ms=6, label="London–New York Trajectory"),
        mlines.Line2D([], [], color="#b83227", lw=1.6, marker="o", ms=6, label="Antwerp–Venice Trajectory"),
        mlines.Line2D([], [], color="#8c6d1f", marker="o", ls="None", ms=6, label="Ancient & Tang Anchors"),
        mlines.Line2D([], [], color="#829ab1", ls="--", lw=1.0, label="Iso-Delivery Contours T(1 MB) = L + M/B"),
    ]
    ax.legend(handles=handles, loc="lower left", bbox_to_anchor=(0.01, 0.14), frameon=True, facecolor="white", edgecolor="#bcccdc", fontsize=7.6)

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated:", OUT_PDF)

if __name__ == "__main__":
    build_gvk_bw()
