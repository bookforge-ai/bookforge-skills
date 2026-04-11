---
name: product-market-fit-readiness-gate
description: "Use this skill to determine whether a product is ready for scaled growth experimentation BEFORE investing in acquisition, activation, or retention hacks. Runs the Sean Ellis must-have survey (40% 'very disappointed' threshold), analyzes retention curve stability, and outputs a binary go/no-go verdict with remediation protocol for failing products. Triggers when a growth PM asks 'are we ready to scale?', 'should we invest in acquisition yet?', 'do we have product/market fit?', 'is my product must-have?', 'should we hire a growth team?', or 'why are our experiments not working?'. Also activates for 'how do I run the Sean Ellis test', 'must-have survey', 'product/market fit check', 'retention curve analysis', 'PMF gate', or 'premature scaling check'. Use BEFORE any other growth skill — this is the gate."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/product-market-fit-readiness-gate
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [2]
tags:
  - growth
  - product-market-fit
  - experimentation
  - startup-ops
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: >
        Product brief (product-brief.md) describing the product, ICP, core value
        proposition, and current stage. Optional: survey-responses.csv with raw
        must-have survey responses. Optional: retention-cohorts.csv with weekly
        or monthly cohort retention data.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set — product brief + optional CSV data. No code execution required.
discovery:
  goal: >
    Prevent premature scaling by producing a defensible go/no-go verdict on
    whether a product has reached must-have status before the team invests
    in scaled growth experimentation.
  tasks:
    - "Read or collect product brief"
    - "Check if must-have survey data exists"
    - "If no survey, generate survey template with exact Sean Ellis wording"
    - "If survey exists, score it against 40% threshold"
    - "Analyze retention curve shape"
    - "Emit go/no-go verdict with rationale"
    - "For no-go: produce remediation protocol"
---

# Product Market Fit Readiness Gate

A go/no-go gate that determines whether a product has achieved must-have status before the team invests in scaled growth experimentation. Produces a structured verdict with evidence and, for failing products, a concrete remediation protocol.

## When to Use

Use this skill at the moment a growth team is deciding whether to shift from product development into high-tempo experimentation. Typical triggers:

- The team is about to hire growth engineers, spin up an ads budget, or launch a referral program
- Experiments are running but results feel inconclusive or disappointing
- Leadership is asking "are we ready to scale?" or "why isn't acquisition converting?"
- A new growth lead has joined and needs a baseline readiness assessment

Do not use as an ongoing monitoring tool once growth is already at scale — at that stage, retention dashboards and North Star metrics replace this gate.

## Context & Input Gathering

Begin by reading the product brief. Then check whether survey data and cohort retention data are available.

**Branch A — Survey data exists (`survey-responses.csv`):**
Proceed directly to Step 3 (scoring). Skip survey template generation.

**Branch B — No survey data:**
Ask the user: "Have you already sent a must-have survey to active users? If yes, share the response file. If not, I'll generate the survey template now so you can send it before scoring."
Generate `must-have-survey-template.md` (Step 2), then pause and wait for results before completing the verdict.

**Branch C — No retention data (`retention-cohorts.csv`):**
Proceed with survey scoring only. Flag in the verdict that retention analysis is incomplete and recommend pulling cohort data from your analytics tool (Mixpanel, Amplitude, Looker, etc.) before treating the verdict as final.

## Process

### Step 1: Gather product context

Read `product-brief.md`. Extract:
- Product name and category
- Ideal customer profile (ICP)
- Core value proposition / aha moment hypothesis
- Current user volume and stage (private beta / public / post-launch)

**Why:** The scoring thresholds and remediation paths differ by product type (high-frequency consumer app vs. annual SaaS vs. marketplace). Without context, the verdict will be generic and the remediation protocol will miss the most likely failure modes.

**Output:** A one-paragraph context summary to embed in the verdict document.

---

### Step 2: Generate the must-have survey (if no data exists)

Write `must-have-survey-template.md` containing the exact survey question and answer options:

```
Subject: Quick question about [Product Name]

How would you feel if you could no longer use [Product Name]?

a) Very disappointed
b) Somewhat disappointed
c) Not disappointed (it really isn't that useful)
d) N/A — I no longer use it
```

Include the following diagnostic questions (send only if initial score is below threshold, or include upfront for efficiency):

1. What would you likely use as an alternative to [Product Name] if it were no longer available?
   - I probably wouldn't use an alternative
   - I would use: ___________

2. What is the primary benefit you have received from [Product Name]?

3. Have you recommended [Product Name] to anyone?
   - No
   - Yes — please explain how you described it: ___________

4. What type of person do you think would benefit most from [Product Name]?

5. How can we improve [Product Name] to better meet your needs?

6. Would it be okay if we followed up by email to clarify one or more of your responses?

**Targeting note:** Send to active users only (those who have used the product in the past 30 days). Dormant users produce uninformative responses and low completion rates. Aim for at least 200–300 responses before treating the score as reliable.

**Why:** Survey wording matters. Substituting "love" or "miss" for "very disappointed" changes the emotional register and invalidates comparison to the published threshold. The exact wording is the validated signal.

**Output:** `must-have-survey-template.md`

---

### Step 3: Score the must-have survey

Count responses by category. Calculate:

```
Very Disappointed % = (count of "Very disappointed" responses) / (total responses excluding "N/A") × 100
```

Apply the three-band decision rule:

| Score | Verdict | Meaning |
|---|---|---|
| >= 40% | GO | Product has achieved must-have status. Green light for growth experimentation. |
| 25–40% | CONDITIONAL | Product or messaging needs targeted improvement. Limited experiments may run in parallel, but broad acquisition investment is premature. |
| < 25% | NO-GO | Either the wrong audience is being surveyed, or the product requires substantial development. Halt acquisition spend immediately. |

**Why:** The 40% floor is not arbitrary — it reflects the minimum density of passionate users needed to sustain word-of-mouth and withstand the churn that follows broad acquisition. Scaling below this threshold accelerates user exodus (the BranchOut pattern): viral mechanics bring users who find no compelling reason to stay, CAC permanently exceeds LTV, and the company burns capital on a leaking bucket. The 25–40% band is actionable because the product has real fans — they just need either a better product or better communication of the existing value.

**Output:** Score summary section in `pmf-readiness-verdict.md`

---

### Step 4: Analyze the retention curve

If `retention-cohorts.csv` is available, read it. Evaluate:

1. **Shape:** Does the curve flatten and stabilize, or does it continue declining toward zero? A curve that flattens — even at a low absolute rate — indicates a core segment of retained users. A curve continuously declining toward zero means no durable value for any cohort.

2. **Level vs. benchmarks:**
   - Consumer mobile apps: average 1-month retention ~10%; best-in-class 60%+
   - SaaS (annual): retention north of 90% is the competitive baseline
   - Marketplaces and social products: compare to closest public comps

3. **Masking signal:** Check whether strong new-user acquisition is hiding early-cohort churn. Isolate cohorts by signup month and track each independently.

**Verdict mapping:**
- Stable curve at competitive level → confirms GO or softens CONDITIONAL
- Stable curve but below benchmarks → retention work needed even if survey passes
- Continuously declining curve → reinforces NO-GO regardless of survey score

**Why:** The survey captures users' stated preference; the retention curve reveals revealed behavior. Both signals need to align. A product can pass the survey (enthusiastic fans who said they'd be very disappointed) but still show declining retention if the aha moment is inconsistently delivered. Retention without survey data is also incomplete — it cannot tell you whether satisfaction is high enough among those who do stay.

**Output:** Retention analysis section in `pmf-readiness-verdict.md`

---

### Step 5: Emit the verdict

Write `pmf-readiness-verdict.md` with the following structure:

```markdown
# PMF Readiness Verdict: [Product Name]

**Date:** [date]
**Verdict:** GO / CONDITIONAL / NO-GO

## Evidence Summary
- Must-have survey score: X% very disappointed (N=total responses)
- Retention curve: [stable at Y% / continuously declining / data unavailable]
- Product category: [consumer mobile / SaaS / marketplace / other]

## Rationale
[2–3 sentences explaining the primary reason for the verdict, using the evidence above]

## Recommended Next Actions
[Specific to verdict — see Step 6 for NO-GO protocol]
```

**Why:** A written verdict forces the decision to be explicit and shared. Growth teams that skip this step frequently re-debate readiness at every planning meeting, wasting cycles. The written artifact is the commitment device.

**Output:** `pmf-readiness-verdict.md`

---

### Step 6: Remediation protocol (NO-GO and CONDITIONAL only)

For products scoring below 40%, do not guess at solutions in internal planning sessions. The three concurrent methods:

**A. Customer interviews (marketing/product design lead)**
Talk to active users — especially the "very disappointed" sub-segment, however small. Observe them using the product in context, not just in a formal interview. What job are they hiring the product to do? What friction prevents others from reaching that same outcome?

**B. Diagnostic analysis of "very disappointed" cohort (data analyst lead)**
Segment survey respondents by score. Identify behavioral differences: what did the "very disappointed" users do in the product that "somewhat disappointed" or "not disappointed" users did not? That difference often reveals the aha moment path that needs to be broadened.

**C. Minimum viable tests on product and messaging (engineering + growth lead)**
Run the smallest possible experiments that could close the gap — starting with messaging changes (cheapest, fastest) before committing to feature builds. Do not add features without evidence from methods A and B that the feature addresses a confirmed gap.

**Caution on feature creep:** Adding features is the intuitive response to a failing score, but it is often wrong. The remediation frequently requires removing friction or improving delivery of existing value, not adding new capabilities.

**Why:** Teams that skip structured remediation and instead hold whiteboard brainstorms burn time and money on unvalidated bets. The three-method approach distributes diagnostic work across specializations and produces convergent evidence before any engineering investment.

**Output:** Remediation plan appended to `pmf-readiness-verdict.md`

## Key Principles

**1. 40% is a floor, not a target.**
Products that just clear 40% are marginal. Teams should continue working to raise the score even after passing the gate. The threshold is the minimum for viable growth, not evidence of a breakout product.

**2. Retention confirms what the survey suggests.**
The survey captures stated preference under a hypothetical. The retention curve reveals actual behavior. Both signals must align before committing to scaled acquisition. A strong survey score with a declining retention curve means the aha moment is being promised but not reliably delivered.

**3. Premature scaling is the number one growth failure mode.**
Viral and paid acquisition mechanics can temporarily inflate user counts regardless of product quality. The BranchOut case demonstrates the collapse pattern: rapid acquisition before must-have status creates a user pool that churns faster than new users arrive, permanently exceeding cost of acquisition over lifetime value. The growth investment is consumed before the product is ready to convert it.

**4. Survey active users only.**
Targeting dormant users produces response bias and low completion rates. The signal you need comes from people who have experienced the product — even if their verdict is disappointment. Dormant users have already voted with their absence.

**5. The 25–40% band is actionable, not a failure.**
A score in this range means real fans exist. The job is to understand what those fans experience that others do not — and redesign the product or messaging to deliver that experience more consistently or to a better-matched audience.

**6. This gate applies once per growth phase, not perpetually.**
Re-run this gate when the product undergoes significant changes (new ICP, major feature pivot, new market entry). Do not use it as a routine measurement tool once growth is established.

## Examples

### Example 1: NO-GO — SaaS Team Collaboration Tool

**Scenario:** A B2B SaaS team has 800 paying users and is considering a $200K acquisition campaign. The Head of Growth asks, "Are we ready to scale paid acquisition?"

**Trigger:** "Are we ready to scale?" + existing user base large enough to survey.

**Process summary:**
- Survey sent to 600 active users; 280 responses received
- Very disappointed: 18% | Somewhat disappointed: 44% | Not disappointed: 31% | N/A: 7%
- Retention curve: month-3 cohorts retaining at 38%, month-6 at 22%, still declining
- Verdict: NO-GO

**Output excerpt from `pmf-readiness-verdict.md`:**
```
Verdict: NO-GO
Score: 18% very disappointed (well below 40% threshold)
Retention: Continuously declining — no stable cohort identified

Rationale: Both signals confirm the product has not achieved must-have status.
Scaling acquisition now would accelerate churn rather than compound growth.

Recommended next actions:
1. Segment the 18% "very disappointed" users — identify their behavioral patterns
2. Conduct 8–10 qualitative interviews with this cohort to identify the aha moment path
3. Run messaging experiments to test whether the core value is being communicated
   to the right audience before building any new features
```

---

### Example 2: GO — Consumer Productivity App

**Scenario:** A productivity app has been in public beta for 4 months. The founding team is debating whether to hire a growth engineer and launch a referral program.

**Trigger:** "Should we hire a growth team?" + "do we have product/market fit?"

**Process summary:**
- Survey sent to 400 active users; 310 responses
- Very disappointed: 52% | Somewhat disappointed: 31% | Not disappointed: 12% | N/A: 5%
- Retention curve: flattens at 41% at month 3, stable through month 6; compares favorably to consumer app benchmarks
- Verdict: GO

**Output excerpt from `pmf-readiness-verdict.md`:**
```
Verdict: GO
Score: 52% very disappointed (above 40% threshold)
Retention: Stable at 41% at month 3 — well above consumer mobile average of ~10%

Rationale: Both signals confirm must-have status. A majority of active users would
be significantly impacted by loss of the product. Retention curve has stabilized at
a competitive level. The product is ready for high-tempo growth experimentation.

Recommended next actions:
1. Proceed with referral program design (see: growth-referral-loop-designer)
2. Identify North Star metric before beginning growth experiments (see: north-star-metric-selector)
3. Re-run this gate if the product undergoes a significant pivot or new market entry
```

## References

Methodology sourced from:
- *Hacking Growth*, Ch. 2: "Determining If Your Product Is Must-Have" — Must-Have Survey (primary)
- *Hacking Growth*, Ch. 2: "Measuring Retention" — retention curve as second signal
- *Hacking Growth*, Ch. 2: "The Flameout of BranchOut" — premature scaling anti-pattern
- *Hacking Growth*, Ch. 2: "Getting to Must-Have" — remediation protocol

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Hacking Growth* by Sean Ellis and Morgan Brown.

## Related BookForge Skills

This skill is the foundation of the Hacking Growth skill set. Run it before these dependents:

- `clawhub install bookforge-north-star-metric-selector` — pick the growth equation variable that matters after PMF is confirmed
- `clawhub install bookforge-retention-phase-intervention-selector` — use the retention curve from this skill as the diagnostic starting point

Browse more: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
