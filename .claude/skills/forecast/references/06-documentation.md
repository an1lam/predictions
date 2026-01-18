# Phase 6: Documentation

**Purpose**: Create reproducible artifacts that document the prediction, analysis, and reasoning for future reference and postmortem analysis.

---

## Artifacts to Generate

By the end of this phase, the waypoint directory should contain:

```
waypoints/forecast_<name>/
├── metadata.json                 # Updated with completed_phases: [0-6]
├── 01_research_priorities.json
├── 02_base_rate_analysis.json
├── 03_inside_view_adjustments.json
├── 04_scenario_models.json
├── 05_uncertainty_bounds.json
├── 06_prediction.md              # ← Final documented prediction (this phase)
├── data/
│   └── *.csv                     # ← Downloaded/processed data
├── plots/
│   └── *.png                     # ← Visualizations
└── scripts/
    └── *.py                      # ← Reproducible analysis scripts
```

---

## 1. Analysis Script

Create a Python script that reproduces the key analysis:

### Script Requirements
- Load and process data
- Fit trend/regression models
- Generate scenario projections
- Calculate final bounds
- Create visualization(s)
- Print summary statistics

### Script Template

```python
#!/usr/bin/env python
"""
Analysis script for: <prediction name>
Generated: <date>

Reproduces the analysis for the forecast.
Run with: uv run python waypoints/forecast_<name>/scripts/analysis.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from datetime import datetime

# --- Configuration ---
TARGET_DATE = "<resolution date>"
PREDICTION_NAME = "<name>"

# --- Load Data ---
data = pd.read_csv("../data/<datafile>.csv")

# --- Trend Analysis ---
# <regression fitting code>

# --- Scenario Projections ---
scenarios = {
    "conservative": <value>,
    "moderate": <value>,
    "optimistic": <value>
}
weights = {
    "conservative": <weight>,
    "moderate": <weight>,
    "optimistic": <weight>
}

# --- Final Prediction ---
weighted_estimate = sum(scenarios[k] * weights[k] for k in scenarios)
p10 = <value>
median = <value>
p90 = <value>

print(f"Prediction: {PREDICTION_NAME}")
print(f"Resolution date: {TARGET_DATE}")
print(f"10th percentile: {p10}")
print(f"Median: {median}")
print(f"90th percentile: {p90}")

# --- Visualization ---
# <plotting code>
plt.savefig("../plots/<prediction_name>.png", dpi=150, bbox_inches="tight")
print("Plot saved to ../plots/<prediction_name>.png")
```

---

## 2. Visualization

Create at least one plot showing:

### For Quantitative Predictions
- Historical data points
- Trend line with confidence band
- Scenario projections (if multiple)
- Final prediction range (p10, median, p90)
- Target date marked

### For Binary Predictions
- Reference class frequencies (if available)
- Probability with uncertainty range
- Key factors visualization (optional)

### Plot Style Guidelines
- Clear labels and title
- Legend explaining different lines/bands
- Consistent color scheme
- Save at 150+ DPI for readability

---

## 3. Final Prediction Markdown

Create `06_prediction.md` with the following structure:

```markdown
# Prediction: <Target Description>

**Prediction type**: Quantitative / Binary
**Created**: <date>
**Resolution date**: <date>
**Resolution criteria**: <precise criteria>

## Summary

<1-2 paragraph summary of the prediction and key reasoning>

## Current State

- **Current value**: <most recent measurement>
- **Data source**: <where data came from>
- **As of**: <date of measurement>

## Base Rate Analysis (Outside View)

<Summary of reference class and historical analysis>

- Reference class: <description>
- Historical trend: <description>
- Base rate anchor: <value>

## Adjustment Factors (Inside View)

| Factor | Direction | Magnitude | Notes |
|--------|-----------|-----------|-------|
| <factor 1> | + | Moderate | <brief reason> |
| <factor 2> | - | Small | <brief reason> |

## Scenario Analysis

| Scenario | Estimate | Weight | Key Assumption |
|----------|----------|--------|----------------|
| Conservative | <value> | <weight> | <assumption> |
| Moderate | <value> | <weight> | <assumption> |
| Optimistic | <value> | <weight> | <assumption> |

## Final Prediction

| Percentile | Value |
|------------|-------|
| 10th (low) | <p10> |
| 50th (median) | <median> |
| 90th (high) | <p90> |

**Distribution**: <type and parameters>

## Confidence Notes

- <Key source of uncertainty #1>
- <Key source of uncertainty #2>
- <What would cause outcome outside bounds>

## Tail Scenarios

**Downside** (outside p10): <specific scenario>

**Upside** (outside p90): <specific scenario>

## Files

- Data: `data/<filename>.csv`
- Analysis: `scripts/analysis.py`
- Plot: `plots/<prediction_name>.png`

---

*Generated using /forecast skill*
```

---

## 4. Update metadata.json

Mark all phases as complete:

```json
{
  "completed_phases": [0, 1, 2, 3, 4, 5, 6],
  "current_phase": null,
  "status": "complete",
  "updated_at": "<today's date>"
}
```

---

## Quality Checklist

Before marking complete, verify:

### Data
- [ ] All data files saved to `data/` directory
- [ ] Data sources documented
- [ ] Data is reproducible (could re-download if needed)

### Scripts
- [ ] Analysis script runs without errors
- [ ] Script reproduces the key numbers in the prediction
- [ ] Script generates the visualization

### Visualization
- [ ] Plot is readable and well-labeled
- [ ] Key information (prediction, bounds) clearly shown
- [ ] Saved to `plots/` directory

### Documentation
- [ ] `06_prediction.md` contains all required sections
- [ ] Reasoning is clear enough for future reference
- [ ] Resolution criteria are unambiguous
- [ ] Tail scenarios documented

### Metadata
- [ ] `metadata.json` updated with status: "complete"
- [ ] All phases marked complete

---

## Checkpoint

Before completing the forecast:

**Ask the user**: "Are all artifacts generated (data, scripts, plots, documentation)? Is the reasoning clear enough for future postmortem?"

- If **YES**: Mark forecast complete
- If **NO**: Generate missing artifacts or clarify documentation

Final verification:
- Can someone else understand this prediction from the documentation alone?
- Could you reproduce this analysis in 6 months?
- Is there enough detail for a postmortem when the outcome is known?
