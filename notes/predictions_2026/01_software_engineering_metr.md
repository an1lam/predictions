# Software Engineering: METR Horizon Doubling Time

## Current Value
4.7 months (as of early 2025)

## Base Rate / Trend Analysis

METR's task horizon metric measures the length of tasks (by human completion time) that AI agents can complete with 50% reliability.

**Historical trajectory:**
- 2019-2025 overall: ~7 months doubling time
- 2024-2025 recent trend: ~4 months doubling time
- Some domain-specific measurements show 2-6 month ranges

**Current model horizons (50% success):**
- Claude 3.7 Sonnet: ~56 hours
- Claude Opus 4.5: ~289 hours
- GPT-5.1 Codex Max: ~173 hours

The metric has shown recent acceleration - the doubling time compressed from 7 months (long-term average) to ~4 months in 2024-2025.

## Adjustment Factors

### Upward pressures (slower progress / longer doubling time)
- As horizons extend from hours to days/weeks, tasks become qualitatively harder
- Error propagation compounds over longer task durations
- Planning and recovery from mistakes require different capabilities
- Training data for multi-day autonomous tasks is scarce
- May hit diminishing returns from current scaling approaches

### Downward pressures (faster progress / shorter doubling time)
- Massive investment in agentic AI from all major labs
- Better scaffolding, tool use, and agent architectures
- Competition driving rapid iteration
- New training paradigms (RL, process supervision)
- Synthetic data generation for longer tasks

## Final Prediction
**Value:** 4.5 months

**Confidence notes:** The recent acceleration from 7 to 4 months is striking but likely represents a transition period as labs focused heavily on agents. I expect the trend to stabilize rather than continue accelerating. A doubling time under 3 months seems unsustainable over a full year given the increasing difficulty of longer tasks. Predicting slight improvement from 4.7 to 4.5 months reflects continued progress without extrapolating recent acceleration indefinitely.

## Sources
- [METR: Measuring AI Ability to Complete Long Tasks](https://metr.org/blog/2025-03-19-measuring-ai-ability-to-complete-long-tasks/)
- [How Does Time Horizon Vary Across Domains?](https://metr.org/blog/2025-07-14-how-does-time-horizon-vary-across-domains/)
