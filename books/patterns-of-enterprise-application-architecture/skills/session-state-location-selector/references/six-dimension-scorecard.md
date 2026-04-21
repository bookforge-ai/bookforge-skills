# Six-Dimension Session State Scorecard

Source: *Patterns of Enterprise Application Architecture* — Fowler et al., Ch 17 Session State Patterns

---

## The Six Dimensions

| Dimension | What It Measures | Why It Matters |
|---|---|---|
| **Bandwidth** | Does session data travel over the network on every request? | Client SS sends full state each round-trip — prohibitive for large state |
| **Security** | Is session data protected from client inspection and tampering? | Client-held data can be read and modified without server-side controls |
| **Clustering / Failover** | Can any node handle any request without coordination? | In-memory Server SS breaks on clusters — requires sticky sessions or external store |
| **Responsiveness** | How fast is session state access per request? | Database SS adds a DB roundtrip; Server SS is in-memory; Client SS needs no server lookup |
| **Cancellation** | How easily can an in-progress business transaction be abandoned and rolled back? | Database SS has explicit rows to delete; Server SS clears an object; Client SS requires no server-side action |
| **Dev Effort** | How much infrastructure and code is required? | Server SS is simple for single server; Database SS requires schema design and cleanup; Client SS requires signing/encryption |

---

## Full Scoring Table

| Dimension | Client Session State | Server Session State | Database Session State |
|---|---|---|---|
| **Bandwidth** | HIGH COST — full state in every request/response. Grows with state size. Prohibitive above a few KB. | NONE — only session ID crosses the wire | NONE — only session ID crosses the wire |
| **Security** | RISKY — data is client-accessible. Must sign (HMAC) for tamper detection; encrypt for confidentiality. Re-validate all returning data. | SAFE — data never leaves server | SAFE — data never leaves server |
| **Clustering / Failover** | EXCELLENT — server holds no state. Any node handles any request. Perfect failover. | POOR without external store — in-memory state is node-local. Requires sticky sessions (node-pinning) or external shared store (Redis). GOOD with external store. | GOOD — all nodes read the same DB. No node-pinning. Survives node death. |
| **Responsiveness** | FAST — no server-side lookup needed. Slight overhead from deserializing the cookie/token. | FAST — in-memory access. Sub-millisecond for local map lookup. Adds network latency if external store (Redis ~1ms). | SLOWER — DB roundtrip on every request. Can be reduced by caching the server object, but write cost always paid. |
| **Cancellation** | EASY — client simply does not submit. No server cleanup needed. | CLEAR — discard or invalidate the session object. Cleanup on timeout. | EXPLICIT — delete all rows WHERE session_id = X. Need daemon for abandoned sessions (timeout cleanup). |
| **Dev Effort** | LOW for tiny state (session ID only). Grows rapidly with size — serialization, size management, signing, encryption. | LOW for single server — platform-provided HttpSession. HIGH for clustered — external store setup, serialization, TTL management. | HIGH — schema design (pending vs committed rows), pending data separation logic, all-queries modification or views, timeout daemon. |

---

## Decision Guide by Scenario

### When Client SS wins
- State is ≤ a few KB total
- Stateless server / elastic scaling is the top priority
- State is not sensitive OR will be signed + encrypted
- Failover without any coordination is required (e.g., multi-region, active-active)

### When Server SS wins
- State is large or complex (object graphs, binary data)
- Responsiveness is critical and DB latency is unacceptable
- External session store (Redis) is already available and the team is comfortable with it
- Single-server deployment where simplicity outweighs clustering concerns

### When Database SS wins
- State must survive server restarts, deploys, or node failures
- Deployment is elastic (nodes appear and disappear)
- Cancellation/rollback of the entire business transaction is required
- State overlaps with domain record data (pending orders, draft documents)
- No external cache infrastructure is available and DB access is already fast

---

## Worked Example: E-Commerce on 3 Nodes

**State concern: shopping cart (20 items, ~2KB serialized)**

| Dimension | Score | Notes |
|---|---|---|
| Bandwidth | Acceptable at 2KB — but grows with cart size | Not a blocking concern unless cart grows large |
| Security | Not sensitive — product IDs and quantities | No signing/encryption required for cart contents |
| Clustering | Required — 3-node cluster, auto-scaling | Client SS or Database SS; Server SS needs external store |
| Responsiveness | DB roundtrip acceptable (~5ms) | Not a sub-10ms requirement |
| Cancellation | Required — user can clear cart | Database SS: DELETE WHERE session_id = X |
| Dev Effort | Medium — session_id FK on cart_items table | Already have a database; no new infrastructure |

**Verdict:** Database Session State. Cart items in `cart_items` table with `session_id` FK. Cleanup daemon with 48-hour TTL.

---

## Worked Example: JWT Auth Token (~300 bytes)

**State concern: user ID, roles, JWT expiry**

| Dimension | Score | Notes |
|---|---|---|
| Bandwidth | Negligible — 300 bytes | No concern |
| Security | HIGH sensitivity — roles determine authorization | Must sign (HMAC) + encrypt. HttpOnly cookie required. |
| Clustering | Required — elastic API nodes | Client SS with signed JWT: perfect stateless scaling |
| Responsiveness | Stateless verify — no server lookup | JWT verify is a local HMAC check |
| Cancellation | Logout requires token invalidation | Access token: wait for TTL (15 min). Refresh token: revocation list in Redis |
| Dev Effort | Low — JWT library + HttpOnly cookie | Standard infrastructure |

**Verdict:** Client Session State (HttpOnly signed JWT cookie). Refresh token revocation via Redis set (Server SS with external store).
