"""Analyze benchmark trajectories for reference class comparison."""
import pandas as pd
import numpy as np

def analyze_benchmark(filepath, name, score_col='mean_score'):
    df = pd.read_csv(filepath)
    df = df[df['Release date'].notna()].copy()
    df['Release date'] = pd.to_datetime(df['Release date'])
    df = df.sort_values('Release date')

    # Get frontier (best score) over time
    df['month'] = df['Release date'].dt.to_period('M')

    # Cumulative max to track frontier
    df['frontier'] = df[score_col].cummax()

    # Get first and latest
    first = df.iloc[0]
    latest_frontier = df[score_col].max()
    latest_date = df[df[score_col] == latest_frontier]['Release date'].max()

    # Calculate improvement
    first_score = first[score_col]
    months_elapsed = (latest_date - first['Release date']).days / 30.44

    if first_score > 0:
        multiplier = latest_frontier / first_score
    else:
        multiplier = float('inf')

    abs_gain = latest_frontier - first_score

    print(f"\n=== {name} ===")
    print(f"First score: {first_score*100:.1f}% ({first['Release date'].strftime('%Y-%m')})")
    print(f"Latest frontier: {latest_frontier*100:.1f}% ({latest_date.strftime('%Y-%m')})")
    print(f"Months elapsed: {months_elapsed:.1f}")
    print(f"Absolute gain: +{abs_gain*100:.1f}pp")
    if multiplier != float('inf'):
        print(f"Multiplier: {multiplier:.2f}x")
    print(f"Monthly gain: {abs_gain*100/months_elapsed:.2f}pp/month")

    # Show progression
    frontier_by_month = df.groupby('month').apply(lambda x: x[score_col].max()).reset_index()
    frontier_by_month.columns = ['month', 'frontier']
    frontier_by_month['cummax'] = frontier_by_month['frontier'].cummax()
    print(f"\nFrontier progression (selected):")
    for i, row in frontier_by_month.iloc[::max(1, len(frontier_by_month)//6)].iterrows():
        print(f"  {row['month']}: {row['cummax']*100:.1f}%")
    print(f"  {frontier_by_month.iloc[-1]['month']}: {frontier_by_month.iloc[-1]['cummax']*100:.1f}%")

# Analyze each benchmark
analyze_benchmark('data/2026_predictions/swe_bench_verified.csv', 'SWE-Bench Verified')
analyze_benchmark('data/2026_predictions/arc_agi_external.csv', 'ARC-AGI', score_col='Score')
analyze_benchmark('data/2026_predictions/os_world_external.csv', 'OSWorld', score_col='Score')
