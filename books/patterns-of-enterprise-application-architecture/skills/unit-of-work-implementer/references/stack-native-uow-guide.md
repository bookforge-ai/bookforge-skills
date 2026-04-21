# Stack-Native UoW Guide — Unit of Work

All major ORM frameworks include a built-in Unit of Work. This guide maps the UoW contract
to each framework's API and shows correct per-request scoping.

---

## Hibernate / Spring Data JPA (Java)

**UoW object:** `Session` (Hibernate) / `EntityManager` (JPA)

| UoW concept | Hibernate/JPA API |
|---|---|
| registerNew | `session.persist(entity)` |
| registerDirty | automatic (snapshot diff on flush) |
| registerClean | automatic on `session.find(class, id)` |
| registerRemoved | `session.remove(entity)` |
| commit | `session.flush()` + `tx.commit()` |
| rollback | `tx.rollback()` |
| clear | `session.close()` (or `session.clear()` to detach all) |
| Identity Map | First-level cache (L1) — built in, per-Session |

**Per-request scoping (Spring Boot):**
```java
// Use @Transactional on service methods — Spring manages Session lifecycle
@Service
public class OrderService {
    @Transactional
    public void confirmOrder(Long orderId) {
        Order order = orderRepo.findById(orderId).orElseThrow();
        order.setStatus("CONFIRMED");
        // session.flush() happens automatically at @Transactional boundary
    }
}
```

**Pitfalls:**
- `LazyInitializationException`: accessing a lazy collection after Session closes. Fix: use `@Transactional` to keep session open, or eager-load what you need.
- Open Session in View (OSIV): Hibernate's default in Spring Boot opens Session for the full request (including view rendering). This can mask N+1 issues. Consider disabling (`spring.jpa.open-in-view=false`) and being explicit about loading.

---

## Entity Framework Core (.NET)

**UoW object:** `DbContext`

| UoW concept | EF Core API |
|---|---|
| registerNew | `dbContext.Add(entity)` or `dbContext.EntitySet.Add(entity)` |
| registerDirty | automatic (change tracker detects mutations on tracked entities) |
| registerClean | automatic on `dbContext.EntitySet.Find(id)` or any LINQ query |
| registerRemoved | `dbContext.Remove(entity)` |
| commit | `await dbContext.SaveChangesAsync()` |
| rollback | dispose `DbContext` without calling `SaveChanges` |
| clear | `dbContext.ChangeTracker.Clear()` |
| Identity Map | Change tracker — per-DbContext instance |

**Per-request scoping (ASP.NET Core):**
```csharp
// Register as Scoped in DI — one instance per HTTP request
builder.Services.AddDbContext<AppDbContext>(opts =>
    opts.UseSqlServer(connectionString));

// Inject into controller or service
public class OrdersController : ControllerBase {
    private readonly AppDbContext _db;
    public OrdersController(AppDbContext db) { _db = db; }

    [HttpPut("{id}/confirm")]
    public async Task<IActionResult> Confirm(int id) {
        var order = await _db.Orders.FindAsync(id);
        order.Status = "CONFIRMED";
        await _db.SaveChangesAsync();   // single commit for the operation
        return Ok();
    }
}
```

**Optimistic Lock:**
```csharp
public class Order {
    [Timestamp]  // EF Core adds WHERE RowVersion=? on UPDATE
    public byte[] RowVersion { get; set; }
}
// DbUpdateConcurrencyException thrown on collision
```

**Pitfalls:**
- Never register `DbContext` as Singleton in ASP.NET Core — it will accumulate state across all requests.
- Avoid multiple `SaveChanges()` calls per request unless each is an intentional partial commit.

---

## SQLAlchemy (Python)

**UoW object:** `Session`

| UoW concept | SQLAlchemy API |
|---|---|
| registerNew | `session.add(entity)` |
| registerDirty | automatic (attribute change tracking) |
| registerClean | automatic on `session.get(Model, pk)` or query |
| registerRemoved | `session.delete(entity)` |
| commit | `session.commit()` |
| rollback | `session.rollback()` |
| clear | `session.close()` or `session.expunge_all()` |
| flush without commit | `session.flush()` (pushes SQL; ID assigned; no DB COMMIT) |
| Identity Map | Identity Map — per-Session instance |

**Per-request scoping (FastAPI):**
```python
from sqlalchemy.orm import Session
from fastapi import Depends

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.put("/orders/{order_id}/confirm")
def confirm_order(order_id: int, db: Session = Depends(get_db)):
    order = db.get(Order, order_id)
    order.status = "CONFIRMED"
    db.commit()
    db.refresh(order)
    return order
```

**Pitfalls:**
- Never use a module-level `Session` singleton — it creates one UoW for all requests.
- `DetachedInstanceError`: accessing a lazy attribute after `session.close()`. Fix: `db.refresh(obj)` or `expire_on_commit=False` + reload.
- `session.flush()` is useful to get auto-generated IDs mid-operation without committing.

---

## TypeORM (TypeScript/JavaScript)

**UoW object:** `EntityManager` / `QueryRunner`

```typescript
// Transaction with EntityManager — explicit UoW scope
await dataSource.transaction(async (manager) => {
    const order = await manager.findOneBy(Order, { id: orderId });
    order.status = "CONFIRMED";
    await manager.save(order);       // registerDirty + immediate flush within tx
    // manager.remove(entity) for DELETE
});
// Transaction commits when the async function resolves; rolls back on throw
```

**Pitfalls:**
- `save()` in TypeORM is an upsert (INSERT or UPDATE based on ID presence) — it does not batch changes until transaction commits.
- QueryRunner gives more explicit control: `await queryRunner.startTransaction()`, `await queryRunner.commitTransaction()`.

---

## Django ORM (Python)

Django ORM has no first-class Unit of Work or dirty tracker. Each `model.save()` writes immediately.

**Partial equivalent — `transaction.atomic()`:**
```python
from django.db import transaction

with transaction.atomic():
    order.status = "CONFIRMED"
    order.save()                     # writes immediately within transaction
    for item in removed_items:
        item.delete()
# DB COMMIT at end of with block; rollback on exception
```

**Batch writes:**
```python
Order.objects.bulk_update([order1, order2], ['status'])
LineItem.objects.bulk_create([item1, item2])
```

Django does not provide identity-map-level identity consistency. Loading the same row twice
yields two Python objects. Rely on Django's queryset caching (within a queryset, not across
separate `.get()` calls) and keep your transactions short.
