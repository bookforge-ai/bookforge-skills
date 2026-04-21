# Identity Map Implementation — Unit of Work

## Purpose

The Identity Map ensures that each database row is loaded into memory exactly once per
business operation (per UoW). Any request for the same primary key returns the same
in-memory instance. This prevents:

- **Conflicting updates:** two objects for the same row, both modified, producing undefined commit behavior.
- **Phantom duplicates:** the same entity appearing twice in a list, with different in-memory states.
- **Double-loading:** unnecessary database round trips for rows already in memory.

Primary purpose = identity consistency. Performance caching = beneficial side-effect.

## Key Design Choices

### 1. Map Key

Use the entity's primary key. For surrogate keys (auto-generated integers or UUIDs):
- Java: `Map<Long, DomainObject>` per entity class, or `Map<String, DomainObject>` with composite key `"ClassName:id"`.
- Python/TS: `dict[(type, id), entity]` or `dict[str, entity]` with `f"{cls.__name__}:{id}"` key.

For composite natural keys: encode the tuple as the map key. Prefer surrogate keys to avoid this complexity (see Identity Field pattern).

### 2. Explicit vs Generic Map

**Explicit map** (one method per entity type):
```java
public Person findPerson(Long id) {
    return (Person) personMap.get(id);
}
public Order findOrder(Long id) {
    return (Order) orderMap.get(id);
}
```
Pros: compile-time type safety; clear API. Cons: must add a new method per entity type.

**Generic map** (single method, all types):
```java
public DomainObject find(Class type, Long id) {
    Map<Long, DomainObject> map = maps.get(type);
    return map != null ? map.get(id) : null;
}
```
Pros: no code change when adding new entity types. Cons: caller must cast; requires all keys to be the same type.

Fowler prefers explicit maps for readability and type safety. Generic maps are common in ORM internals.

### 3. One Map per Class vs One Map for the Whole Session

**One map per class (recommended for most codebases):**
```java
Map<Long, Order>    orderMap    = new HashMap<>();
Map<Long, LineItem> lineItemMap = new HashMap<>();
Map<Long, Product>  productMap  = new HashMap<>();
```
Works well when domain objects and tables are isomorphic (one class = one table).

**One map for the whole session (with session-unique keys):**
```java
Map<String, DomainObject> singleMap = new HashMap<>();
// Key: "Order:42", "LineItem:17", etc.
```
Simpler code; requires globally unique keys across all entity types. Use a surrogate key
strategy that guarantees this (e.g., sequence prefix per table, UUID).

**Inheritance:** For class hierarchies (Vehicle → Car, Vehicle → Truck), use a single map
for the entire inheritance tree. Polymorphic lookups then need only one map.

### 4. Where to Store the Identity Map

The Identity Map must be session-scoped — each request/business-operation gets its own
instance, isolated from all others. Options:

- **Inside the UoW:** simplest; UoW is already per-session. (Recommended.)
- **Thread-scoped Registry:** `ThreadLocal<IdentityMap>` — works for synchronous frameworks.
- **Async context variable:** Python `contextvars.ContextVar`, Java virtual thread scope.

Never store the Identity Map in a static field or application-scope singleton.

## Integration with UoW Commit Cycle

```
find(class, id)
   ↓
identityMap.get(class, id) exists?
   YES → return cached instance (no DB call)
   NO  → load from DB → registerClean(entity) → identityMap.put(key, entity) → return

registerNew(entity)    → identityMap.put(key, entity)
registerRemoved(entity) → identityMap.remove(key)
commit() → [INSERT / UPDATE / DELETE] → clear all maps
```

## Read-Only Entities and Shared Maps

If certain entities are truly read-only (e.g., reference data like country codes, product
categories), they can share a session-spanning or even application-scoped Identity Map.
This is safe only when:
1. No business operation ever modifies these entities.
2. Their lifetime in the map is actively managed (e.g., invalidated when reference data changes).

Fowler notes this as an exception; the default is always per-session isolation.
