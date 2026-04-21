---
name: lazy-load-strategy-implementer
description: |
  Implement Lazy Load (deferred loading) correctly in a persistence layer to avoid N+1 queries, ripple loading, and proxy identity traps. Use when encountering slow object graph loads, N+1 query problems, out-of-memory on eager loading, ORM lazy loading misconfiguration, or deciding between eager vs lazy loading strategies. Applies to: Hibernate FetchType.LAZY / @BatchSize, SQLAlchemy lazy='select'/'selectin'/'subquery', Django select_related / prefetch_related, EF Core Include() vs Load(), TypeORM eager/lazy relations, Rails includes/preload/eager_load, hand-rolled Data Mapper with virtual proxy patterns. Covers all four implementation variants — lazy initialization, virtual proxy, value holder, ghost — with applicability rules and trade-off analysis. Identifies and fixes the ripple loading anti-pattern (N+1 on collections), the proxy identity trap (two proxies, same row, broken equality), and misuse of Lazy Load on small graphs that should just be eagerly loaded. Produces an implementation plan: chosen variant, ORM configuration or code sketch, batch loading config, eager-load overrides for hot paths, Identity Map integration, and a ripple-loading audit. Requires knowing the data-source pattern already in use (Data Mapper / ORM vs Active Record); if unknown invoke data-source-pattern-selector first.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/lazy-load-strategy-implementer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [3, 11]
domain: persistence
tags: ["lazy-loading", "persistence", "orm", "performance", "design-patterns", "n-plus-one", "deferred-loading", "batch-loading", "prefetch", "virtual-proxy", "object-relational-mapping", "fowler-peaa", "database-performance"]
depends-on: ["data-source-pattern-selector"]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Persistence layer source code (entity/model classes, repositories or mappers, ORM configuration). Provide specific classes exhibiting N+1, slow load symptoms, or memory pressure."
    - type: document
      description: "Description of which data-source pattern is in use (Data Mapper / ORM, Active Record, hand-rolled), the ORM/framework name, the domain object graph shape (which associations are optional vs always-needed), and observed performance symptoms."
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Any agent environment with access to the codebase. Works best when the specific slow queries or N+1 symptoms can be located in source code or query logs."
discovery:
  goal: "Produce a Lazy Load implementation plan — variant selection, code sketch or ORM config, batch loading, eager-load overrides, Identity Map integration, and ripple-loading audit."
  tasks:
    - "Identify the data-source pattern and ORM/framework in use"
    - "Classify associations: optional-deep (lazy candidate), expensive-field (lazy candidate), always-needed (eager), immediately-iterated (eager with batch)"
    - "Detect existing ripple loading: collections of individually-lazy objects iterated in a loop"
    - "Select a Lazy Load variant: Virtual Proxy (ORM-provided), Lazy Initialization (hand-rolled Active Record), Value Holder (explicit wrapper), Ghost (instrumentation-heavy stacks)"
    - "Identify proxy identity traps and prescribe Identity Map integration"
    - "Specify batch loading configuration to prevent ripple loading on lazy collections"
    - "Identify hot paths that need eager-load overrides (fetch joins / includes)"
    - "Write the implementation plan artifact"
  audience:
    roles: ["senior-backend-engineer", "software-architect", "tech-lead"]
    experience: "intermediate-to-advanced"
  when_to_use:
    triggers:
      - "Profiling reveals N+1 queries: N database calls where 1 batch would suffice"
      - "Iterating a collection triggers one query per element"
      - "Eager loading a large object graph consumes excessive memory or makes startup slow"
      - "ORM lazy loading is configured but equality/hashCode bugs appear with proxy objects"
      - "Choosing between FetchType.LAZY and FetchType.EAGER in Hibernate / JPA"
      - "Configuring SQLAlchemy relationship lazy parameter"
      - "Deciding when to use Django prefetch_related vs select_related vs neither"
      - "Hand-rolling deferred loading for a large blob or expensive computed field"
      - "Ripple loading crippling an application's performance at scale"
    prerequisites:
      - "Data-source pattern chosen. If unknown, run `data-source-pattern-selector` first."
    not_for:
      - "Query optimization, index design, or schema changes unrelated to loading strategy"
      - "Concurrency or locking concerns — see `optimistic-offline-lock-implementer`"
      - "Choosing the data-source pattern itself — this skill implements Lazy Load within a chosen pattern"
      - "Applications with small, fully in-memory datasets that never hit a database"
  environment:
    codebase_required: false
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: "{filled by tester}"
      baseline: "{filled by tester}"
      delta: "{filled by tester}"
    tested_at: "{filled by tester}"
    eval_count: "{filled by tester}"
    assertion_count: 13
    iterations_needed: "{filled by tester}"
---

# Lazy Load Strategy Implementer

## When to Use

You have an object graph backed by a relational database. Loading some objects eagerly pulls in far more data than any single use case needs — but loading objects lazily without discipline produces N+1 queries (one database call per object in a collection) or ripple loading (a cascade of individual loads triggered across the graph).

Apply this skill when:
- A query log shows N+1 round-trips for a collection
- A single user action triggers dozens of database calls
- Memory or startup latency is unacceptable due to eager-loading large associations
- You are configuring or auditing ORM fetch strategies

Do not apply Lazy Load when:
- The object is always needed immediately after loading its parent (eager load with a fetch-join is simpler)
- The collection is always iterated in full by the first use case that loads the parent (eager load it)
- The application uses a very small, bounded dataset (load everything upfront)

Prerequisite: know which data-source pattern the codebase uses. If unclear, invoke `data-source-pattern-selector` first, or ask the user. Lazy Load implementation differs significantly between hand-rolled Active Record (Lazy Initialization is simplest) and Data Mapper / ORM (Virtual Proxy or Ghost are standard).

## Context & Input Gathering

Gather the following before proceeding:

**Required:**
- Data-source pattern in use: Active Record / Row Data Gateway / Table Data Gateway / Data Mapper (ORM)
- ORM or framework name (Hibernate, EF Core, SQLAlchemy, Django ORM, TypeORM, ActiveRecord Rails, hand-rolled)
- Which associations or fields are suspected of causing performance problems

**Observable from codebase (Grep/Read):**
- ORM relationship annotations / configuration (`@OneToMany`, `relationship()`, `belongs_to`, etc.)
- Existing fetch strategy declarations (`FetchType.LAZY`, `lazy='select'`, `include:` option)
- Query log patterns: identical SELECT statements repeated N times in a loop context

**Defaults if not provided:**
- If ORM is present: assume it ships a Virtual Proxy implementation; configure rather than hand-roll
- If no ORM: Lazy Initialization is the safest starting variant

**Sufficiency check:** If you know the ORM name, one or two entity classes, and the symptom (N+1 or memory pressure), that is enough to produce the implementation plan. Do not wait for full codebase access.

## Process

### Step 1 — Classify every association as eager or lazy candidate

WHY: Applying Lazy Load blindly to every association trades an eager-loading problem for a ripple-loading problem. The classification determines which associations get Lazy Load, and which get eager loading or fetch-join overrides.

For each association in the entity/model:
- **Lazy candidate:** association is optional for most use cases AND loading it requires an extra database round-trip AND the data is not always needed immediately
- **Eager candidate:** association is always used immediately after the parent loads (address on User, status on Order), OR the collection is always iterated in full by the primary use case
- **Hot-path override candidate:** association is lazy by default but specific use cases (reports, listings) need it eagerly — mark for fetch-join override in those queries

Document the classification in a table: association name | direction | lazy/eager/override | reason.

### Step 2 — Detect existing ripple loading

WHY: Ripple loading is the primary failure mode of naively applied Lazy Load. A collection of individually-lazy objects iterated in a loop causes N database calls where one batch call would suffice. This must be identified before choosing a variant.

Search the codebase for these patterns:
- A loop over a collection, with a field access or method call inside the loop that touches an association on each element
- ORM queries that load a list, followed by property accesses on each element that are not covered by a `JOIN FETCH`, `include`, `prefetch_related`, or batch size config

Flag each occurrence: it is a ripple-loading site. The fix in every case is: make the *collection itself* the lazy unit, loaded in one batch, not each element individually.

### Step 3 — Select a Lazy Load variant

WHY: The four variants differ in how visible the lazy mechanism is to calling code, what identity guarantees they provide, and how much infrastructure they require. The ORM context nearly always determines which variant is practical.

Choose one variant per the decision tree:

**If using a standard ORM (Hibernate, EF Core, SQLAlchemy ORM, Django ORM, TypeORM, Rails ActiveRecord):**
- Use the **Virtual Proxy** the ORM provides natively. Configure via fetch type / relationship option, not hand-rolled code. The ORM's proxy already handles load-on-access.
- Skip to Step 4 to configure correctly and prevent ripple loading.

**If using hand-rolled Data Mapper or Active Record (no ORM proxy available):**
- Choose **Lazy Initialization** for simple cases: a getter checks `if (field == null) { field = load(); }` and returns the field. Simplest, but null must not be a legitimate value — use a sentinel flag or loaded boolean if it can be.
- Choose **Value Holder** when you need an explicit, strongly-typed lazy wrapper and calling code can tolerate calling `.getValue()` instead of accessing the field directly. Useful when you want laziness to be visible in the type system.
- Choose **Ghost** when you need identity preservation without a separate proxy object and your stack supports instrumented field access (aspect-oriented programming, bytecode manipulation, or Python descriptors). Every field accessor triggers a full load on first access.
- Do NOT use Virtual Proxy for domain classes in statically-typed languages unless an AOP or code-generation facility is available — you must create one proxy class per proxied class, which becomes unwieldy.

For collections specifically: regardless of variant, always make the collection itself the lazy unit (one database call loads all elements). Never create a collection of individually-lazy domain objects.

Record: chosen variant + rationale + which associations it applies to.

### Step 4 — Implement or configure the chosen variant

WHY: Abstract variant choice produces no value without an executable implementation or ORM configuration.

**Virtual Proxy via ORM (preferred for ORM stacks):**

Java/Hibernate:
```java
@OneToMany(fetch = FetchType.LAZY, mappedBy = "order")
@BatchSize(size = 50)  // prevents ripple loading: loads 50 collections per SQL IN clause
private List<OrderItem> items;
```

Python/SQLAlchemy:
```python
# lazy='select' = default proxy; 'selectin' = batch load (prevents ripple)
items = relationship("OrderItem", lazy="selectin")  # preferred for collections
```

Django:
```python
# Don't configure the model — configure the query
# select_related: SQL JOIN for FK / one-to-one (eager for the query)
Order.objects.select_related("customer")
# prefetch_related: separate batch query for reverse FK and M2M (batch lazy)
Order.objects.prefetch_related("items")
```

EF Core (C#):
```csharp
// Enable lazy loading proxies globally (opt-in)
services.AddDbContext<AppContext>(o => o.UseLazyLoadingProxies());
// Or explicit load (Value Holder style):
context.Entry(order).Collection(o => o.Items).Load();
// Or eager with Include for hot paths:
context.Orders.Include(o => o.Items).Where(...);
```

TypeORM:
```typescript
@OneToMany(() => OrderItem, item => item.order, { lazy: true })
items: Promise<OrderItem[]>;  // caller awaits to trigger load
```

**Lazy Initialization (hand-rolled):**
```java
class Supplier {
    private List<Product> products;  // null = not yet loaded
    private boolean productsLoaded = false;

    public List<Product> getProducts() {
        if (!productsLoaded) {
            products = ProductMapper.findForSupplier(this.id);
            productsLoaded = true;
        }
        return products;
    }
}
```
Use `productsLoaded` flag (not null check) when null is a legitimate value.

**Value Holder (hand-rolled):**
```java
class Supplier {
    private ValueHolder<List<Product>> products;

    public Supplier(long id) {
        this.products = new ValueHolder<>(() -> ProductMapper.findForSupplier(id));
    }

    public List<Product> getProducts() { return products.getValue(); }
}
```

**Ghost (hand-rolled):** See `references/ghost-implementation-guide.md` for full implementation — requires instrumenting every field accessor in a domain supertype and using a Registry + Separated Interface to avoid domain-to-mapper dependency.

### Step 5 — Add batch loading to prevent ripple loading

WHY: A lazy collection still causes ripple loading if each element in a parent collection triggers its own individual sub-collection load. Batch loading converts N queries into ceil(N/batch_size) queries.

- **Hibernate:** `@BatchSize(size = 50)` on the collection. Hibernate issues one `WHERE id IN (...)` for up to 50 parents at a time.
- **SQLAlchemy:** `lazy='selectin'` on the relationship. SQLAlchemy issues one `SELECT ... WHERE parent_id IN (...)` for all loaded parents.
- **Django:** `prefetch_related('items')` on the QuerySet. Django issues one query per prefetched relation for the entire result set.
- **EF Core:** `.Include(o => o.Items)` on the query (adds a JOIN, not N separate SELECTs).
- **Rails:** `includes(:items)` or `preload(:items)` on the scope.

Batch size guidance: 50 is a safe default. Larger batches reduce round-trips but increase per-query data volume. Set based on average result set size.

### Step 6 — Fix the proxy identity trap with Identity Map

WHY: A Virtual Proxy is a different object than the real domain object it wraps. Two proxies for the same database row have different object references (`proxy1 != proxy2`). Code that tests identity (`==`, `is`, `===`) or uses proxied objects as hash keys will break silently.

Detection: search the codebase for:
- `if (a == b)` where `a` or `b` could be a lazy proxy
- Collections that use domain objects as keys or set members

Fix: ensure the ORM's Identity Map (first-level cache / session cache) is active and returns the same proxy instance for the same primary key within a session. For hand-rolled Virtual Proxy, the mapper's Identity Map must return the same proxy object on repeated finds.

For equality checks: override `equals()`/`__eq__()`/`Equals()` to compare by primary key, not by object reference. This is mandatory for any domain class that participates in sets or maps.

Ghost variant avoids this problem entirely: the ghost IS the domain object, so identity is preserved.

### Step 7 — Add eager-load overrides for hot paths

WHY: A good default lazy strategy still needs targeted eager overrides for known high-traffic queries. Without them, report queries and list views generate ripple loads even with batch loading.

For each hot path identified in Step 1:
- Add a dedicated query method that includes a fetch-join / Include / eager_load / select_related for that use case
- Keep the default fetch strategy lazy; override at the query site, not the mapping

Example: an order detail screen needs customer, items, and product names. The general Order association is lazy. The detail query overrides:
```java
// Hibernate JPQL fetch join — overrides lazy for this query only
em.createQuery("SELECT o FROM Order o JOIN FETCH o.items i JOIN FETCH i.product WHERE o.id = :id")
```

Document hot-path overrides: query location | associations eagerly fetched | reason.

### Step 8 — Write the implementation plan artifact

WHY: The plan persists decisions and gives the team a single document to review before applying changes.

Produce a Markdown document containing:
1. Association classification table (Step 1)
2. Ripple-loading sites found (Step 2)
3. Chosen variant + rationale (Step 3)
4. Code sketch or ORM config diff (Step 4)
5. Batch loading config (Step 5)
6. Identity Map integration notes and equality overrides (Step 6)
7. Hot-path eager-load overrides (Step 7)
8. Testing approach: query count assertions before/after

## Inputs

- Persistence layer source files (entity classes, mappers, repositories)
- ORM configuration files (Hibernate XML/annotations, SQLAlchemy models, EF fluent config)
- Query log excerpt or N+1 symptom description
- Data-source pattern in use (from `data-source-pattern-selector`)

## Outputs

**Primary artifact:** `lazy-load-implementation-plan.md` containing:
- Association classification table
- Ripple-loading audit (specific files and lines)
- Variant selection decision
- Code sketch or ORM config diff
- Batch loading configuration
- Identity Map / equality notes
- Hot-path eager-load overrides
- Query count testing approach

**Secondary:** inline code diffs for ORM annotation changes or hand-rolled getter implementations.

## Key Principles

**1. The collection is the lazy unit, not the elements.**
The ripple-loading anti-pattern arises when individual elements in a collection are each lazy. Loading the collection lazily (one batch query) is correct. Loading the collection eagerly but each element's sub-associations lazily is also acceptable if the sub-associations are genuinely optional. Never put a Lazy Load on each element of a collection that is iterated immediately.

**2. Lazy Load is only worth its complexity cost when the field requires an extra database round-trip.**
Do not apply Lazy Load to a field stored in the same row as the main object — there is no performance benefit, only added code complexity. The value of Lazy Load is strictly about deferring extra database calls. If the field is co-located in the same SELECT, eager-load it.

**3. ORM proxies need Identity Map backing or they break equality.**
The proxy identity trap is a silent correctness bug: two proxies for the same row compare unequal by reference. Always ensure the ORM session's Identity Map (first-level cache) returns the same proxy for the same key. Override equality to compare by primary key for all domain objects used in sets, maps, or equality comparisons.

**4. Different use cases may need different fetch strategies — use query-level overrides.**
A single ORM mapping cannot be simultaneously optimal for a list screen (lazy, batch-prefetched) and a detail screen (eager fetch-join). Configure lazy as the default, and add fetch-join overrides at the query site for high-traffic paths. Two mapper variants (one lazy, one eager) for the same entity is a legitimate design.

**5. Ghost preserves identity; Virtual Proxy does not.**
When identity semantics matter (domain objects used as set members, equality comparisons in business logic), Ghost is the correct variant: it IS the domain object. Virtual Proxy is a different object that impersonates the real one. For most ORM stacks the ORM manages identity via its session cache, making this a non-issue in practice — but the distinction matters for hand-rolled implementations.

**6. Ripple loading cripples applications at scale; batch loading prevents it.**
A collection of N parent objects, each with a lazy child collection, causes N+1 queries without batch loading. At N=1000, that is 1001 queries. Batch loading reduces this to ceil(N/batch_size)+1 queries. This is not a micro-optimization — it is the difference between a feature working and not working under load.

## Examples

### Scenario A: Java/Hibernate — Order with N+1 on OrderItems

**Trigger:** A report listing 200 orders calls `order.getItems()` inside a loop. Query log shows 201 SELECT statements (1 for orders, 200 for items).

**Process:**
1. Classify: `items` is a lazy candidate (not always needed), but this report needs it — mark as hot-path override.
2. Ripple loading confirmed: items association is `FetchType.LAZY` with no `@BatchSize`.
3. Fix 1 (default strategy): add `@BatchSize(size = 50)` — reduces 200 queries to 4.
4. Fix 2 (hot path): add a report-specific JPQL query with `JOIN FETCH o.items`.
5. Equality override: add `equals()`/`hashCode()` on Order comparing by `id`.

**Output:** Implementation plan with `@BatchSize` annotation diff, JPQL fetch-join query, and equality override for Order.

---

### Scenario B: Python/SQLAlchemy — User with posts relationship paginating

**Trigger:** A feed endpoint loads 50 User objects. Accessing `user.posts` inside a Jinja template causes 50 additional SELECT statements.

**Process:**
1. Classify: `posts` is a lazy candidate for profile screens; batch-loadable for feed.
2. Ripple loading confirmed: `relationship("Post", lazy="select")` — default per-access load.
3. Variant: SQLAlchemy ships Virtual Proxy equivalent; configure `lazy="selectin"`.
4. `lazy="selectin"` issues one `SELECT posts WHERE user_id IN (1,2,...,50)` for the entire page.
5. For profile screen (single user): no change needed — single load is fine.

**Output:** One-line model change (`lazy="select"` → `lazy="selectin"`), test showing query count drops from 51 to 2.

---

### Scenario C: Hand-rolled Java DAO — large blob field loaded on every access

**Trigger:** A `Document` entity has a `content` field (a large text blob). Every SELECT of any document loads the blob even when only the title and date are needed.

**Process:**
1. Classify: `content` is a lazy candidate (expensive, not needed for listings; needed for detail view).
2. No ripple loading (single field, not a collection).
3. Variant: Lazy Initialization in the hand-rolled Data Mapper.
   - `content` field starts null; a `contentLoaded` boolean flag tracks state.
   - `getContent()` checks the flag, issues a dedicated `SELECT content FROM documents WHERE id=?` if not loaded.
4. No proxy identity issue (the Document object itself is the real object; only the field is deferred).
5. Hot-path override: the document edit screen calls the mapper's `findWithContent(id)` which issues a JOIN or two-column SELECT upfront.

**Output:** Updated `Document.java` getter with lazy init pattern, updated `DocumentMapper.java` with `findWithContent()` method.

## References

- `references/ghost-implementation-guide.md` — Full Ghost variant implementation (domain supertype, load states, Registry + Separated Interface wiring, ghost list for collections)
- `references/lazy-load-variant-comparison.md` — Side-by-side comparison of all four variants on: calling-code transparency, identity preservation, ORM support, instrumentation requirements, null-value handling
- `references/orm-lazy-config-cheatsheet.md` — Per-ORM Lazy Load configuration: Hibernate, EF Core, SQLAlchemy, Django ORM, TypeORM, Rails ActiveRecord

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-unit-of-work-implementer`
- `clawhub install bookforge-data-access-anti-pattern-auditor`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
