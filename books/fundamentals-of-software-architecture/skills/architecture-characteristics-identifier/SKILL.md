---
name: architecture-characteristics-identifier
description: Systematically identify, categorize, and prioritize architecture characteristics (quality attributes / -ilities) from requirements, domain concerns, and stakeholder input. Use this skill whenever the user is starting a new project, defining architecture requirements, translating business needs into technical characteristics, asking "what quality attributes matter?", figuring out nonfunctional requirements, or evaluating what -ilities to optimize for — even if they don't explicitly say "architecture characteristics."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architecture-characteristics-identifier
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []  # Foundation skill — no dependencies
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [4, 5]
tags: [software-architecture, architecture, quality-attributes, requirements, nonfunctional-requirements, ilities]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "Requirements, domain concerns, or stakeholder priorities from the user"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, can scan for existing architecture docs."
---

# Architecture Characteristics Identifier

## When to Use

You're at the start of an architecture decision — before choosing patterns, styles, or technologies. The team needs to understand which quality attributes actually matter for THIS system. Typical situations:

- New project kicking off — "what should we optimize for?"
- Requirements review — translating business language into technical characteristics
- Stakeholder disagreement — everyone has different priorities, need structured resolution
- Architecture audit — evaluating whether an existing system's characteristics match its needs
- Pre-requisite for other skills — `architecture-style-selector`, `architecture-fitness-function-designer`, and others depend on knowing the driving characteristics first

Before starting, verify:
- Are there requirements, domain concerns, or stakeholder inputs to work from? (If nothing exists, help the user articulate their domain concerns first)
- Is this about identifying characteristics (this skill) or analyzing trade-offs between options (use `architecture-tradeoff-analyzer` instead)?

## Context

### Required Context (must have before proceeding)

- **Domain or project description:** What is this system for? What problem does it solve? Ask the user if not stated.
- **At least one source of characteristics:** Requirements document, stakeholder concerns, domain description, or existing system to audit.

### Observable Context (gather from environment if available)

- **Requirements documents:** Search for requirements, PRDs, specs
  → Look for: `docs/`, `requirements/`, `*.prd.md`, `README` sections about goals
  → If unavailable: work from user's verbal description
- **Existing architecture docs:** Check for prior characteristic decisions
  → Look for: ADRs, architecture docs, existing `-ilities` lists
  → If found: audit and update rather than start from scratch
- **Codebase structure:** If a system exists, its structure reveals implicit characteristics
  → Look for: caching layers (performance), retry logic (reliability), auth modules (security), i18n files (localization)
  → If no codebase: greenfield, start from requirements

### Default Assumptions

- If no requirements exist → work from user's verbal domain description
- If no stakeholders available → ask the user to role-play key stakeholders (CTO, product, ops)
- If domain is unfamiliar → apply the three common implicit characteristics (availability, reliability, security) and ask probing questions

## Process

### Step 1: Gather Domain Concerns

**ACTION:** Identify what the business stakeholders care about. Translate their language into a domain concerns list.

**WHY:** Stakeholders speak in business language ("we need to merge with Company X", "time to market is critical", "users must love it"). Architects speak in -ilities ("interoperability", "deployability", "usability"). If you skip this translation, you'll optimize for the wrong things. The "lost in translation" problem is the #1 cause of architecture-business misalignment.

Common domain concerns and what they map to:

| Domain Concern | Architecture Characteristics |
|----------------|------------------------------|
| Mergers and acquisitions | Interoperability, scalability, adaptability, extensibility |
| Time to market | Agility, testability, deployability |
| User satisfaction | Performance, availability, fault tolerance, testability, deployability, agility, security |
| Competitive advantage | Agility, testability, deployability, scalability, availability, fault tolerance |
| Time and budget | Simplicity, feasibility |

For the full domain-concern mapping table, see [references/domain-concern-mapping.md](references/domain-concern-mapping.md).

**CAUTION:** Don't over-simplify the translation. "Agility" is NOT the same as "time to market" — agility = agility + testability + deployability. Focusing on only one ingredient is like forgetting to put the flour in the cake batter.

**IF** stakeholders are available → facilitate a brief discussion: "What are your top business concerns for this system?"
**ELSE** → ask the user to state the key domain concerns, or infer from the domain description.

### Step 2: Extract from Requirements

**ACTION:** Analyze requirements (explicit or stated by user) and extract architecture characteristics from each one.

**WHY:** Requirements contain encoded architecture characteristics. "Support 10,000 concurrent users" explicitly calls for scalability. But a single requirement often implies MULTIPLE characteristics. The classic trap: a stakeholder says "end-of-day fund pricing must complete on time" — an ineffective architect focuses only on performance. A good architect recognizes the need for performance AND availability AND scalability AND reliability AND recoverability AND auditability. It doesn't matter how fast the system is if it crashes at 85% load.

For each requirement:
1. Identify the EXPLICIT characteristic (what it directly states)
2. Probe for HIDDEN characteristics (what else must be true for this requirement to be met?)
3. Check if it requires special STRUCTURAL support (not just implementation) — if it doesn't influence structure, it's a design concern, not an architecture characteristic

### Step 3: Identify Implicit Characteristics

**ACTION:** Add characteristics that aren't in requirements but are necessary for the domain.

**WHY:** The most dangerous characteristics are the ones nobody writes down. Every web application needs availability, reliability, and security — but these rarely appear in requirements because stakeholders assume they're obvious. An architect who only addresses explicitly stated requirements will build a system that fails on implicit needs. Experience in the problem domain is what surfaces these.

Always consider these three for any system:
- **Availability** — can users access it?
- **Reliability** — does it stay up during interactions?
- **Security** — is it protected against threats?

Then probe domain-specific implicit characteristics:
- Handling payments? → security rises to architecture level (needs structural isolation)
- Serving global users? → localization, legal compliance, data residency
- Burst traffic patterns? → elasticity (not just scalability — elasticity handles SPIKES, scalability handles GROWTH)

### Step 4: Validate with the Three-Criteria Test

**ACTION:** For each candidate characteristic, verify it passes ALL three criteria:

1. **Specifies a nondomain design consideration** — It's about HOW to build, not WHAT to build
2. **Influences some structural aspect of the design** — It requires special architectural support, not just good implementation
3. **Is critical or important to application success** — The system would fail or significantly underperform without it

**WHY:** Without validation, the list inflates with everything anyone can think of. Every system COULD support every characteristic, but SHOULDN'T — each one adds complexity. The three-criteria test is the filter that separates real architecture characteristics from design concerns and wishful thinking. If a characteristic doesn't influence structure, handle it at the design level instead.

**IF** a characteristic fails criterion 2 (doesn't influence structure) → it's a design concern, not an architecture characteristic. Note it for the development team but don't include it in the architecture characteristics list.

### Step 5: Categorize

**ACTION:** Organize the validated characteristics into three categories: Operational, Structural, Cross-Cutting.

**WHY:** Categorization reveals blind spots. If all your characteristics are operational (performance, scalability, availability) and none are structural (maintainability, extensibility), you might be building a fast system that's impossible to change. If they're all cross-cutting (security, legal, accessibility), you might be ignoring operational realities. A balanced list across categories is a sign of thorough analysis.

- **Operational:** How the system runs (availability, scalability, performance, reliability, elasticity)
- **Structural:** How the code is organized (maintainability, extensibility, modularity, testability, deployability)
- **Cross-Cutting:** Spans both (security, accessibility, observability, legal, privacy)

For the full taxonomy with definitions, see [references/characteristics-taxonomy.md](references/characteristics-taxonomy.md).

### Step 6: Prioritize to Top 3

**ACTION:** Force-rank to the top 3 driving characteristics. No more.

**WHY:** Trying to optimize for everything produces a generic architecture that optimizes for nothing. Each additional characteristic you support complicates the overall design — like flying a helicopter where every control affects every other control. The Swedish warship Vasa tried to be both a troop transport AND a gunship with two decks of oversized cannons. It capsized and sank on its maiden voyage. Three characteristics is the practical limit for what one architecture can genuinely drive.

Facilitation technique:
1. Present the validated list to stakeholders
2. Ask: "Pick your top 3. Not in priority order — just the 3 most critical."
3. If they resist eliminating any, use the elimination exercise: "If you MUST eliminate one, which would it be?"
4. The top 3 become the DRIVING characteristics. Others are still acknowledged but don't drive architecture decisions.

**IF** stakeholders insist on more than 3 → explain the Vasa story and the helicopter metaphor. More is not better — it's more complex, more expensive, and more fragile.

### Step 7: Produce the Characteristics Report

**ACTION:** Document the identified, validated, categorized, and prioritized characteristics.

**WHY:** This report becomes the input for architecture style selection, fitness function design, and trade-off analysis. Without it, downstream decisions lack a foundation. It also creates alignment — stakeholders sign off on what matters, preventing the "Groundhog Day" anti-pattern (revisiting the same decisions because nobody recorded the rationale).

## Inputs

- Requirements document, PRD, or verbal project description
- Domain concerns from stakeholders (or user role-playing stakeholders)
- Optionally: existing codebase or architecture docs to audit

## Outputs

### Architecture Characteristics Report

```markdown
# Architecture Characteristics: {System Name}

## Domain Concerns
| Concern | Source | Mapped Characteristics |
|---------|--------|----------------------|
| {concern} | {stakeholder/requirement} | {characteristic1, characteristic2} |

## Identified Characteristics

### Explicit (from requirements)
| Characteristic | Source Requirement | Reasoning |
|---------------|-------------------|-----------|
| {characteristic} | {requirement} | {why this requirement implies this characteristic} |

### Implicit (from domain knowledge)
| Characteristic | Reasoning |
|---------------|-----------|
| {characteristic} | {why this is needed even though no one asked for it} |

## Three-Criteria Validation
| Characteristic | Nondomain? | Influences Structure? | Critical? | Verdict |
|---------------|:---:|:---:|:---:|---------|
| {char} | Yes/No | Yes/No | Yes/No | Include / Design-only / Exclude |

## Categorization
| Category | Characteristics |
|----------|----------------|
| Operational | {list} |
| Structural | {list} |
| Cross-Cutting | {list} |

## Top 3 Driving Characteristics
1. **{#1}** — {why this is driving}
2. **{#2}** — {why this is driving}
3. **{#3}** — {why this is driving}

### Acknowledged but not driving
- {characteristic}: {why it's important but not top 3}

## Characteristics NOT Included (and why)
- {candidate}: {failed criterion X / is a design concern / not critical enough}
```

## Key Principles

- **Three-criteria test is the gatekeeper** — A characteristic must be nondomain, influence structure, AND be critical to success. Anything less is a design concern, not an architecture characteristic. This filter prevents characteristic bloat.

- **Implicit characteristics are the dangerous ones** — What nobody writes down in requirements is often what kills the project. Availability, reliability, and security are almost always implicit. An architect's domain experience is what surfaces these.

- **Top 3, not top 10** — Every additional characteristic complicates the architecture like adding controls to a helicopter. The Vasa warship sank because it tried to optimize for too many things. Force stakeholders to choose 3 driving characteristics. This creates focus, not limitation.

- **Translate, don't transcribe** — Stakeholders say "time to market." That's NOT one characteristic — it's agility + testability + deployability. A single domain concern maps to multiple characteristics, and a single requirement often implies multiple characteristics. The translation table is your tool.

- **Over-specifying is as bad as under-specifying** — Adding characteristics you don't need is just as damaging as missing ones you do need. Each unnecessary characteristic adds complexity, cost, and design constraints. When in doubt, leave it out and handle at the design level.

- **Explicit vs implicit, not obvious vs hidden** — Explicit means it's stated in requirements. Implicit means it's necessary but unstated. Don't confuse "obvious" with "explicit" — security is obvious but almost always implicit (unstated in requirements). The distinction matters because implicit characteristics require the architect to proactively surface them.

## Examples

**Scenario: Online sandwich ordering system (Silicon Sandwiches)**
Trigger: "We're building a national online sandwich ordering platform for our franchise chain. What should we optimize for?"
Process: Gathered domain concerns: thousands to millions of users, mealtime burst traffic, franchise customization, online payments, overseas expansion plans, cost-conscious hiring. Extracted explicit characteristics: scalability (user volume), elasticity (mealtime bursts — lurking in the domain, not in requirements), performance (peak times), customizability (franchise-specific behavior). Identified implicit: availability, reliability, security (payments). Validated all against three-criteria test — security doesn't require special structure because payments are handled by a third-party processor, so it stays at design level. Categorized and prioritized: top 3 = scalability, elasticity, customizability.
Output: Characteristics report with 7 candidates, 4 validated, 3 driving. Customizability flagged as architecture-vs-design trade-off (microkernel structure vs Template Method pattern).

**Scenario: Regulatory financial system**
Trigger: "We need to build an end-of-day fund pricing system. The regulator says we absolutely must complete pricing on time."
Process: The naive approach: focus on performance. The thorough approach: "complete on time" requires performance AND availability (system must be up) AND scalability (handle growing fund count) AND reliability (no crashes at 85% load) AND recoverability (recover quickly if something fails) AND auditability (regulators need proof it completed). One requirement → six characteristics. Validated all, categorized, prioritized top 3: reliability, performance, auditability.
Output: Characteristics report showing how one business statement expanded into 6 characteristics, with justification for top 3 selection.

**Scenario: Startup MVP with stakeholder disagreement**
Trigger: "Our CTO wants scalability, product wants time-to-market, and our investor wants low cost. We're 4 developers. What matters?"
Process: Mapped domain concerns: CTO's scalability, product's time-to-market (= agility + testability + deployability), investor's cost (= simplicity + feasibility). Identified implicit: availability, security. Validated — for a 4-person startup MVP, scalability doesn't influence structure YET (can scale later with cloud auto-scaling, no special architecture needed now). Removed from architecture characteristics, noted as design concern. Top 3: agility, simplicity, availability. Elimination exercise confirmed: if forced to drop one, drop availability (cloud platforms provide baseline availability).
Output: Characteristics report that diplomatically resolves stakeholder disagreement by showing that scalability is valid but premature as an architecture driver for an MVP.

## References

- For the full taxonomy of architecture characteristics with definitions, see [references/characteristics-taxonomy.md](references/characteristics-taxonomy.md)
- For the domain-concern-to-characteristic translation table, see [references/domain-concern-mapping.md](references/domain-concern-mapping.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
