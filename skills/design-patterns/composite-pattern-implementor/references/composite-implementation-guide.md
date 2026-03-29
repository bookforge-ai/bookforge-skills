# Composite Pattern — Implementation Guide

> Reference for `composite-pattern-implementor` SKILL.md.
> Source: GoF Design Patterns, pages 156–165 (Composite pattern) and pages 43–48 (Lexi Glyph case study).

---

## The 9 Implementation Concerns

These are the decisions that most frequently arise when implementing the Composite pattern. They are not sequential steps — they are a checklist to work through after the basic structure is in place.

---

### Concern 1: Explicit Parent References

**What it is:** Storing a back-reference from each child component to its parent Composite.

**Why you might want it:**
- Simplifies traversal *upward* in the structure (e.g., "find the nearest ancestor with property X")
- Required for the Chain of Responsibility pattern when used alongside Composite
- Makes deletion cleaner — a component can remove itself from its parent without the parent knowing

**The invariant to maintain:** Every child of a Composite must have that Composite as its parent. The invariant must hold at all times — not just after construction. The safest approach is to change a component's parent *only* in the `add()` and `remove()` operations of the Composite class:

```python
class CompositeComponent(Component):
    def add(self, component: Component) -> None:
        self._children.append(component)
        component._parent = self       # set parent when adding

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        component._parent = None       # clear parent when removing
```

If this logic lives in `CompositeEquipment` (a shared base for all Composites), all Composite subclasses inherit correct parent management automatically.

**When to skip it:** If your traversal is always top-down (root to leaves) and you never need to navigate upward or delete from within, parent references add memory and maintenance cost with no benefit.

---

### Concern 2: Sharing Components (Flyweight Integration)

**What it is:** Allowing a single component to appear as a child of more than one parent.

**Why it is difficult:** When a component has only one parent, parent references (Concern 1) work cleanly. When a component has multiple parents, propagating a request upward becomes ambiguous — which parent do you notify?

**The Flyweight solution:** Redesign the component so it holds no parent reference and externalizes mutable state. Components become intrinsic (shared, immutable) + extrinsic (contextual, passed at request time). Clients pass context (e.g., current position, current composite) as parameters rather than the component looking it up via `parent`.

```python
# Flyweight approach — no parent reference, context passed explicitly
class SharedGlyph:
    """Intrinsic state only — can be shared across multiple Row composites."""
    def __init__(self, char: str):
        self._char = char

    def draw(self, window, x: int, y: int) -> None:
        # x, y are extrinsic — passed by the Row that owns this position
        window.draw_character(self._char, x, y)
```

**When to use:** When memory reduction from sharing outweighs the complexity of externalizing context. Particularly valuable for large trees with repeated primitives (characters in a text document, identical icons in a UI).

---

### Concern 3: Maximizing the Component Interface

**What it is:** Defining as many operations as possible in the Component class so Leaf and Composite subclasses can be used interchangeably.

**The tension:** The Component interface should be wide enough that clients never need to downcast — but a class should only define operations meaningful to its subclasses. Leaf classes should not be burdened with child management operations they cannot meaningfully implement.

**Resolution strategy:** Ask "can this operation have a reasonable default implementation on a Leaf?" If yes, move it to Component.

| Operation | Leaf default | Composite override |
|-----------|-------------|-------------------|
| `get_child(i)` | Return `None` — leaf has no children | Return `_children[i]` |
| `get_children()` | Return `[]` — empty list | Return `_children` |
| `net_price()` | Return own price | Sum children's prices |
| `power()` | Return own wattage | Sum children's wattage |
| `add(c)` | Raise exception | Append to `_children` |
| `remove(c)` | Raise exception | Remove from `_children` |

**Child management is the exception:** `add()` and `remove()` have no sensible default for leaves. These are handled by the safety-vs-transparency decision (Concern 4).

---

### Concern 4: Declaring the Child Management Operations — Safety vs. Transparency

**This is the central design decision of the Composite pattern.**

#### Option A: Transparency — Declare in Component

Child management operations (`add`, `remove`, `get_child`) are declared in the `Component` abstract class.

**What you gain:** Clients can call these operations on any Component without knowing whether it is a Leaf or a Composite. This is the purest form of the pattern — uniform treatment extends to structural operations.

**What you pay:** Leaf classes inherit operations that have no meaning for them. The implementation must handle misuse at runtime (by raising exceptions or returning a null/empty result). There is no compile-time protection.

**Implementation for transparency:**
```python
class Component(ABC):
    def add(self, component: "Component") -> None:
        raise NotImplementedError(f"{type(self).__name__} does not support add()")

    def remove(self, component: "Component") -> None:
        raise NotImplementedError(f"{type(self).__name__} does not support remove()")

    def get_child(self, index: int) -> Optional["Component"]:
        return None
```

#### Option B: Safety — Declare Only in Composite

Child management is declared and implemented only in the `Composite` class (not on `Component`).

**What you gain:** The type system enforces correct usage. In a statically typed language, calling `add()` on a `Component` reference is a compile error.

**What you pay:** Clients cannot uniformly treat all components. Whenever they need to add or remove children, they must obtain a `Composite` reference, either via downcast or the `get_composite()` idiom.

**The `get_composite()` idiom (GoF page 160):** Avoids unsafe downcasting while retaining type safety.

```python
class Component(ABC):
    def get_composite(self) -> Optional["CompositeComponent"]:
        """Returns self if this is a Composite, None otherwise."""
        return None

class CompositeComponent(Component):
    def get_composite(self) -> Optional["CompositeComponent"]:
        return self   # I am a Composite

# Safe type-checked usage:
if composite := component.get_composite():
    composite.add(new_child)   # Only executes if component is actually a Composite
```

#### GoF recommendation

> "We have emphasized transparency over safety in this pattern."

Transparency is the default choice. Safety is appropriate when the cost of runtime leaf-manipulation errors is high and compile-time protection is worth the loss of uniformity.

---

### Concern 5: Should Component Implement a Child List?

**The question:** Should the child storage (the list/set/tree of children) live in the `Component` base class, or only in `Composite`?

**Putting it in Component:**
- Simplifies implementation — all classes inherit the storage
- Costs memory on every Leaf — a Leaf has no children but pays the overhead of an empty collection
- Worthwhile only if there are relatively few leaves in the structure

**Putting it in Composite (or a shared CompositeEquipment base):**
- Leaves pay no cost for storage they will never use
- Preferred when the structure contains many leaves
- Allows different Composite subtypes to use different storage structures

**Practical rule:** If Leaf objects are numerous and small (characters in a text document), keep child storage out of Component. If the tree is shallower with few leaves (an org chart, a UI widget tree), the convenience of shared storage in Component is acceptable.

---

### Concern 6: Child Ordering

**When it matters:** Any time the sequence of children affects the semantics of the operation. Examples:
- Rendering order (children drawn left-to-right define layout)
- Parse trees (compound statements have children ordered to reflect program sequence)
- Layered composites (z-order for UI stacking)

**Implementation:** Use an ordered list (`list` in Python, `std::vector` in C++). Design `add()` to accept an optional position parameter:

```python
def add(self, component: Component, position: int = -1) -> None:
    if position == -1:
        self._children.append(component)
    else:
        self._children.insert(position, component)
```

**Iterator integration:** When traversal order matters and is non-trivial, consider applying the Iterator pattern to encapsulate traversal logic. The Composite's `create_iterator()` factory method returns an iterator appropriate for its structure, keeping traversal policy separate from the containment structure.

---

### Concern 7: Caching to Improve Performance

**When to use:** When traversals are expensive and results can be validly cached between changes. Examples:
- Bounding box of a group of graphic objects (expensive to recompute if nothing moved)
- Net price of an equipment hierarchy (stable unless components are added or removed)
- Rendered HTML of a UI subtree (cacheable until a child changes)

**Implementation:** Store a cached value in the Composite, invalidated when any child changes.

```python
class CachedComposite(Component):
    def __init__(self, name: str):
        self._name = name
        self._children: list[Component] = []
        self._cached_price: Optional[float] = None   # None means cache is invalid

    def add(self, component: Component) -> None:
        self._children.append(component)
        self._invalidate_cache()

    def remove(self, component: Component) -> None:
        self._children.remove(component)
        self._invalidate_cache()

    def net_price(self) -> float:
        if self._cached_price is None:
            self._cached_price = sum(c.net_price() for c in self._children)
        return self._cached_price

    def _invalidate_cache(self) -> None:
        self._cached_price = None
        if self._parent:
            self._parent._invalidate_cache()   # propagate up — requires parent refs (Concern 1)
```

**Dependency on Concern 1:** Cache invalidation propagating up the tree requires parent references. If you need caching, you almost certainly also need parent references.

---

### Concern 8: Who Should Delete Components?

**Context:** In languages without garbage collection (C++, Rust), memory management must be explicit.

**Default rule:** Make the Composite responsible for deleting its children when it is destroyed. This prevents memory leaks when a Composite is removed from the tree.

**Exception:** When Leaf objects are immutable and shared (Flyweight, Concern 2), the Composite must *not* delete shared leaves — doing so would destroy objects still referenced by other parents.

**In garbage-collected languages (Python, Java, JavaScript):** This concern does not apply directly, but the equivalent is reference counting. If a Composite is the sole owner of its children, clearing the children list when the Composite is removed allows GC to reclaim the leaves.

---

### Concern 9: Best Data Structure for Storing Children

**Context:** The GoF default is a list (linked list in C++, array in practice). The right choice depends on the operations most frequently performed.

| Data structure | Best when | Trade-off |
|---------------|-----------|-----------|
| **List (ordered)** | Sequence matters; children often iterated in order | O(n) search and removal |
| **Array/vector** | Random access by index; children rarely inserted in middle | O(n) insertion at arbitrary position |
| **Hash table** | Children looked up by key (name, ID) | No inherent ordering |
| **Tree (sorted)** | Children must be maintained in sorted order | O(log n) insert/search, more complex |
| **Per-child named fields** | Set of children is fixed and known at design time (e.g., a binary tree node always has `left` and `right`) | Requires each Composite subclass to implement its own management interface |

**When named fields are preferred:** If you know a Composite always has exactly N children with semantic roles (e.g., a binary expression node has `left_operand` and `right_operand`), use named fields instead of a generic collection. This is more expressive, provides type-safe access, and eliminates iteration overhead. The trade-off is that each Composite subclass must define its own management interface. See the Interpreter pattern for an example of this approach.

---

## Consequences (Full Catalog)

From GoF pages 158–159:

**1. Defines class hierarchies consisting of primitive objects and composite objects.**
Primitive objects can be composed into more complex objects, which in turn can be composed, and so on recursively. Wherever client code expects a primitive object, it can also take a composite object.

**2. Makes the client simple.**
Clients can treat composite structures and individual objects uniformly. Clients normally don't know (and shouldn't care) whether they're dealing with a leaf or a composite. This simplifies client code, because it avoids having to write tag-and-case-statement-style functions over the classes that define the composition.

**3. Makes it easier to add new kinds of components.**
Newly defined Composite or Leaf subclasses work automatically with existing structures and client code. Clients don't have to be changed for new Component classes.

**4. Can make your design overly general.**
The disadvantage of making it easy to add new components is that it makes it harder to restrict the components of a composite. Sometimes you want a composite to have only certain components. With Composite, you can't rely on the type system to enforce those constraints for you. You'll have to use run-time checks instead.

---

## Related Patterns

| Pattern | Relationship to Composite |
|---------|--------------------------|
| **Chain of Responsibility** | The component-parent link is commonly used for Chain of Responsibility. A request propagates up the tree from child to parent. Requires parent references (Concern 1). |
| **Decorator** | Often used with Composite. When Decorators and Composites are used together, they share a common Component class. Decorators must support the Component interface with `Add`, `Remove`, `GetChild`. |
| **Flyweight** | Lets you share components, but they can no longer refer to their parents. Applicable when memory reduction from sharing outweighs the need for parent navigation. |
| **Iterator** | Can be used to traverse composites. Particularly useful when child ordering is significant and traversal policy should be decoupled from the containment structure. |
| **Visitor** | Localizes operations and behavior that would otherwise be distributed across Composite and Leaf classes. Use when you need to add operations to the hierarchy without modifying each class. |

---

## Language-Specific Notes

### Python
- Use `ABC` and `@abstractmethod` for Component
- `Optional["ClassName"]` for forward references and nullable parent/child types
- List comprehensions make recursive `operation()` implementations concise: `sum(c.net_price() for c in self._children)`
- No manual memory management — Concern 8 is handled by the garbage collector

### Java / C#
- Component as an abstract class or interface
- Java: `List<Component>` as child storage; `Optional<Component>` for nullable returns
- C#: `IComponent` interface pattern common; use `IEnumerable<IComponent>` for children
- Safety option is more natural — `instanceof` (Java) / `is` (C#) checks are common and idiomatic

### C++ (GoF original)
- Component as an abstract base class with pure virtual methods
- Child storage in `CompositeEquipment` using `std::list<Equipment*>` (`_equipment` member)
- Manual memory management applies: Composite destructor deletes children (Concern 8)
- `dynamic_cast` available as alternative to `GetComposite()` idiom for safety approach
- `CreateIterator()` factory method in Component returns `NullIterator` by default (leaves), `ListIterator` in Composite
