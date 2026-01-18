# Phase 5: Uncertainty Quantification

**Purpose**: Generate honest confidence bounds that account for statistical uncertainty, model uncertainty, and tail risks.

---

## The Three-Layer Approach

Prediction uncertainty comes from multiple sources. Account for all three:

### Layer 1: Statistical Uncertainty
Uncertainty from limited data and measurement noise.
- Regression confidence intervals
- Sampling uncertainty in base rates
- Measurement error

### Layer 2: Model Uncertainty
Uncertainty about which model is correct.
- Disagreement across scenarios
- Structural uncertainty about causal mechanisms
- Parameter uncertainty within models

### Layer 3: Tail Risk
Possibility of extreme outcomes outside normal models.
- Unprecedented events
- Regime changes
- Unknown unknowns

**Key insight**: Pure statistical CIs (Layer 1 only) are almost always too narrow. Always add Layers 2 and 3.

---

## Quantifying Each Layer

### Layer 1: Statistical CI
From Phase 2 regression or base rate analysis:
```python
# Example: 90% CI from linear regression
ci_statistical = (lower_bound, upper_bound)
```

### Layer 2: Model Uncertainty
From Phase 4 scenario spread:
```python
# Variance across weighted scenarios
model_variance = weighted_variance(scenario_estimates, weights)

# Or simply: range from conservative to optimistic scenario
ci_model = (conservative_estimate, optimistic_estimate)
```

### Layer 3: Tail Risk Adjustment
Explicit probability mass for extreme scenarios:
```python
# Reserve X% probability for tail scenarios
tail_probability = 0.10  # 5% each tail

# Identify plausible extreme scenarios
extreme_low = <what could go really wrong>
extreme_high = <what could go surprisingly well>
```

---

## Generalized Tail Scenarios

**Not domain-specific** — apply these categories to any prediction:

### Downside Tail Examples
- Market disruption or demand collapse
- Regulatory or policy changes
- Competitive dynamics shifting unfavorably
- Technical plateau or diminishing returns
- Measurement methodology changes (benchmark becomes easier/harder)
- Resource constraints (funding, talent, compute)
- Organizational dysfunction or priority shifts
- External shocks (economic, geopolitical)

### Upside Tail Examples
- Breakthrough innovation or paradigm shift
- Unexpected synergies or compound effects
- Explicit prioritization by major players
- Favorable regulatory or policy environment
- Measurement methodology changes (favorable)
- Resource windfalls
- Competitive pressure driving acceleration
- Serendipitous discoveries

For each prediction, identify 2-3 specific tail scenarios from these categories.

---

## Combining Layers

### Approach 1: Additive Variance
```python
total_variance = stat_variance + model_variance + tail_adjustment
combined_ci = point_estimate ± z * sqrt(total_variance)
```

### Approach 2: Envelope Method
```python
# Take outer bounds across all sources
p10 = min(stat_p10, model_p10, tail_low * tail_prob_weight)
p90 = max(stat_p90, model_p90, tail_high * tail_prob_weight)
```

### Approach 3: Distribution Fitting (Recommended)
Fit a distribution to your scenario estimates and tail scenarios, then read off percentiles.

---

## Distribution Selection

From Steinhardt's course, choose distribution based on the data-generating process:

### Normal Distribution
- **When**: Additive factors, symmetric around mean
- **Examples**: Temperature anomalies, measurement errors
- **Fitting**: `scipy.stats.norm.fit(data)`

### Log-Normal Distribution
- **When**: Multiplicative factors, right-skewed, cannot be negative
- **Examples**: Revenues, populations, durations
- **Fitting**: `scipy.stats.lognorm.fit(data)`

### Truncated Normal
- **When**: Bounded outcomes (0-100%, physical limits)
- **Examples**: Benchmark scores, market shares
- **Fitting**: `scipy.stats.truncnorm.fit(data, a, b)`

### Beta Distribution
- **When**: Probabilities, proportions, bounded [0,1]
- **Examples**: Conversion rates, success probabilities
- **Fitting**: `scipy.stats.beta.fit(data)`

### Fit from Percentiles
If you only have (p10, median, p90) estimates:
```python
from scripts.distributions import fit_from_percentiles
dist = fit_from_percentiles(p10, median, p90, dist_type='auto')
```

---

## Final Bounds Calculation

### For Quantitative Predictions
Output: (10th percentile, median, 90th percentile)

```python
{
  "p10": lower_bound,      # "Things went worse than expected"
  "median": central_estimate,  # "Most likely outcome"
  "p90": upper_bound       # "Things went better than expected"
}
```

### For Binary Predictions
Output: Single probability with confidence notes

```python
{
  "probability": 0.37,
  "confidence_interval": [0.25, 0.50],  # Range based on model uncertainty
  "notes": "Wide CI due to limited reference class and scenario disagreement"
}
```

---

## Calibration Check

Before finalizing, verify bounds are appropriately wide:

### Red Flags for Overconfidence
- 80% CI narrower than pure statistical CI (you forgot model uncertainty)
- Less than 5% or greater than 95% probability (rare without exceptional evidence)
- Bounds exclude scenarios you generated in Phase 3
- Historical forecast accuracy suggests wider bounds needed

### Calibration Questions
- Would you bet at 9:1 odds outside your 90% CI?
- What specific evidence would need to exist for the outcome to fall outside bounds?
- Are there past predictions where your confidence was similar? Were you calibrated?

---

## Output: 05_uncertainty_bounds.json

```json
{
  "phase": 5,
  "completed_at": "<timestamp>",

  "uncertainty_layers": {
    "statistical": {
      "source": "regression 90% CI",
      "bounds": [38, 52]
    },
    "model": {
      "source": "scenario spread",
      "bounds": [35, 60]
    },
    "tail_risk": {
      "scenarios": [
        {"direction": "downside", "description": "<specific scenario>", "probability": 0.05},
        {"direction": "upside", "description": "<specific scenario>", "probability": 0.05}
      ],
      "bounds": [25, 75]
    }
  },

  "distribution": {
    "type": "truncated_normal|lognormal|beta|etc",
    "parameters": {},
    "fitted_from": "percentile estimates|scenario outcomes|historical data"
  },

  "final_prediction": {
    "prediction_type": "quantitative|binary",

    // For quantitative:
    "p10": 32,
    "median": 46,
    "p90": 65,

    // For binary:
    "probability": null,
    "probability_ci": null
  },

  "confidence_notes": [
    "<why bounds are set where they are>",
    "<key sources of uncertainty>",
    "<what would cause outcome outside bounds>"
  ],

  "calibration_check": {
    "bounds_wider_than_statistical_ci": true,
    "tail_scenarios_considered": true,
    "extreme_confidence_justified": "n/a|<justification if <5% or >95%>"
  }
}
```

---

## Checkpoint

Before proceeding to Phase 6, verify:

**Ask the user**: "Are the final bounds wider than pure statistical CI, and have you explicitly considered tail risk scenarios?"

- If **YES**: Proceed to Phase 6 (Documentation)
- If **NO**: Widen bounds or add tail scenario analysis

Also verify:
- Do bounds include all scenarios from Phase 3?
- Is the distribution choice justified?
- Are confidence notes explaining the key uncertainties?
