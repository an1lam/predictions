# Phase 1: Information Prioritization

**Purpose**: Focus research effort on factors that are both important and uncertain. Avoid wasting time on well-known or low-impact considerations.

---

## The Importance × Uncertainty Matrix

From Steinhardt's forecasting course: The highest-value research targets factors that are:
- **High importance**: Significantly affects the outcome
- **High uncertainty**: You don't already know the answer

```
                    High Uncertainty    Low Uncertainty
                    ─────────────────────────────────────
High Importance  │  RESEARCH PRIORITY   Already informed
                 │  (investigate these)  (no need to dig)
                    ─────────────────────────────────────
Low Importance   │  Interesting but      Don't bother
                 │  low ROI              (skip entirely)
                    ─────────────────────────────────────
```

---

## Process

### Step 1: Brainstorm Considerations
List all factors that could affect the outcome. Don't filter yet.

For quantitative predictions:
- Historical trends and growth rates
- Key drivers of change (technology, funding, talent, etc.)
- Potential accelerants or decelerants
- Measurement methodology changes
- Comparable metrics in related domains

For binary predictions:
- Factors that increase probability
- Factors that decrease probability
- Preconditions that must be met
- Potential blockers or dealbreakers
- Historical precedents

### Step 2: Score Each Factor
Rate each consideration on two dimensions (1-5 scale):

**Importance**: How much would this factor affect the final prediction if we knew it?
- 5: Could shift prediction by >20 percentile points or >2x outcome
- 3: Would shift prediction by 5-20 percentile points
- 1: Minimal impact regardless of answer

**Uncertainty**: How much do we already know about this factor?
- 5: Highly uncertain, could go either way
- 3: Some evidence but significant uncertainty remains
- 1: Well-established, strong evidence already available

### Step 3: Calculate Priority Score
Priority = Importance × Uncertainty

Focus research on factors with Priority > 12 (e.g., 4×4, 5×3, etc.)

---

## Example: FrontierMath Tier 4 Prediction

| Factor | Importance | Uncertainty | Priority |
|--------|------------|-------------|----------|
| Current best score | 5 | 2 | 10 |
| Historical rate of improvement | 5 | 3 | 15 |
| Explicit prioritization by labs | 4 | 4 | 16 |
| New architectures in development | 4 | 5 | 20 |
| Benchmark difficulty curve | 3 | 4 | 12 |
| Compute scaling trends | 4 | 2 | 8 |

**Research priorities**: New architectures (20), explicit prioritization (16), improvement rate (15)

---

## Decision-Relevant Quantities

Identify specific numbers or facts that would most inform your prediction:

- "What is the current best score on this benchmark?"
- "What was the improvement rate over the past 12 months?"
- "How many organizations are actively working on this?"
- "What is the historical base rate for similar events?"

These become concrete research tasks for Phase 2.

---

## Anti-Pattern Check

**Are you researching low-importance factors?**

Common traps:
- Interesting technical details that don't affect the outcome
- Historical context that's fascinating but not predictive
- Edge cases that are unlikely to matter
- Factors already well-understood

If you find yourself diving deep into a low-priority factor, stop and refocus.

---

## Output: 01_research_priorities.json

```json
{
  "phase": 1,
  "completed_at": "<timestamp>",
  "considerations": [
    {
      "factor": "<description>",
      "importance": 4,
      "uncertainty": 5,
      "priority": 20,
      "notes": "<why this matters>"
    }
  ],
  "research_priorities": [
    "<top priority factor>",
    "<second priority>",
    "<third priority>"
  ],
  "decision_relevant_quantities": [
    "<specific number or fact to find>",
    "<another specific quantity>"
  ]
}
```

---

## Checkpoint

Before proceeding to Phase 2, verify:

**Ask the user**: "Have you identified 2-3 high-priority research areas (importance × uncertainty > 12)?"

- If **YES**: Proceed to Phase 2 (Outside View)
- If **NO**: Continue brainstorming or re-score factors

Also check:
- Are any critical factors missing from the list?
- Is the prioritization reasonable?
- Are decision-relevant quantities specific enough to research?
