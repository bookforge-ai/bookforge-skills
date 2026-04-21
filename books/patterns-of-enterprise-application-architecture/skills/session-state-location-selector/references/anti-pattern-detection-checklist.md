# Anti-Pattern Detection Checklist: Session State

Source: *Patterns of Enterprise Application Architecture* — Fowler et al., Ch 6 + Ch 17

---

## Anti-Pattern 1: Node-Pinning (Sticky Sessions as a Scaling Crutch)

### What It Is
Using load balancer sticky sessions (server affinity) to route each user's requests to the same server node, instead of using a shared external session store. Treated as a "solution" to in-memory Server Session State on a cluster.

### Fowler's Term
"Server affinity" — Fowler identifies this as a consequence of basic in-memory Server Session State: "it also assumes that there's only one application server — that is, no clustering."

### Detection Signals
- Load balancer config contains: `sticky_sessions`, `ip_hash`, `JSESSIONID` cookie routing, `sticky_cookie`, `session persistence`, or equivalent sticky settings
- No external session store (Redis, Memcached, shared DB) configured
- Application server session data is stored in local JVM heap or local process memory
- Cluster size is fixed (no auto-scaling) — elastic scaling would break sticky sessions

### Consequences
- Horizontal scaling is compromised: adding nodes does not distribute existing sessions
- Failover loses sessions: when a pinned node dies, its sessions die with it
- Uneven load distribution: users with active sessions stay on specific nodes regardless of load
- Elastic auto-scaling is impossible: new nodes can't handle pinned sessions

### Fix
Choose one:
1. Move to external shared session store (Redis, Memcached) — remains Server SS but cluster-safe
2. Move to Database Session State — all nodes access the same DB
3. Move to Client Session State — signed JWT in HttpOnly cookie; fully stateless

---

## Anti-Pattern 2: Session Bloat

### What It Is
Storing large objects — entire domain model graphs, cached query results, lists of business objects, binary resources — in the session store rather than keeping the session minimal (IDs and small scalars).

### Fowler's Reference
Fowler notes Client SS issues grow "exponentially with the amount of data involved" and cites bandwidth cost and storage limits as the binding constraints.

### Detection Signals (Client SS)
- Session cookie approaching or exceeding 4KB
- Hidden form fields containing serialized object graphs
- JWT payload over ~1KB
- Session data includes arrays of objects, nested structures, or binary data

### Detection Signals (Server SS)
- Session object graph > ~50KB per user
- Session contains cached query result sets
- High memory pressure on application server correlated with number of active users
- Slow session serialization/deserialization during clustering or passivation

### Consequences (Client SS)
- Cookie exceeds 4KB browser limit — state silently truncated or cookie rejected
- Every request carries multi-KB payload — bandwidth overhead scales with active users
- Serialization/deserialization cost per request

### Consequences (Server SS)
- Memory pressure: heap exhausted under moderate concurrent user count
- Slow serialization for external store sync
- Large BLOB in session table if persisting to DB

### Fix
- Store only keys (IDs, small scalars) in the session
- Re-query the database for full objects when needed — don't cache them in the session
- Move large state concerns to Database Session State with explicit pending rows
- If state must be large, ensure Server SS with an appropriately sized external Redis instance and memory limits

---

## Anti-Pattern 3: Unsigned/Unencrypted Client Session State

### What It Is
Storing sensitive data (user IDs, roles, prices, permissions, personal data) in client-side storage (cookies, hidden fields, URL parameters, localStorage) without cryptographic signing or encryption.

### Fowler's Warning
"Realize that cookies are no more secure than anything else, so assume that prying of all kinds can happen." And: "Fingers can pry too, so don't assume that what got sent out is the same as what gets sent back. Any data coming back will need to be completely revalidated."

### Detection Signals
- Cookie value is plaintext, base64-encoded (not encrypted), or JWT without signature verification
- Hidden form fields contain role names, prices, discount amounts, or user IDs
- URL parameters contain authorization-relevant data
- JWT `alg: none` or weak signing key
- No server-side re-validation of returned client data

### Consequences
- **Tampering:** user changes their role to `admin`, changes a price to `0.01`, or changes a discount to `100%`
- **Disclosure:** user reads their session data or another user's data if session ID is predictable
- **Session hijacking:** attacker reads auth token from non-HttpOnly cookie via XSS

### Fix
For tamper detection: sign with HMAC (e.g., HMAC-SHA256). Verify signature on every request before trusting any value.
For confidentiality: encrypt the payload (AES-GCM). Use authenticated encryption to get both properties in one operation.
Platform options:
- Rails: `encrypted_cookie_store` (AES-GCM + HMAC automatically)
- Django: signed cookies (`SESSION_COOKIE_SIGNED = True`) or encrypted with django-encrypted-cookie-session
- Express: `cookie-session` with `secret` (HMAC-signed) or Iron (encrypted)
- JWT: use RS256 or HS256 with a strong secret; never use `alg: none`; set short TTL (15 min)

Always: set `HttpOnly` (XSS cannot read), `Secure` (HTTPS only), `SameSite=Strict` or `Lax` (CSRF protection).

---

## Anti-Pattern 4: Server Session State on a Cluster Without External Store

### What It Is
Running multiple application server nodes with in-process (local heap) Server Session State and no shared session store, relying on luck or rare sticky-session misconfiguration rather than a proper architectural fix.

### Detection Signals
- Multi-node deployment (Kubernetes, Docker Swarm, multiple EC2 instances, etc.)
- Session stored in local application process memory (e.g., Express `memorystore`, Django `django.contrib.sessions.backends.cache` with a local cache)
- Random authentication failures or "session not found" errors reported by users
- Errors are intermittent and correlate with deployments or node restarts

### Consequences
- Users get random 401 / 403 / session-not-found errors when load balanced to a different node
- Session loss on any node restart or redeploy
- Debugging is painful — intermittent, hard to reproduce in single-node test environments

### Fix
Same as node-pinning fix: external shared session store. Redis is the standard choice for Server SS on a cluster.

---

## Quick Detection Table

| Signal in Codebase | Anti-Pattern | Severity |
|---|---|---|
| `ip_hash` / `sticky_sessions` in LB config | Node-pinning | High |
| `HttpSession.setAttribute("cart", cartObject)` with full object | Session Bloat | Medium |
| Session cookie > 4KB | Session Bloat (Client SS) | High |
| Cookie without `HttpOnly` flag containing auth data | Unsigned/Unencrypted Client SS | Critical |
| JWT with `alg: none` or base64-only encoding | Unsigned/Unencrypted Client SS | Critical |
| `MemoryStore` session backend + Kubernetes deployment | Server SS on cluster without external store | High |
| Hidden field with `role=admin` or `price=99.99` | Unsigned/Unencrypted Client SS | Critical |
