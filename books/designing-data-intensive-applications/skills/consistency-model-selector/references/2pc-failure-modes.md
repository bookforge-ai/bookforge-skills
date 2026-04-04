# Two-Phase Commit: Failure Modes and Alternatives

## How 2PC Works (Normal Path)

Two-phase commit (2PC) ensures atomic transaction commit across multiple nodes. It requires a *coordinator* (transaction manager) and one or more *participants* (database nodes).

**Phase 1 — Prepare**:
1. Application requests a globally unique transaction ID from the coordinator
2. Application executes the transaction on each participant under that transaction ID
3. When ready to commit, coordinator sends `prepare` to all participants
4. Each participant either:
   - Replies `yes`: writes all transaction data to disk, promises it can commit under any future circumstance (crash, power failure, etc. are no longer excuses for refusing to commit later)
   - Replies `no`: aborts the transaction

**Phase 2 — Commit or Abort**:
5. If all participants replied `yes`: coordinator writes commit decision to its own durable log (the *commit point*), then sends `commit` to all participants
6. If any participant replied `no`: coordinator sends `abort` to all participants
7. Coordinator retries `commit` or `abort` indefinitely until all participants acknowledge

**The commit point** is the critical moment: writing the commit decision to the coordinator's log is the irrevocable decision. Everything before this point can still be aborted; everything after must be committed.

## Failure Modes

### Participant Failure Before Voting
**What happens**: Coordinator detects timeout; aborts the transaction and sends `abort` to all other participants.  
**Safe**: The participant hasn't voted yet, so it can roll back on recovery.

### Participant Failure After Voting "Yes"
**What happens**: Participant is in-doubt. When it recovers, it checks in with the coordinator for the commit/abort decision and applies it.  
**Safe**: The coordinator still holds the decision.

### Coordinator Failure Before Sending Prepare
**What happens**: Coordinator crashes before phase 1. Participants have no in-doubt transactions; they can safely abort.  
**Safe**: No participant has committed anything yet.

### Coordinator Failure After Prepare, Before Commit Point (Most Dangerous)
**What happens**:
- Participants have voted `yes` — they are in-doubt
- Participants CANNOT unilaterally abort (another participant may have committed)
- Participants CANNOT unilaterally commit (another participant may have aborted)
- Participants hold row-level locks on all modified rows — no other transaction can proceed on those rows
- Participants wait indefinitely until the coordinator recovers

**Recovery**: When the coordinator recovers, it reads its transaction log:
- If the commit record is present: send `commit` to in-doubt participants
- If no commit record: the commit point was not reached; send `abort` to all

**Lock-holding duration**: If the coordinator takes 20 minutes to restart, participant locks are held for 20 minutes. During this time, other transactions accessing those rows are blocked.

### Coordinator Log Lost or Corrupted After Crash
**What happens**: Orphaned in-doubt transactions — the coordinator cannot determine the correct outcome.  
**Resolution**: Manual administrator intervention required. Administrator must:
1. Examine the state of each participant (has any participant committed or aborted?)
2. Apply the same outcome to all remaining participants

**Operational risk**: This typically happens during a serious production outage, under time pressure, requiring expert judgment about distributed transaction state.

### XA Heuristic Decisions (Emergency Escape Hatch)
Some XA transaction implementations allow a *heuristic decision* — a participant unilaterally decides to commit or abort an in-doubt transaction without a definitive decision from the coordinator.

This is defined as "probably breaking atomicity." It is intended only for getting out of catastrophic situations (coordinator permanently down, locks held for an unacceptable duration). Regular use violates 2PC's correctness guarantees.

## Complete Failure Catalog

| Failure Timing | Blocked? | Data Safe? | Resolution |
|---|---|---|---|
| Before prepare sent | No | Yes | Coordinator aborts on timeout |
| Participant fails before voting | No | Yes | Coordinator aborts on timeout |
| Participant fails after voting yes | Participant blocked | Yes | Coordinator sends decision on participant recovery |
| Coordinator fails before prepare | No | Yes | Participants can abort |
| Coordinator fails after prepare, before commit | **Yes — in-doubt** | Yes (no commit yet) | Wait for coordinator recovery |
| Coordinator fails after commit point, partial sends | **Partial commit — in-doubt** | Partially committed | Wait for coordinator recovery |
| Coordinator log lost after crash | **Indefinitely blocked** | Unknown | Manual administrator intervention |

## Performance Cost

- **Disk fsyncs**: Coordinator must fsync its log before sending commit (at commit point). Each participant must fsync transaction data before replying yes to prepare. Total: 2+ fsyncs per transaction.
- **Network round-trips**: At minimum 2 round-trips (prepare + commit) vs. 1 for single-node commit.
- **Lock-holding**: Participants hold locks throughout both phases — much longer than single-node transactions.
- **Benchmark**: MySQL distributed transactions reported at 10x slower than single-node transactions.

## 2PC vs. Fault-Tolerant Consensus

| Property | 2PC | Fault-Tolerant Consensus (Raft/Zab) |
|---|---|---|
| Uniform agreement | Yes | Yes |
| Integrity | Yes | Yes |
| Validity | Yes | Yes |
| Termination | **No** (blocks if coordinator crashes) | Yes (majority quorum sufficient) |
| Coordinator | Single point of failure | Leader elected by consensus |
| Requires all nodes? | **Yes** — any participant failure can block | No — majority quorum sufficient |
| Amplifies failures | Yes — one broken participant blocks all | No — minority failures are tolerated |

2PC is a kind of consensus algorithm, but not a very good one — it does not satisfy the termination property.

## Distributed Transaction Types

**Database-internal distributed transactions**: All participants run the same database software (VoltDB, MySQL Cluster NDB, CockroachDB). The coordinator and protocol are optimized for that specific system. Failure modes are more manageable; performance is better.

**Heterogeneous distributed transactions (XA)**: Participants are different technologies (PostgreSQL + Oracle + ActiveMQ). XA is the standard C API for cross-technology 2PC (Java Transaction API/JTA wraps XA for Java). Limitations:
- Cannot detect deadlocks across systems (no shared lock information)
- Does not work with SSI (requires conflict detection across different systems)
- Coordinator log on application server makes the server stateful — breaks horizontal scaling model
- Coordinator is a single point of failure unless explicitly replicated (most XA coordinators are not highly available by default)

## Alternatives to 2PC

### Saga Pattern (Compensating Transactions)
Break a multi-step transaction into a sequence of local transactions, each with a compensating action for rollback.
- Provides eventual atomicity (not strict atomicity)
- Requires idempotent compensating actions
- Application must handle partial state during saga execution
- Best for: long-running business transactions where strict atomicity is not required

### Outbox Pattern
Write the event/message to the same database as the main write, in the same local transaction. A relay process reads the outbox and publishes to the message broker.
- Guarantees at-least-once delivery without cross-system 2PC
- Requires idempotent consumers
- Best for: reliably publishing events to a message broker after a database write

### Total Order Broadcast + Idempotent Consumers
Use a log (Kafka, Kinesis) as the source of truth. All consumers process messages in the same order. Idempotency handles duplicate delivery.
- Best for: systems where all state is derived from a log (event sourcing, CQRS)
- Does not require 2PC across the producer and consumer systems
