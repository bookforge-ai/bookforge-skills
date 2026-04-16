# Refactoring: Improving the Design of Existing Code — Agent Skills

10 agent skills for systematic code refactoring, extracted from **Refactoring: Improving the Design of Existing Code** by Martin Fowler (with Kent Beck).

These skills teach AI agents how to apply Fowler's refactoring catalog — diagnosing the 22 named code smells, decomposing long methods, simplifying tangled conditionals, realigning class responsibilities, organizing data structures, handling type codes, building protective test suites, optimizing performance through profiling, and planning architectural-scale refactoring campaigns. The hub skill (code-smell-diagnosis) feeds all six Level 1 refactoring skills in a star topology.

**Average quality delta: +45.0 points** (85.0% with-skill vs 40.0% baseline, estimated).

## Install

```
claude plugin add bookforge-ai/bookforge-skills/books/refactoring
```

## Skills

| Skill | Description | Tier | Mode | Delta |
|-------|-------------|------|------|------:|
| code-smell-diagnosis | Scan code for the 22 named code smells and produce a prioritized diagnosis with refactoring prescriptions | 2 | hybrid | +48 |
| refactoring-readiness-assessment | Assess whether a codebase warrants refactoring, no refactoring, or rewrite before any changes begin | 1 | plan-only | +44 |
| build-refactoring-test-suite | Build a sufficient automated test suite before refactoring using a 6-step construction workflow | 2 | hybrid | +45 |
| profiling-driven-performance-optimization | Optimize performance by refactoring first, then profiling to find actual hot spots | 3 | hybrid | +38 |
| method-decomposition-refactoring | Decompose long methods into clean, composable units using 9 composing-method refactorings | 2 | full | +48 |
| type-code-refactoring-selector | Select the correct refactoring for type codes using Fowler's three-way decision tree | 2 | hybrid | +46 |
| conditional-simplification-strategy | Select and apply the correct refactoring for complex conditional logic — 8 techniques plus assertions | 2 | hybrid | +46 |
| class-responsibility-realignment | Redistribute methods and fields to correct classes, repair inheritance hierarchies, extend library classes | 2 | hybrid | +48 |
| data-organization-refactoring | Apply correct data organization refactoring for Primitive Obsession, Data Clumps, magic numbers, raw collections | 2 | hybrid | +45 |
| big-refactoring-planner | Plan architectural-scale refactoring campaigns with multi-week plans and interleaved feature milestones | 2 | hybrid | +42 |

## Dependency Graph

```
Level 0 (independent):
  code-smell-diagnosis           [HUB — 6 dependents]
  refactoring-readiness-assessment
  build-refactoring-test-suite
  profiling-driven-performance-optimization

Level 1 (depends on Level 0):
  method-decomposition-refactoring      ──> code-smell-diagnosis
  type-code-refactoring-selector        ──> code-smell-diagnosis
  conditional-simplification-strategy   ──> code-smell-diagnosis
  class-responsibility-realignment      ──> code-smell-diagnosis
  data-organization-refactoring         ──> code-smell-diagnosis
  big-refactoring-planner               ──> code-smell-diagnosis
```

## Install Profiles

**Full** (all 10 skills) — Complete refactoring system covering diagnosis, planning, testing, decomposition, and architectural restructuring.

**Core** (6 skills) — Hub skill plus all Level 1 decision skills for the most common refactoring scenarios:
- `code-smell-diagnosis`
- `method-decomposition-refactoring`
- `type-code-refactoring-selector`
- `conditional-simplification-strategy`
- `class-responsibility-realignment`
- `big-refactoring-planner`

**Minimal** (3 skills) — Foundation skills for assessment and safety:
- `code-smell-diagnosis`
- `refactoring-readiness-assessment`
- `build-refactoring-test-suite`

## Usage

Ask your AI agent anything about refactoring:
- "Scan this class for code smells and tell me what to fix first"
- "Should I refactor this module or is it a rewrite candidate?"
- "Build a test suite for this class before I start refactoring"
- "Break this 200-line method into smaller functions"
- "This switch statement keeps growing — what's the right refactoring?"
- "Plan a multi-week campaign to separate domain logic from our GUI layer"

## Attribution

Skills extracted from **Refactoring: Improving the Design of Existing Code** by Martin Fowler (1999, ISBN 978-0-201-48567-7). The skills encode the book's methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, examples, and narrative.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
