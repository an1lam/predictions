#!/usr/bin/env python3
"""
Epoch Capabilities Index (ECI) Plot

Creates a visualization of the SOTA progression with linear fit and projection.
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Load data
data_path = "/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/epoch_capabilities_index.csv"
df = pd.read_csv(data_path)

# Clean data
df = df[df['ECI Score'].notna()]
df['Release date'] = pd.to_datetime(df['Release date'])
df = df.sort_values('Release date')

# Extract SOTA progression
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

# Convert dates to numeric for regression
reference_date = sota_df['date'].min()
sota_df['days'] = (sota_df['date'] - reference_date).dt.days

# Linear regression
x = sota_df['days'].values
y = sota_df['score'].values
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

# Calculate bounds
n = len(x)
t_val_90 = stats.t.ppf(0.90, n - 2)
t_val_10 = stats.t.ppf(0.10, n - 2)
slope_p10 = slope + t_val_10 * std_err
slope_p90 = slope + t_val_90 * std_err

# Create figure
fig, ax = plt.subplots(figsize=(12, 7))

# Plot all models as light gray dots
ax.scatter(df['Release date'], df['ECI Score'], alpha=0.2, s=20, c='gray', label='All models')

# Plot SOTA progression
ax.scatter(sota_df['date'], sota_df['score'], s=80, c='blue', zorder=5, label='SOTA frontier')

# Create date range for fit line (from first data to Dec 2026)
target_date = datetime(2026, 12, 31)
date_range = pd.date_range(start=reference_date, end=target_date, freq='M')
days_range = [(d - reference_date).days for d in date_range]

# Plot fit line and bounds
fit_central = [intercept + slope * d for d in days_range]
fit_p10 = [intercept + slope_p10 * d for d in days_range]
fit_p90 = [intercept + slope_p90 * d for d in days_range]

ax.plot(date_range, fit_central, 'r-', linewidth=2, label=f'Linear fit (R²={r_value**2:.2f})')
ax.fill_between(date_range, fit_p10, fit_p90, alpha=0.2, color='red', label='10th-90th percentile')

# Mark current SOTA
current_date = sota_df['date'].max()
current_score = sota_df['score'].max()
ax.annotate(f'Current: {current_score:.1f}',
            xy=(current_date, current_score),
            xytext=(current_date - timedelta(days=120), current_score + 5),
            fontsize=10,
            arrowprops=dict(arrowstyle='->', color='blue'))

# Mark projection
target_days = (target_date - reference_date).days
projection = intercept + slope * target_days
projection_p10 = intercept + slope_p10 * target_days
projection_p90 = intercept + slope_p90 * target_days

# Widened bounds for out-of-model error
projection_wide_p10 = 160
projection_wide_p90 = 195

ax.scatter([target_date], [177], s=150, c='green', marker='*', zorder=10, label='Prediction: 177')
ax.errorbar(target_date, 177, yerr=[[177-160], [195-177]],
            fmt='none', c='green', capsize=5, capthick=2, linewidth=2)

ax.annotate(f'Prediction: 177\n(160-195)',
            xy=(target_date, 177),
            xytext=(target_date - timedelta(days=180), 185),
            fontsize=10,
            arrowprops=dict(arrowstyle='->', color='green'))

# Formatting
ax.set_xlabel('Date', fontsize=12)
ax.set_ylabel('ECI Score', fontsize=12)
ax.set_title('Epoch Capabilities Index: SOTA Progression and Projection', fontsize=14)
ax.legend(loc='lower right')
ax.grid(True, alpha=0.3)

# Format x-axis
ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.xticks(rotation=45)

# Add vertical line for "today"
today = datetime(2025, 12, 17)
ax.axvline(x=today, color='gray', linestyle='--', alpha=0.5)
ax.text(today, ax.get_ylim()[0] + 5, 'Today', ha='center', fontsize=9, color='gray')

plt.tight_layout()

# Save figure
output_path = "/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/eci_progression_plot.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Plot saved to: {output_path}")

plt.show()
