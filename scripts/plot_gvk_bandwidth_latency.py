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
    ("1895 BC · Assur–Kültepe", 0.00198, 2.419e6, "Ancient", (8, 3)),
    ("301 AD · Rome", 0.00694, 1.304e6, "Ancient", (-56, 2)),
    ("1395 · Datini", 0.01389, 1.202e6, "Antwerp-Venice", (8, 4)),
    ("1635 · Thurn & Taxis", 0.01852, 9.016e5, "Antwerp-Venice", (9, -3)),
    ("1825 · Sailing packet", 0.00823, 4.188e5, "London-New York", (-78, -2)),
    ("750 AD · Chang'an", 0.00556, 3.840e5, "Ancient", (-68, -9)),
    ("1855 · Steam packet", 0.01821, 1.892e5, "London-New York", (-76, -9)),
    ("1866 · Atlantic cable (1.42 bps)", 1.417, 0.2154, "London-New York", (9, 4)),
    ("1872 · Alpine telegraph", 2.50, 0.0435, "Antwerp-Venice", (9, 5)),
    ("1935 · Telephone", 1200.0, 0.0130, "Antwerp-Venice", (8, 6)),
    ("1956 · TAT-1", 4800.0, 0.00628, "London-New York", (8, 6)),
    ("2026 · EU fibre", 1e13, 0.0050, "Antwerp-Venice", (-56, 8)),
    ("2026 · Atlantic fibre", 1e14, 0.0050, "London-New York", (-68, -12)),
]

COLORS = {"London-New York": "#0F3D5E", "Antwerp-Venice": "#C8372D", "Ancient": "#B47B14"}

def build_gvk_bw():
    plt.rcParams.update({"font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"], "font.family": "sans-serif"})
    fig = plt.figure(figsize=(7.4, 4.7))
    fig.patch.set_facecolor("white")

    fig.lines.append(plt.Line2D([0.02, 0.98], [0.985, 0.985], transform=fig.transFigure, color="#C8372D", lw=2.2))
    fig.text(0.02, 0.935, "The 1866 cable broke the latency barrier—but left bandwidth bottlenecked", fontsize=10.5, fontweight="bold", color="#101828")
    fig.text(0.02, 0.895, "Channel sending rate (bits/sec) vs. latency per 1,000 km, with 1 MB iso-delivery curves", fontsize=8.2, color="#475467")

    handles = [
        mlines.Line2D([], [], color="#0F3D5E", lw=1.6, marker="o", ms=5.5, label="London–New York"),
        mlines.Line2D([], [], color="#C8372D", lw=1.6, marker="o", ms=5.5, label="Antwerp–Venice"),
        mlines.Line2D([], [], color="#B47B14", marker="o", ls="None", ms=5.5, label="Ancient & Tang"),
        mlines.Line2D([], [], color="#64748B", ls="--", lw=0.95, label="1 MB delivery contours"),
    ]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.012, 0.88), ncol=4, frameon=False, fontsize=7.5)

    ax = fig.add_axes([0.11, 0.12, 0.85, 0.67])
    b_grid = np.logspace(-6, 15, 600)
    M_1MB = 8.0e6
    for T_sec, lbl in [(86400.0, "1 day"), (3600.0, "1 hour"), (60.0, "1 min"), (1.0, "1 sec")]:
        b_valid = b_grid[b_grid > (M_1MB / T_sec) * 1.002]
        ax.plot(b_valid, T_sec - (M_1MB / b_valid), color="#94A3B8", ls="--", lw=0.9, zorder=1)
        ax.text(4.5e14, T_sec * 1.25, lbl, ha="right", fontsize=6.9, color="#475467")

    ax.axhline(0.005, color="#C8372D", ls=":", lw=1.1, zorder=2)
    ax.text(2e-6, 0.0068, "Silica guided-wave floor (5.0 ms / 1,000 km)", fontsize=6.9, color="#C8372D", fontweight="bold")
    ax.axhline(0.00333, color="#1E293B", ls="--", lw=0.95, zorder=2)
    ax.text(2e-6, 0.0015, "Vacuum speed of light c (3.33 ms / 1,000 km)", fontsize=6.9, color="#334155")
    ax.fill_between([1e-6, 1e15], 1e-3, 0.00333, color="#E2E8F0", alpha=0.8, zorder=0)

    for corr, c in [("London-New York", "#0F3D5E"), ("Antwerp-Venice", "#C8372D")]:
        seq = [p for p in POINTS if p[3] == corr]
        ax.plot([p[1] for p in seq], [p[2] for p in seq], color=c, lw=1.5, alpha=0.85, zorder=3)

    for lbl, bps, l1000, corr, (dx, dy) in POINTS:
        c = COLORS[corr]
        is_1866 = "1866" in lbl
        ax.scatter(bps, l1000, facecolor="white" if is_1866 else c, edgecolor=c, s=64 if is_1866 else 38, lw=1.8 if is_1866 else 0.75, zorder=5)
        ax.annotate(lbl, (bps, l1000), xytext=(dx, dy), textcoords="offset points", fontsize=6.8,
                    fontweight="bold" if is_1866 else "normal", color="#101828",
                    arrowprops=dict(arrowstyle="-", color="#94A3B8", lw=0.55, shrinkA=0, shrinkB=2),
                    bbox=dict(boxstyle="round,pad=0.07", fc="white", ec="none", alpha=0.85), zorder=6)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-6, 1e15)
    ax.set_ylim(1e-3, 1.5e7)
    ax.set_xlabel("Channel sending rate (bits per second, log scale)", fontsize=8.5, color="#1E293B")
    ax.set_ylabel("Latency per 1,000 km (log scale)", fontsize=8.5, color="#1E293B")
    ax.set_xticks([1e-6, 1e-3, 1, 1e3, 1e6, 1e9, 1e12, 1e15])
    ax.set_yticks([1e-3, 1.0, 60.0, 3600.0, 86400.0, 1e7])
    ax.set_yticklabels(["1 ms", "1 sec", "1 min", "1 hour", "1 day", "116 days"], fontsize=7.8)
    ax.tick_params(axis="x", labelsize=7.8)
    ax.grid(True, which="major", axis="y", ls="-", lw=0.55, color="#E2E8F0")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated:", OUT_PDF)

if __name__ == "__main__":
    build_gvk_bw()
