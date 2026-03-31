# GoF Design Patterns Skills

15 agent skills distilled from **Design Patterns: Elements of Reusable Object-Oriented Software** by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides (Gang of Four).

These skills teach AI coding agents how to identify design problems in object-oriented codebases, select appropriate GoF patterns using structured analytical frameworks, and implement patterns with full awareness of trade-offs, consequences, and related patterns. The agent reads your code, diagnoses design smells, recommends patterns, and produces refactored implementations.

**Average quality delta: +33 points** (~96% with-skill vs ~63% baseline).

## Skills

### Tier 1 — Selection & Foundation (6 skills)

| Skill | Description | Mode | Role |
|-------|-------------|------|------|
| design-pattern-selector | Select the right GoF pattern using variability analysis, purpose×scope classification, and the 8 causes of redesign | full | hub |
| oo-design-principle-evaluator | Evaluate OO design against "program to an interface" and "favor composition over inheritance" with the 4 inheritance failure modes | hybrid | foundation |
| oo-design-smell-detector | Detect design smells using the GoF causes-of-redesign taxonomy with spread×friction severity matrix | full | foundation |
| creational-pattern-selector | Select the right creational pattern using parameterization strategies and evolution path analysis | full | category-selector |
| structural-pattern-selector | Select the right structural pattern using GoF disambiguation criteria (intent, recursion, lifecycle timing) | full | category-selector |
| behavioral-pattern-selector | Select the right behavioral pattern using encapsulation taxonomy and sender-receiver decoupling analysis | full | category-selector |

### Tier 2 — Pattern Implementors (8 skills)

| Skill | Description | Mode | Depends On |
|-------|-------------|------|------------|
| observer-pattern-implementor | Implement Observer with push/pull model, dangling reference prevention, aspect-based registration, and ChangeManager assessment | full | behavioral-pattern-selector |
| strategy-pattern-implementor | Implement Strategy with context-strategy interface design, Flyweight optimization, and client-awareness trade-off | full | behavioral-pattern-selector |
| command-pattern-implementor | Implement Command with undo/redo, macro commands, and command history | full | behavioral-pattern-selector |
| composite-pattern-implementor | Implement Composite with safety-vs-transparency decision, parent references, and caching for aggregate operations | full | structural-pattern-selector |
| visitor-pattern-implementor | Implement Visitor with stability decision rule, double-dispatch explanation, encapsulation warning, and Iterator integration | full | behavioral-pattern-selector |
| abstract-factory-implementor | Implement Abstract Factory with extensibility liability analysis, singleton refinement, and initialization strategy | full | creational-pattern-selector |
| decorator-pattern-implementor | Implement Decorator with lightweight Component principle, composition order semantics, and "lots of little objects" debugging | full | structural-pattern-selector |
| bridge-pattern-implementor | Implement Bridge with evaluate-extremes interface derivation, Abstract Factory wiring, and Bridge-vs-Strategy distinction | full | structural-pattern-selector |

### Tier 2 — Capstone (1 skill)

| Skill | Description | Mode | Depends On |
|-------|-------------|------|------------|
| multi-pattern-system-designer | Design systems using multiple interacting GoF patterns with problem decomposition, pattern interaction mapping, and coherence verification | full | design-pattern-selector + all 3 category selectors |

## Dependency Graph

```
Level 0 (independent):
  design-pattern-selector (hub)
  oo-design-principle-evaluator
  oo-design-smell-detector
  creational-pattern-selector ──> design-pattern-selector
  structural-pattern-selector ──> design-pattern-selector
  behavioral-pattern-selector ──> design-pattern-selector

Level 1 (implementors):
  observer-pattern-implementor ──> behavioral-pattern-selector
  strategy-pattern-implementor ──> behavioral-pattern-selector
  command-pattern-implementor ──> behavioral-pattern-selector
  visitor-pattern-implementor ──> behavioral-pattern-selector
  composite-pattern-implementor ──> structural-pattern-selector
  decorator-pattern-implementor ──> structural-pattern-selector
  bridge-pattern-implementor ──> structural-pattern-selector
  abstract-factory-implementor ──> creational-pattern-selector

Level 2 (capstone):
  multi-pattern-system-designer ──> design-pattern-selector
                                ──> creational-pattern-selector
                                ──> structural-pattern-selector
                                ──> behavioral-pattern-selector
```

## Install Profiles

**Full** (all 15 skills) — Complete design patterns toolkit. Selection frameworks, OO principles, design smell detection, and 8 pattern implementors with capstone.

**Selector-only** (6 skills) — Pattern selection skills only. For choosing patterns, not implementing them:
- `design-pattern-selector`
- `oo-design-principle-evaluator`
- `oo-design-smell-detector`
- `creational-pattern-selector`
- `structural-pattern-selector`
- `behavioral-pattern-selector`

**Essentials** (10 skills) — Hub + 3 most impactful implementors:
- All 6 selector/foundation skills
- `observer-pattern-implementor`
- `strategy-pattern-implementor`
- `command-pattern-implementor`
- `composite-pattern-implementor`

## Attribution

Skills distilled from **Design Patterns: Elements of Reusable Object-Oriented Software** by Erich Gamma, Richard Helm, Ralph Johnson, and John Vlissides (Addison-Wesley, 1994). The skills encode the book's pattern selection methodology and implementation guidance in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, diagrams, and discussion.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
