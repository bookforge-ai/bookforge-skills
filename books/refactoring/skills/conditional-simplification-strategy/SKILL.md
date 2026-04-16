---
name: conditional-simplification-strategy
description: |
  Select and apply the correct refactoring for complex or tangled conditional logic. Use when: a method has a complicated if-then-else that obscures why branching happens (not just what happens); a series of conditions all produce the same result; the same code fragment appears inside every branch; a boolean variable is being used as a control flag to track loop state; nested conditionals bury the normal execution path under special-case checks; a switch statement (or long if-else-if chain) branches on an object's type and new types are expected; a method's parameter controls which of several distinct operations runs; null checks are scattered throughout client code for the same object. Covers all 8 conditional refactorings from Fowler Chapter 9: Decompose Conditional, Consolidate Conditional Expression, Consolidate Duplicate Conditional Fragments, Remove Control Flag, Replace Nested Conditional with Guard Clauses, Replace Conditional with Polymorphism, Replace Parameter with Explicit Methods, Introduce Null Object. Also covers the supporting technique Introduce Assertion for making implicit state assumptions explicit. Includes the key semantic distinction between guard clauses (rare special cases that exit) and if-else (equal-weight alternatives), and Fowler's rejection of the single-exit-point rule as a reason to avoid early returns.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/conditional-simplification-strategy
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - code-smell-diagnosis
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler", "Kent Beck"]
    chapters: [9]
tags: [refactoring, code-quality, conditionals, polymorphism]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source code containing the conditional logic to refactor — the primary input"
    - type: document
      description: "Code snippet or method body if no live codebase is accessible"
  tools-required: [Read, Grep, Write, Edit]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory. Reading source files and grepping for related conditionals is the primary analysis method."
discovery:
  goal: "Identify which of the 8 conditional refactorings applies to the target conditional; execute the selected refactoring correctly; leave the code with conditional logic that clearly separates the reason for branching from the details of each branch"
  tasks:
    - "Read the target conditional and classify its structural problem"
    - "Select the correct refactoring using the decision framework"
    - "Apply the refactoring mechanics step by step, compiling and testing after each step"
    - "Verify the result: is the normal path visible? Does each branch communicate intent, not just action?"
  audience:
    roles: ["software-developer", "senior-developer", "tech-lead"]
    experience: "intermediate — assumes working knowledge of object-oriented programming and refactoring basics"
  triggers:
    - "A method has a complex if-then-else that requires re-reading to understand"
    - "Switch Statements smell is diagnosed by code-smell-diagnosis"
    - "Nested conditionals hide which execution path is the normal one"
    - "Null checks for the same object appear in multiple client code locations"
    - "A control flag (boolean tracking loop state) makes loop termination logic hard to read"
  not_for:
    - "Performance optimization — use profiling-driven-performance-optimization instead"
    - "Type code refactoring decisions — use type-code-refactoring-selector for the full type code decision tree"
    - "General code smell diagnosis — use code-smell-diagnosis first to identify which conditional problem is present"
    - "Conditionals that are simple, stable, and clear — not every conditional needs refactoring"
---

# Conditional Simplification Strategy

## When to Use

You have conditional logic that is hard to read, hard to extend, or hiding its own intent. This includes:

- A method-level conditional where the condition checks multiple things but the code only tells you *what* happens, not *why* the branching exists
- Several separate conditions that all produce the same result, scattered as sequential checks
- The same code fragment repeated in every branch of a conditional
- A boolean variable toggled to control loop exit — the code is structuring state instead of expressing intent
- Nested if-else blocks where finding the "normal" path requires reading through multiple levels of special cases
- A switch (or long if-else-if chain) that dispatches behavior based on an object's type, and new types are expected
- Null checks for the same object in multiple client methods

**The core insight from Fowler:** Conditional logic has two parts — the *switching logic* (which path to take) and the *details* of what each path does. When these are mixed inside the same method body, the reader must decode both simultaneously. The refactorings in this chapter separate these concerns so each part is named and readable on its own.

**This skill depends on diagnosis.** If you arrived here from `code-smell-diagnosis` with a Switch Statements finding, use the decision framework in Step 1 to select the right refactoring. If you have a simpler conditional problem (not a Switch Statements smell), the framework also applies — start with the pattern that matches your code structure.

---

## Context and Input Gathering

### Required Input

- **The target conditional.** Either a file path + method name, or a pasted code block. Why: the selection framework requires reading the actual structure — the number of conditions, whether they share results, what the branches do, whether the type drives behavior in multiple places.

- **Whether the conditional appears in multiple places.** Ask or grep. Why: a conditional that switches on a type in one method might be the right candidate for Replace Parameter with Explicit Methods; the same switch appearing in five methods is the right candidate for Replace Conditional with Polymorphism. Location multiplicity changes the prescription.

### Observable Context (gather before asking)

```
Signals to grep for before reading the code:
  - Same variable in switch/case across multiple files: grep for the type constant names
  - Null checks: grep for "== null" or "!= null" on the same variable
  - Control flags: grep for boolean variables set to true/false inside loop bodies
  - Identical tail code in branches: visually scan each branch body for repeated statements
```

---

## Process

### Step 1: Classify the Conditional and Select the Refactoring

**ACTION:** Read the target conditional and match it to the pattern below. Use the first match that fits — the patterns are ordered from simplest to most structural.

**WHY:** The 8 refactorings are not interchangeable. Applying Decompose Conditional when the real problem is type-based dispatch produces a cleaner conditional that still grows incorrectly when types are added. Applying Replace Conditional with Polymorphism when there are only two stable cases and one method creates unnecessary class hierarchy. Selecting the right refactoring requires classifying the structural problem first.

---

#### Pattern 1: The condition expression itself is complex

**Signal:** The condition in the `if` statement (or the `else if`) is a multi-part boolean expression that requires re-reading to understand. The branch bodies may be simple. The *condition* is the hard part, not the branch logic.

**Refactoring: Decompose Conditional**

Extract the condition, the then-part, and the else-part into their own methods. Name the methods after *why* the branching happens, not *what* the expressions compute.

```
Before:
  if (date.before(SUMMER_START) || date.after(SUMMER_END))
      charge = quantity * _winterRate + _winterServiceCharge;
  else charge = quantity * _summerRate;

After:
  if (notSummer(date))
      charge = winterCharge(quantity);
  else charge = summerCharge(quantity);
```

Why this matters: `notSummer(date)` conveys the *intent* of the condition; the expression `date.before(SUMMER_START) || date.after(SUMMER_END)` conveys the *mechanics*. The method name reads like a comment that cannot go stale.

**Note:** If you find a nested conditional during Decompose Conditional, first check whether Replace Nested Conditional with Guard Clauses (Pattern 5) applies — guard clauses may eliminate the nesting before you need to decompose it.

---

#### Pattern 2: Multiple separate conditions all produce the same result

**Signal:** A sequence of `if` statements (or early `return 0;` checks) where each check is different but all lead to the same action. The checks feel like they belong together.

**Refactoring: Consolidate Conditional Expression, then Extract Method**

Step 1 — Verify no side effects exist in any condition (if side effects are present, consolidation is not safe).
Step 2 — Combine the checks into a single conditional using `||` (or `&&` for and-chains).
Step 3 — Apply Extract Method to give the combined condition a meaningful name.

```
Before:
  if (_seniority < 2) return 0;
  if (_monthsDisabled > 12) return 0;
  if (_isPartTime) return 0;
  // compute disability amount

After:
  if (isNotEligibleForDisability()) return 0;
  // compute disability amount
```

Why this matters: The three separate checks *communicate* that they are independent decisions. They are not — they are three ways of saying "this person does not qualify." The consolidated version makes the semantic unity visible and names it. Extract Method also sets up the consolidated check to be reused or overridden cleanly.

---

#### Pattern 3: The same code appears inside every branch

**Signal:** Looking at each branch of the conditional, you see the same statement (or statements) at the start or end of every branch. The code executes regardless of which branch is taken.

**Refactoring: Consolidate Duplicate Conditional Fragments**

Move the common code to before the conditional (if it appears at the start of all branches) or after (if it appears at the end of all branches).

```
Before:
  if (isSpecialDeal()) {
      total = price * 0.95;
      send();
  } else {
      total = price * 0.98;
      send();
  }

After:
  if (isSpecialDeal())
      total = price * 0.95;
  else
      total = price * 0.98;
  send();
```

Why this matters: Code inside both branches implies the branching decision controls it. Moving it out makes clear that the conditional only determines the price multiplier — `send()` always happens. This reduces duplication and makes the conditional's scope accurate.

If the common code is in the middle of branches (not at start or end), check whether the code before or after it changes anything, then move it to whichever end is safe. If more than one statement is common, extract them into a method.

---

#### Pattern 4: A boolean variable tracks when to stop processing

**Signal:** A variable (`found`, `done`, `flag`) initialized to `false` before a loop, set to `true` inside the loop to signal when to stop, and checked in the loop condition or inside the loop body to skip further processing. The variable exists to work around a single-exit-point constraint, not because the logic requires it.

**Refactoring: Remove Control Flag**

Replace the control flag with a `break` or `return` statement.

- If the flag only controls loop exit (no result value carried): replace `flag = true` with `break` inside the loop, then remove the flag and its condition check.
- If the flag also carries a result value: extract the loop into its own method; replace `flag = result_value` with `return result_value`; the method returns the found value directly.

```
Before:
  boolean found = false;
  for (int i = 0; i < people.length; i++) {
      if (!found) {
          if (people[i].equals("Don")) { sendAlert(); found = true; }
          if (people[i].equals("John")) { sendAlert(); found = true; }
      }
  }

After (with break):
  for (int i = 0; i < people.length; i++) {
      if (people[i].equals("Don")) { sendAlert(); break; }
      if (people[i].equals("John")) { sendAlert(); break; }
  }
```

Why this matters: The control flag is an artifact of structured programming's one-exit-point rule. Fowler rejects this rule: "Clarity is the key principle. If the method is clearer with one exit point, use one; otherwise don't." The `break` or `return` directly expresses the intent — stop processing when the condition is met — without requiring the reader to track an extra variable's state across iterations.

Prefer the `return` approach (extract into a method) even in languages that support `break`, because `return` makes it clear that no further code in the method executes after the match is found.

---

#### Pattern 5: Nested conditionals hide the normal execution path

**Signal:** A method with nested if-else blocks where the "normal" case — the path that runs for the typical, non-exceptional input — is buried inside `else` clauses. Reading the method requires tracking multiple nesting levels to find the main path. The branches before the normal case handle unusual or error conditions.

**Refactoring: Replace Nested Conditional with Guard Clauses**

For each unusual condition, replace its `else` wrapper with a guard clause: a check at the top of the method that returns (or throws) immediately if the unusual condition is true. The normal path falls through to the end.

```
Before:
  double getPayAmount() {
      double result;
      if (_isDead) result = deadAmount();
      else {
          if (_isSeparated) result = separatedAmount();
          else {
              if (_isRetired) result = retiredAmount();
              else result = normalPayAmount();
          }
      }
      return result;
  }

After:
  double getPayAmount() {
      if (_isDead) return deadAmount();
      if (_isSeparated) return separatedAmount();
      if (_isRetired) return retiredAmount();
      return normalPayAmount();
  }
```

**The critical semantic distinction:** An `if-else` construct communicates that both branches are *equally likely and equally important* — the reader gives equal weight to each leg. A guard clause communicates "this is rare and exceptional — handle it and get out." The if-else form is wrong for special cases because it visually equalizes things that are not equal in the domain.

Fowler: "The guard clause says, 'This is rare, and if it happens, do something and get out.'"

**Reversing conditions:** When the nesting goes the other way (the method does something only when conditions are all satisfied), reverse each condition to get the guard. Negate the condition, add the guard clause with an early return, remove the outer if wrapper.

Apply guard clauses one at a time. Compile and test after each replacement.

---

#### Pattern 6: A switch (or if-else-if chain) branches on object type and new types are expected

**Signal:** A `switch` statement (or a chain of `if (type == X) ... else if (type == Y)`) selects different behavior depending on the type of an object. The same switch appears in multiple methods, or the type set is expected to grow. Adding a new type means finding every switch and adding a case.

**Refactoring: Replace Conditional with Polymorphism**

Move each leg of the conditional into an overriding method on a subclass. Make the original method abstract on the superclass.

Prerequisites: You need an inheritance hierarchy. If one does not exist, create it first using Replace Type Code with Subclasses (if the type does not change after object creation) or Replace Type Code with State/Strategy (if the type changes at runtime, or if the class is already subclassed for another reason).

Once the hierarchy exists:
1. If the conditional is part of a larger method, use Extract Method to isolate it.
2. Use Move Method to place the conditional on the class at the top of the hierarchy.
3. For each leg of the conditional: copy the leg body into an overriding method on the appropriate subclass. Compile and test. Remove the copied leg from the original switch. Repeat until all legs are removed.
4. Declare the superclass method abstract.

```
Before (in EmployeeType):
  int payAmount(Employee emp) {
      switch (getTypeCode()) {
          case ENGINEER:  return emp.getMonthlySalary();
          case SALESMAN:  return emp.getMonthlySalary() + emp.getCommission();
          case MANAGER:   return emp.getMonthlySalary() + emp.getBonus();
          default: throw new RuntimeException("Incorrect Employee");
      }
  }

After:
  class Engineer...    int payAmount(Employee emp) { return emp.getMonthlySalary(); }
  class Salesman...    int payAmount(Employee emp) { return emp.getMonthlySalary() + emp.getCommission(); }
  class Manager...     int payAmount(Employee emp) { return emp.getMonthlySalary() + emp.getBonus(); }
  abstract class EmployeeType...  abstract int payAmount(Employee emp);
```

**The polymorphism principle:** The caller does not need to know about the conditional behavior. Adding a new variant means adding a new class and implementing its method — the caller never changes. This is the reason object-oriented programs have fewer switch statements than procedural programs: the dispatch is handled by the language's method resolution mechanism rather than by explicit code.

**When NOT to use polymorphism:** If the conditional appears in only one place, affects only one method, and the type set is stable (not expected to grow), the structural investment of a hierarchy may not be justified. In that case, consider Pattern 7 (Replace Parameter with Explicit Methods) instead.

---

#### Pattern 7: A parameter controls which of several distinct operations runs, in a single method

**Signal:** A method takes a parameter (often a string, constant, or boolean) and uses it to select between a small number of clearly distinct operations. Each branch of the conditional does something completely different. The method's behavior is determined entirely by the parameter value, and the callers always pass a literal value (never a computed one). The type set is stable — no new variants are expected.

**Refactoring: Replace Parameter with Explicit Methods**

Create a separate method for each value of the parameter. Delete the conditional dispatch method. Update each call site to call the appropriate explicit method directly.

```
Before:
  void setValue(String name, int value) {
      if (name.equals("height")) _height = value;
      if (name.equals("width"))  _width = value;
  }
  // callers:  setValue("height", 10);  setValue("width", 5);

After:
  void setHeight(int value) { _height = value; }
  void setWidth(int value)  { _width = value; }
  // callers:  setHeight(10);  setWidth(5);
```

Why this matters: The explicit methods are statically checkable — the compiler catches invalid parameter names. Each method has a clear, single purpose. Callers communicate intent directly in the method name rather than encoding it in a string argument.

**Condition for use:** Only apply this when callers always pass a literal constant — never a variable. If callers compute the parameter value at runtime (e.g., passing a value from user input or a database), the callers need the dispatching method and you cannot eliminate it.

---

#### Pattern 8: Null checks for the same object appear in multiple client methods

**Signal:** Multiple methods in client code contain checks of the form `if (object == null) do default thing; else object.doRealThing()`. The same default behavior is repeated wherever the object might be null. The null-handling is scattered rather than centralized.

**Refactoring: Introduce Null Object**

Create a null version of the class that implements the same interface and returns sensible default values for all methods. Replace null with instances of this null class. Client code stops checking for null and calls methods directly.

Step 1 — Create a subclass (or implement a Nullable interface) as the null version of the source class. Add an `isNull()` method that returns `true` on the null class and `false` on the real class.
Step 2 — Find all places that return null for the source type. Return an instance of the null class instead.
Step 3 — Find all `== null` checks on the source type. Replace each with `isNull()`. Compile and test incrementally — replace one source at a time.
Step 4 — For each check of the form `if (obj.isNull()) defaultValue; else obj.realBehavior()`: add the appropriate method to the null class returning `defaultValue`. Remove the condition. Client code calls `obj.realMethod()` unconditionally.

```
Before (in clients):
  if (customer == null) plan = BillingPlan.basic();
  else plan = customer.getPlan();

  if (customer == null) name = "occupant";
  else name = customer.getName();

After (NullCustomer.getName() returns "occupant", NullCustomer.getPlan() returns BillingPlan.basic()):
  plan = customer.getPlan();
  name = customer.getName();
```

Why this matters: The essence of polymorphism is that you ask an object to do something and it does the right thing based on its type — you do not ask what type it is first. Null objects extend this principle: the null object knows how to behave when it is absent, so the caller never needs to check. The repeated conditional is eliminated at the source, not patched at each call site.

**When to prefer isNull() over null:** Null objects work well when most clients want the same default behavior. Clients that need a different response can still call `isNull()` explicitly. Use this refactoring when the default behavior is shared across many clients.

---

### Step 2: Apply the Selected Refactoring

**ACTION:** Execute the mechanics for the selected refactoring, one small step at a time. Compile and test after each step.

**WHY:** Conditional refactorings are behavior-preserving transformations. Testing after each individual step (not after all steps) means any regression has a minimal search space — you know exactly which change caused it. Skipping intermediate tests and making all changes at once turns a refactoring session into a debugging session.

**Mechanics rule for all 8 refactorings:** Use Extract Method liberally. Extracting any condition, branch body, or common fragment into a named method is always safe (it is behavior-preserving) and always improves readability. When in doubt, extract.

---

### Step 3: Introduce Assertion for Implicit Assumptions (supporting technique)

**ACTION:** After refactoring the conditional, scan the remaining code for implicit assumptions — places where the code works only if some state is true, but that state is not checked or documented.

**WHY:** Assertions make assumptions explicit. They do not change behavior (a failing assertion produces the same exception the code would throw anyway, just closer to the source). They serve as communication: the reader immediately sees what the code requires, rather than decoding the algorithm to discover it. They also help debugging by catching violated assumptions near the violation point rather than downstream.

When to add an assertion:
- A method assumes at least one of several fields has a non-null or non-sentinel value
- A calculation assumes an input is positive (or within a range)
- A method assumes an object has been initialized before being called

```
Before (implicit):
  double getExpenseLimit() {
      // should have either expense limit or a primary project
      return (_expenseLimit != NULL_EXPENSE) ?
          _expenseLimit : _primaryProject.getMemberExpenseLimit();
  }

After (explicit):
  double getExpenseLimit() {
      Assert.isTrue(_expenseLimit != NULL_EXPENSE || _primaryProject != null);
      return (_expenseLimit != NULL_EXPENSE) ?
          _expenseLimit : _primaryProject.getMemberExpenseLimit();
  }
```

Assertions should be easily removable for production deployment. Use an assertion utility class rather than live `if` statements for assertion logic. Do not use assertions to check things that are not truly required — over-asserting creates duplicate logic that drifts from the real code. The test: if the assertion fails and the code still works correctly, the assertion is wrong.

---

## Key Principles

**1. Separate the switching logic from the branch details.**
A conditional should tell you *why* branching happens. The branch bodies should tell you *what* happens in each case. When both are mixed in one method, Extract Method to split them apart. The condition becomes a method call with a meaningful name; the branch bodies become method calls with meaningful names. The if-else statement is now pure routing logic.

**2. Guard clauses are semantically different from if-else.**
Using `if-else` when one branch is a special case is incorrect code communication — it tells the reader both paths are equally probable and important. Guard clauses (early returns) correctly communicate "this is exceptional; handle it and exit." Fowler explicitly rejects the single-exit-point rule: "Clarity is the key principle."

**3. Adding types should not require finding conditionals.**
If adding a new variant of a type requires searching the codebase for every switch on that type and adding a case, Replace Conditional with Polymorphism. The polymorphic design means adding a new type = adding a new class that implements the behavior. No existing code changes. The caller does not need to know about type-specific conditional behavior.

**4. Null objects eliminate scattered default behavior.**
Null checks are repeated default-behavior decisions. When many callers share the same default, the decision belongs in the object, not in every caller. The null object embodies the default; callers stop making the decision.

**5. Apply one refactoring at a time, test between each.**
Conditional refactorings often chain — Consolidate Conditional Expression followed by Extract Method; Replace Conditional with Polymorphism preceded by Replace Type Code with Subclasses. Apply each step independently, verify behavior is preserved, then proceed. The chain is safe; the leap is not.

---

## Examples

### Example 1: Choosing Between Polymorphism and Explicit Methods

**Scenario:** A `Shape` class has this method:

```java
double area(String shapeType) {
    if (shapeType.equals("circle"))    return Math.PI * _radius * _radius;
    if (shapeType.equals("rectangle")) return _width * _height;
    if (shapeType.equals("triangle"))  return 0.5 * _base * _height;
    throw new RuntimeException("Unknown shape");
}
```

Two questions determine the refactoring:

1. Does `shapeType` vary at runtime (computed value), or is it always a literal at call sites?
2. Are new shape types expected?

**If both answers are yes:** Pattern 6 — Replace Conditional with Polymorphism. Create `Circle`, `Rectangle`, `Triangle` subclasses; each implements `area()`. Adding `Pentagon` = adding a class.

**If the type set is stable and callers always pass literals:** Pattern 7 — Replace Parameter with Explicit Methods. Create `circleArea()`, `rectangleArea()`, `triangleArea()` methods. Simpler, statically checkable, no hierarchy overhead.

**Decision rule:** When types will grow or the conditional appears in multiple places → polymorphism. When types are fixed, the conditional is in one place, and callers always pass constants → explicit methods.

---

### Example 2: Identifying a Null Object Opportunity

**Scenario:** Three separate methods in client code contain:

```java
if (customer == null) plan = BillingPlan.basic();
else plan = customer.getPlan();

if (customer == null) name = "occupant";
else name = customer.getName();

if (customer == null) weeksDelinquent = 0;
else weeksDelinquent = customer.getHistory().getWeeksDelinquentInLastYear();
```

**Classification:** Pattern 8 — the same object (`customer`) is null-checked in multiple clients, each providing a sensible default.

**Apply Introduce Null Object:**

```java
class NullCustomer extends Customer {
    public boolean isNull()          { return true; }
    public String getName()          { return "occupant"; }
    public BillingPlan getPlan()     { return BillingPlan.basic(); }
    public PaymentHistory getHistory() { return PaymentHistory.newNull(); }
}
// class NullPaymentHistory: getWeeksDelinquentInLastYear() returns 0

// Site returns NullCustomer instead of null:
Customer getCustomer() {
    return (_customer == null) ? Customer.newNull() : _customer;
}

// Clients become:
plan            = customer.getPlan();
name            = customer.getName();
weeksDelinquent = customer.getHistory().getWeeksDelinquentInLastYear();
```

The three conditional blocks disappear. Note that null objects often return other null objects — `NullCustomer.getHistory()` returns `NullPaymentHistory`, which itself returns sensible defaults.

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/refactoring-prescriptions.md` | Full prescription tree for all conditional refactorings with Fowler chapter references | Verifying the correct conditional branch for a borderline case |

**Dependency skill:**
- `code-smell-diagnosis` — diagnoses the Switch Statements smell and other structural problems that trigger this skill; provides the prioritized finding that this skill executes

**Related skills in the refactoring set:**
- `type-code-refactoring-selector` — when the conditional is driven by a type code and the primary decision is how to restructure the type (Replace Type Code with Subclasses vs. State/Strategy), not just the conditional dispatch
- `method-decomposition-refactoring` — when Long Method is the primary smell and conditional complexity is one contributor among several

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler and Kent Beck.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-code-smell-diagnosis`
- `clawhub install bookforge-type-code-refactoring-selector`
- `clawhub install bookforge-method-decomposition-refactoring`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
