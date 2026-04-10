---
name: marketing-plan-canvas
description: "Use this skill to build, assemble, or audit a complete 9-square
  1-Page Marketing Plan canvas for any small or medium business. Triggers when a
  user asks to create a marketing plan, build a 1-page marketing plan, use the
  1PMP framework, fill in the 9-square canvas, create a marketing strategy, get
  a complete marketing plan, start marketing a business, fix broken marketing,
  audit their marketing, or doesn't know where to start with marketing. Also
  triggers for: 'marketing plan', '1-page marketing plan', 'create marketing
  plan', 'marketing strategy', 'complete marketing plan', '1PMP canvas', '9
  square canvas', 'marketing plan template', 'small business marketing plan',
  'need a marketing plan', 'don't know where to start with marketing', 'my
  marketing is a mess', 'random acts of marketing', 'Allan Dib framework',
  'before during after marketing', 'prospect lead customer framework', 'I have
  no marketing system', 'pull my marketing together', 'marketing audit'. This
  is the hub skill — invoke it whenever a user wants end-to-end marketing
  clarity, not just one tactical element."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/marketing-plan-canvas
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan"
    authors: ["Allan Dib"]
    chapters: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
tags:
  - marketing
  - marketing-plan
  - strategy
  - small-business
  - meta-framework
depends-on:
  - target-market-selection-pvp-index
  - marketing-message-and-usp-crafting
  - advertising-media-roi-framework
  - lead-capture-ethical-bribe-design
  - lead-nurture-sequence-design
  - sales-conversion-trust-system
  - customer-experience-systems-design
  - customer-lifetime-value-growth
  - referral-system-design
  - irresistible-offer-builder
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: >
        Business description at minimum (one paragraph: what the business does,
        who it currently serves, what it sells). Richer inputs are any existing
        outputs from the 10 dependent skills — the skill will integrate whatever
        exists and ask for minimums on whatever is missing.
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: >
    Document set — business description and any existing skill outputs in
    markdown. No code execution required. Can produce a minimum-viable canvas
    in a single conversation from nothing but a business description.
discovery:
  goal: >
    Guide the user through all 9 squares of the 1-Page Marketing Plan, produce
    a coherent single-document canvas (marketing-plan-canvas.md), and bias
    toward shipping an 80% plan over endlessly refining a perfect one.
  tasks:
    - "Explain the 9-square framework and 3-act structure to the user"
    - "Assess current state per square: have output / partial / missing"
    - "For each square, decide: reference existing skill output, invoke
       dedicated skill, or gather minimum viable input directly from user"
    - "Fill all 9 squares in Act order: Before (1-2-3), During (4-5-6),
       After (7-8-9)"
    - "Perform coherence review across all 9 squares"
    - "Write marketing-plan-canvas.md — the single output document"
    - "Apply 80-percent-ships principle — ship the plan, iterate later"
  audience:
    roles:
      - small-business-owner
      - solopreneur
      - entrepreneur
      - freelancer
      - startup-founder
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User wants a complete marketing plan from scratch"
      - "User has partial marketing work and wants to integrate it"
      - "User's marketing is broken or random and they want a system"
      - "User is auditing their marketing against a proven framework"
      - "User mentions the 1-Page Marketing Plan or Allan Dib"
    prerequisites: []
    not_for:
      - "Enterprise/large company brand marketing with multi-million-dollar
         budgets (this framework is explicitly designed for small to medium
         businesses using direct response marketing)"
      - "Detailed execution of a single square — invoke the dedicated
         component skill directly instead"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 100
      baseline: 21.4
      delta: 78.6
    tested_at: "2026-04-09"
    eval_count: 1
    assertion_count: 14
    iterations_needed: 1
---

# The 1-Page Marketing Plan Canvas

A meta-orchestrator that assembles all 9 squares of the direct response
marketing lifecycle into a single canvas document. Covers the full prospect
→ lead → customer journey across three acts: Before (get them to KNOW you),
During (get them to LIKE you and buy), After (get them to TRUST you, buy
again, and refer others).

This skill works in three starting states — from nothing, from partial work,
or as an audit of an existing plan — and always produces a single output
document: `marketing-plan-canvas.md`.

---

## When to Use

Use this skill when the goal is the **complete marketing system**, not one
piece. It is the entry point for any of these situations:

- **Starting from scratch:** no marketing plan, no clarity, just a business
  description
- **Integrating partial work:** some squares filled via other skills, but no
  unified view
- **Auditing a broken plan:** marketing exists but is random, fragmented, or
  not converting

Do NOT use this skill when the user wants deep work on a single square.
Invoke the dedicated component skill directly for that (e.g.,
`target-market-selection-pvp-index` for square #1 alone).

---

## Context and Input Gathering

Before starting, determine the user's starting state:

**Minimum viable input (always ask if absent):**
- What does your business do, in one sentence?
- Who do you currently serve (rough description)?
- What do you sell, and at roughly what price?

**Check for existing outputs from component skills.** If the user has worked
through any of the 9 dependent skills, those outputs become the content for
the corresponding square. Ask:

> "Have you worked through any of the individual marketing squares before?
> If so, share those documents and I'll integrate them. Otherwise I'll ask
> you the minimum question for each square."

**For each square, the decision rule is:**
1. IF a dedicated skill output exists → reference it, extract a 3-5 bullet
   summary for the canvas
2. ELSE IF the user wants depth on this square → invoke the dedicated skill
   before proceeding
3. ELSE → ask the minimum viable question and record the answer directly

---

## Process

### Step 1 — Explain the Framework (WHY: shared vocabulary prevents wasted effort)

Orient the user before gathering any input. Explain:

The 1-Page Marketing Plan organizes all marketing into 9 squares across
3 acts, reflecting the 3 stages every customer passes through:

```
┌──────────────────────────────────────────────────────────────┐
│                  MY 1-PAGE MARKETING PLAN                     │
├─────────────────┬──────────────────┬────────────────────────┤
│  ACT I: BEFORE  │  (Prospect)      │  Goal: they KNOW you   │
├─────────────────┼──────────────────┼────────────────────────┤
│ #1 My Target    │ #2 My Message    │ #3 Media to            │
│    Market       │    to Them       │    Reach Them          │
├─────────────────┴──────────────────┴────────────────────────┤
│  ACT II: DURING │  (Lead)          │  Goal: they LIKE you   │
├─────────────────┬──────────────────┬────────────────────────┤
│ #4 Lead         │ #5 Lead          │ #6 Sales               │
│    Capture      │    Nurture       │    Conversion          │
├─────────────────┴──────────────────┴────────────────────────┤
│  ACT III: AFTER │  (Customer)      │  Goal: they TRUST you  │
├─────────────────┬──────────────────┬────────────────────────┤
│ #7 World-Class  │ #8 Increase      │ #9 Orchestrate         │
│    Experience   │    Customer LTV  │    Referrals           │
└─────────────────┴──────────────────┴────────────────────────┘
```

Key insight: this is a direct response framework for small and medium
businesses. It is NOT mass marketing or branding. Every square is designed
to produce a measurable, trackable result.

### Step 2 — Assess Current State (WHY: avoid redoing completed work)

For each of the 9 squares, determine the status:
- **Have:** a skill output or documented answer exists
- **Partial:** some thinking done but not fully worked through
- **Missing:** no prior work

Present a quick status table to the user and confirm before proceeding.

### Step 3 — Act I: Before (squares 1, 2, 3 in order)

**WHY for the order:** target market must be decided before writing a message,
and media channel only makes sense once you know who you're reaching and
what you're saying. Reversing this order is the definition of "random acts
of marketing."

**Square #1 — Target Market**
- Skill: `target-market-selection-pvp-index`
- IF output exists → extract: primary target segment + customer avatar
  (3-5 bullets)
- ELSE IF user wants depth → invoke `target-market-selection-pvp-index`
- ELSE → ask: *"Who is your primary target customer? Describe them in one
  sentence — their role, their problem, their situation."*
- Note: `irresistible-offer-builder` outputs feed into the offer framing
  for this segment (cross-reference).

**Square #2 — Message to Target Market**
- Skill: `marketing-message-and-usp-crafting`
- IF output exists → extract: USP statement + headline (3-5 bullets)
- ELSE IF user wants depth → invoke `marketing-message-and-usp-crafting`
- ELSE → ask: *"What is your unique selling proposition in 1-2 sentences?
  Why should your target customer choose you over every alternative,
  including doing nothing?"*
- Note: `irresistible-offer-builder` is the cross-cutting input here —
  a strong offer makes the message concrete.

**Square #3 — Advertising Media**
- Skill: `advertising-media-roi-framework`
- IF output exists → extract: primary channels + budget allocation approach
  (3-5 bullets)
- ELSE IF user wants depth → invoke `advertising-media-roi-framework`
- ELSE → ask: *"Where will you reach your target customers? Name 1-2
  specific channels (e.g., Facebook ads, LinkedIn, local newspaper,
  email list, Google search)."*

### Step 4 — Act II: During (squares 4, 5, 6 in order)

**WHY for the order:** leads must be captured before they can be nurtured,
and nurturing must happen before conversion. The sequence is the system.

**Square #4 — Lead Capture**
- Skill: `lead-capture-ethical-bribe-design`
- IF output exists → extract: lead magnet name + capture mechanism (3-5
  bullets)
- ELSE IF user wants depth → invoke `lead-capture-ethical-bribe-design`
- ELSE → ask: *"How do you capture interested prospects' contact details?
  What do you offer them in exchange (e.g., free report, checklist,
  webinar, free consultation)?"*

**Square #5 — Lead Nurture**
- Skill: `lead-nurture-sequence-design`
- IF output exists → extract: nurture medium + sequence length + cadence
  (3-5 bullets)
- ELSE IF user wants depth → invoke `lead-nurture-sequence-design`
- ELSE → ask: *"How do you follow up with leads who haven't bought yet?
  What's your current sequence (email, phone, direct mail) and how long
  does it run?"*

**Square #6 — Sales Conversion**
- Skill: `sales-conversion-trust-system`
- IF output exists → extract: conversion mechanism + trust elements
  (3-5 bullets)
- ELSE IF user wants depth → invoke `sales-conversion-trust-system`
- ELSE → ask: *"How do you convert a nurtured lead into a paying customer?
  What's the final step that gets someone to buy (sales call, proposal,
  checkout page, in-person meeting)?"*
- Note: `irresistible-offer-builder` is a direct feed into square #6 —
  the offer structure determines conversion rate.

### Step 5 — Act III: After (squares 7, 8, 9 in order)

**WHY for the order:** experience must exist before you can measure
lifetime value, and referrals only happen when the experience is strong
enough to earn recommendation. Act III is where most businesses leave
the most money on the table.

**Square #7 — World-Class Experience**
- Skill: `customer-experience-systems-design`
- IF output exists → extract: key experience systems + wow moments (3-5
  bullets)
- ELSE IF user wants depth → invoke `customer-experience-systems-design`
- ELSE → ask: *"What happens after someone becomes a customer? How do you
  make sure they feel looked after and impressed — not just served?"*

**Square #8 — Increase Customer Lifetime Value**
- Skill: `customer-lifetime-value-growth`
- IF output exists → extract: upsell/cross-sell paths + LTV levers (3-5
  bullets)
- ELSE IF user wants depth → invoke `customer-lifetime-value-growth`
- ELSE → ask: *"What do customers buy after their first purchase? Do you
  have a higher-tier offer, a subscription, or a natural next product
  they should move to?"*

**Square #9 — Orchestrate and Stimulate Referrals**
- Skill: `referral-system-design`
- IF output exists → extract: referral mechanism + incentive structure
  (3-5 bullets)
- ELSE IF user wants depth → invoke `referral-system-design`
- ELSE → ask: *"How do you generate referrals? Is there a systematic
  process, or does it happen by accident when a happy customer mentions
  you?"*

### Step 6 — Coherence Review (WHY: incoherent plans waste money faster than no plan)

Before writing the canvas document, check:

1. **Market ↔ Message match:** Does the USP in square #2 speak directly
   to the pain of the target in square #1? If they are misaligned, the
   advertising in square #3 will reach the right people but say the wrong
   thing.

2. **Message ↔ Media match:** Does the channel in square #3 actually reach
   the target from square #1? (Example: LinkedIn reaches B2B professionals;
   Facebook reaches consumers and local businesses. Wrong channel =
   broadcasting to the wrong audience.)

3. **Lead magnet ↔ Target match:** Does the ethical bribe in square #4
   appeal to the specific target from square #1? A generic lead magnet
   attracts generic, low-quality leads.

4. **Offer ↔ Message consistency:** Does the irresistible offer (cross-
   cutting) back up the promise made in square #2? The message sets
   expectations; the offer must fulfil them.

5. **After phase completeness:** At least one element should exist in each
   of squares 7, 8, and 9. A business that excels at Before and During but
   ignores After is leaving its most profitable customers under-served.

Flag any misalignments to the user before writing the canvas. Suggest the
appropriate dedicated skill to resolve each gap, or ask the minimum
corrective question.

### Step 7 — Write `marketing-plan-canvas.md` (WHY: a plan that exists only in conversation cannot be executed)

Produce the single output document. Format:

```
# My 1-Page Marketing Plan
Business: [name]
Date: [date]
Status: [Draft / In Progress / Live]

---

## ACT I: BEFORE — Getting Prospects to KNOW You

| Square | Content |
|--------|---------|
| #1 Target Market | [3-5 bullets from skill output or user input] |
| #2 Message | [3-5 bullets: USP, headline, core promise] |
| #3 Media | [Top 1-2 channels, allocation rationale] |

---

## ACT II: DURING — Getting Leads to LIKE You and Buy

| Square | Content |
|--------|---------|
| #4 Lead Capture | [Lead magnet name, capture mechanism] |
| #5 Lead Nurture | [Sequence summary: medium, cadence, length] |
| #6 Sales Conversion | [Conversion mechanism, trust elements, offer summary] |

---

## ACT III: AFTER — Getting Customers to TRUST You, Buy Again, Refer

| Square | Content |
|--------|---------|
| #7 World-Class Experience | [Key experience systems, wow moments] |
| #8 Increase Customer LTV | [Upsell path, retention mechanism, subscription offer] |
| #9 Orchestrate Referrals | [Referral mechanism, incentive, timing] |

---

## Cross-Cutting: Irresistible Offer
[Summary of offer structure — feeds squares #2 and #6]
Source: irresistible-offer-builder skill output (if available)

---

## Coherence Notes
[Any misalignments flagged in Step 6, with recommended next actions]

---

## Next Actions
[Prioritized list: which squares need deeper work via dedicated skills]
```

For each square, if a dedicated skill output exists, add a reference link:
`→ Full detail: skills/[skill-name]/[output-file].md`

### Step 8 — Apply the 80% Principle (WHY: a shipped plan beats a perfect draft)

After writing the canvas, make this explicit to the user:

> "This plan is ready to execute. It is 80% complete — and 80% out the
> door beats 100% in the drawer every time. Marketing is not an event; it
> is a process. Start executing Act I immediately. Refine as you get
> real-world feedback. The squares that are thin will become clearer once
> you are in market."

Identify the single highest-leverage next action (usually: get the target
market clear first if missing, or start running Act I media if it exists).

---

## Inputs

**Minimum required:**
- Business description (one paragraph): what the business does, who it
  serves, what it sells

**Higher-value inputs (optional, but each one reduces the questions asked):**
- Outputs from any of the 10 dependent skills (in full or as summaries)
- Current marketing assets: ads, lead magnets, email sequences, sales
  scripts, onboarding processes

**Not required:**
- Prior marketing experience
- Large budget
- A completed business plan

---

## Outputs

**Primary output:**
- `marketing-plan-canvas.md` — single document with all 9 squares filled
  at minimum viable detail, plus coherence notes and next actions

**The output has two levels of completeness:**
- **Minimum viable canvas:** all 9 squares answered with 3-5 bullets each,
  gathered directly from user in this skill. Fast to produce; good enough
  to start executing.
- **Integrated canvas:** 9 squares populated from dedicated skill outputs,
  with references to full detail documents. Deeper; better for businesses
  that have worked through the component skills.

Both are valid outputs of this skill. The goal is a canvas that can be
stuck on a wall and used to guide daily marketing decisions.

---

## Key Principles

**Systematic, not random**
Random acts of marketing — trying Facebook ads this week, a podcast next
week, a direct mail campaign the month after — with no connecting strategy
is the single biggest reason small business marketing fails. The 9-square
canvas is the strategy that connects all tactics.

**Direct response, not mass marketing**
This framework is designed for small and medium businesses. It is NOT
brand marketing. Every element must be trackable and measurable. If you
cannot measure whether a square is working, it is not a direct response
element — revisit it.

**80% ships, 100% stays in the drawer**
Paralysis by analysis kills more marketing plans than bad strategy. A
good-enough plan executed today beats a perfect plan executed never.
Set a deadline: this canvas must be complete within one session. Gaps
become the next iteration, not a reason to delay.

**Iterate, don't perfect**
The first version of the canvas is a hypothesis. Real customers will
tell you what to change. Treat the canvas as a living document — review
it quarterly, update squares that are underperforming, and add depth via
dedicated skills when a specific square becomes a bottleneck.

**Marketing is a process, not an event**
High-growth businesses make marketing a daily routine. Failed businesses
treat marketing as something they do when revenue drops. The canvas gives
you the system; you provide the consistent execution.

---

## Examples

### Example A — Starting from Scratch

**Situation:** User runs a bookkeeping business for small trades businesses
(plumbers, electricians). No marketing plan. Gets clients by word of mouth.

**How this skill runs:**
1. Explain the 3-act framework.
2. Assess: all 9 squares missing.
3. Ask the minimum question for each square — takes ~15 minutes.
4. Coherence check: confirm the message in #2 speaks to tradesperson pain
   (cash flow visibility, ATO compliance stress) not generic bookkeeping.
5. Write canvas: minimum viable, 9 squares filled with user's answers.
6. Flag: square #5 (nurture) is thin — recommend invoking
   `lead-nurture-sequence-design` as next step.
7. Ship the plan. Identify Act I (LinkedIn for local trades) as first
   execution priority.

### Example B — Integrating Existing Work

**Situation:** User has outputs from `target-market-selection-pvp-index`,
`marketing-message-and-usp-crafting`, and `irresistible-offer-builder`.
Squares #1, #2, and the cross-cutting offer are done. Squares #3-9 need
work.

**How this skill runs:**
1. Read in the three existing skill outputs.
2. Assess: #1 and #2 have full outputs; cross-cutting offer done.
3. Summarize #1 and #2 into canvas format (3-5 bullets each).
4. Ask minimum questions for squares #3-9.
5. Coherence check: verify the offer (from `irresistible-offer-builder`)
   is consistent with the message in #2.
6. Write integrated canvas with references to the two full skill outputs.
7. Prioritize: squares #4 and #5 are thin — recommend
   `lead-capture-ethical-bribe-design` and `lead-nurture-sequence-design`.

### Example C — Auditing a Broken Plan

**Situation:** User has been running Facebook ads for 6 months with no
results. They have a landing page, some emails, and a sales process. Their
marketing "isn't working."

**How this skill runs:**
1. Map what they have to the 9 squares.
2. Assessment reveals: square #1 is vague ("small business owners"), #2
   has no USP (their ads look like mass marketing), #3 is Facebook only
   with no tracking.
3. Coherence failure: message (#2) is generic; media (#3) is running but
   without a targeted message, it attracts low-quality leads.
4. The root cause is that squares #1 and #2 are broken — not the Facebook
   channel.
5. Recommend: invoke `target-market-selection-pvp-index` to sharpen the
   niche, then `marketing-message-and-usp-crafting` to rebuild the message
   before spending another dollar on ads.
6. Write an audit canvas documenting current state and gap analysis.

---

## References

- `target-market-selection-pvp-index` — square #1: niche selection with
  the PVP Index (Personal fulfillment, Value, Profitability)
- `marketing-message-and-usp-crafting` — square #2: unique selling
  proposition, headline, and message construction
- `advertising-media-roi-framework` — square #3: channel selection and
  media ROI measurement
- `lead-capture-ethical-bribe-design` — square #4: lead magnets and
  ethical bribe design
- `lead-nurture-sequence-design` — square #5: multi-touch nurture
  sequences for unconverted leads
- `sales-conversion-trust-system` — square #6: trust-building conversion
  systems for the final buying decision
- `customer-experience-systems-design` — square #7: world-class experience
  delivery systems
- `customer-lifetime-value-growth` — square #8: upsell, cross-sell, and
  retention mechanisms
- `referral-system-design` — square #9: systematic referral orchestration
- `irresistible-offer-builder` — cross-cutting: offer construction that
  feeds squares #2 (message) and #6 (conversion)
- Source: *The 1-Page Marketing Plan* by Allan Dib — Introduction
  (framework, canvas, 3 acts), Conclusion (anti-patterns, 80% principle,
  marketing-as-process). Canvas downloadable at 1pmp.com.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-target-market-selection-pvp-index`
- `clawhub install bookforge-marketing-message-and-usp-crafting`
- `clawhub install bookforge-irresistible-offer-builder`
- `clawhub install bookforge-advertising-media-roi-framework`
- `clawhub install bookforge-lead-capture-ethical-bribe-design`
- `clawhub install bookforge-lead-nurture-sequence-design`
- `clawhub install bookforge-sales-conversion-trust-system`
- `clawhub install bookforge-customer-experience-systems-design`
- `clawhub install bookforge-customer-lifetime-value-growth`
- `clawhub install bookforge-referral-system-design`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
