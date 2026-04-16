# Refactoring Skills (Martin Fowler)

You have access to 10 refactoring skills. Use them when working with existing code.

## Skills

1. **code-smell-diagnosis** — Scan code for the 22 named code smells from Fowler's catalog and produce a prioritized diagnosis report with specific refactoring prescriptions for each smell.
2. **refactoring-readiness-assessment** — Assess whether a codebase warrants refactoring, no refactoring, or rewrite before any structural changes begin.
3. **build-refactoring-test-suite** — Build a sufficient automated test suite before refactoring using a 6-step sequential construction workflow.
4. **profiling-driven-performance-optimization** — Optimize performance by refactoring first, then profiling to find actual hot spots, applying targeted optimizations only where the profiler points.
5. **method-decomposition-refactoring** — Decompose long methods into clean, composable units using the 9 composing-method refactorings from Fowler's catalog.
6. **type-code-refactoring-selector** — Select the correct refactoring for type codes using Fowler's three-way decision tree (Class, Subclasses, or State/Strategy).
7. **conditional-simplification-strategy** — Select and apply the correct refactoring for complex conditional logic — 8 techniques from Chapter 9 plus Introduce Assertion.
8. **class-responsibility-realignment** — Redistribute methods and fields to correct classes, repair inheritance hierarchies, and extend unmodifiable library classes.
9. **data-organization-refactoring** — Apply correct data organization refactoring for Primitive Obsession, Data Clumps, Data Class, magic numbers, and raw collections.
10. **big-refactoring-planner** — Plan architectural-scale refactoring campaigns (Tease Apart Inheritance, Convert Procedural to Objects, Separate Domain from Presentation, Extract Hierarchy).

## Workflow

Start with `code-smell-diagnosis` to identify problems, then use the specific refactoring skill for the diagnosed smell. For new refactoring efforts, run `refactoring-readiness-assessment` first.

Skill files are in `skills/*/SKILL.md`.
