# /forecast

A systematic forecasting skill implementing superforecasting methodology from Tetlock/Good Judgment Project and Steinhardt's forecasting course.

## Overview

This skill guides you through structured prediction workflows for:
- **Quantitative benchmarks**: Numeric targets with uncertainty bounds (10th, median, 90th percentiles)
- **Binary predictions**: Yes/no outcomes with calibrated probabilities

Key principles:
- Outside view first (anchor to base rates before case-specific analysis)
- Multi-model reasoning (generate competing hypotheses)
- Explicit uncertainty quantification (statistical + model + tail risk)
- Checkpoint-driven (pause for input at each major phase)

---

## Entry Points

When user invokes `/forecast`, ask which mode:

### 1. Create a new forecast
Full systematic workflow through 7 phases. Creates waypoint directory with all artifacts.

### 2. Update an existing forecast
Bayesian revision with new information. Load existing waypoint, document new evidence, adjust prediction.

### 3. Score/calibrate predictions
Evaluate past predictions against outcomes. Calculate Brier score, log score, calibration metrics.

---

## Waypoint Architecture

All analysis is stored in `waypoints/forecast_<name>/` where `<name>` is a snake_case identifier derived from the prediction target.

```
waypoints/forecast_<name>/
├── metadata.json                         # Prediction info, status, completed phases
├── 01_research_priorities.json           # Information prioritization results
├── 02_base_rate_analysis.json            # Outside view findings
├── 03_inside_view_adjustments.json       # Case-specific factors
├── 04_scenario_models.json               # Multi-model weights and projections
├── 05_uncertainty_bounds.json            # Final (p10, median, p90) + distribution
├── 06_prediction.md                      # Final documented prediction
├── data/                                 # Downloaded data files
│   └── *.csv
├── plots/                                # Generated visualizations
│   └── *.png
└── scripts/                              # Analysis scripts for reproducibility
    └── *.py
```

### Resume Behavior

On startup:
1. Check if `waypoints/forecast_<name>/` exists for the given prediction
2. If exists, read `metadata.json` to determine completed phases
3. Display status: "Resuming forecast for X. Completed phases: 0-3. Next: Phase 4 (Multi-Model Weighting)"
4. Continue from last checkpoint

### metadata.json Structure

```json
{
  "name": "frontier_math_tier4_2026",
  "prediction_type": "quantitative",
  "target": "FrontierMath Tier 4 score by December 2026",
  "resolution_date": "2026-12-31",
  "resolution_criteria": "Official published score on FrontierMath Tier 4 by Epoch AI or paper",
  "created_at": "2025-01-15",
  "updated_at": "2025-01-18",
  "completed_phases": [0, 1, 2, 3],
  "current_phase": 4,
  "status": "in_progress"
}
```

---

## Workflow Phases

| Phase | Name | Purpose | Output File | Checkpoint Question |
|-------|------|---------|-------------|---------------------|
| 0 | Question Clarification | Define prediction target precisely | `metadata.json` | Does this have unambiguous resolution criteria? |
| 1 | Information Prioritization | Identify high-value research areas | `01_research_priorities.json` | Have you identified 2-3 priority factors? |
| 2 | Outside View | Establish base rate anchor | `02_base_rate_analysis.json` | Have you anchored to a reference class? |
| 3 | Inside View | Case-specific adjustments | `03_inside_view_adjustments.json` | Have you generated 3+ competing hypotheses? |
| 4 | Multi-Model Weighting | Combine scenarios with weights | `04_scenario_models.json` | Do weights sum to 1.0 with clear rationale? |
| 5 | Uncertainty Quantification | Generate confidence bounds | `05_uncertainty_bounds.json` | Are bounds wider than pure statistical CI? |
| 6 | Documentation | Create final artifacts | `06_prediction.md` + scripts/plots | Are all artifacts generated? |

---

## Execution Instructions

### Phase Execution Pattern

For each phase:
1. **Load reference**: Read the phase-specific reference file from `references/0X-<phase>.md`
2. **Execute guidance**: Follow the structured steps in the reference file
3. **Save checkpoint**: Write results to the appropriate JSON/markdown file
4. **Verify with user**: Ask the checkpoint question before proceeding
5. **Update metadata**: Mark phase as complete in `metadata.json`

### On-Demand Reference Loading

Only load reference files when executing that phase (saves context):

```
Phase 0 → Read: references/00-question-clarification.md
Phase 1 → Read: references/01-information-prioritization.md
Phase 2 → Read: references/02-outside-view.md
Phase 3 → Read: references/03-inside-view.md
Phase 4 → Read: references/04-multi-model-weighting.md
Phase 5 → Read: references/05-uncertainty-quantification.md
Phase 6 → Read: references/06-documentation.md
```

Standalone references (load as needed):
- `references/superforecasting-principles.md` - Core techniques
- `references/combining-forecasts.md` - Aggregation methods
- `references/common-distributions.md` - Distribution selection
- `references/anti-patterns.md` - Common mistakes

### Utility Scripts

Available in `scripts/` directory:
- `distributions.py` - Fit distributions from percentiles, aggregation functions
- `base_rates.py` - Reference class calculations, velocity analysis

Copy scripts to waypoint directory when generating analysis code.

---

## Phase 0: Question Clarification

**Goal**: Ensure the prediction target is precisely defined before any analysis.

**Ask the user**:
1. What exactly are you trying to predict?
2. What is the resolution date or timeframe?
3. What would count as resolving YES vs NO (binary) or how will the value be measured (quantitative)?
4. Do you have a current intuition? (Record but don't anchor to it yet)
5. What evidence would significantly change your mind?

**Determine prediction type**:
- **Quantitative**: Numeric outcome → will produce (p10, median, p90) bounds
- **Binary**: Yes/no outcome → will produce calibrated probability

**Create waypoint directory and metadata.json**:
```bash
mkdir -p waypoints/forecast_<name>/data waypoints/forecast_<name>/plots waypoints/forecast_<name>/scripts
```

**Checkpoint**: Does this prediction have unambiguous resolution criteria that a neutral third party could verify?

→ If yes, proceed to Phase 1
→ If no, refine criteria with user

---

## Phase 1-6: Load Reference Files

For phases 1-6, load and follow the corresponding reference file:

```
Read: .claude/skills/forecast/references/0X-<phase-name>.md
```

Execute the guidance in the reference file, save outputs, and verify checkpoint before proceeding.

---

## Update Mode

When updating an existing forecast:

1. Load the existing waypoint directory
2. Ask: "What new information do you have?"
3. Document the new evidence
4. Determine if revision is warranted:
   - Is the evidence diagnostic (would it change P(outcome|evidence) significantly)?
   - What's the likelihood ratio?
5. Apply Bayesian update or re-run relevant phases
6. Document the update in `metadata.json` (add to update log)
7. Save revised prediction

---

## Score Mode

When scoring past predictions:

1. Load predictions from waypoints or a CSV file
2. For each resolved prediction:
   - Record actual outcome
   - Calculate Brier score: `(predicted_prob - outcome)^2`
   - Calculate log score: `-outcome*log(p) - (1-outcome)*log(1-p)`
3. Aggregate scores
4. Generate calibration plot (predicted probability vs actual frequency)
5. Identify systematic biases

---

## Anti-Pattern Checks

Throughout the workflow, watch for these common mistakes:

- **Starting with inside view**: Always establish base rate first (Phase 2 before Phase 3)
- **Round probabilities**: Avoid 20%, 50%, 80% → use granular values like 23%, 47%, 78%
- **Single hypothesis**: Generate at least 3 competing scenarios
- **Underweighting "other"**: MECE decomposition should account for unlisted outcomes
- **Overconfidence**: Be skeptical of <5% or >95% without exceptional evidence
- **Identical timeframe estimates**: Different timeframes should have different predictions
- **Statistical bounds only**: Add model uncertainty and tail risk to pure CI

---

## Example Invocations

**New quantitative forecast**:
```
User: /forecast
Assistant: [Asks which mode]
User: New forecast
Assistant: [Asks what to predict]
User: FrontierMath Tier 4 score by end of 2026
Assistant: [Begins Phase 0: Question Clarification]
```

**Resume existing forecast**:
```
User: /forecast
Assistant: [Detects existing waypoint]
Assistant: "Found existing forecast: frontier_math_tier4_2026. Completed phases: 0-3. Resume Phase 4?"
```

**Update with new information**:
```
User: /forecast
Assistant: [Asks which mode]
User: Update existing
Assistant: [Lists existing forecasts]
User: frontier_math_tier4_2026
Assistant: "What new information do you have?"
```
