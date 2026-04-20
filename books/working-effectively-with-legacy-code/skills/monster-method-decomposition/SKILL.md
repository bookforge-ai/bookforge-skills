---
name: monster-method-decomposition
description: "Decompose a very large method (100+ lines, deeply nested) safely using automated refactoring and Feathers' Bulleted/Snarled classification. Use whenever a developer faces 'a huge method', 'I have a 500-line function', 'deeply nested conditionals', 'monster method', 'god method', 'need to break up this giant method', 'can't test this method it's too big', 'where do I even start with this method'. Activates for 'method extraction', 'IDE refactoring', 'automated extract method', 'introduce sensing variable', 'find sequences', 'skeletonize', 'coupling count', 'bulleted method', 'snarled method', 'break out method object'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/monster-method-decomposition
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [22]
domain: software-engineering
tags: [legacy-code, refactoring, testing, software-engineering, code-quality]
depends-on:
  - safe-legacy-editing-discipline
  - dependency-breaking-technique-executor
execution:
  tier: 1
  mode: full
  inputs:
    - type: codebase
      description: "Monster method source + language + IDE/refactoring tool availability"
  tools-required: [Read, Edit, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Codebase. Automated refactoring support (IDE or language server) strongly recommended."
discovery:
  goal: "Decompose a monster method into testable pieces using the right strategy for its structure."
  tasks:
    - "Classify the method as Bulleted or Snarled (or hybrid)"
    - "Choose strategy: Find Sequences or Skeletonize"
    - "Extract small low-coupling pieces first"
    - "Introduce sensing variables if needed for partial testing"
    - "Escalate to Break Out Method Object if in-place decomposition is infeasible"
  audience:
    roles: [software-engineer, backend-developer]
    experience: intermediate
  when_to_use:
    triggers:
      - "A method exceeds ~100 lines or has deep nesting"
      - "Developer feels unable to safely change a method"
      - "Testing the method requires too much setup"
    prerequisites:
      - skill: safe-legacy-editing-discipline
        why: "Preserve Signatures and Single-Goal Editing are non-negotiable during decomposition"
    not_for:
      - "Methods that are already small but have testability issues — use test-harness-entry-diagnostics"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 12
    iterations_needed: null
---

# Monster Method Decomposition

## When to Use

A monster method is one so long and so complex that you genuinely do not feel comfortable touching it. It may be hundreds or thousands of lines with scattered indentation that makes navigation nearly impossible. You are tempted to print it out and lay it across the hallway to understand it.

Use this skill when any of the following are true:

- A method exceeds roughly 100 lines, or is deeply nested with multiple levels of conditionals and loops
- You cannot write a test for it without massive setup that mirrors the entire calling context
- Every time you touch it something unrelated breaks
- A developer has declared "I'll just add it here" because breaking the method feels too risky

**Anti-pattern warning:** Reading the method top-to-bottom attempting to comprehend it in full before doing anything is the primary failure mode. Monster methods overwhelm working memory. The structural attack — classify, pick strategy, extract small pieces — is always the right starting point.

**Relationship to prerequisites:** `safe-legacy-editing-discipline` applies throughout (Single-Goal Editing, Preserve Signatures). `dependency-breaking-technique-executor` handles escalation to Break Out Method Object when in-place decomposition stalls.

## Context and Input Gathering

Before starting, collect:

1. **Method source** — the full text of the target method, including its signature
2. **Language** — determines which refactoring tools are available and whether the compiler can assist
3. **Automated refactoring tool** — does the IDE (IntelliJ, Eclipse, VS Code with plugin, ReSharper, etc.) support automated Extract Method? Answer: yes/no/partial
4. **Existing tests** — are any tests currently exercising this method at all? Answer: yes/no/some
5. **Target change** — what is the actual change you need to make? This determines which section of the method to prioritize
6. **Class context** — is the monster method on a class that can be instantiated in a test harness?

## Process

### Step 1: Classify — Bulleted, Snarled, or Hybrid

Read the method structurally, not semantically. Do not try to understand what it does — only observe its shape.

**Bulleted Method** — nearly no dominant indentation. The method reads like a bulleted list of actions. When you squint, you see flat horizontal blocks. Sections may be separated by blank lines or comments. The hidden challenge: sections look separable but often share temporary variables declared in one chunk and used in the next.

**Snarled Method** — dominated by a single large, deeply indented section. The method contains one or more long conditional or loop structures that nest most of the code. Try to align the blocks visually — if you feel vertigo, you have a snarl. Logic buried deep in nesting is nearly impossible to test in isolation.

**Hybrid (most real methods)** — a snarled outer shell with bulleted sections hidden deep inside the nesting, or a bulleted surface with snarled interior chunks. Treat as snarled-first when the dominant indentation level is deep; bulleted-first when the top level reads flat.

Document the classification: `BULLETED | SNARLED | HYBRID (dominant: X)`.

### Step 2: Choose Extraction Strategy

The classification from Step 1 determines the primary strategy. You will likely use both strategies at different points — this is expected. Feathers himself notes going back and forth.

**Find Sequences (for Bulleted methods)**

Extract the condition and body *together* into a single named method. Goal: reveal the overarching sequence of operations that was hidden inside the method's bulk. After extraction, the monster method should read like a sequence of named operations.

```
// Before (extract condition + body together):
if (marginalRate() > 2 && order.hasLimit()) {
    order.readjust(rateCalculator.rateForToday());
    order.recalculate();
}

// After Find Sequences:
recalculateOrder(order, rateCalculator);  // condition + body inside the new method
```

Use Find Sequences when you sense that there is an overarching sequence of steps that will become legible once the chunks are named.

**Skeletonize (for Snarled methods)**

Extract the condition and body *separately* into two different methods. Goal: leave a skeleton of control structure in the original method — the if/for/while bones — with named delegations inside each branch. This makes the control structure visible and refactorable without understanding every branch's logic.

```
// Before (deep nesting):
if (marginalRate() > 2 && order.hasLimit()) {
    order.readjust(rateCalculator.rateForToday());
    order.recalculate();
}

// After Skeletonize (condition and body separated):
if (orderNeedsRecalculation(order)) {
    recalculateOrder(order, rateCalculator);
}
```

Use Skeletonize when the control structure itself needs to be refactored — when the nesting pattern is the primary problem, not just the size of each branch.

### Step 3: Compute Coupling Count on Candidate Extractions

Before extracting any piece, count its coupling:

```
coupling count = number of parameters that would pass in
                 + 1 if there is a return value
                 (instance variable accesses do NOT count — they stay on the object)
```

Example: a method taking `(int a, int b)` and returning an `int` has coupling count 3.

**Prioritize extractions with the lowest coupling count first.** Coupling count 0 (no parameters, no return) is the safest — you are issuing a command to the object to modify its own state. These extractions are nearly impossible to get wrong.

Coupling count 0 extractions are especially valuable as a first pass on any monster method regardless of type — they progressively clarify the method's structure without introducing parameter/return type errors.

When coupling count is greater than 0, consider introducing a sensing variable (Step 5) before extracting.

### Step 4: Execute Extractions — Automated Tool Only

This is the most critical constraint in the entire process:

**If automated refactoring support is available, use the tool exclusively. Do not mix automated extractions with manual edits. Do not reorder statements. Do not split expressions. Do not rename during extraction.**

Why: automated Extract Method performs variable flow analysis that would be error-prone by hand. Mixing manual edits with automated ones eliminates the safety guarantee — you no longer know which changes are tool-verified and which are hand-written. The price of this constraint is that extracted method names will sometimes be awkward. Accept this — names are moved later.

Extraction sequence:
1. Extract 0-coupling-count pieces first — commands with no parameters and no return
2. Extract the next-lowest coupling count candidates
3. After a batch of automated extractions, run the tests (if any exist) to verify behavior
4. Do not attempt to move extracted methods to a better class during this phase — extract to the current class first, always, using whatever name fits. Moving comes after tests exist

**If no automated refactoring tool is available**, proceed more conservatively:
- Only extract pieces where you can verify every variable's declaration and usage by hand
- Use sensing variables (Step 5) to create test checkpoints before extracting
- Prefer coupling count 0 extractions almost exclusively until tests exist

### Step 5: Introduce Sensing Variables Where Needed

When you need to write a test for a piece of logic that is currently inside the monster method — and that logic does not yet have a way to be observed externally — introduce a sensing variable:

1. Add a public or package-visible instance variable (e.g., `public boolean nodeAdded = false;`) to the class
2. Inside the monster method, set this variable at the point you want to sense (e.g., after the condition you are about to extract)
3. Write a test that invokes the method and asserts against the sensing variable
4. Extract the piece you just covered — the test now verifies the extraction did not break behavior
5. After the refactoring session, remove the sensing variable and either delete the test or refactor it to test the extracted method directly

Keep sensing variables in place across the entire refactoring session, deleting them only at the end. This lets you undo extractions easily if a better decomposition direction emerges.

Sensing variables are especially valuable for snarled methods — they allow you to add test coverage deep inside nested logic before you can reach it via the public interface.

### Step 6: Write Tests for Extracted Methods

After each batch of extractions, write characterization tests for the methods you extracted. These tests document actual current behavior. Use `characterization-test-writing` if this is your first time writing characterization tests.

At minimum for each extracted method:
- One test for the primary path (condition true / non-empty input)
- One test for the edge path (condition false / empty input / boundary value)

These tests become the safety net for the next round of extractions.

### Step 7: Escalate to Break Out Method Object if In-Place Decomposition Stalls

If, after applying Steps 1–6, the method is still too monstrous to decompose in place — particularly if it has dozens of local variables that would all become parameters, or if the logic is so entangled that no low-coupling extraction exists — escalate.

Invoke `dependency-breaking-technique-executor` with the Break Out Method Object technique:
- The monster method's parameters become constructor parameters on a new class
- The monster method's body moves to a `run()` or `execute()` method on the new class
- All local variables become instance variables on the new class, where they can be sensed directly in tests

Break Out Method Object is more drastic than in-place decomposition but is often the right call when local variables are so numerous that sensing variables become impractical, or when the method's logic genuinely belongs to a concept that deserves its own type.

## Inputs

| Input | Required | Notes |
|-------|----------|-------|
| Monster method source | Yes | Full text including signature |
| Language | Yes | Determines tool availability |
| Automated refactoring tool | Yes | Yes/no/partial |
| Existing tests | Yes | Drives sensing variable decision |
| Target change | Yes | Guides which section to prioritize |
| Class instantiability in test harness | No | Needed if writing new tests for extracted methods |

## Outputs

| Output | Description |
|--------|-------------|
| `decomposition-plan.md` | Classification, strategy choice, ordered extraction list with coupling counts |
| Extracted methods | Named private methods in the current class |
| Sensing variable tests | Temporary test file for coverage during extraction |
| Characterization tests | Persistent tests for extracted methods |
| Updated monster method | The original method, now a skeleton of delegating calls |

## Key Principles

**Classify first — strategy depends on type.** Bulleted method → Find Sequences (condition + body together, reveal overarching sequence). Snarled method → Skeletonize (condition and body separately, leave control structure visible). Hybrid → lead with the dominant type.

**Use the IDE exclusively.** Never mix automated extraction with manual edits in the same session. No reordering. No expression splitting. No inline renames. The tool's safety guarantee is invalidated the moment you interleave manual edits.

**Coupling count ordering (low → high) reduces risk.** Extract 0-count methods first. They carry no parameter/return-type risk. Even one round of 0-count extractions gives you insight into the method's structure that top-to-bottom reading never could.

**Extract to the current class first with awkward names.** The name `recalculateOrder` is awkward when the logic belongs on `Order` — but it is correct enough to move forward safely. Move the method to its better home only after tests exist.

**Top-to-bottom reading is the anti-pattern.** The structural attack (classify → strategy → extract by coupling count) always proceeds faster and more safely than attempting full comprehension before touching anything.

**Be prepared to redo.** The first round of extractions produces insight that often reveals a better decomposition. Redoing is not wasted — it is the design process working correctly.

## Examples

### Example A: Bulleted 300-line Dispatcher (Find Sequences)

`processRequest()` is 300 lines with 12 flat sections separated by blank lines. Each section handles a different request type. Visual inspection: nearly no dominant indentation, flat shape — this is a Bulleted method.

Strategy: Find Sequences.

1. Identify the 12 sections
2. Compute coupling count for each — most sections use only local variables already in scope (coupling count 0 or 1)
3. Extract each section as a single named method (condition + body together for any sections with a guard clause)
4. After extraction: `processRequest()` reads as a sequence: `validateRequest()`, `parseHeaders()`, `routeToHandler()`, `formatResponse()`, etc.
5. Write characterization tests for each extracted method

The resulting method reveals the overarching sequence that was buried in bulk.

### Example B: Snarled 150-line Nested Conditional (Skeletonize)

`updateCommodities()` is 150 lines. The outer body is a single `if` over a `for` loop with nested conditions 5 levels deep. Visual inspection: deep nesting dominates — this is a Snarled method.

Strategy: Skeletonize.

1. Start at the outermost conditional — extract the condition alone: `commoditiesAreReadyForUpdate()`
2. Extract the body of the outer `if` alone: `runCommodityUpdate()`
3. Now the top level reads: `if (commoditiesAreReadyForUpdate()) { runCommodityUpdate(); }`
4. Move into `runCommodityUpdate()` — apply the same skeletonize pass to its inner loops
5. Introduce sensing variables before extracting deep inner logic where no observable side effects exist
6. After each pass, write tests for the most recently extracted methods

The resulting method is a skeleton of control structure — the nesting pattern is now visible and refactorable.

### Example C: Method Too Monstrous for In-Place Decomposition (Break Out Method Object)

`generateReport()` is 600 lines with 40 local variables. Every candidate extraction has coupling count 5+ because the logic is a deeply interconnected computation. No 0-count methods can be found. In-place decomposition would produce methods with enormous parameter lists that are harder to read than the original.

Decision: escalate to Break Out Method Object.

Invoke `dependency-breaking-technique-executor` with:
- Technique: Break Out Method Object
- Monster method: `generateReport()`
- Parameters: the method's current parameter list becomes the new class's constructor
- Local variables: become instance variables on `ReportGenerator`
- Method body: moves to `ReportGenerator.run()`

Now each local variable is an instance variable — sensing variables are no longer needed because the state is directly observable. Decompose `ReportGenerator.run()` using the same Bulleted/Snarled classification on what is now a class with proper state.

## References

For deeper guidance on techniques referenced here:

- **Characterization Tests** → `characterization-test-writing` skill; also Working Effectively with Legacy Code Ch 13
- **Break Out Method Object** — Working Effectively with Legacy Code Ch 25 (Appendix, p. 330)
- **Targeted Testing during extraction** — Working Effectively with Legacy Code Ch 13, "Targeted Testing" section
- **Gleaning Dependencies** — Ch 22, for preserving critical behavior while editing less-critical sections without full test coverage
- **Subclass and Override Method** — Chapter 25 technique; enables sensing through extracted display/output methods

## License

Content derived from *Working Effectively with Legacy Code* (Michael C. Feathers, 2004). Skill text licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

## Related BookForge Skills

| Skill | Relationship |
|-------|-------------|
| `safe-legacy-editing-discipline` | **Prerequisite.** Preserve Signatures and Single-Goal Editing apply at every extraction step |
| `dependency-breaking-technique-executor` | **Prerequisite.** Break Out Method Object escalation path for in-place-infeasible cases |
| `characterization-test-writing` | Produces the tests written after each extraction batch |
| `test-harness-entry-diagnostics` | Diagnoses why the class cannot be instantiated in a test harness before starting decomposition |
| `scratch-refactoring-for-code-understanding` | Alternative when the goal is comprehension, not safe production change |
