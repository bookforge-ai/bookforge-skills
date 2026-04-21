# Version Column SQL and ORM Config Reference

## Standard Schema (SQL)

```sql
-- Add to every table requiring concurrent-edit protection
ALTER TABLE {table}
  ADD COLUMN version     INTEGER     NOT NULL DEFAULT 0,
  ADD COLUMN modified_by VARCHAR(255),
  ADD COLUMN modified_at TIMESTAMP;
```

`modified_by` and `modified_at` are NOT used in the WHERE clause. They provide context for the collision error message.

## Version-Conditioned SQL Statements

### UPDATE
```sql
UPDATE {table}
SET    field1 = ?,
       ...,
       modified_by = ?,
       modified_at = ?,
       version     = ?          -- new value: old_version + 1
WHERE  id = ?
AND    version = ?;             -- claimed (loaded) version
```
Parameters: `(field1, ..., currentUser, now, oldVersion+1, id, oldVersion)`

### DELETE
```sql
DELETE FROM {table}
WHERE id = ?
AND   version = ?;
```

### Re-query on Collision (row count = 0)
```sql
SELECT version, modified_by, modified_at
FROM   {table}
WHERE  id = ?;
```
- Row returned → record was modified by someone else. Use `modified_by` and `modified_at` in error message.
- No row returned → record was deleted by another session.

---

## ORM-Native Configuration

### Hibernate / JPA (Java)

```java
@Entity
public class Customer extends DomainObject {
    @Version
    private int version;

    @Column(name = "modified_by")
    private String modifiedBy;

    @Column(name = "modified_at")
    private Instant modifiedAt;
}
```

Hibernate auto-generates:
```sql
UPDATE customer SET name=?, modified_by=?, modified_at=?, version=?
WHERE id=? AND version=?
```
Exception: `javax.persistence.OptimisticLockException` (wraps `StaleObjectStateException`).

Catch at service/controller boundary:
```java
@ExceptionHandler(OptimisticLockException.class)
public ResponseEntity<?> handleOptimisticLock(OptimisticLockException ex) {
    // Re-query for modifiedBy + modifiedAt; return 409
}
```

### EF Core (.NET)

**Option A — ConcurrencyCheck on a version int:**
```csharp
[ConcurrencyCheck]
public int Version { get; set; }
```

**Option B — rowversion (SQL Server) / timestamp (PostgreSQL xmin):**
```csharp
[Timestamp]
public byte[] RowVersion { get; set; }
```
Exception: `Microsoft.EntityFrameworkCore.DbUpdateConcurrencyException`.

### SQLAlchemy (Python)

```python
from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customer"
    __mapper_args__ = {"version_id_col": version}

    id      = Column(Integer, primary_key=True)
    version = Column(Integer, nullable=False, default=0)
    # ... other fields
```
Exception: `sqlalchemy.orm.exc.StaleDataError`.

### Rails ActiveRecord

Add migration:
```ruby
add_column :customers, :lock_version, :integer, default: 0, null: false
```

Rails auto-detects `lock_version` column — no model code needed. Exception: `ActiveRecord::StaleObjectError`.

Form must include: `<%= f.hidden_field :lock_version %>`
Strong params must permit: `:lock_version`

### Django (manual implementation)

Django has no built-in optimistic locking. Two approaches:

**Approach A — Filtered update:**
```python
updated = Customer.objects.filter(pk=pk, version=claimed_version).update(
    name=new_name,
    version=claimed_version + 1,
    modified_by=request.user,
    modified_at=timezone.now()
)
if updated == 0:
    raise ConcurrentModificationError(pk, claimed_version)
```

**Approach B — django-concurrency package:**
```python
from concurrency.fields import IntegerVersionField

class Customer(models.Model):
    version = IntegerVersionField()
```

---

## All-Fields WHERE Clause (Frozen Schema Fallback)

When the schema cannot be altered (legacy system), omit the version column and include every field in the WHERE clause:

```sql
UPDATE customer
SET    name = ?, phone = ?, email = ?
WHERE  id = ?
AND    name = ?          -- original loaded value
AND    phone = ?
AND    email = ?;
```

Drawbacks:
- Larger WHERE clause may lose PK index benefits (database-dependent)
- More complex SQL construction; harder to detect which field caused the conflict
- Cannot distinguish "deleted" from "modified to match" if all fields happen to match a later insert

Use only when schema modification is truly impossible.

---

## License

CC-BY-SA-4.0 — Source: BookForge / Patterns of Enterprise Application Architecture by Fowler et al.
