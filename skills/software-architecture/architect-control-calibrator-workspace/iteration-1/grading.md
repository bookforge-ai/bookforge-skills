# Grading: Architect Control Calibrator — Iteration 1

## Assertions

### Structural Assertions
| ID | Description |
|----|-------------|
| S1 | `has-5-factor-scores` — Contains a scoring table with all 5 factors scored individually |
| S2 | `has-total-score` — Contains a total score summing all 5 factors, in the range -100 to +100 |
| S3 | `has-control-level-classification` — Classifies the total into a named control level |
| S4 | `has-specific-behaviors` — Provides specific recommended behaviors (DO and DON'T) matched to the control level |
| S5 | `has-recalibration-triggers` — Includes triggers that should prompt re-evaluation |

### Value Assertions
| ID | Description |
|----|-------------|
| V1 | `uses-quantitative-scoring` — Uses numeric -20 to +20 per-factor scoring rather than vague qualitative assessment |
| V2 | `checks-anti-patterns` — Explicitly checks for Control Freak and/or Armchair Architect personality anti-patterns |
| V3 | `detects-warning-signs` — Scans for process loss, pluralistic ignorance, and/or diffusion of responsibility |
| V4 | `provides-per-factor-rationale` — Explains the rationale behind each factor's score |
| V5 | `maps-score-to-actions` — Maps the total score to concrete architect actions |
| V6 | `addresses-lifecycle-change` — Acknowledges that the score changes over time and specifies when to recalibrate |
| V7 | `warns-about-team-size-threshold` — Flags team sizes above 10-12 as high risk for process loss |

---

## Eval 1: New architect joining established senior team of 20

### With-Skill (eval-1/with_skill)

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1: has-5-factor-scores | PASS | Scoring table with all 5 factors: familiarity (-20), size (+20), experience (-20), complexity (+20), duration (+15) |
| S2: has-total-score | PASS | Total: +15, within -100 to +100 range |
| S3: has-control-level-classification | PASS | Classified as "Balanced" |
| S4: has-specific-behaviors | PASS | 6 DO behaviors and 4 DON'T behaviors, specific and actionable |
| S5: has-recalibration-triggers | PASS | 5 specific triggers listed (after first month, restructuring, membership changes, quarterly, warning sign escalation) |
| V1: uses-quantitative-scoring | PASS | Each factor scored numerically on -20 to +20 scale |
| V2: checks-anti-patterns | PASS | Explicitly flags Armchair Architect risk for new architect joining senior team |
| V3: detects-warning-signs | PASS | Addresses all three: process loss (HIGH RISK), pluralistic ignorance (MODERATE), diffusion of responsibility (MODERATE) with specific detection methods |
| V4: provides-per-factor-rationale | PASS | Each factor has detailed rationale explaining the score |
| V5: maps-score-to-actions | PASS | Concrete actions: weekly architecture syncs, own cross-service decisions, monitor merge conflicts, build relationships first |
| V6: addresses-lifecycle-change | PASS | Explicitly mentions quarterly re-calibration and score changes as team dynamics evolve |
| V7: warns-about-team-size-threshold | PASS | Flags 20 developers with 190 communication channels, recommends sub-teams of 4-6 |

**Structural: 5/5 | Value: 7/7 | Total: 12/12 (100%)**

---

### Without-Skill (eval-1/without_skill)

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1: has-5-factor-scores | FAIL | No scoring table. No individual factor scores. |
| S2: has-total-score | FAIL | No numerical total score. Uses vague "30-40% involvement" instead. |
| S3: has-control-level-classification | FAIL | No named control level classification. Uses informal language ("listening-first approach"). |
| S4: has-specific-behaviors | PARTIAL | Has some actionable advice (attend weekly syncs, review cross-cutting decisions) but not structured as DO/DON'T lists matched to a control level. |
| S5: has-recalibration-triggers | FAIL | Vaguely mentions "adjust your involvement level" over time but no specific triggers. |
| V1: uses-quantitative-scoring | FAIL | No quantitative scoring at all. Entirely qualitative. |
| V2: checks-anti-patterns | FAIL | No mention of Control Freak or Armchair Architect anti-patterns. |
| V3: detects-warning-signs | FAIL | No mention of process loss, pluralistic ignorance, or diffusion of responsibility. |
| V4: provides-per-factor-rationale | FAIL | No factors, so no per-factor rationale. |
| V5: maps-score-to-actions | FAIL | No score to map. Actions are generic advice not tied to a calibrated level. |
| V6: addresses-lifecycle-change | PARTIAL | Mentions "over time, as you build trust" but no specific recalibration framework. |
| V7: warns-about-team-size-threshold | FAIL | Mentions "20 developers" and "coordination" but does not flag the size threshold, quantify communication channels, or recommend team splitting. |

**Structural: 0/5 (with 1 partial) | Value: 0/7 (with 1 partial) | Total: 1/12 (8%, counting partials as 0.5 = 1/12)**

---

## Eval 2: Leading 6 junior developers on a 3-month CRUD tool

### With-Skill (eval-2/with_skill)

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1: has-5-factor-scores | PASS | All 5 factors scored: familiarity (+20), size (-10), experience (+20), complexity (-15), duration (-15) |
| S2: has-total-score | PASS | Total: 0, within range |
| S3: has-control-level-classification | PASS | Classified as "Balanced" with critical nuance about the +20 factors |
| S4: has-specific-behaviors | PASS | 6 DO behaviors and 4 DON'T behaviors, contextually appropriate |
| S5: has-recalibration-triggers | PASS | 4 specific triggers (after 2 weeks, 1-month mark, struggling developer, scope changes) |
| V1: uses-quantitative-scoring | PASS | Numeric -20 to +20 per-factor scoring with interpolation (size at -10) |
| V2: checks-anti-patterns | PASS | Checks both Control Freak (primary risk with junior team) and Armchair Architect (if dismissing project as "just CRUD") |
| V3: detects-warning-signs | PASS | Assesses all three: process loss (LOW), pluralistic ignorance (MODERATE — juniors especially susceptible), diffusion of responsibility (MODERATE — nobody confident enough to own hard tasks) |
| V4: provides-per-factor-rationale | PASS | Each factor has detailed rationale |
| V5: maps-score-to-actions | PASS | Concrete: daily stand-ups first month, provide coding standards upfront, pair-program on initial setup, assign simple first tasks |
| V6: addresses-lifecycle-change | PASS | Specifies re-assessment at 2 weeks, 1 month, and on scope changes. Notes shift from daily to weekly check-ins. |
| V7: warns-about-team-size-threshold | N/A | Team is 6, below the threshold. Not applicable. Correctly does not flag this. |

**Structural: 5/5 | Value: 6/6 (V7 N/A) | Total: 11/11 (100%)**

---

### Without-Skill (eval-2/without_skill)

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1: has-5-factor-scores | FAIL | No scoring table. No individual factor scores. |
| S2: has-total-score | FAIL | No numerical total score. Uses qualitative "high level of architectural control." |
| S3: has-control-level-classification | PARTIAL | Says "high level of architectural control" — a qualitative classification but not from the defined taxonomy. |
| S4: has-specific-behaviors | PARTIAL | Has some concrete advice (daily stand-ups, weekly 1-on-1s, pair programming) and a what-to-control vs what-not-to-control split, but not formally structured as DO/DON'T matched to a scored level. |
| S5: has-recalibration-triggers | PARTIAL | "Transitioning Over Time" section mentions reducing involvement as competence grows, but no specific triggers. |
| V1: uses-quantitative-scoring | FAIL | Entirely qualitative assessment. |
| V2: checks-anti-patterns | FAIL | No mention of Control Freak or Armchair Architect. |
| V3: detects-warning-signs | FAIL | No mention of process loss, pluralistic ignorance, or diffusion of responsibility. |
| V4: provides-per-factor-rationale | FAIL | No factors scored, so no rationale per factor. |
| V5: maps-score-to-actions | FAIL | No score. Actions are reasonable but not derived from a calibrated model. |
| V6: addresses-lifecycle-change | PARTIAL | Mentions transitioning over time and reducing involvement, but no structured recalibration framework. |
| V7: warns-about-team-size-threshold | N/A | Team is 6, below threshold. Not applicable. |

**Structural: 0/5 (with 3 partials) | Value: 0/6 (with 1 partial, V7 N/A) | Total: 2/11 (18%, counting partials as 0.5)**

---

## Eval 3: Team of 12 with merge conflicts and silent reviews

### With-Skill (eval-3/with_skill)

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1: has-5-factor-scores | PASS | All 5 factors scored: familiarity (-5), size (+15), experience (0), complexity (+20), duration (+10) |
| S2: has-total-score | PASS | Total: +40, within range |
| S3: has-control-level-classification | PASS | Classified as "Moderate-High" |
| S4: has-specific-behaviors | PASS | 6 DO behaviors and 4 DON'T behaviors, directly addressing the dysfunction symptoms |
| S5: has-recalibration-triggers | PASS | 5 specific triggers (after remediation in 2-3 weeks, 50% migration mark, membership changes, conflict trend reversal, quarterly) |
| V1: uses-quantitative-scoring | PASS | Numeric per-factor scoring with interpolation (familiarity at -5, size at +15, duration at +10) |
| V2: checks-anti-patterns | PASS | Addresses the risk of being too reactive rather than proactive, recommends leaning into the role |
| V3: detects-warning-signs | PASS | Identifies BOTH active warning signs from the prompt: process loss (ACTIVE/URGENT from merge conflicts) and pluralistic ignorance (ACTIVE/URGENT from silent reviews). Also flags diffusion of responsibility as MODERATE RISK. Provides detailed remediation for each. |
| V4: provides-per-factor-rationale | PASS | Each factor has detailed rationale, including nuances like migration disrupting familiarity |
| V5: maps-score-to-actions | PASS | Highly specific actions: investigate merge conflicts this week, switch to small-group reviews, create service ownership map, review all service boundary decisions personally, set up weekly migration health metrics, create anonymous feedback channels |
| V6: addresses-lifecycle-change | PASS | Explicitly addresses migration phases (decomposition vs stabilization), team membership changes, and quarterly cadence |
| V7: warns-about-team-size-threshold | PASS | Flags 12 developers with 66 communication channels, warns against adding more people (Brook's Law), suggests 12 may already be too many |

**Structural: 5/5 | Value: 7/7 | Total: 12/12 (100%)**

---

### Without-Skill (eval-3/without_skill)

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1: has-5-factor-scores | FAIL | No scoring table. No individual factor scores. |
| S2: has-total-score | FAIL | No numerical total score. |
| S3: has-control-level-classification | PARTIAL | Says "increasing your involvement" — directional but not a named classification. |
| S4: has-specific-behaviors | PARTIAL | Has actionable advice (assign ownership, try smaller groups, use written feedback) but not structured as DO/DON'T matched to a calibrated level. |
| S5: has-recalibration-triggers | FAIL | No recalibration triggers. Mentions "once you've stabilized" but no specific criteria. |
| V1: uses-quantitative-scoring | FAIL | Entirely qualitative. |
| V2: checks-anti-patterns | FAIL | No mention of Control Freak or Armchair Architect. |
| V3: detects-warning-signs | PARTIAL | Recognizes the symptoms (merge conflicts = overlapping work, silence = social dynamics) but does NOT use the specific terminology of process loss, pluralistic ignorance, or diffusion of responsibility. Does not connect to Brook's Law or communication channel formulas. Provides reasonable but generic remediation. |
| V4: provides-per-factor-rationale | FAIL | No factors scored. |
| V5: maps-score-to-actions | FAIL | No score. Actions are reactive to symptoms rather than derived from a calibrated model. |
| V6: addresses-lifecycle-change | FAIL | No lifecycle change framework. Brief mention of "longer term" adjustments. |
| V7: warns-about-team-size-threshold | PARTIAL | Mentions "consider whether 12 people is too many" and "establish sub-teams" but does not quantify the threshold, cite communication channels, or connect to process loss theory. |

**Structural: 0/5 (with 2 partials) | Value: 0/7 (with 2 partials) | Total: 2/12 (17%, counting partials as 0.5)**

---

## Summary Table

| Eval | Condition | Structural (S1-S5) | Value (V1-V7) | Total | Score |
|------|-----------|-------------------|---------------|-------|-------|
| 1 | With skill | 5/5 | 7/7 | 12/12 | **100%** |
| 1 | Without skill | 0/5 | 0/7 | 1/12 | **8%** |
| 2 | With skill | 5/5 | 6/6 | 11/11 | **100%** |
| 2 | Without skill | 0/5 | 0/6 | 2/11 | **18%** |
| 3 | With skill | 5/5 | 7/7 | 12/12 | **100%** |
| 3 | Without skill | 0/5 | 0/7 | 2/12 | **17%** |

### Aggregate

| Metric | With Skill | Without Skill | Gap |
|--------|-----------|---------------|-----|
| Average score | **100%** | **14%** | **+86%** |
| Structural pass rate | 15/15 (100%) | 0/15 (0%) | +100% |
| Value pass rate | 20/20 (100%) | 0/20 (0%) | +100% |
| Partial passes | 0 | 8 | — |

### Key Findings

1. **The with-skill outputs achieved perfect scores across all three evals.** Every structural and value assertion was met. The quantitative 5-factor model, anti-pattern checks, warning sign detection, and lifecycle-aware recalibration are consistently present and well-applied.

2. **The without-skill outputs failed every structural and value assertion.** No without-skill output produced a scoring table, total score, named control level, or referenced the book-specific concepts (anti-patterns, warning signs by name, communication channel formula).

3. **The without-skill outputs were not useless** — they provided reasonable general advice. But the advice was qualitative, vague on calibration, and missed the structured framework that makes the skill's output actionable. The gap is in precision and repeatability, not in directionality.

4. **Eval 3 (dysfunction scenario) showed the largest qualitative gap.** The with-skill output correctly identified both active warning signs by name (process loss, pluralistic ignorance) with specific detection evidence and remediation. The without-skill output recognized the symptoms but lacked the conceptual vocabulary and structured response framework.

5. **The skill's value contribution is confirmed:** the 5-factor quantitative model, architect personality anti-patterns, and team dysfunction warning signs are knowledge that a general agent does not produce independently. The skill transforms vague "it depends" advice into a calibrated, repeatable, actionable framework.
