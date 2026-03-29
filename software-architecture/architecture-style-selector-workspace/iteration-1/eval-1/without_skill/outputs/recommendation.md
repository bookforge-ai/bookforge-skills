# Architecture Recommendation: Real-Time Collaborative Document Editor

## 1. Problem Summary

Build a real-time collaborative document editor (Google Docs-like) supporting:

- **Concurrent editing**: Multiple users editing the same document simultaneously
- **Real-time sync**: Changes propagate to all clients instantly
- **Document versioning**: Full history with ability to review/restore
- **Offline editing**: Users can work without connectivity and sync when reconnected
- **Scale**: Up to 10,000 concurrent active documents, 5-50 users per document
- **Team**: 12 developers, experienced in web apps, no distributed systems background
- **Budget**: Moderate

---

## 2. Architecture Style Analysis

### 2.1 Candidate Styles Considered

I evaluated the following architecture styles against the requirements:

| Style | Fit | Verdict |
|-------|-----|---------|
| Monolithic | Simplest to build, but poor real-time support and scaling limits | Partial fit |
| Microservices | Operational overhead too high for team size and experience | Poor fit |
| Event-Driven Architecture | Strong fit for real-time propagation of edits | Strong fit |
| Space-Based Architecture | Designed for high-concurrency in-memory workloads | Strong fit |
| Service-Based Architecture | Middle ground between monolith and microservices | Good fit |
| Peer-to-Peer (CRDT-native) | Excellent for offline and conflict resolution, complex to build | Partial fit |

### 2.2 Detailed Evaluation

#### Monolithic Architecture
- **Pros**: Simple deployment, easy debugging, fast initial development, low operational burden.
- **Cons**: Real-time WebSocket management at scale becomes a bottleneck in a single process. Horizontal scaling requires sticky sessions or external pub/sub. No natural separation between document state management, sync engine, and API concerns.
- **Rating**: 4/10 -- too limiting for the real-time collaborative core.

#### Microservices Architecture
- **Pros**: Independent scaling of services, technology diversity, fault isolation.
- **Cons**: Massive operational overhead (service mesh, distributed tracing, API gateways). A team of 12 with no distributed systems experience would spend most of their time on infrastructure rather than product. Network latency between services degrades real-time performance. Eventual consistency between services is hard to reason about.
- **Rating**: 3/10 -- overengineered for this team and problem.

#### Event-Driven Architecture
- **Pros**: Natural fit for propagating document changes as events. Decouples producers (editing clients) from consumers (other clients, versioning system, search indexing). Supports replay for versioning. Enables offline sync via event queues.
- **Cons**: Event ordering is critical for document editing and requires careful design. Debugging event flows is harder than request/response. Requires a message broker (adds infrastructure).
- **Rating**: 8/10 -- excellent conceptual fit for the real-time sync problem.

#### Space-Based Architecture
- **Pros**: Designed exactly for high-concurrency, low-latency workloads with shared mutable state. In-memory data grids handle document state naturally. Built-in replication handles multi-user access. Scales by adding processing units.
- **Cons**: Requires specialized infrastructure (in-memory data grids like Hazelcast, Apache Ignite). Complex to operate. Team has no distributed systems experience. Higher infrastructure cost. Fewer developers familiar with this pattern.
- **Rating**: 5/10 -- architecturally elegant but operationally too complex for this team.

#### Service-Based Architecture
- **Pros**: Coarser-grained than microservices (4-8 services instead of dozens). Manageable for a 12-person team. Each service can own a clear domain. Shares a database where appropriate, reducing distributed data problems. Easier deployment than microservices.
- **Cons**: Less granular scaling than microservices. Still requires some distributed systems knowledge for the real-time component. Service boundaries need careful design.
- **Rating**: 7/10 -- practical middle ground, but needs augmentation for real-time concerns.

#### Peer-to-Peer (CRDT-native)
- **Pros**: CRDTs solve conflict resolution mathematically. Offline-first by design. No central server needed for conflict resolution. Growing ecosystem (Yjs, Automerge).
- **Cons**: Pure P2P is hard to secure, authorize, and persist. CRDTs have memory overhead. Full P2P architecture is complex. However, CRDTs as a *data structure choice* within another architecture are excellent.
- **Rating**: 5/10 as an architecture style, but 9/10 as a technology choice within another architecture.

---

## 3. Recommended Architecture

### Primary Style: Service-Based Architecture + Event-Driven Communication

**Use a service-based architecture with 4-5 coarse-grained services, connected via event-driven messaging for real-time sync, and CRDT-based conflict resolution for the collaborative editing core.**

This is a hybrid approach that combines:
1. **Service-Based Architecture** for overall system organization (manageable for the team)
2. **Event-Driven patterns** for real-time document synchronization
3. **CRDT data structures** (via Yjs or Automerge) for conflict-free concurrent editing and offline support

### 3.1 Service Decomposition

```
┌─────────────────────────────────────────────────────────────┐
│                        API Gateway                          │
│              (Auth, Rate Limiting, Routing)                  │
└─────────┬──────────┬──────────────┬────────────┬────────────┘
          │          │              │            │
    ┌─────▼────┐ ┌───▼─────┐ ┌─────▼──────┐ ┌──▼──────────┐
    │ Document │ │  Sync   │ │  Version   │ │   User &    │
    │ Service  │ │ Service │ │  Service   │ │ Presence    │
    │          │ │         │ │            │ │  Service    │
    │ CRUD,    │ │WebSocket│ │ Snapshots, │ │ Auth,       │
    │ Storage, │ │ Hub,    │ │ Diff,      │ │ Permissions,│
    │ Search,  │ │ CRDT    │ │ History,   │ │ Cursors,    │
    │ Metadata │ │ Merge   │ │ Restore    │ │ Awareness   │
    └────┬─────┘ └────┬────┘ └─────┬──────┘ └──────┬──────┘
         │            │            │                │
    ┌────▼────────────▼────────────▼────────────────▼───────┐
    │                   Event Bus (Redis Streams)            │
    └───────────────────────────┬────────────────────────────┘
                                │
    ┌───────────────────────────▼────────────────────────────┐
    │              Shared Data Layer                          │
    │   PostgreSQL (documents, users, metadata)               │
    │   Redis (pub/sub, presence, caching)                    │
    │   Object Storage (snapshots, large assets)              │
    └────────────────────────────────────────────────────────┘
```

### 3.2 Service Responsibilities

**Document Service** (3-4 developers)
- Document CRUD operations (create, read, update, delete)
- Document metadata and permissions storage
- Full-text search indexing
- Folder/workspace organization
- REST API for non-real-time operations

**Sync Service** (4-5 developers -- this is the core)
- WebSocket connection management
- CRDT state management using **Yjs** (battle-tested, MIT licensed)
- Operation transformation and broadcast
- Conflict resolution (handled automatically by CRDT)
- Offline edit queue processing and reconciliation
- Document state persistence (periodic snapshots of CRDT state)

**Version Service** (2 developers)
- Periodic snapshot creation from CRDT state
- Version history storage and retrieval
- Diff computation between versions
- Point-in-time restore capability
- Retention policies and cleanup

**User & Presence Service** (2 developers)
- Authentication and authorization
- Real-time presence (who is viewing/editing)
- Cursor position broadcasting
- User permissions per document
- Activity tracking

### 3.3 Real-Time Sync Flow (The Critical Path)

```
Client A edits         Client B sees change
    │                        ▲
    ▼                        │
[Yjs CRDT local]      [Yjs CRDT local]
    │                        ▲
    ▼                        │
[WebSocket]            [WebSocket]
    │                        ▲
    ▼                        │
[Sync Service]──────►[Redis Pub/Sub]
    │                        │
    ▼                        │
[Persist CRDT      Broadcast to all
 state to DB]      connected clients
```

**How it works:**

1. Client A makes an edit. Yjs generates a compact binary update (delta).
2. The delta is sent via WebSocket to the Sync Service.
3. The Sync Service:
   - Applies the update to the server-side Yjs document (authoritative copy)
   - Publishes the update to Redis Pub/Sub (channel = document ID)
   - Periodically persists the full CRDT state to PostgreSQL
4. All other Sync Service instances subscribed to that document channel receive the update.
5. They forward it via WebSocket to their connected clients.
6. Client B's local Yjs instance merges the update automatically -- no conflicts possible due to CRDT properties.

**Latency target**: < 100ms from edit to other clients seeing it (achievable with this design).

### 3.4 Offline Editing Support

CRDTs make offline editing straightforward:

1. **Going offline**: Client continues editing against local Yjs document state. All operations are stored locally (IndexedDB).
2. **Reconnecting**: Client sends accumulated Yjs updates to the Sync Service. The CRDT merge algorithm guarantees convergence regardless of edit ordering.
3. **No manual conflict resolution needed**: Unlike OT (Operational Transformation), CRDTs guarantee that all clients converge to the same state regardless of the order operations arrive.

This is a major advantage over OT-based systems (which Google Docs uses internally) -- OT requires a central server to order operations, making offline support much harder.

### 3.5 Document Versioning Strategy

```
Continuous CRDT Updates ──► Periodic Snapshots ──► Named Versions
(every keystroke)           (every 5 min or          (user-triggered
                             100 operations)          "save version")
```

- **CRDT update log**: Every change is captured. Used for real-time sync.
- **Snapshots**: Full serialized CRDT state saved every N minutes. Enables fast document loading (load snapshot + replay recent updates).
- **Named versions**: User-triggered save points. Stored as snapshots with metadata (name, description, author).
- **Diff computation**: Compare any two snapshots using Yjs's built-in diff capabilities.
- **Restore**: Load a snapshot, create a new CRDT update that transforms current state to the snapshot state, broadcast to all clients.

### 3.6 Scaling Strategy

**Per-document scaling** (not global):

| Component | Scaling Approach |
|-----------|-----------------|
| Sync Service | Horizontally scaled. Each instance handles N documents. Redis Pub/Sub coordinates between instances. |
| Document Service | Standard horizontal scaling behind load balancer. |
| Version Service | Scales independently. Snapshot creation is async. |
| WebSocket connections | Each Sync Service instance handles ~2,000-5,000 connections. At 10,000 docs x 25 avg users = 250K connections, need ~50-125 Sync Service instances. |
| PostgreSQL | Single primary with read replicas. Document data is naturally partitioned by document ID. |
| Redis | Redis Cluster for pub/sub at scale. |

**Back-of-envelope math:**
- 10,000 concurrent documents x 25 average users = 250,000 WebSocket connections
- Average edit rate: ~2 operations/second/user = 500,000 ops/second total
- Each Yjs update is ~50-200 bytes, so ~25-100 MB/s of sync traffic
- This is well within the capacity of a Redis Cluster + horizontally scaled Sync Service

---

## 4. Technology Stack Recommendations

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **CRDT Library** | **Yjs** | Most mature, best performance, excellent docs, MIT license. Used by Notion, Evernote, others. |
| **WebSocket Server** | **Node.js + ws** (or Hocuspocus) | Hocuspocus is a Yjs-specific WebSocket backend with batteries included. Node.js handles high-concurrency I/O well. |
| **API Framework** | **Node.js + Express/Fastify** or **Python + FastAPI** | REST APIs for non-real-time operations. Use what the team knows. |
| **Message Broker** | **Redis Streams / Pub/Sub** | Low latency, simple to operate, sufficient for this scale. |
| **Primary Database** | **PostgreSQL** | CRDT state stored as binary blobs. Metadata in relational tables. |
| **Client Storage** | **IndexedDB** (via y-indexeddb) | Offline CRDT state persistence in the browser. |
| **Object Storage** | **S3 / GCS** | Version snapshots, document attachments. |
| **Frontend** | **React + TipTap** (or ProseMirror) | TipTap has native Yjs integration. Rich text editing with CRDT sync out of the box. |

**Why Yjs over Automerge?**
- Yjs is 10-100x faster in benchmarks for text editing operations
- Smaller binary encoding (critical for network efficiency)
- Larger ecosystem of editor integrations (TipTap, ProseMirror, Monaco, CodeMirror)
- Hocuspocus provides a production-ready server implementation

---

## 5. Key Architecture Decisions

### 5.1 CRDT over Operational Transformation (OT)

| Factor | CRDT (Yjs) | OT (Google Docs style) |
|--------|-----------|----------------------|
| Conflict resolution | Automatic, mathematical guarantee | Requires central server ordering |
| Offline support | Native -- merge on reconnect | Very hard -- need to buffer and transform |
| Server complexity | Simpler -- just relay updates | Complex -- must transform operations |
| Team learning curve | Lower -- use Yjs library | Higher -- must implement OT algorithm |
| Performance at scale | Excellent | Good but server becomes bottleneck |

**Decision: Use CRDTs.** Given the team's lack of distributed systems experience, CRDTs are safer -- the library handles the hard parts.

### 5.2 Service-Based over Microservices

- 4-5 services is manageable for 12 developers (3-4 per service)
- Services share a database where it makes sense (Document + Version services both access PostgreSQL)
- No service mesh needed -- direct HTTP calls + Redis pub/sub
- Can evolve toward microservices later if needed

### 5.3 Shared Database with Service Ownership

- Each service "owns" its tables but they live in the same PostgreSQL instance
- Sync Service owns: `crdt_states`, `crdt_updates`
- Document Service owns: `documents`, `folders`, `permissions`
- Version Service owns: `snapshots`, `version_history`
- User Service owns: `users`, `sessions`
- This avoids distributed transactions while maintaining logical separation

---

## 6. Risk Analysis and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| CRDT memory usage grows large for long-lived documents | Medium | High | Implement periodic garbage collection / compaction of CRDT state. Yjs supports this natively. |
| WebSocket connection management at scale | Medium | High | Use Hocuspocus (handles reconnection, auth, scaling). Add connection pooling. |
| Team unfamiliar with WebSocket programming | High | Medium | Start with Hocuspocus (abstracts WebSocket details). Invest in training sprint. |
| Offline sync produces unexpected merges | Low | Medium | CRDTs guarantee convergence. Add visual diff review for large offline edits. |
| Redis becomes single point of failure | Low | High | Redis Cluster with automatic failover. Redis Sentinel for monitoring. |
| PostgreSQL CRDT blob storage becomes large | Medium | Medium | Archive old snapshots to object storage. Keep only recent CRDT state in PostgreSQL. |
| Complexity of deploying 4-5 services | Medium | Medium | Start as a modular monolith, extract services as the team gains confidence. Use Docker Compose locally, Kubernetes in production. |

---

## 7. Implementation Roadmap

### Phase 1: Foundation (Weeks 1-4)
- Set up project structure, CI/CD, development environment
- Implement basic document CRUD (Document Service)
- Integrate Yjs + TipTap for single-user editing in the browser
- Set up PostgreSQL schema and basic persistence

### Phase 2: Real-Time Collaboration (Weeks 5-8)
- Deploy Hocuspocus as the Sync Service
- Implement WebSocket-based real-time sync between multiple clients
- Add Redis Pub/Sub for multi-instance sync
- Implement presence (cursors, user awareness)

### Phase 3: Offline & Versioning (Weeks 9-12)
- Add IndexedDB persistence for offline support
- Implement reconnection and sync reconciliation
- Build version snapshot system
- Add version history UI and restore functionality

### Phase 4: Scale & Harden (Weeks 13-16)
- Load testing at target scale (10K documents, 250K connections)
- Performance optimization (CRDT compaction, connection pooling)
- Monitoring and observability (metrics, alerts, dashboards)
- Security hardening (auth, rate limiting, input validation)

---

## 8. Alternatives Considered but Rejected

### Firebase Realtime Database / Firestore
- **Why considered**: Managed real-time sync, offline support, minimal backend code.
- **Why rejected**: Vendor lock-in. Limited conflict resolution (last-write-wins, not CRDT). Expensive at 250K concurrent connections. Limited query capabilities for document search.

### ShareDB (OT-based)
- **Why considered**: Mature OT library for Node.js. Used in production systems.
- **Why rejected**: OT is inherently more complex than CRDTs. Offline support requires significant additional engineering. Server-dependent ordering creates a scaling bottleneck.

### Pure Peer-to-Peer (WebRTC + CRDTs)
- **Why considered**: No server bottleneck. True real-time.
- **Why rejected**: Cannot enforce authorization. No server-side persistence. NAT traversal issues. Difficult to implement presence and versioning.

---

## 9. Summary

| Aspect | Recommendation |
|--------|---------------|
| **Architecture Style** | Service-Based + Event-Driven hybrid |
| **Number of Services** | 4-5 (Document, Sync, Version, User/Presence) |
| **Conflict Resolution** | CRDT via Yjs (not OT) |
| **Real-Time Transport** | WebSockets via Hocuspocus |
| **Inter-Service Messaging** | Redis Pub/Sub + Streams |
| **Offline Support** | Yjs + IndexedDB (y-indexeddb) |
| **Database** | PostgreSQL (shared, with service-owned tables) |
| **Editor Framework** | TipTap + Yjs integration |
| **Deployment** | Start with Docker Compose, evolve to Kubernetes |
| **Timeline** | ~16 weeks to production-ready |

This architecture balances **technical correctness** (CRDTs solve the hardest problem mathematically), **team capability** (service-based is manageable, Yjs/Hocuspocus abstract complexity), and **budget constraints** (open-source stack, moderate infrastructure). The team can start with a modular monolith and extract services incrementally as they gain confidence.
