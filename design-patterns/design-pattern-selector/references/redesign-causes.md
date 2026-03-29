# 8 Causes of Redesign — Mapped to Design Patterns

Source: Design Patterns: Elements of Reusable Object-Oriented Software (GoF, 1994), pp. 34–36, "Designing for Change."

## Purpose

Use this table when you can articulate **what pain you are experiencing** or **what risk you are trying to avoid**. Each cause describes a design dependency that makes software fragile — brittle to change, hard to reuse, or expensive to maintain. The mapped patterns eliminate or reduce that specific dependency.

Key principle from the GoF: *"Each design pattern lets some aspect of system structure vary independently of other aspects, thereby making a system more robust to a particular kind of change."*

---

## The 8 Causes

### 1. Creating an object by specifying a class explicitly

**The problem:** Specifying a concrete class name when creating an object commits you to a particular implementation rather than an interface. Future changes to that concrete class ripple through all call sites.

**Symptom:** `new ConcreteProductX()` scattered throughout client code. Swapping implementations requires changing many files.

**Design patterns:**
- **Abstract Factory** — creates families of related objects without naming concrete classes
- **Factory Method** — lets subclasses decide which class to instantiate
- **Prototype** — creates new objects by cloning a prototypical instance; the class is never named explicitly

---

### 2. Dependence on specific operations

**The problem:** Hard-coding the way a request is satisfied commits you to one implementation at both compile-time and run-time. Changing how the request is handled requires modifying code that should not care.

**Symptom:** `if (requestType == "A") doA(); else if (requestType == "B") doB();` — business logic tangled with dispatch logic. Cannot add new request handling without modifying existing code.

**Design patterns:**
- **Chain of Responsibility** — decouples sender from receiver; any object in the chain can handle the request
- **Command** — encapsulates a request as an object; handling can be changed, queued, logged, or undone independently

---

### 3. Dependence on hardware and software platform

**The problem:** Direct dependencies on OS interfaces, APIs, or platform-specific features make software hard to port and hard to keep current even on its native platform.

**Symptom:** `#ifdef WIN32` / platform-specific API calls in core logic. Cannot run on a new OS or swap a database without touching business code.

**Design patterns:**
- **Abstract Factory** — isolates platform-specific object creation behind an interface
- **Bridge** — separates the abstraction (what the system does) from its platform-specific implementation (how it does it)

---

### 4. Dependence on object representations or implementations

**The problem:** Clients that know how an object is represented (stored, located, or implemented) must change whenever that object changes — changes cascade unnecessarily.

**Symptom:** Client code accesses internal fields directly, or knows whether an object is local vs. remote, or knows whether it is cached.

**Design patterns:**
- **Abstract Factory** — hides how product families are created and structured
- **Bridge** — hides implementation behind a stable abstraction interface
- **Memento** — externalizes and restores state without exposing internal representation
- **Proxy** — controls access to an object and hides its location or construction

---

### 5. Algorithmic dependencies

**The problem:** Algorithms are frequently extended, optimized, or replaced during development and reuse. Objects that depend on a specific algorithm must change when the algorithm changes.

**Symptom:** A sorting routine, a layout engine, or a compression algorithm embedded directly in a class. Cannot swap algorithms or test alternatives without modifying the class.

**Design patterns:**
- **Builder** — isolates the algorithm for building a complex object from the object's representation
- **Iterator** — abstracts the traversal algorithm over an aggregate, decoupling it from the aggregate's structure
- **Strategy** — defines a family of interchangeable algorithms; clients switch algorithms without touching the code that uses them
- **Template Method** — defines the skeleton of an algorithm in a base class, letting subclasses override specific steps
- **Visitor** — adds operations to an object structure without modifying the classes in that structure

---

### 6. Tight coupling

**The problem:** Tightly coupled classes depend heavily on each other — they cannot be reused in isolation, cannot be changed without understanding many other classes, and the system becomes a dense mass that is hard to learn, port, and maintain.

**Symptom:** Fan-out: a class directly references many other concrete classes. Cannot unit-test a class without instantiating half the system.

**Design patterns:**
- **Abstract Factory** — clients depend on factory interface, not concrete products
- **Bridge** — separates abstraction from implementation so neither depends directly on the other
- **Chain of Responsibility** — decouples sender from all potential receivers
- **Command** — decouples the object that invokes the operation from the one that knows how to perform it
- **Facade** — provides a simple interface to a complex subsystem, reducing coupling between clients and the subsystem's internals
- **Mediator** — replaces a web of object-to-object references with a single mediator object; objects only know the mediator
- **Observer** — decouples subjects from observers; subjects do not know observer types

---

### 7. Extending functionality by subclassing

**The problem:** Customizing behavior through inheritance requires an in-depth understanding of the parent class, carries fixed initialization overhead, and can cause a subclass explosion — many subclasses for even a simple extension.

**Symptom:** A class hierarchy that grows by one new leaf class for every combination of features. Overriding one method requires understanding ten others. Cannot add behavior at run-time.

**Design patterns:**
- **Bridge** — lets abstraction and implementation vary independently without deep hierarchies
- **Chain of Responsibility** — adds new handlers without modifying existing ones
- **Composite** — lets clients add new components to a tree structure uniformly
- **Decorator** — attaches responsibilities to objects dynamically, avoiding the combinatorial subclass explosion
- **Observer** — lets you add new observers without modifying subjects
- **Strategy** — defines behavior as a composable object rather than a subclass

---

### 8. Inability to alter classes conveniently

**The problem:** Sometimes you must modify a class you cannot change — no source code, a commercial library, too many existing subclasses that would all need updating.

**Symptom:** A third-party class with the wrong interface, or a core class that is too widely subclassed to change safely.

**Design patterns:**
- **Adapter** — converts an incompatible interface into one clients expect, without touching the original class
- **Decorator** — adds responsibilities to objects without subclassing; works even with sealed or third-party classes
- **Visitor** — adds new operations to an existing class structure without modifying those classes

---

## Quick Diagnostic: Which Cause Matches Your Pain?

| Symptom You're Experiencing | Most Likely Cause |
|-----------------------------|------------------|
| `new ConcreteClass()` everywhere, hard to swap | Cause 1 |
| Request dispatch logic tangled in client code | Cause 2 |
| Platform-specific code mixed into business logic | Cause 3 |
| Client knows too much about another object's internals | Cause 4 |
| Cannot swap or test algorithms independently | Cause 5 |
| Cannot unit-test a class without the whole system | Cause 6 |
| Subclass hierarchy exploding with combinations | Cause 7 |
| Can't modify the class (no source, too many dependents) | Cause 8 |
