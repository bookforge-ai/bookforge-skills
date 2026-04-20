---
name: scratch-refactoring-for-code-understanding
description: "Guide a developer through throwaway refactoring — restructure code freely without tests to understand it, then DISCARD. Use whenever a developer says 'I don't understand this code', 'this code is too complex to change safely', 'need to read legacy code', 'can't figure out what this does', 'overwhelmed by legacy', 'code archaeology', 'understand before change'. Also activates for 'scratch refactoring', 'throwaway refactoring', 'code comprehension', 'code reading technique', 'feature sketch', 'effect sketch', 'notes on legacy code'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/working-effectively-with-legacy-code/skills/scratch-refactoring-for-code-understanding
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: working-effectively-with-legacy-code
    title: "Working Effectively with Legacy Code"
    authors: ["Michael C. Feathers"]
    chapters: [16]
domain: software-engineering
tags: [legacy-code, refactoring, code-quality, software-engineering, code-reading]
depends-on: []
execution:
  tier: 1
  mode: full
  inputs:
    - type: codebase
      description: "Source code section the developer wants to understand"
  tools-required: [Read, Edit, Bash]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Version-controlled codebase. A git branch or scratch checkout is required so the exploration can be discarded."
discovery:
  goal: "Use throwaway refactoring to understand unfamiliar code without risking production changes."
  tasks:
    - "Isolate a scratch branch/checkout"
    - "Guide the developer through exploratory refactorings"
    - "Produce learning notes (what the code actually does)"
    - "Discard the scratch code"
    - "Warn against two failure modes (false model, attachment to scratch structure)"
  audience:
    roles: [software-engineer, backend-developer]
    experience: intermediate
  when_to_use:
    triggers:
      - "Developer does not understand legacy code well enough to change it"
      - "A change is blocked by opaque code"
      - "Onboarding to an unfamiliar codebase section"
    prerequisites: []
    not_for:
      - "Code that is already well-understood"
      - "Code under active production change — use proper characterization tests instead"
  environment:
    codebase_required: true
    codebase_helpful: true
    works_offline: true
  quality:
    scores: {with_skill: null, baseline: null, delta: null}
    tested_at: null
    eval_count: null
    assertion_count: 8
    iterations_needed: null
---

# Scratch Refactoring for Code Understanding

## When to Use

Use this skill when a developer cannot understand a section of code well enough to change it safely. Scratch refactoring is the right tool when:

- Passive reading (scrolling through code) is not producing a clear mental model
- The code is too tangled to trace by eye — hidden coupling, deep nesting, mystery variables
- You are onboarding to a codebase area with no documentation and no author to ask
- A planned change is blocked because the intent of the existing code is unknown

Scratch refactoring is a **comprehension technique**, not a production technique. It is a complement to characterization tests (which pin down behavior) and effect sketches (which map change propagation). When you need to understand structure before you can even write a characterization test, scratch refactoring is the right first step.

Do not use this skill if:
- The code is already understood — skip directly to characterization testing
- You are mid-change on a production branch — a scratch exploration on a dirty working tree risks mixing exploration with production edits

## Context & Input Gathering

Before starting, collect:

1. **Target code path** — the file(s) and class/method range the developer wants to understand. Ask if not provided.
2. **Learning goal** — what specific question the developer wants answered. Examples: "What are the phases of this algorithm?", "What does this class actually own?", "Why does this method need all these parameters?" A precise question produces a focused scratch session.
3. **VCS status** — confirm the working tree is clean (no uncommitted production changes) or that a stash is in place. A dirty working tree makes discarding the scratch exploration unsafe.
4. **Current understanding** — what the developer already knows. This prevents re-explaining what is already clear and focuses the scratch session on the opaque parts.

If the developer cannot state a learning goal, use this default: "Identify the top-level responsibilities of this code and the relationships between them."

## Process

### Step 1: Verify VCS Safety

Create a scratch branch (preferred) or confirm a clean stash before touching any file.

```bash
git checkout -b scratch/understand-<target-name>
# or, if branch creation is not practical:
git stash push -m "scratch: pre-exploration state"
```

**Why:** The discard step (Step 5) only works cleanly if the scratch branch can be deleted or the stash popped. Without this isolation, exploratory changes can accidentally survive into production code. The version-control system is the safety net — it must be set up before the exploration begins, not after.

### Step 2: Identify Target and Learning Goal

Read the target code with fresh eyes. Scan for:
- Methods over 20 lines (candidates for extraction)
- Variables with non-descriptive names (candidates for renaming)
- Conditional blocks that could be named (candidates for extraction)
- Class fields that cluster around different concepts (signals of hidden responsibilities)

Restate the learning goal as a concrete question. Write it down — this becomes the first line of your learning notes.

**Why:** Without a stated goal, scratch sessions drift. The goal acts as a stopping condition: once you can answer the question, the session is done. This prevents over-investment in the scratch structure.

### Step 3: Refactor Freely — No Tests Required

Refactor the target code without writing any tests. Common moves:

- **Extract Method** — pull a block of code into a named method to make its intent visible
- **Rename Variable / Method** — replace cryptic names with names that reflect what you now understand
- **Inline Variable** — collapse a one-use variable to see the expression directly
- **Split Conditional** — break a compound condition into named booleans
- **Reorder Methods** — group related methods together to see cohesion

Do not stop to make the code production-ready. Do not worry about performance, test coverage, or code review standards. The goal is visibility, not correctness.

**Why:** The normal constraint "do not refactor without tests" exists to prevent regressions in production code. In a scratch exploration that will be discarded, that constraint does not apply. Removing it allows rapid structural manipulation that would otherwise require a full seam-introduction and characterization-test cycle. The speed is the point.

### Step 4: Write Learning Notes

As understanding emerges — not at the end, but during the session — write down what you are learning. Do not capture the refactored structure. Capture the insights.

Learning notes template (save as `learning-notes.md` in a scratch location):

```
# Learning Notes: <target code>
Date: <today>
Question: <the learning goal from Step 2>

## Structure discovered
<plain-English description of the top-level structure: phases, responsibilities, collaborators>

## Surprises
<things that were unexpected or counterintuitive>
<any false assumptions that were corrected during the session>

## Dependencies and risks
<anything that propagates changes widely, or that the code depends on unexpectedly>

## Next-step recommendation
<what the developer should do next: write characterization tests for X, apply technique Y, investigate Z>
```

**Why:** The learning notes are the deliverable, not the refactored code. If you write down what you learned but discard the scratch code, you have everything you need. If you keep the scratch code but write nothing down, you have a dangerous artifact and no portable insight.

### Step 5: Discard the Scratch Refactoring

Delete the scratch branch or pop the stash back to the pre-exploration state.

```bash
# If you used a scratch branch:
git checkout main   # or your base branch
git branch -D scratch/understand-<target-name>

# If you used stash:
git checkout -- .
git stash pop
```

Verify the working tree is clean before moving to production work.

**Why:** Feathers is explicit: "Throw that code away." The scratch structure was shaped by the order of your discoveries, not by production design intent. Committing it introduces structure that was never evaluated against the full system, may contain mistakes made during rapid exploration, and — most insidiously — biases future refactoring by making one particular decomposition feel "already done." The insight belongs to the developer's head and the learning notes. The code belongs in the trash.

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| Target code path | Yes | File(s) and class/method to understand |
| Learning goal | Yes | The specific question to answer (elicit if not provided) |
| VCS clean state | Yes | Clean working tree or scratch branch before starting |
| Current understanding | No | What the developer already knows (prevents redundant exploration) |

## Outputs

| Output | Format | Kept or Discarded? |
|--------|--------|--------------------|
| Learning notes | `learning-notes.md` | **Kept** — the primary deliverable |
| Scratch refactored code | Modified source files on scratch branch | **Discarded** — deleted after session |

**Learning notes template** (minimum viable):

```markdown
# Learning Notes: <target>
Date: <YYYY-MM-DD>
Question: <learning goal>

## Structure discovered
<top-level structure in plain English>

## Surprises
<unexpected findings; corrected false assumptions>

## Dependencies and risks
<what propagates changes widely>

## Next-step recommendation
<characterization tests / technique / investigation to do next>
```

## Key Principles

**1. Never commit scratch refactoring — VCS is the safety net, not the deliverable.**
The version-control system exists so that the scratch branch can be deleted cleanly. Committing exploratory code introduces structure that was shaped by the order of discovery, not by production design intent. The branch is a workspace, not a feature branch.

**2. A scratch mistake can create a false mental model — verify conclusions against the original code.**
When you refactor freely, you will sometimes make extraction mistakes: a method name that implies the wrong abstraction, a grouping that hides a real coupling. If you trust the scratch structure without checking it against the original, you may carry a wrong understanding into production work. Before writing learning notes, cross-check surprising conclusions against the unmodified code (easy to do since the original is one branch switch away).

**3. Attachment to scratch structure biases real refactoring — keep the insight, not the shape.**
A scratch session that ends with "I did the refactoring already, let me just commit it" has failed. The scratch decomposition may be one valid decomposition — but it was found under comprehension pressure, without the full context of the change goal, tests, and system design. Real refactoring, done with tests and full context, will often find a better structure. The learning notes preserve what matters; discarding the code preserves the developer's ability to see that better structure.

## Examples

### Example 1: Opaque Algorithm in a Billing System

A developer needs to modify a 300-line `calculateInvoice()` method but cannot determine which lines handle tax calculation versus line-item accumulation versus discount application.

**Scratch session:**
1. Create branch `scratch/understand-calculate-invoice`.
2. Learning goal: "What are the phases of this method, and where does each phase begin and end?"
3. Extract blocks into named methods: `accumulateLineItems()`, `applyVolumeDiscounts()`, `calculateTaxByJurisdiction()`, `formatInvoiceOutput()`.
4. Learning notes record: three-phase structure (accumulate → discount → tax), tax phase reads a hidden configuration object, discount logic has a special case for government accounts.
5. Delete branch. Learning notes survive.

**Result:** The developer now knows exactly where to add the new billing adjustment — in the accumulation phase, before discounts — and what tests to write first (a characterization test for the government-account discount case).

### Example 2: Class with Tangled Responsibilities

A team inheriting a `CustomerManager` class (800 lines, no tests) cannot determine what it owns versus what it delegates.

**Scratch session:**
1. Create branch `scratch/understand-customer-manager`.
2. Learning goal: "What responsibilities does this class actually own?"
3. Rename fields and methods to reflect discovered purpose. Group by responsibility. Notice that 40% of the methods only touch a `subscription` sub-object — extract a `SubscriptionHandler` conceptually in the scratch.
4. Learning notes record: three hidden responsibilities (identity management, subscription lifecycle, notification dispatch). The subscription methods are cohesive enough to become their own class.
5. Delete branch.

**Result:** The team's real refactoring plan is now grounded: introduce a `SubscriptionHandler` class with characterization tests, extracted from `CustomerManager` using the Extract Class technique. The scratch session revealed the seam without committing premature structure.

## References

- Feathers, M. C. (2004). *Working Effectively with Legacy Code*, Chapter 16: I Don't Understand the Code Well Enough to Change It. Prentice Hall.
- Related techniques in the same chapter: Notes/Sketching, Listing Markup, Delete Unused Code.
- Chapter 13 (Characterization Tests) — the natural follow-on once the code structure is understood.
- Chapter 11 (Effect Sketches) — a complementary comprehension tool when propagation, not structure, is the unknown.

## License

This skill is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Derived from *Working Effectively with Legacy Code* by Michael C. Feathers (2004), Prentice Hall.
Attribution required on redistribution.

## Related BookForge Skills

- [`legacy-code-change-algorithm`](../legacy-code-change-algorithm/) — the six-step master procedure that scratch refactoring feeds into; use this skill first when the code is too opaque to identify change points
- [`change-effect-analysis`](../change-effect-analysis/) — use after scratch refactoring to map propagation of a planned change through the now-understood structure
- [`big-class-responsibility-extraction`](../big-class-responsibility-extraction/) — the production technique for splitting large classes discovered via scratch refactoring
