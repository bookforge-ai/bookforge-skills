# GoF Pattern Catalog — Purpose × Scope Matrix (Table 1.1)

Source: Design Patterns: Elements of Reusable Object-Oriented Software (GoF, 1994), Table 1.1 and catalog intents pp. 20–21.

## Classification Axes

**Purpose** — What the pattern does:
- **Creational** — concerns the process of object creation
- **Structural** — deals with the composition of classes or objects
- **Behavioral** — characterizes the ways classes or objects interact and distribute responsibility

**Scope** — What the pattern applies to:
- **Class** — relationships between classes and subclasses (fixed at compile-time, via inheritance)
- **Object** — relationships between objects (dynamic at run-time, via composition/delegation)

---

## Table 1.1: Design Pattern Space

| Scope | Creational | Structural | Behavioral |
|-------|-----------|------------|------------|
| **Class** | Factory Method | — | Interpreter, Template Method |
| **Object** | Abstract Factory, Builder, Prototype, Singleton | Adapter, Bridge, Composite, Decorator, Facade, Flyweight, Proxy | Chain of Responsibility, Command, Iterator, Mediator, Memento, Observer, State, Strategy, Visitor |

---

## Full Catalog: All 23 Patterns with One-Line Intent

### Creational Patterns

| Pattern | Scope | Intent |
|---------|-------|--------|
| **Abstract Factory** | Object | Provide an interface for creating families of related or dependent objects without specifying their concrete classes. |
| **Builder** | Object | Separate the construction of a complex object from its representation so that the same construction process can create different representations. |
| **Factory Method** | Class | Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses. |
| **Prototype** | Object | Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype. |
| **Singleton** | Object | Ensure a class only has one instance, and provide a global point of access to it. |

### Structural Patterns

| Pattern | Scope | Intent |
|---------|-------|--------|
| **Adapter** | Object | Convert the interface of a class into another interface clients expect. Adapter lets classes work together that couldn't otherwise because of incompatible interfaces. |
| **Bridge** | Object | Decouple an abstraction from its implementation so that the two can vary independently. |
| **Composite** | Object | Compose objects into tree structures to represent part-whole hierarchies. Composite lets clients treat individual objects and compositions of objects uniformly. |
| **Decorator** | Object | Attach additional responsibilities to an object dynamically. Decorators provide a flexible alternative to subclassing for extending functionality. |
| **Facade** | Object | Provide a unified interface to a set of interfaces in a subsystem. Facade defines a higher-level interface that makes the subsystem easier to use. |
| **Flyweight** | Object | Use sharing to support large numbers of fine-grained objects efficiently. |
| **Proxy** | Object | Provide a surrogate or placeholder for another object to control access to it. |

### Behavioral Patterns

| Pattern | Scope | Intent |
|---------|-------|--------|
| **Chain of Responsibility** | Object | Avoid coupling the sender of a request to its receiver by giving more than one object a chance to handle the request. Chain the receiving objects and pass the request along the chain until an object handles it. |
| **Command** | Object | Encapsulate a request as an object, thereby letting you parameterize clients with different requests, queue or log requests, and support undoable operations. |
| **Interpreter** | Class | Given a language, define a representation for its grammar along with an interpreter that uses the representation to interpret sentences in the language. |
| **Iterator** | Object | Provide a way to access the elements of an aggregate object sequentially without exposing its underlying representation. |
| **Mediator** | Object | Define an object that encapsulates how a set of objects interact. Mediator promotes loose coupling by keeping objects from referring to each other explicitly, and it lets you vary their interaction independently. |
| **Memento** | Object | Without violating encapsulation, capture and externalize an object's internal state so that the object can be restored to this state later. |
| **Observer** | Object | Define a one-to-many dependency between objects so that when one object changes state, all its dependents are notified and updated automatically. |
| **State** | Object | Allow an object to alter its behavior when its internal state changes. The object will appear to change its class. |
| **Strategy** | Object | Define a family of algorithms, encapsulate each one, and make them interchangeable. Strategy lets the algorithm vary independently from clients that use it. |
| **Template Method** | Class | Define the skeleton of an algorithm in an operation, deferring some steps to subclasses. Template Method lets subclasses redefine certain steps of an algorithm without changing the algorithm's structure. |
| **Visitor** | Object | Represent an operation to be performed on the elements of an object structure. Visitor lets you define a new operation without changing the classes of the elements on which it operates. |

---

## Quick-Reference: Pattern Relationships (Figure 1.1 summary)

Key relationships between patterns that often appear together:

- **Composite** is often used with **Iterator** or **Visitor**
- **Prototype** is an alternative to **Abstract Factory**
- **Abstract Factory** is often implemented using **Factory Method**
- **Abstract Factory**, **Builder**, and **Prototype** can use **Singleton**
- **Decorator** and **Proxy** have similar structures but different intents
- **Chain of Responsibility**, **Command**, **Mediator**, and **Observer** all address how senders and receivers are coupled
- **Strategy** and **State** both delegate behavior to helper objects; State's helper knows about the context, Strategy's typically does not
- **Template Method** uses inheritance; **Strategy** uses delegation — both vary algorithm parts
- **Facade** often uses **Singleton** for the facade object
- **Flyweight** often uses **Composite** for hierarchical structure
