---
name: component-identifier
description: Decompose a system into well-defined components using structured discovery techniques. Use this skill whenever the user is designing a new system from requirements, breaking down a monolith into modules, deciding how to organize code into packages/services, asking "what components should this system have?", or struggling with component granularity — even if they don't use the word "component."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/component-identifier
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - architecture-characteristics-identifier
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [8]
tags: [software-architecture, architecture, components, decomposition, modularity, domain-driven-design]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "System requirements, user stories, or domain description — the skill guides discovery from there"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, can analyze existing component structure."
---

# Component Identifier

## When to Use

You're designing a system and need to figure out what the building blocks should be — what components, modules, or services to create and how they relate. Typical situations:

- New system from requirements — "we have these user stories, what components do we need?"
- Monolith restructuring — "our code is a mess, how should we reorganize?"
- Pre-requisite for architecture style selection — components feed into quantum analysis
- Team is falling into the Entity Trap — creating `UserManager`, `OrderManager` instead of real components

Before starting, verify:
- Do you have requirements, user stories, or at least a domain description? If not, help gather them first.
- Do you know the architecture characteristics? If not, use `architecture-characteristics-identifier` first — characteristics affect component division.

## Context & Input Gathering

### Input Sufficiency Check

The skill needs to know WHO uses the system and WHAT they do. Without actors and actions, component identification is guesswork.

Check the user's prompt for:
- System purpose and domain
- Users/roles/actors
- Key workflows or use cases
- Any existing structure (if restructuring)

### Required Context (must have — ask if missing)

- **System purpose:** What does this system do?
  → Check prompt for: domain description, problem statement
  → If missing, ask: "In one sentence, what is the main purpose of this system?"

- **Actors/users:** Who uses this system?
  → Check prompt for: user types, roles, personas
  → If missing, ask: "Who are the main types of users? For example: customers, admins, operators, external systems?"

- **Key workflows:** What do users DO with the system?
  → Check prompt for: user stories, features, use cases, actions
  → If missing, ask: "What are the 5-7 most important things users do with this system? For example: place an order, submit a review, process a payment."

### Observable Context (gather from environment)

- **Existing codebase:** If restructuring, scan for current component structure
  → Look for: package directories, service folders, module boundaries
  → Reveals: current partitioning (technical vs domain), coupling patterns
- **Architecture characteristics:** If already identified, use them to inform component division
  → Look for: output from `architecture-characteristics-identifier`
  → Reveals: which parts need different quality attributes

### Default Assumptions

- If no existing system → greenfield, use domain partitioning (industry-standard default)
- If actors unclear → assume at least: end user, admin, external system
- If partitioning preference not stated → recommend domain partitioning (book's recommendation for modern architectures)

### Sufficiency Threshold

```
SUFFICIENT when: system purpose + at least 3 actors + at least 5 workflows are known
PROCEED WITH DEFAULTS when: system purpose is known but actors/workflows are sparse
MUST ASK when: system purpose is unclear or no workflows are stated
```

## Process

### Step 1: Choose Partitioning Style

**ACTION:** Decide between technical partitioning (layers) and domain partitioning (workflows).

**WHY:** This is the most fundamental decision — it determines the shape of everything else. Technical partitioning (Presentation → Business Rules → Persistence) was the standard for decades, but domain partitioning (organized by business workflows) has become the industry standard for both monoliths and microservices. Domain partitioning makes it easier to migrate to distributed architecture later, aligns with how the business thinks, and produces components with higher functional cohesion.

| Style | Organizes by | Best for | Watch out for |
|-------|-------------|----------|--------------|
| **Technical** | Layers: presentation, business, persistence | Simple CRUD apps, teams familiar with layered patterns | Domains smeared across layers, hard to migrate |
| **Domain** | Workflows: order processing, inventory, shipping | Modern apps, microservice-ready, cross-functional teams | Customization code appears in multiple places |

**IF** the user hasn't specified → recommend domain partitioning with explanation.
**IF** the user has an existing technically-partitioned system → note the trade-offs of restructuring.

### Step 2: Identify Actors and Actions

**ACTION:** List all actors (users, roles, external systems) and map their actions.

**WHY:** Components should align with what users DO, not what data exists. The Actor/Actions approach (from the Rational Unified Process) starts from real usage patterns, not database tables. This prevents the Entity Trap — the most common component identification mistake. If you start from "what data do we store?", you get `UserManager`, `OrderManager` (an ORM, not an architecture). If you start from "what do users do?", you get `PlaceOrder`, `ProcessPayment`, `ManageInventory` (real workflows).

**Alternative:** For event-heavy systems, use Event Storming instead — map domain events first, then group into components.

Output a table:
```
| Actor | Actions |
|-------|---------|
| Customer | Browse catalog, place order, track delivery, submit review |
| Store owner | Manage inventory, set prices, view reports |
| Payment system | Process payment, issue refund |
```

### Step 3: Map Actions to Initial Components

**ACTION:** Group related actions into candidate components. Each component should represent a cohesive workflow.

**WHY:** The goal is a coarse-grained substrate — not the final design. The likelihood of getting the perfect design on the first attempt is "disparagingly small" (the book's words). What you're building is a starting hypothesis to iterate on. Grouping related actions ensures each component has a clear, unified purpose — high functional cohesion.

Rules for grouping:
- Actions that always happen together → same component
- Actions performed by the same actor on the same domain concept → likely same component
- Actions that need different quality attributes → likely different components

### Step 4: Assign Requirements to Components

**ACTION:** Map each requirement/user story to the component that handles it. Look for mismatches.

**WHY:** This is the validation step — if a requirement doesn't fit cleanly into any component, either the requirement spans too many concerns or the component boundaries are wrong. Requirements that force you to touch 3+ components for a single user action indicate the wrong granularity.

Watch for:
- Requirements that don't fit any component → create a new one
- Requirements that span many components → either the requirement is too broad or components need restructuring
- Components with no requirements → remove them (they're imaginary)

### Step 5: Analyze Architecture Characteristics Per Component

**ACTION:** Check if different components need different quality attributes. Components with different characteristics may need to be in different deployment units (quanta).

**WHY:** This is where component identification connects to quantum analysis. If the Order Processing component needs high elasticity (flash sales) but the Reporting component needs only batch processing, they have different characteristic profiles. This difference suggests they should be separate quanta — which drives the monolith vs distributed decision. Without this step, you might design components that look clean but can't be deployed or scaled appropriately.

**IF** components have uniform characteristics → they can stay in one deployment unit (monolith is fine).
**IF** components have different characteristics → flag for `architecture-quantum-analyzer`. These may become separate quanta.

### Step 6: Check for the Entity Trap

**ACTION:** Review the component design for signs of the Entity Trap anti-pattern.

**WHY:** The Entity Trap is the #1 component identification mistake. It happens when the architect creates components that mirror database entities (`UserManager`, `OrderManager`, `ProductManager`) with CRUD operations instead of real workflow components. This produces an ORM, not an architecture — high coupling, low cohesion, no clear behavior boundaries. The fix is to refocus on workflows: "what does the system DO?" not "what does it STORE?"

Detection checklist:
- [ ] Components are named `[Entity]Manager` or `[Entity]Service`
- [ ] Each component has primarily Create/Read/Update/Delete operations
- [ ] Components map 1:1 to database tables
- [ ] No workflow or behavioral logic is captured

**IF** Entity Trap detected → restructure around workflows using Step 2's actors/actions.

### Step 7: Assess Granularity and Iterate

**ACTION:** Evaluate whether each component is the right size. Restructure if needed.

**WHY:** There is no formula for the right granularity — it requires iterative refinement. Too fine-grained = too much communication between components (chatty architecture). Too coarse-grained = too many responsibilities per component (bloated modules). The sweet spot is components where each handles one cohesive workflow without excessive external calls.

Signs of wrong granularity:
- **Too fine:** A single user action requires calling 5+ components
- **Too coarse:** A single component handles 10+ unrelated responsibilities
- **Just right:** Each component handles 2-5 related actions with minimal cross-component calls

This step feeds back to Step 3 — iterate until stable.

## Inputs

- System requirements, user stories, or domain description
- Architecture characteristics (from `architecture-characteristics-identifier` or user input)
- Optionally: existing codebase to restructure

## Outputs

### Component Identification Report

```markdown
# Component Design: {System Name}

## Partitioning Style
{Domain / Technical} — {reasoning}

## Actors and Actions
| Actor | Actions |
|-------|---------|
| {actor} | {action1, action2, action3} |

## Identified Components
| Component | Responsibility | Key actions | Architecture characteristics |
|-----------|---------------|-------------|----------------------------|
| {name} | {what it does} | {actions it handles} | {relevant -ilities} |

## Requirement Mapping
| Requirement/Story | Component(s) | Notes |
|-------------------|-------------|-------|
| {requirement} | {component} | {any concerns} |

## Entity Trap Check
{Pass / Warning} — {reasoning}

## Granularity Assessment
{Assessment of component sizing — any too fine or too coarse?}

## Characteristic Variance
| Component | Primary characteristic | Differs from others? |
|-----------|---------------------|:---:|
| {component} | {characteristic} | Yes/No |

{If variance detected: flag for quantum analysis}

## Component Relationship Map
{Text diagram showing how components communicate and depend on each other}
```

## Key Principles

- **Workflows, not entities** — Components should represent what the system DOES, not what it STORES. "Process Order" is a component. "Order Manager" is an Entity Trap. Start from actors and actions, not from the database schema.

- **Domain partitioning by default** — The industry trend is firmly toward domain partitioning for both monoliths and microservices. Technical partitioning (layers) smears domains across all layers and makes migration to distributed architecture difficult. Unless you have a specific reason for layers, use domain partitioning.

- **Iteration is the process** — The chance of getting the right component design on the first attempt is near zero. Build a hypothesis, map requirements, find the mismatches, restructure. Component identification is inherently iterative — don't expect to be done in one pass.

- **Different characteristics = different components** — If two parts of the system need different quality attributes (one needs high availability, another needs high throughput), they should be separate components. This separation is what enables them to become separate quanta if needed.

- **Granularity has no formula** — Too fine = chatty. Too coarse = bloated. There's no mathematical answer. The right size is where each component handles one cohesive workflow without excessive cross-component calls. Use the iterative cycle to converge.

- **Ask about workflows, not data** — When gathering input from stakeholders, ask "what do your users DO?" not "what data do you have?" The first question reveals components. The second reveals the Entity Trap.

## Examples

**Scenario: Online auction system (Going, Going, Gone)**
Trigger: "We're building an online auction platform. What components do we need?"
Process: Asked about actors — identified Bidder, Auctioneer, System Admin. Mapped actions: Bidder (view items, place bids, track bids), Auctioneer (create auction, start/stop, manage items), Admin (manage users, view reports). Grouped into components: BidCapture, BidTracking, AuctionSession, ItemManagement, UserManagement, Reporting. Analyzed characteristics — discovered BidCapture needs different characteristics for bidders (high elasticity) vs auctioneers (high reliability). Split BidCapture into BidderCapture + AuctioneerCapture. Entity Trap check: passed — components are workflow-based, not entity-based. Flagged characteristic variance for quantum analysis.
Output: 7 components with characteristic analysis showing the BidderCapture/AuctioneerCapture split and quantum implications.

**Scenario: Detecting the Entity Trap**
Trigger: "Here's our current design: UserManager, OrderManager, ProductManager, PaymentManager. Each handles CRUD for its entity. Does this look right?"
Process: Immediately identified the Entity Trap — all components are [Entity]Manager with CRUD operations. This is an ORM, not an architecture. Asked about actors and workflows: who uses this system and what do they do? Discovered workflows: "browse catalog and place order" (spans Product + Order + Payment), "process payment and update inventory" (spans Payment + Product). Restructured around workflows: OrderProcessing (browse → select → checkout), PaymentProcessing (charge → confirm → receipt), InventoryManagement (stock → reorder → catalog), UserAuthentication. Entity Trap check: resolved.
Output: Restructured from 4 entity-based to 4 workflow-based components with explanation of why the original design was an Entity Trap.

**Scenario: Greenfield with sparse requirements**
Trigger: "We're building an employee scheduling app for a hospital. That's all I know so far."
Process: Insufficient information — asked clarifying questions one at a time: (1) "Who are the main users?" → nurses, doctors, HR admin, department heads. (2) "What are the key things these users do?" → request shifts, swap shifts, approve PTO, generate compliance reports, view schedules. (3) "Are there parts with different performance/availability needs?" → yes, the schedule viewer needs to be always-on (nurses check between rounds) but reporting is weekly batch. Used Actor/Actions to identify: ShiftScheduling, ShiftSwapping, PTOManagement, ComplianceReporting, ScheduleViewing. Flagged ScheduleViewing vs ComplianceReporting as having different availability characteristics.
Output: 5 components with input gathering process documented, showing how asking the right questions leads to better component design.

## References

- For component discovery techniques in detail, see [references/discovery-techniques.md](references/discovery-techniques.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-architecture-characteristics-identifier`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
