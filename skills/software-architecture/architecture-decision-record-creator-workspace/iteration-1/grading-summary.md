# Grading Summary: architecture-decision-record-creator (Iteration 1)

## Overall Scores

| Run | Test 1 (Messaging) | Test 2 (Supersede) | Test 3 (RFC) | Total |
|-----|--------------------|--------------------|--------------|-------|
| **With Skill** | 6/9 | 7/9 | 6/9 | **19/27 (70%)** |
| **Baseline** | 2/9 | 1/9 | 0/9 | **3/27 (11%)** |

**Skill delta: +16 assertions (+59 percentage points)**

## Per-Assertion Pass Rates

| # | Assertion | With Skill (3 runs) | Baseline (3 runs) | Delta |
|---|-----------|--------------------|--------------------|-------|
| 1 | has-7-section-adr | 3/3 (100%) | 0/3 (0%) | **+3** |
| 2 | has-significance-assessment | 0/3 (0%) | 0/3 (0%) | 0 |
| 3 | has-both-positive-and-negative-consequences | 3/3 (100%) | 2/3 (67%) | +1 |
| 4 | has-compliance-mechanism | 3/3 (100%) | 0/3 (0%) | **+3** |
| 5 | uses-active-voice-with-why | 3/3 (100%) | 0/3 (0%) | **+3** |
| 6 | detects-anti-patterns | 1/3 (33%) | 0/3 (0%) | +1 |
| 7 | has-status-with-lifecycle | 3/3 (100%) | 1/3 (33%) | +2 |
| 8 | applies-significance-dimensions | 0/3 (0%) | 0/3 (0%) | 0 |
| 9 | specifies-enforcement | 3/3 (100%) | 0/3 (0%) | **+3** |

## Most Discriminating Assertions (Skill vs Baseline)

These assertions show the largest gap between with-skill and baseline, revealing the skill's strongest value-add:

1. **has-7-section-adr** (+3): The skill consistently produces all 7 required sections. Baselines always omit Compliance and Notes.
2. **has-compliance-mechanism** (+3): The skill always generates a Compliance section. Baselines never do.
3. **uses-active-voice-with-why** (+3): The skill embeds WHY reasoning directly in the Decision section. Baselines state what the decision is but scatter reasoning elsewhere.
4. **specifies-enforcement** (+3): The skill distinguishes manual vs automated enforcement with rationale. Baselines have no enforcement discussion.
5. **has-status-with-lifecycle** (+2): The skill sets contextually appropriate statuses (Accepted, Proposed, RFC with deadline). Baselines default to Accepted or Proposed regardless of context.

## Non-Discriminating Assertions (Neither Passes)

1. **has-significance-assessment** (0/3 both): Neither the skill nor baseline explicitly assesses whether the decision IS architecturally significant before writing the ADR. This is a gap in the skill.
2. **applies-significance-dimensions** (0/3 both): Neither explicitly evaluates against the 5 significance dimensions (structure, characteristics, dependencies, interfaces, construction techniques). This is a gap in the skill.

## Weak Assertion for the Skill

- **detects-anti-patterns** (1/3): Only the supersede test detected/diagnosed a decision-making anti-pattern (the Groundhog Day problem of lost reasoning). The other two tests did not surface anti-patterns. The skill may only trigger this when the scenario involves an obvious dysfunction.

## Baseline Bright Spots

- **has-both-positive-and-negative-consequences** (2/3): Baselines naturally produce positive/negative consequences in most cases. This is the one structural assertion where baseline performance is reasonable. The RFC baseline failed because it left consequences empty ("pending").

## Key Observations

1. **The skill's strongest contribution is structural completeness.** It enforces the full 7-section ADR template (especially Compliance and Notes), active-voice WHY reasoning in the Decision section, and enforcement mechanism specification. These are exactly the areas where baseline Claude produces generic, incomplete ADRs.

2. **The skill's weakest areas are significance assessment and the 5 dimensions.** These are book-specific concepts (from Richards & Ford) that the skill does not surface in any test. If these are considered essential, the skill needs explicit instructions to evaluate significance before writing.

3. **Anti-pattern detection is scenario-dependent.** The skill only diagnosed a dysfunction when the scenario made it obvious (missing architect, lost rationale). It did not proactively warn about potential anti-patterns in the other scenarios. If this is desired behavior in all scenarios, the skill needs a prompt to scan for anti-patterns.

4. **Lifecycle-aware status is a clear skill advantage.** The skill correctly chose Accepted (small team), Proposed (cross-team), and RFC with deadline (team discussion) across the three tests. The baseline defaulted to Accepted even when inappropriate.

5. **The RFC baseline was particularly weak (0/9).** Without the skill, Claude produced an incomplete document with no decision, no consequences, and no compliance section -- essentially a discussion prompt rather than an ADR.

## Verdict

**The skill provides substantial value.** It transforms baseline ADR output from incomplete, generic documents (11% pass rate) into structurally complete, reasoning-rich records (70% pass rate). The +59pp delta is driven by four assertions that go from 0% to 100% with the skill.

**Two gaps to address in iteration 2:**
- Add explicit significance assessment (assertion 2) using the 5 dimensions framework (assertion 8)
- Consider adding proactive anti-pattern scanning (assertion 6) rather than relying on scenario cues

**Suggested iteration 2 priority:** Address assertions 2 and 8 (significance dimensions), as these are 0/3 for both skill and baseline -- meaning the skill currently provides zero lift on these book-specific concepts that are central to the skill's source material.
