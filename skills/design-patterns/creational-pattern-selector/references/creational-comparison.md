# Creational Pattern Comparison Reference

> Source: Design Patterns: Elements of Reusable Object-Oriented Software (Gamma, Helm, Johnson, Vlissides), Chapter 3 — Creational Patterns + Discussion of Creational Patterns (pp. 83–132)

This file provides the detailed per-pattern applicability, consequences, and trade-off data used by the `creational-pattern-selector` skill.

---

## Overview: The Two Parameterization Strategies

Creational patterns all solve the same root problem: **hard-coding the concrete class names of objects that a system creates makes it inflexible**. When the class to instantiate is named explicitly (e.g., `new Room()`), changing it requires editing the code that does the creation — often a cascading change.

The GoF identifies two fundamental approaches to removing these concrete class references:

### Strategy 1: Subclass-Based (Class Parameterization)

Subclass the creator class and override a virtual factory method. The creator calls the virtual method to create products; subclasses decide the concrete type.

- **Only pattern:** Factory Method
- **Mechanism:** Inheritance. The type of product changes by changing the subclass of the creator.
- **Main drawback:** Creating a new product subclass often requires creating a new creator subclass. Subclass changes can cascade — if the creator is itself created by a factory method, you must also override its creator.
- **Best when:** The customization is simple (one virtual method), the variation is known at compile-time, and subclass proliferation is not a concern.

### Strategy 2: Composition-Based (Object Parameterization)

Define a separate "factory object" responsible for knowing which concrete classes to create. Pass this object into the creator as a parameter. The creator delegates instantiation entirely to the factory object.

- **Patterns:** Abstract Factory, Builder, Prototype
- **Mechanism:** Object composition. The type of product changes by passing a different factory/builder/prototype object — no subclassing of the creator needed.
- **Main advantage:** The creator is fully decoupled from concrete product classes. Run-time flexibility is inherent.
- **Best when:** Products must vary at run-time, multiple product families must be managed, or subclassing the creator is undesirable.

**Singleton** is orthogonal to both strategies: it governs instance count, not instantiation mechanism. It is commonly combined with Abstract Factory (to ensure one factory per application).

---

## Pattern 1: Factory Method

**Intent:** Define an interface for creating an object, but let subclasses decide which class to instantiate. Factory Method lets a class defer instantiation to subclasses.

**Also known as:** Virtual Constructor

### Applicability

Use Factory Method when:

1. A class cannot anticipate the class of objects it must create — it knows *when* to create but not *what* to create
2. A class wants its subclasses to specify the objects it creates
3. Classes delegate responsibility to one of several helper subclasses, and you want to localize the knowledge of which helper subclass is the delegate

### Consequences

**Benefits:**
- Eliminates the need to bind application-specific classes into your code — code deals only with the Product interface
- Provides hooks for subclasses: creating objects in a separate factory method is always more flexible than creating them directly
- Connects parallel class hierarchies: factory methods are often called by a Creator that also has a parallel Product hierarchy (e.g., Figure and Manipulator)

**Liabilities:**
- Clients may need to subclass the Creator class just to create a particular ConcreteProduct — adds a point of evolution
- Two major varieties:
  1. Abstract Creator — no default implementation, forces subclasses to define it
  2. Concrete Creator with default — provides flexibility without requiring subclasses

### Key Trade-offs

| | |
|--|--|
| **Flexibility** | Compile-time (via subclassing). Run-time flexibility requires additional mechanism. |
| **New variant cost** | One new Creator subclass + one new Product subclass |
| **Creator coupling** | Creator is decoupled from ConcreteProduct but coupled to its own class hierarchy |
| **Complexity introduced** | Low — only a new virtual method and override |

---

## Pattern 2: Abstract Factory

**Intent:** Provide an interface for creating families of related or dependent objects without specifying their concrete classes.

**Also known as:** Kit

### Applicability

Use Abstract Factory when:

1. A system should be independent of how its products are created, composed, and represented
2. A system should be configured with one of multiple families of products
3. A family of related product objects is designed to be used together, and you need to enforce this constraint
4. You want to provide a class library of products, and you want to reveal just their interfaces, not their implementations

### Consequences

**Benefits:**
1. **Isolates concrete classes** — clients manipulate instances through abstract interfaces; product class names never appear in client code
2. **Makes exchanging product families easy** — the entire family changes when the ConcreteFactory changes, since only one ConcreteFactory is used per application
3. **Promotes consistency among products** — products from one family are always used together; the factory enforces this automatically

**Liabilities:**
4. **Supporting new kinds of products is difficult** — adding a new product type (e.g., a new widget) requires changing the AbstractFactory interface and *all* ConcreteFactory subclasses

### Implementation Notes

- Typically implemented as a Singleton — only one ConcreteFactory per application run
- Factories can be parameterized (accept a product type identifier) to avoid the interface-change problem, at the cost of type safety
- Prototype-based factories can be used to avoid the parallel ConcreteFactory hierarchy: register prototypical product instances in a single factory

### Key Trade-offs

| | |
|--|--|
| **Flexibility** | Run-time — swap the factory object to swap the entire product family |
| **New family cost** | One new ConcreteFactory class implementing all creation methods |
| **New product type cost** | High — requires changing AbstractFactory interface and all ConcreteFactories |
| **Complexity introduced** | Medium-high — factory object hierarchy parallel to product hierarchy |

---

## Pattern 3: Builder

**Intent:** Separate the construction of a complex object from its representation so that the same construction process can create different representations.

### Applicability

Use Builder when:

1. The algorithm for creating a complex object should be independent of the parts that make up the object and how they're assembled
2. The construction process must allow different representations for the object that's constructed

### Structure

- **Director:** Constructs the object using the Builder interface. Calls BuildPart() methods in sequence. Owns the construction algorithm.
- **Builder:** Abstract interface for creating parts of the Product object
- **ConcreteBuilder:** Implements the Builder interface; constructs and assembles parts; provides a GetResult() interface
- **Product:** The complex object under construction. ConcreteBuilder builds its internal representation.

Collaboration: Client creates a Director and configures it with a ConcreteBuilder. Director calls BuildPart() methods. Client retrieves the product from the ConcreteBuilder.

### Consequences

1. **Vary product's internal representation** — to change representation, define a new ConcreteBuilder; the Director is unchanged
2. **Isolate construction from representation** — modularity: the Builder encapsulates all code for creating and assembling the product; the Director knows nothing about the product's structure
3. **Finer control over the construction process** — unlike creational patterns that construct products in one shot, Builder builds step by step under the Director's control

### Key Trade-offs

| | |
|--|--|
| **Flexibility** | Run-time — configure Director with different ConcreteBuilders |
| **New representation cost** | One new ConcreteBuilder class |
| **When not to use** | When product construction is simple (single method call) — adds unnecessary structure |
| **Distinguishing from Abstract Factory** | Builder constructs complex objects step-by-step; Abstract Factory creates families of objects in one step. Builder returns the product at the end; Abstract Factory returns it immediately. |
| **Complexity introduced** | Medium — Director + Builder interface + ConcreteBuilder(s) + Product |

---

## Pattern 4: Prototype

**Intent:** Specify the kinds of objects to create using a prototypical instance, and create new objects by copying this prototype.

### Applicability

Use Prototype when a system should be independent of how its products are created, composed, and represented, **and** when at least one of the following holds:

1. The classes to instantiate are specified at run-time (e.g., dynamic loading)
2. To avoid building a class hierarchy of factories that parallels the class hierarchy of products
3. Instances of a class can have only a few different combinations of state — it's more convenient to install prototypes and clone them than to instantiate the class manually with the appropriate state each time

### Consequences

**Shared benefits with Abstract Factory and Builder:**
- Hides the concrete product classes from the client
- Lets a client work with application-specific classes without modification

**Prototype-specific benefits:**

1. **Add and remove products at run-time** — register/unregister prototypes dynamically; more flexible than other patterns for run-time variation
2. **Specify new objects by varying values** — define new kinds of objects by varying an existing object's state, without defining new classes
3. **Specify new objects by varying structure** — prototype complex composite structures (e.g., circuit diagrams) so they can be cloned and reused
4. **Reduce subclassing** — Factory Method produces a parallel Creator hierarchy for each Product; Prototype eliminates the need for Creator subclasses entirely
5. **Configure application with classes dynamically** — dynamically loaded classes can register prototype instances; application can request them from the prototype manager without knowing the class name

**Liabilities:**
- Each subclass of Prototype must implement a `Clone` operation — can be difficult for existing classes, and for classes with circular references or objects that do not support copying

### Key Trade-offs

| | |
|--|--|
| **Flexibility** | Run-time — swap prototype instances; can add/remove at run-time |
| **New variant cost** | Register a new prototype instance — no new class required |
| **Main constraint** | All product types must implement Clone (deep copy) |
| **Reduces subclassing** | Eliminates parallel Creator hierarchy needed by Factory Method |
| **Complexity introduced** | Low–medium — prototype registry + Clone implementation on all products |

---

## Pattern 5: Singleton

**Intent:** Ensure a class only has one instance, and provide a global point of access to it.

### Applicability

Use Singleton when:

1. There must be exactly one instance of a class, and it must be accessible to clients from a well-known access point
2. The sole instance should be extensible by subclassing, and clients should be able to use an extended instance without modifying their code

### Consequences

1. **Controlled access to sole instance** — the Singleton class encapsulates the instance; it can have strict control over how and when clients access it
2. **Reduced name space** — improvement over global variables: avoids polluting the name space with global variables for sole instances
3. **Permits refinement of operations and representation** — the Singleton class may be subclassed; the application can be configured with an instance of an extended class
4. **Permits a variable number of instances** — the same mechanism can control any fixed number of instances, not just one
5. **More flexible than class operations** — class-level (static) methods cannot be virtual and cannot be overridden polymorphically; Singleton avoids this

### Key Trade-offs

| | |
|--|--|
| **Solves** | Instance count control + global access without global variable |
| **Common combination** | Abstract Factory as a Singleton — one factory object per application |
| **Common combination** | Singleton Facade — one subsystem access point per application |
| **Caution** | Overuse of Singleton creates hidden global state; makes unit testing harder |
| **Complexity introduced** | Low — one static accessor method + lazy initialization |

---

## Side-by-Side Comparison

| Dimension | Abstract Factory | Builder | Factory Method | Prototype | Singleton |
|-----------|-----------------|---------|----------------|-----------|-----------|
| **Problem solved** | Family of related products | Complex object step-by-step | Single product; defer type to subclass | Clone configured instances | Single instance globally accessible |
| **Parameterization** | Composition | Composition | Subclassing | Composition | N/A |
| **Run-time flexibility** | High — swap factory | High — swap builder | Low — compile-time | High — swap prototype | N/A (fixed instance) |
| **Product family support** | Yes (core strength) | No | No | No | No |
| **Construction control** | Single-step | Step-by-step | Single-step | Copy | N/A |
| **New variant cost** | New ConcreteFactory | New ConcreteBuilder | New Creator + Product subclass | Register new prototype | N/A |
| **New product type cost** | High (change all factories) | Low (add builder method) | Low | Low (add Clone) | N/A |
| **Subclass requirement** | Factory subclasses | Builder subclasses | Creator subclasses | Product Clone impl | Optional |
| **Complexity** | Medium-high | Medium | Low | Low-medium | Low |

---

## Maze Game: All Five Patterns Applied

The GoF use `MazeGame::CreateMaze()` as the canonical comparison example. The baseline code hard-codes `new Maze`, `new Room(1)`, `new Room(2)`, `new Door(r1, r2)`. The goal: support enchanted maze variants with `EnchantedRoom` and `DoorNeedingSpell`.

### Baseline (inflexible)
```cpp
Maze* MazeGame::CreateMaze() {
    Maze* aMaze = new Maze;
    Room* r1 = new Room(1);
    Room* r2 = new Room(2);
    Door* theDoor = new Door(r1, r2);
    // ... connect rooms
    return aMaze;
}
```
Problem: The maze layout logic is sound, but any change to the component types requires editing or rewriting this entire method.

### Factory Method Solution
Add virtual creation methods to MazeGame. Subclasses override them.
```cpp
// MazeGame adds:
virtual Room* MakeRoom(int n) { return new Room(n); }
virtual Door* MakeDoor(Room* r1, Room* r2) { return new Door(r1, r2); }

// CreateMaze calls:
Room* r1 = MakeRoom(1);
Door* theDoor = MakeDoor(r1, r2);

// EnchantedMazeGame overrides:
Room* MakeRoom(int n) override { return new EnchantedRoom(n, CastSpell()); }
Door* MakeDoor(Room* r1, Room* r2) override { return new DoorNeedingSpell(r1, r2); }
```
**Trade-off:** Every maze variant = one new MazeGame subclass. Clean for compile-time variants; awkward for run-time selection.

### Abstract Factory Solution
Pass a factory object into CreateMaze. The factory creates all components.
```cpp
Maze* MazeGame::CreateMaze(MazeFactory& factory) {
    Maze* aMaze = factory.MakeMaze();
    Room* r1 = factory.MakeRoom(1);
    Room* r2 = factory.MakeRoom(2);
    Door* theDoor = factory.MakeDoor(r1, r2);
    // ...
    return aMaze;
}
// Call with: game.CreateMaze(EnchantedMazeFactory());
```
**Trade-off:** CreateMaze is fully decoupled from concrete classes. Adding a new component type requires adding to the MazeFactory interface and all concrete factories.

### Builder Solution
Pass a MazeBuilder object that tracks the maze being built. CreateMaze calls the builder incrementally.
```cpp
Maze* MazeGame::CreateMaze(MazeBuilder& builder) {
    builder.BuildMaze();
    builder.BuildRoom(1);
    builder.BuildRoom(2);
    builder.BuildDoor(1, 2);
    return builder.GetMaze();
}
```
**Trade-off:** Builder knows both how to create and how to represent. Multiple builders (StandardMazeBuilder, CountingMazeBuilder) can interpret the same construction calls differently. Best when the construction algorithm is valuable independent of the product type.

### Prototype Solution
Parameterize CreateMaze with prototypical component instances it will clone.
```cpp
Maze* MazeGame::CreateMaze(MazePrototypeFactory& factory) {
    // factory holds prototypical Room*, Door* instances
    Room* r1 = factory.MakeRoom(1); // internally: _protoRoom->Clone()
    Room* r2 = factory.MakeRoom(2);
    Door* theDoor = factory.MakeDoor(r1, r2);
    // ...
}
```
**Trade-off:** No new ConcreteFactory classes needed for each variant. Swap prototype instances to change component types. Requires Clone() on all product classes.

### Singleton Solution
The Maze object itself is managed as a Singleton. Ensures one maze exists per game session; all game objects access it through a well-known access point without passing it as a parameter everywhere.
```cpp
Maze* Maze::_instance = nullptr;
Maze* Maze::Instance() {
    if (_instance == nullptr) _instance = new Maze;
    return _instance;
}
```
**Trade-off:** Orthogonal to the other patterns — controls access to the maze, not how it's built. Often combined with an Abstract Factory Singleton to manage the product family for the whole application run.

---

## GraphicTool: Factory Method vs Abstract Factory vs Prototype

The GoF Discussion section uses the GraphicTool drawing editor as a second comparison. A GraphicTool needs to create Graphic objects (circles, lines, etc.). There are three ways to parameterize it:

| Approach | Structure | Trade-off |
|----------|-----------|-----------|
| **Factory Method** | A GraphicTool subclass for each Graphic subclass. Each subclass redefines a NewGraphic() operation. | Lots of GraphicTool subclasses that differ only in what they instantiate — subclass proliferation. Easy to start with. |
| **Abstract Factory** | A class hierarchy of GraphicsFactories — one for each Graphic subclass (CircleFactory, LineFactory). GraphicTool is parameterized with a factory. | Requires an equally large GraphicsFactory hierarchy. Preferable only if a GraphicsFactory hierarchy already exists for another reason. |
| **Prototype** | Each Graphic subclass implements Clone(). Each GraphicTool instance is parameterized with a prototype it clones when invoked. | Reduces class count significantly — no creator hierarchy needed. Best for this use case. Clone must be implemented on all Graphic types. |

**GoF conclusion:** Prototype is best for the drawing editor because it only requires implementing Clone() on each Graphics class, reduces the number of classes, and Clone() is useful beyond instantiation (e.g., a Duplicate menu operation). Factory Method is easiest to start with, and Abstract Factory is preferable only when a factory hierarchy already exists or is needed elsewhere.

**General evolution guidance (GoF):**
> Designs that use Abstract Factory, Prototype, or Builder are more flexible than those that use Factory Method, but they're also more complex. Often, designs start out using Factory Method and evolve toward the other creational patterns as the designer discovers where more flexibility is needed.
