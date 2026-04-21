# Unit of Work Integration Guide

## Commit Sequence

The Unit of Work (UoW) owns the system transaction boundary. Optimistic Offline Lock checks must run inside the same system transaction that commits the data writes. The sequence from the book:

```
checkConsistentReads()
insertNew()
deleteRemoved()
updateDirty()           ← version-conditioned UPDATEs happen here
```

## Rollback Is Mandatory

```java
public void commit() {
    try {
        checkConsistentReads();
        insertNew();
        deleteRemoved();
        updateDirty();
    } catch (ConcurrencyException e) {
        rollbackSystemTransaction();   // MUST happen before re-throw
        throw e;                       // propagate to caller/controller
    }
}
```

Fowler: "Do not forget this step!" Without rollback, partial writes (some records updated, others not) enter the database in an inconsistent state.

## Inconsistent Read Protection (Optional)

Standard version checks cover the change set (objects that were modified). If the commit's correctness depends on objects that were READ but not WRITTEN (e.g., reading customer address to calculate tax), register them in a read-set:

```java
// Register a read-only dependency
public void registerRead(DomainObject obj) {
    reads.add(obj);
}

// Check at commit time
public void checkConsistentReads() {
    for (DomainObject obj : reads) {
        obj.getVersion().increment();  // aggressive: increments even for read-only
    }
}
```

**Why increment (not just re-read)?** Re-reading the version requires repeatable-read or stronger isolation to avoid false positives. Since we can't always guarantee the isolation level, incrementing the version forces the check to work at any isolation level. The trade-off: it marks the object as modified in the DB even though no business data changed.

**Alternative (less aggressive):** Add read objects to the change set. The mapper re-reads their version at commit and throws ConcurrencyException if changed, without incrementing. Requires repeatable-read isolation.

## Integration with unit-of-work-implementer Skill

If `unit-of-work-implementer` has been applied to this codebase:

1. Locate the `commit()` method in the UoW class.
2. Add version-conditioned SQL in the `updateDirty()` loop (or ensure the mapper's `update()` method already includes it).
3. Wrap the entire `commit()` body in a try/catch that rolls back on `ConcurrencyException`.
4. Optionally add `registerRead()` and `checkConsistentReads()` for inconsistent read protection.

If `unit-of-work-implementer` has not been applied: implement the rollback wrapper at the repository or service class level wherever `save()` is called.

## Java Example (from the book, abbreviated)

```java
class UnitOfWork {
    private List<DomainObject> dirty  = new ArrayList<>();
    private List<DomainObject> reads  = new ArrayList<>();

    public void registerDirty(DomainObject obj)  { dirty.add(obj); }
    public void registerRead(DomainObject obj)    { reads.add(obj); }

    public void commit() {
        Connection conn = ConnectionManager.INSTANCE.getConnection();
        try {
            conn.setAutoCommit(false);
            checkConsistentReads();
            insertNew();
            deleteRemoved();
            updateDirty();
            conn.commit();
        } catch (ConcurrencyException e) {
            conn.rollback();    // rollback BEFORE re-throw
            throw e;
        } catch (Exception e) {
            conn.rollback();
            throw new SystemException("commit failed", e);
        }
    }

    private void checkConsistentReads() {
        for (DomainObject obj : reads) {
            obj.getVersion().increment();  // version check via increment
        }
    }

    private void updateDirty() {
        for (DomainObject obj : dirty) {
            mapperFor(obj).update(obj);    // mapper issues version-conditioned UPDATE
        }
    }
}
```

## License

CC-BY-SA-4.0 — Source: BookForge / Patterns of Enterprise Application Architecture by Fowler et al.
