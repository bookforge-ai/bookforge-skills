---
name: activation-funnel-diagnostic
description: "Use this skill to diagnose where in an activation funnel users drop off and decide between removing friction or adding 'positive friction' (guided steps) to fix it. Maps the route from signup to the aha moment (first core-value experience), builds a channel-segmented funnel conversion report from metrics data, identifies the highest-drop-off step, interprets user survey data at drop-off points, and emits an activation-funnel-diagnosis.md plus a ranked list of activation experiment candidates. Triggers when a growth PM asks 'why are users signing up but not coming back?', 'our activation rate is terrible', 'where are users dropping off in onboarding?', 'activation funnel audit', 'users don't reach aha moment', 'onboarding diagnosis', 'NUX problems', 'first-run experience broken', 'how do I find friction', 'should I simplify or guide my onboarding?', or 'help me diagnose my activation'. Also activates for 'funnel analysis', 'drop-off diagnosis', 'desire friction conversion', 'magic moment audit', 'Twitter 30 follows pattern', or 'Facebook 7 friends rule'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/activation-funnel-diagnostic
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [6]
tags:
  - growth
  - activation
  - onboarding
  - funnel-analysis
  - startup-ops
depends-on:
  - north-star-metric-selector
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: >
        Funnel metrics (funnel-metrics.csv) with step-by-step conversion counts.
        Activation flow doc (activation-flow.md) describing the current onboarding
        step-by-step. Optional: survey-responses.md with user feedback from
        drop-off points.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set + CSV data. Reads metrics and flow docs, produces diagnosis
    and experiment candidates as markdown.
discovery:
  goal: >
    Produce activation-funnel-diagnosis.md that names the highest-drop-off step,
    explains WHY users drop there, and recommends remove-friction vs add-positive-friction
    interventions with a ranked experiment list.
  tasks:
    - "Confirm the aha moment (first core-value experience)"
    - "Read funnel metrics CSV"
    - "Read activation flow doc"
    - "Build channel-segmented funnel conversion table"
    - "Identify highest drop-off step"
    - "Interpret why users drop (from survey data or infer)"
    - "Decide remove-friction vs add-positive-friction"
    - "Generate ranked experiment candidates"
    - "Emit diagnosis and experiment backlog"
---

# Activation Funnel Diagnostic

## When to Use

Use this skill when users are signing up but not coming back — the classic activation gap. Specifically run it when:

- Activation rate is unknown or known to be poor (industry baseline: 98% of website traffic never activates; up to 80% of mobile users churn within three days of install)
- Users reach signup but do not complete the first meaningful action
- You have step-level funnel metrics and want to know which step is bleeding users
- You are unsure whether to simplify onboarding (remove friction) or add guided steps (positive friction)
- Retention is suffering because users never experienced core value in the first session

**Prerequisite:** The aha moment must be defined. If it is not, run `north-star-metric-selector` first — the aha moment is the activation target, and diagnosing a funnel without knowing its destination produces useless results.

---

## Context and Input Gathering

Before starting, confirm you have or can locate:

| Input | Required | Expected Format |
|---|---|---|
| `funnel-metrics.csv` | Required | Columns: step_name, users_entered, users_completed, channel (optional) |
| `activation-flow.md` | Required | Prose or numbered list describing each onboarding step |
| `survey-responses.md` | Optional | User verbatim responses at drop-off points, or email/interview notes |
| Aha moment definition | Required | One sentence: the moment users first experience core product value |

If the aha moment is not confirmed, ask: "What is the single action or outcome that makes this product feel indispensable to a new user?" Do not proceed until you have an answer.

---

## Process

### Step 1: Confirm the aha moment

Ask the growth PM to state the aha moment in one sentence. If they cannot, surface a working hypothesis from the activation flow doc ("completing first X" or "seeing first Y") and ask them to confirm or correct it.

**Why:** The aha moment is the activation target — every funnel step is evaluated by how well it moves users toward that moment. Optimizing a funnel without a defined endpoint means you may be improving steps that lead nowhere near core value. The aha moment is defined through research; it is never assumed.

Typical aha moment patterns:
- SaaS tools: running a first meaningful task (first survey sent, first report generated, first deployment)
- Social products: connecting with enough people to see a relevant feed (Twitter: follow accounts across topics; Facebook: find and connect with friends)
- Marketplaces: completing first transaction on both sides
- Consumer apps: receiving a tangible result (order delivered, recommendation acted on)

---

### Step 2: Read the funnel metrics CSV

Open `funnel-metrics.csv`. Confirm columns are present: `step_name`, `users_entered`, `users_completed`. The `channel` column is optional but critical if present.

Compute for each step:
```
conversion_rate = users_completed / users_entered × 100
drop_off_count  = users_entered - users_completed
drop_off_rate   = 1 - conversion_rate
```

Flag any step where `drop_off_rate > 0.40` (over 40% of entering users do not complete the step) as a high-priority investigation point.

**Why:** Raw user counts obscure the conversion shape. Computing rates per step reveals where the funnel narrows most sharply. The highest drop-off step — not the first step, not the last — is the highest-leverage point for experimentation. Treating all steps equally wastes experiment budget on low-impact changes.

---

### Step 3: Read the activation flow doc

Read `activation-flow.md`. For each step in the funnel metrics, map it to the corresponding description in the flow doc. Note:

- Steps requiring user input (forms, uploads, searches)
- Steps requiring understanding of an unfamiliar concept
- Steps where the product's value is not yet visible to the user
- Steps that could be deferred or reordered

**Why:** Funnel data shows where users drop off; the flow doc shows what they are being asked to do at that point. The combination reveals the gap between what the product asks and what users are willing to do. A high drop-off rate on a "create account" step means something different than a high drop-off on "configure your first workflow" — the flow doc supplies the context that the CSV cannot.

---

### Step 4: Build the channel-segmented funnel conversion table

Construct a markdown table with steps as rows. If the `channel` column exists in the CSV, add columns for each channel. Compute per-channel conversion rates for each step.

```
| Step              | Overall Conv% | Organic | Paid | Referral | Social |
|-------------------|---------------|---------|------|----------|--------|
| App download      | 100%          | 100%    | 100% | 100%     | 100%   |
| Account created   | 68%           | 74%     | 51%  | 81%      | 62%    |
| First action      | 41%           | 48%     | 29%  | 57%      | 38%    |
| Aha moment        | 23%           | 31%     | 14%  | 38%      | 21%    |
```

Flag any channel-step combination where conversion is 2× worse than the channel average for that step. These are broken-channel signals.

**Why:** Averaging across channels hides broken acquisition paths. A paid channel that converts at half the rate of organic at the "first action" step indicates a language or expectation mismatch — the ad promised something the onboarding does not deliver. Fixing the onboarding for everyone does not solve a channel-specific mismatch; it dilutes the fix. Channel segmentation before diagnosis is not optional.

---

### Step 5: Identify the highest drop-off step

Name the single step with the highest absolute `drop_off_count`. This is the primary intervention target. If two steps are close, pick the one earlier in the funnel — fixing it compounds downstream.

State it explicitly:
- Step name
- Users entering vs. users completing
- Drop-off count and rate
- Position relative to aha moment (how many steps before core value?)

**Why:** The highest drop-off step represents the most users who gave up before experiencing the product's core value. Every user who drops here is a user the acquisition spend paid to reach but failed to convert. This step is where the diagnosis concentrates.

---

### Step 6: Interpret why users drop

Use two sources in priority order:

**Source A — Survey data (if available).** Read `survey-responses.md`. Look for recurring themes: confusion about what to do next, missing information, unexpected requirements, unclear value, distrust, technical problems. Cluster responses by theme. Do not project your own assumptions onto them.

High-signal question patterns to look for in the data:
- "What's the one thing that nearly stopped you from completing?" (asked of completers — they know what almost stopped them)
- "Is there anything preventing you from signing up at this point?"
- "What were you hoping to find on this page?"

**Source B — Structural inference (if no survey data).** Examine the flow doc description of the high-drop-off step. Ask:

- Does this step require users to provide significant information before seeing any value?
- Does this step introduce a concept users may not understand (product-specific jargon, unfamiliar workflow)?
- Is it unclear what happens after this step?
- Does this step involve trust or commitment (payment info, contact info, integrations)?
- Is the product's value visible before this step, or has the user been asked to invest effort with no payoff yet?

**Why:** Funnel data is behavioral; it shows that users drop, not why. Survey data is the only direct source of the reasoning behind behavior. Inferring from flow structure is second-best but necessary when survey data does not exist. The book's clearest lesson from the HubSpot Sidekick case: teams that assumed they understood drop-off causes (poor product education) ran 11 failed experiments. The real cause (users needed a trigger to act, not more explanation) only emerged from deeper data analysis and user feedback.

---

### Step 7: Apply the friction decision rule

Apply this formula to evaluate the drop-off step:

```
DESIRE – FRICTION = CONVERSION RATE
```

- **DESIRE** = the strength of the user's want for the product at this step. Proxied by: channel quality, landing page messaging match, user segment fit.
- **FRICTION** = the sum of impediments between the user and completing the step. Includes: form length, required information the user may not have at hand, unclear instructions, technical barriers, unfamiliar concepts, trust gaps.
- **CONVERSION RATE** = the observed output.

**Diagnosis routes:**

**Route A — Remove friction.** Apply when:
- Survey data or structural analysis shows confusion, overwhelm, or unexpected requirements
- Users are asked for information before experiencing any value
- The step involves a standard action (login, form completion) that competes with simpler alternatives
- There is high desire but users are blocked

Remove-friction tactics: single sign-on (Facebook/Google/LinkedIn login); fewer required fields; deferred account creation (let users start using the product before signing up); pre-filling known information; clearer copy and error messages.

**Route B — Add positive friction.** Apply when:
- Users can technically proceed but would not understand the product's value on arrival
- The product requires users to adopt an unfamiliar concept or behavior
- Users arrive with low context about how to use the product
- Structured guidance would create psychological commitment (once users take small actions, they are more inclined to continue)

Positive friction tactics: a learn flow — guided steps that show users what the product does while getting them to take small actions (interest selection, profile setup, first content creation); progress indicators; questionnaires that both collect data and create commitment; gamification (missions, milestones, earned rewards) where the rewards have clear relevance to core value.

**The counterintuitive rule:** More steps in onboarding is not always worse. Pinterest's addition of a topic-selection screen increased activation 20%. Twitter's learn flow — which required new users to follow accounts and set up a profile before arriving at a feed — produced users with a live feed on first visit instead of an empty one. The question is never "how many steps?" but "does each step help users arrive at the aha moment with greater confidence and context?"

**Why:** DESIRE and FRICTION are independent variables. A product with strong desire (early adopters, strong referrals) can tolerate high friction — users push through. A product reaching mainstream users or users who came through a lower-intent channel needs low friction at the exact same steps. The formula makes the diagnostic explicit: if desire is high and conversion is still low, friction is the problem. If desire is low, adding guided steps to help users understand value is the fix — removing friction alone will not help users who do not yet see why they should complete the step.

---

### Step 8: Generate ranked experiment candidates

Produce a ranked list of 3–6 experiment candidates targeting the highest-drop-off step. Each entry includes:

- **Experiment name:** short, descriptive
- **Hypothesis:** "If we [change], then [users_completing_step] will increase because [reason]"
- **Intervention type:** remove-friction or add-positive-friction
- **Implementation effort:** low / medium / high
- **Expected signal speed:** how quickly the experiment will produce measurable results

Prioritize low-effort, fast-signal experiments first. A simple copy change or form-field removal can be tested in days; a full learn flow redesign cannot. Start small — the HubSpot Sidekick team ran 11 failed experiments before finding the trigger message that moved the needle.

**Why:** An experiment list without prioritization creates a queue that teams work through in arbitrary order. Low-effort experiments run faster, generate learnings sooner, and compound. If a low-effort fix solves the problem, the high-effort rebuild was never needed. Ranking by effort and signal speed is the minimum viable prioritization for activation experiments.

For full experiment scoring (ICE: Impact × Confidence × Ease), pass the candidates list to `growth-experiment-prioritization-scorer`.

---

### Step 9: Emit deliverables

Write two files:

**`activation-funnel-diagnosis.md`** — contains:
1. Aha moment (confirmed)
2. Channel-segmented funnel conversion table
3. Highest drop-off step: name, users lost, rate
4. Why users drop (evidence from surveys + structural analysis)
5. Friction decision: remove-friction or add-positive-friction, with reasoning
6. DESIRE–FRICTION diagnosis for the target step

**`activation-experiment-candidates.md`** — contains:
- Ranked list of 3–6 experiment candidates with hypothesis, type, effort, signal speed
- Link to `growth-experiment-prioritization-scorer` for ICE scoring

**Why:** Two separate files keep the diagnosis (what is wrong and why) distinct from the experiment backlog (what to try). The diagnosis is a durable artifact that explains the current state; the experiment list is a working backlog that will change as experiments run. Keeping them separate prevents the team from treating hypotheses as diagnoses before they are tested.

---

## Key Principles

1. **The aha moment is defined, not assumed.** Diagnosing an activation funnel without a clear aha moment is optimizing toward an undefined goal. The aha moment comes from product research (must-have surveys, qualitative interviews) — not from guessing the most impressive-looking step in the onboarding flow.

2. **Segment before optimizing — channel averages hide broken channels.** A 30% average activation rate across channels may be a 50% rate in organic and 15% in paid. Fixing the onboarding for everyone does not fix the paid channel. Segmentation is not a nice-to-have; it determines whether your interventions are targeted or scatter-shot.

3. **Remove vs. add friction is a diagnostic decision, not a preference.** "Simplify everything" is a default, not a diagnosis. Sometimes more steps improve activation by ensuring users arrive at the aha moment with context and commitment. The question is always: why is this step causing drop-off — confusion/blocking (remove friction) or lack of context/commitment (add positive friction)?

4. **Positive friction is counterintuitive and often correct for new-concept products.** If your product asks users to adopt a new behavior or understand a novel concept, stripping all onboarding steps will produce users who arrive at core functionality with no idea what to do. Guided steps that teach and commit simultaneously — as Twitter's learn flow demonstrated — can generate higher activation than minimal-friction raw product access.

5. **Survey completers, not just abandoners.** People who passed a difficult step know what nearly stopped them. "What's the one thing that nearly stopped you from completing?" asked at the order confirmation or activation screen consistently produces higher response rates and more actionable qualitative data than exit surveys of people who left.

6. **Triggers must be tested, not assumed helpful.** Push notifications and email reactivation messages are among the most powerful and most abused activation tools. Deploy them only when the rationale is clear value to the user (a sale on a saved item, a relevant feature alert) — not to inflate short-term engagement statistics. Ask for notification opt-in only after users have experienced enough value to understand why they would want the messages. Test trigger timing, frequency, and copy as experiments, not as settled design.

---

## Examples

### Example 1: SaaS Tool with Empty-State Problem

**Situation:** A B2B analytics tool has 1,200 users sign up per month. Only 180 (15%) reach the aha moment (generating a first report). The team has funnel metrics but no survey data.

**Process summary:**
1. Aha moment confirmed: "user generates and views first analytics report"
2. Funnel metrics read: account creation (78%), workspace setup (61%), first data connection (42%), first report generated (15%)
3. Activation flow read: "first data connection" requires users to input API credentials or upload a CSV — no sample data available
4. Channel-segmented table built: paid search channel drops from 61% to 28% at "first data connection"; organic drops to 48%
5. Highest drop-off: "first data connection" — 490 users lost, 42% completion rate; paid search 2.2× worse than organic
6. Structural inference (no survey data): users are asked to provide credentials before seeing any product output; the product looks empty until connected; users arriving from paid ads may have lower intent than organic
7. Friction decision: **add positive friction** — the product requires users to set up before experiencing value; offer a sandbox dataset so users can generate a sample report before connecting real data
8. Experiments ranked: (1) add sample dataset for demo report — low effort, fast signal; (2) add progress bar showing "one step away from your first report" — low effort; (3) simplify API credential input form — medium effort; (4) add short video showing a completed report at the connection step — medium effort

**Output:**
- `activation-funnel-diagnosis.md`: confirms empty-state as root cause, paid channel mismatch, positive-friction recommendation
- `activation-experiment-candidates.md`: 4 experiments ranked by effort

---

### Example 2: Consumer App with Mid-Funnel Drop

**Situation:** A recipe and grocery app has 8,000 weekly installs. Funnel: app open (100%), browse items (72%), add to cart (48%), enter payment info (31%), first purchase (19%). Team has exit survey responses from users who reached the cart but did not purchase.

**Process summary:**
1. Aha moment confirmed: "user receives first grocery order as expected"
2. Funnel metrics read: steepest absolute drop is "add to cart → payment info" — 17% of all installs lost (1,360 users/week)
3. Activation flow read: payment info step requires new credit card entry and delivery address; no saved defaults; no indication of delivery fee until checkout summary
4. Channel-segmented table built: referral channel activates at 38% vs. paid social at 11% — large gap at payment step
5. Survey data analysis: top cluster (41% of responses) — users did not know whether delivery was free; second cluster (28%) — users forgot their first-order discount code
6. Friction decision: **remove friction** — users want the product (browse and cart rates are solid); specific information gaps are causing abandonment, not lack of understanding
7. Experiments ranked: (1) display delivery fee and first-order discount code automatically on cart page — low effort, addresses top two survey clusters; (2) simplify payment form with single sign-on (Google Pay/Apple Pay) — medium effort; (3) add delivery fee estimate earlier (browse screen) — low effort

**Output:**
- `activation-funnel-diagnosis.md`: payment-step friction identified, two specific causes from survey data, remove-friction recommendation
- `activation-experiment-candidates.md`: 3 experiments ranked, first two directly address surveyed reasons for abandonment

---

## References

- `references/activation-concepts.md` — aha moment definition, DESIRE–FRICTION=CONVERSION formula, positive friction definition, NUX principles, BJ Fogg behavior model
- `references/case-studies.md` — HubSpot Sidekick segmentation case, Airbnb sign-up prompt experiments, Twitter learn flow, Pinterest topic-selection onboarding, Qualaroo 50-response tipping point

---

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — BookForge Skills  
Source book: *Hacking Growth* by Sean Ellis and Morgan Brown. Skills distilled from book content under fair use for transformative educational purposes. See [BookForge copyright framework](https://github.com/bookforge-ai/bookforge/blob/main/docs/legal/copyright-framework.md).

---

## Related BookForge Skills

- `clawhub install bookforge-north-star-metric-selector` — defines the aha moment this skill uses as its activation target; run first if the aha moment is not confirmed
- `clawhub install bookforge-growth-experiment-prioritization-scorer` — apply ICE scoring (Impact × Confidence × Ease) to the experiment candidates this skill produces
- `clawhub install bookforge-retention-phase-intervention-selector` — initial retention is a continuation of activation; users who activated but do not return are a retention problem that begins at the activation boundary
- `clawhub install bookforge-product-market-fit-readiness-gate` — if activation rates are catastrophically low across all channels and positive-friction experiments fail, the product may not yet be must-have; this gate diagnoses whether product work should precede growth work
