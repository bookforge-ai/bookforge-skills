---
name: composite-pattern-implementor
description: |
  Implement the Composite pattern to compose objects into tree structures representing part-whole hierarchies, letting clients treat individual objects and compositions uniformly. Use when building file systems, UI component trees, organization charts, document structures, or any recursive containment hierarchy. Addresses 9 implementation concerns including the safety-vs-transparency trade-off for child management, parent references, component sharing, caching, and child ordering.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/composite-pattern-implementor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - structural-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [4]
    pages: [156-165, 43-48]
tags: [design-patterns, structural, gof, composite, tree, hierarchy, recursion, refactoring]
execution:
  tier: 2
  mode: full
  inputs:
    - type: code
      description: "Existing code that distinguishes between primitive and container objects with separate handling paths, or a description of a part-whole hierarchy to model"
  tools-required: [TodoWrite, Read]
  tools-optional: [Grep, Edit]
  mcps-required: []
  environment: "Any codebase. Language-agnostic — examples use Python but the pattern applies universally."
---

# Composite Pattern Implementor

## When to Use

You need to model a part-whole hierarchy where clients should be able to treat leaf objects and composite objects the same way — without type-checking or branching on "is this a container or a primitive?"

Apply this skill when:

- Code that operates on a structure must repeatedly ask "is this a single item or a group?" to decide what to do — **the primary code smell**
- You want to represent hierarchies like: file systems (files and directories), UI trees (widgets and panels), org charts (employees and departments), document structures (characters, rows, columns), or bill-of-materials (parts and assemblies)
- A recursive containment relationship exists: containers can hold other containers as well as primitives
- New kinds of components should be addable without changing client traversal code

**Two applicability conditions (from GoF):**
1. You want to represent part-whole hierarchies of objects
2. You want clients to be able to ignore the difference between compositions of objects and individual objects — clients will treat all objects in the composite structure uniformly

Before starting, confirm you are not looking for Decorator (which adds responsibilities to a single object, not a tree), or Iterator (which traverses but does not define the containment structure).

---

## Process

### Step 1: Set Up Tracking and Identify the Hierarchy

**ACTION:** Use `TodoWrite` to track progress, then identify the part-whole structure that needs to be modeled.

**WHY:** The shape of the hierarchy — how many levels deep, whether ordering matters, whether nodes can have multiple parents — governs all subsequent design decisions. Capturing this upfront prevents discovering structural constraints mid-implementation that force revisiting earlier steps.

```
TodoWrite:
- [ ] Step 1: Identify the hierarchy and characterize its nodes
- [ ] Step 2: Design the Component interface
- [ ] Step 3: Implement Leaf classes
- [ ] Step 4: Implement the Composite class
- [ ] Step 5: Make the safety-vs-transparency decision
- [ ] Step 6: Apply implementation concerns (parent refs, caching, ordering, deletion)
- [ ] Step 7: Validate the refactored structure
```

Document the hierarchy:

| Element | What to capture |
|---------|----------------|
| **Primitive nodes** | What are the leaf types? What operations do they perform? |
| **Container nodes** | What are the composite types? Do containers vary in type (e.g., Bus vs. Cabinet)? |
| **Shared operations** | Which operations must both leaves and composites support? |
| **Child ordering** | Does sequence matter (parse trees, rendered rows) or is it a set? |
| **Sharing** | Can a node appear under multiple parents? |
| **Depth** | Is the nesting depth bounded or unbounded? |

If working from a description rather than existing code, sketch the object tree showing two or three levels of nesting before writing any classes.

---

### Step 2: Design the Component Interface

**ACTION:** Define the abstract Component class — the common interface for both Leaf and Composite objects.

**WHY:** The Component interface is what enables uniform treatment. When all objects in the hierarchy share this interface, client code can invoke operations without knowing whether it holds a leaf or a composite. If the interface is too narrow, clients must downcast; if too wide, leaf implementations are burdened with operations that have no meaning for them. The goal is to maximize what can be defined here — every operation moved to Component is an operation clients never need to branch on.

**Design the interface by listing operations in two categories:**

| Category | Operations | Where declared |
|----------|-----------|----------------|
| **Domain operations** | `Draw()`, `NetPrice()`, `Render()`, `Execute()` — operations meaningful to every node | Component — always |
| **Child management** | `Add(Component)`, `Remove(Component)`, `GetChild(int)` — structural operations for composites | Component or Composite — see Step 5 |

**Maximizing the Component interface:** Some operations appear to belong only to Composites (e.g., accessing children). However, if you model a Leaf as a Component that *never has children*, you can define a default `GetChild()` on Component that returns nothing, and Composites override it to return their children. This keeps clients ignorant of the distinction. Do this for read-only structural operations. The add/remove write operations are more controversial — see Step 5.

```python
from abc import ABC, abstractmethod
from typing import Optional

class Component(ABC):
    """Abstract base for all nodes in the part-whole hierarchy."""

    @abstractmethod
    def operation(self) -> str:
        """Domain operation — implemented by every node."""
        ...

    def add(self, component: "Component") -> None:
        """Default: raise or no-op. Composite overrides."""
        raise NotImplementedError("Leaf components do not support add()")

    def remove(self, component: "Component") -> None:
        """Default: raise or no-op. Composite overrides."""
        raise NotImplementedError("Leaf components do not support remove()")

    def get_child(self, index: int) -> Optional["Component"]:
        """Default: return None. Composite overrides."""
        return None
```

---

### Step 3: Implement Leaf Classes

**ACTION:** Create one Leaf class per primitive node type. Each implements the domain operation(s) and does not override child management.

**WHY:** Leaves are the base cases of the recursive structure — they do actual work. They represent the primitives of the composition: `FloppyDisk`, `Character`, `Employee`, `File`. Keeping leaves simple is the key benefit: a client can hold a `Component` reference and call `operation()` without knowing it is a leaf.

```python
class Leaf(Component):
    """Represents a primitive object — has no children."""

    def __init__(self, name: str):
        self._name = name

    def operation(self) -> str:
        return f"Leaf({self._name})"
```

**In the Equipment hierarchy (GoF sample code):**

```python
class FloppyDisk(Component):
    """Leaf — a single hardware component with no subparts."""

    def __init__(self, name: str, wattage: int, price: float):
        self._name = name
        self._wattage = wattage
        self._price = price

    def net_price(self) -> float:
        return self._price   # Leaf's price is its own price — no summation needed

    def power(self) -> int:
        return self._wattage
```

---

### Step 4: Implement the Composite Class

**ACTION:** Create the Composite class that stores and manages child components, and implements domain operations by delegating to children recursively.

**WHY:** The Composite is where the recursive power of the pattern lives. It implements the same interface as Leaf but does so by iterating over children and aggregating their results. This means operations like `net_price()` on a Cabinet automatically sum up all nested components — no client code has to know the tree depth or structure.

```python
class CompositeComponent(Component):
    """A container node that can hold both Leaves and other Composites."""

    def __init__(self, name: str):
        self._name = name
        self._children: list[Component] = []

    def add(self, component: Component) -> None:
        self._children.append(component)

    def remove(self, component: Component) -> None:
        self._children.remove(component)

    def get_child(self, index: int) -> Optional[Component]:
        return self._children[index]

    def operation(self) -> str:
        results = [child.operation() for child in self._children]
        return f"Composite({self._name})[{', '.join(results)}]"
```

**Equipment hierarchy — Composite with aggregation (GoF sample code):**

```python
class CompositeEquipment(Component):
    """Base for equipment that contains sub-equipment."""

    def __init__(self, name: str):
        self._name = name
        self._equipment: list[Component] = []

    def add(self, component: Component) -> None:
        self._equipment.append(component)

    def remove(self, component: Component) -> None:
        self._equipment.remove(component)

    def net_price(self) -> float:
        """Sum the net prices of all sub-equipment recursively."""
        # WHY: recursive delegation means Cabinet.net_price() automatically
        # traverses the full tree — no client code needs to walk the structure.
        return sum(child.net_price() for child in self._equipment)

class Chassis(CompositeEquipment):
    """A chassis holds drives, buses, and cards."""
    def __init__(self, name: str):
        super().__init__(name)
        self._wattage = 0

    def net_price(self) -> float:
        return super().net_price()   # inherits summation from CompositeEquipment

class Cabinet(CompositeEquipment):
    """A cabinet holds chassis and other equipment."""
    pass

# Assembly:
cabinet = Cabinet("PC Cabinet")
chassis = Chassis("PC Chassis")
cabinet.add(chassis)

bus = CompositeEquipment("MCA Bus")
bus.add(FloppyDisk("Token Ring Card", wattage=4, price=29.99))
chassis.add(bus)
chassis.add(FloppyDisk("3.5in Floppy", wattage=5, price=19.99))

print(cabinet.net_price())  # Recursively sums all sub-equipment prices
```

---

### Step 5: Make the Safety-vs-Transparency Decision

**ACTION:** Decide where to declare child management operations (`add`, `remove`, `get_child`) — in Component (transparency) or only in Composite (safety). This is the central design decision of the Composite pattern.

**WHY:** This trade-off has no universally correct answer — it depends on what kind of errors your system must catch and at what point. Choosing transparency means clients never need to downcast or type-check, which is the core promise of the pattern. Choosing safety means misuse is caught at compile time, but clients that want to use the full Composite interface must check types at runtime. Consciously choose; do not let it default.

**The trade-off:**

| Option | What it gives you | What it costs you |
|--------|-------------------|-------------------|
| **Transparency** — declare `add`/`remove` in Component | Clients treat all components uniformly; no downcasting needed | Leaves inherit operations that are meaningless for them; `add()` on a Leaf must fail at runtime |
| **Safety** — declare `add`/`remove` only in Composite | Misuse caught at compile time (statically typed languages); Leaf interface is clean | Clients must downcast to `Composite` to manage children; uniformity breaks |

**GoF recommendation:** Emphasize transparency — declare child management in Component, implement defaults that fail at runtime. This preserves the pattern's central benefit.

**Implementing safe transparency with `get_composite()` (GoF idiom):**

If you choose safety but still want to avoid unsafe downcasts, add a `get_composite()` method to Component that returns `None` by default, and override it in Composite to return `self`. Clients use this to obtain the Composite interface safely:

```python
class Component(ABC):
    def get_composite(self) -> Optional["CompositeComponent"]:
        """Returns self if this component is a Composite, None otherwise."""
        return None   # Default: not a composite

class CompositeComponent(Component):
    def get_composite(self) -> Optional["CompositeComponent"]:
        return self   # Override: I am a composite

# Safe usage — no blind downcast:
if composite := component.get_composite():
    composite.add(new_leaf)
```

**When transparency raises on Leaf.add():** Make `add()` fail by raising an exception — not silently succeed. Silently ignoring `add()` on a leaf hides a bug (the caller believes the component was added). Raising makes misuse visible immediately.

---

### Step 6: Apply Remaining Implementation Concerns

**ACTION:** Evaluate each of the 9 implementation concerns and apply the relevant ones to your design.

**WHY:** The 9 concerns are not all mandatory — they are a checklist of decisions that frequently arise. Each one you skip is an implicit default that may cause problems later (e.g., not managing parent references will complicate deletion; not addressing ordering will produce incorrect tree traversal). Work through the list deliberately, even if the answer is "not applicable."

See `references/composite-implementation-guide.md` for full details on each concern.

**Checklist:**

| # | Concern | Decision to make |
|---|---------|-----------------|
| 1 | **Explicit parent references** | Does traversal upward (to parent) simplify your operations? If yes, add a `parent` field to Component and maintain it in `add()`/`remove()`. |
| 2 | **Sharing components** | Can a node appear under two parents? If yes, apply Flyweight — externalize mutable state so nodes do not need to know their parent. |
| 3 | **Maximizing the Component interface** | Have you moved as many operations to Component as reasonable (with sensible leaf defaults)? |
| 4 | **Safety vs. transparency** | Decided in Step 5. Confirm the choice is consistently applied. |
| 5 | **Child list storage** | Does every Composite have the same child storage structure? If Composites vary significantly, store the child list in each Composite subclass rather than a shared base. Watch the memory cost of putting a list in every Leaf. |
| 6 | **Child ordering** | Does the sequence of children matter (rendering order, parse tree structure)? If yes, use an ordered list and design `add()` to accept a position. Consider Iterator for traversal. |
| 7 | **Caching** | Are traversals expensive? Cache computed results (e.g., bounding boxes, aggregated prices) in Composite. Invalidate parent caches when a child changes — requires parent references (concern 1). |
| 8 | **Who deletes components** | In languages without garbage collection: Composite is responsible for deleting its children on destruction, except when Leaf objects are immutable and shared (Flyweight). |
| 9 | **Data structure for children** | Default is a list. Use a tree for sorted order, a hash table for fast lookup by key, or per-child named fields when the set of children is fixed and known. |

**Applying parent references (concern 1):**

```python
class Component(ABC):
    def __init__(self):
        self._parent: Optional["CompositeComponent"] = None

    @property
    def parent(self) -> Optional["CompositeComponent"]:
        return self._parent

class CompositeComponent(Component):
    def add(self, component: Component) -> None:
        self._children.append(component)
        component._parent = self    # maintain invariant: child's parent = this composite

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component._parent = None    # clear parent when removed
```

---

### Step 7: Validate the Refactored Structure

**ACTION:** Verify the implementation is complete and uniform treatment holds end-to-end.

**WHY:** The refactoring is only successful if client code that operated on leaves or composites separately can now use the Component interface uniformly, without branching on type. If any client still does `isinstance(node, Composite)` for anything other than the explicit `get_composite()` safety idiom, the pattern is incomplete.

**Validation checklist:**

- [ ] Client code uses only the `Component` interface for domain operations — no `isinstance` checks to decide which operation to call
- [ ] `operation()` (or equivalent domain method) produces correct results on a Leaf, a shallow Composite, and a deep nested Composite
- [ ] `add()` / `remove()` on a Leaf either raises a clear exception (safety) or fails with a meaningful error (transparency variant)
- [ ] Adding a new Leaf type requires only a new class implementing Component — no changes to existing Composites or client code
- [ ] Adding a new Composite type requires only a new class extending CompositeEquipment (or equivalent) — no changes to clients
- [ ] If caching was added (concern 7), modifying a child correctly invalidates the parent's cache
- [ ] If parent references were added (concern 1), the invariant holds: every child's `parent` points to its containing Composite

---

## Examples

### Example 1: File System Hierarchy

**Scenario:** A file system utility needs to calculate directory sizes. Currently, code special-cases directories vs. files with `isinstance` checks throughout the size calculation logic.

**Trigger:** "Every place we compute size or count files, we have to check whether we're dealing with a file or a directory."

**Before (type-branching code smell):**
```python
def get_size(node):
    if isinstance(node, File):
        return node.size
    elif isinstance(node, Directory):
        return sum(get_size(child) for child in node.children)
```

**After (Composite):**
```python
class FileSystemNode(ABC):
    @abstractmethod
    def size(self) -> int: ...
    def add(self, node: "FileSystemNode") -> None:
        raise NotImplementedError
    def get_children(self) -> list["FileSystemNode"]:
        return []

class File(FileSystemNode):
    def __init__(self, name: str, size_bytes: int):
        self._name = name
        self._size = size_bytes
    def size(self) -> int:
        return self._size

class Directory(FileSystemNode):
    def __init__(self, name: str):
        self._name = name
        self._children: list[FileSystemNode] = []
    def add(self, node: FileSystemNode) -> None:
        self._children.append(node)
    def get_children(self) -> list[FileSystemNode]:
        return self._children
    def size(self) -> int:
        return sum(child.size() for child in self._children)

# Client — no isinstance, no branching:
root = Directory("root")
root.add(File("readme.txt", 1024))
docs = Directory("docs")
docs.add(File("design.pdf", 204800))
root.add(docs)
print(root.size())  # 205824 — traverses entire tree automatically
```

**Output:** Client code calls `node.size()` uniformly. A new `SymbolicLink` type (a Leaf with a `size` pointing to its target) requires zero changes to directories or the size computation.

---

### Example 2: UI Component Tree (React-style)

**Scenario:** A server-side UI renderer builds HTML from a component tree. Panels hold other components; buttons, labels, and inputs are leaves. The renderer must call `render()` on the root and get complete HTML.

**Trigger:** "We're adding more container types (tabs, accordions) and the render function keeps growing with new `if isinstance(...)` branches."

**Design:**
```python
class UIComponent(ABC):
    @abstractmethod
    def render(self, indent: int = 0) -> str: ...
    def add(self, component: "UIComponent") -> None:
        raise NotImplementedError("Leaf UI components do not support add()")

class Button(UIComponent):
    def __init__(self, label: str):
        self._label = label
    def render(self, indent: int = 0) -> str:
        return " " * indent + f"<button>{self._label}</button>"

class Panel(UIComponent):
    def __init__(self, css_class: str):
        self._class = css_class
        self._children: list[UIComponent] = []
    def add(self, component: UIComponent) -> None:
        self._children.append(component)
    def render(self, indent: int = 0) -> str:
        inner = "\n".join(child.render(indent + 2) for child in self._children)
        return f'{" " * indent}<div class="{self._class}">\n{inner}\n{" " * indent}</div>'

# Assembly and rendering:
form = Panel("login-form")
form.add(Button("Sign In"))
form.add(Button("Cancel"))
page = Panel("page")
page.add(form)
print(page.render())  # Full recursive HTML, no type checks
```

**Output:** Adding a `TabContainer` composite or an `Input` leaf requires no changes to `render()` callers or existing components.

---

### Example 3: Lexi Document Structure (GoF Case Study)

**Scenario:** Lexi is a WYSIWYG document editor. Documents are built from graphical elements: characters, images, and lines at the leaf level; rows and columns as composites. Operations like `Draw()`, `Bounds()`, and `Intersects()` must work on any element regardless of complexity — a single character and a multi-column page are treated identically by the rendering engine.

**The Glyph hierarchy (GoF pages 43-48):**

```
Component:  Glyph     — Draw(Window), Bounds(Rect), Intersects(Point), Insert(Glyph, int), Remove(Glyph), Child(int), Parent()
Leaf:       Character — holds a char, draws via w->DrawCharacter(c)
Leaf:       Rectangle — draws via w->DrawRect(x0, y0, x1, y1)
Leaf:       Image     — holds a bitmap, draws to window
Composite:  Row       — arranges children left-to-right; Draw() iterates children, ensures each is positioned, calls c->Draw(w)
Composite:  Column    — arranges Row children vertically
```

**Key design decisions made in Lexi:**

1. **Transparency chosen:** `Insert()`, `Remove()`, and `Child()` are declared on `Glyph` (the Component), not just on `Row` (the Composite). Leaves do not override these — clients can always call them without type-checking.
2. **Parent references used:** `Glyph` declares `Parent()`. Every glyph stores a reference to its parent so the formatter can walk up the structure and so `Remove()` can detach a glyph from its container.
3. **Ordered children:** `Row` uses an ordered list for children — the sequence of characters defines the visual order on screen. `Insert(Glyph* g, int i)` inserts at a specific position.
4. **Operation maximization:** `Bounds()` is defined on all Glyphs, not just containers. A `Character`'s bounding box is its character cell; a `Row`'s bounding box is the union of its children's bounding boxes.

**Result:** The formatter, spell-checker, and renderer all hold `Glyph*` references and call `Draw()`, `Bounds()`, or `Intersects()` uniformly — whether the target is a single character or a nested multi-column structure, the code is identical.

---

## Key Principles

- **The pattern's value is uniform treatment** — if clients still branch on leaf-vs-composite for domain operations, the pattern has failed. Every `isinstance` check for operational dispatch is a sign the Component interface needs expansion.

- **Transparency is a deliberate choice, not a default** — declaring child management in Component trades compile-time safety for uniformity. Make this choice explicitly and document it. Do not let it happen because you copied a template.

- **Recursive delegation is the mechanism** — a Composite's `operation()` should almost always iterate over children and aggregate. The power of the pattern is that `cabinet.net_price()` correctly sums a deeply nested tree without the caller knowing the depth or structure.

- **Leaves must still handle child management calls gracefully** — whether by raising a clear exception (transparency + safety) or silently doing nothing (transparency only). Silent no-ops hide bugs; prefer raising with a message.

- **"Can make design overly general" is a real risk** — the pattern makes it easy to add any component anywhere in the tree. If you want a Composite to hold only certain types of children, Composite cannot enforce that constraint via the type system — you must add runtime checks. Acknowledge this limitation explicitly; it may mean Composite is the wrong choice when type constraints are essential. Always ask: "Should ANY child be addable to ANY composite, or do structural rules apply?" If rules apply, add validation in `add()` and document which child types each Composite accepts.

- **Use Iterator for traversal, Visitor for operations** — once you have a Composite tree, two companion patterns become relevant. Use **Iterator** when clients need to traverse the tree in different orders (preorder, postorder, breadth-first) without knowing the tree's internal structure. Use **Visitor** when you need to add new operations to the tree (validation, rendering, aggregation) without modifying the Component classes. Iterator + Visitor together are the standard way to operate on Composite structures — Iterator handles the "walk" and Visitor handles the "what to do at each node."

---

## References

| File | Contents |
|------|----------|
| `references/composite-implementation-guide.md` | All 9 implementation concerns with full rationale, language-specific notes, related patterns (Chain of Responsibility, Flyweight, Iterator, Visitor, Decorator), and the complete GoF consequences catalog |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-structural-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
