# Societal Effects: YouGov AI Sentiment Poll

## Summary
We predict the YouGov AI net sentiment score will be **-14pp** (10th: -40pp, 90th: +15pp) by December 31, 2026. Net sentiment dropped from +1pp (Dec 2024) to -11pp (Aug 2025) with significant volatility, hitting -21pp in June before recovering. We model three scenarios: (A) utility dominates and AI becomes beloved like Amazon, (B) base case where competing forces roughly cancel, and (C) job fears dominate and AI faces major backlash. The very wide bounds (55pp range) reflect genuine uncertainty about which force will dominate, limited historical data, and the potential for public opinion to shift rapidly.

## Current Value
**-11pp** (August 2025)
- Positive (benefits outweigh): 25%
- Negative (drawbacks outweigh): 36%

## Metric Definition
Net = (benefits greatly + benefits somewhat) - (drawbacks somewhat + drawbacks greatly)

Or equivalently: Positive% - Negative%

## Historical Data

| Date | Net Score | Positive | Negative | Question Phrasing |
|------|-----------|----------|----------|-------------------|
| Nov-Dec 2024 | +1pp | 35% | 34% | "positive/negative effect" |
| Mar 2025 | -11pp | 29% | 40% | "positive/negative effect" |
| Jun 2025 | -21pp | 26% | 47% | "positive/negative effect" |
| Aug 2025 | -11pp | 25% | 36% | "benefits/drawbacks" |

### Key Observations
1. **Significant decline**: +1pp → -11pp over 8 months (net -12pp)
2. **High volatility**: Hit -21pp in June before recovering to -11pp
3. **Question wording changed**: May affect comparability
4. **Positive% declining**: 35% → 25% (steady erosion of optimists)
5. **Negative% volatile**: 34% → 47% → 36% (swings with news cycle)

## Competing Forces Framework

### Force 1: Utility → Improved Sentiment
- AI tools becoming more useful and ubiquitous
- People experience direct benefits (ChatGPT, coding assistants, etc.)
- **Amazon precedent**: Most useful company → highest approval rating
- Familiarity breeds comfort, not contempt
- Could push sentiment positive

### Force 2: Job Fears → Worsened Sentiment
- High-profile layoffs attributed to AI
- Economic anxiety about automation
- Media coverage of AI risks
- Political narratives around AI and jobs
- Could push sentiment deeply negative

## Model Framework

### Scenario A: Utility Dominates (25% weight)
- AI becomes ubiquitous, useful, and liked
- "Amazon effect" - people love tools that help them
- Job displacement less visible than expected
- **Projection: 0pp to +10pp**

### Scenario B: Base Case (50% weight)
- Competing forces roughly cancel out
- Some improvement from utility, some concern about jobs
- Stays near current levels with modest drift
- **Projection: -10pp to -18pp**

### Scenario C: Job Fears Dominate (25% weight)
- Major layoffs explicitly attributed to AI
- AI becomes economic/political villain
- Media focus on displacement stories
- Significant backlash
- **Projection: -30pp to -45pp**

### Weighted Calculation
0.25 × 5pp + 0.50 × -14pp + 0.25 × -37.5pp = **-15pp**

Rounded to **-14pp** (slight adjustment toward current value given mean reversion tendency).

## Adjustment Factors

### Toward improved sentiment (less negative)
- AI tools genuinely becoming more useful
- Familiarity and normalization
- Positive use cases (healthcare, education, productivity)
- Tech companies have recovered from past backlashes
- Amazon precedent: utility wins hearts

### Toward worsened sentiment (more negative)
- Job displacement becoming more visible
- Economic uncertainty amplifies fears
- Political weaponization of AI anxiety
- High-profile AI incidents or failures
- Already trending negative from Dec 2024 baseline

## Final Prediction
**Central estimate:** -14pp
**10th percentile:** -40pp
**90th percentile:** +15pp

### Interpretation
- Central: Slight worsening from current -11pp, competing forces mostly cancel
- 10th: Severe backlash scenario - AI becomes deeply unpopular
- 90th: Utility dominates - AI becomes net positive in public view
- 55pp range reflects genuine uncertainty and volatile underlying data

## Methodology Notes
- Three-scenario model with explicit competing forces
- Very wide bounds (55pp) given:
  - Only 4 historical data points
  - High volatility (~10pp swings between polls)
  - Question wording changes
  - Uncertainty about which force dominates
- Public sentiment can shift rapidly with salient events
- Both tails are plausible: severe backlash or widespread embrace
