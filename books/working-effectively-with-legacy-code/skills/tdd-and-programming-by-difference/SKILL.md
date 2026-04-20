---
name: tdd-and-programming-by-difference
description: "Add features to tested code using TDD or Programming by Difference. Use whenever a developer is adding a feature to a class that already has tests (or can be brought under test) — 'how do I add this feature', 'test-driven development for legacy', 'red green refactor', 'TDD cycle', 'add behavior with tests', 'inheritance to add feature', 'programming by difference', 'subclass to add behavior', 'Liskov substitution', 'LSP violation'. Triggers for 'I just got this class under test, now I need to add X'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/tdd-and-programming-by-difference
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [8]
domain: software-engineering
tags: [legacy-code, testing, tdd, refactoring, software-engineering, feature-addition]
depends-on:
  - legacy-code-change-algorithm
  - safe-legacy-editing-discipline
  - characterization-test-writing
execution:
  tier: 1
  mode: full
  inputs:
    - type: codebase
      description: "Class that is under test (or testable) + feature specification"
  tools-required: [Read, Edit, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Codebase with working test framework."
discovery:
  goal: "Add a feature to tested code using the appropriate technique (TDD vs Programming by Difference)."
  tasks:
    - "Confirm the class IS under test"
    - "Decide TDD vs Programming by Difference"
    - "Execute the chosen approach"
    - "For PbD: normalize the inheritance (push up or push down) once feature works"
    - "Detect LSP violations"
  audience:
    roles: [software-engineer, backend-developer]
    experience: intermediate
  when_to_use:
    triggers:
      - "Adding a feature to a class that has tests"
      - "Feature should coexist with existing class behavior"
      - "Prefer tests-first workflow"
    prerequisites:
      - skill: characterization-test-writing
        why: "If class is not yet under test, characterize first"
    not_for:
      - "Class is NOT testable — use legacy-code-addition-techniques (Sprout/Wrap) instead"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 11
    iterations_needed: null
---

# TDD and Programming by Difference

## When to Use

The class is already under test — or can be brought under test with minimal effort. You need to add a new feature and you want to do it safely, with tests driving the design from the start.

This skill covers two complementary techniques:

- **Test-Driven Development (TDD):** the default. Language-agnostic. Add the feature directly to the class by writing one failing test at a time, implementing just enough to pass, then removing duplication.
- **Programming by Difference (PbD):** object-oriented only. Create a subclass, write tests against it, implement the feature there, then normalize the inheritance hierarchy. Useful when you want to defer the integration decision until you can see the feature working.

If the class is **not yet under test**, do not start here. Run `characterization-test-writing` first to establish a safety net, then return. If the class cannot be brought under test at all, use `legacy-code-addition-techniques` (Sprout Method or Wrap Method) instead.

## Context and Input Gathering

Before choosing an approach, collect:

1. **The target class** — confirm it has passing tests or can be brought into a test harness quickly.
2. **The feature specification** — what the new behavior should do, including edge cases you can identify now.
3. **The language** — PbD requires an object-oriented language with single-class inheritance. TDD works in any language.
4. **Whether modifying the existing class is feasible** — if the class is shared, frozen, or owned by another team, PbD may be the safer path.

## Process

### Step 1: Confirm the Class Is Under Test

Run the existing test suite for the target class. All tests must pass before you write a single new line of feature code. A failing test baseline is a signal: stop, diagnose, and fix before proceeding.

If no tests exist for this class, invoke `characterization-test-writing` now. Come back here when you have a passing baseline.

### Step 2: Decide — TDD or Programming by Difference

Use this decision rule:

**Use TDD (default) when:**
- You can modify the existing class directly.
- The feature belongs in the class — it is not a variant, an override, or an alternative behavior mode.
- The language does not require an OO inheritance model (procedural, functional, etc.).

**Use Programming by Difference when:**
- You cannot or do not want to modify the existing class directly (shared, frozen, or complex dependency on existing behavior).
- You want to prove the feature works in isolation before deciding where it lives in the hierarchy.
- The integration direction is unclear — you need to see the feature first, then decide: push it up (shared behavior) or push it down (specialized subclass).

When uncertain, choose TDD. PbD adds a normalization step that TDD avoids.

### Step 3 (TDD Path): Run the 5-Step Cycle

For each slice of the feature, execute this cycle in full before moving to the next slice:

**1. Write a failing test case.**
Write a test for the method or behavior you need. Do not write more than one new test at a time. The test must fail when you run it now — if it passes immediately, the test is wrong or the feature already exists.

**2. Get it to compile.**
Add the minimum code required for the test to compile: method signature, return type, stub body. Return a nonsense value (NaN, -1, empty string, null) so the test fails at assertion, not at compilation.

**3. Make it pass.**
Implement only enough code to make this specific test pass. Do not generalize. Do not add untested behavior. Write the simplest implementation that works.

**4. Remove duplication.**
Look for structural duplication between the new code and existing code. Extract shared behavior into a helper method, a shared base, or a well-named private. Do not skip this step — duplication left in place becomes a maintenance burden and obscures design intent. The tests you now have make this safe.

**5. Repeat.**
Move to the next test case. Each iteration narrows in on the full behavior — edge cases, error cases, boundary conditions.

**InstrumentCalculator example — two full iterations:**

*Iteration 1: base case*
```java
// Step 1: Failing test
public void testFirstMoment() {
    InstrumentCalculator calculator = new InstrumentCalculator();
    calculator.addElement(1.0);
    calculator.addElement(2.0);
    assertEquals(-0.5, calculator.firstMomentAbout(2.0), TOLERANCE);
}

// Step 2: Stub — compiles, fails assertion
public double firstMomentAbout(double point) {
    return Double.NaN;
}

// Step 3: Implementation that passes
public double firstMomentAbout(double point) {
    double numerator = 0.0;
    for (Iterator it = elements.iterator(); it.hasNext(); ) {
        double element = ((Double)(it.next())).doubleValue();
        numerator += element - point;
    }
    return numerator / elements.size();
}

// Step 4: No duplication yet — proceed
```

*Iteration 2: edge case — empty elements list*
```java
// Step 1: New failing test for the zero-division case
public void testFirstMoment_noElements() {
    try {
        new InstrumentCalculator().firstMomentAbout(0.0);
        fail("expected InvalidBasisException");
    } catch (InvalidBasisException e) { }
}

// Step 2: Update declaration to compile
public double firstMomentAbout(double point) throws InvalidBasisException { ... }

// Step 3: Add guard clause to pass
public double firstMomentAbout(double point) throws InvalidBasisException {
    if (elements.size() == 0)
        throw new InvalidBasisException("no elements");
    // ... existing loop ...
}

// Step 4: When secondMomentAbout arrives, extract nthMomentAbout(point, n)
//         to remove the loop duplication between the two methods.
```

> **Why the duplication step is non-negotiable:** Skipping it leaves clones in the codebase. Future developers find `firstMomentAbout` and `secondMomentAbout` side by side, both with the same loop, and change one but not the other. The TDD cycle's power comes from the entire loop — removing duplication is the step that makes the code better, not just tested.

### Step 4 (Programming by Difference Path): Create a Testing Subclass

Instead of modifying the existing class, create a subclass whose sole purpose is to introduce the new feature. Write tests against the subclass, not the parent.

```java
// Existing tested class — do not touch yet
public class MessageForwarder {
    private InternetAddress getFromAddress(Message message) { ... }
    // ...
}

// New subclass introduces the feature
public class AnonymousMessageForwarder extends MessageForwarder {
    @Override
    protected InternetAddress getFromAddress(Message message)
            throws MessagingException {
        return new InternetAddress("anon-members@" + listAddress);
    }
}

// Test drives against the subclass
public void testAnonymous() throws Exception {
    MessageForwarder forwarder = new AnonymousMessageForwarder();
    forwarder.forwardMessage(makeFakeMessage());
    assertEquals("anon-members@" + forwarder.getDomain(),
                 expectedMessage.getFrom()[0].toString());
}
```

The test passes. The feature is proven. Now you have a decision to make (Step 5).

### Step 5 (PbD Path): Normalize the Inheritance

Once the feature tests are passing, decide how to integrate:

**Option A — Push behavior UP (shared by all subclasses):**
The feature belongs in the parent class. Refactor the parent to include the logic (e.g., via a configuration flag or a new abstract method), verify all tests still pass, and delete the subclass.

```java
// Move anonymous logic into MessageForwarder via configuration
private InternetAddress getFromAddress(Message message) throws MessagingException {
    if (configuration.getProperty("anonymous").equals("true")) {
        return new InternetAddress("anon-members@" + domain);
    }
    Address[] from = message.getFrom();
    if (from != null && from.length > 0)
        return new InternetAddress(from[0].toString());
    return new InternetAddress(getDefaultFrom());
}
// AnonymousMessageForwarder is now deletable — tests pass without the override
```

**Option B — Push behavior DOWN (specialized subclass):**
The behavior is genuinely specific to one variant. Make the parent method abstract, force subclasses to provide their own implementation. No subclass should override a concrete method — that is the normalized form.

```java
// Normalized hierarchy: parent is abstract, subclasses provide implementations
public abstract class MessageForwarder {
    protected abstract InternetAddress getFromAddress(Message message)
            throws MessagingException;
}
public class StandardMessageForwarder extends MessageForwarder {
    protected InternetAddress getFromAddress(Message message) { ... }
}
public class AnonymousMessageForwarder extends MessageForwarder {
    protected InternetAddress getFromAddress(Message message) { ... }
}
```

> **What is a normalized hierarchy?** A hierarchy in which no class has a method that overrides a concrete method it inherited. Every method is either implemented once (in the class that owns it) or abstract (delegated to all subclasses). In a normalized hierarchy, "How does this class do X?" has a single, unambiguous answer.

### Step 6: Watch for LSP Violations

During PbD normalization, check whether the subclass changes method semantics in a way that breaks callers who expect the parent's behavior.

**Classic LSP violation pattern:**
```java
// Parent: setWidth(3) and setHeight(4) gives area = 12
Rectangle r = new Square();
r.setWidth(3);
r.setHeight(4);
// Actual area: 16 — Square.setWidth() also changed height to maintain squareness
// Caller expected 12. LSP is violated.
```

**Red flags during normalization:**
1. The subclass override changes a return value's *meaning*, not just its value.
2. A caller that holds a reference typed as the parent class would behave differently if it received a subclass instance.
3. The override removes a guarantee the parent's contract provided (e.g., parent never throws, subclass throws).

**Rules of thumb to avoid LSP violations:**
- Prefer not to override concrete methods. If you must, call `super.method()` inside the override wherever possible.
- If the override changes semantics rather than extends them, use composition (delegate to a collaborator object) instead of inheritance.

If you detect an LSP violation during normalization, do not suppress it. Restructure: either use composition, make the parent abstract, or move the feature out of the inheritance hierarchy entirely.

### Step 7: Integrate

After normalization (PbD) or after the last duplication-removal pass (TDD):

1. Run the full test suite for the class. All tests — old and new — must pass.
2. Search for callers of any methods you modified or added. Verify callers compile and behave correctly with the new behavior.
3. Delete any scaffolding: temporary subclasses used only during PbD, helper stubs added to make tests compile.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Target class with tests | Yes | The class to extend — must have a passing test baseline |
| Feature specification | Yes | What the new behavior should do, including known edge cases |
| Language + OO capability | Yes | Determines whether PbD is available |
| Integration intent | No | Whether the new behavior is shared or specialized — informs normalization direction |

## Outputs

| Output | Description |
|--------|-------------|
| Feature code | New methods or overrides implementing the specified behavior |
| Passing tests | New test cases covering the feature (base case, edge cases, error cases) |
| Normalized hierarchy | For PbD: inheritance resolved to push-up or push-down form with no LSP violations |
| `chosen-approach.md` | Brief record of why TDD or PbD was selected and how normalization was resolved (create in the working directory or PR description) |

## Key Principles

**TDD is the default — PbD only when integration decision is deferred.**
TDD adds the feature in place with full test support. PbD defers the integration decision to after the feature is proven. Do not use PbD because inheritance "seems easier" — it is only appropriate when you genuinely cannot or should not modify the existing class directly.

**The duplication-removal step is a first-class step, not a suggestion.**
Every TDD cycle must complete through step 4. Leaving duplication behind — two methods with the same loop, two classes with the same logic — creates a compound maintenance burden. The tests make removal safe. Do it now, not "later."

**PbD's test subclass is scaffolding — normalize the inheritance after the feature works.**
A subclass that overrides a concrete method is a temporary construction. Once you have a passing test, decide where the behavior really belongs (parent or subclass) and restructure. Do not ship a normalized-by-accident hierarchy.

**LSP violation = subclass changes method semantics in a way that breaks callers.**
Overriding a concrete method silently redirects callers who are unaware of the subclass. If a caller typed as `Parent p = new ChildInstance()` would receive different behavior from `Parent p = new ParentInstance()` in a way they cannot predict or handle, you have an LSP violation. Detect it during normalization; fix it before shipping.

## Examples

### Example 1: TDD on InstrumentCalculator

**Task:** Add `firstMomentAbout(double point)` to a class with no methods yet.

Iteration 1 writes `testFirstMoment()` asserting −0.5 for inputs [1.0, 2.0] about point 2.0. The stub returns `NaN` (compiles, fails). The implementation adds the numerator loop and returns `numerator / elements.size()`. No duplication yet — proceed.

Iteration 2 writes `testFirstMoment_noElements()` expecting `InvalidBasisException`. The stub adds the declaration but no guard — the test throws `ArithmeticException` (wrong exception, still fails). Adding the guard `if (elements.size() == 0) throw new InvalidBasisException(...)` makes it pass.

When `secondMomentAbout` is needed, copy the loop, change the accumulator to `Math.pow(element - point, 2.0)`, get the test passing, then extract `nthMomentAbout(double point, double n)` as a shared private. Both public methods delegate to it. Duplication removed.

### Example 2: PbD on a Tested PaymentProcessor

**Task:** Add `TrialUser` behavior — 50% discount on everything — without modifying `PaymentProcessor` directly (it is owned by another team and used by 40 callers).

1. Subclass: `TrialPaymentProcessor extends PaymentProcessor`. Override `calculateCharge(double basePrice)` to return `basePrice * 0.5`.
2. Write tests against `TrialPaymentProcessor`. Tests pass.
3. Normalize: Does the discount belong in the parent? No — it is specific to trial users. Push DOWN: make `calculateCharge` abstract in `PaymentProcessor`. Create `StandardPaymentProcessor` for the existing logic. `TrialPaymentProcessor` provides the discounted implementation.
4. Check LSP: callers using `PaymentProcessor` references receive either standard or trial logic — both return a valid charge amount of the same type. No semantic breach. No violation.

### Example 3: LSP Violation Detected and Restructured

**Task:** Add `PremiumEmployee` as a PbD subclass of `Employee`. Override `pay()` to return a struct with base + bonus, whereas `Employee.pay()` returns a plain salary `double`.

This violates LSP: callers typed as `Employee e = new PremiumEmployee()` would receive a struct where they expected a double, breaking code that assigns the result to a `double` variable.

**Fix:** Do not override `pay()`. Instead, add a new `payWithBonus()` method on `PremiumEmployee`. Or restructure `Employee.pay()` to return a `PayResult` object in all cases, with a `bonus` field that is 0.0 for standard employees. Either approach preserves substitutability.

## References

- `references/legacy-code-fundamentals.md` — core definitions: seams, normalized hierarchy, LSP

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — BookForge Skills, derived from "Working Effectively with Legacy Code" by Michael C. Feathers. Skill interpretation, structure, and synthesis are original BookForge content.

## Related BookForge Skills

**Direct dependencies (run before this skill):**
- `legacy-code-change-algorithm` — this skill executes steps 4–5 of that algorithm (write tests, then make the change)
- `safe-legacy-editing-discipline` — guides careful editing once tests are in place
- `characterization-test-writing` — required prerequisite if the class is not yet under test

**Invoke instead if class is not testable:**
- `legacy-code-addition-techniques` — Sprout Method, Sprout Class, Wrap Method for code that cannot be brought under test

**Cross-reference:**
- `unit-test-quality-checker` — validates that the new tests written in this skill meet quality thresholds
