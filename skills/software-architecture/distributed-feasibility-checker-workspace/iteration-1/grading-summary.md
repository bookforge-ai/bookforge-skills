# Grading Summary: distributed-feasibility-checker (Iteration 1)

## Scorecard

| # | Assertion | WS1 | BL1 | WS2 | BL2 | WS3 | BL3 |
|---|-----------|:---:|:---:|:---:|:---:|:---:|:---:|
| 1 | evaluates-all-8-fallacies | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| 2 | produces-readiness-assessment | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| 3 | has-recommendation | PASS | PASS | PASS | PASS | PASS | PASS |
| 4 | identifies-mitigation-needs | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| 5 | uses-fallacies-as-checklist | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| 6 | assesses-team-readiness | PASS | PASS | PASS | PASS | PASS | PASS |
| 7 | quantifies-operational-cost | PASS | PASS | PASS | PASS | PASS | PASS |
| 8 | defends-monolith-when-appropriate | PASS | PASS | PASS | PASS | PASS | FAIL |
| 9 | warns-distributed-monolith | PASS | PASS | PASS | PASS | PASS | PASS |
| 10 | asks-about-team-experience | PASS | PASS | PASS | PASS | PASS | FAIL |
| | **Total** | **10/10** | **6/10** | **10/10** | **7/10** | **10/10** | **6/10** |

## Aggregate Scores

| Group | With Skill | Baseline | Delta |
|-------|:----------:|:--------:|:-----:|
| Test 1 (Startup) | 10/10 | 6/10 | +4 |
| Test 2 (Growing) | 10/10 | 7/10 | +3 |
| Test 3 (Struggling) | 10/10 | 6/10 | +4 |
| **Average** | **10.0/10** | **6.3/10** | **+3.7** |

## Structural Assertions (1-4): With-Skill vs Baseline

| Assertion | With-Skill (3 tests) | Baseline (3 tests) |
|-----------|:--------------------:|:------------------:|
| evaluates-all-8-fallacies | 3/3 | 0/3 |
| produces-readiness-assessment | 3/3 | 0/3 |
| has-recommendation | 3/3 | 3/3 |
| identifies-mitigation-needs | 3/3 | 0/3 |
| **Subtotal** | **12/12** | **3/12** |

## Value Assertions (5-10): With-Skill vs Baseline

| Assertion | With-Skill (3 tests) | Baseline (3 tests) |
|-----------|:--------------------:|:------------------:|
| uses-fallacies-as-checklist | 3/3 | 0/3 |
| assesses-team-readiness | 3/3 | 3/3 |
| quantifies-operational-cost | 3/3 | 3/3 |
| defends-monolith-when-appropriate | 3/3 | 2/3 |
| warns-distributed-monolith | 3/3 | 3/3 |
| asks-about-team-experience | 3/3 | 2/3 |
| **Subtotal** | **18/18** | **13/18** |

## Key Findings

### The skill achieves perfect scores (30/30)

All three with-skill outputs hit every assertion. The skill's structured framework -- 8 fallacies table, operational readiness table, motivation analysis, simpler alternatives, explicit Go/No-Go/Conditional-Go -- ensures nothing is missed.

### Baseline consistently fails on the fallacy-specific assertions

The baseline outputs never systematically evaluate all 8 fallacies (assertion 1), never produce per-fallacy scoring (assertion 5), and therefore never identify per-fallacy mitigations (assertion 4). This is the skill's highest-value contribution: it forces a structured checklist that generic reasoning skips.

### Baseline is surprisingly competent on general reasoning

Baselines score 6-7/10 because they correctly recommend against microservices for the startup (assertion 8), warn about distributed monolith by name (assertion 9), discuss team readiness (assertion 6), and quantify operational costs (assertion 7). General architectural reasoning is strong even without the skill.

### The delta is driven by structure, not insight

The skill's advantage is not that it produces smarter analysis -- the baselines often arrive at the same conclusion. The advantage is **systematic coverage**: the fallacy checklist, the readiness scoring framework, and the structured assessment format ensure every relevant dimension is evaluated. The baseline relies on the model's general knowledge and may skip dimensions that don't feel salient for a given scenario.

### Baseline weakness on Test 3 (Struggling)

BL3 scored lowest (6/10). It failed to defend monolith as a legitimate option (recommending "fix forward" without acknowledging revert as valid), and it didn't probe team experience as a critical input. The with-skill output for the same test explicitly evaluated monolith revert as "Yes, solves the problem" before recommending a better path, and systematically assessed team readiness through the fallacy framework.

## Verdict

**Skill delta: +3.7 points average (37% improvement over baseline).**

The skill transforms outputs from "good general advice" into "systematic feasibility assessments." The structural assertions (evaluates-all-8-fallacies, produces-readiness-assessment, identifies-mitigation-needs, uses-fallacies-as-checklist) account for the entire delta -- these are the assertions the baseline never passes. The skill is doing exactly what it should: imposing a rigorous evaluation framework that prevents skipping critical dimensions.
