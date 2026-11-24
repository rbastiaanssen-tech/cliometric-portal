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
    fig = plt.figure(figsize=(7.4, 5.4))
    fig.patch.set_facecolor("white")

    fig.lines.append(plt.Line2D([0.02, 0.98], [0.985, 0.985], transform=fig.transFigure, color="#C8372D", lw=2.2))
    fig.text(0.02, 0.945, "Commercial posts cut costs by two orders of magnitude; the 1866 cable spiked them 169x", fontsize=10.0, fontweight="bold", color="#101828")
    fig.text(0.02, 0.910, "Real communication cost (labor-hours/message) and transit latency by corridor, 301 AD-2026 AD", fontsize=8.0, color="#475467")

    handles = [
        mlines.Line2D([], [], color="#0F3D5E", lw=1.6, label="London-New York"),
        mlines.Line2D([], [], color="#C8372D", lw=1.6, label="Antwerp-Venice"),
        mlines.Line2D([], [], color="#0F3D5E", ls="--", lw=1.1, marker="o", mfc="white", ms=4.5, label="Estimated door-to-door (D)"),
        mlines.Line2D([], [], color="#15803D", marker="d", ls="None", ms=6.0, label="2026 Retail broadband (T1)"),
        mlines.Line2D([], [], color="#B47B14", marker="P", ls="None", ms=6.0, label="Rome faber proxy (301 AD)"),
        mlines.Line2D([], [], color="#475467", marker="^", mfc="white", ls="None", ms=5.5, label="Sensitivity (-SENS)"),
        mlines.Line2D([], [], color="#475467", marker="s", ls="None", ms=4.6, label="Terminal (T)"),
        mlines.Line2D([], [], color="#475467", marker="D", ls="None", ms=4.4, label="Wire-only (W)"),
    ]
    fig.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.01, 0.898), ncol=4, frameon=False, fontsize=6.8)

    gs = fig.add_gridspec(2, 2, left=0.11, right=0.97, top=0.78, bottom=0.09, width_ratios=[1.0, 2.6], wspace=0.06, hspace=0.22)
    axes = [[fig.add_subplot(gs[r, c]) for c in range(2)] for r in range(2)]

    for row_idx, (metric, ylabel, ylim) in enumerate([("cost", "Real cost (LH, log)", (3e-10, 5e3)), ("transit", "Transit latency (h, log)", (2e-5, 5e3))]):
        ax_l, ax_r = axes[row_idx]
        ax_l.set_xlim(220, 1740)
        ax_r.set_xlim(1805, 2052)
        for ax in (ax_l, ax_r):
            ax.set_yscale("log")
            ax.set_ylim(*ylim)
            ax.grid(True, which="major", axis="y", ls="-", lw=0.5, color="#E2E8F0")
            for spine in ["top", "right", "left"]: ax.spines[spine].set_visible(False)
            ax.tick_params(axis="both", labelsize=7.4)
        ax_r.tick_params(axis="y", which="both", left=False, labelleft=False)
        ax_l.tick_params(axis="y", length=0)
        ax_l.set_ylabel(ylabel, fontsize=8.1, color="#1E293B")

        for corridor in ["London-New York", "Antwerp-Venice"]:
            c = COLORS[corridor]
            pts_l = [r for r in rows if r["corridor"] == corridor and r["specification_type"] == "baseline" and r[metric] is not None and r["year"] < 1800]
            pts_r = [r for r in rows if r["corridor"] == corridor and r["specification_type"] == "baseline" and r[metric] is not None and r["year"] >= 1800]
            if len(pts_l) > 1: ax_l.plot([p["year"] for p in pts_l], [p[metric] for p in pts_l], color=c, lw=1.6, zorder=3)
            if len(pts_r) > 1: ax_r.plot([p["year"] for p in pts_r], [p[metric] for p in pts_r], color=c, lw=1.6, zorder=3)
            for p in pts_l + pts_r:
                target = ax_l if p["year"] < 1800 else ax_r
                target.scatter(p["year"], p[metric], color=c, marker=MARKERS.get(p["transit_scope"], "o"), s=36, edgecolor="white", lw=0.7, zorder=4)

        if row_idx == 1:
            d_pts = [r for r in rows if r["corridor"] == "London-New York" and r["specification_type"] == "baseline" and r["d_est"] is not None]
            ax_r.plot([p["year"] for p in d_pts], [p["d_est"] for p in d_pts], color="#0F3D5E", ls="--", lw=1.2, zorder=3)
            for p in d_pts:
                if p["transit_scope"] != "door_to_door":
                    ax_r.scatter(p["year"], p["d_est"], facecolor="white", edgecolor="#0F3D5E", marker="o", s=30, lw=1.1, zorder=5)

        if row_idx == 0:
            ax_r.scatter(2026, 1.35, color="#15803D", marker="d", s=44, edgecolor="white", lw=0.7, zorder=6)
            ax_r.scatter(2026, 1.61e-5, facecolor="white", edgecolor="#15803D", marker="d", s=40, lw=1.2, zorder=6)
            ax_r.plot([2026, 2026], [1.61e-5, 1.35], color="#15803D", ls=":", lw=1.0, zorder=5)

        for p in rows:
            if p[metric] is None: continue
            target = ax_l if p["year"] < 1800 else ax_r
            if p["corridor"] == "Rome-Brundisium" and p["specification_type"] == "baseline":
                target.scatter(p["year"], p[metric], color="#B47B14", marker="P", s=54, edgecolor="white", lw=0.7, zorder=5)
            elif p["specification_type"] == "sensitivity" and p["id"] != "M/C-T-7-SENS":
                c = COLORS.get(p["corridor"], "#0F3D5E")
                target.scatter(p["year"], p[metric], facecolor="white", edgecolor=c, marker="^", s=46, lw=1.3, zorder=6)

    axes[0][0].set_title("Pre-industrial (301-1635 AD)", loc="left", fontsize=7.9, fontweight="bold", color="#334155")
    axes[0][1].set_title("Industrial & optical era (1825-2026 AD)", loc="left", fontsize=7.9, fontweight="bold", color="#334155")
    axes[1][0].set_xlabel("Year (AD)", fontsize=7.9)
    axes[1][1].set_xlabel("Year (AD)", fontsize=7.9)

    kw = dict(fontsize=6.4, color="#101828", bbox=dict(boxstyle="round,pad=0.05", fc="white", ec="none", alpha=0.88))
    axes[0][0].annotate("301 AD: 144.0 (k=1)", (301, 144.0), xytext=(370, 260), **kw)
    axes[0][0].annotate("k=10: 14.4", (301, 14.4), xytext=(370, 8.0), **kw)
    axes[0][0].annotate("1395: 19.0", (1395, 19.0), xytext=(950, 55), **kw)
    axes[0][0].annotate("1635: 0.87", (1635, 0.87), xytext=(1050, 0.14), **kw)
    axes[0][1].annotate("1825: 3.33", (1825, 3.33), xytext=(1810, 14), **kw)
    axes[0][1].annotate("1855: 1.82", (1855, 1.82), xytext=(1822, 0.15), **kw)
    axes[0][1].annotate("1866 Nov: 307.7", (1866, 307.69), xytext=(1874, 850), **kw)
    axes[0][1].annotate("1872 EU: 18.57", (1872, 18.57), xytext=(1876, 36), **kw)
    axes[0][1].annotate("1935 EU: 4.80", (1935, 4.80), xytext=(1915, 1.1), **kw)
    axes[0][1].annotate("1956 TAT-1: 12.2", (1956, 12.20), xytext=(1922, 65), **kw)
    axes[0][1].annotate("1965 Intelsat: 4.62", (1965, 4.62), xytext=(1968, 8.5), **kw)
    axes[0][1].annotate("1988 TAT-8: 0.31", (1988, 0.31), xytext=(1968, 0.045), **kw)
    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated Figure 4:", OUT_PDF)

if __name__ == "__main__": build_figure()
