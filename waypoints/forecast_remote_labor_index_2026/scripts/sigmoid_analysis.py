"""
Analyze sigmoid dynamics of benchmark progress, focusing on FrontierMath
as a better reference class for RLI (both start at very low scores).
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

# FrontierMath trajectory - ALL data points (we'll compute frontier from this)
frontiermath_all = [
    ("2024-06-20", 1.0, "Claude 3.5 Sonnet"),
    ("2024-08-06", 0.3, "GPT-4o"),
    ("2024-09-12", 1.7, "o1-mini-medium"),
    ("2024-10-22", 2.1, "Claude 3.5 Sonnet v2"),
    ("2024-12-17", 9.3, "o1-high"),
    ("2024-12-26", 1.7, "DeepSeek-V3"),
    ("2025-01-31", 12.4, "o3-mini-high"),
    ("2025-02-24", 4.1, "Claude 3.7 Sonnet"),
    ("2025-04-09", 5.9, "Grok-3-mini-high"),
    ("2025-04-14", 5.5, "GPT-4.1"),
    ("2025-04-16", 18.7, "o3-high"),
    ("2025-04-16", 24.8, "o4-mini-high"),
    ("2025-05-22", 4.5, "Claude Opus 4"),
    ("2025-06-05", 10.3, "Gemini 2.5 Pro"),
    ("2025-07-09", 19.7, "Grok 4"),
    ("2025-08-01", 29.0, "Gemini 2.5 Deep Think"),
    ("2025-08-07", 32.4, "GPT-5-high"),
    ("2025-09-29", 15.2, "Claude Sonnet 4.5"),
    ("2025-11-13", 31.0, "GPT-5.1-high"),
    ("2025-11-18", 37.6, "Gemini 3 Pro"),
    ("2025-11-24", 20.7, "Claude Opus 4.5"),
    ("2025-12-11", 40.3, "GPT-5.2-high"),
]

# SWE-bench trajectory (for comparison - started higher)
swebench_all = [
    ("2024-06-20", 32.0, "Claude 3.5 Sonnet"),
    ("2024-10-22", 40.6, "Claude 3.5 Sonnet v2"),
    ("2024-11-20", 25.4, "GPT-4o"),
    ("2025-01-31", 37.8, "o3-mini"),
    ("2025-02-24", 52.2, "Claude 3.7 Sonnet"),
    ("2025-04-14", 41.0, "GPT-4.1"),
    ("2025-04-16", 43.7, "o3"),
    ("2025-05-22", 60.6, "Claude Sonnet 4"),
    ("2025-05-28", 33.3, "DeepSeek-R1"),
    ("2025-08-05", 63.2, "Claude Opus 4.1"),
    ("2025-08-07", 58.8, "GPT-5"),
    ("2025-09-29", 64.8, "Claude Sonnet 4.5"),
]

def compute_frontier(data):
    """Compute monotonically increasing frontier (best score at each point in time)."""
    # Sort by date
    sorted_data = sorted(data, key=lambda x: datetime.strptime(x[0], "%Y-%m-%d"))

    frontier = []
    best_score = 0
    for date, score, model in sorted_data:
        if score > best_score:
            best_score = score
            frontier.append((date, score, model))

    return frontier

def parse_data(data):
    dates = [datetime.strptime(d[0], "%Y-%m-%d") for d in data]
    scores = [d[1] for d in data]
    models = [d[2] for d in data]
    return dates, scores, models

# Compute frontiers
frontiermath_frontier = compute_frontier(frontiermath_all)
swebench_frontier = compute_frontier(swebench_all)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: FrontierMath frontier trajectory
ax1 = axes[0]
dates_fm, scores_fm, models_fm = parse_data(frontiermath_frontier)

ax1.step(dates_fm, scores_fm, where='post', color='blue', linewidth=2, alpha=0.8)
ax1.scatter(dates_fm, scores_fm, s=60, c='blue', zorder=5)

# Annotate key models
for i, (date, score, model) in enumerate(frontiermath_frontier):
    if score in [1.0, 9.3, 24.8, 32.4, 40.3]:  # Key milestones
        ax1.annotate(f'{model}\n({score}%)',
                     xy=(datetime.strptime(date, "%Y-%m-%d"), score),
                     xytext=(5, 5), textcoords='offset points', fontsize=7,
                     alpha=0.8)

ax1.set_ylabel('Best Score (%)', fontsize=12)
ax1.set_xlabel('Date', fontsize=12)
ax1.set_title('FrontierMath: Frontier from Low Scores\n(1% → 40% in 18 months)', fontsize=12)
ax1.set_ylim(0, 50)
ax1.grid(True, alpha=0.3)
ax1.axhline(y=3.75, color='red', linestyle='--', linewidth=2, label='Current RLI (3.75%)')
ax1.legend(loc='upper left')

# Add shaded region showing where RLI is relative to FM trajectory
ax1.fill_between([datetime(2024, 6, 1), datetime(2025, 1, 1)], 0, 10,
                  alpha=0.1, color='red', label='RLI-analogous region')

# Plot 2: SWE-bench frontier trajectory (started in middle of sigmoid)
ax2 = axes[1]
dates_swe, scores_swe, models_swe = parse_data(swebench_frontier)

ax2.step(dates_swe, scores_swe, where='post', color='green', linewidth=2, alpha=0.8)
ax2.scatter(dates_swe, scores_swe, s=60, c='green', zorder=5)

ax2.set_ylabel('Best Score (%)', fontsize=12)
ax2.set_xlabel('Date', fontsize=12)
ax2.set_title('SWE-bench: Frontier from Mid-Range\n(32% → 65% in 15 months)', fontsize=12)
ax2.set_ylim(0, 80)
ax2.grid(True, alpha=0.3)

ax2.annotate('Started in steep\nmiddle of sigmoid',
             xy=(datetime(2024, 6, 20), 32), fontsize=9,
             xytext=(datetime(2024, 9, 1), 55),
             arrowprops=dict(arrowstyle='->', color='gray'))

plt.tight_layout()
plt.savefig('waypoints/forecast_remote_labor_index_2026/plots/sigmoid_comparison.png', dpi=150, bbox_inches='tight')
print("Saved: waypoints/forecast_remote_labor_index_2026/plots/sigmoid_comparison.png")

# Print frontier data
print("\n" + "=" * 60)
print("FRONTIERMATH FRONTIER (monotonically increasing best scores)")
print("=" * 60)
for date, score, model in frontiermath_frontier:
    print(f"  {date}: {score:5.1f}% - {model}")

print("\n" + "=" * 60)
print("SWE-BENCH FRONTIER")
print("=" * 60)
for date, score, model in swebench_frontier:
    print(f"  {date}: {score:5.1f}% - {model}")

# Analysis
print("\n" + "=" * 60)
print("SIGMOID DYNAMICS ANALYSIS")
print("=" * 60)

print("\nFrontierMath frontier (starting low, like RLI):")
print(f"  Start: {frontiermath_frontier[0][1]}% ({frontiermath_frontier[0][0]})")
print(f"  End: {frontiermath_frontier[-1][1]}% ({frontiermath_frontier[-1][0]})")
total_months_fm = (datetime.strptime(frontiermath_frontier[-1][0], "%Y-%m-%d") -
                   datetime.strptime(frontiermath_frontier[0][0], "%Y-%m-%d")).days / 30.44
print(f"  Period: {total_months_fm:.1f} months")
print(f"  Improvement: {frontiermath_frontier[-1][1] / frontiermath_frontier[0][1]:.1f}x")

print("\nSWE-bench frontier (starting mid-range):")
print(f"  Start: {swebench_frontier[0][1]}% ({swebench_frontier[0][0]})")
print(f"  End: {swebench_frontier[-1][1]}% ({swebench_frontier[-1][0]})")
total_months_swe = (datetime.strptime(swebench_frontier[-1][0], "%Y-%m-%d") -
                    datetime.strptime(swebench_frontier[0][0], "%Y-%m-%d")).days / 30.44
print(f"  Period: {total_months_swe:.1f} months")
print(f"  Improvement: {swebench_frontier[-1][1] / swebench_frontier[0][1]:.1f}x")

print("\n" + "=" * 60)
print("RLI EXTRAPOLATION USING FRONTIERMATH DYNAMICS")
print("=" * 60)

scenarios = {
    "Conservative (SWE-bench 2x trajectory)": 3.75 * 2,
    "Moderate (FrontierMath Jan-Dec 2025 pace, ~5x)": 3.75 * 5,
    "Aggressive (FrontierMath full 40x trajectory, time-adjusted)": 3.75 * (40 ** (11.5/18)),
}

print("\nRLI projections for end of 2026 (from 3.75%):")
for scenario, value in scenarios.items():
    print(f"  {scenario}: {value:.1f}%")
