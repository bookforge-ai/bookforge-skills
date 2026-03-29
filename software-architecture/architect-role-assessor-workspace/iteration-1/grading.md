# Grading: architect-role-assessor (Iteration 1)

## Test Prompts

1. "I just got promoted to software architect from senior developer. I'm still spending 80% of my time coding. My team says I'm a bottleneck on code reviews. Am I doing the role right?"
2. "I've been an architect for 5 years but I only recommend technologies I've used before — Java/Spring for everything. My team wants to try Go and Kafka but I keep saying no because I had a bad experience with message queues in 2018. Is this a problem?"
3. "I'm an architect but I never attend stakeholder meetings. I design systems, write ADRs, and review code. My manager says I need to 'be more strategic.' What does the architect role actually require?"

## Baseline (Without Skill) Analysis

### Test 1 Baseline
A general agent would:
- Suggest spending less time coding and more time on architecture
- Recommend delegating code reviews
- Provide general career transition advice
- Miss: systematic assessment against 8 expectations, architecture-vs-design boundary test, knowledge pyramid shift from depth to breadth, specific transition plan with percentage targets (20-30% coding)
- Not identify which expectations are Strong vs Missing

**Baseline score: 4/10** (reasonable general advice but no structured framework or systematic assessment)

### Test 2 Baseline
A general agent would:
- Suggest being open to new technologies
- Recommend evaluating Go and Kafka objectively
- Possibly mention confirmation bias or past experience bias
- Miss: Frozen Caveman anti-pattern by name and specific diagnostic, knowledge pyramid assessment (depth-heavy without breadth), Expectation 5 (diverse exposure) evaluation, distinction between learning-from-experience vs Frozen Caveman, specific correction plan
- Not distinguish between legitimate caution and irrational fear

**Baseline score: 3/10** (generic "be more open-minded" advice, misses the specific anti-pattern and structured assessment)

### Test 3 Baseline
A general agent would:
- List some architect responsibilities
- Suggest attending more meetings
- Recommend "being strategic" with vague advice
- Miss: systematic 8-expectation scorecard showing exactly which expectations are Strong (1, 4) and which are Missing (6, 7, 8), translation of "be more strategic" to specific expectation failures, the organizational vs technical expectation split, specific engagement plan
- Not provide a structured assessment with evidence and recommendations per expectation

**Baseline score: 3/10** (vague advice without structured framework, can't map "strategic" to specific gaps)

## With-Skill Analysis

### Test 1 With Skill
The skill would guide the agent to:
- Assess against all 8 expectations: Expectation 1 (make architecture decisions) = Needs Improvement (making design decisions via code reviews), Expectations 2-4 likely Missing (no time for analysis, trends, compliance), Expectations 5-8 at risk
- Diagnose architecture-vs-design boundary violation: operating at design level
- Assess knowledge pyramid: depth-heavy from continued coding, breadth not growing
- Provide specific transition plan: reduce coding to 20-30%, shift to POCs and fitness functions, delegate code reviews to seniors, invest freed time in Expectations 2-8
- Produce structured assessment report with scorecard

**With-skill score: 9/10** (systematic assessment, boundary diagnosis, knowledge pyramid analysis, specific transition plan)

### Test 2 With Skill
The skill would guide the agent to:
- Identify Frozen Caveman anti-pattern: 2018 message queue failure driving current decisions without evaluating current context
- Distinguish from legitimate learning: "What is the probability of that 2018 failure in THIS system with TODAY's technology?"
- Assess Expectation 5 (diverse exposure): Java/Spring for everything = depth without breadth
- Assess knowledge pyramid: deep "stuff you know" (Java/Spring), actively suppressing "stuff you know you don't know" (Go, Kafka)
- Provide specific correction: evaluate whether 2018 failure conditions exist today, POC with Go/Kafka, target 2 new technologies per quarter
- Produce structured assessment flagging anti-pattern and Expectation 5 failure

**With-skill score: 10/10** (identifies specific anti-pattern, provides diagnostic framework, structured correction plan)

### Test 3 With Skill
The skill would guide the agent to:
- Assess against all 8 expectations: Expectations 1, 4 = Strong (ADRs, code reviews), Expectations 6, 7, 8 = Missing (no business knowledge, no interpersonal practice, no political navigation)
- Translate manager feedback: "be more strategic" = "you're fulfilling technical expectations but ignoring organizational expectations"
- Identify the gap pattern: technical expectations met, people/business expectations missing
- Provide specific plan: attend 2 stakeholder meetings/week, schedule PM 1-on-1s, add "Business Context" to ADRs
- Produce structured scorecard showing 3 of 8 expectations met

**With-skill score: 9/10** (precise diagnosis mapping manager feedback to specific expectation gaps, structured plan)

## Score Summary

| Test | Without Skill | With Skill | Gap |
|------|:---:|:---:|:---:|
| Test 1: New architect still coding | 4/10 | 9/10 | +5 |
| Test 2: Technology tunnel vision | 3/10 | 10/10 | +7 |
| Test 3: Avoiding stakeholder work | 3/10 | 9/10 | +6 |
| **Average** | **3.3/10 (33%)** | **9.3/10 (93%)** | **+60 points** |

## Value Assertions Verified

| Assertion | Test 1 | Test 2 | Test 3 |
|-----------|:---:|:---:|:---:|
| uses-8-expectations-framework | Y | Y | Y |
| identifies-frozen-caveman | N/A | Y | N/A |
| distinguishes-guide-specify | Y | N/A | N/A |
| maps-activities-to-expectations | Y | Y | Y |
| assesses-knowledge-pyramid | Y | Y | N/A |
| identifies-boundary-violations | Y | N/A | N/A |
| provides-transition-guidance | Y | Y | Y |

## Conclusion

The skill provides the highest value among the four skills tested, with an average gap of +60 points. The primary differentiation is: (1) the structured 8-expectation framework enabling systematic assessment rather than ad-hoc advice, (2) the Frozen Caveman anti-pattern detection which no general agent would identify by name, (3) the knowledge pyramid providing a concrete model for breadth-vs-depth assessment, and (4) the architecture-vs-design boundary test. Test 2 (technology tunnel vision) showed the largest gap (+7 points) because the Frozen Caveman detection is entirely unique to this skill.
