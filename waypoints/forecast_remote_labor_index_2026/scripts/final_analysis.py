#!/usr/bin/env python
"""
Analysis script for: Remote Labor Index highest score by end of 2026
Generated: 2026-01-18

Reproduces the analysis for the RLI forecast.
Run with: uv run python waypoints/forecast_remote_labor_index_2026/scripts/final_analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json

# --- Configuration ---
TARGET_DATE = "2026-12-31"
PREDICTION_NAME = "Remote Labor Index - Highest Score"
CURRENT_SCORE = 3.75
CURRENT_DATE = "2026-01-16"

# --- Scenario Analysis ---
scenarios = {
    "Conservative": {"estimate": 10, "range": (8, 12), "weight": 0.25},
    "Moderate": {"estimate": 23, "range": (18, 28), "weight": 0.45},
    "Optimistic": {"estimate": 40, "range": (35, 45), "weight": 0.25},
    "Very Optimistic": {"estimate": 52, "range": (45, 60), "weight": 0.05},
}

# --- Weighted Estimate ---
weighted_estimate = sum(s["estimate"] * s["weight"] for s in scenarios.values())
print(f"Weighted scenario estimate: {weighted_estimate:.1f}%")

# --- Final Prediction (incorporating tail risks and continual learning) ---
prediction = {
    "p5": 6,
    "p10": 10,
    "p25": 17,
    "p50": 26,
    "p75": 38,
    "p90": 50,
    "p95": 58,
}

print(f"\n{'='*60}")
print(f"FINAL PREDICTION: {PREDICTION_NAME}")
print(f"{'='*60}")
print(f"Resolution date: {TARGET_DATE}")
print(f"Current score: {CURRENT_SCORE}% (as of {CURRENT_DATE})")
print(f"\nPercentiles:")
for pct, val in prediction.items():
    print(f"  {pct}: {val}%")
print(f"\n80% CI: [{prediction['p10']}%, {prediction['p90']}%]")
print(f"Median: {prediction['p50']}%")
print(f"Implied improvement: {prediction['p50']/CURRENT_SCORE:.1f}x from current")

# --- Reference Class Comparison ---
print(f"\n{'='*60}")
print("REFERENCE CLASS COMPARISON")
print(f"{'='*60}")
reference_benchmarks = {
    "FrontierMath": {"start": 1.0, "end": 40.3, "months": 17.7, "factor": 40.3},
    "SWE-bench": {"start": 32.0, "end": 64.8, "months": 15.3, "factor": 2.0},
    "OS World": {"start": 35.8, "end": 66.3, "months": 9.0, "factor": 1.85},
}

for name, data in reference_benchmarks.items():
    print(f"{name}: {data['start']}% → {data['end']}% ({data['factor']:.1f}x in {data['months']:.0f} months)")

# --- Visualization ---
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Scenario breakdown
ax1 = axes[0]
scenario_names = list(scenarios.keys())
scenario_estimates = [s["estimate"] for s in scenarios.values()]
scenario_weights = [s["weight"] for s in scenarios.values()]
colors = ['#3498db', '#2ecc71', '#f39c12', '#e74c3c']

bars = ax1.bar(scenario_names, scenario_estimates, color=colors, alpha=0.7, edgecolor='black')
ax1.axhline(y=CURRENT_SCORE, color='red', linestyle='--', linewidth=2, label=f'Current ({CURRENT_SCORE}%)')
ax1.axhline(y=prediction['p50'], color='purple', linestyle='-', linewidth=2, label=f'Median prediction ({prediction["p50"]}%)')

# Add weight labels on bars
for bar, weight in zip(bars, scenario_weights):
    height = bar.get_height()
    ax1.annotate(f'{int(weight*100)}%',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3), textcoords="offset points",
                ha='center', va='bottom', fontsize=11, fontweight='bold')

ax1.set_ylabel('RLI Score (%)', fontsize=12)
ax1.set_title('Scenario Analysis with Weights', fontsize=13)
ax1.set_ylim(0, 65)
ax1.legend(loc='upper left')
ax1.grid(axis='y', alpha=0.3)

# Plot 2: Probability distribution (simplified visualization)
ax2 = axes[1]
percentiles = [5, 10, 25, 50, 75, 90, 95]
values = [prediction[f'p{p}'] for p in percentiles]

ax2.fill_between([0, 1], prediction['p10'], prediction['p90'], alpha=0.3, color='blue', label='80% CI')
ax2.fill_between([0, 1], prediction['p5'], prediction['p95'], alpha=0.15, color='blue', label='90% CI')
ax2.axhline(y=prediction['p50'], color='blue', linewidth=2, label=f'Median: {prediction["p50"]}%')
ax2.axhline(y=CURRENT_SCORE, color='red', linestyle='--', linewidth=2, label=f'Current: {CURRENT_SCORE}%')
ax2.axhline(y=40, color='orange', linestyle=':', linewidth=2, label='User intuition: 40%')

# Mark percentiles on right side
for pct in [10, 25, 50, 75, 90]:
    val = prediction[f'p{pct}']
    ax2.annotate(f'p{pct}: {val}%', xy=(1.02, val), fontsize=10,
                va='center', ha='left')

ax2.set_xlim(-0.1, 1.3)
ax2.set_ylim(0, 70)
ax2.set_ylabel('RLI Score (%)', fontsize=12)
ax2.set_title('Final Prediction Distribution', fontsize=13)
ax2.set_xticks([])
ax2.legend(loc='upper left')
ax2.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('waypoints/forecast_remote_labor_index_2026/plots/rli_prediction.png', dpi=150, bbox_inches='tight')
print(f"\nPlot saved to: waypoints/forecast_remote_labor_index_2026/plots/rli_prediction.png")

# --- Summary JSON ---
summary = {
    "prediction_name": PREDICTION_NAME,
    "target_date": TARGET_DATE,
    "current_score": CURRENT_SCORE,
    "current_date": CURRENT_DATE,
    "final_prediction": prediction,
    "weighted_scenario_estimate": round(weighted_estimate, 1),
    "scenarios": scenarios,
    "key_insight": "FrontierMath (40x improvement from 1%) is the primary reference class. RLI at 3.75% is analogous to FrontierMath in early 2025. Continual learning (15-20% probability) creates significant right-skew."
}

print(f"\n{'='*60}")
print("SUMMARY")
print(f"{'='*60}")
print(json.dumps(summary, indent=2))
