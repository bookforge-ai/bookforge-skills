# Fencing Token Pattern

Full reference for Step 4 of the distributed-failure-analyzer skill.

---

## Problem

A distributed lock or lease is meant to ensure that only one node acts as the chosen one (leader, lock-holder) at any time. But any locking scheme based on time-limited leases is vulnerable to process pauses:

1. Client 1 acquires a lease with a 30-second expiry.
2. Client 1 enters a stop-the-world GC pause for 40 seconds.
3. The lease expires. Client 2 acquires the lease.
4. Client 2 begins writing to the shared resource.
5. Client 1 resumes. Its clock has not advanced by 40 seconds (virtualized clock, or monotonic clock from its perspective). It checks `lease.isValid()` — the check passes. It begins writing.
6. Two writers are now active simultaneously. The shared resource is corrupted.

**This bug is documented in the HBase codebase** and is not theoretical.

The client-side lease check is the anti-pattern. The check is not atomic with the protected operation — any pause between them invalidates the check's conclusion.

---

## Solution: The Fencing Token

The lock service issues a **fencing token** with every lock or lease grant. A fencing token is a monotonically increasing integer — each new grant increments the counter. The lock-holder must include its token in every request to the protected resource. The resource tracks the highest token it has processed and rejects any request with a lower token.

### Sequence Diagram

```
Lock service                Client 1                Client 2                Storage
     |                          |                       |                       |
     |<-- acquire lock ---------|                       |                       |
     |-- ok, token=33 --------->|                       |                       |
     |                          |                       |                       |
     |           [Client 1: stop-the-world GC pause — 40 seconds]              |
     |                          |                       |                       |
     |                    lease expired                 |                       |
     |<-- acquire lock ---------|--------------------->|                       |
     |-- ok, token=34 --------------------------------->|                       |
     |                          |                       |-- write, token=34 -->|
     |                          |                       |<-- ok ----------------|
     |                          |                       |                       |
     |           [Client 1 resumes — does not know it was paused]              |
     |                          |                       |                       |
     |                          |-- write, token=33 ----------------------->|
     |                          |<-- REJECTED: token 33 < 34 seen ----------|
```

Client 1's write is rejected. No corruption.

---

## Implementation

### Requirements on the lock service
- Every lock grant returns a token that is strictly greater than all previously issued tokens.
- Tokens need not be sequential (gaps are allowed) — they must only be monotonically increasing.

### Requirements on the resource
- Maintain state: `highest_token_seen`.
- On receiving a write request with token `t`:
  - If `t > highest_token_seen`: accept the write, update `highest_token_seen = t`.
  - If `t <= highest_token_seen`: reject the write with an error indicating stale token.
- This state must be persisted durably (survives crashes).

### Requirements on the client
- Extract the fencing token from the lock service response.
- Pass the token with every request to the protected resource.
- Handle rejections: a rejection means the lock has been superseded. The client should not retry — it should abandon the operation and re-acquire the lock if it still needs access.

---

## ZooKeeper Integration

If ZooKeeper is used as the lock service:

- **`zxid` (ZooKeeper transaction ID)**: a globally monotonically increasing ID assigned to every transaction in ZooKeeper. When a client acquires a lock (creates an ephemeral node), the `zxid` of that transaction serves as the fencing token.
- **`cversion` (child version)**: the version number of a node's children, incremented on each child modification. Also monotonically increasing and usable as a fencing token.

Both are guaranteed to be monotonically increasing and are available from the ZooKeeper API response.

**Example (Java, using Curator):**
```java
InterProcessMutex lock = new InterProcessMutex(client, "/locks/my-resource");
lock.acquire();
long fencingToken = client.getZookeeperClient()
    .getZooKeeper()
    .exists("/locks/my-resource", false)
    .getCzxid();  // creation zxid — use as fencing token

storageService.write(data, fencingToken);  // pass token to resource
lock.release();
```

---

## When the Resource Does Not Natively Support Fencing Tokens

Not all storage services expose a fencing token check API. Options:

### Option 1: Conditional writes (compare-and-swap)
Most databases support conditional updates. Use an object version field:
```sql
-- Write only if version matches what we last read
UPDATE resource SET data = ?, version = version + 1
WHERE id = ? AND version = ?
```
This is not exactly fencing tokens, but achieves a similar effect: stale writers whose version does not match the current version will have their writes rejected.

### Option 2: Encode the token in the resource name
For file storage: include the fencing token in the filename or object key.
- Client acquires lock with token 33: writes to `data-33.json`.
- Client acquires lock with token 34: writes to `data-34.json`.
- Readers always use the file with the highest token number.
This is a workaround, not a full solution — it requires readers to be aware of the convention.

### Option 3: External serialization layer
Wrap the resource access in a proxy or middleware that enforces fencing token ordering before forwarding requests to the underlying resource.

---

## What Fencing Tokens Do NOT Protect Against

Fencing tokens protect against **inadvertent** zombie behavior — a node that does not know it has been declared dead, acting in good faith.

They do NOT protect against:
- A node that **deliberately** sends a faked high fencing token to bypass the check. This is a Byzantine fault.
- A resource that does not enforce the token check (client-side checking alone is insufficient).
- Race conditions at the storage layer if the fencing token check and the write are not atomic.

---

## Relationship to Leases and Heartbeats

A lease (lock with timeout) combined with fencing tokens is a robust pattern:
- The lease ensures the lock is eventually released if the holder crashes (liveness).
- The fencing token ensures that a zombie holder cannot corrupt the resource after expiry (safety).

Heartbeats alone (leader sends keep-alive to remain leader) do not solve the zombie problem — a paused leader stops sending heartbeats, gets declared dead, then resumes and continues acting as leader.

---

## Further Reading
- Kleppmann, "Designing Data-Intensive Applications," Chapter 8, pp. 302–303 (fencing tokens) and p. 295–297 (process pauses and the lease anti-pattern).
- Martin Kleppmann, "How to do distributed locking" (blog post) — expands on why Redlock (Redis-based distributed locking without fencing tokens) is unsafe.
