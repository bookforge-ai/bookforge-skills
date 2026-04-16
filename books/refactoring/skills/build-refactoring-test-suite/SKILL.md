---
name: build-refactoring-test-suite
description: Build a sufficient automated test suite before refactoring existing code by applying a 6-step sequential construction workflow (test class → fixture → normal behavior → boundary conditions → expected errors → green-suite gate) and a bug-fix variant (write failing test first → reproduce → fix → verify green). Use this skill when you are about to refactor a class or module that lacks tests, when a bug report arrives and you need to pin it down before fixing it, when you want to establish the compile-and-test gate that makes every subsequent refactoring step safe to revert, or when you need to assess whether an existing test suite is adequate to protect a planned refactoring.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/build-refactoring-test-suite
metadata: {"openclaw":{"emoji":"🧪","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler"]
    chapters: [4]
tags: [refactoring, testing, code-quality]
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "A class, module, or file to be refactored, with or without existing tests."
  tools-required: [Read, Write, Bash]
  tools-optional: []
  mcps-required: []
  environment: "Working codebase with a test runner available. Output: a runnable test file that passes green, covering normal behavior, boundary conditions, and expected errors for the code under refactoring."
discovery:
  goal: "Produce a fast, self-checking test suite that turns green before any refactoring step begins and re-runs in seconds after every atomic change."
  tasks:
    - "Create a test class/file for the code under refactoring"
    - "Implement setup and teardown fixtures to isolate each test"
    - "Write tests for all normal, expected-behavior paths"
    - "Add boundary condition tests at edges and zero-value inputs"
    - "Write tests that verify expected errors and exceptions are raised correctly"
    - "Run the full suite and confirm green before proceeding to refactor"
  audience: "developers, engineers, anyone refactoring existing production code without adequate test coverage"
  when_to_use: "When a class or module needs to be refactored and does not yet have a test suite sufficient to detect regressions after each atomic change"
  environment: "Existing codebase. The code under refactoring should be readable. A test runner (any language) must be available."
  quality: placeholder
---

# Build Refactoring Test Suite

## When to Use

You are about to refactor code — extracting methods, moving fields, changing conditionals — and one of these is true:

- The code has no tests at all
- The existing tests are incomplete, untargeted, or only cover happy paths
- A bug has been reported and you need to pin it down before fixing and refactoring around it
- You are inheriting code from someone else and want a safety net before touching anything

This is the Level 0 foundation skill: every other refactoring mechanic in Fowler's catalog assumes this suite exists. Without it, you are refactoring blind. With it, every subsequent step is reversible — if a test turns red, you revert and try smaller steps.

**The core pattern:** build a self-checking test suite that runs in seconds, covers the code you are about to change, and can answer one question without human inspection: "Did I break anything?"

Before starting, confirm you have:
- Read access to the class or module being refactored
- A test runner installed for the language (pytest, JUnit, RSpec, Vitest, go test, etc.)
- The ability to run the test suite from the command line

---

## Context and Input Gathering

### Required Context

- **Target code:** The class, module, or file to be refactored. Read it fully before writing any tests.
- **Language and test framework:** Identify from the project structure (e.g., `pyproject.toml`, `package.json`, `pom.xml`, `go.mod`). Use the framework already in place — do not introduce a new one.
- **Existing tests:** Check for any test files that already cover the target. Run them first. If they all pass, extend rather than replace.

### Observable Context

Scan the target code for:
- **Public interface:** Every public method, function, or exported symbol is a testing target. Private internals are not — test through the public interface only.
- **Inputs and outputs:** What does each method take in and return? These define what to assert.
- **Error conditions:** What inputs should raise exceptions, return error codes, or produce empty results? These drive the error-path tests.
- **State mutations:** Does the class modify shared state? Fixtures must initialize and tear down that state per-test.
- **External dependencies:** Databases, files, network calls. These need either real test fixtures or test doubles (mocks/stubs). Prefer real fixtures for refactoring — mocks can hide regressions.

### Default Assumptions

- If no test framework exists → pick the language's idiomatic standard (pytest for Python, JUnit for Java, Vitest for TypeScript, etc.)
- If the code reads external files → create small, dedicated test data files in a `testdata/` or `fixtures/` directory
- If the code has database calls → prefer an in-memory or test-mode database over mocking; mocks test the mock, not the code
- If tests already exist and pass → run them first, then add missing coverage; do not re-implement passing tests

### Sufficiency Check

You are ready to start when:
1. You can read the target class/module completely
2. You know which test framework is in use
3. You know at least three things the code is supposed to do (its public contract)

If you cannot determine what the code is supposed to do (no comments, no documentation, unclear naming), read the calling code or integration tests first to reconstruct the intended behavior before writing unit tests.

---

## Process

### Step 1 — Create the Test Class/File

Create a dedicated test file for the code under refactoring. Place it where the project's test convention dictates (e.g., `tests/test_order.py`, `src/__tests__/Order.test.ts`, `OrderTest.java`).

**Why:** Each class under test needs its own test container. Mixing multiple classes into one test file makes isolation harder and failure messages harder to read. Using the project's existing naming convention ensures the test runner discovers the file automatically.

Minimal structure:

```
# Python
class TestOrder:
    pass

# Java
class OrderTest extends TestCase { }

# TypeScript
describe('Order', () => { })

# Go
func TestOrder(t *testing.T) { }
```

Run the empty test file immediately to confirm the runner finds and executes it without errors.

---

### Step 2 — Implement Setup and Teardown Fixtures

Before writing any test methods, define the shared state that every test will need. The test framework's `setUp`/`beforeEach`/`setup` hook runs before each test; `tearDown`/`afterEach`/`cleanup` runs after.

**Why:** Each test must be fully isolated — it must not depend on execution order, and it must not leave side effects that corrupt the next test. Setup creates a fresh environment; teardown cleans up resources (open files, database connections, temp files). Without this isolation, a failure in test 3 can cause test 4 to fail for unrelated reasons, making debugging misleading.

**Guidelines:**
- Initialize only what is shared across most tests in the fixture. Test-specific state belongs in the test method itself.
- If setup can fail (file not found, connection refused), let the error propagate — a setup failure is a hard stop, not a test failure.
- If teardown involves resource release (closing files, dropping test tables), do it unconditionally — use `finally` blocks or the framework's guaranteed cleanup mechanism.

```python
# Python example
class TestFileProcessor:
    def setup_method(self):
        self.input_file = open("testdata/sample.txt", "r")

    def teardown_method(self):
        self.input_file.close()
```

---

### Step 3 — Write Tests for Normal / Expected Behavior

For each public method, test the central, intended behavior first — the happy path. Ask: "What is this method supposed to do when given valid, typical input?"

**Why:** Start with normal behavior so you confirm the code works correctly before probing its edges. If normal behavior tests fail, the code is broken before you even touch it — that is useful information and must be resolved before any refactoring begins.

**Rules:**
- One behavior per test method. Do not write omnibus tests that check five things in sequence — when one assertion fails, you cannot tell which behavior broke.
- Name tests descriptively: `test_read_returns_correct_character`, not `test1`. Descriptive names are the failure message.
- Assert the specific output, not just "no exception was raised." Confirm the actual value.
- Write the test, then verify it can fail: temporarily corrupt the assertion value (e.g., assert `'x' == result` instead of `'d' == result`). If it does not fail, the test is not testing what you think.

```python
def test_read_returns_correct_character(self):
    # advance past the first three characters
    for _ in range(3):
        self.input_file.read(1)
    ch = self.input_file.read(1)
    assert ch == 'd'  # fourth character in the test file
```

---

### Step 4 — Add Boundary Condition Tests

After normal behavior is covered, identify the boundaries where behavior could change or break. Boundary conditions are the most productive place to find bugs.

**Why:** Most bugs hide at the edges — the first item, the last item, the empty collection, the zero value, the maximum value. Fowler calls this "playing the part of an enemy to your own code" — actively trying to find the conditions under which the code will fail, rather than confirming it works for typical input.

**Common boundary categories:**

| Category | Examples |
|---|---|
| **Sequence edges** | First element, last element, element after the last |
| **Empty inputs** | Empty string, empty list, empty file, zero-length collection |
| **Zero / null values** | Zero quantity, null reference, None, empty optional |
| **Maximum / minimum values** | Integer overflow boundary, max string length, single-item list |
| **Repeated calls** | Reading past end-of-file twice, calling close twice |

For each boundary, write a separate test method. Add a descriptive message to assertions so that when a boundary test fails, the output tells you which boundary broke.

```python
def test_read_at_end_of_file_returns_minus_one(self):
    # consume all 141 characters
    for _ in range(141):
        self.input_file.read(1)
    result = self.input_file.read(1)
    assert result == -1, "read at end of file should return -1"

def test_read_from_empty_file_returns_minus_one(self):
    empty = open("testdata/empty.txt", "r")
    result = empty.read(1)
    empty.close()
    assert result == -1, "read from empty file should return -1"
```

---

### Step 5 — Write Tests for Expected Errors and Exceptions

Test that error conditions produce the correct error, not just that they do not crash silently. If the code's contract says "raises ValueError on negative input" or "raises IOError if the stream is closed," write a test that verifies exactly that.

**Why:** Errors are part of the public contract. Failing to raise the expected error — or raising the wrong one — is a bug. These tests also protect against future refactoring silently swallowing exceptions.

**Pattern:**
- Close the resource intentionally, then attempt an operation — expect the specific error.
- Use the framework's `pytest.raises`, `assertRaises`, or `expect { }.to raise_error` idiom.
- If the test body completes without the expected error, force an explicit failure: `fail("expected error was not raised")`.

```python
def test_read_after_close_raises_io_error(self):
    self.input_file.close()
    with pytest.raises(IOError):
        self.input_file.read(1)
    # if no IOError is raised, pytest.raises will fail the test automatically
```

---

### Step 6 — Run the Full Suite: Green Gate

Run the entire test suite. All tests must pass — green — before any refactoring step begins.

**Why:** This is the precondition that makes refactoring safe. If the suite is red before you start, you do not know whether a subsequent red result was caused by your change or by a pre-existing bug. You must start from a known-good baseline.

**What to do if tests are red before you start:**
1. Do not begin refactoring yet.
2. Determine whether the failure is a test bug (wrong assertion) or a production bug.
3. If it is a production bug, decide: fix it first, or document it as a known failure and exclude that test from the baseline. Do not silently ignore red tests.
4. Once all tests pass (or excluded failures are documented), the green gate is established.

**The compile-and-test gate (applies to every subsequent step):**
Once the suite is green and refactoring begins, apply this gate after every single atomic change — not after a batch of changes:

```
make one atomic change → compile/lint → run test suite
  green → continue to next change
  red   → revert immediately, try a smaller step
```

"Atomic" means the smallest possible change that can be independently compiled and tested: extract one method, rename one variable, move one field. Never accumulate multiple changes before testing. Small steps mean small reverting cost.

If a language has a compiler, compile first — compilation errors caught before test execution are faster feedback than test failures.

---

## Bug-Fix Variant: Test-First Bug Reproduction

When fixing a bug rather than refactoring, use this variant workflow:

1. **Write a failing test that reproduces the bug.** Do this before touching production code. The test should fail because the bug exists.
2. **Confirm the test fails.** Run it. If it passes, the test is wrong — it is not actually testing the buggy behavior.
3. **Fix the production code** to make the test pass.
4. **Run the full suite.** All tests should be green. If new failures appeared, your fix introduced a regression.

**Why test first for bugs:** Writing the test first forces you to understand exactly what the bug is, not approximately what it is. It also prevents you from accidentally fixing a different problem and convincing yourself the bug is gone. And the test permanently guards against the same bug recurring.

**When a bug report arrives:**
- Start by writing a unit test that exposes the bug, not by opening the source file.
- If you need multiple tests to narrow the scope of the bug (to rule out related failures), write all of them before fixing anything.
- The unit tests become the regression suite for this bug forever.

---

## Test Adequacy Criteria

A test suite is sufficient for refactoring when it satisfies all four of these criteria:

| Criterion | What to Check |
|---|---|
| **Normal behavior covered** | Every public method has at least one test for its primary intended behavior |
| **Boundaries covered** | Each method has tests for: empty input, first/last element, value after the last, zero/null values |
| **Error paths covered** | Every documented error condition or exception has a test that verifies it is raised correctly |
| **Fast enough to run after every step** | The full suite completes in under 30 seconds. If it takes longer, it will not be run frequently enough |

**What you do not need:**
- 100% branch coverage — Fowler explicitly rejects coverage targets as the goal. The goal is testing where the risk is.
- Tests for simple accessors (getters/setters that do nothing but read/write a field) — too simple to fail.
- Tests for every combination in a class hierarchy — test each alternative independently; only test combinations where the alternatives interact in complex ways.

**Fowler's practical rule:** Test the areas you are most worried about going wrong. Concentrate effort where complexity is highest and where bugs would be hardest to find manually. It is better to run incomplete tests than to have no tests because a complete suite felt impossible to write.

---

## Key Principles

**1. Tests must be self-checking.**
Tests that print output to the console for a human to inspect are not self-checking. Every assertion must be evaluated by the framework automatically. The only acceptable output is a pass/fail signal — ideally a progress bar that turns red on failure.

**2. Tests must be fast.**
Slow tests do not get run. If the suite takes more than 30 seconds, developers will batch changes and run tests infrequently. Infrequent testing means bugs accumulate between runs, making them harder to isolate. For refactoring specifically, tests must be fast enough to run after every single atomic step.

**3. Each test must be isolated.**
A test must not depend on the results of any other test. Execution order must not matter. Use setup/teardown to ensure each test starts from an identical, known state.

**4. Verify that tests can fail.**
When you write a test, temporarily insert a wrong value into the assertion. If the test does not turn red, it is not exercising what you think. A test that cannot fail is not a test — it is false confidence.

**5. Incomplete tests beat no tests.**
The most common failure mode is paralysis: "I can't test everything perfectly, so I won't test anything." Write the tests for the risky areas first. Run them. An imperfect suite that runs frequently is vastly more valuable than a theoretically complete suite that never gets written.

**6. The compile-and-test gate is non-negotiable.**
Every atomic refactoring step ends with: compile + run suite. Red = revert. No exceptions. This is what makes refactoring safe to do in a production codebase.

---

## Examples

### Example 1: Adding tests before extracting methods from a billing class

**Situation:** You want to decompose a 200-line `calculate_invoice()` method into smaller methods but there are no tests.

**Setup fixture:** Create an `Invoice` object with known line items and tax rates.
**Normal behavior tests:** Assert that `calculate_invoice()` returns the correct total for a standard order.
**Boundary tests:** Empty order (zero line items), single item, order with a discount applied to zero-priced items.
**Error tests:** Negative quantity raises `ValueError`, unknown product code raises `KeyError`.
**Green gate:** All pass. Now decompose `calculate_invoice()` one extracted method at a time, running after each extraction.

---

### Example 2: Bug-fix variant for a reported pricing error

**Situation:** A bug report says orders over $1,000 are applying the discount twice.

**Step 1 — Write failing test:**
```python
def test_discount_applied_once_for_large_order(self):
    order = Order(items=[Item("product-A", quantity=10, unit_price=150)])  # total = $1,500
    assert order.total_price() == 1350.00  # 10% discount applied once
```
**Step 2 — Run it.** It fails (returns 1215.00 — discount applied twice). Good. The test reproduces the bug.
**Step 3 — Fix the discount logic.**
**Step 4 — Run full suite.** All green including the new test. Bug is fixed and regression-protected.

---

### Example 3: Assessing an existing test suite before a large refactoring

**Situation:** A module has 12 tests. You want to refactor its data model.

**Audit checklist:**
- [ ] Does every public method have at least one test? — Check: 3 public methods, 12 tests → appears covered
- [ ] Are boundaries tested? — Check: no test for empty input, no test for maximum collection size → gap found
- [ ] Are error paths tested? — Check: no test for invalid state transition → gap found
- [ ] Does the suite run in under 30 seconds? — Check: 4.2 seconds → acceptable

**Action:** Add boundary and error path tests. Run. Green. Now proceed with the refactoring.

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler.

## Related BookForge Skills

- `refactoring-readiness-assessment` — Assess whether code is ready to refactor
- `code-smell-diagnosis` — Identify which smells to address first
- `method-decomposition-refactoring` — Apply once this test suite is green

Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
