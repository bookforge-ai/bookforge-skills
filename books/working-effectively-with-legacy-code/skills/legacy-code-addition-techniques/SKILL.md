---
name: legacy-code-addition-techniques
description: "Add new functionality to untested legacy code using Sprout Method, Sprout Class, Wrap Method, or Wrap Class — whichever best fits the dependency profile. Use whenever a developer needs to add a feature, log statement, validation, or any new behavior to legacy code that they can't easily test — 'I have to add this feature fast', 'no time for a big refactor', 'just need to log this', 'add a check to existing method', 'need to add behavior without breaking legacy', 'sprout method', 'sprout class', 'wrap method', 'wrap class', 'decorator for legacy'. Activates for 'quick change to legacy', 'under time pressure', 'can't test this class but need to add a feature', 'extend without editing'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/legacy-code-addition-techniques
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [6]
domain: software-engineering
tags: [legacy-code, refactoring, testing, software-engineering, feature-addition]
depends-on:
  - legacy-code-change-algorithm
  - safe-legacy-editing-discipline
execution:
  tier: 1
  mode: full
  inputs:
    - type: codebase
      description: "Existing source code + description of the new behavior to add"
  tools-required: [Read, Edit, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Codebase in an OO language. Test framework configured."
discovery:
  goal: "Add new behavior to legacy code using the least-invasive Sprout or Wrap technique."
  tasks:
    - "Classify the scope and temporal-coupling nature of the new behavior"
    - "Select Sprout Method / Sprout Class / Wrap Method / Wrap Class via 2×2 matrix"
    - "Execute the chosen technique step-by-step with TDD"
    - "Leave old code in place; flag for later proper refactoring"
  audience:
    roles: [software-engineer, backend-developer, senior-developer]
    experience: intermediate
  when_to_use:
    triggers:
      - "Time-constrained feature addition to legacy code"
      - "New code must be tested but surrounding code is untestable"
      - "Behavior must co-execute with existing behavior but stay separable"
    prerequisites:
      - skill: legacy-code-change-algorithm
        why: "Sprout/Wrap is Step 5 (make change) when you can't break enough dependencies upfront"
      - skill: safe-legacy-editing-discipline
        why: "Preserve Signatures and Single-Goal Editing apply during the wrapping step"
    not_for:
      - "Code that IS already under test — use TDD directly"
      - "Major new features that justify structural refactoring upfront"
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

# Legacy Code Addition Techniques (Sprout & Wrap)

## When to Use

You need to add new behavior to a legacy codebase — a feature, a logging statement, a validation check, an integration hook — but you cannot get the surrounding code under test right now. The existing method or class is too entangled to test directly.

Any of these conditions apply:

- You need to add a feature today, and breaking dependencies on the source class would take hours you don't have
- The source method contains old logic you must not disturb, and the new behavior is conceptually distinct
- Adding code inline would mingle two separate operations into one method, making future changes harder
- The source class cannot be instantiated in a test harness at all (constructor dependencies are too severe)
- New behavior must execute every time the existing method is called (temporal coupling concern)

This skill is Step 5 of `legacy-code-change-algorithm`. If you haven't identified change points and test points yet, start there. Return here when you've determined that the change must be made without full test coverage of the source class.

**Before executing, have:**
1. Target class/method name(s) where the new behavior must be introduced
2. A one-sentence description of the new behavior
3. An answer to: "Does this behavior need to execute alongside the existing call, or is it standalone?"
4. An answer to: "Can the source class be instantiated in a test harness right now?"

## Context & Input Gathering

### Required

- **Target class and method:** Where in the codebase does the change happen?
  -> Read the file. Identify the specific method where you'd otherwise add the inline code.

- **New behavior description:** What exactly should the new code do?
  -> Must be specific enough to write a test for. "Log the payment" or "filter duplicate entries" — not "add some validation."

- **Testability of source class:** Can you construct an instance of the source class in a test harness within the time available?
  -> Check for: multi-argument constructors with DB connections, HTTP clients, file handles, singletons, or global state.
  -> Default assumption: source class is **not** easily testable (else you wouldn't be here).

- **Temporal coupling:** Must the new behavior fire every time the existing method is called?
  -> YES → the new behavior is temporally coupled → lean toward **Wrap**
  -> NO → the new behavior can stand alone → lean toward **Sprout**

### Observable from Codebase

- Constructor signature of the source class (how hard is instantiation?)
- Whether the method already returns a value (affects Sprout Method's return handling)
- Whether the source class implements an interface (makes Wrap Class easier)
- Language (Java/C#/C++ → all four techniques; dynamic languages → Wrap Method simpler)

## Process

### Step 1: Classify Scope

**ACTION:** Determine whether the new behavior is *method-level* (a single new operation added at one call site in one method) or *class-level* (the behavior is logically a new abstraction, or the source class is so heavily coupled that even a sprouted method can't be tested on it).

**WHY:** Technique selection depends on whether you can get *any* testable unit out of the source class. Method-level scope means you can stay inside the source class. Class-level scope means you need to leave the source class entirely.

**Rule of thumb:**
- If you can write `new SourceClass(...)` in a test harness in under 30 minutes → method-level scope is viable.
- If constructor dependencies (DB, network, file system, singletons) would take hours to untangle → class-level scope; you must move to a new class.

**ARTIFACT:** Declare scope in your working notes: `scope = method-level` or `scope = class-level`.

---

### Step 2: Classify Temporal Coupling

**ACTION:** Determine whether the new behavior is *independent* (it happens separately, can be called on its own) or *temporally coupled* (it must co-execute every time the original method is called).

**WHY:** Temporal coupling is the reason you'd be tempted to add code inline at the bottom of an existing method — "it has to happen at the same time." Wrap techniques explicitly address this by making the co-execution visible and deliberate at the callsite rather than buried inside the method. Sprout techniques assume the new behavior stands alone.

**Rule of thumb:**
- "Every call to `pay()` must also log" → temporally coupled → Wrap
- "I need to add duplicate-detection as a new step, but it could be called separately" → independent → Sprout

**ARTIFACT:** Declare coupling in your working notes: `coupling = temporally-coupled` or `coupling = independent`.

---

### Step 3: Apply the 2×2 Selector

**ACTION:** Cross scope and coupling to select the technique:

```
                    SPROUT              WRAP
                 (independent)     (co-executes)
                ┌─────────────────┬──────────────────┐
 METHOD-LEVEL   │ Sprout Method   │  Wrap Method     │
                ├─────────────────┼──────────────────┤
 CLASS-LEVEL    │ Sprout Class    │  Wrap Class      │
                └─────────────────┴──────────────────┘
```

**Why each quadrant:**

| Technique | When to prefer | Key advantage | Key disadvantage |
|---|---|---|------|
| **Sprout Method** | Method-level + independent | Clearly separates new code from old; new method is fully testable | Gives up on getting source method under test; leaves source method in odd state |
| **Sprout Class** | Class-level + independent | Lets you TDD even when source class can't be constructed | Conceptually fragmenting — new class may seem disconnected |
| **Wrap Method** | Method-level + co-executes | Makes temporal coupling explicit; does not grow the original method | Must invent a new name for the original method's logic |
| **Wrap Class** | Class-level + co-executes | Fully separates new behavior from old using the Decorator pattern | More structural overhead for simple additions |

**Additional selection rules:**
- Prefer **Wrap Method** over **Sprout Method** when the new feature is as important as the original method's purpose — Wrap makes it a first-class operation visible in the calling interface.
- Use **Wrap Class** when the same new behavior needs to apply across many callers uniformly (Decorator pattern), or when the source class has grown so large that any addition makes it worse.
- Use **Sprout Class** when you initially tried Sprout Method but couldn't even pass constructor arguments in a test (e.g., the class needs `new DatabaseConnection()` that you cannot fake quickly).

**ARTIFACT:** Decision recorded: `technique = [Sprout Method | Sprout Class | Wrap Method | Wrap Class]`.

---

### Step 4: Execute the Chosen Technique

Execute the step-by-step mechanics for your chosen technique. Full reference mechanics for all four are in `references/four-techniques-mechanics.md`. The most common two cases are inlined below.

#### Sprout Method (method-level + independent)

1. Identify the exact location in the source method where the new functionality must happen.
2. Write (but comment out) a call to a new method that will do the work. Decide its name and arguments now, before writing it. This forces you to think about its interface in context.
3. Determine which local variables the new method needs from the source method. These become its parameters.
4. Determine whether the new method must return a value to the source method. If yes, assign its return value to a variable in the call.
5. Develop the new sprouted method using test-driven development — write tests for the sprouted method in isolation; make them pass.
6. Uncomment the call in the source method to activate the integration.

**WHY each step matters:**
- Step 2 (comment first): writing the call before the method locks in the right interface and avoids overbuilding.
- Step 5 (TDD the sprout): you may not be able to test the source method, but you can always test the sprouted method because it has no legacy dependencies.
- Step 6 last: the source method is only modified after the new code is fully tested — minimizing risk in the untested zone.

#### Wrap Method (method-level + co-executes)

1. Identify the method whose every call must include the new behavior.
2. Rename the existing method to something that describes what it actually does (e.g., `pay()` → `dispatchPayment()`). **Apply Preserve Signatures:** copy the signature exactly — same parameter types, same return type. Make the renamed method private.
3. Create a new method with the **original name and signature**. This is the new public entry point.
4. In the new method, call both the renamed original method and a new method that you develop using TDD for the new behavior. Order (before or after) depends on the requirement.

**WHY each step matters:**
- Step 2 (rename, don't copy): keeps the original logic in one place; renaming rather than duplicating prevents divergence.
- Step 2 (Preserve Signatures): you are editing without tests; any signature change that breaks callers is a regression you won't catch. Copy-paste the signature verbatim.
- Step 3 (same original name): all existing callers continue to work — they call `pay()` and get both behaviors transparently.
- Step 4 (TDD the new method): the new behavior is tested even though `pay()` itself cannot be tested in isolation.

For **Sprout Class** and **Wrap Class** step-by-step mechanics, see `references/four-techniques-mechanics.md`.

---

### Step 5: Develop New Code with TDD

**ACTION:** Regardless of technique chosen, write and pass tests for the new sprouted method, new sprouted class, or new wrapped method *before* integrating.

**WHY:** The whole point of Sprout/Wrap is to create a seam between tested new code and untested old code. If you skip tests on the new code, you lose the only testing benefit these techniques provide. The surrounding code has no tests — but the new code can and must have tests.

**HOW:**
1. Write the simplest test that fails because the new method/class doesn't exist yet.
2. Implement just enough to make it pass.
3. Refactor the new code. It is clean code; you can afford to refactor it.
4. Repeat until the behavior described in your requirement is fully tested.

---

### Step 6: Integrate

**ACTION:** Activate the new code within the legacy call site.

- **Sprout Method:** Uncomment the call in the source method.
- **Sprout Class:** Uncomment the object creation and method call in the source method.
- **Wrap Method:** The renamed+new structure is already in place from Step 4; verify callers still compile.
- **Wrap Class:** Replace object instantiation site(s) with the wrapper class. If source class implements an interface, the wrapper implements the same interface — all callers remain unchanged.

Run the full build and any available tests (even characterization tests for the legacy code, if they exist) to confirm no regressions.

---

### Step 7: Document the Refactoring Debt

**ACTION:** Add an entry to `refactor-backlog.md` immediately.

**WHY:** Sprout and Wrap are *intentionally temporary*. They leave old code in limbo — the source method or class has not been cleaned up, its responsibilities are now split, and the design is arguably worse than a proper refactoring would achieve. Documenting the debt ensures future work on this area includes a plan to get the source class under test and integrate the sprouted/wrapped logic properly.

**Entry format:**
```markdown
## [ClassName / method] — Sprout/Wrap debt
- Technique applied: [Sprout Method | Sprout Class | Wrap Method | Wrap Class]
- New code location: [method or class name]
- Source method/class: [name] in [file path]
- What still needs doing: Get [SourceClass] under test, inline [NewMethod/NewClass] into proper location, eliminate the split responsibility.
- Date introduced: [today]
```

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Source class and method | Yes | The legacy code where new behavior must appear |
| New behavior description | Yes | What the new code must do (specific enough to test) |
| Temporal coupling answer | Yes | Must new behavior fire on every existing call? |
| Constructor testability answer | Yes | Can source class be instantiated in a test harness quickly? |
| Test framework | Yes | Must be configured to run tests on new isolated code |

## Outputs

| Output | Description |
|--------|-------------|
| New method or new class | The new behavior, fully tested in isolation |
| Modified source method | One-line integration call added (Sprout) or rename+delegate (Wrap) |
| `refactor-backlog.md` entry | Tracks the remaining design debt |
| Test file | TDD tests for the new method/class |

## Key Principles

- **Sprout/Wrap leaves OLD code in place — this is temporary.** The source method is not improved; you are adding tested code beside or around it. Document the debt immediately. The techniques buy time; eventual refactoring of the source class is still required.

- **Wrap when new behavior must co-execute; Sprout when it stands alone.** Temporal coupling is the deciding signal. Adding code inside a method "because it runs at the same time" is exactly the pattern that creates tangled legacy code. Wrap makes the coupling explicit and separable.

- **Class-level when constructor dependencies block method-level.** If you cannot construct the source class in a test harness at all, move to a new class (Sprout Class) or wrap at the class level (Wrap Class). Do not try to sprout a method in a class you can't test.

- **Develop new code with TDD, even though the surrounding code has no tests.** The seam between old and new code is a testing opportunity. The new method/class has clean dependencies — you chose them. This is the one place in the legacy codebase where you can practice full red-green-refactor.

- **Preserve Signatures during rename (Wrap Method).** When renaming the original method, copy its signature verbatim — same parameter names, types, and return type. You are changing an untested method; any accidental signature modification will break callers silently.

- **Name the sprouted/wrapped code for what it actually does.** `dispatchPayment()`, `uniqueEntries()`, `QuarterlyReportTableHeaderProducer` — not `payOld()` or `doWork2()`. The sprout or wrap will likely persist longer than you expect.

## Examples

### Sprout Method: Duplicate-entry detection in `TransactionGate.postEntries()` (Java)

**Situation:** `postEntries(List entries)` posts dates and adds entries to a bundle. A new requirement: skip entries already in the bundle. Adding the check inline mingles duplicate-detection with date-posting in one loop.

**Analysis:** Method-level + independent → Sprout Method.

**Before (inline attempt — avoided):**
```java
public void postEntries(List entries) {
    List entriesToAdd = new LinkedList();
    for (Iterator it = entries.iterator(); it.hasNext(); ) {
        Entry entry = (Entry)it.next();
        if (!transactionBundle.getListManager().hasEntry(entry)) { // new check mixed in
            entry.postDate();
            entriesToAdd.add(entry);
        }
    }
    transactionBundle.getListManager().add(entriesToAdd);
}
```
This mingles two operations: date-posting and duplicate detection. It also introduces a temporary variable that will attract more code.

**After (Sprout Method):**
```java
// New sprouted method — fully tested in isolation
List uniqueEntries(List entries) {
    List result = new ArrayList();
    for (Iterator it = entries.iterator(); it.hasNext(); ) {
        Entry entry = (Entry)it.next();
        if (!transactionBundle.getListManager().hasEntry(entry)) {
            result.add(entry);
        }
    }
    return result;
}

// Source method: single integration call added
public void postEntries(List entries) {
    List entriesToAdd = uniqueEntries(entries);   // Step 6: uncommented
    for (Iterator it = entriesToAdd.iterator(); it.hasNext(); ) {
        Entry entry = (Entry)it.next();
        entry.postDate();
    }
    transactionBundle.getListManager().add(entriesToAdd);
}
```
`uniqueEntries()` is tested with a `FakeListManager` before the call in `postEntries()` is uncommented.

---

### Wrap Method: Payment logging in `Employee.pay()` (Java)

**Situation:** `pay()` calculates timecard totals and dispatches payment. New requirement: log every payment. Logging must happen every time `pay()` is called.

**Analysis:** Method-level + temporally coupled → Wrap Method.

**Before:**
```java
public void pay() {
    Money amount = new Money();
    for (Iterator it = timecards.iterator(); it.hasNext(); ) {
        Timecard card = (Timecard)it.next();
        if (payPeriod.contains(date)) {
            amount.add(card.getHours() * payRate);
        }
    }
    payDispatcher.pay(this, date, amount);
}
```

**After (Wrap Method — rename + delegate):**
```java
// Original logic, renamed, made private — Preserve Signatures applied
private void dispatchPayment() {
    Money amount = new Money();
    for (Iterator it = timecards.iterator(); it.hasNext(); ) {
        Timecard card = (Timecard)it.next();
        if (payPeriod.contains(date)) {
            amount.add(card.getHours() * payRate);
        }
    }
    payDispatcher.pay(this, date, amount);
}

// New public entry point — callers are unchanged
public void pay() {
    logPayment();           // new behavior — TDD'd in isolation
    dispatchPayment();      // delegate to original
}

private void logPayment() { ... }  // TDD'd, tested independently
```
All existing callers of `pay()` continue to work. The two behaviors — logging and dispatch — are independently testable.

---

### Sprout Class: HTML table header in `QuarterlyReportGenerator` (C++)

**Situation:** `QuarterlyReportGenerator::generate()` builds an HTML report. New requirement: add a header row to the HTML table. The class is a large legacy class that would take a day to get into a test harness.

**Analysis:** Class-level + independent → Sprout Class.

**New class developed with TDD:**
```cpp
class QuarterlyReportTableHeaderProducer {
public:
    string makeHeader();
};

string QuarterlyReportTableHeaderProducer::makeHeader() {
    return "<tr><td>Department</td><td>Manager</td>"
           "<td>Profit</td><td>Expenses</td></tr>";
}
```

**Integration into source method (uncommented after TDD passes):**
```cpp
// Inside QuarterlyReportGenerator::generate()
QuarterlyReportTableHeaderProducer producer;
pageText += producer.makeHeader();   // Step 6: uncommented
```

`QuarterlyReportTableHeaderProducer` is tested completely independently of `QuarterlyReportGenerator`. The legacy class is not touched beyond the one integration line.

**Design note:** The class name initially seems disconnected. Over time it can be renamed `QuarterlyReportTableHeaderGenerator` and unified under an `HTMLGenerator` interface — but that refactoring happens later, when the source class is finally brought under test.

## References

Full step-by-step mechanics for all four techniques, including Sprout Class (6 steps) and Wrap Class (4 steps + Decorator pattern guidance):

- `references/four-techniques-mechanics.md`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Working Effectively with Legacy Code by Michael C. Feathers (2004, Prentice Hall), Chapter 6.

## Related BookForge Skills

**Dependencies (must be installed for full value):**
- `legacy-code-change-algorithm` — The 5-step framework that leads to this skill. Sprout/Wrap is used at Step 5 when you can't break enough dependencies upfront. IF not installed → use this skill standalone, but know that you are skipping test point identification and dependency analysis.
- `safe-legacy-editing-discipline` — The 4 safety constraints (Preserve Signatures, Single-Goal Editing, Hyperaware Editing, Lean on the Compiler) that govern Step 4's rename operation. IF not installed → apply Preserve Signatures manually: copy-paste signatures verbatim, make zero other changes during the rename step.

**Cross-references:**
- `characterization-test-writing` — When the source class finally gets under test (Step 7's future work), use this to write characterization tests that lock in its current behavior before you clean up the sprout/wrap debt.
- `dependency-breaking-technique-executor` — When you try Sprout Method but discover the source class can't be instantiated even for a method-level test, this skill applies the full catalog of 24 dependency-breaking techniques to make the class testable.
- `seam-type-selector` — Helps identify which kind of seam (object seam, link seam, preprocessing seam) is available in the source class; useful before choosing between Sprout Method and Sprout Class.

Install the full book skill set: [bookforge-skills — working-effectively-with-legacy-code](https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code)
