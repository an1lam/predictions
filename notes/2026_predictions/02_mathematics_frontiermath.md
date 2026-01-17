# Mathematics: FrontierMath Tier 4

## Summary
We predict a median score of **62%** (10th: 40%, 90th: 85%). We use a weighted multi-model approach: (A) linear trend extrapolation at 2.6%/month → 60%, weighted 40%; (B) accelerated progress model at 4.2%/month based on recent RL-driven gains → 79%, weighted 30%; (C) ceiling/diminishing returns model at 1.5%/month → 47%, weighted 30%. Progress on this benchmark has been stepwise, driven by flagship model releases from OpenAI and Google. RL advances (IMO wins, Erdős solutions) suggest math may progress faster than other domains, but Tier 4 contains the hardest problems so some slowdown is plausible.

## Current Value
29.2% (GPT-5.2 Pro, December 2025)

## Base Rate / Trend Analysis

FrontierMath Tier 4 is the hardest tier of the FrontierMath benchmark, containing research-level mathematics problems.

**Top performers:**
| Model | Score | Release Date | Organization |
|-------|-------|--------------|--------------|
| GPT-5.2 Pro | 29.2% | 2025-12-11 | OpenAI |
| Gemini 3 Pro | 18.8% | 2025-11-18 | Google DeepMind |
| GPT-5.2 (xhigh) | 16.7% | 2025-12-11 | OpenAI |
| GPT-5 (high) | 12.5% | 2025-08-07 | OpenAI |
| Gemini 2.5 Deep Think | 10.4% | 2025-08-01 | Google |

**Key milestones:**
| Milestone | Date | Score |
|-----------|------|-------|
| First non-zero | Jan 2025 | 4.2% |
| First >10% | Aug 2025 | 12.5% |
| First >20% | Dec 2025 | 29.2% |

**Progress characteristics:**
- Stepwise, not smooth - big jumps with flagship model releases
- Only OpenAI and Google making significant progress; most models stuck at 0-4%
- Linear trend: ~2.6%/month average, but R² = 0.17 (very noisy)
- Recent acceleration: 12.5% → 29.2% in 4 months (4.2%/month)

## Forecasting Methodology

Given the stepwise nature of progress and uncertainty about RL-driven acceleration, we use a weighted multi-model approach:

### Model A: Linear Trend (40% weight)
- Extrapolate the ~2.6%/month average from Jan-Dec 2025
- 29% + 12 × 2.6% = **60%**

### Model B: Accelerated Progress (30% weight)
- Recent acceleration: 12.5% (Aug) → 29.2% (Dec) = 4.2%/month
- RL-driven gains on well-specified math problems continue
- Evidence: IMO wins, Erdős problem solutions
- 29% + 12 × 4.2% = **79%**

### Model C: Ceiling / Diminishing Returns (30% weight)
- Tier 4 is the hardest tier; remaining problems are qualitatively harder
- Progress slows to ~1.5%/month as low-hanging fruit exhausted
- 29% + 12 × 1.5% = **47%**

### Weighted Aggregate
```
Median = 0.40 × 60% + 0.30 × 79% + 0.30 × 47%
       = 24% + 23.7% + 14.1%
       = 61.8% ≈ 62%
```

## Adjustment Factors

### Upward pressures (higher score)
- RL advances showing strong results on well-specified math
- Major labs heavily investing in reasoning capabilities
- Math is a prestige benchmark driving competition

### Downward pressures (lower score)
- Tier 4 problems are research-level, qualitatively harder
- Diminishing returns as easier problems solved
- Fewer flagship model releases than 2025

## Final Prediction

| Percentile | Value |
|------------|-------|
| 10th | 40% |
| **Median** | **62%** |
| 90th | 85% |

**Confidence notes:** The 10th percentile (40%) reflects ceiling model + additional downside risk. The 90th percentile (85%) reflects accelerated model + potential breakthrough. The wide range reflects genuine uncertainty about whether RL-driven progress will continue or hit diminishing returns on the hardest problems.

## Data & Sources
- Epoch AI benchmark data: `data/2026_predictions/frontiermath_tier_4.csv`
- Analysis script: `scripts/2026_predictions/frontiermath_tier4_analysis.py`
- [Epoch AI FrontierMath Leaderboard](https://epoch.ai/benchmarks/frontiermath)
