#!/usr/bin/env python3
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

CSV_PATH = Path("public/data/master_benchmarks.csv")
OUT_PDF = Path("manuscript/figure1_macro_spine.pdf")
OUT_PNG = Path("manuscript/figure1_macro_spine.png")

CORRIDOR_STYLE = {
    "London-New York": {"color": "#1b4965", "label": "London-New York"},
    "Antwerp-Venice": {"color": "#c8553d", "label": "Antwerp-Venice"},
    "Rome-Brundisium": {"color": "#8c6d1f", "label": "Rome-Brundisium (301 AD)"},
}

SCOPE_MARKERS = {
    "door_to_door": "o",
    "terminal_to_terminal": "s",
    "wire_signaling_only": "D",
}

def load_records():
    rows = []
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            r["year"] = int(r["era_year"])
            r["transit"] = float(r["transit_hours"]) if r["transit_hours"].strip() else None
            r["cost"] = float(r["labor_hours_per_message"]) if r["labor_hours_per_message"].strip() else None
            rows.append(r)
    return sorted(rows, key=lambda x: x["year"])

def draw_break_marks(ax_left, ax_right):
    d = 0.015
    kw = dict(transform=ax_left.transAxes, color="#444444", clip_on=False, lw=1.0)
    ax_left.plot((1 - d, 1 + d), (-d, +d), **kw)
    ax_left.plot((1 - d, 1 + d), (1 - d, 1 + d), **kw)
    kw["transform"] = ax_right.transAxes
    ax_right.plot((-d, +d), (-d, +d), **kw)
    ax_right.plot((-d, +d), (1 - d, 1 + d), **kw)

def build_figure():
    rows = load_records()
    plt.rcParams.update({"font.family": "serif", "font.size": 9, "axes.labelsize": 9.5, "axes.titlesize": 10})
    fig, axes = plt.subplots(2, 2, figsize=(10.5, 6.4), sharey="row", gridspec_kw={"width_ratios": [1.0, 2.35], "wspace": 0.05, "hspace": 0.24})

    for row_idx, (metric, ylabel, ylim) in enumerate([
        ("cost", "Real Cost (Labor-Hours / Message, Log)", (2e-7, 3e3)),
        ("transit", "Transit Latency (Hours, Log)", (3e-5, 3e3)),
    ]):
        ax_l, ax_r = axes[row_idx]
        ax_l.set_xlim(220, 1740)
        ax_r.set_xlim(1805, 2042)
        for ax in (ax_l, ax_r):
            ax.set_yscale("log")
            ax.set_ylim(*ylim)
            ax.grid(True, which="major", ls="--", lw=0.5, alpha=0.45)
            ax.spines["top"].set_visible(False)
        ax_l.spines["right"].set_visible(False)
        ax_r.spines["left"].set_visible(False)
        ax_r.tick_params(axis="y", which="both", left=False)
        ax_l.set_ylabel(ylabel)
        draw_break_marks(ax_l, ax_r)

        for corridor in ["London-New York", "Antwerp-Venice"]:
            pts = [r for r in rows if r["corridor"] == corridor and r["specification_type"] == "baseline" and r[metric] is not None]
            c = CORRIDOR_STYLE[corridor]["color"]
            xs = [p["year"] for p in pts]
            ys = [p[metric] for p in pts]
            ax_l.plot(xs, ys, color=c, lw=1.6, zorder=3)
            ax_r.plot(xs, ys, color=c, lw=1.6, zorder=3)
            for p in pts:
                target = ax_l if p["year"] < 1800 else ax_r
                m = SCOPE_MARKERS.get(p["transit_scope"], "o")
                target.scatter(p["year"], p[metric], color=c, marker=m, s=46, edgecolor="white", lw=0.7, zorder=4)

        for p in rows:
            if p[metric] is None:
                continue
            target = ax_l if p["year"] < 1800 else ax_r
            if p["corridor"] == "Rome-Brundisium" and p["specification_type"] == "baseline":
                target.scatter(p["year"], p[metric], color="#8c6d1f", marker="P", s=65, edgecolor="white", lw=0.7, zorder=5)
            elif p["specification_type"] == "sensitivity":
                c = CORRIDOR_STYLE.get(p["corridor"], {"color": "#1b4965"})["color"]
                target.scatter(p["year"], p[metric], facecolor="white", edgecolor=c, marker="^", s=62, lw=1.4, zorder=6)

    axes[0, 0].set_title("Pre-Industrial Era (301-1635 AD)", pad=8)
    axes[0, 1].set_title("Industrial & Telecommunications Era (1825-2026 AD)", pad=8)
    axes[1, 0].set_xlabel("Year (AD)")
    axes[1, 1].set_xlabel("Year (AD)")

    axes[0, 0].annotate("301 AD: 288.0 h", (301, 288.0), xytext=(370, 420), fontsize=7.8)
    axes[0, 0].annotate("1395: 19.0 h", (1395, 19.0), xytext=(1080, 28), fontsize=7.8)
    axes[0, 0].annotate("1635: 0.87 h", (1635, 0.87), xytext=(1220, 0.32), fontsize=7.8)
    axes[0, 1].annotate("1825: 3.33 h", (1825, 3.33), xytext=(1812, 9.0), fontsize=7.8)
    axes[0, 1].annotate("1855: 1.82 h", (1855, 1.82), xytext=(1832, 0.40), fontsize=7.8)
    axes[0, 1].annotate("1866 Jul: 615.4 h (Sens.)", (1866, 615.38), xytext=(1874, 720), fontsize=7.8)
    axes[0, 1].annotate("1866 Nov: 307.7 h", (1866, 307.69), xytext=(1874, 145), fontsize=7.8)
    axes[0, 1].annotate("1956: 12.2 h (TAT-1)", (1956, 12.20), xytext=(1936, 28), fontsize=7.8)
    axes[0, 1].annotate("2026: 1e-6 h (T3 Wholesale)", (2026, 1e-6), xytext=(1958, 3e-6), fontsize=7.8)
    axes[1, 1].annotate("1866: 0.25 h (T) / 0.02 h (W)", (1866, 0.25), xytext=(1874, 0.55), fontsize=7.8)

    handles = [
        mlines.Line2D([], [], color="#1b4965", lw=1.6, label="London-New York (Baseline)"),
        mlines.Line2D([], [], color="#c8553d", lw=1.6, label="Antwerp-Venice (Baseline)"),
        mlines.Line2D([], [], color="#8c6d1f", marker="P", ls="None", ms=7, label="Rome-Brundisium (301 AD, T3)"),
        mlines.Line2D([], [], color="#1b4965", marker="^", mfc="white", ls="None", ms=7, label="Declared Sensitivity (-SENS)"),
        mlines.Line2D([], [], color="#444444", marker="o", ls="None", ms=6, label="Door-to-Door (D)"),
        mlines.Line2D([], [], color="#444444", marker="s", ls="None", ms=6, label="Terminal-to-Terminal (T)"),
        mlines.Line2D([], [], color="#444444", marker="D", ls="None", ms=5.5, label="Wire-Signaling-Only (W)"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False, fontsize=8, bbox_to_anchor=(0.5, -0.04))

    OUT_PDF.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT_PDF, bbox_inches="tight")
    fig.savefig(OUT_PNG, dpi=300, bbox_inches="tight")
    print("Generated:", OUT_PDF, "and", OUT_PNG)

if __name__ == "__main__":
    build_figure()
