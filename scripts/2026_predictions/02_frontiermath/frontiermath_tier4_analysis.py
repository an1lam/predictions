"""Analyze FrontierMath Tier 4 benchmark progress."""
import pandas as pd
import numpy as np
from scipy import stats

df = pd.read_csv('data/2026_predictions/frontiermath_tier_4.csv')

# Clean up and sort by release date
df = df[df['Release date'].notna()].copy()
df['Release date'] = pd.to_datetime(df['Release date'])
df = df.sort_values('Release date')

# Get best score per month to see frontier progress
df['month'] = df['Release date'].dt.to_period('M')
frontier = df.groupby('month')['mean_score'].max().reset_index()
frontier['month_date'] = frontier['month'].dt.to_timestamp()

print("=== FrontierMath Tier 4 - Top Performers ===\n")
top = df.nlargest(10, 'mean_score')[['Model version', 'mean_score', 'Release date', 'Organization']]
top['mean_score'] = (top['mean_score'] * 100).round(1).astype(str) + '%'
print(top.to_string(index=False))

print("\n\n=== Frontier Progress by Month ===\n")
frontier['score_pct'] = (frontier['mean_score'] * 100).round(1)
print(frontier[['month', 'score_pct']].to_string(index=False))

# Calculate progress rate for models with score > 0
nonzero = df[df['mean_score'] > 0].copy()
nonzero['days_since_start'] = (nonzero['Release date'] - nonzero['Release date'].min()).dt.days
nonzero['score_pct'] = nonzero['mean_score'] * 100

if len(nonzero) > 2:
    slope, intercept, r_value, p_value, std_err = stats.linregress(
        nonzero['days_since_start'], nonzero['score_pct']
    )
    print(f"\n\n=== Linear Trend (non-zero scores) ===")
    print(f"Slope: {slope:.3f}% per day = {slope * 30.44:.1f}% per month")
    print(f"R²: {r_value**2:.3f}")
    print(f"N: {len(nonzero)}")

# Key milestones
print("\n\n=== Key Milestones ===")
print(f"First non-zero score: {df[df['mean_score'] > 0]['Release date'].min().strftime('%Y-%m-%d')}")
print(f"First >10%: {df[df['mean_score'] > 0.10]['Release date'].min().strftime('%Y-%m-%d') if len(df[df['mean_score'] > 0.10]) > 0 else 'N/A'}")
print(f"First >20%: {df[df['mean_score'] > 0.20]['Release date'].min().strftime('%Y-%m-%d') if len(df[df['mean_score'] > 0.20]) > 0 else 'N/A'}")
print(f"Current best: {df['mean_score'].max() * 100:.1f}% ({df.loc[df['mean_score'].idxmax(), 'Model version']})")
