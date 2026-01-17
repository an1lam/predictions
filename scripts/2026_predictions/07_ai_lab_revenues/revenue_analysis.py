#!/usr/bin/env python3
"""
AI Lab Revenue Analysis

Three-model approach:
- Model A (45%): Company projections / Epoch trend
- Model B (35%): Hyper-growth startup reference class (pessimistic)
- Model C (20%): Ceiling / slowdown scenario
"""

import pandas as pd
from datetime import datetime

# Load revenue data
data_path = "/Users/stephenmalina/dev/an1lam/predictions/data/2026_predictions/ai_companies/ai_companies_revenue_reports.csv"
df = pd.read_csv(data_path)

# Filter for OpenAI, Anthropic, xAI
companies = ['OpenAI', 'Anthropic', 'xAI']
df = df[df['Company'].isin(companies)]
df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values(['Company', 'Date'])

# Convert to billions
df['Revenue_B'] = df['Annualized revenue (USD)'] / 1e9

print("=" * 80)
print("AI LAB REVENUE ANALYSIS")
print("=" * 80)

print("\n### Recent Revenue Data Points")
print("-" * 80)

for company in companies:
    company_df = df[df['Company'] == company].tail(5)
    print(f"\n{company}:")
    for _, row in company_df.iterrows():
        if pd.notna(row['Revenue_B']):
            date_str = row['Date'].strftime('%Y-%m-%d')
            print(f"  {date_str}: ${row['Revenue_B']:.1f}B")

# Latest values (late 2025)
print("\n### Current State (Late 2025)")
print("-" * 80)

# Get most recent annualized revenue for each company
latest = {}
for company in companies:
    company_df = df[(df['Company'] == company) & (df['Revenue_B'].notna())]
    if len(company_df) > 0:
        latest_row = company_df.iloc[-1]
        latest[company] = {
            'date': latest_row['Date'],
            'revenue': latest_row['Revenue_B']
        }
        print(f"{company}: ${latest_row['Revenue_B']:.1f}B (as of {latest_row['Date'].strftime('%Y-%m-%d')})")

current_total = sum(v['revenue'] for v in latest.values())
print(f"\nCombined: ${current_total:.1f}B")

# Model A: Company projections
print("\n### Model A: Company Projections (45% weight)")
print("-" * 80)
print("Based on stated company targets and growth multipliers")

# OpenAI: 2.3x growth in 2026 (from their investor docs)
openai_2026 = 19 * 2.3  # $19B * 2.3x
print(f"OpenAI: $19B × 2.3x = ${openai_2026:.0f}B")

# Anthropic: $26B target by end 2026 (from Reuters report)
anthropic_2026 = 26
print(f"Anthropic: $26B (stated target)")

# xAI: Aggressive growth, ~$0.4B now, assuming 3-4x
xai_2026 = 0.4 * 4  # Aggressive but from small base
print(f"xAI: $0.4B × 4x = ${xai_2026:.1f}B")

model_a_total = openai_2026 + anthropic_2026 + xai_2026
print(f"\nModel A Total: ${model_a_total:.0f}B")

# Model B: Hyper-growth startup reference class
print("\n### Model B: Hyper-growth Startup Reference Class (35% weight)")
print("-" * 80)
print("Historical precedent: fastest companies (Tesla, Meta) took 7 years $10B→$100B")
print("Typical hyper-growth: 1.5-2x annual, not 2-3x sustained")

# More conservative multiplier
growth_mult = 1.7  # Middle of 1.5-2x range
openai_b = 19 * growth_mult
anthropic_b = 7 * growth_mult  # From current $7B, not target
xai_b = 0.4 * 2.5  # Still fast but not 4x

print(f"OpenAI: $19B × {growth_mult}x = ${openai_b:.0f}B")
print(f"Anthropic: $7B × {growth_mult}x = ${anthropic_b:.0f}B")
print(f"xAI: $0.4B × 2.5x = ${xai_b:.1f}B")

model_b_total = openai_b + anthropic_b + xai_b
print(f"\nModel B Total: ${model_b_total:.0f}B")

# Model C: Ceiling / slowdown
print("\n### Model C: Ceiling / Slowdown Scenario (20% weight)")
print("-" * 80)
print("Assumes model improvements slow, reducing demand growth")
print("Revenue growth decelerates to ~1.3x")

growth_mult_c = 1.3
openai_c = 19 * growth_mult_c
anthropic_c = 7 * growth_mult_c
xai_c = 0.4 * 1.5

print(f"OpenAI: $19B × {growth_mult_c}x = ${openai_c:.0f}B")
print(f"Anthropic: $7B × {growth_mult_c}x = ${anthropic_c:.0f}B")
print(f"xAI: $0.4B × 1.5x = ${xai_c:.1f}B")

model_c_total = openai_c + anthropic_c + xai_c
print(f"\nModel C Total: ${model_c_total:.0f}B")

# Weighted average
print("\n### Weighted Projection")
print("-" * 80)

weights = {'A': 0.45, 'B': 0.35, 'C': 0.20}
weighted_avg = (model_a_total * weights['A'] +
                model_b_total * weights['B'] +
                model_c_total * weights['C'])

print(f"Model A ({weights['A']*100:.0f}%): ${model_a_total:.0f}B")
print(f"Model B ({weights['B']*100:.0f}%): ${model_b_total:.0f}B")
print(f"Model C ({weights['C']*100:.0f}%): ${model_c_total:.0f}B")
print(f"\nWeighted Average: ${weighted_avg:.0f}B")

# Bounds
print("\n### Suggested Bounds")
print("-" * 80)
print(f"Central: ${weighted_avg:.0f}B")
print(f"10th percentile (below Model C): ${model_c_total * 0.85:.0f}B")
print(f"90th percentile (above Model A): ${model_a_total * 1.15:.0f}B")
