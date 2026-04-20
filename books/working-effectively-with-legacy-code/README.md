# Working Effectively with Legacy Code — Agent Skills

16 agent skills for safely changing untested legacy code, extracted from **Working Effectively with Legacy Code** by Michael C. Feathers (2004).

These skills teach AI agents how to apply Feathers' complete methodology — diagnosing legacy situations via the 19 symptom-routing chapters (Part II), selecting the right seam type, writing characterization tests that pin current behavior, executing the 24 named dependency-breaking techniques (Part III), decomposing monster methods, extracting big-class responsibilities, adding new features with Sprout/Wrap techniques, and applying the master Legacy Code Change Algorithm throughout. The hub skill (`legacy-code-change-algorithm`) anchors the star topology.

**Average quality delta: +73.1 points** (85.6% with-skill vs 12.4% baseline).

## Install

```
claude plugin add bookforge-ai/bookforge-skills/books/working-effectively-with-legacy-code
```

## Skills

| Skill | Description | Tier | Mode | Delta |
|-------|-------------|------|------|------:|
| legacy-code-change-algorithm | Guide safe modification of legacy code using Feathers' 5-step Legacy Code Change Algorithm | 1 | hybrid | +86 |
| seam-type-selector | Select the right seam type (Preprocessor / Link / Object) for breaking a dependency | 1 | hybrid | +40 |
| unit-test-quality-checker | Evaluate a test suite against rigorous unit-test criteria and choose between fake and mock objects | 2 | hybrid | +64 |
| scratch-refactoring-for-code-understanding | Guide throwaway refactoring to understand legacy code — then discard all changes | 1 | full | +100 |
| safe-legacy-editing-discipline | Apply 4 editing disciplines: Hyperaware Editing, Single-Goal Editing, Preserve Signatures, Lean on the Compiler | 1 | hybrid | +54 |
| legacy-code-symptom-router | Diagnose any legacy-code situation and route to the right technique from 19 symptom chapters | 2 | hybrid | +36 |
| test-harness-entry-diagnostics | Diagnose exactly why a class or method cannot be placed under test | 2 | hybrid | +50 |
| change-effect-analysis | Trace the blast radius of a legacy code change and produce a test placement plan with pinch points | 2 | hybrid | +71 |
| characterization-test-writing | Write tests that pin down actual current behavior of untested legacy code | 2 | full | +72 |
| library-seam-wrapper | Isolate third-party library dependencies behind thin wrapper interfaces | 1 | full | +100 |
| legacy-code-addition-techniques | Add new functionality using Sprout Method, Sprout Class, Wrap Method, or Wrap Class | 1 | full | +67 |
| tdd-and-programming-by-difference | Add features to tested code using TDD or Programming by Difference | 1 | full | +100 |
| dependency-breaking-technique-executor | Select and execute the right dependency-breaking technique from Feathers' catalog of 24 | 1 | full | +63 |
| monster-method-decomposition | Decompose a very large method safely using Bulleted/Snarled classification | 1 | full | +100 |
| big-class-responsibility-extraction | Identify and extract responsibilities from an oversized class using 7 heuristics + feature sketches | 2 | hybrid | +67 |
| duplication-removal-via-extraction | Remove duplicated code by extracting small utilities first and letting structure emerge | 1 | full | +100 |

## Dependency Graph

```
Level 0 (independent):
  legacy-code-change-algorithm         [HUB — feeds characterization-test-writing, legacy-code-addition-techniques]
  seam-type-selector                   [feeds library-seam-wrapper, dependency-breaking-technique-executor]
  unit-test-quality-checker
  scratch-refactoring-for-code-understanding
  safe-legacy-editing-discipline
  legacy-code-symptom-router
  test-harness-entry-diagnostics       [feeds dependency-breaking-technique-executor]
  change-effect-analysis

Level 1 (depends on Level 0):
  characterization-test-writing        ──> legacy-code-change-algorithm
  library-seam-wrapper                 ──> seam-type-selector
  legacy-code-addition-techniques      ──> legacy-code-change-algorithm
  tdd-and-programming-by-difference    ──> characterization-test-writing
  dependency-breaking-technique-executor ──> seam-type-selector, test-harness-entry-diagnostics
  monster-method-decomposition         ──> characterization-test-writing
  big-class-responsibility-extraction  ──> characterization-test-writing
  duplication-removal-via-extraction   ──> characterization-test-writing
```

## Install Profiles

**Full** (all 16 skills) — Complete legacy code skill set covering diagnosis, algorithm, seam selection, characterization testing, dependency breaking, method decomposition, and class restructuring.

**Core** (7 skills) — Foundation plus key technique execution and structural refactoring skills:
- `legacy-code-change-algorithm`
- `seam-type-selector`
- `characterization-test-writing`
- `dependency-breaking-technique-executor`
- `legacy-code-symptom-router`
- `monster-method-decomposition`
- `big-class-responsibility-extraction`

**Minimal** (3 skills) — The three foundational skills:
- `legacy-code-change-algorithm`
- `seam-type-selector`
- `characterization-test-writing`

## Usage

Ask your AI agent anything about legacy code:
- "I need to change this code but there are no tests — how do I do it safely?"
- "I can't instantiate this class in a test harness — what do I do?"
- "This method is 500 lines long and I need to add a feature"
- "There's a singleton / global / database connection I can't avoid — how do I fake it?"
- "I inherited a god class with 80 methods — where do I start?"
- "I need to add a feature to untested code under time pressure"
- "How do I write tests for code I didn't write and don't fully understand?"
- "The same bug keeps appearing in 5 different files — how do I fix the duplication?"

## Attribution

Skills extracted from **Working Effectively with Legacy Code** by Michael C. Feathers (2004, ISBN 978-0-13-117705-5). The skills encode the book's methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, code examples, and narrative.

## License

[CC-BY-SA-4.0](LICENSE) — BookForge Skills. You are free to use and adapt these skills with attribution.
