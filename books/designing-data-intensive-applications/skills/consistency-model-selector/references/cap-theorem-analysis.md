# CAP Theorem Analysis

## What CAP Actually Says

CAP (Consistency, Availability, Partition tolerance) is often summarized as "pick 2 of 3." This framing is misleading. The correct interpretation:

**When a network partition occurs, a linearizable (consistent) system must choose between**:
- **Remaining consistent**: refuse requests from nodes that cannot contact the majority — become *unavailable*
- **Remaining available**: process requests from disconnected nodes — violate *linearizability*

A better statement: **either Consistent or Available when Partitioned (CAAP)**.

## Why "Pick 2 of 3" Is Wrong

Network partitions are not a design choice. They happen whether you want them to or not — packets are delayed, lost, or reordered; hardware fails; datacenter links go down. You cannot opt out of partition tolerance. The real choice is what to do *when* a partition occurs.

Additionally:
- CAP's definition of "availability" is idiosyncratic — it means every request receives a response, not that the system is "highly available" in the operational sense. Many "highly available" systems (that use consensus) do not meet CAP's availability definition.
- CAP only considers one consistency model (linearizability) and one fault type (network partitions). It says nothing about node crashes, network delays, or other faults.
- CAP has been superseded by more precise results (PACELC, etc.) for system design purposes.

## Correct Application

For each operation that requires linearizability, document the expected behavior during a network partition:

| Situation | Linearizable System Behavior | Non-Linearizable System Behavior |
|---|---|---|
| Node disconnected from leader | Must wait or return error | Can serve requests (potentially stale) |
| Cross-datacenter link down (single-leader) | Follower datacenter unavailable for writes and linearizable reads | Multi-leader: both datacenters continue, may conflict |
| Minority partition | Minority nodes unavailable (cannot form quorum) | May continue serving (leaderless, eventual) |

## Partition Behavior by Replication Strategy

**Single-leader (linearizable reads from leader)**:
- Clients connected to leader datacenter: unaffected
- Clients connected to follower datacenter: unavailable for writes and linearizable reads during partition
- This is the correct linearizability/availability trade-off

**Multi-leader**:
- Both datacenters continue operating during partition
- Writes accepted independently; conflict resolution required when partition heals
- Behavior is NOT linearizable

**Leaderless (Dynamo-style)**:
- Sloppy quorums or degraded quorums may serve requests during partition
- Data may diverge; read repair resolves after partition heals
- Behavior is NOT linearizable

**Consensus algorithm (Raft/Zab)**:
- Majority partition: continues normally
- Minority partition: unavailable (cannot make progress without quorum)
- Behavior IS linearizable for the majority partition

## The Latency-Consistency Trade-off (Beyond CAP)

Even on a network that is working correctly (no partition), linearizability is slow. The Attiya-Welch theorem proves that in a network with variable delays, the response time of linearizable reads and writes is at least proportional to the uncertainty of those delays.

This means: in a geographically distributed system with high inter-region latency, linearizable operations will be slow even when nothing is failing. Many distributed databases choose weaker consistency models primarily for latency reasons, not partition tolerance.

**Practical implication**: Even within a single datacenter, RAM on a modern multi-core CPU is not linearizable (CPU caches create multiple copies of data, updated asynchronously). Linearizability was sacrificed for performance — memory barriers (fences) re-introduce ordering when needed.

## When to Apply CAP Analysis

Apply CAP analysis to each operation you have marked as requiring linearizability:

1. What happens during a network partition? Which clients lose access?
2. Is partial availability acceptable (clients on majority partition continue; minority partition returns errors)?
3. What is the expected duration of partitions in your network? (Data center link failure: minutes to hours. Within-DC: milliseconds.)
4. Is the cost of unavailability during a partition acceptable, given how rare partitions are?

If unavailability during a partition is not acceptable, reconsider whether linearizability is truly required for that operation, or whether causal consistency with application-level conflict handling is sufficient.

## CAP Does Not Apply to Causal Consistency

Causal consistency is the strongest model that remains available during network failures and does not slow down due to network delays. The CAP theorem does not apply to causally consistent systems because they do not make the recency guarantee that linearizability requires.

This is why, for many operations that appear to need linearizability (but actually only need causal ordering), causal consistency is the correct — and much cheaper — choice.
