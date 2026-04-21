# Lazy Load Variant Comparison

Source: Patterns of Enterprise Application Architecture, Ch. 11 (Fowler et al., 2002)

## Four Variants at a Glance

| Dimension | Lazy Initialization | Virtual Proxy | Value Holder | Ghost |
|---|---|---|---|---|
| **Mechanism** | Getter checks null/flag; loads on first access | Separate proxy object with same interface; loads on first method call | Field is a wrapper object; caller calls `.getValue()` | Real domain object with placeholder state; loads all fields on first access |
| **Calling code must change** | No (transparent via getter) | No (proxy has same interface) | Yes (must call `.getValue()`) | No (transparent via field accessor instrumentation) |
| **Identity preserved** | Yes (the real object holds the field) | No (proxy != real object) | N/A (holder is internal) | Yes (the object IS the ghost) |
| **Proxy identity trap risk** | None | High — two proxies for same row are not `==` | None | None |
| **Null-value safe** | No by default — use a `loaded` flag if null is valid | Yes | Yes | Yes |
| **ORM support** | Native in Active Record ORMs; manual in Data Mapper | Standard ORM lazy proxy (Hibernate, EF Core, TypeORM) | Rare — mostly hand-rolled | Hibernate "extra lazy"; custom bytecode; SQLAlchemy descriptors |
| **Statically-typed language friction** | Low | High (one proxy class per proxied class unless AOP/codegen) | Low | High (requires AOP or bytecode instrumentation) |
| **Dynamically-typed language friction** | Low | Low (single generic proxy possible) | Low | Low |
| **Best for** | Hand-rolled Active Record; simple optional fields | ORM-backed Data Mapper; collections | Explicit lazy-load in Data Mapper without proxy magic | Instrumentation-heavy stacks; when identity correctness is critical |

## Variant Details

### Lazy Initialization

```java
// Java — simplest form
public List<Product> getProducts() {
    if (products == null) {
        products = productMapper.findForSupplier(this.id);
    }
    return products;
}

// Safe form when null is a valid value
public List<Product> getProducts() {
    if (!productsLoaded) {
        products = productMapper.findForSupplier(this.id);
        productsLoaded = true;
    }
    return products;
}
```

Fowler's note: works best with Active Record, Table Data Gateway, Row Data Gateway. Creates a coupling from domain object to database. For Data Mapper, use Virtual Proxy instead to keep domain ignorant of persistence.

### Virtual Proxy

The proxy implements the same interface as the target. On first method call, it loads the real object and delegates. ORM frameworks ship this as their default lazy proxy implementation.

Identity trap: `proxy1 != proxy2` even if both proxy the same database row. Fix by ensuring the ORM Identity Map (session/unit-of-work first-level cache) returns the same proxy instance for a given primary key. Override `equals()` to compare by primary key, not by reference.

For collections: a virtual collection (list proxy) is the correct technique — the whole collection is the lazy unit, not each element.

### Value Holder

```java
public class ValueHolder<T> {
    private T value;
    private boolean loaded = false;
    private final Supplier<T> loader;

    public ValueHolder(Supplier<T> loader) { this.loader = loader; }

    public T getValue() {
        if (!loaded) {
            value = loader.get();
            loaded = true;
        }
        return value;
    }
}

// Usage in domain class
class Supplier {
    private ValueHolder<List<Product>> products;

    public List<Product> getProducts() { return products.getValue(); }
}
```

Calling code that directly accesses `products` (not through the getter) will bypass the load. Enforce self-encapsulation strictly.

### Ghost

A ghost is a real domain object in a partial state. It has its primary key but no other data. Every field accessor triggers a full load.

```csharp
// C# — domain supertype approach (Fowler's example)
public abstract class DomainObject {
    public LoadStatus Status { get; private set; } = LoadStatus.Ghost;
    public bool IsGhost => Status == LoadStatus.Ghost;

    protected void Load() {
        if (IsGhost) DataSource.Load(this);  // Registry + Separated Interface
    }
}

// Domain class — every property triggers Load()
public class Employee : DomainObject {
    private string _name;
    public string Name {
        get { Load(); return _name; }
        set { Load(); _name = value; }
    }
}
```

Advantage over Virtual Proxy: the ghost IS in the Identity Map immediately on creation (even before load). No identity trap. Two references to the same ghost are the same object.

Disadvantage: requires instrumentation of every field accessor. Ideal target for aspect-oriented programming or bytecode post-processing.

Load states: GHOST → LOADING → LOADED. The LOADING state prevents recursive load calls triggered by associations loaded during the load operation itself.

## Ripple Loading: The Critical Anti-Pattern

Ripple loading occurs when a collection contains individually-lazy objects and the collection is iterated:

```
for each order in orders:          // 1 query: SELECT * FROM orders
    print order.items               // N queries: SELECT * FROM items WHERE order_id = ?
```

Result: N+1 queries. At N=500 this causes 501 database round-trips.

**Wrong fix:** make each `item` load itself lazily (this is already the problem).
**Right fix:** make the collection (`items`) the lazy unit — one query loads all items for all orders.

Batch loading approaches:
- Hibernate `@BatchSize(50)`: loads items for up to 50 orders per SQL `IN` clause
- SQLAlchemy `lazy='selectin'`: one `SELECT WHERE parent_id IN (...)` for all loaded parents
- Django `prefetch_related('items')`: one query per relation for the full QuerySet
- EF Core `.Include(o => o.Items)`: JOIN FETCH at query time
