# Architecture Quality Attributes Reference

Use this reference when you need the full list of quality attributes for trade-off analysis. Organized by category.

## Operational Characteristics

These affect how the system runs in production.

| Attribute | Definition | Trade-off tension |
|-----------|-----------|-------------------|
| **Availability** | System uptime level (e.g., 99.9%) | Higher availability = more redundancy = higher cost |
| **Continuity** | Disaster recovery capability | Better DR = more infrastructure = higher cost/complexity |
| **Performance** | Response time, throughput, capacity | Better performance often conflicts with security (encryption overhead) and maintainability (optimized code is harder to read) |
| **Recoverability** | Time to recover from failure | Fast recovery = more sophisticated backup/failover = cost |
| **Reliability** | Data integrity, fail-safe behavior | Higher reliability often requires synchronous processing = lower throughput |
| **Robustness** | Error handling, boundary conditions | More robust = more defensive code = slower development velocity |
| **Scalability** | Handle growing load | Better scalability typically requires distributed architecture = more complexity, more cost |
| **Elasticity** | Handle sudden bursts | Elastic systems need auto-scaling infrastructure = cloud cost variability |

## Structural Characteristics

These affect how the codebase is organized and evolved.

| Attribute | Definition | Trade-off tension |
|-----------|-----------|-------------------|
| **Configurability** | End-user customization ease | More configurable = more code paths = harder to test |
| **Extensibility** | Adding new functionality | More extensible = more abstraction = initial complexity overhead |
| **Maintainability** | Ease of changes | Better maintainability often requires more modular architecture = more inter-service communication |
| **Modularity** | Separation of concerns | More modular = more boundaries = more coordination overhead |
| **Testability** | Ease of testing | Better testability requires clean interfaces = more upfront design effort |
| **Deployability** | Ease and frequency of releases | Better deployability often requires microservices or containers = operational complexity |
| **Portability** | Run on multiple platforms | More portable = more abstraction layers = potential performance loss |
| **Upgradeability** | Ease of version upgrades | Easier upgrades = more backward compatibility = code bloat |

## Cross-Cutting Characteristics

These span multiple categories.

| Attribute | Definition | Trade-off tension |
|-----------|-----------|-------------------|
| **Security** | Protection against threats | More security = more encryption/indirection = worse performance |
| **Accessibility** | Support for all users | Better accessibility = more implementation effort = slower delivery |
| **Observability** | Visibility into system behavior | More observability = more instrumentation = slight performance overhead |
| **Simplicity** | Ease of understanding | Simpler systems are easier to maintain but may sacrifice scalability/flexibility |
| **Cost** | Total cost of ownership | Lower cost often means accepting trade-offs in scalability, reliability, or performance |
| **Time-to-market** | Speed of initial delivery | Faster delivery often means accepting technical debt |

## Common Trade-off Pairs

These quality attributes frequently conflict:

| Attribute A | vs | Attribute B | Why they conflict |
|-------------|:---:|-------------|-------------------|
| Performance | vs | Security | Encryption, indirection, and access control add latency |
| Scalability | vs | Simplicity | Distributed systems scale better but are fundamentally more complex |
| Scalability | vs | Cost | More instances, more infrastructure, more operational overhead |
| Maintainability | vs | Performance | Clean, readable code runs slower than hand-optimized code |
| Extensibility | vs | Simplicity | Abstraction layers for future flexibility add current complexity |
| Reliability | vs | Performance | Synchronous processing ensures data integrity but limits throughput |
| Deployability | vs | Simplicity | Independent deployments require service boundaries = more moving parts |
| Time-to-market | vs | Maintainability | Shortcuts speed delivery but create technical debt |
