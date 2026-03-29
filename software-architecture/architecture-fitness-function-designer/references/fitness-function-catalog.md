# Fitness Function Catalog

Reference catalog of fitness function types, implementations, and examples organized by architecture characteristic category. Read this file when you need specific implementation details for a fitness function type.

## Classification Dimensions

Every fitness function is classified along five dimensions. This table provides the full taxonomy:

| Dimension | Option A | Option B | Decision Factor |
|-----------|----------|----------|-----------------|
| **Scope** | Atomic (single characteristic) | Holistic (multiple characteristics) | Does the check involve trade-offs between characteristics? |
| **Cadence** | Triggered (on event) | Continuous (always running) | Can you afford to wait for an event, or must violations be caught immediately? |
| **Nature** | Static (no execution) | Dynamic (requires running system) | Does the check need runtime behavior or just code analysis? |
| **Automation** | Automated (machine evaluates) | Manual (human evaluates) | Can the pass/fail criteria be expressed as a machine-readable rule? |
| **Temporality** | Fixed (constant threshold) | Evolving (threshold changes over time) | Is the target state known, or is the team incrementally improving? |

## Structural Fitness Functions

Structural fitness functions verify code organization and design rules at build time. They are the easiest to implement and the most cost-effective governance mechanism.

### Layer Dependency Enforcement

**Protects:** Modularity, maintainability
**Classification:** Atomic / Triggered / Static / Automated / Fixed
**Threshold:** Zero violations (any layer bypass = failure)

**Java/Kotlin (ArchUnit):**
```java
import com.tngtech.archunit.lang.ArchRule;
import static com.tngtech.archunit.lang.syntax.ArchRuleDefinition.noClasses;

@ArchTest
static final ArchRule services_should_not_access_controllers =
    noClasses().that().resideInAPackage("..service..")
        .should().dependOnClassesThat().resideInAPackage("..controller..");

@ArchTest
static final ArchRule controllers_should_not_access_repositories =
    noClasses().that().resideInAPackage("..controller..")
        .should().dependOnClassesThat().resideInAPackage("..repository..");
```

**C# (.NET with NetArchTest):**
```csharp
var result = Types.InAssembly(typeof(ServiceClass).Assembly)
    .That().ResideInNamespace("Services")
    .ShouldNot().HaveDependencyOn("Controllers")
    .GetResult();
Assert.True(result.IsSuccessful);
```

**Python (custom with importlib or AST):**
```python
import ast, os

def check_no_controller_imports_in_services(service_dir):
    violations = []
    for root, _, files in os.walk(service_dir):
        for f in files:
            if f.endswith('.py'):
                tree = ast.parse(open(os.path.join(root, f)).read())
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if 'controller' in alias.name:
                                violations.append(f"{f}: imports {alias.name}")
    assert len(violations) == 0, f"Layer violations: {violations}"
```

### Cyclomatic Complexity Thresholds

**Protects:** Testability, maintainability
**Classification:** Atomic / Triggered / Static / Automated / Evolving
**Thresholds:**

| CC Score | Risk Level | Action |
|:--------:|-----------|--------|
| 1-10 | Low risk | No action needed |
| 11-20 | Moderate risk | Flag for review, refactor when touched |
| 21-50 | High risk | Must refactor before next release |
| 51+ | Untestable | Block pipeline, immediate refactoring required |

**Implementation:** Integrate into CI with language-specific tools:
- Java: PMD, SonarQube, Checkstyle
- Python: radon, flake8 with mccabe plugin
- JavaScript/TypeScript: ESLint complexity rule
- C#: NDepend, SonarQube
- Go: gocyclo

**Evolving threshold example:**
```
Month 1-3:  Block on CC > 50 (catch only untestable code)
Month 4-6:  Block on CC > 30 (start driving improvement)
Month 7-12: Block on CC > 15 (approach target)
Month 12+:  Block on CC > 10 (target state)
```

### No Circular Dependencies

**Protects:** Modularity, deployability
**Classification:** Atomic / Triggered / Static / Automated / Fixed
**Threshold:** Zero circular dependencies between packages/modules

**Java (ArchUnit):**
```java
@ArchTest
static final ArchRule no_cycles =
    slices().matching("com.myapp.(*)..").should().beFreeOfCycles();
```

**Any language (custom):** Build a dependency graph from imports and run a topological sort. If the sort fails, circular dependencies exist.

### Package Access Rules

**Protects:** Encapsulation, modularity
**Classification:** Atomic / Triggered / Static / Automated / Fixed

**Java (ArchUnit) - microservice database isolation:**
```java
@ArchTest
static final ArchRule order_service_uses_only_order_db =
    classes().that().resideInAPackage("..order.repository..")
        .should().onlyAccessClassesThat()
        .resideInAnyPackage("..order..", "java..", "javax..", "org.springframework..");
```

### Component Size Budgets

**Protects:** Maintainability, modularity
**Classification:** Atomic / Triggered / Static / Automated / Evolving
**Thresholds:**
- Maximum lines per file: 500 (recommend 300)
- Maximum methods per class: 20
- Maximum parameters per method: 5
- Maximum depth of inheritance: 4

## Operational Fitness Functions

Operational fitness functions verify runtime behavior. They require a running system and are typically more expensive to implement.

### Response Time Percentiles

**Protects:** Performance, user experience
**Classification:** Atomic / Continuous / Dynamic / Automated / Fixed
**Thresholds (typical web application):**

| Percentile | Threshold | Why This Percentile |
|:----------:|:---------:|---------------------|
| p50 | < 100ms | Median user experience |
| p95 | < 200ms | 95% of users have acceptable experience |
| p99 | < 500ms | Even tail users are not abandoned |
| max | < 2000ms | No request should feel broken |

**Why percentiles, not averages:** A service with average response time of 80ms could have p99 of 5000ms. This means 1% of users (potentially thousands per hour) experience 5-second delays. Averages are statistically meaningless for latency distributions, which are always long-tailed. Always use p95 or p99.

**Implementation:**
- Prometheus + Grafana with histogram metrics and alert rules
- Datadog APM with SLO monitors
- Custom: log response times, compute percentiles, alert on threshold breach

### Scalability Under Load

**Protects:** Scalability
**Classification:** Holistic / Triggered / Dynamic / Automated / Evolving
**Threshold:** Response time degradation < 20% under 2x load, < 50% under 5x load

**Implementation:**
- k6, Gatling, or Locust load test suites running in staging
- Compare p95 at baseline load vs 2x/5x load
- Fail the pipeline if degradation exceeds threshold

### Chaos Engineering (Netflix Simian Army Model)

**Protects:** Resilience, fault tolerance, recoverability
**Classification:** Holistic / Continuous / Dynamic / Automated / Fixed
**Threshold:** System maintains availability SLA during injected failures

The Netflix Simian Army pioneered the concept of using controlled failure injection as a fitness function:

| Tool | What It Tests | Blast Radius |
|------|--------------|--------------|
| Chaos Monkey | Random instance termination | Single instance |
| Latency Monkey | Artificial network delays | Single service |
| Conformity Monkey | Best practice compliance | Configuration |
| Security Monkey | Security configuration | Vulnerability |
| Janitor Monkey | Unused resource cleanup | Cost optimization |

**Key principle:** If your architecture claims to be resilient, prove it by breaking things. A resilience characteristic without chaos testing is an untested assumption.

**Implementation levels:**
1. **Starter:** Kill random test environment instances, verify auto-recovery
2. **Intermediate:** Inject latency between services in staging, verify graceful degradation
3. **Advanced:** Run Chaos Monkey in production during business hours with blast radius controls

### Availability Monitoring

**Protects:** Availability
**Classification:** Atomic / Continuous / Dynamic / Automated / Fixed
**Threshold:** Based on SLA tier:

| SLA | Annual Downtime | Monthly Downtime |
|:---:|:--------------:|:---------------:|
| 99% | 3.65 days | 7.3 hours |
| 99.9% | 8.76 hours | 43.8 minutes |
| 99.95% | 4.38 hours | 21.9 minutes |
| 99.99% | 52.56 minutes | 4.38 minutes |

## Process Fitness Functions

Process fitness functions verify development workflow health. They govern how the team builds software, not just what it builds.

### Test Coverage Gates

**Protects:** Testability
**Classification:** Atomic / Triggered / Static / Automated / Evolving
**Thresholds:**
- Overall coverage: > 70% (minimum viable)
- Service/business logic layer: > 85%
- Critical paths (payment, authentication): > 95%
- New code (diff coverage): > 80%

### Deployment Pipeline Metrics

**Protects:** Deployability
**Classification:** Holistic / Continuous / Dynamic / Automated / Evolving
**Metrics (from DORA):**

| Metric | Elite | High | Medium | Low |
|--------|:-----:|:----:|:------:|:---:|
| Deploy frequency | Multiple/day | Weekly-monthly | Monthly-biannually | Biannually+ |
| Change lead time | < 1 hour | 1 day - 1 week | 1 week - 1 month | 1-6 months |
| Change failure rate | 0-15% | 16-30% | 16-30% | 46-60% |
| MTTR | < 1 hour | < 1 day | < 1 day | 1 week - 1 month |

### Architecture Decision Compliance

**Protects:** All characteristics (meta-governance)
**Classification:** Holistic / Triggered / Static / Manual (with automation support) / Fixed

For each ADR, create a corresponding fitness function:
- ADR says "use event-driven for inter-service communication" -> fitness function scans for synchronous cross-service REST calls
- ADR says "all data at rest must be encrypted" -> fitness function scans database configs for encryption settings
- ADR says "maximum 3 layers of service dependency" -> fitness function analyzes the service dependency graph depth

## Composite Fitness Functions

Some characteristics cannot be measured by a single metric. Composite fitness functions combine multiple measurements:

### Agility Composite

Agility = testability + deployability + modularity

```
agility_score = (
    test_coverage_percentage * 0.3 +
    deploy_frequency_score * 0.3 +
    modularity_distance_from_main_sequence * 0.4
)
threshold: agility_score > 0.7
```

### Process Measure Composite (from the book)

Process measures like testability and deployability are composite by nature:

```
process_health = (
    cyclomatic_complexity_compliance +   # % of functions with CC < 10
    test_coverage +                       # overall test coverage %
    deployment_success_rate +             # % of deploys without rollback
    change_lead_time_score                # normalized 0-1
) / 4

threshold: process_health > 0.75
```

## Anti-Patterns in Fitness Function Design

| Anti-Pattern | Description | Correction |
|-------------|-------------|------------|
| **All-or-nothing** | Setting perfect thresholds day one, causing mass failures | Start permissive, tighten over time (temporal) |
| **Noise factory** | Too many fitness functions generating constant warnings | Prioritize by risk; only block on critical violations |
| **Cargo cult** | Copying fitness functions from another team without adapting | Each function must protect a specific characteristic YOU care about |
| **Test theater** | Fitness functions that always pass (thresholds too loose) | Thresholds must be tight enough to catch real violations |
| **Pipeline blocker** | Dynamic tests on every commit, slowing development | Match function to appropriate lifecycle stage |

## Fitness Function Evolution Roadmap Template

| Phase | Duration | Focus | Actions |
|-------|----------|-------|---------|
| **Baseline** | Weeks 1-2 | Measure current state | Deploy all fitness functions in reporting-only mode |
| **Awareness** | Weeks 3-4 | Team alignment | Share reports, discuss violations, agree on thresholds |
| **Warning** | Months 2-3 | Soft enforcement | Fitness functions warn but don't block |
| **Enforcement** | Month 4+ | Hard governance | Fitness functions block pipeline on violation |
| **Tightening** | Quarterly | Continuous improvement | Review and tighten thresholds each quarter |
