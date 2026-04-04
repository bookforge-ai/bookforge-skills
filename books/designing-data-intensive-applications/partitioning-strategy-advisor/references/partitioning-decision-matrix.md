# Partitioning Decision Matrix

Scoring rubric for selecting among range, hash, and compound key partitioning strategies. Score each dimension 1–5, then total. The highest-scoring method is the primary recommendation; use the runner-up to inform mitigation strategies.

---

## Dimensions

### 1. Range Query Support
Does the application require efficient range scans on the partition key (e.g., date ranges, alphabetical ranges, numeric ranges)?

| Score | Meaning |
|---|---|
| 5 | Range queries are the primary access pattern — efficient range scan is critical |
| 3 | Range queries are needed but not dominant |
| 1 | All queries are point lookups — range queries are never needed |

### 2. Write Distribution (inverted — higher = more uniform)
How uniformly are writes distributed across the key space?

| Score | Meaning |
|---|---|
| 5 | Keys are randomly/uniformly distributed (UUIDs, random hashes) |
| 3 | Moderate skew — some keys receive more writes but not extreme concentration |
| 1 | Strongly monotonic or celebrity-key workload — severe skew without mitigation |

### 3. Cross-Partition Query Avoidance
Does the application's primary access pattern allow most queries to be served from a single partition?

| Score | Meaning |
|---|---|
| 5 | Primary queries always fix the partition key (single-partition lookups) |
| 3 | Mixed — some queries span partitions, most do not |
| 1 | Most queries fan out across all partitions (analytics, global aggregations) |

### 4. Secondary Index Requirements
How demanding are secondary index query patterns (non-primary-key attribute filters)?

| Score | Meaning |
|---|---|
| 5 | No secondary index queries — all queries use the primary key |
| 3 | Secondary index queries exist but are infrequent or can tolerate scatter/gather |
| 1 | Secondary index queries are frequent, latency-sensitive, and cannot scatter/gather |

### 5. One-to-Many Relationship Access
Does the application frequently fetch all child records for a given parent entity, sorted?

| Score | Meaning |
|---|---|
| 5 | Yes — dominant pattern is "fetch all X for user Y, sorted by timestamp" |
| 3 | Occasionally needed |
| 1 | Never — all lookups are for individual records |

### 6. Operational Simplicity
How much operational complexity can the team absorb for partition boundary management?

| Score | Meaning |
|---|---|
| 5 | Prefer fully managed/automatic boundary assignment |
| 3 | Can manage semi-automatic with operator approval |
| 1 | Team has capacity for manual partition boundary administration |

---

## Scoring by Strategy

For each dimension, score the strategy being evaluated:

| Dimension | Range | Hash | Compound |
|---|---|---|---|
| Range query support | High score when range queries are critical | Low score — hash destroys sort order | High score — range scans within partition |
| Write distribution | Low score for monotonic keys | High score — hash distributes evenly | Medium — distributes on hash part, sequential within |
| Cross-partition query avoidance | High score if queries always fix prefix | High score for point lookups | High score — compound key collocates related records |
| Secondary index requirements | Medium | Medium | Medium (same trade-offs apply to secondary indexes) |
| One-to-many relationship access | Low score — all parents share the key space | Low score — cannot sort within partition | High score — clustering columns sort within partition |
| Operational simplicity | Medium — dynamic partitioning helps | High — hash ranges are simple to manage | Medium — compound key design requires upfront modeling |

---

## Quick-Decision Table

| Access pattern | Write distribution | Recommendation |
|---|---|---|
| Range queries dominant | Uniform keys | Range partitioning |
| Range queries dominant | Monotonic keys | Range + compound prefix (prefix + timestamp) |
| Point lookups only | Any | Hash partitioning |
| Point lookup on entity + range scan within entity | Any | Compound key (hash entity, range sort key) |
| Analytics / multi-attribute filter | Any | Hash + accept scatter/gather, or global secondary index |

---

## Example Scores

### IoT sensor platform (sensor_name + timestamp key)
| Dimension | Score |
|---|---|
| Range queries (date range scans) | 5 |
| Write distribution (timestamp = monotonic → needs prefix) | 3 (with prefix mitigation) |
| Cross-partition avoidance (prefix fixes partition) | 5 |
| Secondary index requirements (none needed) | 5 |
| One-to-many (all readings per sensor) | 4 |
| Operational simplicity (HBase dynamic) | 4 |
| **Total** | **26 / 30** |

**Winner: Range with compound prefix**

### User post feed (Cassandra: user_id + post_timestamp)
| Dimension | Score |
|---|---|
| Range queries (fetch posts by time) | 4 |
| Write distribution (user IDs uniform) | 5 |
| Cross-partition avoidance (user_id fixes partition) | 5 |
| Secondary index requirements (none — denormalized) | 5 |
| One-to-many (all posts per user) | 5 |
| Operational simplicity (Cassandra default) | 5 |
| **Total** | **29 / 30** |

**Winner: Compound key (hash + range)**
