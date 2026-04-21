# Layer Anti-Patterns

Common mis-pairings and architecture mistakes when selecting enterprise application patterns.

## Anti-Pattern 1: Premature Data Mapper

**Symptom:** Team chose Data Mapper (or a full ORM) for a simple CRUD system where the schema closely mirrors the object model.

**What goes wrong:** Data Mapper adds significant complexity — separate mapping classes, configuration, behavioral patterns (Unit of Work, Identity Map). For a simple system, Active Record is sufficient and dramatically simpler.

**Detection:** Domain classes map 1:1 to tables with no meaningful behavior beyond getters/setters. No complex inheritance, no rich associations, no domain logic that needs independence from the schema.

**Fix:** Downgrade to Active Record. Most ORM frameworks support an Active Record style (Hibernate with plain JPA entities behaves like Active Record when there's no complex mapping).

---

## Anti-Pattern 2: Transaction Script with embedded database logic

**Symptom:** Transaction Script methods contain inline SQL or ORM calls mixed with business logic.

**What goes wrong:** Testing becomes impossible (you must hit the database to test any logic). Duplication is hidden inside scripts rather than being centralized.

**Detection:** `service.java` contains `conn.prepareStatement(...)` or `em.createQuery(...)` alongside if-else business rules.

**Fix:** Extract all DB access into a Table Data Gateway or Row Data Gateway. The script calls the gateway, not the database directly.

---

## Anti-Pattern 3: Distributing by domain object class

**Symptom:** Architect puts each domain entity (Customer, Order, Product) in a separate process or service and calls between them for every business operation.

**What goes wrong:** Every business transaction becomes a cascade of slow remote calls. Performance collapses. This is the exact pattern Fowler describes as an "inverted hurricane" in Ch. 7.

**Detection:** Network calls between Customer service and Order service happen 10+ times per request. Latency is measured in hundreds of milliseconds for simple operations.

**Fix:** Consolidate into a single in-process domain layer. Extract service boundaries only where truly justified by deployment or team independence, not by entity type.

---

## Anti-Pattern 4: Active Record for a complex Domain Model

**Symptom:** Domain Model is genuinely rich (complex inheritance, many associations, behavior that varies by subtype) but Active Record is used as the persistence strategy.

**What goes wrong:** The domain model becomes tightly coupled to the schema. Any schema refactoring breaks domain logic. Adding business behavior requires database changes. The object model cannot be tested without hitting the database.

**Detection:** Domain entity classes are littered with `findBy*` and `save()` methods alongside complex business calculations. SQL migration triggers cascading class changes.

**Fix:** Introduce a Data Mapper layer (migrate to an ORM or extract mapping classes). The domain model then has no knowledge of persistence, enabling independent testing.

---

## Anti-Pattern 5: Fat controllers / scriptlet views

**Symptom:** Web controllers contain business logic and database queries. View templates contain conditional loops and calculations.

**What goes wrong:** Domain logic is trapped in the presentation layer. It cannot be reused by other presentation channels (API, batch). It cannot be tested without simulating HTTP requests. Changes to UI require touching business logic.

**Detection:** Controller methods are >50 lines. View templates contain SQL fragments or complex conditional blocks.

**Fix:** Extract domain logic to a Service Layer (thin application facade over the Domain Model). Controller calls Service Layer methods and passes simple DTOs to the view.

---

## Anti-Pattern 6: Missing Optimistic Offline Lock on multi-request edits

**Symptom:** User A and User B both retrieve the same record, edit it in separate HTTP sessions, and both save successfully — the last write silently wins.

**What goes wrong:** Lost updates. The earlier save's changes are overwritten without any error or notification to either user.

**Detection:** No version column, ETag, or timestamp on entities that are edited through multi-step forms. No concurrency conflict exception is ever raised during testing.

**Fix:** Add Optimistic Offline Lock — a version column on the entity, incremented on each save. Any save where the version doesn't match the read version raises a conflict error that the user can resolve.
