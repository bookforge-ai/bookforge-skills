# Fitness Function Governance Report: Cross-Database Dependency Enforcement

## Governance Scope
- **Date:** 2026-03-27
- **Architecture characteristic governed:** Data isolation (structural integrity of microservice boundaries)
- **Architecture decision:** "No service should directly depend on another service's database"
- **Technology stack:** Kotlin / Spring Boot (8 microservices)
- **Risk if violated:** Tight coupling between services via shared database access creates a distributed monolith -- changes to one service's schema break other services, independent deployability is lost, and the primary benefit of microservices is negated.

## Characteristic Analysis

This architecture decision protects multiple characteristics simultaneously:

| Characteristic | How Database Isolation Protects It |
|---------------|-----------------------------------|
| Deployability | Each service can evolve its schema independently without coordinating with other services |
| Modularity | Data ownership boundaries enforce clean service boundaries |
| Fault tolerance | One service's database failure doesn't cascade to other services |
| Scalability | Each database can be scaled independently based on service load |

## Fitness Function Inventory

| ID | Fitness Function | Threshold | Scope | Cadence | Nature | Automation |
|----|-----------------|-----------|-------|---------|--------|------------|
| FF-01 | Package-to-schema ArchUnit rule | Zero violations | Atomic | Triggered | Static | Automated |
| FF-02 | Connection string isolation check | Each service config references only its own DB | Atomic | Triggered | Static | Automated |
| FF-03 | Cross-service query detection | Zero cross-schema queries in SQL logs | Holistic | Continuous | Dynamic | Automated |
| FF-04 | Database user permission audit | Each service user has access to only its own schema | Atomic | Triggered | Static | Automated |

## Implementation Details

### FF-01: Package-to-Schema ArchUnit Rule

**Protects:** Data isolation at the code level
**Classification:** Atomic / Triggered (on commit) / Static / Automated / Fixed
**Threshold:** Zero violations -- any repository class that references another service's entities fails the build.

```kotlin
// src/test/kotlin/com/myapp/architecture/DatabaseIsolationTest.kt

@AnalyzeClasses(packages = ["com.myapp"])
class DatabaseIsolationTest {

    @ArchTest
    val order_repositories_only_access_order_entities: ArchRule =
        classes().that().resideInAPackage("..order.repository..")
            .should().onlyAccessClassesThat()
            .resideInAnyPackage(
                "..order..",
                "kotlin..",
                "java..",
                "javax..",
                "org.springframework..",
                "org.jetbrains.."
            )

    @ArchTest
    val payment_repositories_only_access_payment_entities: ArchRule =
        classes().that().resideInAPackage("..payment.repository..")
            .should().onlyAccessClassesThat()
            .resideInAnyPackage(
                "..payment..",
                "kotlin..",
                "java..",
                "javax..",
                "org.springframework..",
                "org.jetbrains.."
            )

    // Repeat for all 8 services, or use a parameterized approach:
    companion object {
        val SERVICE_PACKAGES = listOf(
            "order", "payment", "inventory", "shipping",
            "notification", "user", "catalog", "analytics"
        )
    }

    @ArchTest
    val no_cross_service_entity_access: ArchRule =
        slices().matching("com.myapp.(*).repository..")
            .should().notDependOnEachOther()
}
```

**Integration point:** CI test stage (runs with unit tests in < 5 seconds)
**Failure action:** Block pipeline immediately
**WHY zero tolerance:** Database isolation is binary. Allowing "just one" cross-service query creates a precedent that erodes the boundary over time. ArchUnit catches violations at compile time with zero runtime cost.

### FF-02: Connection String Isolation Check

**Protects:** Data isolation at the configuration level
**Classification:** Atomic / Triggered (on commit) / Static / Automated / Fixed
**Threshold:** Each service's `application.yml` must reference only its own database.

```kotlin
// src/test/kotlin/com/myapp/architecture/ConfigIsolationTest.kt

@SpringBootTest
class ConfigIsolationTest {

    @Value("\${spring.datasource.url}")
    lateinit var datasourceUrl: String

    @Value("\${spring.application.name}")
    lateinit var serviceName: String

    @Test
    fun `datasource URL must reference own service database`() {
        // Each service's DB URL must contain the service name
        // e.g., order-service -> jdbc:postgresql://db:5432/order_db
        val expectedDbPattern = serviceName.replace("-service", "")
        assertTrue(
            datasourceUrl.contains(expectedDbPattern),
            "Service '$serviceName' is connecting to wrong database: $datasourceUrl"
        )
    }
}
```

**Alternative (CI script approach):**
```bash
#!/bin/bash
# check-db-isolation.sh - runs in CI for each service
for service_dir in services/*/; do
    service_name=$(basename "$service_dir" | sed 's/-service//')
    db_url=$(grep "datasource.url" "$service_dir/src/main/resources/application.yml")
    if ! echo "$db_url" | grep -q "${service_name}"; then
        echo "VIOLATION: $service_dir connects to wrong database: $db_url"
        exit 1
    fi
done
```

**Integration point:** CI build stage
**Failure action:** Block pipeline

### FF-03: Cross-Service Query Detection

**Protects:** Data isolation at runtime
**Classification:** Holistic / Continuous / Dynamic / Automated / Fixed
**Threshold:** Zero queries from any service accessing another service's schema.

**Implementation:**
1. Enable SQL query logging in staging/production
2. Tag each query with the originating service (via MDC or connection pool metadata)
3. Create an alert rule:
   ```
   ALERT CrossServiceDatabaseAccess
   IF count(sql_queries{source_service!="schema_owner"}) > 0
   FOR 1m
   LABELS { severity = "critical" }
   ANNOTATIONS { summary = "Service {{ $labels.source_service }} queried schema owned by {{ $labels.schema_owner }}" }
   ```

**Integration point:** Continuous in staging and production
**Failure action:** Alert architecture team immediately (Slack/PagerDuty)
**WHY continuous:** Static analysis catches direct code references, but developers might use dynamic SQL, native queries, or JDBC templates that bypass compile-time detection. Runtime monitoring is the safety net.

### FF-04: Database User Permission Audit

**Protects:** Data isolation at the infrastructure level
**Classification:** Atomic / Triggered (weekly) / Static / Automated / Fixed
**Threshold:** Each database user has GRANT only on its own schema.

```sql
-- audit-db-permissions.sql
-- Run weekly, fail if any cross-schema grants exist
SELECT grantee, table_schema, privilege_type
FROM information_schema.role_table_grants
WHERE grantee LIKE '%_service'
  AND table_schema != REPLACE(grantee, '_service', '_schema')
ORDER BY grantee, table_schema;
-- Result must be empty (zero rows)
```

**Integration point:** Scheduled CI job (weekly)
**Failure action:** Alert infrastructure team

## Integration Map

```
Developer Workstation       CI Pipeline (every push)       Staging/Production
                            ├── Build Stage                ├── Continuous
                            │   └── FF-02: Config check    │   └── FF-03: Query monitor
                            ├── Test Stage                 │
                            │   └── FF-01: ArchUnit        │
                            │   └── FF-02: Spring test     │
                            ├── Weekly Scheduled           │
                            │   └── FF-04: DB permissions  │
```

## Defense in Depth

This design applies four layers of enforcement for one architecture decision:

| Layer | FF | Catches | When |
|-------|-----|---------|------|
| Code structure | FF-01 | Direct entity/repository references | Build time |
| Configuration | FF-02 | Wrong connection strings | Build time |
| Runtime behavior | FF-03 | Dynamic SQL, native queries | Runtime |
| Infrastructure | FF-04 | Database permission drift | Weekly audit |

**WHY defense in depth:** No single check catches all violations. ArchUnit misses native SQL queries. Config checks miss programmatic connection creation. Runtime monitoring misses violations in untested code paths. The four layers together provide comprehensive coverage. This mirrors the security principle of defense in depth -- assume each layer has gaps and compensate with the next.

## Architecture Erosion Risk Assessment

| Risk | Without Fitness Functions | With Fitness Functions |
|------|------------------------|---------------------|
| Developer adds JPA entity referencing another service's table | Undetected until deployment breaks another service | Caught by FF-01 in CI within minutes |
| DevOps accidentally grants cross-schema permissions | Undetected until a developer exploits the permission | Caught by FF-04 in weekly audit |
| Native SQL query accesses another service's table | Undetected until production data inconsistency | Caught by FF-03 in staging/production monitoring |
| New service copy-pastes config with wrong DB URL | Undetected until the service reads stale data | Caught by FF-02 in CI build stage |
