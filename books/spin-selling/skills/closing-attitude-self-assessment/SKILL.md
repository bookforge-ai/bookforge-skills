---
name: closing-attitude-self-assessment
description: "Administer and score the Closing-Attitude Scale — a 15-item validated psychometric from SPIN Selling research. Use when a salesperson wants to evaluate whether their attitude toward closing techniques fits the kind of sale they are running, assess whether they are closing too aggressively or too passively, diagnose if their pro-closing beliefs could be hurting their large-sale results, answer 'should I close harder?', 'am I closing too aggressively?', 'is my closing approach wrong for this type of deal?', or 'evaluate my closing attitude'. Also invoke for anyone who believes 'always be closing' is good sales practice, wants to test themselves against Rackham's research findings, or needs to understand why closing techniques hurt large-sale performance. The skill administers all 15 items interactively, calculates a total (15-75), interprets the score against the user's actual selling context (deal value, buyer sophistication, post-sale relationship), and delivers a written assessment with remediation guidance when score and context are mismatched."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/closing-attitude-self-assessment
metadata: {"openclaw":{"emoji":"🎯","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books: ["spin-selling"]
tags: ["sales", "b2b-sales", "closing", "enterprise-sales", "self-assessment", "sales-methodology"]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: interactive
      description: "User answers to 15 Likert items (1-5 each) administered one at a time or in batch"
    - type: interactive
      description: "Selling context: deal value level, buyer sophistication, and post-sale relationship length"
  outputs:
    - closing-attitude-assessment.md
  tools-required: [Write]
  tools-optional: [Read]
  mcps-required: []
discovery:
  trigger_phrases:
    - "evaluate my closing attitude"
    - "should I close harder"
    - "am I closing too aggressively"
    - "is my closing approach wrong"
    - "how do I know if my closing style is hurting me"
    - "always be closing"
    - "closing techniques in large sales"
    - "why am I losing deals after good demos"
    - "closing attitude test"
    - "spin selling closing scale"
---

# Closing-Attitude Self-Assessment

## When to Use

You are working with a salesperson — B2B account executive, enterprise rep, solutions consultant, or founder-led seller — who wants to evaluate whether their beliefs and instincts about closing techniques align with the type of selling they actually do.

**This skill is the right tool when:**
- The user asks "am I closing too hard?" or "should I be closing more?"
- The user has been trained in closing techniques and wants to know if those beliefs are helping or hurting them
- The user is losing large deals after what felt like strong calls, and instinct is to "close harder"
- A sales manager suspects a rep's pro-closing attitude is alienating sophisticated buyers
- The user wants to benchmark their beliefs against Rackham's empirical research

**This skill is NOT the right tool when:**
- The user wants to plan how to obtain commitment on a specific upcoming call — use `commitment-and-advance-planner`
- The user wants to classify the outcome of a past call — use `call-outcome-classifier`
- The user wants to learn closing techniques (this skill may conclude the opposite is needed)

**Scale origin:** The Closing-Attitude Scale was developed by Neil Rackham and colleagues at Huthwaite when a chemical company's marketing director believed poor results were an "attitude problem." The researchers created the 15-item instrument and measured 38 salespeople. The results were the opposite of what the director expected: those with the most pro-closing attitude were *below* sales target, not above it. The scale and its interpretation framework appear verbatim in SPIN Selling, Appendix B.

## Context and Input Gathering

### Required (ask if not provided)
- **Nothing is required upfront.** The skill administers the assessment first, then gathers selling context for interpretation.

### Gathered During Administration
After scoring, ask about three contextual factors:
1. **Deal value:** Are the deals you typically run low-value (under ~$5K), mid-range, or high-value/enterprise?
2. **Buyer sophistication:** Are your buyers typically consumers or junior buyers — or trained procurement professionals, senior executives, and professional purchasing agents?
3. **Post-sale relationship:** After the sale closes, do you have no ongoing relationship, or does your company provide ongoing service, support, or account management to that buyer?

These three factors are Rackham's exact criteria for determining whether a pro-closing attitude is justified or harmful.

## Process

### Step 1: Administer the Scale
**ACTION:** Present all 15 items from the Closing-Attitude Scale. Either administer one item at a time (recommended for reflective engagement) or present all 15 at once and ask for scores.

**WHY:** The scale is designed to surface instinctive beliefs, not considered positions. Presenting items one at a time reduces the tendency for the user to "correct" later answers based on pattern recognition from earlier ones. However, batch presentation is acceptable when the user explicitly prefers efficiency.

**Administration format (one at a time):**
> "I'll ask you 15 statements. For each one, rate your agreement on a 1-5 scale where:
> 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree, 5 = Strongly Agree
>
> There are no trick questions, and no answer is wrong — the scale is calibrated empirically. Answer what you actually believe, not what you think is 'correct.'"

Present each item and collect the numeric score. See [`references/closing-attitude-scale.md`](references/closing-attitude-scale.md) for all 15 items verbatim. Do not paraphrase the items.

**Record scores in a running list:** Item 1: ___, Item 2: ___, ... Item 15: ___

### Step 2: Calculate the Total Score
**ACTION:** Sum all 15 scores. Present the result clearly.

**WHY:** The sum is the only metric — there are no subscales. The total positions the user on the pro-closing spectrum relative to Rackham's threshold.

**Formula:**
```
Total = Item1 + Item2 + Item3 + ... + Item15
Range: 15 (all 1s) to 75 (all 5s)
Neutral point: 45
Favorable-attitude threshold: > 50
```

**Present as:**
> "Your total score is **[X]** out of 75.
> - Below 45: Skeptical of closing techniques
> - 45-50: Neutral to mildly favorable
> - Above 50: Favorable attitude toward closing techniques"

Do NOT interpret the score yet. Proceed to context gathering first.

**WHY the order matters:** A score of 58 means something very different for a door-to-door canvasser vs an enterprise software AE. Interpreting before establishing context produces advice that could be directionally wrong.

### Step 3: Gather Selling Context
**ACTION:** Ask three context questions about the user's typical sales:

> "Before I interpret your score, I need to understand the type of selling you do. Three quick questions:
>
> 1. **Deal value:** What is the typical deal size in your work — roughly low-value (under $5K, quick transactions), mid-range ($5K-$50K), or high-value/enterprise ($50K+, multi-month sales cycles)?
>
> 2. **Buyer sophistication:** Are the people you sell to typically consumers or informal buyers — or professional procurement agents, trained purchasing managers, and senior executives who buy for organizations regularly?
>
> 3. **Post-sale relationship:** After a deal closes, does the relationship end, or does your company have an ongoing relationship with that buyer (account management, support contracts, renewals, expansions)?"

Record responses for use in Step 4.

**WHY:** Rackham's key finding was that the *effectiveness* of closing techniques depends entirely on sale type. The same pro-closing behavior that helps in low-value transactional sales actively hurts in large, sophisticated, or relationship-based sales. Context is not a secondary consideration — it is the interpretation framework.

### Step 4: Apply Context-Aware Interpretation
**ACTION:** Apply Rackham's interpretation matrix against the user's score and context. Output a clear verdict — ALIGNED, MISMATCH-MILD, or MISMATCH-CRITICAL.

**WHY:** A high score (>50) is only a problem if the selling context is large/sophisticated/relational. The skill must be willing to tell a high-scoring user that their attitude is a **liability** in their context — this is Rackham's empirical finding, not opinion.

**Interpretation Matrix:**

| Score | Deal Value | Buyer Sophistication | Post-Sale Relationship | Verdict |
|-------|-----------|----------------------|------------------------|---------|
| ≤ 50 | Any | Any | Any | ALIGNED — skepticism about closing is well-founded across all sale types |
| > 50 | Low-value | Unsophisticated | None/minimal | ALIGNED — pro-closing attitude may be justified for transactional selling |
| > 50 | Low-value | Unsophisticated | Ongoing | MISMATCH-MILD — closing pressure strains relationships even in smaller sales |
| > 50 | Mid/High | Any | Any | MISMATCH-CRITICAL — pro-closing attitude is a liability in your context |
| > 50 | Any | Sophisticated | Any | MISMATCH-CRITICAL — professional buyers actively resist detected closing techniques |

**Deliver verdict with evidence:**

For ALIGNED (low score, any context):
> "Your score of [X] indicates a skeptical or neutral attitude toward closing techniques. This aligns with Rackham's research. In the Huthwaite 190-call study, calls with the fewest closing attempts outsold calls with the most closing attempts (21 vs 11 sales out of 30 calls each). Your instincts are evidence-based."

For ALIGNED (high score, transactional context):
> "Your score of [X] shows a favorable attitude toward closing. Given your context — [describe their context] — this is defensible. Rackham's Photo-Store Study found that closing training improved low-value sales success from 72% to 76%. The pro-closing approach is suited to transactional, high-volume selling where decision speed matters."

For MISMATCH-MILD:
> "Your score of [X] shows a favorable attitude toward closing. However, your context — [describe their context] — introduces friction. [Explain relevant mismatch factor.] The BP buyer questionnaire found that 34 of 54 professional buyers said they were *less likely* to buy when they detected closing techniques. Consider the risk of eroding the post-sale relationship."

For MISMATCH-CRITICAL:
> "Your score of [X] shows a strongly favorable attitude toward closing. **In your selling context, this is a liability, not an asset.**
>
> Rackham's evidence:
> - **Photo-Store Study:** Closing training *reduced* high-value sales success from 42% to 33%. The same training that helped with cheap goods hurt with expensive goods.
> - **190-Call Study:** Among 190 observed calls, the 30 calls with the most closing attempts produced only 11 sales. The 30 calls with the fewest closing attempts produced 21 sales.
> - **BP Buyer Questionnaire:** 34 of 54 professional buyers said detecting closing techniques made them *less* likely to buy. Only 2 said it made them more likely.
> - **Chemical Company Attitude Study (the origin of this scale):** The salespeople with the most favorable closing attitude were *below sales target*. The pro-closing group underperformed the skeptical group.
>
> Your beliefs about closing are optimized for a type of sale you are NOT running."

### Step 5: Deliver Remediation Guidance (if MISMATCH)
**ACTION:** For any MISMATCH verdict, explain the replacement behavior framework and point to the relevant skill.

**WHY:** Telling a user their beliefs are counterproductive without giving them a replacement creates anxiety without direction. Rackham's research identified exactly what should replace closing pressure — a framework called the Four Successful Actions for Obtaining Commitment.

**Remediation message:**
> "The goal is not to close less — the goal is to replace closing pressure with a framework that actually works in large sales. The research-backed replacement is called Advance-targeting: defining specific customer actions (advances) you want before each call, and using the Four Successful Actions to obtain them.
>
> The Four Successful Actions (Rackham, Chapter 2/Chapter 6):
> 1. **Invest in investigating** — spend enough time in discovery that the buyer has expressed real explicit needs, not just surface-level curiosity
> 2. **Check for unresolved concerns** — explicitly ask if there are remaining objections or issues before moving toward commitment
> 3. **Summarize benefits linked to the buyer's explicit needs** — not features or advantages, but benefits tied to what they said they needed
> 4. **Propose a specific commitment** — name a concrete next action, not a vague 'where do we go from here?'
>
> For a full tool to plan a specific advance for your next call, use `commitment-and-advance-planner`."

### Step 6: Write the Assessment Artifact
**ACTION:** Write a `closing-attitude-assessment.md` file summarizing the full assessment.

**WHY:** The assessment is a starting point for behavioral change, not a one-time read. A written artifact the user can return to — and share with their manager — increases the probability that the insights translate into practice.

**File structure:**
```markdown
# Closing-Attitude Assessment
**Date:** [date]
**Score:** [X] / 75
**Verdict:** [ALIGNED / MISMATCH-MILD / MISMATCH-CRITICAL]

## My Scores
[Item-by-item list with values]

## My Selling Context
- Deal value: [their answer]
- Buyer sophistication: [their answer]
- Post-sale relationship: [their answer]

## Interpretation
[Full interpretation text from Step 4]

## Recommended Next Steps
[Remediation from Step 5, if applicable; or affirmation if aligned]
```

## Key Principles

**The scale is empirically grounded, not prescriptive.**
Rackham did not design this scale to push a philosophical position about selling. It was created in response to a manager's hypothesis that pro-closing attitudes would predict better results. The data falsified that hypothesis. The scale's interpretation reflects what the data showed.

**High score in the right context is fine.**
Do not treat every score above 50 as a failure. The skill's job is context-sensitive interpretation, not universal anti-closing advocacy. A door-to-door canvasser, a retail floor salesperson, or a telesales rep handling low-value inbound may legitimately be well-served by pro-closing instincts.

**The mismatch verdict must be stated clearly.**
Baseline language models, trained on general sales literature, will validate pro-closing beliefs because most sales books still teach closing techniques. This skill enforces Rackham's empirical finding: **in large, sophisticated, or relationship-based sales, closing pressure correlates with worse outcomes.** The skill must be willing to state this plainly to a user who scores >50 and works in that context. Softening the verdict to avoid discomfort defeats the purpose.

**Remediation, not criticism.**
When delivering a mismatch verdict, always pair the critique with the replacement behavior (Four Successful Actions / Advance-targeting). The goal is to change behavior, not shame beliefs.

**Score items at face value — do not reverse-score.**
Items 2, 6, 8, 10, and 15 express skepticism about closing techniques. A high raw score on these means the user *disagrees* with the skepticism (i.e., is pro-closing). Score all items 1-5 as stated and sum them directly. The scale is calibrated so the sum produces the correct result without any adjustment.

## Examples

### Example 1: Enterprise AE with high score
**Scenario:** Senior enterprise AE, $200K average deal size, 6-month sales cycles, ongoing account management.
**Trigger:** User asks "I always close hard — is that hurting me?"
**Process:** Administer 15 items → score = 62 → gather context (high-value deals, trained procurement buyers, long-term account relationships) → apply matrix → MISMATCH-CRITICAL → deliver Photo-Store Study + BP buyer evidence → explain Four Successful Actions → write assessment artifact.
**Output:** `closing-attitude-assessment.md` with MISMATCH-CRITICAL verdict, citing that 42→33% high-value closing data matches their context exactly, plus pointer to `commitment-and-advance-planner`.

### Example 2: Inside sales rep with high score — aligned context
**Scenario:** Inside sales rep, $500 SaaS monthly subscriptions, 1-week close cycles, no post-sale relationship (product-led growth, no CSM).
**Trigger:** User wants to test their beliefs before a sales training.
**Process:** Administer 15 items → score = 55 → gather context (low-value, semi-sophisticated buyers, minimal ongoing relationship) → apply matrix → ALIGNED (pro-closing justified) → affirm with Photo-Store low-value data (72→76%) → acknowledge tradeoff (shorter relationship window).
**Output:** `closing-attitude-assessment.md` with ALIGNED verdict, noting that transactional context makes pro-closing attitude defensible.

### Example 3: New rep wanting to test themselves
**Scenario:** SDR transitioning to AE role, not sure if their closing instincts fit enterprise selling.
**Trigger:** Manager asks them to assess their beliefs before joining the SPIN training cohort.
**Process:** Administer 15 items → score = 47 → context (moving to $80K avg deal size, will be dealing with VP-level buyers) → ALIGNED (neutral score is already appropriate for the context they're entering) → affirm the score, note that as they enter enterprise AE work, scores above 50 would become a risk.
**Output:** `closing-attitude-assessment.md` with ALIGNED verdict and context-forward note about why maintaining this skeptical orientation matters for the new role.

## References

- Full 15-item instrument, scoring formula, and supporting study data: [`references/closing-attitude-scale.md`](references/closing-attitude-scale.md)
- For planning specific commitments and advances using the Four Successful Actions: `commitment-and-advance-planner`
- For classifying past call outcomes (Order / Advance / Continuation / No-sale): `call-outcome-classifier`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill is standalone. Companion skills from SPIN Selling:
- `clawhub install bookforge-commitment-and-advance-planner` — plan the specific commitment to seek on your next call using the Four Successful Actions
- `clawhub install bookforge-call-outcome-classifier` — classify whether a past call ended in an Advance, Continuation, Order, or No-sale

Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
