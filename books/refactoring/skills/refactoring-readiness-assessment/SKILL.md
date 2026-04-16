---
name: refactoring-readiness-assessment
description: "Assess whether a codebase situation warrants refactoring and determine the right approach before any structural changes begin. Use this skill when a developer is about to modify existing code and needs to decide: should I refactor first, refactor not at all, or rewrite entirely? Triggers include: developer is adding a feature and the existing code is hard to understand or extend; developer just received a bug report and suspects the code structure is hiding more bugs; a code review has surfaced design concerns and the team wants concrete guidance; code appears to have been copied more than twice in similar form; developer is unsure whether to clean up code before a deadline; codebase uses a published interface or is tightly coupled to a database schema and the developer wants to know the constraints before restructuring; developer suspects the code is so broken it cannot be stabilized without a full rewrite. This skill produces a structured go/no-go assessment and session plan — it does not apply any refactoring itself. Use code-smell-diagnosis after this skill to identify specific smells, then individual refactoring skills to apply transformations."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/refactoring-readiness-assessment
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler", "Kent Beck", "John Brant", "William Opdyke", "Don Roberts"]
    chapters: [2, 15]
tags: [refactoring, code-quality, software-design]
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: description
      description: "User's description of the code situation: what they are trying to do (add feature, fix bug, review, clean up), what the code looks like, and any constraints (deadline, published interface, database coupling)"
  tools-required: []
  tools-optional: [Read]
  mcps-required: []
  environment: "Any agent environment; user supplies context in text form or answers guided questions. No code changes are made during this skill."
discovery:
  goal: "Produce a structured refactoring readiness assessment: go/no-go decision, opportunity trigger classification, constraint inventory, Two Hats protocol plan, and session discipline rules for this specific situation"
  tasks:
    - "Identify which of the four opportunity triggers applies to the current situation"
    - "Check for hard blockers (non-stabilizable code, published interfaces, deadline proximity, database coupling)"
    - "Apply the refactor-vs-rewrite heuristic if scale of decay is uncertain"
    - "Determine Two Hats sequencing: which hat first, what the boundary is, how to track hat switches"
    - "Define session discipline rules: goal statement, step size, stop condition, backtrack trigger, pairing recommendation"
    - "Produce the go/no-go recommendation with rationale and next steps"
  audience: "Software developers, senior developers, and tech leads deciding whether and how to refactor existing code before making changes"
  triggers:
    - "Developer is about to add a feature and the code is hard to follow"
    - "Bug report received and code structure may be obscuring more bugs"
    - "Code review surfaced design concerns requiring restructuring guidance"
    - "Same or similar code appears in three or more places"
    - "Developer is unsure whether cleanup is worth the time before a deadline"
    - "Code may be too broken to stabilize safely for refactoring"
    - "Published API or database schema may constrain refactoring options"
---

# Refactoring Readiness Assessment

## When to Use

You are about to change existing code — adding a feature, fixing a bug, doing a code review, or cleaning up — and you are not sure whether to refactor first, refactor not at all, or start from scratch.

This skill runs before any code changes. It answers three questions:

1. **Should we refactor?** (Go / No-go)
2. **If yes, what approach?** (Opportunity trigger, Two Hats plan, session rules)
3. **What are the risks?** (Constraint inventory, stop conditions, backtrack rules)

**What this skill does NOT do:**

- It does not apply any refactoring transformations (use `method-decomposition-refactoring`, `conditional-simplification-strategy`, or other catalog skills for that)
- It does not diagnose specific code smells (use `code-smell-diagnosis` after this assessment)
- It does not plan a large multi-session effort (use `big-refactoring-planner` for codebase-scale work)

---

## Context and Input Gathering

### Required (ask if not provided)

- **Immediate task:** What are you trying to do right now — add a feature, fix a bug, review someone's code, or clean up in general?
  -> Ask: "What brought you to the code today?"

- **Code description:** What does the code look like? Long methods, duplicated blocks, tangled conditionals, hard-to-name concepts?
  -> Ask: "Describe the code you are looking at. What makes it difficult to work with?"

- **Test coverage:** Do you have automated tests that verify the current behavior?
  -> Ask: "If you change the code, how do you know it still works?" (This is the single most important safety question.)

### Useful (gather if present)

- **Deadline context:** Is there a deployment, release, or sprint deadline within the next few days?
- **Interface visibility:** Is the code behind a published API, a library interface, or a database schema that external code depends on?
- **Size estimate:** Is this a single method, a class, a module, or a subsystem?
- **Prior rewrite history:** Has this code been rewritten before without improving it?

---

## Process

### Step 1 — Classify the Opportunity Trigger

**Why:** Fowler identifies four specific situations where refactoring is most valuable. Knowing which trigger applies sets the scope and urgency of the refactoring session. Refactoring without a trigger is speculative and hard to time-box.

Identify which trigger best matches the user's situation:

**Trigger A: Rule of Three (Don Roberts)**
The same or structurally similar logic appears in three or more places. The third occurrence is the signal to refactor — not the first (do it), not the second (wince but proceed), but the third.

- Signal: Developer says "I keep copy-pasting this," or three methods share identical structure with minor variations.
- Scope: Extract the shared pattern. Eliminate duplicates. The refactoring is bounded by the duplication.

**Trigger B: Refactor When Adding a Feature**
The code is hard to understand or extend for the planned addition. Refactoring first makes the feature addition faster, not slower — once the code is well-structured, adding the feature is straightforward.

- Signal: Developer says "I need to add X but I can't figure out where it goes" or "the design doesn't support this."
- Scope: Refactor only until the code is ready to receive the new feature. Stop when the feature can be added cleanly. The feature is not added during the refactoring hat.

**Trigger C: Refactor When Fixing a Bug**
A bug report is a sign that code was not clear enough to reveal the bug during development. Refactoring to understand the code often exposes the bug itself, and the improved structure prevents similar bugs.

- Signal: Developer is reading code to understand how a bug could exist. Refactoring improves that understanding, and fixing the code reveals the bug.
- Scope: Refactor enough to make the logic visible and the bug obvious. The bug fix itself happens after switching to the adding-function hat.

**Trigger D: Refactor During Code Review**
Code review is the ideal moment to suggest structural improvements while the author is present and the code is being read fresh. Implementing suggestions in the review session (small review groups) creates more concrete outcomes than suggestions alone.

- Signal: Review session has identified design concerns or clarity issues beyond style. A single reviewer and the original author are present.
- Scope: Apply refactorings that can be demonstrated during the review session. Defer large structural changes to a separate session with a stated goal.

Record the trigger classification. If more than one applies, use the primary motivation for this session.

---

### Step 2 — Check Hard Blockers

**Why:** Some situations make refactoring unsafe, premature, or impossible to complete successfully. Proceeding into these situations without acknowledging the constraints leads to half-finished refactorings that leave the code worse than before.

Run through each blocker category:

**Blocker 1: Non-stabilizable code (rewrite candidate)**
The code does not work correctly and cannot be made to work mostly correctly before refactoring.

- Test: Can you run the existing code, write tests that capture its current behavior, and get those tests passing — before touching the structure?
- If no: Do not refactor. The code cannot be made safe for transformation. Evaluate the rewrite heuristic in Step 3 instead.
- Signal phrase: "The code is so full of bugs that I can't even figure out what it's supposed to do."

**Blocker 2: Deadline proximity**
A release, deployment, or hard commitment is within a few days.

- Fowler's rule: Refactoring near a deadline creates debt that appears after the deadline — the productivity gain lands too late to matter. Ward Cunningham describes this as design debt: you can carry it, but the interest payments (maintenance cost, slower development) will come due.
- If deadline is imminent: Do not start a refactoring session. Make a note of the debt explicitly. Schedule refactoring for after the delivery.
- Exception: A tiny, clearly bounded refactoring (e.g., renaming one confusing variable) that takes under five minutes is acceptable even near a deadline. Anything requiring structural changes is not.

**Blocker 3: Published interfaces**
The code exposes methods or APIs that external code depends on and that you cannot find and change everywhere.

- Risk: Many refactorings change interfaces. Rename Method on a published API breaks callers you do not control.
- Approach if present: You can still refactor internal implementations. You cannot remove or rename the published interface without a migration strategy (keep old interface, call new one, deprecate, remove in a later version). Add this constraint explicitly to the assessment output.
- Tip from Fowler: Do not publish interfaces prematurely. Modify code ownership policies so people can change any caller before publishing. Once published, the refactoring cost multiplies.

**Blocker 4: Database schema coupling**
The code is tightly coupled to a relational database schema, and refactoring the object model would require a data migration.

- Risk: Schema changes are long-fraught tasks. Data migration in production is high-risk and often irreversible.
- Approach if present: Place a separate isolation layer between the object model and the database schema. Refactor to that layer first, so changes to one model do not force immediate changes to the other. Do not move fields across persistence boundaries without an explicit migration plan.

If one or more hard blockers are present, the assessment may be a partial go (proceed with constraints explicitly stated) or a no-go.

---

### Step 3 — Apply the Refactor-vs-Rewrite Heuristic

**Why:** Fowler is explicit that sometimes the right answer is to start over rather than refactor. But "this is a mess" is not a sufficient reason to rewrite — rewrites have their own risks, and partial rewrites that decompose by component are often better than full rewrites.

Apply this heuristic only if Blocker 1 (non-stabilizable code) triggered or if the code appears fundamentally broken:

**Signal that rewrite is warranted:**
- The existing code does not work and cannot be made to work mostly correctly
- It would be easier to start from scratch than to salvage the existing structure
- Trying to refactor it would be longer and riskier than a rewrite

**Fowler's compromise route:**
Do not rewrite the whole system. Decompose it into components with strong encapsulation. Evaluate the refactor-vs-rewrite decision one component at a time. A component that is too broken to stabilize can be rewritten. Components that are poorly structured but functional can be refactored.

**Output of Step 3:**
- For each major component: Refactor (testable, structurally redeemable) or Rewrite (non-stabilizable, easier from scratch)
- Note: A mixed recommendation is common and valid. Do not let one broken component force a full-system rewrite decision.

If no blockers from Step 2 triggered and the code works, skip this step.

---

### Step 4 — Define the Two Hats Protocol

**Why:** Kent Beck's Two Hats metaphor captures the most common refactoring failure mode: developers mix structural cleanup with feature additions or bug fixes, losing track of which changes do what. When a test fails during mixed-hat work, it is impossible to know whether the refactoring broke something or the feature change introduced a bug. Keeping the hats separate preserves this diagnostic clarity.

**The Two Hats:**

- **Adding-function hat:** You add new behavior. You do not change existing code structure. You add tests. You add capabilities. Observable behavior changes.
- **Refactoring hat:** You restructure existing code. You do not add new behavior. You do not add tests (unless you find a case you missed). Observable behavior must not change. Tests pass before and after every step.

**Rules:**
1. You wear exactly one hat at a time. Never both simultaneously.
2. When you realize you need to switch hats, finish your current step, verify tests pass, then switch.
3. Keep a list of hat-switch requests — things you notice that need doing in the other hat. Do not act on them immediately. Act on them when you switch hats.

**For this session, determine:**

- Which hat do you wear first?
  - Trigger B (adding feature): Refactoring hat first. Switch to adding-function hat once the code is ready.
  - Trigger C (fixing bug): Refactoring hat first to understand the code. Switch to adding-function hat to apply the fix.
  - Trigger A (Rule of Three) or Trigger D (code review): Refactoring hat only. No feature work.
  
- What is the hat-switch boundary?
  - State it explicitly: "I will switch to adding-function hat when [specific condition]."
  - Example: "I will switch when the OrderProcessor class has a single clear method for each processing step and all existing tests pass."

- How will you track hat-switch requests?
  - Keep a notepad (physical or digital) for "things to do in the other hat." Write observations there during a session. Do not act on them.

---

### Step 5 — Define Session Discipline

**Why:** Kent Beck's session rules from Chapter 15 are the most commonly skipped part of refactoring practice and the source of most refactoring failures. Without them, developers refactor for too long without testing, get lost, cannot find the source of a test failure, and abandon the session mid-stream — leaving the code in a worse state than when they started. The rules are designed to make stopping and backtracking safe rather than shameful.

Define these five rules for this specific session:

**Rule 1: Pick a goal**
State the refactoring goal in one sentence before touching the code. "I am refactoring to [specific outcome] so that [specific next task] becomes possible."

- The goal bounds the session. Refactoring that does not serve the stated goal is deferred.
- Example: "I am refactoring to extract the fee calculation from OrderProcessor so that I can add the promotional pricing feature without touching the core calculation."

**Rule 2: Move in small steps**
Each step is the smallest transformation that leaves the code in a consistent, passing state. Run tests after each step — not after every three steps, not at the end.

- Why: When a test fails, you want to know exactly which one-step change caused it. If you made three changes before running tests, you have a debugging problem, not a refactoring session.
- If a step feels too large, decompose it into smaller steps.

**Rule 3: Stop when unsure**
If you cannot prove to yourself that the current step preserves behavior, stop. Do not proceed.

- If the code is already better than when you started: commit or save what you have, then stop. Integrate and release.
- If the code is not better: throw away your changes. Start again with a smaller step or a more bounded goal.

**Rule 4: Backtrack to last passing state**
If a test fails and you are not certain which change caused it: do not debug. Backtrack.

- Go back to the last known good configuration where all tests passed.
- Replay your changes one by one, running tests after each. The failing test will identify the specific change.
- Why: An hour of backtracking replays in ten minutes. An hour of debugging an uncertain failure can cost two hours — and you still may not find the root cause.
- Record this rule explicitly: "If any test fails and I cannot immediately identify the cause, I will revert to last passing state and replay."

**Rule 5: Work in pairs (recommended)**
Pair programming provides three benefits specific to refactoring: it keeps step sizes small (partner observes drift), it provides a second opinion on when to stop, and it provides quiet confidence when you are uncertain. Your partner catches the moment you switch from confident steps to uncertain ones.

- Assess: Is pair programming available for this session? If not, what substitute applies? (Time-boxing the session, commit after each step as a proxy for pair check-in.)

---

### Step 6 — Produce the Assessment Output

**Why:** The assessment must be tangible and actionable. A verbal judgment ("yeah, refactor it") is not sufficient. The output is a document the developer can refer to during the session — especially the hat-switch boundary and the backtrack rule, which are hardest to remember under pressure.

Write the assessment in this structure:

---

**REFACTORING READINESS ASSESSMENT**

**Situation:** [One sentence describing the code and the immediate task]

**Opportunity Trigger:** [A / B / C / D] — [name and brief rationale]

**Go / No-Go Recommendation:** [Go / No-Go / Conditional Go]
[2-3 sentences explaining the recommendation]

**Constraint Inventory:**
- Tests available: [Yes / No / Partial — what needs to be added before proceeding]
- Published interfaces: [None / Present — [which ones, constraints]]
- Database coupling: [None / Present — [migration risk level]]
- Deadline: [None within session / Imminent — [do not proceed recommendation]]

**Refactor vs. Rewrite:**
- [If applicable] Component X: Refactor | Rewrite — [rationale]
- [If no blockers triggered] Not evaluated — code is stabilizable

**Two Hats Plan:**
- First hat: [Refactoring | Adding-function]
- Hat-switch boundary: [Explicit condition]
- Hat-switch request tracker: [How to record observations during the session]

**Session Discipline Rules:**
- Goal: [One-sentence refactoring goal]
- Step size: [Specific — e.g., "one method extraction per step, tests after each"]
- Stop condition: [When to stop for the session]
- Backtrack trigger: [Any failing test I cannot immediately explain → revert to last passing state]
- Pairing: [Yes / No — if no, substitute]

**Next Steps:**
1. [First concrete action: e.g., "Add tests for OrderProcessor.process() to establish baseline"]
2. [Second action: e.g., "Run code-smell-diagnosis on OrderProcessor to identify which smells to address"]
3. [Third action: e.g., "Apply method-decomposition-refactoring to extract fee calculation"]

---

## Key Principles

**Refactoring is not a scheduled activity.** Fowler is explicit: do not allocate two weeks every few months to refactoring. Refactoring happens in small bursts, triggered by real tasks. You refactor because you want to do something else, and refactoring helps you do that other thing.

**The code must work before you refactor.** Refactoring restructures working code. Code that does not work mostly correctly cannot be safely transformed — every refactoring step's safety depends on tests that confirm behavior is preserved.

**Design debt accrues interest.** Ward Cunningham's framing: unfinished refactoring is debt. Some debt is necessary to function. But the interest payment is the extra cost of maintenance and slow development caused by overly complex code. When the payments become too great, you are overwhelmed.

**Not having enough time to refactor is a sign you need to refactor.** Tight schedules that prevent cleanup cause the conditions that make schedules tight. If you never have time to clean up, you are paying the interest on accumulated design debt.

**A big refactoring is a recipe for disaster.** Beck's warning from Chapter 15 is direct: when you see all the problems at once and want to clean up everything in sight, resist. Nibble at the problem — take a few minutes to clean up an area when you are about to add functionality there. A three-month cleanup halt is not acceptable to any organization and they are right to refuse it.

---

## Examples

### Example A: Feature Addition (Trigger B)

**Situation:** Adding promotional pricing to OrderProcessor. The method is 200 lines long, mixes fee calculation, tax computation, and discount application in a single block.

**Assessment:**
- Trigger: B (Refactor when adding a feature)
- Go: Yes — tests exist for current behavior, no published interface, no deadline this week
- First hat: Refactoring
- Hat-switch boundary: "When OrderProcessor has separate methods for fee calculation, tax computation, and discount application and all tests pass"
- Goal: "Extract fee calculation into its own method so the promotional pricing hook has a single, clear insertion point"
- Backtrack rule: "Any failing test I cannot explain in thirty seconds → revert to last commit"
- Next step: Run code-smell-diagnosis on OrderProcessor, then apply method-decomposition-refactoring

---

### Example B: Bug Fix (Trigger C)

**Situation:** Bug report: "discounts not applying correctly for international orders." Code mixes currency handling with discount logic in several places.

**Assessment:**
- Trigger: C (Refactor when fixing a bug)
- Conditional Go: Tests exist, but they do not cover international order paths — add tests first
- First hat: Refactoring hat (to understand the code and make the logic visible)
- Hat-switch boundary: "When the discount application logic is isolated and I can see exactly where the international order path diverges"
- Goal: "Clarify the discount calculation path well enough that the bug becomes visible"
- Stop condition: "Stop refactoring the moment the bug is visible — switch to adding-function hat to fix it"
- Backtrack rule: Standard — revert to last passing state on any unexplained failure

---

### Example C: Rewrite Candidate

**Situation:** Legacy billing module. Known to produce incorrect results in certain scenarios. Cannot write tests that pass because the existing behavior is wrong.

**Assessment:**
- Trigger: None of A/B/C/D applies cleanly — the code does not work
- No-Go for refactoring: Cannot stabilize the code before refactoring
- Refactor vs. Rewrite: Evaluate component by component
  - BillingCalculator: Rewrite — non-stabilizable, too broken to test
  - InvoiceFormatter: Refactor — works correctly, poor structure only
  - PaymentGatewayAdapter: Refactor — stable behavior, interface can be preserved
- Next step: Isolate InvoiceFormatter and PaymentGatewayAdapter first; rewrite BillingCalculator behind a clean interface boundary

---

### Example D: Deadline Proximity (No-Go)

**Situation:** Release is tomorrow. Developer wants to clean up the authentication module because it has been bothering them.

**Assessment:**
- No-Go: Productivity gain from refactoring would land after the deadline, not before
- Action: Make a note of the specific concerns (e.g., "AuthService.authenticate() is 150 lines mixing session management with credential validation"). Schedule refactoring for the next working day after release.
- Rule: Even a "quick" refactoring near a deadline expands into unexpected scope. The right time to have done this was before the deadline pressure began.

---

## References

- `references/two-hats-protocol.md` — Extended Two Hats guidance including hat-switch request tracking templates and pair programming patterns for refactoring sessions
- `references/refactoring-constraints.md` — Detailed guidance on published interface migration strategies, database schema isolation layers, and design debt management

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler with Kent Beck, John Brant, William Opdyke, and Don Roberts.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-code-smell-diagnosis`
- `clawhub install bookforge-method-decomposition-refactoring`
- `clawhub install bookforge-big-refactoring-planner`
- `clawhub install bookforge-build-refactoring-test-suite`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
