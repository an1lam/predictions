# AI Research: OpenAI-Proof Q&A (OPQA)

## Summary
We predict a median score of **37%** (10th: 18%, 90th: 55%). OPQA evaluates models on 20 internal OpenAI research/engineering bottlenecks that took senior engineers 1+ day to solve. Current best is GPT-5.1-Codex-Max at 8%. Using FrontierMath Tier 4 as the primary reference class (similar early-stage, hard benchmark), we model three scenarios: conservative (1.5pp/month → 26%), moderate with acceleration (→ 39%), and optimistic given OpenAI's explicit "AI research intern by Sep 2026" goal (→ 44%). Weighted 30/40/30, this yields ~37%. The wide range reflects uncertainty about whether real-world debugging follows benchmark patterns, balanced against OpenAI's clear prioritization of this capability.

## Current Value
8% (GPT-5.1-Codex-Max, November 2025)

## Benchmark Description

OpenAI-Proof Q&A evaluates AI models on 20 internal research and engineering bottlenecks encountered at OpenAI:
- Each task required 1+ day for senior OpenAI engineers to solve
- Tasks involve diagnosing root causes: performance regressions, anomalous training metrics, subtle bugs
- Models get access to a container, code, and run artifacts
- Graded pass@1
- Human baseline is effectively 100% (these are problems humans solved)

**Source:** [OpenAI GPT-5 System Card (arXiv)](https://arxiv.org/pdf/2601.03267#page=41)

## Base Rate / Trend Analysis

**Current scores:**
| Model | Score | Date | Notes |
|-------|-------|------|-------|
| GPT-5.1-Codex-Max | **8%** | Nov 2025 | Current best |
| GPT-5.2 | 3% | Dec 2025 | No browsing |
| GPT-5 | 2% | Aug 2025 | No browsing |
| o3 | 2% | Apr 2025 | No browsing |

**Key observations:**
- Only 20 questions → 5pp granularity (1 question = 5%)
- Progress: 2% → 8% over 7 months (+6pp, ~0.9pp/month)
- Codex-Max variant significantly outperforms base models (8% vs 3%)
- **OpenAI's stated goal: "automated AI research intern" by Sep 2026**

## Reference Class Analysis

GPQA and SWE-Bench started too high (32-36%) to be directly relevant. FrontierMath benchmarks at similar stages provide the best comparison.

**Velocity at ~5-15% stage (most relevant for OPQA at 8%):**
| Benchmark | Range | Velocity |
|-----------|-------|----------|
| FrontierMath Tier 4 | 5% → 15% | 1.7pp/month |
| FrontierMath (all) | 5% → 15% | 2.1pp/month |

**Velocity at ~10-30% stage (if OPQA accelerates):**
| Benchmark | Range | Velocity |
|-----------|-------|----------|
| FrontierMath Tier 4 | 10% → 30% | 4.3pp/month |
| FrontierMath (all) | 10% → 30% | 2.8pp/month |

## Forecasting Methodology

**Model A: Conservative / "Harder than math"** (30% weight)
- OPQA tasks are real-world debugging - arguably harder than mathematical reasoning
- Use lower bound of FM-Tier4 early-stage velocity (~1.5pp/month)
- 8% + 12 × 1.5 = **~26%**

**Model B: Moderate / "FM-Tier4 reference"** (40% weight)
- Follow FM-Tier4 pattern with mid-stage acceleration
- 8% → 15% at 1.7pp/month (4 months), then accelerate to 3pp/month
- **~39%**

**Model C: Optimistic / "OpenAI prioritizes this"** (30% weight)
- OpenAI's explicit Sep 2026 goal: "automated AI research intern"
- Codex-Max already shows specialized models help (8% vs 3%)
- Follow FM-all acceleration pattern (~3pp/month sustained)
- 8% + 12 × 3 = **~44%**

**Weighted median:**
```
0.30 × 26 + 0.40 × 39 + 0.30 × 44 = 36.6% ≈ 37%
```

## Adjustment Factors

### Upward pressures (higher score)
- OpenAI explicitly targeting "AI research intern" capability by Sep 2026
- Codex-Max shows specialized models can significantly outperform base models
- High commercial/strategic value for AI labs
- Could see step-change with targeted investment

### Downward pressures (lower score)
- Real-world debugging may be fundamentally harder than math/coding benchmarks
- Small sample (20 questions) means lumpy, high-variance progress
- Tasks require integration of many skills (code reading, hypothesis generation, systematic debugging)
- May hit capability ceiling before reaching high scores

## Final Prediction

| Percentile | Value |
|------------|-------|
| 10th | 18% |
| **Median** | **37%** |
| 90th | 55% |

**Confidence notes:** The 10th percentile (18%) reflects a world where real-world debugging proves much harder than benchmark progress suggests. The 90th percentile (55%) reflects OpenAI achieving their research intern goal with breakthrough specialized models. The median (37%) represents ~4.5x improvement from current 8%, consistent with FM-Tier4's trajectory over similar timeframes.

## Data & Sources
- Reference class scripts: `scripts/2026_predictions/04_opqa/`
- [OpenAI GPT-5 System Card - OPQA section](https://arxiv.org/pdf/2601.03267#page=41)
- Epoch AI benchmark data for reference class analysis
