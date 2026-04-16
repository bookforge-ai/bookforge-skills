---
name: data-organization-refactoring
description: |
  Apply the correct data organization refactoring when code smells in data structure design are diagnosed — Primitive Obsession, Data Clumps, Data Class, or raw structural anti-patterns like magic numbers, positional arrays, and naked public fields. Covers the full Chapter 8 catalog: Replace Data Value with Object (primitive → first-class object); Change Value to Reference / Change Reference to Value (value vs. reference object decision); Self Encapsulate Field (internal field access via accessors); Encapsulate Field (public → private with accessors); Encapsulate Collection (raw collection → controlled add/remove protocol); Replace Array with Object (positional array → named-field object); Replace Magic Number with Symbolic Constant; Replace Record with Data Class (legacy record → typed wrapper); Duplicate Observed Data (domain data trapped in GUI → domain class + observer sync); Change Unidirectional Association to Bidirectional (one-way link → two-way when both ends need navigation); Change Bidirectional Association to Unidirectional (drop unnecessary back pointer). Use when: a field stores a raw primitive (string, int) but has behavior waiting to happen (formatting, validation, comparison); the same 2-4 data items travel together through method signatures and field lists (Data Clumps); a class exists only as a getter/setter bag with no behavior (Data Class); a collection field is exposed so callers can mutate it directly; positional arrays or records need to cross the boundary into object-oriented design; a numeric literal with special meaning appears in more than one place; a GUI class owns domain data that business methods need; a one-way association is insufficient or a two-way association has become unnecessarily complex. Type code refactorings (Replace Type Code with Class/Subclasses/State-Strategy) are handled by the sibling skill `type-code-refactoring-selector`.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/data-organization-refactoring
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - code-smell-diagnosis
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler", "Kent Beck"]
    chapters: [8]
tags: [refactoring, code-quality, data-modeling, encapsulation]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source code containing the data structure problem — the class(es) with primitive fields, raw collections, exposed data, or positional arrays"
    - type: document
      description: "Code snippet, class description, or diagnosed smell report if no live codebase is accessible"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory. Read source files to locate the data structures; grep for field access patterns and method signatures to understand usage scope."
discovery:
  goal: "Select the correct data organization refactoring for the presenting smell; execute the mechanics step by step; verify that clients use the new interface correctly and that the old exposure points are removed"
  tasks:
    - "Identify the presenting smell: Primitive Obsession, Data Clumps, Data Class, raw collection exposure, positional array, magic number, or structural record"
    - "Apply the selection framework to pick the specific refactoring"
    - "For value vs. reference decisions: determine whether the object has real-world identity or is defined purely by its data values"
    - "Execute the mechanics of the selected refactoring in safe, compilable steps"
    - "Verify that all callers use the new interface; confirm that the old exposure point is removed or made private"
    - "Identify follow-on refactorings (Move Method to the new class; Replace Conditional with Polymorphism for type codes)"
  audience:
    roles: ["software-developer", "senior-developer", "tech-lead", "code-reviewer"]
    experience: "intermediate — assumes working knowledge of object-oriented design and accessor patterns"
  triggers:
    - "Primitive Obsession or Data Clumps smell diagnosed — raw data needs a first-class object"
    - "Data Class smell diagnosed — a class with only getters/setters needs behavior moved in"
    - "A collection field is publicly settable or directly returned, allowing callers to mutate it"
    - "An array where elements at index 0, 1, 2 mean different named things"
    - "A numeric literal with a special meaning appears in more than one place"
    - "Domain business logic is embedded in a GUI class and needs extraction"
    - "A one-way object association is insufficient for a new feature; or a two-way link is creating zombie objects and coupling complexity"
  not_for:
    - "Type code refactorings (Replace Type Code with Class/Subclasses/State-Strategy) — use type-code-refactoring-selector instead"
    - "Conditional simplification not caused by data structure problems — use conditional-simplification-strategy instead"
    - "Class responsibility problems (Feature Envy, Shotgun Surgery, Divergent Change) — use class-responsibility-realignment instead"
    - "New code written from scratch — these refactorings apply to existing data structures"
---

# Data Organization Refactoring

## When to Use

You have data structures in existing code that are making the code harder to read, harder to change, or actively attracting bugs. The data may be raw primitives with hidden behavior, loosely grouped fields that travel together but have no home object, or collections exposed for direct mutation by callers.

This skill applies when:
- A string, integer, or other primitive is doing work that a class should do — formatting, validation, comparison, area code extraction, currency conversion
- The same cluster of 2-4 fields appears together in field lists, parameter lists, and return types (Data Clumps smell)
- A class exists only as a getter/setter holder; other classes manipulate its data in excessive detail (Data Class smell)
- A collection field is returned directly so callers can add, remove, or replace elements without the owning class knowing
- An array uses positional index conventions (element 0 is name, element 1 is wins) that only comments explain
- A numeric literal with domain meaning appears in more than one place, making the meaning invisible
- GUI code contains domain data and business calculations that domain objects need access to
- A one-way object link needs to become bidirectional, or a bidirectional link is no longer earning its complexity cost

**The core insight from Fowler:** Data items start simple and grow. A telephone number starts as a string, but eventually needs formatting, area code extraction, and validation — it has become a first-class object. The signal is not the complexity of the current data item; it's the behavior that wants to live on it. When you find yourself adding the same behavior to the owner of the primitive rather than to a class that represents the concept, the primitive is overdue for promotion.

**Scope boundary:** Type code refactorings (Replace Type Code with Class, Replace Type Code with Subclasses, Replace Type Code with State/Strategy) are covered by the sibling skill `type-code-refactoring-selector`. When a magic number or type code enum is driving switch statement behavior, use that skill. When data merely needs a better structural home, use this one.

---

## Context and Input Gathering

### Required Input (must have — ask if missing)

- **The class or code fragment with the data problem.** Either a file path, a class name, or a pasted snippet. Why: data organization problems are structural — they require seeing the field declarations, the methods that use the fields, and the callers that access those methods. Without this, selection of the correct refactoring is guesswork.

- **The diagnosed smell** (if available). If `code-smell-diagnosis` has already been run, use its output to confirm which smell is present. Why: multiple smells can present similarly (Primitive Obsession vs. Data Clumps vs. Data Class). Knowing the smell name from diagnosis avoids picking the wrong refactoring.

- **Language and framework.** Why: collection encapsulation mechanics differ by language (Java unmodifiable views vs. Python property decorators vs. TypeScript readonly). Value object equality semantics differ. The mechanics steps must match the language.

### Observable Context (gather before asking)

Scan the code to orient:

```
Smell signals to look for:
  - Fields that are primitives with related behavior scattered on the owner → Primitive Obsession
  - Same 2-4 fields appearing together in 3+ places → Data Clumps
  - Class with only getters/setters and no behavior methods → Data Class
  - public field or collection returned directly → missing Encapsulate Field / Encapsulate Collection
  - array[0], array[1], array[2] with comments naming each slot → Replace Array with Object
  - Numeric literals (9.81, 0.85, 24) in domain calculations → Replace Magic Number with Symbolic Constant
  - Business calculation methods on a class that extends a GUI framework → Duplicate Observed Data needed
  - One class holds a reference to another but the referenced class cannot navigate back → unidirectional association
```

### Default Assumptions

- If multiple smells are present: prioritize by structural impact — replace primitives with objects first (enables other refactorings), then encapsulate, then handle associations
- If scope is unclear: focus on the class the user named; expand to callers only when verifying that the new interface is used correctly
- If the smell is borderline: do the delete-one-item test for Data Clumps (if removing one field from a group makes the others meaningless, it's a clump)

---

## Refactoring Selection Framework

**Start here.** Match the presenting symptom to the correct refactoring before executing mechanics.

```
SYMPTOM → REFACTORING

A primitive field has behavior that keeps growing on the owner class
  → Replace Data Value with Object
     Then decide: does the resulting object have identity (real-world entity)?
       YES → Change Value to Reference
       NO  → keep as value object (immutable, equality by value)

A field is accessed directly within the same class, and you need subclass
override flexibility or lazy initialization
  → Self Encapsulate Field

A public field is accessed by external classes
  → Encapsulate Field
     (first step only — a class with just accessors is still a Data Class;
      follow with Move Method to bring behavior in)

A collection field is returned directly, allowing callers to mutate it
  → Encapsulate Collection

An array where index position encodes meaning
  → Replace Array with Object

A numeric literal with domain meaning appears in 2+ places
  → Replace Magic Number with Symbolic Constant
     Exception: if the literal is a type code driving switch behavior
     → use type-code-refactoring-selector instead

A legacy record or external API structure needs an object-oriented interface
  → Replace Record with Data Class

Domain data and business methods are trapped in a GUI class
  → Duplicate Observed Data

One class needs to navigate to the other but only a one-way link exists
  → Change Unidirectional Association to Bidirectional

A two-way association exists but one end no longer needs the other
  → Change Bidirectional Association to Unidirectional

The same 2-4 data items travel together in field lists and parameter lists
  → Extract Class (Data Clumps path — see code-smell-diagnosis for full Data Clumps mechanics)
     Then: Introduce Parameter Object or Preserve Whole Object at call sites
```

---

## Process

### Step 1: Locate and Understand the Data Structure

**ACTION:** Read the class containing the problematic data. Identify the field(s), their type, how they are set, and how they are used. Then grep for all callers.

**WHY:** Data organization refactorings are usage-driven. The field declaration tells you what exists; the callers tell you what behavior the data is accumulating, which decides whether a value object or reference object is needed, and what methods need to move. Reading only the field declaration without understanding usage leads to incomplete refactorings where the data gets a new type but the behavior stays scattered on the wrong class.

Questions to answer before selecting mechanics:
- What type is the field currently? (int, String, array, raw collection)
- What operations are performed on it by the owner class? By callers?
- Does the field appear in method parameter lists? (Data Clumps signal)
- Is it publicly accessible? (Encapsulate Field needed)
- Does it change after the object is created? (relevant for value vs. reference decision)
- Do multiple objects need to represent the same conceptual instance? (Change Value to Reference trigger)

---

### Step 2: Execute the Selected Refactoring

Work through the mechanics of the refactoring selected in the framework above. Each refactoring below states its mechanics and the WHY for each step.

---

#### Replace Data Value with Object

**When:** A field is a primitive (string, int, float) but behavior keeps accumulating on the owner — formatting, parsing, comparison, validation.

**Mechanics:**

1. Create a new class for the value. Give it a final field of the same type as the current primitive. Add a getter and a constructor that takes the primitive as argument. WHY: the new class starts as a thin wrapper; the goal is to create a stable home for the behavior, not to design the perfect API upfront.

2. Compile.

3. Change the field type in the source class to the new class. WHY: this is the type boundary that forces all callers to go through the new class rather than manipulating the raw primitive.

4. Change the getter in the source class to delegate to the getter on the new class. WHY: callers that used the getter continue to work; the internal representation is now the new class.

5. If the field appears in the constructor, assign the field using the new class constructor. WHY: the creation path must build the right type from the start.

6. Update the setter to create a new instance of the new class. WHY: since value objects should be immutable, the setter replaces the whole object rather than mutating it in place.

7. Compile and test.

8. Rename methods on the new class to reflect their purpose in the domain, not just their type. WHY: `getCustomerName()` is clearer than `getCustomer()` when the caller cares about the name, not the object identity.

**Follow-on decision:** After Replace Data Value with Object, determine whether the new object needs to be a reference object. If multiple owner objects need to share the same conceptual instance (e.g., all orders for the same customer should point to the same Customer object), apply Change Value to Reference next.

---

#### Value Object vs. Reference Object Decision

**This is the most consequential decision in data organization refactoring.** Getting it wrong causes aliasing bugs (mutable value objects) or unnecessary coordination complexity (reference objects where values would suffice).

**Value objects** (Date, Money, Currency, PhoneNumber):
- Defined entirely by their data — two instances with the same data are equal
- Immutable: to "change" a value object, you replace it with a new one
- Equality by value: override `equals()` and `hashCode()` based on fields
- Copyable freely: no aliasing risk because mutation is not possible
- Preferred for: amounts, measurements, identifiers, codes, coordinates

**Reference objects** (Customer, Account, Employee, Order):
- Represent a real-world entity with identity independent of their data
- One instance per real-world entity: two Customer objects with the same name are still two different customers
- Equality by identity (object reference, database key)
- Require a registry or factory to enforce the one-instance constraint
- Preferred for: entities that have state that changes over time; entities that multiple other objects need to point to the same instance of

**Decision criteria:**

```
QUESTION                                              → DIRECTION

Does changing this object's data need to be seen      → Reference object
by all other objects that hold a reference to it?       (aliasing is required)

Does the object represent a real-world entity with    → Reference object
independent existence (customer, account, order)?

Is this a measurement, amount, code, or coordinate    → Value object
defined purely by its data?

Would it be correct for two objects to each have      → Value object
their own independent copy?

Is the object used in distributed or concurrent       → Value object (safer)
contexts where shared mutable state is problematic?
```

**Change Value to Reference** (when a value object needs to become a reference object):
1. Apply Replace Constructor with Factory Method on the new class. WHY: a factory gives you control over object creation — the constructor can be made private, and the factory returns the single canonical instance.
2. Decide what object will serve as the registry (static field on the class, a separate registry object, or the container object). WHY: reference objects require a way to find the existing instance rather than creating a new one.
3. Decide whether objects are pre-created or created on demand. WHY: pre-created (loaded at startup from a database or config) requires handling the "not found" case; on-demand creates only when first requested.
4. Alter the factory method to return the existing instance from the registry. Rename the factory to convey that it retrieves rather than creates (e.g., `getNamed()` instead of `create()`). WHY: the name communicates the semantics — callers should know they are getting a shared instance.
5. Compile and test.

**Change Reference to Value** (when a reference object is too awkward and should become a value object):
1. Verify the object is immutable or can be made immutable. Remove setting methods until no mutation remains. WHY: a mutable value object is a trap — callers who copy the reference see each other's changes, producing aliasing bugs that are very hard to diagnose.
2. If the object cannot become immutable, abandon this refactoring. WHY: the immutability requirement is not optional; a mutable value object is worse than the original reference object.
3. Implement `equals()` and `hashCode()` based on the object's data fields. WHY: value objects are equal when their data is equal; without overriding these methods, equality falls back to object identity, defeating the purpose of the conversion.
4. Compile and test.
5. Remove the factory method and make the constructor public. WHY: value objects are created freely; there is no registry, no single-instance constraint.

---

#### Self Encapsulate Field

**When:** A class accesses its own field directly, and you need subclasses to be able to override how the value is produced (computed value, lazy initialization) without changing the field access code scattered through the class.

**Mechanics:**

1. Create getter and setter methods for the field. WHY: accessors are the hook point that subclasses override. Without them, the only way to intercept field access is to change every direct reference.

2. Find all references to the field within the same class and replace direct access with calls to the getter (reads) and setter (writes). WHY: once all internal access goes through the accessor, a subclass can override the getter to return a computed or cached value, and the rest of the class automatically picks up the new behavior.

3. Make the field private. WHY: private forces all access — internal and external — through the accessors. This prevents subclasses from bypassing the accessor by directly accessing the field.

4. In constructors, prefer direct field access or a separate `initialize()` method rather than the setter. WHY: setters often have behavior that is appropriate for changes after construction but not for initialization. Using the setter in the constructor can trigger that behavior prematurely.

5. Compile and test.

---

#### Encapsulate Field

**When:** A field is public and accessed directly by external classes, violating the encapsulation principle. The class cannot control what values are set or observe when the value changes.

**Mechanics:**

1. Create getter and setter methods for the field.

2. Find all external clients that reference the field directly. Replace reads with calls to the getter; replace writes with calls to the setter. WHY: direct field access bypasses the owning class entirely. Once callers go through accessors, the owning class can add validation, notification, or lazy initialization in the future without changing callers.

3. Compile and test after each client change.

4. Once all external references are replaced, declare the field private. WHY: the private modifier enforces that future code cannot bypass the accessor, preserving the encapsulation permanently.

5. After encapsulation, look at which methods on external classes use the new accessor to compute something about this object's data. Those methods are Feature Envy candidates — consider moving them to the class that owns the data.

---

#### Encapsulate Collection

**When:** A method returns a collection field directly (a list, set, or map), allowing callers to add, remove, or replace elements without the owning class knowing.

**Mechanics:**

1. Add `add(element)` and `remove(element) ` methods to the owning class. WHY: these are the controlled mutation points. The owning class can enforce invariants (uniqueness, ordering, related state updates) in these methods.

2. Initialize the field to an empty collection in the field declaration. WHY: callers should not need to check for null before using the collection; an empty collection is always safe.

3. Find all callers of the setter. Modify the setter to use the add and remove methods rather than directly assigning the field, or have callers call add/remove directly and remove the setter. WHY: a setter that replaces the whole collection bypasses the controlled mutation protocol; the setter should be renamed to `initialize` to clarify it is for initial population only, or removed entirely.

4. Find all callers of the getter that then mutate the collection (e.g., `person.getCourses().add(...)`). Change them to call the new add/remove methods on the owning class. WHY: getter-then-mutate is the same as direct field access — it bypasses the owning class's control.

5. Once no caller mutates through the getter, change the getter to return an unmodifiable view (Java: `Collections.unmodifiableSet()`, Python: `tuple()` or `frozenset()`, TypeScript: `readonly` array). WHY: the unmodifiable return makes it structurally impossible for callers to mutate the collection through the getter, enforcing the encapsulation permanently.

6. Look at client code that iterates the collection to perform operations on the elements. If those operations use only the owning class's data, they are candidates for Move Method — they belong on the owning class. WHY: Encapsulate Collection is the beginning; the end goal is a class that can answer questions about its own collection rather than leaking the collection for callers to query.

---

#### Replace Array with Object

**When:** An array is used to hold heterogeneous data where position encodes meaning — `row[0]` is the team name, `row[1]` is wins, `row[2]` is losses. Position-as-convention is fragile and invisible.

**Mechanics:**

1. Create a new class to represent the information in the array. Give it a public field holding the original array (temporarily). WHY: starting with a public field avoids having to change all callers immediately; the array stays inside the new class so existing code keeps working during the transition.

2. Change all sites that create the array to create the new class instead. WHY: the new class is now the entry point; the internal array is an implementation detail that will be replaced.

3. One by one, add a named getter and setter for each element of the array. Name the accessors after the purpose of that element, not after its index. WHY: the names replace the fragile index convention. `row.getName()` is self-documenting; `row[0]` requires the reader to remember the convention.

4. Change all callers to use the named accessors instead of array indexing. Compile and test after each element is converted. WHY: small steps mean each compile-and-test cycle confirms nothing broke. Changing all callers at once risks accumulating errors.

5. Once all external access uses named accessors, make the internal array private. WHY: no caller should be able to access by index anymore; private enforces the new API boundary.

6. Replace each array element with a proper named field in the class. Update the accessors to use the field instead of the array slot. Delete the array when all elements have been replaced. WHY: the array was the transitional mechanism; named fields are the real destination. Each field has a type appropriate to its domain meaning (not all strings).

---

#### Replace Magic Number with Symbolic Constant

**When:** A literal number with special domain meaning appears in the code. The reader cannot tell from the literal what it means.

**Mechanics:**

1. Declare a constant and set it to the value of the magic number. Name the constant after the meaning, not the value (e.g., `GRAVITATIONAL_CONSTANT` not `NINE_POINT_EIGHT_ONE`). WHY: the name is the documentation. A constant named after its value provides no more information than the literal; a constant named after its meaning makes the code self-explanatory.

2. Find all occurrences of the magic number in the codebase. WHY: if the number appears in multiple places and you only replace some, the "constant" now has two representations that can drift.

3. Replace each occurrence with the constant, but only if the usage matches the meaning. WHY: the same numeric value can appear in the code for different reasons (e.g., the number 24 might be hours in a day in one place and an array size in another). Do not replace all occurrences blindly; check that each occurrence represents the same concept.

4. Compile. Verify by changing the constant value temporarily and confirming that all the expected places in the code change behavior — this confirms coverage is complete.

**Alternatives to consider first:**
- If the magic number is the length of an array, use `array.length` instead of a constant. WHY: `array.length` is always correct even if the array size changes; a constant can drift.
- If the magic number is a type code (ENGINEER = 1, SALESMAN = 2), use `type-code-refactoring-selector` instead. WHY: type codes need polymorphism, not just symbolic names.

---

#### Replace Record with Data Class

**When:** Code interfaces with a legacy record structure (from a traditional programming environment, an external API, or a database row) that needs an object-oriented wrapper.

**Mechanics:**

1. Create a class to represent the record. Give it a private field with a getter and a setter for each data item in the record. WHY: the class starts as a dumb data object that matches the external structure. This is intentional — it creates a stable interface between the legacy structure and the rest of the codebase.

2. Once the wrapper exists, apply Encapsulate Field to any public fields, and use Move Method to migrate behavior that operates on the record into the wrapper class. WHY: Replace Record with Data Class is the beginning, not the end. The real value comes when the wrapper grows into a real domain object with its own behavior.

---

#### Duplicate Observed Data

**When:** A GUI class (a window, form, or controller) contains both the domain data (e.g., start date, end date, length of interval) and the business calculations on that data. The business logic cannot be tested without the GUI; it cannot be reused in other contexts.

**This is the most complex refactoring in the chapter.** It requires the Observer pattern (or equivalent event listener mechanism). Apply it when the coupling between GUI and domain is blocking testability or reuse.

**Mechanics:**

1. If no domain class exists for the data, create one. Make it extend or implement an observable/event-source mechanism. WHY: the domain class needs a way to notify the GUI when its data changes; the GUI needs a way to react without the domain class knowing about the GUI.

2. Make the GUI class an observer of the domain class. Store the domain object as a field in the GUI class. WHY: the GUI subscribes to domain changes and updates its controls in response; this is the decoupling mechanism.

3. Apply Self Encapsulate Field on each domain data field within the GUI class. WHY: self-encapsulation is the prerequisite for redirecting the accessor to the domain class later. You cannot redirect scattered direct field access — you can only redirect calls through a single accessor.

4. In each field's event handler, add a call to the setter (using the current field value). WHY: this is the synchronization trigger — when the user changes a field in the GUI, the event fires, the setter runs, and the setter will eventually update the domain object.

5. Add the same field to the domain class with a getter and setter. In the domain setter, trigger notification to observers. WHY: the domain class now owns the canonical value. The notification is what keeps the GUI in sync when the domain changes.

6. Redirect the GUI's getter to read from the domain object. Redirect the GUI's setter to write to the domain object. WHY: the GUI is now a view of the domain data; it does not own the data itself.

7. Implement the observer's update method in the GUI to pull the current value from the domain and update the GUI control. WHY: this is the downstream sync path — when the domain changes (from any source, not just this GUI field), the GUI reflects the change.

8. Once all data is duplicated and synchronized, use Move Method to migrate the business calculation methods from the GUI class to the domain class. WHY: once the domain class has the data, the calculations naturally belong there. The GUI class becomes a pure view.

---

#### Change Unidirectional Association to Bidirectional

**When:** Two classes need to use each other's features, but only a one-way link exists. Adding the reverse link is needed for a new feature.

**Mechanics:**

1. Add a field for the back pointer on the class that currently has no reference. WHY: the back pointer is what makes the association bidirectional; without the field, the reverse navigation does not exist.

2. Decide which class will control the association. Apply this rule: for one-to-many associations, the object that holds the single reference controls; for component-composite associations, the composite controls; for many-to-many, either can control. WHY: one class controlling keeps the pointer-maintenance logic in one place, preventing inconsistency.

3. Create a restricted-access helper method on the non-controlling class to expose the back pointer for the controller's use only. Name it to signal its restricted purpose (e.g., `friendOrders()`). WHY: the helper lets the controlling class maintain consistency without making the back pointer fully public, limiting the surface area for misuse.

4. On the controlling class, modify the setter/modifier to update both pointers: first tell the old related object to remove this; then update this object's pointer; then tell the new related object to add this. WHY: both sides of the association must stay in sync. The three-step update (remove old, set new, add new) handles null cases and prevents a pointer being left dangling.

5. Compile and test. WHY: bidirectional associations are easy to get wrong — the three-step update and the helper method are both error-prone. Test that setting the association from one side is reflected on the other side.

---

#### Change Bidirectional Association to Unidirectional

**When:** A two-way link exists but one end no longer needs the other. Bidirectional associations add complexity: they must be maintained in sync, they can create zombie objects (objects that cannot be garbage-collected because a back pointer keeps them alive), and they introduce coupling between packages.

**Mechanics:**

1. Examine all readers of the field holding the pointer you want to remove. For each reader, determine whether the object can be obtained another way — via a parameter, by traversing from another known object, or via Substitute Algorithm on the getter. WHY: before removing the pointer, you must confirm that every use can be satisfied without it. Finding an alternative is the feasibility gate.

2. If clients need the getter, apply Self Encapsulate Field first, then Substitute Algorithm on the getter body to obtain the object without the field. WHY: Self Encapsulate Field routes all access through one point; Substitute Algorithm changes what that one point returns, eliminating field reads without changing callers.

3. If clients can obtain the object another way, change each caller to get it from that other source. Compile and test after each change. WHY: one-at-a-time changes with compile-and-test between them keeps the code in a working state throughout the refactoring.

4. Once no reader uses the field, remove all assignments to the field and delete the field. WHY: an unread field is dead code; removing it eliminates the maintenance burden and prevents future confusion about why it exists.

---

### Step 3: Verify the New Interface is Complete

**ACTION:** After mechanics are complete, confirm: (1) the old exposure point is gone or private; (2) all callers use the new interface; (3) no callers bypass the new interface through another path.

**WHY:** Data organization refactorings leave behind debris if not verified. A collection field that was encapsulated but still has one caller using the getter to mutate directly is not encapsulated. A primitive replaced with an object but still passed as a raw string through one old parameter path is still a primitive at that path.

Verification checklist:
- Grep for direct field access by external classes (should be zero)
- Grep for the old collection getter usage that modifies the result (should be zero)
- Grep for the removed positional array access patterns (should be zero)
- Grep for the magic number literal (should be zero or only in the constant declaration)
- Confirm the value object has `equals()` and `hashCode()` overridden (if applicable)
- Confirm the reference object's factory enforces single-instance retrieval (if applicable)

---

### Step 4: Identify Follow-On Refactorings

**ACTION:** Look for the next refactoring that the completed refactoring enables.

**WHY:** Data organization refactorings are rarely endpoints. Replace Data Value with Object creates a class that should have behavior moved into it. Encapsulate Collection reveals client code that should be moved to the owning class. The value of each refactoring compounds when the follow-on steps are taken.

Common follow-on sequences:

| Completed refactoring | Natural follow-on |
|---|---|
| Replace Data Value with Object | Move Method — migrate behavior from the old owner to the new class |
| Change Value to Reference | Ensure registry is consistent; check that all creation sites use the factory |
| Encapsulate Collection | Move Method — move iteration/query code from callers to the owning class |
| Replace Array with Object | Move Method — behavior operating on the array slots belongs on the new class |
| Encapsulate Field (on a Data Class) | Move Method — the Data Class smell is not resolved until behavior moves in |
| Duplicate Observed Data | Move Method — business calculation methods migrate from GUI to domain class |

---

## Key Principles

**1. Value vs. reference is a decision that often needs reversing.**
Fowler explicitly notes that this decision is not always clear and frequently needs to be undone. Start with a value object (simpler, no registry needed, no aliasing risk). Convert to a reference object only when the aliasing requirement becomes concrete — when two objects genuinely need to share the same instance so that changes to one are seen by the other.

**2. Immutability is not optional for value objects.**
A mutable value object is worse than no refactoring. If callers copy the reference and then mutate the object through it, they silently affect each other's state. Before completing Change Reference to Value, verify that all setters are removed. If the object cannot become immutable, keep it as a reference object.

**3. Encapsulate Collection is a two-step refactoring.**
The first step is the interface change (add/remove methods, unmodifiable getter). The second step — which most developers skip — is moving the collection-operating code from callers back to the owning class. A collection that is encapsulated but still iterated externally for every operation has the right interface but has not yet earned its encapsulation.

**4. Self Encapsulate Field before Duplicate Observed Data.**
Self Encapsulate Field is the prerequisite for Duplicate Observed Data. Without self-encapsulation, field access is scattered across the GUI class and cannot be redirected to the domain object in a controlled way. Always apply Self Encapsulate Field first, verify it compiles, then proceed to the duplication and synchronization steps.

**5. Magic number replacement requires meaning-matching, not value-matching.**
Replace the literal only where it represents the same concept as the constant's name. The same number value can appear in code for different reasons. Replacing all occurrences of `24` with `HOURS_PER_DAY` will be wrong wherever `24` means something else entirely.

---

## Examples

### Example 1: Primitive Obsession — Telephone Number

**Scenario:** An `Employee` class has a `String telephoneNumber` field. Methods on `Employee` and its callers format the number, extract the area code, and validate the format in multiple places.

**Selection:** Replace Data Value with Object — the primitive has accumulated behavior that belongs on a class.

**Execution:**
1. Create `TelephoneNumber` class with `String _number` field, constructor `TelephoneNumber(String number)`, and getter `getNumber()`.
2. Change `Employee._telephoneNumber` type from `String` to `TelephoneNumber`.
3. Update `Employee`'s getter: `String getTelephoneNumber() { return _telephoneNumber.getNumber(); }`
4. Update constructor: `_telephoneNumber = new TelephoneNumber(number);`
5. Update setter: `_telephoneNumber = new TelephoneNumber(number);`
6. Move `formatNumber()`, `getAreaCode()`, and `isValid()` from `Employee` to `TelephoneNumber`.

**Value vs. reference decision:** Is a TelephoneNumber a real-world entity with independent identity? No — it is defined by its digits. Two `TelephoneNumber` objects with the same string are equal. Keep it as a value object. Implement `equals()` and `hashCode()` on the number string.

---

### Example 2: Data Class with Collection — Person and Courses

**Scenario:** `Person` has a `Set _courses` field with `getCourses()` and `setCourses(Set)` methods. Callers do: `person.getCourses().add(new Course(...))` and iterate the set externally to count advanced courses.

**Selection:** Encapsulate Collection — the collection is directly mutable by callers.

**Execution:**
1. Add `addCourse(Course arg) { _courses.add(arg); }` and `removeCourse(Course arg) { _courses.remove(arg); }`.
2. Initialize: `private Set _courses = new HashSet();`
3. Change the setter to `initializeCourses(Set arg)` that asserts the collection is empty then calls `addCourse` for each element. Or remove the setter entirely if callers can use `addCourse` directly.
4. Find `person.getCourses().add(...)` callers and change to `person.addCourse(...)`.
5. Change getter: `public Set getCourses() { return Collections.unmodifiableSet(_courses); }`
6. Move the advanced-course-counting iteration into `Person` as `numberOfAdvancedCourses()` — the external iteration was Feature Envy on `Person`'s data.

---

### Example 3: Value vs. Reference — Customer Object

**Scenario:** After applying Replace Data Value with Object to a customer name string in `Order`, the `Customer` class exists but each order creates its own Customer object. A requirement arrives: update the credit rating for a customer, and all their orders must see the change.

**Selection:** The aliasing requirement is now concrete — multiple orders need the same customer instance. Apply Change Value to Reference.

**Execution:**
1. Add factory method: `public static Customer create(String name) { return new Customer(name); }` Make constructor private.
2. Create registry: `private static Dictionary _instances = new Hashtable();` and a private `store()` method that puts `this` in the registry by name.
3. Pre-load known customers: `Customer.loadCustomers()` populates the registry at startup.
4. Change factory to retrieve: `public static Customer getNamed(String name) { return (Customer) _instances.get(name); }`
5. Change `Order` constructor and setter to use `Customer.getNamed(name)` instead of `new Customer(name)`.

Result: all orders pointing to the same customer name now share one Customer object. Changes to credit rating are visible everywhere.

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/value-vs-reference-guide.md` | Detailed decision tree for value vs. reference with distributed systems considerations, aliasing risk patterns, and language-specific equality semantics | Step 2 — value/reference decision |
| `references/collection-encapsulation-patterns.md` | Language-specific collection encapsulation patterns: Java unmodifiable views, Python properties and frozenset, TypeScript readonly arrays | Step 2 — Encapsulate Collection mechanics |

**Sibling skill relationships:**
- `code-smell-diagnosis` — run first to identify which data smell is present before selecting a refactoring
- `type-code-refactoring-selector` — for type code integers and enums that drive switch statement behavior; not covered by this skill
- `class-responsibility-realignment` — when Feature Envy or Inappropriate Intimacy is the primary smell alongside data problems
- `method-decomposition-refactoring` — when Long Method is present in the same class; often co-occurs with Data Class smell

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler and Kent Beck.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-code-smell-diagnosis`
- `clawhub install bookforge-type-code-refactoring-selector`
- `clawhub install bookforge-class-responsibility-realignment`
- `clawhub install bookforge-method-decomposition-refactoring`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
