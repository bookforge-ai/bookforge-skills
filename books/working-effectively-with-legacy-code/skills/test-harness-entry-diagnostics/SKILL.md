---
name: test-harness-entry-diagnostics
description: "Diagnose exactly why a class or method cannot be placed under test and route to the right dependency-breaking technique. Use whenever a developer says 'I can't instantiate this class in tests', 'the test harness won't compile', 'this class has too many constructor dependencies', 'the constructor connects to the database', 'can't test this private method', 'I need to sense what this method does', 'hidden singleton dependency'. Activates for 'test harness', 'class under test', 'constructor dependencies', 'irritating parameter', 'hidden dependency', 'construction blob', 'pass null', 'construction test', 'method not accessible', 'method side effects', 'can't get this class in a test harness', 'can't run this method in a test harness', 'singleton in constructor', 'include dependencies', 'onion parameter', 'aliased parameter'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/test-harness-entry-diagnostics
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [9, 10]
domain: software-engineering
tags: [legacy-code, testing, refactoring, software-engineering, dependency-injection]
depends-on:
  - legacy-code-change-algorithm
  - seam-type-selector
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Class file + constructor/method signature + test harness error message or observed obstacle"
  tools-required: [Read, Grep, Bash]
  tools-optional: [Edit]
  mcps-required: []
  environment: "Codebase with a test framework (any xUnit family). Access to the class under investigation."
discovery:
  goal: "Pinpoint the exact reason a class or method resists testing and produce a technique recommendation with ordered sequence."
  tasks:
    - "Run a construction test to surface constructor obstacles"
    - "Classify the obstacle via 4 root causes and 7 class-level cases"
    - "If method-level, classify via 4 Chapter 10 obstacles"
    - "Route to the correct dependency-breaking technique with rationale"
    - "Produce a diagnostic artifact for handoff to technique execution"
  audience:
    roles: [software-engineer, backend-developer, qa-engineer]
    experience: intermediate
  when_to_use:
    triggers:
      - "Class won't instantiate in a test"
      - "Method can't be invoked in a test"
      - "Developer doesn't know which dependency-breaking technique to apply"
      - "Test harness won't compile when the class is added"
    prerequisites:
      - skill: legacy-code-change-algorithm
        why: "This diagnostic executes Step 3 (break dependencies) of the change algorithm — run this skill when you reach that step"
    not_for:
      - "Class IS testable but tests are slow — use unit-test-quality-checker instead"
      - "Designing new code — applies only to existing, hard-to-test code"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 14
    iterations_needed: null
---

# Test Harness Entry Diagnostics

A systematic diagnostic for determining exactly why a class or method cannot be placed under test, and routing each specific obstacle to the correct dependency-breaking technique. Based on Feathers' Chapter 9 (class-level) and Chapter 10 (method-level) obstacle catalogs.

## When to Use

Use this skill when Step 3 of the Legacy Code Change Algorithm ("Break Dependencies") is blocked — when a developer cannot write a test because the class won't instantiate or the method can't be invoked. The diagnostic applies whether the problem surfaces as a compile error, a runtime exception, a dangerously slow test, or an inability to sense what the code actually did.

Do not use this skill when the class is already testable but the tests are too slow or fragile — that is a test quality problem, not a dependency-breaking problem.

## Context and Input Gathering

Before running the diagnostic, collect:

1. **Class name and language** — the class you are trying to place under test
2. **Constructor signature** — parameter types, their constructors if visible
3. **The error or obstacle** — compile error, runtime exception, side-effect description, or accessibility barrier
4. **Test framework in use** — JUnit, NUnit, Google Test, etc.
5. **What you want to test** — a specific method, a behavior, a value returned

If you have not yet attempted to instantiate the class in a test, do that first (Step 1 below). The compiler or runtime error message IS the diagnostic signal.

## Process

### Step 1: Write a Construction Test

Before any analysis, write the simplest possible test: one that just calls the constructor with no assertions.

```java
// Java / JUnit example
public void testCreate() {
    MyClass obj = new MyClass();
}
```

```cpp
// C++ / CppUnit example
TEST(create, MyClass) {
    MyClass obj;
}
```

**Why this first:** The compiler tells you exactly what dependencies are missing. The runtime tells you exactly which side effects fire. You do not need to reason about the code — the toolchain performs the diagnosis for you. Construction tests look strange (no assertion, no verification), but they are free diagnostic instruments. Once you can construct the object, rename or replace the test with a real one.

Attempt to compile and run. The error message routes you directly to the root cause in Step 2.

### Step 2: Classify by Root Cause

Feathers identifies four root causes for class-level test resistance. Map your error to one:

| # | Root Cause | Typical Signal |
|---|-----------|----------------|
| 1 | Objects cannot be created easily | Too many hard-to-build parameters; nested object chains |
| 2 | Test harness won't build with the class in it | Compile errors from header chains (C++) or linker failures |
| 3 | Constructor has bad side effects | Test connects to DB, sends email, writes files, hits network |
| 4 | Significant work in constructor; need to sense it | Heavy initialization; values computed during construction are needed in assertions |

Root causes 1, 6, and 7 (Onion Parameter, Aliased Parameter) → hard-to-create objects
Root cause 2 → build/link failure (Horrible Include Dependencies, C++ only)
Root causes 3 and 4 → constructor side effects or resource allocation (Hidden Dependency, Construction Blob)
Root cause 4 (sensing) → Construction Blob with sensing need

### Step 3: Match to the 7 Class-Level Cases (Chapter 9)

Once you have the root cause, identify the specific case using these detection rules:

**Case 1 — Irritating Parameter**
- Signal: A constructor parameter itself has a heavy constructor (network, file, DB on construction)
- The parameter IS passed in explicitly; it's just expensive to create
- Technique: **Extract Interface** on the problematic parameter type, then create a fake implementation. Alternative: **Pass Null** if the parameter is not actually used in the code path under test.
- Why Extract Interface: It severs the compile-time dependency on the concrete type without changing the caller's API.
- Why Pass Null is legitimate: In a garbage-collected language (Java, C#), passing null for an unused parameter simply means the variable is never dereferenced. The runtime will throw if you're wrong, making the mistake immediately visible.

**Case 2 — Hidden Dependency**
- Signal: Constructor calls `new SomeService()` or `SomeGlobal.connect()` internally — the dependency is not in the parameter list
- No way to substitute the dependency from outside
- Technique: **Parameterize Constructor** — move the `new` call outside the constructor and pass the object in. Provide a convenience constructor with the original signature that delegates to the new one.
- Why: Externalizing the dependency gives tests control over which implementation is used.

**Case 3 — Construction Blob**
- Signal: Constructor builds a chain of objects (A creates B creates C), and you need to sense through one of them
- Parameterize Constructor would require passing too many parameters
- Techniques (in order of preference):
  1. **Extract and Override Factory Method** (Java/C# only) — extract the object-creation code into a protected factory method, override it in a test subclass
  2. **Supersede Instance Variable** — add a setter that replaces the created object after construction; use with extreme care in C++ (manual memory management)
- Why not Parameterize Constructor here: A large parameter list creates its own construction problem.

**Case 4 — Irritating Global Dependency (Singleton)**
- Signal: Constructor calls `SomeClass.getInstance()` or accesses a static global; cannot be replaced from outside
- Technique: **Introduce Static Setter** — add a `setTestingInstance(T instance)` method to the singleton that replaces the static field. In tests, set a fake before each test and reset after.
- Supplement with: **Extract Interface** on the singleton so the static field holds an interface type, not a concrete class — this allows fake implementations.
- Why: Relaxing the singleton property in test environments is safe as long as no production code calls the setter. A build-time check can enforce this.

**Case 5 — Horrible Include Dependencies (C++ only)**
- Signal: Including the class header transitively pulls in thousands of lines; the test file takes minutes to compile or fails to link
- Technique: **Definition Completion** — provide stub definitions of the problematic classes in the test file or a `Fakes.h` include file, creating a separate test binary for this class
- Why: This severs the compile-time dependency without modifying production headers. Maintenance cost is real — reserve for severe cases only.

**Case 6 — Onion Parameter**
- Signal: The constructor needs Object A, which needs Object B, which needs Object C — a deeply nested creation chain
- Technique: **Extract Interface on the outermost layer** to create a single fake that stands in for the entire chain. If the parameter is genuinely unused in the test path, **Pass Null**.
- Why Extract Interface on outermost: You only need to go one level deep. A fake of the immediate parameter type breaks the whole chain.

**Case 7 — Aliased Parameter**
- Signal: A parameter type inherits from a base class that is also used as a field type — you cannot extract an interface for it without redesigning the entire hierarchy
- Technique: **Subclass and Override Method** — subclass the parameter type and override the specific method that causes the problem (the side effect or heavy operation)
- Why not Extract Interface: Building an interface hierarchy parallel to an existing class hierarchy is disproportionate work. Selective method overriding is surgical.

**Full case-to-technique table:** See `references/class-level-cases.md`.

### Step 4: Apply the 4 Method-Level Obstacles (Chapter 10)

If the class IS instantiable but a specific method cannot be exercised in a test, move to Chapter 10 diagnostics. These apply after Step 3 resolves construction obstacles.

**Obstacle 1 — Method Not Accessible**
- Signal: Method is `private`, `package-private`, or otherwise hidden; you cannot call it from the test file
- First ask: Can you test the behavior through a public method that calls this one? If yes, do that — it tests the method as it is actually used.
- If not: Change `private` to `protected` and create a test subclass that exposes it publicly. This is preferable to reflection-based access, which masks design problems.
- Root cause: The class has too many responsibilities. The inaccessible method belongs on a separate class. Schedule that refactoring; use the subclass approach as a bridge.

**Obstacle 2 — Hard to Construct Parameters**
- Signal: The method signature takes parameters that are expensive or impossible to construct in a test
- This is structurally the same as class-level Cases 1, 6, and 7
- Apply the same techniques: **Extract Interface**, **Pass Null**, or **Adapt Parameter** for sealed/final library types that cannot be subclassed

**Obstacle 3 — Method Has Bad Side Effects**
- Signal: Calling the method sends email, writes to DB, launches a process, modifies shared state
- Technique: **Extract and Override Call** — extract the side-effecting call into its own method, then override it in a test subclass to do nothing (or capture the call for assertion)
- Why: This lets you test the logic surrounding the side effect without triggering the side effect itself.

**Obstacle 4 — Need to Sense Effects Through an Object**
- Signal: The method produces its result by mutating an object it holds internally — there is no return value and no output parameter to check
- Technique: **Subclass and Override Method** — override the method that performs the mutation, capture the call, and assert on captured values. Alternatively, extract the collaboration into a seam and substitute a sensing fake.
- Why: Command/Query Separation is violated here by design. The sensing fake enforces it for the test.

**Full obstacle-to-technique table:** See `references/method-level-cases.md`.

### Step 5: Produce a Diagnostic Artifact

After completing the classification, write a short diagnostic report (template in Outputs section) naming:
- The root cause category
- The specific case or obstacle
- The recommended technique
- The ordered sequence if multiple obstacles coexist

When multiple obstacles exist, resolve them in this order:
1. Build/compile obstacles first (Case 5 — cannot proceed until it compiles)
2. Construction obstacles second (Cases 1–4, 6–7 — cannot write any test until the object can be created)
3. Method-level obstacles third (Obstacles 1–4 — apply after the class is instantiable)

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Class name | Yes | Fully qualified name of the class under investigation |
| Language | Yes | Java, C#, C++, Python, etc. |
| Constructor signature | Yes | Parameter types and their dependencies |
| Error message | Recommended | Compile error, linker error, or runtime exception from the construction test |
| Test framework | Yes | JUnit, NUnit, Google Test, pytest, etc. |
| Target method | If method-level | The specific method you want to test |

## Outputs

### Diagnostic Report (`diagnostic-report.md`)

```markdown
## Test Harness Diagnostic: [ClassName]

**Language:** [Java / C# / C++ / other]
**Framework:** [JUnit / NUnit / Google Test / other]
**Date:** [ISO date]

### Construction Test Result
[Paste compile error or runtime exception, or "compiled and ran cleanly"]

### Root Cause
[One of: Objects can't be created easily / Harness won't build / Constructor has bad side effects / Significant work in constructor]

### Specific Case
[One of the 7 class-level cases or 4 method-level obstacles — use the case name]

### Detection Evidence
[The specific line/error/behavior that triggered this classification]

### Recommended Technique
[Technique name (Part III reference page if known)]

### Ordered Sequence (if multiple obstacles)
1. [First technique — addresses build/compile blocker]
2. [Second technique — addresses construction blocker]
3. [Third technique — addresses method-level blocker]

### Rationale
[One sentence per technique explaining why it fits this specific situation]
```

## Key Principles

**Construction tests are free diagnostic tools — use them first.** Writing a `testCreate()` with no assertion costs almost nothing and eliminates all guesswork about which dependencies are actually needed.

**The error message IS the diagnosis — read it.** The compiler or runtime enumerates missing dependencies precisely. Treat it as a structured input to the classification process, not as noise to dismiss.

**Pass Null is legitimate when the parameter is unused in the test path.** In garbage-collected languages, null for an unused parameter is safe — the runtime will surface misuse immediately as a NullPointerException. Do not pass null in production code. In C/C++, do not pass null unless the runtime detects null pointer dereferences.

**When multiple obstacles exist, order matters.** Fix construction obstacles before method-level obstacles. Fix compile/link obstacles before construction obstacles. Attempting to sense through a method while the class still won't compile is wasted effort.

**The goal is testability, not elegance.** Test subclasses and methods with poor names are acceptable intermediate states. Once tests exist, the design can be improved safely.

## Examples

### Example 1: Irritating Parameter

**Situation:** `CreditValidator(RGHConnection connection, CreditMaster master, String id)` — `RGHConnection` opens a TCP socket when constructed.

**Construction test result:** Compiles, but the test takes 10 seconds and fails when the server is down.

**Classification:** Root Cause 1 (objects can't be created easily) → Case 1 (Irritating Parameter)

**Recommended technique:** Extract Interface on `RGHConnection` → create `IRGHConnection`. Implement `FakeConnection` returning pre-configured reports. `CreditMaster` loads a file quickly — it is not the problem.

**Pass Null alternative:** If the specific method being tested does not call any `RGHConnection` methods, pass `null` for `connection` and confirm with the construction test.

---

### Example 2: Hidden Dependency

**Situation:** `PaymentProcessor()` constructor calls `new DatabaseFactory(config).connect()` internally. No parameters.

**Construction test result:** Runs, but hits the database, which is unavailable in CI.

**Classification:** Root Cause 3 (constructor has bad side effects) → Case 2 (Hidden Dependency)

**Recommended technique:** Parameterize Constructor — extract the `DatabaseFactory` creation out of the constructor. Add `PaymentProcessor(DatabaseFactory factory)` as the primary constructor. Provide the original no-arg constructor delegating to it: `PaymentProcessor() { this(new DatabaseFactory(config)); }`. In tests, pass a fake `DatabaseFactory`.

---

### Example 3: Construction Blob

**Situation:** `WatercolorPane(Form border, WashBrush brush, Pattern backdrop)` constructor creates `Panel`, `Panel`, and `FocusWidget` internally in sequence. You need to assert on the state of `FocusWidget` after construction.

**Classification:** Root Cause 4 (significant work in constructor, needs sensing) → Case 3 (Construction Blob)

**Recommended technique (Java/C#):** Extract and Override Factory Method — extract the `FocusWidget` creation into `protected FocusWidget createCursor(WashBrush brush, Panel panel)`, override it in a test subclass to return a `TestingFocusWidget`.

**Fallback (C++):** Supersede Instance Variable — add `void supersedeCursor(FocusWidget* newCursor)`, call it in the test after construction. Delete the old cursor carefully.

## References

- `references/class-level-cases.md` — Full 7-case reference table: detection rules, techniques, worked examples, trade-offs
- `references/method-level-cases.md` — Full 4-obstacle reference table: detection rules, techniques, worked examples

**Source chapters:**
- Chapter 9 — "I Can't Get This Class into a Test Harness" (class-level obstacles and 7 cases)
- Chapter 10 — "I Can't Run This Method in a Test Harness" (method-level obstacles and case studies)

**Part III techniques referenced:**
- Extract Interface (p. 362)
- Parameterize Constructor (p. 379)
- Extract and Override Factory Method (p. 350)
- Supersede Instance Variable (p. 404)
- Introduce Static Setter (p. 372)
- Definition Completion (C++ only)
- Subclass and Override Method (p. 401)
- Adapt Parameter (p. 326)
- Extract and Override Call (p. 348)
- Expose Static Method (p. 345)

## License

[CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — BookForge Skills. Source: *Working Effectively with Legacy Code* by Michael C. Feathers (2004, Prentice Hall). Skills represent transformative synthesis; book content is not reproduced verbatim.

## Related BookForge Skills

**Prerequisites (run before this skill):**
- `legacy-code-change-algorithm` — this diagnostic executes Step 3 of that algorithm
- `seam-type-selector` — identifies the seam type (object, link, preprocessing) to exploit; use when the technique recommendation requires seam selection

**Downstream (run after this skill):**
- `dependency-breaking-technique-executor` — executes the specific technique identified by this diagnostic
