---
name: retention-phase-intervention-selector
description: "Use this skill to diagnose which retention phase (initial / medium / long-term) is broken for a user cohort and select the RIGHT type of intervention for that phase — because retention tactics that work for week-1 users fail completely for month-6 users. Reads cohort retention data, classifies the phase using product-type benchmarks (mobile ~1 day, SaaS ~1 month, e-commerce ~90 days), identifies where the curve breaks, and prescribes phase-appropriate hacks: aha-moment optimization for initial, habit formation + variable rewards for medium, feature velocity + ongoing onboarding for long-term. Includes a resurrection branch for dormant users and flags the churn-masking-by-acquisition anti-pattern. Triggers when a growth PM asks 'users churn after the first week', 'our month 2 retention drops off a cliff', 'retention is bad but I don't know why', 'cohort analysis help', 'how do I improve retention', 'retention curve diagnosis', 'initial vs long-term retention', 'Balfour three-phase retention', 'habit formation', 'variable rewards Hooked', 'zombie users resurrection', 'win-back campaign', 'feature bloat', or 'churn hidden by acquisition'. Also activates for 'my DAU looks good but retention is bad', 'we're growing but churning', or 'retention-first growth'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/retention-phase-intervention-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [7]
tags:
  - growth
  - retention
  - cohort-analysis
  - habit-formation
  - startup-ops
depends-on:
  - product-market-fit-readiness-gate
  - north-star-metric-selector
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: >
        Retention cohorts CSV (retention-cohorts.csv) with weekly or monthly
        cohort retention data. Product brief (product-brief.md) to classify
        product type (mobile / SaaS / e-commerce / consumer).
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set + CSV. Produces retention-phase-diagnosis.md and
    retention-intervention-plan.md.
discovery:
  goal: >
    Produce a diagnosis that names which retention phase is broken, explains
    why, and prescribes phase-appropriate interventions — avoiding the common
    mistake of applying initial-retention tactics to a medium-retention problem.
  tasks:
    - "Read cohort data and product brief"
    - "Classify product type and corresponding phase boundaries"
    - "Plot the cohort retention curve"
    - "Identify which phase the curve breaks in"
    - "Check for churn-masked-by-acquisition anti-pattern"
    - "Prescribe phase-appropriate interventions"
    - "Check feature velocity for long-term cohorts (bloat risk)"
    - "Emit diagnosis and intervention plan"
---

# Retention Phase Intervention Selector

Diagnose which retention phase is failing for a cohort, then prescribe the interventions appropriate to that phase. The core insight: a week-1 drop-off and a month-6 decline have completely different root causes and require completely different treatments. Mixing them up wastes quarters of experiment cycles.

Research by Frederick Reichheld of Bain & Company found that a 5% increase in customer retention rates increases profits by 25 to 95 percent. Retention is not a vanity metric — it is a leverage point. But only if you know which lever to pull.

---

## When to Use

Use this skill when:

- A cohort analysis shows users are churning but you are not sure when or why
- Retention looks stable in aggregate but early cohorts are thinning out
- You are about to invest in retention experiments but have not diagnosed the phase
- A PM asks "should we improve onboarding, add features, or run win-back campaigns?" — the answer depends entirely on which phase is broken
- You suspect churn is being hidden by strong acquisition growth
- Long-term cohorts are declining despite high feature velocity

**Prerequisite signals:** Your product has cleared product-market fit (stable retention curve exists for at least one cohort segment). If the retention curve never stabilizes, run `product-market-fit-readiness-gate` first — this skill cannot fix a pre-PMF product.

---

## Context and Input Gathering

Before starting, collect:

1. **retention-cohorts.csv** — required. Weekly or monthly cohort retention table. Rows = cohort (e.g., "Jan 2024"), columns = periods after signup (Week 1, Week 2 ... or Month 1, Month 2 ...), values = percentage still active.
2. **product-brief.md** — required. Must state product type (mobile app / SaaS / e-commerce / consumer marketplace / other) and the North Star metric for retention. If missing, ask before proceeding — phase boundaries differ materially by product type.
3. **Optional:** churn survey data, exit interviews, user behavior event logs. These speed up root cause identification but are not blockers.

---

## Process

### Step 1 — Read cohort data and product brief

Read both input files. Extract:

- Product type (mobile / SaaS / e-commerce / other)
- Cohort time grain (weekly vs monthly)
- The raw retention percentages by cohort and period

**Why:** Phase boundaries are product-type-specific. Without knowing the product type, period labels ("Month 1") map to different phases. A Month 1 drop in a mobile app is medium-term. A Month 1 drop in a SaaS product is still initial. Getting this wrong causes the wrong intervention type.

---

### Step 2 — Classify product type and phase boundaries

Map the product type to phase boundary definitions:

| Product Type | Initial Phase Ends | Medium Phase Ends | Long-Term Begins |
|---|---|---|---|
| Mobile app | ~Day 1 | ~Week 2–4 | Month 1+ |
| Social network | ~Week 1–2 | ~Month 1–2 | Month 3+ |
| SaaS (subscription) | ~Month 1 or first quarter | ~Month 3–6 | Month 6 / Quarter 3+ |
| E-commerce | ~Day 90 (first 90 days) | ~Month 4–9 | Month 10+ / Year 2 |
| Consumer marketplace | ~Week 2 | ~Month 1–3 | Month 4+ |

These are reference benchmarks (sourced from Lean Analytics sector data and the Balfour three-phase model). Calibrate to your own cohort behavior: the initial phase ends where your churn rate begins to stabilize, not at a fixed calendar point.

**Why:** Applying a NUX optimization experiment to a 6-month cohort decline is a common and expensive mistake. The boundaries enforce discipline about what type of problem is being solved.

---

### Step 3 — Plot and read the retention curve

Construct the retention curve from the CSV. If no charting tool is available, build a text table:

```
Period:    W1    W2    W4    W8    W12   W16
Jan cohort: 68%  52%   41%   39%   38%   37%
Feb cohort: 71%  55%   44%   38%   35%   32%
Mar cohort: 65%  41%   29%   22%   19%   17%
```

Identify:

- **Steep early slope:** Large drop between Period 1 and Period 2–3 (relative to the phase boundaries established in Step 2)
- **Mid-curve inflection:** Curve was stabilizing then resumed decline after 4–8 periods
- **Slow long-term erosion:** Curve never fully stabilizes; continues declining across all measured periods
- **Cohort-to-cohort degradation:** Later cohorts retain worse than earlier cohorts at the same period — signals a product or onboarding regression, not a phase problem

**Why:** The shape of the curve tells you which phase is responsible. Reading curve shape is more diagnostic than reading a single retention number. Cohort-to-cohort degradation is a separate failure mode that must be flagged before prescribing interventions.

---

### Step 4 — Diagnose which phase is broken

Apply the following decision rules:

**Initial phase broken:**
- Steep drop in the first 1–3 periods (relative to product-type phase boundary)
- Majority of churn occurring within the initial window
- Curve never reaches a meaningful plateau
- *Interpretation:* Users are not experiencing core value. This is an activation-extension problem.

**Medium phase broken:**
- Reasonable initial retention (40%+) followed by a drop-off at weeks 4–12 (for mobile) or months 2–5 (for SaaS)
- Curve plateaus briefly, then resumes declining
- *Interpretation:* Users experienced value initially but did not form a habit. The product has not become a default choice.

**Long-term phase broken:**
- Good initial and medium retention but slow, sustained decline over months or quarters
- Early cohorts declining while newer cohorts still look healthy (cross-cohort comparison)
- Feature velocity is high but retention is not improving
- *Interpretation:* Existing power users are losing engagement. Feature bloat or lack of discovery of advanced capabilities is a likely cause.

**Resurrection candidate:**
- A meaningful fraction of a cohort is dormant (not active for N+ periods) but not formally churned
- These users represent a lower-cost re-acquisition opportunity than new user acquisition.

Document the diagnosis in one clear sentence: "The [cohort name] cohort shows [phase] phase failure, characterized by [specific curve observation], which indicates [root cause hypothesis]."

**Why:** Naming the phase locks in the intervention type before generating experiment ideas. Without this gate, teams generate a mix of initial- and long-term tactics and run them simultaneously, making it impossible to isolate what worked.

---

### Step 5 — Anti-pattern check: churn masked by acquisition

Before prescribing interventions, check whether aggregate metrics are hiding the cohort-level problem.

Compute: for the three oldest cohorts in the dataset, is the retention rate at their current period lower than it was at the same period for newer cohorts? If yes, early adopters are churning faster — and if overall user counts are stable or growing, new user volume is masking the defections.

Signal: total users are flat or growing, but the Jan and Feb cohorts are at 15% retention by Month 6 while the May cohort is at 38% at Month 2.

**If churn masking is detected:** Flag it explicitly in the diagnosis. It changes the urgency framing — the company's retention health is worse than aggregate metrics suggest, and the gap will widen as acquisition slows.

**Why:** Teams that skip this check continue to interpret stable DAU as a retention success. The cohort-level picture reveals compounding LTV damage that will not appear in top-line metrics until acquisition slows or stops.

---

### Step 6 — Prescribe phase-appropriate interventions

Select experiments from the appropriate intervention set:

#### If initial phase is broken → Aha-moment acceleration

The initial period is a prolonging of the activation experience. Interventions mirror activation tactics:

- **NUX audit:** Map every step from signup to first value experience. Identify friction points and steps where users drop without completing. Reduce or reorder steps that are not prerequisite to the aha moment.
- **Time-to-value compression:** Remove anything that delays the core experience. If account creation is mandatory before the user sees value, move it after.
- **Trigger calibration:** Deploy push notifications or emails only when behavioral signals indicate a user is returning but has not yet activated. Calibrate to Fogg's motivation × ability model — do not send triggers when motivation is low.
- **At-risk flagging:** Implement a heuristic threshold (e.g., did not return within first 3 days for a mobile app) to trigger a targeted re-engagement message within the initial window.
- **Cross-reference:** Run `activation-funnel-diagnostic` in parallel — initial retention and activation share root causes and experiment types.

#### If medium phase is broken → Habit formation and reward engineering

The goal is to make the product the default choice for the need it serves.

- **Engagement loop audit:** Map the current trigger → action → reward → investment cycle. Identify whether the reward is predictable (low engagement potential) or variable (higher engagement potential). Variable reward schedules sustain engagement by introducing unpredictability — the core mechanism described in Nir Eyal's Hook Model.
- **Tangible rewards:** Discounts, credits, savings programs. Effective for e-commerce and marketplaces. Test multiple reward types — cash equivalents are not always the strongest motivator.
- **Experiential and social rewards:** Status markers, exclusive access, social proof (showing what peers have done). Frequent-flier programs demonstrate that status and access retain better than fare discounts over the long term.
- **Commitment devices:** Features that make switching more costly — saved preferences, accumulated history, social connections, progress streaks. The more a user has invested, the higher the switching barrier.
- **Promise of future value:** Communicate upcoming improvements. For SaaS and content platforms, scheduled feature releases or content drops give users a reason to maintain the relationship. Netflix-style episodic release pacing is an extreme form of this.
- **Notification frequency experimentation:** Test minimum effective notification frequency. Over-triggering during the medium phase accelerates churn rather than preventing it.

#### If long-term phase is broken → Two-pronged feature strategy

Long-term retention requires both maintaining the existing experience and expanding it over time.

**Prong 1 — Optimize existing features:**
- Identify which features correlate with highest long-term retention (behavioral cohort analysis)
- Run experiments to increase discovery and adoption of those features among long-term cohorts
- Address UX friction that accumulates as users attempt advanced use cases

**Prong 2 — Introduce new features at a staged cadence:**
- Release new features to 5–10% of users first; collect behavioral and satisfaction data before broad rollout
- Avoid rapid sequential feature releases that overwhelm users
- Use ongoing onboarding (see Step 7) to guide users to new capabilities
- Feature releases tied to a predictable schedule (annual or semi-annual events) create anticipated value moments

**Why two prongs:** Long-term churn has two distinct drivers — diminishing returns from the current experience, and failure to discover new value. Optimizing existing features alone does not attract users back once they have mentally "finished" the product. New features alone create confusion without proper onboarding.

---

### Step 7 — Feature velocity check (long-term plans only)

If the diagnosis is long-term phase failure and the team has been shipping features at high velocity, run the feature bloat check:

**Detection criteria:**
- Feature release rate is high (>2 significant features per quarter) but long-term retention is not improving
- User interviews or survey data show confusion about product scope or difficulty finding relevant features
- Support volume or "how do I..." queries are rising

**If feature bloat is detected:** Recommend a feature audit. The Marketing Science Institute research (Thompson, Hamilton, Rust 2005) found that maximizing feature count for initial appeal decreases customer lifetime value — users are overwhelmed and the core value is obscured. The intervention is not more features but clearer progressive disclosure of existing ones.

**Why:** Feature velocity feels like progress. The feature bloat anti-pattern makes it possible to invest significant engineering effort in long-term retention experiments that actually make retention worse.

---

### Step 8 — Resurrection branch (dormant user segment)

If a meaningful percentage of a cohort is dormant (users who were active in an early period but have not been active for several periods, without having formally canceled):

1. **Do not lump dormant users into win-back campaigns immediately.** First, interview a sample (target: 5–10 interviews) to understand why they left.
2. Classify reasons as: controllable (e.g., device migration, forgot about the product, lost access) vs. uncontrollable (changed job, life event, moved away from the use case).
3. Design win-back experiments only around controllable reasons. Campaigns targeting uncontrollable churn waste budget and may generate negative brand signal.
4. Experiment formats: re-engagement email sequences, reactivation offers, cross-device installation prompts, milestone-triggered outreach ("It's been 60 days — here's what's new").
5. Track resurrection rate separately from new user acquisition — do not blend the two in retention dashboards.

**Why:** Dormant users already know the product, which makes them cheaper to reactivate than acquiring a new user from scratch. But win-back campaigns without root cause diagnosis have low conversion rates and can create a "desperate" brand perception if poorly calibrated.

---

### Step 9 — Emit outputs

Write two documents:

**retention-phase-diagnosis.md**
```
## Cohort Analyzed
[Cohort identifier, time grain, date range]

## Product Type and Phase Boundaries
[Product type → phase boundary table as applied to this product]

## Retention Curve Summary
[Text or table representation of curve shape]

## Phase Diagnosis
[Named phase: initial / medium / long-term / multiple]
[One-sentence characterization of curve behavior]
[Root cause hypothesis]

## Churn Masking Check
[Result: detected / not detected]
[Evidence if detected]

## Feature Bloat Check (long-term only)
[Result: risk present / not present]
[Evidence]

## Dormant User Population
[Percentage of cohort dormant, if applicable]
```

**retention-intervention-plan.md**
```
## Phase-Appropriate Interventions
[Ordered list of 5–8 specific experiments, each with:]
- Experiment name
- Hypothesis
- Target metric
- Implementation notes

## Resurrection Plan (if applicable)
[Interview protocol, win-back experiment candidates]

## Anti-Patterns to Avoid
[Churn masking / feature bloat warnings as applicable]

## Dependency Skills
[Links to activation-funnel-diagnostic, monetization-experiment-planner as appropriate]
```

---

## Key Principles

1. **Retention is phased — tactics do not transfer across phases.** NUX optimization applied to a month-6 cohort does not address why long-term users disengage. Diagnosis before prescription is non-negotiable.

2. **Cohort analysis is mandatory — point-in-time retention hides the pattern.** Aggregate DAU or monthly active users can be stable or growing while early cohorts are in decline. Always diagnose from the cohort curve, not the headline number.

3. **Acquisition hides churn — compute churn on a fixed cohort.** Strong new user growth masks early-adopter defections. A company can be losing its core users while total counts look healthy. Cohort-level churn must be tracked independently.

4. **Habit formation is not a trick — variable rewards work only for products that deserve habit.** The Hook Model works when the product genuinely solves a recurring need. Applying engagement loop mechanics to a product that does not merit repeat use accelerates churn by irritating users, not retaining them.

5. **Feature bloat is the long-term retention killer.** Adding features at high velocity maximizes initial appeal but decreases customer lifetime value. More features do not equal more retention unless they are discoverable and relevant to existing use cases.

6. **Resurrection is cheaper than new acquisition — but requires root cause first.** Win-back campaigns without understanding why users left have low conversion rates and poor brand optics. Interview before you campaign.

---

## Examples

### Example 1: Mobile app with initial phase broken

**Situation:** A fitness tracking app shows that 65% of new users are active on Day 1, but only 22% return on Day 7, and only 14% return on Day 14. The curve never plateaus.

**Product type:** Mobile app. Initial phase = Day 1. Medium phase = Days 2–14. Long-term = Week 3+.

**Diagnosis:** Initial phase failure. 78% churn within the first week indicates users are not reaching a meaningful experience of core value before disengaging. The curve's failure to plateau confirms there is no retained user segment.

**Churn masking check:** Total downloads growing 20% month-over-month, which was masking the cohort-level pattern in dashboard reviews.

**Interventions prescribed:**
- NUX audit: map from app install to first completed workout. Identify all steps that precede the first success moment. Remove mandatory account creation from before first workout.
- Day 3 trigger: if user has not completed a second workout by Day 3, send a contextual push notification tied to the user's first workout type.
- At-risk threshold: flag any user who has not returned by Day 2 for a targeted re-engagement sequence.
- Run `activation-funnel-diagnostic` to identify the specific funnel step with highest drop-off.

**Not prescribed:** Habit formation experiments, new feature development, or win-back campaigns — all medium- and long-term phase tactics.

---

### Example 2: SaaS product with medium phase broken

**Situation:** A project management SaaS shows 60% of Month 1 users still active in Month 2, but only 28% in Month 4 and 18% in Month 6. The initial drop is acceptable for a SaaS product; the Month 2–4 drop is steep.

**Product type:** SaaS. Initial phase = Month 1. Medium phase = Months 2–5. Long-term = Month 6+.

**Diagnosis:** Medium phase failure. Users are successfully onboarded (strong Month 1 retention) but are not forming a habit of returning. The tool is not yet their default project management environment.

**Churn masking check:** Not detected — new sales are flat, so the cohort-level pattern is visible in aggregate.

**Interventions prescribed:**
- Engagement loop audit: map what power users (top 10% by session frequency) do in Months 2–4 that new users do not. Identify the behavioral correlate of medium-term retention.
- Weekly digest email: summarize team activity from the prior week, sent Monday morning when motivation to plan is high. Trigger is behavioral (inactivity for 5+ days) not calendar-based.
- Collaboration prompt: prompt users to invite a second team member. Social investment (teammates' data is in the tool) raises switching costs.
- Promise of future value: send a "what's coming in Q3" product update to Month 2 cohorts. Creating anticipated value gives users a reason to maintain the subscription through a low-engagement period.

**Not prescribed:** NUX redesign (initial phase is healthy), feature bloat audit (feature velocity is not the issue at Month 2–4).

---

## References

- Balfour, Brian. "Growth Is Good, but Retention Is 4+Ever." Presentation, May 10, 2015.
- Eyal, Nir. *Hooked: How to Build Habit-Forming Products.* Portfolio/Penguin, 2014.
- Thompson, Debora Viana, Rebecca Hamilton, and Roland Rust. "Feature Fatigue: When Product Capabilities Become Too Much of a Good Thing." Marketing Science Institute, 2005.
- Reichheld, Frederick. "Prescription for Cutting Costs." Bain & Company report. Cited in: Ellis & Brown, *Hacking Growth*, Chapter 7.
- Croll, Alistair, and Benjamin Yoskovitz. *Lean Analytics.* O'Reilly Media, 2013. (Phase boundary benchmarks.)
- Ellis, Sean, and Morgan Brown. *Hacking Growth.* Crown Business, 2017. Chapters 6–7.

---

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Distilled from *Hacking Growth* by Sean Ellis and Morgan Brown. Source book is copyright of its respective authors. This skill contains no verbatim excerpts — only synthesized frameworks, process adaptations, and original analysis.

---

## Related BookForge Skills

- **product-market-fit-readiness-gate** — Run this first. Retention curve stability is the second PMF signal; this skill assumes PMF has been achieved.
  `clawhub install bookforge-product-market-fit-readiness-gate`

- **north-star-metric-selector** — Retention improvements need a single metric to optimize toward. Select the retention-appropriate North Star before designing experiments.
  `clawhub install bookforge-north-star-metric-selector`

- **activation-funnel-diagnostic** — Initial retention and activation share root causes. Run in parallel when initial phase failure is diagnosed.
  `clawhub install bookforge-activation-funnel-diagnostic`

- **monetization-experiment-planner** — The natural next step once retention is stable. Increasing lifetime value requires a retained user base first.
  `clawhub install bookforge-monetization-experiment-planner`
