"""Calculate METR time horizon doubling time from Epoch data."""
import pandas as pd
import numpy as np
from scipy import stats

def calculate_doubling_time_with_ci(x, y):
    """
    Calculate doubling time with 10th/90th percentile bounds.

    Since doubling_time = 1/slope, we need to transform the CI on slope.
    CI bounds flip: [1/slope_high, 1/slope_low]
    """
    n = len(x)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # t-values for 10th and 90th percentiles (80% CI)
    t_val_90 = stats.t.ppf(0.90, n - 2)
    t_val_10 = stats.t.ppf(0.10, n - 2)

    # Slope bounds at 10th and 90th percentiles
    slope_p10 = slope + t_val_10 * std_err  # 10th percentile (lower slope)
    slope_p90 = slope + t_val_90 * std_err  # 90th percentile (higher slope)

    # Transform to doubling time (bounds flip because of 1/x)
    doubling_days = 1 / slope
    doubling_p10 = 1 / slope_p90  # High slope -> low doubling time -> 10th percentile
    doubling_p90 = 1 / slope_p10  # Low slope -> high doubling time -> 90th percentile

    return {
        'doubling_days': doubling_days,
        'doubling_months': doubling_days / 30.44,
        'p10_months': doubling_p10 / 30.44,
        'p90_months': doubling_p90 / 30.44,
        'r_squared': r_value**2,
        'n': n,
        'slope': slope,
        'std_err': std_err
    }


df = pd.read_csv('data/2026_predictions/metr_time_horizons_external.csv')

# Filter to rows with release dates and sort
df = df[df['Release date'].notna()].copy()
df['Release date'] = pd.to_datetime(df['Release date'])
df = df.sort_values('Release date')

print("=== METR Time Horizon Data ===\n")
print(df[['Model version', 'Time horizon', 'Release date']].to_string(index=False))

# Convert to log scale for linear regression
df['log_horizon'] = np.log2(df['Time horizon'])
df['days_since_start'] = (df['Release date'] - df['Release date'].min()).dt.days

# Full dataset
result_full = calculate_doubling_time_with_ci(df['days_since_start'], df['log_horizon'])

print(f"\n=== Full Dataset Regression (2019-2025) ===")
print(f"Doubling time: {result_full['doubling_months']:.2f} months")
print(f"10th percentile: {result_full['p10_months']:.2f} months")
print(f"90th percentile: {result_full['p90_months']:.2f} months")
print(f"R²: {result_full['r_squared']:.3f}, N={result_full['n']}")

# Recent period only (2024-2025)
recent = df[df['Release date'] >= '2024-01-01'].copy()
recent['days_since_start'] = (recent['Release date'] - recent['Release date'].min()).dt.days

if len(recent) > 2:
    result_recent = calculate_doubling_time_with_ci(recent['days_since_start'], recent['log_horizon'])

    print(f"\n=== Recent Period (2024-2025) ===")
    print(f"Doubling time: {result_recent['doubling_months']:.2f} months")
    print(f"10th percentile: {result_recent['p10_months']:.2f} months")
    print(f"90th percentile: {result_recent['p90_months']:.2f} months")
    print(f"R²: {result_recent['r_squared']:.3f}, N={result_recent['n']}")
