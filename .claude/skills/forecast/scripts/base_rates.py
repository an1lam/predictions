#!/usr/bin/env python
"""
Base rate and reference class utilities for forecasting.

Functions for calculating historical frequencies, velocity analysis,
and extrapolation methods.

Usage:
    from base_rates import historical_frequency, velocity, extrapolate_linear
"""

import numpy as np
from scipy import stats
from typing import List, Tuple, Optional, Union
from datetime import datetime, timedelta
import pandas as pd


# --- Historical Frequency ---

def historical_frequency(
    events: int,
    total: int,
    ci_level: float = 0.9
) -> Tuple[float, Tuple[float, float]]:
    """
    Calculate base rate with Wilson confidence interval.

    The Wilson interval is preferred over simple proportion CI because
    it behaves well for small samples and extreme proportions.

    Parameters
    ----------
    events : int
        Number of times event occurred
    total : int
        Total number of opportunities
    ci_level : float
        Confidence level (e.g., 0.9 for 90% CI)

    Returns
    -------
    (point_estimate, (ci_lower, ci_upper))
    """
    if total == 0:
        return 0.5, (0.0, 1.0)

    p = events / total
    z = stats.norm.ppf((1 + ci_level) / 2)

    # Wilson score interval
    denominator = 1 + z**2 / total
    center = (p + z**2 / (2 * total)) / denominator
    margin = z * np.sqrt((p * (1 - p) + z**2 / (4 * total)) / total) / denominator

    ci_lower = max(0, center - margin)
    ci_upper = min(1, center + margin)

    return p, (ci_lower, ci_upper)


def laplace_estimate(
    events: int,
    total: int,
    prior_successes: float = 1,
    prior_failures: float = 1
) -> float:
    """
    Laplace (add-one) smoothing for probability estimation.

    Useful when sample size is small or when base rate might be 0 or 1.

    Parameters
    ----------
    events : int
        Number of times event occurred
    total : int
        Total number of opportunities
    prior_successes : float
        Pseudo-count for successes (default: 1)
    prior_failures : float
        Pseudo-count for failures (default: 1)

    Returns
    -------
    Smoothed probability estimate
    """
    return (events + prior_successes) / (total + prior_successes + prior_failures)


# --- Velocity Analysis ---

def velocity(
    values: List[float],
    dates: List[Union[datetime, str]],
    start_pct: float = 0.2,
    end_pct: float = 0.8
) -> Tuple[float, str]:
    """
    Calculate rate of change in a specific range of progress.

    Useful for benchmark velocity analysis: "How fast did this improve
    from 20% to 80%?"

    Parameters
    ----------
    values : list
        Metric values over time
    dates : list
        Corresponding dates (datetime or 'YYYY-MM-DD' strings)
    start_pct : float
        Starting percentage (e.g., 0.2 for 20%)
    end_pct : float
        Ending percentage (e.g., 0.8 for 80%)

    Returns
    -------
    (velocity, units) where velocity is change per month
    """
    # Convert dates if needed
    if isinstance(dates[0], str):
        dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

    # Find indices where values cross thresholds
    start_idx = None
    end_idx = None

    for i, v in enumerate(values):
        if start_idx is None and v >= start_pct * 100:
            start_idx = i
        if v >= end_pct * 100:
            end_idx = i
            break

    if start_idx is None or end_idx is None or start_idx >= end_idx:
        return float('nan'), 'insufficient data'

    # Calculate velocity
    value_change = values[end_idx] - values[start_idx]
    days_elapsed = (dates[end_idx] - dates[start_idx]).days
    months_elapsed = days_elapsed / 30.44  # Average days per month

    if months_elapsed == 0:
        return float('inf'), 'instantaneous'

    velocity_per_month = value_change / months_elapsed

    return velocity_per_month, 'pp/month'


def doubling_time(
    values: List[float],
    dates: List[Union[datetime, str]]
) -> Optional[float]:
    """
    Estimate doubling time from exponential growth.

    Parameters
    ----------
    values : list
        Metric values over time (must be positive)
    dates : list
        Corresponding dates

    Returns
    -------
    Doubling time in days, or None if growth is not exponential
    """
    if isinstance(dates[0], str):
        dates = [datetime.strptime(d, '%Y-%m-%d') for d in dates]

    # Convert to days from start
    start_date = dates[0]
    days = [(d - start_date).days for d in dates]

    # Fit log-linear model
    log_values = np.log(np.array(values) + 1e-10)
    slope, intercept, r_value, _, _ = stats.linregress(days, log_values)

    if slope <= 0 or r_value**2 < 0.8:
        return None  # Not exponential growth

    # Doubling time = ln(2) / slope
    return np.log(2) / slope


# --- Extrapolation ---

def extrapolate_linear(
    current: float,
    velocity: float,
    days: int
) -> float:
    """
    Simple linear extrapolation.

    Parameters
    ----------
    current : float
        Current value
    velocity : float
        Rate of change (units per day)
    days : int
        Days to extrapolate

    Returns
    -------
    Extrapolated value
    """
    return current + velocity * days


def extrapolate_exponential(
    current: float,
    doubling_time: float,
    days: int
) -> float:
    """
    Exponential extrapolation.

    Parameters
    ----------
    current : float
        Current value
    doubling_time : float
        Doubling time in days
    days : int
        Days to extrapolate

    Returns
    -------
    Extrapolated value
    """
    return current * (2 ** (days / doubling_time))


def extrapolate_sigmoid(
    current: float,
    ceiling: float,
    current_velocity: float,
    days: int
) -> float:
    """
    Sigmoid/logistic extrapolation with saturation.

    Uses simple logistic growth model where growth slows as
    value approaches ceiling.

    Parameters
    ----------
    current : float
        Current value
    ceiling : float
        Maximum possible value (e.g., 100 for percentage)
    current_velocity : float
        Current rate of change (units per day)
    days : int
        Days to extrapolate

    Returns
    -------
    Extrapolated value
    """
    if current >= ceiling:
        return ceiling

    # Estimate logistic growth rate from current velocity
    # v = r * y * (1 - y/K), solve for r
    if current <= 0 or current_velocity <= 0:
        return current

    r = current_velocity / (current * (1 - current / ceiling))

    # Logistic growth formula
    # y(t) = K / (1 + ((K - y0) / y0) * exp(-r * t))
    K = ceiling
    y0 = current
    t = days

    denominator = 1 + ((K - y0) / y0) * np.exp(-r * t)
    return K / denominator


# --- Reference Class Analysis ---

def compare_to_reference_class(
    target_velocity: float,
    reference_velocities: List[float],
    reference_names: List[str]
) -> pd.DataFrame:
    """
    Compare a target velocity to reference class.

    Parameters
    ----------
    target_velocity : float
        Velocity of the target prediction
    reference_velocities : list
        Velocities of reference class members
    reference_names : list
        Names of reference class members

    Returns
    -------
    DataFrame with comparison statistics
    """
    ref_arr = np.array(reference_velocities)

    percentile_rank = stats.percentileofscore(ref_arr, target_velocity)
    z_score = (target_velocity - np.mean(ref_arr)) / np.std(ref_arr) if np.std(ref_arr) > 0 else 0

    df = pd.DataFrame({
        'Reference': reference_names + ['Target'],
        'Velocity': list(reference_velocities) + [target_velocity],
        'Percentile': [stats.percentileofscore(ref_arr, v) for v in reference_velocities] + [percentile_rank]
    })

    summary = {
        'target_velocity': target_velocity,
        'reference_mean': np.mean(ref_arr),
        'reference_median': np.median(ref_arr),
        'reference_std': np.std(ref_arr),
        'percentile_rank': percentile_rank,
        'z_score': z_score
    }

    return df, summary


def estimate_time_to_threshold(
    current: float,
    threshold: float,
    velocity: float,
    velocity_std: Optional[float] = None
) -> Tuple[float, Optional[Tuple[float, float]]]:
    """
    Estimate days until threshold is reached.

    Parameters
    ----------
    current : float
        Current value
    threshold : float
        Target threshold
    velocity : float
        Rate of change (units per day)
    velocity_std : float, optional
        Standard deviation of velocity for CI calculation

    Returns
    -------
    (days_estimate, (ci_lower, ci_upper) or None)
    """
    if velocity <= 0:
        return float('inf'), None

    gap = threshold - current
    if gap <= 0:
        return 0, (0, 0)

    days = gap / velocity

    if velocity_std is not None and velocity_std > 0:
        # Approximate CI using velocity uncertainty
        days_low = gap / (velocity + 1.645 * velocity_std)
        days_high = gap / max(velocity - 1.645 * velocity_std, 0.001)
        return days, (days_low, days_high)

    return days, None


# --- Example Usage ---

if __name__ == "__main__":
    # Example: Historical frequency
    print("Historical frequency analysis...")
    events, total = 12, 30
    rate, (ci_low, ci_high) = historical_frequency(events, total)
    print(f"  Base rate: {rate:.1%} (90% CI: [{ci_low:.1%}, {ci_high:.1%}])")

    # Example: Velocity calculation
    print("\nVelocity analysis...")
    values = [10, 20, 35, 50, 65, 80, 88, 92]
    dates = ['2023-01-01', '2023-04-01', '2023-07-01', '2023-10-01',
             '2024-01-01', '2024-04-01', '2024-07-01', '2024-10-01']
    vel, units = velocity(values, dates, start_pct=0.2, end_pct=0.8)
    print(f"  Velocity (20% to 80%): {vel:.2f} {units}")

    # Example: Extrapolation
    print("\nExtrapolation...")
    current_value = 50
    current_vel = 2  # pp per month
    days_ahead = 365

    linear = extrapolate_linear(current_value, current_vel / 30, days_ahead)
    sigmoid = extrapolate_sigmoid(current_value, 100, current_vel / 30, days_ahead)

    print(f"  Current: {current_value}%")
    print(f"  Linear (1 year): {linear:.1f}%")
    print(f"  Sigmoid (1 year, ceiling=100): {sigmoid:.1f}%")

    # Example: Time to threshold
    print("\nTime to threshold...")
    days_est, ci = estimate_time_to_threshold(
        current=50, threshold=80, velocity=2/30, velocity_std=0.5/30
    )
    print(f"  Days to 80%: {days_est:.0f}")
    if ci:
        print(f"  90% CI: [{ci[0]:.0f}, {ci[1]:.0f}] days")
