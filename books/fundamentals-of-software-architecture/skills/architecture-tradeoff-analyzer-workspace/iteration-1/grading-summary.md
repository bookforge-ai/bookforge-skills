# Grading Summary: Architecture Trade-off Analyzer Skill (Iteration 1)

## Per-Test Pass Rates

| Test | With Skill | Baseline | Delta |
|------|-----------|----------|-------|
| Monolith vs Microservices | 8/8 (100%) | 7/8 (87.5%) | +1 |
| Kafka vs RabbitMQ | 8/8 (100%) | 7/8 (87.5%) | +1 |
| Healthcare SaaS | 8/8 (100%) | 7/8 (87.5%) | +1 |

## Overall Pass Rates

| Condition | Passed | Total | Rate |
|-----------|--------|-------|------|
| **With Skill** | 24 | 24 | **100%** |
| **Baseline** | 21 | 24 | **87.5%** |
| **Delta** | +3 | -- | **+12.5%** |

## Per-Assertion Breakdown

| Assertion | With Skill (3 runs) | Baseline (3 runs) | Delta |
|-----------|---------------------|-------------------|-------|
| has-trade-off-matrix | 3/3 | 3/3 | 0 |
| has-multiple-options | 3/3 | 3/3 | 0 |
| has-quality-attributes | 3/3 | 3/3 | 0 |
| has-recommendation | 3/3 | 3/3 | 0 |
| has-negatives-for-recommended | 3/3 | 3/3 | 0 |
| **uses-least-worst-framing** | **3/3** | **0/3** | **+3** |
| context-dependent | 3/3 | 3/3 | 0 |
| hunts-negatives | 3/3 | 3/3 | 0 |

## Key Findings

### Assertion the skill helps most with (biggest delta)

**`uses-least-worst-framing`** -- This is the only assertion where with-skill and baseline diverge, and the delta is maximum (3/3 vs 0/3). All three with-skill outputs explicitly use the phrase "the least worst choice for this context" in their recommendation. All three baseline outputs frame their recommendation positively ("Go with...", "the recommendation is...", "the safest path...") without any "least worst" or equivalent trade-off-acknowledging framing. This is a clear, consistent signal that the skill directly causes this behavior.

### Non-discriminating assertions (both pass equally)

The following 7 assertions passed in all 6 runs (with-skill and baseline alike):

- **has-trade-off-matrix** -- Both conditions produced formatted comparison tables. The with-skill outputs consistently used +/- notation in cells, while baselines used more descriptive text, but both qualify as trade-off matrices.
- **has-multiple-options** -- With-skill outputs consistently analyzed 3 options (often introducing a third option not in the original prompt), while baselines analyzed 2-3 options.
- **has-quality-attributes** -- Both explicitly named quality attributes.
- **has-recommendation** -- Both provided clear recommendations with justification.
- **has-negatives-for-recommended** -- Both acknowledged downsides of the recommended option.
- **context-dependent** -- Both referenced the user's specific constraints.
- **hunts-negatives** -- Both listed 2+ disadvantages per option.

### Qualitative differences not captured by pass/fail

While 7 of 8 assertions are non-discriminating on a pass/fail basis, there are qualitative differences worth noting:

1. **Structural consistency**: With-skill outputs follow a highly consistent structure across all 3 tests (Decision statement, Options Considered, Driving Quality Attributes, Advantages, Disadvantages, Trade-off Matrix, Synergies and Conflicts, Recommendation, Risks, ADR). Baseline outputs vary significantly in structure from test to test.

2. **Third option introduction**: All 3 with-skill outputs analyzed 3 options, often surfacing a middle-ground option not explicitly in the prompt (Strangler Fig, Kinesis, Service-Based Architecture). Baselines analyzed 2 options in 2 out of 3 tests (the healthcare baseline did include 3).

3. **Synergies and Conflicts section**: All with-skill outputs include an explicit "Synergies and Conflicts" section analyzing how quality attributes interact. No baseline output has an equivalent section.

4. **Architecture Decision Record**: All with-skill outputs end with a formal ADR (Status, Context, Decision, Consequences). Only the healthcare baseline lacks a formal ADR; the other baselines also lack one.

5. **Risk tables**: With-skill outputs include structured risk tables with Likelihood, Impact, and Mitigation columns. Baselines address risks but less systematically.

6. **Negative hunting depth**: With-skill outputs average ~5 disadvantages per option. Baselines average ~4. Both pass the threshold but with-skill is more thorough.

## Assessment: Does the Skill Demonstrably Improve Over Baseline?

**Yes, but the improvement is narrow on the current assertion set.**

On a strict pass/fail basis, the skill improves only 1 assertion out of 8: `uses-least-worst-framing`. This is a 100% vs 0% split -- the most decisive possible signal. The skill reliably produces the "least worst" framing that is central to the Richards/Ford trade-off philosophy, while baseline Claude never does.

However, the current assertion set undersells the skill's impact. The 7 non-discriminating assertions all pass for baseline Claude, which means baseline Claude is already quite good at architecture trade-off analysis. The assertions are not sensitive enough to capture the qualitative improvements the skill produces:

- Consistent report structure (an assertion like `follows-standard-template` would discriminate)
- Synergies and conflicts analysis (an assertion like `has-synergy-conflict-analysis` would discriminate)
- Formal ADR inclusion (an assertion like `has-adr` would discriminate)
- Third option generation (an assertion like `introduces-non-obvious-option` might discriminate)
- Structured risk tables (an assertion like `has-risk-mitigation-table` would discriminate)

**Recommendation for iteration 2**: Add 3-5 more assertions that target the qualitative differences observed. The current set proves the skill works for its core philosophical contribution (least-worst framing) but does not measure the structural and analytical depth improvements that are clearly visible in the outputs.
