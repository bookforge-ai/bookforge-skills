---
name: architecture-fitness-function-designer
description: Design automated governance mechanisms (fitness functions) that objectively measure and enforce architecture characteristics over time. Use this skill whenever the user asks about architecture governance, fitness functions, automated architecture testing, architecture compliance checks, preventing architecture erosion, enforcing layer dependencies, cyclomatic complexity thresholds, ArchUnit or NetArchTest rules, structural tests for architecture, CI/CD architecture gates, chaos engineering as governance, measuring architecture characteristics objectively, architecture drift detection, continuous architecture verification, or wants to ensure their codebase stays aligned with architecture decisions -- even if they don't use the term "fitness function."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/architecture-fitness-function-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [6]
tags: [software-architecture, fitness-functions, governance, metrics, architecture-erosion, ArchUnit, CI-CD, cyclomatic-complexity, chaos-engineering]
depends-on:
  - architecture-characteristics-identifier
  - modularity-health-evaluator
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "A software project with identified architecture characteristics to govern"
    - type: none
      description: "Alternatively, a description of architecture decisions and characteristics to protect"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob, Bash]
  mcps-required: []
  environment: "Best results inside a codebase directory with CI/CD pipeline access. Can also produce a governance plan from descriptions."
---

# Architecture Fitness Function Designer

## When to Use

You need to create automated, objective mechanisms that verify your architecture characteristics are maintained over time. Typical triggers:

- The user has identified architecture characteristics (scalability, deployability, testability, etc.) but has no automated way to verify them
- The user's architecture decisions are being violated without detection -- code is drifting from the intended design
- The user wants to enforce structural rules (layer dependencies, package access, no circular dependencies)
- The user wants CI/CD pipeline gates that prevent architecture degradation
- The user is concerned about architecture erosion -- decisions made months ago are no longer reflected in the code
- The user mentions chaos engineering, ArchUnit, NetArchTest, or architectural compliance testing

Before starting, verify:
- Are the target architecture characteristics already identified? (If not, invoke the `architecture-characteristics-identifier` skill first)
- Does the user have a CI/CD pipeline where fitness functions can be integrated?
- What technology stack is in use? (This determines which fitness function tools are available)

## Context & Input Gathering

### Required Context (must have before proceeding)

- **Architecture characteristics to govern:** Which quality attributes need automated enforcement?
  -> Check prompt for: scalability, performance, deployability, testability, security, modularity, maintainability
  -> Check environment for: ADRs, architecture docs, quality attribute definitions
  -> If still missing, ask: "Which architecture characteristics are most important for your system? Pick your top 3."

- **Technology stack:** What language/framework is the codebase built with?
  -> Check prompt for: Java, Kotlin, C#, .NET, Python, Go, JavaScript/TypeScript, Spring, Django
  -> Check environment for: pom.xml, build.gradle, package.json, go.mod, requirements.txt, *.csproj
  -> If still missing, ask: "What is your primary technology stack? This determines which fitness function tools are available."

### Observable Context (gather from environment if available)

- **Existing CI/CD pipeline:** Is there a pipeline to integrate fitness functions into?
  -> Look for: Jenkinsfile, .github/workflows/, .gitlab-ci.yml, Dockerfile, docker-compose.yml
  -> If unavailable: design fitness functions as standalone test suites

- **Existing architecture tests:** Are there any structural tests already in place?
  -> Look for: ArchUnit tests, NetArchTest files, custom architecture validation scripts
  -> If unavailable: start from scratch

- **Codebase structure:** How is the code organized?
  -> Look for: package structure, layer boundaries, module organization
  -> If unavailable: rely on user description

### Default Assumptions

- If no CI/CD pipeline exists -> design fitness functions as test suites that can be run locally and later integrated
- If architecture characteristics are not formally identified -> derive them from the user's concern description
- If no specific thresholds are mentioned -> use industry-standard defaults (CC<10, p95 response times, etc.)
- If technology is unknown -> provide language-agnostic fitness function designs with tool recommendations

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- At least one architecture characteristic is identified for governance
- Technology stack is known or estimable
- The user's governance concern is clear (what they want to prevent)

PROCEED WITH DEFAULTS when:
- Characteristics are identified
- Technology stack is partially known
- Specific thresholds can use industry defaults

MUST ASK when:
- No architecture characteristics are identified AND cannot be inferred
- The user's concern is too vague to design specific fitness functions
```

## Process

### Step 1: Inventory Architecture Characteristics to Govern

**ACTION:** List all architecture characteristics that need automated governance. For each, identify:
- Category: operational (runtime behavior), structural (code organization), or process (development workflow)
- Current state: is this characteristic being measured at all today?
- Risk level: what is the consequence if this characteristic degrades undetected?

**WHY:** Fitness functions are only valuable when they protect characteristics that matter. Trying to govern everything creates noise and slows the pipeline. By categorizing characteristics, you determine which types of fitness functions to create. Operational characteristics need runtime monitoring. Structural characteristics need build-time analysis. Process characteristics need CI/CD pipeline metrics. Prioritize by risk -- a silently degrading scalability characteristic is more dangerous than a slightly suboptimal code style metric.

**IF** characteristics are already identified (from `architecture-characteristics-identifier`) -> proceed with that list
**ELSE** -> extract characteristics from the user's concern description and architecture documentation

### Step 2: Define Measurable Thresholds for Each Characteristic

**ACTION:** For each architecture characteristic, define what "good" looks like with concrete, measurable thresholds:

**Operational characteristics:**
- Response time: use percentiles, not averages. p95 < 200ms, p99 < 500ms (averages hide tail latency)
- Throughput: requests per second under expected load
- Availability: uptime percentage (99.9% = 8.7 hours downtime/year)
- Scalability: response time degradation under 2x, 5x, 10x load

**Structural characteristics:**
- Cyclomatic complexity: CC<10 per function (simple/low risk), 10-20 (moderate), >20 (problematic), >50 (untestable)
- Layer violations: zero tolerance for bypassing layers (e.g., UI directly calling database)
- Package dependency rules: no circular dependencies, enforced dependency direction
- Component coupling: maximum efferent coupling per module

**Process characteristics:**
- Test coverage: minimum percentage per module (e.g., >80% for critical paths)
- Deployment frequency: target deployments per week/day
- Change lead time: commit to production time
- Mean time to recover (MTTR): maximum acceptable recovery time

**WHY:** Without concrete thresholds, fitness functions become subjective opinions rather than objective tests. A fitness function that says "performance should be good" is useless. A fitness function that says "p95 response time for /api/orders must be under 200ms" is a pass/fail gate. The threshold is the line between "architecture is intact" and "architecture is eroding." For response times specifically, averages are misleading -- a p50 of 50ms can hide a p99 of 5000ms, meaning 1% of users have a terrible experience. Always use percentiles.

### Step 3: Classify Each Fitness Function

**ACTION:** For each fitness function, classify along five dimensions:

1. **Scope: Atomic vs Holistic**
   - Atomic: tests a single characteristic in isolation (e.g., "no class exceeds CC of 20")
   - Holistic: tests the interplay of multiple characteristics (e.g., "security + performance: encryption must not push p95 above 300ms")

2. **Cadence: Triggered vs Continuous**
   - Triggered: runs on specific events (commit, PR, deployment)
   - Continuous: runs constantly in production (monitoring, alerting)

3. **Nature: Static vs Dynamic**
   - Static: analyzes code/configuration without running it (linting, dependency analysis)
   - Dynamic: requires running the system (load tests, chaos tests, integration tests)

4. **Automation: Automated vs Manual**
   - Automated: runs without human intervention (preferred)
   - Manual: requires human judgment (code review checklists, architecture review boards)

5. **Temporality: Fixed vs Evolving**
   - Fixed: threshold stays constant (zero layer violations)
   - Evolving: threshold tightens over time (CC limit drops from 30 to 20 to 10 as codebase matures)

**WHY:** Classification determines where and how each fitness function is implemented. An atomic/triggered/static/automated fitness function is a unit test in CI. A holistic/continuous/dynamic/automated fitness function is a production monitoring alert. A holistic/triggered/dynamic/manual fitness function is a pre-release load test with human review. Without classification, teams implement all fitness functions in the same way, which either misses runtime issues (all static) or slows the pipeline (all dynamic).

### Step 4: Design Implementation for Each Fitness Function

**ACTION:** For each classified fitness function, specify the concrete implementation:

**For structural fitness functions (static/triggered):**
- Java/Kotlin: ArchUnit tests in the test suite
  ```java
  @ArchTest
  static final ArchRule no_layer_violations =
      noClasses().that().resideInAPackage("..service..")
          .should().dependOnClassesThat().resideInAPackage("..controller..");
  ```
- C#/.NET: NetArchTest
- Python: custom pytest fixtures using AST analysis or import linting
- Any language: custom scripts analyzing dependency graphs

**For operational fitness functions (dynamic/continuous):**
- Response time monitoring with percentile alerting (Prometheus, Datadog, New Relic)
- Load test suites (k6, Gatling, Locust) with pass/fail thresholds
- Chaos engineering: randomly terminate instances to verify resilience (inspired by Netflix Simian Army)
- Health check endpoints with degradation detection

**For process fitness functions (triggered):**
- CI pipeline gates: test coverage checks, deployment frequency tracking
- Git hooks: commit message format, branch naming conventions
- Build-time metrics: build duration, artifact size budgets

**WHY:** A fitness function that exists only as documentation is not a fitness function -- it is a wish. Implementation specifics ensure each function actually runs, produces a pass/fail result, and blocks or alerts when the architecture is violated. The tool choice matters because some fitness functions only work with specific ecosystems. ArchUnit is powerful for JVM projects but useless for Python. Chaos engineering requires production-like environments. Design the implementation around the team's actual capabilities and tooling.

**IF** codebase is available -> **AGENT: EXECUTES** -- generate fitness function test files, CI config, monitoring config
**ELSE** -> produce implementation specifications with code templates

### Step 5: Design the Integration Strategy

**ACTION:** Determine where each fitness function runs in the development lifecycle:

```
Developer Workstation     CI Pipeline            Staging              Production
├── Pre-commit hooks      ├── Build stage         ├── Load tests       ├── Continuous monitoring
│   └── Linting           │   └── ArchUnit        │   └── p95 gates    │   └── p95/p99 alerts
│   └── CC check (fast)   │   └── CC analysis     ├── Chaos tests      ├── Chaos engineering
├── Pre-push hooks        ├── Test stage          │   └── Resilience    │   └── Simian Army
│   └── Dep. analysis     │   └── Coverage gate   ├── Security scans   ├── Architecture drift
                          ├── Quality gate        │   └── OWASP/SAST    │   └── Daily reports
                          │   └── Pass/fail                            ├── SLA monitoring
                          ├── Deploy gate                              │   └── Uptime alerts
                          │   └── Approval
```

**WHY:** Fitness functions placed too early slow developers down (running load tests on every commit). Fitness functions placed too late catch problems when they are expensive to fix (finding layer violations in production). The integration strategy matches each fitness function to the earliest point where it can run without unacceptable delay. Static/atomic functions run on every commit. Dynamic/holistic functions run in staging or production. This mirrors the testing pyramid: fast/cheap tests run frequently, slow/expensive tests run at key gates.

**HANDOFF TO HUMAN** for production chaos engineering setup -- injecting failures in production requires organizational buy-in, blast radius controls, and runbook preparation that go beyond what an agent can configure.

### Step 6: Create the Fitness Function Governance Report

**ACTION:** Produce the complete fitness function design document combining all classifications, implementations, and integration points.

**WHY:** The governance report serves as the architecture team's contract with the development team. It documents what is being governed, why, and how -- so developers understand that a failing fitness function is not a "broken test" but an architecture violation that needs architectural resolution, not a test skip. Without this document, fitness functions are treated as optional tests that can be ignored under deadline pressure.

## Inputs

- Architecture characteristics to govern (from the `architecture-characteristics-identifier` skill or user description)
- Technology stack and CI/CD pipeline configuration
- Existing architecture decisions or ADRs
- Optionally: current codebase for structural analysis, production monitoring setup

## Outputs

### Fitness Function Governance Report

```markdown
# Fitness Function Governance Report: {System Name}

## Governance Scope
- **Date:** {date}
- **Architecture characteristics governed:** {list}
- **Technology stack:** {stack}
- **CI/CD pipeline:** {tool}

## Fitness Function Inventory

| ID | Characteristic | Fitness Function | Threshold | Scope | Cadence | Nature | Automation |
|----|---------------|-----------------|-----------|-------|---------|--------|------------|
| FF-01 | {characteristic} | {description} | {threshold} | {atomic/holistic} | {triggered/continuous} | {static/dynamic} | {auto/manual} |

## Implementation Details

### FF-01: {Fitness Function Name}
- **Protects:** {characteristic}
- **Threshold:** {measurable pass/fail criteria}
- **Classification:** {scope} / {cadence} / {nature} / {automation} / {temporality}
- **Implementation:** {tool and code/config}
- **Integration point:** {where it runs in the lifecycle}
- **Failure action:** {block pipeline / alert / report}
- **Evolving threshold:** {how the threshold changes over time, if applicable}

## Integration Map

{Lifecycle diagram showing where each FF runs}

## Temporal Evolution Plan

| Phase | Timeline | FF Changes |
|-------|----------|------------|
| Baseline | Now | {initial thresholds — permissive to establish baseline} |
| Tighten | +3 months | {reduce CC limit, increase coverage requirement} |
| Mature | +6 months | {add holistic FFs, chaos engineering} |

## Architecture Erosion Risk Assessment

| Risk | Without Fitness Functions | With Fitness Functions |
|------|------------------------|---------------------|
| {risk description} | {undetected until...} | {caught at... by FF-xx} |
```

## Key Principles

- **Fitness functions must be objective and automated** -- A fitness function that requires subjective human judgment is a code review, not a fitness function. The defining characteristic is objectivity: a machine can evaluate the result as pass or fail without interpretation. Manual fitness functions are acceptable only as a temporary measure while automation is being built, and they must have a migration plan to automation.

- **Measure percentiles, not averages, for operational characteristics** -- An average response time of 100ms can hide a p99 of 5 seconds. Averages are statistically misleading for latency distributions, which are typically long-tailed. Always define operational thresholds using p95 or p99 percentiles. This is the single most common measurement mistake in architecture governance.

- **Fitness functions are tests, not monitoring** -- Monitoring tells you what happened. Fitness functions tell you whether it was acceptable. A fitness function wraps a measurement in a pass/fail threshold. Response time monitoring without a threshold is observability. Response time monitoring that alerts when p95 exceeds 200ms is a fitness function. The threshold transforms data into governance.

- **Start permissive, tighten over time (temporal fitness functions)** -- A codebase with functions averaging CC of 35 cannot jump to a CC<10 threshold overnight. Set initial thresholds just below current worst-case, then ratchet them down quarterly. This prevents fitness functions from being disabled under pressure ("we can't ship if this test blocks us") while still driving improvement. The goal is a trend line, not immediate perfection.

- **Holistic fitness functions catch what atomic ones miss** -- Individual characteristics may pass their thresholds while the system as a whole degrades. Security encryption may pass its test, and response time may pass its test, but the combination degrades user experience. Holistic fitness functions test the interaction between characteristics. They are harder to build but catch the most dangerous architectural problems -- the ones that emerge from trade-off conflicts.

- **Architecture erosion is silent without fitness functions** -- Code naturally drifts from architectural intent. Developers under deadline pressure take shortcuts. Layer boundaries get bypassed. Dependency directions reverse. Without automated detection, this erosion accumulates until the architecture exists only in documentation, not in code. Fitness functions are the immune system that detects violations before they metastasize.

## Examples

**Scenario: Java Spring Boot microservices governance**
Trigger: "We identified scalability, deployability, and testability as our top architecture characteristics. How do we create automated checks to ensure our codebase doesn't drift from these goals? We use Java with Spring Boot and have a Jenkins CI pipeline."
Process: Inventoried three characteristics across operational, structural, and process categories. Defined thresholds: scalability (p95 <200ms under 2x load), deployability (deploy time <15min, zero-downtime deploys), testability (>80% coverage on service layer, CC<10 per method). Classified each: scalability = atomic/triggered/dynamic (load test in staging), deployability = atomic/triggered/static (build time check) + holistic/continuous/dynamic (deploy monitoring), testability = atomic/triggered/static (ArchUnit + JaCoCo in CI). Designed ArchUnit tests for layer dependency enforcement. Configured Jenkins pipeline gates: build -> ArchUnit -> coverage -> deploy-to-staging -> k6 load test -> promote.
Output: 8 fitness functions with Jenkins pipeline integration, ArchUnit test file, k6 load test script, and temporal evolution plan (tighten CC from 20 to 10 over 6 months).

**Scenario: Cross-database dependency enforcement**
Trigger: "Our architecture decision says 'no service should directly depend on another service's database.' How do we enforce this automatically? We have 8 microservices in a Kotlin/Spring project."
Process: Identified this as a structural/holistic fitness function protecting data isolation (a key microservices characteristic). Designed ArchUnit test that verifies each service's repository classes only reference their own database schema. Added a network-level fitness function: database connection strings in each service's config must only point to that service's database. Classified as atomic/triggered/static/automated. Created a holistic companion: integration test that detects cross-service database queries by analyzing SQL query logs. Integrated both into the CI pipeline as blocking gates.
Output: ArchUnit test class enforcing package-to-schema mapping, config validation script, integration test for cross-database query detection, and CI pipeline configuration.

**Scenario: Architecture erosion prevention program**
Trigger: "Our CTO is concerned about architecture erosion. We made decisions 6 months ago but nobody checks if the code still follows them. How do we set up governance that doesn't rely on manual code reviews?"
Process: Audited existing ADRs to identify 5 key architecture decisions. Mapped each decision to a testable fitness function: (1) layered architecture compliance -> ArchUnit layer rules, (2) no circular package dependencies -> JDepend analysis in CI, (3) API response time SLAs -> p95 monitoring with alerting, (4) maximum component coupling -> efferent coupling threshold in static analysis, (5) security: no plaintext secrets -> secret scanning in pre-commit hooks. Classified all as automated. Designed temporal evolution: start with reporting-only mode (2 weeks to establish baseline), then warning mode (2 weeks for team awareness), then blocking mode (permanent). Created architecture erosion dashboard showing fitness function pass rates over time.
Output: 5 fitness functions with phased rollout plan, ArchUnit configuration, CI pipeline gates, monitoring dashboard spec, and team communication template explaining the new governance approach.

## References

- For the complete fitness function classification taxonomy with examples per category, see [references/fitness-function-catalog.md](references/fitness-function-catalog.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-architecture-characteristics-identifier`
- `clawhub install bookforge-modularity-health-evaluator`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
