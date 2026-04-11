# BookForge Skills

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Books: 14](https://img.shields.io/badge/Books-14-8B4513.svg)]()
[![Skills: 167](https://img.shields.io/badge/Skills-167-2F855A.svg)]()
[![Website](https://img.shields.io/badge/site-bookforgeai.dev-1a2332.svg)](https://bookforgeai.dev)

> Every book is a skill waiting to be unlocked.

**You have 50 books on your shelf. Your agent can't read any of them.**

BookForge turns non-fiction books into agent skills — the decision frameworks, checklists, and workflows inside each book, extracted and rewritten as instructions your coding agent can actually execute. Install one, and your agent gains the playbook from a book it'll never read.

No more pasting chapters into context. No more "act as an expert in X". Just `claude plugin install bookforge-never-split-the-difference` and your agent starts negotiating like Chris Voss.

[**Browse the full catalog →**](https://bookforgeai.dev)

## See it in action

A stakeholder pings you: *"We need to add three more integrations before ship. Can you make it work?"*

**Without a skill**, your agent replies with something like:

> *"I understand you need the integrations. I can try to fit them in, but it might affect the timeline. Let me know how you'd like to proceed."*

Generic. Conflict-averse. Gives up leverage before the conversation has started.

**With `bookforge-never-split-the-difference` installed**, the agent reaches for the `calibrated-questions-planner` skill and produces:

> *This is an anchored ask — they've framed the new scope as if it's free. A direct "no" triggers defensiveness. Per the calibrated-questions framework, I'll use a "How" question to make them solve the problem, not me. Draft reply:*
> *"That's a meaningful addition. How am I supposed to fit three new integrations into the existing timeline without pulling from the scope we already committed to?"*

The agent now knows *which framework to reach for*, *why it applies*, and *how to execute it* — because a skill told it.

### Another domain, same pattern

You ask your agent to review a Go service for SQL injection risks.

**Without a skill:**

> *"Use parameterized queries and prepared statements. Avoid string concatenation in SQL. Run a linter to catch unsafe patterns. Make sure code reviewers check for this."*

Correct, but it's guideline-and-pray. The enforcement lives in developer discipline.

**With `bookforge-building-secure-and-reliable-systems` installed**, the agent reaches for `secure-code-review`:

> *Guidelines don't scale — they rely on every developer remembering every rule. The book's Chapter 12 fix is structural: a `TrustedSqlString` typed-builder pattern where the compiler makes the vulnerability impossible by construction. User input is typed as a plain `string`; the SQL builder's `AppendLiteral` method only accepts a package-private `stringLiteral` type. A plain string cannot be implicitly converted, so passing user input to `AppendLiteral` is a compile-time error — not a code-review catch. Recommend migrating the `PaymentRepo` query layer to this pattern; I've drafted the Go interface below...*

Different book, different domain, same mechanic: the skill carries *the specific engineering move* from the source text, not a summary of it.

## What's a skill?

A skill is a single `SKILL.md` file with structured, triggerable expertise — not a rewording of a chapter. Each one encodes:

- **When to use it** — triggering conditions your agent recognizes automatically
- **How to execute** — step-by-step instructions with the *why* behind each step
- **What good looks like** — acceptance criteria and failure modes
- **Supporting material** — references, templates, and scripts loaded on demand

Skills follow the [open Agent Skills convention](https://code.claude.com/docs/en/skills) and work across Claude Code, Cursor, Codex, Gemini CLI, Windsurf, OpenCode, Cline, Aider, and ClawhHub.

## Quality: tested, not trusted

Every skill in this repo is run through a value-contribution test: the same prompt, once with the skill loaded and once without, graded by an independent evaluator against a per-skill rubric. A skill ships only when the delta clears +30 points.

**Never Split the Difference — measured results (8 skills):**

| Metric | With skill | Baseline | Delta |
|---|---|---|---|
| Average pass rate | **82.9%** | 16.3% | **+66.6 points** |

Every single skill in that book cleared the delta threshold. The `calibrated-questions-planner` skill featured above: 75.0% with skill vs 33.3% baseline — **+41.7 points**. The highest-delta skill in the book (`ackerman-bargaining-planner`) scored 100% vs 15.4% — **+84.6 points**.

Every book ships with its grading summary in `.meta/test-results/grading-summary.md`. The test harness is open source and lives in the [BookForge pipeline](https://github.com/bookforge-ai/bookforge) — you can re-run it against any skill in this repo.

## Install

```bash
# Add the BookForge marketplace once
claude plugin marketplace add bookforge-ai/bookforge-skills

# Install any book as a plugin
claude plugin install bookforge-never-split-the-difference
```

Using Cursor, Codex, Gemini CLI, Windsurf, OpenCode, Cline, Aider, or ClawhHub? Every [book page on bookforgeai.dev](https://bookforgeai.dev/books) shows the exact install command for your agent. Or clone this repo and copy `books/<slug>/skills/` into your agent's skills folder — no tooling required.

## Library

14 books, 167 skills, and counting.

### Software & Systems

| Book | Authors | Skills |
|---|---|---|
| [Fundamentals of Software Architecture](books/fundamentals-of-software-architecture) | Mark Richards, Neal Ford | 19 |
| [Design Patterns](books/design-patterns-gof) | Gamma, Helm, Johnson, Vlissides | 15 |
| [Designing Data-Intensive Applications](books/designing-data-intensive-applications) | Martin Kleppmann | 14 |
| [Building Secure and Reliable Systems](books/building-secure-and-reliable-systems) | Adkins, Beyer, Blankinship, Lewandowski, Oprea, Stubblefield | 14 |
| [The Web Application Hacker's Handbook](books/web-application-hackers-handbook) | Dafydd Stuttard, Marcus Pinto | 13 |

### Product & Research

| Book | Authors | Skills |
|---|---|---|
| [INSPIRED: How to Create Tech Products Customers Love](books/inspired-how-to-create-tech-products) | Marty Cagan | 12 |
| [The Craft of Research](books/the-craft-of-research) | Booth, Colomb, Williams, Bizup, FitzGerald | 12 |
| [The Mom Test](books/the-mom-test) | Rob Fitzpatrick | 9 |

### Influence & Negotiation

| Book | Authors | Skills |
|---|---|---|
| [Influence: The Psychology of Persuasion](books/influence-psychology-of-persuasion) | Robert B. Cialdini | 10 |
| [Never Split the Difference](books/never-split-the-difference) | Chris Voss, Tahl Raz | 8 |
| [The Art of Strategy](books/the-art-of-strategy) | Avinash K. Dixit, Barry J. Nalebuff | 10 |

### Marketing & Growth

| Book | Authors | Skills |
|---|---|---|
| [The 1-Page Marketing Plan](books/the-1-page-marketing-plan) | Allan Dib | 13 |
| [$100M Offers](books/100m-offers) | Alex Hormozi | 8 |

### Learning

| Book | Authors | Skills |
|---|---|---|
| [Make It Stick](books/make-it-stick) | Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel | 10 |

## How skills are made

Skills are generated by the [BookForge pipeline](https://github.com/bookforge-ai/bookforge) — a 7-stage process that indexes a book, researches skill-worthy content, plans the skill set, builds each `SKILL.md`, tests every skill against a no-skill baseline, and packages the result. Bring your own book and run it.

## Contributing

- **New skills from an existing book** — open an issue describing the gap, then a PR
- **New books** — see [CONTRIBUTING.md](CONTRIBUTING.md) for the quality bar and proposal template
- **Improvements to existing skills** — PRs welcome; include before/after test evidence where possible

Skill sets must earn their place in the library through measurable value contribution, not page count.

## License

Skills are licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/). Attribution should credit both BookForge and the original book's authors.

These skills are original, generalized knowledge — decision frameworks and workflows — not reproductions of copyrighted book content. See [orchestration/legal/copyright-framework.md](https://github.com/bookforge-ai/bookforge) in the pipeline repo for the full framework.

---

Built with [BookForge](https://github.com/bookforge-ai/bookforge) · [bookforgeai.dev](https://bookforgeai.dev)
