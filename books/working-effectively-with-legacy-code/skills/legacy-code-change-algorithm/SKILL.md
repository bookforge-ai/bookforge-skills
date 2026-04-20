---
name: legacy-code-change-algorithm
description: "Guide safe modification of legacy code (untested production code) using Feathers' 5-step Legacy Code Change Algorithm. Use this skill whenever a developer needs to change code that lacks test coverage — adding a feature, fixing a bug, refactoring, or optimizing — and wants to avoid regressions. Activates for 'I need to change this code but there are no tests', 'how do I safely modify legacy code', 'inherited codebase', 'untested code', 'legacy system change', 'code without tests', 'refactor without regressions', 'make this code testable', 'cover and modify', 'don't break anything', 'risky change to old code', 'no test coverage', 'adding feature to old code', 'fixing bug in untested code', 'legacy codebase change safely'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/legacy-code-change-algorithm
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [1, 2]
domain: software-engineering
tags: [legacy-code, refactoring, testing, software-engineering, technical-debt]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source code the developer needs to change + a description of the intended change"
  tools-required: [Read, Grep, Edit, Bash]
  tools-optional: [Glob]
  mcps-required: []
  environment: "A software codebase (any language) with source code accessible. Existing tests may be sparse or absent."
discovery:
  goal: "Lead a developer through the 5-step Legacy Code Change Algorithm to make a safe change to untested code."
  tasks:
    - "Classify the reason for change (feature/bug/refactor/optimize) to calibrate risk"
    - "Identify change points in the codebase"
    - "Find appropriate test points where coverage will go"
    - "Break dependencies that prevent testing"
    - "Write characterization tests before changing behavior"
    - "Make the change and refactor with continuous test feedback"
  audience:
    roles: [software-engineer, backend-developer, senior-developer, tech-lead]
    experience: intermediate
  when_to_use:
    triggers:
      - "Developer needs to change untested production code"
      - "Inherited codebase with minimal test coverage"
      - "Risk of regression on every change"
      - "Starting any legacy-code modification"
    prerequisites: []
    not_for:
      - "Well-tested greenfield code (use TDD directly)"
      - "Throwaway prototypes"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: null
    assertion_count: 12
    iterations_needed: null
---

# Legacy Code Change Algorithm

## When to Use

You are about to change code that has little or no test coverage. The code may be code you wrote, code you inherited, or code that was written before the team adopted testing practices. Any of these situations apply:

- You need to add a feature but can't easily write tests because of dependencies
- You need to fix a bug in an area with no tests, and you're afraid of regressions
- You need to refactor or optimize but can't tell whether your changes preserve behavior
- You just opened a file, it's tangled with dependencies, and you don't know where to start

Before executing this skill, verify:
1. You have read access to the relevant source files
2. You can run the test suite (or a subset of it) — even if it's empty right now
3. You have a clear description of the change you need to make (even one sentence is enough to start)

If the test suite cannot run at all (build is broken), resolve that first. This algorithm assumes you can get to a green baseline, even if it's zero tests.

## Context & Input Gathering

### Input Sufficiency Check

Before executing, determine: "Do I have enough context to identify the change?"

### Required Context (must have — ask if missing)

- **Change description:** A one-sentence description of what must change and why.
  -> Check prompt for: "I need to", "add X", "fix Y", "change Z"
  -> If still missing, ask: "What exactly needs to change, and what behavior should it produce after the change?"

- **Entry point in codebase:** The file(s) or class(es) where the change will happen.
  -> Check prompt for: file names, class names, method names
  -> Check environment for: matching files via Grep/Glob on mentioned names
  -> If still missing, ask: "Which file or class is the starting point for this change?"

### Observable Context (gather from environment)

- **Test suite status:** Are there any existing tests? Which test runner?
  -> Look for: `test/`, `tests/`, `spec/`, `*Test.java`, `*_test.py`, `*.test.ts`, `pytest.ini`, `build.gradle`, `package.json` scripts section
  -> If no tests found: default to "starting from zero tests"

- **Language and build system:** Determines which dependency-breaking techniques are available.
  -> Look for: file extensions, `pom.xml`, `Makefile`, `package.json`, `requirements.txt`, `go.mod`
  -> If unavailable: note "language unknown" and proceed — the algorithm is language-agnostic

- **Dependency profile:** Does the code under change have constructor dependencies, global state, or direct I/O?
  -> Look for: `new DatabaseConnection()`, `Singleton.getInstance()`, `System.out`, direct file reads in the target file
  -> Default: assume dependencies exist until proven otherwise

### Default Assumptions

- **No tests exist yet:** The algorithm works whether zero or some tests are present.
- **OO language:** Default to object seam-based dependency-breaking techniques; adjust if procedural language detected.
- **Unit test framework is available or installable:** If no framework exists, note it and recommend one before Step 4.

### Sufficiency Threshold

SUFFICIENT: Change description known + entry point file(s) identified + can run build command (even if no tests)
PROCEED WITH DEFAULTS: Change description known + rough area of codebase known
MUST ASK: Change goal is entirely unknown — cannot proceed without user input

## Process

### Step 0: Classify the Change Type

**ACTION:** Read the change description and classify it into one of four types: (A) adding a feature, (B) fixing a bug, (C) refactoring (improving design), or (D) optimizing (improving performance/resource use).

**WHY:** The change type determines your safety posture. Feature addition and bug-fixing both alter behavior — you must write tests that verify the new behavior plus tests that preserve existing behavior. Refactoring and optimization must not change behavior at all — every test you write should still pass before and after. Knowing the type up front prevents you from accidentally testing the wrong thing or under-testing the right thing.

**IF** the change is a refactor or optimization -> your single constraint is "all behavior must be identical after the change." Set a mental flag: zero behavioral change permitted.
**IF** the change is a feature addition -> identify the new behavior you want to add. The old behavior is off-limits for modification (unless the requirement explicitly says otherwise).
**IF** the change is a bug fix -> identify the one slice of behavior that is wrong and needs to change. Everything else is off-limits.
**IF** the intent is ambiguous -> default to "feature addition" (safest posture). Ask for clarification in parallel.

**ARTIFACT:** Write a one-sentence declaration:
> "This is a [feature addition / bug fix / refactor / optimization]: [change description]."

Save this as the header of `change-plan.md`.

---

### Step 1: Identify Change Points

**ACTION:** Locate the specific files, classes, and methods that will need to be modified to implement the change. Trace from the entry point outward using Grep and Read. Document each change point by file path + method/function name.

**WHY:** You cannot write effective tests or plan dependency-breaking until you know exactly where the code will change. "Change points" are the precise locations — not the entire module or service. Precision here prevents over-testing (wasting time on code that won't change) and under-testing (missing code that will).

**HOW:**
1. Start with the file or class named in the change description.
2. Use Grep to find the method(s) that must change. Read their bodies.
3. For each method that must change, note whether it calls other methods that will also need to change (ripple analysis — keep it shallow at this step).
4. Stop when you have a clear list of the specific methods that will be modified.

**IF** the codebase is very large and you can't find the right location -> invoke `legacy-code-symptom-router` or use scratch refactoring (Chapter 16) to explore before committing.
**IF** the architecture is clear and the change point is obvious -> proceed immediately.

**ARTIFACT:** Append to `change-plan.md`:
```
## Change Points
- [file:line] [ClassName.methodName] — reason: [why this changes]
- [file:line] [ClassName.methodName] — reason: [why this changes]
```

---

### Step 2: Find Test Points

**ACTION:** For each change point identified in Step 1, determine where tests can be placed to detect both correct new behavior (for feature/bug) and regressions (for all types). Trace the effect of the change outward to find interception points where test assertions are both meaningful and achievable.

**WHY:** Test points are not the same as change points. The method you change may be deep inside a dependency chain; you may need to test it from a calling method one level up, or from a public interface that routes to it. The goal is to find the narrowest entry point that (a) you can exercise from a test harness and (b) will fail detectably if the change has an unintended side effect.

**HOW:**
1. For each change point, ask: "Can I call this method from a test harness right now?"
   - If yes: it is its own test point.
   - If no: trace upward to the nearest callable method that exercises it.
2. Look for a "pinch point" (a single method whose test coverage protects many of the change points simultaneously) — use this when testing many dependent methods individually would be prohibitive.
3. Document each test point with the specific assertion that will pass/fail.

**IF** test harness construction is blocked (class cannot be instantiated in tests) -> this is a dependency problem. Note it and proceed to Step 3.
**IF** you cannot find any reachable test point -> invoke `test-harness-entry-diagnostics` for the 4-category triage.

**ARTIFACT:** Append to `change-plan.md`:
```
## Test Points
- [ClassName.testableMethod] — covers change points: [...] — assertion: [what the test will assert]
- NOTE: [ClassName] cannot be instantiated in harness because: [reason] — dependency-breaking needed
```

---

### Step 3: Break Dependencies

**ACTION:** For each dependency that blocks test harness construction (identified in Step 2), apply a conservative dependency-breaking technique to make the code testable. Work without tests at this stage — apply strict safety constraints: Preserve Signatures (copy-paste method signatures exactly, no creative changes), Single-Goal Editing (one change at a time, note others for later), and use the compiler as your safety net.

**WHY:** This is the step most people skip, and it is why legacy code stays untestable. Dependencies — hardcoded constructor calls, global singletons, direct I/O, tightly coupled classes — make it structurally impossible to instantiate objects in isolation. Before you can write any test, you need a seam (a place where you can alter behavior without editing in place). Breaking dependencies creates seams. The reason to be conservative here is that you are refactoring without tests: every change carries risk of introducing a bug. Minimizing what you change minimizes that risk.

**HOW:**
1. Identify the specific dependency blocking testability (a concrete class instantiated with `new`, a singleton, a global variable, a direct DB call).
2. Choose the appropriate technique based on the dependency type and language:
   - Constructor depends on a hard-to-create object → Parameterize Constructor
   - Method creates objects internally → Parameterize Method or Extract and Override Factory Method
   - Class has a singleton/global dependency → Introduce Static Setter or Replace Global Reference with Getter
   - Interface does not exist but is needed → Extract Interface
   - Method cannot be called in isolation → Subclass and Override Method
   - (For the full 24-technique catalog, invoke `dependency-breaking-technique-executor`)
3. Apply the technique mechanically. Do not improve the design simultaneously — that is a separate goal for Step 5.
4. Run a build (or compile) after each technique to confirm nothing broke.

**IF** the change required multiple dependency breaks, apply them one at a time, verifying compile between each.
**IF** a dependency-breaking change itself looks risky -> document it in the log and consider Lean on the Compiler (deliberately introduce a type error to let the compiler find all affected locations).

**ARTIFACT:** Create `dependency-break-log.md`:
```
## Dependency Breaks Applied
1. [Technique name]: [what changed] — file: [path] — Signatures preserved: yes
2. [Technique name]: [what changed] — file: [path] — Signatures preserved: yes
```

---

### Step 4: Write Tests

**ACTION:** Write characterization tests (tests that document the actual current behavior of the code, not what it should do) for the test points identified in Step 2. Use the test harness you have now made accessible via Step 3. Run the tests. They must pass on the current (unchanged) code before you proceed.

**WHY:** Characterization tests are written to detect change — not to find bugs. Their purpose is to act as a vise: they lock existing behavior in place so that Step 5 changes only what you intend. If you discover a bug while writing characterization tests, document it but do not fix it now (fixing it would be a behavior change you haven't planned for, and it would make the test suite misleading). The rule is: "What the system does is more important than what it is supposed to do" — at this stage. You are building your safety net, not auditing correctness.

**HOW:**
1. For each test point, write a test that calls the method with realistic inputs.
2. If you don't know what value the method should return, use this technique: write an assertion you know is wrong (e.g., `assertEquals("", result)`), run the test, and let the failure message tell you the actual value. Then update the assertion to match the actual value.
3. Run all tests. They must pass.
4. If the change type is a feature addition or bug fix, also write the test(s) for the new behavior now (they will fail — that's intentional, you haven't made the change yet).

**IF** tests are hard to write because the methods have side effects (DB writes, network calls) -> go back to Step 3 and break those dependencies too.
**IF** you discover the code does something obviously wrong while writing tests -> document it; do not change behavior until Step 5, and only if it's within scope of the current change.
**IF** you are adding a feature or fixing a bug -> the new-behavior test should fail at the end of this step (you haven't implemented the change yet).

**ARTIFACT:** A passing test suite that characterizes current behavior, plus (for feature/bug changes) one or more failing tests that describe the target behavior.

---

### Step 5: Make the Change and Refactor

**ACTION:** With tests in place, implement the change. Run tests after every small edit. When all target-behavior tests pass and no characterization tests regress, the change is done. Then — and only then — refactor the code you touched to improve its structure.

**WHY:** The sequence matters: change first, then refactor. If you interleave them, a test failure won't tell you which caused the regression. Running tests after every small edit keeps the feedback loop tight (ideally under 10 seconds for the local subset). Refactoring after the change is what makes the codebase progressively better — you are not leaving legacy code worse than you found it, you are leaving it with tests and cleaner structure in the area you touched.

**HOW:**
1. Implement the change (add/modify only the code required by the change description).
2. Run tests. Fix failures immediately — do not proceed to the next edit while a test is failing.
3. Once all tests pass (including new behavior tests for feature/bug changes), review the code you touched.
4. Apply refactoring to improve structure: extract methods, rename variables, simplify conditionals. Run tests after each refactoring.
5. Commit with a descriptive message that references the change type and what tests were added.

**IF** a characterization test fails during Step 5 -> stop. This is a regression. Roll back the last edit and try a smaller step.
**IF** the code is too tangled to refactor safely now -> leave it. Document a follow-up ticket. The tests are in place; future work is safer.
**IF** you want to apply TDD for the feature implementation -> the failing tests from Step 4 are your red state; proceed with the red-green-refactor cycle.

**ARTIFACT:** Committed code with all tests passing, including at least one new test per changed behavior.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Source code files | Yes | The legacy codebase, readable via the file system |
| Change description | Yes | What the developer needs the code to do after the change |
| Test runner command | Recommended | How to execute the test suite (e.g., `pytest`, `./gradlew test`, `npm test`) |
| Existing tests (if any) | Optional | Current test suite — algorithm works with zero tests |

## Outputs

All outputs are written to the working directory unless a specific path is provided.

| Output | Description |
|--------|-------------|
| `change-plan.md` | Running document capturing change type, change points, and test points |
| `dependency-break-log.md` | Record of each dependency-breaking technique applied |
| New or modified source files | The actual change implementation |
| New test files | Characterization tests + new-behavior tests |

### change-plan.md Template

```markdown
# Change Plan

## Change Classification
Type: [feature addition | bug fix | refactor | optimization]
Description: [one sentence]
Safety posture: [behavioral change expected: yes/no | behavioral change permitted: yes/no]

## Change Points
- [file:line] [ClassName.methodName] — [why it changes]

## Test Points
- [ClassName.testableMethod] — covers: [...] — assertion: [what fails on regression]
- BLOCKED: [ClassName] needs dependency breaking because: [reason]

## Status
- [ ] Step 0: Change classified
- [ ] Step 1: Change points identified
- [ ] Step 2: Test points identified
- [ ] Step 3: Dependencies broken
- [ ] Step 4: Tests written and passing on current behavior
- [ ] Step 5: Change implemented, all tests passing
```

## Key Principles

- **Cover and Modify, not Edit and Pray.** Edit and Pray (carefully plan, then change, then poke around) feels professional but provides no systematic safety — care alone is not a substitute for a feedback mechanism. Cover and Modify wraps the change in tests that detect any unintended effect automatically. WHY: without test coverage, every change is a bet that you haven't missed an edge case. With coverage, regressions surface in seconds.

- **Change type determines safety posture.** Refactoring and optimization must produce zero behavioral change. Feature addition and bug-fixing produce intentional behavioral change that must be verified by tests. Conflating these types — for example, refactoring while fixing a bug in the same commit — removes your ability to tell which change caused a test failure. WHY: keeping change types separate makes failures diagnostic rather than confusing.

- **Step 3 (break dependencies) comes before Step 4 (write tests) — not after.** This ordering resolves the Legacy Code Dilemma: "when we change code, we should have tests in place; to put tests in place, we often have to change code." The algorithm breaks the cycle by permitting conservative, pre-test dependency-breaking refactorings. Dependencies often make it structurally impossible to call code from a test harness — you cannot write a test for a class that won't compile in isolation. WHY: attempting tests before dependency-breaking wastes time writing tests against unreachable code and demoralizes developers.

- **Every dependency break must be conservative: Preserve Signatures, Single-Goal Editing.** When breaking dependencies without tests, every unnecessary change is an opportunity to introduce a bug. Preserve Signatures means copy-pasting method signatures verbatim — no renaming, no reformatting, no "while I'm here" improvements. Single-Goal Editing means completing each dependency-breaking refactoring fully before starting the next one. WHY: these constraints trade speed for safety in the window between "no tests" and "some tests."

- **Every step produces a reversible intermediate artifact.** change-plan.md, dependency-break-log.md, and a passing test suite are all checkpoints. If Step 5 produces an unexpected regression, you can roll back to the last green test state and try a smaller step. WHY: artifacts make the process auditable and make rollback decisions trivial — you always know exactly what was done and what the last known-good state was.

## Examples

**Scenario: Adding retry logic to a Java order-processing method with a remote billing API dependency**

Trigger: "I inherited a Java microservice with no tests. I need to add retry logic to the order-processing method. It calls a remote billing API synchronously."

Process:
- Step 0: Feature addition. Behavioral change expected (new retry behavior). Existing behavior must be preserved.
- Step 1: `OrderProcessor.process()` calls `BillingApiClient.charge()` directly via `new BillingApiClient()`. Change point: `process()`.
- Step 2: `process()` is public and takes an `Order` object. Test point: call it directly. Blocked: `BillingApiClient` is a concrete class with a live network connection.
- Step 3: Apply Extract Interface to `BillingApiClient` → create `IBillingClient`. Apply Parameterize Constructor to `OrderProcessor` to accept an `IBillingClient`. Build passes.
- Step 4: Write `FakeBillingClient` implementing `IBillingClient`. Write characterization test verifying that `process()` calls `charge()` exactly once on a successful order. Tests pass. Write failing test: `process()` retries up to 3 times when `charge()` throws `TransientException`.
- Step 5: Implement retry loop. Run tests after each iteration of the loop. All tests pass. Refactor retry loop into a helper method.

Output: `OrderProcessor` now has retry logic, a `FakeBillingClient` test double, two new tests, and an `IBillingClient` interface that future tests can reuse.

---

**Scenario: Fixing a null pointer bug in a C++ legacy module with no test harness**

Trigger: "Production keeps crashing with a null dereference in `ConfigLoader::resolve()`. No tests exist. The class uses global state."

Process:
- Step 0: Bug fix. One specific behavior changes (null is handled). All other behavior preserved.
- Step 1: `ConfigLoader::resolve()` reads from a global `ConfigStore*`. Change point: the null check path inside `resolve()`.
- Step 2: `resolve()` is a member function of `ConfigLoader`. Test point: call it directly. Blocked: `ConfigStore` is a global pointer initialized at startup, cannot be replaced in test.
- Step 3: Apply Encapsulate Global References to wrap `ConfigStore*` in a class. Apply Replace Global Reference with Getter in `ConfigLoader` — override the getter in a test subclass to return a fake `ConfigStore`.
- Step 4: Write characterization test confirming `resolve()` returns the current value when `ConfigStore` is populated. Write failing test: `resolve()` returns a default value when `ConfigStore` is null.
- Step 5: Add the null guard. All tests pass.

Output: Bug fixed with test coverage, no regressions, global state encapsulated.

---

**Scenario: Optimizing a Python query function in a monolith**

Trigger: "This function runs a database query that's taking 4 seconds. I want to add query-result caching. Nothing has tests."

Process:
- Step 0: Optimization. Functionality must be identical after. Zero behavioral change permitted.
- Step 1: `ReportService.fetch_report()` queries the DB directly. Change point: the query call.
- Step 2: Test point: `fetch_report()` can be called if the DB dependency is broken. Blocked: `psycopg2.connect()` called at module level.
- Step 3: Apply Parameterize Constructor — pass `db_conn` as a parameter instead of creating it internally. Create `FakeDbConn` that returns fixture data.
- Step 4: Write characterization tests pinning the return value for several known inputs. All must pass before and after the optimization.
- Step 5: Add caching layer (`lru_cache` or a dict-based cache). Run characterization tests — they pass (same values returned). Note: cache eviction policy is out of scope for this change.

Output: Caching added, behavior preserved and verified, no regression.

## References

No supplementary reference files for this skill. The algorithm is self-contained.

For deeper sub-procedures invoked at specific steps, see the Related BookForge Skills section below.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Working Effectively with Legacy Code by Michael C. Feathers (2004, Prentice Hall).

## Related BookForge Skills

These skills handle specific sub-procedures invoked at steps of this algorithm:

- `legacy-code-symptom-router` — Step 1: when you don't know where your change point is; routes you to the relevant Part II chapter for your situation. IF not installed → ask the user to describe their situation and apply the 19-symptom routing from Part II manually.
- `test-harness-entry-diagnostics` — Step 2/3: when a class cannot be instantiated in a test harness; 4-category diagnostic triage. IF not installed → ask: "What happens when you try to construct this class in a test?"
- `characterization-test-writing` — Step 4: the 5-step characterization test algorithm in detail. IF not installed → use the inline Step 4 guidance above (write a failing assertion, let the failure tell you the actual value, update the test).
- `safe-legacy-editing-discipline` — Step 3: the 4 safety constraints for editing without tests (Hyperaware Editing, Single-Goal Editing, Preserve Signatures, Lean on the Compiler). IF not installed → apply the constraints described in Step 3 above.
- `dependency-breaking-technique-executor` — Step 3: the full catalog of 24 dependency-breaking techniques with step-by-step mechanics and language guidance. IF not installed → use the abbreviated technique descriptions in Step 3 above and refer to Chapter 25 of the source book.

Install the full book skill set from GitHub: [bookforge-skills — working-effectively-with-legacy-code](https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code)
