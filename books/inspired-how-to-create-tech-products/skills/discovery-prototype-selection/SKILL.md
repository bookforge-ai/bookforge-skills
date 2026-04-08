---
name: discovery-prototype-selection
description: "Select the right prototype type and fidelity level for any discovery risk. Use when deciding what kind of prototype to build, when choosing between a feasibility spike, user prototype, live-data prototype, or Wizard of Oz prototype, or when someone asks 'what prototype should we build?' Also use when prototyping for usability testing, when validating a technical approach before building, when building a simulation for stakeholder alignment, or when an AI/ML feature needs pre-model validation. Maps the active risk (feasibility/usability/value/viability) to one of four prototype types and determines fidelity. Includes anti-pattern warnings for ambush estimation and prototype-as-value-proof confusion. Best triggered after product-discovery-risk-assessment. For executing usability or value tests after the prototype, use value-testing-technique-selection."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/discovery-prototype-selection
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: inspired-how-to-create-tech-products
    title: "INSPIRED: How to Create Tech Products Customers Love"
    authors: ["Marty Cagan"]
    chapters: [45, 46, 47, 48, 49, 55]
tags: [product-management, product-discovery, prototyping]
depends-on: [product-discovery-risk-assessment]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Risk assessment output from product-discovery-risk-assessment, or description of the risk being addressed"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document-based product management environment"
discovery:
  goal: "Select the right prototype type and fidelity for the active risk, then guide its creation"
  tasks:
    - "Identify which risk is being addressed (feasibility/usability/value/viability)"
    - "Select the matching prototype type"
    - "Determine correct fidelity level for the testing purpose"
    - "Identify who creates the prototype and what constraints apply"
    - "Flag anti-patterns before creation begins"
  audience:
    roles: [product-manager, product-designer, tech-lead, startup-founder]
    experience: any
  when_to_use:
    triggers:
      - "Risk assessment has identified prototyping as a required technique"
      - "Deciding which prototype approach to use for a discovery question"
      - "Team is about to build a prototype and needs to align on type and fidelity"
      - "Evaluating whether to use a user prototype, feasibility spike, or live-data experiment"
    prerequisites:
      - "product-discovery-risk-assessment completed (or risk explicitly identified)"
    not_for:
      - "Executing usability tests (prototype is an input to testing, not the test itself)"
      - "Value testing — user prototypes do not validate value; use value-testing techniques after prototyping"
      - "Delivery work — feasibility prototypes are discovery code, not production code"
  environment:
    codebase_required: false
    codebase_helpful: true
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

# Discovery Prototype Selection

## When to Use

Apply this skill when a risk assessment has identified prototyping as a needed technique, or when the team needs to decide which prototype approach to use. This skill answers three questions:

1. Which prototype type matches the risk being addressed?
2. What fidelity level is appropriate for the testing purpose?
3. Who creates it, and what constraints apply?

Run this before building any prototype. The wrong prototype type wastes significant time — a user prototype cannot answer a feasibility question, and a feasibility prototype cannot answer a usability question.

## Governing Principles

Five principles apply to all prototype types. Violating any of them is a common source of wasted effort.

**Principle 1 — Cost of learning, not cost of building.** The overarching purpose of any prototype is to learn something at a much lower cost in time and effort than building a product. All forms of prototype should require at least an order of magnitude less time and effort than the eventual product. If a prototype is taking as long as shipping would, it has become delivery work.

**Principle 2 — Creation forces depth.** Creating a prototype forces the team to think through a problem at a substantially deeper level than talking about it or writing a document. This is why the act of creating a prototype so often exposes major issues otherwise left uncovered until much later. Do not skip prototyping in favor of documents or meetings.

**Principle 3 — Shared understanding tool.** A prototype is a powerful tool for team collaboration and stakeholder alignment. Members of the product team and business partners can all experience the prototype to develop shared understanding. Use prototypes in stakeholder reviews, not just user tests.

**Principle 4 — No single correct fidelity.** There is no such thing as one appropriate level of fidelity. The right level depends entirely on the testing purpose. Lower fidelity is faster and cheaper than higher fidelity. Only do higher fidelity when the testing purpose requires it.

**Principle 5 — Prototypes are disposable.** The primary purpose of a prototype is to address product risks in discovery. The prototype itself is not the product. Feasibility prototypes are throwaway code. User prototypes are simulations. Live-data prototypes are not commercially shippable. Treat all of them as disposable.

> **Critical warning — Prototype does not equal value validation.** A user prototype — even a high-fidelity one that 15 users say they "love" — does not validate value. User prototypes test usability and comprehension. They cannot prove purchase intent, retention, or behavioral change. People say all kinds of things when looking at a prototype and then do something completely different when real money or real effort is required. If the team needs to validate value, use a dedicated value-testing technique (demand validation, fake door test, live-data prototype with real behavior measurement) after — not instead of — usability testing. This is one of the most common and expensive mistakes in product discovery.

## Process

### Step 1: Identify the Risk Being Addressed

Read the risk assessment output. Determine which risk the prototype is meant to address:

- **Feasibility risk** — Can the team build this at all? (algorithm, performance, scalability, unfamiliar technology, third-party integration, legacy system, cross-team dependency)
- **Usability risk** — Can users figure out how to use this? (workflow complexity, novel interaction, multi-step process, error-prone operations)
- **Value risk (qualitative)** — Do users understand and respond to the value proposition when they see it? (distinct from demand validation — this tests comprehension and perceived value)
- **Viability risk** — Does this work for the business? (requires stakeholder review using prototype as communication tool)

**WHY:** Each risk requires a different prototype type. Mismatching the prototype to the risk produces invalid signal. A user prototype cannot tell you if an algorithm will work. A feasibility prototype cannot tell you if a workflow is learnable.

If multiple risks are present, select the prototype type that addresses the highest-priority risk first. Run multiple prototypes in sequence if necessary — do not try to address all risks with one prototype.

### Step 2: Select the Prototype Type

Use this decision table:

| Risk Being Addressed | Prototype Type | Creator | Output |
|---|---|---|---|
| Feasibility | Feasibility prototype | Engineer(s) | Working code demonstrating the approach |
| Usability | User prototype | Designer | Simulation (interactive wireframe to high-fidelity mock) |
| Value (qualitative, perceived) | User prototype (high fidelity) | Designer | Realistic simulation for qualitative testing |
| Value (quantitative, behavioral) | Live-data prototype | Engineer(s) | Limited real implementation collecting analytics |
| Automation / AI / ML viability + UX simultaneously | Hybrid prototype — Wizard of Oz | Designer + Engineer | Human operator simulates the automated behavior behind a realistic UI |
| Stakeholder alignment | User prototype | Designer | Communication artifact showing what will be built |

**Wizard of Oz prototype (Hybrid variant for AI/ML features):** When the team is validating whether an AI- or automation-powered feature would be valuable and usable before the model or automation exists, a human operator manually performs the automated action in real time while the user interacts with a realistic front-end. The user does not know a human is behind the curtain. This technique answers both value and usability questions for features that would be difficult or slow to build as live-data prototypes (because the model doesn't exist yet). Constraint: only works at very small scale — one session at a time, manually operated. Never use for quantitative validation.

See `references/prototype-type-details.md` for full descriptions of each type, their limitations, and canonical use cases.

### Step 3: Determine Fidelity

For user prototypes, fidelity is the primary variable. Apply this fidelity rule:

| Testing Purpose | Required Fidelity | Rationale |
|---|---|---|
| Value testing (qualitative: does the user perceive value?) | High | Must feel realistic; if users can tell it is fake, their reactions are not valid. People say all kinds of things about low-fi prototypes and then do something different. |
| Usability testing (can they complete the workflow?) | Low to medium acceptable | Information architecture and workflow are testable even without visual polish. |
| Demand validation (will they buy or sign up?) | Live-data or fake door | A user prototype cannot prove purchase behavior. Use live-data prototype or a fake door (demand test). |
| Stakeholder communication | Medium to high | Stakeholders need to experience the product concept clearly. |
| Team alignment / internal exploration | Low | Speed matters more than realism for internal thinking. |

**WHY:** Fidelity is a cost dial. High-fidelity user prototypes take significantly more time to create. Only spend that time when the testing purpose actually requires realism. For usability testing, a low-fidelity prototype is often more than adequate and faster to iterate.

For feasibility prototypes, fidelity is irrelevant — they are code with no user interface, no error handling, and no polish. Write just enough code to answer the feasibility question.

For live-data prototypes, include only the instrumentation needed for the specific use cases being measured. Do not build full analytics infrastructure.

### Step 4: Confirm Creator and Constraints

**Feasibility prototype:**
- Created by: one or more engineers (not designers, not product managers)
- Typical time: one to two days for most questions; longer for major new technology (machine learning, novel algorithms)
- Constraint: this is discovery code — throwaway. No productization judgment from the product manager. If engineers need to productize, they must be given full delivery time.

**User prototype:**
- Created by: designer (primary); some designers prefer to hand-code high-fidelity prototypes — acceptable if fast and treated as disposable
- Tools: standard prototyping tools (Figma, Framer, etc.) or hand-coded
- Constraint: this is a simulation. There is nothing behind the curtain. No real data, no real transactions. Do not show user prototype results as proof of value.

**Live-data prototype:**
- Created by: engineer(s) — designers cannot create this
- Typical scope: 5–10% of eventual productization effort
- Constraint: not commercially shippable. Explicitly communicate this to executives and stakeholders. The product manager does not decide when this is "good enough" — that judgment belongs to the engineers when they productize.

**Hybrid prototype:**
- Created by: designer (front-end simulation) + engineer or team member operating the backend manually
- Constraint: not scalable — never send significant traffic to a Wizard of Oz prototype. Its value is qualitative learning, not quantitative proof.

### Step 5: Check Anti-Patterns Before Proceeding

Before creating a feasibility prototype, check for these two anti-patterns:

**Anti-pattern: Ambush estimation.** Demanding that engineers provide time or effort estimates in a planning meeting, without giving them time to investigate, produces conservative and inflated answers. Engineers put on the spot without investigation time will give answers designed to make the questioner go away. The correct question is not "Can you do this?" but "What is the best way to do this and how long would it take?" — and only after giving engineers time to investigate. If the answer is a feasibility prototype, encourage them to proceed.

**Anti-pattern: Feasibility-averse product management.** Product managers who hate any idea that requires engineering investigation systematically kill the most innovative product ideas. Many of the best product ideas are based on approaches that are only now possible — which means new technology and investigation time. When engineers say they need a day or two to investigate, treat it as an opportunity, not a liability. Engineers given even a day or two often come back not only with answers to the feasibility question but also with better ways to solve the problem.

Before creating a user prototype, check for this anti-pattern:

**Anti-pattern: Prototype-as-validation confusion.** Showing a high-fidelity user prototype to 10–15 people who say they love it does not validate value. People say all kinds of things and then do something different. A user prototype is not good for proving anything — including whether a product will sell. Use separate value testing techniques (demand validation, quantitative value testing) after usability is confirmed. The user prototype is the input to usability testing and stakeholder alignment, not the output of value validation.

### Step 6: Document the Prototype Plan

Write a brief prototype plan (one page or less) capturing:

```
# Prototype Plan: [Feature / Product Name]

## Risk Being Addressed
[Feasibility / Usability / Value-qualitative / Viability]

## Prototype Type Selected
[Feasibility / User / Live-Data / Hybrid]
Rationale: [one sentence]

## Fidelity Level (for user prototypes)
[Low / Medium / High]
Rationale: [testing purpose requires X]

## Creator
[Engineer(s) / Designer / Both]
Estimated time: [X days]

## What Question This Prototype Answers
[Specific, testable question — e.g., "Can we achieve sub-200ms response time with this algorithm?" or "Can a new user complete account setup without help?"]

## What This Prototype Cannot Answer
[List what will NOT be learned — important for setting expectations]

## Anti-Pattern Check
[ ] No ambush estimation applied to engineers
[ ] Team understands this prototype does not validate value
[ ] Prototype is scoped to just enough to answer the question
[ ] Prototype is treated as disposable

## Next Step After Prototype
[Usability test / Feasibility go/no-go decision / Quantitative value test / Stakeholder review]
```

## Outputs

- Prototype plan document (per template above)
- Prototype artifact (created by engineer or designer per type)
- Anti-pattern check completed and documented

## Key Principles Summary

| Principle | What It Means in Practice |
|---|---|
| Learn at fraction of cost | If prototype takes as long as shipping, it has become delivery |
| Creation forces depth | Build the prototype even when discussion feels sufficient |
| Shared understanding | Use prototypes in stakeholder reviews, not just user tests |
| Right fidelity, not one fidelity | Value testing → high fi; usability → low/medium fi acceptable |
| Prototypes are disposable | Discovery code is not production code; simulations are not products |

## References

- `references/prototype-type-details.md` — Full descriptions of all four prototype types, canonical use cases, limitations, and creation guidance
- `references/fidelity-decision-guide.md` — Fidelity selection decision tree with examples across product types
- `references/feasibility-testing-questions.md` — The 10 feasibility questions engineers answer in discovery (Ch55) and how to structure engineer-led investigation

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — INSPIRED: How to Create Tech Products Customers Love by Marty Cagan.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-product-discovery-risk-assessment`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
