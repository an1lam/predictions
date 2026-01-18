# Superforecasting Principles

Core techniques from Philip Tetlock's superforecasting research and the Good Judgment Project.

---

## 1. Outside View First

**Always anchor to base rates before considering case-specific factors.**

The single most important predictor of forecasting accuracy is starting with the outside view:
- What is the reference class of similar events?
- What is the historical frequency in that class?
- What do statistical models predict based on past data?

Only after establishing this anchor should you consider what makes this case different.

**Anti-pattern**: "This situation is unique because..." (without first asking what typically happens)

---

## 2. Granular Probabilities

**Use precise probabilities, not round numbers.**

Round numbers (20%, 50%, 80%) signal lazy thinking. Superforecasters use granular probabilities:

| Instead of | Use |
|------------|-----|
| 20% | 17% or 23% |
| 50% | 47% or 53% |
| 80% | 78% or 82% |

The difference between 20% and 25% is meaningful — it represents different evidence and reasoning.

**Why it works**: Forces you to think carefully about exactly where on the probability scale you should be.

---

## 3. Multi-Handed Thinking

**Generate at least three perspectives on every question.**

- **Two-handed thinking**: "On one hand X, on the other hand Y" — misses alternatives
- **Multi-handed thinking**: "Arguments for A, arguments for B, arguments for C, and what I might be missing"

For every prediction:
1. Generate the strongest case FOR the outcome
2. Generate the strongest case AGAINST the outcome
3. Generate at least one alternative scenario
4. Consider what you might be missing entirely

---

## 4. Seek Disconfirming Evidence

**Actively search for evidence that would prove you wrong.**

Confirmation bias is the enemy of accurate prediction. Counter it by:
- Asking "What would change my mind?"
- Searching for evidence against your current view
- Steel-manning opposing positions
- Identifying your assumptions and testing them

**Question to ask**: "If my prediction is wrong, what would I expect to see?"

---

## 5. Update Proportionally

**Adjust beliefs based on the diagnostic value of evidence.**

Not all evidence deserves equal weight. Update based on:
- **Likelihood ratio**: How much more likely is this evidence under hypothesis A vs B?
- **Base rate adjustment**: Does this evidence change the reference class?
- **Independence**: Is this evidence genuinely new, or correlated with what you already knew?

**Formula**: New probability ∝ Old probability × Likelihood ratio

**Anti-pattern**: Updating dramatically on every piece of news (vs. asking "How diagnostic is this?")

---

## 6. Disaggregate Problems

**Break complex predictions into component estimates.**

Fermi decomposition improves accuracy:
- Identify 3-5 independent factors
- Estimate each factor separately
- Combine using appropriate math (multiply for probabilities, add for linear factors)

**Example**: P(event by 2026) = P(technical feasibility) × P(resources allocated) × P(timeline fits) × P(no blockers)

---

## 7. Consider the Null Hypothesis

**What happens if nothing unusual occurs?**

Many predictions implicitly assume change. But the base case is often:
- Things continue as they have been
- No dramatic breakthroughs or failures
- Mean reversion toward historical averages

Start by asking: "If everything proceeds normally, what would happen?"

---

## 8. Avoid Extremes Without Extreme Evidence

**Probabilities <5% or >95% require extraordinary justification.**

Extreme confidence signals:
- Are you ignoring uncertainty?
- Have you considered tail scenarios?
- What evidence would make you less confident?

Most real-world predictions should fall in the 15-85% range unless you have exceptional evidence.

---

## 9. Document Your Reasoning

**Write down predictions and reasoning before outcomes are known.**

Benefits:
- Prevents hindsight bias ("I knew it all along")
- Enables postmortem learning
- Forces clarity in thinking
- Builds track record for calibration

Record: Prediction, probability, reasoning, date, and what would change your mind.

---

## 10. Track and Calibrate

**Compare predictions to outcomes systematically.**

Calibration = When you say 70%, does it happen 70% of the time?

Metrics:
- **Brier score**: Mean squared error of probability estimates
- **Log score**: Penalizes confident wrong predictions heavily
- **Calibration curve**: Plot predicted probability vs. actual frequency

Good forecasters constantly check their calibration and adjust for systematic biases.

---

## Quick Reference: Superforecaster vs. Average Forecaster

| Superforecaster | Average Forecaster |
|-----------------|-------------------|
| Starts with base rates | Starts with specific case |
| Uses 23%, 67%, 84% | Uses 20%, 70%, 80% |
| Generates multiple hypotheses | Has one main view |
| Seeks disconfirming evidence | Looks for confirmation |
| Updates incrementally | Updates dramatically or not at all |
| Tracks and measures accuracy | Doesn't review past predictions |
| Says "I don't know" when uncertain | Overstates confidence |
| Documents reasoning | Relies on memory |
