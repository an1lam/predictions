# 2026 AI Forecast Predictions Plan

## Overview
Work through 10 AI predictions for December 31st, 2026 using a superforecasting-inspired methodology.

## Methodology (Refined)

For each prediction:

1. **Research & data gathering**
   - Fetch relevant data from Epoch AI or other sources (prefer programmatic access)
   - Download/save trend plots to `data/2026_predictions/`
   - Write analysis scripts to `scripts/2026_predictions/<prediction_num>/` for reproducibility

2. **Base rate analysis**
   - Fit regression or other statistical model to historical data
   - Calculate statistical uncertainty bounds (10th/90th percentiles)
   - Build reference class from similar benchmarks (especially early-stage progression)

3. **Discussion**
   - Present findings to user before finalizing
   - Discuss adjustment factors together
   - Consider outside-model factors (geopolitical, regulatory, etc.)

4. **Multi-model weighting (when appropriate)**
   - Conservative model: assumes harder/slower progress
   - Moderate model: follows reference class trajectory
   - Optimistic model: accounts for explicit prioritization or breakthroughs
   - Weight models based on evidence and reasoning

5. **Widen uncertainty bounds**
   - Statistical CIs only capture trend uncertainty
   - Explicitly add probability mass for tail scenarios:
     - Downside: geopolitical disruption, regulatory pause, capability plateau
     - Upside: architectural breakthroughs, unexpected scaling gains, explicit lab prioritization

6. **Finalize & document**
   - Write prediction file with full reasoning
   - Include 1-paragraph **Summary** at top (for survey submission)
   - Include data sources, scripts, and plot references

## Predictions Status

### Benchmark Performance (6 questions)
| # | Topic | Metric | Current | Prediction | 10th | 90th | Status |
|---|-------|--------|---------|------------|------|------|--------|
| 01 | Software Engineering | METR Horizon Doubling Time | 4.7 mo | **4.5 mo** | 3.0 mo | 6.5 mo | ✅ Done |
| 02 | Mathematics | FrontierMath Tier 4 | 29.2% | **62%** | 40% | 85% | ✅ Done |
| 03 | Remote Work | Remote Labor Index | 3.75% | **18%** | 8% | 35% | ✅ Done |
| 04 | AI Research | OpenAI-Proof Q&A | 8% | **37%** | 18% | 55% | ✅ Done |
| 05 | Software Optimization | GSOBench | 26.5% | **74%** | 45% | 95% | ✅ Done |
| 06 | General Capabilities | Epoch Capabilities Index | 154 | **177** | 160 | 195 | ✅ Done |

### AI Prominence (4 questions)
| # | Topic | Metric | Current | Prediction | 10th | 90th | Status |
|---|-------|--------|---------|------------|------|------|--------|
| 07 | AI Lab Revenues | OpenAI + Anthropic + xAI | $31B | **$60B** | $35B | $90B | ✅ Done |
| 08 | Public Importance | Americans saying AI most important | 0.44% | **1.0%** | 0.3% | 8% | ✅ Done |
| 09 | Developer Productivity | METR Uplift Study | 0.84x | **1.4x** | 0.90x | 2.2x | ✅ Done |
| 10 | Societal Effects | YouGov Poll (net sentiment) | -11pp | **-14pp** | -40pp | +15pp | ✅ Done |

## Key Reference Class Data (for remaining predictions)

**Early-stage benchmark velocities (useful for predictions starting low):**
| Benchmark | Range | Velocity |
|-----------|-------|----------|
| FrontierMath Tier 4 | 0% → 10% | 0.6-0.7pp/month |
| FrontierMath Tier 4 | 5% → 15% | 1.7pp/month |
| FrontierMath Tier 4 | 10% → 30% | 4.3pp/month (acceleration) |
| FrontierMath (all) | 5% → 15% | 2.1pp/month |
| FrontierMath (all) | 10% → 30% | 2.8pp/month |

**Mid-to-high stage velocities:**
| Benchmark | Range | Velocity |
|-----------|-------|----------|
| SWE-Bench Verified | 30% → 50% | 2.1pp/month |
| GPQA Diamond | 30% → 50% | 0.9pp/month |
| FrontierMath (all) | 30% → 50% | 2.0pp/month |

## File Structure

```
notes/2026_predictions/
├── 00_plan.md                          # This file
├── 01_software_engineering_metr.md     # ✅ Complete
├── 02_mathematics_frontiermath.md      # ✅ Complete
├── 03_remote_work_labor_index.md       # ✅ Complete
├── 04_ai_research_opqa.md              # ✅ Complete
├── 05_software_optimization_gsobench.md # ✅ Complete
├── 06_general_capabilities_epoch.md     # ✅ Complete
├── 07_ai_lab_revenues.md                # ✅ Complete
├── 08_public_importance_ai.md           # ✅ Complete
├── 09_developer_productivity_metr.md    # ✅ Complete
└── 10_societal_effects_yougov.md        # ✅ Complete

data/2026_predictions/
├── benchmark_data.zip                  # Epoch AI benchmark data (all benchmarks)
├── metr_time_horizons_external.csv
├── frontiermath_tier_4.csv
├── frontiermath.csv
├── gpqa_diamond.csv
├── swe_bench_verified.csv
├── arc_agi_external.csv
├── 20260117_epoch_metr_time_horizon.png
├── rli_performance_comparison.png
└── ...

scripts/2026_predictions/
├── 01_metr_horizon/
│   └── metr_doubling_time.py
├── 02_frontiermath/
│   └── frontiermath_tier4_analysis.py
├── 03_remote_labor_index/
│   ├── benchmark_reference_class.py
│   └── early_stage_progression.py
├── 04_opqa/
│   └── reference_class_analysis.py
├── 05_gsobench/
│   ├── gso_progression_analysis.py
│   └── gso_sigmoid_fit.py
├── 06_epoch_capabilities/
│   ├── eci_linear_fit.py
│   └── eci_plot.py
└── 07_ai_lab_revenues/
    ├── revenue_analysis.py
    └── revenue_plot.py
```

## Key Lessons Learned

1. **Verify data carefully** - Initial WebFetch gave wrong units (hours vs minutes)
2. **Use Epoch data where possible** - Their CSVs are clean and well-documented
3. **Statistical bounds are too narrow** - Real forecasts need wider tails for outside-model factors
4. **Discuss before documenting** - Catch errors and refine reasoning interactively
5. **Build reference classes** - Early-stage benchmark progression is valuable for predicting new benchmarks
6. **Multi-model weighting** - Use for predictions with multiple plausible scenarios (conservative/moderate/optimistic)
7. **Consider explicit lab priorities** - OpenAI's "research intern" goal influenced OPQA prediction
8. **Sigmoid fitting** - For benchmarks with enough data points, fitting a logistic curve can reveal where we are on the S-curve (GSO: before midpoint, explaining recent acceleration)

## Submission
Submit final predictions at forecast2026.ai
