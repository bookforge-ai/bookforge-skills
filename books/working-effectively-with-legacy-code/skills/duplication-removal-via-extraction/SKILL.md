---
name: duplication-removal-via-extraction
description: "Remove duplicated code across methods and classes by extracting small shared utilities first and letting larger structure (superclass, Template Method) emerge. Use whenever a developer says 'I'm changing the same code in multiple places', 'I'm fixing the same bug in 3 files', 'copy-pasted code everywhere', 'duplicate logic', 'DRY violation', 'same code in multiple classes', 'repeated patterns', 'shotgun surgery'. Activates for 'extract method', 'extract class', 'pull up method', 'Template Method pattern', 'superclass for duplication', 'deduplicate', 'shared utility', 'parallel classes'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/duplication-removal-via-extraction
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [21]
domain: software-engineering
tags: [legacy-code, refactoring, software-engineering, code-quality, dry, duplication]
depends-on:
  - characterization-test-writing
execution:
  tier: 1
  mode: full
  inputs:
    - type: codebase
      description: "Two or more classes/methods with duplicated code + tests (or characterization tests) covering the duplication"
  tools-required: [Read, Grep, Edit, Bash]
  tools-optional: [Glob]
  mcps-required: []
  environment: "Codebase in any OO language. Tests must exist before starting — characterization tests if none available."
discovery:
  goal: "Consolidate duplicated code into shared structures that emerge from bottom-up extraction."
  tasks:
    - "Confirm tests cover the duplication (or write characterization tests first)"
    - "Identify the smallest duplicated fragment"
    - "Extract to local method in one class"
    - "Replicate in the other class"
    - "Introduce shared parent/superclass"
    - "Pull up the shared method"
    - "Let larger patterns (Template Method) emerge"
  audience:
    roles: [software-engineer, backend-developer]
    experience: intermediate
  when_to_use:
    triggers:
      - "Same bug fix needed in multiple places"
      - "Same logic appears across parallel classes"
      - "Developer says 'I'm changing the same code everywhere'"
      - "Shotgun surgery smell detected"
    prerequisites:
      - skill: characterization-test-writing
        why: "Tests must cover the duplication before extraction — the tests catch behavior-changing mistakes during consolidation"
    not_for:
      - "Coincidentally-similar syntax that represents different concepts (don't couple them)"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 10
    iterations_needed: null
---

# Duplication Removal via Extraction

## When to Use

You recognize a duplication problem: every time a rule changes, you make the same edit in multiple places. Every bug fix requires the same patch applied three times. Parallel classes drift apart over time because there is no single location of truth. Feathers calls this "I'm Changing the Same Code All Over the Place" — one of the most frustrating symptoms in legacy systems.

The instinct is often to plan a grand restructuring before touching anything. Resist it. Duplication removal does not require a reengineering effort. You can remove it in small, safe steps while doing your regular work, and the larger structure will reveal itself.

Before arriving here, run `characterization-test-writing` to establish a regression safety net across all the duplicated sites. Every step in this process makes a mechanical change. Without tests, you cannot distinguish "still correct" from "silently broken."

Do not use this skill when the similarity is coincidental — two classes that happen to use the same 3-line sequence but for unrelated reasons. Coupling them creates a false dependency. The test is: if one copy needed to change, would the other need to change too? If yes: real duplication. If no: coincidental similarity.

## Context and Input Gathering

Collect before starting:

1. **The duplicated sites** — which classes and methods contain the repeated code. Use `Grep` to find all occurrences if the duplication is spread across many files.
2. **Test coverage** — confirm tests exist that exercise the behavior of all duplicated sites. If not, invoke `characterization-test-writing` first and return here.
3. **Shared type relationship** — do the classes already share a common superclass or interface? If yes, pulling up is simpler. If no, you will introduce one in Step 5.
4. **Language constraints** — single inheritance languages (Java, C#) mean one superclass slot. In those languages, prefer pulling up to an abstract class when a natural parent exists; use an interface when the shared behavior is incidental to identity.

## Process

### Step 1: Verify Test Coverage Across All Duplicated Sites

Run the test suite. Every class and method containing the duplicated code must be covered by at least one test. The tests do not need to be comprehensive — they need to catch behavior changes in the specific code you are about to move.

If any duplicated site has no test coverage: stop. Invoke `characterization-test-writing` for the uncovered sites, then return here.

> **Why tests before extraction:** Each mechanical step in this process is safe in isolation but can introduce a subtle error. A miscopied variable name, a typo in the extracted method signature, a wrong access modifier — any of these silently changes behavior. Tests transform "I hope this is still correct" into "I know this is still correct."

### Step 2: Identify the Smallest Duplicated Fragment

Read the duplicated methods. Do not look for the largest region of similarity — look for the smallest repeated sequence that forms a coherent unit. A two-line pair that always appears together is a valid extraction target even if the surrounding method has dozens of lines.

Feathers' heuristic: "Start small. If I can remove tiny pieces of duplication, I do those first because often it makes the big picture clearer."

Write down the fragment verbatim. Give it a candidate name. Ask: does this name describe what the fragment does, not how? If yes, you have found your extraction target.

Example: `outputStream.write(field.getBytes()); outputStream.write(0x00);` — always paired, always together. Name: `writeField(OutputStream, String)`.

### Step 3: Extract the Fragment to a Local Method in One Class

Pick one of the classes containing the duplication. Extract the fragment there first.

1. Create the new private method with the candidate name.
2. Replace every occurrence of the fragment in that class with a call to the new method.
3. Run the tests. They must pass.

Do not touch the other class yet. The goal of this step is a passing, locally-clean change in exactly one class.

```java
// Before (LoginCommand.write):
outputStream.write(userName.getBytes());
outputStream.write(0x00);
outputStream.write(passwd.getBytes());
outputStream.write(0x00);

// After extraction:
private void writeField(OutputStream outputStream, String field) throws Exception {
    outputStream.write(field.getBytes());
    outputStream.write(0x00);
}

// LoginCommand.write now calls:
writeField(outputStream, userName);
writeField(outputStream, passwd);
```

### Step 4: Replicate the Same Local Method in the Other Class

Now copy the extracted method — with the identical signature — into the other class. Replace the duplicate fragment in that class with calls to the new method. Run the tests. They must pass.

At the end of this step, both classes have an identical private method with the same name, the same signature, and the same body. This is the deliberate state you are building toward: identical local copies are the precondition for a pull-up.

> **Why replicate before pulling up:** Pulling up to a superclass before both local copies exist means you are designing top-down. That requires you to know the full structure upfront. Replicating bottom-up means you can pull up mechanically — you are not making design decisions, you are moving code that already exists.

### Step 5: Introduce a Shared Superclass (If None Exists)

If the classes already share a common parent that is appropriate for the shared method, skip to Step 6.

If not, introduce one:

1. Create an abstract superclass (e.g., `Command` as parent of `LoginCommand` and `AddEmployeeCmd`).
2. Make both existing classes extend it.
3. Do not move any code yet — only establish the type relationship.
4. Run the tests. They must pass.

Choose a name that describes what the classes have in common, not what is convenient. If the name is awkward, the superclass boundary may be wrong.

### Step 6: Pull the Method Up to the Superclass

Move the shared method from one subclass to the superclass. Delete the copy in the other subclass. Verify both subclasses now call the superclass version.

Run the tests. They must pass.

```java
// Command (superclass) now holds:
protected void writeField(OutputStream outputStream, String field) throws Exception {
    outputStream.write(field.getBytes());
    outputStream.write(0x00);
}
// Removed from LoginCommand and AddEmployeeCmd
```

### Step 7: Repeat for Additional Fragments

Return to Step 2. Look at the now-cleaner methods in both classes. Has the first extraction revealed more duplication? Often it has: the removed fragment was obscuring a larger pattern.

Continue extracting, replicating, and pulling up one fragment at a time. Run the tests after every step.

### Step 8: Observe — Let Structure Emerge

After removing the small fragments, look at what remains. Are the write methods in both subclasses now structurally identical — same steps, different data? That is the Template Method pattern emerging:

- Extract the variation (the "body" of the method — the part that differs per subclass) into an abstract `writeBody()` method.
- Pull the invariant outer structure (header, size, command char, body, footer) up to the superclass as the single concrete `write()` method.
- Each subclass only implements `writeBody()`.

Do not design this structure upfront. Arrive at it by noticing that two method bodies are identical except for one extracted piece. The pattern is a consequence of systematic duplication removal, not a precondition for it.

> **Orthogonality emerges:** When duplication is fully removed, each behavior has exactly one location. To change how fields are written, edit `writeField`. To change the message envelope, edit `write`. To add a new command variant, subclass and implement `writeBody`. This is the open/closed principle made concrete — open for extension (new subclasses), closed to modification (existing methods need not change).

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Duplicated code sites | Yes | Classes and methods containing the repeated logic |
| Test coverage | Yes | Passing tests covering each duplicated site |
| Shared type relationship | No | Whether classes already share a parent (simplifies Step 5) |

## Outputs

| Output | Description |
|--------|-------------|
| Extraction plan | Ordered list of fragment → local method → pull-up steps, with test runs between each |
| Consolidated code | Shared method(s) in superclass or shared interface; thin subclasses containing only variation |
| Passing test suite | Same tests that existed before, still passing — behavioral proof that extraction preserved correctness |

## Key Principles

**Start with the SMALLEST duplicated fragment, not the whole method.**
Large-scale deduplication is the result of many small extractions, not one large one. Small steps are reversible, verifiable, and reveal the next step naturally.

**Tests MUST cover the duplication before extraction begins.**
Without a safety net, a mechanical step that looks correct can silently change behavior. Tests turn this process from "I believe this is safe" to "I know this is safe."

**Replicate locally before pulling up.**
Extract to a local private method in each class first. When both local copies are identical, the pull-up is a mechanical move. This separates the "what to extract" decision from the "where to put it" decision.

**Let structure emerge — do not design it upfront.**
Template Method, common superclasses, abstract methods — these are observations about what the code already implies, not plans imposed on the code. Arrive at them by noticing what is the same.

**Coincidental similarity is not duplication.**
Two classes that have the same 3-line sequence for unrelated reasons should not be coupled. The test: if one copy needed to change, would the other need to change too? Same semantic intent = duplication. Shared syntax, different intent = coincidence.

**After consolidation, the open/closed principle is at work.**
New variations become easier, not harder. A new command subclass only implements its variation. The shared mechanism is inherited. Adding a feature no longer requires changing every copy.

## Examples

### Example 1: LoginCommand + AddEmployeeCmd → Command Superclass

**Situation:** Two Java command classes both contain the repeated pair `outputStream.write(field.getBytes()); outputStream.write(0x00);` for every string field they write. Both classes write header, command char, fields, footer — same structure, different fields.

**Step 2 — Smallest fragment:** The two-line write-and-terminate pair. Name: `writeField(OutputStream, String)`.

**Step 3 — Extract locally in LoginCommand:**
```java
private void writeField(OutputStream outputStream, String field) throws Exception {
    outputStream.write(field.getBytes());
    outputStream.write(0x00);
}
```
Replace all `write/0x00` pairs in `LoginCommand.write()` with `writeField(...)` calls. Tests pass.

**Step 4 — Replicate in AddEmployeeCmd:** Same method, identical signature. Replace its pairs. Tests pass.

**Step 5 — Introduce superclass:** Create abstract `Command` class. Both classes extend it. Tests pass.

**Step 6 — Pull up:** Move `writeField` to `Command`. Delete local copies. Tests pass.

**Step 8 — Emergence:** After writeField is shared, both `write()` methods are structurally identical: header → size → commandChar → writeBody() → footer. Extract `writeBody()` as abstract. Pull `write()` to `Command`. Pull shared constants (`header`, `footer`, `SIZE_LENGTH`). The subclasses reduce to constructor + `writeBody()` + `getCommandChar()`.

Final state: `Command` holds all protocol logic. Adding a new command is one subclass, no copy-paste.

### Example 2: Two Validators with Repeated Null-Check Pattern

**Situation:** `UserValidator` and `OrderValidator` both open with:
```java
if (input == null) {
    throw new IllegalArgumentException("input must not be null");
}
```
The guard is identical across both classes and three other validators as well.

**Step 2 — Smallest fragment:** The three-line null guard. Candidate name: `requireNonNull(Object, String)`.

**Steps 3–4:** Extract to local method in `UserValidator`, replicate in `OrderValidator`. Tests pass in both.

**Step 5:** Check — do the validators share a parent? If they all extend a `BaseValidator`, pull up there. If not, decide: introduce `AbstractValidator` or extract to a shared utility class (`ValidationUtils.requireNonNull`). Choose based on whether validators truly share an identity or are only incidentally similar.

**Step 8 — Observe:** After the guard is shared, look at whether the remaining validation logic also shares structure. If all validators do: guard → validate fields → aggregate errors → return result, Template Method is emerging. Extract `validateFields()` as abstract and pull the outer structure up.

### Example 3: Coincidental Similarity — Do NOT Extract

**Situation:** `FilePermissionChecker` and `DatabaseConnectionPool` each contain:
```java
if (count < 0) {
    throw new IllegalArgumentException("count must be non-negative");
}
```

**Analysis:** `FilePermissionChecker` checks the number of retries. `DatabaseConnectionPool` checks the pool minimum size. These are semantically unrelated. The two classes have nothing in common — no shared parent makes sense, no shared utility class is appropriate.

**Decision: do not extract.** The similarity is coincidental. If the retry validation rule changes (e.g., to allow 0 retries), you would change `FilePermissionChecker` but not `DatabaseConnectionPool`. Coupling them would create false dependencies and make both harder to change.

The test: "If one copy needed to change, would the other need to change too?" Answer here: no. Leave them independent.

## References

- `references/legacy-code-fundamentals.md` — core definitions: legacy code, seams, characterization tests
- `references/refactoring-patterns.md` — extract method, pull up method, template method mechanics

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — BookForge Skills, derived from "Working Effectively with Legacy Code" by Michael C. Feathers. Skill interpretation, structure, and synthesis are original BookForge content.

## Related BookForge Skills

**Direct dependency (run before this skill):**
- `characterization-test-writing` — establish the regression safety net that makes each extraction step safe

**Cross-references:**
- `big-class-responsibility-extraction` — when duplication removal reveals that a class is still doing too much, apply this next to split remaining responsibilities
- `dependency-breaking-technique-executor` — the "Pull Up Feature" technique overlaps with pull-up mechanics; use when dependency breaking and duplication removal are both needed in the same class hierarchy
