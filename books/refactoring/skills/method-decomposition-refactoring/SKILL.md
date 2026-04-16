---
name: method-decomposition-refactoring
description: |
  Decompose long, tangled methods into clean, composable units using the 9 composing-method refactorings from Fowler's catalog. Use when: a method has grown too long to understand at a glance; code contains a comment that explains what a block does (the comment is a signal to extract); a method cannot be changed without understanding all of its internals; local variables are so numerous that Extract Method keeps failing; a method is doing several conceptually distinct things that are collapsed into one body. The flagship technique is Extract Method — applied when the semantic distance between the method name and its body is too large; name the fragment after what it does, not how it does it. Companion techniques handle the obstacles: Replace Temp with Query eliminates the local variables that block extraction; Split Temporary Variable separates a temp that has been reused for two different things; Introduce Explaining Variable names a sub-expression when extraction is blocked by too many locals; Remove Assignments to Parameters prevents a parameter from being reassigned and muddying the intent; Inline Method collapses a method whose body is as clear as its name; Inline Temp removes a temp that obstructs another refactoring; Replace Method with Method Object converts a hopelessly entangled method into its own class so that Extract Method can be applied freely; Substitute Algorithm replaces an obscure implementation with a cleaner one once the method is small enough. Trigger: Long Method smell from code-smell-diagnosis, or any method where a comment is needed to understand a code block.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/method-decomposition-refactoring
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - code-smell-diagnosis
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler", "Kent Beck"]
    chapters: [6]
tags: [refactoring, code-quality, methods]
execution:
  tier: 2
  mode: full
  level: 1
  inputs:
    - type: codebase
      description: "The method or class to decompose — a file path, a method name, or a pasted code block"
    - type: document
      description: "Diagnosis report from code-smell-diagnosis identifying Long Method or related smells, if available"
  tools-required: [Read, Edit, Bash]
  tools-optional: [Grep, Write]
  mcps-required: []
  environment: "Run inside a project directory with source files readable and a test suite runnable via the project's standard test command."
discovery:
  goal: "Transform every method whose semantic distance between name and body is too large into a set of short, intention-revealing methods — each doing one thing, each named after what it does"
  tasks:
    - "Identify the method(s) to decompose from smell diagnosis or user direction"
    - "Eliminate obstructing local variables using Replace Temp with Query or Introduce Explaining Variable"
    - "Extract cohesive code fragments into named methods with Extract Method"
    - "Handle remaining obstacles: split dual-use temps, remove parameter assignments, apply Method Object for irreducible tangles"
    - "Run the test suite after each step to confirm behavior is preserved"
    - "Optionally substitute the algorithm if a cleaner implementation becomes apparent"
  audience:
    roles: ["software-developer", "senior-developer", "tech-lead"]
    experience: "intermediate — assumes working knowledge of the host language and object-oriented design"
  triggers:
    - "Long Method smell identified by code-smell-diagnosis"
    - "A method requires a comment to explain what a block of code does"
    - "A method cannot be understood without reading its entire body"
    - "Adding a feature to a method requires untangling it first"
    - "A code review flags a method as too complex or hard to follow"
  not_for:
    - "Cross-class refactoring (Feature Envy, Shotgun Surgery) — use class-responsibility-realignment instead"
    - "Conditional structure simplification — use conditional-simplification-strategy instead"
    - "Performance optimization — use profiling-driven-performance-optimization instead"
    - "New code that hasn't been written yet — these techniques apply to existing, working code"
---

# Method Decomposition Refactoring

## When to Use

A method has grown beyond the point where its name describes what it does. The body contains
conceptually distinct operations mixed together, or it requires comments to explain sections
of code that should be self-explanatory from method names.

**The key diagnostic question from Fowler:** Length is not the issue. The key is the semantic
distance between the method name and the method body. If extracting a fragment into a named
method improves clarity — even if the extracted method's name is longer than the code it
replaces — extract it.

**Signals that decomposition is needed:**
- A comment precedes a block of code explaining what the block does
- Understanding the method requires tracking many local variables simultaneously
- A loop body, a conditional branch, or an initialization block feels like a separate concept
- The method is long enough that you scroll to read it
- When you try Extract Method, you get blocked by too many parameters from local variables

**This skill executes decomposition.** `code-smell-diagnosis` identifies that decomposition is
needed and points here. After decomposition, `conditional-simplification-strategy` handles
any remaining complex conditionals exposed in the extracted methods.

---

## Context and Input Gathering

### Required Input

- **The method to decompose.** File path and method name, or a pasted code block. Why: the
  refactoring is grounded in the actual code — general descriptions are insufficient for
  making safe, correct transformations.

- **The test suite command.** Why: every Extract Method step must be verified by running
  tests. Without a passing test suite before starting, you cannot confirm you have preserved
  behavior. If no tests exist, flag this and apply `build-refactoring-test-suite` first.

### Observable Context

Before starting, read the method and answer these questions:

```
Local variable inventory:
  - How many local variables does the method declare?
  - Which variables are read-only within a candidate extraction?
  - Which variables are assigned within a candidate extraction?
  - Which variables are used both inside and outside a candidate extraction?

Conceptual block inventory:
  - Where are the comments? Each comment marks a likely extraction boundary.
  - Does the method initialize, then compute, then output? Each phase is a candidate.
  - Are there loops? Each loop and its body is a candidate for extraction.
  - Are there conditionals? Each branch may be a candidate.
```

### Default Assumptions

- If the user has not run the tests: run them first and confirm they pass before any change.
- If a candidate extraction would require more than one output variable: choose different
  extraction boundaries or apply Replace Temp with Query first to eliminate the variable.
- If the method is so entangled that every extraction attempt produces a 5+ parameter
  signature: jump to Replace Method with Method Object (Step 6) before attempting extraction.

---

## Process

### Step 1: Read and Inventory the Method

**ACTION:** Read the entire method. List every local variable, its type, where it is assigned,
and where it is used. Mark conceptual blocks — typically announced by comments.

**WHY:** Extract Method's only real complication is local variables. A full inventory before
starting prevents surprises mid-extraction (discovering a variable is written inside the
extraction and read outside it, which requires returning a value). The inventory also reveals
which temp elimination refactoring to apply before extraction.

**Categorize each local variable:**
- **Read-only inside candidate extraction, declared outside:** pass as parameter to extracted
  method
- **Assigned only inside candidate extraction:** declare inside the extracted method; remove
  the outer declaration afterward if it was declared only for the extracted block
- **Assigned inside, read outside:** the extracted method must return this value; only one
  such variable is workable per extraction
- **Assigned inside, read outside, AND other variables also modified:** you cannot extract
  cleanly; apply Replace Temp with Query or Split Temporary Variable first

---

### Step 2: Eliminate Temp Blockers Before Extracting

**ACTION:** For each local variable that would block a clean extraction, apply one of:

**Replace Temp with Query** — when a temp holds a simple expression assigned once and the
expression has no side effects.

Mechanics:
1. Find a temp assigned only once. Declare it `final` and compile — confirms it is only
   assigned once.
2. Extract the right-hand side of the assignment into a private method.
3. Replace each reference to the temp with a call to the method.
4. Compile and test after each reference replacement.
5. Remove the temp declaration.

See Example 2 below for a full walkthrough.

**WHY Replace Temp with Query:** Temps are local — visible only inside the method, and they
encourage longer methods because the method is the only way to reach the value. A query
method is visible to the entire class and can be reused, making the class's code cleaner
overall. It also unblocks Extract Method by eliminating variables that would otherwise need
to be passed as parameters.

**Split Temporary Variable** — when a temp is assigned more than once for two different
purposes (not a loop variable and not a collecting variable).

Mechanics:
1. Rename the temp at its first declaration and first assignment to a name that reflects
   only the first use. Declare it `final`.
2. Change all references from the first assignment up to the second assignment to use the
   new name.
3. At the second assignment, declare a new temp with the original name.
4. Compile and test.
5. Repeat for further assignments.

**WHY Split Temporary Variable:** A variable used for two different purposes has two
responsibilities. The name cannot honestly reflect both, so it becomes a source of confusion.
Splitting it gives each responsibility an honest name and makes each one available for
Replace Temp with Query.

**Inline Temp** — when a temp is assigned the value of a method call once and never
reassigned, and the temp is blocking another refactoring (most commonly blocking Extract
Method).

Mechanics:
1. Declare the temp `final` and compile — confirms single assignment.
2. Replace each reference to the temp with the method call expression.
3. Compile and test after each replacement.
4. Remove the temp declaration.

**WHY Inline Temp:** Temps that simply name a method call result add indirection without
adding clarity. When they obstruct a more important refactoring, inlining them is the right
trade.

**Introduce Explaining Variable** — when an expression is too complex to extract into a
method (usually because there are too many local variables blocking extraction) and the
expression needs a name to be readable.

Mechanics:
1. Declare a `final` temporary variable whose name explains the purpose of the expression.
2. Replace the expression (or the first occurrence if repeated) with the temp.
3. If the expression is repeated, replace other occurrences one at a time.
4. Compile and test.

**WHY Introduce Explaining Variable:** This is a stepping stone, not a destination. Fowler
prefers Extract Method because a method is available to the whole object while a temp is only
local. Use Introduce Explaining Variable when you are inside a tangled algorithm with many
local variables that block extraction — the explained temps can later become Replace Temp with
Query calls as the tangles loosen.

---

### Step 3: Apply Extract Method

**ACTION:** For each cohesive code fragment that represents a single concept, extract it into
a new method.

**WHY Extract Method:** It is the most common and highest-value refactoring in the catalog.
Short, well-named methods increase reuse (other methods can call them), make higher-level
methods read like a series of comments, and make overriding easier because the granularity
aligns with the conceptual granularity of the domain.

**Full mechanics (9 steps):**

1. **Create a new method.** Name it after the intention — what it does, not how it does it.
   If you cannot find a name more meaningful than the code itself, do not extract.
   Why: the name is the primary value of extraction. A good name turns code into
   self-documentation.

2. **Copy the extracted code** from the source method into the new target method body.

3. **Scan for references to local variables** in scope in the source method. These are
   local variables declared in the source method and parameters of the source method.

4. **Handle read-only variables:** For variables referenced inside the extracted code but
   declared outside it, and that are not modified inside the extraction, declare them as
   parameters of the new method. Why: these are inputs to the computation the method
   represents; passing them as parameters makes the dependency explicit.

5. **Handle variables declared only inside the extracted code:** Move their declaration into
   the target method. After extraction, remove the original declaration from the source
   method if it no longer appears there.

6. **Handle variables modified inside the extracted code:**
   - If only one variable is modified and it is used after the extraction: have the target
     method return that variable's value; assign the return value in the source method.
   - If more than one variable is modified: you cannot cleanly extract. Either choose
     different extraction boundaries, or apply Replace Temp with Query and Split Temporary
     Variable to reduce the number of modified variables, then try again. As a last resort,
     apply Replace Method with Method Object (Step 6 below).

7. **Pass read variables as parameters** into the new method. Compile.

8. **Compile when you have dealt with all locally scoped variables.**

9. **Replace the extracted code in the source method with a call to the new method.** If
   you moved any temp declarations into the target method, remove their declarations from
   the source method. Compile and test.

**The name heuristic:** If extracting improves clarity, do it — even if the name is longer
than the code you extracted. Fowler: "Length is not the issue. The key is the semantic
distance between the method name and the method body."

---

### Step 4: Handle Parameter Assignment

**ACTION:** If the source method assigns to a parameter variable (not just calling a method
on it, but reassigning the parameter reference itself), apply Remove Assignments to Parameters.

**WHY Remove Assignments to Parameters:** Assigning to a parameter is confusing because it
blurs what the parameter represents (the value passed in) with what the local computation
produces. In pass-by-value languages (Java, Python, most modern languages), assigning to a
parameter only affects the local copy — the caller sees no change — which is a common source
of bugs. Using a temp makes the semantics explicit.

Mechanics:
1. Create a temporary variable for the parameter. Initialize it to the parameter's value.
2. Replace all references to the parameter that appear after the assignment with the temp.
3. Change the assignment to assign to the temp instead of the parameter.
4. Compile and test.

---

### Step 5: Apply Inline Method When Indirection Becomes Noise

**ACTION:** After extraction rounds, if a method's body is as clear as its name — or if you
have a cluster of methods that delegate to each other without adding clarity — inline the
method back into its callers.

**WHY Inline Method:** Extraction can overshoot. A method whose name says exactly what its
one-line body says adds indirection without adding comprehension. Inline Method also prepares
a method for Replace Method with Method Object: inlining all the called methods into the
target method first makes it easier to move the whole behavior into the new class.

Mechanics:
1. Confirm the method is not polymorphic (no subclasses override it). Do not inline if they
   do — subclasses cannot override a method that no longer exists.
2. Find all call sites.
3. Replace each call site with the method body.
4. Compile and test.
5. Remove the method definition.

---

### Step 6: Apply Replace Method with Method Object for Irreducible Tangles

**ACTION:** If after applying Replace Temp with Query and Split Temporary Variable, the
method still has so many local variables that Extract Method cannot be applied cleanly,
convert the entire method into its own class.

**WHY Replace Method with Method Object:** All local variables become fields on the new
class, eliminating the parameter-passing problem entirely. Once the method is an object, you
can apply Extract Method freely on the `compute()` method because all the "parameters" are
already available as fields. This is the escalation path for methods that resist decomposition.

Mechanics:
1. Create a new class. Name it after the method.
2. Give the new class a `final` field for the object that hosted the original method (the
   source object). Give it a field for each parameter and each local variable of the method.
3. Give the new class a constructor that takes the source object and each parameter; assigns
   them to the corresponding fields.
4. Give the new class a method named `compute`.
5. Copy the body of the original method into `compute`. Replace any calls to source object
   methods with calls via the source object field.
6. Compile.
7. Replace the original method's body with: `return new MethodObjectClass(this, param1,
   param2, ...).compute();`
8. Now apply Extract Method freely on `compute()` — local variables are all fields, so
   parameter passing is no longer needed.

---

### Step 7: Apply Substitute Algorithm When a Cleaner Path Exists

**ACTION:** Once the method is decomposed enough to be understood, if the algorithm itself
is unnecessarily complex (a clearer algorithm is known, or a library method already provides
the behavior), replace the algorithm wholesale.

**WHY Substitute Algorithm:** Decomposition makes the algorithm legible enough to evaluate.
Sometimes the algorithm can be replaced with a simpler version (a list lookup instead of
cascading conditionals, a standard library call instead of manual iteration). You can only
substitute safely when the method is small; substituting a large complex algorithm is
unreliable.

Mechanics:
1. Prepare the replacement algorithm so it compiles.
2. Run the test suite with both the old and new algorithm available (comment one out) to
   compare results.
3. If results match, replace permanently. If they differ, use the old algorithm to debug
   which test cases fail.

---

### Step 8: Verify and Review

**ACTION:** Run the full test suite. Read the decomposed methods aloud — can each be
understood from its name alone?

**WHY:** The behavioral contract must be preserved exactly. Reading method names aloud is
the fastest test of whether the extraction produced intention-revealing names: if you need
to look at the body to understand what the method does, the name is still wrong.

**Acceptance criteria for completed decomposition:**
- All tests pass
- The original method body reads like a series of high-level steps, each a method call
- No method requires a comment to explain what it does (the name provides that)
- No extracted method has more than 3-4 parameters (if more, check for missed Replace Temp
  with Query or Introduce Parameter Object opportunities)
- Each extracted method has a single, nameable responsibility

---

## Key Principles

**1. The semantic distance heuristic is the decision rule.**
Do not count lines. Ask: is there a gap between what this method's name says and what its
body does? If the body is implementing "how" at a level of detail that the name abstracts
away, extract the implementation detail into its own method. If the name and body are at the
same level of abstraction, leave it.

**2. Extract Method is the primary technique — the others clear the path to it.**
Replace Temp with Query, Split Temporary Variable, and Introduce Explaining Variable exist
primarily to reduce the local variable count so that Extract Method can proceed. Inline Temp
removes a specific class of obstruction. Remove Assignments to Parameters prevents a subtle
class of confusion that Extract Method would propagate. Replace Method with Method Object is
the escape hatch when all else fails.

**3. Names are the product, not the side effect.**
An extract that produces a well-named method is more valuable than ten extracts that produce
vaguely-named helper methods. If you cannot name the fragment better than the comment
describing it, the comment is not a good extraction signal in that case.

**4. Compile and test after every single step.**
Each refactoring is designed to be applied in tiny, verifiable increments. Testing after
each step means that when something breaks, the cause is obvious — it was the last change.
Batching multiple refactorings before testing makes failures hard to diagnose.

**5. Replace Temp with Query before Extract Method, not after.**
The order matters. Eliminating temps first reduces the parameter list of the extraction.
Extracting first and then trying to eliminate temps in the extracted method is harder because
the scope boundaries have already been drawn.

**6. Performance concerns about query methods are almost always premature.**
Replace Temp with Query introduces repeated method calls that a compiler can optimize or
that prove to be negligible. If performance becomes an issue, a profiler will identify it;
at that point, putting the temp back is trivial. Readable, factored code is worth the
theoretical risk.

---

## Examples

### Example 1: Extract Method with No Local Variable Complications

**Before** — a method with a comment marking an extractable block:

```java
void printOwing() {
    Enumeration e = _orders.elements();
    double outstanding = 0.0;

    // print banner
    System.out.println("**************************");
    System.out.println("***** Customer Owes ******");
    System.out.println("**************************");

    while (e.hasMoreElements()) {
        Order each = (Order) e.nextElement();
        outstanding += each.getAmount();
    }
    System.out.println("name: " + _name);
    System.out.println("amount: " + outstanding);
}
```

The banner block has no local variable dependencies. Extract directly:

```java
void printOwing() {
    printBanner();
    // ... rest of method
}

void printBanner() {
    System.out.println("**************************");
    System.out.println("***** Customer Owes ******");
    System.out.println("**************************");
}
```

---

### Example 2: Replace Temp with Query Unblocking Extract Method

**Before** — `discountFactor` temp blocks clean extraction because `basePrice` is used to
compute it:

```java
double getPrice() {
    int basePrice = _quantity * _itemPrice;
    double discountFactor;
    if (basePrice > 1000) discountFactor = 0.95;
    else discountFactor = 0.98;
    return basePrice * discountFactor;
}
```

**Step 1 — Replace Temp with Query for `basePrice`:**
Declare `final`, extract right-hand side, replace references, remove declaration:

```java
private int basePrice() {
    return _quantity * _itemPrice;
}
```

**Step 2 — With `basePrice` as a query, `discountFactor` can now be extracted:**

```java
double getPrice() {
    return basePrice() * discountFactor();
}

private double discountFactor() {
    if (basePrice() > 1000) return 0.95;
    else return 0.98;
}
```

The final `getPrice()` has zero local variables and reads like a specification.

---

### Example 3: Replace Method with Method Object for an Irreducible Tangle

**Before** — `gamma()` has 3 interacting local variables; any extraction would require
multiple output parameters:

```java
int gamma(int inputVal, int quantity, int yearToDate) {
    int importantValue1 = (inputVal * quantity) + delta();
    int importantValue2 = (inputVal * yearToDate) + 100;
    if ((yearToDate - importantValue1) > 100) importantValue2 -= 20;
    int importantValue3 = importantValue2 * 7;
    return importantValue3 - 2 * importantValue1;
}
```

Create class `Gamma` with a field for the source object and a field for each parameter and
local variable. Add a constructor and a `compute()` method containing the original body.
Replace the original body with `return new Gamma(this, inputVal, quantity, yearToDate).compute();`

Now each fragment of `compute()` can be extracted without passing any parameters — they are
already fields. The `if` block becomes `importantThing()` with no arguments.

---

## Decision Framework: Which Technique When?

```
Long method to decompose
│
├── Does a candidate fragment have zero modified local variables?
│   └── YES → Extract Method directly (pass read-only vars as params)
│
├── Does a candidate fragment have exactly one modified variable?
│   └── YES → Extract Method; return that variable's value
│
├── Does a candidate fragment have 2+ modified variables?
│   ├── Can you change temps to query methods? → Replace Temp with Query first
│   ├── Is a temp used for two different purposes? → Split Temporary Variable first
│   ├── Is a temp trivially assigned from a method call? → Inline Temp first
│   └── Still too many params after all the above? → Replace Method with Method Object
│
├── Is a temp needed only to name a complex sub-expression?
│   └── Prefer Extract Method (reusable) over Introduce Explaining Variable (local)
│   └── Use Introduce Explaining Variable only when extraction is blocked by other vars
│
├── Is the method body as clear as the method name?
│   └── YES → Inline Method (remove the indirection)
│
├── Is a parameter being reassigned inside the method?
│   └── YES → Remove Assignments to Parameters first
│
└── Is the algorithm correct but needlessly complex?
    └── YES → Substitute Algorithm (only after method is small enough to test confidently)
```

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/composing-methods-mechanics.md` | Full step-by-step mechanics for all 9 techniques with edge cases | When a specific technique behaves unexpectedly |
| `references/local-variable-decision-tree.md` | Extended decision tree for local variable classification | When local variable analysis is ambiguous |

**Related skills:**
- `code-smell-diagnosis` — identifies Long Method and points here for execution
- `conditional-simplification-strategy` — simplifies complex conditionals exposed after
  decomposition
- `build-refactoring-test-suite` — create the test safety net if none exists before starting
- `class-responsibility-realignment` — when decomposition reveals that extracted methods
  belong in a different class (Feature Envy)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler and Kent Beck.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-code-smell-diagnosis`
- `clawhub install bookforge-conditional-simplification-strategy`
- `clawhub install bookforge-build-refactoring-test-suite`
- `clawhub install bookforge-class-responsibility-realignment`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
