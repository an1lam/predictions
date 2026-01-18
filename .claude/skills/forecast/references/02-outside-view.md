# Phase 2: Outside View

**Purpose**: Establish a base rate anchor before considering case-specific details. This is the most important step in avoiding overconfident predictions.

---

## Core Principle

From Tetlock's superforecasting research: The #1 predictor of forecasting accuracy is starting with the outside view.

**Inside view** (avoid first): "This specific situation has these unique characteristics, so I predict X"

**Outside view** (start here): "In the reference class of similar situations, what typically happens?"

---

## For Quantitative Predictions

### Step 1: Gather Historical Data
Find time series data for the metric you're predicting:
- Official benchmark leaderboards
- Published datasets (Epoch AI, Papers With Code, etc.)
- Academic papers with historical measurements
- Industry reports

Save data to `waypoints/forecast_<name>/data/`.

### Step 2: Calculate Trend/Regression
Fit appropriate model to historical data:

**Linear**: Constant absolute improvement over time
- `y = a + b*t`
- Use when: Additive progress, bounded metrics

**Log-linear (exponential)**: Constant percentage improvement
- `log(y) = a + b*t` or `y = a * e^(b*t)`
- Use when: Multiplicative progress, unbounded metrics

**Sigmoid/logistic**: S-curve with saturation
- `y = L / (1 + e^(-k*(t-t0)))`
- Use when: Approaching ceiling (100% accuracy, physical limits)

Generate prediction with statistical confidence intervals (e.g., 90% CI from regression).

### Step 3: Reference Class Velocity
For benchmarks, calculate improvement rate at comparable stages:

```python
# Example: How fast did similar benchmarks improve from 20% to 40%?
velocity = (end_score - start_score) / days_elapsed  # pp/month or pp/year
```

Compare to other benchmarks at similar difficulty stages. This anchors expectations about plausible improvement rates.

---

## For Binary Predictions

### Step 1: Identify Reference Class
Find the category of similar events that includes your prediction:

**Too narrow** (overfitting): "Predictions about GPT-5 specifically"
**Too broad** (uninformative): "Predictions about technology"
**Just right**: "Predictions about major AI lab product releases" or "Predictions about achieving benchmark thresholds"

The reference class should have enough historical examples to estimate a base rate.

### Step 2: Calculate Base Rate
Count historical frequency in the reference class:

```
Base rate = (# times event occurred) / (# opportunities for event)
```

If no clear precedent exists, start at 50% (maximum uncertainty).

### Step 3: Apply Appropriate Uncertainty
For small sample sizes, use Wilson confidence interval:

```python
from scipy.stats import binom

def wilson_ci(successes, trials, confidence=0.9):
    # Returns (lower, upper) bounds on true probability
```

---

## Key Techniques

### MECE Decomposition
Ensure your outcome categories are:
- **M**utually **E**xclusive: No overlap between categories
- **C**ollectively **E**xhaustive: All possibilities covered

Common mistake: Underweighting "other" outcomes in seemingly binary questions.

Example: "Will OpenAI or Anthropic release AGI first?"
- This ignores: DeepMind, Meta, startups, no one achieves it, definitional disputes

### Hidden Alternatives
Many "binary" questions have hidden alternatives:
- "Will X happen?" → X happens / X doesn't happen / Question becomes moot
- "Will A or B win?" → A / B / Neither / Both / Unclear winner

Account for these in your base rate.

### Reference Class Adjustment
If your case differs systematically from the reference class, note this for Phase 3 (Inside View). But establish the anchor first.

---

## Data Sources

### Benchmarks and AI Progress
- Epoch AI: https://epochai.org/data
- Papers With Code: https://paperswithcode.com/
- Official benchmark leaderboards

### Historical Events
- Wikipedia timelines
- News archives
- Academic databases
- Industry reports

### Base Rate Databases
- Metaculus track record
- Superforecaster historical accuracy
- Domain-specific frequency tables

---

## Output: 02_base_rate_analysis.json

```json
{
  "phase": 2,
  "completed_at": "<timestamp>",
  "prediction_type": "quantitative|binary",

  // For quantitative:
  "historical_data": {
    "source": "<where data came from>",
    "file": "data/<filename>.csv",
    "date_range": "<start> to <end>",
    "current_value": "<most recent measurement>",
    "current_date": "<date of measurement>"
  },
  "trend_analysis": {
    "model_type": "linear|log_linear|sigmoid",
    "parameters": {},
    "r_squared": 0.85,
    "extrapolation": {
      "target_date": "<resolution date>",
      "point_estimate": 42.5,
      "ci_90_lower": 35.0,
      "ci_90_upper": 50.0
    }
  },
  "velocity_comparison": {
    "current_velocity": "<rate of change>",
    "comparable_benchmarks": [
      {"name": "<benchmark>", "velocity_at_similar_stage": "<rate>"}
    ]
  },

  // For binary:
  "reference_class": {
    "description": "<what category of events>",
    "examples": ["<past events in class>"],
    "historical_frequency": {
      "successes": 12,
      "trials": 30,
      "base_rate": 0.40,
      "wilson_ci_90": [0.28, 0.54]
    }
  },

  "base_rate_anchor": "<the outside view estimate>",
  "notes": "<any caveats or limitations>"
}
```

---

## Checkpoint

Before proceeding to Phase 3, verify:

**Ask the user**: "Have you established a base rate anchor from reference class or historical data before considering case-specific factors?"

- If **YES**: Proceed to Phase 3 (Inside View)
- If **NO**: Find appropriate reference class or historical data first

Also verify:
- Is the reference class neither too narrow nor too broad?
- Have you accounted for hidden alternatives?
- Is the statistical confidence interval calculated correctly?
