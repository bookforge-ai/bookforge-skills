---
name: structural-pattern-selector
description: |
  Choose the right structural design pattern (Adapter, Bridge, Composite, Decorator, Facade, Flyweight, or Proxy) for a structural design problem. Use when you need to adapt interfaces between incompatible classes, decouple an abstraction from its implementation so both can vary independently, build part-whole hierarchies where individual objects and compositions are treated uniformly, add responsibilities to objects dynamically without subclassing, simplify access to a complex subsystem, share large numbers of fine-grained objects efficiently, or control and mediate access to another object. Disambiguates commonly confused patterns: Adapter vs Bridge (timing — after design vs before design), Composite vs Decorator vs Proxy (intent — structure vs embellishment vs access control, recursion pattern). Also use when someone asks "should I use Adapter or Bridge?", "what's the difference between Decorator and Proxy?", "when should I use Facade vs Adapter?", or "do I need Flyweight here?"
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/structural-pattern-selector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - design-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [4]
tags: [design-patterns, structural-patterns, adapter, bridge, composite, decorator, facade, flyweight, proxy, object-oriented, gof, disambiguation]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "A structural design problem description — the design challenge, existing code pain points, or a scenario requiring structural composition"
  tools-required: [Read, Write, TodoWrite]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. Scanning an existing codebase for context is helpful but not required."
---

# Structural Pattern Selector

## When to Use

You have a **structural** design problem — one about how classes or objects are composed to form larger structures. This skill applies when:

- Two classes need to work together but have incompatible interfaces
- An abstraction and its implementation are tightly bound and you need them to vary independently
- You need to build tree-like hierarchies where individual items and groups behave the same way
- You need to add capabilities to objects at runtime without subclassing
- A complex subsystem needs a simpler unified entry point
- You're creating large numbers of similar lightweight objects and memory is a concern
- You need a stand-in, gateway, or access-control layer in front of another object
- You're unsure which structural pattern fits, especially between Adapter/Bridge or Composite/Decorator/Proxy

**Not this skill if:** The problem is about object creation (use a creational pattern) or communication/algorithms between objects (use a behavioral pattern). If you haven't yet classified the problem as structural, invoke `design-pattern-selector` first.

## Context & Input Gathering

### Required Context (must have before proceeding)

- **Problem description:** What structural challenge exists? A rough description is fine — "I need these two incompatible classes to work together" or "I'm adding logging/auth to objects without changing them"
  - Check prompt for: words like "interface mismatch", "add responsibility", "part-whole", "subsystem", "access control", "share objects", "decouple abstraction"
  - If missing, ask: "Describe the structural design problem you're facing — what's currently rigid, mismatched, or needs composing?"

- **Design timing:** Is this a new design (before classes exist) or an integration problem (classes already designed and built)?
  - This is the single most important disambiguator between Adapter and Bridge
  - Check prompt for: "existing", "third-party", "can't modify", "library" → likely post-design; "designing now", "new system", "will vary" → likely pre-design
  - If unclear, ask: "Are the classes you're working with already designed and built, or are you designing the structure from scratch?"

### Observable Context (gather from environment if available)

- **Existing code:** If a codebase is available, scan for structural signals:
  - `implements`/`extends` mismatches between incompatible classes → Adapter candidate
  - Deep class hierarchies (subclass count growing combinatorially) → Bridge candidate
  - Tree-structured data with uniform operations → Composite candidate
  - Wrapper classes that add behavior before/after delegation → Decorator candidate
  - A "manager" or "controller" class that forwards to many subsystem classes → Facade candidate
  - Massive collections of identical-except-for-position objects (particles, characters, icons) → Flyweight candidate
  - Classes that gate, cache, or delay access to another class → Proxy candidate

### Default Assumptions

- Object scope (composition) preferred over class scope (inheritance) unless inheritance is clearly appropriate — object patterns are more flexible at runtime
- When timing is ambiguous, lean toward asking — the Adapter vs Bridge decision hinges entirely on this

---

## Process

### Step 1: Set Up Tracking and Frame the Problem

**ACTION:** Use `TodoWrite` to track steps, then extract the core structural problem.

**WHY:** Structural problems often present with symptoms ("this class is too hard to change") rather than causes ("these two abstractions are coupled"). Forcing a structured frame up front prevents jumping to the wrong pattern before the actual problem is clear.

```
TodoWrite:
- [ ] Step 1: Frame the problem
- [ ] Step 2: Classify the structural intent
- [ ] Step 3: Apply the disambiguation decision tree
- [ ] Step 4: Check pattern-specific applicability conditions
- [ ] Step 5: Produce recommendation with rationale
```

Capture these elements from the description:

| Element | Question to answer |
|---------|-------------------|
| **What exists** | What classes/objects are already in play? |
| **What is wrong** | What is currently rigid, mismatched, or inefficient? |
| **What must be possible** | What should the design enable that isn't possible now? |
| **Timing** | Are these classes already designed, or is this a fresh design? |

---

### Step 2: Classify the Structural Intent

**ACTION:** Identify which of the seven structural intents best matches the problem.

**WHY:** Each structural pattern solves a fundamentally different structural problem. Getting the intent right eliminates 5–6 patterns immediately. The intent is the core discriminator — not the implementation mechanics.

**Structural intent map:**

| Intent | Core problem | Pattern |
|--------|-------------|---------|
| **Interface translation** | Two existing, incompatible interfaces must collaborate | Adapter |
| **Abstraction/implementation decoupling** | An abstraction must vary independently of how it is implemented | Bridge |
| **Part-whole uniformity** | Individual objects and compositions must be treated identically | Composite |
| **Dynamic responsibility addition** | Responsibilities must be added/removed at runtime without subclassing | Decorator |
| **Subsystem simplification** | A complex set of classes needs one simplified entry point | Facade |
| **Instance sharing for efficiency** | Large numbers of fine-grained objects must share state to reduce memory cost | Flyweight |
| **Controlled/mediated access** | Access to an object must be gated, deferred, or monitored | Proxy |

**OUTPUT:** Identify the 1–2 most matching intents. If two intents match, proceed to Step 3 for disambiguation.

---

### Step 3: Apply the Disambiguation Decision Tree

**ACTION:** For each commonly confused pair, apply the specific discriminator below.

**WHY:** The structural patterns share implementation mechanics (all use indirection, all involve forwarding calls) but differ sharply in intent and timing. Using the wrong one produces structurally valid but semantically wrong code — Bridge code that should have been Adapter won't adapt; Proxy code that should have been Decorator won't stack.

#### Adapter vs Bridge

**The single question that separates them:**

> "Were the classes being connected designed independently before this problem arose, or are you designing the structure now so they can vary independently later?"

- **Answer: already designed, now incompatible** → **Adapter**
  - Adapter makes things work *after* they're designed. The coupling was unforeseen.
  - The goal is to make two independently developed classes collaborate without rewriting either.
  - The interface you're adapting *to* already exists and is owned by someone else.

- **Answer: designing now, need future flexibility** → **Bridge**
  - Bridge makes things work *before* they're designed. The separation is intentional.
  - The goal is to keep an abstraction hierarchy independent from its implementation hierarchy so both can grow without a subclass explosion.
  - You are designing the structure up-front knowing it will need to vary in two dimensions.

**Facade vs Adapter distinction:** Facade is sometimes described as an adapter for a set of objects. The difference: Facade defines a *new* interface over an existing subsystem. Adapter *reuses* an existing interface by making another class conform to it. If clients already know the target interface and you need another class to satisfy it → Adapter. If there is no target interface and you're creating a convenient entry point → Facade.

#### Composite vs Decorator vs Proxy

These three share a structural mechanism: they all wrap another object and forward calls. Differentiate by intent and recursion:

| Question | Composite | Decorator | Proxy |
|----------|-----------|-----------|-------|
| **What is the purpose?** | Represent part-whole hierarchy (structure) | Add responsibilities dynamically (embellishment) | Control or mediate access (access management) |
| **Does it hold multiple children?** | Yes — a Composite holds a list of Components | No — a Decorator wraps exactly one Component | No — a Proxy references exactly one Subject |
| **Is recursive composition essential?** | Yes — the pattern requires it (tree structure) | Yes — decorators can be nested (stacked behaviors) | No — the proxy-subject relationship is static and one-to-one |
| **Does the wrapper change behavior?** | Yes, by aggregating children | Yes, by adding before/after behavior | Sometimes (protection, logging), but the *subject* defines core behavior |
| **Known at compile time?** | Determined at runtime (tree built dynamically) | Determined at runtime (decoration can be applied/removed) | Often known at compile time (proxy-subject relationship is fixed) |

**Quick diagnostic:**
- "I need to build a tree of objects where nodes and leaves behave the same" → **Composite**
- "I need to add logging/auth/caching to objects at runtime without changing them" → **Decorator**
- "I need a stand-in because the real object is remote, expensive to create, or needs access control" → **Proxy**

---

### Step 4: Check Pattern-Specific Applicability Conditions

**ACTION:** For the leading candidate, verify its specific applicability conditions are met. For Flyweight, ALL five conditions must be true — it is an AND-gate, not an OR-gate.

**WHY:** Each pattern has conditions that make it inappropriate even when the intent matches. Verifying these prevents applying a pattern that will cause more problems than it solves.

**Adapter — use when:**
- You want to use an existing class but its interface does not match the one you need
- You want to create a reusable class that cooperates with unrelated classes that don't have compatible interfaces
- (Object adapter only) You need to adapt multiple existing subclasses — class adapter would require subclassing each one

**Bridge — use when:**
- You want to avoid a permanent binding between an abstraction and its implementation (implementation must be selectable or switchable at runtime)
- Both the abstractions and their implementations should be extensible by subclassing and combined independently
- Changes to the implementation of an abstraction should not require recompiling clients
- You have a class proliferation where subclasses exist for each combination of abstraction variant and implementation variant (the "nested generalizations" smell)

**Composite — use when:**
- You want to represent part-whole hierarchies of objects
- You want clients to be able to ignore the difference between compositions of objects and individual objects — clients treat all objects in the composite structure uniformly

**Decorator — use when:**
- You need to add responsibilities to individual objects dynamically and transparently, without affecting other objects
- You need responsibilities that can be withdrawn (not just added)
- Extension by subclassing is impractical because it produces too many classes or classes are unavailable for subclassing

**Facade — use when:**
- You want to provide a simple interface to a complex subsystem (subsystem complexity has grown such that most clients need a simple default view)
- There are many dependencies between clients and the implementation classes of an abstraction — introducing a Facade decouples the subsystem from clients and promotes subsystem independence
- You want to layer your subsystems — use a facade as a defined entry point at each layer, simplifying inter-subsystem dependencies

**Flyweight — ALL five conditions must be true (AND-gate):**
1. The application uses a large number of objects
2. Storage costs are high because of the sheer quantity of objects
3. Most object state can be made extrinsic (passed to methods rather than stored per-instance)
4. Many groups of objects may be replaced by relatively few shared objects once extrinsic state is removed
5. The application does not depend on object identity — since flyweight objects are shared, identity tests (`==`) will return true for conceptually distinct objects. **If your code needs to distinguish between individual instances that represent different logical entities, Flyweight will break that logic.**

**Proxy — use when:**
- A remote proxy: you need a local representative for an object in a different address space
- A virtual proxy: you need to create expensive objects on demand (lazy initialization)
- A protection proxy: access to the original object requires access-rights control
- A smart reference: you need additional behavior triggered when an object is accessed (reference counting, loading a persistent object, locking)

---

### Step 5: Produce the Recommendation

**ACTION:** Deliver a structured recommendation, explicitly naming the disambiguation rationale if the problem involved a confused pair.

**WHY:** A recommendation without the disambiguation rationale leaves the developer unable to defend the choice to teammates, and unable to re-evaluate if the situation changes (e.g., if a design-time Bridge later needs to become an Adapter because existing classes were introduced).

**Recommendation format:**

```
## Structural Pattern Recommendation: [Pattern Name]

**Intent match:** [One sentence connecting the pattern's intent to the specific problem]

**Why not [confused alternative]:** [The specific discriminator that ruled it out — timing, recursion, identity, etc.]

**Applicability check:** [Confirm the specific conditions from Step 4 are met]

**What it enables:** [What the design can do after applying this pattern]

**Key trade-off:** [What complexity or constraint this pattern introduces]

**Patterns to combine with:** [Any structural or behavioral patterns that complement this, if applicable]
```

---

## Examples

### Example 1: Third-Party Payment SDK with Wrong Interface

**Scenario:** A team is integrating a payment provider's SDK. The SDK's `PaymentGateway` class has a `processCharge(amount, token)` method. The application's internal interface is `IPaymentProcessor` with a `charge(request: PaymentRequest)` method. The SDK cannot be modified.

**Trigger:** "We need to use this payment SDK but it doesn't match our internal interface."

**Process:**
- Step 2: Interface translation — two existing incompatible interfaces
- Step 3: Adapter vs Bridge discriminator — classes are already designed and built; the incompatibility is unforeseen. Bridge is for pre-design. This is post-design. → Adapter
- Step 4: Adapter applicability — want to use an existing class whose interface doesn't match; object adapter appropriate since we don't own the SDK

**Output:**
```
## Structural Pattern Recommendation: Adapter

**Intent match:** The PaymentGateway SDK already exists with a fixed interface;
Adapter translates the existing IPaymentProcessor interface to the SDK's API
without modifying either.

**Why not Bridge:** Bridge is used before design, to keep two hierarchies from being
permanently coupled. These classes are already built — the incompatibility is
discovered, not anticipated. "Adapter makes things work after they're designed;
Bridge makes them work before."

**Applicability check:** Existing class (SDK) with non-matching interface — confirmed.
Object adapter used because subclassing PaymentGateway is not appropriate.

**What it enables:** The application only ever sees IPaymentProcessor. Swapping
the payment provider means swapping the Adapter class, with zero changes to application code.

**Key trade-off:** Each method added to IPaymentProcessor requires a corresponding
translation in the Adapter. If the interfaces diverge significantly, the Adapter
grows. Consider whether the internal interface can be kept stable.

**Patterns to combine with:** Factory Method (to instantiate the correct Adapter
based on configured payment provider)
```

---

### Example 2: UI Component Tree with Uniform Operations

**Scenario:** A document editor has two kinds of graphic objects: primitive shapes (Line, Rectangle, Text) and grouped graphics (Picture, which contains other graphics). The editor needs to move, resize, and draw both primitive and grouped objects through the same interface. Nested groups must work (a Picture can contain another Picture).

**Trigger:** "We need to treat individual shapes and groups of shapes the same way, including nested groups."

**Process:**
- Step 2: Part-whole uniformity — individual and composed objects must behave identically
- Step 3: Composite vs Decorator vs Proxy discriminator:
  - Need to hold multiple children? Yes (Picture holds a list of Graphic)
  - Recursive composition essential? Yes (nested groups required)
  - Purpose: structuring a hierarchy, not adding behavior or controlling access → Composite
- Step 4: Composite applicability — part-whole hierarchy and uniform client treatment — both confirmed

**Output:**
```
## Structural Pattern Recommendation: Composite

**Intent match:** The editor needs to treat individual shapes and grouped shapes
uniformly through a Graphic interface, with arbitrarily deep nesting of groups.

**Why not Decorator:** Decorator also uses recursive composition but its purpose
is embellishment — adding behaviors. Composite's purpose is representation —
organizing objects into a tree where nodes and leaves are interchangeable.
No responsibilities are being added here; a structure is being organized.

**Why not Proxy:** Proxy is a one-to-one stand-in for one Subject, not a
container for multiple children.

**Applicability check:** Part-whole hierarchy (Picture contains Graphics) and
uniform client treatment (editor calls draw() on any Graphic) — both confirmed.

**What it enables:** The editor code can call draw(), move(), or resize() on any
Graphic without knowing whether it's a primitive or a group. Adding new primitive
types requires no changes to the editor.

**Key trade-off:** Makes the design overly general — it becomes hard to restrict
what can be added to a Composite (e.g., preventing a Line from being added as a
child of a TextGroup). If type-safety in the hierarchy matters, extra validation
is needed.

**Patterns to combine with:** Decorator (to add responsibilities to individual
Graphic objects without subclassing), Iterator (to traverse the tree)
```

---

### Example 3: Rate Limiting and Logging Added to Service Calls

**Scenario:** A developer has a `ReportService` that generates reports. They need to add rate limiting (no more than 10 calls per minute), request logging, and authentication checking — all without modifying `ReportService`. The behaviors may need to be applied in different combinations to different service instances.

**Trigger:** "I need to add rate limiting, logging, and auth to our service without touching the service class, and I need to be able to mix and match which ones apply."

**Process:**
- Step 2: Dynamic responsibility addition — behaviors added at runtime without subclassing, and must be composable
- Step 3: Composite vs Decorator vs Proxy discriminator:
  - Adding/removing responsibilities dynamically? Yes → Decorator candidate
  - Controlling access to the real object? Rate limiting and auth do gate access → Proxy candidate
  - Key discriminator: need to stack multiple behaviors and mix-and-match → Proxy is one-to-one and static; Decorator is designed for stacking → **Decorator**
- Step 4: Decorator applicability — responsibilities to add/remove dynamically, subclassing impractical for all combinations — confirmed

**Output:**
```
## Structural Pattern Recommendation: Decorator

**Intent match:** Rate limiting, logging, and auth are responsibilities that need
to be added dynamically and in different combinations — exactly what Decorator
is designed for. Each concern becomes a decorator wrapping the service.

**Why not Proxy:** Proxy controls access through a static one-to-one relationship
to one Subject. It is not designed for recursive composition or for mixing and
matching multiple behaviors. A ProtectionProxy could handle auth alone, but cannot
stack with a RateLimitingProxy without compromising both patterns' intent.

**Applicability check:** Responsibilities are to be added transparently without
affecting other objects; responsibilities can be withdrawn (remove a decorator to
remove the behavior); subclassing for all combinations is impractical (3 behaviors
= 7 possible combinations). Confirmed.

**What it enables:** RateLimitingDecorator(LoggingDecorator(AuthDecorator(reportService)))
composes all three behaviors. Each can be added or removed independently at
construction time.

**Key trade-off:** A decorator and its component are not identical objects — code
that uses object identity (==) to find a specific layer will fail. Also, many small
objects can be harder to debug (stepping through the decorator chain). Keep
decorator chains short and document the wrapping order.

**Patterns to combine with:** Factory Method (to construct the right decorator
combination based on configuration)
```

---

## Key Principles

- **Timing is the Adapter/Bridge axis** — "Adapter makes things work *after* they're designed; Bridge makes them work *before*." If the incompatibility was discovered (classes already exist), that's Adapter territory. If the separation is intentional design-time planning, that's Bridge territory.

- **Intent beats mechanics** — Composite, Decorator, and Proxy all wrap objects and forward calls. The right choice is determined by what you're trying to accomplish: structure a hierarchy (Composite), add behaviors (Decorator), or control access (Proxy). Choosing by implementation similarity produces structurally valid but semantically wrong code.

- **Flyweight is an AND-gate, not an OR-gate** — All five conditions must hold simultaneously. The most commonly missed is identity: if any part of the application needs to distinguish between two flyweight instances representing different logical entities, shared objects will cause silent correctness bugs.

- **Facade defines new; Adapter reuses existing** — Facade creates a convenient new interface over a subsystem where none existed. Adapter makes a class conform to an existing interface someone else owns. If clients already have a target interface they code to, it's Adapter. If you're inventing the interface, it's Facade.

- **Recursive composition signals Composite or Decorator, not Proxy** — Proxy's subject relationship is static and one-to-one. If the design requires stacking, nesting, or building trees of wrapped objects, the choice is between Composite (structural hierarchy) and Decorator (behavioral layering), not Proxy.

---

## References

- For full applicability conditions and disambiguation detail for all seven patterns, see [structural-disambiguation.md](references/structural-disambiguation.md)
- For the complete 23-pattern catalog (purpose, scope, intent), consult `design-pattern-selector/references/pattern-catalog.md`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-design-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
