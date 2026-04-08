---
name: development-checklist-generator
description: Create effective development checklists (code completion, unit/functional testing, software release) that teams will actually follow. Use this skill whenever the user needs to create a checklist for code review, testing, deployment, or release processes, wants to improve team quality by catching recurring mistakes, has a team that ignores existing checklists because they're too long, needs to define "definition of done" for development tasks, wants to reduce production incidents caused by human error, or asks about checklist best practices for software teams — even if they don't explicitly say "checklist."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/development-checklist-generator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [22]
tags: [software-architecture, architecture, checklists, quality, process, team-effectiveness, deployment]
depends-on: []
execution:
  tier: 2
  mode: full
  inputs:
    - type: codebase
      description: "Optionally, a codebase to analyze for common issues that should be on checklists"
  tools-required: [Read, Write]
  tools-optional: [Grep, Bash]
  mcps-required: []
  environment: "Any agent environment. Codebase access optional but improves checklist specificity."
---

# Development Checklist Generator

## When to Use

You need to create or improve development checklists that catch common mistakes without becoming burdensome process overhead. Typical triggers:

- Recurring bugs or production incidents caused by the same types of mistakes
- A team that has no formal "definition of done" for code completion
- Deployment failures caused by forgotten steps (wrong config, missing migration, stale cache)
- An existing checklist that nobody follows because it's too long or procedural
- The user wants to reduce reliance on manual quality checks

Before starting, verify:
- What type of checklist is needed (code completion, testing, release)?
- What problems is the team currently experiencing?

## Context

### Required Context (must have before proceeding)

- **Checklist type:** What kind of checklist is needed?
  -> Check prompt for: "code review," "testing," "deployment," "release," "definition of done"
  -> If still missing, ask: "What type of checklist do you need — code completion, testing, or software release?"

- **Current pain points:** What problems is the team experiencing?
  -> Check prompt for: bugs, incidents, deployment failures, missed steps, recurring issues
  -> If still missing, ask: "What specific problems or recurring mistakes are you trying to prevent?"

### Observable Context (gather from environment)

- **Existing processes:** Does the team have any existing checklists or quality processes?
  -> Check prompt for: "existing checklist," "current process," "QA process," "CI/CD pipeline"
  -> If unavailable: assume no existing checklists

- **Team size and culture:** How large is the team and how process-tolerant are they?
  -> Check prompt for: team size, complaints about process, "too many meetings/processes"
  -> If unavailable: assume moderate process tolerance

- **Technology stack:** What technologies does the team use?
  -> Check prompt for: languages, frameworks, databases, deployment tools
  -> If unavailable: create technology-agnostic checklist items

- **Codebase patterns:** If codebase is available, scan for common issues
  -> Look for: hardcoded values, missing error handling, inconsistent logging, configuration patterns
  -> If unavailable: use generic best-practice items

### Default Assumptions

- If checklist type unclear -> create all three types (code completion, testing, release) starting with what addresses the pain points
- If team culture unknown -> err on the side of shorter checklists (5-10 items)
- If no existing process -> start fresh with minimal viable checklist

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Checklist type is known
- At least 2-3 specific pain points or recurring issues are described
- Technology context is available (from prompt or codebase)

PROCEED WITH DEFAULTS when:
- Checklist type is known
- General pain points can be inferred
- Technology-agnostic items will be useful

MUST ASK when:
- Neither the checklist type nor the problems are described
- The request is too vague to produce anything actionable
```

## Process

### Step 1: Distinguish Checklists from Procedures

**ACTION:** Verify that what the user needs is actually a checklist, not a procedure. If the user's current "checklist" is procedural, explain the difference and restructure it.

**WHY:** A checklist is a set of independent verification items that can be checked in any order. A procedure is a sequence of dependent steps that must be done in order. Procedures should NOT be in a checklist because items can't be verified until prior items complete. A "checklist" for creating a database table that says "1. Fill out request form, 2. Submit form, 3. Verify table created" is a procedure — the table can't be verified if the form hasn't been submitted. Conflating the two creates unusable checklists that people skip entirely.

**The test:** Can each item be independently verified regardless of order?
- YES -> it belongs on a checklist
- NO -> it's a procedural step and should be a workflow, not a checklist

**Additionally:** Simple, well-known processes that are executed frequently without error do NOT need a checklist. Checklists are for error-prone or infrequently-performed processes where items are commonly missed or skipped.

### Step 2: Apply Checklist Design Principles

**ACTION:** Design the checklist following the core principles that determine whether teams will actually use it. For detailed templates, see [references/checklist-templates.md](references/checklist-templates.md).

**WHY:** Architects have found through experience that checklists make development teams more effective — but only when designed correctly. The law of diminishing returns applies: the more checklists an architect creates, the less likely developers will use them. Checklist adoption depends on brevity, relevance, and the perception that the items actually prevent real problems.

**Principles:**

1. **Keep it small** — Developers will NOT follow large checklists. The more items, the more likely developers rubber-stamp everything. Target 5-10 items maximum per checklist. If you need more items, split into multiple purpose-specific checklists.

2. **Automate what you can** — Any item that can be checked automatically should NOT be on a human checklist. If your linter can catch formatting issues, don't put "check formatting" on the checklist. Reserve the checklist for things that REQUIRE human judgment.

3. **State the obvious** — Don't worry about stating the obvious in a checklist. The obvious items are the ones most commonly skipped or missed. If "remove hardcoded API keys" feels too obvious for the checklist, remember that every production credential leak started with someone thinking it was too obvious to check.

4. **No procedural flows** — Every item must be independently verifiable. If item B depends on item A, you have a procedure, not a checklist.

5. **Focus on error-prone areas** — Checklists are for things that go wrong, not things that always go right. If the team never forgets database migrations, don't put it on the checklist. If they regularly forget to update configuration files, that's a checklist item.

### Step 3: Generate the Appropriate Checklist Type

**ACTION:** Create the checklist based on the identified type, pain points, and technology context.

**WHY:** Each checklist type serves a different purpose in the development lifecycle. Code completion checklists define "done." Testing checklists ensure coverage of commonly missed test scenarios. Release checklists prevent deployment disasters. Creating the wrong type for the problem doesn't help.

**Code Completion Checklist (Definition of Done):**
Items to consider including:
- Coding and formatting standards not caught by automated tools
- Frequently overlooked items (absorbed exceptions, missing null validation)
- Project-specific standards (naming conventions, logging patterns)
- Special team instructions or procedures
- Security considerations (no hardcoded secrets, input validation)

**Unit and Functional Testing Checklist:**
Items to consider including:
- Edge cases specific to the domain (empty collections, boundary values, null inputs)
- Error handling paths (what happens when the dependency fails?)
- Performance-sensitive paths (are they tested under load?)
- Integration points (are external service failures simulated?)
- Data integrity scenarios (concurrent writes, transaction boundaries)

**Software Release Checklist:**
Items to consider including:
- Configuration verification (correct config for target environment)
- Database migration status (have migrations been run?)
- Cache invalidation (is stale data being served?)
- Feature flag states (are new features properly toggled?)
- Rollback plan (is there a verified rollback procedure?)
- Monitoring verification (are alerts and dashboards updated?)

### Step 4: Plan for Checklist Compliance (Hawthorne Effect)

**ACTION:** Include a compliance strategy for ensuring the team actually uses the checklist.

**WHY:** One of the biggest challenges with checklists is getting developers to actually use them rather than rubber-stamping all items as complete. Developers who are rushed will mark all items as "done" without actually performing the checks. The Hawthorne Effect provides a solution: people who know they are being observed tend to do the right thing. By letting the team know that checklists will be occasionally spot-checked for correctness, compliance increases significantly — even if the spot-checks rarely happen.

**Compliance strategies:**
1. **Communicate the why** — Explain to the team WHY each checklist item matters. Have team members read "The Checklist Manifesto" by Atul Gawande. Make sure each person understands the reasoning behind each item.
2. **Collaborate on creation** — Have developers help create the checklist items. People follow rules they helped create. Items imposed from above get resisted.
3. **Apply the Hawthorne Effect** — Let the team know that checklists will be verified periodically. The architect or tech lead occasionally spot-checks completed checklists for correctness. The knowledge that spot-checks happen (even rarely) dramatically improves honest completion.
4. **Iterate based on feedback** — Remove items that are always done correctly (they don't need a checklist). Add items when new recurring problems emerge. Keep the checklist alive and relevant.

### Step 5: Format and Deliver the Checklist

**ACTION:** Produce the checklist in a format that integrates with the team's workflow (Markdown for PRs, JIRA template, Confluence page, etc.).

## Inputs

- Checklist type needed (code completion, testing, release, or all)
- Recurring problems or pain points
- Technology stack
- Optionally: existing checklists to improve, codebase to analyze, team size and process tolerance

## Outputs

### Development Checklist

```markdown
# {Checklist Type} Checklist

> **Purpose:** {what this checklist prevents}
> **When to use:** {at what point in the workflow}
> **Target:** {5-10 items, independent verification}

## Items

- [ ] **{Item name}** — {why this matters}
- [ ] **{Item name}** — {why this matters}
- [ ] **{Item name}** — {why this matters}
...

## Compliance
- Spot-checked by: {role}
- Frequency: {how often spot-checks occur}

## Last Updated: {date}
## Items Removed (no longer needed): {list items graduated out}
## Items Added (new recurring issues): {list new items with date added}
```

## Key Principles

- **Small checklists get used, large ones get ignored** — WHY: The law of diminishing returns applies. Each additional checklist item reduces the probability that any item gets genuine attention. A 5-item checklist gets 90% compliance. A 50-item checklist gets 10% compliance and 90% rubber-stamping. If you need 50 items, you need 5 checklists of 10 items each, used at different stages.

- **Automate everything automatable** — WHY: Human attention is the scarcest resource. Spending it on checks that a linter, static analyzer, or CI pipeline could perform is wasteful. Reserve the checklist for judgment calls: "Does this error handling cover the failure modes that matter for this service?" A linter can't answer that.

- **Checklists are not procedures** — WHY: When procedural steps are placed on a checklist, the checklist becomes unusable because items can't be verified until prior items complete. This creates a false sense of security — the team "completed the checklist" but actually just followed a procedure. Procedures belong in runbooks; checklists belong in quality gates.

- **State the obvious because it gets skipped** — WHY: "Did you remove hardcoded credentials from the codebase?" feels too obvious to put on a checklist. But every credential leak in history started with someone who thought it was too obvious to check. The obvious items are the most commonly missed precisely BECAUSE everyone assumes someone else checked them.

- **The Hawthorne Effect is your compliance tool** — WHY: Knowing that checklists will be spot-checked changes behavior even when spot-checks rarely happen. This isn't about distrust — it's about human nature. People do better work when they know someone will look at it. Security cameras don't need to record to be effective; they just need to be visible.

- **Involve the team in checklist creation** — WHY: People follow rules they helped create and resist rules imposed on them. When developers contribute checklist items based on their own experience of what goes wrong, the checklist becomes a shared tool rather than an imposed burden.

## Examples

**Scenario: Creating a code completion checklist for common bugs**
Trigger: "Our team keeps shipping bugs that could be caught with basic checks — missing null validation, hardcoded config values, forgotten log statements."
Process: Identified the three recurring issues. Created a focused 7-item code completion checklist targeting exactly these patterns plus related items the team likely hasn't considered. Verified each item is independently checkable and not automatable (if the language has a null safety feature, that item shouldn't be on the checklist). Included "why this matters" for each item to support the Hawthorne Effect — developers who understand the reasoning comply more honestly. Recommended the tech lead perform random spot-checks on 1 PR per week.
Output: 7-item code completion checklist: (1) No hardcoded configuration values, (2) Null/empty checks on external inputs, (3) Error handling produces actionable log messages, (4) No absorbed exceptions (catch blocks that swallow errors silently), (5) New configuration keys added to all environment configs, (6) Sensitive data excluded from log output, (7) New dependencies justified in PR description.

**Scenario: Creating a release checklist after production incidents**
Trigger: "We've had 3 production incidents caused by deployment mistakes — wrong config file, missing database migration, stale cache."
Process: Each incident maps directly to a checklist item. Created a 6-item release checklist targeting the exact failure modes. Verified that the config check can't be automated (if it can, it should be a CI step, not a checklist item). For the cache item, checked whether cache invalidation can be part of the deployment script. Recommended adding the checklist as a required sign-off step in the deployment pipeline.
Output: 6-item release checklist: (1) Configuration file matches target environment, (2) Database migrations have been run and verified, (3) Cache invalidation performed or scheduled, (4) Feature flags set to correct state for this release, (5) Rollback procedure documented and tested, (6) Monitoring dashboards and alerts verified for new components.

**Scenario: Fixing an existing 50-item checklist that nobody follows**
Trigger: "I want to create a testing checklist but my team complains they already have too many processes. They ignore our existing 50-item QA checklist."
Process: The problem isn't the team — it's the 50-item checklist. Applied the design principles: first, separated procedural items (which belong in a workflow document, not a checklist) from genuine verification items. Found 20 items were procedural. Of the remaining 30, identified 12 that could be automated (linting, formatting, basic test coverage). That left 18 genuine checklist items — still too many. Grouped them into 3 focused checklists of 6 items each: code completion, testing, and release. Each checklist is used at a different stage, so no developer sees more than 6 items at a time. Recommended sunsetting the 50-item checklist and introducing the 3 focused checklists with team input on final items.
Output: Three focused checklists (6 items each) replacing the original 50-item checklist, with a migration plan and team workshop agenda for collaborative refinement.

## References

- For ready-to-use checklist templates by type, with customization instructions, see [references/checklist-templates.md](references/checklist-templates.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
