#!/usr/bin/env python3
"""
FrontierMath Tier 4 Visualization with Multi-Model Scenarios.

Plots SOTA progression with three scenario projections to Dec 2026.
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Load data
df = pd.read_csv('data/2026_predictions/frontiermath_tier_4.csv')
df = df[df['Release date'].notna()].copy()
df['Release date'] = pd.to_datetime(df['Release date'])
df = df.sort_values('Release date')
df['score_pct'] = df['mean_score'] * 100

# Extract SOTA progression (cumulative max over time)
df_sorted = df.sort_values('Release date')
sota_progression = []
current_sota = 0
for _, row in df_sorted.iterrows():
    if row['score_pct'] > current_sota:
        current_sota = row['score_pct']
        sota_progression.append({
            'date': row['Release date'],
            'score': current_sota,
            'model': row['Model version']
        })

sota_df = pd.DataFrame(sota_progression)

# Key dates
first_nonzero = sota_df['date'].min()
target_date = datetime(2026, 12, 31)
current_date = datetime(2025, 12, 11)
current_score = 29.2  # GPT-5.2 Pro

# Calculate months from current to target
months_to_target = 12  # roughly Dec 2025 to Dec 2026

# Create the plot
fig, ax = plt.subplots(figsize=(10, 6))

# Plot all model scores as light scatter
ax.scatter(df['Release date'], df['score_pct'], color='lightblue', s=30, alpha=0.5,
           label='All models', zorder=3)

# Plot SOTA progression
ax.scatter(sota_df['date'], sota_df['score'], color='blue', s=70, zorder=5,
           label='SOTA progression')
ax.plot(sota_df['date'], sota_df['score'], 'b-', alpha=0.5, zorder=4)

# Mark current SOTA
ax.scatter([current_date], [current_score], color='darkblue', s=150, marker='*', zorder=6,
           label=f'Current SOTA ({current_score}%)')

# Project three scenarios to Dec 2026
# Generate projection points from current date to target
proj_dates = [current_date + timedelta(days=30*i) for i in range(13)]
proj_months = list(range(13))

# Model A: Linear trend (2.6%/month)
linear_rate = 2.6
linear_proj = [current_score + linear_rate * m for m in proj_months]
ax.plot(proj_dates, linear_proj, 'g--', linewidth=2, alpha=0.7,
        label=f'Model A: Linear ({linear_rate}%/mo) → {linear_proj[-1]:.0f}%')

# Model B: Accelerated (4.2%/month)
accel_rate = 4.2
accel_proj = [current_score + accel_rate * m for m in proj_months]
ax.plot(proj_dates, accel_proj, 'r--', linewidth=2, alpha=0.7,
        label=f'Model B: Accelerated ({accel_rate}%/mo) → {accel_proj[-1]:.0f}%')

# Model C: Ceiling/diminishing (1.5%/month)
ceiling_rate = 1.5
ceiling_proj = [current_score + ceiling_rate * m for m in proj_months]
ax.plot(proj_dates, ceiling_proj, 'orange', linestyle='--', linewidth=2, alpha=0.7,
        label=f'Model C: Ceiling ({ceiling_rate}%/mo) → {ceiling_proj[-1]:.0f}%')

# Mark Dec 2026 weighted prediction
weighted_pred = 62
ax.scatter([target_date], [weighted_pred], color='purple', s=150, marker='D', zorder=6,
           label=f'Weighted prediction: {weighted_pred}%')

# Add prediction interval band at Dec 2026 (10th: 40%, 90th: 85%)
ax.axhspan(40, 85, xmin=0.85, xmax=1.0, alpha=0.2, color='purple')

# Add horizontal reference lines
ax.axhline(100, color='gray', linestyle=':', alpha=0.3)
ax.axhline(50, color='gray', linestyle=':', alpha=0.3)

# Add prediction info box
pred_text = (f"Weighted prediction: {weighted_pred}%\n"
             f"(10th: 40%, 90th: 85%)\n\n"
             f"Weights:\n"
             f"  A (Linear): 40%\n"
             f"  B (Accel): 30%\n"
             f"  C (Ceiling): 30%")
ax.annotate(pred_text, xy=(0.02, 0.98), xycoords='axes fraction',
            fontsize=9, verticalalignment='top',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

# Formatting
ax.set_xlabel('Release Date', fontsize=11)
ax.set_ylabel('FrontierMath Tier 4 Score (%)', fontsize=11)
ax.set_title('FrontierMath Tier 4 SOTA Progression with Scenario Projections', fontsize=13)
ax.set_ylim(0, 100)
ax.legend(loc='lower right', fontsize=8)
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('data/2026_predictions/frontiermath_tier4_plot.png', dpi=150)
print("Saved plot to data/2026_predictions/frontiermath_tier4_plot.png")

# Print summary
print(f"\nCurrent SOTA: {current_score}% (Dec 2025)")
print(f"\nDec 2026 projections:")
print(f"  Model A (Linear, 40% weight): {linear_proj[-1]:.0f}%")
print(f"  Model B (Accelerated, 30% weight): {accel_proj[-1]:.0f}%")
print(f"  Model C (Ceiling, 30% weight): {ceiling_proj[-1]:.0f}%")
print(f"  Weighted: 0.4×{linear_proj[-1]:.0f} + 0.3×{accel_proj[-1]:.0f} + 0.3×{ceiling_proj[-1]:.0f} = {0.4*linear_proj[-1] + 0.3*accel_proj[-1] + 0.3*ceiling_proj[-1]:.0f}%")
