# Phase 4: Multi-Model Weighting

**Purpose**: Combine multiple scenarios or models into a single prediction with explicit weights and rationale.

---

## When to Use Multi-Model Weighting

Use this approach when:
- You have multiple plausible models with different assumptions
- Significant uncertainty exists about which model is correct
- Different methods give different answers (trend extrapolation vs. structural model)
- You've generated multiple scenarios in Phase 3

Skip to Phase 5 if:
- Only one model is clearly appropriate
- Scenarios converge to similar predictions
- The prediction is simple enough that weighting adds no value

---

## Aggregation Methods

From Steinhardt's forecasting course:

### Simple Mean
When to use: Forecasters or models are roughly equal quality

```python
combined = sum(predictions) / n
```

### Weighted Mean
When to use: Model quality differs based on track record or theoretical grounding

```python
combined = sum(weight_i * prediction_i) / sum(weights)
```

### Trimmed Mean
When to use: Outlier scenarios exist that might be noise

```python
# Remove top and bottom X% before averaging
sorted_predictions = sorted(predictions)
trimmed = sorted_predictions[trim:-trim]
combined = sum(trimmed) / len(trimmed)
```

---

## Weighting Principles

### Higher Weight For:
- **Empirically grounded models**: Based on historical data, tested relationships
- **Simpler models**: Occam's razor, fewer assumptions to go wrong
- **Models with good track records**: Past accuracy on similar predictions
- **Models with clear mechanisms**: Understood causal pathways

### Lower Weight For:
- **Purely extrapolative models**: No structural understanding
- **Complex models with many parameters**: Overfitting risk
- **Speculative scenarios**: Based on weak evidence
- **Extreme outlier scenarios**: Unless strong evidence supports them

### Document Rationale
For each weight, write 1-2 sentences explaining why.

Bad: "Conservative scenario: 30%"
Good: "Conservative scenario: 30% — historical trend has been remarkably stable, but announced initiatives and competitive pressure make acceleration plausible"

---

## Combining Confidence Intervals

When combining multiple models with uncertainty:

### Model Disagreement as Uncertainty
If models disagree, this is a source of uncertainty beyond each model's individual CI.

```python
# Combined uncertainty includes:
# 1. Within-model uncertainty (each model's CI)
# 2. Between-model uncertainty (disagreement across models)

combined_variance = weighted_mean(individual_variances) + variance(model_predictions)
```

### Practical Approach
1. Calculate weighted mean of point estimates
2. Take the widest bounds across models (conservative)
3. Or: Fit distribution to scenario outcomes with weights

---

## Example: Three-Scenario Combination

From Phase 3, you have:

| Scenario | Point Estimate | Weight | Contribution |
|----------|---------------|--------|--------------|
| Conservative | 35% | 0.25 | 8.75% |
| Moderate | 45% | 0.50 | 22.5% |
| Optimistic | 60% | 0.25 | 15.0% |

**Weighted mean**: 8.75 + 22.5 + 15.0 = 46.25%

**Bounds from scenarios**:
- 10th percentile: Conservative estimate (or lower)
- 90th percentile: Optimistic estimate (or higher)

---

## Extremizing

From Steinhardt: When aggregating, consider "extremizing" — pushing probabilities away from 50%.

**Rationale**: Individual forecasts often underweight the information they contain. Aggregation can recover some of this.

```python
def extremize(probability, factor=1.5):
    """Push probability away from 0.5 using log-odds transform"""
    if probability <= 0 or probability >= 1:
        return probability
    log_odds = log(probability / (1 - probability))
    extremized_log_odds = log_odds * factor
    return 1 / (1 + exp(-extremized_log_odds))
```

Use extremizing when:
- Combining multiple independent forecasters
- Forecasters are well-calibrated but conservative
- NOT when you're the only forecaster (don't double-count)

---

## Output: 04_scenario_models.json

```json
{
  "phase": 4,
  "completed_at": "<timestamp>",

  "models": [
    {
      "name": "Conservative",
      "point_estimate": 35,
      "confidence_interval": [28, 42],
      "weight": 0.25,
      "weight_rationale": "<why this weight>"
    },
    {
      "name": "Moderate",
      "point_estimate": 45,
      "confidence_interval": [38, 52],
      "weight": 0.50,
      "weight_rationale": "<why this weight>"
    },
    {
      "name": "Optimistic",
      "point_estimate": 60,
      "confidence_interval": [50, 72],
      "weight": 0.25,
      "weight_rationale": "<why this weight>"
    }
  ],

  "aggregation": {
    "method": "weighted_mean",
    "weighted_point_estimate": 46.25,
    "extremizing_applied": false,
    "extremizing_factor": null
  },

  "weight_validation": {
    "weights_sum_to_one": true,
    "total_weight": 1.0
  },

  "combined_estimate": {
    "point_estimate": 46.25,
    "preliminary_bounds": {
      "p10": 32,
      "p90": 65,
      "method": "scenario range with buffer"
    }
  },

  "notes": "<any additional reasoning or caveats>"
}
```

---

## Checkpoint

Before proceeding to Phase 5, verify:

**Ask the user**: "Do the scenario weights sum to 1.0, and is there clear rationale documented for each weight?"

- If **YES**: Proceed to Phase 5 (Uncertainty Quantification)
- If **NO**: Adjust weights or add rationale documentation

Also verify:
- Are any scenarios getting zero weight? (Consider removing them)
- Are weights dominated by a single scenario? (Is this justified?)
- Have you considered whether extremizing is appropriate?
