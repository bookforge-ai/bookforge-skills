# Decorator Pattern — Implementation Guide

Deep reference for `decorator-pattern-implementor`. Read this file when you need:
- The full participants catalog with responsibility descriptions
- The 5-phase transparent enclosure reasoning process
- Consequences analysis (benefits and liabilities)
- Guidance on omitting the abstract Decorator class
- Decorator vs. Strategy (skin vs. guts) distinction
- Language-specific implementation notes

---

## Participants

| Role | GoF Name | Lexi Name | Responsibility |
|------|----------|-----------|---------------|
| Component | `Component` | `Glyph` / `VisualComponent` | Defines the interface for objects that can have responsibilities added dynamically. Kept lightweight — no data representation. |
| ConcreteComponent | `ConcreteComponent` | `TextView`, `Composition` | The real object to which additional responsibilities are attached. Implements Component. Holds data. |
| Decorator (abstract) | `Decorator` | `MonoGlyph` / `Decorator` | Implements Component interface. Holds a reference to a Component. Default behavior: forward all operations to the wrapped component. |
| ConcreteDecorator | `ConcreteDecoratorA/B` | `Border`, `Scroller`, `BorderDecorator`, `ScrollDecorator` | Subclasses Decorator. Overrides one or more operations to add behavior before or after forwarding. May add state (e.g., `_border_width`, `_scroll_position`). |

---

## The 5-Phase Transparent Enclosure Reasoning Process

This is the mental sequence for deciding whether and how to apply Decorator. Work through each phase before writing any code.

### Phase 1: Rule Out Inheritance

Ask: "Can I achieve what I need with a subclass?"

Inheritance fails when:
- The number of combinations is combinatorial (N independent behaviors → 2^N subclasses)
- The responsibility needs to be added at runtime, not at class definition time
- The responsibility needs to be *withdrawn* at runtime (you cannot un-inherit)
- You do not own or cannot modify the class hierarchy
- You need to add the *same* responsibility twice (e.g., double border) — you cannot inherit from a class twice

If inheritance is adequate (single static addition, always present), stop here — use it. Decorator adds structural complexity that inheritance avoids.

### Phase 2: Choose the Composition Direction

When you decide to use composition (object containing another object), two directions are possible:

**Direction A: Embellishment contains the component** (Decorator direction)
- The border object holds a reference to the text view.
- The border "knows" about the component; the component does not know about the border.
- Border-drawing code stays entirely inside the Border class.
- Component classes remain untouched.

**Direction B: Component contains the embellishment**
- The text view holds a reference to a border object.
- The component must be modified to be aware of the embellishment.
- Adding a new embellishment type requires modifying the component class.

Direction A is the Decorator pattern. Direction B is not — it requires modifying the component, coupling it to the embellishment. Always prefer Direction A when the goal is to keep the component class unaware of and unmodified by its embellishments.

### Phase 3: Establish Interface Conformance

Decide: what interface must both the real component and all decorators share?

This is the "compatible interfaces" half of transparent enclosure. The reason for requiring interface compatibility is client transparency: if a `Border` has a `Draw(Window*)` method and `TextView` also has a `Draw(Window*)` method, and both are `Glyph` subclasses, then clients that call `glyph->Draw(w)` work identically whether `glyph` is a plain `TextView` or a `Border` wrapping a `Scroller` wrapping a `TextView`. The chain is invisible.

Check: Does the Component interface cover *all* operations clients will call? If a client calls an operation that exists only on the ConcreteComponent (not the Component interface), the decorator chain breaks transparency for that operation.

### Phase 4: Define the Abstract Decorator Base

Create the `Decorator` class that implements the Component interface and holds the `_component` reference. Implement every interface operation as a pure forwarding call.

This class exists for two reasons:
1. It makes the chain structurally sound — a Decorator can wrap another Decorator because both implement Component.
2. It provides the default forwarding behavior — ConcreteDecorators only override operations they augment, not the entire interface.

**When to omit this base class:** If you are adding exactly one responsibility and will never add a second ConcreteDecorator, the abstract Decorator base adds a class without adding value. In that case, implement the forwarding and the added behavior directly in a single class. The GoF explicitly acknowledge this: "There's no need to define an abstract Decorator class when you only need to add one responsibility." The optimization merges the Decorator's forwarding responsibility into the ConcreteDecorator.

### Phase 5: Layer at Runtime

Instantiation order determines the decoration chain. The innermost object is the real component; each wrapping object is one decoration layer. The outermost reference is what clients hold and interact with.

```
client → [outer decorator] → [middle decorator] → [inner decorator] → [component]
              ↑
     client's entry point
```

At the construction site, document the order. A future developer changing `BorderDecorator(ScrollDecorator(view))` to `ScrollDecorator(BorderDecorator(view))` will get subtly different behavior — the comment prevents this from being an invisible refactoring accident.

---

## Consequences Analysis

### Benefits

**1. More flexibility than static inheritance**
Responsibilities can be added and removed at runtime simply by attaching and detaching decorators. With inheritance, the set of responsibilities is fixed at compile time. This means a decorator can be added for a debugging session and removed in production without code changes — just configuration changes.

Inheritance requires a new class for each combination. Decorators can be mixed and matched freely. Two decorators covering N behaviors replace 2^N subclasses.

You can also add a responsibility *twice*. Attaching two `BorderDecorator` instances gives a double border. Inheriting from `Border` twice is a compile error.

**2. Avoids feature-laden base classes**
Without Decorator, the pressure is to add all foreseeable features into a single monolithic class. Decorator allows a simple, focused base class with functionality composed incrementally. Clients pay only for what they use. New decorators can be defined independently of the components they decorate, even for unforeseen extensions.

### Liabilities

**3. Decorator and component are not identical**
A decorated component is not the same object as the undecorated component. From an object identity standpoint, `decorated_view is text_view` is `False`. Code that relies on object identity — caching by reference, set membership checks, `isinstance` guards — breaks when decorators are introduced. If identity matters, keep a direct reference to the ConcreteComponent alongside the decorated chain.

**4. Lots of little objects**
A design that uses Decorator heavily produces systems composed of many small objects that look similar (they all implement the same interface). They differ only in how they are connected, not in their class names or visible data. These systems are highly customizable and easy to extend, but can be hard to debug and understand. Inspecting a reference at runtime tells you only the outermost type — you cannot easily see the full chain without traversing it. Document the chain structure explicitly in the code where it is assembled.

---

## Decorator vs. Strategy: Skin vs. Guts

The GoF describe the key distinction as: "A decorator changes an object's skin; a strategy changes its guts."

| Aspect | Decorator | Strategy |
|--------|-----------|----------|
| What changes | Outer behavior (adds to interface, wraps calls) | Inner algorithm (replaces how the object computes) |
| Component awareness | Component does not know about decorators | Component knows about strategy objects; references and maintains them |
| Depth of change | Surface — before/after operation forwarding | Core — the computation itself is replaced |
| Component weight | Works best with lightweight Component class | Viable even when Component is heavyweight |
| Interface requirement | Decorator must conform to Component interface | Strategy can have its own specialized interface |
| Analogy | Wrapping a gift — the gift doesn't change | Swapping the engine in a car — the car has to be designed to allow it |

**When to prefer Strategy:** When the Component class is intrinsically heavyweight (contains significant data and behavior), making the Decorator pattern too costly (every decorator carries the base weight). In that case, design the component to delegate behavior to a separate strategy object, and replace the strategy to extend functionality. The component must be modified to support strategies, but the modification is contained.

**When to prefer Decorator:** When you cannot or should not modify the component, when responsibilities are additive (not replacements), and when the Component interface is stable and lightweight.

---

## Omitting the Abstract Decorator Class — Full Analysis

The abstract Decorator base class is a structural convenience, not a logical requirement. It can be omitted when:

1. **Only one ConcreteDecorator is needed** — there is nothing to share between multiple ConcreteDecorators, so the abstraction layer adds zero value.
2. **Working with an existing class hierarchy** — you are decorating a class you did not design, and adding an intermediate abstract class to the hierarchy would require changes you cannot make (sealed class, third-party library, etc.).
3. **The forwarding logic is trivial** — a one-method interface with a single forwarding line is not worth abstracting.

In these cases, the ConcreteDecorator directly holds the `_component` reference and implements both the forwarding and the decoration:

```python
# Single-responsibility case: omit abstract Decorator base
class LoggingWrapper(TextComponent):
    def __init__(self, component: TextComponent):
        self._component = component   # forwarding is merged into ConcreteDecorator

    def draw(self) -> str:
        result = self._component.draw()
        print(f"draw() → {len(result)} chars")
        return result

    def resize(self, factor: float) -> None:
        self._component.resize(factor)   # pure forwarding for non-decorated operations
```

The trade-off: if a second ConcreteDecorator is needed later, the forwarding boilerplate will be duplicated until the abstract base is extracted. Use a comment to signal the intent: `# Single decorator — abstract base omitted; extract if a second decorator is added`.

---

## Language-Specific Notes

### Python

- Use `ABC` and `@abstractmethod` for the Component interface; this enforces interface conformance at class definition time rather than runtime.
- `super().method()` is the correct forwarding call in a Decorator subclass — do not call `self._component.method()` directly in ConcreteDecorators, because this bypasses other decorators in the chain. `super()` goes to the abstract Decorator base, which then calls `self._component.method()`.
- Python's duck typing means the Component interface does not need to be a formal ABC — decorators and components just need to have the same method names. Prefer explicit ABCs in production code for tooling support (type checking, IDE autocomplete).

### Java / C#

- Use an `interface` for the Component (not an abstract class) to avoid the single-inheritance constraint.
- The abstract Decorator base class implements the interface and holds the `component` field.
- ConcreteDecorators `extend` the abstract Decorator, not the interface directly.

### C++ (GoF style)

- `VisualComponent` is an abstract base class with virtual methods.
- `Decorator` subclasses `VisualComponent`, holds `VisualComponent* _component`.
- `Decorator::Draw()` implements `{ _component->Draw(); }` — pure forwarding.
- ConcreteDecorators override `Draw()` and call `Decorator::Draw()` explicitly (not `_component->Draw()`) to maintain the chain.

### JavaScript / TypeScript

- In TypeScript, define the Component as an `interface`.
- The abstract Decorator class `implements` the interface and holds a `protected component` field.
- Use `protected` rather than `private` for `_component` in the abstract Decorator so ConcreteDecorators can access it directly if needed (though using `super.method()` is preferred).

---

## Known Uses (from GoF)

- **InterViews, ET++ (UI toolkits):** Graphical embellishments on widgets — borders, scroll bars, drop shadows. The `DebuggingGlyph` in InterViews prints debugging information before and after forwarding layout requests, useful for tracing layout behavior.
- **ET++ streams:** `StreamDecorator` for compression (`CompressingStream`) and ASCII encoding (`ASCII7Stream`) — see Example 3 in the skill.
- **MacApp 3.0 / Bedrock:** Use a list of "adorner" objects attached to views — a variant of Decorator where the component maintains a list of decorations rather than each decorator wrapping the next. Necessary because the View class is heavyweight; full Decorator would be too expensive.
- **Java I/O:** `InputStream` → `BufferedInputStream`, `GZIPInputStream`, `DataInputStream` — the canonical real-world Decorator chain.
- **Python WSGI middleware:** Each middleware layer wraps the next application callable — structurally identical to Decorator.
