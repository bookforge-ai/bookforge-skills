# Event-Driven Topology Recommendation: Stock Trading Platform

## Request-Based vs Event-Based Assessment
**Model selected:** Mixed — both event-based and request-based patterns coexist
**Rationale:** The system has two fundamentally different processing models:
- **Trade execution:** Event-based. A trade is a reaction to a market event (price hit, order trigger). It's time-critical and requires immediate asynchronous processing. The system reacts to market conditions.
- **Compliance reporting:** Could be either. Daily aggregation is a scheduled batch process (request-based — "give me today's trades"), but the individual trade events feeding into it are event-based. The reporting workflow itself has complex rules and dependencies.

This is a textbook case for **hybrid topology** — different processing models for different workloads.

## Workflow Analysis

| Workflow | Steps | Dependencies | Error Handling Need | Topology |
|----------|-------|:---:|:---:|:---:|
| Trade execution | Validate trade, execute trade, update position, calculate risk, update P&L | Independent — each processor reacts to trade-executed event independently | Low — individual processor failure is acceptable; positions reconcile | Broker |
| Compliance reporting | Aggregate trades, apply compliance rules, flag exceptions, generate report, submit to regulator | Dependent — rules must be applied after aggregation; exceptions must be flagged before report; report must be complete before submission | High — incomplete or incorrect compliance reports have regulatory consequences | Mediator |

## Topology Decision

### Selected: Hybrid (Broker + Mediator)

**Primary driver:** Two workflows with diametrically opposite characteristics. Trade execution needs sub-millisecond performance with independent processing. Compliance reporting needs coordinated, sequential, error-handled workflow execution. Forcing both into one topology would compromise one of them.

### Trade Execution Path — 7-Dimension Assessment

| Dimension | Need | Broker | Mediator | Fit |
|-----------|------|:---:|:---:|:---:|
| Workflow control | LOW — processors react independently | Low | High | Broker |
| Error handling | LOW — positions reconcile; individual failures acceptable | Low | High | Broker |
| Recoverability | LOW — next trade corrects any drift | Low | High | Broker |
| Restart capability | NOT APPLICABLE — trades are one-shot | Low | High | Broker |
| Scalability | CRITICAL — must handle market-hours volume spikes | High | Moderate | Broker |
| Performance | CRITICAL — sub-millisecond processing required | High | Moderate | Broker |
| Fault tolerance | HIGH — one processor down can't halt trading | High | Low | Broker |

**Score: 7/7 broker.** A mediator in the trade execution path would add unacceptable latency.

### Compliance Reporting Path — 7-Dimension Assessment

| Dimension | Need | Broker | Mediator | Fit |
|-----------|------|:---:|:---:|:---:|
| Workflow control | HIGH — steps must execute in order, rules depend on aggregated data | Low | High | Mediator |
| Error handling | HIGH — compliance errors have regulatory consequences | Low | High | Mediator |
| Recoverability | HIGH — must produce a complete, correct report | Low | High | Mediator |
| Restart capability | HIGH — if report generation fails midway, restart from failure point | Low | High | Mediator |
| Scalability | LOW — daily batch process, not real-time | High | Moderate | Either |
| Performance | LOW — hours-long batch is acceptable | High | Moderate | Either |
| Fault tolerance | MEDIUM — must complete but has time buffer | High | Low | Mediator (error handling compensates) |

**Score: 5/7 mediator.** Compliance workflows need orchestrated coordination.

## Hybrid Architecture Design

```
                                ┌─────────────────────────────────────┐
                                │         Event Router                │
                                │  (classifies incoming events)       │
                                └───────┬────────────┬────────────────┘
                                        │            │
                    ┌───────────────────┘            └───────────────────┐
                    ▼                                                    ▼
        ┌───────────────────────┐                          ┌────────────────────────┐
        │  BROKER TOPOLOGY      │                          │  MEDIATOR TOPOLOGY     │
        │  (Trade Execution)    │                          │  (Compliance)          │
        │                       │                          │                        │
        │  trade-executed topic │                          │  Compliance Mediator   │
        │    ├→ PositionTracker │                          │    Step 1: Aggregate   │
        │    ├→ RiskCalculator  │                          │    Step 2: Apply rules │
        │    ├→ PnLUpdater      │                          │    Step 3: Flag excepts│
        │    └→ AuditLogger     │                          │    Step 4: Gen report  │
        │                       │                          │    Step 5: Submit      │
        └───────────────────────┘                          └────────────────────────┘
```

### Event Router (Simple Mediator for Classification)

A lightweight simple mediator at the entry point classifies events:
- **Trade events** (trade-placed, trade-executed, trade-cancelled) → route to broker topology
- **Compliance events** (compliance-run-triggered, daily-close) → route to mediator topology
- **Mixed events** (trade-executed events are ALSO captured by the compliance system's event store for daily aggregation)

This is the mediator delegation model: the simple mediator classifies and delegates, rather than trying to coordinate everything.

### Trade Execution Path Detail

**Topology:** Pure broker
**Message infrastructure:** Apache Kafka (optimized for high-throughput, low-latency)

```
Initiating Event: trade-placed
  → TradeValidator processor: validates trade parameters
  → publishes [trade-validated] or [trade-rejected]

Processing Event: trade-validated
  → TradeExecutor processor: executes trade against market
  → publishes [trade-executed]

Processing Event: trade-executed (fan-out to independent processors)
  ├→ PositionTracker: updates position book → publishes [position-updated]
  ├→ RiskCalculator: recalculates portfolio risk → publishes [risk-updated]
  ├→ PnLUpdater: updates profit/loss → publishes [pnl-updated]
  └→ AuditLogger: logs trade for compliance capture → publishes [trade-logged]
```

Note: The AuditLogger processor writes trade records to a store that the compliance mediator reads during daily aggregation. This is the bridge between the two topologies — broker events feed the mediator's data source.

**Performance considerations:**
- Kafka partitioning by instrument/symbol for ordered processing per instrument
- In-memory processing where possible (position calculations)
- Processing events use past tense (broker semantics): trade-executed, position-updated

### Compliance Reporting Path Detail

**Topology:** Mediator with simple mediator implementation
**Message infrastructure:** RabbitMQ (reliable delivery, acknowledgments, simpler than Kafka for orchestration)

**Mediator complexity level:** Simple mediator (source code)
**Rationale:** Compliance workflow is sequential with basic conditional branching (flag or don't flag). No human intervention during the batch run. No need for BPEL or BPM engine.

```
Step 1: Aggregate Trades
  - Command: aggregate-daily-trades
  - Processor: TradeAggregator reads from audit log store
  - Mediator waits for acknowledgment with aggregation summary

Step 2: Apply Compliance Rules
  - Command: apply-compliance-rules
  - Processor: RuleEngine applies regulatory rules to aggregated data
  - Mediator waits for acknowledgment with rule results

Step 3: Flag Exceptions
  - Command: flag-exceptions
  - Processor: ExceptionFlagger identifies trades that violate rules
  - IF exceptions found → mediator records them for the report
  - IF critical exceptions → mediator triggers alert to compliance team

Step 4: Generate Report
  - Command: generate-compliance-report
  - Processor: ReportGenerator creates the regulatory report
  - Mediator waits for acknowledgment with report artifact

Step 5: Submit to Regulator
  - Command: submit-report
  - Processor: RegulatorySubmitter sends report to regulatory system
  - Mediator records submission confirmation
  - Workflow complete
```

## Error Handling Strategy

### Trade Execution Path (Broker)

**Per-processor error handling:**
- Each processor handles its own errors independently
- Dead letter queues per processor for failed events
- Position reconciliation runs hourly to catch any drift from missed events

**Data loss prevention:**
| Link | Mitigation |
|------|------------|
| Message send | Kafka's synchronous ack mode (acks=all) ensures message reaches all replicas |
| Message processing | Kafka consumer offsets committed only after processing (at-least-once delivery) |
| Post-processing | Idempotent writes — processing the same trade event twice produces the same result |

### Compliance Reporting Path (Mediator)

**Mediator-managed error handling:**
- Mediator persists workflow state at each step
- If any step fails, mediator records the failure point and halts
- Workflow restarts from the failed step (not from the beginning)
- Critical: compliance report generation is an all-or-nothing workflow — partial reports must not be submitted

**Data loss prevention:**
| Link | Mitigation |
|------|------------|
| Message send | Synchronous send with RabbitMQ publisher confirms |
| Message processing | Client acknowledge mode; messages redelivered on processor failure |
| Post-processing | Last participant support — DB commit and ack in same transaction |

## Architecture Characteristics Impact

### Trade Execution Path
| Characteristic | Rating | Notes |
|---------------|:---:|-------|
| Performance | 5/5 | No mediator overhead; Kafka optimized for throughput |
| Scalability | 5/5 | Per-processor scaling; Kafka partitioning |
| Fault tolerance | 5/5 | Independent processors; Kafka replication |
| Evolutionary | 5/5 | New processors subscribe to existing topics |
| Testability | 2/5 | Async event chains are complex to test |

### Compliance Reporting Path
| Characteristic | Rating | Notes |
|---------------|:---:|-------|
| Performance | 3/5 | Mediator overhead acceptable for batch process |
| Scalability | 3/5 | Not needed — daily batch with known volume |
| Fault tolerance | 3/5 | Mediator is SPOF but workflow is not time-critical |
| Evolutionary | 4/5 | New compliance rules added as new steps |
| Testability | 4/5 | Sequential mediator workflow is testable end-to-end |

## Key Insight

The two workloads in this system are at opposite ends of the topology spectrum. Forcing both into a single topology would either sacrifice trade execution performance (if mediator) or sacrifice compliance workflow reliability (if broker). The hybrid approach — broker for the latency-critical path, mediator for the coordination-critical path — gives each workload the topology that matches its characteristics.

The bridge between the two topologies (AuditLogger writing to a store that the compliance mediator reads) is lightweight and doesn't couple the topologies. Trade execution doesn't know or care about compliance; compliance reads from the audit store independently.
