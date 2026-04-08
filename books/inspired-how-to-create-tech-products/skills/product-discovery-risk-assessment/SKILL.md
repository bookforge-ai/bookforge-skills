---
name: product-discovery-risk-assessment
description: "Assess product risks and decide whether to build. Use when starting product discovery, evaluating a new feature or product idea, deciding which risks to validate first, choosing between prototyping and testing approaches, or when someone asks 'should we build this?' Maps any idea to the 4-risk taxonomy (value risk, usability risk, feasibility risk, business viability risk) plus ethics risk, sequences discovery by priority, and selects the right technique category for each risk. Also use when a team is unsure what to validate next, when structuring a discovery sprint, or when planning pre-build validation activities. Hub skill for all downstream discovery technique selection — for specific techniques, use discovery-framing-technique-selection, discovery-prototype-selection, value-testing-technique-selection, customer-discovery-program, or business-viability-stakeholder-testing instead."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/product-discovery-risk-assessment
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: inspired-how-to-create-tech-products
    title: "INSPIRED: How to Create Tech Products Customers Love"
    authors: ["Marty Cagan"]
    chapters: [33, 34]
tags: [product-management, product-discovery, risk-assessment]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: "Product idea, feature proposal, or initiative description"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document-based product management environment"
discovery:
  goal: "Assess product risks and select appropriate discovery techniques"
  tasks:
    - "Identify which product risks (value/usability/feasibility/viability) apply to this idea"
    - "Select the right discovery technique category for each identified risk"
    - "Sequence discovery activities by risk priority"
    - "Flag ethics risk if applicable"
  audience:
    roles: [product-manager, product-leader, tech-lead, startup-founder]
    experience: any
  when_to_use:
    triggers:
      - "Starting product discovery for a new feature or product"
      - "Deciding which risks to validate first before building"
      - "Evaluating whether a product idea is worth pursuing"
      - "Structuring a discovery sprint or planning discovery activities"
    prerequisites: []
    not_for:
      - "Executing specific discovery techniques (use technique-specific downstream skills)"
      - "Post-build retrospectives or delivery planning"
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

# Product Discovery Risk Assessment

## When to Use

Apply this skill when you have a product idea, feature proposal, or initiative and need to decide:
- Which risks are present and how severe each is
- Which discovery technique categories to deploy
- In what sequence to run discovery activities

This is the **hub skill** for product discovery. Run it before any technique-specific discovery work. Downstream skills (framing technique selection, prototype selection, value testing, viability testing) consume the structured risk assessment this skill produces.

Do NOT use this skill to execute discovery techniques — it produces a plan, not the techniques themselves.

## Context and Input Gathering

Before running the assessment, collect:

1. **Product idea description** — What is the proposed solution or feature? One paragraph minimum.
2. **Target customer/user** — Who will use it? Buyer vs. user distinction matters.
3. **Business context** — How does this fit the company's revenue model, brand, legal environment?
4. **Team context** — What engineering, design, and product capabilities are on the team?
5. **Stage** — New product, new feature on existing product, or improvement to existing feature?

If a document exists (brief, PRD, opportunity assessment), read it. If not, ask the user to describe the idea before proceeding.

## Process

### Step 1: Classify the Idea by Stage and Novelty

Determine: Is this a new product, a new feature on an existing product, or an improvement to an existing feature?

**WHY:** Stage and novelty determine which risks are most acute. New products carry maximum value risk (customers don't yet choose to buy). Improvements to existing features have lower value risk but higher usability risk (existing users have established mental models to disrupt).

- New product → treat all 4 risks as potentially HIGH until evidence says otherwise
- New feature → value and usability risks are primary; feasibility and viability may be moderate
- Improvement → usability risk often dominates; value risk is lower but not zero

### Step 2: Score Each of the 4 Core Risks

For each risk, assign a severity: **Low / Medium / High / Unknown**.

**Risk 1 — Value Risk**
Question: Will customers choose to buy or use this?

Score High if:
- No direct evidence customers want this
- Customers have not asked for this (note: this is expected — customers often can't articulate what they want until they see it)
- Competing alternatives exist that solve the same underlying problem
- The value prop depends on behavior change

Score Low if:
- Existing customers have explicitly requested this capability AND you have validated they'll pay for or switch to use it
- A/B test or demand signal already exists

**WHY:** Value risk is consistently the hardest risk to address and the most common reason products fail. Most discovery time must be allocated here. A product with usability problems can survive; a product nobody values cannot.

**Risk 2 — Usability Risk**
Question: Can users figure out how to use this without help?

Score High if:
- The workflow is multi-step or requires user judgment
- The target user is not a technical expert in the problem domain
- Interaction design is novel (new UI patterns, voice, gesture)
- Errors are costly or hard to reverse

Score Low if:
- Workflow is a single well-understood action
- Users are power users already familiar with analogous tools

**WHY:** Even technically correct products fail if users cannot figure them out. Design skill and engineering skill are not interchangeable — and not every team has adequate design capacity. Usability must be validated with real users, not internal team members.

**Risk 3 — Feasibility Risk**
Question: Can the team build this within acceptable time, cost, and technical constraints?

Score High if:
- The solution requires technology the team has not used
- Significant scale or performance requirements exist
- Third-party integrations or data sources are unproven
- ML/AI components with uncertain quality thresholds are involved

Score Low if:
- The solution uses well-understood, in-production technology
- Engineering has already built analogous components

**WHY:** Feasibility must be validated during discovery — not at sprint planning. If engineers first see an idea at sprint planning, the team has already failed. Early engineer involvement during discovery also improves the solution itself and enables shared learning.

**Risk 4 — Business Viability Risk**
Question: Does this solution work for the business across all relevant dimensions?

Score High if any of the following are uncertain:
- Financial: Can we afford to build and provision it? Does the pricing model work?
- Sales: Can the sales force sell it?
- Marketing: Is it consistent with brand and go-to-market strategy?
- Legal: Are there regulatory, privacy, or contractual constraints?
- Business development: Does it work for existing partners?
- Executive: Will senior leadership support it?

Score Low if the solution is clearly within current business model, existing contracts, and established go-to-market motion.

**WHY:** Business viability must be validated during discovery — not after a product is built. Discovering a legal or financial blocker post-build destroys team morale and wastes engineering investment. Product managers own this risk, not just legal or finance.

### Step 3: Assess Ethics Risk (Fifth Risk)

Ethics risk is distinct from business viability. Ask:
- Could this solution cause harm to users, third parties, or the environment even if it is technically legal and meets business objectives?
- Does the solution optimize for a business metric (engagement, growth, monetization) in a way that produces harmful side effects?

If yes to either: flag as **Ethics Risk Present** and note the specific concern. When ethics risk is present, explore alternative solutions that solve the same underlying problem without the harmful side effect.

**WHY:** Technology capability does not imply ethical permission to build. Solutions can legally satisfy business objectives while harming users. The product manager's role is to identify ethics risks and bring potential alternative solutions to leadership — not to police, but to enable informed decisions.

### Step 4: Map Risks to Technique Categories

For each risk scored Medium or High, select the appropriate technique category. This mapping tells you which class of discovery activity to run.

| Risk | Technique Category | Purpose |
|------|--------------------|---------|
| Value (High) | **Framing** → then **Testing Value** | Clarify underlying problem first; then validate demand |
| Value (Medium) | **Testing Value** | Validate whether customers will choose this |
| Usability (High/Medium) | **Prototyping** → then **Testing Usability** | Build prototype; test with real users |
| Feasibility (High/Medium) | **Testing Feasibility** | Engineer-led feasibility spikes or proof-of-concept |
| Business Viability (High/Medium) | **Testing Business Viability** | Stakeholder review with legal, finance, sales, marketing |
| Ethics Risk Present | **Framing** + stakeholder review | Explore alternatives before committing to solution |
| All risks present | **Planning** techniques first | Use planning techniques to identify biggest challenges before committing to sequence |

**Technique Category Definitions** (for downstream skill selection):

- **Framing** — Clarifies the underlying problem before committing to a solution. Used when the problem is ambiguous or when handed a solution without a clear problem statement.
- **Planning** — Identifies the biggest challenges across the discovery effort and structures how to attack them. Used when multiple significant risks are present simultaneously.
- **Ideation** — Generates promising solutions aimed at the specific problem. Used after the problem is well-framed and when the current solution set is insufficient.
- **Prototyping** — Creates representations of solutions for testing. Four prototype types exist (detail in downstream skill: discovery-prototype-selection). Used before usability and value testing.
- **Testing** — Validates specific risks. Four sub-categories:
  - *Feasibility testing* — Engineer-led. Technology spikes, proof-of-concept, performance tests.
  - *Usability testing* — Designer-led. Interaction design validation with real users.
  - *Value testing* — Three modes: demand validation (will they buy?), qualitative value (do they see the value?), quantitative value (statistical evidence of value).
  - *Business viability testing* — PM-led. Stakeholder review across finance, legal, sales, marketing, brand, business development, and executive dimensions.

**WHY:** Different risks require different techniques and different team members to lead. Applying a usability test to a value problem wastes time. Applying a demand validation to a feasibility problem produces no useful signal. The mapping prevents mismatch between risk type and technique type.

### Step 5: Sequence Discovery Activities

Apply this sequencing logic:

1. **Framing first** — if value risk is High and the underlying problem is not yet clearly defined
2. **Value and usability validation before feasibility** — do not invest engineering time in feasibility spikes until there is evidence customers will use the solution
3. **Feasibility before deep prototyping** — if feasibility risk is High, validate technical viability before building high-fidelity prototypes
4. **Business viability throughout** — do not defer viability stakeholder review to the end; surface legal, financial, and sales concerns early
5. **Ethics review concurrent with framing** — flag and address ethics risk before committing significant discovery effort

**Exception:** If feasibility risk is so high it makes the idea technically impossible regardless of value, address feasibility first.

**WHY:** Validating value and usability first prevents expensive engineering feasibility work on solutions customers will not use. The sequencing reflects cost-of-being-wrong: value failure is cheap to discover; engineering failure after build is expensive.

### Step 6: Produce the Risk Assessment Document

Write a structured output (see Outputs section) that captures:
- Risk scores for all 4 core risks + ethics flag
- Selected technique categories per risk
- Recommended discovery sequence
- Iteration benchmark calibration

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Product idea / feature description | Yes | What is being proposed |
| Target customer/user description | Yes | Who will use it and who will buy it |
| Business model context | Yes | Revenue model, pricing, distribution |
| Team capability summary | Recommended | Engineering, design, and PM capacity |
| Existing research or demand signals | Optional | Any prior customer interviews, surveys, or analytics |

## Outputs

### Output Template: Product Risk Assessment

```
# Product Risk Assessment: [Product/Feature Name]

## Idea Summary
[One paragraph description]

## Stage Classification
[ ] New product  [ ] New feature  [ ] Improvement to existing feature

## Risk Scores

| Risk | Score | Evidence / Rationale |
|------|-------|---------------------|
| Value | High / Medium / Low / Unknown | [Why] |
| Usability | High / Medium / Low / Unknown | [Why] |
| Feasibility | High / Medium / Low / Unknown | [Why] |
| Business Viability | High / Medium / Low / Unknown | [Why] |
| Ethics | Present / Not Present | [If present: specific concern] |

## Technique Category Mapping

| Risk | Technique Category | Lead | Priority |
|------|--------------------|------|----------|
| [Risk] | [Category] | PM / Designer / Engineer | 1-4 |

## Recommended Discovery Sequence

1. [First activity — technique category, who leads, what question it answers]
2. [Second activity...]
3. ...

## Iteration Benchmark
Target: 10-20 discovery iterations per week.
Each iteration = one new idea or approach tested.
Current gap to benchmark: [if team is new to modern discovery techniques, note this]

## Dependencies for Downstream Skills
- discovery-framing-technique-selection: [needed yes/no — value risk High]
- discovery-prototype-selection: [needed yes/no — usability risk High/Medium]
- value-testing-technique-selection: [needed yes/no — value risk Medium/High]
- business-viability-stakeholder-testing: [needed yes/no — viability risk Medium/High]
- customer-discovery-program: [needed yes/no — new product with unknown customers]
```

## Key Principles

These 10 principles from structured pre-build validation (product discovery) govern how this assessment is used:

1. **Customers cannot specify what to build** — Your job is to solve the underlying problem, not implement customer requests literally. Customers don't know what's possible; they can't describe solutions they haven't seen.
2. **Value is the hardest problem** — Without compelling value, no other quality matters. Spend most discovery time here.
3. **UX is harder than it looks** — Coming up with a good user experience is often harder and more critical than the engineering. Not every team has adequate design skill.
4. **Functionality, design, and technology are intertwined** — Not sequential. Technology enables design; design enables functionality. This is why product manager, designer, and engineer must work in proximity.
5. **Expect most ideas to fail** — Approach discovery with the assumption that many, possibly most, ideas won't work — or will require several iterations. This is not a failure; it is the discovery process working correctly.
6. **Validate on real users, not proxies** — Internal teams, friendly users, and customer research cannot substitute for testing actual ideas on real target users before building.
7. **Validate fast and cheap** — Discovery iterations should be at least an order of magnitude less time and effort than delivery iterations. Target: 10–20 discovery iterations per week.
8. **Validate feasibility during discovery** — Engineers must see ideas during discovery, not at sprint planning. Early engineer involvement improves solutions and enables shared learning.
9. **Validate business viability during discovery** — Legal, financial, sales, and executive constraints must be surfaced before building, not after.
10. **Shared learning over division of labor** — The team learns together. Shared context about customer pain, failed ideas, and successful approaches is what creates an empowered team (versus a feature-execution team).

## Examples

### Example 1: New AI-Powered Search Feature (SaaS B2B)

**Scenario:** A B2B SaaS company wants to add AI-powered semantic search to replace their existing keyword search. Engineering has proposed using a third-party LLM API.

**Risk Assessment:**
- Value: Medium — existing customers have complained about search quality, but it's unclear they'll pay more or switch usage patterns for semantic search
- Usability: Medium — semantic search behaves differently from keyword search; users may be confused when results don't match their query literally
- Feasibility: High — third-party LLM integration is unproven at the team's data scale; latency and cost per query are unknown
- Business Viability: Medium — LLM API costs could affect gross margin; legal has concerns about customer data being sent to a third party
- Ethics: Not present

**Technique Sequence:**
1. Testing Value (qualitative) — 5 customer interviews: do they see enough value to change search behavior?
2. Testing Feasibility — Engineering spike: can the LLM API meet latency and cost requirements at scale?
3. Testing Business Viability — Legal review of data processing agreement with LLM provider; finance model on per-query cost impact
4. Prototyping + Testing Usability — If value and feasibility clear, build low-fidelity prototype and run usability test with 5 target users

### Example 2: Mobile Onboarding Redesign (Consumer App)

**Scenario:** A consumer app wants to redesign its 7-step onboarding flow to reduce drop-off. Current completion rate is 34%.

**Risk Assessment:**
- Value: Low — the app already has validated demand; onboarding improvement is retention work, not value creation
- Usability: High — 66% of users are dropping out, direct evidence of severe usability failure
- Feasibility: Low — standard mobile UI components; no new technology required
- Business Viability: Low — no legal, financial, or sales constraints on onboarding design
- Ethics: Not present

**Technique Sequence:**
1. Framing — review existing analytics to identify which of the 7 steps has highest drop-off (clarify the specific problem before designing solutions)
2. Prototyping — build 2-3 prototype variants of the redesigned flow
3. Testing Usability — moderated usability test with 5 target users per variant
4. Testing Value (quantitative) — A/B test winning variant for statistical significance on completion rate

### Example 3: New Monetization Feature (Consumer Platform)

**Scenario:** A consumer platform wants to introduce a "boost" feature where users pay to increase visibility of their content.

**Risk Assessment:**
- Value: High — no evidence users will pay; paying for visibility is a new behavior for this user base
- Usability: Low — simple payment and toggle interaction
- Feasibility: Low — payment infrastructure already exists
- Business Viability: Medium — revenue model works, but marketing has concerns about brand perception; legal needs to review advertising regulations
- Ethics: **Present** — boosting visibility for paying users could harm non-paying users' reach and undermine trust in organic content quality

**Technique Sequence:**
1. Framing — clarify the underlying business problem (revenue growth) and explore alternative solutions that do not create a pay-to-win dynamic
2. Testing Business Viability — marketing brand review + legal advertising regulations review
3. Testing Value (demand) — if ethics risk can be mitigated, validate willingness to pay with target users before building
4. Prototyping + Testing Usability — only if value and viability clear

## References

- `references/four-risk-taxonomy.md` — Full definitions and scoring rubrics for all 4 core risks plus ethics risk
- `references/technique-categories.md` — Descriptions of all 5 technique categories and their 4 testing sub-categories
- `references/discovery-sequencing-logic.md` — Decision tree for sequencing discovery activities across risk combinations
- `references/discovery-principles.md` — Full elaboration of all 10 pre-build validation principles

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — INSPIRED: How to Create Tech Products Customers Love by Marty Cagan.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
