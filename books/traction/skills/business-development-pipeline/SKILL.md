---
name: business-development-pipeline
description: "Build a business development pipeline with 5 partnership types, attribute-based partner selection, and a 9-step BD process. Use whenever a founder or BD lead is planning partnerships, pursuing integration deals, negotiating licensing, structuring joint ventures, setting up distribution deals, sourcing supply partnerships, or transitioning from traditional BD to low-touch self-serve BD. Activates on phrases like 'business development', 'BD', 'partnerships', 'strategic partner', 'integration partner', 'licensing deal', 'distribution partner', 'joint venture', 'channel partner', 'co-marketing', 'white label', 'BD deal'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/business-development-pipeline
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [18]
domain: startup-growth
tags: [startup-growth, business-development, partnerships, strategic-alliances, channel-partnerships]
depends-on: [bullseye-channel-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Company objectives, candidate partners, existing partnerships"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for BD pipeline spreadsheet and deal docs"
discovery:
  goal: "Build a BD pipeline with partner attributes, prioritization, outreach plan, and term sheets"
  tasks:
    - "Define company objectives BD should serve"
    - "Identify which of the 5 partnership types fit"
    - "Build pipeline by partner attributes (not brand names)"
    - "Plan warm introductions via investors/advisors"
    - "Negotiate simple 1-page term sheet"
    - "Document 'how the deal was done' post-close"
    - "Plan Low-touch BD 2.0 transition"
  audience:
    roles: [startup-founder, bd-lead, head-of-partnerships]
    experience: intermediate
  when_to_use:
    triggers:
      - "User is pursuing strategic partnerships"
      - "User needs distribution via a larger partner"
      - "Integration deal negotiation"
      - "Licensing or joint venture consideration"
    prerequisites:
      - skill: bullseye-channel-selection
        why: "BD should be selected via Bullseye"
    not_for:
      - "Pure revenue-for-product transactions (use sales instead)"
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
    assertion_count: 11
    iterations_needed: 0
---

# Business Development Pipeline

## When to Use

The startup is pursuing partnerships — not pure sales. BD differs from sales: **BD exchanges value through partnerships; sales exchanges dollars for a product.** Use this skill when:

- A partner has distribution, inventory, or brand you need
- You need integration deals to complete a product story
- Licensing (either direction) is on the table
- Planning a joint venture or co-marketing arrangement

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Company objectives:** what BD should serve
  → Check prompt for: "need distribution", "want integration with", "raising next round"
  → If missing, ask: "What specific company objectives should BD help achieve? Distribution? Brand credibility? Product completeness? Inventory?"

- **Current state:** existing partnerships, team resources
  → Check prompt for: partners, BD lead, prior deals

### Observable Context

- **Product category:** determines which partners are relevant
- **Investor/advisor network:** source of warm introductions

### Default Assumptions
- Partners identified by attributes, not brand names
- Pipeline size: 10-20 focused partners, not 100+
- Warm introductions only for initial outreach
- 1-page term sheets, not 20-page contracts

### Sufficiency Threshold

```
SUFFICIENT: company objectives + candidate attributes known
PROCEED WITH DEFAULTS: objectives known, infer partner attributes
MUST ASK: no clear objective for BD
```

## Process

Use TodoWrite:
- [ ] Step 1: Define company objectives BD serves
- [ ] Step 2: Pick the 1-2 partnership types that fit
- [ ] Step 3: Build pipeline by partner attributes
- [ ] Step 4: Get warm introductions
- [ ] Step 5: Negotiate simple term sheets
- [ ] Step 6: Document deal completion
- [ ] Step 7: Plan Low-touch BD 2.0

### Step 1: Define Company Objectives

**ACTION:** Start by listing the 1-3 key company objectives BD should serve. Every BD deal should map to an objective. Common objectives:

- **Growth / distribution** — need access to a larger customer base
- **Revenue** — shared revenue models, white-label
- **Product** — integration completes a product story
- **Credibility** — partnership with a recognizable brand
- **Inventory / supply** — access to key inputs (content, data, goods)

Work backwards: "What does our fundraising deck need to show in 12 months?" Use this to define which partnerships are strategic.

**WHY:** BD is easy to do badly — partnerships that feel prestigious but don't advance company goals. Tying BD to specific objectives prevents "shiny partnership" traps where you spend 3 months negotiating a deal that doesn't matter.

### Step 2: Pick the 1-2 Partnership Types That Fit

**ACTION:** The 5 partnership types (see [references/partnership-types.md](references/partnership-types.md)):

1. **Standard Partnership** — joint product enhancement (Nike+/Apple)
2. **Joint Venture** — new product built together (Starbucks/Pepsi Frappuccino)
3. **Licensing** — brand or IP licensed (Starbucks ice cream, Spotify music)
4. **Distribution Deal** — product/service exchanged for customer access (Groupon, Kayak/AOL)
5. **Supply Partnership** — access to key inputs (Half.com used books, YouTube channel partners)

Pick the 1-2 that match the objective. Don't pursue all 5.

**WHY:** Different deal types have different negotiation patterns, legal structures, and risk profiles. Mixing types produces muddled deals that don't close cleanly. Choosing type upfront aligns expectations.

### Step 3: Build the Pipeline by Partner Attributes

**ACTION:** Instead of listing brand names ("let's partner with Microsoft"), list partner *attributes*:

Example attribute filter: "Internet retailers ranked 50-250 on IR500, with shipping infrastructure in North America, revenue $10M-$500M, distributing consumer electronics"

Build a pipeline of 10-20 partners matching these attributes. Score by:
- Strategic fit to company objective
- Ease of reach (warm intro available?)
- Deal size / impact
- Probability of close

Write the pipeline to `bd-pipeline.csv` with columns: company, type, contact, size, relevance, ease, priority_score.

**WHY:** Attribute-based selection avoids the "big brand bias" where founders chase marquee partners who won't take the meeting. Attribute selection produces partners who are the right size, the right industry, and the right stage — who actually return calls. Chris Fralic (Half.com): the pipeline should prioritize fit, not fame.

### Step 4: Get Warm Introductions

**ACTION:** For every partner in the pipeline, identify a warm introduction path:

- Investors who know the partner
- Advisors with relationships
- Former colleagues now at the partner
- Conference connections
- Customer mutual friends

Prepare a 1-page proposal overview the introducer can forward. Make it easy to pass along.

**Never cold-email BD prospects.** Cold sales works; cold BD doesn't. Partners respond to introductions, not pitches.

**WHY:** BD deals involve trust and strategic alignment, which cold contact cannot establish. Warm introductions signal credibility — the introducer's reputation is at stake, so the recipient pays attention. Cold BD outreach produces 1-2% response rates; warm intros produce 40%+.

**IF** no warm intro path exists → build one. Attend industry events, join investor networks, or trade favors with advisors.

### Step 5: Negotiate Simple Term Sheets

**ACTION:** Keep initial term sheets to 1 page. Include:

- **Deal lifetime** — duration of the partnership
- **Exclusivity** — exclusive or non-exclusive, and to what scope
- **Payment structure** — revenue share, flat fee, equity swap
- **Commitment level** — what each side commits to deliver
- **Guarantees** — any minimums or SLAs
- **Revenue share** — if applicable, specific percentages

Long contracts (20+ pages) at initial stage kill deals. 1-page term sheets get signed; 20-page contracts get stuck in legal review for months.

**WHY:** Complexity kills early-stage BD. The goal is to establish clear terms fast so both sides can start executing. Lawyers can add detail later. Over-engineered initial contracts signal distrust and consume negotiation energy that should be spent on the relationship.

### Step 6: Document "How the Deal Was Done"

**ACTION:** After closing, write a memo documenting:
- How the partnership came together (intro path, first meeting, breakthroughs)
- Who the key contacts were
- Sticking points encountered and how they were resolved
- What interested the partner (the specific hook)
- What the next 90 days look like

Save to `bd-deal-postmortem.md` per deal.

**WHY:** BD knowledge is tacit. Founders who do 3 deals and don't document anything lose the patterns. Documenting creates a playbook for the next deal. Chris Fralic's (Half.com) approach: every closed deal gets a "how it was done" memo, and those memos inform the next negotiation.

### Step 7: Plan Low-Touch BD 2.0

**ACTION:** After 2-3 traditional partnerships establish the model, transition to self-serve BD. Build API integrations, embed codes, or partner portals that enable new partners to integrate without custom negotiation.

Delicious/Mozilla example: after manual integration with Mozilla, Delicious built an API that let any partner integrate at scale without BD team involvement.

**WHY:** Manual BD doesn't scale. Every new partner means new negotiations, contracts, custom integrations. Low-touch BD converts the manual work into a product that partners onboard themselves. This is the transition from BD as a channel to BD as a product surface.

## Inputs

- Company objectives (specifically what BD serves)
- Partner attribute criteria
- Warm intro network (investors, advisors)

## Outputs

Five files:

1. **`bd-objectives.md`** — Company objectives BD serves
2. **`bd-pipeline.csv`** — Prioritized partner list by attributes
3. **`bd-term-sheets.md`** — 1-page term sheets per active deal
4. **`bd-deal-postmortem.md`** — "How the deal was done" memo per closed deal
5. **`bd-low-touch-plan.md`** — Transition plan to self-serve integrations (if scale warrants)

## Key Principles

- **BD is not sales.** BD exchanges value; sales exchanges money. WHY: Confusing the two leads to wrong conversations — pitching a sales deal to a BD prospect, or vice versa. The distinction determines everything from introduction style to contract structure.

- **Attributes, not brand names.** Pipeline by fit, not by prestige. WHY: Big-brand BD targets rarely return calls to early-stage startups. Attribute-based pipelines produce partners who are the right size and actually engage.

- **Warm intros only.** Cold BD doesn't work. WHY: BD requires trust that cold outreach can't establish. The investor/advisor who introduces you has reputation at stake, which is the credibility substitute.

- **1-page term sheets at the start.** Long contracts kill deals. WHY: Complexity at the negotiation stage produces legal delays and fatigue. Simple terms get signed; complex ones get stuck. Detail is added later.

- **Every deal gets a "how it was done" memo.** BD knowledge is tacit and perishable. WHY: Without documentation, patterns are lost and each deal is a first-time experience. Documentation creates the BD playbook.

- **Transition to low-touch BD 2.0 after 2-3 deals.** Manual BD doesn't scale past a handful. WHY: Every new partner is a bespoke negotiation unless you build a self-serve layer. At scale, BD must become a product surface.

## Examples

**Scenario: Early-stage SaaS needing integration partners**

Trigger: "We built a project management tool and need integrations with Slack, Google Drive, Notion. How do we do BD?"

Process: (1) Objective: product completeness (integration story). (2) Type: Standard Partnership (product enhancement). (3) Attributes: top 20 tools in PM-adjacent categories that have integration APIs and partner programs. Most don't need BD — they have self-serve partner programs. (4) Warm intros for the 3-5 that require custom integration. (5) 1-page terms: "free integration, mutual logo placement, co-marketing blog post at launch". (6) Post-close memo. (7) After 3 integrations, build an integration framework and self-serve partner docs.

Output: BD pipeline focused on strategic integrations, self-serve path for the rest.

**Scenario: Distribution deal negotiation**

Trigger: "A big retailer wants to distribute our hardware product. They're asking for 40% margin and exclusivity. Is this a good deal?"

Process: (1) Objective check: does this match our distribution objective? (2) Type: Distribution Deal. (3) Evaluate terms against standard distribution ranges: 30-45% margin is normal, exclusivity is negotiable. (4) 1-page term sheet: 40% margin OK, but exclusivity limited to a specific category/region/time period. Guarantees: minimum $X annual purchase. (5) Warm intro path to their CEO (via your board advisor) if negotiations stall. (6) Post-close: document sticking points for next deal.

Output: Term sheet with specific negotiation levers and a backup intro path.

**Scenario: Founder pursuing "marquee" BD**

Trigger: "I want to partner with Apple. We'd be on every iPhone. How do I get a meeting?"

Process: (1) Reality check: Apple doesn't do BD meetings with early-stage startups without existing traction. Marquee targets rarely return calls. (2) Attribute filter: instead of Apple specifically, list all companies with large iOS developer audiences (Stripe, Firebase, Twilio, etc.). These are reachable partners. (3) Pipeline of 15 reachable partners. (4) Warm intros for the top 5. (5) After 2-3 deals close, THEN the Apple conversation becomes plausible — you have credibility to bring.

Output: Redirected BD pipeline from marquee-chasing to attribute-based reachable partners.

## References

- For the 5 partnership types in full detail, see [references/partnership-types.md](references/partnership-types.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select BD as a channel
- `clawhub install bookforge-startup-sales-process` — Sales vs BD distinction
- `clawhub install bookforge-startup-critical-path-planning` — BD deals are often critical path milestones

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
