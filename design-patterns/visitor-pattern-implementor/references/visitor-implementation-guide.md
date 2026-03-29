# Visitor Pattern — Implementation Guide

> Reference for `visitor-pattern-implementor`. Read this when you need full consequences detail, participant role definitions, language-specific implementation notes, or the traversal placement decision tree.

---

## Participants and Their Roles

| Participant | Also called | Role |
|-------------|-------------|------|
| **Visitor** | NodeVisitor, DocumentVisitor, EquipmentVisitor | Declares one `Visit` operation per ConcreteElement class. The signature of each Visit operation encodes the concrete type. |
| **ConcreteVisitor** | TypeCheckingVisitor, SpellingCheckingVisitor, PricingVisitor | Implements each operation declared by Visitor. Provides the algorithm and carries accumulating state. Each ConcreteVisitor is a self-contained operation over the full structure. |
| **Element** | Node, Glyph, Equipment | Defines an `Accept` operation that takes a Visitor as an argument. |
| **ConcreteElement** | AssignmentNode, Character, FloppyDisk | Implements `Accept` by calling the matching `Visit` method on the visitor: `visitor.visit_assignment(self)`. |
| **ObjectStructure** | Program, DocumentStructure | Enumerates its elements. Provides a high-level interface to let visitors visit its elements. May be a Composite (see Composite pattern) or a simple collection. |

### Collaboration sequence

1. Client creates a ConcreteVisitor instance
2. Client calls `object_structure.accept(visitor)` (or starts traversal directly)
3. ObjectStructure iterates and calls `element.accept(visitor)` on each element
4. Each element calls the matching `visitor.visit_X(self)` back on the visitor (double-dispatch)
5. ConcreteVisitor executes the operation fragment for that element type, using the element's interface to access its state
6. After traversal: client retrieves accumulated results from the visitor

---

## Complete Consequences

### Benefits

**1. Easy to add new operations**
Adding a new operation over an object structure requires only defining a new ConcreteVisitor subclass. None of the element classes change. In contrast, if the operation were distributed across element classes, every element class would need modification.

**2. Related operations are gathered, unrelated ones separated**
All the behavior for one operation (e.g., pricing) lives in one class: `PricingVisitor`. The element classes stay clean — they only define structure. Algorithm-specific data structures are hidden inside the visitor.

**3. Visits across class hierarchies**
An Iterator requires all elements to share a common type (the iterator's type parameter). A Visitor imposes no such requirement — `VisitMyType` and `VisitYourType` can operate on completely unrelated classes. This makes Visitor useful when the structure contains elements that are not related by inheritance.

**4. State accumulation during traversal**
Visitors naturally carry state across a traversal as instance variables. Without Visitor, this state would need to be threaded through method parameters or stored globally.

### Liabilities

**5. Adding new ConcreteElement classes is hard**
Each new ConcreteElement subclass requires a new abstract `Visit` method in the Visitor interface, and a new concrete implementation in every ConcreteVisitor. In a codebase with many ConcreteVisitors, this is costly. This is the central trade-off: Visitor makes adding operations easy and adding element types hard.

**The key consideration (GoF, page 310):**
> "The key consideration in applying the Visitor pattern is whether you are mostly likely to change the algorithm applied over an object structure or the classes of objects that make up the structure. The Visitor class hierarchy can be difficult to maintain when new ConcreteElement classes are added frequently. In such cases, it's probably easier just to define operations on the classes that make up the structure. If the Element class hierarchy is stable, but you are continually adding operations or changing algorithms, then the Visitor pattern will help you manage the changes."

**6. Breaking encapsulation**
Visitor's approach assumes the ConcreteElement interface is powerful enough for visitors to do their job. This often forces elements to expose internal state through public accessors that would otherwise be private. Once those accessors exist, the element's internal representation becomes part of its public contract — harder to change later.

Mitigation: design element accessors deliberately. Only expose state that a well-defined visitor operation legitimately needs. Do not expose internal mutable state unnecessarily.

---

## Traversal Placement Decision Tree

```
Is traversal order the same for all operations?
├─ YES → Is the structure a Composite (tree)?
│        ├─ YES → Composite elements recurse in Accept (children first, then self)
│        └─ NO  → ObjectStructure drives a flat iteration
└─ NO  → Do different operations need different traversal orders?
         ├─ YES → Use external Iterator — each ConcreteVisitor picks its iterator
         └─ Is the traversal algorithm complex (irregular, result-dependent)?
                  ├─ YES → ConcreteVisitor controls its own traversal
                  └─ NO  → External Iterator is still cleanest
```

**Composite element traversal (preorder):**
```python
class CompositeElement(Element):
    def accept(self, visitor: Visitor) -> None:
        for child in self._children:
            child.accept(visitor)   # recurse first
        visitor.visit_composite(self)  # then self
```

**External iterator + visitor (maximum flexibility):**
```python
def apply_visitor(root: Element, visitor: Visitor, order: str = "preorder") -> None:
    iterator = PreorderIterator(root) if order == "preorder" else PostorderIterator(root)
    for element in iterator:
        element.accept(visitor)
```

**When the ConcreteVisitor controls traversal:**
The REMatchingVisitor example from GoF (pages 316-317) illustrates this: a `RepeatExpression` must repeatedly traverse its component. The visitor controls the traversal because the traversal algorithm depends on the intermediate match results — something only the visitor can know. This is the exception; prefer external traversal for most cases.

---

## Language-Specific Notes

### Python

Python's `isinstance`-based dispatch is sometimes used as a Visitor alternative (or anti-pattern). The problem the GoF note explicitly (page 76):

```python
# Anti-pattern: manual type dispatch in the visitor
def check(self, glyph):
    if isinstance(glyph, Character): ...
    elif isinstance(glyph, Row): ...
    elif isinstance(glyph, Image): ...
```

This is brittle — adding a new element type requires finding and updating every such `isinstance` chain. The `accept/visit` protocol eliminates this by letting the element announce its own type through method dispatch.

Python supports overloaded `visit` via `functools.singledispatchmethod`:

```python
from functools import singledispatchmethod

class PricingVisitor:
    @singledispatchmethod
    def visit(self, element):
        raise NotImplementedError(f"No visit handler for {type(element)}")

    @visit.register(FloppyDisk)
    def _(self, disk: FloppyDisk):
        self._total += disk.net_price()

    @visit.register(Chassis)
    def _(self, chassis: Chassis):
        self._total += chassis.discount_price()
```

This reduces boilerplate at the cost of slightly less explicit dispatch naming. The `accept` method in each element can then call `visitor.visit(self)` uniformly.

### Java

Java uses the accept/visit naming convention directly. Abstract classes or interfaces work for both Visitor and Element:

```java
public interface DocumentVisitor {
    void visitCharacter(Character character);
    void visitRow(Row row);
    void visitImage(Image image);
}

public class Character implements Element {
    @Override
    public void accept(DocumentVisitor visitor) {
        visitor.visitCharacter(this);
    }
}
```

Java's lack of default method implementations in abstract classes means ConcreteVisitor subclasses must implement all `visit` methods. Use an abstract adapter class with empty default implementations when ConcreteVisitors only care about a subset of element types.

### TypeScript

TypeScript supports both the pattern directly and a discriminated union approach:

```typescript
interface DocumentVisitor {
    visitCharacter(node: Character): void;
    visitRow(node: Row): void;
    visitImage(node: Image): void;
}

abstract class Element {
    abstract accept(visitor: DocumentVisitor): void;
}

class Character extends Element {
    constructor(public readonly charCode: string) { super(); }

    accept(visitor: DocumentVisitor): void {
        visitor.visitCharacter(this);
    }
}
```

For discriminated unions as an alternative (when the type set is truly closed and small), TypeScript's exhaustive `switch` on a `kind` field can replace the accept/visit protocol. This is simpler but loses the extensibility benefit — adding a new type requires updating every `switch`. Use Visitor when operations are added often; use discriminated unions when types are added often.

---

## Comparison with Related Patterns

### Visitor vs. Iterator

| Dimension | Iterator | Visitor |
|-----------|----------|---------|
| Purpose | Traverse a structure uniformly | Perform type-specific operations during traversal |
| Element type requirement | All elements must share a common type | Elements can be unrelated |
| Operation diversity | Single operation (advance, current) | Multiple operations via ConcreteVisitor subclasses |
| State accumulation | No (stateless traversal) | Yes (ConcreteVisitor carries state) |
| Extension axis | Add new traversal orders | Add new operations |

They are complementary: use Iterator for the traversal loop, Visitor for the per-element dispatch body.

### Visitor vs. Interpreter

The Interpreter pattern uses a hierarchy of expression classes, each implementing an `Interpret` method. Adding a new interpretation (e.g., pretty-printing) requires adding `PrettyPrint` to every expression class. Applying Visitor to an Interpreter structure externalizes each interpretation as a ConcreteVisitor, making it easy to add new interpretations without modifying expression classes.

GoF: "Visitor may be applied to do the interpretation." (page 317)

### Visitor vs. Composite

Visitor is typically used together with Composite. The Composite pattern defines the object structure (tree of elements). Visitor provides the mechanism to define operations over that structure without modifying element classes. The `CompositeElement::Accept` implementation that recurses over children and then calls `visitor.visit_composite(self)` is the standard integration point.

---

## Known Uses

- **Smalltalk-80 compiler:** `ProgramNodeEnumerator` — a Visitor class used primarily for algorithms that analyze source code
- **IRIS Inventor 3D toolkit:** Uses "actions" (visitors) for rendering, event handling, searching, filing, and determining bounding boxes over a scene graph hierarchy
- **Java compiler (javac):** Tree visitors (`com.sun.source.tree.TreeVisitor`) walk the AST for different compilation phases
- **Most IDE analysis tools:** Linters, type-checkers, and code formatters typically implement AST visitors over a stable grammar-defined node hierarchy
