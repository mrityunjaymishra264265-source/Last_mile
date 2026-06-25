# Last Mile Delivery — Mini Hackathon Submission
**Dataset:** `last_mile_delivery_dataset.csv` — 2,080 orders · 20 columns · 10 Indian cities · Full year 2024
---
##  File Structure
```
hackathon/
├── Last_Mile_Delivery_Analysis.ipynb   # Main Jupyter notebook
├── analysis.py                         # Standalone Python source
├── README.md                           # This file
├── q1_peak_hour_delay.png              # Q1 chart
├── q2_weather_eda.png                  # Q2 chart
├── q3_rider_experience.png             # Q3 chart
└── q4_dashboard.png                    # Q4 3-panel dashboard
```
##  Step 1 — Data Cleaning (After Cleaning)
| Issue | Fix Applied |
|-------|------------|
| `vehicle_type` mixed casing (bike/Bike/BIKE) | `.str.title()` normalisation |
| `city` typos: Hydrabad, Bangaluru, 'Kolkata ', ' Ahmedabad', delhi, MUMBAI | Manual mapping dict |
| `zone` — 136 nulls | Filled with `'Unknown'` |
| `rider_id` — 113 nulls | Filled with `'UNKNOWN'` |
| `gps_latitude/longitude` — 137 nulls | Not used in analysis |
| datetime parsing | `order_date` → `pd.to_datetime`, `order_time` → `hour` (int) |

Post-cleaning: **10 clean cities**, **4 vehicle types**, **0 duplicates**
## Q1 — Peak Hour Delay Pattern
**Question:** Do orders placed during 8–10 AM and 5–8 PM have significantly higher `delay_mins`?

### Method
- Classified each order as `Peak` (8–10 AM or 5–8 PM) or `Off-Peak`
- Used **Mann-Whitney U test** (one-tailed) — chosen because delay distribution is right-skewed, not normally distributed
### Results
| Group | n | Mean Delay | Median Delay |
|-------|---|-----------|--------------|
| **Peak** | 869 | **23.25 min** | 20.50 min |
| Off-Peak | 1,211 | 7.38 min | 5.50 min |

- **Delta: +15.87 min** (215% higher in peak vs off-peak)
- Mann-Whitney U = 748,550 — **p < 0.0001 → Highly significant**

### Key Finding
Peak hours create a consistent, statistically verified delay surge. Hour 9 AM shows the single worst average delay (25.69 min). Evening peak (5–8 PM) is similarly severe.
---
## Q2 — Weather vs Delay Correlation (EDA)
**Question:** How does median delay vary across Clear, Rain, and Fog? Which order type suffers most in rain?
### Median Delay by Weather
| Condition | Median Delay |
|-----------|-------------|
| Clear | 6.1 min |
| Rain | 29.4 min |
| **Fog** | **37.9 min** |
Fog is the worst weather condition — **6.2× worse than clear skies**.
### Rain Impact by Order Type (Median Delay)
| Order Type | Median Delay in Rain |
|------------|---------------------|
| **Medicine** | **34.65 min**  |
| Documents | 29.80 min |
| Food | 29.20 min |
| Grocery | 29.05 min |
| Electronics | 28.80 min |
| Apparel | 27.10 min |
**Medicine deliveries are hardest hit in rain.** This is operationally critical given their time-sensitivity.
## Q3 — Rider Experience Effect (Statistics)
**Question:** Is there a statistically meaningful difference in `delay_mins` between riders with <2 years vs >4 years experience?
### Method
- **Mann-Whitney U test** (one-tailed: H₁ = juniors have higher delays)
- Effect size: **Cohen's d**
### Results
| Group | n | Mean | Median | Std |
|-------|---|------|--------|-----|
| Junior (<2 yr) | 450 | 13.75 min | 11.60 min | 22.54 |
| Senior (>4 yr) | 1,065 | 14.35 min | 12.20 min | 22.18 |
- Mann-Whitney p = **0.7168** (>> 0.05 → **Not significant**)
- Cohen's d = **-0.027** (negligible — practically zero effect size)
### Conclusion
Experience alone does not predict delivery delay in this dataset. Other factors (traffic, weather, distance, zone) dominate. Rider training programs focused solely on experience-time would not be cost-effective.
---
## Q4 — City-Level Performance Dashboard
### Panel 1 — City On-Time Rate
| City | On-Time % |
|------|----------|
| **Hyderabad** | **51.6%** Best |
| Jaipur | 38.7% |
| Mumbai | 38.4% |
| Pune | 36.3% |
| Chennai | 35.8% |
| Kolkata | 34.9% |
| Lucknow | 34.8% |
| Ahmedabad | 34.7% |
| Delhi | 34.3% |
| **Bangalore** | **31.1%** Worst |
### Panel 2 — Monthly Delay Trend
- Highest delays: **December (15.83 min)**, October (15.52 min), July (15.29 min)
- Lowest delays: **February (10.94 min)**
- Pattern: delays rise through summer/monsoon months and peak at year-end
### Panel 3 — Vehicle Type Comparison
| Vehicle | Mean Delay | Median Delay | On-Time % |
|---------|-----------|--------------|-----------|
| **Bike** | **12.84** | **11.1** | Highest |
| Cycle | 14.28 | 11.4 | — |
| Van | 14.41 | 11.9 | — |
| Auto | 14.83 | 13.2 | Lowest |

**Bikes are the best-performing vehicle type** — lower mean delay and highest on-time rate.
---
##  Final Insights & Observations
| # | Finding | Action |
|---|---------|--------|
| 1 | Peak hours add **+15.87 min** delay — statistically proven | Surge staffing / dynamic routing during 8–10 AM & 5–8 PM |
| 2 | Fog causes 37.9 min median delay — worst weather impact | Proactive rescheduling + rider safety alerts in fog |
| 3 | **Medicine in rain = 34.65 min delay** — time-critical category | Priority queue / weather-aware dispatch for medicine |
| 4 | Experience level has no significant impact on delay | Focus training on route optimisation, not just seniority |
| 5 | Bangalore's 31.1% on-time rate is 20pp below Hyderabad | Audit Bangalore operations — zone mapping, rider density |
| 6 | Bikes outperform Autos in every metric | Shift more deliveries to bikes, reduce Auto allocation |
| 7 | Dec/Oct/Jul show highest average delays | Pre-plan capacity increases before these months |

---
## Single Biggest Operational Fix

> **Implement peak-hour dynamic routing and surge staffing.**
>
> The 8–10 AM and 5–8 PM windows account for 42% of all orders yet carry
> a verified **+215% delay premium**. Addressing this single pattern — through
> better route algorithms, pre-positioned riders, or demand-shifting incentives —
> would deliver the largest measurable improvement in on-time rates across all cities.
## Tech Stack
- **Python 3.11** — pandas, numpy, scipy, matplotlib
- **Statistical tests** — Mann-Whitney U (non-parametric), Cohen's d
- **Visualisation** — matplotlib with custom dark theme
- **Notebook** — Jupyter (.ipynb)
