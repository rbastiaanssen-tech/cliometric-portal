#!/usr/bin/env python3
import csv
import math
from pathlib import Path

CSV_PATH = Path("public/data/master_benchmarks.csv")
MANUSCRIPT_DIR = Path("manuscript")

REQUIRED_FIGS = [
    "figure1_corridor_maps.pdf",
    "figure2_gvk_distance_latency.pdf",
    "figure3_gvk_bandwidth_latency.pdf",
    "figure4_macro_spine.pdf",
]

REQUIRED_PDFS = [
    "paper1_manuscript.pdf",
    "paper1_blind.pdf",
    "eeh_cover_letter.pdf",
]

def run_audit():
    with open(CSV_PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    assert len(rows) == 19, f"Expected 19 rows (17 wage-normalized + 2 physical anchors), found {len(rows)}"

    for r in rows:
        bid = r["id"]
        assert float(r["distance_km"]) > 0, f"Invalid distance_km in {bid}"
        assert float(r["sending_rate_bps"]) > 0, f"Invalid sending_rate_bps in {bid}"
        assert float(r["transit_hours"]) > 0, f"Invalid transit_hours in {bid}"

        if r["specification_type"] == "physical_anchor":
            continue

        for col in ["payload_words", "door_to_door_est_hours", "labor_hours_per_message", "labor_hours_per_100_words"]:
            val = r[col].strip()
            assert val != "" and "Pending" not in val, f"Missing cell in {bid}.{col}"
            num = float(val)
            assert math.isfinite(num) and num > 0

        words = float(r["payload_words"])
        lh_msg = float(r["labor_hours_per_message"])
        lh_100 = float(r["labor_hours_per_100_words"])
        expected_100 = lh_msg * (100.0 / words)
        assert abs(lh_100 - expected_100) / expected_100 < 0.01, f"Scaling mismatch in {bid}"

    for fig in REQUIRED_FIGS:
        p = MANUSCRIPT_DIR / fig
        assert p.exists() and p.stat().st_size > 1000, f"Missing figure: {p}"

    for pdf in REQUIRED_PDFS:
        p = MANUSCRIPT_DIR / pdf
        assert p.exists() and p.stat().st_size > 5000, f"Missing PDF: {p}"

    blind_tex = (MANUSCRIPT_DIR / "paper1_blind.tex").read_text(encoding="utf-8")
    for token in ["Bastiaanssen", "bastiaanssen", "rbastiaanssen"]:
        assert token not in blind_tex, f"Double-blind leak: {token}"

    print(f"[PASS] Audited {len(rows)} rows in {CSV_PATH} (including distance_km & sending_rate_bps)")
    print("[PASS] Verified 4 vector figures, 3 compiled PDFs, and double-blind anonymization")

if __name__ == "__main__":
    run_audit()
