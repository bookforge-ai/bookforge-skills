# Structural Pattern Disambiguation Reference

> Source: Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Chapter 4 — Structural Patterns, pages 133–207.
> This file contains detailed applicability conditions, disambiguation criteria, and cross-pattern relationships for the seven structural GoF patterns. Load this file when the SKILL.md decision tree produces ambiguity or when you need to explain a recommendation in depth.

---

## Overview: The Seven Structural Patterns

Structural patterns are concerned with how classes and objects are composed to form larger structures.

- **Class patterns** use inheritance to compose interfaces or implementations (Adapter class variant)
- **Object patterns** use composition to realize new functionality, gaining the ability to change composition at runtime

| Pattern | Core structural problem | Mechanism |
|---------|------------------------|-----------|
| Adapter | Interface incompatibility between existing classes | Wraps one object to present another interface |
| Bridge | Abstraction and implementation tightly bound | Separates into two independent hierarchies |
| Composite | Part-whole hierarchies need uniform treatment | Recursive tree of Component objects |
| Decorator | Adding responsibilities without subclassing | Wraps a Component and adds before/after behavior |
| Facade | Complex subsystem needs a simple unified entry point | Single object that delegates to subsystem classes |
| Flyweight | Large numbers of fine-grained objects are expensive | Shared objects with extrinsic state passed in |
| Proxy | Need a stand-in, gateway, or access-control layer | One-to-one wrapper that controls access to Subject |

---

## Adapter

### Intent
Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces.

Also known as: **Wrapper**

### Applicability
Use Adapter when:
- You want to use an existing class, and its interface does not match the one you need
- You want to create a reusable class that cooperates with unrelated or unforeseen classes that don't have compatible interfaces
- *(Object adapter only)* You need to use several existing subclasses, but it's impractical to adapt their interface by subclassing each one — an object adapter can adapt the interface of its parent class

### Class Adapter vs Object Adapter

| | Class Adapter | Object Adapter |
|--|--------------|---------------|
| Mechanism | Multiple inheritance | Composition (holds Adaptee reference) |
| Adapts | A single Adaptee class | Any Adaptee subclass |
| Can override Adaptee behavior | Yes | No (must subclass Adaptee) |
| Language support | C++ (multiple inheritance), not Java/C# | Universal |
| When to prefer | When you need to override specific Adaptee behavior | When you need to work with Adaptee subclasses |

### Disambiguation: Adapter vs Facade

Both Adapter and Facade wrap other objects and present a different interface. The distinction:

- **Adapter** reuses an *existing* target interface — there is already a contract (e.g., `IPaymentProcessor`) that other code depends on, and you need to make a new class satisfy it
- **Facade** defines a *new* interface — there is no pre-existing contract; you are creating a convenient entry point for a subsystem that previously had no unified access point

> From the GoF (p.206): "You might think of a facade as an adapter to a set of other objects. But that interpretation overlooks the fact that a facade defines a *new* interface, whereas an adapter reuses an old interface. Remember that an adapter makes two *existing* interfaces work together as opposed to defining an entirely new one."

### Disambiguation: Adapter vs Bridge (THE KEY DISTINCTION)

> From the GoF (p.206): "The Adapter pattern makes things work *after* they're designed; Bridge makes them work *before*."

| Axis | Adapter | Bridge |
|------|---------|--------|
| **When applied** | Post-design — classes exist independently and must be integrated | Pre-design — structure is intentionally separated before classes are built |
| **Origin of incompatibility** | Unforeseen — coupling was not anticipated | Intentional — separation is a deliberate architectural decision |
| **Goal** | Make two independently designed classes work together without reimplementing either | Keep abstraction and implementation hierarchies separately extensible |
| **Relationship to change** | Resolves a fixed incompatibility | Accommodates ongoing independent variation |

Both patterns provide a level of indirection by forwarding requests. The difference is entirely in intent and timing.

---

## Bridge

### Intent
Decouple an abstraction from its implementation so that the two can vary independently.

### Applicability
Use Bridge when:
- You want to avoid a permanent binding between an abstraction and its implementation — for example, when the implementation must be selected or switched at runtime
- Both the abstractions and their implementations should be extensible by subclassing, and the different combinations should be composable independently
- Changes in the implementation of an abstraction should have no impact on clients — their code should not have to be recompiled
- *(C++ context)* You want to hide the implementation of an abstraction completely from clients
- You have a proliferation of classes ("nested generalizations") — a class hierarchy with subclasses for each combination of abstraction variant and implementation variant. Bridge breaks this into two independent hierarchies
- You want to share an implementation among multiple objects and this fact should be hidden from the client

### The "Nested Generalization" Smell That Bridge Solves

If you see a class hierarchy like:
```
Shape
├── RedCircle
├── BlueCircle
├── RedSquare
└── BlueSquare
```

And it is growing as both shapes and colors are added, Bridge is likely the solution. Separate the two dimensions:
```
Shape (abstraction)          Color (implementation)
├── Circle                   ├── Red
└── Square                   └── Blue
```

Circle and Square hold a reference to a Color implementation. 2 shapes + 2 colors = 4 classes, not 4 subclasses (and it scales linearly, not combinatorially).

### Participants

- **Abstraction** — defines the abstraction's interface; maintains a reference to an Implementor
- **RefinedAbstraction** — extends the Abstraction interface
- **Implementor** — defines the interface for implementation classes (does not need to match Abstraction's interface; typically provides primitive operations that Abstraction uses to define higher-level operations)
- **ConcreteImplementor** — implements the Implementor interface

---

## Composite

### Intent
Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly.

### Applicability
Use Composite when:
- You want to represent part-whole hierarchies of objects
- You want clients to be able to ignore the difference between compositions of objects and individual objects — clients will treat all objects in the composite structure uniformly

### Participants

- **Component** — declares the interface for objects in the composition; implements default behavior for the interface common to all classes
- **Leaf** — represents leaf objects in the composition; a Leaf has no children
- **Composite** — defines behavior for components having children; stores child components; implements child-related operations
- **Client** — manipulates objects in the composition through the Component interface

### Key Consequence: The Uniformity Principle

The power of Composite is that clients never need to ask "is this a leaf or a composite?" — they call the same interface either way. The Composite propagates operations through its children automatically (`for g in children: g.Operation()`).

### Disambiguation: Composite vs Decorator vs Proxy

See dedicated section below.

---

## Decorator

### Intent
Attach additional responsibilities to an object dynamically. Decorator provides a flexible alternative to subclassing for extending functionality.

Also known as: **Wrapper**

### Applicability
Use Decorator:
- To add responsibilities to individual objects dynamically and transparently, without affecting other objects
- For responsibilities that can be withdrawn
- When extension by subclassing is impractical — sometimes a large number of independent extensions are possible, producing an explosion of subclasses to support every combination; or a class definition may be hidden or otherwise unavailable for subclassing

### Why Decorator Instead of Subclassing

Subclassing adds behavior statically — all instances of the subclass have the additional behavior, and it cannot be removed. Decorator adds behavior at object level, dynamically. Three separate responsibilities (logging, rate limiting, auth) would require 7 subclasses to cover all combinations ($2^3 - 1$). With Decorator, you wrap the object with whichever decorators you need.

### The Recursive Composition Structure

A Decorator conforms to the interface of the Component it decorates. This means decorators can be nested:

```
AuthDecorator(LoggingDecorator(RateLimitDecorator(realService)))
```

Each layer adds its behavior before/after calling the next layer's method. The real object is at the center. The nesting depth is open-ended — this is the essential feature that distinguishes Decorator from Proxy.

### Important Consequence: Identity Breaks

A Decorator and its Component are not the same object. Code that uses object identity (`decorator == component`) will behave unexpectedly. This is a documented trade-off: Decorator sacrifices identity in exchange for compositional flexibility.

---

## Facade

### Intent
Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use.

### Applicability
Use Facade when:
- You want to provide a simple interface to a complex subsystem. Subsystems often get more complex as they evolve. Most patterns, when applied, result in more and smaller classes. This makes the subsystem more reusable and easier to customize, but also harder to use for clients that don't need to customize it. A facade can provide a simple default view of the subsystem that is good enough for most clients.
- There are many dependencies between clients and the implementation classes of an abstraction. Introduce a facade to decouple the subsystem from clients and other subsystems, thereby promoting subsystem independence and portability.
- You want to layer your subsystems. Use a facade to define an entry point to each subsystem level. If subsystems are dependent, you can simplify the dependencies between them by making them communicate with each other solely through their facades.

### Facade Does Not Encapsulate the Subsystem

Unlike other structural patterns that fully hide the wrapped object, Facade does not prevent clients from using subsystem classes directly if they need to. Facade only provides a convenient default — clients needing advanced customization can bypass the Facade and work with subsystem classes directly.

### Disambiguation: Facade vs Adapter (Summary)

| | Facade | Adapter |
|--|--------|---------|
| Interface it provides | A new, simpler interface that didn't exist before | An existing interface that another class should satisfy |
| What it wraps | A subsystem (multiple classes) | A single class (or class hierarchy) |
| Goal | Simplify usage | Resolve incompatibility |
| Pre-existing target interface? | No — Facade creates the interface | Yes — Adapter maps to an existing interface |

---

## Flyweight

### Intent
Use sharing to support large numbers of fine-grained objects efficiently.

### The AND-Gate: All Five Conditions Must Hold

The Flyweight pattern's effectiveness depends heavily on how and where it's used. Apply Flyweight only when **all** of the following are true:

1. **Large number of objects** — the application creates and manages thousands or more instances
2. **High storage cost** — memory consumption from this quantity of objects is measurably significant
3. **Most state is extrinsic** — the majority of each object's state can be computed or passed in from outside, rather than stored per-instance
4. **Many objects can be replaced by few shared objects** — once extrinsic state is separated out, many "different" objects turn out to be identical in their intrinsic state
5. **No object identity dependency** — the application does not use identity tests (`==`, reference equality) to distinguish objects that represent conceptually different entities

**Condition 5 is the most commonly missed.** Flyweight objects are shared — multiple logical "instances" map to the same physical object. If any code does:

```python
character_a1 = flyweight_factory.get('a')
character_a2 = flyweight_factory.get('a')
assert character_a1 is not character_a2  # FAILS — they're the same object
```

or relies on object identity for tracking, ordering, or comparison, Flyweight will produce silent correctness bugs that are difficult to diagnose.

### Intrinsic vs Extrinsic State

| | Intrinsic state | Extrinsic state |
|--|----------------|----------------|
| Stored in | The flyweight object itself | Passed to flyweight methods by the client |
| Shared? | Yes — all clients sharing this flyweight use the same intrinsic state | No — different for each context |
| Example (character glyph) | Character code ('a', 'b', etc.) | Position, font, color in the document |

Separating intrinsic from extrinsic state is the central design task when implementing Flyweight.

---

## Proxy

### Intent
Provide a surrogate or placeholder for another object to control access to it.

### Four Types of Proxy

1. **Remote proxy** — provides a local representative for an object in a different address space. The proxy handles network communication transparently; clients see a local interface.

2. **Virtual proxy** — creates expensive objects on demand. The proxy stands in until the real object is actually needed, then creates and delegates to it (lazy initialization). Example: ImageProxy that shows a placeholder until the image is loaded.

3. **Protection proxy** — controls access to the original object based on access rights. Useful when objects should have different access rights.

4. **Smart reference** — replacement for a bare pointer that performs additional actions when an object is accessed: reference counting, locking, logging, caching.

### Disambiguation: Proxy vs Decorator

This is the most subtle distinction among structural patterns.

> From the GoF (p.207): "Like Decorator, the Proxy pattern composes an object and provides an identical interface to clients. Unlike Decorator, the Proxy pattern is not concerned with attaching or detaching properties dynamically, and it's not designed for recursive composition."

| Axis | Proxy | Decorator |
|------|-------|-----------|
| **Purpose** | Control or mediate access to the Subject | Add responsibilities to the Component |
| **Who defines core behavior** | The Subject — Proxy only provides/refuses access to it | Both Component and Decorators — Decorator adds to what Component provides |
| **Recursive composition** | Not designed for it — relationship is static one-to-one | Essential to the pattern — decorators stack |
| **Known at compile time** | Often — the proxy-subject relationship is frequently fixed | Typically no — decoration applied at runtime |
| **Can be stacked** | Not the intent — multiple proxies can exist but each is independent | Yes — stacking is the primary value proposition |

**Decision rule:** If you need one wrapper that gates, defers, or monitors access to one object → Proxy. If you need to stack multiple wrappers that each add a piece of behavior → Decorator.

### Proxy vs Adapter

Both Proxy and Adapter wrap an object. The difference:
- **Proxy** implements the *same interface* as its Subject — it is a transparent stand-in
- **Adapter** implements a *different interface* than its Adaptee — it is an interface translator

---

## Cross-Pattern Relationships Summary

| Pattern pair | Relationship | When both are used together |
|-------------|-------------|----------------------------|
| Composite + Decorator | Complementary | Build a tree of objects (Composite), then add behaviors to individual nodes (Decorator) without modifying the tree structure |
| Composite + Iterator | Complementary | Define a Composite tree structure, use Iterator to traverse it |
| Decorator + Strategy | Alternatives for behavioral extension | Decorator changes an object's *skin* (wraps it); Strategy changes an object's *guts* (replaces its algorithm). Use Decorator when the behavior wraps/extends the component's own behavior; use Strategy when the component's behavior needs to be replaced entirely |
| Facade + Singleton | Often combined | A Facade is often implemented as a Singleton — one unified entry point per subsystem |
| Proxy + Decorator | Can be combined (carefully) | A proxy-decorator adds functionality to a proxy, or a decorator-proxy embellishes a remote object. The GoF notes this is possible but recommends treating them separately unless needed |
| Adapter + Factory Method | Common combination | Use Factory Method to instantiate the right Adapter based on runtime configuration |
| Bridge + Abstract Factory | Common combination | Use Abstract Factory to create the ConcreteImplementor for a Bridge |

---

## Quick Disambiguation Card

```
STRUCTURAL PROBLEM
       │
       ├─ Incompatible interface?
       │         ├─ Classes already designed, incompatibility unforeseen? → ADAPTER
       │         └─ Designing now, need long-term independent variation? → BRIDGE
       │
       ├─ Need part-whole tree (nodes and leaves behave the same)? → COMPOSITE
       │
       ├─ Need to add/remove behaviors dynamically without subclassing?
       │         ├─ Need to STACK multiple behaviors? → DECORATOR
       │         └─ Need ONE gateway (access control, lazy init, remote)? → PROXY
       │
       ├─ Complex subsystem needs a simple unified entry point? → FACADE
       │         └─ (Note: Facade creates NEW interface; Adapter reuses EXISTING interface)
       │
       └─ Thousands of fine-grained objects, memory is the problem,
          ALL 5 conditions hold (including no identity dependency)? → FLYWEIGHT
```
