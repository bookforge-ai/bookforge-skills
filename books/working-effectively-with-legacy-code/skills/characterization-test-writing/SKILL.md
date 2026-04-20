---
name: characterization-test-writing
description: "Write tests that pin down the actual current behavior of untested legacy code as a safety net for change. Use whenever a developer needs to create a regression safety net before modifying code — 'I don't know what tests to write', 'what should I test in legacy code', 'how do I write tests for code I didn't write', 'tests to preserve behavior', 'golden tests', 'snapshot tests for old code', 'characterization test', 'cover before modify'. Activates for 'legacy code testing', 'untested code', 'write tests before changing', 'regression safety net', 'behavior-preservation tests', 'pin down behavior'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/characterization-test-writing
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [2, 13]
domain: software-engineering
tags: [legacy-code, testing, unit-testing, refactoring, software-engineering, characterization-tests]
depends-on:
  - legacy-code-change-algorithm
  - unit-test-quality-checker
  - change-effect-analysis
execution:
  tier: 2
  mode: full
  inputs:
    - type: codebase
      description: "Target class/method to characterize + test harness setup"
  tools-required: [Read, Edit, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Codebase with an xUnit-style test framework configured. The target code must be instantiable in the harness."
discovery:
  goal: "Produce a suite of characterization tests that pin down actual current behavior as a regression safety net."
  tasks:
    - "Choose what to characterize (driven by effect-analysis output)"
    - "Place target code in test harness"
    - "Write assertions known to fail, let failures reveal actual behavior"
    - "Update assertions to match actual behavior"
    - "Flag behaviors that look like bugs but preserve them in the test"
    - "Iterate until coverage is sufficient for the planned change"
  audience:
    roles: [software-engineer, backend-developer, qa-engineer]
    experience: intermediate
  when_to_use:
    triggers:
      - "About to change legacy code with no existing tests"
      - "Need to verify no regression after refactoring"
      - "Developer doesn't know what tests to write"
    prerequisites:
      - skill: legacy-code-change-algorithm
        why: "This is Step 4 (write tests) of the algorithm"
      - skill: change-effect-analysis
        why: "Output tells you WHERE to write characterization tests"
    not_for:
      - "Brand new code — use TDD instead"
      - "Code with intended behavior specs — write correctness tests"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 13
    iterations_needed: null
---

# Characterization Test Writing

## When to Use

You are about to change untested legacy code and need to know that your changes won't silently alter the system's existing behavior. You do not have specs or requirements documents you trust — or if you do, you know the code may have drifted from them. You need a behavioral safety net anchored to what the code **actually does**, not to what you hope it does.

This skill is Step 4 of the `legacy-code-change-algorithm`. Before you arrive here, `change-effect-analysis` should have told you *where* to write tests. This skill tells you *how*.

Do not use this skill to find bugs. Manual exploration is faster for bug discovery. Characterization tests are a *change-detection mechanism*, not a correctness oracle.

## Context and Input Gathering

Before writing a single test, collect:

1. **The target code** — which class(es) and method(s) you will change. If you don't have this, run `change-effect-analysis` first.
2. **The change description** — what you plan to modify. This defines the coverage scope. You stop when the tests cover the planned change, not the entire class.
3. **Effect analysis output** — the effect sketch or test-placement plan from `change-effect-analysis`. This tells you which methods to prioritize.
4. **The test framework** — confirm an xUnit-style test runner (JUnit, pytest, NUnit, RSpec, etc.) is configured and can run against the target code. If you cannot get the target class into a harness, invoke `test-harness-entry-diagnostics` before proceeding.

## Process

### Step 1: Determine Scope — What to Characterize

Use the effect analysis output to prioritize. Feathers' three-level heuristic, in priority order:

1. **Write tests for the area where you will make changes.** Cover the class and methods directly involved. Write enough cases to understand their behavior at a high level.
2. **Narrow to the specific things you will change.** Identify the individual branches and code paths your change will touch. You need at least one test that exercises each path the change will affect.
3. **If extracting or moving functionality, verify existence and connection.** Write tests that confirm the behavior you plan to move exists in the current location and is connected correctly. Exercise any type conversions involved — they are a common source of silent errors.

> **Why this order matters:** Starting too broad wastes effort characterizing code your change won't touch. Starting too narrow misses regression surface above the change point. The three levels give you the minimum safety net, nothing more.

### Step 2: Place Target Code in the Test Harness

Open or create a test file for the target class. Instantiate the class under test using the simplest construction path available.

```java
// Example: minimal harness setup
void testInitialState() {
    PageGenerator generator = new PageGenerator();
    // harness is ready — proceed to Step 3
}
```

If construction requires dependencies that are difficult to create (database connections, external services, deeply coupled collaborators), this is a dependency problem — invoke `test-harness-entry-diagnostics`. Do not skip the harness step by writing untestable assertions.

### Step 3: Write a Deliberately-Failing Assertion

Choose an expected value you are **certain is wrong**. Something obviously fake ("fred", -999, "PLACEHOLDER") works well. The point is not to guess the right answer — the point is to force the test runner to tell you the real answer.

```java
// Deliberately wrong — "fred" is certainly not what generate() returns
void testGenerate_initialState() {
    PageGenerator generator = new PageGenerator();
    assertEquals("fred", generator.generate());  // We know this will fail
}
```

> **Why write an assertion you know is wrong?** Because the test framework's failure message will contain the actual value. The failure IS the answer. This technique turns the test runner into a probe: you're not guessing the behavior, you're asking the code to show you.

### Step 4: Run the Test — Read the Failure

Run the test. Do not fix it yet. Read the failure message carefully.

```
junit.framework.ComparisonFailure: expected:<fred> but was:<>
```

The `but was:` portion is the actual current behavior of the code under those conditions. Write it down.

### Step 5: Update the Assertion to Match Actual Behavior

Change the expected value to what the failure message reported. The test now documents one true fact about the system.

```java
void testGenerate_initialState() {
    PageGenerator generator = new PageGenerator();
    assertEquals("", generator.generate());  // Documents: empty PageGenerator generates ""
}
```

Run the test again. It must pass. If it does not (e.g., the output is nondeterministic or environment-dependent), investigate before proceeding.

### Step 6: Handle Discovered Bugs — Preserve, Flag, Decide Later

You will encounter behaviors during characterization that look like bugs. The code produces an output that seems clearly wrong — an off-by-one, an unexpected null, an exception where a value was expected.

**Do not change the test expectation to the "correct" value.** The test must document what the code actually does, not what it should do. Changing it to the intended behavior creates a test that fails immediately — a correctness test, not a characterization test.

Instead:

1. Keep the expected value as the actual observed behavior.
2. Add a comment marking it suspicious:
   ```java
   // SUSPECTED BUG: parse('') throws NullPointerException.
   // Preserving actual behavior. See discovered-bugs.md entry #2.
   @Test
   public void testParse_emptyString_throwsNPE() {
       assertThrows(NullPointerException.class, () -> parser.parse(""));
   }
   ```
3. Log the finding in `discovered-bugs.md` (create this file in the test directory or working directory):
   ```
   ## Bug Candidate #2
   - Method: CsvParser.parse(String)
   - Input: empty string ""
   - Actual behavior: throws NullPointerException
   - Expected (likely correct): return empty list []
   - Decision needed: fix before or after coverage is established?
   - Risk if fixed now: unknown callers may depend on the exception
   ```

> **Why preserve the buggy behavior in the test?** Because callers in legacy systems often depend on behaviors that look like bugs. A method that throws NPE on empty input may have callers that already catch that exception and route around it. Fixing the bug silently changes the callers' environment. Preserve, flag, and decide deliberately — after full coverage is in place and you can see the ripple effects.

### Step 7: Iterate — Cover the Change Surface

Return to the target code. Ask: does what I've characterized so far cover every code path my change will touch?

Techniques for finding more cases:

- **Look for tangled logic.** If a branch is hard to understand, write a test with inputs designed to force that branch. Use a sensing variable if needed to confirm the branch executed.
- **Probe extreme values.** What happens at 0, -1, empty string, null, maximum integer? Often behavior at boundaries is the behavior most likely to break.
- **Check invariants.** Is there something that should always be true about the object's state? Write a test that verifies it.
- **Use the code as a guide.** You are allowed to read the implementation. Every `if` branch, every loop condition, every method call is a hint about what to exercise.

Continue iterating (Steps 3–7) until you can answer yes to: "If my planned change silently alters behavior outside its intended scope, will at least one of these tests catch it?"

### Step 8: Verify Coverage Meets the Change's Requirements

Review the full characterization test suite against the planned change:

- Every code path the change touches has at least one test.
- Every type conversion along those paths has been exercised with inputs that would expose truncation or precision loss.
- Every method you plan to extract or move has a test verifying its behavior exists *before* the move.

You do not need complete coverage of the class. You need coverage sufficient for *this change*. Stop there.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Target class/method | Yes | The code you will change |
| Change description | Yes | What you plan to modify — defines coverage scope |
| Effect analysis output | Yes | From `change-effect-analysis` — test-placement plan or effect sketch |
| Test framework | Yes | Configured xUnit runner targeting the codebase |

## Outputs

| Output | Description |
|--------|-------------|
| Characterization test suite | Source files containing passing tests that document actual behavior |
| `discovered-bugs.md` | Log of flagged suspicious behaviors with context, preserved-but-suspicious test references, and decision notes |

## Key Principles

**"What the system DOES is more important than what it SHOULD do."**
In nearly every legacy system, the code has diverged from the original intent. Characterization tests document reality, not the requirements document. If you write tests based on what you think the code should do, you are writing bug-finding tests — a different and less useful activity for this context.

**A deliberately-failing assertion is a diagnostic tool — the failure IS the answer.**
You are not guessing the expected value. You are asking the test runner to reveal it. The only investment is running the test twice: once to learn the actual value, once to confirm the updated assertion passes.

**Discovered bugs go on paper, not into the corrected test.**
Preserve actual behavior in the test. Flag the bug in `discovered-bugs.md`. Decide whether to fix it after full coverage is established and you can see downstream effects. This is not laziness — it is disciplined risk management in a system where callers may depend on buggy behavior.

**Stop when coverage is sufficient for THIS change.**
The goal is not full system coverage. It is a safety net for a specific planned change. Overcharacterizing wastes effort on code paths your change will never affect. The effect analysis output defines the boundary.

**Testing to detect change — not testing to show correctness.**
These are two different philosophies. Tests that show correctness assert the right answer. Tests that detect change assert the *current* answer and alert you when it shifts. Characterization tests use the second philosophy. This is intentional. The tests have no moral authority over the code — they just record what the pieces do, so you can see when something has moved.

## Examples

### Example 1: PageGenerator — Character-by-Character Discovery

You need to change `PageGenerator.generate()`. No tests exist. You don't know what it currently returns.

```java
// Iteration 1: Probe with obviously-wrong value
void testGenerate_noData() {
    PageGenerator generator = new PageGenerator();
    assertEquals("fred", generator.generate());
}
// Failure: expected:<fred> but was:<>
// Update:
void testGenerate_noData() {
    PageGenerator generator = new PageGenerator();
    assertEquals("", generator.generate());  // Documents: returns "" with no data loaded
}

// Iteration 2: Feed data, probe again
void testGenerate_withBaseRow() {
    PageGenerator generator = new PageGenerator();
    generator.assoc(RowMappings.getRow(Page.BASE_ROW));
    assertEquals("fred", generator.generate());
}
// Failure: expected:<fred> but was:<node><carry>1.1 vectrai</carry></node>
// Update:
void testGenerate_withBaseRow() {
    PageGenerator generator = new PageGenerator();
    generator.assoc(RowMappings.getRow(Page.BASE_ROW));
    assertEquals("<node><carry>1.1 vectrai</carry></node>", generator.generate());
}
```

After two iterations, you have two tests that document exactly what `PageGenerator.generate()` produces under two conditions. Any change you make that accidentally alters either of these outputs will be caught immediately.

### Example 2: Discovering a Bug During Characterization

You are characterizing `CsvParser.parse(String input)`. Your probe:

```java
void testParse_emptyInput() {
    CsvParser parser = new CsvParser();
    assertEquals("fred", parser.parse("").toString());
}
// Failure: NullPointerException at CsvParser.parse(CsvParser.java:34)
```

The code throws NPE on empty input. This looks like a bug — most CSV parsers should return an empty list. What do you do?

1. Write the test to document the actual behavior (the NPE), not the intended behavior:
   ```java
   // SUSPECTED BUG: throws NPE on empty input. See discovered-bugs.md #2.
   void testParse_emptyInput_throwsNPE() {
       assertThrows(NullPointerException.class, () -> new CsvParser().parse(""));
   }
   ```
2. Log it in `discovered-bugs.md`:
   ```
   ## Bug Candidate #2 — CsvParser.parse("")
   Actual: NullPointerException at CsvParser.java:34
   Expected (likely): return Collections.emptyList()
   Risk: 3 callers identified in OrderImporter, UserUploader, DataMigrationJob.
   Decision: review callers before fixing. Mark for post-coverage fix.
   ```
3. Continue characterizing the non-empty paths. Do not fix the bug now.

### Example 3: Pre-Extraction Safety Net for a Method Move

You plan to extract `FuelShare.addReading()`'s inner `if (lease.isMonthly())` block and move it to `ZonedHawthorneLease.computeValue()`. Before moving:

```java
// Characterize the else branch (gallons >= CORP_MIN) — the path being moved
void testAddReading_gallonsAboveCorpMin_chargesAtRate() {
    StandardLease lease = new StandardLease(Lease.MONTHLY);
    FuelShare share = new FuelShare(lease);
    share.addReading(FuelShare.CORP_MIN + 1, new Date());
    assertEquals(expectedCost, share.getCost());
}
```

Choose inputs that force the else branch. Confirm the test exercises the conversion from `priceForGallons(gallons)` to `totalPrice` — use a debugger or sensing variable if uncertain. After extraction, run the same test against `computeValue()` directly to confirm the behavior survived the move.

## References

- `references/legacy-code-fundamentals.md` — core definitions: legacy code, seams, characterization tests
- `references/test-harness-patterns.md` — common patterns for getting legacy classes into test harnesses

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — BookForge Skills, derived from "Working Effectively with Legacy Code" by Michael C. Feathers. Skill interpretation, structure, and synthesis are original BookForge content.

## Related BookForge Skills

**Direct dependencies (run before this skill):**
- `legacy-code-change-algorithm` — this skill is Step 4 of that algorithm
- `change-effect-analysis` — provides the effect sketch and test-placement plan that scopes this skill's work
- `unit-test-quality-checker` — validates the characterization tests you write here meet quality thresholds

**Invoke if blocked:**
- `test-harness-entry-diagnostics` — when the target class cannot be instantiated in the test harness (Step 2 blocker)

**Next steps:**
- `duplication-removal-via-extraction` — apply after characterization tests are in place, when refactoring to remove duplication
