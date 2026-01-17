# Software Optimization: GSOBench

## Summary
We predict GSOBench SOTA will reach **74%** (10th: 45%, 90th: 95%) by December 31, 2026. This prediction is based on fitting a sigmoid curve to the SOTA progression, which shows the benchmark is currently before its inflection point (projected for mid-2026). Using a 90-100% ceiling assumption—appropriate since the benchmark measures performance against human experts rather than a theoretical optimum—the sigmoid projects 71-76% by end of 2026. We centered on 74% and widened bounds to account for out-of-model factors including geopolitical risk, potential for AI to exceed human performance, and benchmark methodology changes.

## Current Value
- **SOTA**: 27.4% (GPT-5.2 + OpenHands, Dec 2025)
- **Hack-adjusted**: 26.5% (per survey methodology)

## Base Rate / Trend Analysis

### SOTA Progression
| Date | Score | Model |
|------|-------|-------|
| Oct 2024 | 4.6% | Claude 3.5 Sonnet |
| Apr 2025 | 8.8% | o3 |
| Sep 2025 | 14.7% | Claude Sonnet 4.5 |
| Nov 2025 | 18.6% | Gemini 3 Pro |
| Nov 2025 | 26.5% | Claude Opus 4.5 |
| Dec 2025 | 27.4% | GPT-5.2 |

### Velocity Analysis
- **Full period** (14 months): 1.65 pp/month average
- **Last 6 months**: 5.22 pp/month (significant acceleration)
- Recent velocity exceeds reference class benchmarks (SWE-Bench, ARC-AGI, OSWorld ~3-4 pp/mo)

### Sigmoid Fitting
Fitted logistic curves to SOTA progression with varying ceiling assumptions:

| Ceiling | R² | Midpoint | Dec 2026 Projection |
|---------|-----|----------|---------------------|
| 60% | 0.880 | Feb 2026 | 53.6% |
| 70% | 0.884 | Mar 2026 | 60.1% |
| 80% | 0.887 | Apr 2026 | 65.9% |
| 90% | 0.889 | May 2026 | 71.2% |
| 100% | 0.890 | Jun 2026 | 76.1% |

**Key insight**: All models place the sigmoid midpoint in early-mid 2026, meaning we're currently in the acceleration phase (before inflection). This explains the recent rapid progress and suggests continued fast gains in H1 2026, then deceleration in H2.

### Ceiling Assumption
We use 90-100% as the appropriate ceiling because:
- GSO measures performance against human software optimization experts, not a theoretical optimum
- AI could potentially exceed 100% (surpass human performance)
- The ceiling is "soft" rather than hard

## Adjustment Factors

### Upward pressures
- Still before sigmoid midpoint → continued acceleration in H1 2026
- Ceiling is human performance, which AI may exceed
- Multiple labs competing actively on this benchmark
- Software optimization aligns well with current LLM+agent paradigm

### Downward pressures
- Diminishing returns as "easy" optimizations are exhausted
- Benchmark may have harder long-tail problems
- Potential for benchmark contamination discoveries leading to score adjustments
- Geopolitical/economic disruption risk

## Final Prediction
**Central estimate:** 74%
**10th percentile:** 45%
**90th percentile:** 95%

## Methodology Notes
- Primary model: Sigmoid fit with 90-100% ceiling (projects 71-76%)
- Bounds widened from model output (55%, 88%) to account for out-of-model factors
- Reference class comparison confirms GSO is moving faster than similar benchmarks, consistent with being in pre-midpoint acceleration phase
