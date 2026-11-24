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
    ("1895 BC · Assur-Kultepe", 0.00198, 2.419e6, "Ancient", 10, 4, "left"),
    ("301 AD · Rome", 0.00694, 1.304e6, "Ancient", -10, 4, "right"),
    ("1395 · Datini", 0.01389, 1.202e6, "Antwerp-Venice", 10, 3, "left"),
    ("1635 · Thurn & Taxis", 0.01852, 9.016e5, "Antwerp-Venice", 10, -4, "left"),
    ("1825 · Sailing packet", 0.00823, 4.188e5, "London-New York", -10, 2, "right"),
    ("750 AD · Chang'an", 0.00556, 3.840e5, "Ancient", -10, -7, "right"),
    ("1855 · Steam packet", 0.01821, 1.892e5, "London-New York", 10, -6, "left"),
    ("1866 · Atlantic cable (1.42 bps)", 1.417, 0.2154, "London-New York", 10, 4, "left"),
    ("1872 · Alpine telegraph", 2.50, 0.0435, "Antwerp-Venice", 10, -3, "left"),
    ("1935 · Telephone", 1200.0, 0.0130, "Antwerp-Venice", 10, 7, "left"),
    ("1956 · TAT-1", 4800.0, 0.00628, "London-New York", -10, -7, "right"),
    ("1965 · Intelsat I (240 ch)", 1.152e6, 0.04488, "London-New York", 10, 6, "left"),
    ("1988 · TAT-8 (280 Mbps)", 2.80e8, 0.0050, "London-New York", 0, -13, "center"),
    ("2026 · EU fibre", 1e13, 0.0050, "Antwerp-Venice", -8, 9, "right"),
    ("2026 · Atlantic fibre", 1e14, 0.0050, "London-New York", -8, -11, "right"),
]

COLORS = {"London-New York": "#0F3D5E", "Antwerp-Venice": "#C8372D", "Ancient": "#B47B14"}

def build_gvk_bw():
    plt.rcParams.update({"font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"], "font.family": "sans-serif"})
    fig = plt.figure(figsize=(7.4, 4.8))
    fig.patch.set_facecolor("white")

    fig.lines.append(plt.Line2D([0.02, 0.98], [0.985, 0.985], transform=fig.transFigure, color="#C8372D", lw=2.2))
    fig.text(0.02, 0.935, "The 1866 cable broke the latency barrier—but left bandwidth bottlenecked", fontsize=10.4, fontweight="bold", color="#101828")
    fig.text(0.02, 0.896, "Channel sending rate (bits/sec) vs. latency per 1,000 km, with total 1 MB delivery contours", fontsize=8.1, color="#475467")

    handles = [
        mlines.Line2D([], [], color="#0F3D5E", lw=1.6, marker="o", ms=5.5, label="London-New York"),
        mlines.Line2D([], [], color="#C8372D", lw=1.6, marker="o", ms=5.5, label="Antwerp-Venice"),
        mlines.Line2D([], [], color="#B47B14", marker="o", ls="None", ms=5.5, label="Ancient & Tang"),
        mlines.Line2D([], [], color="#64748B", ls="--", lw=0.95, label="Total time T to send 1 MB (T = L + M/B)"),
    ]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.012, 0.88), ncol=4, frameon=False, fontsize=7.3)

    ax = fig.add_axes([0.11, 0.12, 0.86, 0.67])
    b_grid = np.logspace(-6, 15, 600)
    M_1MB = 8.0e6
    for T_sec, lbl in [(86400.0, "1 day (1 MB)"), (3600.0, "1 hour"), (60.0, "1 min"), (1.0, "1 sec")]:
        b_valid = b_grid[b_grid > (M_1MB / T_sec) * 1.002]
        ax.plot(b_valid, T_sec - (M_1MB / b_valid), color="#94A3B8", ls="--", lw=0.9, zorder=1)
        ax.text(6.5e14, T_sec * 1.28, lbl, ha="right", fontsize=6.6, color="#475467")

    ax.text(
        1.4e7, 2.2e5,
        "How to read the dashed curves:\n"
        "Total delivery time T = L + M/B for 1 MB.\n"
        "- Vertical knee: bandwidth limit (B)\n"
        "- Horizontal shelf: latency limit (L)",
        fontsize=6.6, color="#334155",
        bbox=dict(boxstyle="round,pad=0.35", fc="#F8FAFC", ec="#CBD5E1", lw=0.7),
        zorder=7
    )

    ax.axhline(0.005, color="#C8372D", ls=":", lw=1.1, zorder=2)
    ax.text(2e-6, 0.0072, "Silica guided-wave floor (5.0 ms / 1,000 km)", fontsize=6.8, color="#C8372D", fontweight="bold")
    ax.axhline(0.00333, color="#1E293B", ls="--", lw=0.95, zorder=2)
    ax.text(2e-6, 0.0017, "Vacuum speed of light c (3.33 ms / 1,000 km)", fontsize=6.8, color="#334155")
    ax.fill_between([1e-6, 1e15], 4e-4, 0.00333, color="#E2E8F0", alpha=0.8, zorder=0)

    for corr, c in [("London-New York", "#0F3D5E"), ("Antwerp-Venice", "#C8372D")]:
        seq = [p for p in POINTS if p[3] == corr]
        ax.plot([p[1] for p in seq], [p[2] for p in seq], color=c, lw=1.5, alpha=0.85, zorder=3)

    for lbl, bps, l1000, corr, dx, dy, ha in POINTS:
        c = COLORS[corr]
        is_1866 = "1866" in lbl
        ax.scatter(bps, l1000, facecolor="white" if is_1866 else c, edgecolor=c, s=62 if is_1866 else 38, lw=1.8 if is_1866 else 0.75, zorder=5)
        ax.annotate(lbl, (bps, l1000), xytext=(dx, dy), textcoords="offset points", ha=ha, va="center",
                    fontsize=6.5, fontweight="bold" if is_1866 else "normal", color="#101828",
                    arrowprops=dict(arrowstyle="-", color="#94A3B8", lw=0.55, shrinkA=0, shrinkB=2),
                    bbox=dict(boxstyle="round,pad=0.05", fc="white", ec="none", alpha=0.9), zorder=6)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-6, 1e15)
    ax.set_ylim(5e-4, 2.5e7)
    ax.set_xlabel("Channel sending rate (bits per second, log scale)", fontsize=8.4, color="#1E293B")
    ax.set_ylabel("Latency per 1,000 km (log scale)", fontsize=8.4, color="#1E293B")
    ax.set_xticks([1e-6, 1e-3, 1, 1e3, 1e6, 1e9, 1e12, 1e15])
    ax.set_yticks([1e-3, 1.0, 60.0, 3600.0, 86400.0, 1e7])
    ax.set_yticklabels(["1 ms", "1 sec", "1 min", "1 hour", "1 day", "116 days"], fontsize=7.6)
    ax.tick_params(axis="x", labelsize=7.6)
    ax.grid(True, which="major", axis="y", ls="-", lw=0.55, color="#E2E8F0")
    for sp in ["top", "right", "left"]: ax.spines[sp].set_visible(False)
    ax.tick_params(axis="y", length=0)

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated clean Figure 3:", OUT_PDF)

if __name__ == "__main__":
    build_gvk_bw()
