# Anti-Pattern Detection Checklist

Run this checklist on any Optimistic Offline Lock implementation — new or existing.

---

## AP-1: Version Not in UPDATE/DELETE WHERE Clause

**Risk:** Critical — Lost Updates occur silently.

**Detection:**
```bash
# Find UPDATE statements on versioned tables that lack AND version=
grep -rn "UPDATE customer" src/ | grep -v "AND version"
grep -rn "DELETE FROM customer" src/ | grep -v "AND version"
```

**Correct:**
```sql
UPDATE customer SET name=?, version=? WHERE id=? AND version=?
```

**Broken:**
```sql
UPDATE customer SET name=?, version=? WHERE id=?   -- version check missing
```

---

## AP-2: Version Not Incremented on Save

**Risk:** High — Subsequent writers see the same version, all saves succeed without conflict.

**Detection:** Check that the new version value passed to UPDATE is `oldVersion + 1`, not `oldVersion`:
```bash
grep -rn "version = ?" src/ | grep -v "version + 1\|version+1\|version=version+1"
```

**Correct:** `version = oldVersion + 1` or `@Version`-managed auto-increment.

**Broken:** `UPDATE ... SET version=? WHERE id=? AND version=?` with params `(oldVersion, id, oldVersion)`.

---

## AP-3: Row Count Not Checked

**Risk:** High — Collisions go silently undetected.

**Detection:**
```bash
# Find executeUpdate() or execute() calls not followed by a row count check
grep -n "executeUpdate\|stmt.execute" src/ | grep -v "rowCount\|affected\|count"
```

Every `UPDATE` and `DELETE` on a versioned table must be followed by `if (rowCount == 0) throwConcurrencyException(...)`.

---

## AP-4: Timestamp Used as Version

**Risk:** Medium — Sub-millisecond updates or cross-server clock skew cause missed conflicts.

**Detection:**
```bash
grep -rn "WHERE.*modified_at\|WHERE.*updated_at\|WHERE.*last_modified" src/
```

Replace with an integer `version` column in the WHERE clause. Keep `modified_at` as an informational column only (for error messages).

---

## AP-5: Stale In-Memory Object Retried After Collision

**Risk:** High — Retry loop immediately fails again; may loop indefinitely.

**Detection:** Look for catch blocks that call save() again without reloading the entity:
```java
// BROKEN
try {
    save(customer);
} catch (ConcurrencyException e) {
    save(customer);  // same object, same old version — will fail again
}

// CORRECT
try {
    save(customer);
} catch (ConcurrencyException e) {
    customer = reload(customer.getId());  // get current version from DB
    customer.applyChanges(pendingChanges);
    save(customer);
}
```

---

## AP-6: Version Not Round-Tripped to Client

**Risk:** High — Server cannot detect conflicts for web/mobile clients.

**Detection:**
```bash
# Check that version appears in API response DTOs and request body handling
grep -rn "class.*DTO\|class.*Request" src/ | xargs grep -l "version"
```

GET responses must include `version`. PUT/POST request bodies must accept and use `version`. Strong parameters / model binders must permit `version`.

---

## AP-7: No Rollback on ConcurrencyException

**Risk:** High — Partial commits leave data inconsistent.

**Detection:**
```bash
grep -rn "catch.*ConcurrencyException\|catch.*OptimisticLock\|catch.*StaleObject" src/
```

Verify the catch block calls `transaction.rollback()` or `session.rollback()` before re-throwing.

---

## AP-8: Raw SQL Bypasses ORM Version Mechanism

**Risk:** High — ORM's @Version protection is invisible to raw SQL writes.

**Detection:**
```bash
# Find raw SQL UPDATE statements in ORM-managed projects
grep -rn "nativeQuery\|createNativeQuery\|execute_sql\|raw_sql" src/
grep -rn "update_columns\|update_all" app/  # Rails bypasses lock_version
```

Any raw SQL write to an ORM-managed table must manually include the version WHERE clause and check row count.

---

## AP-9: Identity Map Not Used — Multiple Versions in One Session

**Risk:** Medium — Two loads of the same record in one business transaction return different version values, making version checks non-deterministic.

**Detection:** Check that `find(id)` checks a session-scoped Identity Map before querying DB. Most ORMs handle this automatically (Session/DbContext cache). Hand-rolled mappers may not.

**Correct:** `find()` returns the cached object if already loaded in this business transaction.

---

## License

CC-BY-SA-4.0 — Source: BookForge / Patterns of Enterprise Application Architecture by Fowler et al.
