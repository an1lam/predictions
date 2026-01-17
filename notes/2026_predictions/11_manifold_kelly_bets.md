# Manifold Markets Kelly Bets - January 2026

## Overview

On January 17, 2026, we placed Kelly-optimal bets on Manifold Markets corresponding to our 10 AI predictions for the forecast2026.ai survey. This document records the reasoning and methodology for future review.

## Methodology

### Kelly Criterion Adaptation

Standard Kelly assumes repeated bets with rebalancing. For our one-shot, bet-and-leave scenario, we made several adjustments:

1. **Quarter-Kelly (0.25)**: More conservative than standard Kelly to account for:
   - No rebalancing opportunity
   - Potential correlation between markets (AI progress affects multiple benchmarks)
   - Model uncertainty in our probability estimates

2. **10% Edge Threshold**: Only bet on buckets where |our_prob - market_prob| > 10%. This filters out marginal edges that might not survive transaction costs and estimation error.

3. **Bankroll Allocation**: Proportional to expected edge per market, calculated as sum(|our_prob - market_prob| * our_prob) across buckets.

### Distribution Fitting

For each prediction, we fit a probability distribution to our (median, 10th percentile, 90th percentile):

- **Normal**: For symmetric predictions (METR Horizon, FrontierMath, OpenAI-Proof QA, Epoch Capabilities, YouGov)
- **Log-normal**: For right-skewed predictions (Remote Labor Index, AI Lab Revenues, Public Importance, METR Uplift)
- **Truncated Normal**: For bounded predictions (GSOBench, 0-100%)

## Bets Placed

| Market | Bucket | Action | Amount | Our Prob | Market Prob | Edge |
|--------|--------|--------|--------|----------|-------------|------|
| Remote Labor Index | 10-20% | YES | 404 mana | 41.9% | 11.9% | +30.0% |
| YouGov Sentiment | -30 to -20pp | NO | 166 mana | 16.2% | 28.0% | -11.8% |
| Epoch Capabilities | ≥185 | YES | 155 mana | 27.9% | 7.1% | +20.8% |
| Public Importance | <0.5% | YES | 103 mana | 29.4% | 12.2% | +17.2% |
| OpenAI-Proof Q&A | 30-40% | YES | 67 mana | 26.8% | 15.5% | +11.3% |

**Total: 895 mana** (~5% of 17,619 mana bankroll)

## Reasoning by Bet

### 1. Remote Labor Index: 10-20% (YES, 404 mana, +30% edge)

**Our prediction**: 18% (10th: 8%, 90th: 35%)

**Why we're more bearish than the market**: The market has a nearly uniform distribution across all buckets (10-12% each from <10% to ≥80%). We think this dramatically overweights high RLI scores.

The Remote Labor Index measures AI's ability to perform remote work tasks. Current performance is ~3.75%. While we expect significant improvement, reaching 40%+ by end of 2026 would require extraordinary progress. Our analysis of early-stage benchmark progression suggests 10-20% is the most likely range, with the bulk of probability mass below 35%.

**Key factors**:
- Benchmark is new and relatively hard
- Current progress from ~0% to ~4% over ~6 months
- Log-normal distribution captures right-skew (breakthrough scenarios)
- Market seems to price in too much probability on very high outcomes

### 2. Epoch Capabilities Index: ≥185 (YES, 155 mana, +20.8% edge)

**Our prediction**: 177 (10th: 160, 90th: 195)

**Why we're more bullish on high scores**: The market concentrates probability in 165-180 range. We think there's substantial probability (28%) of reaching ≥185.

The ECI was at 154 in mid-2025 and has been growing ~1.3 points/month. Linear extrapolation to Dec 2026 gives ~177. However, the distribution of outcomes is wide, and we weight the possibility of acceleration (new model releases, benchmark-focused training) more heavily than the market.

**Key factors**:
- Current trend supports our median
- Our 90th percentile (195) implies strong acceleration is plausible
- Market underweights tail scenarios

### 3. Public Importance: <0.5% (YES, 103 mana, +17.2% edge)

**Our prediction**: 1.0% (10th: 0.3%, 90th: 8.0%)

**Why we expect AI to remain low-salience**: The "most important problem" poll question has historically shown AI at very low levels (0.4-0.5%). Dramatic increases typically require salient events (major job losses, safety incidents).

We use a log-normal distribution because outcomes are bounded below by 0 and have potential for explosive growth in tail scenarios. The median of 1.0% represents modest growth, but we assign 29% probability to staying below 0.5% (roughly current levels).

**Key factors**:
- Historical baseline is very low
- No obvious catalyst for dramatic increase priced in
- Log-normal captures asymmetric upside risk
- Market seems to expect more movement than historical patterns suggest

### 4. YouGov Sentiment: -30 to -20pp (NO, 166 mana, -11.8% edge)

**Our prediction**: -14pp (10th: -40pp, 90th: +15pp)

**Why we're betting against this bucket**: The market assigns 28% to the -30 to -20pp range, but our normal distribution centered at -14pp only assigns 16% to this range.

Our prediction reflects mild continued deterioration in sentiment (current is -11pp), but with wide uncertainty. The distribution is roughly symmetric around -14pp, so the probability mass is spread more evenly than the market's concentration in the -30 to -20pp bucket.

**Key factors**:
- Our median (-14pp) is close to current (-11pp)
- Wide uncertainty (55pp range from p10 to p90)
- Market seems overconfident in specific negative range

### 5. OpenAI-Proof Q&A: 30-40% (YES, 67 mana, +11.3% edge)

**Our prediction**: 37% (10th: 18%, 90th: 55%)

**Why we favor this bucket**: Our median of 37% falls squarely in this bucket. The market spreads probability more uniformly; we think 30-40% deserves more weight.

OpenAI-Proof Q&A measures AI research capability. Current performance is ~8%. We expect significant improvement based on:
- OpenAI's stated goal of "AI research intern" capability
- Reference class of similar benchmarks showing 2-4pp/month gains in middle ranges
- Explicit lab prioritization of research capabilities

**Key factors**:
- Median prediction directly in this bucket (27% probability)
- Market only assigns 15.5%
- Labs are explicitly targeting this capability

## Markets Where We Didn't Bet

The following markets had no bets because no bucket exceeded our 10% edge threshold:

1. **METR Horizon Doubling Time**: Our prediction (4.5 months) aligns closely with market consensus
2. **FrontierMath Tier 4**: Market distribution similar to ours (centered around 60-70%)
3. **GSOBench**: Our prediction (74%) matches market's peak probability range
4. **AI Lab Revenues**: Predictions align (market and our median both ~$60B)
5. **METR Uplift**: Similar distributions, no large edge

## Configuration

```python
TOTAL_BANKROLL = 17619  # mana
KELLY_FRACTION = 0.25   # quarter-Kelly
EDGE_THRESHOLD = 0.10   # 10% minimum
MIN_BET_SIZE = 10       # mana
```

## Files

- Code: `scripts/2026_predictions/manifold/`
- Bet preview: `data/2026_predictions/manifold/bet_preview.json`
- Bet history: `data/2026_predictions/manifold/bet_history.csv`
- Predictions: `notes/2026_predictions/01-10_*.md`

## Review Checklist (December 2026)

- [ ] Compare actual outcomes to our predictions
- [ ] Calculate P&L on each bet
- [ ] Assess calibration: did our probability estimates match realized frequencies?
- [ ] Identify where market was right and we were wrong (and vice versa)
- [ ] Note any systematic biases in our methodology
