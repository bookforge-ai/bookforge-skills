---
name: startup-sales-process
description: "Design startup sales processes using SPIN Selling, A/B/C lead tiering, PNAME qualification, and sales funnel design. Use whenever a founder or sales lead is building a sales process, prioritizing leads, qualifying prospects, structuring sales calls, designing a sales funnel, dealing with enterprise deals, avoiding the Technology Tourist or False Change Agent traps, or transitioning from founder-led sales to a scaled sales team. Activates on phrases like 'sales process', 'sales funnel', 'SPIN selling', 'lead qualification', 'BANT', 'PNAME', 'enterprise sales', 'B2B sales', 'sales call structure', 'closing deals', 'pipeline management', 'sales methodology'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/startup-sales-process
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [19]
domain: startup-growth
tags: [startup-growth, sales, b2b-sales, sales-funnel, enterprise-sales]
depends-on: [bullseye-channel-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Target customer profile, product details, deal sizes, current sales activity"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for sales process docs and pipeline tracker"
discovery:
  goal: "Design a sales process with funnel stages, SPIN conversation structure, and lead prioritization"
  tasks:
    - "Design the sales funnel stages (generate → qualify → close)"
    - "Apply A/B/C lead tiering with time allocation"
    - "Structure sales conversations using SPIN (Situation, Problem, Implication, Need-payoff)"
    - "Qualify prospects using PNAME (Process, Need, Authority, Money, Estimated timing)"
    - "Detect Technology Tourist and False Change Agent traps"
    - "Reduce funnel blockage with specific tactics"
  audience:
    roles: [startup-founder, sales-lead, business-development]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "Founder doing sales for the first time"
      - "Startup transitioning from founder sales to team sales"
      - "Lead pipeline is mismanaged"
      - "Sales calls don't convert"
      - "Enterprise deals are getting stuck"
    prerequisites:
      - skill: bullseye-channel-selection
        why: "Sales should be selected via Bullseye based on product/price fit"
    not_for:
      - "Consumer products that close via self-serve (use content/email instead)"
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
    eval_count: 0
    assertion_count: 13
    iterations_needed: 0
---

# Startup Sales Process

## When to Use

The startup needs a sales process — either designing one from scratch or fixing one that isn't working. Sales is typically right for:

- Enterprise or high-price products ($10k+ deals)
- Products requiring consultation before purchase
- B2B with specific decision-makers
- Complex/configurable products

Sales is typically wrong for:
- Low-price consumer products
- Self-serve SaaS under $100/month
- Products with instant-use value

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product and price point:** what you sell, for how much
  → Check prompt for: product, pricing, tier
  → If missing, ask: "What does your product do, and what's the price point? Enterprise deals, SMB, mid-market?"

- **Current sales state:** who's doing sales, how many deals, win rate
  → Check prompt for: "I do all sales", "hired 2 reps", numbers
  → If missing, ask: "Who's currently doing sales, and what's the rough pipeline state?"

### Observable Context

- **Target customer profile:** industry, size, title of buyer
- **Existing sales assets:** decks, scripts, CRM

### Default Assumptions
- First-customer phase: founder does sales, 20-30 conversations to find 1 buyer
- A/B/C time allocation: 66-75% on A deals, rest on B, zero on C
- SPIN Selling conversation structure
- Deal size floor: $10k enterprise / $250/month SMB for sales to be economical

### Sufficiency Threshold

```
SUFFICIENT: product + price + current state known
PROCEED WITH DEFAULTS: product + price known, assume founder doing sales
MUST ASK: product/price is unknown
```

## Process

Use TodoWrite:
- [ ] Step 1: Design the funnel stages
- [ ] Step 2: Apply A/B/C lead tiering
- [ ] Step 3: Structure sales calls with SPIN
- [ ] Step 4: Qualify with PNAME
- [ ] Step 5: Detect wrong-first-customer traps
- [ ] Step 6: Reduce funnel blockage

### Step 1: Design the Funnel Stages

**ACTION:** Design a 3-stage funnel:

1. **Generate leads** — via other traction channels (SEO, SEM, content, targeting blogs). Cold email/calling is for first customers only; after that, leads should come from scalable channels.
2. **Qualify leads** — apply A/B/C tiering (Step 2) and PNAME qualification (Step 4) to decide where to spend time.
3. **Close leads** — structured conversations using SPIN (Step 3), with timeline commitment and specific deliverables.

Write the funnel to `sales-funnel.md` with stage definitions, handoff criteria, and time budgets.

**WHY:** Unstructured sales wastes time. Without explicit stages, reps work every lead equally, spending time on deals that will never close. The funnel structure is the basic hygiene that makes everything else possible.

### Step 2: Apply A/B/C Lead Tiering

**ACTION:** Classify every lead into one of three buckets:

- **A deals** — realistic close within 3 months. Receive **66-75% of sales rep time.** High-conviction, urgent buyer, clear budget.
- **B deals** — forecast close 3-12 months. Receive the remaining time. Build pipeline for the future.
- **C deals** — unlikely to close within 12 months. **Zero sales time.** Hand back to marketing for nurture.

Write current pipeline classification to `pipeline-tiers.md`.

**WHY:** Time is the scarcest sales resource. Without explicit tiering, reps spend time on C deals that feel interesting but won't close. The 66-75% / rest / zero allocation is a forcing function that produces more closed deals per unit time. Seller time on C deals is the single biggest source of wasted sales effort.

**IF** most deals are C → return to Bullseye. Sales may not be the right channel, or leads may be unqualified.

### Step 3: Structure Sales Calls with SPIN

**ACTION:** Use Neil Rackham's SPIN framework for structured conversations:

- **S — Situation:** 1-2 questions maximum. Establish buying context ("How's your team structured? What are you currently using?"). Over-using Situation questions signals unpreparedness and reduces close rates.
- **P — Problem:** Identify pain points ("What's frustrating about your current approach?"). Use sparingly — quickly define the problem then move on.
- **I — Implication:** Expand perceived problem magnitude ("How does this affect productivity? How many people are affected? What's the cost of not solving this?"). **This is the most important step** — it builds urgency.
- **N — Need-payoff:** Shift attention to the solution's benefits ("How would solving this help you? Whose work improves?"). Get the buyer to articulate the value themselves.

Based on Rackham's research across 35,000 sales calls.

Write scripts/questions per SPIN stage to `spin-questions.md`.

**WHY:** Most sales calls skip directly from Situation to a product pitch, missing the Problem-Implication-Need cycle that builds urgency. SPIN is the framework that makes the buyer talk themselves into the purchase, rather than the seller pushing them. Rackham's research showed it increased close rates meaningfully across 35,000 calls.

### Step 4: Qualify Prospects with PNAME

**ACTION:** Before investing sales time in any deal, check the 5 PNAME factors:

- **P — Process:** How does this company buy solutions? (Procurement process, approval chain)
- **N — Need:** How badly do they need a solution? Is the pain acute or abstract?
- **A — Authority:** Who has purchase authority? Is the person you're talking to the decision-maker?
- **M — Money:** Do they have budget? What does not solving it cost them?
- **E — Estimated timing:** What are budget and decision timelines?

If any factor is missing, the deal is likely C-tier.

**WHY:** Deals fall through because one of the 5 factors was wrong — no authority, no budget, no urgency. Catching missing factors upfront saves weeks of wasted sales time. PNAME is a specific pre-close checklist that forces clarity.

### Step 5: Detect Wrong-First-Customer Traps

**ACTION:** Two specific traps from Sean Murphy:

**Technology Tourist:** Prospect invites you in but has no interest in buying. They want to learn about the technology for intellectual or professional curiosity. Signal: they ask deep product questions but never discuss implementation or budget. Test question: "Have you brought other technology into your company?" — if the answer is "No, this would be our first," proceed cautiously.

**False Change Agent:** Someone claims to be a change agent who will drive your product through the org. Reality: they have no authority or organizational credibility. Signal: they oversell their influence ("I can make this happen"). Test: "How long have you been here? Have you implemented similar things before?" A 6-month-tenure person cannot be a change agent.

**WHY:** Both traps waste months of sales effort. The prospect looks real — meetings happen, demos happen, emails get returned — but the deal never closes because the underlying conditions don't exist. Naming the traps makes them detectable. Founders who don't know the patterns get burned repeatedly.

### Step 6: Reduce Funnel Blockage

**ACTION:** Common blockages and specific tactics:

- **IT install friction** → offer SaaS/cloud version
- **Risk aversion** → free trials, reference customers, case studies
- **Budget approval** → ROI calculators, business case templates
- **Competitive comparison** → competitive battle cards, comparison sheets
- **Long procurement** → channel partners, reseller agreements
- **Price resistance** → low intro price (<$250/mo SMB, <$10k enterprise floor)
- **Need clarification** → detailed FAQs, demo videos

Write blockage-specific tactics to `funnel-blockage-plan.md`.

**WHY:** Each blockage has a specific fix. Generic "sales training" doesn't solve specific blockages. Identifying which blockage is costing the most deals (by postmortem on lost deals) and applying the specific fix produces measurable improvement.

## Inputs

- Product and price point
- Target customer profile
- Current sales state (pipeline, team, metrics)

## Outputs

Five markdown files:

1. **`sales-funnel.md`** — 3-stage funnel with handoff criteria
2. **`pipeline-tiers.md`** — A/B/C classification of current deals
3. **`spin-questions.md`** — Prepared SPIN questions per call type
4. **`pname-checklist.md`** — PNAME qualification applied to top deals
5. **`funnel-blockage-plan.md`** — Specific blockage tactics

## Key Principles

- **A deals get 66-75% of time. C deals get zero.** WHY: Time is scarce. Misallocating it to C deals is the single biggest sales productivity drain. The explicit percentage is a forcing function.

- **SPIN > traditional pitches.** The buyer must articulate the value themselves. WHY: Buyers rationalize away seller claims; they don't rationalize away their own. SPIN makes the buyer do the persuasion.

- **Implication is the most important SPIN stage.** This is where urgency is built. WHY: Without Implication questions, the problem stays abstract and the deal stays in "interested but not urgent." Implication escalates the perceived cost of inaction.

- **Never skip PNAME on enterprise deals.** All 5 factors must be present. WHY: Deals with missing factors feel real but don't close. Catching the missing factor upfront saves weeks or months.

- **Name the wrong-first-customer traps.** Technology Tourist and False Change Agent are specific, detectable patterns. WHY: Unnamed patterns repeat indefinitely. Named patterns can be matched against and flagged.

- **Founder sales is for first 10-20 customers only.** After that, it's a data-gathering exercise that should hand off to hired reps or channels. WHY: Founder sales doesn't scale and founder time has higher-leverage uses. The handoff point is when you know what works well enough to script it.

## Examples

**Scenario: Founder on first enterprise deal**

Trigger: "Our first enterprise prospect is asking for a 30-minute call. They work at a Fortune 500. I've never done sales. What do I do?"

Process: (1) Run PNAME before the call — Process unknown, Need unclear, Authority unclear, Money unknown, Timing unknown. All 5 need answers. (2) SPIN structure: plan 2 Situation questions, 3 Problem questions, 4 Implication questions, 3 Need-payoff questions. (3) Detect traps: ask "have you brought other technology into your company?" and "how long have you been at the company?" (4) End of call: commit to specific deliverable with specific timeline ("If I ship X in 2 weeks, will you commit to a 30-day pilot?"). Get a yes/no.

Output: Call prep doc with PNAME questions, SPIN question list, trap detection script, and specific close question.

**Scenario: Pipeline is full of C deals**

Trigger: "We have 50 deals in our pipeline but only close 2 per quarter. What's wrong?"

Process: (1) A/B/C classify all 50. Likely result: 5 A, 10 B, 35 C. (2) 35 C deals have been consuming sales time with no payoff. Move them all to "marketing nurture" — zero sales time. (3) Reallocate saved time to the 5 A deals. (4) PNAME each A deal to confirm all 5 factors present; if not, downgrade to B. (5) Apply SPIN to next A-deal calls, especially Implication questions to build urgency.

Output: Pipeline restructuring with dramatic time reallocation to A deals.

**Scenario: Technology Tourist trap**

Trigger: "We've been in discussions with a Fortune 500 for 4 months. They keep asking for detailed demos but never move forward. What do I do?"

Process: (1) Classic Technology Tourist pattern. Test: ask "Have you brought similar technology into your company before?" If no → likely tourist. (2) Also ask: "What's your timeline for making a decision?" If vague → more tourist signals. (3) Apply time budget: this deal is C. Reallocate sales time. Leave the door open with a marketing nurture sequence. (4) Use the conversation as a data source for the product — tourists ask real questions, they just don't buy. (5) Move on.

Output: Tourist identification, graceful disengagement plan, reallocation to real deals.

## References

- For full SPIN question templates and PNAME qualification sheet, see [references/sales-templates.md](references/sales-templates.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select Sales as a channel deliberately
- `clawhub install bookforge-business-development-pipeline` — BD vs Sales distinction
- `clawhub install bookforge-startup-traction-strategy-by-phase` — Sales is Phase I first-customer tactic

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
