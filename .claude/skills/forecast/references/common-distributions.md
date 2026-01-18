# Common Distributions for Forecasting

Guide to selecting and fitting probability distributions, based on Steinhardt's forecasting course.

---

## Distribution Selection Flowchart

```
Is the outcome bounded?
├── No → Is it multiplicative or additive?
│   ├── Additive → Normal
│   └── Multiplicative → Log-normal
└── Yes → What are the bounds?
    ├── [0, 1] (proportions) → Beta
    ├── [0, ∞) (counts) → Is it rare events?
    │   ├── Yes → Poisson
    │   └── No → Log-normal or Gamma
    └── [a, b] (other bounds) → Truncated normal or Beta (scaled)
```

---

## Normal Distribution

**When to use**:
- Sum of many small, independent factors
- Symmetric uncertainty around a central estimate
- Errors are additive

**Examples**:
- Temperature anomalies
- Measurement errors
- Height differences from population mean

**Parameters**: μ (mean), σ (standard deviation)

**Fitting from percentiles**:
```python
from scipy import stats

# If you have p10, p50 (median), p90
# For normal: median = mean
mu = median
# p90 - p50 should equal z_0.9 * sigma
sigma = (p90 - median) / stats.norm.ppf(0.9)

dist = stats.norm(loc=mu, scale=sigma)
```

**Reality check**: If values can't be negative, normal may not be appropriate.

---

## Log-Normal Distribution

**When to use**:
- Product of many small, independent factors
- Right-skewed distribution (long right tail)
- Values must be positive
- Percentage changes are more natural than absolute changes

**Examples**:
- Revenue, market caps, valuations
- Time durations
- Population sizes
- Resource consumption

**Parameters**: μ (mean of log), σ (std of log)

**Fitting from percentiles**:
```python
from scipy import stats
import numpy as np

# For log-normal: median = exp(mu)
mu = np.log(median)
# p90/p50 = exp(z_0.9 * sigma)
sigma = np.log(p90 / median) / stats.norm.ppf(0.9)

dist = stats.lognorm(s=sigma, scale=np.exp(mu))
```

**Detecting log-normal**: If p90/median ≠ median/p10, you likely have asymmetry suggesting log-normal.

---

## Truncated Normal Distribution

**When to use**:
- Would be normal, but outcomes are bounded
- Benchmark scores (0-100%)
- Physical quantities with limits

**Examples**:
- Test scores
- Accuracy percentages
- Capacity utilization

**Parameters**: μ (underlying mean), σ (underlying std), a (lower bound), b (upper bound)

**Fitting**:
```python
from scipy import stats

# Bounds
a, b = 0, 100  # Example: percentage

# Convert to standard form
a_std = (a - median) / estimated_sigma
b_std = (b - median) / estimated_sigma

dist = stats.truncnorm(a_std, b_std, loc=median, scale=estimated_sigma)
```

**Caution**: Near boundaries, truncated normal behavior changes significantly.

---

## Beta Distribution

**When to use**:
- Outcomes bounded on [0, 1]
- Proportions, probabilities
- More flexible shape than truncated normal

**Examples**:
- Conversion rates
- Market share
- Success probabilities

**Parameters**: α (alpha), β (beta)
- α = β: symmetric around 0.5
- α > β: skewed toward 1
- α < β: skewed toward 0
- Larger α + β: narrower distribution

**Fitting from percentiles**:
```python
from scipy import stats
from scipy.optimize import minimize

def fit_beta(p10, median, p90):
    def loss(params):
        a, b = params
        dist = stats.beta(a, b)
        return (
            (dist.ppf(0.1) - p10)**2 +
            (dist.ppf(0.5) - median)**2 +
            (dist.ppf(0.9) - p90)**2
        )
    result = minimize(loss, [2, 2], bounds=[(0.1, 100), (0.1, 100)])
    return stats.beta(*result.x)
```

---

## Poisson Distribution

**When to use**:
- Counting rare, independent events
- Number of occurrences in fixed time/space
- Events happen at constant average rate

**Examples**:
- Number of major breakthroughs per year
- Number of failures/accidents
- Arrival counts

**Parameter**: λ (lambda) = expected count

**Key property**: Mean = Variance = λ

**Fitting**:
```python
from scipy import stats

# Lambda is just the expected count
lambda_param = expected_count
dist = stats.poisson(mu=lambda_param)
```

---

## Power Law Distribution

**When to use**:
- Scale invariance (no characteristic scale)
- "Rich get richer" dynamics
- Extreme outliers are common

**Examples**:
- City populations
- Wealth distribution
- Citation counts
- File sizes

**Parameters**: α (tail exponent), x_min (minimum value)

**Warning**: Power laws are often over-applied. Verify with log-log plot linearity.

**Fitting**:
```python
# Power law fitting is tricky - use dedicated library
# pip install powerlaw
import powerlaw
fit = powerlaw.Fit(data)
print(f"Alpha: {fit.alpha}, x_min: {fit.xmin}")
```

---

## Fitting from Percentiles (General Method)

When you only have (p10, median, p90) estimates:

```python
from scipy import stats
from scipy.optimize import minimize

def fit_from_percentiles(p10, median, p90, dist_type='auto'):
    """
    Fit distribution from elicited percentiles.

    dist_type: 'normal', 'lognormal', 'truncnorm', 'beta', or 'auto'
    """
    # Auto-detect based on asymmetry
    if dist_type == 'auto':
        upper_range = p90 - median
        lower_range = median - p10
        asymmetry = upper_range / lower_range if lower_range > 0 else float('inf')

        if asymmetry > 1.5 or asymmetry < 0.67:
            dist_type = 'lognormal'
        else:
            dist_type = 'normal'

    if dist_type == 'normal':
        mu = median
        sigma = (p90 - median) / stats.norm.ppf(0.9)
        return stats.norm(loc=mu, scale=sigma)

    elif dist_type == 'lognormal':
        import numpy as np
        mu = np.log(median)
        sigma = np.log(p90 / median) / stats.norm.ppf(0.9)
        return stats.lognorm(s=sigma, scale=np.exp(mu))

    # Add other distributions as needed
```

---

## Verifying Distribution Choice

### Visual Checks
1. **Histogram**: Does the fitted distribution match data shape?
2. **Q-Q plot**: Do quantiles align on a straight line?
3. **CDF comparison**: Does empirical CDF match fitted CDF?

### Statistical Tests
- **Kolmogorov-Smirnov test**: Compares empirical vs fitted CDF
- **Anderson-Darling test**: More sensitive to tails
- **Chi-square goodness of fit**: For discrete distributions

### Practical Check
Ask: "Does this distribution assign reasonable probability to extreme outcomes?"
- If distribution says P(extreme) < 0.01% but you can imagine it happening, reconsider
- Tail behavior matters for risk assessment

---

## Quick Reference Table

| Scenario | Distribution | Parameters to Estimate |
|----------|--------------|----------------------|
| Symmetric, unbounded | Normal | mean, std |
| Right-skewed, positive | Log-normal | log-mean, log-std |
| Bounded 0-100% | Truncated normal or Beta | varies |
| Proportion/probability | Beta | alpha, beta |
| Counting rare events | Poisson | lambda (expected count) |
| Extreme outliers common | Power law | alpha, x_min |
