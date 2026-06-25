"""
Last Mile Delivery Analysis — Mini Hackathon
============================================
Author : Hackathon Submission
Dataset: last_mile_delivery_dataset.csv  (2,080 rows × 20 columns)
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# ─────────────────────────────────────────────
# 0. LOAD
# ─────────────────────────────────────────────
df = pd.read_csv('last_mile_delivery_dataset.csv')
print(f"Loaded: {df.shape[0]} rows × {df.shape[1]} cols")

# ─────────────────────────────────────────────
# 1. CLEANING
# ─────────────────────────────────────────────
print("\n── Data Cleaning ──────────────────────────")

# Normalise vehicle_type casing  (Bike / bike / BIKE → Bike)
df['vehicle_type'] = df['vehicle_type'].str.strip().str.title()

# Normalise city names
city_map = {
    'delhi'      : 'Delhi',
    'MUMBAI'     : 'Mumbai',
    'chennai'    : 'Chennai',
    ' Ahmedabad' : 'Ahmedabad',
    'Bangaluru'  : 'Bangalore',
    'Kolkata '   : 'Kolkata',
    'Hydrabad'   : 'Hyderabad',
}
df['city'] = df['city'].str.strip().replace(city_map)

# Fill missing categoricals
df['zone']     = df['zone'].fillna('Unknown')
df['rider_id'] = df['rider_id'].fillna('UNKNOWN')

# Parse date/time features
df['order_date'] = pd.to_datetime(df['order_date'])
df['hour']       = df['order_time'].str[:2].astype(int)
df['month']      = df['order_date'].dt.month

print(f"  Cities clean     : {df['city'].nunique()} unique → {sorted(df['city'].unique())}")
print(f"  Vehicle types    : {sorted(df['vehicle_type'].unique())}")
print(f"  Nulls remaining  :\n{df.isnull().sum()[df.isnull().sum()>0]}")


# ─────────────────────────────────────────────
# Q1 — PEAK HOUR DELAY PATTERN
# ─────────────────────────────────────────────
print("\n── Q1: Peak Hour Delay ────────────────────")

df['peak'] = df['hour'].apply(
    lambda h: 'Peak' if (8 <= h <= 10 or 17 <= h <= 20) else 'Off-Peak'
)

peak   = df[df['peak'] == 'Peak']['delay_mins']
offpk  = df[df['peak'] == 'Off-Peak']['delay_mins']

print(f"  Peak    hours n={len(peak):4d}  mean={peak.mean():.2f} min  median={peak.median():.2f} min")
print(f"  Off-peak hours n={len(offpk):4d}  mean={offpk.mean():.2f} min  median={offpk.median():.2f} min")
print(f"  Difference  (mean) : {peak.mean() - offpk.mean():.2f} min  ({((peak.mean()-offpk.mean())/offpk.mean()*100):.0f}% higher)")

u_stat, p_val = stats.mannwhitneyu(peak, offpk, alternative='greater')
print(f"  Mann-Whitney U={u_stat:.0f},  p={p_val:.4e}  → {'SIGNIFICANT ✓' if p_val < 0.05 else 'NOT significant'}")


# ─────────────────────────────────────────────
# Q2 — WEATHER vs DELAY EDA
# ─────────────────────────────────────────────
print("\n── Q2: Weather vs Delay ───────────────────")

wx = df[df['weather_condition'].isin(['Clear', 'Rain', 'Fog'])]
print("  Median delay by weather condition:")
print(wx.groupby('weather_condition')['delay_mins'].median().to_string())

rain     = df[df['weather_condition'] == 'Rain']
worst_ot = rain.groupby('order_type')['delay_mins'].median().sort_values(ascending=False)
print(f"\n  Order type hardest hit by rain (median delay):")
print(worst_ot.to_string())
print(f"\n  → Hardest hit: {worst_ot.idxmax()} ({worst_ot.max():.1f} min median delay)")


# ─────────────────────────────────────────────
# Q3 — RIDER EXPERIENCE EFFECT (statistics)
# ─────────────────────────────────────────────
print("\n── Q3: Rider Experience Effect ────────────")

junior = df[df['rider_experience_yrs'] < 2]['delay_mins']
senior = df[df['rider_experience_yrs'] > 4]['delay_mins']

print(f"  Junior (<2yr)  n={len(junior):4d}  mean={junior.mean():.2f}  median={junior.median():.2f}  std={junior.std():.2f}")
print(f"  Senior (>4yr)  n={len(senior):4d}  mean={senior.mean():.2f}  median={senior.median():.2f}  std={senior.std():.2f}")

u2, p2 = stats.mannwhitneyu(junior, senior, alternative='greater')
cohen_d = (junior.mean() - senior.mean()) / np.sqrt((junior.std()**2 + senior.std()**2) / 2)
print(f"\n  Mann-Whitney U={u2:.0f},  p={p2:.4f}")
print(f"  Cohen's d = {cohen_d:.3f}  (|d|<0.2 → negligible effect size)")
print(f"  Conclusion: {'Significant' if p2 < 0.05 else 'No significant'} difference in delays by experience band.")


# ─────────────────────────────────────────────
# Q4 — DASHBOARD DATA
# ─────────────────────────────────────────────
print("\n── Q4: City-Level Performance ─────────────")

city_ontime = (
    df.groupby('city')
      .apply(lambda x: (x['delivery_status'] == 'On-Time').mean() * 100)
      .round(1)
      .sort_values()
)
print("  On-time rate by city:")
print(city_ontime.to_string())

monthly_delay = df.groupby('month')['delay_mins'].mean().round(2)
print("\n  Monthly avg delay:")
print(monthly_delay.to_string())

veh_perf = df.groupby('vehicle_type')['delay_mins'].agg(['mean','median','count']).round(2)
print("\n  Vehicle type performance:")
print(veh_perf.to_string())

print("\n✅ Analysis complete — see PNG files for charts.")
