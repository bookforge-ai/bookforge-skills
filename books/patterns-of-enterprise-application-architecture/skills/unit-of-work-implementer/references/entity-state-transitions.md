# Entity State Transitions — Unit of Work

## The Four States

Every entity in a Unit of Work business operation is in exactly one state:

| State | Meaning | SQL on commit |
|-------|---------|---------------|
| **New** | Created in memory; not yet in DB | INSERT |
| **Dirty** | Loaded from DB, then modified | UPDATE |
| **Clean** | Loaded from DB, not modified | (none) |
| **Removed** | Marked for deletion | DELETE |

## State Machine

```
            registerNew()
[Not tracked] ──────────────→ [New]
                                │
                                │ commit() INSERT
                                ↓
[Not tracked] ←─── clear() ── [Clean] ←── registerClean() (on DB load)
                                │
                          setField() / markDirty()
                                │
                                ↓
                            [Dirty] ──── commit() UPDATE ──→ [Clean] / discard
                                │
                          registerRemoved()
                                │
                                ↓
                           [Removed] ──── commit() DELETE ──→ discard

[New] ──── registerRemoved() ──→ removed from newObjects (no DB write needed)
```

## Java Object Registration Example

```java
// Layer Supertype for all domain objects
public abstract class DomainObject {
    private Long id;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    protected void markNew() {
        UnitOfWork.getCurrent().registerNew(this);
    }

    protected void markDirty() {
        UnitOfWork.getCurrent().registerDirty(this);
    }

    protected void markRemoved() {
        UnitOfWork.getCurrent().registerRemoved(this);
    }
}

// Concrete entity uses object registration in setters
public class Order extends DomainObject {

    public static Order create(Long id, String status) {
        Order order = new Order(id, status);
        order.markNew();    // registers immediately on creation
        return order;
    }

    public void setStatus(String status) {
        this.status = status;
        markDirty();        // registers on every mutation
    }

    public void remove() {
        markRemoved();
    }
}
```

## UnitOfWork Registration Methods

```java
public class UnitOfWork {
    private List<DomainObject> newObjects     = new ArrayList<>();
    private List<DomainObject> dirtyObjects   = new ArrayList<>();
    private List<DomainObject> removedObjects = new ArrayList<>();
    private Map<String, DomainObject> identityMap = new HashMap<>();

    // ThreadLocal for current UoW per thread/request
    private static ThreadLocal<UnitOfWork> current = new ThreadLocal<>();
    public static UnitOfWork getCurrent()         { return current.get(); }
    public static void newCurrent()               { current.set(new UnitOfWork()); }
    public static void setCurrent(UnitOfWork uow) { current.set(uow); }

    public void registerNew(DomainObject obj) {
        assert obj.getId() != null           : "id must not be null";
        assert !dirtyObjects.contains(obj)   : "object must not be dirty";
        assert !removedObjects.contains(obj) : "object must not be removed";
        assert !newObjects.contains(obj)     : "object must not already be new";
        newObjects.add(obj);
        identityMap.put(key(obj), obj);
    }

    public void registerDirty(DomainObject obj) {
        assert obj.getId() != null           : "id must not be null";
        assert !removedObjects.contains(obj) : "removed objects cannot be dirtied";
        if (!newObjects.contains(obj) && !dirtyObjects.contains(obj)) {
            dirtyObjects.add(obj);
        }
    }

    public void registerClean(DomainObject obj) {
        assert obj.getId() != null : "id must not be null";
        identityMap.put(key(obj), obj);
        // no list entry — clean objects have no SQL action on commit
    }

    public void registerRemoved(DomainObject obj) {
        assert obj.getId() != null : "id must not be null";
        if (newObjects.remove(obj)) return; // never persisted — just forget
        dirtyObjects.remove(obj);
        if (!removedObjects.contains(obj)) {
            removedObjects.add(obj);
        }
        identityMap.remove(key(obj));
    }

    private String key(DomainObject obj) {
        return obj.getClass().getName() + ":" + obj.getId();
    }
}
```

## Caller Registration Alternative

Use when domain objects cannot depend on UoW (e.g., simple value-object-style entities):

```java
// Application/service code must call register explicitly
UnitOfWork uow = UnitOfWork.getCurrent();
Order order = orderMapper.find(orderId);  // mapper calls registerClean internally
order.setStatus("CONFIRMED");
uow.registerDirty(order);               // caller must remember this
uow.commit();
```

Risk: forgetting `registerDirty` silently drops the update. Mitigate with code review checklists or IDE inspections.

## UoW-Controlled (Snapshot-Based) Strategy

Used by ORMs (Hibernate, EF Core, SQLAlchemy):

1. On entity load → UoW stores a deep copy (snapshot) of field values.
2. On `commit()` → UoW compares current field values to snapshot.
3. Differences → generate UPDATE for only changed columns.
4. No `markDirty()` calls in domain code; transparency is complete.

Trade-off: higher memory usage (holds snapshots) and slightly higher commit-time cost.
