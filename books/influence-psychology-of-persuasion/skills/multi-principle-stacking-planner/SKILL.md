---
name: multi-principle-stacking-planner
description: |
  Design a layered persuasion campaign by combining 2–4 Cialdini influence principles in the right sequence. Use when someone asks "how do I combine influence principles?", "what's the best stacking order for my campaign?", "I want to use reciprocity AND scarcity — in what order?", or "how do I build a multi-touch persuasion sequence?" Also use for: designing a launch funnel that layers social proof onto scarcity, building a sales sequence that converts cold leads to committed buyers, creating an in-person event with maximum compliance architecture, auditing a multi-step campaign for principle interaction errors, planning a persuasion sequence for high-ticket or complex sales. Applies Cialdini's documented stacking patterns (Tupperware, Christmas toy tactic, Good Cop/Bad Cop, Regan override study) plus derived interaction rules — which principles amplify each other, which override each other, and which must be sequenced in a specific order. Covers: principle interaction rules, stacking sequences, contrast amplification, structural amplifiers, and ethical stacking thresholds. Outputs a sequenced campaign plan with WHY reasoning for each layer. Depends on influence-principle-selector (for principle scoring) and all 6 principle skills (for per-principle implementation). Best for experienced marketers, campaign strategists, and sales leaders working on multi-touch sequences, launch funnels, or complex sales architectures.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/influence-psychology-of-persuasion/skills/multi-principle-stacking-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - influence-principle-selector
  - reciprocity-strategy-designer
  - commitment-escalation-architect
  - social-proof-optimizer
  - liking-factor-engineer
  - authority-signal-designer
  - scarcity-framing-strategist
source-books:
  - id: influence-psychology-of-persuasion
    title: "Influence: The Psychology of Persuasion"
    authors: ["Robert B. Cialdini"]
    chapters: [2, 3, 4, 5, 6, 7]
tags: [persuasion, multi-principle, stacking, combining, campaign-strategy, sales-funnel, multi-touch, persuasion-sequence, layered-influence, campaign-architecture, influence-principles, reciprocity, commitment, social-proof, liking, authority, scarcity, contrast, cialdini, compliance-architecture]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Campaign brief, sales funnel plan, multi-touch sequence, or persuasion scenario description — any document describing a multi-step or multi-channel persuasion effort"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Document sets — campaign plans, sales funnel specs, multi-touch email sequences, launch plans. Works with any agent environment."
discovery:
  goal: "Design a sequenced multi-principle persuasion campaign that applies documented stacking patterns and interaction rules to compound compliance effect across multiple touchpoints"
  tasks:
    - "Score and select 2–4 principles appropriate for the campaign"
    - "Apply interaction rules to determine which principles amplify, override, or depend on each other"
    - "Design the stacking sequence — which principle fires first, second, third"
    - "Check ethical boundaries — consent, proportionality, real vs. manufactured triggers"
    - "Produce a sequenced campaign plan with per-layer WHY reasoning"
  audience:
    roles: ["marketer", "campaign-strategist", "sales-leader", "product-manager", "growth-lead", "founder"]
    experience: "experienced — audience already understands individual Cialdini principles; this skill adds cross-principle interaction logic"
  triggers:
    - "User has a multi-touch campaign and wants to layer influence principles across touchpoints"
    - "User wants to build a launch funnel with maximum compliance architecture"
    - "User is designing a sales sequence and wants to know the correct principle order"
    - "User has already selected principles and needs help with sequencing and interaction rules"
    - "User wants to audit an existing funnel for stacking errors or missed amplification opportunities"
  not_for:
    - "Selecting which single principle to use — use influence-principle-selector"
    - "Implementing a specific principle in detail — use the dedicated principle skill"
    - "Defending against manipulation — use influence-defense-analyzer"
    - "Single-touchpoint persuasion — this skill adds value when there are 2+ steps or stages"
---

# Multi-Principle Stacking Planner

## When to Use

You have a multi-touch campaign, sales funnel, or persuasion sequence — and you want to layer 2–4 Cialdini principles to compound compliance effect across multiple interactions.

Single-principle strategies are limited. The Tupperware party deploys all six simultaneously. The Christmas toy tactic stacks commitment and scarcity across two months. Good Cop/Bad Cop combines contrast, reciprocity, and liking in a single interrogation session. The compounding happens because principles interact — some amplify each other, some must be sequenced in a specific order, some override each other entirely.

This skill provides the interaction rules and sequencing logic. It does not replace the individual principle skills — it tells you which principles to combine, in what order, and why.

**Do not use this skill if:** You need to select which single principle to use. Use `influence-principle-selector` first, then return here if stacking is warranted.

---

## Context and Input Gathering

Before running the stacking process, collect:

### Required
- **Campaign goals:** What is the desired action at the end of the sequence? (Purchase? Meeting booked? Subscription? Commitment to next step?)
- **Audience profile:** Who is being persuaded? Relationship to them? (Cold lead, warm prospect, existing customer?)
- **Number of touchpoints:** How many interactions or stages does this sequence have?
- **Evidence inventory:** What real evidence do you have? (Genuine testimonials, actual credentials, real scarcity, authentic peer behavior?)

### Important
- **Campaign type:** Launch, ongoing nurture, event, single-session sales conversation, or long sales cycle?
- **Highest-value principles already identified:** If you have run `influence-principle-selector`, bring those scores here.
- **Medium:** Email sequence, event, landing page series, in-person sales, social campaign, or mixed?

### Optional
- **Existing campaign draft:** If auditing an existing sequence, provide the touchpoint plan.
- **Competitor context:** Are you stacking in response to a competitor's persuasion architecture?

If required context is missing, ask before proceeding. Stacking decisions without audience and evidence context produce generic sequences rather than compounding architectures.

---

## Process

### Step 1: Define Campaign Goals and Score Applicable Principles

**Action:** Identify the campaign goal and target action. Score all 6 principles for applicability (1–5 scale). Select the 2–4 highest-scoring principles with real evidence available.

**WHY:** Stacking amplifies whichever principles you choose — but stacking weak principles does not produce strong results. Start with the highest-scoring principles for your specific situation. The 4-principle ceiling is practical: above 4 principles, the sequence becomes unmanageable and each principle receives insufficient development. The Tupperware party achieves all 6 because the format is specifically engineered for it; most campaigns achieve maximum effect with 3–4.

Use the scoring template from `influence-principle-selector` (Step 2) if you have not already scored principles. If scores are already available, bring them directly to Step 2.

**Minimum threshold for inclusion:** Score ≥ 3 (partial fit with real evidence) to include a principle in the stack. Below 3, the principle requires setup investment that exceeds its return in a multi-principle context.

---

### Step 2: Apply Interaction Rules

**Action:** For each pair of selected principles, check the interaction rules from `references/principle-interaction-matrix.md`. Identify: (a) which principles amplify each other, (b) which have sequential dependencies, (c) which override each other.

**WHY:** Principles do not simply add together — they interact. Deploying Scarcity before Commitment is established produces urgency that evaporates when the deadline passes; deploying Commitment first then Scarcity creates durable obligation that persists. Deploying Reciprocity alongside Liking is redundant — Reciprocity overrides Liking entirely for compliance. Knowing the interactions prevents wasted investment and prevents anti-patterns that reduce effect.

Key interaction rules to check for every stack:

**Override check:**
- Reciprocity + Liking → If both selected, Reciprocity makes Liking redundant for compliance. Keep Liking as a structural condition (relationship warmth) rather than a sequential step. Drop it as an active principle if Reciprocity is primary.

**Sequential dependency check:**
- Commitment → Scarcity: Commitment must always precede Scarcity. If both are in the stack, verify Commitment has an activation stage before the Scarcity stage.
- Authority → Social Proof (or other principles): Authority deployed first suppresses skepticism, making all subsequent claims land with less resistance.
- Uncertainty source → Social Proof: Social Proof is most potent after uncertainty is raised. If Social Proof is in the stack, confirm a prior stage creates uncertainty (Authority challenging the status quo, problem framing, or competitor comparison).

**Amplification opportunities:**
- Contrast (not a principle — a framing mechanism): Check whether contrast framing can amplify the primary principle. Present the expensive/negative/extreme anchor before your actual offer. This works for any principle, costs nothing, and is frequently missed.
- Liking as structural amplifier: If any touchpoint passes through a trusted intermediary (referral, partner, existing relationship), mark it as a Liking-amplified touchpoint. Every principle hit through a trusted source achieves higher compliance.

---

### Step 3: Design the Stacking Sequence

**Action:** Order all selected principles into a stacking sequence for the campaign. Assign each principle to a campaign stage or touchpoint. Write the WHY for each placement decision.

**WHY:** Sequencing is where stacking becomes strategy rather than coincidence. The Tupperware party achieves all six principles in a fixed order because the sequence is engineered: value-first (reciprocity) creates obligation before any ask, public commitment amplifies consistency pressure before buying begins, social proof builds during the purchase phase, scarcity closes. A different order would produce lower compliance at each stage.

**Sequence construction rules:**
1. **Reciprocity always opens** in cold or new-relationship contexts. Give before you ask.
2. **Commitment comes before Scarcity.** Scarcity deployed before commitment is established is temporary pressure that resolves when the deadline passes.
3. **Authority opens before technical or performance claims.** Establish credibility before making claims that require expertise.
4. **Social Proof follows uncertainty.** Raise a problem or challenge first; then resolve it with peer evidence.
5. **Scarcity closes.** Scarcity is the urgency mechanism — it motivates action on an already-established desire. Deploying it before desire is established creates pressure without direction.
6. **Contrast is a framing modifier on any stage** — apply it where you need a favorable comparison.

**Output format for this step:**

```
Stage 1 — [Principle]: [What happens at this touchpoint]
  WHY: [Reason this principle comes first]
  
Stage 2 — [Principle]: [What happens at this touchpoint]
  WHY: [Reason for this position; interaction rule applied]
  
Stage 3 — [Principle]: [What happens at this touchpoint]
  WHY: [Reason for this position; what Stage 1 and 2 set up]
  
[Contrast framing: Where contrast amplification applies and why]
```

---

### Step 4: Ethical Boundary Check

**Action:** For each principle in the stack, verify: (a) trigger features are real, (b) the audience has consented to a persuasion context, (c) the intensity is proportionate to the stakes.

**WHY:** Stacking multiplies persuasive force. What is ethical for a single principle can become manipulative when three or four principles are combined at full intensity against an audience that has not consented to a sales context. The proportionality test is the key ethical check for stacking: a warm lead who has engaged across multiple touchpoints can ethically receive a full stack; a cold contact receiving their first message should not.

Run each principle through the three-question test:

| Question | Pass Condition | Fail Condition |
|----------|---------------|----------------|
| Is the trigger feature real? | Genuine scarcity, actual testimonials, real credentials | Manufactured countdown, fake reviews, invented credentials |
| Has the audience consented? | Opted into email, attended event, is in an active sales process | Cold contact, no prior consent, captive audience |
| Is intensity proportionate? | Multi-principle sequence for a considered purchase decision | 3+ principles applied in a single cold outreach touchpoint |

**Practical threshold:** More than 2 principles in a single cold touchpoint is disproportionate. For a full stack (4+ principles), the audience should have taken at least one prior voluntary action (opted in, requested info, attended a session).

Flag any principle that fails any of the three tests. Either revise the trigger to be genuine, reduce the stack intensity for early-stage cold contacts, or remove the principle.

---

### Step 5: Produce the Sequenced Campaign Plan

**Action:** Write the complete stacking plan — campaign goal, selected principles, interaction rules applied, stacking sequence with per-stage WHY, contrast framing opportunities, ethical classification, and next-step implementation pointers.

**WHY:** A documented stacking plan creates alignment across teams, makes the persuasion architecture explicit for review and iteration, and enables handoff to the dedicated principle skills for implementation. The WHY reasoning at each stage is what separates strategic stacking from tactical coincidence — it allows the team to adapt the sequence when a stage underperforms without losing the overall architecture.

**Output format:**

```
## Campaign Stacking Plan: [Campaign Name]

### Goal
[Target action. Audience profile. Number of touchpoints.]

### Selected Principles
[List with scores and evidence available for each]

### Interaction Rules Applied
[Which interactions were identified and how they affected sequencing]

### Stacking Sequence
Stage 1 — [Principle]: [Touchpoint description]
  WHY: [Reason for placement; evidence used]
  
Stage 2 — [Principle]: [Touchpoint description]
  WHY: [Reason for placement; interaction with Stage 1]

[Continue for all stages]

### Contrast Framing
[Where applied; anchor vs. target; expected amplification]

### Ethical Classification
[Pass/Fail for each principle on: real triggers, consent, proportionality]
[Overall assessment: Fair practitioner / Revise before deploying]

### Implementation Pointers
→ [Principle skill] for [stage name]
→ [Principle skill] for [stage name]
```

---

## Inputs / Outputs

### Inputs
- Campaign goal and target action (required)
- Audience profile and relationship type (required)
- Evidence inventory (testimonials, credentials, scarcity data) (required)
- Principle scores from `influence-principle-selector` (recommended; will run inline if absent)
- Existing campaign touchpoint plan (optional — for audit use)

### Outputs
- Selected principle set (2–4 principles with scores and rationale)
- Interaction rules applied to the selected set
- Stacking sequence with per-stage WHY reasoning
- Contrast framing opportunities
- Ethical classification (per principle and overall)
- Implementation pointers to dedicated principle skills

---

## Key Principles

**Stacking compounds, not adds.** Reciprocity + Commitment + Scarcity in the right sequence does not produce 3x the compliance of one principle alone — it produces a compounding architecture where each stage builds the conditions the next stage needs. Commitment makes Scarcity hit harder. Reciprocity creates the obligation Commitment then locks in. The compound effect is what makes Tupperware parties generate $2.5M/day.

**Sequencing is the skill.** Most practitioners know which principles exist. Few know that Commitment must precede Scarcity, or that Authority should open before Social Proof to maximize effect. The order is where the value lives.

**Reciprocity is force-independent.** The Regan study proves that reciprocity obligation persists even when the audience dislikes the requester. This makes it the most reliable opener for cold interactions where no relationship exists — and it makes investing heavily in Liking redundant when Reciprocity is already active.

**Contrast is a free amplifier.** The contrast principle is not one of the six principles — it is a perceptual mechanism that amplifies any principle when applied directionally. Present the expensive anchor before your price. Present the problem before your solution. Present the competitor's limitations before your advantages. It costs nothing and is frequently left on the table.

**Ethical stacking requires proportionality.** A full 6-principle stack is ethical at a Tupperware party where attendees chose to come. It is not ethical in a cold outreach email. The consent and proportionality test governs how many principles you can ethically deploy at each stage of a campaign — more principles are appropriate as the audience has taken more voluntary actions signaling genuine interest.

---

## Examples

### Example 1: SaaS Product Launch Funnel (4-Principle Stack)

**Scenario:** B2B SaaS tool launching to an email list of 3,000 marketing professionals. Seven-day launch window. Real scarcity: founding member pricing ends on day 7. Real social proof: 23 beta customers with documented results. Real authority: founding team credentials. No prior commitment from the list.

**Trigger:** "We have a 7-day launch window and an email list. Design the stacking sequence."

**Process:**
- Step 1: Scores — Authority=5 (real credentials), Social Proof=5 (23 beta results), Scarcity=5 (real deadline), Commitment=3 (no prior, but micro-commitment possible via free demo)
- Step 2: Interactions — Authority should open (suppress skepticism before social proof claims). Social proof needs uncertainty; problem-framing creates it. Commitment precedes Scarcity — add a micro-commitment stage (demo request or waitlist confirmation) before the deadline push.
- Step 3: Sequence — 4 stages over 7 days
- Step 4: All triggers real. List opted in. Proportionate for a purchase decision.

**Output:**
```
## Campaign Stacking Plan: SaaS Launch — Founding Member Pricing

### Goal
Convert list subscribers to paying customers within 7 days.
Audience: 3,000 opted-in marketing professionals. Cold leads — no prior commercial interaction.

### Selected Principles
Authority (5/5) — Founding team credentials + beta results evidence
Social Proof (5/5) — 23 beta customers with measurable results
Commitment (3/5) — Micro-commitment via demo or free trial request
Scarcity (5/5) — Founding member pricing, real 7-day deadline

### Interaction Rules Applied
1. Authority → Social Proof: Authority opens (Day 1) to suppress skepticism;
   Social Proof follows after uncertainty is raised about current approach.
2. Commitment → Scarcity: Demo request (Day 3) creates micro-commitment;
   Day 5-7 scarcity push works against that commitment, not just a cold clock.
3. Contrast: Day 5 email contrasts "current state" (status quo pain) with
   "founding member result" before the pricing offer.

### Stacking Sequence
Day 1 — Authority: "Who we are and why this matters." Founding team story,
  credentials, problem we solved.
  WHY: Cold list has no reason to trust. Credibility must come before claims.

Day 2 — Social Proof: "What 23 marketing teams achieved in the beta."
  3 case studies with specific metrics.
  WHY: Authority (Day 1) created credibility for these claims. Uncertainty
  about current approach (opened in Day 1 problem framing) makes peer results
  compelling.

Day 3 — Commitment: "Want a free demo walkthrough?" Demo request = micro-commitment.
  Responders are now on record as interested.
  WHY: A list subscriber who requests a demo has taken an active step. The
  consistency drive will apply to the purchase decision on Day 5+.

Day 5 — Contrast + Scarcity opening: "Here's what beta customers' results look
  like vs. the status quo — and why founding member pricing closes in 48 hours."
  Contrast frame (before → after) before the deadline.
  WHY: Commitment established on Day 3 means scarcity now works against a prior
  decision, not against nothing. Contrast makes the offer appear favorable after
  the before-after framing.

Day 7 — Scarcity close: "Founding pricing ends tonight." Hard deadline.
  WHY: Desire is established across 4 prior touchpoints. Scarcity now functions
  as urgency on a warm decision, not pressure on a cold one.

### Contrast Framing
Day 5: Present current-state problems (benchmark metrics the audience recognizes
as their own) before presenting the beta result metrics. Contrast anchor = pain;
contrast target = solution. Sequence is directional — anchor first.

### Ethical Classification
Authority: Real credentials. Fair practitioner.
Social Proof: 23 genuine beta customers, real results. Fair practitioner.
Commitment: Demo request is voluntary and genuine. Fair practitioner.
Scarcity: Founding pricing deadline is real. Fair practitioner.
Overall: Full stack is proportionate for a purchase decision from an opted-in list.

### Implementation Pointers
→ authority-signal-designer for Day 1 email credibility architecture
→ social-proof-optimizer for beta case study selection and metrics framing
→ commitment-escalation-architect for demo CTA design
→ scarcity-framing-strategist for Day 5-7 deadline copy
```

---

### Example 2: In-Person Sales Event (Tupperware-Pattern Stack)

**Scenario:** A B2B consultancy hosts a half-day workshop for 20 invited prospects — all warm leads from past conversations. Goal: convert workshop attendees to signed project proposals within 2 weeks.

**Trigger:** "I have a live workshop with warm prospects. How do I design the compliance architecture?"

**Process:**
- Step 1: Warm audience with prior relationship → Liking already high (structural amplifier). Real credentials (authority). Peer participants (social proof potential). Can create commitment during workshop. Reciprocity via workshop value delivery.
- Step 2: Liking is structural (relationship exists — use it as amplifier, not a sequential step). Reciprocity opens (workshop IS the gift). Commitment can be activated during the session. Social proof via peer discussion. Authority via facilitation expertise.

**Output:**
```
## Campaign Stacking Plan: B2B Consultancy Workshop

### Goal
Convert 20 warm prospects to signed proposals within 2 weeks.
Audience: Warm leads — prior conversations, no proposals yet.

### Selected Principles
Reciprocity (5/5) — Workshop is a high-value gift before the sales ask
Commitment (4/5) — Can activate public commitment during the session
Social Proof (4/5) — Peer participants provide real-time social proof of problem
Liking (structural amplifier — pre-existing warm relationships)

### Stacking Sequence
Before workshop — Liking structural setup: Warm personal invitation, not
  generic calendar. Acknowledge the specific prior conversation that led here.
  WHY: Liking amplifies every other principle. Set the relational tone before
  participants arrive.

Workshop opening — Reciprocity: Deliver genuine, immediately usable insight
  in the first 30 minutes. Participants must feel "I already got value" before
  any commercial discussion.
  WHY: Reciprocity creates obligation that persists through the session. The ask
  comes later — the value comes first.

Workshop mid-section — Social Proof: Structured peer discussion of current
  challenges. Participants hear others in the room with the same problems.
  WHY: Peer recognition of shared problems creates social validation. "Others
  like me have this problem" is social proof in the problem space — it amplifies
  urgency for the solution.

Workshop commitment activation: Structured exercise where participants document
  their own problem and write one specific goal they want to achieve. Collected
  on paper (active + written = high commitment quality).
  WHY: A written, active commitment to a goal creates consistency pressure.
  When the proposal addresses exactly that written goal, the participant's
  consistency drive supports a yes.

Post-workshop — Scarcity: Proposal offer is time-bound (specific window) and
  may be capacity-limited (genuine: only 3 new projects in Q2).
  WHY: Commitment established in workshop means scarcity now works against a
  prior decision, not a cold one. Deadline motivates action on already-established
  desire.

### Ethical Classification
All triggers real. Warm audience chose to attend. Workshop value genuine.
Scarcity is real (capacity-limited Q2 slots). Full stack is proportionate.

### Implementation Pointers
→ reciprocity-strategy-designer for workshop content design
→ commitment-escalation-architect for the written exercise format
→ scarcity-framing-strategist for the post-workshop proposal framing
```

---

### Example 3: Campaign Audit — Email Funnel with Stacking Errors

**Scenario:** A 5-email nurture sequence for a $1,200 online course. Current sequence: Email 1 (course overview), Email 2 (discount offer — 30% off expires in 24 hours), Email 3 (testimonials), Email 4 (FAQ), Email 5 (last chance). Conversion rate: 0.4%.

**Trigger:** "Audit this email sequence. What stacking errors are we making?"

**Process:**
- Identify current principles in use: Scarcity (Email 2), Social Proof (Email 3)
- Check sequencing against interaction rules
- Anti-pattern: Scarcity before commitment is established = urgency without obligation. Social Proof after Scarcity = backward sequence (social proof should reduce uncertainty BEFORE urgency is applied)
- Missing: Reciprocity (no value given before ask), Authority, Commitment

**Output:**
```
## Campaign Stacking Audit: 5-Email Course Funnel

### Current State
Email 1: Course overview (no principle active)
Email 2: 24-hour discount (Scarcity — premature)
Email 3: Testimonials (Social Proof — misplaced)
Email 4: FAQ (no principle active)
Email 5: Last chance (Scarcity repeat)

### Stacking Errors Identified

Error 1 — Scarcity before Commitment (Email 2)
The discount fires in Email 2 before any commitment is established.
A subscriber who has read one course overview email has made no commitment.
The 24-hour clock creates urgency that evaporates when it expires — and teaches
the list that deadlines don't matter (they got the same price when it "expired").
FIX: Add a micro-commitment stage before the scarcity stage. (Quiz completion,
free lesson request, explicit "I'm interested" click.)

Error 2 — Social Proof after Scarcity (Email 3)
Testimonials follow the scarcity push, but social proof is most powerful BEFORE
the urgency close. It reduces uncertainty so the audience enters the scarcity
stage with desire already formed.
FIX: Move testimonials to Email 2 or 3, before the scarcity push.

Error 3 — No Reciprocity opener
Email 1 describes the course but gives nothing. No obligation is created.
A free lesson, diagnostic, or high-value piece of content in Email 1 creates
obligation before any ask is made.
FIX: Lead with value. Give a free lesson, worksheet, or high-utility piece of
content before the first commercial message.

### Revised Stacking Sequence
Email 1 — Reciprocity: Free mini-lesson or diagnostic tool. Value before ask.
Email 2 — Authority + Social Proof: Instructor credentials + 3 student results
  with specific outcomes. Reduces uncertainty; builds trust.
Email 3 — Commitment: "What's your biggest X challenge?" CTA or mini-quiz.
  Micro-step creates consistency pressure.
Email 4 — Contrast + Scarcity opening: Before/after framing, then discount
  deadline introduced. Contrast makes discount appear favorable.
Email 5 — Scarcity close: Hard deadline with commitment reference.
  ("You said your goal was X — this is how to achieve it, and pricing ends tonight.")

### Ethical Classification
Free lesson is real. Testimonials are genuine. Discount deadline must be real
(if the offer extends past the deadline, this becomes exploitative scarcity).

### Implementation Pointers
→ reciprocity-strategy-designer for Email 1 value offer design
→ social-proof-optimizer for testimonial selection
→ commitment-escalation-architect for Email 3 micro-commitment design
→ scarcity-framing-strategist for Email 4-5 deadline framing
```

---

## References

| File | Contents |
|------|----------|
| `references/principle-interaction-matrix.md` | Full interaction rules for all 6 principles; documented case studies (Tupperware, Christmas toy, Good Cop/Bad Cop, Regan study); ethical stacking thresholds; 5 stacking sequence templates (cold outreach through full Tupperware-pattern event) |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Influence: The Psychology of Persuasion by Robert B. Cialdini.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-influence-principle-selector`
- `clawhub install bookforge-reciprocity-strategy-designer`
- `clawhub install bookforge-commitment-escalation-architect`
- `clawhub install bookforge-social-proof-optimizer`
- `clawhub install bookforge-liking-factor-engineer`
- `clawhub install bookforge-authority-signal-designer`
- `clawhub install bookforge-scarcity-framing-strategist`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
