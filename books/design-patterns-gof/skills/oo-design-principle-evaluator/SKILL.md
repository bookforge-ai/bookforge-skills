---
name: oo-design-principle-evaluator
description: |
  Evaluate object-oriented designs against the two foundational GoF principles: 'Program to an interface, not an implementation' and 'Favor object composition over class inheritance.' Use when reviewing class hierarchies, assessing reuse strategies, or deciding between inheritance and composition for a specific design problem. Identifies violations like white-box reuse, broken encapsulation from subclassing, concrete class coupling, delegation overuse, and inheritance hierarchies that should be flattened. Use when someone says 'should I use inheritance or composition here', 'is this class hierarchy right', 'my subclass is breaking when the parent changes', 'how do I make this more flexible', 'is this design too rigid', 'I want to change behavior at runtime', or 'review my OO design for best practices'. Produces a design principle compliance report with specific violations and recommended refactoring.
model: sonnet
context: 1M
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: codebase
      description: "Class definitions, inheritance hierarchies, or design descriptions to evaluate"
    - type: none
      description: "Skill can also work from a verbal description of the design"
  tools-required: [Read, TodoWrite]
  tools-optional: [Grep, Bash]
  environment: "Can run from any directory; codebase access improves analysis depth"
---

# OO Design Principle Evaluator

## When to Use

Use this skill when you are:
- **Reviewing a class hierarchy** — assessing whether inheritance is being used correctly or overused
- **Deciding between inheritance and composition** — need a principled recommendation for a specific design choice
- **Diagnosing brittleness** — a subclass is breaking when parent classes change, indicating broken encapsulation
- **Designing for flexibility** — want behavior that can change at runtime, which inheritance cannot provide
- **Code reviewing OO designs** — evaluating whether a design follows established reuse best practices

Preconditions: you have at least one of:
- Source code with class definitions and inheritance relationships
- A verbal or written description of the class hierarchy and how classes relate
- A UML diagram or design document describing the object model

**Agent:** Before starting, confirm whether you have access to source code or only a description. Code access enables deeper analysis (scanning for concrete class instantiation, checking method override patterns). A description enables principle-level analysis.

## Context & Input Gathering

### Input Sufficiency Check

```
User prompt → Extract the design being evaluated (classes, relationships, context)
                    ↓
Environment → Scan for class files, inheritance declarations, interface definitions
                    ↓
Gap analysis → Do I know WHAT is being evaluated and WHY they're concerned?
                    ↓
         Missing critical info? ──YES──→ ASK (one question at a time)
                    │
                    NO
                    ↓
              PROCEED with analysis
```

### Required Context (must have — ask if missing)

- **The design being evaluated:** What classes, relationships, or hierarchy is under review?
  → Check prompt for: class names, inheritance descriptions, "extends"/"inherits" language, code snippets
  → Check environment for: source files with class definitions, UML files, design docs
  → If still missing, ask: "Can you describe the class hierarchy or share the relevant code? I need to know which classes inherit from which, and what behavior each class is trying to reuse or extend."

- **The design goal:** What is the design trying to achieve? What problem does the hierarchy solve?
  → Check prompt for: stated purpose, feature description, problem context
  → If still missing, ask: "What behavior are you trying to reuse or share across these classes? Understanding the goal helps me assess whether inheritance is the right mechanism."

### Observable Context (gather from environment)

- **Concrete class instantiation:** Look for `new ConcreteClass()` in client code — signals coupling to implementation rather than interface.
  → Look for: constructor calls, direct class references in field declarations, factory-less instantiation
  → If unavailable: assess from description

- **Abstract class / interface usage:** Check whether clients depend on abstractions or concrete types.
  → Look for: abstract classes, interfaces, protocol declarations, abstract base classes
  → If unavailable: assume based on user description

- **Override patterns:** Identify whether subclasses merely add behavior or override parent internals.
  → Look for: method overrides that call `super`, overrides that replace parent logic entirely
  → If unavailable: note as unverifiable

### Default Assumptions

- If language is not specified: assume a statically typed OO language (Java, C#, C++) where the inheritance-vs-composition distinction is most consequential.
- If no design context given: assume production code under active development (not a throwaway prototype), so flexibility and maintainability matter.
- If no explicit goal stated: assume the design should support future extension without modification.

### Questioning Guidelines

Ask ONE question at a time, most critical first. Show what you already know before asking. State why you need the information.

## Process

Use `TodoWrite` to track steps before beginning.

```
TodoWrite([
  { id: "1", content: "Gather design context and identify all classes/relationships", status: "pending" },
  { id: "2", content: "Apply Principle 1: Program to interface, not implementation", status: "pending" },
  { id: "3", content: "Apply Principle 2: Favor composition over inheritance", status: "pending" },
  { id: "4", content: "Evaluate delegation usage (simplifies vs complicates)", status: "pending" },
  { id: "5", content: "Assess run-time vs compile-time flexibility needs", status: "pending" },
  { id: "6", content: "Produce compliance report with violations and recommendations", status: "pending" }
])
```

---

### Step 1: Map the Design

**ACTION:** Build a structural map of the design — all classes, their inheritance relationships, interfaces or abstract types they implement, and how clients reference them.

**WHY:** You cannot evaluate OO principles without first understanding the structure. Many violations are invisible until you see the full inheritance tree. A class that looks reasonable in isolation may reveal a 5-level deep hierarchy when mapped completely — a strong signal of inheritance overuse.

**AGENT: EXECUTES** — read source files or extract from user description

If code is available:
- Identify all classes and their parent classes
- Identify all interfaces/abstract classes used
- Note which types appear in field declarations, method parameters, and return types in client code
- Note any `new ConcreteClass()` calls in clients

If only description is available:
- Reconstruct the hierarchy from user's explanation
- Note any ambiguities explicitly in the report

Mark Step 1 complete in TodoWrite.

---

### Step 2: Apply Principle 1 — Program to an Interface, Not an Implementation

**ACTION:** For each relationship where a client holds a reference to another object, determine whether the client is coupled to an interface/abstract type or a concrete class.

**WHY:** When clients depend on concrete classes, changes to those classes force changes in clients. This creates cascading modifications — the opposite of reusable design. Programming to an interface means clients only know about the abstract contract, not the specific class behind it. Two benefits follow: (1) clients remain unaware of the specific type of object they use, and (2) clients remain unaware of which class implements that object. This greatly reduces implementation dependencies between subsystems.

**Violation signals to look for:**

| Signal | What it means |
|--------|---------------|
| Field declared as `ConcreteClass foo` | Client coupled to implementation |
| Method parameter typed as `ConcreteClass` | Caller must provide a specific class, not any compatible type |
| `new ConcreteClass()` scattered through client code | Object creation mixed with business logic; no interface boundary |
| No abstract class or interface in the hierarchy | Nothing defines a contract independent of implementation |
| Subclass inheriting from a concrete class | Inheriting implementation details, not just interface |

**Class vs Interface Inheritance — critical distinction:**
- **Class inheritance** defines an object's implementation in terms of another's implementation. It is a mechanism for code and representation sharing.
- **Interface inheritance** (subtyping) describes when an object can be used in place of another — it defines substitutability, not implementation sharing.

Confusing these two is a root cause of brittle designs. A class can inherit an interface (what it can do) without inheriting implementation (how it does it). Pure interface inheritance in C++ means inheriting from abstract classes with pure virtual functions. In Java/C#, it means implementing interfaces. In Python/duck-typed languages, structural compatibility serves the same role.

**Detection question:** "Is the client bound to HOW this object does its job, or only to WHAT it promises to do?"

Mark Step 2 complete in TodoWrite.

---

### Step 3: Apply Principle 2 — Favor Composition over Inheritance

**ACTION:** For each use of class inheritance (not interface inheritance), assess whether it is justified or whether object composition would serve better.

**WHY:** Inheritance is defined at compile-time and cannot change at run-time. It also breaks encapsulation: parent classes often define at least part of a subclass's physical representation, exposing internal details. This makes subclasses so bound to their parent's implementation that any change in the parent forces a change in the subclass — the "fragile base class" problem. Object composition, by contrast, is defined dynamically at run-time. Objects acquired through composition are accessed only through their interfaces, so encapsulation is preserved. Any object can be replaced at run-time by another of the same type.

**Four inheritance failure modes to check:**

1. **Cannot change behavior at run-time** — Does the design require behavior to switch dynamically? Inheritance fixes behavior at compile-time; composition allows swapping collaborators at run-time.

2. **Broken encapsulation** — Does the subclass depend on parent internals? Inheriting from a concrete class often means the subclass must understand the parent's implementation, not just its interface. This is white-box reuse.

3. **Subclass permanently bound to parent** — If ANY aspect of the inherited implementation is inappropriate for new problem domains, the parent must be rewritten or replaced. This limits reusability.

4. **Implementation dependency chain** — Does the design have deeply nested concrete inheritance? Each level adds a dependency. The cure: inherit only from abstract classes, which provide little or no implementation and therefore create no implementation dependencies.

**White-box vs black-box reuse:**
- **White-box reuse (inheritance):** Internal details of the parent are visible to the subclass. The subclass knows HOW the parent works. Changes to parent internals break subclasses.
- **Black-box reuse (composition):** Composed objects are accessed only through their interfaces. The composing object knows only WHAT the component does, not HOW.

**Assessment questions:**
- "If the parent class changes its internal implementation, does the subclass break?"
- "Does the subclass need to override methods that call other parent methods (fragile override chains)?"
- "Could this behavior be achieved by holding a reference to a collaborator object instead of inheriting from it?"
- "Does this hierarchy keep each class encapsulated and focused on one task, or does it create large entangled hierarchies?"

Mark Step 3 complete in TodoWrite.

---

### Step 4: Evaluate Delegation Usage

**ACTION:** Identify any use of delegation (a class forwarding requests to a component it holds a reference to). Assess whether each delegation point simplifies or complicates the design.

**WHY:** Delegation is a way to make composition as powerful as inheritance for reuse. The key test is: "Does this delegation simplify more than it complicates?" Delegation makes software more flexible but also harder to understand — dynamic, highly parameterized software is harder to read than more static software. There are also run-time inefficiencies. Delegation is a good design choice only when it simplifies more than it complicates. It works best when used in well-established patterns (Strategy, State, Visitor) rather than ad hoc.

**How delegation works:** In delegation, two objects handle a request: the receiver delegates the operation to its delegate. The receiver passes itself to the delegate so the delegated operation can refer back to the receiver. The main advantage: behaviors can be composed and changed at run-time by replacing the delegate object (as long as the replacement has the same type/interface).

**The Window/Rectangle test:** Instead of making Window a subclass of Rectangle (because windows are rectangular), Window holds a Rectangle instance and delegates area calculations to it. Window "has a" Rectangle rather than "is a" Rectangle. This is delegation enabling composition. The question: is this clearer than inheritance would have been?

**Delegation assessment signals:**
- Delegation that enables run-time behavior change → justified
- Delegation following a named pattern (Strategy, State, Bridge) → justified, works in "stylized ways"
- Ad hoc delegation chains with many small forwarding methods → may complicate more than simplify
- Delegation introduced where a simple method call would suffice → likely overengineered

Mark Step 4 complete in TodoWrite.

---

### Step 5: Assess Run-Time vs Compile-Time Structure

**ACTION:** Identify where the design's flexibility requirements are run-time vs compile-time, and check whether the mechanism used matches the need.

**WHY:** An OO program's run-time structure often bears little resemblance to its compile-time code structure. Compile-time structure is frozen in inheritance relationships. Run-time structure is the network of communicating objects — which is far more dynamic. Inheritance cannot provide run-time flexibility; composition can. Designs that try to use inheritance to achieve run-time variability end up requiring new subclasses for every behavioral variant — a combinatorial explosion.

**Also assess aggregation vs acquaintance:**
- **Aggregation:** One object owns or is responsible for another; they share identical lifetimes. Stronger relationship — changes to the aggregate affect the component.
- **Acquaintance (association):** One object merely knows about another; they aren't responsible for each other. Weaker relationship, more dynamic — acquaintances are made and remade more frequently, sometimes only for the duration of one operation.

Both are often implemented the same way in code (as references), but their INTENT differs. Designs that treat acquaintances as if they were aggregates create unnecessary coupling.

Mark Step 5 complete in TodoWrite.

---

### Step 6: Produce the Compliance Report

**ACTION:** Write a structured design principle compliance report covering all findings from Steps 2-5.

**WHY:** The report must be specific and actionable. Identifying "uses inheritance" is not useful. Identifying "class `ReportGenerator` inherits from `DatabaseConnection` to reuse connection pooling, but connection strategy cannot change at run-time and a change to `DatabaseConnection`'s pool sizing logic will force changes in `ReportGenerator`" is useful — and immediately points to the refactoring (extract an interface, inject a connection strategy via composition).

**HANDOFF TO HUMAN** — the agent prepares the report; the human reviews, prioritizes, and executes refactoring.

**Report format:**

```markdown
# OO Design Principle Compliance Report

## Design Under Review
[Brief description of what was evaluated]

## Principle 1: Program to an Interface, Not an Implementation
**Compliance:** [Compliant / Partial / Violated]

### Violations Found
- [Class/relationship]: [Specific violation description and why it matters]

### Recommendations
- [Specific refactoring: what to change and what pattern/structure to use instead]

## Principle 2: Favor Composition over Inheritance
**Compliance:** [Compliant / Partial / Violated]

### Inheritance Failure Modes Detected
- [ ] Cannot change behavior at run-time
- [ ] Broken encapsulation (white-box reuse)
- [ ] Subclass permanently bound to parent implementation
- [ ] Implementation dependency chain (concrete inheritance depth > 1)

### Violations Found
- [Class/relationship]: [Specific violation with failure mode]

### Recommendations
- [Specific refactoring: what composition structure to use, which pattern applies]

## Delegation Assessment
**Usage:** [Not present / Appropriate / Overused / Underused]
- [Finding]: [Simplifies or complicates, and why]

## Run-Time vs Compile-Time Structure
**Flexibility match:** [Matched / Mismatched]
- [Finding]: [Where run-time flexibility is needed but compile-time mechanism was used, or vice versa]

## Aggregation vs Acquaintance
- [Any relationships where intent doesn't match implementation]

## Summary
**Overall compliance:** [High / Medium / Low]
**Priority refactorings:**
1. [Most impactful change]
2. [Second priority]
3. [Third priority]

**What to preserve:** [Aspects of the design that are already well-structured]
```

Mark Step 6 complete in TodoWrite.

## Inputs

- **Class definitions or design description:** source code, UML diagram, verbal description of the hierarchy
- **Design context:** what the hierarchy is trying to achieve (reuse goal, feature being modeled)
- **Language/framework:** helps calibrate which mechanisms are available (interfaces, abstract classes, generics/templates)

## Outputs

- **Design Principle Compliance Report** (Markdown) — structured assessment with violations, failure modes, and specific refactoring recommendations
- **Decision rationale** — for each recommendation, the WHY (which principle is violated, which failure mode applies)

## Key Principles

- **Distinguish class inheritance from interface inheritance** — class inheritance shares implementation and breaks encapsulation; interface inheritance defines substitutability. A design can use interface inheritance without white-box reuse. The violation is class inheritance where only interface inheritance is needed.

- **Inheritance is a compile-time commitment; composition is a run-time commitment** — when behavior must vary at run-time, composition is not optional. Inheritance cannot fulfill this need without creating new subclasses for every variant. Evaluate what flexibility the design actually requires before prescribing either mechanism.

- **White-box reuse is a red flag, not a feature** — inheriting from a concrete class means the subclass knows the parent's internals. This is usually described as "convenient" but is actually a coupling problem. Evaluate whether the convenience is worth the brittleness.

- **Delegation is good only when it simplifies more than it complicates** — not every method forwarding is delegation in the GoF sense. True delegation passes `self` to the delegate so the delegate can refer back to the receiver. Assess whether the indirection is earning its complexity cost.

- **Small, encapsulated classes with clear interfaces beat deep hierarchies** — favoring composition keeps each class focused on one task. Hierarchies grow into unmanageable monsters when inheritance is the default reuse mechanism. The question is not "can I inherit?" but "should I inherit, or does holding a reference serve better?"

- **Abstract classes are the safe inheritance target** — inheriting from abstract classes creates minimal implementation dependencies because abstract classes provide little or no implementation. When inheritance is genuinely warranted, the parent should be abstract.

## Examples

**Scenario: Animal hierarchy with behavior coupling**
Trigger: "I have `Animal → Bird → Duck` with `fly()` defined on `Bird`. Now I need `Penguin` and `Ostrich` and I'm stuck."
Process:
1. Map hierarchy: `Animal` (abstract) → `Bird` (concrete, has `fly()`) → `Duck`, `Penguin`, `Ostrich`
2. Principle 1 check: `Bird` is concrete with `fly()` implementation — subclasses inherit implementation, not just interface. If clients reference `Bird`, they're coupled to the flying implementation.
3. Principle 2 check: `fly()` behavior cannot change at run-time. `Penguin` must override `fly()` to throw or do nothing — a violation of substitutability. The hierarchy is trying to share behavior that not all subtypes share.
4. Failure modes: broken encapsulation (Penguin must override parent internals), subclass bound to parent (Penguin must know Bird's flying assumption).
5. Recommendation: Extract a `FlyingBehavior` interface. `Bird` holds a reference to `FlyingBehavior` (composition). `Duck` gets `StandardFlight`, `Penguin` gets `NoFlight`, new birds get the right behavior without touching the hierarchy. Birds that develop flight mutations at runtime can swap behaviors.
Output: Compliance report identifying white-box reuse violation, recommending Strategy pattern for flying behavior.

---

**Scenario: Window inheriting from Rectangle**
Trigger: "My `Window` class extends `Rectangle` because windows are rectangular and I wanted the area calculation."
Process:
1. Map hierarchy: `Window extends Rectangle`. Client code uses `Window` directly.
2. Principle 1 check: `Window` is coupled to `Rectangle`'s implementation. If window shape changes (not all windows are rectangular), `Window` must change its parent or override geometry methods.
3. Principle 2 check: Window "is a" Rectangle is the claim, but "Window has a shape" is more accurate. The reuse is purely for `Area()` — implementation reuse, not subtype substitutability. If `Rectangle`'s area formula changes (e.g., to account for different coordinate systems), `Window` inherits the change whether it wants it or not.
4. Failure modes: cannot change shape at run-time (a `Window` is always a `Rectangle`); white-box reuse (Window depends on Rectangle's implementation of area).
5. Recommendation: `Window` holds a `Shape` interface reference. Area calculation is delegated to the `Shape`. At run-time, `Window` can be circular by replacing its `Shape` delegate. This is the GoF delegation pattern.
Output: Report recommending delegation over inheritance; notes this is exactly the Window/Rectangle canonical delegation example.

---

**Scenario: Plugin system using abstract base class correctly**
Trigger: "We have an abstract `DataExporter` with concrete `CsvExporter`, `JsonExporter`, `XmlExporter`. Is this design OK?"
Process:
1. Map hierarchy: `DataExporter` (abstract, defines interface) → `CsvExporter`, `JsonExporter`, `XmlExporter` (concrete, all siblings, no further inheritance).
2. Principle 1 check: If client code references `DataExporter` (the abstract type), not the concrete exporters — compliant. Creational patterns or factories handle instantiation, keeping client code decoupled.
3. Principle 2 check: Each concrete exporter inherits from an abstract class (no implementation to inherit, only interface). No white-box reuse. Each exporter is focused and encapsulated. No deep hierarchy.
4. Failure modes: None detected. Runtime flexibility is preserved — a new exporter can be added without modifying clients.
5. Recommendation: Compliant design. Verify client code uses `DataExporter` type, not concrete types. If new exporters need shared utility methods, add them to `DataExporter` as concrete methods carefully, or extract to a separate utility class to avoid introducing implementation coupling.
Output: Report with High compliance rating; notes the design correctly uses abstract class as a pure interface target.

## References

- For detailed comparison of all reuse mechanisms with decision criteria, see [reuse-mechanisms.md](references/reuse-mechanisms.md)
- Source: *Design Patterns: Elements of Reusable Object-Oriented Software*, GoF (Gang of Four), Chapter 1, pages 28-34

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns Gof by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
