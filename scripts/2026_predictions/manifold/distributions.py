"""Distribution fitting and bucket probability calculations."""

from dataclasses import dataclass
from typing import Any, Literal
import numpy as np
from scipy import stats


DistributionType = Literal["normal", "lognormal", "truncated_normal"]


@dataclass
class FittedDistribution:
    """A fitted probability distribution."""

    dist_type: DistributionType
    params: dict
    scipy_dist: Any  # scipy frozen distribution

    def cdf(self, x: float) -> float:
        """Cumulative distribution function."""
        return float(self.scipy_dist.cdf(x))

    def pdf(self, x: float) -> float:
        """Probability density function."""
        return float(self.scipy_dist.pdf(x))

    def ppf(self, q: float) -> float:
        """Percent point function (quantile)."""
        return float(self.scipy_dist.ppf(q))


def fit_distribution(
    median: float,
    p10: float,
    p90: float,
    dist_type: DistributionType | None = None,
    lower_bound: float | None = None,
    upper_bound: float | None = None,
) -> FittedDistribution:
    """Fit a distribution to median and 10th/90th percentiles.

    If dist_type is None, automatically chooses based on asymmetry:
    - asymmetry > 1.5 -> log-normal (right-skewed)
    - otherwise -> normal

    For truncated_normal, requires lower_bound and/or upper_bound.
    """
    if dist_type is None:
        # Check for asymmetry
        if median - p10 > 0:
            asymmetry = (p90 - median) / (median - p10)
        else:
            asymmetry = 1.0

        if asymmetry > 1.5 or (p10 > 0 and median / p10 > 2):
            dist_type = "lognormal"
        else:
            dist_type = "normal"

    if dist_type == "lognormal":
        return _fit_lognormal(median, p10, p90)
    elif dist_type == "truncated_normal":
        return _fit_truncated_normal(median, p10, p90, lower_bound, upper_bound)
    else:
        return _fit_normal(median, p10, p90)


def _fit_normal(median: float, p10: float, p90: float) -> FittedDistribution:
    """Fit a normal distribution."""
    # For normal: median = mean
    mean = median
    # p90 - p10 spans 2 * 1.28 * sigma (since z_0.9 ≈ 1.28)
    sigma = (p90 - p10) / (2 * 1.28)

    dist = stats.norm(loc=mean, scale=sigma)
    return FittedDistribution(
        dist_type="normal",
        params={"mean": mean, "sigma": sigma},
        scipy_dist=dist,
    )


def _fit_lognormal(median: float, p10: float, p90: float) -> FittedDistribution:
    """Fit a log-normal distribution.

    For log-normal:
    - median = exp(mu)
    - p10 = exp(mu - 1.28*sigma)
    - p90 = exp(mu + 1.28*sigma)
    """
    if median <= 0 or p10 <= 0 or p90 <= 0:
        raise ValueError("Log-normal requires positive values")

    mu = np.log(median)
    # Average the two sigma estimates
    sigma_from_p10 = (mu - np.log(p10)) / 1.28
    sigma_from_p90 = (np.log(p90) - mu) / 1.28
    sigma = (sigma_from_p10 + sigma_from_p90) / 2

    # scipy lognormal: scale=exp(mu), s=sigma
    dist = stats.lognorm(s=sigma, scale=np.exp(mu))
    return FittedDistribution(
        dist_type="lognormal",
        params={"mu": mu, "sigma": sigma},
        scipy_dist=dist,
    )


def _fit_truncated_normal(
    median: float,
    p10: float,
    p90: float,
    lower_bound: float | None = None,
    upper_bound: float | None = None,
) -> FittedDistribution:
    """Fit a truncated normal distribution.

    We fit a normal first, then truncate it.
    The resulting distribution will have slightly different quantiles
    than the input, but it's a reasonable approximation.
    """
    # First fit underlying normal
    mean = median
    sigma = (p90 - p10) / (2 * 1.28)

    # Set default bounds
    a = (lower_bound - mean) / sigma if lower_bound is not None else -np.inf
    b = (upper_bound - mean) / sigma if upper_bound is not None else np.inf

    dist = stats.truncnorm(a=a, b=b, loc=mean, scale=sigma)
    return FittedDistribution(
        dist_type="truncated_normal",
        params={
            "mean": mean,
            "sigma": sigma,
            "lower_bound": lower_bound,
            "upper_bound": upper_bound,
        },
        scipy_dist=dist,
    )


def compute_bucket_probs(
    dist: FittedDistribution,
    buckets: list[tuple[float | None, float | None]],
) -> np.ndarray:
    """Compute probability for each bucket.

    Each bucket is (lower, upper) where None means unbounded.

    Returns array of probabilities (sums to 1).
    """
    probs = []

    for lower, upper in buckets:
        if lower is None:
            cdf_lower = 0.0
        else:
            cdf_lower = dist.cdf(lower)

        if upper is None:
            cdf_upper = 1.0
        else:
            cdf_upper = dist.cdf(upper)

        prob = cdf_upper - cdf_lower
        probs.append(max(0, prob))  # Ensure non-negative

    probs = np.array(probs)

    # Normalize to sum to 1 (handles any edge cases)
    total = probs.sum()
    if total > 0:
        probs = probs / total

    return probs


def bucket_midpoint(lower: float | None, upper: float | None) -> float:
    """Get the midpoint of a bucket for display purposes."""
    if lower is None and upper is None:
        return 0.0
    if lower is None:
        return upper - 1.0  # Arbitrary offset for "less than" buckets
    if upper is None:
        return lower + 1.0  # Arbitrary offset for "greater than" buckets
    return (lower + upper) / 2
