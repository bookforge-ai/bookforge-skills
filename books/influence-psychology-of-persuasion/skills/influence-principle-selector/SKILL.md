---
name: influence-principle-selector
description: |
  Identify which of Cialdini's 6 influence principles to apply for a persuasion scenario. Use when someone asks "which persuasion tactic should I use?", "how do I make this more persuasive?", "what's the best influence strategy for this situation?", or "which Cialdini principle applies here?" Also use for: persuasion audit of marketing copy, sales email, or landing page; choosing between reciprocity vs scarcity vs social proof for a campaign; mapping a persuasion scenario to compliance psychology; diagnosing why content isn't converting; identifying influence tactics being used against you in a negotiation; evaluating ethical boundaries of a persuasion approach. Applies Cialdini's master taxonomy of 6 principles (reciprocity, commitment, consistency, social proof, liking, authority, scarcity) plus contrast principle and cross-principle interaction rules to produce a scored, rationale-backed recommendation. Classifies practitioners as ethical (real evidence) vs exploitative (manufactured triggers). Works on marketing strategy, sales psychology, copywriting, product onboarding, negotiation briefs, and any compliance scenario.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/influence-psychology-of-persuasion/skills/influence-principle-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: influence-psychology-of-persuasion
    title: "Influence: The Psychology of Persuasion"
    authors: ["Robert B. Cialdini"]
    chapters: [1]
tags: [persuasion, influence, cialdini, reciprocity, commitment, consistency, social-proof, liking, authority, scarcity, marketing-psychology, sales-psychology, compliance, persuasion-audit, influence-tactics, ethical-persuasion, contrast-principle]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Persuasion scenario or marketing content to analyze — a situation brief, marketing copy, sales email, landing page text, or any persuasive communication"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Works with pasted text or document files."
discovery:
  goal: "Identify the optimal influence principle(s) for a given persuasion scenario and produce an actionable recommendation with rationale"
  tasks:
    - "Score all 6 principles against a persuasion scenario"
    - "Identify cross-principle interactions and stacking opportunities"
    - "Evaluate ethical boundaries of proposed influence approach"
    - "Produce a ranked recommendation with application guidance"
    - "Audit existing content for principle usage and gaps"
  audience:
    roles: ["marketer", "salesperson", "copywriter", "product-manager", "negotiator", "entrepreneur", "UX-designer", "consultant"]
    experience: "any — no psychology background required"
  triggers:
    - "User describes a persuasion or sales scenario and wants to know which principle to apply"
    - "User has marketing copy, a sales email, or a landing page and wants it more persuasive"
    - "User wants to audit content for compliance with influence principles"
    - "User is in a negotiation and wants to understand the influence dynamics"
    - "User wants to diagnose why their marketing isn't converting"
    - "User has identified a Cialdini principle mentioned and needs help applying it"
  not_for:
    - "Building individual principle tactics in depth — use the dedicated principle skills (reciprocity-strategy-designer, scarcity-framing-strategist, etc.)"
    - "Executing persuasion (writing copy, sending emails) — this skill selects the principle; execution skills implement it"
    - "Defending against manipulation — use influence-defense-analyzer"
---

# Influence Principle Selector

## When to Use

You have a persuasion scenario — a marketing campaign, sales email, landing page, product launch, negotiation, or onboarding sequence — and need to identify which of Cialdini's 6 influence principles to apply, and in what combination.

This is the hub skill. Use it when you need principle selection and rationale. Once you have your recommendation, hand off to the dedicated principle skill (e.g., `reciprocity-strategy-designer`, `scarcity-framing-strategist`) for detailed implementation.

**Do not use this skill if:** You already know which principle applies and need implementation tactics. Go directly to the relevant principle skill.

---

## Context & Input Gathering

Before running the scoring process, collect:

### Required
- **The scenario:** What is the persuasion situation? (Cold outreach? Conversion page? Negotiation? Retention campaign?)
- **The audience:** Who is being persuaded? What do they want, fear, or value?
- **The goal:** What specific action or decision do you want the audience to take?
- **Your relationship to the audience:** First contact? Existing relationship? Warm referral?

### Important
- **What evidence you have:** Do you have real testimonials, genuine scarcity, actual credentials? (This determines ethical applicability of each principle.)
- **The medium:** Email, landing page, in-person pitch, ad copy, product UI?
- **Previous interactions:** Has the audience already taken any prior action or commitment?

### Optional (improves scoring precision)
- **Existing content:** If auditing existing copy, provide the text.
- **Competitor context:** Are you entering a crowded space or establishing a new category?
- **Conversion data:** If you have metrics, they can identify which principles are underperforming.

If required context is missing, ask for it before proceeding. A principle recommendation without audience and goal context is unreliable.

---

## Process

### Step 1: Map the Scenario to Principle Conditions

**Action:** Analyze the scenario against each principle's optimal activation conditions. Identify which conditions are present naturally vs. which would need to be created.

**WHY:** Each of the 6 principles activates through a specific trigger condition — a feature in the situation that fires the automatic compliance response. Some features may already exist in your scenario (e.g., you have genuine testimonials → social proof is ready to deploy). Others may need to be constructed (e.g., you need to establish a prior commitment before using consistency). Knowing which conditions are present vs. absent determines which principles are immediately available vs. which require setup.

Score each principle 1–5:
- **5** — All trigger conditions present. Real evidence exists. Strong fit.
- **4** — Most conditions present. Minor element missing; principle applies with small adjustments.
- **3** — Partial fit. Would need to set up conditions before deploying principle (e.g., create a commitment first).
- **2** — Key condition absent or scenario contradicts principle requirements.
- **1** — Principle does not fit scenario. Forcing it would be artificial or unethical.

See `references/principle-comparison-matrix.md` for the full activation condition checklist per principle.

---

### Step 2: Score Each Principle

**Action:** Run the scoring rubric against all 6 principles. Produce a score and a one-sentence rationale for each.

**WHY:** Scoring all 6 — not just the obvious one — prevents premature convergence on familiar principles (most practitioners default to scarcity or social proof). Running the full set often surfaces a high-scoring principle that was overlooked. The rubric also surfaces ethical flags: if the only way to score a principle highly requires manufacturing fake evidence, that is a clear signal to deprioritize it.

**Scoring template:**

```
Reciprocity:     [1-5] — [one-sentence rationale]
Commitment:      [1-5] — [one-sentence rationale]
Social Proof:    [1-5] — [one-sentence rationale]
Liking:          [1-5] — [one-sentence rationale]
Authority:       [1-5] — [one-sentence rationale]
Scarcity:        [1-5] — [one-sentence rationale]
```

---

### Step 3: Identify the Optimal Conditions and Sequencing

**Action:** For each principle scoring 3 or above, determine: (a) what makes it applicable now, and (b) if it scores 3 (setup required), what would need to happen first.

**WHY:** Sequencing matters enormously. Scarcity is far more powerful if commitment has been established first (Christmas toy tactic). Social proof is far stronger when the audience is uncertain. Authority suppresses skepticism before other principles are applied. Knowing the right sequence turns a mediocre single-principle approach into a layered strategy that compounds.

Key sequencing rules:
- **Commitment before Scarcity:** Establish desire/commitment first, then apply time/quantity pressure. Reverse order is weak.
- **Reciprocity before Request:** Give value before asking. Never reverse.
- **Authority before Technical Claims:** Establish credibility before making claims that require expertise.
- **Social Proof under Uncertainty:** Most powerful when the audience doesn't know what's normal or correct.
- **Contrast before Price:** Present expensive anchor before the actual price.

---

### Step 4: Check Cross-Principle Interactions

**Action:** Identify any stacking opportunities or interaction effects between the top-scoring principles. Flag any known interactions from the cross-principle map.

**WHY:** Principles interact — they can amplify or override each other. A practitioner who knows only individual principles misses the compounding effects. Reciprocity overrides liking (a cold prospect who received genuine value will comply even without rapport). Commitment plus scarcity stacks multiplicatively. Social proof amplifies any principle in uncertain situations. Identifying interactions turns a single-principle strategy into a layered one with compounding effect.

Check for:
- **Stacking opportunities:** Top 2–3 principles present simultaneously? (e.g., Tupperware: all 6)
- **Override effects:** Does one principle (especially reciprocity) make another unnecessary or redundant?
- **Sequencing dependencies:** Does one principle need to fire before another will work?
- **Contrast amplification:** Can contrast framing make any of the top principles hit harder?

---

### Step 5: Evaluate Ethical Boundaries

**Action:** For each recommended principle, verify that the trigger evidence is real — not manufactured, falsified, or misrepresented.

**WHY:** The 6 principles work because they tap normally-reliable decision shortcuts. When triggers are real, using them is legitimate persuasion — you're helping the audience make a correct decision efficiently. When triggers are manufactured (fake scarcity, paid testimonials presented as organic, fake credentials), you corrupt a shortcut that the audience depended on for accurate decisions. This causes harm beyond the individual interaction — it degrades the reliability of shortcuts that everyone uses. Ethically, it's also a liability risk.

Classify each recommended principle:

| Principle | Real evidence? | Classification |
|-----------|---------------|----------------|
| [Principle] | [Yes/No — describe] | Fair practitioner / Exploitative |

**Classification rule:**
- All trigger evidence is real → Fair practitioner. Proceed.
- Any trigger evidence is manufactured, falsified, or misrepresented → Exploitative. Revise or remove.

If a high-scoring principle requires fake evidence to activate, flag it explicitly and recommend the next-highest scoring principle with real evidence instead.

---

### Step 6: Produce the Recommendation

**Action:** Write a structured recommendation covering the top 1–3 principles, the recommended sequence, cross-principle interactions to exploit, and application guidance.

**WHY:** A ranked recommendation with explicit rationale enables confident decision-making. Surfacing the runner-up principle and why it was ranked lower prevents second-guessing. Including the sequence ensures the practitioner deploys principles in the order that maximizes effect — not just which principle, but when.

**Output format:**

```
## Influence Principle Recommendation

### Primary Principle: [Name] (Score: X/5)
**Why:** [1–2 sentences connecting activation conditions to scenario]
**Trigger to use:** [The specific feature to present]
**Application:** [1–2 concrete steps]
**Ethical check:** Fair practitioner — [real evidence available]

### Secondary Principle: [Name] (Score: X/5)
**Why:** [rationale]
**Sequence note:** [When to deploy relative to primary]
**Application:** [steps]

### Stacking Opportunity: [If applicable]
**Interaction:** [Which principles amplify each other and how]
**Recommended sequence:** [Order of deployment]

### Contrast Principle: [If applicable]
**Anchor:** [What to present first to create favorable contrast]

### Ruled Out: [Principle] (Score: X/5)
**Why not:** [Reason — missing condition, setup cost too high, or ethical flag]

### Next Step
→ Use [specific principle skill] to implement the primary recommendation.
```

---

## Inputs / Outputs

### Inputs
- Persuasion scenario description (required)
- Target audience profile (required)
- Goal / desired action (required)
- Existing content to audit (optional)
- Evidence inventory (testimonials, credentials, scarcity data) (optional)

### Outputs
- Scored principle ranking (all 6 scored)
- Structured recommendation with primary and secondary principles
- Sequencing guidance
- Cross-principle stacking opportunities
- Ethical classification
- Pointer to next-step principle skill

---

## Key Principles

**All 6 principles operate on the same mechanism.** Each one activates an automatic compliance response by presenting a single trigger feature. The feature causes the audience to reach a "yes" decision without full analysis. This is why shortcuts are powerful — and why they can be exploited. Understanding the mechanism (not just the label) helps you select the right one for your situation.

**The trigger condition — not the principle name — drives effectiveness.** Naming "scarcity" is not enough. Scarcity works when items are genuinely limited, newly scarce (not always scarce), and ideally under competition. Missing any of these conditions reduces effectiveness sharply. Always trace back to the trigger condition.

**Reciprocity is force-independent.** Unlike liking or authority, reciprocity obligation persists even when the recipient dislikes or distrusts the giver. This makes it the most reliable principle for cold interactions where no relationship exists yet.

**Stacking compounds compliance.** Principles applied in combination are not additive — they are multiplicative. The Tupperware party deploys all 6 simultaneously. Even 2–3 well-chosen, sequenced principles dramatically outperform any single principle alone.

**Contrast is a framing amplifier, not a principle.** The contrast principle (present expensive before cheap, hostile before reasonable) is not one of the 6 — it is a perceptual mechanism that can amplify any of them. Always check whether contrast framing can increase the impact of your primary principle.

**Ethical use requires real triggers.** Fair practitioners use real evidence (genuine scarcity, authentic testimonials, actual credentials). Exploitative practitioners manufacture fake triggers. The ethical test is simple: is the trigger feature true? Using real triggers is legitimate — you help the audience make a correct decision efficiently. Fake triggers corrupt a cognitive shortcut the audience relied on.

---

## Examples

### Example 1: SaaS Product Launch Email Campaign

**Scenario:** A B2B SaaS product is launching. The team wants to convert 200 beta users to paid. They have: 10 existing paying pilot customers who love the product, genuine limited launch pricing (first 50 seats at 40% off), and a credentialed founding team (ex-Google, Stanford PhD).

**Trigger:** "We have a launch email going out next week. How do we make it more persuasive?"

**Process:**
- Step 1: Conditions present — real testimonials (social proof ready), real limited pricing (scarcity ready), real credentials (authority ready), existing relationship from beta (liking/familiarity ready)
- Step 2: Scarcity=5, Social Proof=5, Authority=4, Commitment=3 (setup possible via free trial commitment), Liking=3, Reciprocity=2
- Step 3: Deploy Authority first (credibility reduces skepticism), then Social Proof (reduce uncertainty), then Scarcity (motivate action now)
- Step 4: Social Proof amplifies Scarcity when others are competing for limited seats
- Step 5: All triggers real — fair practitioner classification

**Output:**
```
## Influence Principle Recommendation

### Primary Principle: Scarcity (Score: 5/5)
Why: Launch pricing is real, genuinely limited to 50 seats, and time-bound.
Trigger: "First 50 seats at launch pricing — 23 remaining as of today."
Application: Show a counter or real number; update it. Combine with deadline.
Ethical check: Fair practitioner — pricing tier is real, seat count is genuine.

### Secondary Principle: Social Proof (Score: 5/5)
Why: 10 paying pilot customers with results provide authentic peer evidence.
Sequence: Lead with social proof before scarcity — first establish "this works
for people like you," then motivate urgency.
Application: Quote 2–3 pilot customers with specific results in the email body.

### Stacking: Social Proof + Scarcity
Interaction: Others competing for limited seats amplifies scarcity response.
Sequence: [1] Authority (founding team) → [2] Social Proof (pilot results) → [3] Scarcity (limited seats)

### Authority (Score: 4/5)
Sequence: Open with founding team credentials — one sentence.
Purpose: Suppress initial skepticism so social proof lands more strongly.

→ Next step: Use scarcity-framing-strategist for launch pricing copy.
   Use social-proof-optimizer for testimonial selection and placement.
```

---

### Example 2: Negotiation — Enterprise Sales Close

**Scenario:** Enterprise sales rep is in final negotiation. The prospect has been evaluating for 3 months, has participated in 2 demos and a pilot, and is comparing to one competitor. Procurement wants a 15% discount the rep cannot give.

**Trigger:** "How do I handle the discount request and close this deal?"

**Process:**
- Step 1: Conditions — 3-month evaluation = strong commitment foundation, pilot = effortful commitment, no discount room but can offer value concessions
- Step 2: Commitment=5 (effortful prior investment is a major consistency anchor), Reciprocity=4 (concession exchange possible via door-in-the-face), Scarcity=3 (end-of-quarter pricing), Authority=3, Social Proof=2, Liking=3
- Step 3: Lead with Commitment (their 3-month investment creates consistency pressure), use Reciprocity via strategic concession (not discount — offer added value), apply Contrast before the concession (frame what they lose by not proceeding)
- Step 4: Commitment makes departure psychologically costly; Contrast frames the alternative as inferior; Reciprocity makes the value concession feel like a real give

**Output:**
```
## Influence Principle Recommendation

### Primary Principle: Commitment/Consistency (Score: 5/5)
Why: Three months of evaluation, two demos, and a completed pilot are all
active, effortful commitments that create strong consistency pressure.
Trigger: "You've invested three months validating this. The pilot confirmed X."
Application: Explicitly name the prior investment; connect it to the decision.

### Secondary Principle: Reciprocity — Door-in-the-Face (Score: 4/5)
Why: Cannot offer price discount but can make a value concession that feels
substantive. Offer something real (extended onboarding, dedicated CSM, extra
seats) as a give — not a discount. The concession creates reciprocity obligation.
Sequence: After anchoring commitment, make the value offer as a concession.

### Contrast Framing
Anchor: Frame the competitor alternative first — highlight what they'd lose
in switching costs, implementation time, feature gaps. Then present your offer.
Effect: Your terms appear more favorable after the competitor contrast.

### Ruled Out: Social Proof (Score: 2/5)
Why not: Procurement at this stage is not uncertain — they've evaluated.
Social proof would feel irrelevant to a procurement conversation about price.

→ Next step: Use commitment-escalation-architect for the specific framing.
```

---

### Example 3: Persuasion Audit — Landing Page Not Converting

**Scenario:** A landing page for a premium online course ($997) has a 1.2% conversion rate. The page has: a course description, instructor bio, curriculum list, and pricing. No testimonials, no enrollment deadline.

**Trigger:** "My landing page isn't converting. What influence principles am I missing?"

**Process:**
- Step 1: Page audit — social proof absent (no testimonials, no student count), scarcity absent (no deadline or limit), authority present but thin (bio exists but lacks specific credentials), commitment absent (no lead magnet or low-friction entry), reciprocity absent (no free value offered)
- Step 2: Social Proof=1 (missing, has no evidence to support), Scarcity=1 (missing), Authority=3 (bio present but underbuilt), Reciprocity=2 (nothing given before the ask), Commitment=2 (no entry point), Liking=3 (instructor voice could be stronger)
- Step 3: Biggest gap is social proof — uncertainty is high at $997, and there's no peer evidence. Second gap is scarcity — no urgency to act now.
- Step 5: All would require real evidence — need to collect genuine testimonials before adding social proof

**Output:**
```
## Influence Principle Audit: Landing Page

### Critical Gap 1: Social Proof (Current Score: 1/5)
Why missing: No testimonials, no student count, no case results.
At $997, uncertainty is high — this is exactly when social proof is most needed.
Fix: Collect 3–5 student testimonials with specific outcome results. Add enrollment
count ("1,200 students enrolled"). A/B test a results-focused testimonial above the fold.
Ethical check: Must use genuine testimonials — do not fabricate.

### Critical Gap 2: Scarcity (Current Score: 1/5)
Why missing: No enrollment window, no seat limit, page is always open.
Fix: Create a real enrollment period (cohort-based intake, or limited seats per month).
Do not manufacture fake countdown timers if enrollment never actually closes.
Ethical check: Scarcity must be real. If it's not, do not add it.

### Improvement: Authority (Current Score: 3/5 → target 5/5)
Current: Bio exists but generic.
Fix: Add specific credentials, outcomes delivered, named clients or publications.
Add a short video to increase familiarity and liking simultaneously.

### Quick Win: Reciprocity (Score: 2/5 → target 4/5)
Fix: Offer a free lesson, worksheet, or mini-course before the main ask.
This creates obligation before the purchase decision and demonstrates quality.

→ Next step: Use social-proof-optimizer for testimonial collection and placement.
   Use scarcity-framing-strategist if enrollment windows can be made real.
```

---

## References

| File | Contents |
|------|----------|
| `references/principle-comparison-matrix.md` | Full 6-principle activation condition checklists; scoring rubric; cross-principle interaction map; scenario-to-principle routing guide; ethical boundary checklist; case study breakdowns (Tupperware, Good Cop/Bad Cop, Christmas toy tactic) |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Influence: The Psychology of Persuasion by Robert B. Cialdini.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
