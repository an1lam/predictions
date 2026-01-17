# Remote Work: Remote Labor Index (RLI)

## Summary
We predict a median automation rate of **18%** (10th: 8%, 90th: 35%). The RLI measures AI agents' ability to complete real freelance work to client-ready standards - currently at 3.75% with a 96% failure rate even for frontier models. Using FrontierMath Tier 4 as a reference class (similar early-stage trajectory from ~0%), we estimate ~1-2pp/month progress. The conservative model assumes "real work" is qualitatively harder than benchmarks (~12%), while the optimistic model follows FM-Tier4's acceleration pattern (~25%). Wide bounds reflect genuine uncertainty about whether end-to-end work reliability follows benchmark trajectories.

## Current Value
3.75% automation rate (Claude Opus 4.5 Thinking, November 2025)

## Base Rate / Trend Analysis

The Remote Labor Index (RLI) from Scale AI/CAIS measures AI agents' ability to complete real paid freelance work across 23 domains to professional, client-ready standards.

**Current leaderboard:**
| Rank | Model | Automation Rate |
|------|-------|-----------------|
| 1 | Claude Opus 4.5 (Thinking) | 3.75% |
| 2 | Manus 1.5 | 2.50% |
| 4 | GPT-5.2 | 2.08% |
| 6 | GPT-5 | 1.67% |
| 9 | Gemini 2.5 Pro | 0.83% |

**Key characteristics:**
- 96-97% failure rate even for best models
- Common failures: poor quality (45.6%), incomplete deliverables (35.7%)
- AI succeeds at: simple creative tasks (logos, sound effects), basic reports
- AI fails at: complex editing, multi-step briefs, professional polish
- Measures real economic value ($144k human earnings vs $1.7k for best agent)

**Observed trajectory (limited data):**
- Gemini 2.5 Pro (Jun 2025): 0.83%
- GPT-5 (Aug 2025): 1.67%
- Claude Opus 4.5 (Nov 2025): 3.75%

## Reference Class Analysis

First looked at benchmarks that started low and showed rapid progress
  ┌────────────────────┬───────┬─────────┬────────┬──────────┬────────────┬──────────┐
  │     Benchmark      │ Start │ Current │ Months │ Abs Gain │ Multiplier │ pp/month │
  ├────────────────────┼───────┼─────────┼────────┼──────────┼────────────┼──────────┤
  │ SWE-Bench Verified │ 32%   │ 65%     │ 15     │ +33pp    │ 2.0x       │ 2.1      │
  ├────────────────────┼───────┼─────────┼────────┼──────────┼────────────┼──────────┤
  │ ARC-AGI            │ 14%   │ 86%     │ 15     │ +72pp    │ 6.2x       │ 4.8      │
  ├────────────────────┼───────┼─────────┼────────┼──────────┼────────────┼──────────┤
  │ GDPVal             │ 14%   │ 48%     │ 15     │ +34pp    │ 3.4x       │ 2.3      │
  ├────────────────────┼───────┼─────────┼────────┼──────────┼────────────┼──────────┤
  │ OSWorld            │ ~5%   │ ~65%    │ ~14    │ +60pp    │ ~13x       │ ~4.3     │
  └────────────────────┴───────┴─────────┴────────┴──────────┴────────────┴──────────┘

Ended up using FrontierMath Tier 4 as primary reference - similar characteristics (started near 0, hard benchmark, stepwise progress).

**Early-stage benchmark velocities:**
| Benchmark | Early Stage Range | Velocity |
|-----------|-------------------|----------|
| FrontierMath Tier 4 | 0% → 19% | 1.1pp/month |
| FrontierMath (all) | 1% → 17% | 1.6pp/month |

**FrontierMath Tier 4 showed acceleration:**
- Early stage (0-10%): ~0.6-0.7pp/month
- Mid stage (10-20%): ~1.6-2.1pp/month
- Late acceleration: +10pp in single month (Dec 2025)

## Forecasting Methodology

**Model A: Conservative / "Real work is harder"** (50% weight)
- End-to-end reliability requirements create friction
- Growth rate: ~0.7pp/month (FM-Tier4 early stage)
- 3.75% + 12 × 0.7 = **~12%**

**Model B: Optimistic / "FM-Tier4 reference class"** (50% weight)
- Progress accelerates as with FM-Tier4
- Growth rate: ~1.8pp/month (FM-Tier4 mid-stage average)
- 3.75% + 12 × 1.8 = **~25%**

**Weighted median:**
```
0.50 × 12% + 0.50 × 25% = 18.5% ≈ 18%
```

## Adjustment Factors

### Upward pressures (higher automation rate)
- Massive commercial incentive to crack "real work" automation
- Agent-specific companies (Manus) focusing on reliability
- Labs may prioritize this as prestige metric
- Tool use and multi-step planning improving rapidly

### Downward pressures (lower automation rate)
- "Client-ready" bar may be qualitatively different from benchmark performance
- End-to-end reliability harder than isolated capabilities
- Professional polish and judgment difficult to automate
- Benchmark methodology may prove sticky

## Final Prediction

| Percentile | Value |
|------------|-------|
| 10th | 8% |
| **Median** | **18%** |
| 90th | 35% |

**Confidence notes:** The 10th percentile (8%) reflects a world where real work automation proves much harder than benchmark progress suggests. The 90th percentile (35%) reflects FM-Tier4-style acceleration continuing through 2026. The asymmetric range (10pp below, 17pp above median) reflects floor effects on the downside and more room for upside if acceleration materializes.

## Data & Sources
- Leaderboard image: `data/2026_predictions/rli_performance_comparison.png`
- Reference class scripts: `scripts/2026_predictions/03_remote_labor_index/`
- [Scale AI RLI Leaderboard](https://scale.com/leaderboard/rli)
- [RLI Paper (arXiv)](https://arxiv.org/abs/2510.26787)
- [Scale AI Blog: Remote Labor Index](https://scale.com/blog/rli)
