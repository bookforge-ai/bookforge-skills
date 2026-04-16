---
name: big-refactoring-planner
description: |
  Plan and execute architectural-scale refactoring campaigns that take weeks to months — the four named patterns for large-scale structural restructuring from Fowler and Beck's Chapter 12. Use when: an inheritance hierarchy is doing two distinct jobs and subclass names share the same adjective prefix at every level (Tease Apart Inheritance); a codebase written in an object-oriented language uses a procedural style with long methods on behavior-less classes and dumb data objects (Convert Procedural Design to Objects); GUI or window classes contain SQL queries, business rules, or pricing logic instead of just display code (Separate Domain from Presentation); a single class has accumulated so many conditional statements that every new case requires editing the same class in multiple places (Extract Hierarchy). Applies when code-smell-diagnosis has surfaced Parallel Inheritance Hierarchies, Data Class, or Large Class with deep conditional branching and the fix is too large for a single refactoring session. Distinguishes between the four patterns by structural signal, selects the correct pattern and variant, and produces a multi-week campaign plan with interleaved feature development milestones.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/big-refactoring-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - code-smell-diagnosis
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler", "Kent Beck"]
    chapters: [12]
tags: [refactoring, code-quality, legacy-code, architecture]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "The target codebase or subsystem with the architectural-scale structural problem"
    - type: document
      description: "Code-smell-diagnosis report identifying which big refactoring pattern applies, if already run"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory. Read source files to identify the structural pattern; write the campaign plan as output."
discovery:
  goal: "Identify which of the four big refactoring patterns applies; select the correct execution variant; produce a campaign plan with milestones, decision points, and interleaving strategy for working alongside ongoing feature development"
  tasks:
    - "Read the codebase to confirm the structural pattern from the signal list"
    - "Select the correct pattern and variant based on the structural signals"
    - "Identify the key decision points within the selected pattern"
    - "Produce a phased campaign plan that can be executed alongside feature work"
    - "Establish the stopping condition: when is the refactoring done enough?"
  audience:
    roles: ["software-developer", "senior-developer", "tech-lead", "architect"]
    experience: "senior — assumes comfort with object-oriented design and familiarity with individual refactoring moves"
  triggers:
    - "An inheritance hierarchy has the same adjective prefix appearing at every level of subclasses"
    - "Procedural code in an object-oriented language: long methods on classes with no data, dumb data objects with no behavior"
    - "Window or GUI classes contain SQL statements, pricing logic, or business rules"
    - "A single class requires editing in five different places every time a new case is added"
    - "code-smell-diagnosis found Parallel Inheritance Hierarchies, Data Class, or a god class with pervasive conditionals"
    - "A team cannot add a new feature type without touching the same class in multiple unrelated ways"
  not_for:
    - "Individual refactoring moves that can be completed in a single session — use method-decomposition-refactoring or conditional-simplification-strategy instead"
    - "Performance optimization — use profiling-driven-performance-optimization"
    - "Diagnosing which smells are present — run code-smell-diagnosis first"
    - "Test coverage setup before starting refactoring — use build-refactoring-test-suite first"
---

# Big Refactoring Planner

## When to Use

You have a structural design problem that cannot be fixed in a single refactoring session. The individual moves — Extract Method, Move Method, Extract Class — are not in question. The challenge is that the problem is architectural: dozens of classes are tangled, or a hierarchy is doing multiple jobs, or procedural logic is spread across a codebase that nominally uses objects. The fix takes weeks to months, not minutes.

This skill is for those campaigns.

**Fowler and Beck's core principle:** "You refactor not because it is fun but because there are things you expect to be able to do with your programs if you refactor that you just can't do if you don't."

Big refactorings are done for a purpose — specifically because a particular kind of change that the team needs to make is blocked or costly without the restructuring. You are not refactoring for cleanliness. You are refactoring because the architecture is standing in the way of features you need to build.

**This skill applies to four named patterns:**

| Pattern | Core problem | Time scale |
|---------|-------------|------------|
| Tease Apart Inheritance | One hierarchy doing two independent jobs | Weeks |
| Convert Procedural Design to Objects | OO language used in procedural style | Weeks to months |
| Separate Domain from Presentation | Business logic embedded in GUI classes | Weeks |
| Extract Hierarchy | God class with accumulated conditionals | Weeks to months |

**Prerequisites:** Run `build-refactoring-test-suite` before starting. Big refactorings require a test suite that can catch regressions — the campaign moves incrementally and tests must confirm each step is safe.

---

## Context and Input Gathering

### Required Input (ask if missing)

- **The structural problem.** Either a code-smell-diagnosis report, a description of where the pain is ("every time we add a new deal type, we have to subclass in two hierarchies"), or a specific class or directory to examine. Why: the four patterns apply to distinct structural situations. Reading the code to confirm the signal is mandatory — big refactorings cannot be planned without inspecting the structure.

- **The purpose of the refactoring.** What feature work is blocked? What change is currently too costly? Why: Fowler and Beck are explicit that big refactorings must be done toward a purpose. A campaign without a purpose will be abandoned when pressure mounts. The purpose also determines when to stop — when the blocked change becomes easy, the refactoring has succeeded.

### Observable Context (read before asking)

Scan the codebase to identify which structural pattern is present:

```
Tease Apart Inheritance signals:
  - Subclasses with identical prefix adjectives at every level
    (TabularActiveDeal, TabularPassiveDeal — "Tabular" appears in both branches)
  - Adding a new variation in one dimension requires adding subclasses in every branch
  - Hierarchy depth exceeds 3 levels with cross-cutting concerns

Convert Procedural Design to Objects signals:
  - Classes with only static methods or methods that take data objects as parameters
  - Data classes (fields + accessors, no behavior) that are passed into procedure-style classes
  - Long methods (50+ lines) on classes with few or no instance variables
  - A single "calculator" or "processor" class that takes many different data objects

Separate Domain from Presentation signals:
  - SQL statements inside window, panel, dialog, or view classes
  - Window/form classes over 300 lines with business logic in event handlers
  - Pricing, discount, or calculation logic in GUI event handlers
  - java.sql imports in UI classes; database calls triggered directly by UI events

Extract Hierarchy signals:
  - One class with 10+ boolean flags or type code fields
  - Methods with large switch/case or if-elif chains that check the same flag
  - Adding a new "type" or "mode" requires editing the same class in 5+ methods
  - The class's behavior changes entirely based on a flag set at construction time
```

---

## Process

### Step 1: Confirm the Pattern

**ACTION:** Read the target code, identify which structural pattern applies, and confirm the diagnosis.

**WHY:** The four patterns require different remedies. Applying Extract Hierarchy mechanics to a tangled inheritance hierarchy will make it worse. Applying Tease Apart Inheritance to a god class with conditionals will create a hierarchy where subclassing is not the right solution. Correct pattern identification determines whether the campaign succeeds.

Work through the pattern-confirmation checklist:

**Tease Apart Inheritance — confirm by answering:**
- Do classes at the same level of the hierarchy share the same adjective prefix? (e.g., `Tabular` appearing in both ActiveDeal and PassiveDeal branches)
- Is the hierarchy growing combinatorially? (adding 1 new deal type requires adding 2 new subclasses because presentation styles cross with deal types)
- Can you draw a two-dimensional grid where one axis is one job and the other axis is the other job?

If yes to all three: this is Tease Apart Inheritance.

**Convert Procedural Design to Objects — confirm by answering:**
- Are there classes whose methods all take data objects as their primary parameter (e.g., `calculatePrice(Order order)` on `OrderCalculator`)?
- Are the data objects pure data holders with accessors but no behavior?
- If you removed the "calculator" class, would its behavior need to live somewhere on the data objects?

If yes: this is Convert Procedural Design to Objects.

**Separate Domain from Presentation — confirm by answering:**
- Do GUI or window classes contain SQL, database calls, or business computation?
- Is business logic triggered directly by UI events?
- If you wanted to change the pricing algorithm, would you have to open a window class?

If yes: this is Separate Domain from Presentation.

**Extract Hierarchy — confirm by answering:**
- Does one class control its behavior almost entirely through flags or type codes checked in conditionals?
- Are the conditionals static during the object's lifetime — does the type or mode get set at construction and not change?
- Does adding a new type require editing conditional logic in five or more methods of the same class?

If yes: this is Extract Hierarchy. Then determine the variant:
- **Variant A (unclear variations):** You are not sure what all the subclasses should be — discover them one at a time.
- **Variant B (clear variations):** The full set of variations is already known upfront — create all subclasses at once.

---

### Step 2: Select Execution Strategy

**ACTION:** Based on the confirmed pattern, select the execution strategy and identify the key decision points.

**WHY:** Each pattern has a fixed sequence of moves, but the sequence has decision points that cannot be fully specified in advance — the specific code you encounter will determine which moves apply. Knowing the decision points before starting prevents mid-campaign confusion and ensures the team pushes through when the refactoring gets messy.

---

#### Strategy: Tease Apart Inheritance

**Problem:** One hierarchy is doing two jobs. (Example: `Deal` hierarchy also captures presentation style, creating `TabularActiveDeal`, `TabularPassiveDeal`.)

**Goal:** Two clean, focused hierarchies connected by delegation.

**Sequence:**

1. **Draw the two-dimensional grid.** Label the axes with the two jobs the hierarchy is doing. Every current subclass should map to a cell in the grid. Cells that are missing reveal gaps in the current implementation. Why: the grid makes the tangling visible and determines how many new classes will be needed in the extracted hierarchy.

2. **Decide which job stays in the original hierarchy.** The rule of thumb: leave the job with more code in place — it has less to move. Extract the job with less code into the new hierarchy. Why: moving less code reduces the risk of bugs during extraction. The job that stays will be simplified once the other job is extracted.

3. **Apply Extract Class at the common superclass** to create a new class representing the subsidiary job. Add an instance variable to the original superclass to hold a reference to the new object. Why: the new class becomes the root of the extracted hierarchy; the instance variable is the delegation link between the two hierarchies.

4. **Create subclasses of the extracted class** — one for each variation of the subsidiary job (e.g., `TabularPresentationStyle`, `SinglePresentationStyle`). Initialize the instance variable in each original subclass to the appropriate subclass of the extracted class. Why: until the subclasses are created, the extracted class is just an empty shell with no behavior — this step populates the second hierarchy.

5. **Move behavior into the extracted hierarchy.** Apply Move Method (and Move Field where needed) in each original subclass to transfer presentation-related behavior to the corresponding extracted subclass. Why: behavior must follow data — the extracted hierarchy is not useful until it carries the code that belongs to it.

6. **Eliminate empty original subclasses.** When a subclass has no more code of its own, delete it. Continue until all subclasses are gone from the dimension being extracted. Why: the original hierarchy should now contain only the classes representing the primary job; the second hierarchy handles the subsidiary job entirely through delegation.

7. **Look for further simplification.** After the hierarchies are separated, each can often be simplified further with Pull Up Method or Pull Up Field — logic that was previously tangled may now be clearly common to all subclasses. Why: separation frequently reveals that what appeared to be variation was actually duplication.

**Key decision point:** Which job stays? Lean toward leaving the job with more code in place. If the code is evenly split, choose the job that is semantically primary — the job that gives the class its name.

---

#### Strategy: Convert Procedural Design to Objects

**Problem:** An object-oriented language is being used in a procedural style. Behavior is concentrated in procedure classes; data is concentrated in data-holder classes with no behavior.

**Goal:** Behavior distributed into the data objects where it belongs.

**Sequence:**

1. **Turn each record type into a dumb data object with accessors.** If you have a relational database, create a class for each table with accessor methods. Why: the data classes are the correct eventual home for the behavior that currently lives in procedure classes. They must exist before behavior can move into them.

2. **Concentrate all procedural code into a single class.** If it is scattered across multiple procedure classes, consolidate. Make the class a singleton or make its methods static to allow easy invocation during the transition. Why: having all procedural code in one place makes it easier to track progress and apply Extract Method systematically. This is a temporary state — the goal is to empty this class.

3. **Apply Extract Method to each long procedure** to break it into smaller named operations. Immediately follow with Move Method to move each extracted operation to the data class whose data it primarily uses. Why: Extract Method creates handles on behavior units; Move Method is the act of distributing those units to their natural home. The procedure class shrinks with each Move Method applied.

4. **Continue until the procedure class is empty.** If the original class was a purely procedural class, delete it — this is a sign the refactoring is complete. Why: an empty procedure class is the evidence that behavior has been fully distributed. If the class cannot be deleted, some behavior genuinely has no home and a new class may need to be created.

**Key decision point:** What to do when a method uses data from multiple record types equally. Move Method to the record type it uses most; extract the portions that use other records into separate methods that can be moved to those records.

---

#### Strategy: Separate Domain from Presentation

**Problem:** GUI classes contain domain logic. Business rules, SQL queries, and calculations are embedded in window or event handler classes.

**Goal:** Clean separation where GUI classes handle only presentation and domain classes carry all business logic.

**Sequence:**

1. **Create a domain class for each window.** If a window displays grid data, also create a class for the rows in the grid. Link the domain class to the window class via a reference field. Why: the domain class is the eventual home for all business logic currently in the window. It must exist before any logic can be moved.

2. **Examine each field and data element in the window.** Classify each one into one of three categories:
   - *Pure GUI only (not used in domain logic):* Leave it on the window.
   - *Domain data not displayed in the GUI:* Move Field directly to the domain class using Move Field. Why: non-displayed domain data has no presentation dependency and can be moved immediately with low risk.
   - *Domain data that is also displayed in the GUI:* Use Duplicate Observed Data — create a corresponding field on the domain class with synchronization logic. Why: these fields cannot be moved directly because the GUI needs them; duplication with sync is the safe intermediate step before the GUI can be updated to reference the domain object's field instead.

3. **Examine the logic in the window class.** Classify each logical operation:
   - *Pure presentation logic:* Leave it in the window.
   - *Domain logic:* Apply Extract Method to isolate it, then Move Method to transfer it to the domain class.
   - *Mixed presentation and domain logic:* Apply Extract Method to separate the domain portion, then Move Method for the domain portion; leave the presentation portion in the window.

4. **Target SQL statements specifically.** Drive SQL statements and database logic toward the domain class. Moving SQL imports away from the window class is a useful completion signal — when the window class no longer imports `java.sql` (or equivalent), the separation is largely complete. Why: SQL in a window class is the clearest signal of domain logic in the wrong place; its removal confirms the domain class is carrying its responsibilities.

5. **Stop when risk is addressed.** The resulting domain classes will not be perfectly factored — they will hold the right logic but may need further refactoring (Data Clumps, Feature Envy). Stop the Separate Domain from Presentation campaign once the primary risk is eliminated. If the risk was the mixing of presentation and domain logic, that risk is gone when the separation is clean. Further refactoring of the domain classes is a separate, smaller campaign. Why: trying to fully factor the domain classes simultaneously with the separation campaign overextends the scope and increases the risk of abandonment.

**Key decision point:** What to do with data that is both displayed and used in domain logic. Always use Duplicate Observed Data as the intermediate step. Direct Move Field will break the GUI. Accept the duplication temporarily — it is easier to eliminate once the logic is clearly in the domain class.

---

#### Strategy: Extract Hierarchy

**Problem:** A single class is doing too much, controlled by flags or type codes, with behavior that varies entirely based on those flags.

**Prerequisite check:** The conditional logic must be static during the object's lifetime. If the flags can change after construction, apply Extract Class first to create a separate object for the varying aspect before applying Extract Hierarchy. Why: Extract Hierarchy uses subclasses to represent variations. Subclass membership cannot change after instantiation — if a flag changes at runtime, the variation cannot be a subclass.

**Variant A — Unclear variations (discover one at a time):**

1. **Identify one recurring variation in the conditional logic.** Look for a flag or condition that recurs across multiple methods of the class. Why: starting with one variation keeps the scope manageable and prevents the campaign from becoming paralyzing.

2. **Create a subclass for that variation.** Apply Replace Constructor with Factory Method on the original class so that clients receive a subclass instance when the variation applies. Why: the factory method is necessary because constructors cannot return subclass instances; it also gives the campaign a controlled entry point for the new subclass.

3. **Copy conditional methods to the subclass.** For each method in the original class that has conditional logic based on the variation, copy the method to the subclass and simplify it — remove the branches that cannot apply to this subclass. Use Extract Method in the superclass if needed to isolate the conditional from the unconditional parts. Why: copying rather than moving allows the original class to continue working for all other variations while the subclass is being built.

4. **Continue isolating variations.** Pick the next variation, create the next subclass, repeat. Continue until the original class's conditional methods can be declared abstract — all variations are now handled by subclasses. Why: each new subclass removes one variation from the superclass; when the superclass has no remaining conditional logic for a method, that method becomes abstract.

5. **Delete superclass method bodies when all subclasses override them.** Make the superclass declarations abstract. Why: an abstract superclass with no concrete implementations is the evidence that the hierarchy is complete.

**Variant B — Clear variations (create all subclasses at once):**

1. **Create a subclass for each known variation.** Apply Replace Constructor with Factory Method to return the appropriate subclass for each variation.

2. **For each method with conditional logic, apply Replace Conditional with Polymorphism.** If the whole method varies, move it in full to each subclass. If only part of the method varies, apply Extract Method first to isolate the varying part, then move the extracted method. Why: Replace Conditional with Polymorphism is the terminal move — it eliminates the conditional by making each subclass responsible for its own case.

**Key decision point:** Which variant to use. Use Variant A when you are unsure how many variations exist or the existing conditional logic is inconsistent. Use Variant B when the full set of variations is well-understood and each variation is consistently represented in the conditional logic.

---

### Step 3: Build the Campaign Plan

**ACTION:** Produce a phased campaign plan the team can execute over weeks or months.

**WHY:** Big refactorings that are not planned as campaigns get abandoned. The team hits a messy intermediate state, feature pressure mounts, and the refactoring is frozen half-done — a state that is worse than the starting point. A campaign plan with explicit milestones and interleaving rules allows the team to make progress every day without disrupting feature delivery.

**Campaign plan structure:**

```markdown
# [Pattern Name] Campaign Plan — [Target Class/System]

## Purpose
[The specific feature or change that is currently blocked. Why this refactoring now.]

## Pattern
[Selected pattern and variant, with one-sentence rationale for the selection]

## Team Alignment Required
Big refactorings require shared awareness. Every developer working in the affected
area must know:
  1. This refactoring is "in play"
  2. Which classes are being restructured
  3. How to continue the refactoring when adding new code (new code goes into the
     new structure, not the old one)

[List the classes and files "in play" for this campaign]

## Milestones

### Milestone 1: [Name] — [Estimated: N days]
Goal: [What structural state the code is in at the end of this milestone]
Steps:
  1. [Specific move to apply]
  2. [Specific move to apply]
  ...
Done when: [Specific, observable condition — e.g., "TabularPresentationStyle class exists
  and holds all tabular layout methods"]

### Milestone 2: [Name] — [Estimated: N days]
[...]

## Interleaving Rules
- Refactoring steps happen during feature work, not in a dedicated freeze.
- Each milestone step is small enough to complete between feature commits.
- New features that touch the affected area use the new structure, not the old.
- Do not skip milestones to reach the end state — intermediate states must compile
  and pass all tests.

## Decision Points
[List the key decisions that cannot be made until the code is read at that milestone:
  e.g., "At Milestone 2: decide which job stays in the original hierarchy based on
  line count of each dimension"]

## Stopping Condition
[The specific observable state that means the refactoring is done enough:
  e.g., "When OrderWindow no longer imports java.sql"]
[The specific feature or change that was blocked must now be easy to make]
```

---

### Step 4: Identify Interleaving Strategy

**ACTION:** Establish the rules for how the campaign runs alongside feature development.

**WHY:** "Refactoring not because it is fun but because there are things you expect to do with your programs" — Fowler and Beck. Big refactorings must coexist with feature delivery. The alternative — a two-month code freeze to refactor — is not available in production systems. The nibble-at-the-edges approach is the only viable one.

**Interleaving rules (apply to every big refactoring campaign):**

1. **Refactor to a purpose, not for cleanliness.** The campaign starts because a specific feature or change is blocked. Every step of the campaign should move toward making that feature easier. If a step does not contribute to that goal, question whether it is necessary.

2. **Nibble at the edges.** Each time a developer touches an affected file for feature work, they apply the next step of the refactoring. The refactoring rides along with feature development — it does not block it. A little today, a little tomorrow.

3. **Do as much as needed to achieve the real task.** You do not have to complete the entire campaign before shipping the feature. You have to complete enough of the campaign that the feature becomes easy to add. Stop when the purpose is achieved.

4. **Never leave tests failing overnight.** Each step of the campaign must leave the codebase in a state where all tests pass. An intermediate state with failing tests is a blocker for the whole team. The campaign must be executed in safe steps, each verifiable by the test suite.

5. **New code follows the new structure.** When adding new features in the affected area during the campaign, use the new structure (the extracted class, the new hierarchy, the domain class) — not the old one. This prevents the old structure from growing while the campaign is in progress.

---

### Step 5: Define the Stopping Condition

**ACTION:** Establish when the campaign is done and communicate it to the team.

**WHY:** Big refactorings without a stopping condition run forever or collapse under pressure. The stopping condition is the purpose stated in terms of observable code state. It is the answer to "how will we know when we are done?"

**Stopping condition by pattern:**

- **Tease Apart Inheritance:** Done when the two hierarchies are fully separated, each class in the original hierarchy has a single job, and adding a new variation in one dimension does not require adding subclasses in the other.

- **Convert Procedural Design to Objects:** Done when the procedure class is empty or deleted, and all behavior lives in the data objects. (Optional secondary: when the data objects no longer need to be passed as parameters because they know how to perform their own operations.)

- **Separate Domain from Presentation:** Done when the window class contains no SQL, no database calls, and no business computation — only display logic and event routing. The domain class handles all business logic. (Observable signal: the window class no longer imports database libraries.)

- **Extract Hierarchy:** Done when the original god class is abstract, each variation is a subclass, and adding a new variation requires adding only one new subclass with its own implementations — not editing any existing class.

---

## Key Principles

**1. Big refactorings are purposeful, not cosmetic.**
The motivation for a big refactoring is always a specific blocked capability. "The code is messy" is not sufficient motivation — a campaign that long will be abandoned. "We cannot add a new billing scheme without editing conditional logic in twelve methods of BillingScheme" is a sufficient motivation. The purpose drives the campaign and defines when it is complete.

**2. Steps cannot be fully specified in advance.**
Unlike the individual refactoring moves in Chapters 6-11, the steps of a big refactoring emerge as you do it. The pattern provides the strategy; the code provides the specifics. The plan must include decision points — places where you explicitly pause to assess the code and decide the next move based on what you find.

**3. Team agreement is mandatory.**
A big refactoring affects every developer working in the area. If one developer is teasing apart a hierarchy while another is subclassing the old tangled one, the campaign moves backward. Every developer must know that the refactoring is "in play" and must use the new structure when writing new code.

**4. Intermediate states are dangerous — tests must pass at every step.**
The period between starting and finishing a big refactoring is the most dangerous time. The code is in a partially restructured state. Without a test suite that passes after each step, the team cannot detect regressions. Run build-refactoring-test-suite before starting any campaign.

**5. Accumulation is the enemy.**
Fowler and Beck: "Accumulation of half-understood design decisions eventually chokes a program as a water weed chokes a canal." Big refactorings address accumulated design debt. They are not optional maintenance — they are necessary for the system to remain changeable.

---

## Examples

### Example 1: Tease Apart Inheritance — Deal Hierarchy

**Situation:** A codebase has a `Deal` hierarchy with subclasses `ActiveDeal`, `PassiveDeal`, `TabularActiveDeal`, and `TabularPassiveDeal`. Every time a new deal type is added, tabular and non-tabular subclasses must both be added. Every time a new presentation style is added, active and passive subclasses must both be added. The team needs to add a chart-based presentation style.

**Pattern confirmed:** Tease Apart Inheritance — same adjective prefix ("Tabular") appears in both branches; the hierarchy is growing combinatorially.

**Two-dimensional grid:**

```
             | Active Deal | Passive Deal |
-------------|-------------|--------------|
(single)     |      X      |      X       |
Tabular      |      X      |      X       |
```

**Decision — which job stays:** Deal type (Active/Passive) has more code; presentation style (single/tabular) has less. Extract presentation style.

**Campaign milestones:**

Milestone 1 (Day 1-2): Apply Extract Class at `Deal` superclass — create `PresentationStyle`. Add `presentation` instance variable to `Deal`. Tests pass.

Milestone 2 (Day 3-5): Create `TabularPresentationStyle` and `SinglePresentationStyle` subclasses of `PresentationStyle`. Initialize `presentation` in `TabularActiveDeal` and `TabularPassiveDeal` constructors to `TabularPresentationStyle`. Tests pass.

Milestone 3 (Day 6-10): Apply Move Method in each tabular subclass — move presentation-related methods to `TabularPresentationStyle`. When a subclass is empty, delete it. Apply Move Method in single subclasses similarly. Tests pass after each deletion.

Milestone 4 (Day 11-12): Apply Pull Up Method/Field to simplify each hierarchy now that they are separated. Tests pass.

**Stopping condition:** `TabularActiveDeal` and `TabularPassiveDeal` are deleted. Adding `ChartPresentationStyle` requires only one new class.

---

### Example 2: Separate Domain from Presentation — Order Window

**Situation:** An `OrderWindow` class (400 lines) handles all GUI rendering and also contains SQL queries for fetching product prices, customer discount calculations, and order total computation. The team cannot unit test pricing logic because it is embedded in GUI event handlers.

**Pattern confirmed:** Separate Domain from Presentation — SQL statements in a window class, business calculation in event handlers.

**Purpose:** Make pricing logic unit-testable without a running GUI.

**Campaign milestones:**

Milestone 1 (Day 1): Create `Order` domain class linked from `OrderWindow`. Create `OrderLine` for grid rows. Tests pass (no behavior moved yet).

Milestone 2 (Day 2-5): Examine each field. `customerCodes` field is not displayed — apply Move Field directly to `Order`. Display fields (`customerName`, `amount`) — apply Duplicate Observed Data: add mirrored fields to `Order` with sync. Tests pass.

Milestone 3 (Day 6-15): Apply Extract Method to isolate SQL calls and pricing calculations in `OrderWindow`. Apply Move Method to transfer each extracted operation to `Order`. Drive all SQL toward `Order`. Tests pass after each move.

**Observable stopping signal:** `OrderWindow` no longer imports `java.sql`. Pricing methods exist on `Order` and can be unit tested without instantiating the GUI.

---

### Example 3: Extract Hierarchy — Billing Scheme (Variant A)

**Situation:** `BillingScheme` has flags for disability status, lifeline status, and business type. Every method contains conditional logic checking these flags. Adding a new billing category requires editing conditional logic in eight methods.

**Pattern confirmed:** Extract Hierarchy, Variant A — variations not fully clear upfront; flags static during object lifetime.

**First variation picked:** disability scheme.

**Campaign milestones:**

Milestone 1: Apply Replace Constructor with Factory Method on `BillingScheme`. Create `DisabilityBillingScheme` subclass. Factory method returns `DisabilityBillingScheme` when disability flag is set. Tests pass.

Milestone 2: Copy `createBill` to `DisabilityBillingScheme`. Simplify — remove branches that check `disabilityScheme()` since the subclass is always in disability context. Tests pass.

Milestone 3: Continue for other methods with disability conditionals. Pick next variation (lifeline). Create `LifelineBillingScheme`. Repeat. Tests pass after each subclass iteration.

Milestone 4: When all variations are subclassed, declare `BillingScheme` abstract. Delete conditional method bodies from the superclass. Tests pass.

**Stopping condition:** Adding a new billing category requires creating one new subclass of `BillingScheme` — no edits to existing classes.

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/big-refactoring-patterns.md` | Full mechanics for all four patterns with decision tables and edge cases | Step 2 — selecting execution strategy |

**Related skills:**
- `code-smell-diagnosis` — run first to identify which pattern applies (Parallel Inheritance Hierarchies, Data Class, or Large Class god class)
- `build-refactoring-test-suite` — run before starting any campaign to establish the safety net
- `method-decomposition-refactoring` — for the Extract Method and Move Method steps within the campaign
- `conditional-simplification-strategy` — for the Replace Conditional with Polymorphism steps in Extract Hierarchy

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler and Kent Beck.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-code-smell-diagnosis`
- `clawhub install bookforge-build-refactoring-test-suite`
- `clawhub install bookforge-method-decomposition-refactoring`
- `clawhub install bookforge-conditional-simplification-strategy`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
