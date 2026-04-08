---
name: architecture-decision-record-creator
description: Create structured Architecture Decision Records (ADRs) with 7 sections to document architecture decisions with full justification. Use this skill whenever the user has made or needs to make an architecture decision, wants to document why a technical choice was made, is choosing between technologies or patterns, needs to create an ADR, or is experiencing repeated debates about past decisions — even if they don't explicitly mention "ADR" or "architecture decision record."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architecture-decision-record-creator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - architecture-tradeoff-analyzer
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [19]
tags: [software-architecture, architecture, decisions, documentation, adr, governance]
execution:
  tier: 1
  mode: full
  inputs:
    - type: none
      description: "An architecture decision that needs to be documented — the choice, the context, and the alternatives"
  tools-required: [Write]
  tools-optional: [Read, Grep, Glob]
  mcps-required: []
  environment: "Any agent environment. If a codebase exists, can check for existing ADRs and suggest numbering."
---

# Architecture Decision Record Creator

## When to Use

An architecture decision has been made (or needs to be made) and it should be documented. Typical situations:

- A technology or pattern choice has been decided — needs formal documentation
- A decision keeps getting revisited ("didn't we already decide this?") — the Groundhog Day anti-pattern
- A stakeholder asks "why did we choose X?" and nobody can answer — missing documentation
- Before implementing a significant technical change — document BEFORE building
- An existing decision needs to be superseded by a new one

Before starting, verify:
- Is there actually a DECISION to document? (If it's still an open question, use `architecture-tradeoff-analyzer` first to analyze trade-offs, then come back here to document the result)
- Is this decision architecturally significant? (Step 1 below helps determine this)

## Context

### Required Context (must have before proceeding)

- **The decision:** What was decided (or what needs to be decided). Ask the user if not stated.
- **The alternatives:** What options were considered. If only one option was considered, that's a red flag — push back and identify at least one alternative.

### Observable Context (gather from environment if available)

- **Existing ADRs:** Check for prior decisions in the project
  → Look for: `docs/adr/`, `docs/decisions/`, `architecture/`, `*.adr.md`, files matching `ADR-*.md` or `*-adr.md`
  → If found: determine the next sequential number, check for related/conflicting prior decisions
  → If none: this will be ADR 1, suggest establishing an ADR directory
- **Codebase context:** What technologies, patterns, and structures currently exist
  → Look for: package.json, pyproject.toml, docker-compose, CI configs
  → This informs the Context section of the ADR

### Default Assumptions

- If no existing ADR numbering → start at ADR 1
- If no approval process exists → default to "Accepted" status (solo dev or small team)
- If compliance mechanism is unclear → suggest manual review as the starting point

## Process

### Step 1: Assess Architectural Significance

**ACTION:** Determine if this decision is architecturally significant by evaluating against 5 dimensions.

**WHY:** Not every technical decision needs an ADR. Over-documenting trivial choices creates noise and dilutes the value of ADRs. A decision is architecturally significant if it affects at least one of these dimensions — and it's the significance that justifies the effort of formal documentation.

Evaluate the decision against:

| Dimension | Question |
|-----------|---------|
| **Structure** | Does this affect the patterns or styles of architecture? |
| **Nonfunctional characteristics** | Does this impact a quality attribute that matters to the system? |
| **Dependencies** | Does this create or change coupling between components/services? |
| **Interfaces** | Does this affect how services or components are accessed? |
| **Construction techniques** | Does this impact platforms, frameworks, tools, or processes? |

**IF** the decision affects at least one dimension → it's architecturally significant, proceed to write the ADR.
**IF** it affects none → it's a technical implementation detail, not an architecture decision. Document it in code comments or a tech spec instead.

**IMPORTANT: Show your work.** Include the significance assessment as a visible section in your output BEFORE the ADR itself. This is not just an internal check — it demonstrates rigor and helps stakeholders understand why this decision warrants formal documentation.

Output the assessment as:

```
## Significance Assessment
| Dimension | Affected? | How |
|-----------|:---------:|-----|
| Structure | Yes/No | {explanation} |
| Nonfunctional characteristics | Yes/No | {explanation} |
| Dependencies | Yes/No | {explanation} |
| Interfaces | Yes/No | {explanation} |
| Construction techniques | Yes/No | {explanation} |

**Verdict:** Architecturally significant — affects {N} of 5 dimensions.
```

**CAUTION:** Don't assume technology decisions aren't architectural. If choosing Kafka over RabbitMQ directly supports a performance or scalability characteristic, it IS an architecture decision — the technology choice supports the architecture.

### Step 2: Determine Status

**ACTION:** Set the appropriate ADR status based on the decision's approval context.

**WHY:** Status isn't just metadata — it communicates where the decision is in its lifecycle and what action is needed. Setting the wrong status (e.g., "Accepted" when approval is needed) can lead to unauthorized implementations. Setting "Proposed" when the architect can self-approve adds unnecessary bureaucracy.

| Status | When to use |
|--------|------------|
| **Proposed** | Decision needs approval from a governance body or senior architect |
| **Accepted** | Decision is approved and ready for implementation |
| **Superseded by ADR N** | Decision has been replaced (link to the new ADR) |
| **RFC (with deadline)** | Architect wants broader input before deciding. MUST include a deadline date — otherwise it becomes an open-ended discussion that never concludes (Analysis Paralysis). |

Escalation triggers — the decision should be **Proposed** (not self-approved) when:
- **Cost** exceeds the team's authority (significant purchases, licensing)
- **Cross-team impact** — it affects other teams or systems
- **Security implications** — any security-relevant change needs governance review

### Step 3: Write the Context Section

**ACTION:** Describe the forces at play — what situation is forcing this decision? Include the alternatives considered.

**WHY:** Context serves double duty: it explains WHY the decision is needed AND documents the architecture. A future developer reading this ADR learns both the decision and the architectural context it applies to. Keep it concise — if alternatives need detailed analysis, add a separate Alternatives section or reference a trade-off analysis.

Format: A clear, concise statement of the situation + the alternatives.

Good: *"The order service must pass information to the payment service. This could be done using REST (synchronous) or asynchronous messaging via Kafka."*

Bad: *"We need to figure out how services should communicate."* (Too vague — which services? What are the options?)

**Before writing context, diagnose the situation for anti-patterns.** Check if the scenario shows signs of:
- **Covering Your Assets** — Has this decision been deferred repeatedly? Is the architect afraid to commit?
- **Groundhog Day** — Is this a decision that was already made but nobody recorded WHY, so it's being revisited?
- **Email-Driven Architecture** — Was a prior decision made but lost in email/Slack, so it's being re-made?

If an anti-pattern is present, NAME IT explicitly in the Context section and note how this ADR addresses it. For example: *"This decision is being re-made because the original rationale (ADR-12) did not document WHY the monolith was chosen — a classic Groundhog Day anti-pattern. This ADR includes full justification to prevent recurrence."*

### Step 4: Write the Decision Section

**ACTION:** State the decision in active, commanding voice with full justification emphasizing WHY.

**WHY:** "Why is more important than how" (Second Law of Software Architecture). Anyone can look at the system and figure out HOW it works. What they can't figure out is WHY it was built that way. Without WHY, future developers may undo good decisions — like the architect who replaced gRPC with messaging for "better decoupling," not knowing the original gRPC choice was specifically to reduce latency, causing timeouts throughout the system.

- Use **affirmative, commanding voice**: "We will use..." not "I think we should..."
- Lead with the decision, then justify
- Include BOTH technical AND business justification
- Apply the **business value litmus test**: if the decision provides no business value (cost savings, time to market, user satisfaction, or strategic positioning), reconsider whether it should be made at all

### Step 5: Write the Consequences Section

**ACTION:** Document BOTH positive and negative impacts of the decision.

**WHY:** Every architecture decision has trade-offs — this is the First Law. Documenting only positives is dishonest and sets up future surprises. Documenting negatives explicitly forces the architect to think about whether the impacts outweigh the benefits. It also prevents the Groundhog Day anti-pattern — when someone questions the decision later, the consequences are already documented with the reasoning.

For each consequence, indicate whether it's positive or negative:
- **Positive:** What improves because of this decision?
- **Negative:** What gets worse or becomes more complex? What new risks are introduced?
- **Trade-off:** What are we accepting in exchange for the benefits?

### Step 6: Write the Compliance Section

**ACTION:** Specify HOW the decision will be measured and governed.

**WHY:** A decision without enforcement is a suggestion. Many architecture decisions erode over time because nobody checks whether they're being followed. The Compliance section forces the architect to think about governance at decision time, not as an afterthought. This is the difference between "we decided to use layered architecture" and "we decided to use layered architecture, AND here's the ArchUnit test that enforces it."

Two types of compliance:

| Type | When to use | Example |
|------|------------|---------|
| **Manual** | Decision is hard to check automatically, involves judgment | "Review service boundaries during quarterly architecture review" |
| **Automated fitness function** | Decision can be verified programmatically | "ArchUnit test ensures shared services reside in the services layer" |

For automated compliance, specify:
- How the fitness function would be written
- Where the test lives
- How and when it's executed (CI pipeline, pre-commit, scheduled)

### Step 7: Write the Notes Section

**ACTION:** Add metadata: original author, approval date, last modified, approvers, supersession history.

**WHY:** Notes provide the audit trail. When a decision is questioned months later, the Notes section shows who made it, who approved it, and what changed. This is especially important in regulated environments where decision provenance matters.

## Inputs

- The decision to document (from user or from a completed trade-off analysis)
- Context: what alternatives were considered, what constraints apply
- Optionally: existing ADR directory for numbering and cross-referencing

## Outputs

### Architecture Decision Record

```markdown
## Significance Assessment
| Dimension | Affected? | How |
|-----------|:---------:|-----|
| Structure | Yes/No | {explanation} |
| Nonfunctional characteristics | Yes/No | {explanation} |
| Dependencies | Yes/No | {explanation} |
| Interfaces | Yes/No | {explanation} |
| Construction techniques | Yes/No | {explanation} |

**Verdict:** Architecturally significant — affects {N} of 5 dimensions.

---

# ADR {N}: {Short Descriptive Title}

## Status
{Proposed | Accepted | Superseded by ADR N | RFC, Deadline YYYY-MM-DD}

## Context
{Clear, concise description of the situation and forces at play.
What alternatives were considered?}

## Decision
{Active voice. Affirmative. Full justification emphasizing WHY.
Both technical and business justification.}

## Consequences

### Positive
- {What improves}

### Negative
- {What gets worse or becomes more complex}

### Trade-offs
- {What we're accepting in exchange}

## Compliance
{How this decision will be enforced}
- **Type:** Manual review | Automated fitness function
- **Mechanism:** {Specific enforcement mechanism}
- **Frequency:** {When/how often compliance is checked}

## Notes
- **Author:** {name}
- **Date:** {YYYY-MM-DD}
- **Approved by:** {name(s), if applicable}
- **Last modified:** {YYYY-MM-DD}
- **Supersedes:** {ADR N, if applicable}
- **Superseded by:** {ADR N, if applicable}
```

## Key Principles

- **WHY over HOW** — The Decision section's most powerful aspect is the justification. Anyone can see how a system works; only the ADR explains why it was built that way. Without WHY, good decisions get undone by well-meaning but uninformed future developers.

- **Decisions without enforcement are suggestions** — The Compliance section is what separates an ADR from a wish. If you can automate compliance (fitness functions, ArchUnit tests), do it. If not, schedule manual reviews. But never leave enforcement unspecified.

- **Both positive AND negative consequences** — Every decision has trade-offs. Documenting only positives is dishonest. The negative consequences, acknowledged upfront, prevent surprise later and provide ammunition when someone asks "did you consider X?"

- **Name the anti-pattern when you see it** — If a team avoids deciding (Covering Your Assets), revisits decisions repeatedly (Groundhog Day), or loses decisions in email (Email-Driven Architecture), name the dysfunction. These three anti-patterns form a progressive chain — overcoming one often reveals the next.

- **Last responsible moment, not last possible moment** — Decide when you have enough information to justify the choice, but before development teams are blocked. Too early = premature commitment. Too late = analysis paralysis. The sweet spot is "last responsible moment."

- **Business value litmus test** — If a decision provides no business value (cost, time to market, user satisfaction, strategic positioning), reconsider making it. Architecture decisions exist to serve business outcomes, not architectural purity.

## Examples

**Scenario: Documenting a messaging decision for an auction system**
Trigger: "We decided to use asynchronous messaging between the order and payment services. Can you write an ADR for this?"
Process: Assessed significance — affects structure (async vs sync), dependencies (service coupling), and nonfunctional characteristics (performance, reliability). Set status: Accepted (small team, self-approved). Context: order → payment communication, REST vs async messaging. Decision: "We will use asynchronous messaging via RabbitMQ" with WHY: reduces latency from 3,100ms to 25ms for review posting, decouples services. Consequences: positive (responsiveness, decoupling), negative (complex error handling for bad content). Compliance: automated test verifying no direct REST calls between these services.
Output: Complete ADR with all 7 sections, filed as ADR-42.

**Scenario: Superseding a previous technology decision**
Trigger: "We originally chose gRPC for service communication but now want to switch to messaging. There's an existing ADR for the gRPC decision."
Process: Assessed significance — affects structure and dependencies. Created new ADR with status "Accepted, supersedes ADR 23." Documented WHY the original decision (latency reduction) is no longer the priority and why decoupling now matters more. Explicitly noted the consequence: latency will increase, and upstream timeouts must be reconfigured. Updated ADR 23 status to "Superseded by ADR 45."
Output: New ADR-45 + updated status on ADR-23, creating a traceable decision history.

**Scenario: Decision that needs broader input**
Trigger: "I think we should adopt event sourcing for our audit trail, but I want the team's input before committing."
Process: Assessed significance — affects structure (event store pattern), construction techniques (new tooling). Set status: RFC, Deadline 2026-04-15. Wrote Context explaining the audit requirements and alternatives (event sourcing vs append-only table vs CDC). Decision section presents the architect's recommendation with justification, inviting comments. Noted in Compliance: "if adopted, automated test verifying all state changes emit events."
Output: ADR in RFC status with deadline, ready for team review. After deadline, architect incorporates feedback and moves to Accepted.

## References

- For the ADR file template, see [assets/adr-template.md](assets/adr-template.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-architecture-tradeoff-analyzer`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
