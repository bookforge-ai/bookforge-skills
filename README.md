# BookForge Skills

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)
[![Books: 15](https://img.shields.io/badge/Books-15-8B4513.svg)]()
[![Skills: 178](https://img.shields.io/badge/Skills-178-2F855A.svg)]()
[![Website](https://img.shields.io/badge/site-bookforgeai.dev-1a2332.svg)](https://bookforgeai.dev)

> Every book is a skill waiting to be unlocked.

<p align="center">
  <img src="docs/images/sheldon-reading-bookforge.webp" alt="Sheldon the robot reading a BookForge book" width="100%" />
</p>

**You have 50 books on your shelf. Your agent can't read any of them. And the existing agent-skills ecosystem can't help, because skills only exist where someone bothered to hand-write one, and that someone is almost always a programmer writing programming skills.**

BookForge is a book knowledge engine for AI agents. It runs an automated pipeline that distills non-fiction books into tested agent skills: the decision frameworks, checklists, and workflows inside each book, extracted as instructions your agent can actually execute. Every book, every domain, no expert bottleneck.

Install one, and your agent gains the playbook from a book it'll never read.

No more pasting chapters into context. No more "act as an expert in X". Just `claude plugin install bookforge-never-split-the-difference` and your agent starts negotiating like Chris Voss.

[**Browse the full catalog →**](https://bookforgeai.dev)

## Contents

- [What BookForge is (and isn't)](#what-bookforge-is-and-isnt)
- [Install](#install)
- [See it in action](#see-it-in-action)
- [Quality: tested, not trusted](#quality-tested-not-trusted)
- [FAQ](#faq)
- [Library](#library)
- [How skills are made](#how-skills-are-made)
- [Contributing](#contributing)
- [License](#license)

## What BookForge is (and isn't)

BookForge is a **book knowledge engine for AI agents**. It's an automated pipeline that distills non-fiction books into tested, executable skills across every domain. The library today covers 15 books and 178 skills, with a roadmap targeting 29 domains and 60-100 books. Every skill is tested against a no-skill baseline and shipped only when it measurably changes agent behavior.

**What BookForge isn't:**

- **Not a prompt library.** Prompts are strings you paste into a chat. Skills are triggerable modules your agent reaches for automatically when the context calls for them. No copy-paste, no context-window bloat.
- **Not a RAG system.** RAG retrieves chunks of text at query time. BookForge pre-processes books into decision frameworks at build time, shipped as static files with zero runtime overhead.
- **Not fine-tuning.** Fine-tuning modifies the model's weights. BookForge runs on any base model. Swap the skill set, not the model.
- **Not a replacement for reading the book.** If the stakes are high and the book is worth your time, read the book. BookForge skills are for when you want the framework without the prose.

**BookForge is for** anyone using an agent for serious work: shipping code, writing marketing, running research, negotiating hard conversations, pricing offers, designing product strategy. If your daily workflow runs through Claude Code, Cursor, Codex, Gemini CLI, or a similar agent platform, and you've wanted your agent to have the playbook from a specific book without burning the context window, BookForge is for you.

## Install

The fastest path is the Claude Code marketplace:

```bash
# Add the BookForge marketplace once
claude plugin marketplace add bookforge-ai/bookforge-skills

# Install any book as a plugin
claude plugin install bookforge-never-split-the-difference
```

Using Cursor, Codex, Gemini CLI, Windsurf, OpenCode, Cline, Aider, or ClawhHub? Every [book page on bookforgeai.dev](https://bookforgeai.dev/books) shows the exact install command for your agent. Or clone this repo and copy `books/<slug>/skills/` into your agent's skills folder. No tooling required.

## See it in action

A stakeholder pings you: *"We need to add three more integrations before ship. Can you make it work?"*

**Without a skill**, your agent replies with something like:

> *"I understand you need the integrations. I can try to fit them in, but it might affect the timeline. Let me know how you'd like to proceed."*

Generic. Conflict-averse. Gives up leverage before the conversation has started.

**With `bookforge-never-split-the-difference` installed**, the agent reaches for the `calibrated-questions-planner` skill and produces:

> *This is an anchored ask. They've framed the new scope as if it's free. A direct "no" triggers defensiveness. Per the calibrated-questions framework, I'll use a "How" question to make them solve the problem, not me. Draft reply:*
> *"That's a meaningful addition. How am I supposed to fit three new integrations into the existing timeline without pulling from the scope we already committed to?"*

The agent now knows *which framework to reach for*, *why it applies*, and *how to execute it*. A skill told it.

### Another domain, same pattern

You ask your agent to review a Go service for SQL injection risks.

**Without a skill:**

> *"Use parameterized queries and prepared statements. Avoid string concatenation in SQL. Run a linter to catch unsafe patterns. Make sure code reviewers check for this."*

Correct, but it's guideline-and-pray. The enforcement lives in developer discipline.

**With `bookforge-building-secure-and-reliable-systems` installed**, the agent reaches for `secure-code-review`:

> *Guidelines don't scale. They rely on every developer remembering every rule. The book's Chapter 12 fix is structural: a `TrustedSqlString` typed-builder pattern where the compiler makes the vulnerability impossible by construction. User input is typed as a plain `string`; the SQL builder's `AppendLiteral` method only accepts a package-private `stringLiteral` type. A plain string cannot be implicitly converted, so passing user input to `AppendLiteral` is a compile-time error, not a code-review catch. Recommend migrating the `PaymentRepo` query layer to this pattern; I've drafted the Go interface below...*

Different book, different domain, same mechanic: the skill carries *the specific engineering move* from the source text, not a summary of it.

## Quality: tested, not trusted

Every skill in this repo is run through a value-contribution test: the same prompt, once with the skill loaded and once without, graded by an independent evaluator against a per-skill rubric. A skill ships only when the delta clears +30 points.

**Measured results for Never Split the Difference (8 skills):**

| Metric | With skill | Baseline | Delta |
|---|---|---|---|
| Average pass rate | **82.9%** | 16.3% | **+66.6 points** |

Every single skill in that book cleared the delta threshold. The `calibrated-questions-planner` skill featured above: 75.0% with skill vs 33.3% baseline (**+41.7 points**). The book's highest-delta skill, `ackerman-bargaining-planner`, scored 100% vs 15.4% (**+84.6 points**).

Every book ships with its grading summary in `.meta/test-results/grading-summary.md`. The test harness is open source and lives in the [BookForge pipeline](https://github.com/bookforge-ai/bookforge). You can re-run it against any skill in this repo.

## FAQ

### Is this legal?

BookForge's position: copyright protects expression, not ideas, procedures, or methods. Skills extract methods (decision frameworks, checklists, and workflows), not the prose around them. That's the idea/expression dichotomy (17 USC §102(b)), with fair use as a secondary backup. BookForge is non-commercial and open source, every skill has mandatory source attribution, and any author can opt out with one email (honored within 48 hours, no lawyers required). Read the full framework in [COPYRIGHT.md](COPYRIGHT.md) and the takedown path in [TAKEDOWN.md](TAKEDOWN.md).

### How is this different from RAG, fine-tuning, or prompting?

RAG retrieves text chunks at query time. Fine-tuning modifies model weights. Prompting means pasting instructions into a chat. BookForge skills are something else: **pre-processed, tested, triggerable modules** that your agent reaches for automatically when the context calls for them. They ship as static files, they run on any base model, and they don't burn context window tokens on every turn. The comparison isn't philosophical. It's mechanical. Different layer, different tradeoffs.

### How do I know skills aren't hallucinated or wrong?

Every skill is run through a value-contribution test: the same prompt, once with the skill loaded and once without, graded by an independent evaluator against a per-skill rubric. A skill only ships when the delta clears +30 points. The grading summary for every book lives at `books/<slug>/.meta/test-results/grading-summary.md` and is public. You can re-run the test yourself against the open-source [pipeline](https://github.com/bookforge-ai/bookforge). For Never Split the Difference, 8 of 8 skills passed the test with an average +66.6 delta. Skills that fail the test are either rewritten or cut entirely. There's a handful of those in the archive.

### What's BookForge's relationship with the authors?

BookForge is not affiliated with any of the authors or publishers in the library, and the [COPYRIGHT.md](COPYRIGHT.md) and [TAKEDOWN.md](TAKEDOWN.md) files make that explicit. Every skill includes mandatory attribution to the source book and its authors. Any author or rights holder can request removal with one email (honored within 48 hours), or opt into the **author-verified badge program** instead, reviewing their book's skills and receiving a verified badge on their skill set. BookForge would rather have authors as collaborators than adversaries, and the program is the bridge. The goal is that every skill points readers *back to* the book, not away from it.

### What happens when a book is wrong or outdated?

Books get updated, fields evolve, and yesterday's best practice becomes today's legacy advice. BookForge skills are versioned, improvements ship as PRs, and the grading summary for each book documents what the skills were tested against. When a book is revised (new edition, errata, retraction), the corresponding skill set is updated or retired. If you're working in a fast-moving field or the stakes are high, read the book itself. BookForge is meant to complement book reading for the 90% case, not replace it for the 10% where the details matter.

## Library

15 books, 178 skills, and counting.

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
| [Hacking Growth](books/hacking-growth) | Sean Ellis, Morgan Brown | 11 |

### Learning

| Book | Authors | Skills |
|---|---|---|
| [Make It Stick](books/make-it-stick) | Peter C. Brown, Henry L. Roediger III, Mark A. McDaniel | 10 |

## How skills are made

Skills are generated by the [BookForge pipeline](https://github.com/bookforge-ai/bookforge), a 7-stage process that indexes a book, researches skill-worthy content, plans the skill set, builds each `SKILL.md`, tests every skill against a no-skill baseline, and packages the result. Bring your own book and run it.

## Contributing

**BookForge has a novel contribution path.** Pick a book, run the pipeline, submit a PR. You're not just fixing typos. You're adding entire domains of expertise to the agent ecosystem. Each merged book is a new corner of human knowledge your agent can reach.

Three ways in:

- **Propose a new book.** See [CONTRIBUTING.md](CONTRIBUTING.md) for the book selection criteria, the scoring rubric, and the proposal template. Any domain with actionable frameworks is fair game.
- **Add a skill to an existing book.** If you spot a gap in a book we've already processed, open an issue and draft a skill. Include the source chapter reference.
- **Improve existing skills.** PRs welcome. Include before/after test evidence showing the delta against baseline.

Skill sets earn their place through measurable value contribution, not page count. Every skill is tested against a no-skill baseline before it ships.

## License

Skills are licensed under [Creative Commons Attribution-ShareAlike 4.0 International](https://creativecommons.org/licenses/by-sa/4.0/). Attribution should credit both BookForge and the original book's authors.

These skills are original, generalized knowledge (decision frameworks and workflows), not reproductions of copyrighted book content. See [COPYRIGHT.md](COPYRIGHT.md) for the full framework and [TAKEDOWN.md](TAKEDOWN.md) for the rights-holder takedown path.

---

**Status (v0.1):** 15 books, 178 skills, measurably tested. Roadmap: 29 domains and 60-100 books through 2026-Q3.

**Governance:** [Security policy](SECURITY.md) · [Code of conduct](CODE_OF_CONDUCT.md) · [Legal framework](COPYRIGHT.md) · [Takedown policy](TAKEDOWN.md)

---

Built with [BookForge](https://github.com/bookforge-ai/bookforge) · [bookforgeai.dev](https://bookforgeai.dev)
