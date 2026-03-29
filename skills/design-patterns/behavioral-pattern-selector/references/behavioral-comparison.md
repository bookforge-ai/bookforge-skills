# Behavioral Pattern Comparison Reference

> Source: *Design Patterns: Elements of Reusable Object-Oriented Software* (Gamma, Helm, Johnson, Vlissides), Chapter 5
> Used by: `behavioral-pattern-selector` — Steps 2, 3, 4

---

## Quick-Select Table

| Pattern | Scope | Use when... | Encapsulates | Decoupling role |
|---------|-------|-------------|--------------|-----------------|
| Chain of Responsibility | Object | More than one object may handle a request; handler not known a priori | — | Sender from receiver via forwarding chain |
| Command | Object | Parameterize, queue, log, or undo operations | Request (invocation) | Invoker from receiver via command object |
| Interpreter | Class | Sentences in a simple grammar need to be interpreted | Grammar rule (as a class) | — |
| Iterator | Object | Access aggregate contents without exposing internal structure | Traversal method | — |
| Mediator | Object | Complex many:many object interactions need to be simplified | Inter-object protocol | Colleagues from each other via central hub |
| Memento | Object | Object state must be saved and restored without breaking encapsulation | State snapshot | — |
| Observer | Object | One object changes and an unknown number of dependents must react | — | Subject from observers via interface subscription |
| State | Object | Object behavior must change radically when internal state changes | State-dependent behavior | — |
| Strategy | Object | A family of algorithms must be interchangeable | Algorithm | — |
| Template Method | Class | Invariant algorithm steps should be fixed; variable steps deferred to subclasses | — (uses inheritance) | — |
| Visitor | Object | Operations on a stable object structure must grow without modifying the classes | Operations on a structure | — |

---

## Full Applicability — Per Pattern

### Chain of Responsibility

**Use when:**
- More than one object may handle a request, and the handler is not known a priori — it should be ascertained automatically.
- You want to issue a request to one of several objects without specifying the receiver explicitly.
- The set of objects that can handle a request should be specified dynamically.

**Encapsulation type:** None — the pattern works with an existing set of objects; it does not extract a variation into a standalone encapsulating object.

**Decoupling role:** Sender from receiver. The sender submits a request to the head of the chain; any handler in the chain may fulfill it. The sender has no reference to any specific receiver.

**Key trade-off:** The chain can be changed and extended easily at runtime. However, **there is no guarantee a request is handled** — if no handler claims it, the request falls off the end of the chain silently. Always include a fallback handler (a "catch-all" at the chain's tail) in production systems.

**Confusable with:** Command — both decouple sender from receiver, but Command binds a specific receiver at creation time, whereas Chain of Responsibility leaves the receiver implicit and determined at runtime by chain order.

---

### Command

**Use when:**
- You want to parameterize objects by an action to perform (an object-oriented replacement for callbacks).
- You need to specify, queue, and execute requests at different times — a command object can outlive the original request.
- You need to support undo: `Execute()` performs the operation; `Unexecute()` reverses it. Unlimited undo/redo is achieved by maintaining a history list and traversing it.
- You need to support crash recovery via logging: commands are stored to disk and re-executed on restart.
- You want to structure a system around high-level transactions built on primitive operations.

**Encapsulation type:** Request (invocation). The command object holds the receiver reference, the operation to invoke, and any arguments. The invoker never sees the receiver.

**Decoupling role:** 1 invoker (sender) : 1 receiver per command. The Command object is the explicit binding between them.

**Key trade-off:** Each unique sender-receiver binding nominally requires a Command subclass. In languages with first-class functions, closures or lambdas can replace subclasses. MacroCommand composes multiple commands — this composability is a significant advantage for scripting and transaction support.

**Confusable with:**
- Chain of Responsibility — Command knows its receiver; Chain does not.
- Memento — both are "magic tokens" passed around as arguments; Command encapsulates a request (executable), Memento encapsulates state (not executable, opaque to all but the originator).

---

### Interpreter

**Use when:**
- There is a language (or notation) to interpret, and its statements can be represented as abstract syntax trees.
- The grammar is simple — for complex grammars, the class hierarchy becomes large and unmanageable; use a parser generator instead.
- Efficiency is not a critical concern — the most efficient interpreters usually compile to another form rather than interpreting parse trees directly.

**Encapsulation type:** Grammar rule. Each rule in the grammar becomes a class in the hierarchy. The pattern derives its name from the class that implements interpretation across that hierarchy.

**Decoupling role:** None specific to sender/receiver decoupling.

**Key trade-off:** Easy to extend the grammar (add a new rule = add a new class). Hard to maintain when the grammar grows large. For production languages, use parser generators (yacc, ANTLR) that can interpret without building full abstract syntax trees.

**Confusable with:** Composite — Interpreter commonly uses Composite to structure the abstract syntax tree. Non-terminal expression classes are Composite nodes; terminal expression classes are leaves.

---

### Iterator

**Use when:**
- You need to access an aggregate object's contents without exposing its internal representation.
- You need to support multiple simultaneous traversals of the same aggregate.
- You want to provide a uniform interface for traversing different aggregate structures (polymorphic iteration).

**Encapsulation type:** Traversal method. The iterator object holds the traversal state (current position) and the traversal algorithm, separate from the aggregate that holds the elements.

**Decoupling role:** Client from aggregate internal structure. The client calls `First()`, `Next()`, `IsDone()`, `CurrentItem()` without knowing whether the aggregate is a list, a skip list, a tree, or any other structure.

**Key trade-off:** Separating traversal from the aggregate enables multiple simultaneous traversals of the same collection without interference. The aggregate must provide a factory method (`CreateIterator()`) to produce the appropriate iterator — this is a Factory Method application. Internal iterators (where the aggregate controls traversal) are simpler to use but less flexible than external iterators (where the client controls traversal).

**Confusable with:** Visitor — Visitor applies an operation to each element during traversal; Iterator handles the traversal itself. They compose: an Iterator traverses while a Visitor performs the operation on each item visited.

---

### Mediator

**Use when:**
- A set of objects communicate in well-defined but complex ways. The resulting interdependencies are unstructured and difficult to understand.
- Reusing an object is difficult because it refers to and communicates with many other objects.
- A behavior distributed between several classes should be customizable without a lot of subclassing.

**Encapsulation type:** Inter-object protocol. The mediator object owns all the routing logic between colleague objects. Colleagues refer only to the mediator, never to each other directly.

**Decoupling role:** Many colleagues from each other via a central hub. The mediator centralizes rather than distributes communication. This is the opposite architectural direction from Observer.

**Key trade-off:**
- *Advantage over Observer:* Communication flow is easier to understand and change — all logic lives in one place.
- *Disadvantage vs. Observer:* The mediator itself can become a monolithic bottleneck — a "god object" that knows too much. Observer produces more reusable subjects and observers (finer-grained classes) but harder-to-trace communication flow.
- Mediator can reduce the need for subclassing by centralizing behavior that would otherwise be distributed across subclasses.

**Confusable with:** Observer — see "Observer vs. Mediator" section below.

---

### Memento

**Use when:**
- A snapshot of (some portion of) an object's state must be saved so it can be restored later, **and**
- A direct interface to obtaining that state would expose implementation details and break the object's encapsulation.

**Encapsulation type:** State snapshot. The memento holds the originator's internal state at a point in time. Only the originator can write to or read from the memento — it is opaque to all other objects (the caretaker holds it but never inspects it).

**Decoupling role:** None specific to sender/receiver. Memento supports undo mechanisms and checkpointing without coupling the undo mechanism to the originator's internal structure.

**Key trade-off:** If the originator must copy large amounts of state frequently, mementos can be expensive in memory. Incremental mementos (storing only the diff) can mitigate this but add complexity. The narrow interface (caretaker cannot inspect) preserves encapsulation but prevents caretakers from managing memento storage efficiently.

**Confusable with:** Command — both are "tokens" passed as arguments. Command is executable (it has a polymorphic `Execute()` operation); Memento's interface is so narrow it presents no polymorphic operations to its clients.

---

### Observer

**Use when:**
- An abstraction has two aspects, one dependent on the other. Encapsulating them in separate objects lets you vary and reuse them independently.
- A change to one object requires changing others, and you do not know how many objects need to change.
- An object should be able to notify other objects without making assumptions about who those objects are — without tight coupling.

**Encapsulation type:** None in the "extract a variation" sense — Observer encapsulates a dependency relationship. The Subject and Observer interfaces together maintain the constraint, distributed across both sides.

**Decoupling role:** 1 subject (sender) : many observers (receivers), dynamic membership. Observers self-register and self-deregister. The subject has no direct references to any observer.

**Key trade-off:**
- Promotes loose coupling and finer-grained classes (more reusable subjects and observers) — *advantage over Mediator*.
- Communication flow is hard to trace — when observers and subjects are connected indirectly, the "why did this change?" question requires following indirect chains — *disadvantage vs. Mediator*.
- Update cascades are possible: if an observer is also a subject, a notification can trigger a chain of updates that is difficult to debug.

**Confusable with:** Mediator — see "Observer vs. Mediator" section below.

---

### State

**Use when:**
- An object's behavior depends on its state, and it must change its behavior at runtime depending on that state.
- Operations have large multipart conditional statements that depend on the object's state (typically represented by enumerated constants). The State pattern puts each branch of the conditional into a separate class.

**Encapsulation type:** State-dependent behavior. Each `ConcreteState` class encapsulates all behavior appropriate to one state of the context. The context delegates requests to its current state object.

**Decoupling role:** None specific to sender/receiver. The context decouples its behavior from its state by delegating to state objects rather than inspecting `if state == X` inline.

**Key trade-off:** State transitions can be defined in either the `ConcreteState` classes or the `Context` class. Putting transitions in state classes is more flexible but introduces dependencies between state classes (they know their successors). Putting transitions in `Context` keeps state classes independent but centralizes transition logic. The number of classes grows by one per state, which is the appropriate trade-off when states have meaningfully different behavior.

**Confusable with:** Strategy — see "State vs. Strategy" section below.

---

### Strategy

**Use when:**
- Many related classes differ only in their behavior. Strategy provides a way to configure a class with one of many behaviors.
- You need different variants of an algorithm — for example, algorithms with different space/time trade-offs.
- An algorithm uses data that clients should not know about. Use Strategy to avoid exposing complex, algorithm-specific data structures.
- A class defines many behaviors that appear as multiple conditional statements in its operations. Move related conditional branches into their own Strategy class.

**Encapsulation type:** Algorithm. The strategy object holds one interchangeable computation. Context holds a reference to a Strategy interface and delegates the algorithm to whichever concrete strategy is installed.

**Decoupling role:** None specific to sender/receiver. Strategy decouples algorithm selection from algorithm use — the context does not know which algorithm is running.

**Key trade-off:** Clients must know which strategy to select. If strategy selection is complex, pair with a factory. All strategies share the same interface — if different strategies need very different data from the context, the Strategy interface may become bloated, or strategies may receive data they do not use.

**Confusable with:**
- State — same class diagram, different intent. See section below.
- Template Method — same goal (varying an algorithm), opposite mechanism. See section below.

---

### Template Method

**Use when:**
- You want to implement the invariant parts of an algorithm once and leave it to subclasses to implement the variable behavior.
- Common behavior among subclasses should be factored and localized in a common class to avoid code duplication.
- You want to control which points subclasses can extend. A template method that calls "hook" operations permits extension only at those points.

**Encapsulation type:** None in the "separate object" sense — Template Method uses inheritance. The abstract class owns the algorithm skeleton (the template method); concrete subclasses fill in the abstract steps.

**Decoupling role:** None specific to sender/receiver.

**Key trade-off:** Template Method is the fundamental technique for code reuse in class libraries. The inversion of control ("don't call us, we'll call you") is its defining characteristic — the parent class calls the subclass's overrides, not the other way around. The cost is that variation is fixed at compile time (subclass selection) and cannot be changed at runtime.

**Confusable with:** Strategy — see section below.

---

### Visitor

**Use when:**
- An object structure contains many classes of objects with differing interfaces, and you want to perform operations on them that depend on their concrete classes.
- Many distinct and unrelated operations need to be performed on objects in an object structure, and you want to avoid "polluting" their classes with these operations. Visitor groups related operations in one class.
- The classes defining the object structure rarely change, but you often want to define new operations over the structure. (If the object structure changes frequently, it is usually better to define operations in those classes instead of using Visitor.)

**Encapsulation type:** Operations on a structure. The visitor object holds a family of operations — one per element type in the object structure — and defines them outside those classes.

**Decoupling role:** None specific to sender/receiver.

**Key trade-off:** Adding a new operation is easy — add a new Visitor class. Adding a new element type is hard — requires updating every Visitor class. The pattern is appropriate when the object structure is stable but the set of operations over it is expected to grow. Visitor breaks encapsulation: element classes must expose enough state for visitors to do their work, which may expose internals.

**Confusable with:** Iterator — Iterator traverses; Visitor operates. They compose cleanly.

---

## Key Differentiating Pairs

### Observer vs. Mediator

The GoF explicitly frames these as competing patterns. The choice is a trade-off between two architectural values:

| | Observer | Mediator |
|---|----------|----------|
| Communication model | **Distributed** — subjects and observers maintain the constraint together | **Centralized** — mediator owns all routing logic |
| Reusability | Higher — subjects and observers are fine-grained, independently reusable | Lower — mediator is application-specific |
| Understandability | Lower — indirect connections are hard to trace | Higher — all communication logic in one place |
| Typical use | Data dependency: one thing changes, many unknown others must react | Interaction complexity: many things communicate in structured but tangled ways |

Both can be present in the same system: Observer for state-change notification between subjects and their dependents; Mediator to coordinate the subjects themselves.

---

### State vs. Strategy

Same class diagram. Completely different intent.

| | Strategy | State |
|---|----------|-------|
| Who installs the variant? | The **client** (externally, explicitly) | The **context itself** (internally, based on its own logic) |
| Do concrete variants know about each other? | No — strategies are independent | Often yes — state objects initiate transitions to sibling states |
| Question being answered | "Which algorithm should run?" | "What behavior is appropriate for the current lifecycle stage?" |
| Runtime changeability | Yes — by client replacing the strategy object | Yes — by the context or state object transitioning to a new state |

If the behavior changes because someone outside the object chose a configuration → Strategy.
If the behavior changes because the object itself reached a new lifecycle milestone → State.

---

### Template Method vs. Strategy

Both vary an algorithm. The mechanism is opposite.

| | Template Method | Strategy |
|---|----------------|----------|
| Mechanism | **Inheritance** — abstract class skeleton, subclass fills steps | **Composition** — context holds a replaceable strategy object |
| Runtime flexibility | None — algorithm variant is fixed at class definition | Full — strategy can be swapped at runtime |
| Coupling | Subclass is tightly coupled to the superclass skeleton | Context and strategy are loosely coupled via interface |
| Migration path | Often the starting point (simpler) | Often the refactoring target when Template Method becomes too inflexible |

A system commonly begins with Template Method (simpler, no extra objects) and refactors to Strategy when the variation needs to be swapped at runtime or composed dynamically.

---

### Command vs. Chain of Responsibility

Both decouple sender from receiver, but the receiver's identity is handled differently.

| | Command | Chain of Responsibility |
|---|---------|------------------------|
| Receiver identity | **Known** at command-creation time (held by the command object) | **Unknown** — determined at runtime by chain order |
| Request lifecycle | First-class object — storable, undoable, loggable | Transient — request is forwarded until handled |
| Guarantee of handling | Yes — command always has a receiver | No — request may go unhandled if chain is exhausted |
| Composition | Commands compose into MacroCommands | Chain can use Commands as request objects |

Use Command when the request needs a lifecycle beyond the invocation call. Use Chain when the right handler is context-dependent and should be discovered at runtime — but always add a fallback handler.

---

## Pattern Interaction Map

Behavioral patterns that frequently combine:

| Combination | Why |
|-------------|-----|
| Chain of Responsibility + Command | Chain uses Command objects as request representations; request is then loggable and replayable |
| Chain of Responsibility + Template Method | Template Method defines each handler's dispatch logic (check → handle or forward) |
| Command + Memento | Command performs operations; Memento provides state snapshot for operations whose reversal cannot be computed from the operation alone |
| Iterator + Visitor | Iterator traverses the aggregate; Visitor applies an operation to each element visited |
| Observer + Mediator | Observer for state-change notification; Mediator to coordinate subjects that interact with each other |
| Strategy + Template Method | Template Method provides the skeleton; Strategy fills in variable steps (evolution path from inheritance to composition) |
| Interpreter + Composite | Non-terminal expression classes are Composite nodes; Interpreter uses the composite structure to interpret sentences |
| Interpreter + Iterator | Iterator traverses the abstract syntax tree that Interpreter evaluates |
