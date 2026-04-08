---
name: architecture-quantum-analyzer
description: Analyze a system's architecture quanta — independently deployable units with distinct quality attribute needs. Use this skill whenever the user needs to determine if their system should be monolith or distributed, is analyzing deployment boundaries, evaluating which parts of a system need different scalability/reliability/performance characteristics, decomposing a monolith, or asking "should this be one service or many?" — even if they don't use the term "quantum."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architecture-quantum-analyzer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - architecture-characteristics-identifier
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [3, 7, 8]
tags: [software-architecture, architecture, quantum, deployment, monolith-vs-distributed, coupling, connascence]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "A software project to analyze for quantum boundaries — or a system description if no codebase exists"
  tools-required: [Read, Grep, Glob]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Best with access to a codebase. Can work from system description for greenfield projects."
---

# Architecture Quantum Analyzer

An **architecture quantum** (or "independently deployable unit") is an independently deployable artifact with high functional cohesion and synchronous connascence. The quantum count determines whether a system should use a monolith or distributed architecture — because different quanta need different quality attributes, and a single monolith can only optimize for one set.

## When to Use

You're deciding whether a system should be one deployable unit or many, or you're analyzing the deployment boundaries of an existing system. Typical situations:

- "Should this be a monolith or microservices?" — quantum analysis provides the answer
- Decomposing a monolith — which parts should separate?
- Performance/scalability issues in one part of a system while other parts are fine
- Different teams need to deploy independently
- Pre-requisite for `architecture-style-selector` — quantum count informs style choice

Before starting, verify:
- Do you know the system's architecture characteristics? If not, use `architecture-characteristics-identifier` first
- Is there a codebase to analyze, or is this a greenfield design?

## Context

### Required Context (must have before proceeding)

- **System description:** What does the system do? What are its major components/services? Ask the user if not apparent.
- **Architecture characteristics:** The quality attributes that matter for this system. If unknown, invoke `architecture-characteristics-identifier` first.

### Observable Context (gather from environment if available)

- **Codebase structure:** Scan for service boundaries, packages, modules
  → Look for: `docker-compose.yml`, `k8s/` manifests, service directories, separate `package.json`/`pyproject.toml` per service
  → These reveal deployment topology and current boundaries
- **Communication patterns:** How do components talk to each other?
  → Look for: HTTP client imports (`httpx`, `requests`, `axios`), message queue imports (`pika`, `kafka`, `amqplib`), gRPC definitions
  → Synchronous = same quantum potential. Asynchronous = different quanta.
- **Database configuration:** Shared database = single quantum. Per-service databases = potential separate quanta
  → Look for: database connection configs, ORM models, migration files
- **Deployment configs:** What deploys together vs separately?
  → Look for: `docker-compose.yml` services, Kubernetes deployments, CI/CD pipeline stages
- **Architecture characteristics per component:** Do different parts have different scaling/reliability needs?
  → Look for: replica counts, resource limits, SLA configs, autoscaling rules

### Default Assumptions

- If no codebase → work from user's system description (greenfield analysis)
- If no deployment configs → assume everything deploys together (monolith)
- If no explicit characteristics per component → ask user which parts have different needs

## Process

### Step 1: Identify Components

**ACTION:** List all major components, services, or modules in the system.

**WHY:** You can't find quantum boundaries without knowing what the pieces are. Components are the building blocks — quanta are how they group based on deployment and coupling. If you're analyzing a codebase, scan the file structure. If greenfield, list the planned components.

**IF** codebase exists → scan directory structure, docker-compose, deployment configs
**ELSE** → ask user to list the major components and their responsibilities

### Step 2: Map Communication Patterns

**ACTION:** For each pair of components that communicate, determine if the communication is synchronous or asynchronous.

**WHY:** This is the critical step. Synchronous connascence (one component waits for another's response) means both components share fate during the call — they MUST have compatible operational characteristics. If Service A calls Service B synchronously and A needs 99.99% availability but B only has 99%, A's availability is capped at B's. Asynchronous communication (fire-and-forget via message queue) breaks this fate-sharing — each component can have independent characteristics.

Map each communication as:
- **Synchronous:** REST calls, gRPC, direct function calls, shared database reads/writes
- **Asynchronous:** Message queues (RabbitMQ, Kafka, SQS), event buses, async event publishing

### Step 3: Identify Architecture Characteristics Per Component

**ACTION:** Determine what quality attributes each component needs. Look for differences between components.

**WHY:** The whole point of quantum analysis is discovering that different parts of the system need DIFFERENT characteristics. If everything needs the same scalability, reliability, and performance — it's one quantum, and a monolith is fine. But if the bidding engine needs extreme elasticity while the payment service needs extreme reliability, they're in different quanta with different architectural needs. This non-uniformity is what drives the need for distributed architecture.

**CAUTION — the uniform characteristics anti-pattern:** Don't assume the whole system has one set of characteristics. This is the most common mistake. Ask: "Does the order processing part of the system need the same scalability as the notification part?" If the answer is no, you have multiple quanta.

### Step 4: Group Into Quanta

**ACTION:** Group components into quanta based on the three-criteria test. Components belong to the same quantum if they satisfy ALL THREE:

1. **Deploy together** — they ship as one unit (or must be deployed in lockstep)
2. **High functional cohesion** — they serve a unified business purpose together
3. **Synchronous connascence** — they communicate synchronously (fate-sharing)

**WHY:** These three criteria are AND conditions, not OR. Two services might deploy independently (criterion 1 fails) but communicate synchronously (criterion 3 met) — they're still NOT the same quantum because independent deployment means they CAN have different characteristics. Conversely, two components that deploy together but serve unrelated purposes (low cohesion) are forced into the same quantum by deployment, but this might be a design problem worth flagging.

**Remember:** Databases are part of the quantum. If two services share a database, they share a quantum — because you can't deploy the database independently from either service.

### Step 5: Analyze Quantum Characteristics

**ACTION:** For each identified quantum, list its driving architecture characteristics (use the top 3 from `architecture-characteristics-identifier`). Note where quanta DIFFER.

**WHY:** The value of quantum analysis is revealing that different quanta have different needs. If Quantum A needs elasticity + performance and Quantum B needs reliability + security, a single monolith cannot optimize for both simultaneously. This difference is what justifies the complexity of distributed architecture.

### Step 6: Determine Architecture Direction

**ACTION:** Based on quantum count and characteristic differences, recommend monolith vs distributed.

**WHY:** This is the payoff. The quantum count IS the architecture style driver:

| Quantum count | Characteristic uniformity | Recommendation |
|:---:|:---:|-------------|
| 1 | N/A (only one) | **Monolith** — single set of characteristics, simple deployment |
| Multiple | Same characteristics | **Monolith might still work** — if quanta need the same things, a monolith can satisfy all |
| Multiple | **Different** characteristics | **Distributed required** — different quanta need different optimization, monolith can't serve both |

## Inputs

- Codebase to analyze (preferred) OR system description for greenfield
- Architecture characteristics (from `architecture-characteristics-identifier` or user input)

## Outputs

### Quantum Analysis Report

```markdown
# Quantum Analysis: {System Name}

## Components Identified
| Component | Responsibility | Deployment unit |
|-----------|---------------|----------------|
| {name} | {what it does} | {how it deploys} |

## Communication Map
| From | To | Type | Mechanism | Fate-sharing? |
|------|-----|------|-----------|:---:|
| {A} | {B} | Sync/Async | REST/MQ/gRPC | Yes/No |

## Quantum Map
| Quantum | Components | Driving Characteristics | Communication type |
|---------|-----------|------------------------|:---:|
| {Quantum 1} | {A, B} | {elasticity, performance} | Internal: sync |
| {Quantum 2} | {C} | {reliability, security} | External: async from Q1 |

## Characteristic Comparison
| Characteristic | Quantum 1 | Quantum 2 | Quantum 3 | Uniform? |
|---------------|-----------|-----------|-----------|:---:|
| {attr} | High/Med/Low | High/Med/Low | High/Med/Low | Yes/No |

## Architecture Direction
**Quantum count:** {N}
**Characteristic uniformity:** {Uniform / Non-uniform}
**Recommendation:** {Monolith / Distributed}
**Reasoning:** {why, based on quantum analysis}

## Warnings
- {Any anti-patterns detected: uniform characteristics assumption, shared DB coupling, etc.}
```

## Key Principles

- **Synchronous connascence = shared fate** — If Service A calls Service B synchronously, they must have compatible operational characteristics for the duration of that call. A highly scalable caller paired with a non-scalable callee creates a bottleneck. This is why sync communication defines quantum boundaries.

- **The database is part of the quantum** — A shared database means shared deployment. You cannot independently deploy services that share a database without risk of schema conflicts. Legacy systems with one shared database are, by definition, a single quantum regardless of how many services exist.

- **Non-uniform characteristics drive distribution** — The ONLY valid reason to accept the complexity of distributed architecture is that different parts of the system need genuinely different quality attributes. If everything needs the same characteristics, keep it monolith. Distribution for its own sake is unnecessary complexity.

- **Don't assume uniformity** — The most common mistake is applying one set of characteristics to the entire system. Ask about each major component: "Does this part need the same scalability/reliability/performance as the other parts?" Differences reveal quantum boundaries.

- **Quantum = bounded context (deployment lens)** — In Domain-Driven Design, bounded contexts define functional boundaries. Architecture quanta add the deployment and operational perspective. A bounded context with its own database that deploys independently IS a quantum.

## Examples

**Scenario: Online auction system (Going Going Gone)**
Trigger: "Our auction platform has bidding, payment, and notification features. Should we use microservices?"
Process: Identified 4 components (Bidder, Auction, Payment, Notification). Mapped communication: Bidder↔Auction is synchronous REST (same quantum — bidders need instant auction state), Auction→Payment is async via message queue (different quantum — payment needs reliability, not speed), Auction→Notification is async (different quantum — notifications can be delayed). Characteristics: Bidding quantum needs elasticity+performance (auction traffic bursts), Payment quantum needs reliability+security, Notification quantum needs availability. Three quanta with different characteristics → distributed architecture required.
Output: Quantum analysis showing 3 quanta, non-uniform characteristics, recommending distributed with event-driven communication between quanta.

**Scenario: Simple ordering system analysis**
Trigger: "We're a small team building an ordering app. Our CTO wants microservices but I think we're overcomplicating things."
Process: Identified components (Order, Inventory, Payment, User). All communicate synchronously via REST, share one PostgreSQL database, deploy as one Docker container. All need the same moderate characteristics (availability, simplicity). One quantum with uniform characteristics → monolith recommended. Flagged the shared database as proof of single quantum.
Output: Quantum analysis showing 1 quantum, recommending monolith. Diplomatically addressed CTO's microservices enthusiasm by showing the quantum analysis doesn't justify distribution.

**Scenario: Codebase analysis of existing system**
Trigger: User has a codebase at `./test-env/` — "Analyze this system's architecture quanta"
Process: Scanned docker-compose.yml, found 4 services with different networks. Read source files, found synchronous HTTP calls (httpx) between bidder and auction services, asynchronous RabbitMQ between auction→payment and auction→notification. Read architecture-characteristics.yaml, found different characteristic profiles per service. Grouped: Bidder+Auction (sync, shared network, same scaling) = Quantum 1, Payment (async consumer, independent) = Quantum 2, Notification (async consumer, independent) = Quantum 3.
Output: Full quantum analysis with communication map, quantum groupings, characteristic comparison, and distributed architecture recommendation.

## References

- For connascence types and their implications, see [references/connascence-types.md](references/connascence-types.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-architecture-characteristics-identifier`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
