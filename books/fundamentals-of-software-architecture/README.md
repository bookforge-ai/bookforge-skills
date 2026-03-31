# Fundamentals of Software Architecture Skills

19 agent skills distilled from **Fundamentals of Software Architecture: An Engineering Approach** by Mark Richards and Neal Ford.

These skills teach AI coding agents how to guide the full software architecture lifecycle — from identifying quality attributes and analyzing modularity, through selecting architecture styles and designing governance, to documenting decisions and facilitating risk assessment. The agent applies the book's specific frameworks, scoring models, and taxonomies to produce structured architecture artifacts.

**Average quality delta: +72 points** (97% with-skill vs 25% baseline).

## Skills

### Foundation & Analysis (Level 0 — 11 skills)

| Skill | Description | Mode |
|-------|-------------|------|
| architect-role-assessor | Evaluate architect performance against 8 core expectations and technical breadth vs depth balance | hybrid |
| architecture-characteristics-identifier | Systematically identify, categorize, and prioritize quality attributes (-ilities) from requirements and domain concerns | full |
| architecture-tradeoff-analyzer | Analyze trade-offs across quality attribute dimensions for architecture decisions | full |
| modularity-health-evaluator | Assess code modularity using LCOM, coupling metrics, abstractness, instability, and connascence taxonomy | hybrid |
| architecture-risk-assessor | Quantify architecture risk using a 2D risk matrix (impact x likelihood, scored 1-9) | full |
| distributed-feasibility-checker | Evaluate distributed architecture feasibility against the 8 Fallacies of Distributed Computing | full |
| event-driven-topology-selector | Choose between broker and mediator event-driven topologies | full |
| architecture-diagram-creator | Create architecture diagrams following UML, C4, and ArchiMate standards | full |
| architect-control-calibrator | Determine appropriate architect control level using a 5-factor scoring model (-100 to +100) | full |
| development-checklist-generator | Create effective development checklists (code completion, testing, release) | full |
| stakeholder-negotiation-planner | Prepare architecture negotiation strategies for stakeholder conversations | hybrid |

### Design & Governance (Level 1 — 6 skills)

| Skill | Description | Mode | Depends On |
|-------|-------------|------|------------|
| architecture-decision-record-creator | Create structured ADRs with 7 sections and full justification | full | architecture-tradeoff-analyzer |
| architecture-quantum-analyzer | Analyze architecture quanta — independently deployable units with distinct quality needs | hybrid | architecture-characteristics-identifier |
| component-identifier | Decompose systems into well-defined components using structured discovery | full | architecture-characteristics-identifier |
| risk-storming-facilitator | Plan and facilitate collaborative risk storming sessions | plan-only | architecture-risk-assessor |
| service-based-architecture-designer | Design service-based architecture with 4-12 domain services | full | architecture-characteristics-identifier |
| architecture-fitness-function-designer | Design automated governance mechanisms (fitness functions) | hybrid | architecture-characteristics-identifier, modularity-health-evaluator |

### Style Selection & Optimization (Level 2 — 2 skills)

| Skill | Description | Mode | Depends On |
|-------|-------------|------|------------|
| architecture-style-selector | Guide systematic architecture style selection across all major styles | full | architecture-characteristics-identifier, architecture-quantum-analyzer |
| microservice-granularity-optimizer | Right-size microservice boundaries using disintegrator/integrator forces | hybrid | component-identifier |

## Dependency Graph

```
Level 0 (independent — 11 skills):
  architect-role-assessor
  architecture-characteristics-identifier
  architecture-tradeoff-analyzer
  modularity-health-evaluator
  architecture-risk-assessor
  distributed-feasibility-checker
  event-driven-topology-selector
  architecture-diagram-creator
  architect-control-calibrator
  development-checklist-generator
  stakeholder-negotiation-planner

Level 1 (6 skills):
  architecture-decision-record-creator ──> architecture-tradeoff-analyzer
  architecture-quantum-analyzer ──> architecture-characteristics-identifier
  component-identifier ──> architecture-characteristics-identifier
  risk-storming-facilitator ──> architecture-risk-assessor
  service-based-architecture-designer ──> architecture-characteristics-identifier
  architecture-fitness-function-designer ──> architecture-characteristics-identifier
                                         ──> modularity-health-evaluator

Level 2 (2 skills):
  architecture-style-selector ──> architecture-characteristics-identifier
                               ──> architecture-quantum-analyzer
  microservice-granularity-optimizer ──> component-identifier
```

## Install Profiles

**Full** (all 19 skills) — Complete software architecture toolkit covering the entire lifecycle.

**Decision-making** (8 skills) — Core decision-making skills for architecture selection and governance:
- `architecture-characteristics-identifier`
- `architecture-tradeoff-analyzer`
- `architecture-quantum-analyzer`
- `architecture-style-selector`
- `distributed-feasibility-checker`
- `component-identifier`
- `architecture-decision-record-creator`
- `architecture-risk-assessor`

**Essentials** (5 skills) — Minimum for architecture guidance:
- `architecture-characteristics-identifier`
- `architecture-tradeoff-analyzer`
- `architecture-quantum-analyzer`
- `architecture-style-selector`
- `architecture-decision-record-creator`

## Attribution

Skills distilled from **Fundamentals of Software Architecture: An Engineering Approach** by Mark Richards and Neal Ford (O'Reilly, 2020). The skills encode the book's architecture frameworks, scoring models, and taxonomies in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, case studies, and discussion.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
