---
name: decorator-pattern-implementor
description: |
  Implement the Decorator pattern to attach additional responsibilities to objects dynamically, providing a flexible alternative to subclassing. Use when you need to add behaviors like logging, caching, validation, authentication, compression, or UI embellishments without creating a subclass for every combination. Addresses the subclass explosion problem through transparent enclosure — decorators conform to the component interface so clients cannot distinguish decorated from undecorated objects. Covers composition order effects and the lightweight-decorator optimization. Triggers when: adding optional behaviors to objects at runtime, wrapping streams or middleware, layering cross-cutting concerns, needing to mix and match responsibilities without combinatorial subclass growth.
model: sonnet
context: 1M
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/decorator-pattern-implementor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - structural-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [4]
    pages: [51-54, 166-174]
tags: [design-patterns, structural, gof, decorator, composition, wrapper, embellishment, middleware]
execution:
  tier: 2
  mode: full
  inputs:
    - type: code
      description: "Existing code showing a class that needs optional behaviors added, or a description of the responsibilities to layer dynamically"
  tools-required: [TodoWrite, Read]
  tools-optional: [Grep, Edit]
  mcps-required: []
  environment: "Any codebase. Language-agnostic — examples use Python but the pattern applies universally."
---

# Decorator Pattern Implementor

## When to Use

You need to add responsibilities to individual objects — not to an entire class — and you want to do it dynamically, without modifying the component or generating a subclass for every possible combination of responsibilities.

Apply this skill when:

- **Subclass explosion** is imminent or already present: a class needs behaviors like `Logged`, `Cached`, `Validated`, `Compressed` in varying combinations, and creating `LoggedCachedValidator` subclasses has become unmanageable.
- **Responsibilities are optional or withdrawable** at runtime: a feature toggles on per-object, not per-class.
- **Individual objects** need embellishment while other instances of the same class stay plain.
- **You cannot subclass** the target: the class definition is sealed, final, or belongs to a third-party library.
- You want to **compose responsibilities incrementally** — add one, try it, add another — rather than building a monolithic class.

Before starting, confirm this is Decorator and not another structural pattern:
- Need to adapt an incompatible interface? → Use Adapter instead.
- Need to aggregate multiple children, not wrap one? → Use Composite instead.
- Need to change the algorithm inside the object (its "guts") rather than its visible behavior (its "skin")? → Consider Strategy instead.
- Do you need to vary responsibilities at the *class* level (compile-time), not per-object at runtime? → Use inheritance directly.

---

## Process

### Step 1: Set Up Tracking and Assess the Subclass Explosion Problem

**ACTION:** Use `TodoWrite` to track all steps, then identify the component class and enumerate the responsibilities that need to be added in combination.

**WHY:** The central problem Decorator solves is subclass explosion. Before reaching for the pattern, you need to see the problem concretely: if N responsibilities can be independently combined, inheritance requires 2^N subclasses. Mapping this out makes the trade-off visible and confirms that Decorator is worth the additional structural complexity it introduces.

```
TodoWrite:
- [ ] Step 1: Assess the combination space and confirm Decorator applies
- [ ] Step 2: Define or confirm the Component interface
- [ ] Step 3: Define the abstract Decorator base class
- [ ] Step 4: Implement ConcreteDecorator classes
- [ ] Step 5: Determine composition order and wire the chain at runtime
- [ ] Step 6: Validate and address implementation concerns
```

Map the combination space:

| Responsibility | Independent? | Withdrawable? | Optional per-object? |
|---------------|:---:|:---:|:---:|
| e.g., Logging | Yes | Yes | Yes |
| e.g., Caching | Yes | Yes | Yes |
| e.g., Validation | Yes | No | Yes |

If each row answers Yes to at least one column, Decorator applies.

Also note: **how many responsibilities** will be combined. If there is only ever one additional responsibility and it is always present, plain inheritance may suffice — the Decorator trade-off (more classes, "lots of little objects" debugging complexity) is not worth it for a single static enhancement.

---

### Step 2: Define or Confirm the Component Interface

**ACTION:** Identify the abstract interface (class or protocol) that both the real object and all decorators must implement. If it does not exist, extract one.

**WHY:** Transparent enclosure — the core mechanism of the pattern — depends entirely on this interface. Clients pass a `Component*` reference; they cannot tell whether they hold the real component or a chain of three decorators. This transparency is what allows decorators to be nested recursively and layered at runtime without clients knowing. If the Component class is too heavyweight (stores data, has many non-interface methods), decorators inherit that bulk and the pattern becomes expensive to use in quantity.

**Two situations:**

**A — Interface already exists** (common when working with existing architecture):
- Confirm the ConcreteComponent implements it.
- Confirm all operations that decorators need to forward are declared on the interface, not just the ConcreteComponent.

**B — Interface needs to be extracted** (common when refactoring legacy code):
- Identify every operation clients call on the component.
- Extract those into an abstract base class or interface.
- Keep the Component class **lightweight** — define the interface only, defer data representation to subclasses.

```python
# Component interface — lightweight, defines interface only
from abc import ABC, abstractmethod

class TextComponent(ABC):
    @abstractmethod
    def draw(self) -> str: ...

    @abstractmethod
    def resize(self, factor: float) -> None: ...

# ConcreteComponent — data and real behavior live here, not on Component
class TextView(TextComponent):
    def __init__(self, content: str):
        self._content = content

    def draw(self) -> str:
        return self._content

    def resize(self, factor: float) -> None:
        # resize logic
        pass
```

**Pitfall:** If `TextComponent` had stored `_content` itself, every decorator instance would carry that unused field. Keep data out of the Component base.

---

### Step 3: Define the Abstract Decorator Base Class

**ACTION:** Create an abstract `Decorator` class that (1) implements the Component interface and (2) holds a reference to a wrapped Component. Each operation in the interface delegates to that wrapped component by default.

**WHY:** This class is what makes the chain work. Because it implements the Component interface, a Decorator can wrap another Decorator — arbitrary nesting is possible. Because it delegates by default, ConcreteDecorators only need to override the operations they augment; all other operations pass through transparently. Without this base, each ConcreteDecorator would have to manually implement every forwarding call, creating boilerplate and the risk of forgetting to forward an operation.

**Note on omitting the abstract Decorator class:** If you only need to add *one* responsibility and are adapting an existing class hierarchy (not designing from scratch), you can merge the Decorator base into a single ConcreteDecorator. Omit the abstraction when the abstraction adds no value — there will never be a second ConcreteDecorator to share it.

```python
class Decorator(TextComponent):
    """Abstract Decorator — conforms to Component interface, delegates by default."""

    def __init__(self, component: TextComponent):
        # WHY: store as Component reference, not as TextView — allows decorating
        # decorators (recursive wrapping) transparently.
        self._component = component

    def draw(self) -> str:
        # Default: pure forwarding. ConcreteDecorators override to augment.
        return self._component.draw()

    def resize(self, factor: float) -> None:
        self._component.resize(factor)
```

---

### Step 4: Implement ConcreteDecorator Classes

**ACTION:** For each responsibility to be added, create a ConcreteDecorator subclass that overrides the relevant operations, calls the parent Decorator (to forward to the wrapped component), and adds its behavior before or after the forwarding call.

**WHY:** The before/after placement is a meaningful design decision. Running added behavior *before* forwarding (pre-processing) is appropriate when you need to gate or transform the request before the component handles it — e.g., validation, authentication, input transformation. Running behavior *after* forwarding (post-processing) is appropriate when you need to augment or annotate the component's output — e.g., drawing a border after the component draws itself, logging the result of an operation, caching the return value. Either order is valid; the choice is determined by what the decoration is semantically doing.

```python
class BorderDecorator(Decorator):
    """Draws a border around the component's rendered output."""

    def __init__(self, component: TextComponent, border_width: int = 1):
        super().__init__(component)
        self._border_width = border_width

    def draw(self) -> str:
        # Post-processing: let the component draw first, then add the border
        inner = super().draw()           # delegates up the chain
        return self._draw_border(inner)

    def _draw_border(self, content: str) -> str:
        border = "-" * (len(content.splitlines()[0]) + 2 * self._border_width)
        return f"{border}\n{content}\n{border}"


class ScrollDecorator(Decorator):
    """Adds scrolling capability — clips to viewport and tracks scroll position."""

    def __init__(self, component: TextComponent, viewport_height: int = 20):
        super().__init__(component)
        self._scroll_position = 0
        self._viewport_height = viewport_height

    def draw(self) -> str:
        full = super().draw()
        lines = full.splitlines()
        visible = lines[self._scroll_position:self._scroll_position + self._viewport_height]
        return "\n".join(visible)

    def scroll_to(self, position: int) -> None:
        """Decorator-specific operation — only callable when client knows the type."""
        self._scroll_position = position


class LoggingDecorator(Decorator):
    """Logs every draw call with timestamp."""

    def draw(self) -> str:
        import datetime
        result = super().draw()
        print(f"[{datetime.datetime.now().isoformat()}] draw() called")
        return result
```

**Decorator-specific operations:** `ScrollDecorator` adds `scroll_to()`, which is not on the Component interface. Clients that need this operation must hold a `ScrollDecorator` reference directly, not a `TextComponent` reference. This is a deliberate trade-off: the transparency guarantee (clients treat everything as `TextComponent`) breaks only when a client explicitly needs decorator-specific behavior. In that case, keep a direct reference to the decorator alongside the component reference in the window object.

---

### Step 5: Determine Composition Order and Wire the Chain at Runtime

**ACTION:** Decide the order in which decorators wrap the component, then instantiate the chain. Composition order determines which decorator's behavior is "outermost" and therefore executes first on the way in and last on the way out.

**WHY — the Lexi Border/Scroller case study:** The GoF "Embellishing the User Interface" case study (pages 51-54) demonstrates this directly. Lexi needs a text editing area with both a border and scroll bars. Two composition orders are possible:

```
Order A (Border outside Scroller):
  border → scroller → composition (text content)
```
When `Draw()` is called on `border`, it tells `scroller` to draw, which renders the clipped scrollable view of the text, and then `border` draws around the scrolled viewport. The **border is fixed relative to the window** — it does not scroll.

```
Order B (Scroller outside Border):
  scroller → border → composition (text content)
```
Now when `scroller` renders its viewport, it is clipping a bordered composition. The **border scrolls with the text** — when the user scrolls down, the border moves off-screen. This may or may not be desirable, but it is a different visual behavior.

The general rule: **the outermost decorator's behavior is the last thing applied to the output.** Order from innermost (closest to the real component) to outermost (what clients actually interact with):

```python
# Lexi-style: fixed border around a scrollable text view (Order A)
text_view = TextView(content)
scrollable = ScrollDecorator(text_view, viewport_height=20)
bordered_scrollable = BorderDecorator(scrollable, border_width=1)

# Clients interact with bordered_scrollable — it is a TextComponent
window.set_contents(bordered_scrollable)

# Alternative: scrollable border (Order B) — the border scrolls with the text
bordered = BorderDecorator(text_view, border_width=1)
scrollable_bordered = ScrollDecorator(bordered, viewport_height=20)
window.set_contents(scrollable_bordered)
```

**Decision guide for composition order:**

| Question | Implication |
|----------|-------------|
| Does decorator A need to see the output of decorator B? | A must be outer (A wraps B) |
| Is decorator A a gateway/guard that should run before B? | A must be outer |
| Should decorator A's additions be inside B's scope? | A must be inner |
| Does one decorator's state affect the other's behavior? | Explicit contract needed; document the order requirement |

---

### Step 6: Validate and Address Implementation Concerns

**ACTION:** Verify the implementation satisfies the transparency requirement, check for the "lots of little objects" problem, and mark tasks complete.

**WHY:** The Decorator pattern's primary liability — documented by the GoF — is that it produces systems of many small, similar-looking objects. Each decorator layer is a separate object; a chain of five decorators wrapping one component is six objects that all respond to the same interface. This makes the system highly customizable but harder to debug (you cannot inspect the class name of a reference and know what you are dealing with) and potentially harder for teammates to understand. Acknowledging this upfront means it will not be a surprise during maintenance.

**Validation checklist:**

- [ ] The Component interface does not store data — data representation lives in ConcreteComponent and ConcreteDecorators only
- [ ] Every ConcreteDecorator calls `super().operation()` (or equivalent) rather than skipping the forwarding — skipping silently breaks the chain
- [ ] Clients that only use the Component interface have not been given a concrete Decorator type reference (they should hold a Component reference)
- [ ] Object identity: if any code uses `isinstance` checks or identity comparisons (`obj is component`), it must be updated — a decorated component is *not* identical to the original
- [ ] The composition order is documented wherever the chain is wired together (not left implicit)
- [ ] If the abstract Decorator class was omitted (single-responsibility case), confirm this choice in a comment so future developers understand there is no base class to extend

**Mark all TodoWrite tasks complete.**

---

## Examples

### Example 1: Lexi Embellishment — Border and Scroller (GoF Case Study)

**Scenario:** Lexi, a WYSIWYG document editor, displays a text editing area. The design requires both a border (to demarcate the page) and scroll bars (to navigate long documents). The embellishments must be removable at runtime and must not affect other UI components in the application.

**Trigger:** "We need to add a border and scrolling to the text editing area. Other parts of the UI should not know about these embellishments."

**Key design decisions from the GoF:**
- `MonoGlyph` (abstract Decorator base) stores a single child `_component` and forwards all `Draw()` calls to it by default. This is exactly the abstract Decorator base from Step 3.
- `Border` subclasses `MonoGlyph`, overrides `Draw()` to call `MonoGlyph::Draw()` first (forward to child), then call `DrawBorder()` — post-processing.
- `Scroller` also subclasses `MonoGlyph` and adds `scroll_to()` as a decorator-specific operation.

```
Composition chain (border fixed, scroller inside border):
  Border → Scroller → Composition (text content + layout glyphs)

border->Draw() calls:
  MonoGlyph::Draw()  (forwards to scroller)
    scroller->Draw() (clips to viewport, calls composition->Draw())
  DrawBorder()       (draws the border around what scroller rendered)
```

**Reversing the order** (scroller outside border) makes the border scroll with the text — a different UX behavior from the same two classes, zero code changes, only the instantiation order changes.

**Output:** A `Border*` reference that is also a `Glyph*`. The window treats it as a plain glyph; the embellishments are invisible to the rest of the system.

---

### Example 2: HTTP Middleware Stack (Web Backend)

**Scenario:** A web API handler needs logging, authentication checking, and response caching, in varying combinations per endpoint. Using inheritance would require `LoggedAuthenticatedCachedHandler`, `LoggedHandler`, `AuthenticatedHandler`, etc.

**Trigger:** "Different API endpoints need different combinations of logging, auth, and caching. I can't keep creating subclasses for every combination."

```python
class RequestHandler(ABC):
    @abstractmethod
    def handle(self, request: dict) -> dict: ...

class UserProfileHandler(RequestHandler):
    def handle(self, request: dict) -> dict:
        return {"user": "Alice", "email": "alice@example.com"}

class HandlerDecorator(RequestHandler):
    def __init__(self, handler: RequestHandler):
        self._handler = handler

    def handle(self, request: dict) -> dict:
        return self._handler.handle(request)

class AuthDecorator(HandlerDecorator):
    def handle(self, request: dict) -> dict:
        # Pre-processing: gate before forwarding
        if not request.get("auth_token"):
            return {"error": "Unauthorized", "status": 401}
        return super().handle(request)

class LoggingDecorator(HandlerDecorator):
    def handle(self, request: dict) -> dict:
        print(f"Request: {request.get('path')}")
        result = super().handle(request)
        print(f"Response status: {result.get('status', 200)}")
        return result

class CachingDecorator(HandlerDecorator):
    def __init__(self, handler: RequestHandler):
        super().__init__(handler)
        self._cache: dict = {}

    def handle(self, request: dict) -> dict:
        key = str(request)
        if key in self._cache:
            return self._cache[key]
        result = super().handle(request)
        self._cache[key] = result
        return result

# Composition: Auth gate → Cache → real handler, with logging on the outside
handler = LoggingDecorator(
    AuthDecorator(
        CachingDecorator(
            UserProfileHandler()
        )
    )
)
```

**Composition order matters:** `AuthDecorator` is inside `LoggingDecorator`, so failed auth attempts are still logged. Moving `AuthDecorator` outside `LoggingDecorator` would suppress logs for unauthenticated requests. Neither is wrong — the choice reflects product intent.

**Output:** Any combination of behaviors can be assembled at configuration time. Adding rate-limiting is a new `RateLimitDecorator` class — no changes to existing handlers or decorators.

---

### Example 3: I/O Stream Decoration (GoF Known Uses)

**Scenario:** A file streaming system needs to support optional compression (run-length encoding, Lempel-Ziv, etc.) and optional 7-bit ASCII conversion for transmission over legacy channels. Any combination of these should work with any stream type (`FileStream`, `MemoryStream`).

**Trigger:** "We need to compress and/or ASCII-convert stream data. Different streams need different combinations and we don't want to create CompressedFileStream, ASCIIFileStream, CompressedASCIIFileStream..."

```
Component:       Stream (abstract — PutInt, PutString, HandleBufferFull)
ConcreteComp:    FileStream, MemoryStream
Decorator base:  StreamDecorator (forwards HandleBufferFull by default)
ConcreteDecA:    CompressingStream (overrides HandleBufferFull — compresses buffer)
ConcreteDecB:    ASCII7Stream      (overrides HandleBufferFull — converts to 7-bit ASCII)
```

Wiring a compressed, ASCII-encoded file stream:
```cpp
// C++ (from GoF page 174)
Stream* aStream = new CompressingStream(
    new ASCII7Stream(
        new FileStream("aFileName")
    )
);
aStream->PutInt(12);
aStream->PutString("aString");
```

`CompressingStream` wraps `ASCII7Stream` which wraps `FileStream`. Data flows from the client down to `FileStream`, then back up through ASCII conversion, then through compression, before being written to disk. The order ensures data is first ASCII-encoded, then compressed — reversing would compress raw binary data and then attempt ASCII encoding on it, which is semantically wrong for this use case.

**Output:** Two decorator classes cover four combinations (plain, compressed, ASCII, compressed+ASCII) across any number of stream types, with no subclass proliferation.

---

## Decorator vs. Inheritance — When to Use Which

| Dimension | Decorator | Inheritance |
|-----------|-----------|-------------|
| When behaviors are added | Runtime (dynamic) | Compile-time (static) |
| Combinations | 2 decorators = 4 combinations (mixed freely) | 2 behaviors = 3 subclasses minimum |
| Withdrawing a responsibility | Remove from chain | Impossible — class is fixed |
| Object identity | Decorated object ≠ original (identity breaks) | Is-a relationship preserved |
| Debugging | Chains of small objects — harder to inspect | Single class — straightforward |
| Adding same behavior twice | Wrap with the same decorator twice | Inheriting from a class twice is an error |

**Choose Decorator** when responsibilities are optional, additive, and need to vary per-object at runtime.

**Choose inheritance** when the additional behavior is always present for all instances of a class and there is no combinatorial variation.

---

## Key Principles

- **Interface conformance over convenience** — a decorator that does not fully implement the Component interface breaks the transparency guarantee. Every operation on the Component interface must be implemented, even if the implementation is pure delegation. Partial forwarding means some clients will get wrong behavior silently.

- **Keep the Component base lightweight** — the Component class's job is to define the interface, not store data. If data representation is placed on the Component, every decorator instance in a long chain carries that data as dead weight. Data belongs on ConcreteComponent and ConcreteDecorators only.

- **Forward before or after based on semantics, not convention** — whether a ConcreteDecorator calls `super().operation()` before or after its added behavior is a semantic decision: "does my addition depend on what the component did, or does the component's output depend on what I do first?" Make this explicit in a comment.

- **Document composition order wherever the chain is assembled** — composition order is behavior-changing and invisible at the call site. A reader seeing `BorderDecorator(ScrollDecorator(view))` must understand the layering effect. A short comment stating "border is fixed; scroller is inside" prevents order from being accidentally reversed during refactoring.

- **Object identity breaks — acknowledge it** — clients that use `==`, `is`, or `isinstance` against the original component will fail with decorated versions. If identity checks are present in the codebase, keep a direct reference to the ConcreteComponent alongside the decorated chain rather than expecting clients to unwrap it.

---

## Reference Files

| File | Contents |
|------|----------|
| `references/decorator-implementation-guide.md` | Full participants catalog, consequences analysis, language-specific implementation notes, transparent enclosure reasoning process, comparison with Strategy (skin vs. guts), and omitting the abstract Decorator class |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-structural-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
