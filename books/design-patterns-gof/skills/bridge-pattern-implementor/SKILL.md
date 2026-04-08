---
name: bridge-pattern-implementor
description: |
  Implement the Bridge pattern to decouple an abstraction from its implementation so both can vary independently. Use when you want to avoid a permanent binding between abstraction and implementation, when both abstractions and implementations should be extensible by subclassing, when implementation changes should not require recompiling clients, or when you need to share an implementation among multiple objects. Includes the evaluate-extremes design process (union vs intersection of functionality) and Abstract Factory integration for runtime implementation selection.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/bridge-pattern-implementor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissimos"]
    chapters: [2, 4]
    pages: [58-64, 146-155]
tags: [design-patterns, bridge, structural-pattern, decoupling, abstraction, implementation, cross-platform]
depends-on: []
execution:
  tier: 2
  mode: full
  inputs:
    - type: codebase
      description: "A software project where you need to decouple an abstraction from its implementation — or a design scenario described by the user"
  tools-required: [Read, Write, TodoWrite]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any coding environment. Works with or without an existing codebase."
---

# Bridge Pattern Implementor

## When to Use

You are designing or refactoring a system where an abstraction (e.g., a Window, Shape, or Device) must work across multiple implementations (e.g., platform APIs, rendering engines, storage backends) and both the abstraction and implementation dimensions need to evolve independently.

Specific triggers:
- You notice a class hierarchy "exploding" — adding a new abstraction variant requires N new classes, one per implementation platform
- Client code is bound to a specific implementation at compile time and you need runtime flexibility
- You need to change or swap an underlying implementation without recompiling clients
- You want to share a single implementation object across multiple abstraction instances (e.g., reference counting, shared state)
- You are porting an existing system to multiple platforms and want the abstraction hierarchy to remain platform-neutral

Before starting, verify:
- Is the variation driven by **two independent axes**? (If only one axis varies, plain inheritance suffices.)
- Are the implementations genuinely interchangeable from the abstraction's point of view? (If they require different calling conventions the client must know about, Adapter may be a better fit.)

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **The abstraction to decouple:** What concept does the client use? (e.g., Window, Shape, Queue)
  → Check prompt for: class names, interface names, the concept being modeled
  → If missing, ask: "What is the abstraction — the concept your client code works with?"

- **The implementation axis:** What varies underneath? (e.g., OS platform, rendering backend, storage engine)
  → Check prompt for: mentions of platforms, backends, vendors, environments
  → If missing, ask: "What are the different implementations you need to support?"

### Observable Context (gather from environment)

- **Existing class hierarchy:** Check for signs of the "proliferation" problem
  → Look for: abstract base classes with many concrete subclasses, class names combining two concepts (e.g., `XIconWindow`, `PMIconWindow`, `LinuxFilePrinter`, `WindowsFilePrinter`)
  → If present: this confirms a Bridge is appropriate; use existing names as abstraction/implementor candidates

- **Existing platform coupling:** Scan for platform-specific API calls inside abstraction classes
  → Look for: `#include <windows.h>`, OS-specific function calls, vendor SDK imports inside domain classes
  → If found: the Bridge's job is to push all such calls into the Implementor subclasses

### Default Assumptions

- If no existing codebase: work from the user's verbal description of the two axes
- If language not specified: illustrate with language-neutral pseudocode; note the user's language if evident from context
- If only one implementation variant exists today: still apply Bridge if more are planned, or if compile-time isolation from clients is needed

## Process

Use `TodoWrite` to track all steps before starting.

```
[ ] Step 1: Diagnose the design problem
[ ] Step 2: Apply evaluate-extremes to define the Implementor interface
[ ] Step 3: Define the Abstraction interface
[ ] Step 4: Implement Concrete Implementors
[ ] Step 5: Implement the Abstraction and Refined Abstractions
[ ] Step 6: Wire the Implementor at construction (Abstract Factory or parameter)
[ ] Step 7: Verify independence — extend both hierarchies without touching the other
```

---

### Step 1: Diagnose the Design Problem

**ACTION:** Identify the two independently varying axes and verify you have a Bridge candidate, not an Adapter or Strategy situation.

**WHY:** Bridge is designed upfront to allow independent extension. Adapter is applied retroactively to make incompatible interfaces cooperate. Strategy varies the algorithm, not a structural implementation dependency. Diagnosing early prevents building the wrong pattern. The clearest symptom of a Bridge candidate is "nested generalization" — a class hierarchy that doubles with every new platform or implementation type added.

Draw or enumerate the current (or planned) hierarchy. If adding a new abstraction variant requires creating N classes (one per implementation), and adding a new implementation variant requires creating M classes (one per abstraction) — you have the proliferation problem Bridge solves.

**IF** the symptom is an N×M class explosion → proceed to Step 2
**IF** only the algorithm varies, not the platform/backend structure → consider Strategy instead
**IF** you're adapting a pre-existing incompatible interface → consider Adapter instead

---

### Step 2: Apply the Evaluate-Extremes Process to Define the Implementor Interface

**ACTION:** Determine the Implementor (implementation interface) by reasoning about two extreme positions, then choosing a balanced middle.

**WHY:** The Implementor interface is the hardest design decision in Bridge. It must be broad enough to serve all abstraction variants, but not so broad that it becomes incoherent. The evaluate-extremes technique makes this decision systematic rather than arbitrary.

**The two extremes:**

**Extreme 1 — Intersection of functionality:** Define the Implementor interface as only the operations that EVERY implementation platform supports. This produces the most portable interface but is dangerously limiting — the interface is only as capable as the weakest platform. Features that most (but not all) platforms support become inaccessible.

**Extreme 2 — Union of functionality:** Define the Implementor interface as the total set of operations across ALL platforms. This produces the richest interface but it becomes huge, incoherent, and must change whenever any vendor revises their API. Every concrete Implementor must stub out capabilities it doesn't have.

**The balanced middle (what to actually do):**
1. List all operations your abstractions need to perform (from the client's perspective).
2. For each operation, determine whether ALL target implementations can support it (even via different primitives).
3. Group into "core primitives" — low-level operations that every implementation can provide in some form, even if via different mechanisms.
4. The Implementor interface declares only these primitives. The Abstraction composes them into higher-level operations.

**Example (Lexi Window System):** The Window class needs `DrawLine`, `DrawRect`, `DrawText`, `Raise`, `Lower`. Instead of the Implementor interface mirroring these exactly, it exposes lower-level device primitives like `DeviceRect`, `DeviceText`, `DeviceBitmap`. The Abstraction (`Window`) translates its higher-level calls into combinations of these primitives. This keeps the Implementor interface small and platform-expressible, while the Abstraction interface remains application-friendly.

**IF** you find a device primitive that some platforms lack → check whether it can be emulated using other primitives. If yes, keep it. If no, either remove it from the Implementor interface or accept it as a known limitation in that ConcreteImplementor.

See [references/bridge-implementation-guide.md](references/bridge-implementation-guide.md) for the complete evaluate-extremes worksheet.

---

### Step 3: Define the Abstraction Interface

**ACTION:** Define the Abstraction class — the interface the client sees. It holds a reference (pointer/field) to an Implementor. Its public operations are high-level and application-oriented.

**WHY:** The Abstraction is the client's view of the world. Its interface should express domain concepts, not implementation primitives. The key structural rule: the Abstraction holds a reference to an Implementor object, and delegates to it — it does NOT inherit from it. This composition is what makes the two hierarchies independent.

Key design rules:
- The Abstraction's public operations speak the domain's language (e.g., `DrawRect(point1, point2)`, not `DeviceRect(x0, y0, x1, y1)`)
- The Abstraction translates its operations into calls to `_imp->DeviceXxx(...)` primitives
- The Implementor reference is protected (or package-private) — concrete Abstraction subclasses may need to call it

```
// Pseudocode structure
class Abstraction {
  protected:
    Implementor* _imp;  // The bridge reference

  public:
    // High-level domain operations — these are what clients call
    virtual void HighLevelOperation() {
        // Composed from low-level implementor primitives
        _imp->PrimitiveA();
        _imp->PrimitiveB();
    }
}
```

---

### Step 4: Implement the Concrete Implementors

**ACTION:** For each target platform or backend, create a ConcreteImplementor class that inherits from the Implementor interface and translates each primitive into that platform's actual API calls.

**WHY:** The Concrete Implementors are where all platform-specific code lives. Once these classes exist, no platform-specific code should appear anywhere else in the system. The Abstraction and its subclasses remain entirely platform-neutral. Changing a platform means changing only its ConcreteImplementor.

The implementations of the same operation will often look radically different across platforms — and that is expected. The point is that Window's `DrawRect` doesn't need to know or care about these differences.

**Illustrative contrast — drawing a rectangle:**

The X Window System has a direct rectangle primitive:
```cpp
// XWindowImp::DeviceRect — X Window System implementation
void XWindowImp::DeviceRect(Coord x0, Coord y0, Coord x1, Coord y1) {
    int x = round(min(x0, x1));
    int y = round(min(y0, y1));
    int w = round(abs(x0 - x1));
    int h = round(abs(y0 - y1));
    XDrawRectangle(_dpy, _winid, _gc, x, y, w, h);
}
```

IBM's Presentation Manager has no rectangle primitive — it uses a general path/polygon API:
```cpp
// PMWindowImp::DeviceRect — IBM Presentation Manager implementation
void PMWindowImp::DeviceRect(Coord x0, Coord y0, Coord x1, Coord y1) {
    Coord left = min(x0, x1);  Coord right = max(x0, x1);
    Coord bottom = min(y0, y1); Coord top = max(y0, y1);
    PPOINTL point[4];
    point[0] = {left, top};    point[1] = {right, top};
    point[2] = {right, bottom}; point[3] = {left, bottom};
    if (GpiBeginPath(_hps, 1L) == false
        || GpiSetCurrentPosition(_hps, &point[3]) == false
        || GpiPolyLine(_hps, 4L, point) == GPI_ERROR
        || GpiEndPath(_hps) == false) {
        // report error
    } else {
        GpiStrokePath(_hps, 1L, 0L);
    }
}
```

Both satisfy the same `DeviceRect` interface. Window's `DrawRect` calls `_imp->DeviceRect(...)` and is completely shielded from this difference.

---

### Step 5: Implement the Abstraction and Refined Abstractions

**ACTION:** Implement the base Abstraction's operations in terms of Implementor primitives. Then create Refined Abstraction subclasses for each logical variation of the abstraction.

**WHY:** Refined Abstractions capture semantic variations of the concept (e.g., `ApplicationWindow`, `IconWindow`, `TransientWindow`) without duplicating any platform-specific code. Each refined abstraction overrides or extends the base abstraction, relying on the same inherited `_imp` reference. This is what makes the N×M explosion disappear — you write N abstraction classes and M implementor classes, not N×M combinations.

```
// Base Abstraction — delegates to implementor
void Window::DrawRect(const Point& p1, const Point& p2) {
    _imp->DeviceRect(p1.X(), p1.Y(), p2.X(), p2.Y());
}

// Refined Abstraction — adds application-level behavior, still platform-neutral
class IconWindow : public Window {
    void DrawContents() {
        WindowImp* imp = GetWindowImp();
        if (imp) imp->DeviceBitmap(_bitmapName, 0.0, 0.0);
    }
};
```

---

### Step 6: Wire the Implementor at Construction

**ACTION:** Decide how and when the Abstraction receives its Implementor. Choose one of three approaches based on your constraints.

**WHY:** The Abstraction must acquire a concrete Implementor to function, but Bridge's goal is that the Abstraction should NOT be hardwired to a specific Implementor class. The wiring strategy determines how clean this decoupling is at runtime.

**Three wiring strategies:**

**Option A — Constructor parameter (simplest):** Pass the ConcreteImplementor in as a constructor argument. Straightforward, but the caller must know which Implementor to pass.

```python
window = ApplicationWindow(XWindowImp())   # caller decides
```

**Option B — Factory method (runtime selection):** The Abstraction's constructor calls a factory to obtain the right Implementor. The Abstraction stays decoupled from any specific ConcreteImplementor class.

```cpp
// Window's constructor uses a factory — knows nothing about XWindowImp or PMWindowImp
Window::Window() {
    _imp = WindowSystemFactory::Instance()->MakeWindowImp();
}
```

**Option C — Abstract Factory (recommended for platform families):** Introduce an Abstract Factory (e.g., `WindowSystemFactory`) whose sole job is to encapsulate all platform-specific object creation. The factory knows what platform is in use; it returns the right Implementor. This is the cleanest approach when the implementation axis is a family of related objects (window system, color system, font system all need to be platform-consistent).

```cpp
class WindowSystemFactory {
public:
    virtual WindowImp* CreateWindowImp() = 0;
    virtual ColorImp*  CreateColorImp()  = 0;
    virtual FontImp*   CreateFontImp()   = 0;
};

class XWindowSystemFactory : public WindowSystemFactory {
    WindowImp* CreateWindowImp() { return new XWindowImp(); }
    // ...
};
```

The factory is configured once at application startup (as a Singleton). From then on, every Window just calls `factory->CreateWindowImp()` and gets the right one for the current platform.

**IF** implementations are a family of related objects → use Abstract Factory (Option C)
**IF** the Abstraction is genuinely agnostic to which Implementor it gets → use factory method (Option B)
**IF** tests or simple configurations need direct control → use constructor parameter (Option A)

---

### Step 7: Verify Independence — Extend Both Hierarchies Without Touching the Other

**ACTION:** As a verification exercise, add one new ConcreteImplementor and one new Refined Abstraction, and confirm neither change affects the other hierarchy.

**WHY:** This is the core promise of Bridge. If your implementation is correct, adding `MacWindowImp` requires only a new class inheriting from `WindowImp` — no Window subclass changes. Adding `PaletteWindow` requires only a new class inheriting from `Window` — no WindowImp subclass changes. If you find yourself modifying the other hierarchy to accommodate a new variant, the bridge is leaky — most likely because the Implementor interface doesn't match what some Abstraction variants actually need.

Checklist for a correct Bridge:
- [ ] Can a new ConcreteImplementor be added without touching any Abstraction class?
- [ ] Can a new Refined Abstraction be added without touching any Implementor class?
- [ ] Does the client only see the Abstraction interface — never a ConcreteImplementor directly?
- [ ] Is all platform-specific code confined to ConcreteImplementor classes?
- [ ] Does the Abstraction forward to the Implementor via delegation (not inheritance)?

---

## Inputs

- Description of the concept to model (the abstraction axis)
- Description of the implementation variants (the implementation axis)
- Optionally: existing class hierarchy showing the proliferation problem

## Outputs

- **Implementor interface** — pure abstract class/interface with platform primitives
- **ConcreteImplementor classes** — one per platform/backend (all platform code lives here)
- **Abstraction base class** — holds `_imp` reference, provides high-level operations
- **Refined Abstraction subclasses** — domain variations, fully platform-neutral
- **Factory wiring** — mechanism to select the right ConcreteImplementor at runtime

## Key Principles

- **Composition over inheritance for implementation** — the Abstraction holds a reference to an Implementor; it does NOT inherit from it. This single structural choice is what enables independent variation. Inheritance would permanently bind the abstraction to one implementation.

- **Implementor interface ≠ Abstraction interface** — the two interfaces serve different audiences. The Abstraction interface speaks to application developers (domain concepts). The Implementor interface speaks to platform implementors (device primitives). They can and should be different in style and granularity.

- **Evaluate extremes before committing** — union is too broad (unstable, incoherent), intersection is too narrow (loses platform capabilities). The right Implementor interface is a set of primitives that every platform can satisfy in some form, even if via different mechanisms.

- **All platform code in ConcreteImplementors** — if you find a platform API call anywhere outside a ConcreteImplementor class, the bridge is incomplete. The whole point is to isolate platform variation so the abstraction hierarchy never needs to change when platforms change.

- **Bridge is designed upfront; Adapter is applied retroactively** — Bridge is a proactive design decision made when building a system that must span multiple implementations. If you're adapting a pre-existing incompatible interface, Adapter is more appropriate.

- **One Implementor is still valid** — if today there is only one implementation, Bridge still has value: it eliminates compile-time dependencies from clients. Changing the Implementor class no longer requires recompiling anything that uses the Abstraction. This is the "Cheshire Cat" idiom.

## Examples

### Example 1: Cross-Platform Document Editor Window System (Lexi)

**Scenario:** A WYSIWYG document editor must run on X Window System and IBM Presentation Manager without duplicating window logic. The team faces a 3×2 class explosion (ApplicationWindow, IconWindow, TransientWindow × XWindow, PMWindow = 6 classes, growing to 3×N for each new platform).

**Trigger:** "I need my document editor to run on X and PM without duplicating the window logic."

**Process:**
- Step 1: Diagnosed N×M explosion — 3 window types × 2 platforms = 6 classes today, 3×N tomorrow.
- Step 2: Applied evaluate-extremes. Intersection misses PM-specific path capabilities. Union exposes X-specific display handles everywhere. Balanced: `WindowImp` with device primitives (`DeviceRect`, `DeviceText`, `DeviceBitmap`).
- Step 3: `Window` base class provides `DrawRect()`, `DrawText()` to application code.
- Step 4: X uses `XDrawRectangle` directly (1 call). PM uses `GpiBeginPath`/`GpiPolyLine`/`GpiStrokePath` (5+ calls) — dramatically different for the same operation.
- Step 6: Wired via `WindowSystemFactory` (Abstract Factory). `Window` constructor calls `factory->CreateWindowImp()`.
- Step 7: Verified — adding `MacWindowImp` required zero changes to Window, IconWindow, or ApplicationWindow.

**Output:** `Window`/`WindowImp` bridge — 5 classes (3 abstractions + 2 implementors) vs 6, scaling to 3+N instead of 3×N.

---

### Example 2: Multi-Backend Notification Service

**Scenario:** A notification system must support email, SMS, and push today, with Slack and webhooks planned. Notification types (Alert, Digest, Reminder) format content differently but must work across all delivery backends.

**Trigger:** "We want to add Slack and webhooks later without rewriting the notification logic."

**Process:**
- Step 1: Two axes identified — notification type (Alert, Digest, Reminder) × delivery backend (Email, SMS, Push). N×M = 9 classes today, growing.
- Step 2: Evaluate-extremes. Intersection: `send(to, subject, body)` — too weak for rich push payloads. Union: expose APNS tokens everywhere — leaks implementation details. Balanced: `Deliver(recipient, title, body, metadata)`.
- Steps 3-5: `Notification` abstraction with `Alert`, `Digest`, `Reminder` as refined abstractions. `EmailDelivery`, `SMSDelivery`, `PushDelivery` as ConcreteImplementors.
- Step 7: Verified — adding `SlackDelivery` requires zero changes to Alert/Digest/Reminder.

**Output:** Notification Bridge — 3 abstractions × 3 implementors, easily extended on both axes independently.

---

### Example 3: Degenerate Bridge — Single Implementation with Compile Isolation

**Scenario:** A system uses a proprietary graphics library. The team wants to be able to swap libraries without breaking client code or forcing recompiles, even though there's only one implementation today.

**Trigger:** "We want to change to a different graphics library without breaking client code."

**Process:**
- Step 1: Only one implementation exists. N×M = N×1 — no explosion yet, but dependency is system-wide.
- Steps 2-5: Created thin `GraphicsImp` interface mirroring only the operations the Abstraction uses. `ProprietaryGraphicsImp` implements it. Client code depends only on `GraphicsImp`.
- Step 7: When the library changes, only `ProprietaryGraphicsImp` is rewritten — clients need not recompile.

**Output:** Compile-time isolation achieved. Future library migration becomes a contained, low-risk change. This is the "Cheshire Cat" idiom.

## References

- For the evaluate-extremes worksheet and Implementor interface design process in detail, see [references/bridge-implementation-guide.md](references/bridge-implementation-guide.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissimos.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
