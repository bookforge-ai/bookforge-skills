# Architecture Risk Assessment: Payment Processing Service

## Assessment Scope
- **Date:** 2026-03-27
- **Assessed by:** AI Architecture Risk Assessor (with skill)
- **Architecture style:** Distributed (service integrating with 3 external gateways)
- **Components assessed:** 4
- **Risk criteria:** Scalability, Availability, Performance, Security, Data Integrity

## Architecture Components
1. **Payment Processing Service** — Core service handling credit card transaction orchestration
2. **Gateway Integration Layer** — Adapter layer connecting to 3 external payment gateways (Gateway A, B, C)
3. **PCI Data Store** — Database storing PCI-compliant cardholder data
4. **Transaction Audit Log** — Immutable log of all transaction events for compliance and reconciliation

## Full Risk Assessment

| Risk Criteria    | Payment Service  | Gateway Integration | PCI Data Store   | Audit Log        | Total |
|------------------|------------------|---------------------|------------------|------------------|-------|
| Scalability      | 4 (M) =         | 6 (H) -            | 3 (M) =         | 2 (L) =         | 15    |
| Availability     | 6 (H) -         | 9 (H) -            | 6 (H) =         | 3 (M) =         | 24    |
| Performance      | 4 (M) =         | 6 (H) -            | 3 (M) =         | 1 (L) =         | 14    |
| Security         | 6 (H) =         | 9 (H) =            | 9 (H) =         | 3 (M) =         | 27    |
| Data Integrity   | 6 (H) =         | 4 (M) =            | 9 (H) =         | 6 (H) =         | 25    |
| **Total**        | **26**           | **34**              | **30**           | **15**           |       |

### Scoring Key
- Score = Impact (1-3) x Likelihood (1-3)
- Low (L): 1-2 | Medium (M): 3-4 | High (H): 6-9
- Direction: + improving, - worsening, = stable

## High-Risk Summary (Filtered View)

| Risk Criteria    | Payment Service  | Gateway Integration | PCI Data Store   | Audit Log        |
|------------------|------------------|---------------------|------------------|------------------|
| Scalability      | .                | 6 (H) -            | .                | .                |
| Availability     | 6 (H) -         | 9 (H) -            | 6 (H) =         | .                |
| Performance      | .                | 6 (H) -            | .                | .                |
| Security         | 6 (H) =         | 9 (H) =            | 9 (H) =         | .                |
| Data Integrity   | 6 (H) =         | .                   | 9 (H) =         | 6 (H) =         |

## Risk Details and Mitigations

### Gateway Integration — Security (Score: 9)
- **Impact (3):** A breach in the gateway layer exposes cardholder data to all 3 external providers. PCI DSS non-compliance means fines up to $500K/month and potential loss of processing privileges.
- **Likelihood (3):** Three external integrations triple the attack surface. Each gateway has different security protocols, key rotation schedules, and API authentication methods. The team has never built a distributed payment system, increasing the chance of misconfiguration.
- **Direction:** = (new system, no baseline)
- **Mitigation:** Implement a gateway abstraction with a security proxy pattern. All outbound calls route through a single security gateway that handles TLS termination, credential management, and request signing. Use a secrets manager (e.g., HashiCorp Vault) for all gateway credentials with automatic rotation.
- **Post-mitigation estimate:** 6 (impact remains 3, likelihood reduces to 2 with centralized security controls)

### Gateway Integration — Availability (Score: 9)
- **Impact (3):** If the gateway layer fails, zero transactions can be processed. Direct revenue impact every second it's down.
- **Likelihood (3):** Three external dependencies, each with their own SLA. Any single gateway outage plus no failover logic means a complete service disruption. Team inexperience with distributed systems increases likelihood of missing failure modes.
- **Direction:** - (worsening — no failover logic exists yet)
- **Mitigation:** Implement active failover across gateways. If Gateway A fails, automatically route to Gateway B or C. Use circuit breaker pattern per gateway with configurable thresholds. Add health checks with <30s detection time.
- **Post-mitigation estimate:** 3 (impact remains 3, likelihood drops to 1 with active failover)

### PCI Data Store — Security (Score: 9)
- **Impact (3):** Breach of PCI-compliant data store is the worst-case scenario: cardholder data exposure, regulatory fines, legal liability, brand damage.
- **Likelihood (3):** Team has never built PCI-compliant storage. PCI DSS has 300+ controls. Missing even one control creates a compliance gap that is both a security risk and an audit failure.
- **Direction:** = (new system)
- **Mitigation:** Use a PCI-certified tokenization service (e.g., Stripe's vault, Basis Theory) instead of storing raw cardholder data. This shifts PCI scope from your infrastructure to the tokenization provider, dramatically reducing both impact and likelihood.
- **Post-mitigation estimate:** 3 (impact drops to 1 — you never store raw card data; likelihood stays 3 until certified)

### PCI Data Store — Data Integrity (Score: 9)
- **Impact (3):** Corrupted or lost transaction data means financial discrepancy, failed reconciliation, regulatory audit failure.
- **Likelihood (3):** Team inexperience with PCI data handling. No mention of backup strategy, replication, or consistency guarantees in the current description.
- **Direction:** = (new system)
- **Mitigation:** Implement synchronous replication with point-in-time recovery. Daily automated backup verification. Use database-level checksums. Implement application-level idempotency keys for all transaction writes.
- **Post-mitigation estimate:** 3 (impact stays 3 — financial data is always high impact; likelihood drops to 1 with proper replication and verification)

### Payment Service — Availability (Score: 6)
- **Impact (3):** Payment service down = no revenue. Every minute of downtime has direct financial impact.
- **Likelihood (2):** Single service orchestrating across 3 gateways. Cascading failures from gateway timeouts can lock threads and bring down the service. Moderate likelihood because standard patterns exist (circuit breakers, bulkheads) but team may not implement them.
- **Direction:** - (no resilience patterns implemented yet)
- **Mitigation:** Implement bulkhead pattern isolating each gateway call. Add circuit breakers with fallback. Set aggressive timeouts on all external calls (2-5 seconds max). Deploy at least 2 instances behind a load balancer.
- **Post-mitigation estimate:** 3 (impact stays 3, likelihood drops to 1)

### Payment Service — Security (Score: 6)
- **Impact (3):** Core service has access to all transaction data and gateway credentials.
- **Likelihood (2):** Moderate — service is internal, but any vulnerability exposes the entire payment chain.
- **Direction:** = (new system)
- **Mitigation:** Apply principle of least privilege. Payment service should only hold tokenized references, not raw card data. Use service mesh for mTLS between all services. Implement request-level authorization.
- **Post-mitigation estimate:** 3 (impact drops from 3 to 1 if tokenization is used; likelihood stays 3 during initial build)

### Audit Log — Data Integrity (Score: 6)
- **Impact (3):** Lost audit trail = failed PCI audit, inability to reconcile transactions, regulatory non-compliance.
- **Likelihood (2):** Append-only logs are simpler to protect than mutable data, but without proper implementation, log gaps or corruption go undetected.
- **Direction:** = (new system)
- **Mitigation:** Use an append-only, immutable storage backend (e.g., S3 with Object Lock, or a purpose-built audit service). Implement hash chaining for tamper detection. Separate write path from read path.
- **Post-mitigation estimate:** 2 (impact stays 3 but likelihood drops to 1 with immutable storage — score 3, further improved by hash chaining)

### Gateway Integration — Scalability (Score: 6)
- **Impact (2):** Under peak load, gateway rate limits or connection pool exhaustion cause transaction failures, but this is recoverable.
- **Likelihood (3):** Three gateways each have different rate limits, connection limits, and throttling behaviors. Without explicit handling, peak load will hit these limits.
- **Direction:** - (no rate limit handling exists)
- **Mitigation:** Implement client-side rate limiting matching each gateway's published limits. Add request queuing with backpressure for burst traffic. Pre-negotiate higher rate limits with primary gateway provider.
- **Post-mitigation estimate:** 2 (impact stays 2, likelihood drops to 1)

### Gateway Integration — Performance (Score: 6)
- **Impact (2):** Slow gateway responses degrade user experience but don't cause data loss.
- **Likelihood (3):** External network calls inherently variable. Three different gateways means three different latency profiles. Without caching of non-sensitive data and connection pooling, p99 latency will spike.
- **Direction:** - (no optimization exists)
- **Mitigation:** Implement connection pooling per gateway. Cache gateway configuration/routing data. Set SLA-based timeouts per gateway. Route to the fastest healthy gateway when multiple are available.
- **Post-mitigation estimate:** 2 (impact stays 2, likelihood drops to 1)

### PCI Data Store — Availability (Score: 6)
- **Impact (3):** Data store outage means all payment processing stops.
- **Likelihood (2):** Moderate — modern databases have good uptime, but a single instance without replication is a single point of failure.
- **Direction:** = (new system)
- **Mitigation:** Deploy database with synchronous replication and automatic failover. Use read replicas for non-transactional queries. Implement connection pooling (e.g., PgBouncer) to prevent connection exhaustion.
- **Post-mitigation estimate:** 2 (impact stays 3 but likelihood drops to 1 — score 3; further improved by connection pooling)

## Systemic Risk Observations

- **Security is the systemic crisis (total: 27).** The entire system handles sensitive financial data, yet the team has no experience with PCI-compliant distributed systems. This is not a single-service problem — it's architecture-wide.
- **Gateway Integration is the riskiest component (total: 34).** It is high-risk across 4 of 5 criteria. This single component represents the most concentrated risk in the architecture and should receive the most architectural attention.
- **Team inexperience is a risk multiplier.** The team has never built a distributed payment system. This elevates likelihood scores across every component. Consider engaging a payment systems consultant for the initial architecture and security review.

## Recommendations Priority

1. **Adopt tokenization** — Shifts PCI scope to a certified provider, reducing security and data integrity risk across Payment Service and PCI Data Store simultaneously. Highest leverage single action.
2. **Implement gateway failover with circuit breakers** — Addresses the single highest-risk score (availability 9) in the Gateway Integration layer. Without this, any single gateway outage stops all transactions.
3. **Engage PCI compliance expertise** — Team inexperience is the root cause of elevated likelihood scores across the board. A compliance consultant or PCI-certified architect reduces risk across every cell, not just one.
4. **Build the audit log on immutable storage from day 1** — Much harder to retrofit an immutable audit trail than to build it correctly initially. Foundation for all compliance requirements.
