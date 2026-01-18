#!/usr/bin/env python
"""
Distribution utilities for forecasting.

Functions for fitting distributions from percentiles, sampling, and aggregation.
Based on techniques from Steinhardt's forecasting course.

Usage:
    from distributions import fit_from_percentiles, extremize, combine_distributions
"""

import numpy as np
from scipy import stats
from scipy.optimize import minimize
from typing import Union, List, Optional, Tuple
import matplotlib.pyplot as plt


# --- Core Distribution Fitting ---

def fit_from_percentiles(
    p10: float,
    median: float,
    p90: float,
    dist_type: str = 'auto',
    bounds: Optional[Tuple[float, float]] = None
) -> stats.rv_continuous:
    """
    Fit a distribution from elicited percentiles.

    Parameters
    ----------
    p10 : float
        10th percentile estimate
    median : float
        50th percentile (median) estimate
    p90 : float
        90th percentile estimate
    dist_type : str
        Distribution type: 'normal', 'lognormal', 'truncnorm', 'beta', or 'auto'
        If 'auto', detects based on asymmetry ratio
    bounds : tuple, optional
        (lower, upper) bounds for truncated distributions

    Returns
    -------
    scipy.stats distribution object (frozen)
    """
    # Auto-detect based on asymmetry
    if dist_type == 'auto':
        upper_range = p90 - median
        lower_range = median - p10
        if lower_range <= 0:
            dist_type = 'lognormal'
        else:
            asymmetry = upper_range / lower_range
            if asymmetry > 1.5:
                dist_type = 'lognormal'
            elif p10 >= 0 and p90 <= 1:
                dist_type = 'beta'
            elif bounds is not None:
                dist_type = 'truncnorm'
            else:
                dist_type = 'normal'

    if dist_type == 'normal':
        mu = median
        # p90 - median = z_0.9 * sigma, where z_0.9 ≈ 1.28
        sigma = (p90 - median) / stats.norm.ppf(0.9)
        return stats.norm(loc=mu, scale=sigma)

    elif dist_type == 'lognormal':
        # For lognormal: median = exp(mu), so mu = log(median)
        mu = np.log(median)
        # p90/median = exp(z_0.9 * sigma)
        sigma = np.log(p90 / median) / stats.norm.ppf(0.9)
        return stats.lognorm(s=sigma, scale=np.exp(mu))

    elif dist_type == 'truncnorm':
        if bounds is None:
            bounds = (0, 100)  # Default for percentages
        a, b = bounds

        # Estimate underlying normal parameters
        mu = median
        sigma = (p90 - median) / stats.norm.ppf(0.9)

        # Convert bounds to standard form
        a_std = (a - mu) / sigma
        b_std = (b - mu) / sigma

        return stats.truncnorm(a_std, b_std, loc=mu, scale=sigma)

    elif dist_type == 'beta':
        # Fit beta by optimization
        def loss(params):
            alpha, beta_param = params
            if alpha <= 0 or beta_param <= 0:
                return float('inf')
            dist = stats.beta(alpha, beta_param)
            return (
                (dist.ppf(0.1) - p10)**2 +
                (dist.ppf(0.5) - median)**2 +
                (dist.ppf(0.9) - p90)**2
            )

        result = minimize(loss, [2, 2], bounds=[(0.01, 100), (0.01, 100)])
        return stats.beta(result.x[0], result.x[1])

    else:
        raise ValueError(f"Unknown distribution type: {dist_type}")


def sample(dist: stats.rv_continuous, n: int = 1000) -> np.ndarray:
    """Generate n random samples from a distribution."""
    return dist.rvs(size=n)


def percentile(dist: stats.rv_continuous, q: float) -> float:
    """Get value at quantile q (0-1) from distribution."""
    return dist.ppf(q)


def probability_in_range(dist: stats.rv_continuous, low: float, high: float) -> float:
    """Calculate P(low < X < high) for distribution."""
    return dist.cdf(high) - dist.cdf(low)


def credible_interval(dist: stats.rv_continuous, level: float = 0.8) -> Tuple[float, float]:
    """
    Get symmetric credible interval at given level.

    Parameters
    ----------
    dist : distribution
    level : float
        Credible level (e.g., 0.8 for 80% CI)

    Returns
    -------
    (lower, upper) bounds
    """
    alpha = 1 - level
    return (dist.ppf(alpha / 2), dist.ppf(1 - alpha / 2))


# --- Aggregation Functions ---

def extremize(probability: float, factor: float = 1.5) -> float:
    """
    Push probability away from 0.5 using log-odds transform.

    From Steinhardt: When aggregating correlated forecasts, information
    is often underweighted. Extremizing recovers some of this.

    Parameters
    ----------
    probability : float
        Probability to extremize (0-1)
    factor : float
        Extremizing factor (>1 = more extreme, <1 = less extreme)

    Returns
    -------
    Extremized probability
    """
    if probability <= 0 or probability >= 1:
        return probability

    log_odds = np.log(probability / (1 - probability))
    extremized_log_odds = log_odds * factor
    return 1 / (1 + np.exp(-extremized_log_odds))


def trimmed_mean(values: List[float], trim_pct: float = 0.1) -> float:
    """
    Calculate trimmed mean, removing outliers.

    Parameters
    ----------
    values : list
        Values to average
    trim_pct : float
        Fraction to trim from each tail (e.g., 0.1 = remove top/bottom 10%)

    Returns
    -------
    Trimmed mean
    """
    sorted_vals = sorted(values)
    n = len(sorted_vals)
    trim_count = int(n * trim_pct)

    if trim_count == 0 or 2 * trim_count >= n:
        return np.mean(sorted_vals)

    trimmed = sorted_vals[trim_count:-trim_count]
    return np.mean(trimmed)


def weighted_mean(values: List[float], weights: List[float]) -> float:
    """Calculate weighted mean of values."""
    values = np.array(values)
    weights = np.array(weights)
    return np.sum(values * weights) / np.sum(weights)


def log_odds_mean(probabilities: List[float]) -> float:
    """
    Average probabilities in log-odds space.

    More appropriate for aggregating probability estimates than
    arithmetic mean, especially for extreme probabilities.
    """
    def to_log_odds(p):
        p = np.clip(p, 1e-10, 1 - 1e-10)
        return np.log(p / (1 - p))

    def from_log_odds(lo):
        return 1 / (1 + np.exp(-lo))

    log_odds = [to_log_odds(p) for p in probabilities]
    mean_lo = np.mean(log_odds)
    return from_log_odds(mean_lo)


def combine_distributions(
    distributions: List[stats.rv_continuous],
    weights: Optional[List[float]] = None,
    n_samples: int = 10000
) -> Tuple[float, float, float]:
    """
    Combine multiple distributions into summary statistics.

    Uses Monte Carlo sampling to approximate the mixture distribution.

    Parameters
    ----------
    distributions : list
        List of scipy.stats distribution objects
    weights : list, optional
        Weights for each distribution (default: equal weights)
    n_samples : int
        Number of samples for Monte Carlo approximation

    Returns
    -------
    (p10, median, p90) of the mixture distribution
    """
    if weights is None:
        weights = [1.0 / len(distributions)] * len(distributions)

    weights = np.array(weights) / np.sum(weights)

    # Sample from mixture
    samples = []
    for dist, w in zip(distributions, weights):
        n = int(n_samples * w)
        samples.extend(dist.rvs(size=n))

    samples = np.array(samples)

    return (
        np.percentile(samples, 10),
        np.percentile(samples, 50),
        np.percentile(samples, 90)
    )


# --- Utility Functions ---

def bucket_probabilities(
    dist: stats.rv_continuous,
    boundaries: List[float]
) -> List[Tuple[str, float]]:
    """
    Calculate probabilities for discrete buckets (for prediction markets).

    Parameters
    ----------
    dist : distribution
    boundaries : list
        Bucket boundaries [b0, b1, b2, ...] defining ranges:
        (-inf, b0], (b0, b1], (b1, b2], ..., (bn, inf)

    Returns
    -------
    List of (range_label, probability) tuples
    """
    results = []

    # First bucket: (-inf, boundaries[0]]
    prob = dist.cdf(boundaries[0])
    results.append((f"≤{boundaries[0]}", prob))

    # Middle buckets
    for i in range(len(boundaries) - 1):
        prob = dist.cdf(boundaries[i + 1]) - dist.cdf(boundaries[i])
        results.append((f"({boundaries[i]}, {boundaries[i + 1]}]", prob))

    # Last bucket: (boundaries[-1], inf)
    prob = 1 - dist.cdf(boundaries[-1])
    results.append((f">{boundaries[-1]}", prob))

    return results


def plot_distribution(
    dist: stats.rv_continuous,
    ax: Optional[plt.Axes] = None,
    show_percentiles: bool = True,
    label: Optional[str] = None,
    **kwargs
) -> plt.Axes:
    """
    Visualize distribution PDF with percentile markers.

    Parameters
    ----------
    dist : distribution
    ax : matplotlib axes, optional
    show_percentiles : bool
        Whether to show p10, p50, p90 vertical lines
    label : str, optional
        Label for legend
    **kwargs : passed to plot()

    Returns
    -------
    matplotlib axes
    """
    if ax is None:
        fig, ax = plt.subplots(figsize=(10, 6))

    # Determine plotting range
    p01 = dist.ppf(0.01)
    p99 = dist.ppf(0.99)
    x = np.linspace(p01, p99, 500)
    y = dist.pdf(x)

    ax.plot(x, y, label=label, **kwargs)
    ax.fill_between(x, y, alpha=0.3)

    if show_percentiles:
        for q, color, name in [(0.1, 'red', 'p10'), (0.5, 'green', 'p50'), (0.9, 'red', 'p90')]:
            val = dist.ppf(q)
            ax.axvline(val, color=color, linestyle='--', alpha=0.7)
            ax.annotate(f'{name}={val:.1f}', xy=(val, 0), xytext=(val, ax.get_ylim()[1] * 0.9),
                       fontsize=9, ha='center')

    ax.set_xlabel('Value')
    ax.set_ylabel('Probability Density')
    ax.set_title('Probability Distribution')

    if label:
        ax.legend()

    return ax


# --- Example Usage ---

if __name__ == "__main__":
    # Example: Fit distribution from percentile estimates
    print("Fitting distribution from percentiles...")

    # Example: AI benchmark prediction
    p10, median, p90 = 35, 50, 70

    # Auto-detect distribution type
    dist = fit_from_percentiles(p10, median, p90)
    print(f"Fitted distribution: {dist.dist.name}")
    print(f"Verification - p10: {dist.ppf(0.1):.1f}, p50: {dist.ppf(0.5):.1f}, p90: {dist.ppf(0.9):.1f}")

    # Example: Extremizing
    print("\nExtremizing probabilities...")
    for p in [0.3, 0.5, 0.7]:
        print(f"  {p:.0%} → {extremize(p, factor=1.5):.1%}")

    # Example: Aggregation
    print("\nAggregating forecasts...")
    forecasts = [0.3, 0.4, 0.35, 0.8]  # One outlier
    print(f"  Simple mean: {np.mean(forecasts):.1%}")
    print(f"  Trimmed mean (10%): {trimmed_mean(forecasts, 0.1):.1%}")
    print(f"  Log-odds mean: {log_odds_mean(forecasts):.1%}")
