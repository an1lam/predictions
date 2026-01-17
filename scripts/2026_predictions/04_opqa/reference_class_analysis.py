"""Analyze reference class benchmarks for OPQA prediction."""
import pandas as pd
import numpy as np

def analyze_benchmark_progression(filepath, name, score_col='mean_score', score_is_pct=False):
    df = pd.read_csv(filepath)
    df = df[df['Release date'].notna()].copy()
    df['Release date'] = pd.to_datetime(df['Release date'])
    df = df.sort_values('Release date')

    # Normalize scores
    if score_is_pct:
        df['score'] = df[score_col] / 100
    else:
        df['score'] = df[score_col]

    # Track cumulative frontier
    df['frontier'] = df['score'].cummax()

    # Get frontier progression (unique max values)
    frontier_changes = df.groupby('frontier').first().reset_index()
    frontier_changes = frontier_changes.sort_values('Release date')

    print(f"\n{'='*70}")
    print(f"=== {name} ===")
    print(f"{'='*70}")

    # Full progression
    print(f"\nFrontier progression:")
    for _, row in frontier_changes.iterrows():
        print(f"  {row['Release date'].strftime('%Y-%m-%d')}: {row['frontier']*100:.1f}%")

    # Calculate velocities at different stages
    print(f"\nVelocity analysis:")

    stages = [
        (0.00, 0.10, "0-10%"),
        (0.05, 0.15, "5-15%"),
        (0.10, 0.20, "10-20%"),
        (0.10, 0.30, "10-30%"),
        (0.20, 0.40, "20-40%"),
        (0.30, 0.50, "30-50%"),
    ]

    for low, high, label in stages:
        stage_data = frontier_changes[(frontier_changes['frontier'] >= low) & (frontier_changes['frontier'] <= high)]
        if len(stage_data) >= 2:
            first = stage_data.iloc[0]
            last = stage_data.iloc[-1]
            days = (last['Release date'] - first['Release date']).days
            if days > 0:
                gain = last['frontier'] - first['frontier']
                velocity = gain * 100 * 30.44 / days
                print(f"  {label}: {first['frontier']*100:.1f}% → {last['frontier']*100:.1f}% in {days} days ({velocity:.2f}pp/month)")

    # Time to reach milestones from ~5-10% starting point
    print(f"\nTime to milestones (from first entry):")
    first_date = frontier_changes.iloc[0]['Release date']
    first_score = frontier_changes.iloc[0]['frontier']

    milestones = [0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50]
    for m in milestones:
        reached = frontier_changes[frontier_changes['frontier'] >= m]
        if len(reached) > 0:
            first_reach = reached.iloc[0]
            days = (first_reach['Release date'] - first_date).days
            print(f"  {m*100:.0f}%: {days} days ({days/30.44:.1f} months) from {first_score*100:.1f}%")

    return frontier_changes

print("="*70)
print("REFERENCE CLASS ANALYSIS FOR OPQA (current: 8%)")
print("="*70)

# Analyze each benchmark
gpqa = analyze_benchmark_progression('data/2026_predictions/gpqa_diamond.csv', 'GPQA Diamond')
swe = analyze_benchmark_progression('data/2026_predictions/swe_bench_verified.csv', 'SWE-Bench Verified')
fm4 = analyze_benchmark_progression('data/2026_predictions/frontiermath_tier_4.csv', 'FrontierMath Tier 4')
fm = analyze_benchmark_progression('data/2026_predictions/frontiermath.csv', 'FrontierMath (all tiers)')
