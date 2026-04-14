---
name: classify-rep-profile
description: "Classify a sales rep against the five CEB selling profiles (Challenger, Hard Worker, Relationship Builder, Lone Wolf, Reactive Problem Solver) and score their Teach/Tailor/Take-Control subscales using the Appendix B self-diagnostic. Use when a rep wants to know 'am I a Challenger', 'which sales profile am I', 'sales style assessment', 'classify sales rep', 'Challenger profile quiz', 'CEB sales profile', 'Teach Tailor Take Control self-diagnostic', 'what kind of rep am I', 'Relationship Builder Hard Worker Lone Wolf Reactive Problem Solver assessment', 'B2B sales rep diagnostic', 'rep profile classification', 'sales enablement assessment'. Applies CEB's empirical study of 6,000+ reps and 44 behavioral attributes. Produces a rep-profile-assessment.md artifact with profile classification, three subscale scores, threshold interpretation, dominant profile flags, and prioritized development recommendations."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/classify-rep-profile
metadata: {"openclaw":{"emoji":"📊","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors: ["Matthew Dixon", "Brent Adamson"]
    chapters: [2, 3, "Appendix B"]
tags: [sales, b2b-sales, sales-methodology, rep-diagnostic, sales-enablement, challenger-sale]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Rep's self-description, recent deal notes, or behavioral observations (optional — agent will gather via questions if not provided)"
  tools-required: [Read, Write, AskUserQuestion]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any working directory. No codebase required."
discovery:
  goal: "Classify a sales rep against the five CEB profiles and score their Teach/Tailor/Take-Control subscales"
  tasks:
    - "Guide rep through the 10-statement Appendix B self-diagnostic"
    - "Compute Teach / Tailor / Take-Control subscale scores"
    - "Classify dominant selling profile and secondary profile flags"
    - "Interpret scores against empirical thresholds"
    - "Produce development recommendations with prioritized subscale focus"
  audience:
    roles: ["B2B sales reps", "sales managers", "sales enablement professionals"]
    experience: intermediate
  when_to_use:
    triggers:
      - "Rep wants to self-assess their selling style"
      - "Manager wants to diagnose a rep's behavioral profile before coaching"
      - "Enablement team wants to baseline the team before a Challenger training initiative"
    prerequisites: []
    not_for:
      - "Hiring assessment or candidate screening (use a separate hiring guide)"
      - "Personality-type profiling (this measures observable behaviors, not traits)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: null
    assertion_count: 12
    iterations_needed: null
---

# Classify Rep Profile

Guides a sales rep (or their manager) through the 10-statement Appendix B self-diagnostic from CEB's research. Computes three Challenger subscale scores — Teach for Differentiation, Tailor for Resonance, Take Control — against empirical thresholds derived from a study of 6,000+ reps across 90 companies. Produces a structured assessment artifact with profile classification, subscale scores, profile flag analysis, and prioritized development recommendations.

The empirical basis: CEB's factor analysis of 44 behavioral attributes collapsed to five selling profiles. Only one profile dominates star performance (~40% of all high performers; >50% in complex solution sales): the Challenger.

## When to Use

- A rep asks "am I a Challenger?", "what's my selling style?", or "which sales profile fits me?"
- A manager wants a structured baseline before starting Challenger coaching with a rep
- A sales enablement team wants to assess where reps cluster before a training rollout
- A rep received feedback that they're "too accommodating" or "not pushing enough" and wants to understand why
- A team lead wants to check whether their perceived high performers are actually Challengers before scaling their behaviors

**Not for:** candidate screening, personality assessment, or competency-based performance reviews.

## Context & Input Gathering

Before running the diagnostic, collect two pieces of context:

**1. Deal complexity context** — Ask: "Are you primarily selling complex, bundled solutions with long sales cycles and multiple stakeholders, or simpler transactional products with short cycles?"

WHY: The Challenger profile dominates complex sales. In transactional/simple sales, the Hard Worker profile performs comparably. Context determines which profile classification carries the most urgency.

**2. Existing self-description (optional)** — Ask: "Is there a deal log, coaching note, or brief description of how you typically sell that I can read before we run the diagnostic?"

WHY: Pre-reading lets the agent validate self-reported scores against observed behaviors and flag potential score inflation.

## Process

### Step 1 — Establish context (2 questions)

Ask the user:
1. "Are your deals primarily complex solution sales (multi-stakeholder, long cycle, bundled offers) or simpler transactional sales?"
2. "Are you completing this for yourself (self-assessment), or are you assessing someone else (coaching/enablement)?"

WHY: The two answers calibrate how to interpret the results — which profile to prioritize developing toward, and whether to phrase questions in first or third person.

If existing deal notes or a coaching log are available, read them before proceeding.

### Step 2 — Administer the diagnostic

Present all 10 statements from `references/self-diagnostic-questionnaire.md`, one at a time (or in a single grouped prompt). For each statement, collect a score from 1 to 5.

WHY: The self-diagnostic was designed by CEB as the validated scoring instrument for the five-profile taxonomy. Each statement maps to a specific behavioral dimension — three map to the Challenger subscales (Q2, Q3, Q5, Q6, Q8, Q9); four flag other profile tendencies (Q1, Q4, Q7, Q10).

Guidance for the agent while presenting:
- Paraphrase each statement clearly in the current conversation context
- Do not hint at which answer is "more Challenger" — that biases results
- If a rep seems unsure, offer a concrete example relevant to their deal context

### Step 3 — Compute subscale scores

Calculate the three Challenger subscale scores:

| Subscale | Statements | Max |
|---|---|---|
| Teaches for Differentiation | Q2 + Q3 | 10 |
| Tailors for Resonance | Q5 + Q6 | 10 |
| Takes Control | Q8 + Q9 | 10 |

Apply empirical thresholds per subscale:
- **8+** → Strong Challenger behavior in this dimension
- **5–7** → Foundation established; targeted development needed
- **4 or below** → New territory; start with the most approachable behavior in this subscale

WHY: The thresholds come directly from CEB's scoring guide (Appendix B). They are not normative relative rankings — they are calibrated against the 6,000-rep study to indicate readiness to employ Challenger behaviors in each dimension.

Also note: profile flags for Q1 (Relationship Builder), Q4 (Lone Wolf), Q7 (Reactive Problem Solver), Q10 (Hard Worker). A score of 4 or 5 on any flag statement signals natural selling tendency outside the Challenger model.

### Step 4 — Classify dominant profile

Use this logic to determine primary profile:

1. If any Challenger subscale scores 8+ → the rep has Challenger capability in that subscale; note which ones
2. If all three subscales score 5–7 or higher → classify as Challenger in development
3. If one or more subscales score 4 or below AND a profile flag scored 4+ → the flag profile is the rep's dominant current profile
4. If multiple flags scored 4–5 → list all as secondary tendencies; the rep is a profile blend

WHY: CEB's model holds that every rep has some presence across all five profiles — the classification identifies the dominant behavioral "major," not a binary label. A rep can be a Challenger with Hard Worker tendencies.

**Complexity overlay:**
- Complex sales: Flag Relationship Builder classification as high-risk (nearly zero star performance in complex deals)
- Transactional sales: Hard Worker classification is viable — don't push Challenger development where deal complexity doesn't warrant it

### Step 5 — Write the assessment artifact

Create `rep-profile-assessment.md` in the working directory (or a specified output path).

WHY: A written artifact makes the assessment portable — it can be shared with a manager, filed in a coaching system, or revisited at the next development checkpoint.

## Inputs

| Input | Required | Description |
|---|---|---|
| Self-assessment responses (Q1–Q10) | Yes | Collected interactively during the diagnostic |
| Deal complexity context | Yes | Complex solution vs. transactional (gathered in Step 1) |
| Self/manager mode | Yes | Determines first/third person framing |
| Deal notes or coaching log | Optional | Used to validate or contextualize self-reported scores |

## Outputs

**Primary artifact:** `rep-profile-assessment.md`

```markdown
# Sales Rep Profile Assessment
**Rep:** [Name or "Self-Assessment"]
**Date:** [YYYY-MM-DD]
**Assessed by:** [Self / Manager: Name]
**Deal complexity context:** [Complex solution / Transactional]

---

## Diagnostic Scores

| Statement | Score (1–5) |
|---|---|
| Q1 — Lasting customer relationships | [score] |
| Q2 — Delivers unique customer perspectives | [score] |
| Q3 — Deep product/service expertise | [score] |
| Q4 — Willing to risk disapproval | [score] |
| Q5 — Adapts message to customer value drivers | [score] |
| Q6 — Identifies customer business drivers | [score] |
| Q7 — Personally resolves customer requests | [score] |
| Q8 — Guides customers to decisions in difficult situations | [score] |
| Q9 — Comfortable discussing pricing/money | [score] |
| Q10 — Extensive pre-call preparation | [score] |

---

## Challenger Subscale Scores

| Subscale | Score | Threshold |
|---|---|---|
| Teaches for Differentiation (Q2+Q3) | [x/10] | [Strong / Foundation / New territory] |
| Tailors for Resonance (Q5+Q6) | [x/10] | [Strong / Foundation / New territory] |
| Takes Control (Q8+Q9) | [x/10] | [Strong / Foundation / New territory] |

---

## Profile Classification

**Dominant profile:** [Challenger / Hard Worker / Relationship Builder / Lone Wolf / Reactive Problem Solver]

**Secondary tendencies:**
- [Profile if flag scored 4+, else "None detected"]

**Performance context:** [Challenger wins in complex sales (>50% of stars). Relationship Builder underperforms in complex sales (nearly zero star rate). Hard Worker is viable in transactional/simple deals.]

---

## Profile Flag Summary

| Flag | Statement | Score | Interpretation |
|---|---|---|---|
| Relationship Builder | Q1 | [score] | [High ≥4: tendency detected / Low: not dominant] |
| Lone Wolf | Q4 | [score] | [High ≥4: tendency detected / Low: not dominant] |
| Reactive Problem Solver | Q7 | [score] | [High ≥4: tendency detected / Low: not dominant] |
| Hard Worker | Q10 | [score] | [High ≥4: tendency detected / Low: not dominant] |

---

## Development Recommendations

**Priority 1 — [Lowest-scoring Challenger subscale]:**
[Specific development focus for this subscale — what to practice in the next 30 days]

**Priority 2 — [Second-lowest subscale]:**
[Specific development focus]

**Priority 3 — [If a profile flag scored high and it creates risk in current deal context]:**
[Specific behavioral shift to address the flag]

**Note on profile classification:** ~40% of star performers are Challengers; only ~7% of stars are Relationship Builders overall, dropping to nearly zero in complex solution sales. This diagnostic measures current behavior, not fixed capacity — all three Challenger subscales are learnable with deliberate practice.

---

## Next Steps

- [ ] Share with manager for validation against observed behaviors
- [ ] Identify one Challenger subscale to develop over the next 30 days
- [ ] Re-take diagnostic in 90 days to measure progress
```

## Key Principles

**1. Behavior, not personality** — The five profiles describe observable selling behaviors, not personality types or fixed traits. Every rep has a behavioral "major" today that can shift with deliberate practice. Never treat the classification as a permanent label.

WHY: CEB specifically designed the study around demonstrated behaviors because skills and behaviors are actionable immediately, whereas personality traits cannot be coached in any practical timeframe.

**2. Challenger advantage is context-dependent** — The Challenger profile dominates complex solution sales. In transactional, high-volume, simple sales, the Hard Worker profile is equally viable. Avoid pushing Challenger development in contexts where deal complexity doesn't warrant it.

WHY: CEB's data shows all five profiles perform roughly equally in simple/transactional deals. The Challenger advantage emerges specifically as deal complexity increases.

**3. High performer ≠ Challenger** — Only ~40% of star performers are Challengers. When managers identify "their Challengers" without using a diagnostic, they typically just select their high performers regardless of selling style. This risks scaling Lone Wolf or Relationship Builder behaviors instead.

WHY: The Appendix B diagnostic exists precisely to solve this problem — it separates profile from performance so organizations scale the right behaviors.

**4. The Relationship Builder risk is real in complex sales** — Relationship Builders represent only 7% of star performers overall, and nearly zero in complex solution sales. A service-oriented, tension-avoidant approach cannot drive the behavioral change complex buying decisions require.

WHY: Complex sales ask customers to change how they operate. A rep who defuses tension and accommodates every demand cannot push the customer to think differently — which is the core commercial mechanism of complex buying.

**5. Self-report needs behavioral validation** — Self-assessment scores are a starting point, not a verdict. High performers sometimes understate their Challenger behaviors (false modesty); Relationship Builders sometimes overstate them (not recognizing the gap). Supplement with manager observations or call-review evidence when the stakes are high.

WHY: CEB's original methodology used manager observations of rep behaviors, not self-reports. Appendix B is a practical approximation — calibrate it against behavioral evidence wherever possible.

## Examples

### Example 1 — Sales rep self-assessment (complex B2B SaaS)

**Scenario:** A mid-market account executive at a SaaS company asked "I always get good reviews from customers but I'm not hitting quota. What profile am I?"

**Trigger:** "What sales profile am I? I think I might be a Relationship Builder."

**Process:** Agent established deal complexity (complex, multi-stakeholder SaaS deals, 60-90 day cycles). Administered the diagnostic — rep scored: Q1=5, Q2=3, Q3=4, Q4=2, Q5=3, Q6=3, Q7=4, Q8=2, Q9=2, Q10=3.

**Output excerpt from rep-profile-assessment.md:**

```
Challenger Subscale Scores:
- Teaches for Differentiation (Q2+Q3): 7 — Foundation
- Tailors for Resonance (Q5+Q6): 6 — Foundation
- Takes Control (Q8+Q9): 4 — New territory

Dominant profile: Relationship Builder (Q1=5 flag; Takes Control at floor)

Priority 1 — Takes Control (score: 4): Practice holding the silence after a proposal.
In the next 3 deals, script one moment where you guide the customer to a decision rather
than waiting. Specifically: become comfortable discussing pricing on the customer's terms.

Note: In complex SaaS deals (your context), Relationship Builder profile correlates with
nearly zero star performance. Your teaching and tailoring foundations are buildable —
but Take Control is the most urgent gap between your current approach and quota attainment.
```

---

### Example 2 — Manager diagnosing a rep before coaching

**Scenario:** A regional sales manager wants to understand her top performer's profile before scaling his approach to the team.

**Trigger:** "My best rep is crushing quota. I want to understand his selling style before I ask him to mentor others."

**Process:** Agent flagged the anti-pattern — high performer ≠ Challenger. Manager provided deal notes from the rep's last three wins. Agent administered diagnostic in third-person ("How would [rep] rate himself on each statement?"). Rep scored: Q1=3, Q2=5, Q3=5, Q4=4, Q8=4, Q9=5 (Lone Wolf flag on Q4; strong Challenger subscales).

**Output excerpt:**

```
Dominant profile: Challenger (all three subscales 8+)
Secondary tendency: Lone Wolf (Q4=4 — willing to risk disapproval)

Safe to scale: Yes — this rep's performance is driven by Challenger behaviors
(Teach/Tailor/Take Control), not Lone Wolf rule-breaking. The Lone Wolf flag
is a secondary tendency, not the primary mechanism of their success.

Recommendation: Observe and codify this rep's commercial teaching conversations
specifically — how they frame unique perspectives and hold tension before closing.
Those are the replicable behaviors.
```

---

### Example 3 — Team enablement baseline

**Scenario:** A sales enablement leader wants to understand where her 12-person team clusters before rolling out a Challenger training program.

**Trigger:** "Can you help me assess what profile mix I have on my team so I know where to focus training?"

**Process:** Agent recommended running the diagnostic for each rep individually (or self-administered in a group session) and aggregating subscale scores. Agent produced a team profile summary template.

**Output excerpt:**

```
Team Profile Summary (12 reps):
- 3 reps: Challenger (all subscales 5+, no dominant profile flags)
- 4 reps: Relationship Builder dominant (Q1=5, Takes Control at 4 or below)
- 2 reps: Hard Worker dominant (Q10=5, transactional deal focus)
- 2 reps: Challenger in development (subscales 5-7, no strong flags)
- 1 rep: Lone Wolf flag (Q4=5, inconsistent subscale scores)

Training priority: Takes Control subscale (team average: 5.2 — lowest).
8 of 12 reps score below 7 on Takes Control. Recommend leading training with
money conversation practice and guided commitment techniques before moving
to teaching content — the team can teach but cannot close the tension.
```

## References

- [Five Sales Rep Profiles](references/five-profiles.md) — Full profile definitions, behavioral signatures, and CEB performance data
- [Self-Diagnostic Questionnaire](references/self-diagnostic-questionnaire.md) — 10-statement instrument, scoring guide, threshold interpretations, and sample score interpretation

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The skill was generated by the [BookForge](https://github.com/bookforge-ai/bookforge) pipeline from _The Challenger Sale_ by Matthew Dixon and Brent Adamson (Portfolio/Penguin, 2011). Content has been paraphrased and structured as an executable skill — it does not reproduce verbatim passages from the copyrighted work. Attribution required on redistribution.

## Related BookForge Skills

This skill has no dependencies. It is the foundational classification layer for the Challenger Sale skill set — other skills in this set assume the rep has already completed a profile assessment.
