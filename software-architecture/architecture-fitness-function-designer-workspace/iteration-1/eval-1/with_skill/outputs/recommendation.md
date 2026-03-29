# Fitness Function Governance Report: Spring Boot Microservices

## Governance Scope
- **Date:** 2026-03-27
- **Architecture characteristics governed:** Scalability, Deployability, Testability
- **Technology stack:** Java / Spring Boot
- **CI/CD pipeline:** Jenkins

## Characteristic Inventory

| Characteristic | Category | Current State | Risk if Undetected |
|---------------|----------|---------------|-------------------|
| Scalability | Operational | Unknown - no load testing | High - system fails under traffic spikes, user-facing outage |
| Deployability | Process | Manual deploys assumed | Medium - slow deploys reduce agility, increase risk per release |
| Testability | Structural + Process | Unknown coverage | High - untestable code accumulates, bugs reach production |

## Fitness Function Inventory

| ID | Characteristic | Fitness Function | Threshold | Scope | Cadence | Nature | Automation | Temporality |
|----|---------------|-----------------|-----------|-------|---------|--------|------------|-------------|
| FF-01 | Testability | Cyclomatic complexity gate | CC < 10 per method | Atomic | Triggered | Static | Automated | Evolving |
| FF-02 | Testability | Test coverage gate | > 80% service layer, > 60% overall | Atomic | Triggered | Static | Automated | Evolving |
| FF-03 | Testability | Layer dependency enforcement | Zero violations | Atomic | Triggered | Static | Automated | Fixed |
| FF-04 | Scalability | Response time under load | p95 < 200ms at 2x baseline | Atomic | Triggered | Dynamic | Automated | Fixed |
| FF-05 | Scalability | Scalability degradation | < 20% p95 increase at 2x load | Holistic | Triggered | Dynamic | Automated | Fixed |
| FF-06 | Deployability | Build + deploy time | < 15 minutes total | Atomic | Triggered | Dynamic | Automated | Evolving |
| FF-07 | Deployability | Zero-downtime deployment verification | Zero failed health checks during deploy | Holistic | Triggered | Dynamic | Automated | Fixed |
| FF-08 | All (composite) | Architecture agility score | > 0.7 composite | Holistic | Triggered | Static | Automated | Evolving |

## Implementation Details

### FF-01: Cyclomatic Complexity Gate
- **Protects:** Testability
- **Threshold:** No method may exceed CC of 10 (evolving: start at CC < 20 for month 1-3, tighten to CC < 15 months 4-6, target CC < 10 by month 7+)
- **Classification:** Atomic / Triggered (on commit) / Static / Automated / Evolving
- **Implementation:** PMD rule in Maven build
  ```xml
  <!-- pom.xml PMD plugin config -->
  <rule ref="category/java/design.xml/CyclomaticComplexity">
    <properties>
      <property name="methodReportLevel" value="10"/>
    </properties>
  </rule>
  ```
- **Integration point:** CI build stage (runs on every push)
- **Failure action:** Block pipeline, report offending methods with CC values
- **WHY CC < 10:** Functions with CC > 10 have more than 10 independent paths through code. Each path requires a separate test case. Beyond 10, testing becomes impractical and bugs hide in untested paths. Beyond 50, the function is literally untestable -- the combinatorial explosion of paths makes comprehensive testing impossible.

### FF-02: Test Coverage Gate
- **Protects:** Testability
- **Threshold:** > 80% line coverage for `src/main/java/**/service/**`, > 60% overall, > 80% diff coverage on new code
- **Classification:** Atomic / Triggered / Static / Automated / Evolving
- **Implementation:** JaCoCo with Jenkins coverage plugin
  ```xml
  <!-- pom.xml JaCoCo config -->
  <plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <configuration>
      <rules>
        <rule>
          <element>BUNDLE</element>
          <limits>
            <limit>
              <counter>LINE</counter>
              <value>COVEREDRATIO</value>
              <minimum>0.60</minimum>
            </limit>
          </limits>
        </rule>
      </rules>
    </configuration>
  </plugin>
  ```
- **Integration point:** CI test stage
- **Failure action:** Block pipeline

### FF-03: Layer Dependency Enforcement
- **Protects:** Testability (structural modularity enables isolated testing)
- **Threshold:** Zero layer violations
- **Classification:** Atomic / Triggered / Static / Automated / Fixed
- **Implementation:** ArchUnit test class
  ```java
  @AnalyzeClasses(packages = "com.myapp")
  public class LayerDependencyTest {

      @ArchTest
      static final ArchRule services_should_not_depend_on_controllers =
          noClasses().that().resideInAPackage("..service..")
              .should().dependOnClassesThat().resideInAPackage("..controller..");

      @ArchTest
      static final ArchRule repositories_should_not_depend_on_services =
          noClasses().that().resideInAPackage("..repository..")
              .should().dependOnClassesThat().resideInAPackage("..service..");

      @ArchTest
      static final ArchRule no_circular_dependencies =
          slices().matching("com.myapp.(*)..").should().beFreeOfCycles();
  }
  ```
- **Integration point:** CI test stage (runs with unit tests)
- **Failure action:** Block pipeline
- **WHY zero tolerance:** Layer violations are binary -- either the architecture is enforced or it isn't. Allowing "a few" violations creates a broken window effect where developers assume the boundary is optional. ArchUnit runs in milliseconds, so there is no performance cost to strict enforcement.

### FF-04: Response Time Under Load
- **Protects:** Scalability
- **Threshold:** p95 response time < 200ms at 2x baseline load
- **Classification:** Atomic / Triggered (pre-release) / Dynamic / Automated / Fixed
- **Implementation:** k6 load test script
  ```javascript
  import http from 'k6/http';
  import { check, sleep } from 'k6';

  export const options = {
    stages: [
      { duration: '2m', target: 100 },   // baseline
      { duration: '5m', target: 200 },   // 2x load
      { duration: '2m', target: 0 },     // ramp down
    ],
    thresholds: {
      'http_req_duration{scenario:default}': ['p(95)<200'],
      'http_req_duration{scenario:default}': ['p(99)<500'],
    },
  };

  export default function () {
    const res = http.get('http://staging:8080/api/orders');
    check(res, { 'status is 200': (r) => r.status === 200 });
    sleep(1);
  }
  ```
- **Integration point:** Staging environment, after deployment to staging
- **Failure action:** Block promotion to production
- **WHY p95 not average:** An average response time of 80ms can hide a p99 of 5000ms, meaning 1% of users experience unacceptable delays. Latency distributions are always long-tailed. p95 ensures that 95% of users have an acceptable experience.

### FF-05: Scalability Degradation
- **Protects:** Scalability
- **Threshold:** p95 at 2x load must be < 120% of p95 at baseline load
- **Classification:** Holistic / Triggered / Dynamic / Automated / Fixed
- **Implementation:** k6 with custom metric comparison
- **Integration point:** Staging, pre-release gate
- **Failure action:** Block promotion, alert architecture team
- **WHY holistic:** This function tests the relationship between load and performance -- a property that emerges from the interaction of multiple components, not a single service.

### FF-06: Build + Deploy Time
- **Protects:** Deployability
- **Threshold:** Total pipeline time < 15 minutes (evolving: start at 30 min, tighten quarterly)
- **Classification:** Atomic / Triggered / Dynamic / Automated / Evolving
- **Implementation:** Jenkins pipeline duration tracking
- **Integration point:** Meta-monitoring of the pipeline itself
- **Failure action:** Alert (non-blocking), trigger investigation

### FF-07: Zero-Downtime Deployment Verification
- **Protects:** Deployability
- **Threshold:** Zero HTTP 503 responses during rolling deployment
- **Classification:** Holistic / Triggered / Dynamic / Automated / Fixed
- **Implementation:** Health check polling during deployment with readiness probe verification
- **Integration point:** Deployment stage
- **Failure action:** Automatic rollback

### FF-08: Architecture Agility Composite Score
- **Protects:** Overall architecture health
- **Threshold:** Composite score > 0.7
- **Formula:**
  ```
  agility_score = (
      cc_compliance * 0.25 +        # % of methods with CC < 10
      test_coverage * 0.25 +         # normalized coverage ratio
      deploy_success_rate * 0.25 +   # % of deploys without rollback
      layer_compliance * 0.25        # % of ArchUnit rules passing
  )
  ```
- **Classification:** Holistic / Triggered / Static / Automated / Evolving
- **Integration point:** Weekly report
- **Failure action:** Architecture review meeting trigger

## Integration Map

```
Developer Workstation          Jenkins CI Pipeline              Staging                Production
├── Pre-commit                 ├── Build Stage                  ├── Post-deploy          ├── Continuous
│   └── (none yet)             │   └── FF-01: CC gate           │   └── FF-04: k6 load   │   └── FF-04: p95
├── Pre-push                   ├── Test Stage                   │   └── FF-05: Degrade    │       monitoring
│   └── (none yet)             │   └── FF-02: Coverage gate     │   └── FF-07: Zero-DT    │
                               │   └── FF-03: ArchUnit layers   │                         │
                               ├── Quality Gate                 │                         │
                               │   └── FF-08: Agility score     │                         │
                               ├── Deploy to Staging             │                         │
                               │   └── FF-06: Time check        │                         │
```

## Temporal Evolution Plan

| Phase | Timeline | Changes |
|-------|----------|---------|
| **Baseline** | Weeks 1-2 | Deploy FF-01 through FF-03 in reporting-only mode. Measure current CC distribution, coverage, and layer violations. |
| **Awareness** | Weeks 3-4 | Share baseline report with team. Agree on initial thresholds. FF-01 starts at CC < 20. |
| **Soft enforcement** | Month 2 | FF-01, FF-02, FF-03 block pipeline. FF-04/FF-05 run in staging but report-only. |
| **Full enforcement** | Month 3 | All fitness functions enforce. FF-06, FF-07 added. |
| **Tighten** | Month 4-6 | FF-01 tightens to CC < 15. FF-02 raises to 85% service coverage. |
| **Target** | Month 7+ | FF-01 at CC < 10. FF-08 composite score enforced. Add chaos engineering in staging. |

## Architecture Erosion Risk Assessment

| Risk | Without Fitness Functions | With Fitness Functions |
|------|------------------------|---------------------|
| Service layer bypasses repository pattern | Undetected until refactoring becomes impossible | Caught immediately by FF-03 (ArchUnit) in CI |
| Complex methods accumulate | Found during incident postmortem | Caught by FF-01 (CC gate) on every commit |
| Test coverage erodes as deadlines approach | Discovered when bugs reach production | Caught by FF-02 (coverage gate) on every PR |
| Response time degrades under load | Discovered during traffic spike (production outage) | Caught by FF-04/FF-05 in staging before release |
| Deployments cause downtime | Users report outages | Caught by FF-07 (zero-downtime check) during deploy |
