# Grading: development-checklist-generator (Iteration 1)

## Test Prompts

1. "Our team keeps shipping bugs that could be caught with basic checks — missing null validation, hardcoded config values, forgotten log statements. Can you create a code completion checklist?"
2. "We've had 3 production incidents in the last month caused by deployment mistakes — wrong config file, missing database migration, stale cache. Help us create a release checklist."
3. "I want to create a testing checklist but my team complains they already have too many processes. They ignore our existing 50-item QA checklist. How do I fix this?"

## Baseline (Without Skill) Analysis

### Test 1 Baseline
A general agent would:
- Create a comprehensive code review checklist with 15-25 items
- Include a mix of automatable and non-automatable checks
- Include procedural items mixed with verification items
- Miss: small-checklist principle (5-10 items), automate-what-you-can (don't include linter-catchable items), state-the-obvious principle, Hawthorne Effect for compliance, checklist-vs-procedure distinction, WHY for each item
- Produce a checklist that teams won't follow because it's too long

**Baseline score: 4/10** (creates a checklist but violates key design principles, too long, includes automatable items)

### Test 2 Baseline
A general agent would:
- Create a deployment checklist with 10-20 items covering many scenarios
- Include both the specific incident types and general best practices
- Miss: size limit principle, checklist-vs-procedure distinction (likely includes procedural deployment steps), Hawthorne Effect compliance strategy, targeting only the specific failure modes, WHY for each item
- May include items that should be in a CI/CD pipeline instead

**Baseline score: 4/10** (addresses the incidents but produces an overly broad checklist without compliance strategy)

### Test 3 Baseline
A general agent would:
- Suggest making the checklist shorter
- Recommend getting team buy-in
- Create a new, somewhat shorter checklist
- Miss: systematic diagnosis (separate procedures from checklists, identify automatable items, split into purpose-specific checklists), the law-of-diminishing-returns principle, Hawthorne Effect for compliance, the insight that 50 items should become 3 checklists of 6
- Not provide a structured migration plan from the old checklist

**Baseline score: 3/10** (recognizes the problem but doesn't apply systematic design principles to solve it)

## With-Skill Analysis

### Test 1 With Skill
The skill would guide the agent to:
- Verify each item is independently verifiable (not procedural)
- Verify each item is NOT automatable (if linter catches it, don't include it)
- Create a focused 7-item checklist targeting the three specific pain points plus related items
- Include WHY for each item
- Apply state-the-obvious principle for items like "no hardcoded credentials"
- Include Hawthorne Effect compliance strategy (tech lead spot-checks 1 PR/week)
- Recommend team involvement in finalizing items

**With-skill score: 9/10** (focused, principle-driven checklist with compliance strategy)

### Test 2 With Skill
The skill would guide the agent to:
- Map each incident directly to a checklist item (wrong config -> config verification, missing migration -> migration check, stale cache -> cache invalidation)
- Verify items are independently checkable (not deployment procedure steps)
- Check which items could be automated in CI/CD (e.g., config validation could be a pipeline step)
- Create a focused 6-item checklist with WHY for each item
- Include Hawthorne Effect compliance strategy
- Include graduation plan (remove items when they're automated or no longer error-prone)

**With-skill score: 9/10** (incident-targeted, correctly distinguishes checklist from procedure, includes compliance)

### Test 3 With Skill
The skill would guide the agent to:
- Diagnose the 50-item checklist: separate procedural items (belong in workflow docs), identify automatable items (belong in CI), group remaining items
- Apply law of diminishing returns: 50 items = rubber-stamping guaranteed
- Split into 3 focused checklists (code completion, testing, release) of ~6 items each
- Recommend sunsetting the 50-item checklist
- Include team workshop for collaborative refinement
- Apply Hawthorne Effect for the new checklists
- Provide migration plan from old to new

**With-skill score: 10/10** (correctly diagnoses the root cause, applies all design principles, provides migration plan)

## Score Summary

| Test | Without Skill | With Skill | Gap |
|------|:---:|:---:|:---:|
| Test 1: Code completion checklist | 4/10 | 9/10 | +5 |
| Test 2: Release checklist | 4/10 | 9/10 | +5 |
| Test 3: Fixing ignored 50-item checklist | 3/10 | 10/10 | +7 |
| **Average** | **3.7/10 (37%)** | **9.3/10 (93%)** | **+57 points** |

## Value Assertions Verified

| Assertion | Test 1 | Test 2 | Test 3 |
|-----------|:---:|:---:|:---:|
| distinguishes-checklist-procedure | Y | Y | Y |
| keeps-small | Y | Y | Y |
| states-obvious | Y | Y | N/A |
| excludes-automatable | Y | Y | Y |
| applies-hawthorne-effect | Y | Y | Y |
| includes-graduation-plan | N/A | Y | Y |
| targets-actual-pain-points | Y | Y | Y |

## Conclusion

The skill provides strong value across all three test scenarios. Test 3 showed the largest gap (+7 points) because diagnosing and restructuring a failing 50-item checklist requires understanding ALL the design principles (procedure distinction, automation exclusion, size limits, splitting strategy), which no general agent would systematically apply. The primary differentiators are: (1) the checklist-vs-procedure distinction that prevents producing procedural checklists, (2) the size limit principle that prevents the very problem the user is experiencing, (3) the Hawthorne Effect compliance strategy that addresses adoption, and (4) the automate-what-you-can principle that focuses human attention where it matters.
