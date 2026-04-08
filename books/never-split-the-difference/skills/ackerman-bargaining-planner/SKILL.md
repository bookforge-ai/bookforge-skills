---
name: ackerman-bargaining-planner
description: |
  Build a complete price-negotiation offer schedule using the Ackerman bargaining model. Use when someone asks "how do I negotiate a lower price?", "what should my opening offer be?", "how do I avoid splitting the difference?", "how do I structure my counter-offers so I don't give too much away?", or "how do I make my final offer feel credible?" Also use for: designing a salary negotiation offer sequence, structuring a vendor price reduction campaign, planning a real estate purchase offer ladder, deciding how far to push on a freelance rate, or building an offer schedule for any purchase or contract negotiation where you are trying to reach a specific target price. Produces a situation-specific ackerman-plan.md with your 4-stage offer sequence showing actual dollar amounts computed from your target price, scripted phrases for each stage, fairness-challenge responses, a noncash item list for the final offer, and anti-patterns to avoid. Works for any negotiation where you are the buyer (or the party making offers). Pair with calibrated-questions-planner (to generate questions to use between offers) and counterpart-style-profiler (to adapt delivery pace and tone).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/never-split-the-difference/skills/ackerman-bargaining-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: never-split-the-difference
    title: "Never Split the Difference: Negotiating as if Your Life Depended on It"
    authors: ["Chris Voss"]
    chapters: [6, 9, 23]
tags: [negotiation, price-negotiation, ackerman-model, offer-sequence, anchoring, loss-aversion, fairness-framing, concession-strategy, salary-negotiation, procurement, bargaining, noncash-offers, anti-patterns]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Situation brief — what you are buying or negotiating, the counterpart's current ask or opening position, and the context (B2B, consumer, salary, real estate, etc.)"
    - type: document
      description: "Your target price — the specific number you want to reach. This is NOT your walk-away point. It is your optimistic goal."
    - type: document
      description: "Noncash items available — non-monetary concessions you could offer at the final stage (faster payment, testimonial, referral, extended contract, flexibility on timing, etc.)"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Works with pasted briefs or document files."
discovery:
  goal: "Produce a 4-stage offer schedule with computed dollar amounts, scripted phrases per stage, fairness-challenge responses, and a noncash item for the final offer — so the negotiator can execute with confidence and without improvising in the moment"
  tasks:
    - "Gather target price, current counterpart ask, and available noncash items"
    - "Compute the 4 Ackerman offer amounts (65%, 85%, 95%, 100% of target)"
    - "Write scripted phrases for each stage transition"
    - "Generate fairness-challenge responses for all three fairness challenge types"
    - "Select or generate one noncash item for the final offer"
    - "Write the ackerman-plan.md artifact"
  audience:
    roles: ["buyer", "salesperson", "founder", "manager", "consultant", "recruiter", "procurement", "freelancer", "job-seeker", "real-estate-buyer"]
    experience: "beginner to intermediate — no negotiation training required"
  triggers:
    - "User is preparing to negotiate a price and wants a structured offer sequence"
    - "User wants to know what their opening offer should be"
    - "User has been countered and wants to know how much to concede"
    - "User wants their final offer to feel like a firm limit, not a round number"
    - "User is being pressured to split the difference and wants a better alternative"
    - "User has been accused of being unfair during a negotiation"
    - "User wants to make their final offer feel credible without lying"
  not_for:
    - "Generating the full negotiation preparation document — use negotiation-one-sheet-generator for the 5-section prep"
    - "Designing the questions to ask between offers — use calibrated-questions-planner for that"
    - "Understanding the counterpart's communication style — use counterpart-style-profiler"
    - "Defusing hostility before negotiation begins — use accusation-audit-generator first"
    - "Seller-side negotiations where you are receiving offers — adapt the framework manually"
  quality: placeholder
---

# Ackerman Bargaining Planner

## When to Use

You are preparing to negotiate a price — a purchase, a salary, a vendor contract, a freelance rate, or any deal where you need to move a counterpart from their current ask down to your target number.

You want a structured offer sequence that signals seriousness, creates credible commitment, and avoids the most common mistakes: splitting the difference, opening too close to your goal, using round numbers, making equal-sized concessions, or revealing your deadline.

**Input this skill needs:** Your target price (the number you want to reach — optimistic, not your walk-away point), the counterpart's current ask or opening position, and a list of noncash items you could offer as a final sweetener.

**Do not use this skill if:** You need a full negotiation preparation document — use `negotiation-one-sheet-generator`. You need to defuse hostility before you can make any offer — use `accusation-audit-generator` first. You are negotiating something where price is not the primary variable (use `calibrated-questions-planner` to find out what actually matters to them first).

---

## Context & Input Gathering

### Required
- **Your target price:** The specific number you want to reach. Be concrete — a vague target produces a vague plan. This is your optimistic goal, not your minimum acceptable price.
- **Counterpart's current ask:** Their stated price or opening position. If they have not yet made an ask, note that — you may be making the first offer.
- **Situation context:** What are you negotiating? (Purchase, salary, vendor contract, freelance rate, real estate, etc.) Who is the counterpart?

### Important
- **Noncash items available:** What non-monetary concessions could you offer? Examples: early payment, a testimonial or referral, extended contract term, flexibility on delivery schedule, exclusivity, training, or any item of genuine value to them that costs you little.
- **Counterpart type (if known):** Are they an Analyst (methodical, data-driven), Accommodator (relationship-focused, wants harmony), or Assertive (direct, time-focused)? If unknown, proceed — the skill works without this but use `counterpart-style-profiler` to adapt delivery.

### Observable (tell the skill what you can observe)
- **Their anchoring behavior:** Did they open extreme? Did they hold firm or move quickly?
- **Their deadline signals:** Have they mentioned timing constraints, deadlines, or urgency? (Important: protect your own deadline from disclosure.)
- **Their fairness language:** Have they used the word "fair" or accused you of being unreasonable?

### Defaults (used if not provided)
- **Noncash item:** If no items are provided, the skill will generate 3 plausible options based on the situation type for you to choose from.
- **Counterpart's ask:** If unknown, the skill will generate an anchor-response strategy and a recommended opening offer.

### Sufficiency check
If you have your target price and the situation context, proceed. Missing counterpart ask or noncash items is acceptable — the skill will generate estimates and options.

---

## Process

### Step 1: Establish Your True Target

**Action:** Confirm the target price the user wants to reach. Record it as a single specific number — not a range. If the user provides a range ("I want to pay between $40K and $50K"), set the target at the optimistic end ($40K). This number becomes the 100% anchor for all subsequent calculations.

**WHY:** Ranges invite the counterpart's brain to anchor on the number most favorable to them. A single optimistic target forces you to plan and execute toward your actual goal, not a compromise. Research on goal-setting in negotiations shows that negotiators with specific, ambitious single targets consistently outperform those with ranges or minimum-acceptable-outcome targets. This is the most common mistake: people confuse their walk-away point with their target and negotiate from the wrong number from the start.

**IF** user provides a walk-away point instead of a target → ask them to separate the two. Walk-away is the point at which you exit; target is what you are aiming for. The Ackerman model operates from the target, not the floor.

---

### Step 2: Compute the 4-Stage Offer Schedule

**Action:** Calculate the four Ackerman offer amounts using the following formula, then present them as a numbered schedule with actual dollar amounts:

```
Stage 1 — Opening offer:   TARGET × 0.65
Stage 2 — Second offer:    TARGET × 0.85
Stage 3 — Third offer:     TARGET × 0.95
Stage 4 — Final offer:     TARGET × 1.00  (use a non-round number near target)
```

**Increment psychology (critical):** The gap between each offer shrinks deliberately:
- Stage 1 → Stage 2: +20 percentage points
- Stage 2 → Stage 3: +10 percentage points
- Stage 3 → Stage 4: +5 percentage points

**Non-round number rule:** Make the final offer (Stage 4) a precise, non-round number that is at or near your target. If your target is $40,000, use $39,893 or $40,127 — not $40,000. If your target is $85/hour, use $84.35 — not $85.

**WHY:** The decreasing increment pattern communicates to the counterpart's subconscious that you are approaching your absolute limit. Each smaller concession signals "I have less room left." This is not a trick — it is honest signaling about your actual flexibility. Equal-sized concessions do the opposite: they suggest infinite room ("they moved $1,000 each time, so they can move $1,000 more"). The precise non-round final number creates the impression that the number was calculated from real constraints — because specific numbers imply research and limits, while round numbers imply padding. A counterpart receiving $39,893 thinks "that's an oddly specific number — they must have a real reason for it." A counterpart receiving $40,000 thinks "they rounded up, so maybe $38,000 is actually fine."

**Example calculation (target = $40,000):**
```
Stage 1: $40,000 × 0.65 = $26,000
Stage 2: $40,000 × 0.85 = $34,000
Stage 3: $40,000 × 0.95 = $38,000
Stage 4: $40,000 × 1.00 = $39,893 (non-round near target)
```

**IF** the counterpart's ask is below the Stage 1 opening → do not use this model as designed (you are already above their ask). Instead, start at Stage 3 or Stage 4 and use anchoring techniques from the Key Principles section.

---

### Step 3: Write Scripted Phrases for Each Stage

**Action:** For each of the 4 stages, write one scripted transition phrase the negotiator can say when moving to that offer. Each phrase must include: an empathic acknowledgment (label or calibrated question), then the offer amount.

**WHY:** The offer itself is only part of the communication. How you deliver each concession determines whether the counterpart feels heard or steamrolled. An empathic acknowledgment before each offer triggers the counterpart's cooperative instincts and makes the concession feel like a response to their situation rather than a mechanical formula. Calibrated questions between offers shift the problem-solving burden: instead of you explaining why you can't pay more, they explain what would make this work — which often reveals creative solutions.

**Stage 1 phrase template (opening offer):**
```
"I appreciate that this is an important [deal/purchase/hire] for both of us.
I want to be respectful of your time, so I'll be straightforward —
my current position is [STAGE 1 AMOUNT]."
```

**Stage 2 phrase template (after counterpart counters):**
```
"I hear you. It sounds like [label their stated concern or constraint].
I've looked at this again, and I can get to [STAGE 2 AMOUNT]."
```

**Stage 3 phrase template (after second counter):**
```
"I understand this isn't where you'd like to land, and I genuinely want to make this work.
How am I supposed to get to your number?
[Pause for answer]
The most I can do is [STAGE 3 AMOUNT]."
```

**Stage 4 phrase template (final offer — use with noncash item):**
```
"I've pushed as far as I possibly can.
[STAGE 4 AMOUNT — non-round number] is my absolute limit,
and I'd like to include [NONCASH ITEM] to make this work for you."
```

**Timing rule:** Do not rush from stage to stage. A label or calibrated question must precede each concession. The counterpart should be doing more talking than you between stages.

---

### Step 4: Generate Fairness-Challenge Responses

**Action:** Write a scripted response for each of the three types of fairness challenges the counterpart may deploy. Identify which type is most likely given the situation context, and mark it as the primary scenario.

**WHY:** The word "fair" is the most potent weapon in a negotiator's arsenal because it triggers loss aversion and puts the accused party on the defensive. Understanding the three distinct uses of "fair" — each with a different intent and a different required response — prevents you from either caving out of guilt or dismissing a genuine concern. Treating all three the same way is a high-cost mistake.

**Type 1 — Accusatory fairness (weaponized):**
*Signal:* "We just want what's fair." Said early in negotiation, often without evidence.
*Their intent:* Destabilize you. Put you on the defensive. Force an emotional concession.
*Response:*
```
"I understand — fairness matters to both of us.
I want you to feel this has been a fair process.
Can you help me understand specifically what feels unfair to you right now?"
```
*Why this works:* Returning the word "fair" without defensiveness takes away their weapon. Asking them to specify what feels unfair forces them to either articulate a real concern (which you can address) or reveal that the accusation was purely tactical.

**Type 2 — Genuine fairness (relational check-in):**
*Signal:* "I want to make sure we're both getting a fair deal." Said in a collaborative tone.
*Their intent:* Genuinely calibrate whether the deal feels balanced. Often used by Accommodator types.
*Response:*
```
"I appreciate you saying that — it matters to me too.
I've tried to be transparent throughout this process.
Is there something specific about the terms that doesn't feel right to you?"
```

**Type 3 — Inoculative fairness (offered by you proactively):**
*Signal:* You use it first.
*Your intent:* Disarm before they can weaponize it.
*How to deploy it:*
```
"I want to treat you fairly throughout this conversation.
If at any point something I propose seems off to you, I want you to tell me."
```
*Why this works:* Offering fairness before they demand it removes their ability to use it as a pressure tactic. It also signals confidence — you wouldn't offer to be fair if you planned to be unfair.

---

### Step 5: Select the Noncash Final Item

**Action:** From the user's provided noncash item list, select the one item most likely to be genuinely valuable to the counterpart based on the situation context. If no list was provided, generate 3 plausible options and ask the user to select one.

**WHY:** The noncash item serves two functions simultaneously. First, it provides the counterpart with a genuine concession that does not cost you money — preserving the financial terms of your final offer while giving them something to "win." People need to feel they got something, not just that they capitulated. Second, including a noncash item alongside a precise non-round final offer signals that you have exhausted your financial flexibility and are finding creative alternatives — confirming that the number is real.

**Noncash item selection criteria:**
- High perceived value to counterpart, low cost to you
- Relevant to their situation (not generic)
- Deliverable — something you can actually provide

**Examples by situation type:**
- Purchasing: Faster payment terms, favorable payment schedule, public testimonial, referral to similar buyers
- Salary negotiation: Extra PTO days, remote work flexibility, earlier performance review, professional development budget, equity accelerator
- Vendor/freelance: Longer contract term (predictable revenue), case study rights, priority queue access, introduction to other clients
- Real estate: Flexible closing date, furniture items, appliance upgrades, quick pre-approval

---

### Step 6: Write the Ackerman Plan Artifact

**Action:** Write `ackerman-plan.md` containing the complete offer schedule, scripted phrases, fairness responses, noncash item, and anti-patterns reminder.

**WHY:** A written plan with computed numbers and scripted phrases prevents the most common negotiation failure mode: improvising under pressure. When a counterpart pushes back hard, the human nervous system triggers the fawn or freeze response — and negotiators abandon their plan, concede too quickly, or split the difference just to end the discomfort. Having the script in front of you anchors the plan and gives you words to say when your brain goes blank. The anti-patterns section is included as a live reminder because the temptation to violate them will be highest at the moment of greatest emotional pressure.

**Output format:** See Outputs section below.

---

## Inputs / Outputs

### Inputs
- Target price (required)
- Counterpart's current ask or opening position (important — needed for calibration)
- Situation context (required)
- Noncash items available (important — skill can generate options if missing)
- Counterpart type/style (optional)

### Outputs

**File:** `ackerman-plan.md`

**Template:**

```markdown
# Ackerman Bargaining Plan: [Situation Name]

**Prepared for:** [Your name / role]
**Counterpart:** [Name / organization / role]
**Situation:** [What you are negotiating]
**Your target price:** [TARGET]
**Counterpart's current ask:** [THEIR ASK]

---

## Offer Schedule

| Stage | Multiplier | Amount | Increment |
|-------|-----------|--------|-----------|
| 1 — Opening offer | 65% of target | [AMOUNT] | — |
| 2 — Second offer | 85% of target | [AMOUNT] | +[X] from Stage 1 |
| 3 — Third offer | 95% of target | [AMOUNT] | +[X] from Stage 2 |
| 4 — Final offer | ~100% of target | [NON-ROUND AMOUNT] | +[X] from Stage 3 |

**Non-round final offer rationale:** [Explain the logic if needed — e.g., "calculated based on 12-month depreciation estimate"]

---

## Scripted Phrases

**Stage 1 — Opening:**
> "[Script from Step 3]"

**Stage 2 — After first counter:**
> "[Script from Step 3]"

**Stage 3 — After second counter:**
> "[Script from Step 3]"

**Stage 4 — Final offer:**
> "[Script from Step 3] + [NONCASH ITEM]"

---

## Fairness Challenge Responses

**If they say "We just want what's fair" (accusatory):**
> "[Response from Step 4]"

**If they raise fairness collaboratively:**
> "[Response from Step 4]"

**Inoculative fairness — use proactively at the start:**
> "[Proactive fairness statement from Step 4]"

---

## Noncash Final Item

**Selected item:** [ITEM]
**Why it works for them:** [Brief explanation]
**How to present it:** Include with Stage 4 offer as an add-on, not a trade.

---

## Anti-Patterns — Do Not Do These

- **Do not split the difference.** If they are at $50K and you are at $40K, $45K is not a solution — it rewards their extreme anchor and leaves you $5K short.
- **Do not use round numbers.** Round numbers signal padding. Use precise numbers at every stage.
- **Do not make equal-sized concessions.** Equal increments ($5K, $5K, $5K) signal infinite room. Shrink each increment.
- **Do not reveal your deadline.** Deadlines create urgency — but only for the person whose deadline is known. If you say "I need this done by Friday," you have handed them leverage.
- **Do not fixate on your walk-away point.** Negotiating from your minimum acceptable outcome anchors you low. Negotiate from your target and walk away if the target proves unreachable.
- **Do not make three or more rapid concessions.** Pace your concessions. A calibrated question or label between each offer is not optional — it is structurally required.

---

## Notes
[Space for observations made during the negotiation — what they said, what surprised you, what to adjust for the next conversation]
```

---

## Key Principles

**The 4-stage formula is a psychological signaling system, not just a math formula.** The percentages (65→85→95→100) work because of what the decreasing increments communicate: you are running out of room. Each smaller concession is an honest signal about your diminishing flexibility. The formula tells the counterpart's subconscious a coherent story: "this person started with room to move, they've moved, and now they're almost done." That story produces the settlement psychology that ends negotiations.

**WHY:** Counterpart decision-making during price negotiation is not rational — it is emotional and narrative-driven. The Ackerman formula exploits this by creating a credible narrative arc through the structure of your concessions alone. You are not arguing that your price is fair; you are demonstrating through behavior that you are at your limit.

**Loss aversion is twice as powerful as equivalent gain motivation.** Losses activate the emotional brain (System 1) approximately twice as strongly as equivalent gains. A counterpart who feels they might lose something they already have will negotiate harder than a counterpart who might gain the same thing. This means framing your offers and final position in terms of what they stand to lose if the deal falls apart is more motivating than framing it in terms of what they gain by accepting.

**WHY:** This is not manipulation — it is accurate communication. If the deal fails, they lose the certainty of a signed agreement, the time already invested, and any relationship goodwill built during negotiation. Naming those losses honestly is legitimate leverage. The key distinction: you are describing real consequences, not fabricating threats.

**Splitting the difference is a trap, not a compromise.** When both parties split the difference, the party who opened with a more extreme anchor wins more of the value. Splitting rewards extreme anchoring and punishes reasonable opening positions. It also produces outcomes that neither party is satisfied with — both feel they gave up the same amount, but neither feels they won.

**WHY:** The negotiator who proposes splitting the difference frames the midpoint as "fair" — but the midpoint is only fair relative to the two anchors, not relative to the actual value of the deal. If your anchor was accurate and theirs was inflated, the midpoint is inflated. The Ackerman model prevents this by anchoring your offers against your target, not their ask.

**Extreme anchoring makes your target seem reasonable by comparison.** Opening at 65% of your target — far below it — shifts the entire perceived range of the negotiation. When your Stage 1 offer is $26,000 and your target is $40,000, your final offer at $39,893 looks generous. If you had opened at $35,000, $39,893 would look like a small concession from an already-tight position. The opening offer shapes the psychological midpoint.

**WHY:** This is the anchoring effect in action. The first number spoken in a negotiation has disproportionate influence on where the settlement lands. Your opening offer is not your first concession — it is your opening anchor. It sets the range. Open extreme, then move systematically toward your target.

**Never reveal your deadline.** Deadlines create urgency — and urgency belongs to whoever needs the deal done faster. If you reveal your timeline ("I need to close this by end of quarter"), you have handed the counterpart the ability to slow-walk the negotiation until your deadline is imminent, then extract last-minute concessions under time pressure.

**WHY:** Your deadline is a constraint that limits your options. Any constraint that only you know about is a private vulnerability; any constraint both parties know about is leverage for the party without the constraint. Protect your deadline the same way you protect your walk-away point.

**The noncash item at the final stage creates a face-saving exit for the counterpart.** When you make your final non-round offer accompanied by a noncash item, the counterpart can tell themselves — and their boss — "I got the price plus X." This psychological face-saving function is as important as the financial function of the item. People need to feel they won something to agree to stop fighting.

**WHY:** Negotiations fail not because parties cannot find a number that works, but because one party cannot accept feeling like they lost. The noncash item gives the counterpart a "win" to report — which removes the psychological barrier to saying yes to your actual target price.

---

## Examples

### Example 1: Toyota 4Runner Purchase

**Scenario:** A buyer wants to purchase a used Toyota 4Runner. The dealer is asking $30,000. The buyer's research shows fair market value is approximately $25,000, which becomes the target price.

**Trigger:** "How do I negotiate the price on this truck without insulting the dealer?"

**Process:**
- Step 1: Target = $25,000
- Step 2: Offer schedule:
  - Stage 1: $25,000 × 0.65 = $16,250 (opening)
  - Stage 2: $25,000 × 0.85 = $21,250
  - Stage 3: $25,000 × 0.95 = $23,750
  - Stage 4: $25,000 × 1.00 = $24,893 (non-round final)
- Step 3: Each stage preceded by a label or calibrated question to the dealer
- Step 4: Fairness inoculation used proactively at the opening
- Step 5: Noncash item — immediate cash payment with same-day title transfer (saves dealer floor-plan carrying costs)
- Step 6: Plan written with scripted phrases

**Output:** `ackerman-plan.md` with the offer schedule showing actual amounts, Stage 4 delivery script including "I have the cash ready today and can do the title transfer this afternoon — that's worth something to you in terms of floor-plan savings," and a fairness-challenge response prepared for the dealer's likely "that's way below what we have in this truck."

**Result type:** Buyer reaches $24,893 — $5,107 below the ask — by moving systematically and making the dealer feel each concession was extracted through real effort.

---

### Example 2: Kidnapping Ransom Negotiation (Haiti)

**Scenario:** A Haitian kidnapping gang holds a victim and opens with a $150,000 ransom demand. The negotiating team's actual upper limit is $5,000, established as the target price. The goal is to use the Ackerman model to move the gang to a number the team can actually pay.

**Trigger:** Operational scenario — structured offer sequence needed under extreme pressure.

**Process:**
- Step 1: Target = $5,000
- Step 2: Offer schedule:
  - Stage 1: $5,000 × 0.65 = $3,250
  - Stage 2: $5,000 × 0.85 = $4,250
  - Stage 3: $5,000 × 0.95 = $4,750
  - Stage 4: $5,000 × 1.00 = $4,751 (non-round)
- Step 3: Calibrated questions used between stages: "How am I supposed to get that kind of money together?" "What would help us move this forward?" Labels used to acknowledge the gang's stated urgency without accepting their framing
- Step 5: Noncash item — a Christian burial for the victim (no cost to the team, high cultural value to the negotiating parties given Haiti's religious context)
- Step 6: Written plan maintained under pressure

**Output:** `ackerman-plan.md` used as a live script during multi-day negotiation. Settlement reached near the $5,000 target, with the burial offer accepted as the face-saving noncash item at the final stage.

**Key lesson:** The formula works under maximum emotional pressure precisely because it removes the need to improvise. When the gang demands more, the script provides the next move. The negotiator does not need to calculate in real time — the plan already computed every number.

---

### Example 3: Freelance Rate Negotiation

**Scenario:** A UX designer is negotiating her project rate. A startup wants to pay $8,000 for a 6-week engagement. The designer's target rate is $15,000 based on scope analysis and market comparables.

**Trigger:** "The client said $8,000 is their budget. How do I get to $15,000 without them walking away?"

**Process:**
- Step 1: Target = $15,000
- Step 2: Offer schedule:
  - Stage 1: $15,000 × 0.65 = $9,750 (opening counter to their $8,000)
  - Stage 2: $15,000 × 0.85 = $12,750
  - Stage 3: $15,000 × 0.95 = $14,250
  - Stage 4: $15,000 × 1.00 = $14,850 (non-round final)
- Step 3: Calibrated questions between stages: "What's driving the $8,000 figure — is that a hard budget cap or where you started?" (Stage 1→2 transition); "How am I supposed to cover [scope element] at that number?" (Stage 2→3)
- Step 4: Fairness inoculation — "I want to make sure we're both comfortable with the terms, so I'll be transparent about how I arrived at my numbers."
- Step 5: Noncash item — two rounds of free revisions after delivery (high perceived value to client nervous about scope creep; low cost to designer who plans one revision cycle anyway)
- Step 6: Written plan

**Output:** `ackerman-plan.md` with the offer schedule showing that the designer's opening counter ($9,750) is above the client's budget but below her target — which reframes the midpoint. Stage 4 script: "The absolute most I can do is $14,850, and I'll include two full revision rounds after delivery so you're not locked into the first cut."

---

## References

| File | Contents |
|------|----------|
| `references/formula-reference.md` | Ackerman percentages table, increment psychology, non-round number examples across common negotiation contexts, noncash item library by situation type, deadline protection tactics, extreme anchoring examples |
| `references/anti-patterns.md` | Full anti-pattern analysis: splitting the difference (why it rewards bad anchoring), BATNA-fixation (how walk-away point becomes psychological ceiling), equal-sized concessions (signaling infinite room), round numbers (padding signal), deadline disclosure (urgency transfer), over-scripting (rigidity trap) |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Never Split the Difference: Negotiating as if Your Life Depended on It by Chris Voss.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
