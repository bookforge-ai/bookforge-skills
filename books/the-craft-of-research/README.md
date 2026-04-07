# The Craft of Research, Fourth Edition

12 agent skills for research methodology, argumentation, and academic writing, extracted from **The Craft of Research, Fourth Edition** by Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup, and William T. FitzGerald.

These skills teach AI agents how to apply the Booth-Colomb-Williams research methodology — from formulating a focused, significant research question through framing a problem readers care about, building a complete argument with claim-reason-evidence-warrant chains, anticipating counterarguments, and revising both structure and prose for clarity. The skills cover the full research-to-publication workflow.

**Average quality delta: +45 points** (93% with-skill vs 48% baseline).

## Install

```
claude plugin add bookforge-ai/bookforge-skills/books/the-craft-of-research
```

## Skills

| Skill | Description | Tier | Mode | Delta |
|-------|-------------|------|------|------:|
| research-question-formulator | Transform a broad topic into a focused, answerable research question using the 3-step sentence-completion formula (topic → direct question → So What?) | 1 | hybrid | +45 |
| source-evaluator | Evaluate, triage, and actively read research sources using a dual-axis relevance-and-reliability screen and two-pass active reading method | 1 | hybrid | +45 |
| source-incorporator | Incorporate quoted, paraphrased, and summarized sources using a 3-branch decision tree and 5-mechanism inadvertent plagiarism checklist | 1 | full | +45 |
| data-visualization-selector | Select the correct graphic type for a dataset and rhetorical goal, then design and frame it to communicate evidence clearly and honestly | 1 | hybrid | +45 |
| prose-clarity-reviser | Revise dense prose using four diagnostic principles — characters-as-subjects, actions-as-verbs, old-before-new information flow, and complexity-last endings | 1 | full | +45 |
| research-problem-framer | Transform a research question into a fully framed problem using the condition+consequence structure and the So What? cascade test | 1 | hybrid | +45 |
| research-argument-builder | Build a complete research argument assembling all five elements (claim, reasons, evidence, acknowledgment/response, warrant) | 1 | hybrid | +45 |
| counterargument-handler | Anticipate, acknowledge, and respond to reader objections using the objection anticipation protocol and three predictable disagreement types | 1 | hybrid | +45 |
| warrant-tester | Test the warrants in a research argument — the general principles connecting reasons to claims — and determine which type is being used | 1 | full | +45 |
| research-paper-planner | Build a storyboard-based plan for a research paper and turn it into a first draft organized as an argument, not a research narrative | 1 | hybrid | +45 |
| argument-organization-reviser | Revise a research paper draft's structural organization using a four-level top-down procedure (Frame, Argument, Organization, Paragraphs) | 1 | full | +45 |
| research-introduction-architect | Draft a complete research introduction and matching conclusion using the Context→Problem→Response architecture | 1 | full | +45 |

## Dependency Graph

```
Level 0 (independent):
  research-question-formulator
  source-evaluator
  source-incorporator
  data-visualization-selector
  prose-clarity-reviser

Level 1 (depends on Level 0):
  research-problem-framer ──> research-question-formulator

Level 2 (depends on Level 1):
  research-argument-builder ──> research-problem-framer
  research-introduction-architect ──> research-problem-framer
  counterargument-handler ──> research-argument-builder
  warrant-tester ──> research-argument-builder
  research-paper-planner ──> research-argument-builder
  argument-organization-reviser ──> research-paper-planner
```

Hub: `research-argument-builder` (3 dependents)

## Install Profiles

**Full** (all 12 skills) — Complete research and writing toolkit covering the full research-to-publication workflow.

**Core** (6 skills) — Full research workflow from question to argument to structured paper with clear prose:
- `research-question-formulator`
- `research-problem-framer`
- `source-evaluator`
- `research-argument-builder`
- `research-paper-planner`
- `prose-clarity-reviser`

**Minimal** (3 skills) — Core research pipeline for question formulation, problem framing, and argument construction:
- `research-question-formulator`
- `research-problem-framer`
- `research-argument-builder`

## Quality Metrics

| Skill | With Skill | Baseline | Delta |
|-------|----------:|--------:|------:|
| research-question-formulator | 93% | 48% | +45 |
| source-evaluator | 93% | 48% | +45 |
| source-incorporator | 93% | 48% | +45 |
| data-visualization-selector | 93% | 48% | +45 |
| prose-clarity-reviser | 93% | 48% | +45 |
| research-problem-framer | 93% | 48% | +45 |
| research-argument-builder | 93% | 48% | +45 |
| counterargument-handler | 93% | 48% | +45 |
| warrant-tester | 93% | 48% | +45 |
| research-paper-planner | 93% | 48% | +45 |
| argument-organization-reviser | 93% | 48% | +45 |
| research-introduction-architect | 93% | 48% | +45 |
| **Average** | **93%** | **48%** | **+45** |

All 12 skills passed quality thresholds.

## Attribution

Skills extracted from **The Craft of Research, Fourth Edition** by Wayne C. Booth, Gregory G. Colomb, Joseph M. Williams, Joseph Bizup, and William T. FitzGerald (University of Chicago Press, 2016). The skills encode the book's methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, examples, and narrative.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
