---
name: creational-pattern-selector
description: |
  Choose the right creational design pattern (Abstract Factory, Builder, Factory Method, Prototype, or Singleton) for an object creation problem. Use when someone asks "which factory pattern should I use?", "should I use Abstract Factory or Factory Method?", "how do I create objects without specifying the concrete class?", "I need a factory but don't know which one", or "how do I make object creation flexible?" Also use when you see hard-coded `new ConcreteClass()` calls scattered throughout code, when product families must be swapped at runtime, when object construction is too complex for a single constructor, or when objects should be created by cloning a prototype. Compares patterns using two parameterization strategies — subclassing vs object composition — with trade-offs and an evolution path from Factory Method to more flexible alternatives.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/creational-pattern-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - design-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [3]
tags: [design-patterns, object-oriented, gof, creational, abstract-factory, builder, factory-method, prototype, singleton]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "Description of an object creation problem — concrete class references, construction complexity, or any creation-related design pain"
  tools-required: [TodoWrite]
  tools-optional: [Read, Grep]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, scanning it provides additional context but is not required."
---

# Creational Pattern Selector

## When to Use

You have an object creation problem that needs a structural solution. This skill applies when:

- Code hard-codes `new ConcreteClass()` calls in places where the class type should be variable
- You need to create families of related objects that must be used together consistently
- Object construction is complex — multi-step, multi-part, or produces different representations
- You want to create objects by copying a known configuration rather than constructing from scratch
- A class must have exactly one instance with globally accessible state
- You've been told to "use a creational pattern" but need help picking which one

Before starting, verify you have a creation problem — not a structural or behavioral one. If you're not sure whether it's a creation problem at all, invoke the `design-pattern-selector` skill first, which will classify the problem and route here if appropriate.

## Context & Input Gathering

### Required Context

- **What is being created:** What type of object? Is it a product, a complex structure, a family of related objects, or a resource that should be shared?
- **What is inflexible now:** Where are concrete class names hard-coded? What happens when a new variant is needed?
- **Who calls the creation code:** Is it a framework, an application, a client class?

### Useful Context (gather from codebase if available)

- Search for `new ConcreteClass()` calls scattered across multiple files — indicates Factory Method or Abstract Factory
- Search for telescoping constructors (many parameters or many overloads) — indicates Builder
- Look for `clone()` or copy-constructor patterns — indicates Prototype already in use or needed
- Look for global variables or static accessor patterns managing a shared object — indicates Singleton

---

## Process

### Step 1: Frame the Creation Problem

**ACTION:** Use `TodoWrite` to track steps, then articulate what aspect of creation is inflexible.

**WHY:** Creational patterns solve five distinct problems. The right pattern becomes obvious once you identify which of the five matches your situation. Without this framing, patterns get conflated (e.g., using Builder when Factory Method would suffice).

```
TodoWrite:
- [ ] Step 1: Frame the creation problem
- [ ] Step 2: Identify the parameterization strategy
- [ ] Step 3: Check the five applicability checklists
- [ ] Step 4: Consider the evolution path
- [ ] Step 5: Produce scored recommendation with trade-offs
```

Capture these elements:

| Element | Question |
|---------|----------|
| **Product type** | Single object, family of related objects, or complex composite object? |
| **Variation axis** | What needs to vary — the concrete class, the construction steps, or the state? |
| **Flexibility timing** | Must creation be flexible at compile-time or at run-time? |
| **Uniqueness constraint** | Must the system allow only one instance? |

---

### Step 2: Identify the Parameterization Strategy

**ACTION:** Determine which of the two fundamental strategies applies to this problem.

**WHY:** The GoF Discussion of Creational Patterns identifies two recurring ways to make a system independent of how objects are created. Understanding which strategy you're using eliminates half the candidate patterns immediately and reveals the underlying design commitment you're making.

**Strategy 1 — Subclass-based (class parameterization):**
The class that creates objects is subclassed to change what gets created. The creator class calls a virtual factory method; subclasses override it to return different product types.
- **Pattern:** Factory Method
- **Commitment:** Adding a new product variant means adding a new subclass of the creator
- **Risk:** Subclass proliferation — changing the product can cascade to changing the creator's class hierarchy
- **When appropriate:** You're building a framework where the instantiation hook is the only customization needed; creation logic is confined to one method

**Strategy 2 — Composition-based (object parameterization):**
An external object is responsible for knowing which concrete classes to create. That object is passed into the creator as a parameter or configured at startup.
- **Patterns:** Abstract Factory, Builder, Prototype
- **Commitment:** Adding a new product variant means creating a new factory/builder/prototype object — no subclassing of the creator required
- **Advantage:** More flexible — the creator is entirely unaware of concrete product classes
- **When appropriate:** You need run-time flexibility, multiple product families, or want to decouple creation from the creator's class hierarchy entirely

**Output of this step:** Identify which strategy fits. If the flexibility is needed at run-time or affects multiple product types, lean toward composition-based (Strategy 2). If a single virtual method suffices, consider Factory Method (Strategy 1).

---

### Step 3: Check the Five Applicability Checklists

**ACTION:** Run the problem against each pattern's applicability criteria. Mark which conditions are satisfied.

**WHY:** Each creational pattern has a precise set of conditions that distinguish it from the others. Checking all five prevents the common mistake of picking the most familiar pattern rather than the most fitting one. A pattern with 3 of 3 matching conditions beats one with 2 of 4.

Detailed applicability criteria are in `references/creational-comparison.md`. Summary checklists:

**Abstract Factory** — use when ALL of these hold:
- [ ] The system creates families of related or dependent objects
- [ ] The system must be configured with one of multiple product families
- [ ] You need to enforce that products from one family are used together (compatibility constraint)
- [ ] You want to reveal only product interfaces, not implementations

*Example trigger:* UI toolkit supporting multiple look-and-feel standards — Motif or Presentation Manager. Each look-and-feel is a product family (windows, scrollbars, buttons). Swapping the factory swaps the entire family consistently.

**Builder** — use when ALL of these hold:
- [ ] Object construction is complex: multi-step, multi-part assembly
- [ ] The same construction process should produce different representations
- [ ] The construction algorithm must be independent of the parts and how they're assembled

*Example trigger:* A document converter that reads one format (RTF) and can produce multiple output formats (ASCII text, TeX, interactive widget). The parsing algorithm (Director) is stable; only the converter object (Builder) changes.

**Factory Method** — use when ANY of these hold:
- [ ] A class cannot anticipate the class of objects it must create
- [ ] A class wants its subclasses to specify the objects it creates
- [ ] Classes delegate creation responsibility to helper subclasses and you want to localize the knowledge of which helper is used

*Example trigger:* An application framework that manages Document objects, but the framework cannot know which Document subclass the application will use. The framework calls a virtual `CreateDocument()` factory method; application subclasses override it.

**Prototype** — use when ALL of these hold:
- [ ] The system must be independent of how its products are created AND
- [ ] Classes to instantiate are specified at run-time (e.g., dynamic loading) OR
- [ ] You want to avoid building a parallel creator class hierarchy for each product type OR
- [ ] Instances can have only a few different combinations of state — cloning configured instances is easier than manual construction each time

*Example trigger:* A graphical editor where each tool creates graphic objects. Instead of subclassing the tool for each graphic type (subclass explosion), each tool is parameterized with a prototype it clones when the user draws.

**Singleton** — use when BOTH of these hold:
- [ ] There must be exactly one instance of the class, accessible to all clients
- [ ] The sole instance may need to be extensible by subclassing, and clients must be able to use the extended instance without modifying their code

*Example trigger:* A maze game where all game objects need access to the Maze — without passing the maze as a parameter everywhere. Singleton ensures one maze exists and provides a well-known access point.

---

### Step 4: Consider the Evolution Path

**ACTION:** Assess where the system is now and where it needs to go. Map that against the natural evolution path.

**WHY:** The GoF explicitly states that designs often start with Factory Method and evolve toward Abstract Factory, Builder, or Prototype as flexibility needs grow. Starting with the most flexible pattern when Factory Method would suffice is over-engineering. But starting with Factory Method when Abstract Factory is needed leads to a painful refactor. Knowing the trajectory saves both mistakes.

**Evolution path:**

```
Factory Method
    |
    | → When you need multiple product families  → Abstract Factory
    |
    | → When construction is complex/multi-step  → Builder
    |
    | → When subclass proliferation is the pain  → Prototype
    |
    | → When you need one shared instance        → Singleton (orthogonal — often combined with the above)
```

**Trajectory questions:**
1. Will the number of product variants grow? If yes, how — more types of the same product (stay with Factory Method), or multiple coordinated families (move to Abstract Factory)?
2. Will construction complexity grow? If construction is currently simple but expected to gain optional parts, configure-then-build patterns, or multiple output representations → Builder
3. Is subclass proliferation already a problem, or is it a future risk? Prototype is the aggressive solution; Factory Method may be enough early on
4. Singleton is often combined with, not instead of, the other patterns — e.g., a Singleton AbstractFactory manages the product family for the whole application

**Maze game comparison (from the GoF):**

The `MazeGame::CreateMaze()` function is the baseline: it hard-codes `new Room`, `new Wall`, `new Door`. To support enchanted mazes (EnchantedRoom, DoorNeedingSpell), each pattern applies differently:

| Pattern | How CreateMaze changes |
|---------|----------------------|
| Factory Method | MazeGame calls virtual `MakeRoom()`, `MakeWall()`, `MakeDoor()`. EnchantedMazeGame overrides them. |
| Abstract Factory | CreateMaze is passed a MazeFactory parameter. EnchantedMazeFactory returns enchanted parts. |
| Builder | CreateMaze is passed a MazeBuilder object. Builder constructs the maze incrementally. |
| Prototype | CreateMaze is passed prototypical Room, Wall, Door instances it clones. |
| Singleton | MazeFactory is a Singleton — one factory per application, globally accessible. |

---

### Step 5: Produce Recommendation

**ACTION:** Deliver a structured recommendation in the format below, based on the steps above.

**WHY:** A clear recommendation with explicit trade-offs enables the developer to commit confidently or challenge the reasoning. Surfacing the runner-up pattern and why it was ruled out prevents second-guessing after implementation starts.

**Recommendation format:**

```
## Creational Pattern Recommendation: [Pattern Name]

**Parameterization strategy:** [Subclass-based / Composition-based]

**Why this pattern:** [1–2 sentences: connect the pattern's applicability conditions to the specific problem]

**What it decouples:** [What concrete class references are eliminated from the caller]

**What you gain:** [Key benefit — flexibility, consistency, construction control, etc.]

**Key trade-off:** [Cost — added classes, complexity, or constraint]

**Evolution note:** [When to migrate to a more flexible pattern, if applicable]

**Alternative considered:** [Runner-up] — [Why it was not chosen]

**Compatible with:** [Other patterns that combine well, e.g., Singleton + Abstract Factory]
```

---

## Examples

### Example 1: Cross-Platform UI Toolkit

**Scenario:** A UI toolkit must support two look-and-feel standards (Motif and a custom dark theme). Both have windows, buttons, and scrollbars. Clients should be able to switch the entire look-and-feel without knowing which concrete widget classes they're using.

**Trigger:** "We need to support multiple themes and the theme selection should be swappable at startup without touching client code."

**Process:**
- Step 2: Composition-based — the factory object knows which concrete widget classes to create; clients are parameterized with the factory
- Step 3: Abstract Factory matches all four conditions — related family (window + button + scrollbar), multiple families (Motif + dark), compatibility constraint (all widgets from same family), hide implementations
- Step 4: Evolution — if more themes are expected, Abstract Factory scales cleanly (add a new ConcreteFactory). Factory Method would require subclassing the client for each theme combination.

**Output:**
```
## Creational Pattern Recommendation: Abstract Factory

**Parameterization strategy:** Composition-based

**Why this pattern:** There are multiple coordinated product families (widget sets per look-and-feel),
and clients must use widgets from one consistent family. Abstract Factory encapsulates this
family constraint as a factory object passed to clients.

**What it decouples:** All concrete widget class names from client code. Clients
only reference abstract Widget interfaces and the WidgetFactory interface.

**What you gain:** Swapping the entire look-and-feel is a single factory substitution.
The constraint that Motif widgets go with Motif scrollbars is enforced automatically.

**Key trade-off:** Adding a new widget type (e.g., a tooltip) requires changing the
AbstractFactory interface and all ConcreteFactory implementations.

**Evolution note:** If themes are runtime-configurable (loaded from disk, user preference),
combine with Prototype — register prototypical widget instances per theme.

**Alternative considered:** Factory Method — would require subclassing the client application
for each theme, which does not scale when themes are selected at run-time.
```

---

### Example 2: Document Converter with Multiple Output Formats

**Scenario:** An application reads one input format (Markdown) and must produce different output representations: plain text, HTML, and a rich text widget for in-app editing. The parsing algorithm is stable; only the output format changes.

**Trigger:** "The same parsing logic needs to produce completely different output formats. Adding a new format shouldn't require touching the parser."

**Process:**
- Step 2: Composition-based — a converter object (Builder) is passed to the parser (Director)
- Step 3: Builder matches — complex multi-part output, same construction process (parsing), multiple representations (plain text vs HTML vs widget)
- Step 4: Evolution path — if the number of formats grows, each is a new ConcreteBuilder, zero changes to the parser

**Output:**
```
## Creational Pattern Recommendation: Builder

**Parameterization strategy:** Composition-based

**Why this pattern:** The parsing algorithm (Director) is stable and orthogonal to
how the output format is assembled. Builder separates the algorithm from the
representation by providing the parser with a converter interface (Builder) that
each output format implements independently.

**What it decouples:** The parser from all output format classes. The parser calls
BuildParagraph(), BuildHeading() — it never references HTMLConverter or TextConverter.

**What you gain:** New output format = new ConcreteBuilder class. Zero changes to parser.
Formats can have internal state (e.g., tracking open tags in HTML) hidden from the parser.

**Key trade-off:** Builder requires a Director–Builder collaboration; it adds more
structure than directly parameterizing with a conversion function. Justified when
construction is genuinely multi-step with internal state.

**Evolution note:** If the parser needs to support multiple input formats too,
Abstract Factory could manage the pairing of reader + builder per format combination.

**Alternative considered:** Abstract Factory — suited for families of related objects,
not for a single complex object assembled step-by-step from sequential operations.
```

---

### Example 3: Game Maze with Variant Room Types

**Scenario:** A maze game's `CreateMaze()` method directly instantiates `Room`, `Wall`, and `Door` with `new`. The team wants to introduce an enchanted maze variant with `EnchantedRoom` and `DoorNeedingSpell` without duplicating the construction logic.

**Trigger:** "We want to reuse the maze creation algorithm for different maze variants, but it's hard-coded to specific classes."

**Process:**
- Step 2: Depends on flexibility needed. If one override point suffices (just override a few virtual methods), Factory Method is enough. If the entire set of maze component types must vary together, Abstract Factory is cleaner.
- Step 3: Factory Method matches — a class (MazeGame) cannot anticipate which Room subclass to create; subclasses should specify it. Abstract Factory also matches if the component types must be coordinated as a family.
- Step 4: Start with Factory Method — it only requires adding virtual `MakeRoom()`, `MakeWall()`, `MakeDoor()` to MazeGame and overriding them in EnchantedMazeGame. Evolve to Abstract Factory only if maze variants proliferate and need to be swappable at runtime.

**Output:**
```
## Creational Pattern Recommendation: Factory Method (evolve to Abstract Factory if needed)

**Parameterization strategy:** Subclass-based (Factory Method) — composition-based
(Abstract Factory) when variants must be runtime-swappable

**Why this pattern:** MazeGame knows when to create rooms and doors but should not
decide which concrete type. Factory Method adds virtual creation methods; EnchantedMazeGame
overrides them. The construction algorithm in CreateMaze() is unchanged.

**What it decouples:** MazeGame from the concrete component classes Room, Wall, Door.
CreateMaze() calls MakeRoom() instead of new Room().

**What you gain:** Adding a new maze variant is one new subclass of MazeGame with
three method overrides. No duplication of the construction algorithm.

**Key trade-off:** Every new maze variant requires a new MazeGame subclass. If variants
must be selected at runtime (not compile-time), this becomes awkward — that signals
the need to migrate to Abstract Factory.

**Evolution note:** When maze types need to be chosen at startup or loaded from config,
replace the subclass approach with an AbstractMazeFactory passed to CreateMaze(). The
factory object becomes a Singleton if only one maze type is active per application run.

**Alternative considered:** Abstract Factory — more flexible but requires an extra
factory object hierarchy from the start; over-engineered if compile-time subclassing is sufficient.
```

---

## Key Principles

- **Start with Factory Method, evolve as needed.** Designs typically start with Factory Method (simplest) and evolve toward Abstract Factory, Builder, or Prototype as flexibility needs emerge. Don't over-engineer from day one. WHY: The GoF authors document this evolution path explicitly — premature flexibility adds complexity without value.
- **Two strategies, one question.** The fundamental choice is: parameterize by subclassing (Factory Method) or by object composition (Abstract Factory/Builder/Prototype)? If you need runtime swapping, you need composition. WHY: This single fork eliminates 3 of 5 candidates immediately.
- **Factory Method cascading is the key warning sign.** If creating a new product variant requires a new creator subclass, AND that creator is itself created by a factory method, the cascade has begun. This signals the need to evolve to Abstract Factory or Prototype. WHY: Cascade subclassing is the primary cost of Factory Method.

## Reference Files

| File | Contents |
|------|----------|
| `references/creational-comparison.md` | Full applicability, consequences, and trade-off table for all 5 creational patterns; maze game comparison; GraphicTool example |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-design-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
