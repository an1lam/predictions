# Phase 0: Question Clarification

**Purpose**: Ensure the prediction target is precisely defined before any analysis begins.

---

## Detect Prediction Type

Ask the user to describe what they want to predict, then classify:

### Quantitative Predictions
- Numeric target (benchmark score, revenue, metric, count)
- Will produce: (10th percentile, median, 90th percentile) bounds
- Examples: "FrontierMath Tier 4 score", "GPT-5 MMLU accuracy", "Revenue in Q4"

### Binary Predictions
- Yes/no outcome with probability
- Will produce: Calibrated probability (e.g., 37%)
- Examples: "Will AGI be achieved by 2030?", "Will company X be acquired?"

---

## Information to Collect

### 1. Exact Resolution Criteria
Ask: "How will we know the outcome? What specific measurement or event determines resolution?"

**Good criteria** (unambiguous):
- "Score on benchmark X as reported by organization Y"
- "Official announcement of event Z by source W"
- "Value published in dataset D on date T"

**Problematic criteria** (refine these):
- "When AI gets really good" → What specific capability? Measured how?
- "When the economy improves" → Which metric? Compared to what baseline?
- "If the project succeeds" → Define success criteria precisely

### 2. Resolution Date/Timeframe
Ask: "By when does this need to resolve? Is there a hard deadline?"

- Specific date: "December 31, 2026"
- Event-triggered: "Within 6 months of GPT-5 release"
- Rolling: "At any point during 2026"

### 3. Current Intuition
Ask: "Do you have a gut feeling about the outcome? (I'll record it but we won't anchor to it)"

Record their intuition but explicitly note this is pre-analysis. The structured process may produce a different result.

### 4. Evidence That Would Change Their Mind
Ask: "What evidence would significantly update your belief? What would make you much more or less confident?"

This reveals:
- Key uncertainties in their mental model
- Potential research priorities for Phase 1
- Implicit assumptions to examine

---

## Create Waypoint Directory

Once criteria are clear, create the waypoint structure:

```bash
mkdir -p waypoints/forecast_<name>/data waypoints/forecast_<name>/plots waypoints/forecast_<name>/scripts
```

Where `<name>` is a snake_case identifier (e.g., `frontier_math_tier4_2026`, `gpt5_release_2025`).

---

## Write metadata.json

```json
{
  "name": "<snake_case_name>",
  "prediction_type": "quantitative|binary",
  "target": "<full description of prediction target>",
  "resolution_date": "<YYYY-MM-DD or description>",
  "resolution_criteria": "<precise criteria for resolution>",
  "initial_intuition": "<user's pre-analysis gut feeling, if provided>",
  "evidence_that_would_update": ["<list of evidence types>"],
  "created_at": "<today's date>",
  "updated_at": "<today's date>",
  "completed_phases": [0],
  "current_phase": 1,
  "status": "in_progress"
}
```

---

## Checkpoint

Before proceeding to Phase 1, verify:

**Ask the user**: "Does this prediction have unambiguous resolution criteria that a neutral third party could verify?"

- If **YES**: Proceed to Phase 1 (Information Prioritization)
- If **NO**: Refine the criteria together until they pass this test

Common issues to address:
- Vague terms that need operational definitions
- Multiple possible interpretations
- Unclear data sources
- Ambiguous edge cases
