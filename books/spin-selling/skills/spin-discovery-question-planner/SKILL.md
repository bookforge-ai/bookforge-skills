---
name: spin-discovery-question-planner
description: "Plan Situation, Problem, Implication, and Need-payoff (SPIN) questions for a specific B2B sales call. Use this skill whenever a sales rep wants to prepare discovery questions for an upcoming meeting, when someone asks 'what should I ask in this call?', when planning questions for a deal in any industry, when drafting Implication questions for a complex sale, when prepping for a discovery call with a prospect, when a seller wants to go into a meeting with a structured question bank instead of winging it, or when a rep has a call next week and needs help thinking through what to ask. This skill applies Rackham's empirically-validated SPIN methodology — specifically including the 3-step Implication question planning sub-workflow (problem → related difficulties → questions) that makes the hardest question type executable. The output is NOT a generic discovery checklist: it is a planned conversation with branches, Implication chains, and Need-payoff conversion moves tied to specific likely customer problems and product capabilities the seller can actually deliver."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/spin-discovery-question-planner
metadata: {"openclaw":{"emoji":"❓","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [4]
domain: b2b-sales
tags: [sales, b2b-sales, enterprise-sales, discovery, spin-methodology, questioning-techniques, implication-questions, need-payoff, pre-call-planning]
depends-on:
  - need-type-classifier
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "deal-brief.md — company, contact, deal stage, deal size, what is known so far"
    - type: document
      description: "product-capabilities.md — what the seller's product can and cannot do"
    - type: document
      description: "account-research.md — company background, priorities, recent news (optional but valuable)"
    - type: document
      description: "needs-log.md — Implied/Explicit needs from prior calls (if this is a follow-up call)"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Document set: deal-brief.md, product-capabilities.md, account-research.md (optional), needs-log.md (optional). Agent produces question-bank-{deal}-{date}.md. Human asks the questions on the actual call."
discovery:
  goal: "Produce a pre-call question bank organized by SPIN type, with Implication chains planned in advance and Need-payoff questions ready to deploy when needs are confirmed"
  tasks:
    - "Plan Situation Questions that establish context without boring the buyer"
    - "Plan Problem Questions to surface 3+ specific likely problems this prospect may have"
    - "Apply the 3-step Implication planning sub-workflow for each problem: consequences → questions"
    - "Plan Need-payoff Questions keyed to capabilities the seller can actually deliver"
    - "Produce a sequence guide: when to move from S → P → I → N, and when to loop back"
  audience:
    roles: [account-executive, enterprise-sales-rep, sdr, solutions-consultant, founder-led-seller]
    experience: intermediate
  when_to_use:
    triggers:
      - "Rep has a discovery or follow-up call coming up and needs to plan questions"
      - "Seller wants to move beyond 'winging it' and into structured discovery"
      - "Manager is coaching a rep on how to develop Implication questions"
      - "Preparing for a call with a decision-maker who responds to implications, not features"
    prerequisites:
      - "Some knowledge of the prospect's business situation (even basic) — gathered from deal-brief.md, public research, or prior calls"
      - "Knowledge of what capabilities the seller's product offers"
    not_for:
      - "Classifying customer responses during or after the call (use need-type-classifier)"
      - "Drafting Benefit statements after Explicit Needs are confirmed (use benefit-statement-drafter)"
      - "Classifying whether a call outcome was an Advance or Continuation (use call-outcome-classifier)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 0
      baseline: 0
      delta: 0
    tested_at: ""
    eval_count: 0
    assertion_count: 0
    iterations_needed: 0
    what_skill_catches:
      - "Output organizes questions by SPIN type, not as a flat generic list"
      - "Implication questions are derived from specific problems via the 3-step sub-workflow"
      - "Need-payoff questions are keyed to capabilities the seller can actually deliver"
      - "Sequence guide tells the rep when to transition between question types"
      - "Anti-pattern warnings prevent over-asking Situation Questions and premature Need-payoff"
    what_baseline_misses:
      - "Produces a flat list of generic open questions with no internal structure"
      - "Implication questions are filler ('why does that matter?') not consequence chains"
      - "Need-payoff questions appear before the need has been developed"
      - "No guidance on sequence, branching, or when to transition between types"
---

# SPIN Discovery Question Planner

## When to Use

You have a B2B sales call coming up — discovery, follow-up, or executive conversation — and you want to go in with more than good intentions. This skill produces a pre-call question bank organized by SPIN type (Situation, Problem, Implication, Need-payoff) with Implication chains planned in advance and Need-payoff questions ready to deploy once a need is confirmed.

Use this skill when:
- Preparing for a discovery call with a new prospect or existing account
- Coaching a rep to plan questions for a specific deal
- Moving from a generic question list to a structured conversation with branches
- Dealing with a decision-maker (Implication Questions are especially powerful with people who think in consequences and effects)

**Critical prerequisite:** Before deploying Need-payoff Questions from this plan on an actual call, use `need-type-classifier` to verify that customer responses represent Implied Needs that have been sufficiently developed — or Explicit Needs that are ready for conversion. The question bank is a plan; what the customer says on the call determines where you actually go.

This skill is OUT OF SCOPE for: classifying customer responses (use `need-type-classifier`), drafting Benefit statements (use `benefit-statement-drafter`), or assessing whether a call outcome was an Advance (use `call-outcome-classifier`).

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Deal context:** Who is the prospect? What's the deal stage? What do we know about their situation?
  -> Check environment for: `deal-brief.md`
  -> If missing, ask: "Tell me about the deal — company, contact role, what stage you're at, and what you already know about their situation."

- **Product capabilities:** What can your product solve? What can it NOT solve?
  -> Check environment for: `product-capabilities.md`
  -> If missing, ask: "What are the main problems your product solves? Are there any capabilities it definitely does not cover?"

### Observable Context (gather from environment)

- **Account research:** `account-research.md` — company priorities, recent news, competitors
  -> If available: use to hypothesize likely problems. If unavailable: use deal-brief plus industry knowledge.

- **Prior needs log:** `needs-log.md` — Implied/Explicit needs from previous calls
  -> If available: read it. If some Implied Needs are already identified, the Implication chain work is partially done — plan questions to develop them further or convert them.
  -> If unavailable: treat this as a first call; hypothesize likely problems from scratch.

- **Call type:** New account (first contact) vs follow-up call
  -> If first contact: more Situation Questions are appropriate — you have less background
  -> If follow-up: reduce Situation Questions aggressively; move faster to Problem → Implication

### Default Assumptions

- Default to a **large-sale context** (high value, multi-stakeholder, relationship-dependent). In large sales, Implied Needs alone do not predict success; they must be developed into Explicit Needs before presenting solutions.
- Default to **not presenting solutions** in the question bank. This is a plan-only output; Benefit statements come after Explicit Needs are confirmed on the call.

### Sufficiency Threshold

SUFFICIENT: Deal context + product capabilities → produce full question bank
PROCEED WITH DEFAULTS: Only deal context known, no product capabilities → produce Problem + Implication plans, note that Need-payoff questions require capability mapping
MUST ASK: No deal context at all (no account, no call objective, no product)

## Process

### Step 1: Establish Deal Context and Confirm the Large-Sale Gate

**ACTION:** Read available deal documents or gather from the user. Confirm: is this a large sale (high value, multiple stakeholders, long cycle) or a small/transactional sale? Note the call type (new account vs follow-up) and what has already been uncovered.

**WHY:** The entire SPIN question sequence is designed for large sales. If this is a small sale (low value, single decision-maker, one-call close), Implication Questions are useful but not as critical — Problem Questions alone can move the sale. In large sales, failing to develop Implied Needs into Explicit Needs before presenting solutions is the primary cause of price objections and stalled deals. Knowing the sale type calibrates how many Situation Questions to plan and how aggressively to build Implication chains.

**Output:** A one-paragraph deal context summary: company, contact, stage, what is already known about problems or needs, and sale type (large/small).

### Step 2: Identify 3+ Likely Customer Problems Mapped to Your Capabilities

**ACTION:** Based on the account research, deal brief, and product capabilities, write down at least three specific problems this customer is likely to have that your product or service can solve. These are hypotheses — you will surface and confirm them on the call. Do not include problems you cannot solve.

**WHY:** This is the foundational planning step from the book's methodology: "Before the call, write down at least three potential problems which the buyer may have and which your products or services can solve." This step forces you to pre-qualify which problems are worth pursuing (you can solve them) and prevents two failure modes: (1) spending the call on Situation Questions that do not lead anywhere, and (2) accidentally developing a problem via Need-payoff Questions that you cannot address — which strengthens a need you cannot meet.

**Format:**
```
Problem 1: [Specific problem — e.g., "Manual reporting process takes 2+ days per month"]
  -> Capability match: [What we can solve — e.g., "Automated report generation"]

Problem 2: [...]
  -> Capability match: [...]

Problem 3: [...]
  -> Capability match: [...]
```

Add additional problems if context supports them.

### Step 3: Plan Situation Questions (Limited Set)

**ACTION:** For each problem identified in Step 2, plan 1-2 Situation Questions that establish the factual background needed to ask about that specific problem. Keep the total Situation Question list short (5-8 maximum for a new account call; 2-3 for a follow-up call).

**WHY:** Situation Questions collect background facts. They serve the seller, not the buyer — buyers find them tedious when overused. Research on thousands of calls found that inexperienced sellers ask far more Situation Questions than experienced ones, and that excessive Situation Questions are negatively correlated with call success. The goal is to do homework before the call (reducing unnecessary fact-finding), then ask only the Situation Questions directly needed to set up a Problem Question. Think of Situation Questions as runway, not the flight.

**Anti-pattern: Situation Question overload.** Detection signal: your Situation Question list has more than 8 items for a first call, or any for a follow-up where context is established. Fix: cut any Situation Question that doesn't directly enable a Problem Question you've already planned.

**Format:**
```
Situation Questions for Problem 1:
- "How does your team currently handle [process area]?"
- "What system do you use for [relevant function]?"
```

### Step 4: Plan Problem Questions for Each Identified Problem

**ACTION:** For each problem in Step 2, write 2-3 Problem Questions that probe directly for that problem, difficulty, or dissatisfaction. These questions should invite the customer to express an Implied Need.

**WHY:** Problem Questions are more strongly linked to sales success than Situation Questions, especially in smaller sales. In large sales, they provide the raw material — the Implied Needs — that Implication Questions will develop. Without Problem Questions, you have no foundation to build an Implication chain. The goal is to hear the customer say something like "Yes, that is a problem for us" — that statement is the Implied Need you will develop in the next step.

**Format:**
```
Problem Questions for Problem 1:
- "Are you finding [process area] takes longer than it should?"
- "What difficulties do you run into when [specific situation]?"
- "Is [current approach] creating any reliability or bottleneck issues?"
```

### Step 5: Apply the 3-Step Implication Question Planning Sub-Workflow

**ACTION:** For each problem identified in Step 2, apply this three-step method to generate a chain of Implication Questions:

**Step 5a — Write down the problem:**
State the specific Implied Need the customer might express (from your Problem Question above).
Example: *"Our current system is hard for operators to use."*

**Step 5b — Write down the related difficulties this problem leads to:**
Ask yourself: what are the downstream consequences of this problem? Think broadly — cost, time, people, quality, risk, downstream processes, stakeholder impact. Be especially alert for implications that reveal the problem to be more severe than it initially appears.
Example consequences:
- Only 3 trained operators → creates bottleneck when one is absent
- Bottleneck → overtime costs
- Overtime → operator dissatisfaction → turnover
- Turnover → retraining cost (estimate: $5,000/operator)
- Sending work outside → quality risk, delivery delays

**Step 5c — Write the questions each difficulty suggests:**
For each consequence, write the Implication Question that surfaces it. These questions are problem-centered — they make the problem feel more serious. This is intentional: the customer must perceive the problem as large enough to justify the cost of solving it.
Example questions:
- "If you only have three trained operators, what happens when one is out sick or leaves?"
- "How does that bottleneck affect your production schedules?"
- "What does retraining a replacement operator cost you in wages and training fees?"
- "When you send work outside, how does that affect your quality control?"

**WHY this step is the hardest and most valuable:** Research found that only 1 in 20 questions asked in an average sales call is an Implication Question — not because sellers don't know they're useful, but because good Implication Questions require advance planning. They cannot be improvised reliably. The reason $120,000 solutions seem outrageous against a small Implied Need is that the buyer has not yet connected the Implied Need to its full cost. The Implication chain makes that connection explicit — not by manipulation, but by helping the buyer see the total size of the problem. This is also why Implication Questions are especially powerful with decision-makers: executives think in consequences and effects, not surface symptoms.

**Apply Quincy's Rule to verify your Implication Questions:** Implication Questions should feel "sad" — they are problem-centered and make the problem more serious. If a question feels "happy" or solution-focused, it has drifted into Need-payoff territory. Reclassify it in the next step.

**Format per problem:**
```
Problem 1 Implication Chain:
  Implied Need likely heard: "[Customer's words if the Problem Q works]"

  Related difficulties:
  - [Consequence A]
  - [Consequence B]
  - [Consequence C]

  Implication Questions:
  - "[Question surfacing Consequence A]"
  - "[Question surfacing Consequence B]"
  - "[Question surfacing Consequence C — if appropriate given conversation flow]"
```

### Step 6: Plan Need-Payoff Questions Keyed to Deliverable Capabilities

**ACTION:** For each problem, plan 2-3 Need-payoff Questions to ask after the Implication chain has developed the need. Each Need-payoff Question must map to a capability your product can actually deliver.

**WHY:** Need-payoff Questions shift the conversation from problem-focused (which is "sad") to solution-focused (which is "happy"). They achieve two things simultaneously: (1) they focus the customer's attention on what a solution would mean for them — positive and constructive; (2) they get the customer articulating the benefits themselves. A customer who explains to you why your solution would help them is rehearsing the pitch they will later give to their internal stakeholders. This internal selling effect is a major reason Need-payoff Questions are so powerful in large, multi-stakeholder deals.

**Critical restrictions:**
- **Do not ask Need-payoff Questions before the need is developed.** If the Problem Question has just been asked and the customer has only given a mild Implied Need, the Implication chain must come first. Need-payoff before development produces customer defensiveness.
- **Do not ask Need-payoff Questions for capabilities you cannot deliver.** If a customer raises a need you cannot meet and you ask "Why would that be important to you?" — you are strengthening a need you have no answer for. Ask Need-payoff Questions only where you have a capability match (Step 2).

**Format per problem:**
```
Need-payoff Questions for Problem 1:
  (Ask only after Implication chain confirms the need is felt as serious)
  - "If you could eliminate [the core difficulty], what would that mean for your team?"
  - "Would it help you if [capability we offer]?"
  - "Is there any other way solving [problem] would benefit you?"
```

### Step 7: Write the Sequence Guide and Branching Rules

**ACTION:** Produce a one-page sequence guide for the call. This tells the seller: when to move from S → P, from P → I, from I → N, and when to loop back.

**WHY:** The SPIN sequence is a guideline, not a rigid formula. Calls branch. The customer might open the call by volunteering an Explicit Need — in which case move directly to Need-payoff. They might raise a problem the seller cannot solve — in which case do NOT ask Need-payoff Questions. They might shut down after too many Implication Questions — in which case shift to Need-payoff earlier to restore positive energy. The sequence guide arms the seller with conscious decision rules rather than reactive improvisation.

**Sequence guide format:**
```
CALL SEQUENCE GUIDE — [Deal Name] — [Date]

Opening: [1-2 Situation Questions to establish context — see Step 3]
↓
Problem surfacing: Ask Problem Questions for Problem 1. 
  If customer confirms → move to Implication chain.
  If customer denies or deflects → move to Problem Questions for Problem 2 or 3.
↓
Implication development: Work through the Implication chain for the confirmed problem.
  If customer language shifts from "it's a minor issue" to "actually, this is significant" → 
  the need is developed enough. Move to Need-payoff.
  If customer seems uncomfortable or negative → move to Need-payoff earlier to shift energy.
↓
Need-payoff conversion: Ask Need-payoff Questions for the developed need.
  Get the customer talking about what a solution would mean for them.
  Only present a capability AFTER a Need-payoff Question has elicited a customer statement 
  describing the value they want. That statement is the Explicit Need.
↓
If a second problem path is needed: repeat Problem → Implication → Need-payoff cycle.

LOOP BACK SIGNALS:
- Customer raises a new problem mid-Implication chain → finish current chain or note 
  the new problem and return to it. Do not abandon a chain once started.
- Customer raises a need you cannot meet → do NOT ask Need-payoff Questions. 
  Acknowledge and redirect to a need you can meet.
- Call is running short → compress by combining Implication Questions and moving to 
  Need-payoff faster. Never skip the Problem Questions — they are the foundation.
```

### Step 8: Write the Question Bank File

**ACTION:** Compile all outputs from Steps 2-7 into a single file: `question-bank-{deal}-{date}.md`. The file should be readable in 5 minutes before the call starts.

**WHY:** A written artifact carries the work forward. Without it, the planning exists only in this conversation. The question bank is also the input to `spin-skill-practice-coach` if the rep wants to learn from the call afterward, and to `sales-call-plan-do-review-coach` for a full Plan-Do-Review cycle.

## Key Principles

- **Implication Questions require advance planning.** They are the most powerful question type in large sales — and the hardest to generate under fire. Research found only 1 in 20 questions asked in an average call is an Implication Question. The 3-step sub-workflow (problem → consequences → questions) is the only reliable way to have good Implication Questions ready before the call. Sellers who skip this step improvise generic probes that do not build a consequence chain.

- **Need-payoff Questions only work when the need is developed.** A Need-payoff Question asked against a mild, undeveloped Implied Need produces price shock ("$120,000 just to make a machine easier to use?"). The same question asked after a thorough Implication chain — where the buyer has walked through $25,000 in training costs, expensive overtime, and quality failures from work sent outside — produces the opposite reaction. The problem is now large enough to make the solution feel justified.

- **Situation Questions serve you, not the buyer.** Do your homework before the call. Every Situation Question you eliminate through pre-call research is a question that doesn't bore your prospect. Experienced sellers ask far fewer Situation Questions than inexperienced ones — they move faster to problems because they have prepared better.

- **Never ask Need-payoff Questions for capabilities you cannot deliver.** When a customer raises a need you cannot meet, do NOT ask "Why is that important to you?" — you will strengthen a need that will become an objection you cannot answer. Redirect to a need within your capability set.

- **The SPIN sequence is a map, not a script.** Customers branch. If the customer opens with an Explicit Need, go directly to Need-payoff. If a new problem surfaces mid-chain, note it and return. If the customer seems discouraged after several Implication Questions, shift to Need-payoff earlier to restore positive energy. Quincy's Rule is the reset button: Implication = sad (problem-centered); Need-payoff = happy (solution-centered). If the conversation tone needs to change, shift question types accordingly.

- **For decision-makers, lean into Implication Questions.** Decision-makers respond most favorably to sellers who explore consequences and effects. The language of implications is the language of senior executives. More Implication Questions in calls with executives; more Problem Questions in calls with users and operational stakeholders.

## Examples

**Scenario: First discovery call with a mid-market manufacturing prospect**

Trigger: Rep asks — "I have a discovery call next Tuesday with an operations director at a 200-person manufacturer. We sell production scheduling software. Help me plan my questions."

Process:
1. Deal context: large sale, first call, no prior needs data. Product capabilities: scheduling automation, bottleneck detection, operator load balancing.
2. Likely problems: (a) manual scheduling leads to production bottlenecks, (b) operator overtime from poor load distribution, (c) last-minute changes cascade into downstream delays.
3. Situation Questions (limited): "What does your current scheduling process look like?" / "How far in advance are you typically scheduling production runs?"
4. Problem Questions: "Are you finding that last-minute order changes create downstream disruptions?" / "When one line slows down, how does that ripple into the rest of the schedule?"
5. Implication chain for Problem (a): Implied Need likely heard: "Yes, we have bottlenecks when orders change." Consequences: delayed shipments → customer dissatisfaction → expediting costs → overtime. Implication Questions: "What's the downstream effect when a bottleneck forces a late shipment?" / "How much overtime do you typically absorb when you're trying to catch up?"
6. Need-payoff: "If you could catch a bottleneck forming 24 hours in advance, what would that mean for your on-time delivery rate?"

Output: `question-bank-acme-mfg-2026-04-15.md` — a three-problem, three-chain question bank with sequence guide. Rep reads it the morning of the call.

---

**Scenario: Follow-up call after a discovery call where Implied Needs were surfaced**

Trigger: Rep shares needs-log.md showing two Implied Needs: "approval workflow is slow" and "reporting takes two days." "I'm seeing them next week — what do I ask?"

Process:
1. Deal context: follow-up call, large sale, two Implied Needs already logged. Reduce Situation Questions to near zero — context is established.
2. Prior implied needs → needs to be developed into Explicit Needs via Implication chains before any solution presentation.
3. Implication chain for "approval workflow is slow": Consequences: deals slip because contracts wait in queue → salespeople lose momentum → deals lost to faster-moving competitors → revenue at risk. Implication Questions: "When a contract sits in queue, how long does the delay typically run?" / "Have you lost any deals because a competitor moved faster while your approval was pending?"
4. Need-payoff after development: "If you could cut approval time from days to hours, what would that mean for your close rate?"

Output: `question-bank-deal-name-2026-04-22.md` with two Implication chains, minimal Situation Questions, and Need-payoff questions ready after each chain.

---

**Scenario: Implication chain worked example (verbatim dialogue reference)**

Trigger: Rep asks — "How do Implication Questions actually work in practice? Show me an example."

Process: Reference the Contortomat/Easiflo dialogue in `references/contortomat-implication-dialogue.md`. The dialogue shows a seller starting from a mild Implied Need ("the machines are rather hard to use") and building it — through 7 Implication Questions — into a recognized $25,000+ annual problem, at which point a $120,000 solution no longer seems unreasonable. The worked example is the clearest illustration of how the value equation shifts through Implication questioning.

## References

- Verbatim Contortomat/Easiflo Implication Question dialogue (the worked example that shows how the value equation shifts): [references/contortomat-implication-dialogue.md](references/contortomat-implication-dialogue.md)
- Verbatim telephone system Need-payoff dialogue (the worked example showing buyer-stated benefits): [references/telephone-needpayoff-dialogue.md](references/telephone-needpayoff-dialogue.md)
- Stock question patterns by SPIN type (template library for rapid planning): [references/spin-question-templates.md](references/spin-question-templates.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill depends on:
- `clawhub install bookforge-need-type-classifier` — classify customer responses as Implied or Explicit Needs during or after the call (reads `needs-log.md` that this skill uses as input)

Skills that build on this one:
- `clawhub install bookforge-benefit-statement-drafter` — draft Benefit statements once Explicit Needs are confirmed (Level 2, depends on this skill)
- `clawhub install bookforge-commitment-and-advance-planner` — plan the specific Advance you'll seek on the call (Level 1, use alongside this skill)
- `clawhub install bookforge-sales-call-plan-do-review-coach` — wrap the full Plan-Do-Review cycle around a single call (Level 2, orchestrates this skill)
- `clawhub install bookforge-spin-skill-practice-coach` — build your SPIN questioning skill systematically over weeks (Level 2, depends on this skill)

Or install the full SPIN Selling skill set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
