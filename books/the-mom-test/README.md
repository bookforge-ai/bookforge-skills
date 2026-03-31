# Customer Discovery Skills

9 agent skills for systematic customer discovery, extracted from **The Mom Test** by Rob Fitzpatrick.

These skills teach AI coding agents how to help founders and product people prepare for customer conversations, analyze conversation data for bias, evaluate commitment signals, and run a structured discovery process. The agent handles preparation, analysis, and synthesis while the human conducts the actual conversations.

**Average quality delta: +76.3 points** (98.6% with-skill vs 22.2% baseline).

## Skills

| Skill | Description | Mode | Delta |
|-------|-------------|------|------:|
| conversation-question-designer | Write, rewrite, or audit interview questions so they extract honest behavioral data instead of false validation | hybrid | +82 |
| conversation-data-quality-analyzer | Classify every statement in conversation notes as fact, compliment, fluff, or idea — separating signal from noise | hybrid | +62 |
| question-importance-prioritizer | Prioritize which assumptions to validate first, classifying risks as product risk versus market risk | hybrid | +82 |
| conversation-format-selector | Choose the right conversation format — casual chat, scheduled meeting, or call — for a discovery interaction | plan-only | +91 |
| commitment-signal-evaluator | Evaluate whether a meeting produced real interest or polite enthusiasm using time, reputation, and money currencies | hybrid | +82 |
| conversation-sourcing-planner | Create a plan for finding and reaching people to talk to, including channel selection and outreach messages | hybrid | +65 |
| customer-segment-slicer | Iteratively narrow broad customer segments into specific, findable sub-segments with who-where pairs | hybrid | +73 |
| conversation-learning-process | Structure the before-and-after process around conversations so learning reaches the whole team | hybrid | +83 |
| customer-discovery-process | Hub skill — orchestrates the full before/during/after discovery process, referencing all specialized skills | hybrid | +67 |

## Dependency Graph

```
Level 0 (independent):
  conversation-question-designer
  question-importance-prioritizer
  conversation-format-selector
  commitment-signal-evaluator
  customer-segment-slicer
  conversation-learning-process

Level 1 (depends on Level 0):
  conversation-data-quality-analyzer ──> conversation-question-designer
  conversation-sourcing-planner ──> customer-segment-slicer

Level 2 (hub):
  customer-discovery-process ──> conversation-question-designer
                              ──> conversation-data-quality-analyzer
                              ──> commitment-signal-evaluator
                              ──> customer-segment-slicer
                              ──> conversation-learning-process
```

## Install Profiles

**Full** (all 9 skills) — Complete customer discovery toolkit. Install everything for end-to-end coverage.

**Essentials** (4 skills) — Core skills for question design, data analysis, commitment evaluation, and segmentation:
- `conversation-question-designer`
- `conversation-data-quality-analyzer`
- `commitment-signal-evaluator`
- `customer-segment-slicer`

**Minimal** (1 skill) — Hub skill only. Orchestrates the full process and references specialized skills:
- `customer-discovery-process`

## Attribution

Skills extracted from **The Mom Test: how to talk to customers and learn if your business is a good idea when everybody is lying to you** by Rob Fitzpatrick. The skills encode the book's methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, examples, and narrative.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
