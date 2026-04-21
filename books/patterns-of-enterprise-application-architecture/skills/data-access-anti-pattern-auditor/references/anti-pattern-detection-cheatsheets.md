# Anti-Pattern Detection Cheatsheets

Reference for `data-access-anti-pattern-auditor`. Each section provides per-stack
grep/search patterns and evidence classification for one anti-pattern.

---

## AP-1: N+1 / Ripple Loading

### Grep signatures (any ORM)

```
# Loop + lazy access — generic
forEach|for\s+\w+\s+in\s+|\.each\s*\{|\.map\s*\{|\.stream\(\)

# Inside the loop — look for DB access
\.find\(|\.query\(|\.fetch\(|\.load\(|\.count\(|\.size\(|\.all\b|SELECT
```

### Rails / ActiveRecord
```ruby
# Bad — N+1 smell
orders.each { |o| o.line_items.count }  # one query per order

# Good — eager load
Order.includes(:line_items).each { |o| o.line_items.count }
```
Grep: `has_many\|belongs_to` combined with loop constructs that do not use `.includes` or `.eager_load`.

### Hibernate / JPA
```java
// Bad — N+1 smell
for (Order o : orders) { o.getLineItems().size(); }  // triggers proxy load each time

// Good
@Query("SELECT o FROM Order o JOIN FETCH o.lineItems")
```
Grep: `@OneToMany(fetch = FetchType.LAZY)` or `@ManyToOne(fetch = FetchType.LAZY)` — then
check if the relationship is accessed inside a loop without `JOIN FETCH` or `@BatchSize`.

### SQLAlchemy (Python)
```python
# Bad
for order in session.query(Order).all():
    print(order.line_items)   # lazy SELECT per order

# Good
from sqlalchemy.orm import joinedload
session.query(Order).options(joinedload(Order.line_items)).all()
```
Grep: `relationship(` without `lazy='joined'` or `lazy='subquery'` or `options(joinedload`.

### EF Core (C#)
```csharp
// Bad
foreach (var o in context.Orders.ToList())
    Console.WriteLine(o.LineItems.Count);  // lazy navigation

// Good
context.Orders.Include(o => o.LineItems).ToList()
```
Grep: `virtual ICollection` combined with loop that accesses the property without `.Include`.

### Evidence classification
- **Definite**: Loop body contains explicit `find`, `query`, or ORM lazy proxy access on
  a field that maps to a FK relationship, AND no eager-load option is present.
- **Probable**: Loop iterates collection of entities; inner body accesses navigation property.
- **Possible**: `lazy=True` or `FetchType.LAZY` in model definition — flag for review.

---

## AP-2: Ghost / Proxy Identity Trap

### Grep signatures
```
# Equality comparison on entity/domain objects
==\s*\w+Entity|equals\(.*entity|assertSame\(|assert.*==.*proxy

# Multiple sessions / detached entities
new Session\(|new DbContext\(|sessionFactory.openSession\(\)
# within the same request/transaction — signals multiple identity maps in one transaction
```

### Evidence classification
- **Definite**: Two `find(sameId)` calls in the same request that return different object
  references (checked via reference equality); OR detached entity used after session close.
- **Probable**: Multiple `Session`/`DbContext` instances opened in the same request scope.
- **Possible**: `equals()` / `__eq__` not overridden on entity classes (all proxy comparisons
  use reference equality by default).

### Diagnostic test (manual)
```python
a = session.query(Person).get(1)
b = session.query(Person).get(1)
assert a is b   # should pass with Identity Map; fails if bypassed
```

---

## AP-3: AR / Data Mapper Mismatch

### Signal A — AR on non-isomorphic schema

Grep for conversion methods inside AR classes:
```
to_domain\|from_record\|to_entity\|from_model\|toDomain\|fromRecord
```
Grep for domain inheritance inside AR classes:
```
class \w+ < ApplicationRecord.*\n.*STI|type_column|polymorphic
```
Schema divergence signals:
- Domain field names differ systematically from DB column names (snake_case domain ≠ DB abbrev).
- Value Objects referenced from AR (Money, Address, DateRange) mapped via `composed_of` / `@Embeddable`
  inside what is supposed to be a simple AR.

### Signal B — DM with no structural complexity

Grep for mapper classes that are pure field-copy:
```python
# SQLAlchemy mapper with no transform
mapper(Person, people_table, properties={'first_name': people_table.c.first_name, ...})
# every property is identity — no transformation
```
- Mapper class count equals table count with no complex mappings → likely over-engineered for CRUD app.

### Evidence classification
- **Definite**: AR class contains `to_domain` / `from_record` methods AND schema has
  inheritance or value objects.
- **Probable**: AR class has explicit column-name-to-field-name mappings that differ in structure
  (not just naming convention).
- **Possible**: AR class exceeds 200 lines with heavy methods — worth reviewing for DM candidate.

---

## AP-4: Serialized LOB Overuse

### Grep signatures
```sql
-- Querying inside LOB
WHERE config LIKE '%theme%'
WHERE prefs->>'setting' = 'value'
jsonb_extract_path_text(data, 'field') = 'value'
CAST(xml_col AS TEXT) LIKE '%<status>active%'
```

```
# Schema definition — suspicious column types
TEXT|BLOB|JSONB|CLOB|XML.*column
# AND referenced in WHERE/ORDER BY/JOIN
```

```python
# Deserialization inside a finder — LOB is being filtered after fetch
[x for x in session.query(Config).all() if json.loads(x.data)['theme'] == 'dark']
```

### Evidence classification
- **Definite**: LOB column appears in a WHERE clause (SQL filtering inside the LOB) or is
  deserialized in application code to filter before returning to caller.
- **Probable**: LOB column has a GIN index, indexed expression, or computed column — indicates
  pressure to query inside it.
- **Possible**: Column type is TEXT/BLOB/JSONB with more than ~3 application reads that each
  parse/deserialize the content.

### Versioning trap indicator
- Migration file modifies structure of content inside a LOB column (e.g., renames a JSON key,
  adds a required nested field) → schema-within-schema churn.

---

## AP-5: Meaningful Primary Key Leakage

### Grep signatures
```sql
-- PK is a business value
CREATE TABLE orders (order_number VARCHAR(20) PRIMARY KEY, ...)
CREATE TABLE employees (ssn CHAR(9) PRIMARY KEY, ...)
CREATE TABLE line_items (order_number VARCHAR(20), seq INT, PRIMARY KEY (order_number, seq))
```

```python
# Domain object exposes PK as stable business ID
def get_order_number(self):
    return self.id   # id IS the business key
```

```
# FK references to business-meaningful PK
REFERENCES orders(order_number)
REFERENCES employees(ssn)
```

### Evidence classification
- **Definite**: PK column name is `email`, `ssn`, `order_number`, `username`, `code`, `sku`,
  or a composite of business-meaningful components.
- **Probable**: PK is a VARCHAR or CHAR type (surrogate keys are almost always INT/BIGINT/UUID).
- **Possible**: Composite PK with more than one column — check if components carry business meaning.

---

## AP-6: Business Logic in Gateway

### Grep signatures
```python
# Gateway method names that suggest domain logic
class CustomerGateway:
    def apply_loyalty_discount(self, ...):  # business rule
    def calculate_tax(self, ...):           # business calculation
    def validate_credit_limit(self, ...):   # validation
```

```java
// TDG method beyond CRUD
public class OrderGateway {
    public BigDecimal computeTotal(long orderId) { ... }  // domain logic
    public boolean isEligibleForPromotion(long orderId) { ... }
}
```

### CRUD boundary definition
A Gateway's legal methods: `find*(...)`, `insert(...)`, `update(...)`, `delete(...)`,
`findBy*(...)`. Any method that does not fit these templates is a candidate for leakage.

### Evidence classification
- **Definite**: Gateway method contains conditional business rules, calculations, or validation
  that references business policy (discount %, tax rate, eligibility rule).
- **Probable**: Gateway method name is a verb other than find/insert/update/delete.
- **Possible**: Gateway method has more than ~10 lines of logic beyond SQL construction.

---

## Severity Ranking Reference

| Anti-Pattern | Severity | Primary Risk |
|---|---|---|
| Missing Identity Map / proxy identity trap | Critical | Data integrity: double-write, lost update |
| N+1 / Ripple Loading | High | Performance: O(N²) queries |
| AR / DM Mismatch | High | Correctness + maintainability |
| Serialized LOB overuse | Medium-High | Queryability + versioning |
| Meaningful key leakage | Medium | Stability: cascade updates, uniqueness collisions |
| Business logic in Gateway | Medium | Maintainability: test isolation, logic scatter |

---

## Remediation Cross-References

| Anti-Pattern | Primary BookForge Skill |
|---|---|
| N+1 / Ripple Loading | `lazy-load-strategy-implementer` |
| AR / DM Mismatch | `data-source-pattern-selector` |
| Serialized LOB | `object-relational-structural-mapping-guide` |
| Meaningful key | `object-relational-structural-mapping-guide` |
| Business logic in Gateway | `data-source-pattern-selector` |
| Missing Identity Map | `unit-of-work-implementer` (if built) |
