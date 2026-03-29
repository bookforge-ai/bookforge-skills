# Architecture Style Selection: Real-Time Collaborative Document Editor

## Decision Context

**System:** A real-time collaborative document editor (Google Docs-like). Multiple users edit the same document simultaneously with concurrent edit handling, real-time sync, document versioning, and offline editing support.

**Scale:** Up to 10,000 concurrent active documents, 5-50 users per document.

**Driving characteristics (top 3, in priority order):**
1. **Performance** -- Sub-second latency for edit propagation across all connected clients is the core user experience requirement. Users expect keystrokes to appear instantly for all collaborators.
2. **Scalability** -- 10,000 concurrent documents with 5-50 users each means 50,000-500,000 concurrent connections. The system must scale horizontally to handle this connection density.
3. **Fault tolerance** -- Edits cannot be lost. If a server node goes down, in-flight edits and document state must survive. Offline editing further demands that the system gracefully handles disconnected clients and reconciles divergent states.

**Architecture quanta:** **Multiple quanta.** The system has components with fundamentally different characteristic profiles:
- **Real-time sync engine** (collaboration sessions): Needs extreme performance, low-latency event propagation, high connection density, and elasticity (documents come and go). This is a stateful, connection-heavy workload.
- **Document storage and versioning service**: Needs reliability, consistency, and durability. This is a write-heavy, persistence-focused workload with different scaling characteristics.
- **Offline sync/conflict resolution**: Needs fault tolerance and eventual consistency handling. Operates on different timescales (reconnection can happen minutes to hours later).
- **User/auth/permissions**: Standard request-reply, low-latency reads, different scaling profile from the real-time engine.

The real-time sync engine and the document persistence layer have fundamentally different quality attribute needs, confirming multiple quanta.

**Team context:** 12 developers, experienced in web applications, no distributed systems experience. Moderate budget.

## Step 1: Monolith vs Distributed

**Decision: Distributed**

**Reasoning:** Multiple architecture quanta are present. The real-time collaboration engine requires performance (5) and scalability (5) that no monolithic style can deliver -- layered scores 2/1, pipeline scores 2/1, microkernel scores 3/1 on performance/scalability respectively. The connection density alone (potentially 500,000 concurrent WebSocket connections) rules out a single deployment unit. Furthermore, the document persistence layer has different characteristics (reliability, consistency) than the real-time engine (performance, scalability), confirming the need for independent deployment units with different scaling profiles.

## Step 2B: Evaluate Distributed Styles

### Service-Based Architecture
- Good general-purpose distribution with shared database preserving ACID
- Scores only 3 on scalability and 2 on elasticity -- insufficient for the real-time sync engine's needs
- Pragmatic, but cannot handle the connection density or real-time event propagation requirements

### Event-Driven Architecture
- Performance (5) and scalability (5) are exactly what the real-time sync engine needs
- Fault tolerance (5) ensures edits survive node failures
- The domain is inherently event-driven: every keystroke/edit is an event that must propagate to all connected clients
- Broker topology fits the edit-propagation pattern (fire events to all subscribers on a document channel)
- Mediator topology fits conflict resolution and version reconciliation workflows

### Space-Based Architecture
- Elasticity (5), scalability (5), performance (5) are strong
- The in-memory data grid model actually maps well to collaborative editing (document state held in memory, replicated across processing units)
- However: cost (2) and simplicity (1) are significant concerns given moderate budget and team inexperience with distributed systems
- Testability (1) is a major risk for a team learning distributed patterns

### Microservices Architecture
- Scalability (5) and elasticity (5) are strong
- But performance (2) is a critical weakness -- the inter-service communication overhead works against sub-second edit propagation
- Requires mature DevOps practices the team lacks
- Cost (1) exceeds moderate budget

## Step 3: Organizational Fit

| Factor | Assessment |
|--------|-----------|
| **Team size: 12** | In the 10-30 range. Service-based or limited microservices viable. Full microservices is a stretch. |
| **No distributed experience** | This is the critical constraint. Rules out microservices and space-based. Event-driven is complex (simplicity: 1, testability: 2) but the domain naturally maps to it, which reduces cognitive overhead. |
| **Moderate budget** | Eliminates space-based (cost: 2) and microservices (cost: 1). Event-driven (cost: 3) and service-based (cost: 4) are feasible. |
| **Recommendation adjustment** | Pure event-driven is technically ideal but risky for the team. A **service-based architecture with event-driven communication for the real-time layer** provides the pragmatic middle ground -- the team gets distribution benefits through coarse-grained services (manageable) while using event-driven patterns only where the domain demands it (real-time sync). |

## Step 4: Anti-Pattern Check

| Anti-pattern | Risk | Mitigation |
|-------------|------|------------|
| **Distributed monolith** | Medium -- team inexperience could lead to tightly coupled services | Keep services coarse-grained (4-6 domain services, not dozens). Use shared database initially for non-realtime data. |
| **Broker/mediator mismatch** | Medium -- using the wrong event topology for different workflows | Broker for edit propagation (simple fan-out). Mediator for conflict resolution and offline reconciliation (complex workflow with error handling). |
| **Too-fine-grained services** | Low-medium -- temptation to split "editing" into many tiny services | Group by bounded context: collaboration-session service, document-storage service, user service, notification service. Not per-feature. |
| **Transactions across boundaries** | Medium -- document saves touching both real-time state and persistent storage | Use eventual consistency between real-time layer and persistence. Document storage service owns the write path; real-time engine operates on in-memory state. |

## Candidate Evaluation

| Criterion | Event-Driven | Service-Based | Space-Based |
|-----------|:-----------:|:------------:|:-----------:|
| Performance (priority 1) | **5**/5 | 3/5 | 5/5 |
| Scalability (priority 2) | **5**/5 | 3/5 | 5/5 |
| Fault tolerance (priority 3) | **5**/5 | 4/5 | 3/5 |
| **Characteristic total** | **15** | **10** | **13** |
| Organizational fit | Fair (-1) | Good | Poor (-2) |
| Domain isomorphism | Yes (+1) | No | Partial |
| Anti-pattern risk | Broker/mediator mismatch | Insufficient for real-time needs | Over-engineering, budget mismatch |
| **Adjusted score** | **15** | **10** | **11** |

## Data Architecture

**Data location:** Hybrid -- shared database for document metadata, user data, and permissions (service-based pattern). Dedicated real-time state management (in-memory with event sourcing) for the collaboration engine.

**Communication:** Hybrid -- WebSocket connections for real-time edit propagation (async, event-driven). REST/gRPC for document CRUD, user management, and permissions (synchronous). Message broker (e.g., Redis Pub/Sub or NATS) for inter-service event distribution.

**Consistency model:** Mixed -- Strong consistency for document saves and version snapshots. Eventual consistency for real-time edit propagation across clients (using Operational Transformation or CRDTs for conflict resolution). Eventual consistency for offline-to-online reconciliation.

## Recommendation

**Selected style: Event-Driven Architecture (hybrid with Service-Based structure)**

Specifically: A service-based backbone (4-6 coarse-grained domain services) with event-driven communication for the real-time collaboration layer. This is not pure event-driven nor pure service-based -- it takes the service granularity and operational simplicity of service-based architecture while applying event-driven patterns where the domain demands them.

**Why this style:**
- **Primary reason -- characteristic alignment:** The driving characteristics (performance 5, scalability 5, fault tolerance 5) are the exact strengths of event-driven architecture. No other style scores 15/15 on these three characteristics. The real-time collaborative editing domain is inherently event-driven: every user action is an event that must propagate to all participants. This is textbook domain/architecture isomorphism.
- **Secondary reason -- pragmatic organizational fit:** By wrapping event-driven patterns inside a service-based structure, the team gets manageable service boundaries (4-6 services instead of dozens) while using event patterns only for the collaboration engine where they are unavoidable. The team can learn distributed patterns incrementally rather than being thrown into full event-driven or microservices complexity.

**Trade-offs accepted:**
- Lower simplicity (1) and testability (2) for the event-driven collaboration layer -- mitigated by keeping this complexity isolated to one service boundary and investing in integration testing infrastructure
- Higher cost than monolithic alternatives -- but monoliths cannot meet the scalability requirements
- Team learning curve for event-driven patterns -- mitigated by starting with a well-understood message broker and proven CRDT/OT libraries rather than building from scratch

**Trade-offs rejected (why alternatives were not chosen):**
- **Service-based (pure):** Scores only 3 on performance and 3 on scalability. A collaborative editor with 500K concurrent connections and sub-second latency requirements cannot be served by synchronous request-reply patterns. Service-based is a good backbone but insufficient as the sole architecture for the real-time layer.
- **Space-based:** Scores well on characteristics (13) but organizational fit is poor. Cost (2) exceeds moderate budget. Simplicity (1) and testability (1) are dangerous for a team with no distributed experience. The in-memory data grid model is interesting for this domain but operationally complex to build and maintain.
- **Microservices:** Performance (2) is a critical weakness for real-time collaboration. The inter-service communication overhead directly conflicts with sub-second edit propagation. Additionally, requires mature DevOps the team lacks, and cost (1) exceeds budget.

## Getting Started

1. **Define 4-6 coarse-grained services aligned to bounded contexts:**
   - **Collaboration Service** -- Manages real-time editing sessions, WebSocket connections, edit event propagation, conflict resolution (OT/CRDT). This is the event-driven core.
   - **Document Service** -- Document CRUD, version history, snapshots, offline sync reconciliation. Owns the persistent document store.
   - **User & Auth Service** -- Authentication, authorization, sharing permissions, presence tracking.
   - **Notification Service** -- Email/push notifications for comments, mentions, sharing invitations.
   - Optional: **Media Service** (image/file uploads within documents), **Search Service** (full-text document search).

2. **Build the Collaboration Service with event-driven internals:**
   - Use WebSockets for client-to-server and server-to-client real-time communication.
   - Implement a CRDT-based conflict resolution algorithm (e.g., Yjs or Automerge) -- this handles concurrent edits without a central coordinator and naturally supports offline editing.
   - Use a message broker (Redis Pub/Sub for simplicity, or NATS for higher throughput) to fan out edit events across server instances handling the same document.
   - Event source all edits for the version history (append-only edit log).

3. **Adopt key patterns and practices:**
   - **CRDT over OT:** CRDTs (Conflict-free Replicated Data Types) are better suited for this use case because they handle offline editing naturally -- each client can diverge and merge without a central server. OT requires a central transformation server which becomes a bottleneck and single point of failure.
   - **Event sourcing for document history:** Store every edit as an immutable event. Document versions are reconstructed by replaying events up to a point. Periodically snapshot for performance.
   - **Shared database initially for non-realtime services:** Document metadata, user data, and permissions can share a PostgreSQL database (service-based pattern). This preserves ACID for permission changes and avoids premature data partitioning.
   - **Connection affinity with horizontal scaling:** Route all WebSocket connections for a given document to the same server instance (sticky sessions by document ID). When a single instance isn't enough, use the message broker to sync across instances.

## Migration Path

This is a greenfield system, so no migration is needed. However, the architecture supports incremental build-out:

1. **Phase 1 (Weeks 1-6):** Build as a near-monolith with clear internal module boundaries. Single deployable with the Collaboration module, Document module, and User module as separate packages/modules. Use in-process event bus for edit propagation. This lets the team ship a working product fast.

2. **Phase 2 (Weeks 7-12):** Extract the Collaboration Service as an independent deployment unit. Replace the in-process event bus with Redis Pub/Sub. Add WebSocket horizontal scaling with sticky sessions. This is the first real distributed step.

3. **Phase 3 (Weeks 13-18):** Extract Document Service and User Service as independent deployments. Implement proper offline sync with CRDT merge. Add event sourcing for document versioning. Scale-test to 10,000 concurrent documents.

4. **Phase 4 (Ongoing):** Optimize based on production data. Consider upgrading the message broker to NATS or Kafka if Redis Pub/Sub becomes a bottleneck. Add Search Service if needed. Tune CRDT compaction and snapshot intervals.

This incremental approach lets the team learn distributed patterns progressively rather than facing all complexity at once -- directly addressing the "no distributed experience" constraint while building toward the target architecture.
