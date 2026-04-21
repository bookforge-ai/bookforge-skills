# Commit Ordering — Unit of Work

## Why Order Matters

Relational databases enforce FK constraints. If `LineItem.order_id` references `Order.id`,
inserting a `LineItem` before its `Order` exists raises a FK violation. Similarly, deleting
an `Order` before its `LineItem` children raises a constraint error.

The Unit of Work must perform all INSERTs in FK dependency order (parents first) and all
DELETEs in reverse FK dependency order (children first).

## Commit Sequence

```
1. INSERT newObjects    — parents before children
2. UPDATE dirtyObjects  — order within this set is usually safe
3. DELETE removedObjects — children before parents (reverse of INSERT order)
4. DB COMMIT
5. Clear UoW state
```

## Order/LineItem/Product Example

FK graph:
```
Product  ←── LineItem ──→ Order
```

- `LineItem.product_id` → `Product.id`
- `LineItem.order_id`   → `Order.id`

INSERT order: `Product` and `Order` first (no dependencies on each other), then `LineItem`.

DELETE order: `LineItem` first, then `Order` and `Product`.

## Explicit Ordering (Small Schemas)

For small, well-known schemas, hardcode the order:

```java
// INSERT
for (DomainObject obj : filter(newObjects, Product.class))  insertMapper(obj);
for (DomainObject obj : filter(newObjects, Order.class))    insertMapper(obj);
for (DomainObject obj : filter(newObjects, LineItem.class)) insertMapper(obj);

// DELETE (reverse)
for (DomainObject obj : filter(removedObjects, LineItem.class)) deleteMapper(obj);
for (DomainObject obj : filter(removedObjects, Order.class))    deleteMapper(obj);
for (DomainObject obj : filter(removedObjects, Product.class))  deleteMapper(obj);
```

## Topological Sort (Large or Dynamic Schemas)

For larger applications, drive ordering from metadata:

```python
# Dependency graph as adjacency list (child → [parents])
FK_DEPS = {
    "LineItem": ["Order", "Product"],
    "Order":    [],
    "Product":  [],
}

def topological_sort(deps: dict) -> list:
    """Kahn's algorithm — returns insertion order (parents first)."""
    in_degree = {node: 0 for node in deps}
    for node, parents in deps.items():
        for parent in parents:
            in_degree[parent] = in_degree.get(parent, 0)
    for node, parents in deps.items():
        for parent in parents:
            in_degree[node] += 0   # count incoming, not outgoing

    # Correctly: count how many other nodes depend on each node
    rev = {}
    for node, parents in deps.items():
        for parent in parents:
            rev.setdefault(parent, []).append(node)

    in_deg = {node: len(parents) for node, parents in deps.items()}
    queue = [n for n, d in in_deg.items() if d == 0]
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for child in rev.get(node, []):
            in_deg[child] -= 1
            if in_deg[child] == 0:
                queue.append(child)
    return order  # INSERT order; reverse() for DELETE order
```

## Deferring FK Constraint Checks

Most databases can defer FK constraint checking to transaction commit time:

```sql
-- PostgreSQL
SET CONSTRAINTS ALL DEFERRED;

-- Oracle
ALTER SESSION SET CONSTRAINTS = DEFERRED;
```

With deferred checking, INSERT/DELETE order within the transaction does not matter — only
the final committed state must satisfy constraints. If your database supports this, you can
simplify the UoW commit by omitting the topological sort. Check your database and DBA policy
before relying on this.

## Minimizing Deadlocks

Deadlocks often arise when two transactions update the same rows in opposite order. The UoW
provides a natural solution: always commit tables (and rows within tables) in the same fixed
sequence. Two concurrent transactions that both start with `Order` then `LineItem` will
queue behind each other rather than deadlock.
