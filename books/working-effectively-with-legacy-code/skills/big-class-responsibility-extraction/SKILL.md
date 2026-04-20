---
name: big-class-responsibility-extraction
description: "Identify and extract responsibilities from an oversized class using Feathers' 7 heuristics + feature sketches. Use whenever a developer faces 'this class is too big', 'god class', 'monster class', '500-line class', 'class with 50+ methods', 'class with too many responsibilities', 'SRP violation', 'hard to test because class does too much', 'team keeps editing same class', 'merge conflicts on one class'. Activates for 'single responsibility', 'extract class', 'class decomposition', 'responsibility split', 'interface segregation', 'class bloat', 'swamp class', 'god object', 'feature sketch', 'class too big'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/big-class-responsibility-extraction
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [20]
domain: software-engineering
tags: [legacy-code, refactoring, software-engineering, code-quality, srp, interface-segregation]
depends-on:
  - change-effect-analysis
  - dependency-breaking-technique-executor
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Oversized class source file + optional change history + current change triggering the refactor"
  tools-required: [Read, Grep]
  tools-optional: [Bash, Edit]
  mcps-required: []
  environment: "Codebase; git log access improves H7 (focus on current work) accuracy."
discovery:
  goal: "Produce a responsibility map and incremental extraction plan for a big class — act only when a change triggers the work."
  tasks:
    - "Detect the Incremental Class Bloat pattern"
    - "Apply the 7 responsibility heuristics"
    - "Build a feature sketch to find internal clusters"
    - "Produce a responsibility map"
    - "Produce an incremental extraction plan tied to current change"
  audience:
    roles: [software-engineer, backend-developer, tech-lead]
    experience: intermediate-advanced
  when_to_use:
    triggers:
      - "A class has 50+ methods or many instance variables"
      - "Merge conflicts concentrate on one class"
      - "Multiple reasons to change the same class"
      - "Testing is hard because of class size"
    prerequisites:
      - skill: change-effect-analysis
        why: "Before extracting, know the blast radius of proposed changes"
    not_for:
      - "Small classes with local issues (use smaller refactorings)"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 13
    iterations_needed: null
---

# Big Class Responsibility Extraction

## When to Use

Apply this skill when you encounter a class that has become a "swamp" — one that has accumulated so many responsibilities that changing it is slow, risky, and conflict-prone. The immediate trigger signal is any of:

- The class has 50+ methods or a large number of instance variables
- Multiple developers are colliding on edits in the same iteration
- You cannot describe what the class does in a single sentence without using "and"
- Adding a test requires understanding the entire class
- Merge conflicts cluster on one file repeatedly

**What this skill does NOT do:** it does not prescribe a full rewrite schedule. The output is a responsibility map and an incremental extraction plan that you act on only when a change touches a responsibility area.

## Context and Input Gathering

Before starting, collect:

1. **Class source path** — the full file for the oversized class
2. **Method inventory** — a complete list of all methods and their access modifiers (public, private, protected)
3. **Instance variable list** — all fields and their types
4. **Current change** — the specific ticket, feature, or bug fix that brought you here today
5. **Change history** (optional) — `git log --follow -p <file>` reveals who edits what, and how often multiple responsibilities change together

## Process

### Step 1: Confirm the Big Class Pattern

Verify the class meets the threshold for this skill. A big class has two or more of:

- 50+ methods (or 20+ public methods)
- 10+ instance variables
- Multiple developers modifying it in the same sprint
- Inability to write a test for a single method without setting up the entire class
- Methods that require reading through large blocks of unrelated code to understand

If the class is borderline, check git history: if the same file appears in commits for unrelated features (login, notifications, billing), the bloat is confirmed.

### Step 2: Name the Anti-Pattern — Incremental Class Bloat

Before doing any analysis, name what happened. The class became a swamp through **Incremental Class Bloat**: each new feature added a few lines or a method because "the data I need is already here." No single commit was catastrophic. Thirty small decisions compounded into a structural problem.

Naming this matters because it prevents the team from repeating it. The rule going forward: when you reach for data in an existing class to add new behavior, ask whether that behavior *belongs* to this class or whether it should live in a class that *uses* this class.

### Step 3: Apply the 7 Heuristics to Find Responsibility Candidates

Work through each heuristic. Not all will fire — stop when you have enough candidates to drive the current change.

**H1 — Group Methods:** Write down every method with its access modifier. Look for naming clusters — groups of methods that share a common noun or verb prefix. For example: `authenticate()`, `validateToken()`, `refreshSession()` form one cluster; `sendWelcomeEmail()`, `sendResetEmail()` form another. Each distinct cluster is a candidate responsibility.

*Why:* Method names are the developer's primary signal about what a method is for. Clusters that share a purpose usually share a responsibility.

**H2 — Look at Hidden Methods:** Count the private and protected methods. If there are far more private methods than public ones, a hidden class is trying to emerge. The test: if you made a private method public, would it feel odd on this class? If yes, it belongs on a different class.

*Why:* The RuleParser example (see Examples section) has 2 public methods and many private ones. The private cluster around `nextTerm` and `hasMoreTerms` is a `TermTokenizer` in disguise.

**H3 — Look for Decisions That Can Change:** Identify hard-coded assumptions — a specific database, a fixed API endpoint, a particular algorithm. These are not just implementation details; they are responsibilities. If the decision could change independently of everything else the class does, it can be extracted.

*Why:* A change to the hard-coded decision would ripple through methods that have no other reason to change together. Extraction creates a seam.

**H4 — Look for Internal Relationships (Feature Sketches):** Draw a rough diagram — circles for each instance variable, circles for each method. Draw an arrow from each method to every instance variable or other method it reads or modifies. Look for clusters: groups of methods and variables with dense internal connections but few lines crossing to the rest of the diagram.

The connection between clusters — a thin set of lines linking two otherwise independent groups — is a **pinch point**. The pinch point defines the interface a new class would present.

*Why:* Feature sketches make latent structure visible without requiring you to read all the code. Clusters with pinch points are extractable with low risk.

**H5 — The Primary Responsibility Sentence Test:** Try to describe the class in one sentence. Each time you add an "and" or "also" clause, you have identified a secondary responsibility. Example: "UserManager handles authentication **and** stores preferences **and** sends notifications" — three distinct responsibilities.

*Why:* The Single Responsibility Principle says a class should have one reason to change. Each "and" clause in your sentence is a separate reason to change.

**H6 — Scratch Refactoring:** If heuristics H1–H5 do not give you clear candidates, do a scratch refactoring. Spend 20–30 minutes extracting classes and methods freely, ignoring test coverage and production risk. The goal is not to produce working code — it is to reveal what structure is latent in the class. Throw away the scratch work; keep the insights.

*Why:* Sometimes the structure is only visible once you start moving things. Scratch refactoring is an exploration tool, not a commitment.

**H7 — Focus on the Current Work:** Look at the specific change you need to make today. The code you are adding or modifying is in a particular responsibility area. That area — and only that area — is a candidate for extraction right now.

*Why:* The current change is telling you what the software needs to evolve. Recognizing that a new capability represents a separable responsibility is enough to justify extracting it. You do not need to refactor the whole class — only the responsibility the change touches.

### Step 4: Build a Feature Sketch for the Top Candidate

For the responsibility cluster that H4 or H7 identified as most relevant to your current change:

1. List all methods and instance variables on paper or in a text file
2. For each method, note which instance variables and other methods it reads or writes
3. Draw arrows: method → variable/method it uses
4. Circle groups that have dense internal arrows and thin external connections
5. Identify the pinch point: the crossing lines between the candidate cluster and the rest of the class

The feature sketch does not need to be precise. It is a disposable tool — make it in 10 minutes, use it, discard it.

### Step 5: SRP Sentence Test and Two-Level Check

Write the one-sentence description of the class. Then check two levels:

**Interface-level SRP:** Does the class *appear* to have too many responsibilities based on its public API? If so, consider adding per-client interfaces (Interface Segregation Principle). Clients that only need a subset of the class's behavior can depend on the interface rather than the full class.

**Implementation-level SRP:** Does the class *actually do* the work, or does it delegate to helper classes? If it already delegates, the violation is only at the interface level — less urgent. If it actually does everything itself, extraction is urgent.

Always address implementation-level SRP first. Introducing delegation is safer and sets the stage for interface-level cleanup later.

### Step 6: Produce the Responsibility Map

Summarize findings from H1–H5 into a responsibility map. Format:

```
Class: <ClassName>
Primary responsibility: <one sentence>

Identified responsibilities:
  R1: <name> — methods: [...], variables: [...]
  R2: <name> — methods: [...], variables: [...]
  R3: <name> — methods: [...], variables: [...]

Pinch points:
  R1 ↔ R2: <method that connects them>
  R2 ↔ R3: <method that connects them>

Current change touches: R<N>
```

### Step 7: Produce the Incremental Extraction Plan

**Strategy:** Do not schedule a refactoring week. Identify all responsibilities, share the map with the team, then extract on an as-needed basis. When a change touches a responsibility, extract that responsibility at that time.

**Tactics for the current change:**

1. Identify the responsibility area the current change touches (from the map)
2. List all methods and instance variables belonging to that responsibility
3. If tests exist for those methods, use Extract Class with full delegation. Feathers' safe extraction steps when tests are absent:
   a. Separate the target instance variables into a distinct block in the class declaration
   b. Extract the bodies of target methods to new methods, prefixed `MOVING_`
   c. Verify — by text search, not just compile — that no moved variables are accessed outside the moved methods
   d. Create the new class; move the `MOVING_`-prefixed methods and variables into it
   e. Create an instance of the new class in the old class and delegate
   f. Remove the `MOVING_` prefix from all moved methods
4. The old class now delegates to the new class for that responsibility — SRP at the implementation level
5. If client code must also change, that work is deferred until you have tests around those clients

**What to defer:** All other responsibilities in the map stay in the class for now. The map is a shared record — the team knows the direction, and each change moves one step toward it.

## Inputs

| Input | Required | Source |
|-------|----------|--------|
| Class source file | Yes | Codebase |
| Method + variable list | Yes | Read/Grep the source file |
| Current change description | Yes | Ticket, PR, or developer context |
| Git log for the file | Optional | `git log --follow -p <file>` |

## Outputs

**responsibility-map.md** — The results of H1–H5 analysis: method clusters, hidden method findings, decision candidates, feature sketch clusters, sentence test result, two-level SRP assessment.

**extraction-plan.md** — Incremental extraction steps tied to the current change: which responsibility to extract now, which methods and variables move, the safe step-by-step procedure, and what is deferred.

## Key Principles

- **Don't binge-refactor.** Extract only what the current change requires. The rest of the map informs future changes; it does not mandate immediate action.
- **SRP has two levels.** A class can violate SRP at the interface (looks too big) without violating it at the implementation (actually delegates). Always fix implementation-level first.
- **Private-method clusters are hidden classes trying to emerge.** Many private methods on a class is a signal, not a coincidence.
- **Feature sketches are disposable.** Rough, fast, and thrown away after use. They are not UML diagrams and should not be maintained.
- **The sentence test is the fastest signal.** If you need "and" to describe the class, you have found at least two responsibilities in under a minute.
- **Scratch refactoring is exploration, not commitment.** Code produced in scratch refactoring is thrown away. Insights from it are kept.
- **The current change is your guide.** The change tells you what the software is being asked to do. That is the area to clean up.

## Examples

### Example 1: RuleParser — Method Grouping Reveals 4 Responsibilities

`RuleParser` has 2 public methods (`evaluate`, `addVariable`) and many private methods (`nextTerm`, `hasMoreTerms`, several `*Expression` methods).

Apply H1 (group methods): the `*Expression` methods cluster together (evaluation); `nextTerm` and `hasMoreTerms` cluster together (tokenization); `addVariable` stands alone with the `variables` field (variable management); `evaluate` anchors parsing.

Apply H2 (hidden methods): the private `nextTerm`/`hasMoreTerms` group would not feel odd as public methods — but only on a class called `TermTokenizer`, not on `RuleParser`.

**Responsibility map:** Parsing, Expression evaluation, Term tokenization, Variable management.

**Extraction plan:** When the next change touches tokenization (e.g., new term syntax), extract `TermTokenizer` with `nextTerm`, `hasMoreTerms`, and the `currentPosition` field. Delegate from `RuleParser`. Leave the other responsibilities in place until a change triggers them.

---

### Example 2: UserService — Feature Sketch Reveals 3 Clusters

`UserService` has 82 methods and 30+ instance variables. Four developers modify it in every sprint and hit merge conflicts weekly.

Apply H4 (feature sketch): draw method-to-variable arrows. Three dense clusters emerge with thin connections between them:
- Cluster A: `authenticate()`, `validateToken()`, `refreshSession()` + `sessionStore`, `tokenSecret`
- Cluster B: `getPreferences()`, `updatePreferences()`, `resetPreferences()` + `preferenceStore`, `defaultPrefs`
- Cluster C: `sendWelcomeEmail()`, `sendResetEmail()`, `queueNotification()` + `emailClient`, `notificationQueue`

Apply H5 (sentence test): "UserService authenticates users **and** manages preferences **and** sends notifications" — three clauses, three responsibilities.

**Extraction plan for the current sprint's social login feature:** The feature touches authentication. Extract `AuthenticationService` with Cluster A methods and variables. Delegate from `UserService`. Cluster B and C remain until a change touches them.

---

### Example 3: Change-Triggered Extraction for a Pricing Ticket

A ticket arrives: "Change the pricing calculation to support volume discounts." `PricingEngine` has 60 methods covering pricing, tax calculation, invoice formatting, and coupon redemption.

Apply H7 (focus on current work): the volume discount change touches the pricing calculation methods. Apply H4 to find the pricing cluster: `calculateBasePrice()`, `applyDiscount()`, `computeTotal()` + `priceTable`, `discountRules`.

**Extraction plan:** Extract `PriceCalculator` with the pricing cluster. The `calculateBasePrice()` and `applyDiscount()` methods become public on `PriceCalculator`; `PricingEngine` delegates to it. Add the volume discount logic to `PriceCalculator`. Tax, formatting, and coupons remain in `PricingEngine` for now.

This is change-triggered extraction: the ticket forced you to touch pricing, and that is the right time to clean it up.

## References

- Working Effectively with Legacy Code, Michael C. Feathers (2004), Chapter 20: This Class Is Too Big and I Don't Want It to Get Any Bigger
- Refactoring: Improving the Design of Existing Code, Martin Fowler — Extract Class technique
- Single Responsibility Principle: Robert C. Martin, Agile Software Development (2002)
- Interface Segregation Principle: Robert C. Martin

## License

CC-BY-SA 4.0 — BookForge Skills contributors. Source book content is copyright Michael C. Feathers / Prentice Hall. This skill distills techniques into executable guidance; it does not reproduce substantial portions of the text.

## Related BookForge Skills

**Dependencies (run these first):**
- `change-effect-analysis` — trace the blast radius of a change before extracting
- `dependency-breaking-technique-executor` — break dependencies that block extraction

**Cross-references (apply alongside):**
- `scratch-refactoring-for-code-understanding` — the H6 heuristic in standalone form
- `monster-method-decomposition` — the method-level analog of this skill
- `dependency-breaking-technique-executor` — when extraction is blocked by deep coupling
