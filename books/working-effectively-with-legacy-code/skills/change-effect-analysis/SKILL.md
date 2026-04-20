---
name: change-effect-analysis
description: "Trace the blast radius of a legacy code change and produce a test placement plan with pinch points. Use whenever a developer needs to decide WHERE to write tests for a pending change — 'what should I test?', 'where to test?', 'how far do the effects propagate?', 'what else could this break?', 'how to find test points', 'pinch point', 'effect sketch', 'impact analysis', 'blast radius', 'interception point', 'high-leverage test'. Triggers for 'I need to make many changes', 'many classes affected', 'cluster of related changes', 'cross-class refactoring'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/change-effect-analysis
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [11, 12]
domain: software-engineering
tags: [legacy-code, testing, refactoring, software-engineering, impact-analysis]
depends-on:
  - legacy-code-change-algorithm
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Target method/class to change + the change description + accessible codebase for tracing"
  tools-required: [Read, Grep, Bash]
  tools-optional: [Edit]
  mcps-required: []
  environment: "Codebase (any language). LSP or code navigation tools improve precision but Grep is sufficient."
discovery:
  goal: "Produce a concrete test placement plan identifying pinch points and the minimal test set for a change."
  tasks:
    - "Identify the change point(s)"
    - "Trace effects through 3 propagation mechanisms"
    - "Build an effect sketch"
    - "Identify pinch points"
    - "Produce test placement plan"
  audience:
    roles: [software-engineer, backend-developer, tech-lead]
    experience: intermediate
  when_to_use:
    triggers:
      - "About to change a method or class with unclear downstream impact"
      - "Multiple related classes need changes in one area"
      - "Need to decide which methods to test for a given change"
    prerequisites:
      - skill: legacy-code-change-algorithm
        why: "This skill executes Step 2 (find test points) of the algorithm in depth"
    not_for:
      - "Greenfield code where TDD is applied per method"
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

# Change Effect Analysis

## When to Use

You are about to change a method or class in a legacy codebase and you need to decide where to write tests. Specifically:

- You need to change a method and you're not sure which of its callers could break
- Multiple related classes need coordinated changes and breaking all their dependencies individually would take days
- Someone asks "what could this change affect?" and you need a systematic answer, not a guess
- You are executing Step 2 (Find Test Points) of the `legacy-code-change-algorithm` and need a deeper procedure

This skill does not determine whether the change is safe to make. It determines where to place the tests that will make it safe.

Before executing this skill, confirm:
1. You have at least one specific change point (method or class being changed) identified
2. You have read access to the relevant source files
3. You have a description of the change, even if approximate

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Change point:** Which method(s) or class(es) will change?
  -> Check prompt for: class names, method names, file paths
  -> If still missing, ask: "Which specific method or class needs to change?"

- **Change description:** What is being modified and why?
  -> If still missing, ask: "What should the code do differently after the change?"

- **Language and codebase access:** What language? Can the files be read?
  -> Check environment for: file extensions, project structure
  -> If unknown: proceed — the analysis is language-agnostic, though language-specific firewalls affect where you stop

### Default Assumptions

- **No tests exist yet:** The analysis works regardless of test coverage.
- **OO codebase:** Default to tracing through instance variables, superclasses, subclasses, and callers. Adjust if procedural or functional language detected.
- **Globals exist until proven otherwise:** Always execute the global/static trace (Step 4 below) even if the code looks clean.

### Sufficiency Threshold

SUFFICIENT: Change point named + read access to files + change description available  
PROCEED WITH DEFAULTS: Change point named + rough file area identified  
MUST ASK: No change point at all — this analysis cannot begin without knowing what changes

## Process

### Step 1: Identify Change Points

**ACTION:** Locate the exact method(s) or variable(s) being modified. Record each as a change point entry.

**WHY:** Every downstream effect traces from a specific origin. Vague change points ("we're changing the billing area") produce incomplete effect sketches. Precise change points ("we're modifying `Invoice.calculateShipping()`") let you trace outward systematically.

**HOW:**
1. Read the target file(s). Identify the specific method body that changes.
2. If multiple methods change, list each one separately — they may produce independent effect paths that only converge at a pinch point.
3. Note any instance variables the method reads or writes. These will feed Step 3.

**ARTIFACT:** Start `effect-sketch.md`:
```
## Change Points
- [ClassName.methodName] — what changes: [brief description]
- [ClassName.fieldName] — what changes: [brief description]
```

---

### Step 2: Trace Mechanism 1 — Return Values

**ACTION:** For each change point that is a method, determine if it has a return value. If yes, trace who uses that return value.

**WHY:** Return values are the most visible propagation mechanism. When a method's return value changes, every caller that uses that value is affected — and each of those callers may propagate the effect further through their own return values.

**HOW:**
1. Read the method signature. Does it return a non-void value?
2. If yes: Grep for all callers of this method. Read each caller.
3. For each caller that uses the return value (not just calls and discards it):
   - Does the caller return it or assign it to a field? → recurse: trace that caller's return value chain
   - Does the caller use it in a condition or computation? → that caller's return value (if any) is also affected
4. Draw arrows in `effect-sketch.md`: `changeMethod → callerA → callerB`
5. Stop when you reach a method with no further users, or a system boundary (network, file, UI).

**STOP condition:** If the same method appears twice in your trace chain, you have a cycle. Mark it and do not recurse further.

**ARTIFACT:** Add to `effect-sketch.md`:
```
## Mechanism 1: Return Value Chain
changeMethod() → [callerA(), callerB()] → [callerA: used in callerX()] → ...
```

---

### Step 3: Trace Mechanism 2 — Parameter Mutation

**ACTION:** For each change point method, check whether it modifies state on any object it receives as a parameter.

**WHY:** Parameter mutation is sneaky because it does not appear in the method's return type. A method that accepts a `List`, an `Order`, or any mutable object and modifies its state will cause effects to propagate silently back through the caller. You cannot detect this from the signature alone — you must read the body.

**HOW:**
1. Read the method body. Look for any assignment to fields of a parameter object (e.g., `order.setStatus(...)`, `list.add(...)`, `buf.append(...)`).
2. For each parameter that is mutated: find all callers. For each caller, trace what they do with that parameter object after this method returns.
3. Follow the mutated object forward: does the caller pass it to another method? Return it? Store it in a field?
4. Add each discovered path to `effect-sketch.md`.

**Language note:** In Java and C#, object parameters are passed by reference — the handle can be used to mutate the object. Primitive parameters (`int`, `double`) cannot be mutated. In C++, check whether parameters use `const` — but also check if the type uses `mutable` internally.

**ARTIFACT:** Add to `effect-sketch.md`:
```
## Mechanism 2: Parameter Mutation
changeMethod(order) — mutates order.status → callers that use order after call: [callerA, callerB]
```

---

### Step 4: Trace Mechanism 3 — Global and Static Data

**ACTION:** Check whether any method in your change points reads or writes global variables, static fields, or singleton state.

**WHY:** Global and static data is the sneakiest propagation mechanism. It does not appear in method signatures at all. A change point that writes to a global silently affects every method that reads that global anywhere in the codebase — including methods in completely unrelated classes. Skipping this step is how developers introduce regressions they cannot explain.

**HOW:**
1. Grep the method body for: static field references (`ClassName.fieldName`), singleton calls (`.getInstance()`), global variables, or calls that clearly write to shared state (e.g., `View.getCurrentDisplay().addText(...)`).
2. For each global or static reference found: Grep the entire codebase for that global name. Every location that reads it is a potential effect path.
3. Add all discovered global readers to the effect sketch.
4. If no globals are found: record "No global/static effects detected" — this confirms you looked, not that you skipped it.

**ARTIFACT:** Add to `effect-sketch.md`:
```
## Mechanism 3: Global/Static Data
changeMethod() writes: [GlobalClass.sharedField]
  → readers found: [ClassA.methodX(), ClassB.methodY()]
  — OR —
No global/static effects detected.
```

---

### Step 5: Include Superclasses and Subclasses

**ACTION:** If the change point is on an instance method or field, check whether superclasses or subclasses access the same data.

**WHY:** In OO code, subclasses can override or directly access instance variables from a parent. If a field is `protected` or package-scoped rather than `private`, subclasses (and classes in the same package) may read or write it. Forgetting subclasses leads to incomplete effect sketches that miss real propagation paths.

**HOW:**
1. Check the visibility of every instance variable accessed in the change point method. Private fields are safe — subclasses cannot reach them without a method. Protected, package-scoped, or public fields must be checked.
2. Grep for subclasses of the class containing the change point. Read their methods for uses of the shared fields.
3. Add any discovered subclass usages to the effect sketch.

**ARTIFACT:** Add to `effect-sketch.md`:
```
## Superclass/Subclass Check
[ClassName.field] visibility: [private/protected/public/package]
Subclasses found: [SubA, SubB]
SubA accesses field in: [SubA.someMethod()] → adds to effect path
```

---

### Step 6: Build the Effect Sketch

**ACTION:** Consolidate all paths discovered in Steps 2–5 into a single text diagram. Each node is a method or variable. Each arrow represents "can be affected by."

**WHY:** The effect sketch is not documentation — it is a thinking tool. Seeing all paths in one place reveals convergences (potential pinch points), dead ends (method results that are discarded), and the true scope of the change. Without the sketch, the analysis lives only in your head and is easy to compress incorrectly.

**Format:** Use indented text or ASCII arrows. There is no required notation — clarity of comprehension is the only standard.

**Example sketch for a change to `generateIndex()`:**
```
generateIndex()
  └─ writes: elements (collection)
       ├─ read by: getElementCount() → return value used by callers
       └─ read by: getElement(name) → return value used by callers
addElement()
  └─ writes: elements (collection)
       ├─ (same paths as above)
```

Both `getElementCount()` and `getElement(name)` are interception points — places where a test can detect changes.

**ARTIFACT:** Finalize `effect-sketch.md` with the consolidated diagram.

---

### Step 7: Identify Pinch Points (Multi-Class Changes Only)

**ACTION:** If the effect sketch covers multiple classes, look for a narrowing — a single method or small set of methods through which all (or most) effect paths pass. That narrowing is a pinch point.

**WHY:** When three or four classes need coordinated changes and breaking each class's dependencies individually would take hours, a pinch point gives you test coverage over all of them through a single, already-reachable entry point. Pinch point tests are temporary scaffolding, not the goal — but they let you start changing safely today rather than waiting until all dependencies are broken.

**HOW:**
1. Look at your effect sketch. Count how many change-point effect paths converge on each interception point.
2. An interception point is a pinch point if testing it detects effects from most or all of your change points simultaneously.
3. A pinch point is determined by your specific change points — not by global class structure. The same class may or may not be a pinch point depending on what changes.
4. Reject false pinch points: a method that covers only one of six change paths is an interception point, not a pinch point.

**Pinch Point Trap Warning:** Pinch point tests cover a wide area but they are high-level tests. If left in place permanently, they grow into slow mini-integration tests that test cluster behavior rather than individual class behavior. Mark pinch point tests explicitly in the test file (e.g., `// PINCH POINT — delete when unit tests cover OrderBuilder, OrderValidator, OrderPricer`).

**Exit criterion:** When every class in the cluster has its own unit tests, delete the pinch point test. It has done its job.

**ARTIFACT:** Add to `effect-sketch.md`:
```
## Pinch Point Analysis
Candidate: [ClassName.methodName]
  Effects covered: [changePoint1, changePoint2, changePoint3] ✓
  Effects missed: [changePoint4] — needs separate test
  Verdict: PINCH POINT (covers 3 of 4 change paths)
```

---

### Step 8: Write the Test Placement Plan

**ACTION:** Using the effect sketch and pinch point analysis, produce an ordered plan: which tests to write first, at which methods, in which order.

**WHY:** The test placement plan turns the analysis into action. Without it, the effect sketch is only a map — the plan is the route. The plan answers: "Given what I just traced, exactly which methods should I call in my test harness?"

**HOW:**
1. If a pinch point was found:
   - Write pinch point tests first. These cover the most ground immediately.
   - Mark them as temporary (see Step 7 warning).
   - List the unit tests to write as dependencies are broken.
2. If no pinch point was found (single-class change, or effects don't converge):
   - Identify the narrowest interception points closest to the change — these are the unit tests to write.
   - Prefer interception points close to the change point (fewer logical steps = fewer assumptions about intermediate behavior).
3. For each test in the plan, record: which method to call, which effects it covers, and what assertion will detect a regression.

**ARTIFACT:** Write `test-placement-plan.md`:
```
# Test Placement Plan

## Phase 1: Pinch Point Coverage (immediate)
- Test: [ClassName.methodName]
  Covers change points: [list]
  Assertion: [what fails on regression]
  Status: TEMPORARY — delete when Phase 2 tests are in place

## Phase 2: Unit Tests (as dependencies are broken)
- Test: [ClassName.methodName]
  Covers: [specific change point]
  Dependency to break first: [technique]

## Uncovered Effects
- [anything the plan doesn't cover, and why it's acceptable or not]
```

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Change point(s) | Yes | Specific method(s) or class(es) being changed |
| Change description | Yes | What the code should do differently |
| Source files | Yes | Readable codebase for tracing callers, globals, subclasses |
| Language | Recommended | Affects visibility rules and parameter passing semantics |

## Outputs

| Output | Description |
|--------|-------------|
| `effect-sketch.md` | Text diagram of all effect paths from change points to detectable endpoints |
| `test-placement-plan.md` | Ordered plan: which methods to test, which tests are pinch points, which are unit tests |

## Key Principles

- **Three mechanisms cover all effect paths — don't skip globals.** Return values are the most visible. Parameter mutation is quieter. Globals are invisible from signatures. A thorough analysis executes all three traces, even when the code looks clean. Globals are where the surprises live.

- **Effect sketches are rough drawings, not UML.** The goal is to see which things affect which other things. Formal notation adds no value here — a bulleted indentation tree is sufficient. The point is comprehension for test placement decisions, not documentation for future readers.

- **Pinch points are temporary scaffolding.** A pinch point test is not a goal — it is a bridge. It lets you cover a cluster of classes with one test while you gradually break individual class dependencies. When unit tests cover the cluster, delete the pinch point test. Leaving it in place permanently creates a slow mini-integration test that duplicates work and masks the individual class behavior.

- **A pinch point that doesn't narrow the sketch isn't a pinch point.** A method that sits at the top of the call chain is only a pinch point if testing it actually detects effects from the specific changes you are making. A broad "God method" that touches everything is not a pinch point — it's just a large test surface. Evaluate convergence relative to your change points.

## Examples

### Single-Class Change: Return Value Propagation

**Setup:** `CppClass.getInterface()` needs to add a language-qualifier prefix to all return values. CppClass has three methods: `getInterface()`, `getDeclaration()`, `getDeclarationCount()`.

**Trace:**
- Mechanism 1 (return values): `getInterface()` returns a `String`. Grep callers. → One caller: `Parser.generateOutput()`, which formats the interface into a file. `generateOutput()` returns a `String` used by `FileWriter.write()`.
- Mechanism 2 (parameter mutation): `getInterface()` does not mutate any parameter.
- Mechanism 3 (globals): No global reads or writes in `getInterface()`.
- Subclasses: `declarations` field is private. No subclass access.

**Effect sketch:**
```
getInterface() → return String
  → Parser.generateOutput() → return String
       → FileWriter.write() → side effect (file output)
```

**Test placement plan:**
- Write tests on `getInterface()` directly (closest to change point, directly callable).
- One test verifying the prefix appears in the returned string.
- No pinch point needed — single class, single propagation chain.

---

### Multi-Class Change: Convergence to a Pinch Point

**Setup:** Three classes — `OrderBuilder`, `OrderValidator`, `OrderPricer` — all need changes for a new discount feature. Each takes 2 hours to break dependencies individually. All three are consumed by `BillingStatement.makeStatement()`, which produces the final billing output.

**Trace:**
- `OrderBuilder.build()` writes a discount field → `OrderValidator.validate()` reads it → `OrderPricer.price()` computes discounted total → both feed into `BillingStatement.makeStatement()`.
- Effect sketch shows all three change paths converge on `makeStatement()`.

**Pinch point:** `BillingStatement.makeStatement()` — one test covers all three change paths.

**Test placement plan:**
- Phase 1: Write integration-style test on `makeStatement()` with a known Invoice. Mark as TEMPORARY.
- Phase 2: As each class gets unit tests (break `OrderBuilder` dependency first, then `OrderValidator`, then `OrderPricer`), add narrower unit tests per class.
- When all three classes have unit tests: delete the `makeStatement()` pinch point test.

---

### Global Reference Change: Finding All Readers

**Setup:** `Element.addText()` is being changed to log to a different display system. The current implementation contains `View.getCurrentDisplay().addText(newText)` — a global reference. The new change will swap `getCurrentDisplay()` for `Logger.getStream()`.

**Trace:**
- Mechanism 3 (globals): Grep the entire codebase for `View.getCurrentDisplay`. Found in 4 additional places: `HeaderRenderer`, `FooterRenderer`, `SummaryBuilder`, `AuditLogger`.
- Each of these reads the display global. Changing the display target in `addText()` does not directly break them — but confirms the global is shared across unrelated classes.

**Effect sketch:**
```
Element.addText() → writes: View.getCurrentDisplay()
  → readers of same global: [HeaderRenderer, FooterRenderer, SummaryBuilder, AuditLogger]
  → these are NOT affected by the addText change (they call getCurrentDisplay() independently)
  → confirmed: no transitive effect through the global
```

**Test placement plan:**
- Write tests on `Element.addText()` directly. Verify logging target changes.
- No pinch point needed — the global is read independently by others, not fed through a common parent.
- Note: if `View.getCurrentDisplay()` itself is being changed, re-run this analysis with `getCurrentDisplay()` as the new change point.

## References

The full 6-step effect-analysis heuristic from Chapter 11 is reproduced verbatim in the process steps above. No supplementary reference file is required — the heuristic is self-contained within this skill.

For the broader algorithm that calls this skill as Step 2, see `legacy-code-change-algorithm`.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Working Effectively with Legacy Code by Michael C. Feathers (2004, Prentice Hall).

## Related BookForge Skills

- `legacy-code-change-algorithm` — This skill is Step 2 (Find Test Points) of the 5-step algorithm. Always execute the parent algorithm first to classify the change and identify change points.
- `characterization-test-writing` — Downstream: once the test placement plan is written, use this skill to write the actual characterization tests at the interception points identified here.
- `big-class-responsibility-extraction` — Cross-reference: when effect sketch analysis reveals that a large class has many unrelated effect paths, it is a signal that the class has too many responsibilities. Effect sketches can reveal hidden class boundaries — clusters of methods that only affect each other form natural candidates for extraction.
- `seam-type-selector` — When a test placement plan identifies a dependency that blocks test harness construction, use the seam selector to choose the right seam type for that dependency.

Install the full book skill set from GitHub: [bookforge-skills — working-effectively-with-legacy-code](https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code)
