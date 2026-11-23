#!/usr/bin/env python3
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

CSV_PATH = Path("public/data/master_benchmarks.csv")
OUT_PDF = Path("manuscript/figure4_macro_spine.pdf")
OUT_PNG = Path("manuscript/figure4_macro_spine.png")

COLORS = {"London-New York": "#0F3D5E", "Antwerp-Venice": "#C8372D", "Rome-Brundisium": "#B47B14"}
MARKERS = {"door_to_door": "o", "terminal_to_terminal": "s", "wire_signaling_only": "D"}

def load_records():
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["year"] = int(r["era_year"])
            r["transit"] = float(r["transit_hours"]) if r["transit_hours"].strip() else None
            r["d_est"] = float(r["door_to_door_est_hours"]) if r["door_to_door_est_hours"].strip() else None
            r["cost"] = float(r["labor_hours_per_message"]) if r["labor_hours_per_message"].strip() else None
            rows.append(r)
    return sorted(rows, key=lambda x: x["year"])

def build_figure():
    rows = load_records()
    plt.rcParams.update({"font.sans-serif": ["Helvetica Neue", "Arial", "DejaVu Sans"], "font.family": "sans-serif"})
    fig = plt.figure(figsize=(7.4, 5.2))
    fig.patch.set_facecolor("white")

    fig.lines.append(plt.Line2D([0.02, 0.98], [0.985, 0.985], transform=fig.transFigure, color="#C8372D", lw=2.2))
    fig.text(0.02, 0.945, "Commercial posts cut costs 99%; the 1866 cable spiked them 169×", fontsize=10.5, fontweight="bold", color="#101828")
    fig.text(0.02, 0.910, "Real communication cost (labor-hours/message) and transit latency by corridor, 301 AD–2026 AD", fontsize=8.1, color="#475467")

    handles = [
        mlines.Line2D([], [], color="#0F3D5E", lw=1.6, label="London–New York"),
        mlines.Line2D([], [], color="#C8372D", lw=1.6, label="Antwerp–Venice"),
        mlines.Line2D([], [], color="#B47B14", marker="P", ls="None", ms=6.5, label="Rome (301 AD, T3)"),
        mlines.Line2D([], [], color="#0F3D5E", marker="^", mfc="white", ls="None", ms=6.5, label="Sensitivity (-SENS)"),
        mlines.Line2D([], [], color="#475467", marker="o", ls="None", ms=5, label="Door-to-door (D)"),
        mlines.Line2D([], [], color="#475467", marker="s", ls="None", ms=5, label="Terminal (T)"),
        mlines.Line2D([], [], color="#475467", marker="D", ls="None", ms=4.8, label="Wire-only (W)"),
    ]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.012, 0.898), ncol=4, frameon=False, fontsize=7.1)

    gs = fig.add_gridspec(2, 2, left=0.11, right=0.97, top=0.79, bottom=0.09, width_ratios=[1.0, 2.5], wspace=0.06, hspace=0.22)
    axes = [[fig.add_subplot(gs[r, c]) for c in range(2)] for r in range(2)]

    for row_idx, (metric, ylabel, ylim) in enumerate([
        ("cost", "Real cost (labor-hours, log)", (3e-10, 5e3)),
        ("transit", "Transit latency (hours, log)", (2e-5, 5e3)),
    ]):
        ax_l, ax_r = axes[row_idx]
        ax_l.set_xlim(220, 1740)
        ax_r.set_xlim(1805, 2048)
        for ax in (ax_l, ax_r):
            ax.set_yscale("log")
            ax.set_ylim(*ylim)
            ax.grid(True, which="major", axis="y", ls="-", lw=0.5, color="#E2E8F0")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)
            ax.spines["left"].set_visible(False)
            ax.tick_params(axis="both", labelsize=7.5)
        ax_r.tick_params(axis="y", which="both", left=False, labelleft=False)
        ax_l.tick_params(axis="y", length=0)
        ax_l.set_ylabel(ylabel, fontsize=8.2, color="#1E293B")

        for corridor in ["London-New York", "Antwerp-Venice"]:
            c = COLORS[corridor]
            pts_l = [r for r in rows if r["corridor"] == corridor and r["specification_type"] == "baseline" and r[metric] is not None and r["year"] < 1800]
            pts_r = [r for r in rows if r["corridor"] == corridor and r["specification_type"] == "baseline" and r[metric] is not None and r["year"] >= 1800]
            if len(pts_l) > 1:
                ax_l.plot([p["year"] for p in pts_l], [p[metric] for p in pts_l], color=c, lw=1.6, zorder=3)
            if len(pts_r) > 1:
                ax_r.plot([p["year"] for p in pts_r], [p[metric] for p in pts_r], color=c, lw=1.6, zorder=3)
            for p in pts_l + pts_r:
                target = ax_l if p["year"] < 1800 else ax_r
                target.scatter(p["year"], p[metric], color=c, marker=MARKERS.get(p["transit_scope"], "o"), s=38, edgecolor="white", lw=0.7, zorder=4)
                if row_idx == 1 and p["transit_scope"] != "door_to_door" and p["d_est"] is not None:
                    target.plot([p["year"], p["year"]], [p[metric], p["d_est"]], color=c, ls=":", lw=1.0, zorder=2)
                    target.scatter(p["year"], p["d_est"], facecolor="white", edgecolor=c, marker="o", s=28, lw=1.0, zorder=3)

        for p in rows:
            if p[metric] is None:
                continue
            target = ax_l if p["year"] < 1800 else ax_r
            if p["corridor"] == "Rome-Brundisium" and p["specification_type"] == "baseline":
                target.scatter(p["year"], p[metric], color="#B47B14", marker="P", s=56, edgecolor="white", lw=0.7, zorder=5)
            elif p["specification_type"] == "sensitivity":
                c = COLORS.get(p["corridor"], "#0F3D5E")
                target.scatter(p["year"], p[metric], facecolor="white", edgecolor=c, marker="^", s=52, lw=1.3, zorder=6)

    axes[0][0].set_title("Pre-industrial (301–1635 AD)", loc="left", fontsize=8.0, fontweight="bold", color="#334155")
    axes[0][1].set_title("Industrial & telecommunications era (1825–2026 AD)", loc="left", fontsize=8.0, fontweight="bold", color="#334155")
    axes[1][0].set_xlabel("Year (AD)", fontsize=8.0)
    axes[1][1].set_xlabel("Year (AD)", fontsize=8.0)

    kw_ann = dict(fontsize=6.8, color="#101828", bbox=dict(boxstyle="round,pad=0.06", fc="white", ec="none", alpha=0.85))
    axes[0][0].annotate("301 AD: 288.0 LH", (301, 288.0), xytext=(390, 500), **kw_ann)
    axes[0][0].annotate("1395: 19.0 LH", (1395, 19.0), xytext=(880, 45), **kw_ann)
    axes[0][0].annotate("1635: 0.87 LH", (1635, 0.87), xytext=(940, 0.12), **kw_ann)
    axes[0][1].annotate("1825: 3.33 LH", (1825, 3.33), xytext=(1810, 22), **kw_ann)
    axes[0][1].annotate("1855: 1.82 LH", (1855, 1.82), xytext=(1825, 0.14), **kw_ann)
    axes[0][1].annotate("1866 Jul: 615.4 LH", (1866, 615.38), xytext=(1882, 950), **kw_ann)
    axes[0][1].annotate("1866 Nov: 307.7 LH", (1866, 307.69), xytext=(1882, 85), **kw_ann)
    axes[0][1].annotate("1956: 12.2 LH (TAT-1)", (1956, 12.20), xytext=(1932, 48), **kw_ann)
    axes[0][1].annotate("2026 EU: 1.30e-6 LH", (2026, 1.30e-6), xytext=(1942, 4e-5), **kw_ann)
    axes[0][1].annotate("2026 US: 3.89e-9 LH", (2026, 3.89e-9), xytext=(1942, 2e-9), **kw_ann)
    axes[1][1].annotate("1866: 2.25h (D) / 0.25h (T) / 0.02h (W)", (1866, 0.25), xytext=(1880, 0.04), **kw_ann)

    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated:", OUT_PDF)

if __name__ == "__main__":
    build_figure()
