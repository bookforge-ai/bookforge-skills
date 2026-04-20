---
name: safe-legacy-editing-discipline
description: "Apply 4 editing disciplines when modifying legacy code: Hyperaware Editing, Single-Goal Editing, Preserve Signatures, Lean on the Compiler. Use whenever a developer is about to edit untested code, refactor without a safety net, or is caught in avoidance anti-patterns (Edit-and-Pray, Minimization Freeze, Legacy Code Dilemma paralysis). Activates for 'how do I refactor safely', 'edit legacy code without breaking it', 'preserve behavior during refactor', 'lean on the compiler', 'preserve signatures', 'single-goal editing', 'make safe changes', 'edit and pray', 'cover and modify', 'careful editing', 'refactor without tests', 'break dependencies safely', 'avoid regressions in legacy code'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/safe-legacy-editing-discipline
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [1, 23]
domain: software-engineering
tags: [legacy-code, refactoring, software-engineering, code-quality, editing-discipline]
depends-on:
  - legacy-code-change-algorithm
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: codebase
      description: "Pending change specification + current test coverage status for the target code"
  tools-required: [Read, Grep, Edit]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Codebase in any language; Lean on the Compiler discipline applies only to statically-typed languages."
discovery:
  goal: "Produce a safe-editing plan applying the 4 disciplines to a specific legacy code change."
  tasks:
    - "Determine whether a discipline applies to the editing context"
    - "Apply Hyperaware Editing for unavoidable edits without tests"
    - "Apply Single-Goal Editing to prevent scope creep mid-refactor"
    - "Apply Preserve Signatures during initial dependency-breaking"
    - "Apply Lean on the Compiler (when language allows) for discovery-driven edits"
    - "Name the anti-pattern the developer is avoiding"
  audience:
    roles: [software-engineer, backend-developer, tech-lead]
    experience: intermediate
  when_to_use:
    triggers:
      - "About to edit code that has no tests"
      - "Doing initial dependency-breaking as a bootstrap to testing"
      - "Developer wants to 'just tweak' something without a safety net"
      - "Team paralyzed by Legacy Code Dilemma or using Edit-and-Pray"
    prerequisites:
      - skill: legacy-code-change-algorithm
        why: "The disciplines apply during Steps 3 and 5 of the algorithm"
    not_for:
      - "Editing well-tested code (tests ARE the safety net)"
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

# Safe Legacy Editing Discipline

## When to Use

You are about to edit code that has no tests, or you are doing the initial dependency-breaking refactoring that must happen *before* tests can be written. These disciplines exist precisely for this window — the gap between "no tests" and "some tests."

Apply this skill when any of the following are true:

- You are about to make an edit and there are no automated tests covering the code
- You are mid-dependency-breaking and tempted to also "clean up" something you notice
- You catch yourself reasoning: "I'll just tweak it here — it's a small change"
- Your team has stopped touching code because "if it's not broke, don't fix it"
- You recognize the Edit-and-Pray pattern in your own recent work

**Relationship to the Legacy Code Change Algorithm:** These disciplines activate at Step 3 (break dependencies) and continue through Step 5 (make the change). They are the behavioral layer underneath the algorithm — the how of editing when the safety net is thin.

## Context & Input Gathering

Before producing the editing plan, gather:

| Input | How to Obtain |
|-------|---------------|
| **Target code** | Read the file(s) being changed — understand current signatures, method bodies, and call sites |
| **Planned change description** | One sentence: what will change and why |
| **Test coverage status** | Are there any tests covering this code right now? (zero / partial / good) |
| **Language** | Determines whether Lean on the Compiler is applicable (statically-typed: yes; dynamically-typed: no) |
| **Phase of work** | Initial dependency-breaking (before tests) or post-test refactoring? |

The editing plan format differs depending on phase:
- **Before first test:** All four disciplines are in play; Preserve Signatures is mandatory.
- **After tests are in place:** Hyperaware Editing and Single-Goal Editing remain; Preserve Signatures is no longer required; Lean on the Compiler is optional.

## Process

### Step 1: Classify the Editing Context

**ACTION:** Determine which phase of the Legacy Code Change Algorithm you are in.

Three contexts:
1. **Tested:** Tests exist and cover the code being changed. The tests ARE your safety net. These disciplines are supplementary, not critical.
2. **Untested — initial dependency-breaking:** You are breaking dependencies as a bootstrap to writing tests. No tests exist yet. This is the highest-risk editing context. ALL four disciplines apply.
3. **Untested — direct edit:** You are making a behavioral change directly to untested code (a bug fix, a feature). Tests do not exist. This is Edit-and-Pray territory — name the anti-pattern and recommend writing characterization tests first (invoke `legacy-code-change-algorithm` Step 4 before proceeding).

**ARTIFACT:** Record the context:
```
Editing context: [Tested / Untested-bootstrap / Untested-direct]
```

---

### Step 2: Name the Anti-Pattern to Avoid

**ACTION:** Identify which avoidance pattern is most present. This is not optional — naming the pattern makes it visible and prevents relapse.

Ask these diagnostic questions:

**Is this Edit-and-Pray?**
- "Will I verify this change by manually running the application and poking around?"
- "Am I about to trust my own memory of which paths I need to test?"
- If yes: the change needs characterization tests before it proceeds. The target mental model is Cover-and-Modify — wrap the change in tests so that any behavior change is detected automatically, not discovered by memory-guided poking.

**Is this the Legacy Code Dilemma?**
- "Do we refuse to add tests because refactoring is needed, but refuse to refactor because tests are needed?"
- "Has the team been stuck in this circularity for weeks or months?"
- If yes: conservative dependency-breaking techniques (Ch 25 catalog) break the cycle. These are safe enough to apply without tests and unlock the first test.

**Is this Minimization Freeze?**
- "Does the team decline to extract methods or create seams with 'if it's not broke, don't fix it' reasoning?"
- "Is the implicit rule 'make as few edits as possible'?"
- If yes: the reasoning is inverted. True safety requires *more* edits (to create seams and tests), not fewer. Minimizing edits without a safety net accumulates risk on every future change — methods grow, dependencies harden, and every future edit becomes more dangerous.

**ARTIFACT:** Record the anti-pattern:
```
Anti-pattern in play: [Edit-and-Pray / Legacy Code Dilemma / Minimization Freeze / None]
Diagnostic evidence: [what the developer said or planned that signals this]
```

---

### Step 3: Apply Hyperaware Editing

**ACTION:** Before making any edit, classify each planned change as behavior-changing or not.

Walk through your intended edit and label each action:

| Action | Behavior-changing? |
|--------|-------------------|
| Add/change a string literal in live code | Yes |
| Rename a local variable | No (if renamed consistently) |
| Change a numeric literal | Yes |
| Add whitespace / reformat | No |
| Add a new method call | Yes |
| Copy-paste a method signature | No (same type, same name) |
| Change a parameter type | Yes |
| Add a comment | No |

**WHY:** Every behavior-changing keystroke is a risk when tests are absent. Knowing exactly which actions change behavior lets you treat those actions with more care — run a build after them, pause and re-read, consider whether a test should exist before you make the change.

**Closing the feedback loop:** The ideal is test-driven development where you can run tests in under a second after every change. When that is not possible, use pair programming (second person watches for accidental edits) as the nearest substitute.

**ARTIFACT:** For each planned edit, annotate your change-plan.md:
```
- [action]: behavior-changing: yes/no — risk level if no tests: [low/medium/high]
```

---

### Step 4: Apply Single-Goal Editing

**ACTION:** Write down the one thing you intend to accomplish in this editing session. Then, as you work, capture every "also" item on paper instead of acting on it.

**The single goal (write this before touching the keyboard):**
```
Goal: [one sentence — e.g., "Extract the body of processOrders() into a private static method"]
```

**The "also" list (capture mid-edit, do NOT act on these):**
```
Also noticed:
- [thing 1 you want to clean up]
- [thing 2 that looks wrong but is out of scope]
```

**Enforcement pattern (when pairing):** The partner's job is to ask "What are you doing?" If the answer includes more than one thing, stop. Pick one. Return to the goal.

**Why the paper list matters:** The list prevents two failure modes:
1. Forgetting the secondary item entirely (and leaving it broken)
2. Acting on it now and losing track of the primary goal

The items on the paper list become future tasks — possibly new tickets. They are not lost; they are deferred with intention.

**ARTIFACT:** Append to change-plan.md:
```
## Single-Goal Edit
Goal: [one sentence]
Deferred items:
- [ ] [item 1]
- [ ] [item 2]
```

---

### Step 5: Apply Preserve Signatures

**ACTION:** During initial dependency-breaking (before any tests exist), never retype a method signature — always copy-paste it.

**Scope constraint — critical:** Preserve Signatures applies ONLY when you are doing initial dependency-breaking refactoring with no tests in place. It is NOT a rule for general refactoring once tests exist. When tests are in place, the tests tell you when you've mistyped a signature.

**The mechanical procedure:**
1. Copy the entire argument list from the source method into the clipboard
2. Type the new method declaration with empty parentheses
3. Paste the clipboard into the new method declaration
4. Type the call site for the new method with empty parentheses
5. Paste the clipboard into the call
6. Delete the types, leaving only argument names in the call

**What this eliminates:**
- Wrong parameter type (e.g., `int` vs `long`)
- Wrong parameter order (e.g., `rate, target` vs `target, rate`)
- Wrong variable name (e.g., `interestRate` vs `interest_rate`)
- Accidental signature "improvements" (e.g., changing a parameter to take an object when the original took a primitive)

**What Preserve Signatures does NOT mean:** You may add new methods, move code, and create new classes. You just may not change the signatures of the methods you are copying or calling while doing so.

**ARTIFACT:** Add to dependency-break-log.md:
```
- [technique name]: signatures preserved: yes — method: [ClassName.methodName(args)]
```

---

### Step 6: Apply Lean on the Compiler

**PRECONDITION:** Language must be statically typed (Java, C++, C#, Go, TypeScript, Kotlin, Rust, Swift). If the codebase uses Python, Ruby, or JavaScript: skip this step and rely on text-based search (Grep) instead.

**ACTION:** To find all locations that need updating after a declaration change, deliberately introduce a compile error by altering or removing the declaration, then let the compiler guide you to every affected location.

**Two steps:**
1. Alter the declaration to cause compile errors (e.g., comment out a global variable, change a class type to an interface, remove a method)
2. Compile; navigate to each error; make the required change

**Example (C++ global encapsulation):** Comment out `double domestic_exchange_rate;`. The compiler reports every file and line that references it. Update each reference to `exchange.domestic_exchange_rate`. Re-compile. Repeat until clean.

**The inheritance trap — do not skip this caveat:** If you comment out a method in a class and get zero compile errors, do NOT conclude the method is unused. If the method's parent class (or any ancestor) has a method with the same name and signature, the compiler will silently resolve all call sites to the parent's version. The method may have many callers — you just can't see them. This applies equally to variables and multiple inheritance hierarchies.

**Safe procedure:** Before concluding "no callers," verify whether any superclass in the hierarchy has a method with the same signature. If yes, use text search (Grep) to find callers instead.

**ARTIFACT:** Add to change-plan.md:
```
## Lean on the Compiler Plan
Declaration altered: [e.g., removed / commented out / type-changed]
Inheritance check: [verified no superclass has same signature: yes/no/N/A]
Errors found at: [list of files/lines]
```

---

### Step 7: Produce the Editing Plan Artifact

Consolidate the outputs from Steps 1–6 into a single `editing-plan.md` for the change. This is the artifact that lets you (or a reviewer) verify the disciplines were applied.

See the Outputs section for the template.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Target source file(s) | Yes | The code being modified |
| Change description | Yes | One sentence — what changes and why |
| Test coverage status | Yes | Zero tests / some tests / well-tested |
| Language | Yes | Determines Lean on the Compiler applicability |
| Phase of work | Yes | Bootstrap dependency-breaking vs. post-test change |

## Outputs

| Output | Description |
|--------|-------------|
| `editing-plan.md` | Disciplines applied, anti-pattern identified, step-by-step edit sequence with rollback points |
| Annotations in `change-plan.md` | Behavior-change classification per edit, single-goal declaration, deferred items |
| Annotations in `dependency-break-log.md` | Signatures-preserved confirmation per technique applied |

### editing-plan.md Template

```markdown
# Editing Plan

## Context
Editing context: [Tested / Untested-bootstrap / Untested-direct]
Language: [e.g., Java / C++ / Python]
Lean on the Compiler: [applicable / not applicable — reason]

## Anti-Pattern Identified
Anti-pattern: [Edit-and-Pray / Legacy Code Dilemma / Minimization Freeze / None]
Evidence: [what signaled this]
Mitigation: [what discipline or action addresses it]

## Single-Goal Edit
Goal: [one sentence]
Deferred items:
- [ ] [item 1]
- [ ] [item 2]

## Edit Sequence
For each step in the planned edit:
1. [action] — behavior-changing: yes/no — rollback point: yes/no
2. [action] — behavior-changing: yes/no — rollback point: yes/no

## Preserve Signatures
Applies: [yes / no — reason]
Methods copied (not retyped): [list]

## Lean on the Compiler
Declaration altered: [or N/A]
Inheritance check completed: [yes / no / N/A]
Errors found at: [list or N/A]

## Rollback Points
- After step [N]: compile clean, behavior unchanged
- After step [M]: compile clean, behavior unchanged
```

## Key Principles

- **Safety comes from disciplines before it comes from tests.** When tests do not yet exist, the four disciplines are the only systematic protection between you and an invisible regression. They are not a substitute for tests — they are the bridge to getting tests in place.

- **Do one thing at a time — "also" items go on paper.** The paper list is not a concession. It is a precision tool. It captures what you noticed without letting it derail what you intended, and it ensures deferred items become tracked work rather than forgotten debt.

- **Preserve Signatures during initial dependency-breaking — the machine-perfect copy is a safety net.** Retyping a parameter list introduces a class of error that tests would catch if tests existed. They do not exist yet. Copy-paste eliminates that error class entirely. Preserve Signatures is not a permanent style rule — it applies only in the pre-test window.

- **In typed languages, lean on the compiler — but beware inheritance masking.** The compiler is a trustworthy guide for finding all callers of a declaration you change. The one place it fails silently is inheritance: a superclass method with the same signature will silently absorb all call sites when the subclass method is removed. Always verify the inheritance hierarchy before concluding the compiler found all callers.

- **Name the anti-pattern you're avoiding — awareness prevents relapse.** Edit-and-Pray, Legacy Code Dilemma, and Minimization Freeze are named patterns for a reason: naming them makes them visible. A team that can say "we're in Minimization Freeze" can reason about how to exit it. A team that just has a vague feeling of avoidance cannot.

## Examples

### (a) Java developer about to add a parameter to a legacy method with no tests

**Situation:** A Java developer needs to add a `locale` parameter to a 200-line method `InvoiceFormatter.format(Invoice invoice)` that has no tests.

**Step 1 (context):** Untested-bootstrap. There are no tests. This is initial dependency-breaking work.

**Step 2 (anti-pattern):** Edit-and-Pray risk — the developer plans to add the parameter and then "test it manually by running the UI." Name the pattern and flag it.

**Step 3 (Hyperaware):** Adding a new parameter is behavior-changing. Every call site that currently compiles with one argument will break. Every place that constructs the string output may now differ. High-risk edits — note them explicitly.

**Step 4 (Single-Goal):** Write: "Goal: add `Locale locale` parameter to `format()` and thread it to the one callsite that needs it." While reading the method, the developer notices three other parameters that "should really be an object." Write them on the deferred list. Do not act on them now.

**Step 5 (Preserve Signatures):** Copy `Invoice invoice` from the current signature. Type `public String format(` then paste, add `, Locale locale)`. Do not retype. Do not reorder. Do not rename `invoice` to `inv`.

**Step 6 (Lean on the Compiler):** The compiler error list after adding the parameter reveals 7 call sites, not the 2 the developer thought existed. Update all 7 before checking inheritance (no superclass has a `format()` method — confirmed via Grep).

**Result:** The parameter is threaded through all 7 call sites. No signature mutations were introduced. 5 deferred cleanup items are on paper. The code compiles. The developer can now write a characterization test.

---

### (b) Team stuck in Minimization Freeze rationalization

**Situation:** A tech lead says: "Our core billing class has 800 lines. We can't add tests without refactoring, but we don't want to refactor because something might break. The policy is: if it's not broke, don't fix it."

**Step 2 (anti-pattern):** This is Minimization Freeze combined with Legacy Code Dilemma. Name both.

**The inversion to surface:** "It involves less editing, and it's safer" is backwards. Every future change to the 800-line class is made without any safety net. The cumulative risk grows with every undisciplined edit. True safety requires more edits (to create seams), not fewer.

**The path out of Legacy Code Dilemma:** Conservative dependency-breaking techniques (from Chapter 25) are designed specifically to be safe enough to apply without tests. They are not general refactoring — they are a bootstrap protocol. Apply one conservative technique (e.g., Parameterize Constructor), confirm it compiles, write the first test against the newly isolated code. The circularity is broken at the first test.

**Single-Goal application:** The first goal is not "clean up the billing class." It is: "break one dependency so we can write one test." Write that as the goal. Everything else is deferred.

---

### (c) C++ developer encapsulating globals via Lean on the Compiler

**Situation:** A C++ developer wants to encapsulate two global variables (`domestic_exchange_rate`, `foreign_exchange_rate`) into a class so they can be substituted in tests.

**Step 1 (context):** Untested-bootstrap. Encapsulating globals IS a dependency-breaking technique. No tests yet.

**Step 5 (Preserve Signatures):** The globals are variables, not methods. The principle still applies: the new class fields should have identical names (`domestic_exchange_rate`, `foreign_exchange_rate`), not renamed versions.

**Step 6 (Lean on the Compiler):**
1. Comment out both global variable declarations
2. Compile — 34 errors across 9 files
3. Navigate to each error; prefix the reference with `exchange.`
4. Re-compile — 0 errors

**Inheritance check:** These are global variables, not class methods. Inheritance masking does not apply. The compiler's 34 errors are the complete set of usages.

**Result:** All 34 usages updated mechanically. No manual search required. The change is ready for a characterization test of the exchange rate behavior.

## References

No supplementary reference files for this skill. The disciplines are self-contained.

Source material: Chapter 23 of Working Effectively with Legacy Code (the full chapter is dedicated to these four disciplines). Chapter 1 provides the Minimization Freeze and Edit-and-Pray context.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Working Effectively with Legacy Code by Michael C. Feathers (2004, Prentice Hall).

## Related BookForge Skills

- `legacy-code-change-algorithm` — The parent algorithm. These disciplines apply at Steps 3 and 5. IF not installed → apply the inline discipline guidance above.
- `dependency-breaking-technique-executor` — The full Chapter 25 catalog of 24 techniques. Lean on the Compiler is a sub-step within many of them. IF not installed → use the abbreviated technique descriptions in `legacy-code-change-algorithm` Step 3.
- `characterization-test-writing` — Step 4 of the algorithm: how to write tests that document current behavior. Applies after these disciplines have made the code testable. IF not installed → use the inline Step 4 guidance in `legacy-code-change-algorithm`.
