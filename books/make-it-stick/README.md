# Make It Stick: The Science of Successful Learning

10 agent skills for evidence-based learning design, study system optimization, and training program auditing, extracted from **Make It Stick: The Science of Successful Learning** by Peter C. Brown, Henry L. Roediger III, and Mark A. McDaniel.

These skills teach AI agents how to apply cognitive science research on retrieval practice, spaced repetition, interleaving, desirable difficulties, and metacognitive calibration to study planning, course design, corporate training, and self-directed learning. They also detect and replace ineffective practices — rereading, cramming, learning styles myths, and illusions of knowing — with evidence-based alternatives.

**Average quality delta: +39.1 points** (95.2% with-skill vs 55.6% baseline).

## Install

```
claude plugin add bookforge-ai/bookforge-skills/books/make-it-stick
```

## Skills

| Skill | Description | Tier | Mode | Delta |
|-------|-------------|------|------|------:|
| retrieval-practice-study-system | Design a complete self-quizzing study system with quiz generation, Leitner box spacing, and mastery signals | 1 | hybrid | +40 |
| practice-schedule-designer | Design a concrete practice schedule — diagnosing massed practice and producing day-by-day calendars with interval management | 1 | hybrid | +37 |
| learning-calibration-audit | Diagnose false confidence using 7 cognitive distortions, matched calibration instruments, and dynamic testing cycles | 1 | hybrid | +48 |
| desirable-difficulty-classifier | Classify learning activities as desirable or undesirable difficulties — auditing for 6 named strategies with redesign recommendations | 1 | hybrid | +43 |
| structured-reflection-protocol | Run a structured debrief after any learning experience using a 4-question protocol grounded in cognitive science | 1 | hybrid | +40 |
| growth-mindset-and-deliberate-practice | Diagnose fixed vs growth mindset and design deliberate practice protocols using Dweck and Ericsson frameworks | 1 | hybrid | +47 |
| mnemonic-device-selector-and-builder | Build mnemonic devices and memory palaces — covering acronyms, peg method, chunking, and method of loci | 1 | hybrid | +15 |
| evidence-based-classroom-designer | Design or redesign courses using evidence-based instructional principles — producing design audits, quiz schedules, and syllabus inserts | 2 | hybrid | +43 |
| evidence-based-training-designer | Redesign corporate training programs using Farmers Insurance, Jiffy Lube, and Andersen Windows models | 2 | hybrid | n/a |
| learning-practice-auditor | Audit study habits and training for 5 named anti-patterns with severity ratings and routing to corrective skills | 1 | hybrid | n/a |

## Dependency Graph

```
Level 0 (independent):
  retrieval-practice-study-system
  practice-schedule-designer
  learning-calibration-audit
  desirable-difficulty-classifier
  structured-reflection-protocol
  growth-mindset-and-deliberate-practice
  mnemonic-device-selector-and-builder

Level 1 (depends on Level 0):
  evidence-based-classroom-designer ──> retrieval-practice-study-system
                                    ──> practice-schedule-designer
                                    ──> desirable-difficulty-classifier
  evidence-based-training-designer  ──> practice-schedule-designer
  learning-practice-auditor         ──> retrieval-practice-study-system
                                    ──> desirable-difficulty-classifier
                                    ──> learning-calibration-audit
```

## Install Profiles

**Full** (all 10 skills) — Complete learning science toolkit including classroom design, training design, and practice auditing.

**Core** (7 skills) — All independent learning skills. Full coverage for students, educators, and self-directed learners:
- `retrieval-practice-study-system`
- `practice-schedule-designer`
- `learning-calibration-audit`
- `desirable-difficulty-classifier`
- `structured-reflection-protocol`
- `growth-mindset-and-deliberate-practice`
- `mnemonic-device-selector-and-builder`

**Minimal** (2 skills) — Entry point for effective self-study:
- `retrieval-practice-study-system`
- `learning-calibration-audit`

## Quality Metrics

| Skill | With Skill | Baseline | Delta |
|-------|----------:|--------:|------:|
| retrieval-practice-study-system | 95% | 55% | +40 |
| practice-schedule-designer | 97% | 60% | +37 |
| learning-calibration-audit | 98% | 50% | +48 |
| desirable-difficulty-classifier | 98% | 55% | +43 |
| structured-reflection-protocol | 95% | 55% | +40 |
| growth-mindset-and-deliberate-practice | 97% | 50% | +47 |
| mnemonic-device-selector-and-builder | 80% | 65% | +15 |
| evidence-based-classroom-designer | 98% | 55% | +43 |
| evidence-based-training-designer | 97% | n/a | n/a |
| learning-practice-auditor | 97% | n/a | n/a |
| **Average** | **95.2%** | **55.6%** | **+39.1** |

All 10 skills passed quality thresholds.

## Attribution

Skills extracted from **Make It Stick: The Science of Successful Learning** by Peter C. Brown, Henry L. Roediger III, and Mark A. McDaniel (2014). The skills encode the book's methodology in agent-executable format using domain-standard terminology. They do not reproduce the book's text — read the book for the full context, examples, and narrative.

## License

Skills are licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt them with attribution and under the same license terms.

Pipeline code is licensed under [MIT](https://opensource.org/licenses/MIT).

---

Part of the [BookForge](https://github.com/bookforge-ai) project.
