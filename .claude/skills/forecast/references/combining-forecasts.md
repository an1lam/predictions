# Combining Forecasts

Aggregation methods from Jacob Steinhardt's forecasting course and ensemble prediction research.

---

## Why Combine Forecasts?

Combining multiple forecasts typically outperforms any individual forecast:
- **Wisdom of crowds**: Errors cancel out when forecasters are independent
- **Jensen's inequality**: Mean of forecasts beats mean forecaster accuracy
- **Model uncertainty**: No single model captures all relevant factors

---

## Basic Aggregation Methods

### Simple Mean
```python
combined = sum(forecasts) / len(forecasts)
```

**When to use**:
- Forecasters/models have roughly equal quality
- No strong reason to prefer one over another
- You want robustness to outliers (somewhat)

**Advantage**: Simple, hard to get wrong, surprisingly effective

### Weighted Mean
```python
combined = sum(w_i * f_i for w_i, f_i in zip(weights, forecasts)) / sum(weights)
```

**When to use**:
- Track records differ significantly
- Some models have better theoretical grounding
- You have evidence for differential quality

**Weighting options**:
- Past accuracy (Brier score, log score)
- Inverse variance
- Expertise-based assessment

### Trimmed Mean
```python
sorted_forecasts = sorted(forecasts)
trim_count = int(len(forecasts) * trim_pct)
trimmed = sorted_forecasts[trim_count:-trim_count] if trim_count > 0 else sorted_forecasts
combined = sum(trimmed) / len(trimmed)
```

**When to use**:
- Outliers might be noise rather than signal
- You want robustness to a few bad forecasts
- Sample size is large enough to afford trimming

---

## Advanced Aggregation

### Median
```python
combined = sorted(forecasts)[len(forecasts) // 2]
```

**When to use**:
- Extreme robustness to outliers needed
- Distribution of forecasts is skewed
- You suspect some forecasts are systematically biased

### Geometric Mean (for probabilities)
```python
log_mean = sum(log(f) for f in forecasts) / len(forecasts)
combined = exp(log_mean)
```

**When to use**:
- Combining probability estimates
- Preventing one extreme forecast from dominating
- Log-odds space averaging is more appropriate

### Log-Odds Averaging
```python
def prob_to_log_odds(p):
    return log(p / (1 - p))

def log_odds_to_prob(lo):
    return 1 / (1 + exp(-lo))

log_odds = [prob_to_log_odds(p) for p in probabilities]
mean_log_odds = sum(log_odds) / len(log_odds)
combined = log_odds_to_prob(mean_log_odds)
```

**When to use**:
- Aggregating probabilities
- When you want to treat 10% and 90% symmetrically
- Standard method in many aggregation systems

---

## Extremizing

**Push combined probability away from 50% to account for information overlap.**

**Rationale**: When forecasts are correlated (share information), simple averaging understates the evidence. Extremizing recovers some of this.

```python
def extremize(probability, factor=1.5):
    """
    Push probability away from 0.5 using log-odds transform.
    factor > 1: more extreme
    factor < 1: less extreme
    """
    if probability <= 0 or probability >= 1:
        return probability
    log_odds = log(probability / (1 - probability))
    extremized_log_odds = log_odds * factor
    return 1 / (1 + exp(-extremized_log_odds))
```

**When to use**:
- Aggregating multiple forecasters who share information
- Individual forecasters are well-calibrated but conservative
- NOT when you're the only forecaster (don't double-count your own information)

**Typical factors**:
- 1.2-1.5: Moderate extremizing
- 1.5-2.0: Aggressive extremizing
- 1.0: No extremizing (equivalent to log-odds mean)

---

## Combining Confidence Intervals

### Method 1: Union (Conservative)
Take the outer bounds:
```python
combined_low = min(f.low for f in forecasts)
combined_high = max(f.high for f in forecasts)
```

Pros: Never overconfident
Cons: Can be very wide

### Method 2: Weighted Average of Bounds
```python
combined_low = sum(w * f.low for w, f in zip(weights, forecasts)) / sum(weights)
combined_high = sum(w * f.high for w, f in zip(weights, forecasts)) / sum(weights)
```

Pros: Accounts for relative quality
Cons: May still underestimate uncertainty

### Method 3: Account for Disagreement
Include between-model variance:
```python
point_estimates = [f.point for f in forecasts]
mean_point = mean(point_estimates)
model_variance = variance(point_estimates)

# Combined uncertainty = average within-model + between-model
within_variance = mean((f.high - f.low)**2 / 4 for f in forecasts)  # Approx
total_variance = within_variance + model_variance
combined_se = sqrt(total_variance)
```

---

## Delphi Method (Team Forecasting)

Structured process for group predictions:

1. **Round 1**: Each forecaster makes independent prediction with reasoning
2. **Share**: Distribute anonymized predictions and rationales
3. **Round 2**: Forecasters update based on others' reasoning
4. **Iterate**: Repeat until convergence or stopping criterion
5. **Aggregate**: Combine final predictions

**Benefits**:
- Reduces anchoring to first speaker
- Surfaces diverse considerations
- Allows learning from others

---

## When Aggregation Fails

Aggregation works best when:
- Forecasters have diverse information sources
- Errors are independent (not correlated)
- No systematic bias affects all forecasters

**Warning signs**:
- All forecasters share the same information
- Group has similar backgrounds/training
- Common bias (e.g., everyone overconfident)
- One forecaster dominates discussion

---

## Practical Guidelines

1. **Start with simple mean** — it's hard to beat consistently
2. **Weight by track record** if you have enough data (20+ predictions)
3. **Trim outliers** if sample size > 5 and some forecasts seem unreasonable
4. **Extremize 1.2-1.5x** when aggregating correlated forecasters
5. **Use log-odds space** for probability aggregation
6. **Always include model disagreement** in confidence intervals
