# Strategy Pattern — Implementation Guide

Full reference for the `strategy-pattern-implementor` skill. Contains the complete participants catalog, all 7 consequences, the interface design decision tree, Flyweight optimization details, and language-specific implementation notes.

---

## Participants

### Strategy (e.g., `Compositor`, `SortStrategy`, `PaymentStrategy`)
- Declares an interface common to all supported algorithms
- Context uses this interface exclusively — it never imports a ConcreteStrategy directly
- The interface method signature is the central design decision (see Interface Design section below)

### ConcreteStrategy (e.g., `SimpleCompositor`, `TeXCompositor`, `QuickSortStrategy`)
- Implements the algorithm using the Strategy interface
- Each class encapsulates one algorithm and its algorithm-specific data
- ConcreteStrategies do not know about each other (unlike State, where state objects may initiate transitions to siblings)

### Context (e.g., `Composition`, `DataProcessor`, `PaymentService`)
- Configured with a ConcreteStrategy object at construction or via a setter
- Maintains a reference to a Strategy object
- May define an interface that lets Strategy access its data (relevant for Approach 2 — passing context as argument)
- Forwards algorithm execution to the Strategy; does not implement the algorithm itself

---

## Collaborations

- Strategy and Context interact to implement the chosen algorithm
- A context may pass all required data to the strategy when the algorithm is called (Approach 1), or pass itself as an argument and let the strategy request what it needs (Approach 2)
- Clients usually create and pass a ConcreteStrategy object to the context; thereafter, clients interact with the context exclusively
- There is often a family of ConcreteStrategy classes for a client to choose from — a factory or registry can centralize this selection

---

## All 7 Consequences

### Benefits

**1. Families of related algorithms**
Strategy hierarchies define a reusable family of algorithms or behaviors. Inheritance can factor out common functionality of the algorithms into a shared base ConcreteStrategy class (not the interface). This keeps common logic out of both the Context and the individual concrete implementations.

**2. An alternative to subclassing**
Without Strategy, you would subclass the Context directly to give it different behaviors (e.g., `BubbleSortDataProcessor`, `QuickSortDataProcessor`). This hard-wires the algorithm into the Context: it mixes algorithm implementation with Context logic, makes Context harder to understand and extend, and prevents runtime algorithm swapping. You end up with many related subclasses whose only difference is the algorithm they employ. Strategy via composition avoids all of this.

**3. Strategies eliminate conditional statements**
When different behaviors are lumped into one class, conditional statements to select the right behavior are unavoidable. Encapsulating behaviors in separate Strategy classes eliminates these conditionals entirely.

Example — without Strategy (the code smell):
```cpp
void Composition::Repair() {
    switch (_breakingStrategy) {
    case SimpleStrategy:
        ComposeWithSimpleCompositor();
        break;
    case TeXStrategy:
        ComposeWithTeXCompositor();
        break;
    // ...
    }
    // merge results with existing composition, if necessary
}
```

With Strategy (the refactored form):
```cpp
void Composition::Repair() {
    _compositor->Compose();
    // merge results with existing composition, if necessary
}
```

Code containing many conditional statements often indicates the need to apply the Strategy pattern.

**4. A choice of implementations**
Strategies can provide different implementations of the same behavior. The client can choose among strategies with different time and space trade-offs — for example, a fast-but-approximate algorithm vs. a slower but globally optimal one (SimpleCompositor vs. TeXCompositor).

### Drawbacks

**5. Clients must be aware of different Strategies**
The pattern has a potential drawback: a client must understand how Strategies differ before it can select the appropriate one. Clients may be exposed to implementation details. Therefore, use Strategy only when the variation in behavior is relevant to clients. If clients do not care about algorithm selection and a sensible default exists, provide a default strategy so they never have to deal with strategy objects at all.

**6. Communication overhead between Strategy and Context**
The Strategy interface is shared by all ConcreteStrategy classes whether the algorithms they implement are trivial or complex. Hence it is likely that some ConcreteStrategies will not use all the information passed to them through this interface — simple ConcreteStrategies may use none of it.

In the Lexi case, `SimpleCompositor` ignores stretchability data; `ArrayCompositor` ignores everything. This means the context creates and initializes parameters that never get used. If this overhead is an issue, tighter coupling between Strategy and Context is needed — but this reduces the generality of the pattern.

**7. Increased number of objects**
Strategies increase the number of objects in an application. Sometimes you can reduce this overhead by implementing strategies as stateless objects that contexts can share (see Flyweight Optimization below). Any residual state is maintained by the context, which passes it in each request to the Strategy object.

---

## Interface Design Decision Tree

Use this to choose between Approach 1 (pass data as parameters) and Approach 2 (pass context reference):

```
Does the strategy need a bounded, well-known set of inputs?
├── YES → Use Approach 1: explicit parameters
│         Keeps Strategy and Context decoupled.
│         Context passes data[], counts, and output buffers.
│         Risk: some ConcreteStrategies receive parameters they don't use.
│
└── NO → Does the data set vary significantly across ConcreteStrategies?
         ├── YES → Use Approach 2: pass context as argument
         │         Strategy calls back on the context to get what it needs.
         │         Context must expose a richer interface to its data.
         │         Risk: tighter coupling between Strategy and Context.
         │
         └── Can Strategy store a reference to Context at construction?
                  YES → Initialize strategy with context reference.
                        Eliminates per-call parameter passing entirely.
                        Strategy can request exactly what it needs on demand.
                        Risk: tightest coupling — Strategy is bound to one Context type.
```

**General rule:** The needs of the particular algorithm and its data requirements determine the best technique. Prefer Approach 1 when parameters are bounded and stable. Move to Approach 2 when parameter lists grow unwieldy or vary significantly across strategies.

---

## Flyweight Optimization

Strategies increase object count. When strategies are stateless — all working data comes from parameters, nothing is stored between calls — they can be shared as Flyweights:

**When it applies:**
- The ConcreteStrategy has no instance variables
- All state is passed in via the interface method parameters
- The same algorithm is used by many Context instances simultaneously

**When it does NOT apply:**
- The ConcreteStrategy stores configuration (e.g., `ArrayCompositor` stores an interval count — this is constructor-injected state, not per-invocation state, but it makes the strategy non-shareable unless all contexts want the same interval)
- The algorithm accumulates state across multiple invocations

**Implementation pattern:**

```python
# Stateless strategy — safe to share
class JsonExportStrategy(ExportStrategy):
    # No instance variables — all data comes through export()
    def export(self, records, output_path):
        import json
        with open(output_path, "w") as f:
            json.dump(records, f, indent=2)

# Shared instance registry — one object per algorithm
class StrategyRegistry:
    _instances: dict[str, ExportStrategy] = {}

    @classmethod
    def get(cls, key: str) -> ExportStrategy:
        if key not in cls._instances:
            cls._instances[key] = _STRATEGY_CLASSES[key]()
        return cls._instances[key]
```

Shared strategies should not maintain state across invocations. The Flyweight pattern (GoF p. 195) describes this approach in detail.

---

## Making Strategy Optional

The Context class can be simplified when it is meaningful to have no strategy. The Context checks for a strategy before delegating; if none is set, it executes default behavior:

```python
class DataProcessor:
    def __init__(self, strategy: SortStrategy = None):
        self._strategy = strategy  # None is valid

    def process(self, data: list) -> list:
        if self._strategy is None:
            # Default behavior — no strategy object required
            return sorted(data)
        return self._strategy.sort(data)
```

The benefit: clients who are satisfied with the default behavior never need to deal with Strategy objects at all. Only clients that need non-default behavior need to know strategies exist.

---

## Strategy as Template Parameters (C++ / Generics)

In statically typed languages with generics, Strategy can be expressed as a template/generic parameter rather than a runtime interface:

```cpp
template <class AStrategy>
class Context {
    void Operation() { theStrategy.DoAlgorithm(); }
    // ...
private:
    AStrategy theStrategy;
};

// Configured at compile time — no virtual dispatch overhead
Context<MyStrategy> aContext;
```

This approach is applicable only when:
1. The strategy is selected at compile time (not runtime)
2. It does not need to be changed at runtime

The benefit: static binding eliminates virtual dispatch overhead. Strategy and Context are bound at compile time — this can increase efficiency significantly in performance-critical code.

---

## Strategy vs. State — The Critical Distinction

Strategy and State have identical class diagrams. The difference is intent and who initiates the swap:

| Question | Strategy | State |
|----------|----------|-------|
| Who changes the behavior? | The **client** installs a strategy explicitly | The **context object** transitions itself based on internal logic |
| Do concrete variants know about each other? | No — strategies are independent | Yes — state objects often initiate transitions to sibling states |
| Is the variation about selecting an algorithm? | Yes — same interface, different computation | No — about representing a lifecycle that drives behavior |
| Can the same "strategy" be active indefinitely? | Yes | No — states have transition logic |

**Rule:** If the behavioral swap is driven by external selection (caller chooses the algorithm), it is Strategy. If the behavioral swap is driven by the object's internal state machine (the object decides when to change its own behavior), it is State.

---

## Known Uses

- **Lexi document editor (GoF case study):** `Composition`/`Compositor` — formatting algorithm encapsulated as interchangeable Compositor strategies (SimpleCompositor, TeXCompositor, ArrayCompositor)
- **RTL compiler optimizer:** `RegisterAllocator` and `RISCScheduler`/`CISCScheduler` — register allocation and instruction scheduling as strategies, enabling retargeting to different machine architectures
- **ObjectWindows dialog validation:** `Validator` objects encapsulate field validation strategies (`RangeValidator`, custom validators) — attached optionally to entry fields
- **ET++SwapsManager:** Financial instrument pricing strategies — `YieldCurve` subclasses encapsulate discount factor computation strategies, mixed and matched per instrument type
- **Java `Comparator`:** `Collections.sort(list, comparator)` — the Comparator is a Strategy object encapsulating the comparison algorithm
- **Python `key=` parameter in `sorted()`:** A function reference as a lightweight Strategy (first-class function as ConcreteStrategy, no subclass required)

---

## Language-Specific Notes

### Python
- First-class functions eliminate the need for explicit ConcreteStrategy classes in simple cases: `processor.set_strategy(lambda data: sorted(data))` is a valid Strategy
- Use `abc.ABC` and `@abstractmethod` for the Strategy interface to enforce implementation at class-definition time
- Stateless strategies can be module-level singletons (avoid repeated instantiation)

### Java
- Use an interface (not abstract class) for the Strategy unless shared implementation is needed
- Java lambdas (single-method functional interfaces) make lightweight strategies trivial: `sorter.setStrategy(data -> Arrays.sort(data))`
- `java.util.Comparator` is the canonical Strategy in the standard library

### TypeScript / JavaScript
- Strategy interface expressed as a TypeScript interface or type alias with a single call signature
- Functions as strategies are idiomatic: `context.setStrategy((data) => data.sort())`

### Go
- Strategy interface is a Go interface — implicit implementation, no declaration required
- Structs implementing the interface are ConcreteStrategies
- Function types can serve as lightweight strategies for single-method interfaces
