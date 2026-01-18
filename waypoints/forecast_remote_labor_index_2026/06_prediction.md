# Prediction: Remote Labor Index - Highest Score by End of 2026

**Prediction type**: Quantitative
**Created**: 2026-01-18
**Resolution date**: 2026-12-31
**Resolution criteria**: The highest automation rate (%) shown for any AI agent on the Scale AI Remote Labor Index leaderboard (scale.com/leaderboard/rli) on or around December 31, 2026.

## Summary

This forecast predicts the highest AI agent automation rate on the Remote Labor Index (RLI) by end of 2026. The RLI measures end-to-end agent performance on real-world professional work projects (240 projects, $144k total value, 23 domains including game dev, architecture, video animation, etc.).

The central estimate is **26%** (median), with an 80% confidence interval of **10% to 50%**. This represents approximately 7x improvement from the current top score of 3.75%. The wide uncertainty reflects genuine disagreement about whether RLI will experience FrontierMath-like rapid acceleration (which saw 40x improvement from similar low starting scores) or prove fundamentally harder due to requiring end-to-end execution of complex professional tasks rather than just reasoning.

## Current State

- **Current value**: 3.75% (Claude Opus 4.5 with thinking)
- **Data source**: Scale AI RLI Leaderboard (scale.com/leaderboard/rli)
- **As of**: 2026-01-16
- **Benchmark details**: 240 projects from 358 Upwork freelancers, 23 domains, projects cost >$10k and take 100+ hours

## Base Rate Analysis (Outside View)

**Primary reference class**: FrontierMath benchmark trajectory

FrontierMath is the best analog because it also started at very low scores (~1%) on genuinely hard tasks and demonstrated that rapid acceleration is possible once capabilities cross thresholds.

| Benchmark | Start | End | Period | Improvement |
|-----------|-------|-----|--------|-------------|
| FrontierMath | 1% | 40% | 18 mo | **40x** |
| SWE-bench | 32% | 65% | 15 mo | 2x |
| OS World | 36% | 66% | 9 mo | 1.8x |

**Key insight**: Position on sigmoid curve matters. Benchmarks starting at 30-50% showed ~2x improvement. FrontierMath starting at ~1% showed 40x improvement. RLI at 3.75% is analogous to FrontierMath in early 2025.

**Base rate anchor**: 18% (revised to account for sigmoid dynamics)

## Adjustment Factors (Inside View)

| Factor | Direction | Magnitude | Notes |
|--------|-----------|-----------|-------|
| Task difficulty vs FrontierMath | - | Moderate-Large | Execution harder than reasoning; 100+ hour tasks compound errors |
| Labs' explicit agent focus | + | Moderate | All major labs shipping agent products; enormous economic incentives |
| AI-accelerated R&D | + | Small-Moderate | Claude Code, Codex accelerating development; compounding effect |
| Expected model releases | + | Moderate | GPT-6, Claude 5, Gemini 4 expected in 2026 |
| Continual learning potential | + | Moderate | 15-20% probability of significant impact |
| Multi-domain breadth | - | Small | 23 domains harder than specialized benchmarks |
| Human quality standards | - | Small | Satisfying human judgment harder than correctness |

**Net adjustment**: Modestly positive (+4 to +8pp from base rate)

## Scenario Analysis

| Scenario | Estimate | Weight | Key Assumption |
|----------|----------|--------|----------------|
| Conservative | 10% | 25% | RLI execution requirements are fundamentally harder than FrontierMath reasoning |
| Moderate | 23% | 45% | FrontierMath-like acceleration at ~50% rate due to task difficulty |
| Optimistic | 40% | 25% | Capability thresholds crossed, FrontierMath-like trajectory |
| Very Optimistic | 52% | 5% | Breakthrough architecture + explicit lab targeting |

**Weighted estimate**: 25.4%

## Final Prediction

| Percentile | Value | Interpretation |
|------------|-------|----------------|
| 5th | 6% | Technical plateau / major disruption |
| **10th** | **10%** | Conservative scenario |
| 25th | 17% | Below moderate expectations |
| **50th (median)** | **26%** | Central estimate (~7x improvement) |
| 75th | 38% | Above moderate expectations |
| **90th** | **50%** | Optimistic scenario + continual learning |
| 95th | 58% | Breakthrough conditions |

**80% Confidence Interval: 10% to 50%**
**90% Confidence Interval: 6% to 58%**

**Distribution**: Right-skewed due to 15-20% probability of continual learning driving acceleration. User intuition of 40% falls at approximately p80.

## Confidence Notes

- Wide uncertainty reflects genuinely novel prediction: RLI is a new benchmark with no historical trajectory
- 80% CI spans from "RLI is fundamentally harder" to "continual learning accelerates progress"
- Median of 26% is between SWE-bench pace (2x → 7.5%) and FrontierMath pace (40x → 150%)
- Distribution is right-skewed due to continual learning probability (15-20%)

## Tail Scenarios

### Downside (below p10 = 10%)
- **Technical plateau**: Error compounding in long-horizon tasks proves fundamentally unsolvable
- **Benchmark hardening**: RLI adds harder tasks or raises quality bar
- **Geopolitical risks**: Chip supply chain disruption (export controls, Taiwan tensions)
- **Regulatory slowdown**: New regulations impact datacenter build-out or AI deployment

### Upside (above p90 = 50%)
- **Breakthrough architecture**: New approach dramatically improves long-horizon execution
- **Explicit targeting**: Major lab prioritizes RLI as competitive benchmark
- **AI-accelerated R&D compounding**: Internal AI tools create faster-than-historical improvement
- **Continual learning**: Agents gain ability to improve from deployment experience

## Key Uncertainties to Watch

1. **Do new model releases (GPT-6, Claude 5) show proportional RLI gains?** If yes, supports moderate/optimistic. If not, supports conservative.
2. **Does continual learning make meaningful progress?** 15-20% probability this is transformative.
3. **Do agents crack specific RLI domains?** Progress may be uneven across 23 domains.

## Files

- Phase 1: `01_research_priorities.json`
- Phase 2: `02_base_rate_analysis.json`
- Phase 3: `03_inside_view_adjustments.json`
- Phase 4: `04_scenario_models.json`
- Phase 5: `05_uncertainty_bounds.json`
- Analysis scripts: `scripts/benchmark_analysis.py`, `scripts/sigmoid_analysis.py`, `scripts/final_analysis.py`
- Plots: `plots/sigmoid_comparison.png`, `plots/rli_prediction.png`
- Data: `data/` (Epoch AI benchmark data)

---

*Generated using /forecast skill on 2026-01-18*
