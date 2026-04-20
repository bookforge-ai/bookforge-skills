---
name: unit-test-quality-checker
description: "Evaluate a test suite against rigorous unit-test criteria, classify test types, and choose between fake and mock objects. Use whenever a developer asks 'are these unit tests?', 'why is my test suite slow', 'should I use mocks or fakes', 'fake vs mock', 'what's wrong with my tests', 'my tests hit the database / network / filesystem', 'how do I speed up tests', 'unit vs integration', or when reviewing a codebase's test quality. Activates for 'unit test', 'fake object', 'mock object', 'test double', 'test speed', 'test isolation', 'xUnit', 'JUnit / NUnit / CppUnit', 'slow test suite', 'flaky tests', 'test pyramid'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/unit-test-quality-checker
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [2, 3, 5]
domain: software-engineering
tags: [legacy-code, testing, unit-testing, code-quality, software-engineering]
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Test file(s) or test directory to evaluate"
  tools-required: [Read, Grep, Bash]
  tools-optional: [Glob]
  mcps-required: []
  environment: "Codebase with an existing test suite. Bash access to run tests and measure timing."
discovery:
  goal: "Produce a scored quality report of a test suite, classifying each test and recommending fake vs mock."
  tasks:
    - "Classify each test as unit / higher-level / characterization"
    - "Detect tests that disqualify as unit tests (DB, network, filesystem, env)"
    - "Measure test timing against the 1/10 second threshold"
    - "Recommend fake-vs-mock choice for substitutions"
    - "Produce an improvement plan for failing tests"
  audience:
    roles: [software-engineer, qa-engineer, tech-lead]
    experience: intermediate
  when_to_use:
    triggers:
      - "Reviewing or auditing an existing test suite"
      - "Slow or flaky test suite"
      - "Deciding between fakes and mocks for a new test"
      - "Developer confused about test boundaries"
    prerequisites: []
    not_for:
      - "Writing brand-new tests from scratch (use TDD skills)"
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

# Unit Test Quality Checker

Evaluate whether existing tests are true unit tests per Feathers' criteria, classify each test by type, assess test double choices, and produce a scored quality report with a prioritized improvement plan.

## When to Use

Use this skill when:
- A test suite is slow and you need to understand why
- You are auditing a legacy codebase's test coverage quality
- A team debates whether their "unit tests" are actually unit tests
- Someone asks "should I use a mock or a fake here?"
- Tests are flaky, hard to run locally, or require environment setup before running

Do not use this skill to write brand-new tests from scratch. For writing characterization tests, use `characterization-test-writing`. For breaking the dependencies that make tests slow, use `dependency-breaking-technique-executor`.

## Context and Input Gathering

Before beginning, confirm:

1. **Test file paths or directory** — where do the tests live? (`test/`, `src/test/`, `spec/`, etc.)
2. **Language and test framework** — JUnit, pytest, NUnit, RSpec, Vitest, Go testing, etc.
3. **Can tests be run?** — Bash access to run the full suite or individual files and measure timing?
4. **Are there known test doubles?** — Any existing fakes, mocks, stubs, or spies in the codebase?

If the user cannot run tests, timing analysis will be static (pattern-based). Flag this explicitly in the report.

## Process

### Step 1: Inventory Tests

Use Glob and Grep to enumerate test files and count individual test cases.

```
Glob: test/**/*.{java,py,ts,js,rb,cs,go}  (adapt to language)
Grep: pattern for test method/function declarations
```

Record: total test count, test framework detected, test file structure.

**Why:** You cannot classify tests you cannot see. A count also reveals whether the suite is at a scale where slow tests compound into minutes of build lag.

### Step 2: Apply the Four Exclusion Criteria

For each test file, grep for patterns that signal disqualification from unit-test status.

**The four disqualifiers — a test is NOT a unit test if it:**
1. Talks to a database
2. Communicates across a network
3. Touches the file system
4. Requires special environment setup to run (editing config files, setting env vars, starting services)

Grep patterns to run (adapt to language):

| Disqualifier | Patterns to search |
|---|---|
| Database | `DataSource`, `EntityManager`, `@Repository`, `sqlite3`, `psycopg2`, `mongoose`, `ActiveRecord`, `db.execute`, `cursor.execute` |
| Network | `HttpClient`, `requests.get`, `fetch(`, `RestTemplate`, `socket.`, `urllib`, `axios`, `WebClient` |
| Filesystem | `File(`, `open(`, `fs.readFile`, `FileInputStream`, `Path.of`, `os.path`, `tmpfile`, `shutil` |
| Env setup | `System.getenv`, `os.environ`, `process.env`, `dotenv`, `application.properties` loaded at test level, `@SpringBootTest`, `@IntegrationTest` |

For each test flagged, record: file, test name, disqualifier type, line reference.

**Why:** These four disqualifiers are concrete and checkable. A test can be logically small while still violating all four. The disqualifiers are the reason Feathers' definition diverges from the informal "small test" meaning — the exclusions exist because DB/network/FS/env dependencies make tests slow, flaky, and unable to localize failures.

### Step 3: Measure Timing

If Bash access is available, run the test suite (or a representative subset) and measure per-test timing.

```bash
# JUnit / Maven
mvn test -pl module 2>&1 | grep "Tests run"

# pytest with timing
pytest --tb=no -q --durations=20

# Jest
npx jest --verbose --testPathPattern="..."

# Go
go test ./... -v -timeout 60s 2>&1 | grep -E "^--- (PASS|FAIL)"
```

**The threshold:** Any individual test taking longer than 1/10 second (100ms) is a slow unit test. This is not a guideline — it is the definition. A test that takes 1/10 second to run IS a slow unit test.

Flag every test exceeding 100ms. For suites where aggregate time exceeds 60 seconds, flag the top-10 slowest tests as priority targets.

**Why:** Speed is not a nice-to-have quality — it is definitional. A slow test suite stops giving developers fast feedback. When tests take minutes, developers stop running them. The entire feedback loop breaks.

### Step 4: Classify Each Test

Using the exclusion results and timing data, classify each test into one of three categories:

**Unit test:** Passes all four exclusion criteria AND runs in under 100ms. Failure points to a specific, small scope of code.

**Higher-level test:** Intentionally covers interactions across multiple classes or components. May cross boundaries (DB, network, FS) by design. Slower. Useful for pinning down integration behavior when unit tests are hard to write. These are legitimate — do not demand they meet unit-test criteria. They serve a different purpose.

**Characterization test:** Written to document actual current behavior, not to prove correctness. Typically found in legacy codebases as safety nets before refactoring. Key marker: the assertion matches what the code currently does (possibly including bugs), not what it should do. Purpose: hold behavior stable while nearby code changes. Legitimate category — do not reclassify as bugs.

**Edge/unclear:** Tests that do not clearly fit the above — include in report for manual review.

**Why:** Treating all slow tests as "bad unit tests" is wrong. A higher-level test covering a checkout workflow is supposed to hit the database — that is its job. Misclassification leads to either abandoning useful tests or writing pointless unit tests for integration behavior. The classification enables the right improvement per category.

### Step 5: Evaluate Existing Test Doubles

Grep for existing fakes and mocks in the test codebase.

```
Grep: "class Fake", "Mock", "Stub", "Spy", "when(", "verify(", "mock(", "thenReturn"
```

For each test double found, assess:

**Is it a fake object or a mock object?**

A **fake object** impersonates a collaborator. It has two sides:
- A production-facing side that implements the real interface's methods
- A test-facing side with query methods the test calls after the operation (e.g., `getLastLine()`, `getLastCall()`)

Sensing is external: the test calls a query method to inspect what happened.

A **mock object** asserts conditions internally. Expectations are set before the operation, and `verify()` is called after. The assertions live inside the mock, not the test body. Most mock frameworks (Mockito, unittest.mock, RSpec doubles) implement this pattern.

**Selection recommendation:**
- Default to fake objects. They are simpler, require no framework, work in any language, and make tests easier to read.
- Use mock objects (or a mocking framework) when: (a) you are writing many similar fakes for different scenarios and the custom query-method approach becomes repetitive, or (b) you specifically need to assert that a method was called with particular arguments and call-count matters.

The rule: "Simple fake objects suffice in most situations."

**Why:** The choice is not aesthetic. Fakes externalize sensing (the test controls what to check). Mocks internalize assertions (the mock controls what matters). When fakes proliferate with repetitive query methods, mocks become the more maintainable option. But mock overuse — especially mocking everything — produces brittle tests that break on implementation changes rather than behavior changes.

### Step 6: Produce the Quality Report

Write the report artifact to `test-suite-quality-report.md` using the template in the Outputs section.

## Inputs

| Input | Required | Description |
|---|---|---|
| Test directory or file paths | Yes | Where tests live in the codebase |
| Language and test framework | Yes | For correct grep patterns and timing commands |
| Source code (for context on collaborators) | Recommended | Helps identify what test doubles are substituting |
| Ability to run tests via Bash | Optional | Required for timing data; static analysis possible without |

## Outputs

Write `test-suite-quality-report.md` to the project root (or a location the user specifies).

**Report template:**

```markdown
# Test Suite Quality Report
Generated: [date]
Test framework: [framework]
Total tests found: [N]

---

## Summary

| Category | Count | % of Total |
|---|---|---|
| Unit tests (passing all criteria) | | |
| Higher-level tests (intentional) | | |
| Characterization tests | | |
| Disqualified (claim to be unit, are not) | | |
| Unclear / needs review | | |

Slow tests (>100ms): [N]
Suite aggregate time: [Xs]

---

## Disqualification Violations

| Test | File | Disqualifier | Line | Recommendation |
|---|---|---|---|---|
| [test name] | [path] | [DB / network / FS / env] | [line] | [break dependency / reclassify] |

---

## Timing Results

| Test | Time (ms) | Category | Action |
|---|---|---|---|
| [test name] | [N]ms | [unit/higher/char] | [break dep / reclassify / ok] |

Top-10 slowest: [list]

---

## Test Double Assessment

| Double | File | Type (fake/mock) | Justified? | Recommendation |
|---|---|---|---|---|
| [name] | [path] | [fake/mock] | [yes/no] | [keep/convert/simplify] |

---

## Prioritized Improvement Plan

### High Priority (impacts speed most)
1. [Test name] — [action] — estimated gain: [Xs]

### Medium Priority (disqualification violations)
1. [Test name] — [action]

### Low Priority (reclassification / cleanup)
1. [Test name] — [action]

---

## Notes

- Higher-level tests left in place: [list with rationale]
- Characterization tests identified: [list]
- Tests requiring manual review: [list]
```

## Key Principles

1. **Speed is definitional, not optional.** A test that takes 1/10 second to run is, by definition, a slow unit test. This is not a style preference — it is the criterion that separates tests that give fast feedback from tests that do not.

2. **If it talks to DB, network, filesystem, or requires env setup, it is not a unit test.** These four disqualifiers are binary and checkable. A test violating any one of them is a higher-level test, regardless of how small or well-named it is.

3. **Fake objects first; mocks when expectations become the test.** Fakes are simpler and always available. Move to a mocking framework when writing many similar fakes or when verifying call behavior is the core assertion.

4. **Characterization tests are legitimate — do not demand they meet unit-test criteria.** They document actual behavior, not intended behavior. Classifying them as "broken unit tests" and deleting them removes the safety net before refactoring.

5. **Higher-level tests are not failures.** A test that intentionally covers an integration boundary serves a different purpose than a unit test. The improvement goal is not to eliminate all higher-level tests — it is to ensure tests that claim to be unit tests actually are, and to write unit tests for logic that currently has none.

## Examples

### Example A: JUnit Suite with Slow DB-Hitting Tests

**Situation:** A team reports their "unit test" suite of 320 tests takes 8 minutes to run. They run it rarely as a result.

**What the skill does:**
- Greps test files for `DataSource`, `@Transactional`, `EntityManager`, `JdbcTemplate` — finds 180 tests with DB patterns.
- Runs `mvn test` with `--durations` flag (or parses surefire XML) — confirms those 180 tests average 2.5 seconds each.
- Classifies: 140 tests pass all 4 exclusion criteria and run under 100ms (unit tests); 180 tests hit the DB (higher-level); remaining are unclear.
- Report shows: the 8-minute build is caused entirely by the 180 DB tests; the true unit tests run in 14 seconds.
- Improvement plan: reclassify the 180 as integration tests and move them to a separate Maven profile (`mvn test -P integration`). For the business logic inside those DB tests, extract pure computation into separate classes and add real unit tests. Use `Parameterize Constructor` or `Extract Interface` to inject a fake repository for the logic currently entangled with DB calls.

### Example B: Team Debating Fake vs Mock for a Payment Gateway

**Situation:** A team is writing tests for an `OrderService` that calls a `PaymentGateway`. Half the team wants to write a `FakePaymentGateway` class; the other half wants Mockito's `when(gateway.charge(...)).thenReturn(...)` pattern.

**What the skill does:**
- Asks: are there already multiple fake gateway implementations in the test codebase? Greps for `FakePaymentGateway`, `MockPaymentGateway`, `StubPaymentGateway` — finds none.
- Recommends: start with a fake object. Write `FakePaymentGateway implements PaymentGateway` with a `getLastChargeAmount()` query method. The test calls `orderService.submitOrder(order)`, then asserts `fakeGateway.getLastChargeAmount()` equals expected amount. No framework needed.
- Follow-up rule: if the team later writes 8 similar fake gateways (for different error scenarios, partial charge cases, etc.) and the query-method pattern becomes repetitive, then switch to Mockito's `verify()` pattern. The mock framework earns its complexity at that point.
- Key distinction for the team: fakes are better when sensing (observing what happened) is the goal; mocks are better when verifying call behavior (exactly which method was called, with which arguments, how many times) is the goal.

### Example C: Python pytest Suite with Mixed Test Types

**Situation:** A Python codebase has 95 tests in `tests/`. The team has no idea which are unit tests. Some use `requests_mock`, some use `pytest-django`, some are plain `assert` statements.

**What the skill does:**
- Globs `tests/**/*.py`, greps for: `requests`, `os.path`, `open(`, `@pytest.mark.django_db`, `client.get(`, `tmpdir`, `os.environ`.
- Classifies:
  - 40 tests with `@pytest.mark.django_db` — higher-level (DB), legitimate, leave in place.
  - 12 tests using `requests_mock` — these are unit tests (the fake intercepts network; no real network calls). Pass.
  - 8 tests using `tmpdir` (pytest fixture for temp filesystem) — examine case by case: if the business logic only needs a file path abstraction, reclassify and extract; if the test genuinely exercises file handling behavior, reclassify as higher-level.
  - 35 tests with plain `assert` on pure functions — unit tests, fast, no dependencies.
- Timing: `pytest --durations=10` reveals the `@pytest.mark.django_db` tests average 300ms; pure tests average 3ms.
- Report: 2 categories of test doubles found (`requests_mock` = mock pattern, recommended; `unittest.mock.patch` in 6 tests = mock overuse suspected — review whether patching internals is causing brittleness).

## References

- `references/unit-test-criteria.md` — full text of Feathers' two positive qualities and four exclusion criteria (Chapter 2)
- `references/fake-vs-mock-objects.md` — structural anatomy of fake objects (two sides) and mock objects (internal assertions), with selection rule (Chapter 3, Chapter 5)
- `references/test-type-taxonomy.md` — unit / higher-level / characterization taxonomy with philosophy note on "testing to detect change" vs "testing to show correctness" (Chapter 2, Chapter 13)

## License

CC-BY-SA 4.0. Derived from "Working Effectively with Legacy Code" by Michael C. Feathers (2004). Skill content is transformative — original book required for full context.

## Related BookForge Skills

- `characterization-test-writing` — once you know which tests are characterization tests (this skill classifies them), use this to write more
- `legacy-code-change-algorithm` — the master procedure for safe change; this skill's output feeds directly into Step 4 (Write Tests) of that algorithm
- `dependency-breaking-technique-executor` — when this skill identifies tests that hit DB/network/FS, that skill provides the mechanics to break those dependencies and enable true unit tests
