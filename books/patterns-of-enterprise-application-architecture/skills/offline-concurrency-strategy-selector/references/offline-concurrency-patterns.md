# Offline Concurrency Pattern Details

Source: *Patterns of Enterprise Application Architecture*, Ch 16 (David Rice)

## Optimistic Offline Lock — Infrastructure

### Version Column Schema

```sql
-- Add to every table that needs offline concurrency protection
ALTER TABLE customer ADD COLUMN version INTEGER NOT NULL DEFAULT 0;
ALTER TABLE customer ADD COLUMN modified_by VARCHAR(255);
ALTER TABLE customer ADD COLUMN modified_at TIMESTAMP;
```

### Version-Conditioned SQL

```sql
-- UPDATE must include version in WHERE
UPDATE customer
   SET name = ?, modified_by = ?, modified_at = ?, version = version + 1
 WHERE id = ? AND version = ?;

-- DELETE must include version in WHERE
DELETE FROM customer WHERE id = ? AND version = ?;

-- After executing: check rowsAffected. 0 = conflict.
```

**Never use `modified_at` as the version marker.** System clocks are unreliable, especially across multiple servers. Always use a monotonic integer counter.

### Conflict Error Lookup

When row count = 0, query to build the error message:
```sql
SELECT version, modified_by, modified_at FROM customer WHERE id = ?;
```
If row exists: "Record modified by [modified_by] at [modified_at]."
If row missing: "Record has been deleted by another session."

### Inconsistent Read Extension

If the business transaction's correctness depends on data it READ (not just wrote), register those reads for version check too:

```python
# In Unit of Work commit phase:
for obj in self.dirty:
    self._check_or_increment_version(obj)   # blocks concurrent writes
for obj in self.reads_that_matter:
    self._check_version(obj)                 # blocks if someone else modified
```

NOTE: Version reread-only (no increment) requires REPEATABLE READ or stronger isolation. If isolation level is unknown, increment to be safe.

---

## Pessimistic Offline Lock — Lock Table Schema

```sql
-- Application-managed lock table (NOT the DB's internal locking mechanism)
CREATE TABLE app_lock (
    lockable_id  BIGINT       NOT NULL,
    owner_id     VARCHAR(255) NOT NULL,
    acquired_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (lockable_id)   -- uniqueness constraint enforces exclusivity
);
```

For **read/write locks**, a more complex schema is needed (lock_type column + application-side logic to enforce mutual exclusion).

### Lock Manager Protocol

```python
class LockManager:
    def acquire(self, lockable_id: int, owner_id: str) -> None:
        """Raises ConcurrencyException if lock unavailable. NEVER blocks."""
        if self._has_lock(lockable_id, owner_id):
            return  # idempotent — already held by this session
        try:
            db.execute("INSERT INTO app_lock VALUES (?, ?, NOW())",
                       lockable_id, owner_id)
        except UniqueConstraintViolation:
            owner = db.scalar("SELECT owner_id FROM app_lock WHERE lockable_id=?",
                              lockable_id)
            raise ConcurrencyException(f"Locked by {owner}")

    def release(self, lockable_id: int, owner_id: str) -> None:
        db.execute("DELETE FROM app_lock WHERE lockable_id=? AND owner_id=?",
                   lockable_id, owner_id)

    def release_all(self, owner_id: str) -> None:
        db.execute("DELETE FROM app_lock WHERE owner_id=?", owner_id)
```

### Session Expiry Listener (HTTP)

```python
# Django signal / Flask session teardown / Spring HttpSessionBindingListener
def on_session_destroyed(session_id: str):
    with transaction():
        lock_manager.release_all(session_id)
```

### Lock Timeout Policy

Option A: Application-side check on acquire:
```sql
DELETE FROM app_lock WHERE acquired_at < NOW() - INTERVAL '30 minutes';
```
Run before every acquire, or in a background job.

Option B: DB-level expiry via event or scheduled job.

---

## Coarse-Grained Lock — Shared Version Pattern

### Shared Version Table

```sql
CREATE TABLE aggregate_version (
    id          BIGINT PRIMARY KEY,
    value       BIGINT NOT NULL DEFAULT 0,
    modified_by VARCHAR(255),
    modified_at TIMESTAMP
);

-- Each member table references the shared version
ALTER TABLE order_line_item ADD COLUMN version_id BIGINT REFERENCES aggregate_version(id);
ALTER TABLE order_header     ADD COLUMN version_id BIGINT REFERENCES aggregate_version(id);
```

All members of an Order aggregate share the same `aggregate_version` row (same `version_id`).

### Version Increment (Optimistic)

```sql
-- Increment the SHARED version; all members are now "locked" for concurrent sessions
UPDATE aggregate_version
   SET value = value + 1, modified_by = ?, modified_at = NOW()
 WHERE id = ? AND value = ?;
-- rowCount = 0 → conflict on the aggregate
```

### Root Lock (Pessimistic complement)

Use the aggregate root's primary key as the `lockable_id` in the lock table. All child objects navigate to the root to acquire/check the lock. Requires child-to-parent navigation in the domain model.

---

## Implicit Lock — Mapper Decorator Pattern

```python
class LockingRepository:
    """Decorator that wraps any Repository to acquire locks transparently."""

    def __init__(self, inner: Repository, lock_manager: LockManager):
        self._inner = inner
        self._lm = lock_manager

    def find(self, entity_id: int) -> DomainObject:
        # Acquire lock BEFORE load (guarantees currency)
        self._lm.acquire(entity_id, current_session_id())
        return self._inner.find(entity_id)

    def update(self, obj: DomainObject) -> None:
        # Validate lock is held before committing (write lock variant)
        if not self._lm.has_lock(obj.id, current_session_id()):
            raise ConcurrencyException(
                f"Write lock not held for {type(obj).__name__} {obj.id}. "
                "This is a programmer error — acquire the lock before editing."
            )
        self._inner.update(obj)

    def delete(self, obj: DomainObject) -> None:
        if not self._lm.has_lock(obj.id, current_session_id()):
            raise ConcurrencyException(f"Write lock not held for {obj.id}")
        self._inner.delete(obj)
```

Register the locking decorator in your repository registry / DI container so all callers receive it transparently.
