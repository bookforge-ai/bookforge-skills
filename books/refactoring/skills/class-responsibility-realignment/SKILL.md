---
name: class-responsibility-realignment
description: |
  Redistribute methods and fields to the classes that own them, repair broken inheritance hierarchies, and extend unmodifiable library classes. Use when: a method uses another class's data far more than its own (Feature Envy — the method belongs in the other class); a single logical change forces edits across many files (Shotgun Surgery — scattered behavior needs consolidation); a class delegates half or more of its methods without adding value (Middle Man — remove the hollow layer or collapse it into inheritance); two classes share too much private knowledge about each other (Inappropriate Intimacy — separate the entangled pieces); a recurring group of fields travels together across class boundaries (Data Clumps — extract the group into its own class); a class has grown to serve two distinct responsibilities that change for different reasons (Extract Class — split it); a class that used to have a purpose has been refactored down to almost nothing (Inline Class — absorb it into its most active collaborator). For inheritance hierarchies: move common behavior upward (Pull Up Method, Pull Up Field) when subclasses duplicate it; push specialized behavior downward (Push Down Method, Push Down Field, Extract Subclass) when only some subclasses need it; create a shared abstraction over two similar but unrelated classes (Extract Superclass); extract a protocol-only contract (Extract Interface) when clients use only a subset of the class; merge a hierarchy that has converged (Collapse Hierarchy); move similar-but-not-identical subclass methods into a common template (Form Template Method); swap inheritance for delegation (Replace Inheritance with Delegation) when a subclass uses only part of the superclass interface or inherits inappropriate data; swap back (Replace Delegation with Inheritance) when the delegation covers the full interface and adds no control. For unmodifiable library classes: add one or two methods as foreign methods in the client class; add many methods via a local extension (subclass or wrapper). Decision rule for encapsulation balance: Hide Delegate to shield clients from internal structure; Remove Middle Man when the delegating layer has grown hollow. Decision rule for inheritance vs delegation: use Extract Subclass when variation is fixed at construction time and single-dimensional; use Extract Class (delegation) when variation is runtime-flexible or multi-dimensional — "if you want the class to vary in several different ways, you have to use delegation for all but one of them."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/class-responsibility-realignment
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - code-smell-diagnosis
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler", "Kent Beck"]
    chapters: [7, 11]
tags: [refactoring, code-quality, object-oriented-design, responsibilities]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source code — the class or set of classes whose responsibility assignment is being corrected"
    - type: document
      description: "Code-smell-diagnosis report naming Feature Envy, Shotgun Surgery, Middle Man, Inappropriate Intimacy, or a hierarchy smell — use this if no live codebase is accessible"
  tools-required: [Read, Grep, Write, Edit]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory. Read source files to assess which class owns which data; grep to find all callers before moving anything."
discovery:
  goal: "Identify the correct home for each misplaced method or field; select the appropriate refactoring from the responsibility-redistribution, hierarchy-repair, or library-extension catalogs; execute step by step with compile-and-test after each move"
  tasks:
    - "Read the target class to determine what data and behavior it contains"
    - "Identify which other classes the target class interacts with most heavily"
    - "Classify the structural problem using the smell-to-refactoring decision framework"
    - "Select and apply the correct refactoring mechanics"
    - "Verify: each class now does one clearly named thing; no class acts as a pass-through without adding value"
  audience:
    roles: ["software-developer", "senior-developer", "tech-lead"]
    experience: "intermediate — assumes familiarity with object-oriented design and basic refactoring mechanics"
  triggers:
    - "Feature Envy, Shotgun Surgery, Middle Man, or Inappropriate Intimacy diagnosed by code-smell-diagnosis"
    - "A class has two distinct change axes (Divergent Change) and needs splitting"
    - "Duplicated behavior across subclasses that should live in the superclass"
    - "A subclass rejects its inheritance by throwing exceptions or ignoring parent data (Refused Bequest)"
    - "A library class is missing one or more methods needed throughout the codebase"
    - "A delegation layer has grown to cover the entire interface of the delegate"
  not_for:
    - "Type code and switch statement refactoring — use type-code-refactoring-selector instead"
    - "Conditional logic simplification — use conditional-simplification-strategy instead"
    - "Diagnosis of which smell is present — run code-smell-diagnosis first"
    - "Performance optimization — use profiling-driven-performance-optimization instead"
---

# Class Responsibility Realignment

## When to Use

You have identified (via `code-smell-diagnosis` or direct inspection) that behavior or data is in the wrong class. The concrete signals are:

- A method calls six getter methods on another object to do its work — it belongs in that other class (Feature Envy)
- One logical change requires touching five files — the behavior is scattered and needs a home (Shotgun Surgery)
- A class does nothing but forward calls to another class — it is a hollow Middle Man
- Two classes share internal knowledge they should not — they are Inappropriately Intimate
- A cluster of fields migrates together across method signatures — it is a Data Clump waiting to be extracted
- A hierarchy has duplicate methods across siblings, or specialized behavior sitting in the wrong layer
- A library class is missing one or two methods you need repeatedly but cannot add directly

**The core insight from Fowler:** One of the most fundamental decisions in object design is deciding where to put responsibilities. Getting it wrong the first time is not a problem — refactoring exists to correct it. The moment you realize a method uses another class's data more than its own, you have the diagnosis and the prescription simultaneously: Move Method.

---

## Context and Input Gathering

### Required Input

- **The target class or classes.** Either a file path, a class name, or the output of a `code-smell-diagnosis` report. Why: responsibility decisions are made relative to the data each class owns — you cannot realign without knowing what each class contains.
- **The smell classification.** Which of the catalog smells applies (Feature Envy, Shotgun Surgery, Middle Man, Inappropriate Intimacy, Data Clumps, hierarchy smell, library gap). Why: each smell maps to a distinct set of refactorings; applying the wrong one produces a different structural problem.

### Observable Context

Before touching anything:

```
Scan targets:
  - Which class does this method call getters on most? → Move Method candidate
  - Which fields travel together in parameter lists? → Extract Class / Data Clumps
  - How many files change together for one logical edit? → Shotgun Surgery scope
  - How many methods on class A just call class B? → Middle Man threshold
  - Which subclass methods are identical? → Pull Up Method candidates
  - Does a subclass throw NotImplemented or ignore parent fields? → Refused Bequest
```

### Default Assumptions

- If the smell is ambiguous between Feature Envy and Inappropriate Intimacy: start with Move Method; see which class becomes more cohesive
- If Shotgun Surgery scope is large (>5 files): consolidate into a new class rather than an existing one — no existing class is the right home if the behavior is truly scattered
- If Move Field is needed alongside Move Method: move the field first (Fowler's preference — it stabilizes the data layout before moving the behavior)

---

## Process

### Step 1: Classify the Structural Problem

**ACTION:** Map the symptoms to one of the three problem clusters below.

**WHY:** Each cluster uses a different set of refactorings. Misclassification wastes a move or creates a new smell.

**Cluster A — Misplaced behavior (flat class graph)**

| Symptom | Refactoring |
|---------|------------|
| Method uses another class's data more than its own | Move Method |
| Field is referenced more by another class | Move Field |
| Class does too much; subset of fields/methods coheres separately | Extract Class |
| Class does too little; its responsibilities fit an absorbing class | Inline Class |
| Client navigates `a.getB().getC()` chains | Hide Delegate (add delegating method on server) |
| Server delegates more than half its interface, adds no value | Remove Middle Man |
| Library class missing 1–2 methods | Introduce Foreign Method |
| Library class missing 3+ methods | Introduce Local Extension |

**Cluster B — Hierarchy misalignment**

| Symptom | Refactoring |
|---------|------------|
| Identical method/field in two or more subclasses | Pull Up Method / Pull Up Field |
| Constructors in subclasses with mostly identical bodies | Pull Up Constructor Body |
| Superclass method only meaningful in one subclass | Push Down Method |
| Superclass field only used in one subclass | Push Down Field |
| Subset of features used only in some instances | Extract Subclass |
| Two unrelated classes share common behavior | Extract Superclass |
| Several clients use only a subset of one class's interface | Extract Interface |
| Subclass and superclass have converged — barely different | Collapse Hierarchy |
| Two subclass methods do the same steps in the same order, but differently | Form Template Method |
| Subclass uses only part of superclass interface, or inherits wrong data | Replace Inheritance with Delegation |
| Delegation covers the full interface, delegation methods are boilerplate | Replace Delegation with Inheritance |

**Cluster C — Encapsulation balance**

| Symptom | Action |
|---------|--------|
| Clients know too much about delegate's internals | Add Hide Delegate methods on server |
| Server has grown into a pass-through layer | Remove Middle Man — let clients talk to delegate |

---

### Step 2: Apply Cluster A — Misplaced Behavior

**ACTION:** Execute the mechanics for the identified refactoring(s).

**WHY:** Each step produces a compilable intermediate state; verifying after each move catches errors before they compound.

#### Move Method

When a method is more interested in another class than its own:

1. **Examine all features** the method uses. If several features from the same source class are involved, consider moving them as a group — moving a clutch of methods is sometimes easier than moving them one at a time.
2. **Check subclasses and superclasses** of the source class for other declarations. If other declarations exist, the move may be blocked unless the target class can also express the polymorphism.
3. **Declare the method in the target class.** A rename that makes better sense in the target context is appropriate.
4. **Copy the method body.** Adjust it to work in its new home — four options for referencing the source object: (a) move the feature to the target class as well, (b) create or use an existing reference from target to source, (c) pass the source object as a parameter, (d) pass the specific value as a parameter.
5. **Turn the source method into a simple delegation** (return `target.methodName()`). Compile and test.
6. **Decide whether to remove the delegation.** Leaving it is easier if there are many callers; removing it is cleaner if callers can be updated.

#### Move Field

When a field is used more by another class:

1. **If the field is public,** use Encapsulate Field first. If many methods access it, use Self Encapsulate Field so only accessors touch the raw field.
2. **Create the field with getter/setter in the target class.** Compile.
3. **Determine how to reference the target object** from the source. Use an existing field or method; if none exists, create one (possibly temporary).
4. **Remove the field from the source class.** Replace all references with calls to the target's accessor.
5. Compile and test.

#### Extract Class

When a class is doing work that should be done by two:

1. **Decide the split.** A useful test: remove a field — do the remaining fields and methods still make sense without it? If yes, you have found an extraction boundary.
2. **Create the new class.** Rename the old class if its name no longer matches its reduced scope.
3. **Move fields first** (Move Field), then **move methods** (Move Method) — start with lower-level methods (called, not calling) and work toward higher-level ones.
4. **Review and reduce interfaces** after each move. If a two-way link exists, examine whether it can become one-way.
5. **Decide visibility of the new class.** If exposing it, decide between reference object (mutable, aliasing possible) and immutable value object.

#### Inline Class

When a class is no longer pulling its weight:

1. Declare the public protocol of the source class on the absorbing class. Delegate all methods to the source class temporarily.
2. Change all external references from the source class to the absorbing class.
3. Use Move Method and Move Field to move features from the source to the absorbing class until nothing is left.
4. Delete the empty class.

#### Hide Delegate vs. Remove Middle Man — the encapsulation balance

Fowler's observation: these two are inverse refactorings and neither is permanently correct. "Refactoring means you never have to say you're sorry — you just fix it." Apply the rule by tracking:

- **Hide Delegate:** Client calls `manager = john.getDepartment().getManager()`. Add `getManager()` directly to Person so the client does not need to know about Department. Do this for each method on the delegate that clients use. Remove the delegate accessor if clients no longer need it.
- **Remove Middle Man:** After applying Hide Delegate repeatedly, Person has grown a long list of one-liner delegation methods — it is now a Middle Man. Add an accessor for the delegate. For each client use of a delegation method, redirect the client to call the delegate directly. Remove each delegation method as its clients migrate.

**The judgment call:** Hide more when the delegate's implementation is likely to change (clients should not be coupled to it). Remove the middle man when the delegating layer adds no value and the cost of maintaining all those one-liners exceeds the coupling cost.

#### Library Extension Strategy

When you cannot modify a class but need additional behavior from it:

**1–2 methods needed → Introduce Foreign Method**

1. Create a method in the client class that does what is needed.
2. Make an instance of the server class the first parameter.
3. Comment the method: `// foreign method; should be on [ServerClass]`. Why: this marks it for migration if you later gain access to the source, and enables grep-based discovery of all foreign methods for a given class.
4. The method must not access any features of the client class — it should feel like it belongs on the server.

**3+ methods needed → Introduce Local Extension**

1. Decide between subclass and wrapper:
   - **Subclass** (preferred): simpler, less code. Constraint: apply at object-creation time. If the original is immutable, a copy constructor suffices and aliasing is not a problem.
   - **Wrapper**: required when (a) you cannot control creation of the original objects, (b) the original is mutable and you need the extension and the original to share state, or (c) you need to apply the extension to existing objects. Tradeoff: must delegate all original class methods, and symmetrical equality checks (`a.equals(b)` where `a` is original and `b` is wrapper) cannot be fully hidden.
2. Add converting constructors — one that takes an instance of the original as argument.
3. Add new methods to the extension class. Move any existing foreign methods defined for this class onto the extension.
4. Replace uses of the original class with uses of the extension where the new methods are needed.

---

### Step 3: Apply Cluster B — Hierarchy Repair

**ACTION:** Select and apply the hierarchy refactoring identified in Step 1.

**WHY:** Hierarchy smells compound — duplicate methods in subclasses create two maintenance points; misplaced fields make Pull Up Method harder. Address the fields before the methods.

#### Pull Up Field / Pull Up Method

Fields first, then methods. Why: Pull Up Method may depend on the field being in the superclass already.

- **Pull Up Field:** Inspect that all uses of the candidate fields are equivalent across subclasses. Rename if needed. Create the field in the superclass; delete from subclasses. Mark protected if subclasses need direct access.
- **Pull Up Method:** Inspect methods to confirm they are identical (or can be made identical via algorithm substitution). If similar but not identical, see Form Template Method. If the method references a feature that is only on the subclass, generalize that feature first (Pull Up the feature, or declare an abstract method on the superclass). Copy one body to the superclass; delete from subclasses one at a time, compiling and testing after each deletion.
- **Pull Up Constructor Body:** Constructors cannot be inherited. Extract the common initialization code into a superclass constructor; call it via `super(...)` from each subclass. If common code must run after subclass-specific initialization, use Extract Method on the common post-init logic and Pull Up Method to put it in the superclass, then call it explicitly from the subclass constructor.

#### Push Down Method / Push Down Field

When superclass behavior is only relevant to some subclasses:

- Declare the method/field in all subclasses that need it. Copy the body. Remove from the superclass. Remove from subclasses that do not need it. Compile and test.
- If the superclass is abstract and the method should still be accessible via a superclass variable, declare it abstract on the superclass instead of removing it.

#### Extract Subclass

When a class has features used only in some instances:

1. The main alternative is Extract Class (delegation vs. inheritance). **Choose Extract Subclass when:** the variation is fixed at construction time (the object's kind does not change after creation), the variation is single-dimensional (one axis of difference), and the class being extended is modifiable. Why: subclassing is simpler — the class-based behavior is changed by plugging in different components with Extract Class, but Extract Subclass requires only Push Down Method and Push Down Field.
2. **Choose Extract Class instead when:** the object's kind varies at runtime, or the class must vary in multiple dimensions simultaneously. Fowler: "If you want the class to vary in several different ways, you have to use delegation for all but one of them."
3. Define the new subclass. Provide constructors. Find all calls to the superclass constructor that should use the subclass — replace with subclass constructor calls.
4. Use Push Down Method and Push Down Field to move specialized features. Unlike Extract Class, work on methods first, data last.
5. Find boolean or type-code fields that now encode information already expressed by the hierarchy — eliminate them by replacing their getter with a polymorphic constant method.

#### Extract Superclass

When two classes share common behavior:

1. Create a blank abstract superclass. Make both classes its subclasses.
2. Move common fields first (Pull Up Field). Move common methods (Pull Up Method). If method signatures differ but purpose is the same, rename first.
3. If methods have different bodies doing the same thing, try Substitute Algorithm to unify them.
4. If methods have the same signature but different bodies that cannot be unified, declare the method abstract on the superclass.
5. Check clients — if they use only the common interface, change their type declarations to the superclass.

#### Extract Interface

When several clients use only a subset of a class's interface, or when a class needs to work with any class that can handle certain requests:

- Create an empty interface. Declare the common operations. Declare the relevant classes as implementing the interface. Update client type declarations to use the interface.
- Unlike Extract Superclass, Extract Interface cannot move common code — only the contract. If common code is needed too, combine with Extract Class (for the shared implementation).

#### Collapse Hierarchy

When a subclass and superclass have converged:

- Choose which class to remove (usually the subclass). Pull Up or Push Down all methods and fields to the surviving class. Update all references. Remove the empty class.

#### Form Template Method

When two subclass methods perform the same steps in the same order but the steps are implemented differently:

1. **Decompose each method** using Extract Method so that each extracted piece is either identical across subclasses or completely different — no partial overlap.
2. **Pull Up the identical extracted methods** to the superclass.
3. **Rename the different methods** so they have the same signature in both subclasses. Why: making the signatures identical makes the calling method identical across subclasses — it calls the same method names in the same order.
4. **Pull Up the calling method** on one of the subclasses. Declare the different methods as abstract on the superclass.
5. Remove the calling method from the other subclass.

Result: the superclass holds the invariant algorithm; subclasses supply only the steps that vary. This is the Template Method pattern — adding a new variant requires only a new subclass that overrides the abstract steps.

#### Replace Inheritance with Delegation

When a subclass uses only part of the superclass interface or inherits data that does not make sense for it (Refused Bequest, strong form):

1. **Create a field in the subclass** that refers to the superclass — initialize it to `this` so delegation and inheritance can coexist during the transition.
2. **Change each subclass method** to use the delegate field instead of implicit inheritance. Compile and test after each change. Note: methods that call `super` cannot be changed until the inheritance link is broken — they would recurse.
3. **Remove the inheritance declaration.** Change the delegate field from `this` to a new instance of the former superclass.
4. **For each superclass method used by clients,** add a simple delegating method on the subclass. Compile and test.

Contraindications: do not apply when the subclass uses all methods of the superclass (delegation is boilerplate without benefit), or when the delegate is shared and mutable (data sharing cannot be replicated with delegation).

#### Replace Delegation with Inheritance

When a class delegates to another class for the full interface and the delegating methods are pure boilerplate:

1. Precondition: the delegating class uses all of the delegate's methods. If not, use Remove Middle Man or Extract Interface instead.
2. Precondition: the delegate is not shared and mutable. If it is, delegation must remain (you cannot replicate shared mutable state via inheritance).
3. Make the delegating class a subclass of the delegate.
4. Set the delegate field to the object itself. Remove simple delegation methods. Compile and test.
5. Replace remaining uses of the delegate field with direct calls. Remove the delegate field.

---

### Step 4: Verify the Realignment

**ACTION:** Confirm the structural goals are achieved.

**WHY:** It is possible to complete all mechanics correctly but still have the smell — if the wrong refactoring was chosen for the symptom, or if a second smell was hidden beneath the first.

Verify each:

- Each class has a name that describes a single responsibility. If the name requires "and" to describe what it does, the split may be incomplete.
- No method calls another class's getters more than its own class's fields. If Feature Envy persists, a deeper extraction is needed.
- No class delegates more than half its public methods without adding any logic. If Middle Man persists, Remove Middle Man was not fully applied.
- Hierarchy: identical code does not appear in two sibling subclasses. Pull Up was not applied completely if it does.
- The delegation/inheritance decision is correct: delegation if the class varies in multiple dimensions or at runtime; inheritance if the variation is single-axis and fixed at construction.

---

## Key Principles

**1. Move Field before Move Method when doing both.**
A method moved before its data is moved will still reference the old class via getter calls. Moving the field first stabilizes the data layout; the method move then resolves cleanly.

**2. The encapsulation balance is not fixed.**
Hide Delegate protects clients from implementation changes. Remove Middle Man removes hollow layers. Apply whichever is appropriate given current coupling pressure — and reapply the inverse when conditions change.

**3. Inheritance vs. delegation: the variation-dimensions rule.**
Fowler's criterion: if you need the class to vary in only one way, subclassing (Extract Subclass) is simpler. If you need it to vary in several different ways, you must use delegation for all but one of them — a class can only have one superclass, but it can hold multiple delegate objects.

**4. Foreign methods are a workaround, not a destination.**
Comment them as `// foreign method; should be on [ServerClass]` so they can be found and migrated if you gain access to the server class. If the count grows beyond 2, promote to a local extension.

**5. Form Template Method is Extract Method + Pull Up.**
It is a composed refactoring, not a single step. The key is the decomposition: extracted methods must be either identical (candidates for Pull Up) or completely different (candidates for abstract methods). Partial overlap defeats the pattern.

---

## Examples

### Example 1: Feature Envy → Move Method

**Scenario:** `Account.overdraftCharge()` calls `_type.isPremium()` and uses `_type.daysOverdrawn()` — most of its logic is about `AccountType`, not `Account`.

**Diagnosis:** Feature Envy. The method is more interested in `AccountType` than in `Account`.

**Apply Move Method:**
1. Copy `overdraftCharge` to `AccountType`. Pass `daysOverdrawn` as a parameter (option d — pass the specific value).
2. Replace `Account.overdraftCharge()` body with `return _type.overdraftCharge(_daysOverdrawn);`
3. Compile and test. Callers of `account.overdraftCharge()` still work — the source is now a delegating method.
4. Decision: several account types will be added, each needing its own overdraft rule. Remove the delegation in `Account` and redirect all callers to `_type.overdraftCharge(_daysOverdrawn)` directly.

**Result:** `AccountType` owns overdraft logic. New account types require changes only in `AccountType` — Shotgun Surgery is eliminated.

---

### Example 2: Data Clumps → Extract Class

**Scenario:** `Person` has `_officeAreaCode` and `_officeNumber` as separate fields. Both appear in method signatures throughout the codebase. Deleting `_officeAreaCode` makes `_officeNumber` meaningless without context.

**Diagnosis:** Data Clumps. These two fields form a natural object.

**Apply Extract Class:**
1. Create `TelephoneNumber` class.
2. Add a link from `Person` to `TelephoneNumber`: `private TelephoneNumber _officeTelephone = new TelephoneNumber()`.
3. Move Field: move `_officeAreaCode` to `TelephoneNumber`. Update `Person`'s accessors to delegate: `getOfficeAreaCode()` → `_officeTelephone.getAreaCode()`.
4. Move Field: move `_officeNumber`. Move Method: move `getTelephoneNumber()` to `TelephoneNumber`.
5. Decide visibility: expose `TelephoneNumber` as a reference object (aliasing allowed) or make it immutable (safer).

**Result:** `TelephoneNumber` is a named concept. It can be reused by `HomeAddress`, `MobileContact`, and others without duplicating the area-code/number pair.

---

### Example 3: Extract Subclass vs. Extract Class — the variation-dimensions decision

**Scenario:** `JobItem` has an `_isLabor` boolean that controls behavior in `getUnitPrice()`. Labor items use `employee.getRate()`; parts items use `_unitPrice`. The `_employee` field is null for parts items.

**Classification step:**
- Is the variation fixed at construction time? Yes — a job item is either a labor item or a parts item from the start.
- Is the variation single-dimensional? Yes — there is one axis (labor vs. parts).
- Conclusion: Extract Subclass.

**Apply Extract Subclass (creating LaborItem):**
1. Create `LaborItem extends JobItem`.
2. Push Down Method: `getEmployee()` moves to `LaborItem`.
3. Push Down Field: `_employee` moves to `LaborItem`.
4. Self Encapsulate Field `_isLabor`; replace its getter with a polymorphic constant: `JobItem.isLabor()` returns `false`, `LaborItem.isLabor()` returns `true`.
5. Apply Replace Conditional with Polymorphism on `getUnitPrice()`: `JobItem` returns `_unitPrice`; `LaborItem` returns `_employee.getRate()`.
6. Remove `_isLabor` field.

**Contrast with delegation case:** If job items needed to vary along a second axis (e.g., taxable vs. non-taxable), subclassing could cover only one axis. The second axis would require a delegate: `JobItem` holds a `TaxStrategy` delegate and a `PricingStrategy` delegate, with the hierarchy handling neither.

---

### Example 4: Form Template Method

**Scenario:** `TextStatement.value()` and `HtmlStatement.value()` perform the same three steps (header, body loop, footer) but format them differently. The two methods are similar but not identical.

**Apply Form Template Method:**
1. Move both methods to subclasses of a new `Statement` superclass.
2. Extract Method on each differing step: `headerString()`, `eachRentalString()`, `footerString()` — extracted with identical signatures in both subclasses, different bodies.
3. The calling method `value()` becomes identical in both subclasses: it calls `headerString()`, loops calling `eachRentalString()`, and calls `footerString()`.
4. Pull Up Method on `value()` to `Statement`. Declare `headerString()`, `eachRentalString()`, `footerString()` as abstract on `Statement`.
5. Remove `value()` from both subclasses.

**Result:** Adding a `PdfStatement` requires only a new subclass that overrides three methods — the algorithm structure is untouchable.

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/smell-catalog.md` | Full detection criteria for all 22 smells | Confirming the smell classification in Step 1 |
| `references/refactoring-prescriptions.md` | Full prescription trees per smell | Selecting the correct conditional branch for each refactoring |

**Hub skill relationships:**
- `code-smell-diagnosis` — diagnose before realigning; this skill executes what that skill prescribes
- `data-organization-refactoring` — when Data Clumps or Primitive Obsession are the primary smell (Extract Class for data, not behavior)
- `type-code-refactoring-selector` — when the hierarchy problem involves a type code (Replace Type Code with Subclasses / State / Strategy)
- `conditional-simplification-strategy` — when Replace Conditional with Polymorphism is needed after Extract Subclass
- `big-refactoring-planner` — when multiple smells indicate a systemic design problem requiring coordinated multi-step refactoring

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler and Kent Beck.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-code-smell-diagnosis`
- `clawhub install bookforge-data-organization-refactoring`
- `clawhub install bookforge-type-code-refactoring-selector`
- `clawhub install bookforge-conditional-simplification-strategy`
- `clawhub install bookforge-big-refactoring-planner`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
