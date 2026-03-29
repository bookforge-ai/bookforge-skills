# Abstract Factory — Implementation Reference Guide

> Source: Design Patterns: Elements of Reusable Object-Oriented Software (GoF), Chapter 3, pages 87-96. Lexi case study: pages 54-58.

---

## Participants

### AbstractFactory (e.g., `GUIFactory`, `MazeFactory`)

Declares an interface for operations that create each abstract product object. One creation method per product type. Returns AbstractProduct types, never concrete types.

### ConcreteFactory (e.g., `MotifFactory`, `PMFactory`, `EnchantedMazeFactory`)

Implements the creation operations to produce concrete product objects. Exactly one ConcreteFactory per product family. ConcreteFactory class names are the *only* place concrete product class names appear — they are hidden from the client entirely.

### AbstractProduct (e.g., `ScrollBar`, `Button`, `Room`, `Wall`)

Declares an interface for a type of product object. One AbstractProduct per product type. The client codes against this interface exclusively.

### ConcreteProduct (e.g., `MotifScrollBar`, `PMButton`, `EnchantedRoom`)

Defines a product object to be created by the corresponding ConcreteFactory. Implements the AbstractProduct interface.

### Client

Uses only interfaces declared by AbstractFactory and AbstractProduct classes. No concrete class names. No `new ConcreteProduct(...)` calls. Receives the factory reference at initialization — typically via constructor injection or a configuration step at startup.

---

## Consequences — Full Analysis

### Benefit 1: It Isolates Concrete Classes

The factory encapsulates the responsibility and process of creating product objects. It isolates clients from implementation classes. Clients manipulate instances through their abstract interfaces. Concrete product class names are isolated inside the ConcreteFactory — they do not appear in client code at all.

**Practical effect:** You can audit isolation with `grep`. If a file imports or references `MotifScrollBar`, `PostgresConnection`, or any concrete product class, the isolation guarantee is broken.

### Benefit 2: It Makes Exchanging Product Families Easy

A ConcreteFactory appears only once in an application — at its instantiation site. Changing the entire product family requires changing this single line. Because a factory creates a complete product family, the whole family changes atomically.

**Practical effect:** In the Lexi example, switching from Motif to Presentation Manager widgets requires changing `new MotifFactory` to `new PMFactory` at startup. All downstream widget creation automatically uses PM products.

### Benefit 3: It Promotes Consistency Among Products

When product objects in a family are designed to work together, it is important that the application use objects from only one family at a time. The AbstractFactory makes this easy to enforce — a client holding a `MotifFactory` reference can only receive Motif products. Cross-family mixing (a Motif scroll bar with a PM button) is structurally prevented.

**Practical effect:** The consistency guarantee holds *only if* clients obtain all products through the factory. If a client directly instantiates even one concrete product, the guarantee is void for that product.

### Liability: Supporting New Kinds of Products Is Difficult

The AbstractFactory interface fixes the set of products that can be created. Adding a new product type (e.g., adding a `Slider` to `GUIFactory`) requires:

1. Changing the AbstractFactory interface
2. Changing every ConcreteFactory subclass
3. Changing every client that uses the factory (if they need the new product)

This cascades across the entire hierarchy. The pattern is appropriate when the product type set is **stable**. If new product types are expected frequently, evaluate the extensible factory approach (see below) or a different pattern.

---

## Implementation Concern 1: Factories as Singletons

An application typically needs only one instance of a ConcreteFactory per product family. Multiple instances would allow different parts of the application to hold different factories and silently produce products from different families — the consistency benefit disappears.

**Standard approach:** Apply the Singleton pattern to each ConcreteFactory. The factory's constructor is controlled and the instance is shared.

```cpp
// C++ Singleton factory
class MotifFactory : public GUIFactory {
public:
    static MotifFactory* Instance() {
        if (!instance_) instance_ = new MotifFactory;
        return instance_;
    }
private:
    MotifFactory() = default;
    static MotifFactory* instance_;
};
```

**Alternative:** If Singleton feels heavy, pass the factory reference via constructor injection and ensure only one instantiation site exists in the application bootstrap. The injection approach is more testable.

---

## Implementation Concern 2: Creating the Products

AbstractFactory only **declares** an interface for creating products. ConcreteFactory subclasses **define** how products are created. Two main approaches:

### Factory Method per Product (Standard)

Each ConcreteFactory overrides a virtual factory method for each product type. Simple, type-safe, and idiomatic in statically typed languages.

```cpp
class MotifFactory : public GUIFactory {
    ScrollBar* CreateScrollBar() override { return new MotifScrollBar; }
    Button*    CreateButton()    override { return new MotifButton; }
};
```

**Drawback:** Requires one ConcreteFactory subclass per product family. When many families exist (or families differ only slightly), the number of subclasses grows linearly with family count.

### Prototype-Based Factory

The concrete factory stores a prototypical instance of each product. The `Make` method retrieves and clones the appropriate prototype. A single factory class serves all product families — differentiated only by which prototypes it is initialized with.

**Smalltalk implementation:**

```smalltalk
"Factory stores prototypes in a dictionary keyed by part name"
make: partName
    ^ (partCatalog at: partName) copy

addPart: partTemplate named: partName
    partCatalog at: partName put: partTemplate

"Adding prototypes to the factory"
aFactory addPart: aPrototype named: #ACMEWidget
```

**Creating an EnchantedMazeFactory without subclassing:**
```smalltalk
createMazeFactory
    ^ (MazeFactory new
        addPart: Wall named: #wall;
        addPart: EnchantedRoom named: #room;
        addPart: DoorNeedingSpell named: #door;
        yourself)
```

Compare to a BombedMazeFactory — identical structure, different prototypes:
```smalltalk
createBombedMazeFactory
    ^ (MazeFactory new
        addPart: BombedWall named: #wall;
        addPart: RoomWithABomb named: #room;
        addPart: Door named: #door;
        yourself)
```

**Class-based variant (Smalltalk/Objective-C):** In languages where classes are first-class objects, `partCatalog` stores classes rather than prototypes. The `make:` method sends `new` to the class instead of `copy` to a prototype:

```smalltalk
make: partName
    ^ (partCatalog at: partName) new
```

This is structurally identical to the prototype approach but leverages the language's class system. It takes advantage of language characteristics and is not portable to C++ or Java without additional machinery.

**When to prefer prototype over factory-method:**
- Many product families exist (avoids N ConcreteFactory subclasses)
- Families differ only in which concrete products they use
- New families need to be created at runtime by composing existing products
- Language treats classes as first-class objects

---

## Implementation Concern 3: Defining Extensible Factories

AbstractFactory normally defines a different operation for each product type. The product types are encoded in the operation signatures. Adding a new product type requires changing the AbstractFactory interface and all classes that depend on it.

**The extensible alternative:** A single parameterized `Make` operation that accepts an identifier for the kind of object to create.

```cpp
// Standard — type-safe but closed
class GUIFactory {
public:
    virtual ScrollBar* CreateScrollBar() = 0;
    virtual Button*    CreateButton()    = 0;
};

// Extensible — flexible but loses static type safety
class GUIFactory {
public:
    virtual AbstractWidget* Make(const string& widgetKind) = 0;
};
```

**Use the parameterized form when:**
- New product types are expected to be added (not just new families)
- You are in a dynamically typed language (Python, Ruby, Smalltalk) — the type-safety cost is zero
- All products can reasonably share a common abstract base class

**Avoid the parameterized form when:**
- Static type checking is important (C++, Java, C#)
- Products are heterogeneous in interface (a ScrollBar and a Menu have nothing in common)
- You want the compiler to catch "I forgot to handle this product type"

**The inherent problem with the parameterized form:** All products are returned via the same abstract return type. The client receives a `AbstractWidget*` or `object` and must know which concrete type to cast or coerce to. If the client performs subclass-specific operations on a product, it needs a downcast, and that downcast can fail. This is the classic **extensibility vs. type safety** trade-off — a highly flexible interface with less static safety.

---

## Lexi GUIFactory Case Study — Full Detail

Lexi is a WYSIWYG document editor that must run on Motif, Presentation Manager (PM), and Macintosh. Its user interface is built from widgets — scroll bars, buttons, menus — that must conform to the platform's look-and-feel standard.

**The problem:** Widget creation calls naming concrete classes (`new MotifScrollBar`) scattered across the application code make it impossible to:
- Switch look-and-feel at runtime
- Port to a new platform without auditing the entire codebase
- Test the UI against different look-and-feel standards

**The solution structure:**

```
GUIFactory (AbstractFactory)
  CreateScrollBar() → ScrollBar
  CreateButton()    → Button
  CreateMenu()      → Menu

MotifFactory : GUIFactory
  CreateScrollBar() → MotifScrollBar
  CreateButton()    → MotifButton
  CreateMenu()      → MotifMenu

PMFactory : GUIFactory
  CreateScrollBar() → PMScrollBar
  CreateButton()    → PMButton
  CreateMenu()      → PMMenu

MacFactory : GUIFactory
  CreateScrollBar() → MacScrollBar
  CreateButton()    → MacButton
  CreateMenu()      → MacMenu
```

Product hierarchies (Figure 2.10 in GoF):
```
ScrollBar (AbstractProduct)
  MotifScrollBar
  PMScrollBar
  MacScrollBar

Button (AbstractProduct)
  MotifButton
  PMButton
  MacButton

Menu (AbstractProduct)
  MotifMenu
  PMMenu
  MacMenu
```

**Factory initialization (pages 57-58):**

```cpp
// Compile-time known look and feel
GUIFactory* guiFactory = new MotifFactory;

// Runtime-selected via environment variable
GUIFactory* guiFactory;
const char* styleName = getenv("LOOK_AND_FEEL");
if (strcmp(styleName, "Motif") == 0) {
    guiFactory = new MotifFactory;
} else if (strcmp(styleName, "Presentation_Manager") == 0) {
    guiFactory = new PMFactory;
} else {
    guiFactory = new DefaultGUIFactory;
}
```

**Key insight from the Lexi case:** `guiFactory` could be a global, a static member of a well-known class, or a local variable if the entire UI is created within one function. The important constraint is: initialize `guiFactory` *before* it is first used to create widgets, and *after* the desired look and feel is known. The pattern does not mandate a specific storage mechanism — it mandates a specific initialization discipline.

---

## MazeFactory Case Study — Full Code

The MazeFactory example from GoF demonstrates Abstract Factory on a smaller, concrete domain.

**AbstractFactory (also serves as default ConcreteFactory via non-abstract base):**
```cpp
class MazeFactory {
public:
    MazeFactory();
    virtual Maze* MakeMaze()  const { return new Maze; }
    virtual Wall* MakeWall()  const { return new Wall; }
    virtual Room* MakeRoom(int n) const { return new Room(n); }
    virtual Door* MakeDoor(Room* r1, Room* r2) const {
        return new Door(r1, r2);
    }
};
```

**Note:** `MazeFactory` is not abstract — it acts as both the AbstractFactory *and* the ConcreteFactory for the default (plain) maze. This is a common simplification for small applications. It means creating a new maze variant requires only overriding the methods that differ — inherited defaults handle the rest.

**Client — factory-mediated creation:**
```cpp
Maze* MazeGame::CreateMaze(MazeFactory& factory) {
    Maze* aMaze = factory.MakeMaze();
    Room* r1    = factory.MakeRoom(1);
    Room* r2    = factory.MakeRoom(2);
    Door* aDoor = factory.MakeDoor(r1, r2);

    aMaze->AddRoom(r1);
    aMaze->AddRoom(r2);

    r1->SetSide(North, factory.MakeWall());
    r1->SetSide(East,  aDoor);
    r1->SetSide(South, factory.MakeWall());
    r1->SetSide(West,  factory.MakeWall());

    r2->SetSide(North, factory.MakeWall());
    r2->SetSide(East,  factory.MakeWall());
    r2->SetSide(South, factory.MakeWall());
    r2->SetSide(West,  aDoor);

    return aMaze;
}
```

**EnchantedMazeFactory — overrides room and door creation:**
```cpp
class EnchantedMazeFactory : public MazeFactory {
public:
    EnchantedMazeFactory();
    Room* MakeRoom(int n)  const override {
        return new EnchantedRoom(n, CastSpell());
    }
    Door* MakeDoor(Room* r1, Room* r2) const override {
        return new DoorNeedingSpell(r1, r2);
    }
protected:
    Spell* CastSpell() const;
};
```

**BombedMazeFactory — overrides wall and room creation:**
```cpp
class BombedMazeFactory : public MazeFactory {
public:
    Wall* MakeWall()       const override { return new BombedWall; }
    Room* MakeRoom(int n)  const override { return new RoomWithABomb(n); }
};
```

**Usage:**
```cpp
MazeGame game;
BombedMazeFactory factory;
game.CreateMaze(factory);  // all rooms are RoomWithABomb, all walls are BombedWall

// Alternatively
EnchantedMazeFactory enchantedFactory;
game.CreateMaze(enchantedFactory);  // all rooms are EnchantedRoom, doors need spells
```

**Smalltalk prototype-based equivalent:**

The Smalltalk version uses a single `MazeFactory` class with a `partCatalog` dictionary, eliminating the `EnchantedMazeFactory` and `BombedMazeFactory` subclasses:

```smalltalk
"createMaze equivalent in Smalltalk"
createMaze: aFactory
    | room1 room2 aDoor |
    room1 := (aFactory make: #room) number: 1.
    room2 := (aFactory make: #room) number: 2.
    aDoor := (aFactory make: #door) from: room1 to: room2.
    room1 atSide: #north put: (aFactory make: #wall).
    room1 atSide: #east  put: aDoor.
    room1 atSide: #south put: (aFactory make: #wall).
    room1 atSide: #west  put: (aFactory make: #wall).
    room2 atSide: #north put: (aFactory make: #wall).
    room2 atSide: #east  put: (aFactory make: #wall).
    room2 atSide: #south put: (aFactory make: #wall).
    room2 atSide: #west  put: aDoor.
    ^ Maze new addRoom: room1; addRoom: room2; yourself

"Default MazeFactory — classes as prototypes"
createMazeFactory
    ^ (MazeFactory new
        addPart: Wall  named: #wall;
        addPart: Room  named: #room;
        addPart: Door  named: #door;
        yourself)

"EnchantedMazeFactory — no new class needed"
createEnchantedMazeFactory
    ^ (MazeFactory new
        addPart: Wall             named: #wall;
        addPart: EnchantedRoom    named: #room;
        addPart: DoorNeedingSpell named: #door;
        yourself)
```

---

## Known Uses

**InterViews** uses the "Kit" suffix to denote AbstractFactory classes. `WidgetKit` and `DialogKit` are abstract factories for generating look-and-feel-specific user interface objects. `LayoutKit` generates different composition objects depending on document orientation (portrait or landscape).

**ET++** uses Abstract Factory to achieve portability across window systems (X Windows and SunView). The `WindowSystem` abstract base class defines the interface for creating objects representing window system resources (`MakeWindow`, `MakeFont`, `MakeColor`). Concrete subclasses implement the interfaces for a specific window system. At runtime, ET++ creates an instance of a concrete `WindowSystem` subclass.

---

## Related Patterns

- **Factory Method** — AbstractFactory classes are often implemented with factory methods. The ConcreteFactory is a collection of factory methods, one per product type.
- **Prototype** — AbstractFactory classes can also be implemented using the Prototype pattern. The factory stores prototype instances and clones them to create new products. Eliminates the need for a ConcreteFactory subclass per family.
- **Singleton** — A ConcreteFactory is often a Singleton. An application typically needs only one instance per product family.
