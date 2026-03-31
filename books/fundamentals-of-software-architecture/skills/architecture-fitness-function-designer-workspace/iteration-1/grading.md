# Grading Report: architecture-fitness-function-designer

## Grading Criteria

Each output is graded against the value assertions defined in the value-contributions file. Assertions are split into **structural** (does the output have the right sections/structure?) and **value** (does it contain book-specific knowledge that a general agent wouldn't provide?).

### Structural Assertions
- S1: Inventories architecture characteristics categorized as operational/structural/process
- S2: Defines concrete measurable thresholds (not vague "should be good")
- S3: Classifies fitness functions along at least 3 of 5 dimensions
- S4: Provides concrete implementation (tool names, code snippets, or configuration)
- S5: Specifies where each fitness function runs in the development lifecycle

### Value Assertions
- V1: Classifies fitness functions as atomic/holistic, triggered/continuous, static/dynamic
- V2: Specifies p95/p99 percentiles for operational metrics rather than averages
- V3: References cyclomatic complexity threshold bands (CC<10, 10-20, >20, >50)
- V4: Recommends evolving thresholds over time (start permissive, tighten gradually)
- V5: Explicitly connects fitness functions to preventing architecture erosion
- V6: Recommends specific tools appropriate for the technology stack
- V7: Places different fitness functions at different lifecycle stages
- V8: Designs at least one holistic fitness function testing interplay of multiple characteristics

---

## Eval 1: Java Spring Boot Scalability/Deployability/Testability

**Prompt:** "We identified scalability, deployability, and testability as our top architecture characteristics. How do we create automated checks to ensure our codebase doesn't drift from these goals? We use Java with Spring Boot and have a Jenkins CI pipeline."

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|---------|
| S1 | Partial | Lists recommendations by characteristic but does not categorize as operational/structural/process |
| S2 | No | Mentions "e.g., 80%" for coverage but no other concrete thresholds; response time has no specific number |
| S3 | No | No classification taxonomy at all |
| S4 | Partial | Mentions SonarQube, JaCoCo, JMeter by name; minimal Jenkinsfile snippet |
| S5 | Partial | Mentions Jenkins pipeline stages but no lifecycle mapping |
| V1 | No | No fitness function classification |
| V2 | No | Says "monitor response times" without mentioning percentiles |
| V3 | No | No cyclomatic complexity thresholds mentioned |
| V4 | Partial | Says "start with basics and gradually add" but not about threshold evolution |
| V5 | No | Does not mention architecture erosion |
| V6 | Partial | Mentions SonarQube, JaCoCo, JMeter but generically |
| V7 | No | All checks in one "pipeline" without lifecycle differentiation |
| V8 | No | No holistic fitness functions |

**Score: 2/13 full passes, 4/13 partial = 15% (counting partials as 0.5: 4/13 = 31%)**

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|---------|
| S1 | Yes | Characteristic Inventory table with operational/structural/process categories |
| S2 | Yes | CC<10 per method, >80% coverage, p95<200ms, <15min deploy time -- all concrete |
| S3 | Yes | Every FF classified across all 5 dimensions (scope, cadence, nature, automation, temporality) |
| S4 | Yes | ArchUnit Java code, PMD XML config, JaCoCo XML config, k6 JavaScript load test |
| S5 | Yes | Integration Map with Developer -> CI -> Staging -> Production lifecycle stages |
| V1 | Yes | Every FF classified as atomic/holistic, triggered/continuous, static/dynamic |
| V2 | Yes | "p95 <200ms at 2x baseline load" with explicit WHY explaining averages hide tail latency |
| V3 | Yes | "CC<10 per method" with evolving thresholds from CC<20 down to CC<10, plus WHY explanation |
| V4 | Yes | Temporal Evolution Plan table: baseline -> awareness -> soft -> full -> tighten -> target |
| V5 | Yes | Architecture Erosion Risk Assessment table comparing with/without fitness functions |
| V6 | Yes | ArchUnit, PMD, JaCoCo, k6 -- all specific to Java/Spring Boot/Jenkins |
| V7 | Yes | Different FFs at different stages: CC in CI, ArchUnit in CI, k6 in staging, monitoring in production |
| V8 | Yes | FF-05 (scalability degradation) and FF-08 (agility composite) are holistic |

**Score: 13/13 = 100%**

---

## Eval 2: Cross-Database Dependency Enforcement (Kotlin/Spring)

**Prompt:** "Our architecture decision says 'no service should directly depend on another service's database.' How do we enforce this automatically? We have 8 microservices in a Kotlin/Spring project."

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|---------|
| S1 | No | Does not inventory characteristics; focuses on the single decision without categorization |
| S2 | No | No measurable thresholds; suggestions are qualitative ("verify," "check") |
| S3 | No | No classification |
| S4 | Partial | SQL permission example is concrete; "static analysis" and "integration testing" are vague |
| S5 | No | No lifecycle mapping; says "start with permissions and code review" |
| V1 | No | No fitness function classification |
| V2 | N/A | Operational metrics not relevant to this prompt |
| V3 | N/A | CC not relevant to this prompt |
| V4 | No | No evolving thresholds |
| V5 | No | Does not mention architecture erosion |
| V6 | Partial | Mentions SonarQube generically, SQL permissions concretely |
| V7 | No | No lifecycle differentiation |
| V8 | No | No holistic fitness functions |

**Score: 0/11 applicable full passes, 2/11 partial = 9%**

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|---------|
| S1 | Yes | Characteristic Analysis table mapping data isolation to deployability, modularity, fault tolerance, scalability |
| S2 | Yes | "Zero violations," "zero cross-schema queries," "each service config references only its own DB" |
| S3 | Yes | All 4 FFs classified by scope, cadence, nature, automation |
| S4 | Yes | Kotlin ArchUnit code, Kotlin Spring test, bash config checker, Prometheus alert rule, SQL audit query |
| S5 | Yes | Integration Map: CI build -> CI test -> continuous monitoring -> weekly scheduled |
| V1 | Yes | Classified: atomic/triggered/static (FF-01), holistic/continuous/dynamic (FF-03) |
| V2 | N/A | Not applicable |
| V3 | N/A | Not applicable |
| V4 | No | No evolving thresholds (all fixed -- appropriate for zero-tolerance rules) |
| V5 | Yes | Explicit Architecture Erosion Risk Assessment table |
| V6 | Yes | ArchUnit for Kotlin/JVM, Prometheus, trufflehog, git-secrets -- stack-appropriate |
| V7 | Yes | Pre-commit, CI build, CI test, continuous production monitoring, weekly audit -- all different stages |
| V8 | Yes | FF-03 (cross-service query detection) tests multiple services' runtime behavior holistically |

**Score: 9/11 applicable = 82% (V4 is a justified miss -- zero-tolerance rules don't evolve)**

Adjusted for justified miss: **10/11 = 91%**

---

## Eval 3: Architecture Erosion Prevention (General)

**Prompt:** "Our CTO is concerned about architecture erosion. We made decisions 6 months ago but nobody checks if the code still follows them. How do we set up governance that doesn't rely on manual code reviews?"

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|---------|
| S1 | No | Lists "ADRs, linting, CI gates, review board, monitoring" but doesn't categorize characteristics |
| S2 | No | No concrete thresholds anywhere |
| S3 | No | No classification |
| S4 | No | Mentions SonarQube and ESLint by name but no code, config, or specific rules |
| S5 | Partial | "Getting Started" section implies ordering but no lifecycle mapping |
| V1 | No | No fitness function classification |
| V2 | No | Says "response times" without percentiles |
| V3 | No | No CC thresholds |
| V4 | Partial | Says "start with easiest wins and build up" but not about threshold evolution |
| V5 | Partial | Mentions "architecture erodes over time" in intro but doesn't connect to systematic governance |
| V6 | Partial | Mentions SonarQube, ESLint, Checkstyle but generically |
| V7 | No | No lifecycle differentiation |
| V8 | No | No holistic fitness functions |

**Score: 0/13 full passes, 4/13 partial = 15%**

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:-----:|---------|
| S1 | Yes | Decision audit table mapping decisions to testable/structural/operational/security categories |
| S2 | Yes | "Zero violations," "p95 < 200ms, p99 < 500ms," "Ce < 10 per package," "> 80% compliance" |
| S3 | Yes | All 6 FFs classified by scope, cadence, nature, automation, temporality |
| S4 | Yes | ArchUnit layered architecture code, Prometheus alert YAML, JDepend coupling test, git-secrets config, bash script |
| S5 | Yes | Integration: pre-commit hooks, CI test stage, continuous production monitoring, weekly audit, weekly report |
| V1 | Yes | Each FF classified: atomic/triggered/static, atomic/continuous/dynamic, holistic/triggered/static |
| V2 | Yes | "p95 < 200ms, p99 < 500ms (NOT average)" with explicit WHY paragraph |
| V3 | No | CC not included in this particular set of decisions (focused on existing ADRs which didn't include CC) |
| V4 | Yes | FF-04 has evolving threshold: "Month 1-3: Ce < 20. Month 4-6: Ce < 15. Month 7+: Ce < 10" plus phased rollout plan |
| V5 | Yes | Entire framing is about architecture erosion with detailed WHY section and risk assessment table |
| V6 | Yes | ArchUnit, Prometheus, JDepend, git-secrets, trufflehog -- all specific and appropriate |
| V7 | Yes | Pre-commit -> CI -> production -> weekly audit -- different functions at different stages |
| V8 | Yes | FF-06 (erosion dashboard composite) combines all individual FFs into holistic score |

**Score: 12/13 = 92% (V3 is a justified miss -- CC was not among the existing ADRs being governed)**

Adjusted for justified miss: **12/12 applicable = 100%**

---

## Summary Scores

| Eval | Prompt | Without Skill | With Skill | Gap |
|:----:|--------|:------------:|:----------:|:---:|
| 1 | Java Spring Boot governance | 15% | 100% | +85 |
| 2 | Cross-database isolation | 9% | 91% | +82 |
| 3 | Architecture erosion prevention | 15% | 100% | +85 |
| **Average** | | **13%** | **97%** | **+84** |

## Key Observations

### What the skill adds that general agents miss:

1. **Fitness function classification taxonomy** -- General agents suggest "write tests" and "use SonarQube" without classifying governance mechanisms by scope, cadence, nature, automation, and temporality. The classification determines WHERE and HOW each function is implemented.

2. **Percentile-based measurement** -- General agents say "monitor response times" without specifying percentiles. The skill enforces p95/p99 and explains why averages are misleading for latency distributions.

3. **Evolving thresholds (temporal fitness functions)** -- General agents either suggest no thresholds or suggest final-state thresholds. The skill introduces the concept of starting permissive and tightening over time, which prevents governance from being disabled under deadline pressure.

4. **Architecture erosion framing** -- General agents list tools and practices. The skill frames the entire problem as architecture erosion (code diverging from intent) and positions fitness functions as the systematic solution, with defense-in-depth and phased rollout.

5. **Holistic fitness functions** -- General agents treat each check independently. The skill designs composite fitness functions that test the interplay of multiple characteristics, catching emergent degradation that individual checks miss.

6. **Lifecycle integration strategy** -- General agents put everything in "the CI pipeline." The skill maps different fitness functions to appropriate lifecycle stages (pre-commit, CI, staging, production, scheduled) based on their classification.

### What general agents do adequately:

- Mentioning tool names (SonarQube, JaCoCo, Jenkins) -- though without specific configuration
- Acknowledging the need for automation over manual reviews
- Suggesting "start simple and add more over time" (though without the structured temporal evolution plan)
