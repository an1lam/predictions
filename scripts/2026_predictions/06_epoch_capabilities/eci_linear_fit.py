#!/usr/bin/env python3
"""
Epoch Capabilities Index (ECI) Linear Fit Analysis

Fits a linear regression to the SOTA progression and projects forward.
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta

# Load data
data_path = "/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/epoch_capabilities_index.csv"
df = pd.read_csv(data_path)

# Clean data - remove rows with missing ECI scores
df = df[df['ECI Score'].notna()]
df['Release date'] = pd.to_datetime(df['Release date'])
df = df.sort_values('Release date')

print("=" * 80)
print("EPOCH CAPABILITIES INDEX (ECI) LINEAR FIT ANALYSIS")
print("=" * 80)

# Extract SOTA progression (only keep points that set new records)
sota_progression = []
current_sota = 0
for _, row in df.iterrows():
    if row['ECI Score'] > current_sota:
        current_sota = row['ECI Score']
        sota_progression.append({
            'date': row['Release date'],
            'score': current_sota,
            'model': row['Model version'] if pd.notna(row['Model version']) else row['Model name'],
            'org': row['Organization']
        })

sota_df = pd.DataFrame(sota_progression)

print("\n### SOTA Progression")
print("-" * 80)
for _, row in sota_df.iterrows():
    date_str = row['date'].strftime('%Y-%m-%d')
    print(f"{date_str}: {row['score']:6.1f} - {row['model'][:40]:<40} ({row['org']})")

# Convert dates to numeric (days since first observation)
reference_date = sota_df['date'].min()
sota_df['days'] = (sota_df['date'] - reference_date).dt.days

# Linear regression
x = sota_df['days'].values
y = sota_df['score'].values

slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

print("\n### Linear Regression")
print("-" * 80)
print(f"Intercept: {intercept:.2f}")
print(f"Slope: {slope:.4f} points/day ({slope * 30:.2f} points/month)")
print(f"R²: {r_value**2:.4f}")
print(f"Standard error of slope: {std_err:.6f}")

# Calculate 10th/90th percentile bounds on slope
n = len(x)
t_val_90 = stats.t.ppf(0.90, n - 2)
t_val_10 = stats.t.ppf(0.10, n - 2)

slope_p10 = slope + t_val_10 * std_err  # Lower bound (t_val_10 is negative)
slope_p90 = slope + t_val_90 * std_err  # Upper bound

print(f"\nSlope bounds:")
print(f"  10th percentile: {slope_p10:.4f} points/day ({slope_p10 * 30:.2f} points/month)")
print(f"  90th percentile: {slope_p90:.4f} points/day ({slope_p90 * 30:.2f} points/month)")

# Project to Dec 31, 2026
target_date = datetime(2026, 12, 31)
target_days = (target_date - reference_date).days

projection_central = intercept + slope * target_days
projection_p10 = intercept + slope_p10 * target_days
projection_p90 = intercept + slope_p90 * target_days

print("\n### Projection to Dec 31, 2026")
print("-" * 80)
print(f"Days from reference: {target_days}")
print(f"Central estimate: {projection_central:.1f}")
print(f"10th percentile: {projection_p10:.1f}")
print(f"90th percentile: {projection_p90:.1f}")

# Current state
current_date = sota_df['date'].max()
current_score = sota_df['score'].max()
months_remaining = (target_date - current_date).days / 30

print(f"\n### Summary")
print("-" * 80)
print(f"Current SOTA: {current_score:.1f} (as of {current_date.strftime('%Y-%m-%d')})")
print(f"Months to Dec 31, 2026: {months_remaining:.1f}")
print(f"Expected gain: {projection_central - current_score:.1f} points")
print(f"  (Range: {projection_p10 - current_score:.1f} to {projection_p90 - current_score:.1f})")

# Quick sanity check with monthly velocity
print("\n### Alternative: Recent Monthly Velocity")
print("-" * 80)
# Look at last 12 months
cutoff = datetime.now() - timedelta(days=365)
recent = sota_df[sota_df['date'] >= cutoff]
if len(recent) >= 2:
    first = recent.iloc[0]
    last = recent.iloc[-1]
    days_diff = (last['date'] - first['date']).days
    score_diff = last['score'] - first['score']
    if days_diff > 0:
        recent_velocity = score_diff / (days_diff / 30)
        print(f"Last 12 months: {first['score']:.1f} -> {last['score']:.1f}")
        print(f"Velocity: {recent_velocity:.2f} points/month")
        print(f"Projection at this rate: {current_score + recent_velocity * months_remaining:.1f}")
