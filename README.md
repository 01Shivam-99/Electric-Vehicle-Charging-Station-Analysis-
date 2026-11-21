# Project 26: Electric Vehicle Charging Station Analysis

**Student:** Shivam Mishra  
**Institution:** ABES Engineering College, Ghaziabad  
**Programme:** B.Tech, ELCE (Electrical and Computer Engineering)  
**Admission No:** 2026B022310161 | **Serial No:** 2  
**Date:** 20 November 2026  

---

## Project Overview

A charging network operator runs **49 stations** across five site types (Highway, Transit Hub, Mall, Residential, Office District). This project cleans the raw session records, analyses demand and charging-duration patterns with **Python, NumPy and Pandas**, and delivers **five evidence-based recommendations** for improving station availability.

### Industry
Transportation / Clean Energy

### Period Covered
1 January 2025 – 29 October 2026

---

## Dataset

| File | Description |
|------|-------------|
| `26_ev_charging_sessions.csv` | Raw input (862 rows, 8 columns) |
| `26_ev_charging_sessions_clean.csv` | Cleaned output (850 rows, 13 columns) |

### Original Columns
- `Session_ID`, `Station_ID`, `Station_Location`, `Charger_Type`
- `Charging_Start_Time`, `Energy_kWh`, `Charging_Duration_Mins`, `Vehicle_Type`

### Derived Columns (after cleaning)
- `Hour`, `Weekday`, `Month`, `Year`, `Duration_Group`

---

## How to Run

```bash
# Prerequisites
pip install pandas numpy

# Run the complete analysis
pip install pandas numpy
```

The script executes top-to-bottom without errors and prints every required metric, table and recommendation.

---

## Functional Requirements Covered

| ID | Requirement | Status |
|----|-------------|--------|
| FR1 | Load dataset, show shape / columns / dtypes | ✅ |
| FR2 | Missing values & duplicate Session_IDs | ✅ |
| FR3 | Deduplicate + median imputation by Charger_Type | ✅ |
| FR4 | Datetime conversion + Hour / Weekday / Month / Year | ✅ |
| FR5 | Total sessions, total energy, avg duration | ✅ |
| FR6 | Average energy per session | ✅ |
| FR7 | Rank stations by sessions & total energy | ✅ |
| FR8 | Avg duration by charger type | ✅ |
| FR9 | Peak hours & busiest weekdays | ✅ |
| FR10 | Energy by station location | ✅ |
| FR11 | Tuple (charger types) + Set (locations) | ✅ |
| FR12 | Dictionary (station counts) + reusable function | ✅ |
| FR13 | NumPy mean / median / 90th percentile | ✅ |
| FR14 | IQR outlier detection + Duration_Group | ✅ |
| FR15 | ChargingSession class + 5 recommendations | ✅ |

---

## Key Findings (from the run)

- **850 unique sessions** after removing 12 duplicate Session_IDs  
- **21 missing values** each in Energy_kWh and Charging_Duration_Mins → imputed with Charger_Type median  
- Mean duration ≈ **186 min**, 90th percentile ≈ **320 min**  
- **0 statistical outliers** by 1.5 × IQR rule  
- ≈ **33 %** of sessions classified as “Long” (> 240 min)  
- Peak hour and busiest weekday identified programmatically  

---

## Five Operational Recommendations

1. **Prioritise capacity** at the highest-demand stations (extra / faster chargers).  
2. **Align maintenance** with off-peak hours; consider reservations for the peak hour.  
3. **Reduce long-idle occupancy** via over-stay fees or completion notifications.  
4. **Match charger type to location** (DC Fast at Highway / Transit Hub; Level-2 at Residential / Office).  
5. **Optimise charger-type mix** at high-turnover sites to increase daily throughput.

---

## Project Structure

```
ev-charging-station-analysis/
├── 26_ev_charging_sessions.csv          # Raw dataset
├── 26_ev_charging_sessions_clean.csv    # Cleaned dataset (generated)
├── ev_charging_analysis.py              # Complete analysis script
└── README.md                            # This file
```

---

## Tools & Technologies

| Tool | Purpose |
|------|---------|
| Python 3.10+ | Core language |
| Pandas | Loading, cleaning, grouping, ranking |
| NumPy | Mean, median, percentiles, IQR |
| VS Code | Development environment |

---

## Assumptions & Limitations

- Dataset is a **simulated teaching set**; results must not be generalised to real networks.  
- Findings are **associations**, not causal claims.  
- No pricing, revenue or grid-load modelling is included (columns absent).  

---

*Generated for academic submission – Project 26*  
