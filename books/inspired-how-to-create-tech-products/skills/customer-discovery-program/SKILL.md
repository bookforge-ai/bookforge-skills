---
name: customer-discovery-program
description: "Design a customer discovery program to achieve product-market fit for a significant new product or market expansion. Use when launching a new product, entering a new market segment, redesigning a product for a different customer segment, or when someone asks 'how do we find product-market fit?', 'how do we get reference customers?', or 'are we stuck in a sales-driven fragmentation spiral?' Also use when the team is unsure if they have achieved product-market fit, when scaling sales feels premature, or when checking whether the Sean Ellis test applies. Produces a complete program plan: single target market definition, recruitment criteria for 6 reference customers, co-development relationship structure, and product-market fit definition by product type (B2B, platform/API, consumer, internal). Not for small features or minor improvements — use value-testing-technique-selection for those."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/customer-discovery-program
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: inspired-how-to-create-tech-products
    title: "INSPIRED: How to Create Tech Products Customers Love"
    authors: ["Marty Cagan"]
    chapters: [39]
tags: [product-management, product-market-fit, customer-development]
depends-on: [product-discovery-risk-assessment]
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Product idea, initiative description, or opportunity brief for a significant new product or market expansion"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document-based product management environment"
discovery:
  goal: "Design a complete customer discovery program plan that generates reference customers in parallel with product development"
  tasks:
    - "Identify the single target market for the program"
    - "Define recruitment criteria for 6-8 prospective reference customers"
    - "Structure the co-development relationship and program rules"
    - "Set product-market fit definition appropriate for the product type"
    - "Diagnose whether the sales-driven fragmentation spiral is present"
    - "Produce the full program plan document"
  audience:
    roles: [product-manager, startup-founder, product-leader]
    experience: any
  when_to_use:
    triggers:
      - "Launching a new product or business line"
      - "Taking an existing product to a new market or geography"
      - "Redesigning a product for a different customer segment"
      - "Determining whether the team has achieved product-market fit"
      - "Breaking out of a sales-driven fragmentation spiral"
    prerequisites: []
    not_for:
      - "Small features or minor improvements to existing products"
      - "Products already past product-market fit with an established customer base"
      - "Executing discovery techniques (use technique-specific downstream skills)"
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
---

# Customer Discovery Program

## When to Use

Apply this skill when the team is launching a significant new product, entering a new target market, or redesigning a product — and needs to achieve product-market fit before scaling sales and marketing.

This skill produces a **program plan**, not a discovery execution log. The output is a structured document the PM uses to recruit, co-develop with, and validate a set of reference customers in parallel with building the product.

Do NOT use this skill for:
- Small features or minor product improvements (overhead is too high)
- Products already past product-market fit
- Executing specific discovery techniques (see downstream technique skills)

The program takes substantial PM effort over multiple months. It is also the single best leading indicator of future product success.

## Context and Input Gathering

Before designing the program, collect:

1. **Product initiative description** — What is being built? One paragraph minimum.
2. **Product type** — B2B (selling to businesses), platform/API (selling to developers), internal tools (employees are users), or consumer (direct-to-consumer).
3. **Target market** — Which customer segment, vertical, or geography is the primary target? If multiple segments are under consideration, list them — the plan will force a choice.
4. **Current customer/prospect relationships** — Are there existing customers, active prospects, or is the team starting from zero?
5. **Company stage** — Early-stage startup (limited cash) or established company with an existing sales organization?
6. **Sales organization involvement** — Is a sales team already pursuing deals? If so, describe recent deal patterns.

If a product brief, opportunity assessment, or risk assessment from `product-discovery-risk-assessment` exists, read it before proceeding.

## Diagnosing the Sales-Driven Fragmentation Spiral

Before designing the program, check whether the team is already in the fragmentation spiral. This is the primary motivation for the program in established companies.

### The 5-Stage Fragmentation Spiral

**Stage 1 — Weak product:** The product does not yet strongly solve the target customer's problem. Customer acquisition costs are high because marketing must work hard to attract prospects who are not already sold.

**Stage 2 — Sales creativity:** To hit quota, the sales organization gets creative. They lengthen the sales pitch, offer heavy discounts, and negotiate custom terms to close deals. Sales cycles grow longer. Margin shrinks.

**Stage 3 — Requirements capture:** Sales starts bringing individual deal requirements to the PM as the condition for closing the next big customer. Each new deal has slightly different needs.

**Stage 4 — Product fragmentation:** The PM, under pressure, implements the requirements from the latest set of deals. The product accumulates feature combinations that work for specific customers but create complexity that makes the product worse for everyone.

**Stage 5 — Weaker product:** The accumulated complexity makes the core product harder to use and position. The cycle repeats. The team complains about working at a "sales-driven company."

**WHY this matters:** The spiral is self-reinforcing. Diagnosing it explains why the team is under pressure to take one-off requirements. The customer discovery program is the escape because it builds a strong product before sales scales — eliminating the root cause rather than managing the symptoms.

### Spiral Diagnosis Checklist

Mark each symptom as Present / Absent:

| Symptom | Status |
|---------|--------|
| Marketing requires high spend to generate qualified leads | |
| Sales cycles are lengthening | |
| PM receives feature requests that are framed as "deal requirements" | |
| Product has features that were built for one or two customers but rarely used broadly | |
| Win/loss analysis shows losses due to feature gaps vs. competitors | |
| Customer success team reports frequent escalations from frustrated customers | |

**If 3+ symptoms are present:** the spiral is active. The program is urgent. Do NOT let sales scale until reference customers are established.

**If 0-2 symptoms present:** the team is pre-spiral or in early stages. The program is preventive.

## Process

### Step 1: Define the Single Target Market

Choose exactly one target market for this program. The program fails if customers are drawn from two or three different segments.

**Market definition options:**
- By vertical (e.g., financial services, manufacturing, healthcare)
- By company size (e.g., enterprise >1,000 employees; mid-market 100-999)
- By geography (e.g., United States first, then Germany, then Brazil)
- By job function (e.g., engineering leaders at software companies)

**WHY single market:** Six reference customers from two or three different markets will not give you focus. The product will be pulled in multiple directions, which is how fragmentation starts. Six from one segment gives the sales team a clear, replicable motion: "We've helped six companies like yours."

**Decision rule:** If the team is debating two markets, pick the one where the pain is most acute and the PM has the most existing access to real customers. Market expansion comes after the first set of six is complete.

**Output of this step:** One sentence defining the target market: [Segment] + [Geography/Size qualifier if applicable].

### Step 2: Define Recruitment Criteria

Recruit 6-8 prospective reference customers to allow for 1-2 who drop out or prove to be a poor fit. The target is to end with exactly 6.

**Required criteria (all must be present):**

| Criterion | Description | Why It Matters |
|-----------|-------------|----------------|
| Acute pain | The customer feels the problem acutely — near-desperate for a solution. They have tried alternatives and those alternatives have failed or are insufficient. | Customers who feel pain moderately will not engage deeply with co-development. They'll participate passively and give polite feedback, not honest signal. |
| Time and people available | The customer has staff who can spend real time with the product team: testing early prototypes, giving feedback, running the product in their environment. | Co-development requires genuine collaboration. A customer who is "interested" but cannot show up to working sessions is not a reference customer candidate. |
| From the single target market | The customer must be from the defined target market — not an adjacent segment or personal contact who happens to be interested. | Mixing segments destroys the focus the program is designed to create. |
| Willing to serve as public reference | The customer, if the product works for them, is willing to be named publicly by marketing. | A reference customer who cannot be named publicly provides no sales collateral value. Coordinate with the customer's marketing organization before confirming. |

**Preferred criteria (strongly preferred, not required):**

| Criterion | Description |
|-----------|-------------|
| Marquee name | Well-recognized brand in the target market. A marquee reference is more valuable to sales than five unknown names combined. |
| Not a technologist | Screen out customers who are primarily interested in the technology itself rather than the business problem. Technologists distort feedback toward technical features rather than business value. |

**Sources for candidates:** Existing customer base, active prospect pipeline, inbound leads who inquired but did not buy, and introductions from the product marketing manager.

**Recruitment signal test:** If the team cannot find even 4-5 prospective customers willing to participate, this is a demand validation failure. The problem may not be as important as assumed. Reconsider the initiative before proceeding.

**Recruitment coordinator:** The PM leads recruitment in tight collaboration with the product marketing manager. The product marketing manager coordinates reference permissions and helps convert reference customers into sales collateral.

### Step 3: Structure the Co-Development Relationship

The relationship is a **development partnership**, not a consulting engagement or a custom development contract.

**Explain to each prospective member:**
- The goal is a general product that can be sold to many companies — not a custom solution built for them alone
- The PM will dive deep with each of the six customers to find a single solution that works well for all six — not implement every feature that all six request
- The customer gets genuine input into the product direction and real access to early prototypes and versions
- The customer gets the product before general release, live and validated in their environment before public launch
- The customer agrees to buy and serve as a public reference **if** the resulting product works for them

**Program rules:**

| Rule | Rationale |
|------|-----------|
| Do not charge customers in advance | Paying in advance changes the relationship from partnership to vendor/client. The PM is not a custom development shop. (Exception: early-stage startups with limited cash may use escrow.) |
| Cap program at 6-8 members | Sales organizations will pressure the PM to add more. More than 8 is unmanageable and produces unfocused signal. Customers who want early access but are not right for the program can join a separate early-release program without the co-development commitment. |
| Release to program members before general release | Reference customers must be live and happy before the general release. They stand up for the product at launch. |
| Treat members as colleagues | Share context openly. The PM will show prototypes, ask detailed questions, test early versions in their environment. These relationships often last many years. |

**The PM's job in this relationship:** Find a single solution that works well for all 6 customers. This requires deep understanding of each customer's underlying problem — not surface-level feature comparison across all 6. Listing all features that all 6 request and implementing them produces a fragmented product.

### Step 4: Define Product-Market Fit for This Product Type

Select the appropriate product-market fit definition based on product type.

**B2B (Selling to businesses):**
- Product-market fit = 6 reference customers in the target market who are:
  - Active (running the product in production, not trial or prototype)
  - Paying real money (not given away or deeply discounted)
  - Willing to recommend voluntarily and sincerely to peers

**Platform / API (Selling to developers):**
- Product-market fit = 6 reference **applications** built on the platform
- Work with development teams (engineers and product managers) at partner companies, not business buyers
- Focus on successful applications created with the platform, not just developers who signed up

**Internal tools (Customer-enabling tools for employees):**
- Product-market fit = 6-8 influential internal employees who:
  - Regard themselves as thought leaders among their peers
  - Genuinely believe the tool is great
  - Actively recommend it to colleagues voluntarily
- These are internal "references" rather than paying customers — no payment criterion

**Consumer (Direct-to-consumer products):**
- Primary metric: 10-50 engaged consumers who are actively using the product and loving it
- Supplementary metric: **Sean Ellis test** — survey active users who have experienced core value: "How would you feel if you could no longer use this product?" Target: **>40% responding "very disappointed"**
- Sean Ellis survey mechanics: survey only users who have used the product recently (at least twice), have reached the core value of the product per analytics, and are from the target market — not all registered users
- Consumer products must supplement the small reference group with broader testing on users who have not been exposed to the product, since individual consumers do not carry the sales collateral weight that B2B references do

**WHY the B2B definition is more practical than the Sean Ellis test for business products:** Six named reference customers in a specific market give sales a concrete, replicable proof point. The Sean Ellis test is subjective and sample-dependent for B2B; the reference customer definition is binary and verifiable.

**Declaring product-market fit:** When the program reaches the PMF definition for the product type, declare it. PMF does not mean the product is finished — continuous improvement continues. But PMF enables aggressive and effective selling to the rest of that target market.

### Step 5: Set the Pre-Launch Gate

Do not launch broadly — do not turn on the sales or marketing machine — until the PMF definition is met.

**Pre-launch gate criteria (B2B):**

| Gate | Status |
|------|--------|
| 6 reference customers active in production | |
| All 6 paying (or escrow committed for early-stage) | |
| All 6 willing to be named publicly (marketing permission confirmed) | |
| All 6 live and happy before general release date | |
| Product marketing has converted at least 2-3 into sales collateral (case study, quote, or logo) | |

**WHY do not launch early:** Without reference customers, the sales team does not know where the real product-market fit is. With quota pressure, they will sell to any customer they can close — which recreates the fragmentation spiral. Reference customers give sales a clear target profile and social proof for that profile.

### Step 6: Produce the Program Plan Document

Write a structured program plan document (see Outputs section).

## Outputs

### Output Template: Customer Discovery Program Plan

```
# Customer Discovery Program Plan: [Product/Initiative Name]

## Initiative Summary
[One paragraph: what is being built and why]

## Product Type
[ ] B2B  [ ] Platform/API  [ ] Internal tools  [ ] Consumer

## Spiral Diagnosis
[Present / Pre-spiral — list active symptoms if present]

## Single Target Market
[One sentence: segment + qualifier]

## Product-Market Fit Definition
[B2B: 6 reference customers active, paying, willing to recommend]
[Consumer: 10-50 engaged users + >40% "very disappointed" on Sean Ellis]
[Platform: 6 reference applications]
[Internal: 6-8 influential internal users who recommend to peers]

## Recruitment Plan

### Target count
Recruit [6-8] prospective members to end with 6.

### Candidate sources
- [Source 1: existing customers / prospects / inbound / introductions]
- [Source 2]
- [Source 3]

### Recruitment criteria checklist (per candidate)
- [ ] Feels the problem acutely / near-desperate
- [ ] Has time and people to collaborate
- [ ] From the single target market
- [ ] Willing to serve as public reference (marketing permission coordinated)
- [ ] Screened: not primarily a technologist
- [ ] Preferred: marquee brand name

### Candidates under consideration
| Candidate | Source | Pain Level | Marquee? | Status |
|-----------|--------|------------|----------|--------|
| [Name/Company] | | High/Med/Low | Y/N | Prospecting/Confirmed/Declined |

## Co-Development Relationship Structure
- Payment: [not in advance / escrow arrangement for early-stage]
- Program size cap: [6-8 members]
- Commitment from customer: test early prototypes, give real feedback, buy if product works, serve as public reference
- Commitment from product team: genuine input to product direction, pre-release access, product that works for them specifically
- Coordination: PM leads; product marketing manager handles reference permissions and collateral

## Timeline
| Phase | Duration | Activities |
|-------|----------|-----------|
| Recruitment | [weeks] | Identify candidates, qualify, confirm |
| Early co-development | [weeks] | Prototypes, early versions, deep qualitative work |
| Production validation | [weeks] | Full product in reference customer environment |
| PMF declaration | [date target] | All 6 criteria met |
| General launch | [date target] | Reference customers live; sales/marketing enabled |

## Pre-Launch Gate
- [ ] 6 reference customers active in production
- [ ] All 6 paying (or escrow committed)
- [ ] All 6 with marketing permission confirmed
- [ ] All 6 live and happy before launch date
- [ ] 2-3 converted to sales collateral by product marketing

## Risks and Contingencies
| Risk | Mitigation |
|------|-----------|
| Cannot recruit 4-5 candidates | Demand validation failure — reconsider initiative |
| Sales pressure to add more than 8 | Direct oversubscribed prospects to early-release program (no co-development commitment) |
| Customer requests custom feature not useful for all 6 | PM finds generalized solution — not the specific request; explain general product framing |
| Spiral symptoms accelerating | Do not scale sales until gate is met; present spiral diagnosis to leadership |
```

## Key Principles

1. **Reference customers are the single best leading indicator of product success.** They are more predictive than any internal metric or survey result because they represent real commitment: real money, real production usage, real willingness to recommend.

2. **Develop reference customers in parallel with the product.** The program is not a post-launch validation exercise. The PM discovers and develops reference customers at the same time as discovering and developing the product.

3. **Single target market is non-negotiable.** The program's value comes from focus. Mixed segments produce mixed signal and a product that half-solves multiple problems.

4. **The PM's job is one solution for all six, not a union of all requests.** Building every feature that all six customers request produces a fragmented product. The PM dives deep with each customer to understand the underlying problem, then finds a single solution that works for all.

5. **Do not charge in advance.** Payment in advance changes the relationship from partnership to vendor contract. The customer should buy because the product works — not because they already paid.

6. **The spiral escape requires a gate.** The only way to break the sales-driven fragmentation spiral is to refuse to scale sales before the PMF gate is met. This requires leadership alignment — the gate must be a shared commitment, not just a PM preference.

7. **Recruitment difficulty is a demand signal.** If the PM cannot find 4-5 prospective customers willing to participate, the problem is probably not important enough to build a business around.

8. **Product marketing is a co-owner of the program.** The product marketing manager coordinates reference permissions, keeps the program running smoothly under sales pressure, and converts reference customers into sales collateral. They must be involved from the start.

## Product Type Variants Summary

| Dimension | B2B | Platform/API | Internal Tools | Consumer |
|-----------|-----|--------------|----------------|----------|
| PMF definition | 6 reference customers | 6 reference applications | 6-8 influential internal users | 10-50 loving users + >40% Ellis |
| Who you work with | Business buyers + their users | Engineering teams at partner companies | Internal employees (thought leaders) | Individual consumers |
| Payment criterion | Yes — real money | Typically yes | No — internal | Usually no (at program stage) |
| Reference type | Named company + logo | Named application | Colleague referral | User testimonial / press |
| Sean Ellis test | Optional supplement | Optional | Not applicable | Primary metric |

## References

- `references/sales-driven-spiral.md` — Full 5-stage spiral mechanics, spiral recovery case patterns, and escalation language for leadership alignment
- `references/recruitment-screening-guide.md` — Detailed interview questions and scoring rubric for screening prospective reference customer candidates
- `references/pmf-definitions.md` — Complete product-market fit definitions per product type, Sean Ellis survey instrument, and B2B reference customer criteria checklist
- `references/program-rules-rationale.md` — Detailed rationale for each program rule (payment, cap, release timing) and objection handling for sales pressure

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — INSPIRED: How to Create Tech Products Customers Love by Marty Cagan.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-product-discovery-risk-assessment`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
