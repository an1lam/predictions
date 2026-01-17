#!/usr/bin/env python3
"""
GSO Benchmark Progression Analysis

Analyzes the historical progression of scores on GSOBench to inform
predictions for Dec 31, 2026.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Load data
data_path = "/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/gso_external.csv"
df = pd.read_csv(data_path)

# Convert to percentages for easier interpretation
df['Score_pct'] = df['Score OPT@1'] * 100

# Parse release dates
df['Release date'] = pd.to_datetime(df['Release date'])

# Sort by date
df = df.sort_values('Release date')

print("=" * 80)
print("GSO BENCHMARK PROGRESSION ANALYSIS")
print("=" * 80)

print("\n### Full History (sorted by date)")
print("-" * 80)
for _, row in df.iterrows():
    model = row['Model version'] if pd.notna(row['Model version']) else 'Unknown'
    org = row['Organization'] if pd.notna(row['Organization']) else 'Unknown'
    date = row['Release date'].strftime('%Y-%m-%d')
    score = row['Score_pct']
    print(f"{date}: {score:5.1f}% - {model[:40]:<40} ({org})")

# Track SOTA progression
print("\n### SOTA Progression")
print("-" * 80)
sota_progression = []
current_sota = 0
for _, row in df.iterrows():
    if row['Score_pct'] > current_sota:
        current_sota = row['Score_pct']
        sota_progression.append({
            'date': row['Release date'],
            'score': current_sota,
            'model': row['Model version'],
            'org': row['Organization']
        })
        date_str = row['Release date'].strftime('%Y-%m-%d')
        model = row['Model version'] if pd.notna(row['Model version']) else 'Unknown'
        print(f"{date_str}: {current_sota:5.1f}% - {model}")

sota_df = pd.DataFrame(sota_progression)

# Calculate velocity at different periods
print("\n### Velocity Analysis")
print("-" * 80)

if len(sota_df) >= 2:
    # Recent velocity (last 6 months)
    cutoff_6mo = datetime.now() - timedelta(days=180)
    recent_sota = sota_df[sota_df['date'] >= cutoff_6mo]

    if len(recent_sota) >= 2:
        first_recent = recent_sota.iloc[0]
        last_recent = recent_sota.iloc[-1]
        days_diff = (last_recent['date'] - first_recent['date']).days
        score_diff = last_recent['score'] - first_recent['score']
        if days_diff > 0:
            velocity_recent = score_diff / (days_diff / 30)  # pp per month
            print(f"Last 6 months: {first_recent['score']:.1f}% -> {last_recent['score']:.1f}%")
            print(f"  Change: +{score_diff:.1f}pp over {days_diff} days")
            print(f"  Velocity: {velocity_recent:.2f} pp/month")

    # Full period velocity
    first = sota_df.iloc[0]
    last = sota_df.iloc[-1]
    days_total = (last['date'] - first['date']).days
    score_total = last['score'] - first['score']
    if days_total > 0:
        velocity_total = score_total / (days_total / 30)
        print(f"\nFull period: {first['score']:.1f}% -> {last['score']:.1f}%")
        print(f"  From: {first['date'].strftime('%Y-%m-%d')} to {last['date'].strftime('%Y-%m-%d')}")
        print(f"  Change: +{score_total:.1f}pp over {days_total} days ({days_total/30:.1f} months)")
        print(f"  Velocity: {velocity_total:.2f} pp/month")

# Project forward to Dec 31, 2026
print("\n### Projections to Dec 31, 2026")
print("-" * 80)

current_score = 27.4  # GPT-5.2 raw score
current_date = datetime(2025, 12, 11)
target_date = datetime(2026, 12, 31)
months_remaining = (target_date - current_date).days / 30

print(f"Current SOTA: {current_score:.1f}% (as of Dec 2025)")
print(f"Months to Dec 31, 2026: {months_remaining:.1f}")

# Different velocity scenarios
print("\nScenarios based on different velocity assumptions:")

scenarios = [
    ("Conservative (1.5 pp/mo - slowdown)", 1.5),
    ("Moderate (3.0 pp/mo - slight decel)", 3.0),
    ("Recent trend (5.0 pp/mo)", 5.0),
    ("Accelerated (7.0 pp/mo)", 7.0),
]

for name, velocity in scenarios:
    projected = current_score + velocity * months_remaining
    projected = min(projected, 100)  # Cap at 100%
    print(f"  {name}: {projected:.1f}%")

# Compare with other benchmarks we've analyzed
print("\n### Reference Class: Mid-Stage Benchmark Velocities")
print("-" * 80)
print("(From our previous analysis)")
print("  SWE-Bench (20-40% range): ~3-4 pp/month")
print("  FrontierMath Tier 4 (20-30%): ~4.3 pp/month")
print("  ARC-AGI (20-40% range): ~3-4 pp/month")
print("  OSWorld (20-40% range): ~3-4 pp/month")
print("\nGSO recent velocity (~5 pp/mo) is notably faster than these benchmarks")
