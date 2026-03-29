# Bridge Pattern Implementation Guide

Companion reference for the `bridge-pattern-implementor` skill. Contains the evaluate-extremes worksheet, structural participants reference, implementation decision matrix, and the complete Lexi case study.

---

## 1. Evaluate-Extremes Worksheet

Use this worksheet when designing the Implementor interface — the hardest decision in applying Bridge.

### Step 1: List all operations the Abstraction needs (from the client's perspective)

Write down every operation clients will call on your Abstraction. This is the client's vocabulary, not the platform's.

Example:
```
Window clients need:
- DrawLine(p1, p2)
- DrawRect(p1, p2)
- DrawPolygon(points, n)
- DrawText(text, position)
- Raise()
- Lower()
- Iconify()
- DrawContents()
```

### Step 2: Enumerate your target implementations

List every platform, backend, or implementation variant you must support (including near-future ones you can anticipate).

Example:
```
Platforms: X Window System, IBM Presentation Manager, macOS Quartz
```

### Step 3: Determine the intersection

For each Abstraction operation, mark which implementations support it natively:

| Operation         | X Window | PM | macOS |
|-------------------|:---:|:---:|:---:|
| Draw rectangle    | Yes (XDrawRectangle) | No (path only) | Yes (CGContextAddRect) |
| Draw line         | Yes | Yes | Yes |
| Draw text         | Yes | Yes | Yes |
| Raise window      | Yes | Yes | Yes |

Operations where ALL platforms say Yes = the intersection.

**Problem with pure intersection:** PM cannot draw a rectangle directly. If you design only around the intersection, you lose XDrawRectangle's directness and force X to emulate rectangle drawing via a polygon — that's a capability regression.

### Step 4: Determine the union

List every operation any platform exposes, even platform-specific ones.

**Problem with pure union:** PM path operations (`GpiBeginPath`, `GpiSetCurrentPosition`, `GpiPolyLine`, `GpiEndPath`, `GpiStrokePath`) are opaque to X and macOS developers. Including them in the interface creates a leaking abstraction that forces X developers to understand PM idioms. The interface also grows fragile — any PM SDK change breaks the interface.

### Step 5: Define balanced primitives (the actual output)

Design primitives that:
1. Every platform can satisfy in SOME form (even if mechanisms differ)
2. Express device-level operations, not domain-level operations
3. Enable the Abstraction to compose its higher-level calls

For windows:

| Implementor Primitive | How X satisfies it | How PM satisfies it |
|-----------------------|-------------------|---------------------|
| `DeviceRect(x0,y0,x1,y1)` | `XDrawRectangle` | `GpiBeginPath` + `GpiPolyLine` + `GpiStrokePath` |
| `DeviceLine(x0,y0,x1,y1)` | `XDrawLine` | `GpiLine` |
| `DeviceText(s, x, y)` | `XDrawString` | `GpiCharStringAt` |
| `DeviceBitmap(name, x, y)` | `XCopyPlane` | `GpiBitBlt` |
| `ImpTop()` | `XRaiseWindow` | `WinSetWindowPos(HWND_TOP)` |
| `ImpBottom()` | `XLowerWindow` | `WinSetWindowPos(HWND_BOTTOM)` |

Key insight: the PM implementation of `DeviceRect` uses a path — that's fine. The Implementor interface doesn't care HOW it's done, only that the outcome (a rectangle drawn) is achieved.

---

## 2. Structural Participants Reference

### Abstraction
- Defines the interface clients use
- Holds a reference `_imp` to an Implementor object
- Implements its operations by delegating to `_imp`
- Does NOT contain any platform-specific code

```cpp
class Window {
  protected:
    WindowImp* _imp;
    WindowImp* GetWindowImp();   // may use factory to lazily initialize

  public:
    void DrawRect(const Point& p1, const Point& p2) {
        _imp->DeviceRect(p1.X(), p1.Y(), p2.X(), p2.Y());
    }
    virtual void DrawContents() = 0;
    // ...
};
```

### Refined Abstraction
- Extends Abstraction with additional operations or specializations
- Still delegates to `_imp` — adds no platform-specific code
- Examples: `ApplicationWindow`, `IconWindow`, `TransientWindow`

```cpp
class IconWindow : public Window {
  public:
    void DrawContents() {
        WindowImp* imp = GetWindowImp();
        if (imp) imp->DeviceBitmap(_bitmapName, 0.0, 0.0);
    }
  private:
    const char* _bitmapName;
};
```

### Implementor
- Defines the primitive interface for platform-specific operations
- Does NOT mirror the Abstraction's interface — it's lower-level
- Operations are primitives that ConcreteImplementors translate to platform calls

```cpp
class WindowImp {
  public:
    virtual void ImpTop() = 0;
    virtual void ImpBottom() = 0;
    virtual void ImpSetExtent(const Point&) = 0;
    virtual void ImpSetOrigin(const Point&) = 0;
    virtual void DeviceRect(Coord, Coord, Coord, Coord) = 0;
    virtual void DeviceText(const char*, Coord, Coord) = 0;
    virtual void DeviceBitmap(const char*, Coord, Coord) = 0;
    // ...
  protected:
    WindowImp();
};
```

### Concrete Implementor
- Inherits from Implementor
- Translates each primitive into the target platform's actual API calls
- All platform-specific code lives here and only here

See Section 4 below for the full X vs PM contrast.

---

## 3. Wiring Decision Matrix

How should the Abstraction get its Implementor? Choose based on your context.

| Wiring Strategy | How it works | When to use | Trade-off |
|-----------------|-------------|-------------|-----------|
| **Constructor parameter** | Caller passes a ConcreteImplementor directly | Tests, simple configurations, DI containers | Caller must know which Implementor to create |
| **Factory method in Abstraction** | Abstraction's constructor calls a virtual factory method to create its own Implementor | Single Implementor with possible subclass variation | Tight but contained; no external factory needed |
| **Abstract Factory (recommended for families)** | An external factory (e.g., `WindowSystemFactory`) encapsulates all platform-specific object creation | Multiple related implementation objects must be consistent (same platform family) | Requires factory infrastructure; best long-term |
| **Lazy initialization (default + switch)** | Abstraction starts with a default Implementor, switches based on runtime conditions | Adaptive algorithms (e.g., small collection = linked list, large = hash table) | Most flexible; adds complexity |

### Abstract Factory pattern for Bridge wiring

When your Bridge operates in a world where multiple implementation objects must all come from the same platform family (window system + color system + font system all must be PM or all X), the Abstract Factory pattern cleanly encapsulates this constraint.

```cpp
class WindowSystemFactory {
  public:
    virtual WindowImp* CreateWindowImp() = 0;
    virtual ColorImp*  CreateColorImp()  = 0;
    virtual FontImp*   CreateFontImp()   = 0;
};

class PMWindowSystemFactory : public WindowSystemFactory {
    WindowImp* CreateWindowImp() { return new PMWindowImp(); }
    ColorImp*  CreateColorImp()  { return new PMColorImp();  }
    FontImp*   CreateFontImp()   { return new PMFontImp();   }
};

class XWindowSystemFactory : public WindowSystemFactory {
    WindowImp* CreateWindowImp() { return new XWindowImp(); }
    // ...
};

// Window constructor — knows nothing about X or PM
Window::Window() {
    _imp = WindowSystemFactory::Instance()->CreateWindowImp();
}
```

The factory is configured once (typically as a Singleton) at application startup. The rest of the system never mentions `XWindowImp` or `PMWindowImp` directly.

---

## 4. Lexi Case Study — Window / WindowImp

### The problem

The Lexi document editor needs a Window abstraction that application code uses for drawing and window management. Lexi must run on multiple window systems: X Window System, IBM Presentation Manager, and macOS.

**Naive approach:** Create `XApplicationWindow`, `PMApplicationWindow`, `XIconWindow`, `PMIconWindow`, etc. Result: N window kinds × M platforms classes, plus every new platform requires editing every abstraction class.

**Bridge approach:** Separate the hierarchy.
- `Window` hierarchy: `ApplicationWindow`, `IconWindow`, `TransientWindow`, `DialogWindow` — captures kinds of windows
- `WindowImp` hierarchy: `XWindowImp`, `PMWindowImp`, `MacWindowImp` — captures platform implementations

### The evaluate-extremes analysis for Lexi's Window

**Intersection approach rejected:** Limiting `WindowImp` to only what all platforms share would omit PM-specific path capabilities. Worse, it would give the X implementation nothing to lean on for rectangle drawing — X HAS a rectangle primitive (`XDrawRectangle`) that would go unused.

**Union approach rejected:** Exposing `GpiBeginPath`, `GpiSetCurrentPosition`, `GpiPolyLine`, `GpiEndPath`, `GpiStrokePath` in the interface forces every X implementor to understand PM path semantics. Every PM SDK change would break the interface.

**Balanced primitives chosen:** `DeviceRect`, `DeviceLine`, `DeviceText`, `DeviceBitmap`, `ImpTop`, `ImpBottom`, `ImpSetOrigin`, `ImpSetExtent`. These are the minimal set that:
- Every window system can provide (even via emulation)
- Compose into all the operations Window needs
- Do not expose any platform-specific idioms

### Contrasting implementations: DeviceRect

**X Window System** — has a native rectangle-drawing primitive:

```cpp
void XWindowImp::DeviceRect(Coord x0, Coord y0, Coord x1, Coord y1) {
    int x = round(min(x0, x1));
    int y = round(min(y0, y1));
    int w = round(abs(x0 - x1));
    int h = round(abs(y0 - y1));
    // XDrawRectangle takes lower-left corner + width + height
    XDrawRectangle(_dpy, _winid, _gc, x, y, w, h);
}
```

Note: XDrawRectangle defines a rectangle by lower-left corner + dimensions, so DeviceRect must compute those from two arbitrary corner coordinates. Simple math, direct API.

**IBM Presentation Manager** — has no rectangle primitive; uses a general multi-segment path API:

```cpp
void PMWindowImp::DeviceRect(Coord x0, Coord y0, Coord x1, Coord y1) {
    Coord left   = min(x0, x1);  Coord right = max(x0, x1);
    Coord bottom = min(y0, y1);  Coord top   = max(y0, y1);

    PPOINTL point[4];
    point[0] = {left,  top};      // top-left
    point[1] = {right, top};      // top-right
    point[2] = {right, bottom};   // bottom-right
    point[3] = {left,  bottom};   // bottom-left

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

Note: PM defines a rectangle by specifying 4 vertices of a polygon path, then stroking it. Completely different idiom — but both satisfy the same `DeviceRect(x0, y0, x1, y1)` signature.

### How the Abstraction uses these primitives

```cpp
// Window::DrawRect is completely platform-neutral
void Window::DrawRect(const Point& p1, const Point& p2) {
    _imp->DeviceRect(p1.X(), p1.Y(), p2.X(), p2.Y());
}

// IconWindow uses another primitive
void IconWindow::DrawContents() {
    WindowImp* imp = GetWindowImp();
    if (imp != 0) {
        imp->DeviceBitmap(_bitmapName, 0.0, 0.0);
    }
}
```

`Window::DrawRect` is the same code for X, PM, and Mac. The platform difference is entirely hidden inside the ConcreteImplementors.

### Factory wiring in Lexi

```cpp
// Window's lazy GetWindowImp — uses Abstract Factory
WindowImp* Window::GetWindowImp() {
    if (_imp == 0) {
        _imp = WindowSystemFactory::Instance()->MakeWindowImp();
    }
    return _imp;
}

// Configured once at startup: windowSystemFactory = new XWindowSystemFactory()
// All subsequent Window instances automatically get XWindowImp
```

`WindowSystemFactory::Instance()` is a Singleton. It is set to the appropriate concrete factory at application launch based on the detected platform. No Window subclass ever mentions `XWindowImp` or `PMWindowImp`.

---

## 5. Implementation Considerations Checklist

### One Implementor (degenerate Bridge)
When only one implementation exists, you still create the Implementor interface even though there is only one ConcreteImplementor. Benefit: changes to the implementation class (even compilation) don't require recompiling any Abstraction class or its clients. This is the "Cheshire Cat" idiom in C++ — the implementation can be defined in a private header not shipped to clients, hiding the implementation entirely.

### Sharing Implementors (reference counting)
When multiple Abstraction objects share one Implementor (e.g., Coplien's Handle/Body idiom for shared string representations), the Implementor needs a reference count. The Abstraction's assignment operator manages Ref/Unref:

```cpp
Handle& Handle::operator=(const Handle& other) {
    other._body->Ref();
    _body->Unref();
    if (_body->RefCount() == 0) delete _body;
    _body = other._body;
    return *this;
}
```

### Multiple inheritance — why it does NOT work
In C++, you might try to combine Abstraction and ConcreteImplementor via multiple inheritance (publicly from Abstraction, privately from ConcreteImplementor). This permanently binds one implementation to one abstraction via static inheritance. You cannot switch implementations at runtime. This is NOT a Bridge — it is the original problem Bridge solves.

---

## 6. Related Patterns

| Pattern | Relationship to Bridge |
|---------|----------------------|
| **Abstract Factory** | Natural partner for wiring. An Abstract Factory creates and configures a specific Bridge by returning the right ConcreteImplementor for the current context. |
| **Adapter** | Adapter makes unrelated classes work together — applied retroactively. Bridge is designed upfront to separate abstraction and implementation — applied proactively. Structurally similar, intent is different. |
| **Strategy** | Strategy varies an algorithm. Bridge varies a structural implementation. Strategy's context doesn't usually extend the strategy interface; Bridge's Abstraction has a full subclass hierarchy. |
