# Lexi Case Study — Full Pattern Interaction Map

**Source:** Design Patterns: Elements of Reusable Object-Oriented Software, Chapter 2 (Gamma, Helm, Johnson, Vlissides)

This reference documents the complete multi-pattern design of Lexi, a WYSIWYG document editor. Eight patterns solve seven design problems in one coherent system. This is the canonical demonstration that patterns are not isolated solutions — they form a coordinated architecture.

---

## The Seven Design Problems

Lexi's designers identified these seven distinct design challenges before choosing any pattern:

1. **Document structure:** Internal representation must support text and graphics uniformly, handle arbitrary nesting (characters → rows → columns → pages), and allow traversal for rendering, formatting, and analysis.

2. **Formatting:** The algorithm that breaks text into lines and columns must be independent of the document structure it operates on. Lexi needs multiple formatting algorithms (fast/simple vs. slow/high-quality) that clients can swap at runtime.

3. **Embellishing the user interface:** Scroll bars and borders must be addable and removable without modifying the document view class. Adding them via subclassing causes combinatorial class explosion (BorderedScrollableView, etc.).

4. **Supporting multiple look-and-feel standards:** Widget glyphs (buttons, scroll bars, menus) must match the platform's look-and-feel (Motif, Presentation Manager, Mac) without hardcoded constructor calls scattered through client code.

5. **Supporting multiple window systems:** The window drawing abstraction must work across incompatible window system APIs (X11, Presentation Manager, Mac OS) without requiring a different build per platform or a parallel class hierarchy explosion.

6. **User operations:** Operations triggered from menus, buttons, and keyboard shortcuts must share a uniform mechanism. Undo and redo must be supported for document-modifying operations without an arbitrary limit on levels.

7. **Spelling checking and hyphenation:** Analysis operations (spell checking, hyphenation, word counting, etc.) must be extensible without modifying the Glyph class hierarchy every time a new analysis is needed.

---

## The Eight Pattern Solutions

### Problem 1 → Composite

**Design problem:** Uniform treatment of document elements at all levels of nesting.

**Solution:** Define `Glyph` as an abstract base class with a common interface (Draw, Bounds, Intersects, Insert, Remove, Child, Parent). Leaf glyphs (`Character`, `Image`, `Rectangle`, `Polygon`) and composite glyphs (`Row`, `Column`, `Page`) both subclass `Glyph`. Clients treat all glyphs uniformly — a `Row::Draw()` iterates over children and calls `Draw()` on each without knowing whether any child is a leaf or a composite.

**Key participants:**
- `Glyph` — Component (abstract base class)
- `Character`, `Image`, `Rectangle`, `Polygon` — Leaf
- `Row`, `Column`, `Page` — Composite
- `Window` — Client (calls Draw on the root Glyph)

**Why this works:** The tenth element in a row could be a single character or an intricate diagram with hundreds of subelements. As long as it can `Draw()` and report its `Bounds()`, its internal complexity is irrelevant to the compositor, the formatter, and the display system.

---

### Problem 2 → Strategy

**Design problem:** Formatting algorithm must be swappable independently of document structure.

**Solution:** Define a `Compositor` abstract class with a `Compose()` operation. Introduce a `Composition` Glyph subclass that delegates formatting to a `Compositor` object. An unformatted `Composition` holds visible glyphs. When formatting is needed, it calls `compositor->Compose()`, which inserts `Row` and `Column` glyphs according to its algorithm. Three concrete strategies are defined: `SimpleCompositor` (fast, no hyphenation), `TeXCompositor` (full TeX algorithm with good color), `ArrayCompositor` (fixed-interval breaks for tables).

**Key participants:**
- `Compositor` — Strategy interface
- `SimpleCompositor`, `TeXCompositor`, `ArrayCompositor` — Concrete strategies
- `Composition` — Context (holds a reference to a Compositor)

**Why this works:** Adding a new formatting algorithm requires only a new `Compositor` subclass. The `Glyph` class hierarchy is never touched. The algorithm can be changed at runtime by calling `Composition::SetCompositor()`.

**Key insight:** The Strategy pattern requires designing interfaces general enough to support the full range of algorithms without the context (Composition) needing to know which one is running. The basic Glyph child-access interface is sufficient for all three Compositor strategies.

---

### Problem 3 → Decorator

**Design problem:** Add scroll bars and borders to the document view without class explosion via inheritance.

**Solution:** Introduce `MonoGlyph` as a `Glyph` subclass that stores a reference to one component glyph and forwards all operations to it by default. `Border` and `Scroller` subclass `MonoGlyph` and override `Draw()` to first delegate to their component (drawing the content), then draw their embellishment on top. Embellishments are composed at runtime: `Border(Scroller(Composition))` adds both a border and scroll bars.

**Key participants:**
- `MonoGlyph` — Decorator base (transparent enclosure)
- `Border` — Concrete Decorator (draws border after delegating)
- `Scroller` — Concrete Decorator (clips and offsets content)
- Any `Glyph` subclass — Component

**Why this works:** The order of composition matters and is under application control. `Border(Scroller(c))` gives a border that does not scroll; `Scroller(Border(c))` gives scroll bars that move both content and border. Neither requires a new class — just a different composition order.

**Why not inheritance:** If you add a border by subclassing `Composition`, you get `BorderedComposition`. Add scroll bars the same way and you need `BorderedComposition`, `ScrollableComposition`, and `BorderedScrollableComposition`. Every new embellishment doubles the class count. Transparent enclosure keeps embellishment classes small and their count constant.

---

### Problem 4 → Abstract Factory

**Design problem:** Create platform-specific widget glyphs (buttons, scroll bars, menus) without embedding platform names in client code.

**Solution:** Define a `GUIFactory` abstract class with factory methods: `CreateScrollBar()`, `CreateButton()`, `CreateMenu()`, etc. Concrete subclasses `MotifFactory`, `PMFactory`, `MacFactory` implement each method to return the appropriate platform-specific widget glyph. Client code holds only a `GUIFactory*` reference. The concrete factory is instantiated once at startup based on the platform environment.

**Key participants:**
- `GUIFactory` — Abstract Factory
- `MotifFactory`, `PMFactory`, `MacFactory` — Concrete Factories
- `ScrollBar`, `Button`, `Menu` — Abstract Products
- `MotifScrollBar`, `PMButton`, `MacMenu`, etc. — Concrete Products

**Why this works:** Once `guiFactory` is set to `new MotifFactory`, all subsequent widget creation calls return Motif widgets without any code change. Switching to Mac requires only `guiFactory = new MacFactory` at startup. No Motif or Mac names appear anywhere in the client code.

**Constraint:** Abstract Factory works here because Lexi controls its own widget class hierarchies. It would not work if the widget hierarchies came from incompatible vendor libraries without common abstract base classes — that is why a different approach was needed for window system portability (Problem 5).

---

### Problem 5 → Bridge

**Design problem:** Window drawing must work on multiple incompatible window systems without duplicating the Window class hierarchy per platform.

**Solution:** Separate the `Window` class hierarchy (application-level windowing: `ApplicationWindow`, `IconWindow`, `DialogWindow`) from the `WindowImp` class hierarchy (platform-level implementation: `XWindowImp`, `PMWindowImp`, `MacWindowImp`). `Window` holds a `WindowImp*` reference. All platform-specific drawing operations are delegated to `WindowImp`. Application code uses `Window`; it never calls `WindowImp` directly.

**Key participants:**
- `Window` — Abstraction
- `ApplicationWindow`, `IconWindow`, `DialogWindow` — Refined Abstractions
- `WindowImp` — Implementor interface
- `XWindowImp`, `PMWindowImp`, `MacWindowImp` — Concrete Implementors

**Why not Abstract Factory here:** Window system APIs are incompatible — they come from different vendors and cannot be made to share abstract product base classes. Abstract Factory requires common abstract products. Bridge does not — it only requires that the abstraction (`Window`) call through to `WindowImp`'s interface.

**Key insight:** `Window`'s interface caters to application programmers. `WindowImp`'s interface caters to window system engineers. They serve different masters and should evolve independently. Bridge enables both.

**Interaction with Abstract Factory:** `WindowSystemFactory` (an Abstract Factory) provides the means to create the right `WindowImp` subclass. `Window`'s constructor calls `windowSystemFactory->CreateWindowImp()` to initialize its `_imp` member. This is the canonical example of Abstract Factory configuring a Bridge.

---

### Problem 6 → Command

**Design problem:** Operations must be triggerable from multiple UI surfaces (menu items, buttons, keyboard shortcuts) with a uniform mechanism, and document-modifying operations must be undoable.

**Solution:** Define a `Command` abstract class with `Execute()` and `Unexecute()` operations, plus `Reversible()` to determine if undo is applicable. `MenuItem` stores a `Command*` reference. When clicked, `MenuItem` calls `command->Execute()`. A command history (list of Commands with a "present" pointer) supports multi-level undo: step backward calls `Unexecute()` on the command to the left of present; step forward calls `Execute()` on the command to the right.

**Key participants:**
- `Command` — abstract command interface
- `FontCommand`, `PasteCommand`, `SaveCommand`, `QuitCommand` — Concrete Commands
- `MacroCommand` — Composite Command (see interaction with Composite below)
- `MenuItem` — Invoker
- `CommandHistory` — stores the history list and present pointer

**Undo/redo mechanism:**
```
Past:  [cmd1] [cmd2] [cmd3] [cmd4] ← present
                                  ↑
                            Unexecute() moves present left
                            Execute() moves present right
```

**Selective undo:** `Reversible()` returns false for `SaveCommand` and `QuitCommand` — these are skipped during undo traversal.

**Interaction with Composite:** `MacroCommand` is a `Command` subclass that contains a list of `Command*` objects. `MacroCommand::Execute()` calls `Execute()` on each child. `MacroCommand::Unexecute()` calls `Unexecute()` on each child in reverse. This means macros can be stored in history and undone as a unit, exactly like atomic commands.

---

### Problem 7a → Iterator

**Design problem:** Traverse the Glyph structure to access elements without exposing whether the underlying storage is an array, linked list, or other structure.

**Solution:** Define an `Iterator` abstract class with `First()`, `Next()`, `IsDone()`, and `CurrentItem()` operations. Glyph subclasses override `CreateIterator()` to return the appropriate concrete iterator. `ArrayIterator` and `ListIterator` handle the data structure differences. `PreorderIterator` and `PostorderIterator` implement traversal strategies in terms of the structural iterators. Leaf glyphs return a `NullIterator` whose `IsDone()` always returns true.

**Key participants:**
- `Iterator` — abstract interface
- `ArrayIterator`, `ListIterator` — structure-specific iterators
- `PreorderIterator`, `PostorderIterator` — traversal-specific iterators
- `NullIterator` — for leaf glyphs
- `Glyph::CreateIterator()` — factory method returns the right iterator

**Why external iteration:** Putting traversal in Glyph would require adding `First()`, `Next()`, `IsDone()` to the Glyph interface, biasing it toward arrays. External iterators encapsulate traversal without modifying the traversed class hierarchy. Multiple concurrent traversals can run over the same structure — each iterator object holds its own traversal state.

---

### Problem 7b → Visitor

**Design problem:** Support multiple extensible analysis operations (spell check, hyphenation, word count, search) over the Glyph structure without adding operations to every Glyph subclass.

**Solution:** Define a `Visitor` abstract class with a `Visit` operation for each Glyph subclass: `VisitCharacter(Character*)`, `VisitRow(Row*)`, `VisitImage(Image*)`, etc. Add a single `Accept(Visitor&)` operation to `Glyph`. Each Glyph subclass implements `Accept` by calling the appropriate `Visit` method on the visitor, passing `this`. New analyses are new `Visitor` subclasses: `SpellingCheckingVisitor`, `HyphenationVisitor`, `WordCountVisitor`.

**Key participants:**
- `Visitor` — abstract visitor interface
- `SpellingCheckingVisitor`, `HyphenationVisitor` — Concrete Visitors
- `Glyph::Accept(Visitor&)` — the single dispatch hook added to Glyph
- `Character`, `Row`, `Image` — Visited elements (call the appropriate Visit method)

**Double dispatch:** `glyph->Accept(visitor)` causes a virtual call on Glyph that resolves to the correct subclass (e.g., `Character::Accept`). `Character::Accept` then calls `visitor.VisitCharacter(this)` — a second dispatch on the Visitor type. This double dispatch allows the analysis to specialize by both the element type and the visitor type without type casts.

**Interaction with Iterator:** A `PreorderIterator` traverses the Glyph structure. At each glyph, the analysis calls `glyph->Accept(spellingChecker)`. The Iterator provides *how to move*; the Visitor provides *what to do at each node*. Either can be changed independently.

**Visitor applicability constraint:** Visitor is most valuable when the class structure (Glyph hierarchy) is stable and the operations on it are expected to grow. If new Glyph subclasses are added frequently, every Visitor must be updated. For Lexi, new Glyph types are rare; new analyses (spell check, grammar check, word count) are common — Visitor is the right fit.

---

## Pattern Interaction Map (Summary from GoF Chapter 2)

The eight patterns applied to Lexi and how they relate:

```
                    ┌──────────────────────────────────────────────────────┐
                    │                   LEXI ARCHITECTURE                   │
                    └──────────────────────────────────────────────────────┘

  DOCUMENT REPRESENTATION                    PLATFORM ADAPTATION
  ┌───────────────────┐                     ┌────────────────────────────┐
  │    Composite      │                     │      Abstract Factory      │
  │  (Glyph tree:     │                     │  (GUIFactory creates       │
  │  Character, Row,  │                     │   platform widgets)        │
  │  Column, Page)    │                     └─────────────┬──────────────┘
  └────────┬──────────┘                                   │ creates WindowImp
           │ structure for                                 ▼
           │ traversal               ┌────────────────────────────────────┐
           ▼                        │           Bridge                    │
  ┌─────────────────────┐           │  (Window ↔ WindowImp)               │
  │     Strategy        │           │  Window: app abstraction            │
  │  (Compositor algo   │           │  WindowImp: OS implementation       │
  │   runs on Glyph     │           └────────────────────────────────────┘
  │   tree to produce   │
  │   Row/Column layout)│
  └─────────────────────┘           BEHAVIORAL
                                    ┌────────────────────────────────────┐
  EMBELLISHMENT                     │          Command                    │
  ┌─────────────────────┐           │  (MenuItem → Command → Execute)    │
  │     Decorator       │           │  History enables undo/redo         │
  │  (MonoGlyph:        │           └─────────────────┬──────────────────┘
  │   Border, Scroller  │                             │ uses
  │   wrap Composition) │                             ▼
  └─────────────────────┘           ┌────────────────────────────────────┐
                                    │   Composite (MacroCommand)          │
                                    │  Command list = undoable macro      │
                                    └────────────────────────────────────┘

  ANALYSIS
  ┌─────────────────────┐           ┌────────────────────────────────────┐
  │     Iterator        │ ────────► │          Visitor                   │
  │  (PreorderIterator  │  enables  │  (SpellingCheckingVisitor,         │
  │   traverses Glyph   │           │   HyphenationVisitor carry         │
  │   tree)             │           │   analysis over the structure)     │
  └─────────────────────┘           └────────────────────────────────────┘
```

### The Three Interaction Points Explained

**Interaction 1: Abstract Factory configures Bridge**

`WindowSystemFactory` is a concrete Abstract Factory. `Window`'s constructor calls:
```cpp
Window::Window() {
    _imp = windowSystemFactory->CreateWindowImp();
}
```
The Bridge (`Window` ↔ `WindowImp`) does not know which window system is in use. The Abstract Factory decides this at startup. Swapping the factory object changes the entire window system — without modifying a single Window class.

**Interaction 2: Command uses Composite**

`MacroCommand` inherits from `Command` and holds a `List<Command*>`:
```cpp
class MacroCommand : public Command {
    void Execute() override {
        for (each cmd in _commands) cmd->Execute();
    }
    void Unexecute() override {
        for (each cmd in reverse) cmd->Unexecute();
    }
    List<Command*> _commands;
};
```
The command history stores `MacroCommand` instances alongside atomic commands. Undo/redo works uniformly on both. No special-casing is needed for macros vs. individual commands.

**Interaction 3: Iterator enables Visitor**

The traversal and the analysis are strictly separated:
```cpp
// Traversal via Iterator
PreorderIterator i(composition);
// Analysis via Visitor
SpellingChecker spellingChecker;

for (i.First(); !i.IsDone(); i.Next()) {
    Glyph* g = i.CurrentItem();
    g->Accept(spellingChecker);  // Visitor double dispatch
}
```
Adding hyphenation analysis = new `HyphenationVisitor` subclass. Changing traversal order = different `Iterator` subclass. Neither change touches the Glyph hierarchy.

---

## Complete Extension Guide

| To add...                          | Implement...                        | Extend...          | Touch...        |
|------------------------------------|-------------------------------------|--------------------|-----------------|
| New formatting algorithm           | `TeXCompositor : Compositor`        | Nothing            | Nothing         |
| New UI embellishment               | `ShadowDecorator : MonoGlyph`       | Nothing            | Nothing         |
| New look-and-feel standard         | `MacFactory : GUIFactory` + products| Nothing            | Nothing         |
| New window system platform         | `WaylandWindowImp : WindowImp`      | `WindowSystemFactory` | Nothing     |
| New undoable operation             | `IndentCommand : Command`           | Nothing            | Nothing         |
| New macro (compound operation)     | `MacroCommand` + fill with Commands | Nothing            | Nothing         |
| New document analysis              | `WordCountVisitor : Visitor`        | Nothing            | `Glyph::Accept` (already done once) |
| New traversal order                | `PostorderIterator : Iterator`      | Nothing            | Nothing         |
| New glyph type (rare)              | `Table : Glyph`                     | All Visitor classes (add VisitTable) | Nothing |

The last row illustrates the Visitor trade-off: adding a new Glyph type requires updating every Visitor. This is acceptable when new analyses (new Visitors) are added far more frequently than new Glyph types. For Lexi, this is the correct assumption.

---

## GoF Chapter 2 Summary (verbatim list)

From page 80 of the source text — the eight patterns applied to Lexi:

1. **Composite (163)** to represent the document's physical structure
2. **Strategy (315)** to allow different formatting algorithms
3. **Decorator (175)** for embellishing the user interface
4. **Abstract Factory (87)** for supporting multiple look-and-feel standards
5. **Bridge (151)** to allow multiple windowing platforms
6. **Command (233)** for undoable user operations
7. **Iterator (257)** for accessing and traversing object structures
8. **Visitor (331)** for allowing an open-ended number of analytical capabilities without complicating the document structure's implementation

The GoF note: "None of these design issues is limited to document editing applications like Lexi. Indeed, most nontrivial applications will have occasion to use many of these patterns, though perhaps to do different things."
