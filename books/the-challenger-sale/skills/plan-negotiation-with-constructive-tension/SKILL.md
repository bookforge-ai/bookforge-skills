---
name: plan-negotiation-with-constructive-tension
description: |
  Build a pre-call negotiation plan using DuPont's four-step framework and sequence concessions to avoid the proactive-discount and ultimatum traps.

  Trigger this skill when you need to:
  - Plan a negotiation for a B2B sales deal before a pricing or concession conversation
  - Respond to a customer discount request without immediately caving on price
  - Counter a price reduction demand by broadening the negotiation beyond price
  - Structure your concession sequence so you trade low-value items first and protect margin
  - Avoid proactive discounting, escalating concession patterns, or ultimatum traps
  - Apply the DuPont four-step negotiation framework (Acknowledge & Defer → Deepen & Broaden → Explore & Compare → Concede According to Plan)
  - Use the Situational Sales Negotiation (SSN) pre-call planning template to score concessions before the call
  - Build scripted deferral language to buy time without threatening the deal
  - Prepare for a challenger negotiation with constructive tension
  - Draft a pre-call negotiation worksheet for an upcoming customer conversation

  NOT for: diagnosing whether you have a taking-control problem in the first place — run diagnose-taking-control-gaps first to produce the control diagnosis this skill consumes.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/plan-negotiation-with-constructive-tension
metadata:
  openclaw:
    emoji: "⚖️"
    homepage: "https://github.com/bookforge-ai/bookforge-skills"
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors:
      - Matthew Dixon
      - Brent Adamson
    chapters:
      - 7
tags:
  - sales
  - b2b-sales
  - challenger-sale
  - negotiation
  - concession-management
  - sales-control
depends-on:
  - diagnose-taking-control-gaps
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "deal-brief.md + taking-control-diagnosis.md + counter-proposal.md (or equivalent deal context including the customer's specific ask, deal size, and available solution elements)"
  tools-required:
    - Read
    - Write
    - AskUserQuestion
  works-offline: true
discovery:
  goal: "Build a pre-call negotiation plan using DuPont's four-step framework and sequence concessions to avoid the proactive-discount and ultimatum traps."
  audience:
    - B2B sales representatives preparing for a pricing or concession conversation
    - Account executives managing enterprise deals with procurement-driven pressure
    - Sales managers coaching reps on negotiation discipline and concession sequencing
  prerequisites:
    - "diagnose-taking-control-gaps produces the taking-control-diagnosis.md this skill consumes"
  not_for:
    - Posture diagnosis and foil RFP detection → use diagnose-taking-control-gaps
    - Building a commercial teaching pitch → use build-commercial-insight
---

# Plan Negotiation with Constructive Tension

## Overview

Most reps lose value in negotiations not because customers are more powerful, but because reps seek premature closure. When a customer asks for a discount, the rep's instinct is to resolve the tension immediately — by conceding. The DuPont four-step framework, built on BayGroup International's Situational Sales Negotiation (SSN) methodology, is a pre-call planning and in-call navigation system that equips any rep to hold position assertively without crossing into aggression.

The framework works in two phases:

1. **Before the call** — complete the SSN pre-call worksheet to score every possible concession by cost-to-supplier and value-to-customer. This converts the call from an improvised reaction to a planned negotiation.
2. **During the call** — navigate four named steps in sequence. Skipping steps is the primary cause of premature concessions.

This skill produces a `negotiation-plan.md` file containing the completed worksheet and scripted language for each step.

---

## When to Use

Use this skill when:
- A customer has made a specific demand (price reduction, extended terms, added scope) and you have an upcoming conversation to respond
- You have completed `diagnose-taking-control-gaps` and have a `taking-control-diagnosis.md` indicating passive posture or concession risk
- A deal is at or near commercial terms and you need a structured plan for the negotiation conversation
- You want to ensure concessions are sequenced (low-value first) rather than improvised under pressure

**Run `diagnose-taking-control-gaps` first** if you have not yet established whether you have a control gap. This skill assumes the diagnosis is complete and the rep has decided to plan a negotiation, not diagnose a deal.

---

## Step 1 — Load Deal Artifacts

Read all available deal documents from the working directory.

**Required (at least one):**
- `deal-brief.md` — account name, deal size, deal stage, what the customer is asking for (the demand), what solution elements are on the table
- `taking-control-diagnosis.md` — output of `diagnose-taking-control-gaps`; tells you the rep's behavioral posture and whether active misconceptions are present

**Optional but high-value:**
- `counter-proposal.md` — the customer's formal counter-proposal or written demand
- `discovery-notes.md` — customer's underlying business objectives, key stakeholders, what they care about beyond price
- `solution-capabilities.md` — full inventory of what can be traded (service tiers, terms, delivery options, support packages)

**If no documents exist**, ask the user:

1. What is the customer asking for? (specific demand — e.g., "20% price reduction before signing")
2. What is the deal size and current stage?
3. What solution elements are on the table beyond price? (service plans, terms, implementation support, delivery timelines)
4. What does the customer care about most beyond price, if known?
5. What is the supplier's walkaway position — the floor below which the deal is not worth doing?

Why this matters: the SSN worksheet in Step 2 cannot be scored without knowing what is on the table. The scripted language in Steps 3–6 cannot be calibrated without knowing the specific customer demand.

---

## Step 2 — Complete the SSN Pre-Call Worksheet

Complete the six-section SSN worksheet before drafting any call language. This is the planning foundation that enables assertive behavior in the call. Challengers do this intuitively; this worksheet makes it explicit for all reps.

See `references/ssn-template.md` for the full template with scoring tables.

**Section 1 — Power Positions**

List the supplier's strengths and weaknesses across five dimensions: products/capabilities, brand/reputation, pricing/value ratio, service/support, customer relationships. Score each 1–10.

Purpose: most reps underestimate their leverage. Writing strengths down shifts the psychological default away from immediate concession. A rep who knows they have a 9/10 in technical implementation support is harder to move off price than one who hasn't thought about it.

**Section 2 — Information to Get from Customer**

List the questions to ask in the Deepen and Broaden step. The most important: "What are you looking to achieve with a [X]% price reduction?" — this surfaces whether the demand is driven by budget constraint or a specific business outcome that can be satisfied another way.

**Section 3 — Information to Provide or Protect**

Decide in advance what information to share with the customer and what to withhold. Deciding this during a live negotiation under pressure leads to disclosing too much or too little.

**Section 4 — Anticipated Objections and Planned Responses**

Write out 3–5 likely objections and draft specific responses. Improvised responses under pressure almost always result in unnecessary concessions.

**Section 5 — Supplier Goals and Customer Hypotheses**

State the supplier's non-negotiable terms (scope items, price floor, delivery requirements). Then write at least two hypotheses about the customer's underlying need — the business outcome behind the stated demand. These hypotheses drive the Deepen and Broaden conversation.

**Section 6 — Concession Inventory with Scoring**

This is the operational core of the SSN template. For each potential concession:
- Score cost to supplier (1 = minimal cost, 10 = very expensive)
- Score value to customer (1 = low value, 10 = high value)

Identify the concessions that are high-value to the customer but low-cost to the supplier — offer these first. Price concessions typically score high on cost to supplier and low-to-moderate on customer value, which is why they should come last, not first.

Also list concessions to request from the customer in exchange for each offer. Concessions should be traded, not donated.

---

## Step 3 — Draft Step 1 Language: Acknowledge and Defer

Write the scripted language the rep will use to defer the customer's demand without dismissing it.

**The key principle:** Deferring without customer permission is aggressive. Winning permission first makes the same deferral assertive. The script must do three things: acknowledge the demand, promise eventual closure, and ask permission to defer.

**Template (adapt to deal context):**

> "I understand that [price / the discount / the terms change] is something we need to address, and I want to make sure we do. Before we get there, I'd like to take a few minutes to make sure I fully understand what you're trying to achieve — so we can look at everything we can do to make this deal as valuable as possible for you. Is that all right?"

**What makes this work:**
- "I understand" — acknowledges the demand without committing to it
- "I want to make sure we do" — promises the customer they will get a resolution
- "Is that all right?" — seeks explicit permission; without this, the deferral reads as avoidance

Write the deal-specific version of this language in `negotiation-plan.md`.

---

## Step 4 — Draft Step 2 Language: Deepen and Broaden

Write the questions and prompts the rep will use to expand the negotiation beyond the single stated demand.

**Purpose:** Price is rarely the only thing the customer cares about. Deepen and Broaden surfaces what else matters — warranty coverage, service response time, implementation timeline, payment terms, future roadmap commitments — so that price is no longer the only negotiable.

**Technique — start with what the customer already values:**

Begin by getting the customer to restate what they like about the offering. This activates positive framing before returning to the demand. Then introduce the broadening questions.

**Core broadening questions (adapt to deal):**

1. "What are you looking to achieve with a [X]% price reduction?" — surfaces the business rationale; the answer often reveals a non-price solution
2. "Beyond price, what other elements of this deal are most important to you in terms of making this work?" — expands the negotiable surface
3. "If we were able to [address the underlying need another way], how would that compare to the price reduction you're looking for?"

**Write 2–3 deal-specific questions** in `negotiation-plan.md` based on what is known about the customer's business situation from the discovery notes.

---

## Step 5 — Draft Step 3 Language: Explore and Compare

Using the concession scoring from Section 6 of the SSN worksheet, draft the trade offers the rep will put on the table during the Explore and Compare conversation.

**Purpose:** Convert the expanded negotiable universe (identified in Step 2) into concrete trade proposals. The SSN scoring determines which concessions to offer first.

**Trade structure:**

Prioritize concessions where cost-to-supplier is low and value-to-customer is high. Present these as genuine value moves, not consolation prizes. Frame each as a trade with a reciprocal ask:

> "If we [extend the service plan by six months / move the delivery date up / include implementation support], would that address the concern you're trying to solve with the price reduction?"

> "If I can [do X], I'd want [ask for Y in return] — does that work for you?"

**Concession sequencing rules:**
1. Never skip to price while non-price options remain on the table
2. Always frame concessions as trades — what the rep gives must come with something the customer gives
3. Follow the SSN scoring order — highest customer value / lowest supplier cost comes first
4. Hold price concessions as the final lever, not the first

Write the ordered list of trade proposals in `negotiation-plan.md`.

---

## Step 6 — Draft Step 4 Language: Concede According to Plan

Write the concession sequence the rep will follow if Steps 2–3 do not resolve the customer's demand and a price concession is required.

**The core rule:** Start with a meaningful concession, then offer progressively smaller concessions as negotiations continue. This is the inverse of the escalating pattern.

**Why this works:** The customer perceives movement and good faith from the initial meaningful concession. The decreasing size of subsequent concessions signals that the rep is approaching their limit, which motivates the customer to close rather than push further. Both parties end the negotiation feeling they won.

**Concession plan structure (write this in negotiation-plan.md):**

| Round | Concession | Amount / Scope | Trigger | Reciprocal Ask |
|-------|------------|----------------|---------|----------------|
| 1 | (First offer — meaningful) | | If they reject the non-price trades from Step 5 | (what to ask in return) |
| 2 | (Second — smaller) | | If they reject Round 1 | (what to ask in return) |
| 3 | (Third — smaller still) | | If they reject Round 2 | (what to ask in return) |
| Walkaway | — | — | If they reject Round 3 | Disengage protocol |

**Before executing any concession in this plan:** verify the concession is in the pre-planned sequence. If the customer is pushing for a concession not in the plan, pause, reference Section 5 (supplier goals and non-negotiables), and respond deliberately.

---

## Step 7 — Anti-Pattern Check

Before finalizing `negotiation-plan.md`, review the plan against the three named concession anti-patterns. See `references/concession-antipatterns.md` for full descriptions.

**Check 1 — Escalating concessions:**
Is each concession in your plan smaller than the previous one? If Round 2 is larger than Round 1, reorder the sequence.

**Check 2 — Proactive discounting:**
Does the plan include any concession offered before the customer has made a specific ask? Remove it. Concessions are given in response to demands, not in anticipation of them.

**Check 3 — Ultimatums:**
Does the plan use language like "this is our final offer" or "take it or leave it" before the walkaway point has been reached? Replace with the Acknowledge and Defer language from Step 3. Reserve the walkaway statement for the genuinely planned walkaway — the position identified in Section 5 of the SSN template.

---

## Step 8 — Write negotiation-plan.md

Produce `negotiation-plan.md` in the working directory with the following structure:

```
# Negotiation Plan — [Deal Name / Account]
Date: [date]
Customer demand: [specific ask]
Deal context: [deal size, stage, key stakeholders]

## SSN Pre-Call Worksheet Summary
[Power position highlights — top 3 supplier strengths]
[Key information to gather — top 3 questions]
[Concession inventory — scored table]
[Walkaway terms]

## Step 1 — Acknowledge and Defer Script
[Deal-specific scripted language]

## Step 2 — Deepen and Broaden Questions
[3–5 deal-specific questions to expand the negotiation]

## Step 3 — Explore and Compare: Trade Offers
[Ordered list of trade proposals with framing language]

## Step 4 — Concede According to Plan
[Concession sequence table with triggers and reciprocal asks]

## Anti-Pattern Status
[ ] Escalating concessions — [CLEAR / FLAG: describe]
[ ] Proactive discounting — [CLEAR / FLAG: describe]
[ ] Ultimatums — [CLEAR / FLAG: describe]
```

---

## Self-Check Before Delivering the Plan

Before writing `negotiation-plan.md`, verify:

- [ ] SSN concession scoring is complete — every potential concession has a cost-to-supplier AND a value-to-customer score
- [ ] Acknowledge and Defer script explicitly seeks customer permission ("Is that all right?" or equivalent)
- [ ] Deepen and Broaden includes the rationale question: "What are you looking to achieve with [X]%?"
- [ ] Explore and Compare trade offers follow the SSN scoring order (high-value/low-cost first)
- [ ] Concession sequence gets smaller each round, not larger
- [ ] No concession in the plan is offered before the customer makes a specific ask
- [ ] Walkaway terms are defined in the SSN worksheet, not invented during the call
- [ ] Anti-pattern check passed for all three patterns
- [ ] No verbatim book passages appear in the output artifact

---

## Reference Materials

- `references/ssn-template.md` — Full SSN pre-call planning template with scoring tables
- `references/concession-antipatterns.md` — Detailed descriptions and detection signals for all three named anti-patterns
- Prerequisite skill: `diagnose-taking-control-gaps` — posture diagnosis that produces the `taking-control-diagnosis.md` this skill consumes

---

## Example Test Scenarios

**Scenario A — Enterprise software deal, CFO discount request:**
> "We have a $2M enterprise deal. The CFO called our AE yesterday and said they need a 25% discount to get board approval. We have discovery notes showing their main concern is implementation risk, not budget. The call is tomorrow."

Expected outputs: SSN worksheet completed with implementation support and extended warranty as high-value/low-cost concessions; Acknowledge and Defer script that buys time; Deepen and Broaden questions probing the board's actual concern (budget vs. implementation risk); trade offer: extended implementation support package in exchange for full contract term; concession plan with 10% / 5% / final offer structure; all three anti-pattern checks clear.

**Scenario B — Manufacturing contract renewal, procurement escalation:**
> "A $500K annual contract renewal. Procurement is demanding a 15% price reduction or they will 'go to market.' They haven't asked for anything else. Our account manager always caves on price. We have solution-capabilities.md listing 8 service elements we can trade."

Expected outputs: SSN scoring of 8 service elements (2–3 will be high-value/low-cost); proactive discounting anti-pattern flagged as risk based on account manager history; Acknowledge and Defer language; Deepen and Broaden questions to determine whether "going to market" is a real threat or an ultimatum; concession sequence starting with service element trades, price last.

**Scenario C — Late-stage deal, customer issued an ultimatum:**
> "Customer sent an email: 'Our final position is 30% off or we're done.' We've already given 10% in the last two rounds. The AE wants to give them 20% more just to close."

Expected outputs: escalating concession anti-pattern flagged (10% already given, AE wants to give 20% — escalating); ultimatum anti-pattern in customer behavior noted (but rep should not mirror it); SSN worksheet check — has the rep exhausted non-price concessions? If not, Deepen and Broaden before any further price concession; if yes, assess whether the deal meets walkaway terms; Acknowledge and Defer script to re-open the conversation rather than respond to the ultimatum directly.

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The skill was generated by the [BookForge](https://github.com/bookforge-ai/bookforge) pipeline from _The Challenger Sale_ by Matthew Dixon and Brent Adamson (Portfolio/Penguin, 2011). Content has been paraphrased and structured as an executable skill — it does not reproduce verbatim passages from the copyrighted work. Attribution required on redistribution.

## Related BookForge Skills

This skill depends on:

- `diagnose-taking-control-gaps` — produces the `taking-control-diagnosis.md` this skill consumes as input. Run it first to confirm the deal posture before negotiating.
