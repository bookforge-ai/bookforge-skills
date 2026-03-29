# Reuse Mechanisms in Object-Oriented Design

Detailed comparison of the four mechanisms for reusing functionality in OO systems. Read this when evaluating which mechanism to recommend for a specific design, or when a violation requires a specific refactoring path.

Source: *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF), Chapter 1, pages 28-34.

---

## Overview: The Four Mechanisms

| Mechanism | Defined at | Encapsulation | Run-time flexibility | Implementation dependency |
|-----------|-----------|---------------|---------------------|--------------------------|
| Class inheritance | Compile-time | Broken (white-box) | None | High |
| Interface inheritance | Compile-time | Preserved | None | None |
| Object composition | Run-time | Preserved (black-box) | High | Low |
| Parameterized types (generics/templates) | Compile-time | Preserved | None | Low |

---

## 1. Class Inheritance (White-Box Reuse)

**What it is:** Defining one class's implementation in terms of another's. The subclass inherits the parent's data representation and operations.

**Why it's called white-box:** The internals of the parent class are often visible to (and depended on by) the subclass. The subclass can see HOW the parent works, not just WHAT it promises.

**Advantages:**
- Defined statically at compile-time — straightforward and directly supported by the language
- Easy to modify the implementation being reused — subclass can override specific operations
- Less code — inheriting most of what you need from an existing class

**Disadvantages:**
1. **Cannot change at run-time** — the class relationship is fixed at compile-time. If you need a different behavior, you need a different class.
2. **Breaks encapsulation** — parent classes often define part of subclasses' physical representation. Because inheritance exposes a subclass to details of its parent's implementation, it is said that "inheritance breaks encapsulation." (Snyder, 1986)
3. **Subclass bound to parent implementation** — the implementation of a subclass becomes so bound up with the implementation of its parent class that any change in the parent's implementation will force the subclass to change.
4. **Implementation dependency** — if any aspect of the inherited implementation is not appropriate for new problem domains, the parent class must be rewritten or replaced. This dependency limits flexibility and ultimately reusability.

**When to use:**
- The subclass is truly a subtype of the parent (satisfies the Liskov Substitution Principle)
- The parent is abstract (provides no implementation — only interface) — this is the safe case
- You need to create families of objects with identical interfaces (polymorphism)
- Implementation sharing is secondary; the primary goal is subtype relationship

**The cure for inheritance misuse:** Inherit only from abstract classes, since they usually provide little or no implementation. This eliminates implementation dependencies while preserving the interface relationship.

---

## 2. Interface Inheritance (Subtyping)

**What it is:** Describing when an object can be used in place of another — defining substitutability, not implementation sharing.

**How it differs from class inheritance:** Class inheritance defines implementation. Interface inheritance defines type compatibility. An object can have many types; objects of different classes can have the same type.

**In practice:**
- **C++/Eiffel:** Inherit from pure abstract classes (classes with only pure virtual functions). Public inheritance from a class with pure virtual functions approximates interface inheritance.
- **Java/C#:** Implement interfaces (keyword: `implements`).
- **Python/Smalltalk/duck-typed languages:** Structural compatibility — if an object responds to the messages expected, it satisfies the type.

**Benefits:**
- Clients remain unaware of the specific types of objects they use (as long as objects adhere to the expected interface)
- Clients remain unaware of which class implements those objects
- Greatly reduces implementation dependencies between subsystems

**The GoF principle it enables:** *Program to an interface, not an implementation.*

**Design patterns that depend on this distinction:**
- Chain of Responsibility — objects must have a common type but usually don't share a common implementation
- Composite — Component defines a common interface; Composite often defines a common implementation
- Command, Observer, State, Strategy — often implemented with abstract classes that are pure interfaces

---

## 3. Object Composition (Black-Box Reuse)

**What it is:** Assembling or composing objects to get more complex functionality. New functionality is obtained by assembling existing objects rather than defining it in a new class.

**Why it's called black-box:** Objects are accessed solely through their interfaces. No internal details of composed objects are visible to the composing object. Objects appear only as "black boxes."

**How it works:** Requires that objects being composed have well-defined interfaces. The composing object holds a reference to a component object and calls its interface to get behavior. The component can be replaced at run-time by any other object with the same interface/type.

**Advantages:**
1. **Run-time flexibility** — any object can be replaced at run-time by another as long as it has the same type. Behavior can change dynamically.
2. **Preserved encapsulation** — objects are accessed only through interfaces; no white-box visibility into internals.
3. **Fewer implementation dependencies** — because implementation is written in terms of object interfaces, there are substantially fewer implementation dependencies.
4. **Smaller, focused classes** — favoring composition keeps each class encapsulated and focused on one task. Class hierarchies remain small and manageable.
5. **Behavior defined by interrelationships** — a design based on object composition has more objects (if fewer classes), and the system's behavior depends on their interrelationships instead of being defined in one large class.

**Disadvantages:**
- More objects to manage and understand
- Dynamic, highly parameterized software is harder to understand than more static software
- Requires carefully designed interfaces that don't stop you from using one object with many others

**When to use:**
- Behavior needs to vary at run-time
- The reuse relationship is "has-a" rather than "is-a"
- You want to keep classes encapsulated and focused on single responsibilities
- You want to avoid the fragile base class problem
- New components need to be composed with old ones (inheritance and composition work together here)

**The GoF principle it enables:** *Favor object composition over class inheritance.*

**Practical note from GoF:** Ideally, you shouldn't have to create new components to achieve reuse — just assemble existing components through composition. In practice, available components are never quite rich enough. Reuse by inheritance makes it easier to create new components that can be composed with old ones. Inheritance and composition thus work together.

---

## 4. Delegation

**What it is:** A specific form of composition where a receiving object delegates operations to a delegate object. Delegation makes composition as powerful for reuse as inheritance.

**How it differs from simple composition:** In true delegation, the receiver passes itself (`this` in C++, `self` in Smalltalk) to the delegate, so the delegated operation can refer back to the receiver. This is analogous to subclasses deferring requests to parent classes, but without inheritance.

**The Window/Rectangle canonical example:**
- Instead of: `class Window extends Rectangle` (Window is a Rectangle — class inheritance)
- Use: `class Window { private Rectangle rectangle; }` (Window has a Rectangle — delegation)
- Window delegates area calculations to its Rectangle instance
- Window can become circular at run-time by replacing its Rectangle with a Circle instance (same type)

**Main advantage:** Easy to compose behaviors at run-time and to change the way they're composed. Behaviors can be swapped by swapping the delegate.

**The critical test:** "Does this delegation simplify more than it complicates?"
- Delegation has a disadvantage it shares with other composition techniques: dynamic, highly parameterized software is harder to understand than more static software
- There are also run-time inefficiencies
- Delegation is a good design choice only when it simplifies more than it complicates
- It isn't easy to give rules for when to use delegation — it depends on context and experience
- **Delegation works best when it's used in highly stylized ways — that is, in standard patterns**

**Patterns that use delegation heavily:**
- **State** — an object delegates requests to a State object representing its current state. As state changes, the delegate changes, so behavior changes at run-time without changing the object's class.
- **Strategy** — an object delegates a specific request to an object representing a strategy for carrying out that request. An object can have many strategies for different requests.
- **Visitor** — the operation performed on each element of an object structure is always delegated to the Visitor object.

**Patterns that use delegation lightly:**
- **Mediator** — sometimes implements operations by forwarding to other objects; other times passes a reference to itself (true delegation).
- **Chain of Responsibility** — forwards requests from one object to another; sometimes carries a reference to the original receiver (delegation).
- **Bridge** — if abstraction and implementation are closely matched, the abstraction may simply delegate operations to that implementation.

---

## 5. Parameterized Types (Generics / Templates)

**What it is:** A third way (in addition to class inheritance and object composition) to compose behavior in OO systems. Lets you define a type without specifying all the other types it uses — unspecified types are supplied as parameters at the point of use.

**Known as:**
- **Generics** in Ada, Eiffel, Java, C#
- **Templates** in C++
- Not natively supported in Smalltalk (which doesn't have compile-time type checking)

**Example:** A `List` class parameterized by element type. `List<Integer>` vs `List<String>` — the List algorithm is the same; the element type is a parameter.

**Key comparison with inheritance and composition:**

| | Class inheritance | Object composition | Parameterized types |
|---|---|---|---|
| When bound | Compile-time | Run-time | Compile-time |
| Can change behavior at run-time | No | Yes | No |
| Default implementations | Yes (inherited) | No (must delegate) | Language-specific |
| Changes types used | No | No | Yes |

**Limitations:** Neither inheritance nor parameterized types can change at run-time. Which approach is best depends on design and implementation constraints.

**GoF note:** None of the GoF patterns concern parameterized types, though they are used occasionally to customize C++ implementations. Parameterized types are not needed at all in languages like Smalltalk that lack compile-time type checking.

---

## Decision Guide: Which Mechanism to Use

```
Need to vary behavior at RUN-TIME?
    YES → Object composition (or delegation)
    NO  → Continue below

Is this a genuine IS-A subtype relationship?
    YES → Consider interface inheritance (define the contract)
         → If implementation sharing is also needed: class inheritance from ABSTRACT class only
    NO  → Object composition ("has-a" relationship)

Is the parent class concrete (not abstract)?
    YES → Red flag: white-box reuse. Consider extracting interface + composition.
    NO  → Abstract inheritance is safe.

Does the subclass need to understand parent internals to work correctly?
    YES → White-box reuse violation. Refactor to composition.
    NO  → Inheritance may be appropriate.

Does the hierarchy have more than 2 levels of concrete inheritance?
    YES → Likely overuse of inheritance. Evaluate flattening with composition.
    NO  → Acceptable if each level represents a genuine subtype.

Does the reuse need to vary by type parameter (generic algorithm, different element types)?
    YES → Parameterized types (generics/templates)
    NO  → Inheritance or composition as above.
```

---

## Run-Time vs Compile-Time Structures

An OO program's **run-time structure** (the network of communicating objects) often bears little resemblance to its **compile-time structure** (classes in fixed inheritance relationships).

- **Compile-time:** Frozen in inheritance relationships. Static. Determined by the code.
- **Run-time:** Rapidly changing networks of communicating objects. Dynamic. Determined by object interactions.

The two structures are largely independent. Understanding one from the other is difficult — like trying to understand the dynamism of a living ecosystem from the static taxonomy of plants and animals.

Many design patterns (especially those with object scope) capture the distinction between compile-time and run-time structures explicitly:
- **Composite** and **Decorator** — especially useful for building complex run-time structures
- **Observer** — involves run-time structures that are often hard to understand unless you know the pattern
- **Chain of Responsibility** — results in communication patterns that inheritance doesn't reveal

**Implication for evaluation:** When assessing a design, ask not just "what does the class hierarchy look like?" but "what does the run-time object graph look like?" A design that looks clean statically may have brittle or inflexible run-time behavior if inheritance was used where composition was needed.

---

## Aggregation vs Acquaintance

Both are forms of object relationships implemented as references, but their intent differs significantly.

**Aggregation:**
- One object *owns* or is *responsible for* another
- An object *has* or is *part of* another
- Aggregate object and its owner have identical lifetimes
- Stronger relationship — fewer, more permanent
- Notation: arrowhead line with a diamond at the base

**Acquaintance (association / "using" relationship):**
- One object merely *knows of* another
- Acquainted objects may request operations of each other, but aren't responsible for each other
- Weaker coupling — acquaintances are made and remade frequently, sometimes only for the duration of an operation
- More dynamic, harder to discern in source code
- Notation: plain arrowhead line

**Why the distinction matters:** Acquaintance and aggregation are often implemented the same way in code (both as pointers or references). The distinction is determined more by intent than by explicit language mechanisms. Treating an acquaintance as if it were an aggregate creates unnecessary coupling. Treating an aggregate as a mere acquaintance risks lifetime management bugs.

In evaluation: ask whether a reference represents ownership (aggregate — shared lifetime, owning class responsible) or knowledge (acquaintance — loose, dynamic, temporary). Designs that conflate these tend to have lifecycle bugs or unnecessarily tight coupling.
