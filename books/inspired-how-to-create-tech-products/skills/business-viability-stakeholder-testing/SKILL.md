---
name: business-viability-stakeholder-testing
description: "Test whether a product solution is viable for the business before building. Use when business viability risk is Medium or High, when multiple internal functions (legal, sales, finance, marketing) may have constraints on a proposed solution, when someone asks 'will this work for our business?', 'do we have stakeholder buy-in?', or 'does legal/finance/sales need to review this?' Also use when a proposed solution would change pricing, go-to-market motion, or support model, or when you need documented cross-functional sign-off before committing engineering resources. Identifies all stakeholders who can veto launch across 8 domains, conducts 1:1 preview sessions with high-fidelity prototypes, and resolves disagreements with evidence rather than opinions. Produces a structured viability sign-off document. Not for customer value testing — use value-testing-technique-selection. Not for product-market fit — use customer-discovery-program."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/business-viability-stakeholder-testing
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: inspired-how-to-create-tech-products
    title: "INSPIRED: How to Create Tech Products Customers Love"
    authors: ["Marty Cagan"]
    chapters: [31, 56, 61]
tags: [product-management, stakeholder-management, business-viability]
depends-on: [product-discovery-risk-assessment]
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Product solution description or high-fidelity prototype, plus a brief on the company's business model, go-to-market motion, and any known stakeholder concerns"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document-based product management environment"
discovery:
  goal: "Confirm that a proposed product solution works for the business across all relevant dimensions before the team commits to building it"
  tasks:
    - "Identify which of the 8 stakeholder domains apply and who holds veto power"
    - "Map concern categories for each relevant stakeholder domain"
    - "Plan and conduct 1:1 stakeholder preview sessions using high-fidelity prototypes"
    - "Resolve any stakeholder objections with evidence rather than authority"
    - "Produce a viability sign-off document capturing status across all domains"
  audience:
    roles: [product-manager, product-leader, startup-founder]
    experience: any
  when_to_use:
    triggers:
      - "Business viability risk is scored Medium or High in the product discovery risk assessment"
      - "Multiple internal functions (legal, finance, sales, marketing) may have constraints on a proposed solution"
      - "A proposed solution would change the go-to-market motion, pricing model, or support model"
      - "You need documented cross-functional sign-off before committing engineering resources"
      - "A senior stakeholder or executive has unaddressed concerns about a proposed direction"
    prerequisites:
      - "product-discovery-risk-assessment completed — viability risk must be identified as Medium or High"
      - "A high-fidelity prototype or detailed solution description exists to show stakeholders"
    not_for:
      - "User testing or usability validation (different technique — user drives; see discovery-prototype-selection)"
      - "Value testing with customers (different goal — viability testing is internal, not customer-facing)"
      - "Feasibility testing (engineer-led technical spikes — different risk type)"
      - "Post-build review meetings or retrospectives"
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

# Business Viability Stakeholder Testing

## When to Use

Apply this skill when your product discovery risk assessment has flagged business viability as Medium or High risk. This means the proposed solution may conflict with the constraints of internal functions that have power to block launch.

This skill produces a structured viability sign-off — confirmation that the solution works for the business across all relevant dimensions — before the team commits to building.

Do NOT use this skill for customer-facing validation (user testing, demand validation). Those address value and usability risk. This skill addresses the internal business dimension: will finance, legal, sales, marketing, and executive stakeholders support this solution?

## Context and Input Gathering

Before running this process, collect:

1. **Solution description** — What is the proposed product or feature? Sufficient detail to expose constraints (not a vague concept).
2. **High-fidelity prototype** — Stakeholders need to see actual proposed screens, workflows, and wording. Presentations and slide decks are not sufficient.
3. **Business model context** — Revenue model, pricing structure, distribution channels, existing partner agreements, brand positioning.
4. **Known concerns** — Any constraints already surfaced (legal has flagged X; sales team worried about Y).
5. **Stakeholder map** — Who in this organization holds authority over each relevant domain?

If no high-fidelity prototype yet exists, this process should be deferred until one does. Showing presentations to stakeholders produces false sign-off — they agree to something they have not actually seen.

## Process

### Step 1: Identify Relevant Stakeholder Domains

A stakeholder is any person who can veto your work or prevent launch. Work through the 8 standard domains and determine which apply to this solution:

| Domain | Veto Test |
|--------|-----------|
| Marketing | Could this solution affect brand promise, go-to-market channels, or market positioning? |
| Sales | Could this change what the sales force is asked to sell, or how they sell it? |
| Customer Success | Could this change the support burden, onboarding model, or customer-facing service model? |
| Finance | Could this affect unit economics, provisioning costs, pricing model, or investor reporting? |
| Legal | Does this touch privacy, compliance, intellectual property, or competitive constraints? |
| Business Development | Does this interact with existing partner agreements or external relationships? |
| Security | Does this introduce new data exposure, access control changes, or security surface area? |
| Executive (CEO/COO/GM) | Is there overall business risk, or does this require executive-level trust and endorsement? |

Mark each domain as: **Applicable** (must engage), **Monitor** (low concern, check briefly), or **Not applicable**.

**WHY:** The worst outcome is discovering post-build that launch is blocked by a constraint you did not surface. Every domain in the applicable list represents a potential launch blocker. Skipping any applicable domain is not a time saving — it is a liability that compounds if discovered after the team has built.

Full concern details for each domain: `references/stakeholder-domain-concerns.md`

### Step 2: Map Specific Concerns Per Domain

For each applicable domain, identify the specific concern categories that apply to this solution. This is not a generic checklist — it requires judgment about what the proposed solution actually touches.

**Marketing concerns to check:**
- Brand consistency — does the solution fit within the brand promise customers expect from this company?
- Go-to-market channel impact — does the solution require a different distribution or marketing channel?
- Messaging and differentiation — does it conflict with current positioning or market segment strategy?

**Sales concerns to check:**
- Channel capability — can the existing sales force sell this? Does it require different skills, relationships, or deal cycles?
- Price point alignment — is this priced for the sales motion the team is equipped for?
- Sales cycle impact — does this lengthen, shorten, or restructure the sales process?

**Customer success concerns to check:**
- Support burden — does this create new categories of customer questions or failure modes?
- Onboarding complexity — can customers be successfully onboarded at current staffing levels and model (high-touch vs. low-touch)?

**Finance concerns to check:**
- Unit economics — can the company afford to build, provision, and operate this at scale?
- Pricing model viability — does the proposed pricing generate sufficient margin?
- Reporting and investor relations — are there financial disclosures or reporting constraints?

**Legal concerns to check:**
- Privacy — does the solution collect, store, or transmit user data in ways that create regulatory exposure?
- Regulatory compliance — are there industry-specific regulations that apply (GDPR, HIPAA, SOC 2, etc.)?
- Intellectual property — does the solution use third-party technology, content, or IP in ways that require agreements?
- Competitive constraints — do any existing agreements limit competitive positioning?

**Business development concerns to check:**
- Existing partner agreements — does the solution violate commitments or constraints in current partner contracts?
- Partner alignment — does the solution affect the value delivered through key distribution or integration partners?

**Security concerns to check:**
- Data protection — what new data does this solution handle and how is it protected?
- Access control — does this introduce new permission boundaries or authentication requirements?
- Security review requirements — does this trigger mandatory security review processes in this organization?

**Executive concerns to check:**
- Overall business risk — does the CEO/COO/GM have unresolved concerns about this direction?
- Trust in product manager — does the executive believe the PM understands the business constraints and is managing them?

**WHY:** Mapping specific concerns (not just domains) before stakeholder conversations ensures you enter each meeting informed. It also lets you structure the prototype walkthrough to specifically address the concerns most relevant to that stakeholder — which is more efficient and more likely to surface real objections.

### Step 3: Build 1:1 Stakeholder Relationships Before Preview Sessions

Before scheduling preview sessions, ensure you have an ongoing relationship with each key stakeholder:

- Meet regularly with key stakeholders (target: half an hour weekly or every two weeks per stakeholder)
- Understand their constraints by listening first — ask what they worry about, what constraints they operate under, what makes their work harder
- Share product learnings openly and continuously — after every user test or customer visit, brief relevant stakeholders on what you learned
- Share credit — ensure stakeholders see the product as a shared success, not the product manager's solo effort

**WHY:** Stakeholders who trust the product manager give latitude for better solutions. Stakeholders who do not trust the product manager escalate or attempt to control the product. Trust is built through demonstrated competence and genuine concern for their constraints — not through status updates. A stakeholder encountered cold in a group meeting will protect themselves; a stakeholder who knows and trusts you will collaborate.

The target is 2-3 hours per week total across all key stakeholders, not a one-time review.

### Step 4: Conduct 1:1 Preview Sessions with High-Fidelity Prototypes

Schedule individual meetings with each applicable stakeholder. Do not aggregate into a group meeting.

**Session format:**
1. Remind the stakeholder of the product goal and the specific risk you are testing
2. Walk them through the high-fidelity prototype (PM drives — this is a walkthrough, not a user test)
3. Explicitly invite them to raise concerns — give them every chance to spot problems
4. Listen without defensiveness; capture every concern
5. Do not negotiate in the meeting — acknowledge concerns and commit to following up with evidence

**Critical rules for these sessions:**

Use a **high-fidelity prototype, not a presentation.** A lawyer needs to see the actual proposed screens and wording. A marketing leader needs to see the actual product design. A security leader needs to see exactly what the product does with data. Slide decks are too ambiguous to test viability — stakeholders will agree to something they have not actually seen, then object when they see the real product.

Conduct **1:1 meetings, not group sessions.** Group meetings produce design-by-committee dynamics and mediocre results. In a group setting, stakeholders perform for each other rather than engage with the actual constraints. Individual sessions give each stakeholder space to raise concerns without political pressure.

**WHY behind the walkthrough format:** The purpose of a stakeholder preview session is different from a user test and different from a demo:
- **User test** — user drives the prototype; goal is to test usability and value with real users
- **Product demo** — PM drives, goal is to sell or persuade (evangelism context)
- **Stakeholder walkthrough** — PM drives, goal is to give the stakeholder every opportunity to identify problems before build

Full taxonomy and technique comparison: `references/prototype-review-taxonomy.md`

### Step 5: Resolve Disagreements with Data, Not Opinion

When a stakeholder raises an objection:

1. **Do not resolve by seniority** — the fact that a stakeholder is more senior does not make their opinion correct. This is a common trap that produces bad outcomes and erodes product team credibility.
2. **Do not resolve by PM authority** — asserting product authority does not address the constraint.
3. **Resolve by running a test** — quickly generate evidence relevant to the disagreement. Move the conversation from competing opinions to shared data.

Practical approaches:
- Run a targeted user test to test the disputed design assumption
- Model the disputed economics with finance (cost per unit, provisioning cost at scale)
- Get a legal opinion in writing rather than debating legal risk in the room
- Run a limited market test to answer the marketing or sales concern empirically

**WHY:** Stakeholders who lose opinion battles feel disrespected and disengage. Stakeholders who are shown evidence that neither party's original intuition was fully right become collaborative. Discovery exists specifically to generate this kind of evidence at low cost — use it to resolve disagreements before they become political.

### Step 6: Produce the Viability Sign-Off Document

After completing all stakeholder sessions, produce a structured document capturing the outcome.

```
# Business Viability Sign-Off: [Product/Feature Name]

## Solution Summary
[One paragraph: what is being proposed]

## Prototype Version Used
[Version/date of high-fidelity prototype shown to stakeholders]

## Stakeholder Domain Review

| Domain | Applicable | Stakeholder | Session Date | Status | Open Items |
|--------|-----------|-------------|--------------|--------|------------|
| Marketing | Yes/No | [Name] | [Date] | Cleared / Conditional / Blocked | [Any unresolved items] |
| Sales | Yes/No | [Name] | [Date] | Cleared / Conditional / Blocked | |
| Customer Success | Yes/No | [Name] | [Date] | Cleared / Conditional / Blocked | |
| Finance | Yes/No | [Name] | [Date] | Cleared / Conditional / Blocked | |
| Legal | Yes/No | [Name] | [Date] | Cleared / Conditional / Blocked | |
| Business Development | Yes/No | [Name] | [Date] | Cleared / Conditional / Blocked | |
| Security | Yes/No | [Name] | [Date] | Cleared / Conditional / Blocked | |
| Executive | Yes/No | [Name] | [Date] | Cleared / Conditional / Blocked | |

## Unresolved Items and Resolution Plan
[For any domain with status Conditional or Blocked: what is the specific issue, what evidence is needed to resolve it, and who owns resolution?]

## Decision
[ ] All applicable domains cleared — proceed to build
[ ] Conditional clearance — proceed with the following constraints: [list]
[ ] Blocked — do not proceed; revisit solution design

## Constraints Carried Forward
[Any constraints stakeholders confirmed that must be respected in the build — e.g., "must not expose PII to the LLM API per legal review", "pricing must not undercut enterprise tier per sales leadership"]
```

## PM Evangelism During Viability Testing

Stakeholder preview sessions are both a testing activity and an evangelism activity. These 10 practices build the organizational support that makes viability testing effective:

1. **Use the prototype** — not slides, not words. The prototype makes the solution concrete for everyone who cannot visualize from a description.
2. **Share the customer pain** — bring engineers and stakeholders to customer visits so they experience the problem directly. People who have seen the pain are more willing to accept solutions that address it.
3. **Connect to the product vision** — show stakeholders how this solution fits into the larger product direction and company strategy.
4. **Share learnings after every test** — distribute what you learned from user tests and customer sessions. Include what failed, not just what worked.
5. **Share credit generously** — ensure stakeholders see the product as a collective achievement. When things go wrong, step forward and take responsibility.
6. **Learn to give great demos** — a product demo is a persuasion tool, not training and not a user test. Develop this skill for customer and executive contexts.
7. **Build 1:1 relationships before group meetings** — never let a group meeting be the first time a stakeholder engages with your thinking. Individual relationships make group conversations productive.
8. **Be genuinely excited** — if you are not genuinely excited about what you are working on, that is a signal about the work or your role. Forced enthusiasm is detectable and counterproductive.
9. **Show enthusiasm visibly** — enthusiasm is contagious. People follow genuine energy. Make yours visible.
10. **Spend face time** — you cannot build trust through email. Regular in-person or video time with your designer, engineers, and key stakeholders is a direct investment in team velocity.

**WHY:** Business viability testing requires stakeholder trust to work. Stakeholders who trust the product manager surface real concerns early. Stakeholders who distrust the product manager either withhold concerns until too late or attempt to control the product. Evangelism practices build the trust that makes stakeholders collaborative.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Product solution description | Yes | What is being proposed in sufficient detail to expose constraints |
| High-fidelity prototype | Yes | Stakeholders need to see actual screens/wording — not slides |
| Business model context | Yes | Revenue model, pricing, distribution channels, partner agreements |
| Stakeholder map | Yes | Who holds authority over each applicable domain |
| Risk assessment output | Yes | From product-discovery-risk-assessment — confirms viability risk is Medium/High |
| Known stakeholder concerns | Recommended | Any constraints already identified before sessions begin |

## Outputs

- Stakeholder domain review table (completed, with status per domain)
- Viability sign-off document (structured output from Step 6)
- Constraints carried forward list (binding constraints the build must respect)
- Open items and resolution plan (for any Conditional or Blocked domains)

## Key Principles

1. **Never show finished solutions** — preview during discovery, before build. The most common and costly stakeholder management mistake is showing a completed product at review, only to discover a launch-blocking constraint that requires rework.
2. **High-fidelity prototypes, not presentations** — presentations are too ambiguous for viability testing. Lawyers need to see the actual wording. Marketers need to see the actual design. Executives need to see the actual product behavior.
3. **1:1 sessions, not group reviews** — group meetings produce design by committee. Individual sessions surface real constraints without political dynamics.
4. **Resolve with data, not opinion or seniority** — when a PM opinion conflicts with a stakeholder opinion, run a test. The stakeholder is usually more senior; the answer is not to concede but to generate evidence.
5. **The product manager owns viability** — not legal, not finance, not the CEO. It is the PM's job to understand every applicable constraint and bring that knowledge into the product team before build.
6. **Trust is the precondition** — stakeholders who trust the PM give latitude and surface concerns early. Stakeholders who distrust the PM escalate or attempt to control. Trust is built through demonstrated competence and genuine care for stakeholder constraints.

## Examples

### Example: Freemium Tier for Enterprise Security Product

**Scenario:** A security product team wants to launch a freemium tier. Sales is worried about cannibalization of enterprise deals. Legal has compliance concerns for free-tier users. The CEO wants to see unit economics before committing.

**Step 1 — Applicable domains:**
- Sales: Yes — freemium changes what the sales force sells and potentially undercuts their pipeline
- Legal: Yes — free-tier users may be subject to different compliance obligations (data retention, audit logging)
- Finance: Yes — CEO wants unit economics; provisioning costs for free-tier users must be modeled
- Marketing: Yes — freemium tier affects brand positioning (enterprise premium vs. broad access)
- Customer Success: Yes — free-tier users may generate high support volume at low revenue
- Security: Monitor — freemium may change data isolation requirements
- Business Development: Not applicable (no partner agreements affected)
- Executive: Yes — CEO has explicitly flagged concern

**Step 2 — Specific concerns mapped:**
- Sales: Can sales still close enterprise deals if prospects start on free tier? Does free-tier cap the deal size?
- Legal: Do free-tier users get the same data processing agreements? Are audit logs required for free users in regulated industries?
- Finance: What is the cost to provision each free-tier user? At what conversion rate is the tier profitable?
- CEO: What is the strategic bet — growth via free acquisition or revenue protection?

**Step 3 — Relationship preparation:** PM has standing weekly check-ins with sales leadership and CFO. Legal is a new relationship — PM schedules introductory meeting before the preview session to understand their review process.

**Step 4 — Sessions:**
- Sales leadership: walkthrough of free-tier feature set vs. enterprise feature set using high-fidelity prototype. Sales leader identifies that free tier must not include the SSO feature (enterprise differentiator).
- Legal: walkthrough of free user sign-up flow and data handling screens. Legal identifies that audit log exemption for free users requires explicit terms of service language.
- Finance: co-model unit economics using current infrastructure cost data. Finance clears at 5% conversion rate assumption.
- CEO: walkthrough of full tier structure. CEO clears with constraint: free tier must have a hard cap of 5 users per account.

**Step 5 — No opinion conflicts in this case** — all concerns resolved with data and concrete design decisions.

**Step 6 — Sign-off document:**
- Sales: Cleared — constraint: SSO excluded from free tier
- Legal: Cleared — constraint: audit log exemption requires specific ToS language
- Finance: Cleared — at 5% conversion rate assumption; monitor if below 3%
- Marketing: Cleared — positioning as "try before you buy" consistent with enterprise brand
- Customer Success: Conditional — support volume model must be revisited if free-tier adoption exceeds 10,000 users/month
- Security: Monitor — no new concerns surfaced
- CEO: Cleared — constraint: 5-user hard cap per free account

**Decision:** Conditional clearance — proceed with constraints listed above.

## Anti-Patterns

- **Scheduling a group review meeting with all stakeholders** — produces design by committee, political dynamics, and superficial sign-off. Individual sessions surface real constraints.
- **Using a slide deck presentation** — stakeholders agree to abstractions and object to the real product. High-fidelity prototype is required.
- **Waiting until after build to show stakeholders** — the most common failure mode. Discovery is the time for viability testing, not post-build review.
- **Resolving disagreements by invoking seniority or PM authority** — generates resentment and suppresses legitimate constraints. Run a test instead.
- **Treating all viability stakeholders as equal** — apply the veto test. Only engage domains with real launch-blocking authority. Do not create bureaucracy by including everyone who has an opinion.
- **Conflating walkthrough with user test** — in a user test, the user drives and the PM observes. In a stakeholder walkthrough, the PM drives and gives the stakeholder every opportunity to spot problems. These are different techniques with different purposes.

## References

- `references/stakeholder-domain-concerns.md` — Detailed concern categories for all 8 stakeholder domains with specific questions to ask and signals to look for
- `references/prototype-review-taxonomy.md` — Full comparison of user test vs. product demo vs. stakeholder walkthrough: who drives, what the purpose is, and when to use each
- `references/pm-evangelism-practices.md` — Elaboration of all 10 evangelism practices with application guidance for stakeholder management contexts

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — INSPIRED: How to Create Tech Products Customers Love by Marty Cagan.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-product-discovery-risk-assessment`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
