#!/usr/bin/env python3
"""
METR Time Horizon Analysis with Visualization.

Plots time horizon progression with regression fits for full and recent periods.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime, timedelta

def calculate_doubling_time_with_ci(x, y):
    """Calculate doubling time with 10th/90th percentile bounds."""
    n = len(x)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    t_val_90 = stats.t.ppf(0.90, n - 2)
    t_val_10 = stats.t.ppf(0.10, n - 2)

    slope_p10 = slope + t_val_10 * std_err
    slope_p90 = slope + t_val_90 * std_err

    doubling_days = 1 / slope
    doubling_p10 = 1 / slope_p90
    doubling_p90 = 1 / slope_p10

    return {
        'doubling_days': doubling_days,
        'doubling_months': doubling_days / 30.44,
        'p10_months': doubling_p10 / 30.44,
        'p90_months': doubling_p90 / 30.44,
        'r_squared': r_value**2,
        'n': n,
        'slope': slope,
        'intercept': intercept,
        'std_err': std_err
    }

# Load data
df = pd.read_csv('data/2026_predictions/metr_time_horizons_external.csv')
df = df[df['Release date'].notna()].copy()
df['Release date'] = pd.to_datetime(df['Release date'])
df = df.sort_values('Release date')

# Convert to log scale
df['log_horizon'] = np.log2(df['Time horizon'])
df['days_since_start'] = (df['Release date'] - df['Release date'].min()).dt.days

# Calculate regressions
result_full = calculate_doubling_time_with_ci(df['days_since_start'], df['log_horizon'])

recent = df[df['Release date'] >= '2024-01-01'].copy()
recent['days_since_start'] = (recent['Release date'] - recent['Release date'].min()).dt.days
result_recent = calculate_doubling_time_with_ci(recent['days_since_start'], recent['log_horizon'])

# Create plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot actual data points
ax.scatter(df['Release date'], df['Time horizon'], color='blue', s=50, alpha=0.7,
           label='Model time horizons', zorder=5)

# Generate regression lines
start_date = df['Release date'].min()
end_date = datetime(2026, 12, 31)

# Full period regression line
full_days = np.array([0, (end_date - start_date).days])
full_log_pred = result_full['intercept'] + result_full['slope'] * full_days
full_pred = 2 ** full_log_pred
full_dates = [start_date + timedelta(days=int(d)) for d in full_days]
ax.plot(full_dates, full_pred, 'g--', linewidth=2, alpha=0.7,
        label=f'Full period trend ({result_full["doubling_months"]:.1f} mo doubling)')

# Recent period regression line (extend from 2024 start)
recent_start = datetime(2024, 1, 1)
recent_days_range = np.array([0, (end_date - recent_start).days])
recent_log_pred = result_recent['intercept'] + result_recent['slope'] * recent_days_range
recent_pred = 2 ** recent_log_pred
recent_dates = [recent_start + timedelta(days=int(d)) for d in recent_days_range]
ax.plot(recent_dates, recent_pred, 'r-', linewidth=2, alpha=0.7,
        label=f'Recent trend ({result_recent["doubling_months"]:.1f} mo doubling)')

# Mark current SOTA
current_sota = df.loc[df['Time horizon'].idxmax()]
ax.scatter([current_sota['Release date']], [current_sota['Time horizon']],
           color='darkblue', s=150, marker='*', zorder=6,
           label=f'Current SOTA ({current_sota["Time horizon"]:.0f} min)')

# Mark Dec 2026 projection (using recent trend)
dec_2026_days = (end_date - recent_start).days
dec_2026_log = result_recent['intercept'] + result_recent['slope'] * dec_2026_days
dec_2026_pred = 2 ** dec_2026_log
ax.scatter([end_date], [dec_2026_pred], color='red', s=150, marker='D', zorder=6,
           label=f'Dec 2026 projection ({dec_2026_pred:.0f} min)')

# Add prediction info box
pred_text = (f"Our prediction: 4.5 mo\n"
             f"(10th: 3.0, 90th: 6.5)")
ax.annotate(pred_text, xy=(0.02, 0.98), xycoords='axes fraction',
            fontsize=10, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Formatting
ax.set_yscale('log', base=2)
ax.set_xlabel('Release Date', fontsize=11)
ax.set_ylabel('Time Horizon (minutes, log scale)', fontsize=11)
ax.set_title('METR Time Horizon Progression', fontsize=13)
ax.legend(loc='lower right', fontsize=9)
ax.grid(True, alpha=0.3, which='both')

# Set y-axis to show nice tick labels
yticks = [0.1, 1, 10, 60, 360, 1440, 10080]  # 0.1min to 1 week
ytick_labels = ['6s', '1m', '10m', '1h', '6h', '1d', '1w']
ax.set_yticks(yticks)
ax.set_yticklabels(ytick_labels)
ax.set_ylim(0.01, 20000)

plt.tight_layout()
plt.savefig('data/2026_predictions/metr_horizon_plot.png', dpi=150)
print("Saved plot to data/2026_predictions/metr_horizon_plot.png")

# Print summary stats
print(f"\nFull period: {result_full['doubling_months']:.2f} mo [{result_full['p10_months']:.2f}, {result_full['p90_months']:.2f}]")
print(f"Recent (2024+): {result_recent['doubling_months']:.2f} mo [{result_recent['p10_months']:.2f}, {result_recent['p90_months']:.2f}]")
print(f"Dec 2026 projection (recent trend): {dec_2026_pred:.0f} min ({dec_2026_pred/60:.1f} hrs)")
