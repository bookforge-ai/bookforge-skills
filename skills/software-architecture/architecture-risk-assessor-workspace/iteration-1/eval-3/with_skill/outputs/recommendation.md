# Architecture Risk Assessment: COBOL Banking System Cloud Migration

## Assessment Scope
- **Date:** 2026-03-27
- **Assessed by:** AI Architecture Risk Assessor (with skill)
- **Architecture style:** Migration from monolithic mainframe (COBOL) to cloud-native distributed architecture
- **Components assessed:** 5 (migration-phase components)
- **Risk criteria:** Scalability, Availability, Performance, Security, Data Integrity + Migration-specific: Operational Continuity
- **Critical context:** 2M transactions/day, downtime costs $50,000/minute

## Architecture Components
1. **Transaction Processing Engine** — Core transaction handling (currently COBOL batch + online, migrating to cloud services)
2. **Data Migration Pipeline** — ETL pipeline moving data from mainframe DB to cloud database
3. **Legacy Integration Layer** — Bridge/strangler fig layer connecting old and new systems during migration
4. **Cloud Database Cluster** — New cloud-native database receiving migrated data and handling new transactions
5. **API Gateway / Service Mesh** — New entry point routing traffic between legacy and cloud services

## Full Risk Assessment

| Risk Criteria          | Transaction Engine | Data Migration     | Legacy Integration | Cloud Database     | API Gateway        | Total |
|------------------------|--------------------|--------------------|--------------------|--------------------|--------------------| ------|
| Scalability            | 4 (M) =           | 3 (M) =           | 6 (H) -           | 3 (M) =           | 4 (M) =           | 20    |
| Availability           | 9 (H) =           | 4 (M) =           | 9 (H) -           | 6 (H) =           | 6 (H) =           | 34    |
| Performance            | 9 (H) -           | 3 (M) =           | 9 (H) -           | 4 (M) =           | 6 (H) =           | 31    |
| Security               | 6 (H) =           | 6 (H) =           | 9 (H) =           | 4 (M) =           | 6 (H) =           | 31    |
| Data Integrity         | 9 (H) =           | 9 (H) -           | 6 (H) -           | 6 (H) =           | 2 (L) =           | 32    |
| Operational Continuity | 9 (H) -           | 6 (H) =           | 9 (H) -           | 4 (M) =           | 4 (M) =           | 32    |
| **Total**              | **46**             | **31**             | **48**             | **27**             | **28**             |       |

### Scoring Key
- Score = Impact (1-3) x Likelihood (1-3)
- Low (L): 1-2 | Medium (M): 3-4 | High (H): 6-9
- Direction: + improving, - worsening, = stable
- **Custom criterion:** Operational Continuity — risk that the migration disrupts the 2M daily transactions

## High-Risk Summary (Filtered View)

| Risk Criteria          | Transaction Engine | Data Migration     | Legacy Integration | Cloud Database     | API Gateway        |
|------------------------|--------------------|--------------------|--------------------|--------------------|--------------------|
| Scalability            | .                  | .                  | 6 (H) -           | .                  | .                  |
| Availability           | 9 (H) =           | .                  | 9 (H) -           | 6 (H) =           | 6 (H) =           |
| Performance            | 9 (H) -           | .                  | 9 (H) -           | .                  | 6 (H) =           |
| Security               | 6 (H) =           | 6 (H) =           | 9 (H) =           | .                  | 6 (H) =           |
| Data Integrity         | 9 (H) =           | 9 (H) -           | 6 (H) -           | 6 (H) =           | .                  |
| Operational Continuity | 9 (H) -           | 6 (H) =           | 9 (H) -           | .                  | .                  |

**18 of 30 cells are high-risk.** This is an extremely high-risk migration. Every component except the API Gateway has multiple high-risk scores.

## Risk Details and Mitigations

### Transaction Processing Engine — Availability (Score: 9)
- **Impact (3):** Every minute of transaction engine downtime costs $50,000. At 2M transactions/day, that's ~1,389 transactions/minute. Any interruption is catastrophic.
- **Likelihood (3):** COBOL-to-cloud migration of core transaction processing is one of the highest-risk activities in banking. Functional equivalence is extremely difficult to verify — COBOL systems accumulate decades of undocumented business rules.
- **Direction:** = (risk has always been this high, migration hasn't started yet)
- **Mitigation:** Use the **Strangler Fig pattern** exclusively. Never do a "big bang" cutover. Route transactions one category at a time from legacy to cloud. Each category must run in parallel (dual-write) for minimum 30 days with automated comparison before cutting over. Build an automated rollback mechanism with <60 second activation.
- **Post-mitigation estimate:** 6 (impact stays 3 — downtime cost doesn't change; likelihood drops to 2 with strangler fig + parallel run)

### Transaction Processing Engine — Performance (Score: 9)
- **Impact (3):** COBOL on mainframe processes transactions in milliseconds with decades of optimization. Cloud services must match this latency or risk SLA violations and regulatory non-compliance.
- **Likelihood (3):** Extremely high. Mainframe COBOL is optimized for batch and OLTP at a level that cloud services rarely match out of the box. Network hops, serialization overhead, and distributed coordination all add latency that doesn't exist in the monolith.
- **Direction:** - (worsening — as more transaction types move to cloud, performance risk increases)
- **Mitigation:** Performance benchmark EVERY transaction type on cloud before migrating it. Set explicit latency budgets per transaction type based on current mainframe performance. Use in-memory databases (Redis, Hazelcast) for hot data. Consider co-located cloud services (same availability zone, same VPC) to minimize network latency. Accept that some transaction types (high-frequency batch) may need to stay on mainframe longer.
- **Post-mitigation estimate:** 6 (impact stays 3, likelihood stays 2 — this remains a high-risk area even with mitigation)

### Transaction Processing Engine — Data Integrity (Score: 9)
- **Impact (3):** Corrupted or lost financial transactions = regulatory violation, customer financial harm, potential bank charter risk.
- **Likelihood (3):** COBOL business logic has evolved over decades with implicit rules, edge cases, and workarounds that may not be documented. Re-implementing this logic guarantees some discrepancies that manifest as data integrity issues.
- **Direction:** = (inherent risk of any legacy migration)
- **Mitigation:** Implement comprehensive transaction reconciliation: every transaction processed by the cloud system is independently verified against what the legacy system would have produced (shadow mode). Automated discrepancy detection with <5 minute alerting. Build a "golden dataset" of 10,000+ representative transactions with known correct outputs for regression testing.
- **Post-mitigation estimate:** 6 (impact stays 3, likelihood drops to 2 with shadow mode + reconciliation)

### Transaction Processing Engine — Operational Continuity (Score: 9)
- **Impact (3):** Migration disrupts the core revenue-generating system. At $50K/minute, even brief disruptions are unacceptable.
- **Likelihood (3):** Mainframe-to-cloud migrations in banking have a documented high failure rate. The complexity of maintaining dual operations while migrating is extreme.
- **Direction:** - (risk increases as migration progresses and more load moves to cloud)
- **Mitigation:** Phase the migration over 18-24 months minimum. Start with the lowest-risk transaction types (informational queries, balance checks) before touching financial transactions. Maintain full mainframe capacity throughout — do not decommission any mainframe capacity until the corresponding cloud service has proven stable for 90+ days in production. Build organizational muscle for rollback — practice it quarterly.
- **Post-mitigation estimate:** 6 (impact stays 3, likelihood drops to 2 with phased approach)

### Legacy Integration Layer — Availability (Score: 9)
- **Impact (3):** The integration layer is the bridge between old and new. If it fails, BOTH systems lose the ability to function together, potentially halting all transactions.
- **Likelihood (3):** Integration layers in mainframe migrations are notoriously fragile. They must handle two different data formats, two different transaction protocols, two different error handling paradigms, and two different performance profiles simultaneously.
- **Direction:** - (worsening — complexity increases as more services migrate)
- **Mitigation:** Build the integration layer as a stateless, horizontally scalable service with no single point of failure. Implement circuit breakers in both directions (legacy-to-cloud and cloud-to-legacy). Design for independent operation: if the bridge fails, each side should have a fallback mode. Test bridge failure scenarios explicitly in disaster recovery exercises.
- **Post-mitigation estimate:** 6 (impact stays 3, likelihood drops to 2)

### Legacy Integration Layer — Performance (Score: 9)
- **Impact (3):** The integration layer adds latency to EVERY transaction during the migration period. This is directly on the critical path for $50K/minute worth of transactions.
- **Likelihood (3):** Protocol translation (COBOL CICS/IMS to REST/gRPC), data format conversion (EBCDIC to UTF-8, packed decimal to JSON), and network hops between mainframe and cloud all add measurable latency.
- **Direction:** - (worsening — more transaction types through the bridge = more latency)
- **Mitigation:** Minimize bridge traversals — each transaction should go through the bridge at most once (not back and forth). Use binary protocols (gRPC, not REST) for bridge communication. Pre-compute data format conversions where possible. Set strict SLAs on bridge latency (<10ms overhead) and alert if exceeded.
- **Post-mitigation estimate:** 6 (impact 3, likelihood 2)

### Legacy Integration Layer — Security (Score: 9)
- **Impact (3):** The integration layer bridges two security models. Mainframe security (RACF/ACF2/Top Secret) and cloud security (IAM, mTLS) are fundamentally different. Any gap in translation is a vulnerability.
- **Likelihood (3):** Bridging two different security paradigms always introduces gaps. Authentication tokens must be translated, authorization models mapped, and audit trails maintained across both systems. This is where security breaches in migrations historically occur.
- **Direction:** = (inherent architectural risk)
- **Mitigation:** Implement a dedicated security translation layer within the bridge. All cross-boundary calls must be authenticated AND authorized on BOTH sides (not just one). Maintain unified audit trail across both systems. Engage a security auditor specializing in mainframe-to-cloud migrations. Conduct penetration testing specifically targeting the bridge.
- **Post-mitigation estimate:** 6 (impact 3, likelihood 2)

### Legacy Integration Layer — Operational Continuity (Score: 9)
- **Impact (3):** Bridge instability = transaction processing instability.
- **Likelihood (3):** The bridge must evolve as more services migrate. Each change to the bridge is a potential disruption to the $50K/minute transaction flow.
- **Direction:** - (each migration phase adds complexity to the bridge)
- **Mitigation:** Treat the bridge as the most critical component in the architecture. Dedicated team. Canary deployments with <1% traffic routing. Automated rollback on any error rate increase. Feature flags for each transaction type routing. Never deploy bridge changes during peak hours.
- **Post-mitigation estimate:** 6 (impact 3, likelihood 2)

### Data Migration Pipeline — Data Integrity (Score: 9)
- **Impact (3):** Incorrect data migration = every subsequent transaction on the cloud system operates on wrong data. Financial discrepancies, incorrect balances, regulatory violations.
- **Likelihood (3):** COBOL data formats (packed decimal, COMP-3, EBCDIC, implicit decimal positions, redefined record structures) are extremely prone to conversion errors. A single byte misalignment corrupts every subsequent record.
- **Direction:** - (worsening — as more complex data types are migrated, conversion complexity increases)
- **Mitigation:** Build automated data validation comparing source (mainframe) and target (cloud) record-by-record after each migration batch. Start with non-financial reference data (customer names, addresses) before financial data (balances, transactions). Use checksums/hash comparison at the batch level. Implement point-in-time reconciliation that can detect drift between systems during dual-operation period.
- **Post-mitigation estimate:** 4 (impact stays 3, likelihood drops to 1 with record-level validation — score 3; conservatively 4 given COBOL complexity)

### Transaction Processing Engine — Security (Score: 6)
- **Impact (3):** Financial transaction data breach = regulatory catastrophe.
- **Likelihood (2):** Moderate — cloud platforms have mature security controls, but the transition period creates temporary gaps as security models are migrated.
- **Direction:** = (stable)
- **Mitigation:** Implement zero-trust architecture from day 1 on cloud side. Encrypt all data in transit and at rest. Use cloud-native secrets management. Maintain RBAC parity with mainframe authorization model.
- **Post-mitigation estimate:** 3 (impact 3, likelihood 1)

### Data Migration Pipeline — Security (Score: 6)
- **Impact (3):** Migration pipeline handles the most sensitive banking data in bulk. A breach during migration exposes the entire customer database.
- **Likelihood (2):** Migration pipelines are often treated as temporary infrastructure with less security scrutiny than production systems.
- **Direction:** = (stable)
- **Mitigation:** Apply production-grade security to the migration pipeline. Encrypt data in transit between mainframe and cloud. Use dedicated, isolated network paths. Audit all access. Destroy intermediate data stores after verification.
- **Post-mitigation estimate:** 3 (impact 3, likelihood 1)

### Data Migration Pipeline — Operational Continuity (Score: 6)
- **Impact (3):** Failed migration batch = stale data on cloud side = incorrect transactions until fixed.
- **Likelihood (2):** Batch migration jobs can fail due to mainframe scheduling conflicts, network issues, or format errors. Moderate likelihood with monitoring.
- **Direction:** = (stable with proper monitoring)
- **Mitigation:** Implement real-time change data capture (CDC) instead of batch migration for transactional data. Batch migration only for initial historical data load. CDC provides continuous synchronization with much lower operational continuity risk.
- **Post-mitigation estimate:** 3 (impact 3, likelihood 1 with CDC)

### Cloud Database — Availability (Score: 6)
- **Impact (3):** Cloud database outage stops all cloud-side transaction processing.
- **Likelihood (2):** Cloud-managed databases have good SLAs (99.99%+), but the team must configure replication, failover, and backup correctly.
- **Direction:** = (new system)
- **Mitigation:** Use managed database service with multi-AZ deployment, automatic failover, and point-in-time recovery. Test failover monthly. Maintain read replicas in separate availability zones.
- **Post-mitigation estimate:** 3 (impact 3, likelihood 1 with multi-AZ)

### Cloud Database — Data Integrity (Score: 6)
- **Impact (3):** Corrupted financial data in the new system undermines the entire migration.
- **Likelihood (2):** Cloud databases are mature, but data integrity depends on application-level constraints, transaction isolation, and backup verification.
- **Direction:** = (new system)
- **Mitigation:** Implement database-level constraints mirroring all COBOL data validation rules. Use serializable isolation for financial transactions. Automated daily backup verification (restore and validate). Implement application-level checksums for financial totals.
- **Post-mitigation estimate:** 3 (impact 3, likelihood 1)

### API Gateway — Availability (Score: 6)
- **Impact (3):** Gateway outage = no external access to either legacy or cloud systems.
- **Likelihood (2):** API gateways are well-understood infrastructure, but misconfiguration or overload during traffic routing changes can cause outages.
- **Direction:** = (new system)
- **Mitigation:** Deploy gateway in active-active across multiple zones. Use canary routing for traffic migration (1% -> 10% -> 50% -> 100%). Implement health-check based routing with automatic fallback to legacy path.
- **Post-mitigation estimate:** 2 (impact 3, likelihood 1 — score 3; improved further with active-active)

### API Gateway — Performance (Score: 6)
- **Impact (3):** Gateway adds latency to every request during migration.
- **Likelihood (2):** Moderate — gateway overhead is typically <5ms, but routing logic complexity during migration can increase this.
- **Direction:** = (new system)
- **Mitigation:** Use hardware-accelerated or highly optimized gateway (e.g., Envoy). Minimize routing logic in the gateway — use simple path-based routing, not complex content-based routing. Monitor p99 latency continuously.
- **Post-mitigation estimate:** 2 (impact 2, likelihood 1)

### API Gateway — Security (Score: 6)
- **Impact (3):** Gateway is the public entry point. Compromise here exposes both legacy and cloud systems.
- **Likelihood (2):** API gateways are high-value targets but well-defended with standard practices.
- **Direction:** = (new system)
- **Mitigation:** Implement WAF, rate limiting, DDoS protection. mTLS for backend communication. Regular penetration testing.
- **Post-mitigation estimate:** 3 (impact 3, likelihood 1)

### Legacy Integration Layer — Scalability (Score: 6)
- **Impact (2):** Bridge can't handle peak transaction volume during migration.
- **Likelihood (3):** Bridge must handle 2M transactions/day while performing protocol translation. Under peak load, this becomes a bottleneck.
- **Direction:** - (worsening as more traffic routes through bridge)
- **Mitigation:** Design bridge as stateless and horizontally scalable. Load test to 5x peak (10M transactions/day) before go-live. Implement backpressure to prevent overload.
- **Post-mitigation estimate:** 2 (impact 2, likelihood 1)

### Legacy Integration Layer — Data Integrity (Score: 6)
- **Impact (3):** Data format conversion errors in the bridge corrupt transactions silently.
- **Likelihood (2):** COBOL-to-cloud data conversion is error-prone but can be validated systematically.
- **Direction:** - (each new data type through bridge is a new conversion risk)
- **Mitigation:** Unit test EVERY data type conversion with boundary values (max int, negative amounts, zero, special characters, multi-byte encoding). Implement end-to-end hash validation: hash before bridge, hash after bridge, compare.
- **Post-mitigation estimate:** 3 (impact 3, likelihood 1)

## Systemic Risk Observations

- **This is the highest-risk architecture assessment possible.** 18 of 30 cells are high-risk. Total system risk score: 180 across 30 cells. Average cell score: 6.0. This is not a system with some risks — this is a system where risk management IS the project.
- **Legacy Integration Layer is the most dangerous component (total: 48).** It scores 9 on four criteria. This is the component most likely to cause a catastrophic failure during migration. It deserves a dedicated team, dedicated monitoring, and dedicated testing.
- **Availability (34) and Data Integrity (32) are tied for systemic risk.** Both are existential to the bank. A migration that loses availability loses $50K/minute. A migration that loses data integrity loses customer trust and regulatory standing.
- **The $50,000/minute downtime cost changes everything.** This single fact means the migration strategy must be ultra-conservative. No big-bang cutover. No weekend maintenance windows. Strangler fig with parallel runs is the only responsible approach.
- **COBOL data format conversion is the hidden time bomb.** Packed decimal, COMP-3, EBCDIC, implicit decimal positions, and redefined record structures are all sources of silent corruption. This risk is invisible until you're reconciling financial totals and finding discrepancies.

## Recommendations Priority

1. **Adopt Strangler Fig pattern with parallel run validation** — The only responsible migration strategy given $50K/minute downtime cost. Migrate one transaction type at a time. Run both systems in parallel. Validate output matches before cutting over. This is slow (18-24 months) but dramatically reduces catastrophic failure risk.
2. **Build the Legacy Integration Layer as the most critical component** — Dedicated team, stateless architecture, 5x load testing, circuit breakers in both directions, <60s rollback capability. This is the bridge the entire migration depends on.
3. **Implement record-level data validation for every migration batch** — COBOL data format conversion errors are the #1 source of silent corruption. Validate every record, not just spot-check. Use checksums for batch-level verification.
4. **Use CDC instead of batch migration for transactional data** — Change data capture provides continuous, near-real-time synchronization, reducing the "data staleness" risk during dual operation.
5. **Performance benchmark every transaction type before migrating it** — Set explicit latency budgets based on current mainframe performance. Do not migrate any transaction type that doesn't meet its latency budget on cloud.
6. **Practice rollback quarterly** — The ability to fall back to mainframe must be tested, not assumed. Run rollback drills on a schedule. The cost of a drill is negligible compared to the cost of discovering your rollback doesn't work during an incident.
