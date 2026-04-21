---
name: session-state-location-selector
description: "Route session state storage to the right location — Client Session State (cookies, JWT, hidden fields, URL parameters), Server Session State (in-memory or Redis session store), or Database Session State (SQL/NoSQL session table) — based on six dimensions: bandwidth cost, security sensitivity, clustering and failover needs, responsiveness, cancellation requirements, and development effort. Use when designing session management for a new web application, debugging sticky-session or node-pinning scaling problems, deciding between JWT vs server session vs database session, choosing a shared session store for a clustered or elastic deployment, handling shopping carts, multi-step forms, auth context, or edit-in-progress across HTTP requests, or auditing for session bloat or unsigned client session state. Applies to stateless session design, distributed session architecture, and HTTP session management in any language or framework. Relevant keywords: session state, session storage, session location, sticky sessions, JWT vs session, shared session store, stateless session, session management, HTTP session, distributed session, session cookie, server session, database session, Redis session, node-pinning, session scaling, client-side session, server-side session, session bloat."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/session-state-location-selector
metadata: {"openclaw":{"emoji":"🗂️","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors:
      - Martin Fowler
      - David Rice
      - Matthew Foemmel
      - Edward Hieatt
      - Robert Mee
      - Randy Stafford
    chapters:
      - "Chapter 6. Session State (narrative: The Value of Statelessness + Session State)"
      - "Chapter 17. Session State Patterns (Client / Server / Database Session State)"
domain: software-architecture
tags:
  - session-state
  - web-application
  - scalability
  - security
  - design-patterns
  - distributed-systems
  - enterprise-patterns
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: description
      description: "Description of the state that must persist across requests: what data, size estimate, security sensitivity, and deployment topology (single server vs cluster vs elastic)."
    - type: codebase
      description: "Web/session layer source files. Optional — improves anti-pattern detection (node-pinning config, session object size, unencrypted cookie content)."
  tools-required:
    - Read
    - Grep
    - Write
  tools-optional:
    - Glob
    - Edit
  mcps-required: []
  environment: "Enterprise web application. Can work from description alone. Codebase improves anti-pattern detection via Grep on session configuration, load balancer config, and session object definitions."
discovery:
  goal: "Assign each session state concern to the right storage location (Client / Server / Database) and produce a session state design record with rationale, implementation sketch, and anti-pattern warnings."
  tasks:
    - "Challenge whether session state is actually necessary (stateless redesign option)"
    - "Enumerate the distinct state concerns that must persist across requests"
    - "Apply the six-dimension scorecard to each concern"
    - "Route each concern to Client, Server, or Database Session State"
    - "Flag security requirements for Client SS (sign/encrypt); latency requirements for Database SS (cache layer)"
    - "Audit for node-pinning and session-bloat anti-patterns"
    - "Produce a session state design record"
  audience:
    roles:
      - software-architect
      - senior-backend-engineer
      - tech-lead
      - platform-engineer
    experience: intermediate
  when_to_use:
    triggers:
      - "Designing session management for a new web application or API"
      - "Application fails or loses sessions when scaled horizontally or deployed to a new node"
      - "Deciding between JWT and server-side sessions for auth context"
      - "Shopping cart, multi-step form, or edit-in-progress must survive page navigation"
      - "Load balancer config uses sticky sessions (node-pinning symptom)"
      - "Session data is large and causing bandwidth or memory problems"
      - "Sensitive data is stored in cookies without signing or encryption"
      - "Migrating from single-server to clustered or cloud-elastic deployment"
    prerequisites: []
    not_for:
      - "Selecting persistence patterns for record data (use data-source-pattern-selector)"
      - "Selecting web presentation patterns (use web-presentation-pattern-selector)"
      - "Designing transaction isolation or offline locking (use offline-concurrency-strategy-selector)"
  environment:
    codebase_required: false
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: null
    assertion_count: 14
    iterations_needed: null
---

# Session State Location Selector

## When to Use

Use this skill when your web application must remember user state across HTTP requests — shopping carts, multi-step forms, auth context, edits-in-progress, wizard progress, or any data that belongs to a specific user interaction but is not yet committed to the database of record.

The skill routes each state concern to one of three storage locations: **Client Session State** (stored on the client and sent with each request), **Server Session State** (held in server memory or an external cache), or **Database Session State** (persisted as rows in a durable store). Different concerns within the same application can legitimately use different locations.

**Typical triggers:** scaling problems caused by sticky sessions, JWT vs server-session debate, shopping cart durability requirements, auth token design, migrating from a single server to a cluster.

**NOT for:** record data persistence (use `data-source-pattern-selector`), web presentation patterns (use `web-presentation-pattern-selector`), or transaction concurrency (use `offline-concurrency-strategy-selector`).

**Prerequisites:** none. Works with a description of the session data and deployment topology.

---

## Context & Input Gathering

Before routing, gather the following. Ask if not provided.

**Required:**
- What state must persist across requests? List each concern separately (auth token, shopping cart, form progress, user preferences, etc.)
- Estimated size per concern (bytes/KB — critical for Client SS feasibility)
- Security sensitivity of each concern (roles, prices, personal data = high sensitivity)
- Deployment topology: single server, fixed-size cluster, or elastic/auto-scaling?
- Cancellation requirement: does the user need to abandon a multi-step operation and roll it back?

**Observable from codebase:**
- Session configuration files (`application.yml`, `settings.py`, `config/initializers/session_store.rb`, `web.config`)
- Load balancer config for sticky sessions (`JSESSIONID` routing, `ip_hash`, `sticky_cookie`)
- Session object definitions or `HttpSession.setAttribute` calls for size estimation
- Cookie settings (`httpOnly`, `secure`, `sameSite`, signed/encrypted flags)

**Defaults if unknown:**
- Assume cluster topology unless told otherwise (conservative: design for clustering even on single server)
- Assume high security sensitivity for any session data beyond a session ID
- Assume session state exists if there is any multi-request user flow

**Sufficiency check:** proceed when you know the state concerns, their sizes, and the deployment topology.

---

## Process

### Step 1 — Challenge: Can This Be Stateless?

*WHY: Session state is a compromise forced by inherently stateful business transactions. Some apparent session state can be eliminated entirely — pushed into client-initiated request parameters, derived from the database on each request, or encoded in the URL. Stateless server objects can be pooled: 10 objects can serve 100 concurrent users at 10% activity. Eliminating session state is always preferable to choosing its location.*

For each state concern, ask:
- Can this be re-derived from a database query on each request without meaningful performance cost?
- Can this be passed explicitly as a request parameter (URL token, pagination cursor)?
- Is this truly mid-transaction state, or is it already committed data the server can look up?

If any concern can be made stateless: note it as "eliminate — stateless redesign" and remove it from further routing.

---

### Step 2 — Apply the Six-Dimension Scorecard

*WHY: The three session state patterns make different trade-offs across six dimensions. Evaluating each concern on all six dimensions before routing prevents "default to Server SS" anti-patterns and surfaces the actual constraints that drive the decision.*

For each remaining state concern, score it on:

| Dimension | Client SS | Server SS | Database SS |
|---|---|---|---|
| **Bandwidth** | Costly — full state sent per request | Free — session ID only | Free — session ID only |
| **Security** | Risky — client can inspect and tamper | Safe — server-side only | Safe — server-side only |
| **Clustering / Failover** | Excellent — fully stateless | Poor without external store | Good — shared DB |
| **Responsiveness** | Fast — no server lookup | Fast — in-memory | Slower — DB roundtrip |
| **Cancellation** | Easy — client stops submitting | Clear server-side object | Delete rows by session ID |
| **Dev Effort** | Low for tiny state; grows rapidly | Low for single server; high for cluster | High — schema design + cleanup |

Mark each dimension as a **constraint** (hard requirement), **preference** (nice to have), or **not relevant** for this concern.

---

### Step 3 — Route Each Concern

*WHY: Different state concerns have different dimension profiles. Auth tokens are small and security-sensitive but benefit from stateless serving. Shopping carts are medium-sized and need durability. Edit-in-progress may be large and complex. Routing each concern independently produces a better overall design than choosing one location for all session state.*

**Route to Client Session State when:**
- State is small (session ID alone: always Client SS; up to a few KB total: viable with care)
- Stateless server / maximal clustering is the priority
- State is not sensitive OR it will be signed and encrypted on every round-trip
- Failover resilience is critical (state survives node death automatically)

**Route to Server Session State when:**
- State is large or complex (object graphs, binary data, things that don't serialize to small blobs)
- Deployment is a fixed single server or small cluster with an external session store (Redis, Memcached)
- Responsiveness is the priority and a DB roundtrip per request is unacceptable
- Dev simplicity outweighs clustering concerns (and the deployment topology allows it)

**Route to Database Session State when:**
- State must survive server restarts and deploys
- Deployment is elastic (nodes come and go — no permanent home for in-memory state)
- Cancellation/rollback of the whole business transaction is required (delete rows by session ID)
- State concerns overlap with record data (pending orders alongside committed orders)

**Mixing rule:** assigning different concerns to different locations is not only allowed but common and recommended. Examples: session ID → Client SS (required), auth JWT → Client SS (signed cookie), shopping cart → Database SS (durability), UI preferences → Server SS (fast, low risk of loss).

---

### Step 4 — Flag Security, Size, and Latency Requirements

*WHY: Each location has a distinct failure mode that must be addressed in implementation. These are non-optional implementation constraints, not optional enhancements.*

**For Client Session State:**
- Sign and encrypt any data beyond a session ID. Use HMAC signatures for tamper detection; use AES or equivalent encryption for confidentiality. Never send roles, prices, or personally identifiable data without both.
- Re-validate all data returning from the client. Do not trust it.
- Keep within size limits: cookies ≤ 4KB. For more data, use URL parameters for minimal state (session ID, cursor) or hidden fields for form wizard state.
- Set `HttpOnly`, `Secure`, and `SameSite` attributes on session cookies.

**For Server Session State on a cluster:**
- Must use an external session store (Redis, Memcached, or equivalent) accessible to all nodes. In-memory-only Server SS on a cluster requires sticky sessions — a node-pinning anti-pattern (see Step 5).
- Set appropriate TTL on the external store to expire abandoned sessions.

**For Database Session State:**
- Add a session ID column to any table that may hold pending (uncommitted) data, and filter it out of all "record data" queries.
- Implement a cleanup mechanism: a background job or TTL that deletes rows for abandoned sessions.
- Consider a cache layer (Server SS cache backed by Database SS persistence) to absorb the DB roundtrip cost.

---

### Step 5 — Audit for Anti-Patterns

*WHY: Session anti-patterns are common and have serious consequences — scaling failures (node-pinning), bandwidth or memory exhaustion (session bloat), and security vulnerabilities (unsigned client state). Catching them here prevents incidents.*

**Node-Pinning (sticky sessions as a scaling crutch):**
- Symptom: load balancer configured for sticky sessions (`ip_hash`, sticky cookie, `JSESSIONID` routing) with no external session store.
- Consequence: horizontal scaling is compromised (adding nodes doesn't distribute sessions), failover loses sessions (the pinned node dying means session loss), load is uneven.
- Fix: move Server SS to an external shared store (Redis), or move state to Database SS, or move state to Client SS.

**Session Bloat:**
- Symptom: session object contains large lists, entire domain object graphs, cached query results, or binary resources.
- Consequence in Client SS: cookie or hidden-field payload approaching or exceeding size limits on every request. Massive bandwidth overhead.
- Consequence in Server SS: high memory pressure per active session; slow serialization for clustering/failover.
- Fix: store only keys and small scalar values in the session. Re-query the database for object graphs when needed. Move large state to Database SS with explicit pending rows.

**Unsigned/Unencrypted Client Session State:**
- Symptom: session cookie or hidden field contains roles, prices, user IDs, or other sensitive values in plaintext or base64 without HMAC or encryption.
- Consequence: user can inspect the data (disclosure) or modify it (privilege escalation, price manipulation).
- Fix: sign with HMAC (tamper detection) and encrypt (confidentiality). Use a platform-provided signed/encrypted cookie store (Rails `encrypted_cookie_store`, Django signed cookies, Express `cookie-session` with `secret`).

**Server Session State on a Cluster Without External Store:**
- Symptom: multi-node deployment + in-process session memory.
- Consequence: requests routed to a different node find no session → random authentication failures, lost cart state, broken wizard flows.
- Fix: same as node-pinning — external shared session store.

---

### Step 6 — Produce the Session State Design Record

*WHY: A written record of the routing decisions and rationale enables team alignment, review, and future change without re-litigating the decision from scratch.*

Write a session state design record (see Outputs).

---

## Inputs

- List of session state concerns with: data description, estimated size, security sensitivity
- Deployment topology: single server / fixed cluster / elastic auto-scaling
- Cancellation / rollback requirements
- Framework and session infrastructure in use (optional — improves specificity of recommendations)
- Codebase session configuration and object definitions (optional — enables anti-pattern detection)

---

## Outputs

### Session State Design Record

```
## Session State Design: [System Name]

### Deployment Context
- Topology: [single server | fixed cluster | elastic]
- Framework / runtime: [e.g., Express + Node.js, Django, Spring Boot]
- Current session infrastructure: [e.g., HttpSession in-memory, Redis, none]

### Statelessness Opportunities
- [Concern A]: [Can be eliminated — re-derive from DB on each request]
- [Concern B]: [Must remain stateful — mid-transaction edit]

### Routing Decisions

| Concern | Location | Rationale | Size | Security Controls |
|---|---|---|---|---|
| Session ID | Client SS | Always client — just one token | ~32 bytes | HttpOnly, Secure, SameSite=Strict |
| Auth context (roles, user ID) | Client SS | Signed JWT in HttpOnly cookie — stateless, cluster-friendly | ~300 bytes | HMAC-signed + encrypted |
| Shopping cart | Database SS | Durability + cluster support; cancelable by deleting rows | Variable | Server-side only |
| Multi-step form progress | Server SS | Large object, short-lived, Redis external store | ~10KB | External Redis store |

### Implementation Notes
- [Concern]: [specific implementation sketch]
- Auth JWT: use short-lived access token (15 min) + HttpOnly refresh token cookie; validate on every request
- Shopping cart: `cart_items` table with `session_id` FK; cleanup daemon runs every 30 min deleting rows with last_activity > 2h

### Anti-Pattern Status
- Node-pinning: [NOT PRESENT | PRESENT — fix required: ...]
- Session bloat: [NOT PRESENT | PRESENT — fix required: ...]
- Unsigned Client SS: [NOT PRESENT | PRESENT — fix required: ...]

### Open Questions
- [Any unresolved decisions or constraints that need clarification]
```

---

## Key Principles

**1. Stateless by default, stateful only where the business transaction requires it.**
Server objects that hold no inter-request state can be pooled and freely load-balanced. Session state forces one-to-one affinity or external coordination. Start by questioning whether the state is genuinely necessary.

**2. Client Session State scales perfectly but costs bandwidth and security diligence.**
Every byte stored on the client is sent on every request. Works well for a session ID or a signed JWT. Becomes a liability for shopping cart contents or form state measured in kilobytes. The security contract is firm: sign everything, encrypt anything sensitive, re-validate everything on return.

**3. Server Session State is simple but requires an external store for any clustered deployment.**
In-memory Server Session State is the simplest programming model. It breaks the moment there is more than one server node. The fix (external Redis/Memcached store) is straightforward but must be done proactively — retrofitting it after a scaling incident is painful. Never accept sticky sessions as a substitute for a shared store.

**4. Database Session State is the most durable and cluster-friendly but has real costs.**
Every request pays a database roundtrip. Schema design must carefully separate pending session rows from committed record data, or queries for record data will accidentally include in-progress session data. A background cleanup mechanism for abandoned sessions is not optional.

**5. Mix patterns per concern, not per application.**
A session ID belongs in Client SS (always). Auth context likely belongs in Client SS (small, signed JWT). A shopping cart belongs in Database SS (durable, cancelable). Edit-in-progress on a large domain object belongs in Server SS (complex, short-lived). Forcing all session state into one location to avoid mixing is a false simplification.

**6. The six dimensions are constraints, not preferences.**
Clustering/failover is not optional for elastic deployments. Security controls are not optional for sensitive data. Size limits are not optional for Client SS. Evaluate all six before routing — skipping a dimension is how node-pinning and session bloat enter production.

---

## Examples

### Example 1 — E-Commerce on an Elastic Cluster

**Scenario:** Online retailer with variable traffic (3x on sale days). Three-node cluster behind a load balancer with auto-scaling.

**Trigger:** New feature: multi-item shopping cart that must survive page refresh and browser close. Auth is already in-place using a session cookie.

**Process:**
1. Challenge statelessness: cart contents cannot be derived without the user's choices — genuinely stateful.
2. Scorecard: cart is medium-sized (~5–50 items), not security-sensitive (product IDs and quantities), needs durability (survive node death), needs cancellation (user can empty cart), cluster topology.
3. Routing: auth session ID → Client SS (existing, HttpOnly cookie). Cart → Database SS (elastic cluster + durability + cancellation). UI preferences → Client SS (small, not sensitive, fine to lose on client failure).
4. Security: session ID cookie: HttpOnly + Secure + SameSite=Strict. No sensitive data in Client SS beyond signed session ID.
5. Anti-pattern audit: confirm load balancer is NOT using sticky sessions for cart requests. Add `session_id` column to `cart_items` table. Implement background cleanup for abandoned carts (TTL 48h).

**Output:** Design record routing cart to Postgres `cart_items` table with session_id FK. Auth cookie stays Client SS. No node-pinning. Cleanup daemon specified.

---

### Example 2 — Multi-Step Insurance Policy Editor (LOB App, Single Server)

**Scenario:** Line-of-business app for insurance agents. Single application server (no clustering). Agents edit complex policies across 6 wizard steps over 10–20 minutes. Policies have 80+ fields and nested objects.

**Trigger:** Current approach stores the entire partially-edited policy as a Java serialized object in `HttpSession`. Server runs out of memory under load.

**Process:**
1. Challenge statelessness: multi-step wizard with partial validation — genuinely stateful.
2. Scorecard: state is large (serialized policy graph ~200KB), not security-sensitive to external exposure (internal LOB app), single server (no clustering concern), slow serialization causing memory pressure.
3. Session-bloat anti-pattern detected: 200KB per active session in memory is the root cause.
4. Routing options: Database SS (persist pending policy rows with `session_id` field) is preferable — survives server restart, eliminates memory pressure, makes partial edits queryable (admin can see in-progress edits). Client SS is ruled out (200KB far exceeds cookie limits).
5. Implementation: add `is_pending` flag and `session_id` column to policy and policy_line tables. All "committed policies" queries add `WHERE session_id IS NULL`. Cleanup daemon deletes rows with `session_id IS NOT NULL AND last_activity < NOW() - INTERVAL '4 hours'`.
6. Note: single server means Server SS with external Redis is also viable as a simpler migration step. Document the trade-off.

**Output:** Design record recommending Database SS for policy editor state. Session-bloat anti-pattern resolved. Migration path from current HttpSession noted.

---

### Example 3 — SPA with JWT Authentication

**Scenario:** React SPA with a Node.js/Express API backend. Team is debating JWT in localStorage vs JWT in HttpOnly cookie vs server-side session.

**Trigger:** Security review flagged localStorage JWT as vulnerable to XSS. Team wants guidance on the session state trade-off.

**Process:**
1. Challenge statelessness: auth context must persist — genuinely stateful.
2. Auth concern: small (user ID, roles, expiry ~300 bytes), security-sensitive (roles determine authorization), cluster topology (multiple API nodes behind a load balancer).
3. Scorecard: Client SS (HttpOnly cookie with signed JWT) wins on clustering (stateless API nodes), responsiveness (no server lookup), and size (tiny). Beats Server SS on clustering; beats Database SS on latency.
4. Security controls: HttpOnly cookie (XSS cannot read it), Secure flag, SameSite=Strict (CSRF protection). JWT signed with HMAC-SHA256. Short TTL (15 min access token) + longer HttpOnly refresh token (7 days). Re-validate JWT signature on every request.
5. Audit: localStorage flagged as anti-pattern for auth tokens — XSS exposure. Recommend HttpOnly cookie.
6. If refresh tokens need server-side revocation: store refresh token IDs in a Redis set per user (Server SS with external store). On logout, delete the Redis entry. Access tokens remain stateless until expiry.

**Output:** Design record: access JWT in HttpOnly cookie (Client SS). Refresh token revocation list in Redis (Server SS with external store). No localStorage. Anti-pattern (localStorage JWT) flagged and resolved.

---

## References

- `references/six-dimension-scorecard.md` — Full scoring table with worked examples for all three patterns
- `references/anti-pattern-detection-checklist.md` — Node-pinning, session-bloat, unsigned Client SS: detection criteria and fixes
- `references/pending-data-schema-patterns.md` — Pending field, pending tables, and session ID column approaches for Database SS
- `references/modern-session-store-map.md` — Fowler's patterns mapped to Redis, Postgres, DynamoDB, JWT, and framework-native session stores

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

---

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-web-presentation-pattern-selector`
- `clawhub install bookforge-enterprise-architecture-pattern-stack-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
