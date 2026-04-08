---
name: abstract-factory-implementor
description: |
  Implement the Abstract Factory pattern to create families of related objects without specifying their concrete classes. Use when a system must be independent of how its products are created, when it must work with multiple product families, when products are designed to be used together and you need to enforce that constraint, or when providing a class library revealing only interfaces. Covers factory-as-singleton, prototype-based factories, and extensible factory interfaces.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/abstract-factory-implementor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - creational-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [3]
    pages: [54-58, 88-96]
tags: [design-patterns, creational, gof, abstract-factory, product-families, portability, refactoring]
execution:
  tier: 2
  mode: full
  inputs:
    - type: code
      description: "Existing code with hard-coded concrete class instantiation spread across a client, or a design description of a system that must support multiple product families"
  tools-required: [TodoWrite, Read]
  tools-optional: [Grep, Edit]
  mcps-required: []
  environment: "Any codebase. Language-agnostic — examples use C++ and Python but the pattern applies universally."
---

# Abstract Factory Implementor

## When to Use

You are creating families of related objects and the client must stay independent of which concrete family it uses. This skill applies under four specific conditions — all are sufficient; any one justifies the pattern:

1. **Product-creation independence** — a system should not depend on how its products are created, composed, or represented. Clients should work against abstract interfaces, not constructor calls.
2. **Multiple product families** — the system must be configured with one of several families of products (e.g., Motif widgets vs. Presentation Manager widgets vs. Mac widgets), and the choice of family should be a single point of configuration, not scattered throughout the codebase.
3. **Enforced co-usage** — products within a family are designed to work together, and you need a structural guarantee that clients never mix products from different families (a MotifScrollBar with a PMButton, for instance, is a violation the pattern makes structurally impossible).
4. **Interface-only library** — you are providing a class library and want to reveal only interfaces, not implementations. Clients code against the abstract factory and abstract product classes; the concrete implementations are deployment-time choices.

Before starting, confirm this is not a simpler case:
- If only **one** product type varies, prefer Factory Method — Abstract Factory is for *families* of products that must vary together.
- If the products are not related (no co-usage constraint), the coordination overhead of Abstract Factory is not justified.

---

## Process

### Step 1: Set Up Tracking and Map the Product Families

**ACTION:** Use `TodoWrite` to track progress, then identify all product types and all families.

**WHY:** The Abstract Factory interface is fixed at design time based on the product types you identify here. Missing a product type now means changing the AbstractFactory interface later, which requires updating every ConcreteFactory — the most expensive structural change possible. A complete product-family map made upfront prevents this.

```
TodoWrite:
- [ ] Step 1: Map product types and product families
- [ ] Step 2: Define AbstractProduct interfaces
- [ ] Step 3: Define the AbstractFactory interface
- [ ] Step 4: Implement ConcreteFactory classes
- [ ] Step 5: Wire the client to use the factory
- [ ] Step 6: Handle singleton, prototype, or extensibility concerns
- [ ] Step 7: Validate and document known trade-offs
```

**Applicability gate — confirm at least one of these four GoF conditions holds before proceeding:**

| # | Condition | Check |
|---|-----------|-------|
| 1 | System should be independent of how its products are created/composed/represented | Does client code currently name concrete product classes? |
| 2 | System must be configured with one of multiple product families | Are there 2+ families that could be swapped? |
| 3 | Products within a family are designed to be used together — co-usage must be enforced | Would mixing products from different families cause bugs? |
| 4 | You want to reveal only product interfaces, not implementations | Should concrete classes be hidden from library consumers? |

**IF none hold → this is not an Abstract Factory problem.** Consider Factory Method (single product) or Builder (complex construction).

**Alternative to consider — Prototype-based factory:** If many product families exist or families differ only slightly, a single factory initialized with prototype instances (cloning instead of subclassing) eliminates the ConcreteFactory subclass explosion. Evaluate this option in Step 6 — but be aware of it now so you don't commit to a subclass-per-family design prematurely.

Produce a product matrix before writing any code:

| Product type | Family A | Family B | Family C |
|--------------|----------|----------|----------|
| ScrollBar | MotifScrollBar | PMScrollBar | MacScrollBar |
| Button | MotifButton | PMButton | MacButton |
| Menu | MotifMenu | PMMenu | MacMenu |

The columns are your ConcreteFactories. The rows are your AbstractProduct interfaces. Count the rows — that is the number of factory methods on your AbstractFactory interface.

---

### Step 2: Define AbstractProduct Interfaces

**ACTION:** For each product type (each row in the matrix), declare an abstract interface or base class.

**WHY:** The AbstractProduct interfaces are the contracts the client codes against. They are what make the client independent of concrete classes. Every method the client needs to call on a product must appear on the AbstractProduct interface — if a client has to downcast to access concrete behavior, the interface is incomplete and the isolation benefit disappears.

For each product type:
1. Name it for the domain concept, not the family (e.g., `ScrollBar`, not `MotifScrollBar`)
2. Declare only the operations all families must support
3. Keep it minimal — only what the client actually calls

See the reference file for full code examples in C++, Python, and Smalltalk.

---

### Step 3: Define the AbstractFactory Interface

**ACTION:** Declare an abstract factory class with one creation method per product type.

**WHY:** The AbstractFactory interface encodes the complete set of products the system knows about. Its method signatures return AbstractProduct types, never concrete types — this is what prevents concrete class names from appearing in client code. The factory interface is the "catalog" of the product family; each ConcreteFactory is one edition of that catalog.

```cpp
class GUIFactory {
public:
    virtual ScrollBar* CreateScrollBar() = 0;
    virtual Button*    CreateButton()    = 0;
    virtual Menu*      CreateMenu()      = 0;
    virtual ~GUIFactory() = default;
};
```

**Naming convention:** Prefix with `Create` (C++/Java) or `create_` (Python). This makes factory methods instantly recognizable in code review and distinguishes them from ordinary method calls.

---

### Step 4: Implement ConcreteFactory Classes

**ACTION:** For each product family (each column in the matrix), create a ConcreteFactory subclass that implements every creation method.

**WHY:** Each ConcreteFactory encapsulates complete knowledge of one product family. A client that holds a `MotifFactory` reference is guaranteed to receive only Motif products — the factory enforces the co-usage constraint structurally, not through documentation or convention. This is the core value: consistency across a product family is automatic, not policed.

```cpp
class MotifFactory : public GUIFactory {
public:
    ScrollBar* CreateScrollBar() override { return new MotifScrollBar; }
    Button*    CreateButton()    override { return new MotifButton; }
    Menu*      CreateMenu()      override { return new MotifMenu; }
};

class PMFactory : public GUIFactory {
public:
    ScrollBar* CreateScrollBar() override { return new PMScrollBar; }
    Button*    CreateButton()    override { return new PMButton; }
    Menu*      CreateMenu()      override { return new PMMenu; }
};
```

For each ConcreteFactory, implement the corresponding ConcreteProduct classes:

```cpp
class MotifScrollBar : public ScrollBar {
public:
    void ScrollTo(int position) override {
        // Motif-specific scroll rendering
    }
};

class PMScrollBar : public ScrollBar {
public:
    void ScrollTo(int position) override {
        // Presentation Manager scroll rendering
    }
};
```

---

### Step 5: Wire the Client to Use the Factory

**ACTION:** Refactor the client to receive an AbstractFactory reference and call only factory methods and AbstractProduct interfaces — no `new ConcreteProduct(...)` calls anywhere in client code.

**WHY:** The client has to commit to using the factory interface consistently. A single stray `new MotifScrollBar` in the client code breaks the isolation guarantee — the concrete class name is back in client code and the family-switching benefit is lost. This step is not complete until `grep` finds zero concrete class names imported or instantiated in client code.

**Before (hard-coded, platform-specific):**
```cpp
// Every widget creation exposes a concrete class name
ScrollBar* sb = new MotifScrollBar;
Button* btn   = new MotifButton;
Menu* menu    = new MotifMenu;
```

**After (factory-mediated, platform-independent):**
```cpp
void Application::BuildInterface(GUIFactory* factory) {
    // No concrete class names — family is entirely encapsulated in factory
    ScrollBar* sb  = factory->CreateScrollBar();
    Button*    btn = factory->CreateButton();
    Menu*      menu = factory->CreateMenu();
    // ...
}
```

**Factory initialization** — this must happen once, before the client first needs a product, at the program's configuration point:

```cpp
// Compile-time known family
GUIFactory* guiFactory = new MotifFactory;

// Runtime-selected family (environment or config)
const char* styleName = getenv("LOOK_AND_FEEL");
if (strcmp(styleName, "Motif") == 0) {
    guiFactory = new MotifFactory;
} else if (strcmp(styleName, "Presentation_Manager") == 0) {
    guiFactory = new PMFactory;
} else {
    guiFactory = new DefaultGUIFactory;
}
// Pass guiFactory to all subsystems — they never see a concrete class name
```

---

### Step 6: Handle Singleton, Prototype, or Extensibility Concerns

**ACTION:** Apply one or more of the three standard implementation refinements based on the system's constraints.

**WHY:** The basic four-step structure above covers the standard case. The three refinements address recurring complications. Choosing the wrong refinement (or skipping one when it is needed) leads to: unnecessary multi-instantiation of factories (singleton concern), an explosion of ConcreteFactory subclasses when families multiply (prototype concern), or a brittle interface that breaks when new product types are added (extensibility concern).

**Refinement A — Factories as Singletons**

An application typically needs exactly one instance of each ConcreteFactory per product family. Multiple instances would allow different parts of the application to use different families simultaneously, which is precisely the co-usage violation the pattern prevents.

Apply the Singleton pattern to each ConcreteFactory class. The factory's construction is then controlled and the single instance is shared across all clients.

**Refinement B — Prototype-based Factories (when families are many and similar)**

The factory-method approach requires a new ConcreteFactory subclass for each product family. When many product families exist (or families differ only slightly), this produces a combinatorial number of factory subclasses.

The alternative: a single concrete factory initialized with prototype instances. The factory's `Make` method clones the appropriate prototype rather than calling a subclass-specific factory method:

```smalltalk
"Smalltalk prototype-based factory"
make: partName
    ^ (partCatalog at: partName) copy

addPart: partTemplate named: partName
    partCatalog at: partName put: partTemplate
```

Creating an EnchantedMazeFactory requires no new class — only a different factory initialization:

```smalltalk
createMazeFactory
    ^ (MazeFactory new
        addPart: Wall named: #wall;
        addPart: EnchantedRoom named: #room;
        addPart: DoorNeedingSpell named: #door;
        yourself)
```

Prefer the prototype approach when: (a) many product families exist, (b) families differ only in which concrete products they use, or (c) you need to create new families at runtime by composing existing prototypes.

**Refinement C — Extensible Factory Interface**

The standard AbstractFactory interface is closed: adding a new product type requires changing the interface and all ConcreteFactories. A more flexible (but less type-safe) alternative is a single parameterized `Make` method:

```cpp
// Type-safe but closed
virtual ScrollBar* CreateScrollBar() = 0;
virtual Button*    CreateButton() = 0;

// Flexible but loses static type safety
virtual AbstractProduct* Make(const string& productKind) = 0;
```

The parameterized version needs only one method change when new product types are added, but products are returned as a common abstract type — clients must cast (or use dynamic typing). This trade-off is the classic **extensibility vs. type safety** tension.

Use the extensible form when: the product type set is known to grow, you are in a dynamically typed language (where the casting cost disappears), or the flexibility benefit outweighs the safety cost. Stick with the standard form when: the product set is stable, static type checking matters, and you want the compiler to catch misuse.

---

### Step 7: Validate and Document Known Trade-offs

**ACTION:** Verify the implementation satisfies all invariants, then explicitly document the extensibility liability.

**WHY:** Two of the four consequences of Abstract Factory are benefits (isolation, easy exchange), one is a benefit-with-a-condition (consistency, which only holds if you never mix factories), and one is a genuine liability (supporting new product kinds is hard). Documenting the liability upfront prevents the team from discovering it painfully later when someone tries to add a new product type.

**Validation checklist:**
- [ ] No concrete product class names appear in client code (verify with grep)
- [ ] Every product type in the matrix has an AbstractProduct interface
- [ ] Every ConcreteFactory implements every AbstractProduct creation method
- [ ] Factory is initialized once, at application startup or configuration boundary
- [ ] If Singleton refinement was applied — factory construction is controlled
- [ ] If Prototype refinement was applied — prototype registry is populated before first use
- [ ] If Extensibility refinement was applied — all clients handle the downcast safely

**Document the trade-off:**

| Consequence | Effect |
|-------------|--------|
| Isolates concrete classes | Client code contains zero concrete class names; all coupling runs through abstract interfaces |
| Easy family exchange | Changing the entire product family requires changing exactly one factory instantiation site |
| Enforces product consistency | Using objects from different families simultaneously is structurally impossible — the factory guarantees the constraint |
| Hard to add new product types | Adding a new product type requires changing AbstractFactory and every ConcreteFactory — this cascades across the entire hierarchy |

---

## Inputs

- Existing code with scattered `new ConcreteProduct(...)` calls that need to be family-switched, OR
- A design description identifying: (a) product types, (b) product families, (c) the client that consumes products

## Outputs

- `abstract_factory.py` (or `.h`/`.cpp`, `.java`, etc.) — AbstractFactory + AbstractProduct interfaces
- `concrete_factories.py` — one ConcreteFactory per family, with ConcreteProduct implementations
- Updated client code — factory-mediated, with all concrete class names removed

---

## Key Principles

- **The interface is the commitment** — every product type your AbstractFactory declares is a permanent entry in the contract. Adding product types later is costly. Invest in completeness at design time rather than patching the interface repeatedly.

- **One factory initialization point** — the concrete factory should be chosen exactly once, at the application's configuration boundary. Allowing factory selection to spread through the codebase recreates the family-mixing problem the pattern solves.

- **Consistency is structural, not conventional** — the value of Abstract Factory over a naming convention ("always use Motif widgets together") is that the structure makes family mixing impossible. If clients can bypass the factory, the guarantee evaporates.

- **Prototype over subclass when families multiply** — factory-method-based AbstractFactory creates one ConcreteFactory subclass per product family. When families are many or differ only slightly, the prototype approach eliminates the subclass explosion without sacrificing the interface guarantee.

- **The extensibility liability is real** — Abstract Factory trades extensibility for consistency. The pattern is appropriate when the product type set is stable. If new product types are expected frequently, the parameterized `Make` interface or a different pattern (Prototype, Builder) may be more appropriate.

---

## Examples

### Example 1: Lexi GUIFactory — Look-and-Feel Portability

**Scenario:** Lexi, a document editor, must run on Motif, Presentation Manager, and Mac. Every widget creation call currently names a concrete class, making it impossible to switch look-and-feel at runtime or port to a new platform without auditing the entire codebase.

**Trigger:** "We need to support a new look-and-feel standard, but widgets are instantiated directly throughout the application."

**Product matrix:**

| Product type | MotifFactory | PMFactory | MacFactory |
|---|---|---|---|
| ScrollBar | MotifScrollBar | PMScrollBar | MacScrollBar |
| Button | MotifButton | PMButton | MacButton |
| Menu | MotifMenu | PMMenu | MacMenu |

**AbstractFactory interface:**
```cpp
class GUIFactory {
public:
    virtual ScrollBar* CreateScrollBar() = 0;
    virtual Button*    CreateButton()    = 0;
    virtual Menu*      CreateMenu()      = 0;
};
```

**Runtime family selection at startup:**
```cpp
GUIFactory* guiFactory;
const char* styleName = getenv("LOOK_AND_FEEL");

if (strcmp(styleName, "Motif") == 0)
    guiFactory = new MotifFactory;
else if (strcmp(styleName, "Presentation_Manager") == 0)
    guiFactory = new PMFactory;
else
    guiFactory = new DefaultGUIFactory;

// guiFactory passed to all Application subsystems
// No subsystem ever imports or names MotifScrollBar, PMButton, etc.
```

**Output:** Adding Mac support requires a `MacFactory` + three `MacProduct` classes. Zero changes to application logic, layout code, or event handling. A `MotifMenu` can never appear beside a `PMButton` — the factory makes this impossible.

---

### Example 2: MazeFactory — Swappable Maze Components

**Scenario:** A maze game hard-codes `Room`, `Wall`, and `Door` in its `CreateMaze` function. Adding enchanted mazes or bombed mazes requires forking `CreateMaze` for each variant — a maintenance problem.

**Trigger:** "Every new maze type requires duplicating the maze-building logic with different class names."

**AbstractFactory (also acts as ConcreteFactory for the default case):**
```cpp
class MazeFactory {
public:
    virtual Maze* MakeMaze()  const { return new Maze; }
    virtual Wall* MakeWall()  const { return new Wall; }
    virtual Room* MakeRoom(int n) const { return new Room(n); }
    virtual Door* MakeDoor(Room* r1, Room* r2) const { return new Door(r1, r2); }
};
```

**Client uses only factory calls — no concrete class names:**
```cpp
Maze* MazeGame::CreateMaze(MazeFactory& factory) {
    Maze* aMaze = factory.MakeMaze();
    Room* r1 = factory.MakeRoom(1);
    Room* r2 = factory.MakeRoom(2);
    Door* aDoor = factory.MakeDoor(r1, r2);

    aMaze->AddRoom(r1);
    aMaze->AddRoom(r2);
    r1->SetSide(North, factory.MakeWall());
    r1->SetSide(East, aDoor);
    r1->SetSide(South, factory.MakeWall());
    r1->SetSide(West, factory.MakeWall());
    // ...
    return aMaze;
}
```

**ConcreteFactories override only the methods that differ:**
```cpp
class EnchantedMazeFactory : public MazeFactory {
public:
    Room* MakeRoom(int n) const override {
        return new EnchantedRoom(n, CastSpell());
    }
    Door* MakeDoor(Room* r1, Room* r2) const override {
        return new DoorNeedingSpell(r1, r2);
    }
protected:
    Spell* CastSpell() const;
};

class BombedMazeFactory : public MazeFactory {
public:
    Wall* MakeWall() const override { return new BombedWall; }
    Room* MakeRoom(int n) const override { return new RoomWithABomb(n); }
};
```

**Usage — single factory swap changes the entire maze variant:**
```cpp
MazeGame game;
BombedMazeFactory factory;
game.CreateMaze(factory);  // builds a maze with bombs — zero changes to CreateMaze
```

**Output:** `CreateMaze` is written once. Supporting three maze variants requires three factory classes — none of which touch the maze-building algorithm. The Smalltalk prototype-based version creates `EnchantedMazeFactory` without a new class, by initializing a `MazeFactory` with different prototype instances for `#room` and `#door`.

---

### Example 3: Database Abstraction Layer

**Scenario:** A backend application runs tests against SQLite and production against PostgreSQL. Connection, query builder, and transaction objects all vary by database. Currently the database type is conditionally checked in dozens of places.

**Trigger:** "We have `if db == 'postgres'` scattered everywhere — adding a MySQL test environment would require touching every one."

**Product matrix:**

| Product type | PostgresFactory | SQLiteFactory |
|---|---|---|
| Connection | PostgresConnection | SQLiteConnection |
| QueryBuilder | PostgresQueryBuilder | SQLiteQueryBuilder |
| Transaction | PostgresTransaction | SQLiteTransaction |

**AbstractFactory + client:**
```python
class DatabaseFactory(ABC):
    @abstractmethod
    def create_connection(self) -> Connection: ...

    @abstractmethod
    def create_query_builder(self) -> QueryBuilder: ...

    @abstractmethod
    def create_transaction(self) -> Transaction: ...

# Client receives factory — never imports Postgres or SQLite classes
class Repository:
    def __init__(self, factory: DatabaseFactory):
        self._conn = factory.create_connection()
        self._qb   = factory.create_query_builder()

    def find_by_id(self, id: int):
        query = self._qb.select("users").where("id", id).build()
        return self._conn.execute(query)
```

**Test environment wiring:**
```python
# tests/conftest.py
factory = SQLiteFactory(":memory:")

# production
factory = PostgresFactory(os.environ["DATABASE_URL"])

repo = Repository(factory)
```

**Output:** Adding MySQL support is a `MySQLFactory` class and three concrete products. Zero changes to `Repository`, zero changes to test setup beyond adding a new factory option.

---

## Reference Files

| File | Contents |
|------|----------|
| `references/abstract-factory-implementation-guide.md` | Full participants catalog, consequences analysis, prototype-based factory deep dive, extensible factory trade-off analysis, known uses (InterViews, ET++) |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-creational-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
