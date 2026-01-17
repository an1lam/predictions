#!/usr/bin/env python3
"""
GSO Benchmark Sigmoid Fitting

Fits a logistic (sigmoid) curve to the SOTA progression and projects forward.
"""

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Load data
data_path = "/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/gso_external.csv"
df = pd.read_csv(data_path)

# Convert to percentages
df['Score_pct'] = df['Score OPT@1'] * 100
df['Release date'] = pd.to_datetime(df['Release date'])
df = df.sort_values('Release date')

# Extract SOTA progression
sota_progression = []
current_sota = 0
for _, row in df.iterrows():
    if row['Score_pct'] > current_sota:
        current_sota = row['Score_pct']
        sota_progression.append({
            'date': row['Release date'],
            'score': current_sota,
            'model': row['Model version']
        })

sota_df = pd.DataFrame(sota_progression)

# Convert dates to numeric (days since first observation)
reference_date = sota_df['date'].min()
sota_df['days'] = (sota_df['date'] - reference_date).dt.days

print("=" * 80)
print("GSO SIGMOID FITTING ANALYSIS")
print("=" * 80)

print("\n### SOTA Data Points")
print("-" * 80)
for _, row in sota_df.iterrows():
    print(f"Day {row['days']:4d}: {row['score']:5.1f}% - {row['model']}")

# Define logistic function
def logistic(x, L, k, x0):
    """
    L = maximum value (ceiling)
    k = steepness
    x0 = x-value of sigmoid midpoint
    """
    return L / (1 + np.exp(-k * (x - x0)))

# Fit the curve
x_data = sota_df['days'].values
y_data = sota_df['score'].values

print("\n### Sigmoid Fitting")
print("-" * 80)

# Try different ceiling assumptions
ceilings = [60, 70, 80, 90, 100]

results = []
for ceiling in ceilings:
    try:
        # Constrain L to the ceiling
        def logistic_fixed_L(x, k, x0):
            return ceiling / (1 + np.exp(-k * (x - x0)))

        popt, pcov = curve_fit(
            logistic_fixed_L,
            x_data,
            y_data,
            p0=[0.01, 300],  # Initial guesses for k and x0
            bounds=([0.001, 0], [0.1, 1500]),
            maxfev=10000
        )

        k, x0 = popt

        # Calculate R²
        y_pred = logistic_fixed_L(x_data, k, x0)
        ss_res = np.sum((y_data - y_pred) ** 2)
        ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
        r_squared = 1 - (ss_res / ss_tot)

        # Project to Dec 31, 2026
        target_date = datetime(2026, 12, 31)
        target_days = (target_date - reference_date).days
        projection = logistic_fixed_L(target_days, k, x0)

        results.append({
            'ceiling': ceiling,
            'k': k,
            'x0': x0,
            'r_squared': r_squared,
            'projection': projection
        })

        print(f"\nCeiling = {ceiling}%:")
        print(f"  k (steepness) = {k:.5f}")
        print(f"  x0 (midpoint) = {x0:.0f} days ({(reference_date + timedelta(days=x0)).strftime('%Y-%m-%d')})")
        print(f"  R² = {r_squared:.4f}")
        print(f"  Projection (Dec 31, 2026): {projection:.1f}%")

    except Exception as e:
        print(f"\nCeiling = {ceiling}%: Fitting failed - {e}")

# Also try unconstrained fit
print("\n### Unconstrained Sigmoid Fit")
print("-" * 80)
try:
    popt, pcov = curve_fit(
        logistic,
        x_data,
        y_data,
        p0=[80, 0.01, 400],  # L, k, x0
        bounds=([30, 0.001, 0], [100, 0.1, 2000]),
        maxfev=10000
    )

    L, k, x0 = popt

    y_pred = logistic(x_data, L, k, x0)
    ss_res = np.sum((y_data - y_pred) ** 2)
    ss_tot = np.sum((y_data - np.mean(y_data)) ** 2)
    r_squared = 1 - (ss_res / ss_tot)

    target_days = (datetime(2026, 12, 31) - reference_date).days
    projection = logistic(target_days, L, k, x0)

    print(f"Fitted ceiling (L) = {L:.1f}%")
    print(f"Steepness (k) = {k:.5f}")
    print(f"Midpoint (x0) = {x0:.0f} days ({(reference_date + timedelta(days=x0)).strftime('%Y-%m-%d')})")
    print(f"R² = {r_squared:.4f}")
    print(f"Projection (Dec 31, 2026): {projection:.1f}%")

except Exception as e:
    print(f"Unconstrained fit failed: {e}")

# Summary table
print("\n### Summary: Projections by Ceiling Assumption")
print("-" * 80)
print(f"{'Ceiling':>10} {'R²':>8} {'Midpoint':>12} {'Dec 2026':>10}")
print("-" * 80)
for r in results:
    midpoint_date = (reference_date + timedelta(days=r['x0'])).strftime('%Y-%m')
    print(f"{r['ceiling']:>9}% {r['r_squared']:>8.4f} {midpoint_date:>12} {r['projection']:>9.1f}%")

# Current position analysis
print("\n### Where are we on the curve?")
print("-" * 80)
current_days = (datetime(2025, 12, 11) - reference_date).days
print(f"Current: Day {current_days}, Score 27.4%")
for r in results:
    pct_of_ceiling = 27.4 / r['ceiling'] * 100
    past_midpoint = "past" if current_days > r['x0'] else "before"
    print(f"  At {r['ceiling']}% ceiling: {pct_of_ceiling:.0f}% of max, {past_midpoint} midpoint")
