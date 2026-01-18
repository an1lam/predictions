# Phase 3: Inside View

**Purpose**: Adjust the base rate anchor based on case-specific evidence. Generate multiple competing hypotheses to avoid single-scenario thinking.

---

## Core Principle

The inside view considers what makes this specific case different from the reference class. But it must be applied **after** establishing the outside view anchor.

Order matters:
1. Outside view → Base rate anchor (Phase 2)
2. Inside view → Adjustments (this phase)
3. Final estimate → Anchor + Adjustments (Phase 5)

---

## Fermi Decomposition

Break the prediction into 3-5 subproblems that can be estimated independently:

### For Quantitative Predictions
Example: "FrontierMath Tier 4 by end of 2026"

```
Current score: 25%
Time remaining: 12 months
Required improvement: (target - current) / months remaining

Decomposition:
1. Base trend extrapolation: +X pp based on historical rate
2. Architecture improvements: +Y pp for expected advances
3. Explicit prioritization: +Z pp if labs focus on this benchmark
4. Difficulty ceiling effects: -W pp for diminishing returns
```

### For Binary Predictions
Example: "Will company X be acquired by 2026?"

```
Decomposition:
1. P(company is acquisition target) = base rate from reference class
2. P(acquirer exists and interested | target) = industry conditions
3. P(deal closes | interested acquirer) = regulatory, financial factors
4. P(timeline fits | deal attempted) = typical deal duration
```

Combine: P(acquired) = P1 × P2 × P3 × P4

---

## Multi-Hypothesis Generation

**Critical requirement**: Generate at least 3 competing scenarios with different assumptions.

### Scenario Template

For each scenario:
1. **Label**: Conservative / Moderate / Optimistic (or descriptive names)
2. **Key assumption**: What must be true for this scenario?
3. **Supporting evidence**: What data supports this scenario?
4. **Disconfirming evidence**: What would falsify this scenario?
5. **Implied outcome**: What does this scenario predict?

### Example Scenarios

**Conservative**: "Business as usual"
- Assumes: No major architectural breakthroughs, typical resource allocation
- Supports: Historical base rates continue, no exceptional effort
- Disconfirms: Announced major initiatives, surprising early progress
- Predicts: Outcome near or below trend extrapolation

**Moderate**: "Following reference class"
- Assumes: Some advances but within historical variance
- Supports: Reference class velocity, comparable benchmark trajectories
- Disconfirms: Evidence of stagnation or acceleration
- Predicts: Outcome matching trend extrapolation

**Optimistic**: "Accelerated progress"
- Assumes: Explicit prioritization, architectural advances, increased resources
- Supports: Announced initiatives, early positive signals, strong incentives
- Disconfirms: Resource constraints, technical barriers, competing priorities
- Predicts: Outcome significantly above trend extrapolation

---

## Seeking Disconfirming Evidence

For each scenario, actively search for evidence that would falsify it:

### Questions to Ask
- What would make this scenario impossible or unlikely?
- What early warning signs would indicate this scenario is wrong?
- Who disagrees with this scenario and why?
- What historical examples contradict this scenario?

### Evidence Types to Consider
- Technical feasibility constraints
- Resource and timeline constraints
- Organizational and incentive factors
- External dependencies and conditions
- Historical precedents that failed

**Anti-pattern**: Only searching for confirming evidence. Force yourself to steelman alternatives.

---

## Adjustment Factors

Document how each inside view factor adjusts the base rate:

| Factor | Direction | Magnitude | Confidence | Notes |
|--------|-----------|-----------|------------|-------|
| Explicit prioritization | + | Moderate | Medium | Labs have announced focus |
| Technical ceiling | - | Small | High | Diminishing returns near saturation |
| Competitive dynamics | + | Small | Low | Uncertain if accelerates progress |

### Magnitude Guidelines
- **Large**: >20pp shift or >2x change
- **Moderate**: 10-20pp shift or 1.5-2x change
- **Small**: 5-10pp shift or 1.1-1.5x change
- **Minimal**: <5pp shift

### Confidence Guidelines
- **High**: Strong evidence, well-established mechanism
- **Medium**: Reasonable evidence, plausible mechanism
- **Low**: Weak evidence, speculative mechanism

---

## Output: 03_inside_view_adjustments.json

```json
{
  "phase": 3,
  "completed_at": "<timestamp>",

  "fermi_decomposition": {
    "components": [
      {
        "factor": "<subproblem description>",
        "estimate": "<value or probability>",
        "reasoning": "<how estimated>"
      }
    ],
    "combination_method": "<how components combine>",
    "decomposition_result": "<combined estimate>"
  },

  "scenarios": [
    {
      "name": "Conservative",
      "key_assumption": "<what must be true>",
      "supporting_evidence": ["<evidence list>"],
      "disconfirming_evidence": ["<evidence that would falsify>"],
      "implied_outcome": "<prediction under this scenario>",
      "initial_weight": 0.3
    },
    {
      "name": "Moderate",
      "key_assumption": "<what must be true>",
      "supporting_evidence": ["<evidence list>"],
      "disconfirming_evidence": ["<evidence that would falsify>"],
      "implied_outcome": "<prediction under this scenario>",
      "initial_weight": 0.5
    },
    {
      "name": "Optimistic",
      "key_assumption": "<what must be true>",
      "supporting_evidence": ["<evidence list>"],
      "disconfirming_evidence": ["<evidence that would falsify>"],
      "implied_outcome": "<prediction under this scenario>",
      "initial_weight": 0.2
    }
  ],

  "adjustment_factors": [
    {
      "factor": "<description>",
      "direction": "+|-",
      "magnitude": "large|moderate|small|minimal",
      "confidence": "high|medium|low",
      "notes": "<reasoning>"
    }
  ],

  "adjusted_estimate": {
    "point_estimate": "<adjusted from base rate>",
    "reasoning": "<how adjustments were applied>"
  }
}
```

---

## Checkpoint

Before proceeding to Phase 4, verify:

**Ask the user**: "Have you generated at least 3 competing scenarios with explicit disconfirming evidence for each?"

- If **YES**: Proceed to Phase 4 (Multi-Model Weighting)
- If **NO**: Add more scenarios or strengthen disconfirming evidence search

Also verify:
- Is there a scenario where you're wrong in each direction?
- Have you actively sought evidence against your preferred scenario?
- Are adjustment magnitudes justified by evidence strength?
