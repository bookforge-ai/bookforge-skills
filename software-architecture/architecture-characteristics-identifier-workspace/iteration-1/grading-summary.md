# Grading Summary: architecture-characteristics-identifier (Iteration 1)

## Overall Scores

| Run | Passed | Failed | Score |
|-----|--------|--------|-------|
| Sandwich Shop — with skill | 10 | 1 | **91%** |
| Sandwich Shop — baseline | 1 | 10 | **9%** |
| Fintech Settlement — with skill | 10 | 1 | **91%** |
| Fintech Settlement — baseline | 1 | 10 | **9%** |
| Hospital Scheduling — with skill | 11 | 0 | **100%** |
| Hospital Scheduling — baseline | 1 | 10 | **9%** |

| Aggregate | With Skill | Baseline |
|-----------|-----------|----------|
| Total passed | **31/33** | **3/33** |
| Average score | **93.9%** | **9.1%** |

---

## Per-Assertion Pass Rates

| # | Assertion | With Skill (3 runs) | Baseline (3 runs) | Delta |
|---|-----------|:---:|:---:|:---:|
| 1 | has-categorized-characteristics | **3/3** | 0/3 | +3 |
| 2 | has-prioritized-top-3 | **3/3** | 0/3 | +3 |
| 3 | has-characteristic-table | **3/3** | **3/3** | 0 |
| 4 | has-explicit-and-implicit | **3/3** | 0/3 | +3 |
| 5 | has-validation | **3/3** | 0/3 | +3 |
| 6 | applies-three-criteria-test | **3/3** | 0/3 | +3 |
| 7 | maps-domain-concerns | **3/3** | 0/3 | +3 |
| 8 | hunts-implicit-characteristics | **3/3** | 0/3 | +3 |
| 9 | enforces-top-3-limit | **3/3** | 0/3 | +3 |
| 10 | warns-characteristic-overload | **1/3** | 0/3 | +1 |
| 11 | uses-domain-mapping-table | **3/3** | 0/3 | +3 |

---

## Discriminating vs Non-Discriminating Assertions

### Perfectly Discriminating (with-skill: 3/3, baseline: 0/3) — 9 assertions

These assertions passed in ALL with-skill runs and NONE of the baseline runs. They represent the core book-specific knowledge the skill transfers:

1. **has-categorized-characteristics** — The book's operational/structural/cross-cutting taxonomy. Baseline outputs use flat priority lists.
2. **has-prioritized-top-3** — The book's "pick exactly 3 driving characteristics" discipline. Baselines list 6-10 without enforcing a limit.
3. **has-explicit-and-implicit** — The book's distinction between stated requirements and domain-inferred needs. Baselines treat all characteristics as a single undifferentiated list.
4. **has-validation** — The book's three-criteria gate (nondomain, influences structure, critical). Baselines never validate before inclusion.
5. **applies-three-criteria-test** — Evidence of actually applying the gate to demote/exclude characteristics. Baselines never exclude anything through structured reasoning.
6. **maps-domain-concerns** — The book's structured translation from business language to technical characteristics. Baselines skip this step entirely.
7. **hunts-implicit-characteristics** — The book's emphasis on proactively finding unstated characteristics. Baselines never label anything as implicit.
8. **enforces-top-3-limit** — The book's "less is more" principle for driving characteristics. Baselines list everything without pushback.
9. **uses-domain-mapping-table** — A structured table mapping domain concerns to characteristics. Baselines go directly from context to characteristics ad-hoc.

### Non-Discriminating — 1 assertion

10. **has-characteristic-table** — Passed in ALL 6 runs (3/3 with-skill, 3/3 baseline). Both LLM outputs naturally produce tables. This assertion does not measure book-specific knowledge.

### Partially Discriminating — 1 assertion

11. **warns-characteristic-overload** — Passed in 1/3 with-skill runs (Hospital Scheduling only, which explicitly referenced the Vasa warship) and 0/3 baseline runs. The skill does not consistently trigger this warning. The Hospital Scheduling scenario may have elicited it because the IT Director's "enterprise-grade and scalable" demand creates a natural opening for the overload warning, while the other scenarios did not present the same tension.

---

## Analysis

### What the skill transfers successfully

The skill reliably transfers the **complete analytical process** from "Fundamentals of Software Architecture" (Richards & Ford), Chapter 5:

1. **Domain concern mapping** — Translating vague business language into a structured table of technical characteristics (the "translation step" the book emphasizes)
2. **Explicit/implicit distinction** — Actively hunting for characteristics that nobody asked for but the domain demands
3. **Three-criteria validation gate** — Testing each candidate against nondomain / influences structure / critical to success before including it
4. **Top-3 discipline** — Forcing prioritization to exactly 3 driving characteristics with explicit justification for what's excluded
5. **Operational/structural/cross-cutting categorization** — Organizing characteristics using the book's taxonomy

### What the baseline produces without the skill

All three baselines follow the same pattern:
- Flat prioritized list of 6-10 characteristics
- No structured process (domain mapping, validation, categorization)
- No distinction between explicit and implicit
- No limit enforcement — everything that seems relevant gets listed
- Reasonable domain knowledge but presented as ad-hoc analysis rather than a systematic process

The baselines demonstrate that Claude has general architecture knowledge but lacks the **specific analytical framework** from the book. The skill's value is not in identifying individual characteristics (the baselines find similar ones) but in providing a **rigorous, structured process** that prevents common mistakes: over-specifying, failing to hunt implicit characteristics, and not validating before inclusion.

### Weakness in the skill

The Vasa/overload warning (assertion 10) only appeared in 1 of 3 with-skill runs. This suggests the skill does not consistently surface this metaphor. Consider strengthening the skill's language around characteristic overload to make this warning more prominent, or adding it as a required step in the process.

---

## Final Verdict

**Yes, the skill demonstrably transfers book-specific knowledge.**

The evidence is overwhelming: a **84.8 percentage-point gap** (93.9% vs 9.1%) between with-skill and baseline runs, with 9 of 11 assertions perfectly discriminating. The skill transforms Claude's output from generic architecture advice into a structured, book-faithful analytical process. The one non-discriminating assertion (has-characteristic-table) is a formatting expectation that any LLM meets naturally. The one partial assertion (warns-characteristic-overload) is a minor gap that can be addressed in iteration 2.
