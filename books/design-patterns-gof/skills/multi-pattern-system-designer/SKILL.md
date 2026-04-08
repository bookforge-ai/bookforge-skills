---
name: multi-pattern-system-designer
description: |
  Design a system using multiple coordinated design patterns, moving beyond single-pattern application to pattern composition. Use when facing a complex system with multiple design problems — object creation inflexibility, structural rigidity, and behavioral coupling occurring simultaneously. Guides through the Lexi document editor methodology: decompose the system into design problems, map each to a pattern, identify pattern interaction points (e.g., Abstract Factory configures Bridge, Command uses Composite for macros, Iterator enables Visitor), and verify the patterns work together coherently.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/multi-pattern-system-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - design-pattern-selector
  - abstract-factory-implementor
  - composite-pattern-implementor
  - command-pattern-implementor
  - visitor-pattern-implementor
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [2]
tags: [design-patterns, object-oriented, gof, system-design, pattern-composition, capstone, lexi, multi-pattern]
execution:
  tier: 2
  mode: full
  inputs:
    - type: none
      description: "System description with multiple co-existing design problems — or a codebase to analyze"
  tools-required: [Read, Write, TodoWrite]
  tools-optional: [Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. A codebase is useful but not required — a verbal system description is sufficient."
---

# Multi-Pattern System Designer

## When to Use

Your system has several design problems at once, and applying patterns in isolation is not enough — the patterns need to work together. This skill is appropriate when:

- You're designing a non-trivial system from scratch and want a principled way to select and arrange patterns
- You're refactoring a complex system and need to map multiple pain points to coordinated solutions
- You understand individual patterns but aren't sure how to combine them without conflicts
- You want to validate that your chosen patterns interact correctly rather than fighting each other
- You're learning how expert designers think at the system level, not just the class level

**Prerequisite check before starting:**
- Do you have a description of the system being designed? (Even informal is fine — "a WYSIWYG document editor" is sufficient)
- Has the user already identified some design problems, or should you surface them? (This skill does both)
- Are you working with object-oriented design? (Pattern composition assumes classes, inheritance, and delegation)

This skill is a **capstone** — it assumes you can apply individual patterns. If a specific pattern is unfamiliar, consult the relevant `*-implementor` skill after the design map is complete.

---

## Context & Input Gathering

### Required Context

- **System description:** What is the system being designed or refactored? What does it do?
- **At least one known pain point or design goal:** "It needs to support multiple platforms" or "we want to add behaviors without modifying existing classes"

### Observable Context (gather from environment if available)

- **Existing codebase:** Scan for design smells — large `if/else` on types, hardcoded constructors, deep inheritance hierarchies, classes that both store data and run algorithms on it
- **Prior pattern usage:** Note which patterns are already in place — the new patterns must compose with them
- **Platform and language:** Some patterns are provided by the platform (Java `Iterator`, Python context managers); skip those and note the gap is already covered

### Sufficiency Check

You have enough to proceed with one well-described system and at least two distinguishable design problems (e.g., structure + behavior, or creation + extensibility). If only one problem is visible, proceed — the decomposition step usually surfaces others.

---

## Process

### Step 1: Decompose the System into Design Problems

**ACTION:** Use `TodoWrite` to track all steps, then list every distinct design problem in the system — not symptoms, but underlying design challenges.

**WHY:** Multi-pattern design fails when problems are not clearly separated. A single vague problem statement produces a single pattern choice, which leaves the rest of the system unaddressed. Decomposing first ensures every axis of flexibility gets its own solution rather than one pattern being stretched to cover everything.

```
TodoWrite:
- [ ] Step 1: Decompose system into design problems
- [ ] Step 2: Map each problem to a candidate pattern
- [ ] Step 3: Identify pattern interaction points
- [ ] Step 4: Verify pattern coherence
- [ ] Step 5: Produce multi-pattern design document
```

**Decomposition approach — ask these seven questions about the system:**

| Question | Design problem it surfaces | Lexi example |
|----------|---------------------------|--------------|
| How are complex objects represented internally? | Structure — how to treat composites and primitives uniformly | Documents contain characters, lines, columns — all need uniform treatment |
| How are algorithms applied to that structure? | Algorithm inflexibility — algorithm embedded in structure | Multiple formatting algorithms (simple, TeX-quality) must be swappable |
| How is behavior added to objects over time? | Embellishment rigidity — inheritance causes class explosion | Adding scroll bars + borders via subclassing → combinatorial explosion |
| How are families of related objects created? | Creational coupling — code names concrete classes | UI widgets must match look-and-feel (Motif vs. Mac) without hardcoded constructors |
| How does the system run on multiple platforms? | Platform dependency — business logic knows too much about infrastructure | Window drawing logic tied to X11, PM, Mac APIs |
| How do users trigger and undo operations? | Behavioral coupling — UI directly calls operation logic | Menu items, buttons, keyboard shortcuts all trigger the same operations; undo needed |
| How are analytical operations added to a stable structure? | Extensibility — adding analysis modifies every class | Adding spell check, hyphenation, word count should not change the structure classes |

For your system, fill in the right two columns. Not all seven will apply — typically 3–6 design problems exist in a well-scoped system. If fewer than 3 are visible, the system may be simpler than a multi-pattern design warrants.

**Output:** A numbered list of design problems, each stated as a design challenge (not a symptom). Example:

```
1. Document structure: need uniform treatment of characters, images, and composite containers
2. Formatting: formatting algorithm must be changeable independently of document structure
3. Embellishment: scroll bars and borders must be addable without subclassing
4. Look-and-feel: widget family must match platform standard without hardcoded constructors
5. Window platform: window drawing must run on multiple OS window systems
6. User operations: operations must be triggerable from multiple UI surfaces, with undo
7. Analytical operations: analysis (spell check, hyphenation) must be extensible without modifying structure classes
```

---

### Step 2: Map Each Problem to a Pattern

**ACTION:** For each design problem from Step 1, select a single primary pattern. Apply the heuristics below.

**WHY:** The mapping is not arbitrary — each pattern was discovered because it solves a recurring class of structural problem. Using the right pattern for each problem ensures the solutions are independent and can be reasoned about separately. Using the wrong pattern creates entanglement that defeats the purpose of the pattern.

**Problem-to-pattern heuristics:**

| Design problem type | Signal in the code | Primary pattern | Why this pattern |
|--------------------|--------------------|-----------------|-----------------|
| Uniform treatment of composites and primitives | Code has `if (isLeaf) ... else ...` on structure | **Composite** | Gives leaves and composites a common interface; clients never distinguish |
| Algorithm must vary independently of the structure it operates on | Algorithm is a method on the data class; swapping it means modifying that class | **Strategy** | Encapsulates each algorithm as an object; context delegates to it |
| Adding responsibilities without subclassing | Subclass names encode combinations: `ScrollableBorderedPanel` | **Decorator** | Wraps objects at run-time; responsibilities compose via chaining |
| Creating families of related objects without naming concrete classes | `new MotifButton()` scattered through client code | **Abstract Factory** | Client calls factory interface; concrete factory encapsulates platform decisions |
| Two independent hierarchies that must evolve separately | One class hierarchy tries to cover both "what" and "how" | **Bridge** | Separates abstraction hierarchy from implementation hierarchy; they vary independently |
| Decoupling request issuance from request execution, with undo | Menu items subclass per operation; no undo mechanism | **Command** | Encapsulates each request as an object with Execute/Unexecute; history enables undo |
| Traversal of structure without coupling to internal representation | Traversal logic lives inside structure classes; changing containers breaks traversal | **Iterator** | Encapsulates traversal algorithm; clients navigate without knowing the storage structure |
| Adding open-ended operations to a stable class hierarchy | New operation requires adding a method to every class in the hierarchy | **Visitor** | Encapsulates operations as visitor objects; adding analysis = new Visitor subclass |

**For each problem in your list:** state the primary pattern and a one-sentence justification connecting the pattern's intent to the specific problem. If two patterns seem equally applicable, note both and add a trade-off sentence.

**Pattern application table (fill in for your system):**

```
| # | Design Problem | Pattern | Justification |
|---|---------------|---------|---------------|
| 1 | [problem]     | [name]  | [one sentence] |
```

**Lexi reference:** The completed table for Lexi is in `references/lexi-case-study.md`.

---

### Step 3: Identify Pattern Interaction Points

**ACTION:** Review each pair of patterns from Step 2 and determine: do they interact? If so, how?

**WHY:** This is the step most developers skip — and where multi-pattern designs break down. Patterns are not isolated. When one pattern creates objects that another pattern uses, or when one pattern's structure is traversed by another, there is an interaction point. Failing to design these interactions explicitly leads to tight coupling between the patterns themselves, defeating their purpose.

**Three canonical interaction types:**

**Type 1 — Creational configures structural (factory creates implementation):**
A creational pattern (Abstract Factory, Factory Method) produces the concrete objects that a structural or behavioral pattern needs to function. The factory encapsulates which concrete variant is selected, and the structural pattern receives the result without knowing what it is.

- Lexi example: `WindowSystemFactory` (Abstract Factory) creates `WindowImp` objects. `Window` (Bridge abstraction) receives a `WindowImp` from the factory at construction time. The Bridge pattern doesn't know which window system is in use; the factory decides.
- Generalized: When your Bridge or Strategy uses platform-specific or environment-specific implementations, use Abstract Factory to configure it at startup.

**Type 2 — Behavioral pattern uses structural pattern (command composes commands):**
A behavioral pattern's objects are themselves organized using a structural pattern. This allows single behavioral objects and groups of behavioral objects to be treated uniformly.

- Lexi example: `MacroCommand` is a `Command` subclass that contains a `Composite` of other commands. Executing a macro executes its children. The Command pattern gains the benefit of the Composite pattern — macros can be nested, undone as a unit, and stored in history alongside atomic commands.
- Generalized: Whenever you need to batch or sequence Command objects, use Composite to build macro commands. The same Execute/Unexecute interface applies to both atomic and composite commands.

**Type 3 — Traversal enables analysis separation (iterator enables visitor):**
An Iterator provides traversal over a structure independently of how it is stored. A Visitor receives each element during that traversal and performs analysis. The two patterns divide responsibility cleanly: Iterator owns *how to move* through the structure; Visitor owns *what to do* at each element.

- Lexi example: A `PreorderIterator` traverses the Glyph structure. A `SpellingCheckingVisitor` is carried along and called at each node via `Accept(visitor)`. Adding hyphenation analysis = new Visitor subclass, not a change to Glyph or Iterator.
- Generalized: If your Visitor needs to be applied across a Composite structure, pair it with an external Iterator. The Iterator decouples traversal order from the Visitor's analysis logic — either can change independently.

**How to identify interactions in your system:**

Go through your pattern map from Step 2 and ask:
1. Does any pattern produce objects that another pattern consumes? → Creational-configures-structural interaction
2. Does any behavioral pattern need to operate on groups as well as individuals? → Behavioral-uses-structural interaction
3. Does any traversal need to carry analysis logic that should be changeable? → Traversal-enables-analysis interaction

**Output:** A list of interaction points, each with: Pattern A → Pattern B, interaction type, and which class is the "bridge" between them.

---

### Step 4: Verify Pattern Coherence

**ACTION:** Apply four coherence checks to the full pattern map.

**WHY:** Individual patterns can each be correctly chosen while still conflicting at the system level. Coherence verification surfaces these conflicts before implementation begins — when they are cheap to fix. The four checks cover the most common failure modes in multi-pattern design.

**Check 1 — No duplicate responsibilities:**
Each design problem should be assigned to exactly one pattern. If two patterns both claim to solve the same problem, one is misapplied. Example: using both Decorator and Bridge to handle "multiple rendering implementations" duplicates responsibility; only one should own that axis.

**Check 2 — Interaction points are explicit:**
Every place where one pattern's output becomes another pattern's input must be a named class or method, not an implicit assumption. The `WindowSystemFactory::CreateWindowImp()` method is explicit. An interaction that exists only in the developer's head is not a design — it's a future bug.

**Check 3 — Extension paths are clear:**
For each pattern, ask: "What happens when we add a new variant?" The answer should be a new class, not a modification to existing ones. If adding a new window system requires modifying the `Window` class, the Bridge is mis-configured. If adding a new analysis requires modifying `Glyph`, the Visitor is not set up correctly.

**Check 4 — No pattern is doing too much:**
If a single pattern (especially Composite or Strategy) appears to solve three or four design problems, that is a signal that the decomposition in Step 1 was not fine-grained enough. Re-examine whether those "problems" are actually one problem stated too broadly.

**Fail conditions:** If any check fails, return to the step where the problem originates (usually Step 1 or Step 2) and revise. Do not proceed to Step 5 with known coherence failures.

---

### Step 5: Produce the Multi-Pattern Design Document

**ACTION:** Assemble the complete design as a structured document with four sections.

**WHY:** A multi-pattern design is too complex to keep in working memory. Writing it down serves three purposes: it forces precision (vague plans don't survive structured documentation), it creates a reviewable artifact, and it acts as the blueprint for implementation. The document should be specific enough that a developer unfamiliar with the decisions can implement it correctly.

**Document structure:**

---

```markdown
# [System Name] — Multi-Pattern Design

## System Overview
[2–3 sentences: what the system does, what design challenges drove the pattern choices]

## Design Problem Map

| # | Design Problem | Pattern | Key Participant Classes |
|---|---------------|---------|------------------------|
| 1 | ...           | ...     | ...                    |

## Pattern Interaction Diagram

[Text diagram or description of the interaction points]

Key interactions:
1. [Pattern A] → configures → [Pattern B]: [class/method that links them]
2. [Pattern A] → uses structure of → [Pattern B]: [class that is both]
3. [Pattern A] → enables → [Pattern B]: [traversal mechanism]

## Extension Guide

| To add...                          | Action required                    | Classes to create |
|------------------------------------|------------------------------------|-------------------|
| New [variant of problem 1]         | Subclass [participant]             | [class name]      |
| New [variant of problem 2]         | Subclass [participant]             | [class name]      |
| New analysis operation             | New Visitor subclass               | [class name]      |

## Coherence Notes
[Any trade-offs or constraints the implementation must respect]
```

---

## Examples

### Example 1: WYSIWYG Document Editor (Lexi)

**Scenario:** Building a document editor that must represent rich document structure, support multiple formatting algorithms, allow UI embellishments (borders, scroll bars), support multiple look-and-feel standards, run on multiple window systems, support undo, and allow extensible analysis (spell check, hyphenation).

**Trigger:** "We need to design Lexi, a WYSIWYG document editor. It has to handle everything from basic text rendering to platform portability to undoable editing."

**Process summary:**

Step 1 decomposed this into 7 design problems. Step 2 mapped each to a pattern. Step 3 found 3 interaction points. Step 4 confirmed coherence — each pattern owns exactly one problem, interactions are explicit through named factory and composite classes, every new variant is a new class.

**Output (abbreviated):**

```
# Lexi — Multi-Pattern Design

## Design Problem Map

| # | Design Problem                      | Pattern          | Key Participant Classes         |
|---|-------------------------------------|------------------|---------------------------------|
| 1 | Uniform treatment of doc elements   | Composite        | Glyph, Character, Row, Column   |
| 2 | Swappable formatting algorithms     | Strategy         | Compositor, Composition         |
| 3 | Adding UI embellishments at runtime | Decorator        | MonoGlyph, Border, Scroller     |
| 4 | Multiple look-and-feel widget sets  | Abstract Factory | GUIFactory, MotifFactory        |
| 5 | Multiple window system platforms    | Bridge           | Window, WindowImp, XWindowImp   |
| 6 | Undoable user operations            | Command          | Command, MenuItem, History      |
| 7 | Extensible document analysis        | Visitor          | Visitor, SpellingCheckingVisitor|

## Pattern Interaction Diagram

                  ┌─────────────────┐
                  │ Abstract Factory │
                  │  (GUIFactory)   │
                  └────────┬────────┘
                           │ creates WindowImp
                           ▼
              ┌────────────────────────┐
              │   Bridge               │
              │  Window ←→ WindowImp  │
              └────────────────────────┘

   ┌────────────────┐      uses Composite
   │    Command     │ ──────────────────► MacroCommand
   │  (MenuItem)    │                    (Command + Composite)
   └────────────────┘

   ┌─────────────┐      traversal
   │  Iterator   │ ────────────────► ┌─────────┐
   │(PreorderIt.)│                   │ Visitor │
   └─────────────┘                   │(Spelling│
                                     │Checker) │
                                     └─────────┘

Key interactions:
1. Abstract Factory → configures → Bridge: WindowSystemFactory::CreateWindowImp()
2. Command → uses structure of → Composite: MacroCommand contains List<Command*>
3. Iterator → enables → Visitor: PreorderIterator carries Visitor to each Glyph::Accept()

## Extension Guide

| To add...                    | Action required                     | Classes to create         |
|------------------------------|-------------------------------------|---------------------------|
| New formatting algorithm     | Subclass Compositor                 | TeXCompositor             |
| New UI embellishment         | Subclass MonoGlyph                  | ShadowDecorator           |
| New look-and-feel standard   | Subclass GUIFactory                 | MacFactory                |
| New window system platform   | Subclass WindowImp                  | WaylandWindowImp          |
| New undoable operation       | Subclass Command                    | IndentCommand             |
| New document analysis        | Subclass Visitor                    | WordCountVisitor           |
```

Full details: `references/lexi-case-study.md`

---

### Example 2: Financial Portfolio System

**Scenario:** A financial system needs to represent portfolios that contain accounts and sub-portfolios (hierarchical structure), support multiple risk calculation algorithms, log every transaction with undo, and generate various regulatory reports without modifying account classes.

**Trigger:** "We need to redesign our portfolio system. It needs hierarchical holdings, pluggable risk models, an audit trail, and extensible reporting."

**Process summary:**

Step 1 surfaces 4 design problems: (1) hierarchical portfolio structure, (2) multiple risk algorithms, (3) auditable transactions with undo, (4) extensible reporting over a stable hierarchy.

Step 2 maps: Composite for hierarchy (portfolios contain portfolios and accounts uniformly), Strategy for risk models (each model is interchangeable), Command for transactions (undo/redo + audit log), Visitor for reporting (new report type = new Visitor subclass).

Step 3 interaction: Command uses Composite — a BatchTransaction is a MacroCommand holding a list of individual Commands. Visitor is enabled by Iterator traversal over the Composite hierarchy.

```
# Portfolio System — Multi-Pattern Design

## Design Problem Map

| # | Design Problem                       | Pattern   | Key Participant Classes                    |
|---|--------------------------------------|-----------|--------------------------------------------|
| 1 | Uniform treatment of holdings        | Composite | Holding, Account, Portfolio                |
| 2 | Swappable risk calculation           | Strategy  | RiskModel, VaRModel, StressTestModel       |
| 3 | Auditable transactions with undo     | Command   | Transaction, TradeCommand, BatchTransaction|
| 4 | Extensible regulatory reporting      | Visitor   | ReportVisitor, BaselIIIReportVisitor       |

Key interaction:
1. Command → uses → Composite: BatchTransaction contains List<Transaction>
2. Iterator → enables → Visitor: PreorderIterator carries ReportVisitor through Portfolio tree
```

---

### Example 3: Game Engine with Multiple Platforms

**Scenario:** A game engine needs a scene graph (hierarchical game objects), pluggable rendering backends (OpenGL, Vulkan, Metal), UI behaviors that can be stacked (glow + shadow + border), and a scriptable action system with undo for level editing.

**Trigger:** "We're building a cross-platform game engine. We need a scene graph, multiple renderers, stackable UI effects, and undoable editor commands."

**Process summary:**

Step 1: (1) scene hierarchy, (2) rendering platform independence, (3) stackable visual effects, (4) undoable level-editor operations.

Step 2: Composite (scene graph), Bridge (game object abstraction vs. renderer implementation), Decorator (stackable visual effects), Command (undoable editor operations).

Step 3 interactions: Abstract Factory creates the concrete Renderer that Bridge uses. Command uses Composite for compound editor operations (GroupMoveCommand).

```
# Game Engine — Multi-Pattern Design

## Design Problem Map

| # | Design Problem                  | Pattern          | Key Participant Classes                      |
|---|-------------------------------- |------------------|----------------------------------------------|
| 1 | Scene hierarchy                 | Composite        | SceneNode, MeshNode, GroupNode               |
| 2 | Renderer platform independence  | Bridge           | Renderer, RendererImpl, VulkanRendererImpl   |
| 3 | Stackable visual effects        | Decorator        | EffectNode, GlowEffect, ShadowEffect         |
| 4 | Undoable level-editor ops       | Command          | EditorCommand, MoveCommand, GroupMoveCommand |

Key interaction:
1. Abstract Factory → configures → Bridge: PlatformFactory::CreateRendererImpl()
2. Command → uses → Composite: GroupMoveCommand contains List<EditorCommand>
```

---

## Reference Files

| File | Contents |
|------|----------|
| `references/lexi-case-study.md` | Full Lexi pattern map: 7 problems, 8 patterns, 3 interaction points, extension guide, summary from GoF Chapter 2 |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-design-pattern-selector`
- `clawhub install bookforge-abstract-factory-implementor`
- `clawhub install bookforge-composite-pattern-implementor`
- `clawhub install bookforge-command-pattern-implementor`
- `clawhub install bookforge-visitor-pattern-implementor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
