---
name: visitor-pattern-implementor
description: |
  Implement the Visitor pattern to define new operations on an object structure without changing the classes of the elements it operates on. Use when you have a stable class hierarchy but frequently add new operations, when many unrelated operations need to be performed on an object structure, or when you want to accumulate state across a traversal. Includes the critical stability decision rule, double-dispatch mechanism (Accept/Visit), Iterator integration for traversal, and the encapsulation trade-off warning.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/visitor-pattern-implementor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - behavioral-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [5]
    pages: [70-80, 306-318]
tags: [design-patterns, behavioral, gof, visitor, double-dispatch, iterator, traversal, object-structure]
execution:
  tier: 2
  mode: full
  inputs:
    - type: code
      description: "Existing code with a stable element class hierarchy needing multiple new operations, or a description of the object structure and the operations to add"
  tools-required: [TodoWrite, Read]
  tools-optional: [Grep, Edit]
  mcps-required: []
  environment: "Any codebase. Language-agnostic — examples use Python but the pattern applies universally."
---

# Visitor Pattern Implementor

## When to Use

You have an object structure (a hierarchy of related element classes) and need to perform operations on those objects without modifying the element classes themselves. This skill applies when:

- **The element class hierarchy is stable** — it rarely gains new subclasses, but you frequently need to add new operations over the structure. This is the **stability decision rule**: if the hierarchy changes often, do not use Visitor.
- **Many distinct and unrelated operations** need to be performed on the same object structure, and you want to avoid polluting element classes with those operations.
- **State must accumulate across a traversal** — the operation builds up a result by visiting multiple elements in sequence (e.g., collecting all misspellings, computing a total price).
- The object structure is shared across multiple applications and you want each application to add only its own operations, not affect shared element code.

**The go/no-go decision before proceeding:**

| Element hierarchy stability | Operation change frequency | Verdict |
|-----------------------------|---------------------------|---------|
| Stable (rare new elements)  | High (many new operations) | Use Visitor |
| Unstable (frequent new elements) | Any | Avoid Visitor — each new element requires adding an abstract `Visit` method to every Visitor and implementing it in every ConcreteVisitor |
| Stable | Low (1-2 operations total) | Consider simpler approach — Visitor may be over-engineering |

If the hierarchy is unstable, it is easier to define the operation in the element classes directly. If you use Visitor anyway, every new element type forces a cascade of changes through all existing Visitor classes — exactly the problem Visitor was meant to solve in the other direction.

Before starting, confirm this is not better handled by:
- **Iterator alone** — if the operation is simple and all elements are the same type, an Iterator may suffice
- **Template Method** — if the operation structure is fixed and only small steps vary per element type

---

## Process

### Step 1: Set Up Tracking and Apply the Stability Test

**ACTION:** Use `TodoWrite` to track progress, then evaluate whether Visitor is the right pattern.

**WHY:** The stability test is the most critical decision in the entire workflow. Applying Visitor to an unstable hierarchy produces a brittle system — every new element class requires modifying the abstract Visitor interface and all ConcreteVisitor classes. This is a worse maintenance burden than the original problem. Confirming stability first prevents committing to the wrong pattern.

```
TodoWrite:
- [ ] Step 1: Apply stability test and confirm Visitor is appropriate
- [ ] Step 2: Define the Visitor interface
- [ ] Step 3: Add Accept methods to element classes
- [ ] Step 4: Implement ConcreteVisitor classes
- [ ] Step 5: Implement traversal (ObjectStructure or Iterator)
- [ ] Step 6: Wire up the client and validate
```

Document the element hierarchy:

| Element | How often new subclasses are added | Operations needed now | Planned future operations |
|---------|-----------------------------------|----------------------|--------------------------|
| (list each concrete element class) | rarely / sometimes / often | N | estimate |

If "often" appears in column 2, stop and use `behavioral-pattern-selector` to reconsider.

---

### Step 2: Define the Visitor Interface

**ACTION:** Create an abstract Visitor class (or interface) that declares one `Visit` method for every ConcreteElement class in the structure.

**WHY:** The Visitor interface is the contract that lets each ConcreteElement call back to the visitor with its concrete type. Having a separate `Visit` method per element type — rather than a single generic method — allows the visitor to access element-specific state through each element's own interface without type checks or casts. The operation's name encodes the element type it operates on, making the code self-documenting and enabling compiler-enforced completeness.

```python
# Abstract Visitor — one Visit method per ConcreteElement
class DocumentVisitor:
    def visit_character(self, character: "Character") -> None:
        """Called when a Character element accepts this visitor."""
        pass  # Default: do nothing (allows selective override)

    def visit_row(self, row: "Row") -> None:
        pass

    def visit_image(self, image: "Image") -> None:
        pass
```

**Design decisions for the Visitor interface:**

| Decision | Options | Guidance |
|----------|---------|---------|
| **Default implementations** | Empty default vs. abstract (forced override) | Empty defaults allow ConcreteVisitors to handle only the elements they care about, reducing boilerplate |
| **Method naming** | `visit_character` vs. overloaded `visit(character)` | Distinct names are clearer in languages without overloading; overloading reduces noise in languages that support it well |
| **Return value** | void vs. typed return | Void with accumulated state in the visitor is simpler; typed returns work if each visit produces an independent result |

---

### Step 3: Add Accept Methods to Element Classes

**ACTION:** Add an `Accept(visitor)` method to the abstract Element class and implement it in each ConcreteElement.

**WHY:** This is where double-dispatch is achieved. In single-dispatch languages (Python, Java, C++), when you call `element.Accept(visitor)`, only `element`'s type is used to select the method. Inside `Accept`, when the element calls `visitor.visit_character(self)`, now *both* the visitor's type and the element's concrete type determine which `Visit` implementation runs. This two-step dispatch is the mechanism that lets a single `Accept(visitor)` call route to the right combination of visitor-and-element behavior — without any `isinstance` checks or casts.

The pattern for every ConcreteElement is identical:

```python
class Element:
    """Abstract base — declares the Accept protocol."""
    def accept(self, visitor: DocumentVisitor) -> None:
        raise NotImplementedError

class Character(Element):
    def __init__(self, char_code: str):
        self._char_code = char_code

    def get_char_code(self) -> str:
        return self._char_code

    def accept(self, visitor: DocumentVisitor) -> None:
        # Double-dispatch: calls the Visit method specific to Character
        visitor.visit_character(self)

class Row(Element):
    def __init__(self):
        self._children: list[Element] = []

    def add(self, element: Element) -> None:
        self._children.append(element)

    def get_children(self) -> list[Element]:
        return self._children

    def accept(self, visitor: DocumentVisitor) -> None:
        visitor.visit_row(self)

class Image(Element):
    def accept(self, visitor: DocumentVisitor) -> None:
        visitor.visit_image(self)
```

**The double-dispatch mechanism step by step:**

1. Client calls `element.accept(visitor)` — dispatch 1: resolved by `element`'s concrete type
2. Inside `Character.accept`, calls `visitor.visit_character(self)` — dispatch 2: resolved by `visitor`'s concrete type
3. The specific `Visit` body that runs depends on **both** the element type AND the visitor type

This is the key to adding new operations: adding a new `ConcreteVisitor` subclass provides a new set of `Visit` implementations without touching any element class.

**Encapsulation warning:** For the visitor to do its work, element classes must expose the state the visitor needs through public accessors (e.g., `get_char_code()`). If elements keep their state private with no accessors, the visitor pattern forces you to add those accessors — potentially breaking encapsulation. Evaluate which internal state each planned visitor operation needs, and add only those accessors. This is the main liability of the pattern.

---

### Step 4: Implement ConcreteVisitor Classes

**ACTION:** For each distinct operation, create a ConcreteVisitor class that implements the Visitor interface and defines what to do for each element type.

**WHY:** Each ConcreteVisitor encapsulates one complete operation over the entire object structure. Gathering all per-element logic for a single operation in one class keeps the algorithm coherent — you can read `SpellingCheckingVisitor` and understand the entire spelling algorithm in one place. This contrasts with distributing the logic across element classes, where the algorithm for a single operation is split across every element class and difficult to follow. The visitor also carries its own state (e.g., the accumulated list of misspellings), which would otherwise require global state or awkward parameter-passing.

```python
class SpellingCheckingVisitor(DocumentVisitor):
    """Accumulates misspelled words during traversal."""

    def __init__(self):
        self._current_word: list[str] = []
        self._misspellings: list[str] = []

    def visit_character(self, character: "Character") -> None:
        ch = character.get_char_code()
        if ch.isalpha():
            self._current_word.append(ch)
        else:
            # Non-alphabetic character terminates a word — check it
            word = "".join(self._current_word)
            if word and self._is_misspelled(word):
                self._misspellings.append(word)
            self._current_word = []

    def visit_row(self, row: "Row") -> None:
        pass  # Rows have no direct spelling content — children handled by traversal

    def visit_image(self, image: "Image") -> None:
        pass  # Images are not text — skip

    def get_misspellings(self) -> list[str]:
        return list(self._misspellings)

    def _is_misspelled(self, word: str) -> bool:
        # Plug in actual dictionary lookup here
        return False


class HyphenationVisitor(DocumentVisitor):
    """Inserts discretionary hyphens into the document structure."""

    def visit_character(self, character: "Character") -> None:
        ch = character.get_char_code()
        if ch.isalpha():
            # Accumulate word characters; when complete, apply hyphenation algorithm
            # and insert Discretionary glyphs at computed break points
            pass

    def visit_row(self, row: "Row") -> None:
        pass

    def visit_image(self, image: "Image") -> None:
        pass
```

**State management in ConcreteVisitors:**

- State that accumulates across the traversal (word buffer, running total, inventory count) lives as instance variables on the visitor — this is the designed purpose of ConcreteVisitor state
- State should be reset between traversals if the same visitor instance is reused
- Algorithm-specific data structures that would pollute element classes are natural residents in the ConcreteVisitor

---

### Step 5: Implement Traversal

**ACTION:** Decide who is responsible for traversal — the ObjectStructure, the elements themselves (composite recursion), or an external Iterator — and implement accordingly.

**WHY:** Traversal must be separated from the visit action because different operations often require the same traversal order, and you want to reuse the traversal without duplicating it. The three options have different trade-offs for flexibility, reuse, and coupling.

**Traversal option 1 — ObjectStructure drives iteration (simplest for collections):**

```python
class DocumentStructure:
    """Owns and iterates the element collection."""

    def __init__(self):
        self._elements: list[Element] = []

    def add(self, element: Element) -> None:
        self._elements.append(element)

    def accept(self, visitor: DocumentVisitor) -> None:
        for element in self._elements:
            element.accept(visitor)
```

**Traversal option 2 — Composite elements recurse (natural for tree structures):**

```python
class Row(Element):
    def accept(self, visitor: DocumentVisitor) -> None:
        # Visit children first (preorder: swap order for postorder)
        for child in self._children:
            child.accept(visitor)
        # Then visit self
        visitor.visit_row(self)
```

**Traversal option 3 — External Iterator (maximum flexibility, required when traversal order varies per operation):**

```python
# Using an Iterator to drive traversal externally
# Allows different visitors to use different traversal orders on the same structure
def traverse_with_visitor(root: Element, visitor: DocumentVisitor) -> None:
    iterator = PreorderIterator(root)
    for element in iterator:
        element.accept(visitor)
```

**Iterator integration — why it complements Visitor:**

An Iterator traverses a structure but cannot distinguish between element types. A Visitor distinguishes between element types but needs a mechanism to visit them all. The combination — Iterator for traversal order, Visitor for per-type behavior — separates two independent concerns cleanly. The Lexi case study (GoF pages 70-80) demonstrates this: a `PreorderIterator` walks the glyph structure, and a `SpellingCheckingVisitor` is passed to each glyph via `CheckMe`/`Accept` as the iterator advances.

**Choose traversal placement:**

| Situation | Recommended traversal placement |
|-----------|--------------------------------|
| Structure is a flat collection (list, set) | ObjectStructure drives iteration |
| Structure is a tree (Composite pattern) | Elements recurse in `Accept` |
| Traversal order varies by operation | External Iterator |
| Traversal algorithm is complex (irregular, depends on intermediate results) | ConcreteVisitor controls its own traversal |

---

### Step 6: Wire Up the Client and Validate

**ACTION:** Write client code that creates a ConcreteVisitor, passes it to the ObjectStructure's `Accept` method, and retrieves results. Then validate the implementation.

**WHY:** The client is the proof of the pattern's value. The client creates a visitor and passes it into the structure — it never needs to change when new visitor types are added. Validating this "closed to modification" property confirms the implementation is correct.

```python
# Client usage — adding a new operation (spelling check) without modifying element classes
structure = DocumentStructure()
structure.add(Character("a"))
structure.add(Character("l"))
structure.add(Character("u"))
structure.add(Character("_"))   # underscore terminates "alu" — not a word
structure.add(Character("m"))

spelling_visitor = SpellingCheckingVisitor()
structure.accept(spelling_visitor)
misspellings = spelling_visitor.get_misspellings()

# Later: add hyphenation — zero changes to Document, Character, Row, Image
hyphenation_visitor = HyphenationVisitor()
structure.accept(hyphenation_visitor)
```

**Validation checklist:**

- [ ] No element class was modified to add the new operation
- [ ] Each `Accept` method calls exactly the matching `Visit` method (`visitor.visit_character(self)` in `Character`, etc.) — not a generic method
- [ ] The ConcreteVisitor accumulates all state it needs without accessing global variables
- [ ] The traversal visits all elements in the structure (no elements skipped unless intentional)
- [ ] Adding a second ConcreteVisitor requires zero changes to element classes
- [ ] If a new ConcreteElement were added, you can enumerate all Visitor classes that would need updating — and confirm this list is acceptably small

---

## Examples

### Example 1: Lexi Document Editor (GoF Case Study — Spelling + Hyphenation)

**Scenario:** Lexi is a document editor representing text as a hierarchy of Glyph objects (Character, Row, Image, etc.). The Glyph class hierarchy is stable — it changes infrequently because it represents the document model. But new analytical capabilities are added often: spelling checking, hyphenation, word count, forward search, grammar checking.

**Trigger:** "We need to add spelling checking and hyphenation to Lexi without wiring these algorithms into the Glyph class hierarchy, and we want to add more analyses in the future."

**Stability assessment:** Glyph hierarchy is stable (Character, Row, Image, Discretionary — defined by the language model). Operations are frequent and varied. Visitor is appropriate.

**Design:**

```
Abstract:     Visitor          — VisitCharacter, VisitRow, VisitImage
Concrete A:   SpellingCheckingVisitor — accumulates _currentWord, checks IsMisspelled
Concrete B:   HyphenationVisitor      — assembles words, inserts Discretionary glyphs
Elements:     Glyph hierarchy — each subclass has Accept(Visitor&)
Traversal:    PreorderIterator drives Accept calls glyph-by-glyph
```

**Double-dispatch in action:**

1. Iterator reaches a `Character` glyph
2. `character.accept(visitor)` → dispatch 1: Character's Accept executes
3. Inside `Character::Accept`: `visitor.visit_character(this)` → dispatch 2: SpellingCheckingVisitor's `VisitCharacter` executes
4. `SpellingCheckingVisitor::VisitCharacter` calls `character.get_char_code()` to get the character — this is the element-specific accessor the visitor uses

**Output:** SpellingCheckingVisitor produces `get_misspellings()`. HyphenationVisitor modifies the document structure in-place. Neither operation touched any Glyph class. Adding `WordCountVisitor` is one new class — no other code changes.

---

### Example 2: Abstract Syntax Tree Compiler (GoF Motivation)

**Scenario:** A compiler represents programs as an abstract syntax tree (AST) with node classes: `AssignmentNode`, `VariableRefNode`, `LiteralNode`, `BinaryOpNode`. The node classes are fixed by the grammar. Operations needed: type-checking, code generation, pretty-printing, flow analysis, constant folding. These are added as the compiler evolves.

**Trigger:** "TypeCheck, GenerateCode, and PrettyPrint are methods on every AST node class. Adding flow analysis means touching 12 node classes again."

**Stability assessment:** AST nodes are stable (defined by the grammar; grammar rarely changes for a given language). Compiler passes are frequent. Visitor is well-suited.

**Before (the problem — operations distributed across node classes):**
```
AssignmentNode: TypeCheck(), GenerateCode(), PrettyPrint()
VariableRefNode: TypeCheck(), GenerateCode(), PrettyPrint()
```

**After (Visitor — operations centralized in visitor classes):**
```python
class NodeVisitor:
    def visit_assignment(self, node: "AssignmentNode") -> None: pass
    def visit_variable_ref(self, node: "VariableRefNode") -> None: pass
    def visit_literal(self, node: "LiteralNode") -> None: pass

class TypeCheckingVisitor(NodeVisitor):
    def visit_assignment(self, node): ...   # type-check assignment
    def visit_variable_ref(self, node): ... # verify variable is declared
    def visit_literal(self, node): ...      # validate literal type

class CodeGeneratingVisitor(NodeVisitor):
    def visit_assignment(self, node): ...
    def visit_variable_ref(self, node): ...
    def visit_literal(self, node): ...

class AssignmentNode:
    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_assignment(self)

class VariableRefNode:
    def accept(self, visitor: NodeVisitor) -> None:
        visitor.visit_variable_ref(self)
```

**Output:** Adding `FlowAnalysisVisitor` is one new class. `AssignmentNode` and `VariableRefNode` are never modified. Each compiler pass is readable as a coherent whole in its own class.

---

### Example 3: Equipment Pricing and Inventory (GoF Sample Code)

**Scenario:** A hardware product catalog uses a Composite structure: `Chassis` (composite) contains `FloppyDisk`, `Card`, `Bus` (leaves). Two unrelated operations need to run over the structure: compute total price and compute inventory count.

**Trigger:** "We need both `GetTotalPrice()` and `GetInventory()` on the equipment structure, and the equipment class hierarchy is finished — we don't want to add more methods to it."

**Design:**

```python
class EquipmentVisitor:
    def visit_floppy_disk(self, disk: "FloppyDisk") -> None: pass
    def visit_card(self, card: "Card") -> None: pass
    def visit_chassis(self, chassis: "Chassis") -> None: pass
    def visit_bus(self, bus: "Bus") -> None: pass

class PricingVisitor(EquipmentVisitor):
    def __init__(self): self._total = 0.0

    def visit_floppy_disk(self, disk):
        self._total += disk.net_price()     # leaf: net price

    def visit_chassis(self, chassis):
        self._total += chassis.discount_price()  # composite: discounted

    def get_total_price(self) -> float:
        return self._total

class InventoryVisitor(EquipmentVisitor):
    def __init__(self): self._inventory: list = []

    def visit_floppy_disk(self, disk):
        self._inventory.append(disk)

    def visit_chassis(self, chassis):
        self._inventory.append(chassis)

    def get_inventory(self) -> list:
        return self._inventory

# Chassis traverses children before visiting itself (composite Accept)
class Chassis(Equipment):
    def accept(self, visitor: EquipmentVisitor) -> None:
        for part in self._parts:
            part.accept(visitor)
        visitor.visit_chassis(self)  # visit self after children
```

**State accumulation:** `PricingVisitor._total` and `InventoryVisitor._inventory` grow as the traversal proceeds. Without the Visitor pattern, this state would need to be passed as parameters through every element's pricing method or stored as globals — the Visitor makes it a natural instance variable.

**Output:** Running `component.accept(PricingVisitor())` produces the total cost. Running `component.accept(InventoryVisitor())` produces the component list. Equipment classes were not modified.

---

## Key Principles

- **Stability test is a prerequisite, not a suggestion** — applying Visitor to an unstable hierarchy creates a maintenance cascade. Every new element type requires a new abstract method in `Visitor` and a new implementation in every `ConcreteVisitor`. If this will happen often, the pattern costs more than it saves.

- **Double-dispatch is the mechanism, not a coincidence** — the two-step `Accept` → `Visit` call is intentional. Without it, single-dispatch languages would route all elements to the same `Visit` method, requiring type checks. The `Accept` method in each ConcreteElement is boilerplate by design: it exists solely to tell the visitor the element's concrete type.

- **ConcreteVisitor state is accumulation, not side-effect leakage** — the Visitor pattern is specifically designed to carry state across a traversal. Use visitor instance variables freely for this purpose. Each traversal run should get a fresh visitor instance (or reset the visitor's state) to avoid contamination between runs.

- **Encapsulation is explicitly traded for extensibility** — the Visitor pattern assumes element interfaces are powerful enough for visitors to do their work. If elements are too encapsulated, visitors cannot access what they need. The design obligation is to expose element state through well-defined accessors, accepting that internal state becomes part of the public contract.

- **Iterator + Visitor is a natural pairing** — Iterator solves "how to traverse" (order, data structure independence), Visitor solves "what to do at each element" (type-specific behavior). The two patterns are complementary, not competing. Use Iterator for the traversal loop, Visitor for the per-element dispatch.

- **Adding a new ConcreteVisitor is free; adding a new ConcreteElement is expensive** — this asymmetry is the fundamental trade-off. Design the element hierarchy to completion before adopting Visitor. If the hierarchy grows regularly, the cost of updating all existing Visitors may outweigh the benefit.

---

## Reference Files

| File | When to read |
|------|-------------|
| `references/visitor-implementation-guide.md` | Participants reference, full consequences catalog, language-specific notes (Java, TypeScript, Python), traversal placement decision tree, comparison with Interpreter pattern |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-behavioral-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
