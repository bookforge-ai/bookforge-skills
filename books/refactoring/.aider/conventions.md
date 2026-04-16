# Refactoring Skills — Aider Conventions

This plugin provides 10 refactoring skills from Refactoring: Improving the Design of Existing Code by Martin Fowler.

## Hub Skill

**code-smell-diagnosis** — Scan code for the 22 named code smells and produce a prioritized diagnosis with refactoring prescriptions. This is the entry point for all refactoring work.

## All Skills

1. **code-smell-diagnosis** — Scan a codebase for the 22 named code smells from Fowler's catalog and produce a prioritized diagnosis report with specific refactoring prescriptions.
2. **refactoring-readiness-assessment** — Assess whether a codebase warrants refactoring, no refactoring, or rewrite before any structural changes begin.
3. **build-refactoring-test-suite** — Build a sufficient automated test suite before refactoring using a 6-step sequential construction workflow.
4. **profiling-driven-performance-optimization** — Optimize performance by refactoring first, then profiling to find actual hot spots.
5. **method-decomposition-refactoring** — Decompose long methods into clean, composable units using 9 composing-method refactorings.
6. **type-code-refactoring-selector** — Select the correct refactoring for type codes using Fowler's three-way decision tree.
7. **conditional-simplification-strategy** — Select and apply the correct refactoring for complex conditional logic.
8. **class-responsibility-realignment** — Redistribute methods and fields to correct classes, repair inheritance hierarchies.
9. **data-organization-refactoring** — Apply correct data organization refactoring for Primitive Obsession, Data Clumps, magic numbers.
10. **big-refactoring-planner** — Plan architectural-scale refactoring campaigns with multi-week plans.

## Install

Add to your `.aider.conf.yml`:

```yaml
read: [skills/code-smell-diagnosis/SKILL.md]
```

See https://aider.chat/docs/usage/conventions.html for details.
