---
name: type-code-refactoring-selector
description: |
  Select and execute the correct refactoring path for type codes — enumerations, integer constants, or string tags that flag object variants (e.g., ENGINEER/SALESMAN/MANAGER as ints, blood group as 0/1/2/3, ORDER_STATUS as strings). Applies Fowler's three-way decision tree to pick between Replace Type Code with Class, Replace Type Code with Subclasses, and Replace Type Code with State/Strategy, then drives the full mechanics for the chosen path through to Replace Conditional with Polymorphism. Use when: a class stores an integer or enum constant that controls conditional behavior in switch statements or if-else chains scattered across multiple methods or callers; Primitive Obsession or Switch Statements smells have been diagnosed and the root cause is a type code; a new variant keeps requiring edits in multiple places (classic signal that polymorphism is needed); a type code is passed between classes as a raw integer, weakening type safety and allowing invalid values; subclasses exist that vary only in constant return values (reverse path: Replace Subclass with Fields). Also covers the exceptions: use Replace Parameter with Explicit Methods instead of polymorphism when the switch affects only a single method and variants are stable; use Introduce Null Object when one of the cases is null.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/type-code-refactoring-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - code-smell-diagnosis
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler", "Kent Beck"]
    chapters: [3, 8]
tags: [refactoring, code-quality, type-codes, polymorphism]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source code containing the type code — the class that holds the integer/enum constant and the methods that switch on it"
    - type: document
      description: "Code snippet or class description if no live codebase is accessible"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory. Reading source files and grepping for switch/case patterns on the type code are the primary analysis methods."
discovery:
  goal: "Correctly route a type code to one of three replacement paths; execute the full mechanics for the chosen path; eliminate the original conditional branching with polymorphism"
  tasks:
    - "Identify the type code: the field, its values, and the class that holds it"
    - "Determine whether the type code affects behavior (switch/if-else chains that execute different code per value)"
    - "If behavior-affecting: determine whether the class can be subclassed (no existing inheritance blocking it, and the type value does not change after object creation)"
    - "Select and execute the correct path: Replace Type Code with Class, Replace Type Code with Subclasses, or Replace Type Code with State/Strategy"
    - "Complete the follow-up: Replace Conditional with Polymorphism on all switch statements that remain"
    - "Apply exceptions where polymorphism is overkill or a null case is present"
  audience:
    roles: ["software-developer", "senior-developer", "tech-lead"]
    experience: "intermediate — assumes working knowledge of object-oriented design and subclassing"
  triggers:
    - "Switch statement or if-else chain that branches on a type code integer or enum constant"
    - "Adding a new variant requires editing multiple switch statements in multiple places"
    - "Primitive Obsession or Switch Statements smell diagnosed and traced to a type code"
    - "Type code is passed between classes as a raw integer, allowing invalid values"
    - "Subclasses vary only in constant return values (reverse path trigger)"
  not_for:
    - "Conditionals that do not involve a type code — use conditional-simplification-strategy instead"
    - "Structural smells not related to type codes (Feature Envy, Shotgun Surgery, etc.) — use class-responsibility-realignment instead"
    - "New code being written from scratch — this skill refactors existing type codes"
---

# Type Code Refactoring Selector

## When to Use

You have a class that stores a type code: an integer constant, an enum, or a string tag whose value identifies which variant of the object this is. The code switches on this value in multiple places — different methods, different callers — and adding a new variant means hunting down every switch and adding a case.

This skill applies when:
- A `switch (_type)` or `if (type == ENGINEER)` pattern recurs across the codebase, driven by the same type code field
- The `code-smell-diagnosis` skill has named Switch Statements or Primitive Obsession and the underlying cause is a type code
- A new business variant (new employee role, new payment method, new order state) keeps requiring edits in multiple places
- The type code is passed as a raw `int` — the compiler cannot enforce valid values, and callers can pass arbitrary numbers

**The core insight from Fowler:** Polymorphism eliminates the need to know which variant you have. Instead of asking "what type are you?" and branching, you call a method and each variant answers differently. But to reach polymorphism, you first need the right structural foundation — and which foundation you build depends on two criteria: does the type code affect behavior, and can the class be subclassed?

**Upstream dependency:** `code-smell-diagnosis` identifies the smell. This skill executes the remedy once Switch Statements or Primitive Obsession (type code variant) has been diagnosed.

**Downstream:** After this skill, use `conditional-simplification-strategy` if any complex conditionals remain that are not type-code-driven.

---

## Context and Input Gathering

### Required Input (ask if missing)

- **The class holding the type code.** File path or class name. Why: the mechanics work on the class that owns the type code field and its accessors. Everything else is found from there.
- **The type code field and its values.** Name of the field; the named constants and their meanings (e.g., `ENGINEER = 0`, `SALESMAN = 1`, `MANAGER = 2`). Why: each value becomes either a subclass or a state object; knowing the full value set before starting prevents incomplete refactoring.

### Observable Context (gather before asking)

Grep for the type code to map the full scope before choosing a path:

```
Search targets:
  - The type code field name across all files → how many switch sites are there?
  - switch (_type) or if (type == X) patterns → do they affect behavior or just read the value?
  - The class's extends clause → does it already have a superclass?
  - Setter methods on the type code → does the type change after object creation?
  - Subclasses of the class → are there existing subclasses for another reason?
```

### Default Assumptions

- If the type code is only read (no switch statements execute different logic per value): treat as non-behavior-affecting → Path A
- If it is unclear whether the type changes at runtime: check for setter methods on the type field. Presence of a setter = mutable type = cannot use subclasses → Path C
- If the class already extends another class: cannot add a second superclass in single-inheritance languages → Path C

---

## The Three-Way Decision Tree

```
Does the type code drive different behavior?
(switch statements / if-else chains execute different code per value)
│
├── NO ──→ PATH A: Replace Type Code with Class
│          (type code is pure data — used for identity/classification only,
│           no conditional branching on its value)
│
└── YES
    │
    Can the class be subclassed?
    (No existing inheritance blocking it AND type value does not change
     after the object is created — no setter on the type field)
    │
    ├── YES ──→ PATH B: Replace Type Code with Subclasses
    │           (simplest path — the class itself grows subclasses,
    │            one per type code value)
    │
    └── NO ──→ PATH C: Replace Type Code with State/Strategy
                (class already subclassed for another reason, OR
                 type value changes at runtime — use a state object
                 that holds the variant behavior instead)
```

**State vs. Strategy sub-decision (within Path C):**
- Simplifying a **single algorithm** with Replace Conditional with Polymorphism → name it **Strategy** (behavior is the unit being varied)
- Object feels like it **transitions between states** at runtime (e.g., an order moves from PENDING to SHIPPED to DELIVERED) → name it **State** (object identity is the unit being varied)
- Mechanically identical — the naming reflects intent, not structure

---

## Process

### Step 1: Identify and Scope the Type Code

**ACTION:** Read the class holding the type code. Grep for the type code constants and field name across the entire codebase.

**WHY:** A type code refactoring that only touches the host class and misses switch statements in callers produces an inconsistent codebase — old integer-based calls mixed with new class-based ones. The full scope must be known before any transformation begins.

**Identify:**
1. The type code field (`private int _type`, `private String status`, etc.)
2. All named constant values and their meanings
3. Every location in the codebase that switches on or compares against this field
4. Whether those locations execute different behavior per value (not just format or display the value)
5. Whether the field has a setter (mutable = cannot subclass directly)
6. Whether the host class already extends another class

**Output of this step:** A table like:

```
Type code field: Employee._type
Values: ENGINEER(0), SALESMAN(1), MANAGER(2)
Switch sites:
  - Employee.payAmount() — behavioral (different pay calculation per type)
  - ReportGenerator.formatTitle() — behavioral (different title per type)
  - EmployeeDAO.save() — non-behavioral (writes type code as integer to DB)
Type mutable: YES (setType() method exists) → cannot use subclasses
Host class inherits: NO
Decision: PATH C — Replace Type Code with State/Strategy
```

---

### Step 2: Route to the Correct Path

**ACTION:** Apply the decision tree using the observations from Step 1. Select Path A, B, or C.

**WHY:** Each path produces a fundamentally different structure. Applying Path B (subclasses) when the type changes at runtime will break the object model — an object cannot change its class. Applying Path A when the type code drives behavior leaves the switch statements in place and produces no improvement. The routing decision is the highest-leverage moment in this skill.

**Decision criteria (in order):**

1. Are there switch statements or if-else chains that execute different code depending on the type code's value?
   - No → Path A
   - Yes → continue to criterion 2

2. Does the type code field have a setter, or does the host class already extend another class?
   - No setter AND no existing superclass → Path B
   - Setter exists OR existing superclass → Path C

**Exception checks (apply before executing the chosen path):**

- **Polymorphism overkill:** If the switch affects only a single method and the variants are not expected to grow — use Replace Parameter with Explicit Methods instead of the full type code replacement. Signal: the type code appears in only one switch in one method, and the method's callers already know which variant they want.
- **Null case:** If one of the cases in the switch is `null` — apply Introduce Null Object for that case before or alongside the main path.

---

### Step 3A: Path A — Replace Type Code with Class

**Precondition:** Type code is pure data — no switch statements execute different behavior per value.

**WHY this path:** The compiler sees integers, not type names. Any integer can be passed, including invalid ones. Replacing the integer with a class gives the compiler the ability to enforce valid values at call sites. It also creates a home for behavior that belongs to the type (Move Method opportunities).

**Mechanics:**

1. **Create the type code class.**
   - Name it after the concept the type code represents (e.g., `BloodGroup`, `EmployeeType`)
   - Give it a private integer field `_code` that stores the underlying value
   - Add a private constructor taking the integer code
   - Add static final instances for each value: `public static final BloodGroup O = new BloodGroup(0);`
   - Add a private static array `_values` to map integers to instances
   - Add a public static factory method `code(int arg)` that returns the correct instance from `_values`
   - Add a public `getCode()` method that returns the integer (needed during the transition)

2. **Modify the host class to use the new type.**
   - Change the type of the field from `int` to the new class
   - Keep old integer-based constants pointing at `NewClass.INSTANCE.getCode()` so existing callers still compile
   - Update the constructor and any setter to use `NewClass.code(intArg)` to convert incoming integers
   - Compile and test — this is a safe checkpoint

3. **Migrate callers one by one.**
   - For each caller using the integer constants: change to use the new class's static instances (`BloodGroup.O` instead of `Person.O`)
   - For each caller using the integer getter: change to use the new class-returning getter
   - Rename the old integer getter before adding the new class getter to make the transition visible: `getBloodGroupCode()` (old) → `getBloodGroup()` (new, returns `BloodGroup`)
   - Compile and test after each caller is updated

4. **Remove the old integer interface.**
   - Once all callers use the new class, remove the integer-based constants, the integer-based getter, and the integer-based constructor
   - Privatize `getCode()` on the type class — it is now an implementation detail
   - Compile and test

**Alert:** Even if the type code does not cause different behavior in switch statements, check whether any behavior would be better placed on the new type code class. Apply Move Method for any method that primarily operates on the type value.

---

### Step 3B: Path B — Replace Type Code with Subclasses

**Precondition:** Type code drives behavior (switch statements exist) AND the type value is immutable after object creation AND the host class has no existing superclass blocking subclassing.

**WHY this path:** The simplest path to polymorphism. Each type code value becomes a subclass of the host class. The subclasses override the type code getter to return their specific value (a temporary measure), then the switch statements are replaced with polymorphic method dispatch. Knowledge of which variant you have moves from callers into the class itself.

**Mechanics:**

1. **Self-encapsulate the type code.**
   - Add a getter method for the type code field if one does not exist: `int getType() { return _type; }`
   - Replace all direct field access in the host class with calls to the getter
   - Why: subclasses will override the getter; direct field access would bypass the override

2. **Replace the constructor with a factory method** (if the type code is passed to the constructor).
   - Create a static factory: `static Employee create(int type) { return new Employee(type); }`
   - Make the constructor private
   - Update all callers to use the factory — compile and test
   - Why: once there are subclasses, the factory will instantiate the correct subclass. The constructor cannot be made to return a subclass instance.

3. **Create one subclass per type code value.**
   - For each value (ENGINEER, SALESMAN, MANAGER): create a subclass that overrides the type code getter to return the hard-coded value
   ```java
   class Engineer extends Employee {
     int getType() { return Employee.ENGINEER; }
   }
   ```
   - Update the factory method to return the correct subclass per value:
   ```java
   static Employee create(int type) {
     if (type == ENGINEER) return new Engineer();
     else if (type == SALESMAN) return new Salesman();
     // etc.
   }
   ```
   - Compile and test after adding each subclass

4. **Remove the type code field from the superclass.**
   - Once all subclasses override the getter, the field in the superclass is unused
   - Remove the field; declare `getType()` abstract in the superclass
   - Compile and test

5. **Apply Replace Conditional with Polymorphism** (Step 4 below) on all switch statements that remain.

6. **Push down type-specific features.**
   - Use Push Down Method and Push Down Field on any methods or fields that are only relevant to certain subclasses
   - These are now clearly expressed by being in the subclass rather than guarded by a type code check

---

### Step 3C: Path C — Replace Type Code with State/Strategy

**Precondition:** Type code drives behavior (switch statements exist) AND either (a) the type value changes at runtime (mutable type), OR (b) the host class already has a superclass.

**WHY this path:** Path B requires the host class to be extended. When that is not possible — the host already has a superclass (single inheritance), or the type changes during the object's lifetime — the polymorphic behavior must live in a separate object. The host class delegates to a state/strategy object, which can be swapped at runtime without changing the host object's class.

**Mechanics:**

1. **Self-encapsulate the type code.**
   - Add getter and setter for the type code field if not present
   - Replace all direct field access in the host class with calls to the getter/setter
   - Why: the getter and setter will be redirected to delegate to the state object in step 4

2. **Create the state/strategy abstract class.**
   - Name it after the purpose of the type code (e.g., `EmployeeType` for an employee type code)
   - Declare an abstract method to return the type code: `abstract int getTypeCode();`
   - Why: the host class's existing getter will delegate to this method; all callers of the host's getter continue to work unchanged

3. **Create one concrete subclass per type code value.**
   - Add all subclasses at once (easier than one at a time for this path)
   - Each subclass returns its specific type code from `getTypeCode()`
   ```java
   class Engineer extends EmployeeType {
     int getTypeCode() { return Employee.ENGINEER; }
   }
   ```
   - Compile

4. **Connect the host class to the state/strategy object.**
   - Add a private field of the state class type: `private EmployeeType _type;`
   - Redirect the host class's type code getter to delegate: `int getType() { return _type.getTypeCode(); }`
   - Redirect the host class's type code setter to instantiate the correct state subclass:
   ```java
   void setType(int arg) {
     switch (arg) {
       case ENGINEER: _type = new Engineer(); break;
       case SALESMAN: _type = new Salesman(); break;
       // etc.
     }
   }
   ```
   - Update the constructor to call the setter (not directly assign)
   - Compile and test
   - Note: this creates one switch statement in the setter. It is acceptable — it is isolated to object creation/transition and will be the only switch remaining once Replace Conditional with Polymorphism eliminates all the behavioral switches

5. **Move type code constants to the state class.**
   - Copy the constant definitions into `EmployeeType`; add a factory method `newType(int code)` with the switch
   - Update the host class's setter to call `EmployeeType.newType(arg)` instead of the switch
   - Remove the constant definitions from the host class; update any remaining references to use `EmployeeType.ENGINEER` etc.
   - Compile and test

6. **Apply Replace Conditional with Polymorphism** (Step 4 below) on all behavioral switch statements.

---

### Step 4: Replace Conditional with Polymorphism

**ACTION:** For each switch statement (or if-else chain) that branches on the type code, replace it with a polymorphic method call.

**WHY:** This is the payoff step. After Paths B and C, the type code has an inheritance structure. Replace Conditional with Polymorphism moves each branch of each switch into the appropriate subclass. The switch disappears; callers simply invoke the method and get the right behavior for their variant automatically. Adding a new variant now means adding one subclass — no switch hunting.

**Mechanics (apply per switch statement):**

1. **Extract Method** on the switch statement if it is embedded in a longer method. Give it a name that describes what it computes.
2. **Move Method** to the class that holds the type code (the host class in Path B, or the state/strategy abstract class in Path C).
3. For each case in the switch:
   - Create an overriding method in the appropriate subclass that contains that case's body
   - The superclass version becomes abstract (or raises an error if there is a default case that should never be reached)
4. Delete the switch statement from the moved method; make it abstract.
5. Compile and test after each case is moved.

**After all switches are replaced:**
- The type code field exists only in the getter (Path B: abstract; Path C: delegating to state object)
- No caller needs to ask what type an object is — they just call the method
- Adding a new variant is a single-class addition

---

### Step 5: Apply Exceptions and Reverse Path

**Replace Parameter with Explicit Methods (polymorphism overkill):**

Apply instead of the full type code replacement when ALL of these are true:
- The switch appears in only one method
- The method takes the type code as a parameter (not a stored field)
- The variants are stable — new cases are not expected

**Mechanics:** Create a separate named method for each case. Instead of one `setHeight(int metricType, double amount)` with a switch on `metricType`, create `setHeightInMeters(double amount)` and `setHeightInFeet(double amount)`. Callers use the explicit method name instead of passing a type code constant.

**Introduce Null Object:**

Apply when one of the switch cases handles `null`:
- Create a null-object subclass that returns neutral/safe values for every method (zero, empty string, no-op, etc.)
- Replace all null checks in callers with polymorphic calls — the null object responds correctly without special-casing
- The null check disappears from the switch

**Replace Subclass with Fields (reverse path):**

Apply when you have subclasses that vary only in constant return values — no real behavior difference, just returning different hard-coded constants.

Signal: subclasses that look like:
```java
class Male extends Person { boolean isMale() { return true; } char getCode() { return 'M'; } }
class Female extends Person { boolean isMale() { return false; } char getCode() { return 'F'; } }
```

**Mechanics:**
1. Apply Replace Constructor with Factory Method on the subclasses — create factory methods on the superclass (`createMale()`, `createFemale()`)
2. Update all callers to use the factory methods; remove direct references to the subclass names
3. For each constant method on the subclasses: declare a field on the superclass; add a protected superclass constructor that initializes those fields; update subclass constructors to call `super(true, 'M')` etc.
4. Implement each constant method on the superclass to return the field; remove the override from the subclass
5. Compile and test after each subclass method is removed
6. When a subclass has no remaining methods: use Inline Method to inline its constructor into the superclass factory method; delete the subclass
7. Repeat until all constant-only subclasses are gone

---

## Decision Summary (Quick Reference)

| Situation | Path |
|-----------|------|
| Type code is pure data — no switches on value | A: Replace Type Code with Class |
| Type code drives behavior + class can be subclassed + type is immutable | B: Replace Type Code with Subclasses |
| Type code drives behavior + (class already subclassed OR type changes at runtime) | C: Replace Type Code with State/Strategy |
| Focusing on a single algorithm | Name the object Strategy |
| Object transitions between states at runtime | Name the object State |
| Switch affects only one method, variants stable | Replace Parameter with Explicit Methods |
| One switch case is null | Introduce Null Object |
| Subclasses vary only in constant return values | Replace Subclass with Fields (reverse) |

---

## Examples

### Example 1: Path A — Blood Group (Pure Data)

**Situation:** `Person` class stores blood group as `int _bloodGroup` with constants `O=0, A=1, B=2, AB=3`. No method switches on blood group value — it is stored and retrieved for display. The type code is pure data.

**Routing:** No behavior-affecting switch → Path A.

**Outcome:** Create `BloodGroup` class with static instances `O, A, B, AB`. `Person` stores `private BloodGroup _bloodGroup`. All callers that used `Person.O` now use `BloodGroup.O`. The compiler now rejects `person.setBloodGroup(99)` — invalid blood groups become compile errors, not runtime surprises.

---

### Example 2: Path B — Employee Type (Immutable, No Inheritance Conflict)

**Situation:** `Employee` stores `int _type` with `ENGINEER=0, SALESMAN=1, MANAGER=2`. Method `payAmount()` switches on `_type` to calculate different pay. The type is set once at construction. `Employee` has no existing superclass.

**Routing:** Behavior-affecting switch + no setter + no existing superclass → Path B.

**Outcome:** `Engineer`, `Salesman`, `Manager` subclasses of `Employee`. `payAmount()` becomes abstract on `Employee`; each subclass implements its own pay calculation. Adding a new employee type (Contractor) means adding one class — no switch hunting.

---

### Example 3: Path C — Employee Type (Mutable — Can Change Role)

**Situation:** Same `Employee` as above, but employees can be promoted (a manager can become an engineer). `setType(int arg)` exists. Subclassing is impossible because the type changes at runtime.

**Routing:** Behavior-affecting switch + setter exists (type mutable) → Path C.

**Outcome:** `EmployeeType` abstract class with `Engineer`, `Salesman`, `Manager` subclasses. `Employee` holds `private EmployeeType _type`. `payAmount()` moves to `EmployeeType` and is overridden in each subclass. Calling `employee.setType(Employee.ENGINEER)` swaps in a new `Engineer` state object. The object model is valid — `Employee` does not change class, its delegate does.

---

### Example 4: Polymorphism Overkill — Replace Parameter with Explicit Methods

**Situation:** A single method `setValue(int metricType, double amount)` switches on `metricType` (FEET=0, METERS=1). This switch appears only in this one method.

**Routing:** Single method affected, stable variants → Replace Parameter with Explicit Methods.

**Outcome:** `setValueInFeet(double amount)` and `setValueInMeters(double amount)`. Callers are more readable; the compiler enforces the call rather than trusting the caller to pass a valid constant.

---

## Key Principles

**1. Route before executing.** The most expensive mistake is applying the wrong path. Applying Path B when the type is mutable requires undoing the subclass structure and building a state object instead. Take 10 minutes to answer the two decision tree questions before writing any code.

**2. Self-encapsulate first, always.** Both Paths B and C begin with self-encapsulation of the type code field. Skipping this step and leaving direct field access in the host class means subclasses' getter overrides are bypassed. The refactoring silently fails.

**3. One switch is acceptable after Path C.** The setter in Path C has a switch that instantiates the correct state subclass. This is the only remaining switch and it is isolated to one place. Do not try to eliminate it with more indirection — it is the factory, and one factory switch is exactly right.

**4. Migrate callers one at a time.** In Path A especially, changing all callers at once is error-prone. Change one caller, compile, test, then the next. The old and new interfaces can coexist during the transition — that is the point of keeping `getCode()` available until all callers have migrated.

**5. Replace Conditional with Polymorphism is the payoff.** Paths B and C are scaffolding. The actual gain — no more switch hunting when adding variants — comes from completing Replace Conditional with Polymorphism. Do not stop at the structural step.

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/refactoring-prescriptions.md` | Full prescription tree per smell with all conditional branches | Verifying routing decisions |
| `references/smell-catalog.md` | Switch Statements and Primitive Obsession detection criteria | Confirming the type code is the root cause |

**Skill relationships:**
- `code-smell-diagnosis` — upstream: identifies Switch Statements or Primitive Obsession that routes here
- `conditional-simplification-strategy` — downstream: handles complex conditionals not driven by type codes
- `data-organization-refactoring` — parallel: handles Primitive Obsession when the issue is data clusters, not type codes

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler and Kent Beck.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-code-smell-diagnosis`
- `clawhub install bookforge-conditional-simplification-strategy`
- `clawhub install bookforge-data-organization-refactoring`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
