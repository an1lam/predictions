# Forecasting Anti-Patterns

Common mistakes to avoid in prediction. Check for these throughout the forecasting process.

---

## 1. Starting with Inside View

**Anti-pattern**: Jumping straight to case-specific analysis without establishing base rates.

**Symptom**: "This situation is unique because..." without first asking "What typically happens?"

**Fix**: Always complete Phase 2 (Outside View) before Phase 3 (Inside View). Even if the case seems unique, anchor to the closest reference class.

**Example**:
- Wrong: "GPT-5 will achieve X because of these specific technical improvements..."
- Right: "Historically, new model generations improve by Y%. Now let's consider if GPT-5 differs..."

---

## 2. Round Number Probabilities

**Anti-pattern**: Using round numbers like 10%, 20%, 50%, 80%.

**Symptom**: All predictions end in 0 or 5.

**Fix**: Use granular probabilities (23%, 47%, 78%) that reflect your actual uncertainty. The difference between 20% and 25% represents real information.

**Why it matters**: Round numbers signal lazy thinking and reduce the information content of your predictions. They also make calibration analysis less useful.

---

## 3. Single Hypothesis Reasoning

**Anti-pattern**: Having one main view and looking for evidence to support it.

**Symptom**: "I think X will happen because..." with no alternative scenarios.

**Fix**: Generate at least 3 competing scenarios. Actively seek disconfirming evidence for each.

**Question to ask**: "What's the best argument against my current view?"

---

## 4. Underweighting "Other"

**Anti-pattern**: In decomposition, assigning tiny probability to "other outcomes."

**Symptom**: Scenarios sum to 95%+ with "other" getting leftover probability.

**Fix**:
- Ensure MECE decomposition (Mutually Exclusive, Collectively Exhaustive)
- Ask: "What am I missing?" before assigning "other" probability
- Consider: Hidden alternatives in seemingly binary questions

**Example**:
- Wrong: "A wins (40%), B wins (55%), Other (5%)"
- Right: "A wins (35%), B wins (45%), C emerges (10%), No clear winner (10%)"

---

## 5. Identical Timeframe Estimates

**Anti-pattern**: Giving the same prediction for different timeframes.

**Symptom**: "50% by 2025, 50% by 2026, 50% by 2027"

**Fix**: Longer timeframes should generally have higher cumulative probability (for "will happen" questions) or adjusted point estimates (for quantitative questions).

**Reality check**: If your 2-year and 5-year predictions are identical, you haven't thought carefully about timing.

---

## 6. Overconfidence

**Anti-pattern**: Assigning probabilities <5% or >95% without exceptional evidence.

**Symptoms**:
- "This will definitely happen" (99%)
- "This is impossible" (1%)
- Narrow confidence intervals

**Fix**:
- Ask: "What would make me wrong?"
- Check: Historical accuracy at extreme confidence levels
- Remember: Even experts are wrong 10-20% of the time on "near-certain" predictions

**When extremes are justified**:
- Mathematical certainty
- Direct observation of outcome
- Massive evidence with no plausible alternative

---

## 7. Statistical Bounds Only

**Anti-pattern**: Using regression confidence intervals as final prediction bounds.

**Symptom**: 90% CI from regression = final 90% prediction interval.

**Fix**: Add model uncertainty and tail risk to statistical CI:
1. Statistical layer (from data)
2. Model uncertainty layer (from scenario disagreement)
3. Tail risk layer (from extreme scenarios)

Final bounds should almost always be wider than pure statistical CI.

---

## 8. Anchoring to First Estimate

**Anti-pattern**: Sticking close to initial intuition despite contrary evidence.

**Symptom**: Final prediction within 5pp of gut feeling despite extensive analysis.

**Fix**:
- Record initial intuition separately
- Explicitly compare final prediction to initial intuition
- Ask: "What evidence would justify a larger update?"

**Note**: Sometimes analysis confirms intuition, which is fine. The problem is insufficient updating when evidence suggests otherwise.

---

## 9. Availability Bias

**Anti-pattern**: Overweighting recent or memorable examples.

**Symptoms**:
- Recent news heavily influences prediction
- Dramatic past events dominate thinking
- Ignoring base rates in favor of salient examples

**Fix**:
- Use systematic data collection (not cherry-picked examples)
- Weight examples by relevance, not memorability
- Check: "Am I overweighting because this example is vivid?"

---

## 10. Hindsight Bias in Updates

**Anti-pattern**: Updating beliefs after outcomes as if you "knew it all along."

**Symptom**: After outcome: "I always thought X was likely" (but didn't record it).

**Fix**:
- Document predictions and reasoning BEFORE outcomes
- Compare actual predictions to post-hoc memory
- Track prediction accuracy formally

---

## 11. Confusing Confidence with Accuracy

**Anti-pattern**: Feeling confident means being correct.

**Symptom**: High confidence correlates with conviction, not evidence quality.

**Fix**:
- Separate "how sure do I feel" from "how much evidence do I have"
- Track: Are confident predictions more accurate?
- Remember: Confidence should reflect information quality, not emotional certainty

---

## 12. Neglecting Base Rate Changes

**Anti-pattern**: Assuming historical base rates apply unchanged to future.

**Symptoms**:
- "It's always been X%, so it will continue to be X%"
- Ignoring structural changes in the environment

**Fix**:
- Ask: "Has the underlying mechanism changed?"
- Consider: Technology shifts, policy changes, market structure evolution
- Distinguish: Stable base rates vs. trending metrics

---

## 13. Correlation vs. Causation

**Anti-pattern**: Assuming correlated factors are causally related.

**Symptom**: "X increased when Y increased, so Y causes X"

**Fix**:
- Consider alternative explanations
- Look for natural experiments or controlled comparisons
- Ask: "What's the mechanism?"

---

## 14. Scope Insensitivity

**Anti-pattern**: Similar predictions for differently-scoped questions.

**Symptom**: Same probability for "at least one X" vs. "exactly five X" vs. "widespread X"

**Fix**:
- Carefully parse the exact question scope
- Decompose: P(at least one) ≠ P(exactly N) ≠ P(widespread)
- Verify bounds make sense across scopes

---

## Anti-Pattern Checklist

Use this checklist before finalizing any prediction:

- [ ] Did I establish base rates before case-specific analysis?
- [ ] Am I using granular (non-round) probabilities?
- [ ] Have I generated 3+ competing scenarios?
- [ ] Did I seek disconfirming evidence for my favored view?
- [ ] Is "other" appropriately weighted in my decomposition?
- [ ] Do my predictions differ across timeframes?
- [ ] Are extreme probabilities (<5% or >95%) justified?
- [ ] Are my bounds wider than pure statistical CI?
- [ ] Have I updated sufficiently from my initial intuition?
- [ ] Am I overweighting recent/memorable examples?
