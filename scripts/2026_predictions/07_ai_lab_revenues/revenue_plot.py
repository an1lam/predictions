#!/usr/bin/env python3
"""
AI Lab Revenue Visualization

Creates plots showing historical revenue and projections for OpenAI, Anthropic, xAI.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta

# Load revenue data
data_path = "/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/ai_companies/ai_companies_revenue_reports.csv"
df = pd.read_csv(data_path)

# Filter for our companies and annualized revenue
companies = ['OpenAI', 'Anthropic', 'xAI']
df = df[df['Company'].isin(companies)]
df['Date'] = pd.to_datetime(df['Date'])
df = df[df['Annualized revenue (USD)'].notna()]
df['Revenue_B'] = df['Annualized revenue (USD)'] / 1e9
df = df.sort_values(['Company', 'Date'])

# Create figure with two subplots
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Colors for each company
colors = {'OpenAI': '#10a37f', 'Anthropic': '#d4a574', 'xAI': '#1da1f2'}

# --- Plot 1: Historical Revenue by Company ---
ax1 = axes[0]

for company in companies:
    company_df = df[df['Company'] == company]
    ax1.scatter(company_df['Date'], company_df['Revenue_B'],
                label=company, color=colors[company], s=50, alpha=0.7)
    # Connect with lines
    ax1.plot(company_df['Date'], company_df['Revenue_B'],
             color=colors[company], alpha=0.5, linestyle='-')

ax1.set_xlabel('Date', fontsize=11)
ax1.set_ylabel('Annualized Revenue ($B)', fontsize=11)
ax1.set_title('AI Lab Revenue Growth (2023-2025)', fontsize=12)
ax1.legend(loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)

# --- Plot 2: Combined Revenue with Projections ---
ax2 = axes[1]

# Survey baseline data points
historical_points = [
    (datetime(2024, 12, 31), 6.6),   # Dec 2024
    (datetime(2025, 12, 31), 30.8),  # Dec 2025 (current)
]

# Plot historical combined
hist_dates = [p[0] for p in historical_points]
hist_values = [p[1] for p in historical_points]
ax2.scatter(hist_dates, hist_values, s=100, c='blue', zorder=5, label='Historical (combined)')
ax2.plot(hist_dates, hist_values, 'b-', linewidth=2, alpha=0.7)

# Annotate historical
ax2.annotate(f'Dec 2024\n$6.6B', xy=(hist_dates[0], hist_values[0]),
             xytext=(hist_dates[0] - timedelta(days=60), hist_values[0] + 8),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='blue'))
ax2.annotate(f'Dec 2025\n$30.8B', xy=(hist_dates[1], hist_values[1]),
             xytext=(hist_dates[1] - timedelta(days=90), hist_values[1] + 12),
             fontsize=9, arrowprops=dict(arrowstyle='->', color='blue'))

# Projection scenarios to Dec 2026
target_date = datetime(2026, 12, 31)

# Model A: Company projections ($74B)
# Model B: Reference class ($52B)
# Model C: Slowdown ($40B)
# Weighted: $60B

scenarios = [
    ('Model A: Company projections', 74, 'green', '--'),
    ('Model B: Reference class', 52, 'orange', '--'),
    ('Model C: Slowdown', 40, 'red', '--'),
]

for name, value, color, style in scenarios:
    ax2.plot([hist_dates[1], target_date], [hist_values[1], value],
             color=color, linestyle=style, linewidth=1.5, alpha=0.6)
    ax2.scatter([target_date], [value], color=color, s=40, alpha=0.6)

# Weighted prediction with error bars
prediction = 60
p10 = 35
p90 = 90

ax2.scatter([target_date], [prediction], s=150, c='purple', marker='*',
            zorder=10, label=f'Prediction: ${prediction}B')
ax2.errorbar(target_date, prediction, yerr=[[prediction-p10], [p90-prediction]],
             fmt='none', c='purple', capsize=5, capthick=2, linewidth=2)

ax2.annotate(f'Prediction\n${prediction}B\n({p10}-{p90})',
             xy=(target_date, prediction),
             xytext=(target_date - timedelta(days=120), prediction + 15),
             fontsize=10, color='purple',
             arrowprops=dict(arrowstyle='->', color='purple'))

# Add scenario labels
ax2.text(target_date + timedelta(days=10), 74, 'A: $74B', fontsize=8, color='green', va='center')
ax2.text(target_date + timedelta(days=10), 52, 'B: $52B', fontsize=8, color='orange', va='center')
ax2.text(target_date + timedelta(days=10), 40, 'C: $40B', fontsize=8, color='red', va='center')

ax2.set_xlabel('Date', fontsize=11)
ax2.set_ylabel('Combined Revenue ($B)', fontsize=11)
ax2.set_title('Combined AI Lab Revenue: History & Projection', fontsize=12)
ax2.legend(loc='upper left')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(datetime(2024, 9, 1), datetime(2027, 3, 1))
ax2.set_ylim(0, 100)
ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=4))
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=45)

# Add "4.7x YoY" annotation
mid_date = datetime(2025, 6, 1)
ax2.annotate('4.7x YoY\ngrowth', xy=(mid_date, 18), fontsize=9,
             ha='center', style='italic', color='gray')

plt.tight_layout()

# Save figure
output_path = "/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/ai_lab_revenue_plot.png"
plt.savefig(output_path, dpi=150, bbox_inches='tight')
print(f"Plot saved to: {output_path}")

plt.show()
