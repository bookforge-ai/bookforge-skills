# Quorum Calculator

Use this reference when configuring leaderless replication (Cassandra, Riak, Voldemort, DynamoDB) to determine the correct values of n, w, and r for your availability and consistency requirements.

## The Core Formula

```
w + r > n
```

- **n** = replication factor (total number of nodes that store each key)
- **w** = write quorum (number of nodes that must acknowledge a write for it to succeed)
- **r** = read quorum (number of nodes queried on each read; freshest value returned)

When w + r > n, the write set and read set must overlap by at least one node. That overlapping node has the most recent write. This guarantees the read returns the latest value — provided no concurrent writes are happening and no sloppy quorum is in use.

## Worked Examples

### Standard balanced configuration (n=3, w=2, r=2)

```
w + r = 4 > n = 3  ✓
Fault tolerance: 1 node can be unavailable (writes need 2/3; reads need 2/3)
Staleness risk: Low — any read will hit at least 1 node with the latest write
Space cost: 3x data stored
```

Best for: General-purpose workloads where both availability and consistency matter. This is the default for most Cassandra deployments.

### Write-heavy, reads can be stale (n=3, w=1, r=2)

```
w + r = 3 = n  ✗ (quorum condition not strictly satisfied)
Fault tolerance: 2 nodes can be unavailable for writes; 1 for reads
Staleness risk: High — write is on 1 node; read may hit 2 nodes that don't have it
Space cost: 3x data stored
```

Best for: High-throughput event ingestion where eventual consistency is explicitly acceptable. Do not use if read-after-write is required.

### Read-fast, write-durable (n=5, w=3, r=1)

```
w + r = 4 < n = 5  ✗ (quorum condition not satisfied)
```

Wait — this means reads can return stale values. To fix this:

```
n=5, w=3, r=3: w + r = 6 > 5 ✓
Fault tolerance: 2 nodes can fail
Read cost: 3 parallel reads required per operation
Write cost: 3 acknowledgments required
```

### High availability bias — sloppy quorum (n=3, w=1, r=1)

```
w + r = 2 < n = 3  ✗ (intentionally not a strict quorum)
```

Used when write availability is the top priority. Writes are accepted on any available node. Reads may return stale values. Enable hinted handoff to propagate writes to home nodes when partition heals.

**Do not use if:** data loss is unacceptable, read-after-write is required, or application logic requires seeing the latest value.

## Availability vs. Consistency Trade-off Table

| n | w | r | w+r>n | Node failures tolerated | Stale read risk |
|---|---|---|-------|------------------------|----------------|
| 3 | 3 | 1 | 4>3 ✓ | 0 writes, 2 reads | Very low |
| 3 | 2 | 2 | 4>3 ✓ | 1 | Low |
| 3 | 1 | 3 | 4>3 ✓ | 2 writes, 0 reads | Low |
| 3 | 2 | 1 | 3=3 ✗ | 1 writes, 2 reads | High |
| 3 | 1 | 2 | 3=3 ✗ | 2 writes, 1 reads | High |
| 5 | 3 | 3 | 6>5 ✓ | 2 | Low |
| 5 | 4 | 2 | 6>5 ✓ | 1 writes, 3 reads | Low |
| 5 | 2 | 4 | 6>5 ✓ | 3 writes, 1 reads | Low |

## Cassandra Consistency Level Mapping

In Cassandra, you configure consistency levels per-query rather than global n/w/r. Cassandra translates consistency levels to the quorum formula automatically based on the replication factor.

| Cassandra CL | Meaning | Equivalent |
|-------------|---------|-----------|
| ONE | w=1 or r=1 | Any single replica |
| QUORUM | w=(n/2)+1 or r=(n/2)+1 | Majority of replicas |
| LOCAL_QUORUM | Majority within local datacenter only | Multi-DC: quorum per-DC |
| ALL | w=n or r=n | All replicas |
| ANY | w=1, accepts hinted handoff node | Maximum write availability |
| SERIAL | Lightweight transactions (Paxos) | Linearizable per-key |

**For multi-datacenter Cassandra:** Use `LOCAL_QUORUM` for both reads and writes. This satisfies quorum within each datacenter independently and avoids cross-datacenter latency on every operation.

## Sloppy Quorum Configuration by Database

| Database | Sloppy quorum setting | Default |
|----------|----------------------|---------|
| Riak | `allow_mult = true`, sloppy quorum enabled | Enabled by default |
| Cassandra | Implicit via `hinted_handoff_enabled = true` | Enabled, but strict quorum by default |
| Voldemort | Configurable `prefer-reads`, `prefer-writes` | Disabled by default |
| DynamoDB | Not directly configurable; managed by AWS | AWS-managed |

## Replication Factor Selection Rules

- **n=1:** No fault tolerance. Only acceptable for development or non-critical caches.
- **n=3:** Standard minimum. Tolerates 1 node failure with majority quorum (w=2, r=2).
- **n=5:** Higher fault tolerance (2 node failures). Use for mission-critical data or when rolling restarts (which take nodes offline one at a time) should not reduce quorum.
- **Odd n is preferred:** Simplifies majority quorum math. n=4 does not give more fault tolerance than n=3 for majority quorums (both tolerate 1 failure before majority is lost).
