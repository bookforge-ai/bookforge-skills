# End-to-End Correctness and Operation Identifier Implementation

## The End-to-End Argument

The end-to-end argument (Saltzer, Reed, and Clark, 1984) states:

> The function in question can completely and correctly be implemented only with the knowledge and help of the application standing at the endpoints of the communication system. Therefore, providing that questioned function as a feature of the communication system itself is not possible.

Applied to data systems: **correctness guarantees provided by individual layers — TCP, database transactions, stream processor exactly-once — cannot, by themselves, guarantee correctness across the entire request path from client to database.**

### The Concrete Problem

A user submits a bank transfer via a web form:

1. Browser sends HTTP POST to application server
2. Application server opens a database transaction
3. Transaction updates two account balances
4. Transaction commits (ACID guarantee: atomically)
5. Database sends success response to application server
6. Application server sends 200 OK to browser

**What if the network fails at step 6?** The transaction committed in step 4, but the browser never received the success response. The browser shows an error. The user clicks "Submit" again. Now:

- TCP duplicate suppression: does not help — this is a new TCP connection
- Database transaction: does not help — this is a new transaction; the database does not know it is a retry
- 2PC: does not help — it handles coordinator failure during the commit protocol, not client-level retries after commit

The transfer executes twice. The user is charged $22 instead of $11.

**Real banks do not work this way.** Real banks use end-to-end idempotency: each transfer request carries a unique identifier that is stored in the database. A retry of the same request is detected and rejected at the application level.

## The Operation Identifier Pattern

### Structure

Every mutating operation that must be idempotent end-to-end needs a unique operation identifier:

1. **Generated at the client** — not at the application server. The client generates the ID before the first attempt and reuses it on every retry.
2. **Derived deterministically** — either a UUID (random, globally unique) or a hash of the request's meaningful fields (from_account, to_account, amount, initiating_session). Deterministic derivation allows reconstruction if the client forgets the ID.
3. **Passed through every hop** — HTTP header, message broker key, stream processor message field, database column. The ID is never dropped or regenerated at any intermediate layer.
4. **Enforced at the final storage layer** — a unique constraint on the operation ID in the database prevents duplicate execution, even under concurrent retries.

### Implementation

```sql
-- Schema: operation ID as a unique constraint
CREATE TABLE money_transfers (
    request_id    UUID        PRIMARY KEY,
    from_account  BIGINT      NOT NULL,
    to_account    BIGINT      NOT NULL,
    amount        DECIMAL     NOT NULL,
    initiated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- The unique constraint on request_id makes concurrent retries safe
-- even at weak isolation levels (read committed, snapshot isolation)
-- because uniqueness constraints are enforced correctly at all isolation levels
-- in most relational databases
```

```sql
-- Execution: idempotent transfer using operation identifier
BEGIN TRANSACTION;

-- Insert the transfer request — fails with a unique violation if already processed
INSERT INTO money_transfers (request_id, from_account, to_account, amount)
VALUES ('0286FDB8-D7E1-423F-B40B-792B3608036C', 4321, 1234, 11.00)
ON CONFLICT (request_id) DO NOTHING;  -- Idempotent: second attempt is a no-op

-- Conditionally apply the debit/credit only if the insert succeeded
-- (i.e., this is the first time this request_id has been processed)
UPDATE accounts SET balance = balance + 11.00 WHERE account_id = 1234
  AND EXISTS (SELECT 1 FROM money_transfers WHERE request_id = '0286FDB8-D7E1-423F-B40B-792B3608036C');

UPDATE accounts SET balance = balance - 11.00 WHERE account_id = 4321
  AND EXISTS (SELECT 1 FROM money_transfers WHERE request_id = '0286FDB8-D7E1-423F-B40B-792B3608036C');

COMMIT;
```

**Note on isolation level:** The unique constraint on `request_id` works correctly even at read committed isolation, because uniqueness constraints are enforced at a lower level than MVCC snapshot visibility. A concurrent insert of the same `request_id` will either serialize (one succeeds, one fails) or abort. The `ON CONFLICT DO NOTHING` clause makes the retry a safe no-op.

### The requests Table as an Event Log

The `money_transfers` table in the pattern above functions as an event sourcing log for transfer requests. The account balance updates do not need to happen in the same transaction as the transfer request insertion — they can be applied asynchronously by a downstream consumer that reads the `money_transfers` table as an event log, because:

- The request is durably recorded (the INSERT committed)
- The downstream consumer processes each request exactly once (it deduplicates by `request_id`)
- The downstream consumer is idempotent (applying the same transfer twice is prevented by the deduplication check)

This is the event sourcing pattern: record the intent durably first; derive the effects asynchronously.

## Multi-Partition Correctness Without Distributed Transactions

When an operation spans multiple partitions — for example, debiting account A (in partition 1) and crediting account B (in partition 2) — distributed atomic commit (2PC) is the traditional solution. 2PC achieves atomicity but has high cost: blocking during coordinator failure, heterogeneous protocol requirements, poor fault tolerance.

The alternative achieves equivalent correctness without cross-partition coordination:

### The Pattern

**Step 1:** Client generates a unique `request_id`. Application server appends a single transfer-request message to a Kafka topic partitioned by `request_id`. The message contains `{request_id, from_account, to_account, amount}`. This is a single-object write — atomic in almost all message brokers.

**Step 2:** A stream processor reads the transfer-request log. For each message, it emits two derived messages:
- A debit instruction to the `account-debits` topic, partitioned by `from_account`, containing `{request_id, from_account, amount}`
- A credit instruction to the `account-credits` topic, partitioned by `to_account`, containing `{request_id, to_account, amount}`

If the stream processor crashes and replays from its last checkpoint, it re-emits the same debit and credit instructions. Because the derivation is deterministic and the `request_id` is preserved, the downstream processors can safely deduplicate.

**Step 3:** Separate account processors for debits and credits each consume their respective topics. They maintain a deduplication table keyed by `request_id`. For each message:
- If `request_id` already in the deduplication table → skip (already applied)
- Otherwise → apply the debit/credit and record the `request_id`

**Why this achieves the same correctness as 2PC:**
- Every valid transfer request is applied exactly once to both the payer and payee accounts
- This holds even in the presence of stream processor crashes and message redelivery
- No cross-partition coordination is required at any step
- A failure of the debit processor does not affect the credit processor (they are independent consumers)

**The key insight:** Distributing the operation into two separately partitioned stages, connected by a durably logged request, avoids the need for atomicity across partitions. The `request_id` propagated through all stages is the mechanism that ties the distributed operation together and ensures exactly-once application.

## Timeliness vs. Integrity

These are two distinct dimensions of correctness that are conflated by the term "consistency":

**Timeliness:** Users observe the system in an up-to-date state. A timeliness violation means a user reads stale data — they see a version of the state that has since been updated. Timeliness violations are **temporary**: waiting and retrying will eventually show the correct state (assuming eventual consistency).

**Integrity:** No data is lost and no contradictory or false data exists. An integrity violation means the data is permanently corrupted — a record is missing, an account balance is wrong, a derived view contains a record that does not exist in the source. Integrity violations are **permanent**: waiting and retrying does not fix database corruption.

| Property | Violation | Recovery | Example |
|----------|-----------|----------|---------|
| Timeliness | Stale read | Wait and retry | User's profile update not yet visible in search index |
| Integrity | Data corruption | Manual repair | Account charged twice; search index contains records deleted from the source |

**Design principle:** In most applications, integrity is far more important than timeliness. Design the integration architecture to preserve integrity unconditionally — even at the cost of weak timeliness guarantees. Stale data is annoying; corrupted data is catastrophic.

The event log + idempotent consumer pattern preserves integrity while accepting weak timeliness: derived views will eventually be consistent with the source of record (when the consumer catches up), and the derivation will not corrupt data even if it runs multiple times.

## Auditing and Self-Verification

The end-to-end argument implies that end-to-end integrity checks are valuable. Because each individual layer assumes the layers above and below it are working correctly, bugs in any layer can produce corruption that only manifests at the application level.

**Useful audit patterns:**

1. **Periodic reconciliation:** Count or sum records in the source of record and each derived view. Discrepancies indicate lost events or failed derivations.

2. **Event log as audit trail:** If the event log is immutable and append-only, it provides a complete, replayable record of all writes. Any derived view can be verified by replaying the log and comparing the output to the current state.

3. **Deterministic reprocessing as verification:** Run the derivation function twice on the same input. If the outputs differ, the function is non-deterministic (a bug). If the output differs from the stored derived view, events were lost or applied out of order.

4. **Cryptographic integrity:** Hash the event log periodically and store the hashes. A mismatch indicates tampering or silent corruption. This is the principle behind Merkle trees used in certificate transparency systems.
