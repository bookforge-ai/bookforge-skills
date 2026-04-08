---
name: behavioral-pattern-selector
description: |
  Choose the right behavioral design pattern from the 11 GoF behavioral patterns. Use when someone asks "how do I make this algorithm swappable?", "should I use Strategy or State?", "how do I decouple senders from receivers?", "what's the difference between Observer and Mediator?", "how do I add undo/redo?", "how do I traverse a collection without exposing its internals?", or "how do I add operations to classes I can't modify?" Also use when you see switch statements selecting between algorithms, tightly coupled event handlers, objects that change behavior based on state, or request-handling logic that should be distributed across a chain. Analyzes via two taxonomies — what aspect to encapsulate as an object (algorithm, state, protocol, traversal) and how to decouple senders from receivers (Command, Observer, Mediator, Chain of Responsibility) — with explicit trade-offs for each choice.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/behavioral-pattern-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - design-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [5]
tags: [design-patterns, behavioral, gof, strategy, state, observer, command, chain-of-responsibility, mediator, template-method, iterator, visitor, interpreter, memento]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "A description of the behavioral problem — how objects communicate, how algorithms vary, or how responsibilities should be distributed"
  tools-required: [TodoWrite]
  tools-optional: [Read, Grep]
  mcps-required: []
  environment: "Any agent environment. A codebase is helpful but not required."
---

# Behavioral Pattern Selector

## When to Use

You have identified that a problem is behavioral — it concerns how objects communicate, distribute responsibilities, or vary their actions — and need to pick the right one of the 11 GoF behavioral patterns. This skill is appropriate when:

- You have algorithms that vary across contexts and clients should swap them independently
- An object must change its behavior radically when its internal state changes
- You need to issue requests without knowing the receiver or the operation in advance
- Multiple objects are communicating in complex, entangled ways and need decoupling
- You need to traverse or operate on a collection without exposing its internals
- You want to add operations to a stable class hierarchy without modifying it
- You need to save and restore an object's internal state without breaking encapsulation
- You want to define a grammar for simple sentences and interpret them
- You are deciding among behavioral patterns and want an explicit trade-off comparison

Before starting, confirm:
- Is the problem genuinely behavioral (communication/algorithm), not creational (object construction) or structural (interface composition)? If unsure, invoke `design-pattern-selector` first for purpose classification.
- Do you have at least a rough description of what the system needs to do differently — even informally?

---

## Context & Input Gathering

### Required Context (must have before proceeding)

- **Behavioral problem description:** What interaction, communication, or algorithmic variability challenge are you solving? Even a rough description works — "objects notify each other in a tangled web" or "I have switch statements picking between algorithms."
- **What varies or needs decoupling:** Identify whether it's an algorithm, state-dependent behavior, communication protocol, or request handling that needs flexibility.

### Observable Context (gather from environment)

- **Existing codebase:** If available, scan for behavioral smell signals — switch/if-else chains on type, tightly coupled event handlers, state-dependent conditionals, hard-coded request routing.
- **Related patterns already in use:** Check if creational or structural patterns are already applied — they constrain which behavioral patterns compose well.

### Sufficiency
```
SUFFICIENT: problem description + what varies identified
PROCEED WITH DEFAULTS: rough problem description only (skill will help classify)
MUST ASK: no behavioral problem articulated at all
```

## Process

### Step 1: Set Up Tracking and Characterize the Problem

**ACTION:** Use `TodoWrite` to track progress, then capture the behavioral problem in structured form.

**WHY:** Behavioral patterns share surface similarities — Strategy, State, and Template Method all vary an algorithm, but for fundamentally different reasons. Without explicitly articulating *what* varies and *why*, you risk picking a pattern that fits the shape of the problem but not the intent. Forcing structured framing surfaces the distinction.

```
TodoWrite:
- [ ] Step 1: Characterize the behavioral problem
- [ ] Step 2: Apply Taxonomy 1 — What aspect to encapsulate
- [ ] Step 3: Apply Taxonomy 2 — Sender-receiver decoupling (if applicable)
- [ ] Step 4: Resolve ambiguous pairs with differentiating questions
- [ ] Step 5: Produce recommendation with trade-offs
```

Capture these elements from the user's description:

| Element | Question to answer |
|---------|-------------------|
| **What varies** | What behavior or aspect is expected to change across contexts or time? |
| **Who decides** | Does the client choose, or does the object itself decide based on state? |
| **Coupling concern** | Must the sender of a request be decoupled from who handles it? |
| **Stability** | Is the object structure stable but operations on it need to grow? |
| **Lifecycle** | Does the varying thing need to exist independently (be passed around, stored, undone)? |

If more than one element is unclear, ask one targeted question and wait for a response before continuing.

---

### Step 2: Apply Taxonomy 1 — What Aspect to Encapsulate

**ACTION:** Match the problem against the encapsulation taxonomy. Identify which aspect of the program is expected to change and therefore needs its own object.

**WHY:** The defining theme of behavioral patterns is *encapsulating variation*. Each pattern names the thing that changes and lifts it into a dedicated object. If you can identify what that thing is, you can identify the pattern — because the pattern is literally named for it. Skipping this step leads to pattern matching by feel rather than by structure.

**Encapsulation taxonomy:**

| Encapsulated aspect | Pattern | The object holds... |
|---------------------|---------|---------------------|
| An algorithm | **Strategy** | The interchangeable computation — clients choose which strategy to install |
| State-dependent behavior | **State** | Behavior for one state of a context — object self-transitions at runtime |
| Inter-object protocol | **Mediator** | The communication rules between a group of colleague objects |
| Traversal method | **Iterator** | The logic for stepping through an aggregate's elements without exposing structure |
| A request (invocation) | **Command** | One operation — parameterized, deferrable, undoable, loggable |
| A state snapshot | **Memento** | A private checkpoint of an object's internals, opaque to all but the originator |
| Operations on a structure | **Visitor** | A family of operations across an object structure — defined outside the classes |

**Three patterns that do not fit this taxonomy** (they work at the class or communication level):

| Pattern | What it does instead |
|---------|---------------------|
| **Template Method** | Uses inheritance, not encapsulation in a separate object — a superclass skeleton calls abstract steps that subclasses fill in |
| **Observer** | Encapsulates a dependency relationship, not a discrete aspect — subjects and observers cooperate to maintain a constraint |
| **Chain of Responsibility** | Distributes handling across an open-ended chain — no single encapsulating object |
| **Interpreter** | Represents a grammar as a class hierarchy — each grammar rule is a class, not a standalone encapsulated object |

**Output:** Identify the encapsulated aspect and the candidate pattern(s) it points to. If the problem description mentions both an algorithm and state-driven behavior, or both communication and a protocol object, flag both candidates and proceed to Step 4.

---

### Step 3: Apply Taxonomy 2 — Sender-Receiver Decoupling (If Applicable)

**ACTION:** If the problem involves decoupling who sends a request from who handles it, evaluate the four decoupling patterns against each other.

**WHY:** Command, Observer, Mediator, and Chain of Responsibility all decouple senders from receivers, but with very different structures and trade-offs. Choosing the wrong one produces either the right decoupling for the wrong granularity (Observer when you need Command) or centralized logic that makes the system harder to understand (Mediator when Observer's distributed model is sufficient). This taxonomy makes the choice explicit.

**Apply only if** the problem includes any of these:
- "The sender should not know who handles the request"
- "Multiple objects need to react to a change"
- "Objects are too tightly coupled to each other"
- "Requests should be queued, logged, or undone"

**Decoupling comparison:**

| Pattern | Coupling model | Cardinality | Receiver identity | Key trade-off |
|---------|---------------|-------------|-------------------|---------------|
| **Command** | Object binding — command holds reference to receiver | 1 sender : 1 receiver (per command) | Known at command-creation time; hidden from invoker | Invoker stays decoupled; a subclass is nominally required per sender-receiver pair |
| **Observer** | Interface-based — subject notifies any attached observer | 1 subject : many observers, dynamic | Not known to subject; observers self-register | Promotes loose coupling and fine-grained reuse; communication flow is harder to trace |
| **Mediator** | Centralized — all colleagues route through mediator | Many senders : many receivers via one hub | Hidden from colleagues; mediator knows all | Simplifies colleague interaction; mediator itself can become a complexity bottleneck |
| **Chain of Responsibility** | Chain forwarding — request walks a linked list of handlers | 1 sender : implicit receiver (first willing handler) | Not known to sender; determined at runtime by chain order | Very loose coupling; **warning: request may go unhandled if no handler claims it** |

**Decision rules:**

- Need **undo/redo**, **queuing**, or **logging of requests**? → Command (the request is a first-class object)
- One object changes and **an unknown number of others must react**? → Observer (broadcast, data dependency)
- **Many objects interact in complex ways** and the interaction logic should live in one place? → Mediator (centralize the protocol)
- **Multiple candidate handlers exist** and the right one is determined at runtime, but any one is sufficient? → Chain of Responsibility (but add a fallback handler to prevent silent drops)

**Output:** If this taxonomy applies, add the appropriate decoupling pattern as a candidate or as a confirmation of the candidate from Taxonomy 1.

---

### Step 4: Resolve Ambiguous Pattern Pairs

**ACTION:** If two or more candidates remain after Steps 2–3, apply the differentiating questions for the relevant pair.

**WHY:** Several behavioral patterns share structural similarities. Strategy and State have identical class diagrams. Template Method and Strategy both vary algorithms. Without asking the right differentiating question, you will correctly identify the problem category but pick the wrong pattern.

**Pair: Strategy vs. State**

Both encapsulate behavior that can be swapped at runtime via a context object. The difference is *who initiates the swap and why*:

| Question | Strategy → if... | State → if... |
|----------|-----------------|---------------|
| Who changes the behavior? | The **client** installs a strategy explicitly | The **context object itself** transitions to a new state based on internal logic |
| Do the concrete variants know about each other? | No — strategies are independent | Yes — state objects often initiate transitions to sibling states |
| Is the variation about selecting an algorithm? | Yes — same interface, different computation | No — about representing a lifecycle that drives behavior |

**Pair: Template Method vs. Strategy**

Both vary an algorithm, but via opposite mechanisms:

| Question | Template Method → if... | Strategy → if... |
|----------|------------------------|-----------------|
| How is variation expressed? | **Inheritance** — a subclass overrides abstract steps | **Composition** — a context object holds a replaceable strategy |
| Can the algorithm be swapped at runtime? | No — fixed at class definition time | Yes — a different strategy object can be installed at any time |
| Do you control the superclass? | Yes — you define the skeleton | Doesn't matter — client provides the algorithm |

**Pair: Observer vs. Mediator**

Both decouple objects from direct references, but in opposite directions:

| Question | Observer → if... | Mediator → if... |
|----------|-----------------|-----------------|
| Where does communication logic live? | **Distributed** — observers and subjects cooperate to maintain the constraint | **Centralized** — the mediator owns all routing logic |
| What is the coupling concern? | One object changes; **unknown others must react** | Many objects interact; **the interactions themselves are complex** |
| What is more important? | Reusability of subjects and observers | Understandability of the overall interaction flow |

**Pair: Command vs. Chain of Responsibility**

Both issue a request without the sender knowing the receiver, but via different mechanisms:

| Question | Command → if... | Chain of Responsibility → if... |
|----------|-----------------|---------------------------------|
| Is there a known receiver at request-creation time? | Yes — command holds a reference to its receiver | No — the receiver is determined by walking the chain |
| Does the request need to be stored, undone, or replayed? | Yes — Command is a first-class object | No — the request is transient |
| Is exactly one handler expected? | Yes | Not necessarily — could be zero (silent drop) or one |

**Output:** A single confirmed pattern, or at most two if the problem genuinely requires both (e.g., Command + Chain of Responsibility is a valid composition — the chain uses Command objects as the request representation).

---

### Step 5: Produce Recommendation with Trade-offs

**ACTION:** Deliver the recommendation in the format below. Include the taxonomy reasoning that led to it, the key trade-off, and the runner-up pattern with why it was not chosen.

**WHY:** A recommendation without reasoning is a guess. The user needs to understand the taxonomy path that produced the choice — both to validate it and to apply the pattern correctly. The trade-off section prevents misapplication in edge cases.

**Recommendation format:**

```
## Pattern Recommendation: [Pattern Name]

**Category:** Behavioral — [Class / Object] scope

**Encapsulation taxonomy:** [What aspect is being encapsulated as an object]
**Decoupling taxonomy:** [If applicable — which sender-receiver model applies]

**Why this pattern:** [1–2 sentences connecting the pattern's intent to the specific problem]

**What it enables:** [What becomes possible that wasn't before]

**Key trade-off:** [What complexity or constraint is introduced]

**Warning (if applicable):** [Chain of Responsibility: silent drop risk; Mediator: bottleneck risk; etc.]

**Alternative considered:** [Runner-up pattern] — [Why it was not chosen]

**Patterns to combine with:** [Any complementary patterns]
```

**Common combinations:**

- **Chain of Responsibility + Command** — chain uses Command objects so requests can be logged or replayed; Template Method defines handler dispatch logic
- **Observer + Mediator** — Observer for subject-observer notification; Mediator to coordinate the subjects themselves
- **Strategy + Template Method** — Template Method defines the algorithm skeleton; Strategy fills in variable steps via composition (evolution path when inheritance becomes limiting)
- **Iterator + Visitor** — Iterator traverses the aggregate; Visitor applies an operation to each element
- **Command + Memento** — Command executes operations; Memento provides state snapshots to support undo

---

## Examples

### Example 1: Order Processing with Multiple Tax Algorithms

**Scenario:** An e-commerce system computes tax differently depending on region (US federal, EU VAT, Canadian GST). The tax logic is embedded in the `Order` class as a large `if/else` block. A new region is coming and the team does not want to keep modifying `Order`.

**Trigger:** "We have different tax rules per region and the order class keeps getting bigger every time we add one."

**Process:**
- Step 2 (Taxonomy 1): What varies is the *algorithm* for tax computation. Clients (or configuration) choose which algorithm to apply. → Strategy
- Step 3 (Taxonomy 2): No sender-receiver decoupling concern — Order calculates tax directly.
- Step 4: Strategy vs. State? The variation is client-selected (region at order creation), not self-transitioning behavior. Confirmed: Strategy.

**Output:**
```
## Pattern Recommendation: Strategy

**Category:** Behavioral — Object scope

**Encapsulation taxonomy:** Algorithm (tax computation rule) is extracted into a TaxStrategy object

**Why this pattern:** Strategy replaces the if/else dispatch with a TaxStrategy
interface. Each region (USTaxStrategy, EUVATStrategy, CAGSTStrategy) is a
ConcreteStrategy. Order holds a reference and delegates to it.

**What it enables:** New regions are new TaxStrategy subclasses — Order is never
modified. Strategies can be tested independently.

**Key trade-off:** Clients must know which strategy to instantiate; this knowledge
must come from somewhere (configuration, factory). If strategy selection is itself
complex, pair with Abstract Factory.

**Alternative considered:** Template Method — would require subclassing Order for
each region (OrderForUS, OrderForEU), which tightly couples the algorithm variation
to the order lifecycle. Strategy via composition is cleaner.

**Patterns to combine with:** Abstract Factory (to instantiate the correct strategy
based on region configuration)
```

---

### Example 2: UI Form with Enable/Disable Logic Across States

**Scenario:** A wizard dialog has three states: empty (all fields disabled except the first), partial (some fields enabled, Submit disabled), and complete (Submit enabled). Currently, every button-click handler contains the same conditional: "if state == X, enable Y, disable Z." The logic is duplicated across 12 event handlers.

**Trigger:** "Every event handler has to know what state the dialog is in. Adding a new state means touching all 12 handlers."

**Process:**
- Step 2 (Taxonomy 1): What varies is *behavior per state* — not a client-selected algorithm, but self-determined transitions. The dialog itself decides when to move from partial to complete. → State
- Step 4: Strategy vs. State? The dialog transitions itself (the "partial" state knows when to transition to "complete" based on field validation). No external client selects the behavior. Confirmed: State.

**Output:**
```
## Pattern Recommendation: State

**Category:** Behavioral — Object scope

**Encapsulation taxonomy:** State-dependent behavior — each wizard state (EmptyState,
PartialState, CompleteState) encapsulates its own enable/disable logic

**Why this pattern:** Each state object handles the event and applies the correct
enable/disable rules for that state. The wizard context delegates all event handling
to its current state object. Transitions (EmptyState → PartialState) are initiated by
the state objects themselves when conditions are met.

**What it enables:** Adding a new state is a new class — existing handlers are not
touched. The 12 duplicated conditionals collapse into the state objects that own them.

**Key trade-off:** State objects may need access to the context to initiate transitions,
introducing some coupling. The number of classes grows by one per state.

**Alternative considered:** Strategy — the behavior here is not client-selected; the
dialog self-transitions. Strategy would require the external caller to manage state
changes, which belongs inside the dialog lifecycle.
```

---

### Example 3: Audit Log for Spreadsheet Operations

**Scenario:** A spreadsheet application must support unlimited undo/redo for cell edits, formula applications, and formatting changes. Operations may take several seconds. The team also wants a log of all executed operations for crash recovery.

**Trigger:** "We need full undo/redo and also want to replay operations from a log after a crash."

**Process:**
- Step 2 (Taxonomy 1): The *request itself* (each operation) needs to be a first-class object — stored, reversed, and replayed. → Command
- Step 3 (Taxonomy 2): Sender-receiver decoupling: the UI (invoker) must not know the cell/formula/formatting receiver details. Command is the binding object. 1:1 per operation. Confirmed: Command.
- Step 4: Command vs. Chain? The receiver is known at command-creation time (the specific cell being edited). No chain needed. Command confirmed.

**Output:**
```
## Pattern Recommendation: Command

**Category:** Behavioral — Object scope

**Encapsulation taxonomy:** Request (each operation) is encapsulated as a Command
object with Execute() and Unexecute() operations

**Decoupling taxonomy:** 1 invoker (toolbar/keyboard) : 1 receiver (cell/formula/formatter)
per command — invoker stays decoupled from receiver details

**Why this pattern:** Each operation (EditCellCommand, ApplyFormulaCommand,
FormatRangeCommand) is an object. Execute() applies it; Unexecute() reverses it.
The history list holds executed commands. Undo traverses it backward; redo forward.
Crash recovery replays the log by re-executing stored commands.

**What it enables:** Unlimited undo/redo with no special logic in the UI. Crash
recovery by replaying the command log. Macro recording by composing commands into
MacroCommands.

**Key trade-off:** Each unique operation requires a Command subclass. If operations
are highly varied (many receiver types), this produces many classes. Closures or
lambdas can replace subclasses in languages that support first-class functions.

**Alternative considered:** Memento — captures state snapshots for undo but stores
full state copies, which is expensive for large spreadsheets. Command stores only the
delta (what changed), which is far more efficient.

**Patterns to combine with:** Memento (for operations whose reversal cannot be
computed — store a snapshot as part of the command's undo data)
```

---

## Key Principles

- **Two taxonomies, not one.** Behavioral patterns can be classified by what they encapsulate (algorithm, state, protocol, traversal) AND by how they decouple senders from receivers. Use both lenses — one narrows the candidate set, the other confirms the choice. WHY: Patterns that look similar under one taxonomy (Strategy vs State) are clearly different under the other.
- **Strategy and State have identical structure but opposite intents.** Strategy varies the algorithm while context stays the same. State varies the context's behavior when its internal state changes. If the "which object to delegate to" decision is made by the client, it's Strategy. If it's made by the context itself (state transitions), it's State. WHY: This is the single most confused pair in the behavioral catalog.
- **Observer distributes, Mediator centralizes.** Both decouple interacting objects. Observer promotes finer-grained, more reusable classes but makes communication flow harder to trace. Mediator makes flow explicit but can become a monolith. WHY: Choosing wrong creates either untraceable event spaghetti (Observer misuse) or a god-object mediator.
- **Chain of Responsibility has no delivery guarantee.** A request can fall off the end of the chain unhandled, silently. Always include a catch-all handler or an assertion that the chain is complete. WHY: Silent request drops are the hardest bugs to diagnose.

## Reference Files

| File | Contents |
|------|----------|
| `references/behavioral-comparison.md` | All 11 patterns: applicability summary, encapsulation type, decoupling role, key trade-offs, and confusable pairs |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-design-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
