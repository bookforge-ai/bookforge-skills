# ORM Lazy Load Configuration Cheatsheet

Quick reference for configuring Lazy Load (deferred loading) in popular ORMs and frameworks. All map to the Virtual Proxy variant the ORM ships natively.

## Hibernate / Spring Data JPA (Java)

```java
// Default: collections are LAZY, single-valued associations are EAGER
// Best practice: set everything to LAZY, add EAGER only where proven necessary

@OneToMany(fetch = FetchType.LAZY, mappedBy = "order")
@BatchSize(size = 50)   // Critical: prevents ripple loading on parent collections
private List<OrderItem> items;

@ManyToOne(fetch = FetchType.LAZY)  // Override EAGER default
private Customer customer;

// Hot-path override — fetch join for specific use case
@Query("SELECT o FROM Order o JOIN FETCH o.items i JOIN FETCH i.product WHERE o.id = :id")
Order findWithItemsAndProducts(@Param("id") Long id);

// Batch fetch for parent collections — prevents N+1 when iterating orders
@Entity
@BatchSize(size = 50)   // Also valid at entity level (ghosts/proxies batched)
public class Order { ... }
```

## EF Core (C#)

```csharp
// Option 1: Lazy loading proxies (global opt-in)
services.AddDbContext<AppDbContext>(opt =>
    opt.UseLazyLoadingProxies()
       .UseSqlServer(connString));
// All virtual navigation properties become lazy proxies

// Option 2: Explicit loading (Value Holder style — no proxy required)
var order = context.Orders.Find(id);
context.Entry(order).Collection(o => o.Items).Load();  // explicit trigger

// Option 3: Eager with Include (hot-path override)
context.Orders
    .Include(o => o.Items)
    .ThenInclude(i => i.Product)
    .Where(o => o.Id == id)
    .FirstOrDefault();

// Option 4: Split queries (avoids Cartesian explosion on large collections)
context.Orders
    .Include(o => o.Items)
    .AsSplitQuery()   // EF Core 5+: issues separate SELECT per Include
    .ToList();
```

## SQLAlchemy ORM (Python)

```python
from sqlalchemy.orm import relationship

class Order(Base):
    # lazy='select' (default): load on first access, one query per parent — RIPPLE RISK
    items_default = relationship("OrderItem", lazy="select")

    # lazy='selectin': one IN-clause query for all loaded parents — PREFERRED for collections
    items = relationship("OrderItem", lazy="selectin")

    # lazy='joined': eager join in the same query (use for single-valued associations)
    customer = relationship("Customer", lazy="joined")

    # lazy='subquery': subquery instead of JOIN (avoids Cartesian explosion for collections)
    items_subquery = relationship("OrderItem", lazy="subquery")

    # lazy='raise': raises error if accessed without explicit load — enforces discipline
    items_strict = relationship("OrderItem", lazy="raise")

# Query-level override (ignores model default)
session.query(Order).options(
    joinedload(Order.customer),         # eager join for this query
    subqueryload(Order.items),          # batch subquery for this query
).all()
```

Recommendation: use `lazy="selectin"` for one-to-many collections (batch load, no Cartesian product). Use `lazy="joined"` for many-to-one / one-to-one (single-row joins are safe). Use `lazy="raise"` in performance-critical code paths to catch accidental lazy access.

## Django ORM (Python)

Django ORM does not configure laziness on the model — all ForeignKey and related manager access is lazy by default. You opt into batch loading at the queryset level.

```python
# N+1 — BAD: each order.customer triggers a separate query
orders = Order.objects.all()
for order in orders:
    print(order.customer.name)  # 1 query per order

# select_related — SQL JOIN for FK / one-to-one (eager for this queryset)
orders = Order.objects.select_related("customer").all()

# prefetch_related — separate batch query for reverse FK, M2M, generic relations
orders = Order.objects.prefetch_related("items").all()

# Chain both
orders = Order.objects.select_related("customer").prefetch_related("items__product")

# Prefetch with custom queryset (filter, order, annotate the prefetch)
from django.db.models import Prefetch
orders = Order.objects.prefetch_related(
    Prefetch("items", queryset=OrderItem.objects.filter(active=True).select_related("product"))
)
```

## Rails ActiveRecord (Ruby)

```ruby
# N+1 — BAD
Order.all.each { |o| puts o.customer.name }  # 1 query per order

# includes — smart: uses preload or eager_load depending on WHERE/ORDER
Order.includes(:customer).all

# preload — always separate queries (like Django prefetch_related)
Order.preload(:customer, :items)

# eager_load — always LEFT OUTER JOIN (use when filtering on association)
Order.eager_load(:customer).where(customers: { vip: true })

# Nested associations
Order.includes(items: :product).all
```

## TypeORM (TypeScript/Node)

```typescript
// Model: lazy relation uses Promise<T>
@Entity()
export class Order {
    @OneToMany(() => OrderItem, item => item.order, { lazy: true })
    items: Promise<OrderItem[]>;   // caller must await

    @ManyToOne(() => Customer, { eager: true })  // always-eager
    customer: Customer;
}

// Query builder with explicit join (hot-path override)
const orders = await dataSource
    .getRepository(Order)
    .createQueryBuilder("order")
    .leftJoinAndSelect("order.items", "item")
    .leftJoinAndSelect("item.product", "product")
    .where("order.id = :id", { id })
    .getOne();

// Find options with relations (eager for this query)
const order = await orderRepo.findOne({
    where: { id },
    relations: { items: { product: true }, customer: true }
});
```

## Summary Decision Matrix

| ORM | Collection default | Fix ripple loading | Single-valued default | Hot-path override |
|---|---|---|---|---|
| Hibernate | LAZY | `@BatchSize(50)` | EAGER (change to LAZY!) | `JOIN FETCH` in JPQL |
| EF Core | Lazy (with proxies) or None | `.AsSplitQuery()` | Lazy or None | `.Include().ThenInclude()` |
| SQLAlchemy | `lazy='select'` (per-access) | `lazy='selectin'` | `lazy='select'` | `joinedload()` option |
| Django | Lazy (always) | `prefetch_related()` | Lazy (always) | `select_related()` |
| Rails | Lazy (always) | `includes()` / `preload()` | Lazy (always) | `eager_load()` |
| TypeORM | Depends on config | `relations:` in find options | `eager: true` | `leftJoinAndSelect()` |
