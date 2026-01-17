#!/usr/bin/env python3
"""
GSO Benchmark Sigmoid Fit Visualization

Plots the SOTA progression with fitted sigmoid curves and Dec 2026 projection.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
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

# Define logistic function
def logistic(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

# Fit with 95% ceiling (human performance)
ceiling = 95
def logistic_fixed_L(x, k, x0):
    return ceiling / (1 + np.exp(-k * (x - x0)))

x_data = sota_df['days'].values
y_data = sota_df['score'].values

popt, _ = curve_fit(
    logistic_fixed_L,
    x_data,
    y_data,
    p0=[0.01, 300],
    bounds=([0.001, 0], [0.1, 1500]),
    maxfev=10000
)
k, x0 = popt

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Generate fitted curve
target_date = datetime(2026, 12, 31)
target_days = (target_date - reference_date).days
x_curve = np.linspace(0, target_days + 50, 500)
y_curve = logistic_fixed_L(x_curve, k, x0)

# Convert days back to dates for x-axis
curve_dates = [reference_date + timedelta(days=d) for d in x_curve]

# Plot sigmoid curve
ax.plot(curve_dates, y_curve, 'b-', linewidth=2, label=f'Sigmoid fit (ceiling={ceiling}%)')

# Plot actual SOTA points
ax.scatter(sota_df['date'], sota_df['score'], color='red', s=80, zorder=5, label='SOTA progression')

# Mark key points
# Current SOTA (Dec 2025)
current_date = datetime(2025, 12, 11)
current_score = 27.4
ax.scatter([current_date], [current_score], color='darkred', s=150, marker='*', zorder=6, label=f'Current ({current_score}%)')

# Dec 2026 projection
projection = logistic_fixed_L(target_days, k, x0)
ax.scatter([target_date], [projection], color='green', s=150, marker='D', zorder=6, label=f'Dec 2026 projection ({projection:.0f}%)')

# Mark sigmoid midpoint
midpoint_date = reference_date + timedelta(days=x0)
midpoint_score = ceiling / 2
ax.axvline(midpoint_date, color='gray', linestyle='--', alpha=0.5)
ax.annotate(f'Midpoint\n{midpoint_date.strftime("%Y-%m")}',
            xy=(midpoint_date, midpoint_score),
            xytext=(midpoint_date + timedelta(days=30), midpoint_score + 10),
            fontsize=9, ha='left',
            arrowprops=dict(arrowstyle='->', color='gray', alpha=0.5))

# Add prediction interval band (10th-90th percentile: 45%-95%)
ax.axhspan(45, 95, xmin=0.85, xmax=1.0, alpha=0.2, color='green', label='10th-90th percentile')

# Mark our prediction
ax.axhline(74, color='green', linestyle=':', alpha=0.7)
ax.annotate('Prediction: 74%', xy=(target_date - timedelta(days=180), 74),
            fontsize=10, color='green', va='bottom')

# Formatting
ax.set_xlabel('Date', fontsize=11)
ax.set_ylabel('GSOBench Score (%)', fontsize=11)
ax.set_title('GSOBench SOTA Progression with Sigmoid Fit', fontsize=13)
ax.set_ylim(0, 100)
ax.legend(loc='upper left', fontsize=9)
ax.grid(True, alpha=0.3)

# Add horizontal line at ceiling
ax.axhline(ceiling, color='orange', linestyle='--', alpha=0.5, label=f'Ceiling ({ceiling}%)')

plt.tight_layout()
plt.savefig('/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/gso_sigmoid_plot.png', dpi=150)
print("Saved plot to data/2026_predictions/gso_sigmoid_plot.png")

# Also print key stats
print(f"\nKey statistics:")
print(f"  Fitted k (steepness): {k:.5f}")
print(f"  Fitted midpoint: {midpoint_date.strftime('%Y-%m-%d')}")
print(f"  Current score: {current_score}%")
print(f"  Dec 2026 projection: {projection:.1f}%")
print(f"  Final prediction: 74% (10th: 45%, 90th: 95%)")
