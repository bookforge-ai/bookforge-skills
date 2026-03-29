# Fitness Function Governance Report: Architecture Erosion Prevention Program

## Governance Scope
- **Date:** 2026-03-27
- **Problem:** Architecture decisions made 6 months ago are not being enforced. Code has drifted from the intended design without detection. Manual code reviews are insufficient for continuous governance.
- **Solution:** Architecture fitness functions -- automated, objective tests that verify architecture characteristics are maintained over time. Fitness functions transform architecture decisions from documentation into executable governance.

## What Is Architecture Erosion?

Architecture erosion occurs when the actual code diverges from the intended architecture without anyone detecting it. It is silent and cumulative:

1. A developer bypasses a layer boundary "just this once" under deadline pressure
2. Another developer sees the precedent and does the same
3. Within months, the layer boundary exists only in documentation, not in code
4. The architecture team discovers the erosion during a crisis when refactoring is 10x more expensive

**WHY fitness functions solve this:** Manual code reviews catch violations only when a reviewer remembers the rule AND reviews the right file at the right time. Fitness functions catch violations on every commit, 24/7, with zero cognitive load on reviewers. They are the immune system that detects violations before they metastasize.

## Step 1: Audit Existing Architecture Decisions

Before designing fitness functions, inventory what decisions need enforcement. For each existing ADR or architecture decision:

| # | Architecture Decision | Testable? | Fitness Function Type |
|---|----------------------|-----------|----------------------|
| 1 | Layered architecture: controllers -> services -> repositories | Yes | Structural / Static |
| 2 | No circular package dependencies | Yes | Structural / Static |
| 3 | API response time SLAs (p95 < 200ms) | Yes | Operational / Dynamic |
| 4 | Maximum component coupling (Ce < 10 per package) | Yes | Structural / Static |
| 5 | No plaintext secrets in codebase | Yes | Security / Static |

**Decisions that CANNOT become fitness functions** (require human judgment):
- "Choose the simplest architecture that meets requirements" -- too subjective
- "Prefer composition over inheritance" -- context-dependent, no binary threshold

**WHY audit first:** Designing fitness functions without knowing which decisions to enforce produces generic checks that don't protect your specific architecture. The ADR audit ensures every fitness function maps to a real decision that someone made for a real reason.

## Fitness Function Inventory

| ID | Decision Protected | Fitness Function | Threshold | Classification | Tool |
|----|-------------------|-----------------|-----------|----------------|------|
| FF-01 | Layered architecture | Layer dependency rules | Zero violations | Atomic/Triggered/Static/Automated/Fixed | ArchUnit |
| FF-02 | No circular deps | Cycle detection | Zero cycles | Atomic/Triggered/Static/Automated/Fixed | ArchUnit / JDepend |
| FF-03 | API response SLAs | p95 response time monitoring | p95 < 200ms, p99 < 500ms | Atomic/Continuous/Dynamic/Automated/Fixed | Prometheus + alerting |
| FF-04 | Component coupling limit | Efferent coupling check | Ce < 10 per package | Atomic/Triggered/Static/Automated/Evolving | JDepend / custom |
| FF-05 | No plaintext secrets | Secret scanning | Zero matches | Atomic/Triggered/Static/Automated/Fixed | git-secrets / trufflehog |
| FF-06 | Overall architecture health | Erosion dashboard composite | > 80% compliance | Holistic/Triggered/Static/Automated/Evolving | Custom |

## Implementation Details

### FF-01: Layer Dependency Rules
- **Decision:** "The system follows a layered architecture: controllers depend on services, services depend on repositories. No layer may bypass another."
- **Threshold:** Zero violations. Any bypass = pipeline failure.
- **Implementation:**
  ```java
  @AnalyzeClasses(packages = "com.myapp")
  public class ArchitectureGovernanceTest {

      @ArchTest
      static final ArchRule layer_dependencies =
          layeredArchitecture()
              .consideringAllDependencies()
              .layer("Controller").definedBy("..controller..")
              .layer("Service").definedBy("..service..")
              .layer("Repository").definedBy("..repository..")
              .whereLayer("Controller").mayOnlyAccessLayers("Service")
              .whereLayer("Service").mayOnlyAccessLayers("Repository")
              .whereLayer("Repository").mayNotAccessAnyLayer();
  }
  ```
- **Integration point:** CI test stage (every push, runs in < 3 seconds)
- **Failure action:** Block pipeline, report exact class and dependency that violates the rule

### FF-02: Circular Dependency Detection
- **Decision:** "No circular dependencies between packages."
- **Threshold:** Zero cycles in the package dependency graph.
- **Implementation:**
  ```java
  @ArchTest
  static final ArchRule no_package_cycles =
      slices().matching("com.myapp.(*)..").should().beFreeOfCycles();
  ```
- **Integration point:** CI test stage
- **Failure action:** Block pipeline, report the cycle path

### FF-03: API Response Time SLA
- **Decision:** "All API endpoints must respond within SLA targets."
- **Threshold:** p95 < 200ms, p99 < 500ms (NOT average -- averages hide tail latency)
- **Implementation:**
  ```yaml
  # Prometheus alerting rule
  groups:
    - name: architecture-fitness-functions
      rules:
        - alert: ResponseTimeSLAViolation
          expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 0.2
          for: 5m
          labels:
            severity: critical
            fitness_function: FF-03
          annotations:
            summary: "p95 response time exceeds 200ms SLA"
            description: "Endpoint {{ $labels.endpoint }} p95 is {{ $value }}s"
  ```
- **Integration point:** Continuous in production
- **Failure action:** Alert on-call engineer + architecture team
- **WHY p95/p99:** An endpoint with average response time of 80ms may have p99 of 5000ms. This means 1 in 100 requests takes 5 seconds. At 10,000 requests/hour, that is 100 users per hour with terrible experience. Percentiles reveal what averages hide.

### FF-04: Efferent Coupling Limit
- **Decision:** "No package should depend on more than 10 other packages."
- **Threshold:** Ce < 10 per package (evolving: start at Ce < 20, tighten quarterly)
- **Implementation:**
  ```java
  @Test
  void no_package_exceeds_coupling_limit() {
      JavaClasses classes = new ClassFileImporter().importPackages("com.myapp");
      Map<String, Long> couplingByPackage = classes.stream()
          .collect(Collectors.groupingBy(
              c -> c.getPackageName(),
              Collectors.flatMapping(
                  c -> c.getDirectDependenciesFromSelf().stream()
                      .map(d -> d.getTargetClass().getPackageName()),
                  Collectors.toSet()
              ).andThen(s -> (long) s.size())
          ));
      couplingByPackage.forEach((pkg, ce) ->
          assertTrue(ce <= 10, pkg + " has efferent coupling of " + ce + " (max 10)")
      );
  }
  ```
- **Integration point:** CI test stage
- **Failure action:** Block pipeline
- **Evolving threshold:** Month 1-3: Ce < 20. Month 4-6: Ce < 15. Month 7+: Ce < 10.
- **WHY evolving:** A codebase with packages averaging Ce of 18 cannot adopt Ce < 10 overnight. Setting the initial threshold just below the current worst case and tightening quarterly drives improvement without causing the team to disable the check under deadline pressure.

### FF-05: Secret Scanning
- **Decision:** "No plaintext secrets in the codebase."
- **Threshold:** Zero matches for secret patterns.
- **Implementation:**
  ```bash
  # Pre-commit hook using git-secrets
  git secrets --install
  git secrets --register-aws  # AWS key patterns
  git secrets --add 'password\s*=\s*["\'][^"\']+["\']'  # Custom pattern
  git secrets --add 'api[_-]?key\s*=\s*["\'][^"\']+["\']'
  ```
  ```yaml
  # CI pipeline step
  - name: Secret Scan
    run: |
      docker run --rm -v $(pwd):/repo trufflesecurity/trufflehog filesystem /repo
      if [ $? -ne 0 ]; then exit 1; fi
  ```
- **Integration point:** Pre-commit hook + CI build stage
- **Failure action:** Block commit (pre-commit) or block pipeline (CI)

### FF-06: Architecture Erosion Dashboard (Composite)
- **Decision:** "Overall architecture health must remain above 80%."
- **Threshold:** Composite score > 80%
- **Formula:**
  ```
  erosion_score = (
      layer_compliance_rate +           # FF-01: % of builds with zero violations
      cycle_free_rate +                  # FF-02: % of builds with zero cycles
      sla_compliance_rate +              # FF-03: % of time p95 within SLA
      coupling_compliance_rate +         # FF-04: % of packages within Ce limit
      secret_scan_pass_rate              # FF-05: % of commits with zero secrets
  ) / 5
  ```
- **Integration point:** Weekly automated report
- **Failure action:** Trigger architecture review meeting if score drops below 80%
- **WHY composite:** Individual fitness functions can all be "mostly passing" while the architecture is slowly eroding across multiple dimensions simultaneously. The composite score detects cumulative drift that no single function catches.

## Phased Rollout Plan

**WHY phased:** Deploying all fitness functions as blocking gates on day one creates developer backlash and risks the entire governance program being abandoned. A phased approach builds trust and gives teams time to address existing violations before enforcement begins.

| Phase | Timeline | Actions | Mode |
|-------|----------|---------|------|
| **1. Baseline** | Week 1-2 | Deploy FF-01 through FF-05 in reporting-only mode. Measure current violation counts. Establish baseline for each metric. | Report only |
| **2. Awareness** | Week 3-4 | Share baseline report with all teams. Present the erosion dashboard. Discuss which violations are most critical. Agree on initial thresholds for evolving functions (FF-04). | Report only |
| **3. Pre-commit** | Month 2 | Enable FF-05 (secret scanning) as pre-commit hook. This is the least disruptive function with the highest security value. | FF-05 blocking |
| **4. CI gates** | Month 3 | Enable FF-01 and FF-02 as CI blocking gates. Layer violations and circular dependencies are clear-cut -- zero tolerance. | FF-01, FF-02 blocking |
| **5. Full enforcement** | Month 4 | Enable FF-03, FF-04, FF-06. All fitness functions now enforce. Evolving thresholds (FF-04) start at current baseline + 10% buffer. | All blocking |
| **6. Tighten** | Quarterly | Review thresholds. Tighten FF-04 coupling limit. Review p95 SLA targets. Assess whether new architecture decisions need new fitness functions. | Continuous improvement |

## Team Communication Template

Share this with the development team when rolling out fitness functions:

> **What's changing:** We're adding automated architecture tests to our CI pipeline. These tests verify that our code follows the architecture decisions we made 6 months ago.
>
> **Why:** Without automation, architecture decisions erode over time. We've found that some of our original decisions are no longer reflected in the code. These tests prevent further drift.
>
> **Impact on you:** For the first month, these tests will only report -- they won't block your builds. Starting month 2, specific tests will become pipeline gates. We'll communicate before each test becomes blocking.
>
> **What if a test blocks my build?** The test failure message will explain which architecture rule was violated and point to the relevant ADR. Fix the violation or, if you believe the architecture decision should change, raise it in the architecture review meeting.
>
> **This is not about blame.** Existing violations were not caught because we didn't have automation. The goal is to prevent NEW violations going forward, not to punish past decisions.

## Architecture Erosion Risk Assessment

| Architecture Decision | Without Fitness Functions | With Fitness Functions |
|----------------------|------------------------|---------------------|
| Layered architecture | Developers bypass layers for "quick fixes." Within 6 months, 30% of requests bypass the service layer. Refactoring cost: weeks. | FF-01 catches every bypass on commit. Zero layer violations accumulate. |
| No circular dependencies | Circular deps creep in as features span packages. Build times increase, testing becomes coupled. Discovered during performance investigation. | FF-02 catches cycles immediately. Clean dependency graph maintained. |
| API response SLAs | Slow queries accumulate. p99 degrades from 200ms to 2s over months. Discovered during customer complaints. | FF-03 alerts within 5 minutes of SLA breach. Issue fixed before customers notice. |
| Component coupling | Packages grow increasingly coupled. Changes in one package break 5 others. Discovered during a routine feature change that takes 3 days instead of 3 hours. | FF-04 prevents coupling growth. Packages stay within Ce limit. |
| No plaintext secrets | A developer commits an API key. It sits in git history for months before a security audit finds it. Key rotation required. | FF-05 blocks the commit. Secret never enters version control. |
