---
name: legacy-code-symptom-router
description: "Diagnose any legacy-code situation in plain language and route to the right technique. Use as the FIRST skill when a developer has a vague or specific complaint about a codebase — 'I have to change this but there are no tests', 'this method is huge', 'can't test this class', 'library is killing us', 'changes take forever', 'don't know where to start', 'overwhelmed', 'inherited this mess'. Activates for 'legacy code', 'untested code', 'where do I start', 'what should I do with this code', 'help me plan a refactor', 'I'm stuck with legacy', 'how do I change X safely', 'symptom triage'. Dispatches to technique-specific skills."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/legacy-code-symptom-router
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24]
domain: software-engineering
tags: [legacy-code, refactoring, testing, software-engineering, code-quality, diagnostic]
depends-on:
  - legacy-code-change-algorithm
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: description
      description: "Developer's plain-language description of their situation + optional pointer to the code in question"
  tools-required: [Read, Grep]
  tools-optional: [Glob]
  mcps-required: []
  environment: "A codebase (any language) the developer is working on. This skill is primarily reasoning over descriptions; code access is helpful but not required."
discovery:
  goal: "Match a developer's situation to the right technique and downstream skill in under 2 minutes."
  tasks:
    - "Elicit a clear symptom description"
    - "Match to one of 19 symptom chapters"
    - "Identify root cause category (time pressure / testability / design / comprehension / morale)"
    - "Recommend the downstream skill(s) with rationale"
    - "Provide a brief technique preview so the developer knows what to expect"
    - "Produce a written triage artifact (triage.md)"
  audience:
    roles: [software-engineer, backend-developer, tech-lead, engineering-manager]
    experience: any
  when_to_use:
    triggers:
      - "Developer has a problem with legacy code but doesn't know the right technique"
      - "Team needs to plan a legacy-code modification and doesn't know where to start"
      - "Unfamiliar codebase work — inherited code, onboarding to new system"
    prerequisites: []
    not_for:
      - "Developer already knows the specific technique needed — go directly to that skill"
      - "Greenfield code with test coverage in place — use TDD directly"
  environment:
    codebase_required: false
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 14
    iterations_needed: null
---

# Legacy Code Symptom Router

## When to Use

You have legacy code (code without tests, or with very few tests) and you need to change it, understand it, or improve it — but you are not sure which technique applies. You may be feeling one of these:

- "I don't know where to start with this codebase."
- "I need to add a feature but there are no tests."
- "I can't get this class to compile in a test."
- "This method is enormous and I can't write tests for it."
- "We keep changing the same code in 20 places."
- "Our builds take forever."
- "We feel overwhelmed. It's never going to get better."

This skill takes your situation in plain language and matches it to one of the 19 symptom chapters in Part II of *Working Effectively with Legacy Code* (Feathers, 2004). Each chapter maps to a downstream skill with the specific technique you need.

**Use this skill BEFORE any other skill in this set**, unless you already know the technique. The outer procedure is always `legacy-code-change-algorithm`; this skill tells you which sub-procedure to invoke.

## Context & Input Gathering

### What This Skill Needs

The only required input is a plain-language description of the situation in the developer's own words.

Helpful additional context (ask if not provided):

- **Language and environment:** Is this Java, C#, Python, C++, JavaScript, or something else? Non-OO languages (C, procedural) have a different technique set.
- **Test status:** Are there any tests at all? Does the test suite run? (Even "zero tests but builds" is a usable baseline.)
- **The specific obstacle:** What exactly isn't working? Can't compile the class in a test? Can't understand the code? Builds are too slow? Method is too large?
- **Time constraints:** Is there a deadline forcing a shortcut approach?

### When to Ask vs Infer

If the developer's description maps unambiguously to one symptom (e.g., "500-line method"), proceed to classification without asking. If the description is ambiguous between two symptoms (e.g., "everything takes forever" could be comprehension lag or build lag), ask the one diagnostic question that distinguishes them.

## Process

### Step 1: Elicit the Symptom

Ask the developer to describe their situation in plain language. If they have given you a description already, extract the core symptom phrase — the thing that feels wrong.

**If the description is vague**, ask one targeted question from this list:

- "Where is the time going — figuring out what to change, or waiting for the build after you change it?"
- "When you try to write a test for this class, what happens — compile error, runtime error, or you just can't see the output?"
- "Is the problem one specific method/class, or is it a pattern spread across many files?"
- "Do you know what the code is supposed to do, or is the behavior itself a mystery?"
- "Is there a time constraint (deadline, production issue) forcing a shortcut?"

### Step 2: Classify the Symptom

Match the description to one of the 19 symptom categories below. The full routing table with technique details is in `references/symptom-routing-table.md`. Use the quick-reference summary here to classify.

**19 Symptoms — Quick Reference**

| # | Plain-Language Symptom | Chapter | Root Cause | Downstream Skill |
|---|---|---|---|---|
| 1 | "I have no time and must change it now" | Ch 6 | Time pressure | `legacy-code-addition-techniques` |
| 2 | "Changes take forever" | Ch 7 | Lag: build or comprehension | `scratch-refactoring-for-code-understanding` (comprehension) or `dependency-breaking-technique-executor` (build) |
| 3 | "How do I add a feature?" | Ch 8 | Feature addition with tests | `tdd-and-programming-by-difference` |
| 4 | "Can't get this class into a test harness" | Ch 9 | Class testability | `test-harness-entry-diagnostics` |
| 5 | "Can't run this method in a test harness" | Ch 10 | Method testability | `test-harness-entry-diagnostics` |
| 6 | "What methods should I test?" | Ch 11 | Effect radius unknown | `change-effect-analysis` |
| 7 | "Many changes in one area" | Ch 12 | Multi-class change cluster | `change-effect-analysis` (pinch points) |
| 8 | "Don't know what tests to write" | Ch 13 | Behavior unknown | `characterization-test-writing` |
| 9 | "Library dependencies are killing me" | Ch 14 | Library coupling | `library-seam-wrapper` |
| 10 | "My app is all API calls" | Ch 15 | API coupling | `library-seam-wrapper` |
| 11 | "Don't understand code well enough to change it" | Ch 16 | Comprehension failure | `scratch-refactoring-for-code-understanding` |
| 12 | "App has no structure" | Ch 17 | Architectural opacity | `scratch-refactoring-for-code-understanding` + `big-class-responsibility-extraction` |
| 13 | "Test code is in the way" | Ch 18 | Test organization | `unit-test-quality-checker` + conventions |
| 14 | "Not object oriented" | Ch 19 | No OO seams | `dependency-breaking-technique-executor` (link/procedural techniques) |
| 15 | "Class is too big" | Ch 20 | SRP violation | `big-class-responsibility-extraction` |
| 16 | "Changing same code all over the place" | Ch 21 | Duplication | `duplication-removal-via-extraction` |
| 17 | "Monster method" | Ch 22 | Method too large to test | `monster-method-decomposition` |
| 18 | "How do I know I'm not breaking anything?" | Ch 23 | No safety net | `safe-legacy-editing-discipline` + `characterization-test-writing` |
| 19 | "We feel overwhelmed" | Ch 24 | Morale / no procedure | `legacy-code-change-algorithm` (start here) |

**Confirm with the developer:** "I'm reading your situation as: [symptom summary]. Does that match what you're experiencing?" If yes, proceed. If no, ask the diagnostic question that disambiguates.

### Step 3: Identify Root Cause Category

Classify the root cause into one of five categories. This shapes the technique approach:

- **Time pressure** (Symptom 1): Cannot do the full safe-change cycle. Use addition-without-modification techniques.
- **Testability** (Symptoms 4, 5): Something structural prevents testing. Need dependency-breaking before any tests can be written.
- **Design** (Symptoms 15, 16, 17): The code's structure is the obstacle. Need extraction and decomposition.
- **Comprehension** (Symptoms 11, 12): The developer cannot understand the code. Need a throwaway understanding technique before technique application.
- **Morale / Strategy** (Symptom 19): The obstacle is not technical — it's a lack of procedure. Install the algorithm.

Some symptoms span categories (Symptom 2 = build lag OR comprehension lag; Symptom 18 = safety discipline AND characterization tests). Where two root causes apply, identify the primary one to address first.

### Step 4: Dispatch to Downstream Skill

Recommend the downstream skill by name with a 1-paragraph preview of what the developer should expect. See `references/symptom-routing-table.md` for full technique previews for each symptom.

Provide:
1. The downstream skill name (from the table above)
2. A one-sentence description of what that skill will do
3. Any prerequisite steps to complete first (e.g., "run seam-type-selector before dependency-breaking-technique-executor if you're in a non-OO language")
4. An explicit fallback: "If that skill is not installed, here is what to do manually: [one sentence]"

### Step 5: Produce the Triage Artifact

Write a `triage.md` file in the working directory capturing the session output.

See triage.md template in the Outputs section below.

## Inputs

| Input | Required | Description |
|---|---|---|
| Developer's symptom description | Yes | Plain-language description of what is wrong or difficult |
| Language / runtime | Recommended | Determines which seam types and techniques apply |
| Test suite status | Recommended | Whether any tests exist and whether they run |
| Specific code pointer (file, class, method) | Optional | Narrows classification for ambiguous symptoms |

## Outputs

| Output | Description |
|---|---|
| `triage.md` | Written triage record: symptom, chapter match, recommended skill, rationale, fallback |
| Verbal recommendation | Immediate dispatch with 1-paragraph technique preview |

### triage.md Template

```markdown
# Legacy Code Triage

## Symptom
[Developer's description in their own words]

## Symptom Category
[Symptom number] — [Chapter title] (Chapter [N], Part II)
Root cause: [time pressure / testability / design / comprehension / morale]

## Recommended Skill
`[skill-name]`

## Rationale
[1-2 sentences: why this symptom maps to this skill, what the skill does]

## What to Expect
[1 paragraph: brief preview of the technique the developer is about to use]

## Prerequisites
[Any skills to run first, or "none"]

## Fallback (if skill not installed)
[One sentence: what to do manually without the skill]

## Related Symptoms
[Other symptoms that may also be relevant, with chapter references]
```

## Key Principles

**The book's 19 Part II chapters ARE the decision tree — respect the taxonomy.** Feathers organized the book explicitly as symptom → technique. The chapter titles are the decision branches. Each chapter was written to answer a single real developer question. Treating this as an arbitrary classification and rerouting arbitrarily loses the structural knowledge in the book's architecture.

**Route by symptom, not by technique.** Developers experiencing legacy code problems cannot name the technique they need — that is why they need routing. A developer says "I can't understand this code" and needs to be routed to scratch refactoring; they do not say "I need scratch refactoring." The symptom description is the input; the technique is the output. Never ask "which technique do you want?" — that inverts the skill.

**Some symptoms have multiple legitimate routes — let the developer choose.** Symptom 2 (changes take forever) has two root causes with different solutions. Symptom 18 (fear of breaking things) has two applicable skills. When a symptom branches, name both routes, explain the key diagnostic question that separates them, and let the developer identify which applies. Do not pick for them.

**When in doubt, route to `legacy-code-change-algorithm` as the outer procedure.** If the symptom is vague, if the developer is overwhelmed, or if no specific chapter match is clear, start the 5-step Legacy Code Change Algorithm. It is the master procedure. Every other skill is a sub-procedure that plugs into one of its five steps. Starting the algorithm always surfaces the specific symptom on the first step that blocks progress.

## Examples

### Example A: "My class won't instantiate in the test" → Test Harness Diagnostics

**Developer input:** "I'm trying to write a unit test for `InvoiceCalculator`. When I try to instantiate it in my test, I get a compile error because the constructor requires a live `DatabaseConnection` object. I can't create one of those in tests."

**Classification:** Symptom 4 — "I Can't Get This Class into a Test Harness" (Ch 9). Root cause: testability obstacle — constructor has a hard dependency on a concrete class.

**Recommendation:** Run `test-harness-entry-diagnostics`. It will walk through the 7-case triage from Chapter 9. In this case the pattern is "Irritating Parameter" (constructor requires a hard-to-create object) — the solution is either Extract Interface on `DatabaseConnection` and Parameterize Constructor, or pass null if `InvoiceCalculator` has logic to check for it.

**Triage entry:**
```
Symptom: Constructor requires a live DatabaseConnection
Chapter: Ch 9 — I Can't Get This Class into a Test Harness
Root cause: testability — class-level obstacle
Recommended skill: test-harness-entry-diagnostics
Fallback: Apply Parameterize Constructor manually (pass a DatabaseConnection interface instead of creating it in the constructor)
```

---

### Example B: "500-line method I can't write tests for" → Monster Method Decomposition

**Developer input:** "We have a `processOrder()` method that's 600 lines. It handles everything: validation, pricing, inventory, notifications. I can't test it because it's too big — I don't know what inputs to use or what assertions to write. And it's tangled — calls methods all over the class."

**Classification:** Symptom 17 — "I Need to Change a Monster Method and I Can't Write Tests for It" (Ch 22). Root cause: design — method too large to test.

**Recommendation:** Run `monster-method-decomposition`. First classify the method type: is it Bulleted (sequential chunks with low indentation between logical sections) or Snarled (dominated by one deeply nested block)? From the description, this sounds Bulleted (validation, then pricing, then inventory, then notifications = sequential chunks). The strategy is Find Sequences: identify the overarching sequence of operations, then extract each operation to a named method, working from smallest chunks outward. Use automated refactoring only — no manual copy-paste.

**Triage entry:**
```
Symptom: 600-line processOrder() method, too complex to test
Chapter: Ch 22 — I Need to Change a Monster Method
Root cause: design — method too large, no seam to test individual operations
Recommended skill: monster-method-decomposition
Fallback: Classify as Bulleted or Snarled, then extract the smallest identifiable chunk first using automated Extract Method
```

---

### Example C: "Our builds take 40 seconds, changes are painful" → Dependency Breaking for Build Speed

**Developer input:** "Any time we change a file in our core library, we have to recompile everything. A 40-second wait every change. It's killing our velocity. We don't know which parts of the build depend on which others."

**Classification:** Symptom 2 — "It Takes Forever to Make a Change" (Ch 7), specifically the **build lag** variant (not comprehension lag — they know what to change, they're just waiting for builds).

**Diagnostic question asked:** "Are you spending time figuring out WHAT to change, or waiting for the build after you've already changed it?" Developer said: "I know exactly what to change — I'm just waiting for the build."

**Recommendation:** Run `dependency-breaking-technique-executor` targeting the inter-module dependency structure. The goal is to break compilation dependencies between the core library and its consumers so a change to one area does not force recompilation of everything. Feathers' target: isolated class/module compilation + test run in under 10 seconds. Technique likely needed: Extract Interface to decouple consumers from the concrete class, allowing separate compilation.

**Triage entry:**
```
Symptom: 40-second builds on every change to core library
Chapter: Ch 7 — It Takes Forever to Make a Change (build lag variant)
Root cause: build lag — architecture creates excessive recompilation fan-out
Recommended skill: dependency-breaking-technique-executor
Fallback: Identify which concrete class is included by everything; introduce an interface for it so consumers compile against the interface, not the implementation
```

## References

Full 19-symptom routing table with complete technique previews and diagnostic guidance:
`references/symptom-routing-table.md`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Working Effectively with Legacy Code by Michael C. Feathers (2004, Prentice Hall).

## Related BookForge Skills

This skill is the primary entry point. It dispatches to the following skills:

**Depends on (prerequisite):**
- `legacy-code-change-algorithm` — the 5-step master procedure this skill routes into. When in doubt, start here.

**Dispatches to (downstream skills):**
- `legacy-code-addition-techniques` — Symptoms 1 (time pressure): Sprout Method, Sprout Class, Wrap Method, Wrap Class
- `tdd-and-programming-by-difference` — Symptom 3 (add feature to tested code): TDD + Programming by Difference
- `test-harness-entry-diagnostics` — Symptoms 4, 5 (class/method can't be tested): 7-case class triage + method-level triage
- `change-effect-analysis` — Symptoms 6, 7 (what to test, many changes): effect sketching + pinch points
- `characterization-test-writing` — Symptom 8 (don't know what tests to write): behavior-pinning test algorithm
- `library-seam-wrapper` — Symptoms 9, 10 (library/API coupling): wrapper interface pattern
- `scratch-refactoring-for-code-understanding` — Symptoms 11, 12 (comprehension, no structure): throwaway refactoring
- `big-class-responsibility-extraction` — Symptoms 12, 15 (no structure, class too big): 7-heuristic extraction
- `unit-test-quality-checker` — Symptom 13 (test code in the way): test classification and organization
- `dependency-breaking-technique-executor` — Symptoms 2, 14 (build lag, non-OO): 24-technique catalog
- `duplication-removal-via-extraction` — Symptom 16 (same code everywhere): deduplication via extraction
- `monster-method-decomposition` — Symptom 17 (monster method): Bulleted/Snarled decomposition
- `safe-legacy-editing-discipline` — Symptom 18 (fear of breaking things): 4 editing safety disciplines
- `seam-type-selector` — prerequisite for Symptom 14 (non-OO language): Object/Link/Preprocessor seam selection

Install the full book skill set: [bookforge-skills — working-effectively-with-legacy-code](https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code)
