# Developer Productivity: METR Uplift Study

## Summary
We predict the METR developer uplift study will show a **1.4x** speedup (10th: 0.90x, 90th: 2.2x) when replicated with late-2026 AI tools. The original early-2025 study found a surprising 0.84x slowdown with Claude 3.5/3.7 Sonnet, contradicting expert predictions of 1.6x speedup. However, significant capability improvements (Opus 4.5 shows median 100% productivity gains in Anthropic's internal survey) suggest the 2026 replication will likely show net speedup. We center on 1.4x as a compromise between process-driven estimates (~1.35x) and intuition informed by direct experience with newer models (~1.5x), with wide bounds reflecting genuine uncertainty, including about when the study would have run.

## Current Value
**0.84x** (early-2025 study result - a slowdown)

### Study Details
- 16 experienced developers, 246 issues
- Mature open-source repositories
- Per-issue random assignment (AI-allowed vs AI-disallowed)
- Tools: Cursor Pro with Claude 3.5/3.7 Sonnet
- Issues averaged ~2 hours to complete
- Developers had ~5 years prior experience on their repositories
- 75% of developers were slowed down

### Expectation Gap
| Group | Predicted Speedup |
|-------|-------------------|
| Developers (pre-study) | 1.32x |
| Developers (post-study) | 1.25x |
| Economics experts | 1.64x |
| ML experts | 1.61x |
| **Actual result** | **0.84x** |

## Conflicting Evidence

### Evidence for Slowdown (METR Study)
- Rigorous RCT methodology
- Experienced devs on familiar codebases (hard test case)
- 75% of developers individually slowed down
- Robust across alternative estimators and subset checks

### Evidence for Speedup (Anthropic Data)
- **Project Fetch**: AI successfully helped build robot dog project
- **Opus 4.5 internal survey**:
  - 9/18 participants reported ≥100% productivity improvements
  - Median: 100% improvement (2x speedup)
  - Mean: 220% improvement
- Significant capability jump from Claude 3.5/3.7 → Opus 4.5

### Key Differences Explaining Gap
| Factor | METR Study | Anthropic Data |
|--------|------------|----------------|
| Tools | Claude 3.5/3.7 (early 2025) | Opus 4.5 (late 2025) |
| Methodology | Rigorous RCT | Self-reported survey |
| Tasks | Mature OSS issues | Internal R&E tasks |
| Population | External experienced devs | Anthropic employees |

## Model Framework

### Scenario A: Still Slight Slowdown (15% weight)
- METR methodology is specifically hard for AI
- Even with better tools, experienced devs on familiar codebases may be faster alone
- Projection: **0.90-0.95x**

### Scenario B: Break-even to Modest Speedup (45% weight)
- Tools improve enough to flip to neutral or slight positive
- AI helps with some tasks but not others
- Projection: **1.0-1.3x**

### Scenario C: Meaningful Speedup (40% weight)
- Capability improvements (Opus 4.5+) translate to real gains
- Approaches Anthropic internal survey results
- Projection: **1.5-2.0x**

### Weighted Calculation
0.15 × 0.93 + 0.45 × 1.15 + 0.40 × 1.75 = **1.36x**

Adjusted to **1.4x** to balance process-driven estimate with intuition from direct experience with newer models.

## Adjustment Factors

### Upward pressures
- Massive capability improvements: Claude 3.5 → Opus 4.5 → 2026 frontier
- Better tool integration (Cursor improvements, new IDEs)
- Anthropic internal data shows 2x median improvement
- Models with longer context, better codebase understanding
- Direct experience suggests Opus 4.5 provides real speedup

### Downward pressures
- METR methodology is specifically designed to be hard
- Experienced devs on familiar codebases is where AI helps *least*
- Self-reported surveys (Anthropic) may overestimate gains
- Context-switching costs may persist
- AI suggestions may still not match expert mental models

## Final Prediction
**Central estimate:** 1.4x
**10th percentile:** 0.90x
**90th percentile:** 2.2x

### Interpretation
- 1.4x means AI saves experienced developers ~30% of their time
- Wide bounds (0.90x to 2.2x) reflect genuine uncertainty
- 10th percentile allows for methodology still showing slight slowdown
- 90th percentile allows for exceeding Anthropic survey results

## Methodology Notes
- Only one prior data point (0.84x from early-2025 study)
- Cannot fit trend; relying on scenario weighting
- Balanced process-driven estimate (~1.35x) with intuition (~1.5x)
- Wide bounds reflect conflicting evidence and uncertainty about tool improvements
- Key assumption: 2026 study uses similar methodology with then-frontier tools
