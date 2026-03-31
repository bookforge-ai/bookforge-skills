# Variability Table — What Each Pattern Lets You Vary (Table 1.2)

Source: Design Patterns: Elements of Reusable Object-Oriented Software (GoF, 1994), Table 1.2, p. 40.

## Purpose

This table answers the question: **"What do I want to be able to change without redesign?"**

Instead of diagnosing what is causing pain (see `redesign-causes.md`), approach pattern selection from the other direction — identify the concept you want to keep variable, and this table points directly to the pattern that encapsulates it.

Key principle from the GoF: *"Encapsulate the concept that varies."* Each pattern isolates a specific aspect of your design so it can vary independently of everything else.

---

## Table 1.2: Design Aspects That Design Patterns Let You Vary

| Purpose | Pattern | Aspect(s) That Can Vary |
|---------|---------|------------------------|
| **Creational** | Abstract Factory | families of product objects |
| | Builder | how a composite object gets created |
| | Factory Method | subclass of object that is instantiated |
| | Prototype | class of object that is instantiated |
| | Singleton | the sole instance of a class |
| **Structural** | Adapter | interface to an object |
| | Bridge | implementation of an object |
| | Composite | structure and composition of an object |
| | Decorator | responsibilities of an object without subclassing |
| | Facade | interface to a subsystem |
| | Flyweight | storage costs of objects |
| | Proxy | how an object is accessed; its location |
| **Behavioral** | Chain of Responsibility | object that can fulfill a request |
| | Command | when and how a request is fulfilled |
| | Interpreter | grammar and interpretation of a language |
| | Iterator | how an aggregate's elements are accessed, traversed |
| | Mediator | how and which objects interact with each other |
| | Memento | what private information is stored outside an object, and when |
| | Observer | number of objects that depend on another object; how dependent objects stay up to date |
| | State | states of an object |
| | Strategy | an algorithm |
| | Template Method | steps of an algorithm |
| | Visitor | operations that can be applied to object(s) without changing their class(es) |

---

## How to Use This Table

**Selection approach:** When you know what aspect of your design must remain flexible, scan the "Aspect(s) That Can Vary" column for a match, then apply the corresponding pattern.

**Examples of working backwards from variability needs:**

| You want to vary... | Start with... |
|--------------------|---------------|
| Which algorithm runs at runtime | Strategy |
| How objects notify each other of changes | Observer |
| The interface presented to clients | Adapter or Facade |
| Which object handles a request | Chain of Responsibility |
| An object's behavior based on its state | State |
| Whether an object is created once or many times | Singleton, Prototype, Factory Method |
| How deep/complex an object graph gets built | Builder, Composite |
| Operations on a stable object structure | Visitor |
| Undo/redo capability | Command, Memento |
