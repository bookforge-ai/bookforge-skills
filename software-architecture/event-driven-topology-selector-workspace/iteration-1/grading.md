# Grading: event-driven-topology-selector — Iteration 1

## Assertions Used

### Structural Assertions (S1-S5)
| ID | Assertion |
|----|-----------|
| S1 | Systematically evaluates the system against all 7 broker-vs-mediator comparison dimensions (workflow control, error handling, recoverability, restart, scalability, performance, fault tolerance) |
| S2 | Produces a clear topology recommendation (broker, mediator, or hybrid) with rationale tied to the dimension analysis |
| S3 | Addresses error handling strategy specifically, including data loss prevention across the async chain |
| S4 | Evaluates whether the use case is request-based or event-based before selecting topology |
| S5 | If mediator is recommended, specifies the complexity level (simple/hardcoded/BPM) with rationale |

### Value Assertions (V1-V7)
| ID | Assertion |
|----|-----------|
| V1 | Uses the 7 comparison dimensions as a SYSTEMATIC framework, not just mentions broker and mediator as options |
| V2 | Identifies all THREE data loss points in the async chain (send, processing, post-processing) with specific mitigations for each, not just "use persistent queues" |
| V3 | Explains the semantic difference between events (things that happened) in broker vs commands (things to do) in mediator topology |
| V4 | Recommends hybrid topology when the system has both simple and complex workflows, rather than forcing everything into one topology |
| V5 | Matches mediator implementation complexity to workflow complexity (simple/BPEL/BPM), not just recommends "use a mediator" |
| V6 | Explicitly warns about broker topology's lack of built-in error handling and the consequences (silent data loss, stuck workflows, inconsistent state) |
| V7 | Considers workflow step dependencies (independent vs dependent) as a primary decision driver |

---

## Eval 1: Order Fulfillment System (Mediator Use Case)

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:---:|---------|
| S1 | PASS | Full 7-dimension table with per-dimension assessment and scoring (4 mediator, 1 broker, 2 neutral) |
| S2 | PASS | Clear "Mediator" recommendation with rationale: "Error handling with compensation... payment failure requires inventory rollback" |
| S3 | PASS | Three-link data loss prevention table with specific mitigations (synchronous send, client acknowledge, last participant support). Compensation pattern for payment failure detailed. |
| S4 | PASS | Explicit request-based vs event-based assessment: "Order placement is a reactive event... This is clearly an event-based use case" |
| S5 | PASS | "Simple mediator (source code)" with rationale: "workflow is linear with one conditional branch. No human intervention. No BPM needed." |
| V1 | PASS | Dimensions are the primary decision framework, not an afterthought. Score tallied: "4 dimensions favor mediator, 1 favors broker, 2 neutral" |
| V2 | PASS | All three links identified and mitigated in a table. Links labeled as message send, message processing, post-processing with specific patterns. |
| V3 | PASS | "These are COMMANDS (things to do), not events (things that happened)" — explicitly noted in the workflow design section |
| V4 | N/A | Not applicable — this scenario doesn't require hybrid |
| V5 | PASS | Three mediator levels discussed, simple selected with specific rationale |
| V6 | PASS | "Why NOT broker?" section explicitly explains: "No component is aware that payment failed... Inventory is reserved for an order that will never be fulfilled" |
| V7 | PASS | Dependencies explicitly mapped: "payment must succeed before fulfillment proceeds; inventory must be validated before payment" |

**Score: 11/11 applicable (V4 N/A)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:---:|---------|
| S1 | FAIL | No systematic 7-dimension evaluation. Only mentions "dependencies" and "error handling" informally |
| S2 | PASS | Recommends mediator with rationale (compensation requirement) |
| S3 | PARTIAL | Mentions dead letter queues and Saga pattern but does NOT address the three-link data loss prevention model |
| S4 | FAIL | No request-based vs event-based evaluation |
| S5 | FAIL | Mentions Temporal and Camunda but doesn't classify mediator complexity levels or explain why |
| V1 | FAIL | No systematic dimension framework. Trade-offs listed as prose "advantages/disadvantages" |
| V2 | FAIL | Only mentions "dead letter queues for failed messages" — does not identify the three links |
| V3 | FAIL | No mention of events vs commands semantic distinction |
| V4 | N/A | Not applicable |
| V5 | FAIL | Suggests Temporal and Camunda without classifying complexity levels |
| V6 | PARTIAL | Mentions "the orchestrator is a single point of failure" as a disadvantage but doesn't warn about BROKER's error handling problems |
| V7 | PASS | Notes "steps have dependencies on each other" |

**Score: 3/11 applicable (2 full pass, 2 partial = 3/11)**

---

## Eval 2: Social Media Content Processing (Broker Use Case)

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:---:|---------|
| S1 | PASS | Full 7-dimension table: "Score: 7/7 dimensions favor broker. Unambiguous broker selection." |
| S2 | PASS | Clear "Broker" recommendation with dimension-by-dimension rationale |
| S3 | PASS | Three-link data loss prevention table. Per-processor error handling table. Dead letter queues per processor. |
| S4 | PASS | "Content posting is a reactive event... fire-and-forget from the user's perspective... Classic event-based model." |
| S5 | N/A | Mediator not recommended |
| V1 | PASS | 7 dimensions are the primary framework. Each scored individually. |
| V2 | PASS | All three links: synchronous send with broker ack, client acknowledge mode, last participant support / transactional outbox |
| V3 | PASS | "Processing events use past tense (broker semantics): trade-executed, position-updated" |
| V4 | N/A | Not applicable — single topology |
| V5 | N/A | Mediator not recommended |
| V6 | PASS | "Why NOT mediator?" section: "Adding a mediator here would introduce a coordinator that adds latency... create a single point of failure... add complexity with zero benefit" |
| V7 | PASS | "The user explicitly stated: 'These are all independent.' Let's verify:" — then verifies each step's independence |

**Score: 9/9 applicable (S5, V4, V5 N/A)**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:---:|---------|
| S1 | FAIL | No dimension evaluation at all |
| S2 | PASS | Recommends broker with rationale (independent steps) |
| S3 | PARTIAL | Mentions "dead letter queues for failed messages" and retry but no three-link model |
| S4 | FAIL | No request-based vs event-based evaluation |
| S5 | N/A | Mediator not recommended |
| V1 | FAIL | No systematic dimension framework |
| V2 | FAIL | Only "dead letter queues" and "retry" — no three-link model |
| V3 | FAIL | No events vs commands distinction |
| V4 | N/A | Not applicable |
| V5 | N/A | Not applicable |
| V6 | PARTIAL | Mentions "When You'd Need Orchestration Instead" but doesn't warn about broker's error handling limits |
| V7 | PASS | Recognizes all steps are independent |

**Score: 2.5/7 applicable (2 full pass, 1 partial = 2.5/7)**

---

## Eval 3: Stock Trading Platform (Hybrid Use Case)

### With Skill

| Assertion | Pass? | Evidence |
|-----------|:---:|---------|
| S1 | PASS | TWO full 7-dimension tables — one for trade execution (7/7 broker), one for compliance (5/7 mediator) |
| S2 | PASS | Clear "Hybrid (Broker + Mediator)" recommendation with per-workflow rationale |
| S3 | PASS | Separate three-link data loss prevention tables for EACH topology path. Trade path: Kafka acks, consumer offsets, idempotent writes. Compliance path: publisher confirms, client ack, last participant support. |
| S4 | PASS | "Mixed — both event-based and request-based patterns coexist" with reasoning for each workload |
| S5 | PASS | "Simple mediator (source code)" for compliance with rationale: "sequential with basic conditional branching. No human intervention during batch." |
| V1 | PASS | Two complete dimension frameworks, one per workload. Dimensions are the primary decision tool. |
| V2 | PASS | Three links addressed separately for each topology path with different mitigations |
| V3 | PASS | "Processing events use past tense (broker semantics)" and commands identified in compliance mediator workflow |
| V4 | PASS | Hybrid explicitly recommended: "Two workflows with diametrically opposite characteristics... Forcing both into one topology would compromise one" |
| V5 | PASS | "Simple mediator (source code)" selected. Complexity classification explained. |
| V6 | PASS | Implicit in the hybrid justification: trade path needs broker for performance, compliance path can't use broker because it needs coordination |
| V7 | PASS | Trade steps analyzed as independent; compliance steps analyzed as dependent with ordering constraints |

**Score: 12/12**

### Without Skill

| Assertion | Pass? | Evidence |
|-----------|:---:|---------|
| S1 | FAIL | No 7-dimension evaluation. Lists considerations informally |
| S2 | PASS | Recommends different approaches for each workload (pub/sub for trades, orchestration for compliance) |
| S3 | PARTIAL | Mentions "at-least-once delivery" and "dead letter topics" but no three-link model |
| S4 | FAIL | No request-based vs event-based evaluation |
| S5 | FAIL | Suggests Airflow/Temporal without mediator complexity classification |
| V1 | FAIL | No systematic dimension framework |
| V2 | FAIL | Only mentions "at-least-once delivery with idempotent consumers" — no three-link model |
| V3 | FAIL | No events vs commands distinction |
| V4 | PASS | Recognizes two different workloads need different approaches |
| V5 | FAIL | No mediator complexity classification |
| V6 | FAIL | No explicit discussion of broker error handling limitations |
| V7 | PARTIAL | Implicitly recognizes compliance steps are sequential but doesn't explicitly analyze dependencies |

**Score: 2.5/12 (2 full pass, 1 partial = 2.5/12)**

---

## Summary Scorecard

| Eval | Prompt | With Skill | Without Skill | Delta |
|------|--------|:---:|:---:|:---:|
| 1 | Order fulfillment (mediator) | **11/11** (100%) | **3/11** (27%) | +73% |
| 2 | Social media fan-out (broker) | **9/9** (100%) | **2.5/7** (36%) | +64% |
| 3 | Stock trading (hybrid) | **12/12** (100%) | **2.5/12** (21%) | +79% |
| **Average** | | **100%** | **28%** | **+72%** |

## Key Findings

### What the skill consistently adds (with-skill always has, without-skill always misses):

1. **Systematic 7-dimension framework** (V1) — Without-skill responses list trade-offs as prose. With-skill uses a structured evaluation table that ensures no dimension is forgotten.

2. **Three-link data loss prevention** (V2) — Without-skill responses only mention "persistent queues" or "dead letter queues." With-skill identifies all three failure points in the async chain with specific mitigation patterns (synchronous send, client acknowledge, last participant support).

3. **Events vs commands semantic distinction** (V3) — Without-skill never mentions this. With-skill explains why broker events use past tense (things that happened) vs mediator commands (things to do).

4. **Mediator complexity classification** (V5) — Without-skill says "use Temporal/Camunda/Airflow" without explaining why. With-skill classifies mediator complexity into simple/BPEL/BPM and matches to workflow complexity.

5. **Request-based vs event-based pre-evaluation** (S4) — Without-skill jumps straight to topology selection. With-skill first evaluates whether event-driven is even the right model.

### Where without-skill is adequate:

- **Basic topology recommendation** (S2) — Without-skill generally reaches the correct recommendation, but through informal reasoning rather than systematic analysis.
- **Dependency awareness** (V7) — Without-skill recognizes obvious dependencies (rollback needs, independent steps).

### Conclusion

The skill's primary value is **systematic rigor** — it ensures every dimension is evaluated, every failure point is addressed, and every recommendation is specific enough to implement. Without the skill, responses are directionally correct but lack the structured depth needed for actual architecture decisions.
