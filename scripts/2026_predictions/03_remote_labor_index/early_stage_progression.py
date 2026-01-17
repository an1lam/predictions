"""Analyze early-stage benchmark progression (from ~0 to meaningful scores)."""
import pandas as pd
import numpy as np

def analyze_early_stage(filepath, name, score_col='mean_score', score_is_pct=False):
    df = pd.read_csv(filepath)
    df = df[df['Release date'].notna()].copy()
    df['Release date'] = pd.to_datetime(df['Release date'])
    df = df.sort_values('Release date')

    # Normalize scores to 0-1 range if needed
    if score_is_pct:
        df['score'] = df[score_col] / 100
    else:
        df['score'] = df[score_col]

    # Track cumulative frontier
    df['frontier'] = df['score'].cummax()

    # Get unique frontier progression points
    frontier_changes = df[df['score'] == df['frontier']].copy()
    frontier_changes = frontier_changes.drop_duplicates(subset=['frontier'], keep='first')

    print(f"\n{'='*60}")
    print(f"=== {name} - Early Stage Progression ===")
    print(f"{'='*60}")

    print(f"\nFull frontier progression:")
    for _, row in frontier_changes.iterrows():
        print(f"  {row['Release date'].strftime('%Y-%m-%d')}: {row['frontier']*100:.1f}%")

    # Focus on early stage (scores < 20%)
    early = frontier_changes[frontier_changes['frontier'] < 0.20]
    if len(early) > 0:
        print(f"\nEarly stage (< 20%) progression:")
        for _, row in early.iterrows():
            print(f"  {row['Release date'].strftime('%Y-%m-%d')}: {row['frontier']*100:.1f}%")

        # Calculate early stage velocity
        if len(early) > 1:
            first = early.iloc[0]
            last = early.iloc[-1]
            days = (last['Release date'] - first['Release date']).days
            if days > 0:
                gain = last['frontier'] - first['frontier']
                print(f"\nEarly stage velocity: {gain*100:.1f}pp over {days} days = {gain*100*30.44/days:.2f}pp/month")

    # Transition from <10% to >10%
    below_10 = frontier_changes[frontier_changes['frontier'] < 0.10]
    above_10 = frontier_changes[frontier_changes['frontier'] >= 0.10]
    if len(below_10) > 0 and len(above_10) > 0:
        last_below = below_10.iloc[-1]
        first_above = above_10.iloc[0]
        days = (first_above['Release date'] - last_below['Release date']).days
        print(f"\nTransition from <10% to >10%:")
        print(f"  {last_below['frontier']*100:.1f}% ({last_below['Release date'].strftime('%Y-%m-%d')}) → {first_above['frontier']*100:.1f}% ({first_above['Release date'].strftime('%Y-%m-%d')})")
        print(f"  Time: {days} days ({days/30.44:.1f} months)")

# Analyze benchmarks
analyze_early_stage('data/2026_predictions/swe_bench_verified.csv', 'SWE-Bench Verified')
analyze_early_stage('data/2026_predictions/arc_agi_external.csv', 'ARC-AGI', score_col='Score')
analyze_early_stage('data/2026_predictions/frontiermath_tier_4.csv', 'FrontierMath Tier 4')

# For FrontierMath overall (not just tier 4)
analyze_early_stage('data/2026_predictions/frontiermath.csv', 'FrontierMath (all tiers)')
