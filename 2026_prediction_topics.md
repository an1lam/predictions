# 2026 Prediction Topics

Based on track record analysis (strong on AI capabilities, weaker on deployment timelines) and interests in AI and biotech/biopharma.

---

## AI Capabilities & Benchmarks

1. **Frontier model on ARC-AGI-2**: What score will the best frontier model achieve by end of 2026? (Ladder: >25%, >40%, >60%, >80%)

2. **FrontierMath progress**: Best model score by EOY 2026?

  a. Predictions: 90% CI = [45%, 85%], Median = 65%
  b. Reasoning: Extrapolated the trend lines from the Epoch leaderboard for Google and OpenAI, both of which involved jumps from single digits to ~40% this past year. That means 85% would be even faster progress than this past year and require taking a big chunk out of tier 3. I give that much faster progress a 10% chance, hence how I get 85%. For my median, I am roughly taking this past year's progress and repeating it in terms of absolute scale, under the assumption that we remain in the straight line part of the sigmoid.
  c. Resolution source(s): [Epoch AI Leaderboard](https://epoch.ai/benchmarks/frontiermath)

3. **SWE-Bench Verified**: Will any model exceed 90% on SWE-Bench Verified?

  a: Prediction: 75%
  b. Reasoning: I think if the current trend continues, this happens easily. The real Q I have is where SWE-Bench Verified's noise ceiling is. It's supposedly the verified (by the labs) subset of the broader SWE-Bench, so I'm guessing it's reasonably high, but I still give a 1 in 4 chance that either progress slows dramatically (5%) or it's close enough to 90% that getting there proves difficult (20%).

4. **GPQA Diamond**: Will any model exceed 95%?

5. **Mathematical theorem proving**: Will an AI system be the primary author of a novel proof of a result that would be publishable in a top math journal (not just IMO problems)?

  a. Prediction: 70%
  b. Reasoning: I don't think we're that far off with GPT 5.2 Pro / Gemini 3 Deep Think. Plus, this is now an extremely hyped application, so lots of people are going to be trying (which there's nothing wrong with). Plus, we already have reports of GPT 5.2 Pro proving small conjectures. Altogether, feels quite likely. The main Q is whether the models will get good enough this year to be primary author on a substantial enough piece of work.

6. **Agentic coding reliability**: Will you personally trust an AI agent to complete a multi-file PR without review on a real project you care about?

7. **RE-Bench (AI Research)**: What score will the best model achieve by EOY 2026? (Ladder: >1.5, >2.0, >2.5, >3.0)

8. **Cybench (Cybersecurity)**: Best model score by EOY 2026? (Ladder: >60%, >70%, >80%)

9. **OSWorld (Computer Use)**: Best model score by EOY 2026? (Ladder: >50%, >70%, >85%)

**GDPVal performance**: 

**Remote labor index**:

**[TextQuests](https://www.textquests.ai/)** ([leaderboard backup](https://dashboard.safe.ai/)): 

**[Terminal Bench 2.0](https://www.tbench.ai/leaderboard/terminal-bench/2.0)**

Continual learning: 
1. Will one of the major labs release a product that applies a form of continual weight updates to a large generative model?

  a. Prediction: 25%
  b. Reasoning: I think this is enough of a logistical difficulty that unless they already have something in research, it's very unlikely to be released externally, even if they were to have it. Note that something like Cursor Tab doesn't count here.

1. Will one of the major labs release a paper or product that involves a model controlling the contents of a non-text/image external memory?

  a. Prediction: 40%
  b. Reasoning: I keep thinking this is going to happen and then it doesn't, so I need to update downwards on the base probability of it happening. That said, my inside view intuition is that, given that contexts aren't growing nearly as quickly YoY as other capabilities, the allure of an external memory that's "trained in" will become too great to resist at some point. Anthropic already has the memory tool, so this seems like an obvious potential next step.

1. Will a paper come out that I view as making substantial, fundamental progress on the continual learning problem?

  a. Prediction: 44%
  b. Reasoning: Conjunction - it needs to come out and I need to see it. I give 55% chance to something coming out and then 80% chance I see it.


Memory predictions

---

## Agentic & Real-World Utility

*Targeting the gap between benchmark performance and practical utility*

10. **METR 50% time horizon**: What will be the frontier model's 50% time horizon (task length in human-professional-time completed with 50% probability) by EOY 2026? Current: ~2 hours. Predict 90th %ile confidence interval and median.

  a. Prediction(s): 90% CI: [5 hours, 24 hours], Median: 12 hours
  b. My base case is the trend continues. If the trend continues, then my current median for EOY is roughly 3 hours based on [this Epoch forecast](). Extrapolate 14 months, so two doublings and we get 12 hours. For 90% CI, I took my current lower (2 hours) and upper (4 hours) bounds and then my bounds on the trend and extrapolate them 13 months ahead. So 5 hours is assuming a little over one doubling rather than 2, and 24 hours assumes a little more than 2 doublings rather than less.

12. **SciCode**: Best model score by EOY 2026? (Ladder: >30%, >50%, >70%)

13. **BALROG (game playing)**: Best model score by EOY 2026?


16. **Memory and adaptation**: Will any deployed AI system demonstrate persistent memory and learning across sessions that meaningfully improves performance on user-specific tasks?

17. **Multi-day agent runs**: Will any AI agent successfully complete a task requiring multiple days of autonomous operation (with appropriate checkpointing)?

18. **Tool use reliability**: Will agentic tool use (web browsing, code execution, API calls) reach >90% reliability for straightforward tasks in any deployed system?

---

## AI Deployment & Business

*Note: This is a historically weaker area - good calibration practice.*

19. **AI revenue milestone**: Will any pure-play AI company (not Google/Microsoft/Amazon) exceed $10B ARR? $5B?

20. **Combined AI lab revenue**: What will be the sum of OpenAI, Anthropic, and xAI revenues by EOY 2026? (Ladder: >$15B, >$20B, >$30B)

21. **Coding assistant penetration**: What % of professional developers will use AI coding assistants daily? (Ladder: >30%, >50%, >70%)

22. **AI lab valuation**: Will Anthropic's valuation exceed $100B by EOY 2026?

23. **Enterprise AI agents**: Will any Fortune 500 company publicly claim to have replaced >1000 FTEs with AI agents?

24. **Public attention**: What % of Google searches will be AI-related by EOY 2026? (Ladder: >0.5%, >1%, >2%)

---

## AI Safety & Risk Levels

*Based on OpenAI Preparedness Framework categories*

25. **Cybersecurity risk level**: Will any frontier model reach "Medium" or higher on OpenAI's cybersecurity preparedness scale?

26. **CBRN risk level**: Will any frontier model reach "High" on CBRN (chemical, biological, radiological, nuclear) risk?

27. **Persuasion risk level**: Will any frontier model reach "High" on persuasion/manipulation capabilities?

28. **Model Autonomy risk level**: Will any frontier model reach "Medium" or higher on autonomous operation capabilities?

29. **Major AI incident**: Will there be a publicly reported incident where an AI system causes >$100M in damages or demonstrable harm at scale?

---

## Biotech/Biopharma

30. **AI-designed drug milestone**: Will a drug where AI played a central role in target or molecule discovery receive FDA approval in 2026?

31. **AlphaFold-class breakthrough**: Will there be another structural biology prediction breakthrough on par with AlphaFold (e.g., reliable protein dynamics, full complex prediction, variant effect prediction)?

32. **Cell therapy manufacturing**: Will CAR-T manufacturing costs drop below $50k/patient for any approved therapy?

33. **GLP-1 competition**: Will a non-Novo/Lilly GLP-1 agonist gain significant US market share (>10% of new prescriptions)?

34. **Gene therapy approvals**: How many new gene therapy approvals in 2026? (Ladder: >3, >5, >8)

35. **Biotech IPO window**: Will there be >20 biotech IPOs in 2026?

---

## AI + Bio Intersection

36. **Lab automation**: Will any company demonstrate a fully autonomous "scientist-in-a-loop" system that runs >100 experiments without human intervention?

37. **AI in clinical trials**: Will AI-driven patient selection/trial design demonstrably reduce a Phase II/III trial timeline by >30% for a major pharma company?

38. **Foundation models for biology**: Will a bio foundation model (protein, cell, etc.) achieve a clear commercial success (>$50M revenue or acquisition >$500M)?

39. **Closed-loop drug discovery**: Will any company announce an AI-discovered drug entering Phase I where the entire target-to-candidate pipeline was <18 months?

---

## Calibration Challenges

These deliberately target historically weaker areas:

- **Physical deployment**: Pick 2-3 robotics/hardware predictions to test "deployment discount"
- **Personal predictions**: Include 1-2 about your own output (papers, projects) with explicit planning-fallacy correction
