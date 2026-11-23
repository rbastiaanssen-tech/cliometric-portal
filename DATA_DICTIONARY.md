# Data Dictionary & Empirical Classification Protocol (Section 1.2)

## 1. Evidence Tier Taxonomy (`T1` / `T2` / `T3`)
Following standard cliometric practice (Nordhaus 1996; Allen 2001), every observation is classified into a three-tier evidence hierarchy. In `master_benchmarks.csv`, tariff pricing (`tariff_tier`) and physical payload/throughput (`capacity_tier`) are scored independently so hybrid observations receive explicit credit for primary tariffs without masking stylized capacity assumptions.

* **`T1` — Authenticated Primary:** Directly transcribed from contemporary archival ledgers, statutory enactments, official gazettes, or primary corporate tariff notices.
* **`T2` — Corroborated Secondary:** Sourced from peer-reviewed economic/postal historiography; awaiting visual inspection or folio-level archival transcription.
* **`T3` — Parameterized Calibration:** Stylized engineering benchmark, statutory state-requisition quota where open-access commercial mail did not exist (`M/C-A-2` 301 AD; `M/C-A-3` 750 AD), or wholesale network capacity allocation (`2026` DWDM/subsea fiber).

## 2. Dataset Inventory

### `public/data/master_benchmarks.csv` (Layers 1 & 2)
* `id`: Unique corridor-era identifier (`-SENS` suffix denotes declared sensitivity specification).
* `specification_type`: `baseline` (13 core macro-spine records) or `sensitivity` (4 alternative payload/speed/mode specifications).
* `tariff_tier` / `capacity_tier`: Independent `T1`, `T2`, or `T3` classification for price and payload.
* `daily_wage_nominal` / `wage_unit`: Matched local unskilled/craftsman wage numéraire.
* `labor_hours_per_message`: Headline real communication cost in labor-hours per standardized message (blank cells await final manuscript calibration import; never synthetically imputed).

### `public/data/atlantic_milestones.csv` (Layer 3)
* 17 transatlantic market-structure milestones (1815–1956).
* `is_dual_rate`: Boolean flag identifying the May 1886 transatlantic cable price war (`primary_rate_gbp = 0.0250` [12¢ pool rate] vs. `secondary_rate_gbp = 0.0500` [25¢ Commercial Cable Co. rate]).

### `public/data/brenner_track.csv` (Layer 4)
* Transalpine / Brenner corridor institutional tariffs (`DÖTV 1850`, `1867 Railway Opening`, and unpromoted candidate lines).

### `public/data/grain_panel_events.csv` (Layer 5)
* Municipal commercial telegraph and railway opening dates for the 8-town British Corn Returns panel (1842–1864).

### `public/data/sensitivity_parameters.csv` (Layer 6)
* Theoretical quote-age risk break-even (`H* = 2.515` labor-hours/hour, Steinwender 2018 AER) and 2026 retail broadband vs. wholesale transit scopes.
