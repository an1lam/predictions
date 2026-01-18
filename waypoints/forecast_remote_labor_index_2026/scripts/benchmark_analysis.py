"""
Analyze agentic benchmark trajectories to establish base rate for RLI prediction.
"""

import pandas as pd
import numpy as np
from datetime import datetime

# Current RLI state
rli_current = {
    "score": 3.75,
    "date": "2026-01-16",
    "prediction_target_date": "2026-12-31"
}

# Reference class: Agentic benchmark improvement rates
# Data extracted from Epoch AI benchmark data

benchmarks = {
    "SWE-bench Verified": {
        "early": {"date": "2024-06-20", "score": 32.0, "model": "Claude 3.5 Sonnet"},
        "recent": {"date": "2026-01-16", "score": 64.8, "model": "Claude Sonnet 4.5"},
    },
    "The Agent Company": {
        "early": {"date": "2024-12-17", "score": 34.4, "model": "Claude 3.5 Sonnet"},
        "recent": {"date": "2025-10-13", "score": 52.4, "model": "DeepSeek V3.2"},
    },
    "OS World": {
        "early": {"date": "2025-02-24", "score": 35.8, "model": "Claude 3.7 Sonnet"},
        "recent": {"date": "2025-11-24", "score": 66.3, "model": "Claude Opus 4.5"},
    },
    "METR Time Horizons": {
        "early": {"date": "2024-06-20", "score": 18.7, "model": "Claude 3.5 Sonnet"},  # minutes
        "recent": {"date": "2025-11-24", "score": 289.0, "model": "Claude Opus 4.5"},  # minutes
        "note": "Time horizon in minutes, not percentage"
    }
}

def calculate_improvement_rate(early, recent):
    """Calculate multiplicative and additive improvement rates."""
    d1 = datetime.strptime(early["date"], "%Y-%m-%d")
    d2 = datetime.strptime(recent["date"], "%Y-%m-%d")
    months = (d2 - d1).days / 30.44  # average days per month

    multiplicative = recent["score"] / early["score"]
    additive_per_month = (recent["score"] - early["score"]) / months
    multiplicative_per_month = multiplicative ** (1/months)

    return {
        "months": months,
        "multiplicative_total": multiplicative,
        "multiplicative_per_month": multiplicative_per_month,
        "additive_per_month": additive_per_month,
        "start_score": early["score"],
        "end_score": recent["score"]
    }

print("=" * 60)
print("AGENTIC BENCHMARK IMPROVEMENT RATES")
print("=" * 60)

for name, data in benchmarks.items():
    rates = calculate_improvement_rate(data["early"], data["recent"])
    print(f"\n{name}:")
    print(f"  Period: {rates['months']:.1f} months")
    print(f"  Score: {rates['start_score']:.1f}% → {rates['end_score']:.1f}%")
    print(f"  Total improvement: {rates['multiplicative_total']:.2f}x")
    print(f"  Monthly improvement: {rates['multiplicative_per_month']:.3f}x ({rates['additive_per_month']:.2f} pp/month)")

# Extrapolate for RLI
print("\n" + "=" * 60)
print("RLI BASE RATE EXTRAPOLATION")
print("=" * 60)

months_to_target = 11.5  # Jan 18 to Dec 31, 2026

# Use different improvement models
improvement_factors = {
    "Conservative (SWE-bench pace)": 1.042,  # ~2x per 18 months
    "Moderate (OS World pace)": 1.070,       # ~1.8x per 9 months
    "Aggressive (METR pace)": 1.18,          # ~15x per 17 months
}

print(f"\nCurrent RLI: {rli_current['score']}%")
print(f"Months to target: {months_to_target}")
print("\nExtrapolations:")

for scenario, monthly_factor in improvement_factors.items():
    projected = rli_current["score"] * (monthly_factor ** months_to_target)
    print(f"  {scenario}: {projected:.1f}%")

# Summary statistics for base rate
print("\n" + "=" * 60)
print("BASE RATE SUMMARY")
print("=" * 60)
print("""
Reference class: Agentic AI benchmark improvement rates (2024-2026)

Key observations:
1. SWE-bench: 2.0x improvement over 18 months (coding tasks)
2. Agent Company: 1.5x improvement over 10 months (workplace tasks)
3. OS World: 1.85x improvement over 9 months (computer use)
4. METR Horizons: 15x improvement over 17 months (task time horizons)

RLI characteristics that differ from reference class:
- Much harder tasks (real professional work, $10k+ projects)
- Very low current scores (3.75% vs 30-50% for comparisons)
- Real economic value at stake (not synthetic benchmarks)

Base rate extrapolations (11.5 months from 3.75%):
- 2x improvement → 7.5%
- 3x improvement → 11.3%
- 5x improvement → 18.8%
- 10x improvement → 37.5%

Anchor: 8-12% (median), wide uncertainty due to novel benchmark characteristics
""")
