---
name: design-pattern-selector
description: |
  Select the right GoF design pattern for a specific object-oriented design problem. Use when facing any of these situations: object creation inflexibility (too many concrete class references), tight coupling between classes, subclass explosion from trying to extend behavior, inability to modify a class you don't own, need to vary an algorithm or behavior at runtime, want to add operations to a stable class hierarchy without modifying it, need to decouple a sender from its receivers, need undo/redo or event notification, or any time someone asks "which design pattern should I use?", "is there a pattern for this?", or "how do I design this more flexibly?" Analyzes the problem through 6 complementary selection approaches — intent scanning, purpose/scope classification, variability analysis, redesign cause diagnosis, pattern relationship navigation, and category comparison — to produce a scored pattern recommendation with trade-off analysis.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/design-pattern-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [1]
tags: [design-patterns, object-oriented, gof, creational, structural, behavioral, refactoring, software-design]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "Design problem description from user — existing code, pain points, or a design scenario"
  tools-required: [Read, Write, TodoWrite]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, scanning it for context is helpful but not required."
---

# Design Pattern Selector

## When to Use

You've encountered a concrete object-oriented design problem and need a proven structural solution. This skill is appropriate when:

- You're designing a new component and want to get the structure right before writing code
- Existing code has a design smell — tightly coupled classes, a proliferating subclass hierarchy, or brittle object creation — and you want a pattern to address it
- You know roughly what you want (e.g., "something like a factory") but need to pick the right variant or confirm it fits
- You're reviewing someone else's code and want to identify what pattern(s) would improve it
- You want to understand trade-offs between two candidate patterns before committing

Before starting, verify:
- Do you have a description of the design problem, even informally? (Ask the user if not)
- Are you working with object-oriented design? (These patterns are OO-specific — they assume classes, objects, and inheritance)
- Is this about pattern *selection* (this skill) or pattern *implementation*? If the user already knows which pattern they want, move directly to the application process in Step 6

## Context & Input Gathering

### Required Context (must have before proceeding)

- **Problem description:** What design challenge are you solving? Even a rough description works — "I have a class that does too many things" or "I need multiple algorithms that clients can swap at runtime"
- **Design intent:** What should the result allow? (e.g., "swap implementations without changing clients", "add behaviors without modifying existing classes")

### Observable Context (gather from environment if available)

- **Existing code:** If a codebase is present, scan for the problematic class or module
  - Look for: large switch/if-else dispatch blocks (Cause 2), `new ConcreteClass()` proliferation (Cause 1), deep inheritance hierarchies (Cause 7), classes doing too many unrelated things (Cause 6)
  - Use `Grep` for `new `, `extends`, `implements` patterns to map existing structure
- **Prior patterns:** Check if related patterns are already in use — the new pattern should compose well with them
- **Language/framework:** Some patterns are idiomatically provided by the language (e.g., Java's `Iterator`, Python's context managers as a form of Template Method); note where native constructs already cover the need

### Sufficiency Check

You have enough to proceed if you can articulate: (a) what problem exists, and (b) what the solution should enable. If only (a) is known, the redesign-cause diagnosis (Step 3) will derive (b).

---

## Process

### Step 1: Frame the Problem

**ACTION:** Use `TodoWrite` to track the steps, then articulate the design problem in structured form.

**WHY:** Vague problems produce vague pattern matches. Forcing a structured framing surfaces the real constraints and eliminates patterns that technically apply but don't fit the actual need.

```
TodoWrite:
- [ ] Step 1: Frame the problem
- [ ] Step 2: Classify by purpose and scope
- [ ] Step 3: Diagnose redesign causes
- [ ] Step 4: Check variability requirements
- [ ] Step 5: Compare candidate patterns
- [ ] Step 6: Produce recommendation with trade-offs
```

Capture these four elements from the user's description:

| Element | Question to answer |
|---------|-------------------|
| **Context** | What type of system/component is this? |
| **Problem** | What is currently wrong or inflexible? |
| **Forces** | What constraints must the solution respect? (performance, simplicity, existing code) |
| **Goal** | What must the solution make possible? |

If any element is unclear, ask one targeted question before proceeding.

---

### Step 2: Classify by Purpose and Scope

**ACTION:** Narrow the candidate set using the purpose × scope classification matrix from `references/pattern-catalog.md`.

**WHY:** The 23 GoF patterns split cleanly into three purposes and two scopes. Getting this classification right eliminates 15–20 patterns immediately. It also forces precision about *what kind* of problem you're solving — a creation problem is fundamentally different from a communication problem.

**Decision rules:**

**Purpose:**
- **Creational** — the problem is about *how objects are created*. Objects are being created from concrete classes; you need flexibility in what gets created, or how.
- **Structural** — the problem is about *how classes or objects are composed*. You need a different interface, a flexible structure, or want to add responsibilities.
- **Behavioral** — the problem is about *how objects communicate and distribute work*. You need to decouple who initiates operations from who carries them out, or vary algorithms/state.

**Scope (within the chosen purpose):**
- **Class scope** — the relationship is fixed at compile-time via inheritance. Behavioral class patterns use inheritance to describe algorithms. Use when the variation can be determined at compile-time.
- **Object scope** — the relationship is dynamic at run-time via composition/delegation. Most patterns are object-scoped. Use when you need run-time flexibility.

**Output:** Identify 1–2 most likely purposes. If the problem spans purposes (e.g., creation inflexibility AND tight coupling), note both — you may need two patterns, or one pattern that addresses both.

---

### Step 3: Diagnose Redesign Causes

**ACTION:** Match the problem description against the 8 causes of redesign in `references/redesign-causes.md`.

**WHY:** The GoF identified that most design problems stem from dependencies that make change expensive. Each cause maps directly to the patterns that eliminate that specific dependency. This is the fastest path from "something is wrong" to "here are the patterns that fix it."

**Diagnostic questions to ask:**

1. Does the code create objects by naming concrete classes? → Cause 1 (object creation)
2. Is there hard-coded dispatch logic for handling requests? → Cause 2 (specific operations)
3. Is there platform-specific code mixed into business logic? → Cause 3 (platform dependence)
4. Does the client know too much about another object's internal structure? → Cause 4 (representation dependence)
5. Is an algorithm embedded in a class that should not own it? → Cause 5 (algorithmic dependence)
6. Can you not unit-test a class without instantiating many others? → Cause 6 (tight coupling)
7. Is the inheritance hierarchy growing combinatorially? → Cause 7 (subclassing for extension)
8. Does the class need changing but cannot be modified (no source, or too many dependents)? → Cause 8 (unmodifiable classes)

**Output:** Identify the 1–3 most relevant causes. Cross-reference with the patterns mapped to each cause — this produces a candidate shortlist.

---

### Step 4: Check Variability Requirements

**ACTION:** Consult `references/variability-table.md` to identify which patterns encapsulate the aspects of the design that must remain variable.

**WHY:** This is the "opposite" approach to cause diagnosis — instead of asking what is breaking, ask what must stay flexible. The variability table maps directly from "aspect I want to vary" to pattern. It catches cases where the user knows what they need to keep variable but cannot articulate the pain yet.

**Key question:** "What concept in this design must be encapsulated so it can change independently?"

Common variability needs and their patterns:

| I need to vary... | Candidates |
|-------------------|------------|
| Which algorithm runs | Strategy, Template Method |
| Which object handles a request | Chain of Responsibility |
| How objects notify each other | Observer |
| The interface exposed to clients | Adapter, Facade |
| An object's behavior by state | State |
| How and when a request executes | Command |
| The structure of a part-whole hierarchy | Composite |
| Responsibilities without subclassing | Decorator |
| How an object is located/accessed | Proxy |
| Which concrete class gets instantiated | Abstract Factory, Factory Method, Prototype |

**Output:** Add any new candidates surfaced by variability analysis to the shortlist from Step 3.

---

### Step 5: Compare Candidate Patterns

**ACTION:** For each candidate pattern on the shortlist (aim for 2–4), evaluate it against the problem using these lenses:

**WHY:** Multiple patterns often address the same problem. The right choice depends on trade-offs specific to this context — complexity budget, run-time flexibility needs, relationship to existing code, and what the solution must remain open to in the future.

**Evaluation lens for each candidate:**

| Lens | Question |
|------|----------|
| **Fit** | Does the pattern's intent directly address the core problem? |
| **Scope match** | Does it operate at class or object scope — which is right here? |
| **Complexity cost** | How many new classes/interfaces does it introduce? Is that justified? |
| **Run-time flexibility** | Does it need to vary at run-time or compile-time? |
| **Composition** | Does it work with patterns already in use, or conflict? |
| **Over-engineering risk** | Does the flexibility it provides actually apply to this problem's future? |

**Pattern relationship check:** Consult the "Pattern Relationships" section in `references/pattern-catalog.md` to identify whether candidates are alternatives (choose one), complements (use both), or sequenced (use first one, then the other as the system evolves).

**Output:** A ranked shortlist with a 1–2 sentence rationale and a key trade-off noted for each.

---

### Step 6: Produce Recommendation

**ACTION:** Deliver a structured recommendation in the following format, then offer to walk through the 7-step application process if the user wants to implement it.

**WHY:** A recommendation without trade-offs is advice without accountability. The user needs to understand not just what to do but why this pattern beats the alternatives, and what they give up. This enables informed commitment rather than cargo-culting.

**Recommendation format:**

```
## Pattern Recommendation: [Pattern Name]

**Category:** [Creational / Structural / Behavioral] — [Class / Object] scope

**Why this pattern:** [1–2 sentences connecting the pattern's intent to the specific problem]

**What it enables:** [What becomes possible that wasn't before]

**Key trade-off:** [What you give up or what additional complexity you accept]

**Alternative considered:** [Runner-up pattern] — [Why it was not chosen]

**Patterns to combine with:** [Any complementary patterns, if applicable]
```

**If the user wants to implement:** Walk through the 7-step application process:

1. **Read the pattern** — focus on Applicability and Consequences sections to confirm fit
2. **Study the structure** — understand all participants (classes/objects) and how they collaborate
3. **Review sample code** — see a concrete implementation to understand how it works
4. **Name participants contextually** — rename pattern roles to application-specific names (e.g., `LayoutStrategy` not just `Strategy`)
5. **Define the classes** — declare interfaces, establish inheritance, identify existing classes the pattern will affect
6. **Name operations** — use application-specific names for pattern operations; follow consistent naming conventions (e.g., `Create-` prefix for factory methods)
7. **Implement** — write the operations, following hints in the pattern's Implementation section

---

## Examples

### Example 1: Subclass Explosion for UI Rendering

**Scenario:** A UI library has a `Button` class. Over time, the team added `RoundButton`, `FlatButton`, `DarkRoundButton`, `LightFlatButton` — 12 subclasses for 3 shapes × 4 themes, and it keeps growing.

**Trigger:** "Our button hierarchy is exploding. Every new theme or shape doubles the subclass count."

**Process:**
- Step 2: Structural (composition problem), Object scope (need run-time flexibility)
- Step 3: Cause 7 — extending functionality by subclassing
- Step 4: Need to vary "responsibilities of an object without subclassing" → Decorator; also "implementation of an object" → Bridge
- Step 5: Decorator adds responsibilities dynamically but doesn't separate two orthogonal dimensions. Bridge separates abstraction (shape) from implementation (theme) — exactly the two dimensions causing explosion.

**Output:**
```
## Pattern Recommendation: Bridge

**Category:** Structural — Object scope

**Why this pattern:** Bridge separates the Button abstraction (shape: Round, Flat)
from its implementation (theme: Dark, Light) into two independent hierarchies.
Adding a new theme requires one new class, not N new subclasses.

**What it enables:** Shape and theme can vary independently. 3 shapes × 4 themes = 7 classes total, not 12.

**Key trade-off:** Increases design complexity upfront; adds one level of indirection
(button delegates to its renderer). Justified when both dimensions are genuinely
expected to grow.

**Alternative considered:** Decorator — works well for adding single responsibilities
but doesn't solve two orthogonal variation axes as cleanly as Bridge.
```

---

### Example 2: Hardcoded Payment Processing

**Scenario:** An e-commerce checkout class contains a large `if/else` block selecting between Stripe, PayPal, and bank transfer logic. Adding a new payment method means modifying the checkout class and its tests.

**Trigger:** "Every new payment provider requires touching the core checkout code."

**Process:**
- Step 2: Behavioral (communication/delegation problem), Object scope
- Step 3: Cause 2 — dependence on specific operations (hard-coded request handling)
- Step 4: Need to vary "an algorithm" → Strategy
- Step 5: Strategy replaces the `if/else` dispatch with a family of interchangeable payment-processing objects. Command could encapsulate payment as an undoable request — but undo is not required here and adds unnecessary complexity.

**Output:**
```
## Pattern Recommendation: Strategy

**Category:** Behavioral — Object scope

**Why this pattern:** Strategy replaces the dispatch block with a PaymentStrategy
interface. Each provider (Stripe, PayPal, bank transfer) is a ConcreteStrategy.
Checkout receives a strategy object at runtime and delegates payment to it.

**What it enables:** New payment providers are new classes, not modifications to Checkout.
Checkout can be tested with a MockPaymentStrategy.

**Key trade-off:** Clients must know which strategy to instantiate. If selection logic
is complex, pair with Abstract Factory to manage strategy creation.

**Alternative considered:** Command — adds request queuing and undo capability not
needed here; over-engineers this use case.

**Patterns to combine with:** Abstract Factory (for strategy instantiation by region/config)
```

---

### Example 3: Cannot Modify a Third-Party Logger

**Scenario:** A team is integrating a third-party analytics library whose `Logger` class has an interface incompatible with the `IEventTracker` interface the rest of the application uses. Source code is unavailable.

**Trigger:** "We need to use this library's logger but it doesn't match our interface and we can't change it."

**Process:**
- Step 2: Structural (interface composition), Object scope
- Step 3: Cause 8 — inability to alter classes conveniently
- Step 4: Need to vary "interface to an object" → Adapter
- Step 5: Adapter is the canonical solution. Decorator adds behavior but requires the same interface. Facade simplifies a subsystem but doesn't translate interfaces.

**Output:**
```
## Pattern Recommendation: Adapter

**Category:** Structural — Object scope

**Why this pattern:** An Adapter class wraps the third-party Logger and implements
IEventTracker, translating calls between the two interfaces. The rest of the
application only ever sees IEventTracker.

**What it enables:** Library can be swapped for a different provider by swapping the
Adapter, with zero changes to application code.

**Key trade-off:** Each new method in IEventTracker requires a corresponding
translation in the Adapter. If the interfaces diverge significantly, the Adapter
becomes a maintenance burden — consider whether the interfaces can be aligned upstream.

**Alternative considered:** Facade — would simplify the logger API but cannot make it
implement IEventTracker.
```

---

## Key Principles

- **Start from the problem, not the pattern.** The most common mistake is picking a familiar pattern and forcing it onto a problem. The 6-step process starts with the problem and narrows to the pattern. WHY: Pattern-first thinking produces over-engineered designs with unnecessary indirection.
- **Patterns introduce indirection — only add it when needed.** Every pattern adds a layer of abstraction. Apply only when the flexibility it affords is genuinely required. WHY: The GoF authors warn explicitly against indiscriminate pattern application (p41).
- **Use the redesign causes as a diagnostic, not just a lookup.** The 8 causes of redesign are symptoms, not just labels. When reviewing code, check whether the system exhibits any of these causes — that reveals which patterns to consider. WHY: Symptom-driven selection finds patterns you wouldn't think to look for.
- **Table 1.2 is the reverse lookup.** When you know what must stay flexible, Table 1.2 tells you which pattern encapsulates that aspect. When you know what's breaking, the redesign causes table tells you which pattern prevents that fragility. Use both. WHY: Two complementary angles catch more candidates than either alone.
- **Patterns evolve.** Designs often start with Factory Method and evolve toward Abstract Factory or Prototype as flexibility needs emerge. Don't over-design from the start — pick the simplest pattern that solves the current problem and know the evolution path.

## Reference Files

| File | Contents |
|------|----------|
| `references/pattern-catalog.md` | Table 1.1: all 23 patterns by purpose × scope, one-line intents, pattern relationships |
| `references/variability-table.md` | Table 1.2: what each pattern lets you vary independently |
| `references/redesign-causes.md` | 8 causes of redesign with symptoms and mapped patterns |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
