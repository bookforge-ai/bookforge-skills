# SPIN Selling Skills

11 agent skills for B2B sales execution, extracted from **SPIN Selling** by Neil Rackham.

These skills encode the empirically-validated SPIN methodology — derived from Huthwaite's analysis of 35,000+ sales calls across 23 countries. They teach AI agents how to plan SPIN question sequences, classify customer need statements, audit FAB presentations, plan commitment progressions, and coach skill development. The agent handles preparation, classification, and planning while the human conducts the actual sales calls.

**Average quality delta: +28 points** (96% with-skill vs 68% baseline).

> Note: SPIN Selling terminology has become industry-standard B2B vocabulary since 1988. The delta reflects the skills' value-add of enforcing strict methodological adherence, refusal logic, and empirical grounding — not introducing unfamiliar concepts.

## Install

### Claude Code (recommended)

```bash
# Add to your Claude Code project
claude mcp add bookforge-skills https://github.com/bookforge-ai/bookforge-skills
```

Or install from the [BookForge marketplace](https://github.com/bookforge-ai/bookforge-skills):

```bash
# Clone and link
git clone https://github.com/bookforge-ai/bookforge-skills.git
# Then reference skills/spin-selling/ in your Claude Code settings
```

### Other platforms

- **Cursor:** See `.cursor-plugin/plugin.json`
- **Codex:** See `.codex/INSTALL.md`
- **Gemini CLI:** See `gemini-extension.json` and `GEMINI.md`
- **Aider:** See `.aider/INSTALL.md`
- **OpenCode:** See `.opencode/plugins/spin-selling.js`

## Skills

### Level 0 — Foundation Classifiers and Planners (independent)

| Skill | Description | Mode | Delta |
|-------|-------------|------|------:|
| need-type-classifier | Classify customer statements as Implied Needs or Explicit Needs and recommend the next questioning move | hybrid | +20 |
| call-outcome-classifier | Classify a call outcome as Order, Advance, Continuation, or No-sale — with detection of Continuations misread as success | hybrid | +30 |
| closing-attitude-self-assessment | Administer Rackham's 15-item closing-attitude assessment with context-aware interpretation for sale type | hybrid | +45 |
| discovery-call-opening-planner | Draft a 60–90 second non-product opening script that earns the right to ask questions without triggering early resistance | plan-only | +25 |

### Level 1 — Core SPIN Skills (depend on Level 0)

| Skill | Description | Mode | Delta |
|-------|-------------|------|------:|
| spin-discovery-question-planner | Build a pre-call question bank mapping likely customer problems to SPIN question sequences (S→P→I→N) | plan-only | +43 |
| fab-statement-classifier | Audit pitch decks, emails, or transcripts for Feature/Advantage/Benefit distribution and flag Advantages mislabeled as Benefits | hybrid | +10 |
| commitment-and-advance-planner | Define a primary and fallback Advance for the next call and script the Four Successful Actions without closing pressure | plan-only | +28 |

### Level 2 — Advanced Skills (depend on Level 1)

| Skill | Description | Mode | Delta |
|-------|-------------|------|------:|
| benefit-statement-drafter | Draft Benefit statements that link product capabilities to specific Explicit Needs, with coverage gap analysis | hybrid | +48 |
| objection-source-diagnoser | Trace objections to their FAB-behavior root cause and produce a prevention plan for the next call | hybrid | +20 |
| sales-call-plan-do-review-coach | Orchestrate pre-call planning and post-call review using Rackham's seven review questions in a closed learning loop | plan-only | +25 |
| spin-skill-practice-coach | Build a personalized multi-week SPIN practice plan applying the Four Golden Rules and 4-step learning sequence | plan-only | +15 |

## Dependency Graph

```
Level 0 (independent):
  need-type-classifier
  call-outcome-classifier
  closing-attitude-self-assessment
  discovery-call-opening-planner

Level 1 (depends on Level 0):
  spin-discovery-question-planner ──> need-type-classifier
  fab-statement-classifier ──> need-type-classifier
  commitment-and-advance-planner ──> call-outcome-classifier

Level 2 (depends on Level 1):
  benefit-statement-drafter ──> fab-statement-classifier
                            ──> spin-discovery-question-planner
  objection-source-diagnoser ──> fab-statement-classifier
  sales-call-plan-do-review-coach ──> spin-discovery-question-planner
                                  ──> call-outcome-classifier
  spin-skill-practice-coach ──> spin-discovery-question-planner
```

Hub skill: `spin-discovery-question-planner` (depended on by 3 Level 2 skills)

## Install Profiles

**Minimal** (4 skills) — Foundation diagnostics you can use today, independent of each other:
- `need-type-classifier`
- `call-outcome-classifier`
- `closing-attitude-self-assessment`
- `discovery-call-opening-planner`

**Core** (7 skills) — Minimal + SPIN question planning, FAB auditing, and commitment-advance planning:
- All minimal skills
- `spin-discovery-question-planner`
- `fab-statement-classifier`
- `commitment-and-advance-planner`

**Full** (all 11 skills) — Complete SPIN Selling methodology toolkit, including benefit drafting, objection prevention, call review, and practice coaching.

## Quality Summary

| Metric | Score |
|--------|------:|
| Avg with-skill score | 96 / 100 |
| Avg baseline score | 68 / 100 |
| Avg delta | +28 |
| Skills passing | 11 / 11 |

## Attribution

Skills extracted from **SPIN Selling: The Best Validated Sales Method Available Today** by Neil Rackham (1988, ISBN 978-0070511132). The skills encode the book's empirically-validated methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full research, case studies, and examples.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
