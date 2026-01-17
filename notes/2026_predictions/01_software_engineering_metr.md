# Software Engineering: METR Horizon Doubling Time

## Summary
We predict a median doubling time of **4.5 months** (10th: 3.0, 90th: 6.5). Regression on Epoch's 32-model dataset shows the long-term trend is ~5.75 months, but the 2024-2025 period accelerated to ~4.14 months. We anchor near the recent trend but shade slightly pessimistic (4.5 vs 4.1) because longer tasks (multi-day) may prove qualitatively harder. We widen bounds beyond the statistical CI to account for tail risks: the 10th percentile (3.0 mo) captures breakthrough scenarios, while the 90th (6.5 mo) covers disruptions like a Taiwan invasion affecting chip supply, regulatory slowdowns, or capability plateaus.

## Current Value
4.7 months (as of early 2025)

## Base Rate / Trend Analysis

![METR Horizon Progression](../../data/2026_predictions/metr_horizon_plot.png)

METR's task horizon metric measures the length of tasks (by human completion time) that AI agents can complete with 50% reliability.

**Current model horizons (50% success, in minutes):**
| Model | Time Horizon | Release Date |
|-------|--------------|--------------|
| Claude Opus 4.5 | 289 min (~4.8 hrs) | 2025-11-24 |
| GPT-5.1-Codex-Max | 162 min (~2.7 hrs) | 2025-11-19 |
| Claude 3.7 Sonnet | 56 min (~1 hr) | 2025-02-24 |
| GPT-4 | 5.4 min | 2023-03-14 |
| GPT-2 | 0.04 min | 2019-11-05 |

**Regression analysis on Epoch data (32 models):**

| Period | Doubling Time | 10th pctl | 90th pctl | R² |
|--------|---------------|-----------|-----------|-----|
| Full (2019-2025) | 5.75 mo | 5.18 mo | 6.46 mo | 0.825 |
| Recent (2024+) | 4.14 mo | 3.62 mo | 4.83 mo | 0.764 |

The recent period shows clear acceleration from the long-term ~6 month trend to ~4 months.

## Adjustment Factors

### Upward pressures (slower progress / longer doubling time)
- As horizons extend from hours to days/weeks, tasks become qualitatively harder
- Error propagation compounds over longer task durations
- Geopolitical risk: ~10% chance of Taiwan invasion disrupting chip supply
- Potential regulatory responses to safety incidents
- Training data scarcity for multi-day autonomous tasks

### Downward pressures (faster progress / shorter doubling time)
- Massive investment in agentic AI from all major labs
- Better scaffolding, tool use, and agent architectures
- Competition driving rapid iteration
- New training paradigms (RL, process supervision)
- Possible architectural breakthroughs

## Final Prediction

| Percentile | Value |
|------------|-------|
| 10th | 3.0 months |
| **Median** | **4.5 months** |
| 90th | 6.5 months |

**Confidence notes:** The statistical estimate from recent data is 4.14 months [3.62, 4.83]. We widen the bounds to account for non-model factors:
- 10th percentile (3.0 mo): Breakthrough scenario with unexpected acceleration
- Median (4.5 mo): Slight slowdown from recent trend as tasks get longer
- 90th percentile (6.5 mo): Disruption scenario (geopolitical, regulatory, or capability plateau)

## Data & Sources
- Epoch AI benchmark data: `data/2026_predictions/metr_time_horizons_external.csv`
- Analysis scripts: `scripts/2026_predictions/01_metr_horizon/`
- Trend plot: `data/2026_predictions/metr_horizon_plot.png`
- [METR: Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)
- [Epoch AI METR Time Horizons](https://epoch.ai/benchmarks/metr-time-horizons)
