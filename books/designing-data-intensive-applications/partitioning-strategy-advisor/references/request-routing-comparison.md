# Request Routing Comparison

Detailed comparison of the three request routing approaches for partitioned databases, with operational trade-offs and database-specific guidance.

---

## The Problem

When a client sends a read or write request, the database must route it to the node that owns the target partition. As partitions rebalance (nodes added, removed, or failed over), the mapping from partition to node changes. Every component that makes routing decisions must have an up-to-date copy of this mapping.

Using stale routing metadata results in:
- Request forwarded to wrong node → error or extra hop latency
- Silent stale reads (wrong node returns stale data)
- Write to wrong node → data on the correct node is not updated

---

## Option 1: Any-Node with Forwarding (Gossip Protocol)

### How it works
1. Client sends request to any node (e.g., via round-robin load balancer or DNS).
2. If the receiving node owns the target partition, it handles the request directly.
3. If not, the receiving node looks up the correct owner in its local routing table and forwards the request to that node.
4. The correct node handles the request and returns the result (either directly to client or via the forwarding node).

Nodes maintain an up-to-date routing table by gossiping — periodically exchanging cluster state information with random peers. Changes propagate through the cluster over time (eventual consistency in metadata, not data).

### Used by
- Apache Cassandra (gossip protocol, token-aware drivers)
- Riak (riak_core gossip)

### Cassandra-specific
Cassandra drivers support "token-aware routing": the driver computes the partition key hash and connects directly to the owning node, bypassing the forwarding step. This reduces latency by eliminating the unnecessary hop.

```python
# Python cassandra-driver: token-aware load balancing policy
from cassandra.policies import TokenAwarePolicy, DCAwareRoundRobinPolicy
from cassandra.cluster import Cluster

cluster = Cluster(
    contact_points=['10.0.0.1', '10.0.0.2'],
    load_balancing_policy=TokenAwarePolicy(DCAwareRoundRobinPolicy())
)
```

### Operational trade-offs
| Dimension | Assessment |
|---|---|
| External dependency | None — no ZooKeeper or etcd required |
| Routing consistency | Eventual — gossip convergence may take seconds; brief stale routing is possible |
| Node complexity | Higher — routing logic lives in each database node |
| Failure tolerance | Good — no single coordinator to fail; gossip continues without central coordination |
| Configuration | Minimal — gossip is enabled by default in Cassandra/Riak |

### Best for
Systems that must avoid external coordination service dependencies. Multi-datacenter deployments where cross-DC ZooKeeper consensus would add latency. Teams with operational experience with Cassandra or Riak.

---

## Option 2: Routing Tier with Coordination Service

### How it works
1. A dedicated routing tier (partition-aware proxy/load balancer) sits between clients and database nodes.
2. Routing tier consults a coordination service (ZooKeeper, etcd) to look up the current partition-to-node mapping.
3. Routing tier forwards the request to the correct node and returns the response to the client.
4. Nodes register their partition assignments in ZooKeeper on join/leave. ZooKeeper notifies the routing tier of changes via watches.

### Used by
- Apache HBase (HMaster + ZooKeeper)
- Apache SolrCloud (ZooKeeper)
- Apache Kafka (ZooKeeper, pre-KRaft)
- LinkedIn Espresso (Helix + ZooKeeper)
- MongoDB (config server + mongos routing daemon)

### ZooKeeper-based routing (HBase/SolrCloud pattern)
```
Client → Routing Tier → ZooKeeper (watches partition assignment)
                      ↓
                  Node N (owns target partition)
```

ZooKeeper stores:
- Partition-to-node assignment map
- Node health/liveness registration
- Cluster epoch (version of the assignment)

Routing tier subscribes to ZooKeeper watches on the assignment node. When a partition moves, ZooKeeper notifies all subscribed routing tier instances, which update their local routing tables.

### MongoDB routing (mongos)
MongoDB uses a dedicated `config server` (replicated MongoDB deployment) to store shard metadata. `mongos` daemons act as the routing tier, caching shard metadata locally and refreshing from config server on stale-route errors.

```
Client → mongos → config server (shard map)
               ↓
           shard N (mongod)
```

### Operational trade-offs
| Dimension | Assessment |
|---|---|
| External dependency | Required — ZooKeeper/etcd cluster must be maintained and highly available |
| Routing consistency | Strong — ZooKeeper watch notifications are reliable; routing tier can have up-to-date metadata at all times |
| Node complexity | Lower — routing logic is isolated to the routing tier and coordination service |
| Failure tolerance | ZooKeeper itself becomes a critical path; ZooKeeper outage impairs routing tier operation |
| Operational overhead | Higher — ZooKeeper cluster requires its own deployment, monitoring, and maintenance |

### Best for
Systems with complex multi-partition query routing (e.g., analytics queries spanning multiple shards). Systems where routing correctness is critical and brief stale routing is unacceptable. Teams already operating ZooKeeper for other services (e.g., Kafka, HBase).

---

## Option 3: Partition-Aware Client

### How it works
1. The client library maintains a local cache of the partition-to-node mapping.
2. Client computes the target partition for the request and connects directly to the owning node.
3. Client refreshes its local routing map from a known source (ZooKeeper, config server, a seed node) on startup and periodically, or upon receiving a routing error from a node.

### Used by
- Cassandra drivers in token-aware mode (driver holds the token ring map)
- MongoDB application drivers (can bypass mongos and connect directly with partition info)
- DynamoDB (fully managed — AWS handles routing; client only calls the service endpoint)

### Cassandra token-aware driver (detailed)
The Cassandra driver downloads the full token ring topology from the cluster (via the `system.peers` table). For each write/read, the driver computes `hash(partition_key)` to determine the token, then looks up the token ring to find the owning node's IP address, and connects directly.

When the token ring changes (node added/removed), the driver receives a topology change event and updates its local copy. This update is asynchronous — there is a brief window where the driver has stale routing information.

### Operational trade-offs
| Dimension | Assessment |
|---|---|
| External dependency | None to minimal — may need initial seed node or config server endpoint |
| Routing consistency | Eventually consistent — client cache is refreshed asynchronously |
| Node complexity | Low — database nodes have no routing responsibility |
| Client complexity | Higher — routing logic is in each client library; library versions must be kept current |
| Latency | Lowest — zero-hop direct connection to owning node |

### Best for
Performance-critical applications where eliminating the forwarding hop matters. Systems using Cassandra with token-aware drivers. Managed database services (DynamoDB, Azure Cosmos DB) where routing is fully abstracted.

---

## Summary Comparison

| | Any-node + Forward | Routing Tier + Coord Service | Partition-Aware Client |
|---|---|---|---|
| Routing consistency | Eventual (gossip) | Strong (ZooKeeper watch) | Eventual (client cache refresh) |
| Hop count | 1–2 | 2 | 1 (direct) |
| External dependency | None | ZooKeeper/etcd | None (or seed node) |
| Operational complexity | Low | High | Medium |
| Best databases | Cassandra, Riak | HBase, SolrCloud, Kafka | Cassandra (token-aware), managed DBs |
| Failure of routing component | Gossip-based self-healing | ZooKeeper outage impairs routing | Client cache staleness |

---

## Handling Stale Routing in All Approaches

Regardless of which approach is used, clients should implement a stale-routing recovery path:

1. Send request using current routing information.
2. If the target node returns an error indicating it no longer owns the partition (e.g., Cassandra's `UnavailableException` with a "wrong coordinator" hint), refresh routing information from the authoritative source.
3. Retry the request with updated routing information.
4. If retry fails, surface the error to the application layer.

This retry-on-stale-route pattern ensures correctness even during rebalancing events when routing information is temporarily inconsistent.
