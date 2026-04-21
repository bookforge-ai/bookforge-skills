# Base Patterns Cheatsheet

All 11 patterns from Chapter 18 of *Patterns of Enterprise Application Architecture* (Fowler et al., 2002).

---

## Quick-Lookup Table

| Pattern | One-line intent | When to apply | Modern equivalent |
|---------|----------------|---------------|-------------------|
| **Gateway** | Wrap an external system/resource with a clean OO interface | Any external resource access (API, DB, messaging, XML) | HTTP client wrappers, DAO adapters, adapter classes |
| **Mapper** | Decouple two subsystems by having a third object move data between them | When neither subsystem may know about the other AND the interaction is complex | Data Mapper (DB), AutoMapper, anti-corruption layer |
| **Layer Supertype** | Shared base class for all objects in a layer | Many classes in one layer share behavior (ID, timestamps, change-tracking) | Spring `JpaRepository`, Django `Model`, Rails `ApplicationRecord` |
| **Separated Interface** | Interface lives in a different package from its implementation | Breaking dependency cycles between layers or modules | Repository interface in domain, impl in infrastructure |
| **Registry** | Global finder/locator for widely needed objects or services | Last resort — when dependency injection doesn't fit the call tree | Service Locator (prefer DI container instead) |
| **Value Object** | Small immutable object whose equality is based on field values, not reference | Any domain concept where value-identity makes sense (money, date, address) | Java records, C# structs/records, Kotlin data class |
| **Money** | Value Object for monetary amounts with safe arithmetic | Any monetary calculation | Joda-Money, BigDecimal + Currency, Dinero.js |
| **Special Case** | Subclass that provides harmless default behavior for a particular case | Repeated null checks / special-value checks in multiple places with same behavior | Null Object pattern, Result/Option types |
| **Plugin** | Runtime-selected implementation bound via external configuration | Different implementations per deployment environment | DI container `@Profile`, twelve-factor env config |
| **Service Stub** | In-memory test double for an external service | External service is slow, unreliable, or unavailable during tests | Mockito/Moq mocks, WireMock, in-memory fakes |
| **Record Set** | Generic in-memory tabular structure identical to a SQL result set | Platform provides data-aware UI tools that consume Record Sets | ADO.NET DataSet, JDBC ResultSet, Pandas DataFrame |

---

## Gateway

**Intent:** An object that encapsulates access to an external system or resource.

**Problem it solves:** External systems have awkward APIs (JDBC/SQL for databases, W3C/JDOM for XML, proprietary SDKs for messaging). This awkwardness spreads through your codebase if not contained.

**How it works:**
1. Identify what your application needs to do with the external resource (just your use cases, not all capabilities).
2. Create a clean interface with application-friendly method signatures.
3. Implement the Gateway to translate those calls to the external API.
4. Keep the Gateway minimal — complex logic belongs in its clients.
5. Design the interface to be replaceable with a Service Stub for testing.

**Key distinction from similar patterns:**
- **vs Facade (GoF):** Facade is written by the service author for general use. Gateway is written by the client for its own specific use.
- **vs Adapter (GoF):** Adapter converts an existing interface to another existing interface. Gateway usually creates a new interface where none existed.
- **vs Table Data Gateway:** Table Data Gateway is a specific data-access pattern that returns Record Sets. Generic Gateway is the broader pattern. Table Data Gateway IS a Gateway, but not all Gateways are Table Data Gateways.
- **vs Mapper:** Use Gateway (simpler) unless neither subsystem may be aware of the other interaction.

**Implementation sketch (TypeScript):**
```typescript
// Without Gateway — awkward SDK everywhere
const result = await messagingSDK.send("CNFRM", [orderId, amount, symbol]);
if (result !== 0) throw new Error(`Messaging error: ${result}`);

// With Gateway — application-friendly interface
interface OrderNotificationGateway {
  sendConfirmation(orderId: string, amount: number, symbol: string): Promise<void>;
}

class MessagingServiceGateway implements OrderNotificationGateway {
  async sendConfirmation(orderId: string, amount: number, symbol: string): Promise<void> {
    const result = await messagingSDK.send("CNFRM", [orderId, amount, symbol]);
    if (result !== 0) throw new Error(`Messaging error code: ${result}`);
  }
}

// Test stub — same interface, in-memory
class StubOrderNotificationGateway implements OrderNotificationGateway {
  public sentConfirmations: string[] = [];
  async sendConfirmation(orderId: string): Promise<void> {
    this.sentConfirmations.push(orderId);
  }
}
```

---

## Mapper

**Intent:** An object that sets up communication between two independent objects without either knowing about the mapper.

**Problem it solves:** Two subsystems need to exchange data, but architectural rules prohibit either from depending on the other (or on the mapping mechanism).

**Key rule:** Use Mapper only when you CANNOT allow either subsystem to have a dependency on the interaction. Otherwise, use Gateway (simpler, far more common).

**Most common enterprise use:** Data Mapper (database ↔ domain layer) where the domain model must not depend on persistence infrastructure.

**Modern parallels:** AutoMapper / MapStruct (automated field-to-field mapping), anti-corruption layer (DDD), request/response translators in event-driven systems.

---

## Layer Supertype

**Intent:** A base class for all objects in a layer that contains common layer-level behavior.

**Typical contents per layer:**
- **Domain layer:** ID field + getter/setter, `markDirty()` / `markNew()` / `markDeleted()` for Unit of Work integration, audit timestamps.
- **Data Mapper layer:** Common CRUD SQL helpers, type converters, connection accessors.
- **Web controller layer:** `currentUser()`, response helpers, error rendering.

**Multiple Layer Supertypes:** If a layer has distinct kinds of objects (e.g., Entities and Services), create a separate Layer Supertype for each kind.

**Implementation note:** Fowler's Java example has a `DomainObject` with an ID Long field and getter/setter. Every domain entity extends it, and every Data Mapper can then assume `DomainObject` has an ID.

---

## Separated Interface

**Intent:** Defines an interface in a package separate from its implementation.

**Problem it solves:** Package A depends on Package B, but B needs to call something in A — creating a cycle. Or: domain code should not depend on persistence infrastructure, but the domain needs to query for objects.

**Package placement options:**
1. **Interface in client package** — appropriate when one client defines the contract and the implementation team implements it.
2. **Interface in third package** — appropriate when multiple clients use the same interface, or when the interface team is separate from both client and implementation.

**Fowler's warning:** Do NOT use Separated Interface for every class. It adds factory boilerplate (factories also need Separated Interfaces and implementations). Only use it to break a specific dependency or to support multiple independent implementations.

**Modern parallels:**
```
// DDD example: Repository interface in domain, implementation in infrastructure
package com.myapp.domain.customer;       // <-- interface lives HERE
public interface CustomerRepository {
    Optional<Customer> findById(CustomerId id);
    void save(Customer customer);
}

package com.myapp.infrastructure.persistence;  // <-- implementation lives HERE
@Repository
public class JpaCustomerRepository implements CustomerRepository { ... }
```

---

## Registry

**Intent:** A well-known global finder for objects/services that other objects need but can't navigate to via normal object associations.

**Implementation options by scope:**
- **Process-scoped:** Singleton with static methods. Use for immutable/rarely-changed lookup data (country lists, currency tables).
- **Thread-scoped:** ThreadLocal variable. Use for request-scoped data (database connection, current user session).
- **Session-scoped:** Map keyed by session ID stored in thread-local. Use for multi-request session data.

**Critical warning from Fowler:** "Any global data is always guilty until proven innocent." Try passing dependencies explicitly first. Registry is a last resort.

**Registry vs DI Container (modern view):**
- Registry is pull-style: `Registry.getCustomerFinder()` — the caller fetches its dependency.
- DI Container is push-style: dependencies are injected into the constructor at wiring time.
- DI is now the standard recommendation because it makes dependencies explicit and testable. Use Registry only when DI isn't practical (e.g., deeply nested utility code that cannot be wired via constructor).

**Testing note:** Subclass Registry for tests (`RegistryStub`) to swap in Service Stubs. Reset between tests.

---

## Value Object

**Intent:** A small object whose equality is defined by its field values, not its object reference.

**Characteristics:**
- Equality by field values (`equals()` compares fields, not references).
- Immutable — changing a Value Object means creating a new instance.
- Typically small (date, money, address, range, color, measurement).

**Why immutability is critical — the aliasing bug:**
```java
// WRONG: mutable Value Object
Date hireDate = new Date(2024, 3, 18);
employee1.setHireDate(hireDate);
employee2.setHireDate(hireDate);  // both share same object
hireDate.setMonth(5);              // accidentally mutates BOTH employees' hire date
```
With an immutable Value Object, `setMonth()` doesn't exist — you create a new Date.

**Persistence:** Use Embedded Value (store fields inline in owner's row). Avoid persisting as a separate table with its own primary key — that treats a Value Object like an Entity.

**Modern language support:**
- Java: `record` (immutable by default, equals/hashCode auto-generated)
- C#: `struct` or `record struct` (value semantics built-in)
- Kotlin: `data class` (equals/hashCode auto-generated; mark `val` for immutability)
- Python: `@dataclass(frozen=True)` or `NamedTuple`
- TypeScript: `readonly` interface members + constructor
- Swift: `struct` (value semantics)

**Name collision:** J2EE community incorrectly used "Value Object" to mean Data Transfer Object. These are different: a Value Object is a domain concept with value-based equality; a DTO is an anemic data carrier for crossing process boundaries.

---

## Money

**Intent:** A Value Object representing a monetary amount, with correct currency-aware arithmetic.

**The float trap:**
```java
double val = 0.00;
for (int i = 0; i < 10; i++) val += 0.10;
System.out.println(val == 1.00);  // prints FALSE — IEEE 754 rounding
```
Always use integer cents (`long`) or fixed-point (`BigDecimal`). Never `double` or `float`.

**Core fields:**
```java
class Money {
    private final long amount;      // in smallest currency unit (cents)
    private final Currency currency;
}
```

**Arithmetic rules:**
- Addition/subtraction: assert same currency first. Throw if currencies differ (or use a "money bag" for multi-currency sums).
- Multiplication by scalar: use BigDecimal with explicit rounding mode. Force the caller to specify rounding for division/percentage operations.
- Allocation: do NOT use simple rounding. Use the ratio-allocation algorithm.

**Foemmel's Conundrum — the allocation algorithm:**
Problem: Allocate $0.05 between 70% and 30%. Naïve rounding: 3.5¢ → 4¢ + 1.5¢ → 2¢ = 6¢ (gained a penny).

Solution — allocate-by-ratio: compute each share by integer math, then distribute remaining cents one-by-one:
```java
public Money[] allocate(long[] ratios) {
    long total = Arrays.stream(ratios).sum();
    long remainder = amount;
    Money[] results = new Money[ratios.length];
    for (int i = 0; i < results.length; i++) {
        results[i] = newMoney(amount * ratios[i] / total);
        remainder -= results[i].amount;
    }
    // Distribute remaining cents one-by-one (pseudo-random but lossless)
    for (int i = 0; i < remainder; i++) results[i].amount++;
    return results;
}
// allocate([7,3]) on $0.05 → [$0.03, $0.02] ✓
```

**Persistence:** Embedded Value — two columns: `amount_cents BIGINT`, `currency_code CHAR(3)`. If all entries for an entity share the same currency, store currency once on the entity and derive it during mapping.

---

## Special Case

**Intent:** Replace repeated null-checks (or special-value-checks) with a subclass that provides valid, harmless default behavior.

**Before (null checks spread everywhere):**
```python
customer = find_customer(id)
if customer is None:
    name = "Unknown"
    balance = 0
    last_bill = None
else:
    name = customer.name
    balance = customer.balance
    last_bill = customer.last_bill
```

**After (Special Case):**
```python
class NullCustomer(Customer):
    @property
    def name(self): return "Unknown"
    @property
    def balance(self): return Decimal("0")
    @property
    def last_bill(self): return NullBill()   # chains to another Special Case

def find_customer(id) -> Customer:
    customer = db.find(id)
    return customer if customer else NullCustomer()

# All call sites become clean — no null checks needed
name = find_customer(id).name
balance = find_customer(id).balance
```

**When Special Cases chain:** `nullEmployee.contract` returns `NullContract` (not None). This propagates polymorphism all the way through the domain model.

**Multiple Special Cases:** Consider separate Special Cases for distinct states — `MissingCustomer` vs `UnknownCustomer` vs `OccupantCustomer` when they have different behaviors.

**Flyweight note:** Usually only one instance of each Special Case needed — implement as singleton unless the Special Case has unique state (e.g., each occupant customer is separate).

**Modern alternatives:**
- `Optional<T>` / `Option<T>` / `Maybe<T>` — makes nullability explicit in the type system but doesn't eliminate branching.
- Result types — for operations that can fail (different use case).
- Special Case is still the cleanest solution when the "no-result" behavior is well-defined and domain-meaningful.

---

## Plugin

**Intent:** Bind interface implementations at configuration time, not compile time. Centralize all environment-specific wiring in one place.

**Problem it solves:** Scattered `if (testMode) { return new TestImpl(); } else { return new ProdImpl(); }` factory methods that require code changes and rebuilds to switch environments.

**How it works:**
1. Define behavior with Separated Interface.
2. Write a PluginFactory that reads a config file mapping interface names → implementation class names.
3. Use reflection (if available) to instantiate the implementation class.
4. Each deployment has its own config file (`test.properties`, `prod.properties`).

```properties
# test.properties
com.myapp.TaxService=com.myapp.stubs.FlatRateTaxService
com.myapp.IdGenerator=com.myapp.stubs.CounterIdGenerator

# prod.properties
com.myapp.TaxService=com.myapp.services.RealTaxService
com.myapp.IdGenerator=com.myapp.db.OracleSequenceIdGenerator
```

**Modern equivalent:** This is exactly what DI container `@Profile` / `@ConditionalOnProperty` does in Spring, or `IServiceCollection` configuration in .NET. The core insight — centralize environment-specific wiring — remains fundamental.

---

## Service Stub

**Intent:** A simple, fast, in-memory test double for an external service that is slow, unreliable, or unavailable during testing.

**The triad (Gateway + Plugin + Service Stub):**
```
Gateway (Separated Interface) → Plugin (factory, reads config) → Real impl (production)
                                                               → Service Stub (test)
```

**Key rule — keep stubs simple:**
- Flat rate stub: 3-5 lines. Returns the same result for all inputs.
- Conditional stub: 10-15 lines. Handles a few well-known test cases.
- Dynamic stub: 20-30 lines. Allows test setup (add exemptions, configure responses).
- If your stub is getting complex, reconsider whether you're testing the right thing.

**Test setup methods that aren't on the real interface:** Add them to the stub, but make the production Gateway implementation throw assertion failures for these methods. This prevents test-only methods from leaking into production.

**Modern landscape:**
- **Mockito (Java) / Moq (.NET) / Jest mocks (JS):** Dynamic mocks with verification semantics. More powerful but also more complex.
- **WireMock / MockServer:** HTTP-level service stubs for integration testing.
- **Testcontainers:** Runs the real service in a container — heavier, more accurate.
- **Pact / contract testing:** Stubs derived from consumer contracts.
- Service Stub is the in-process, simplest option — Fowler's recommended starting point.

---

## Record Set

**Intent:** An in-memory structure that looks and behaves like a SQL query result, enabling data-aware UI tools to work with data generated by domain logic.

**Two essential properties:**
1. Identical interface to a database query result — data-aware UI widgets bind to it seamlessly.
2. Can be built and manipulated by domain logic (not just by querying the database).

**Implicit vs Explicit interface:**
- Implicit: `aReservation["passenger"]` — flexible but error-prone, no type safety, no discoverability.
- Explicit (preferred): `aReservation.Passenger` — typed, discoverable, refactorable.
- ADO.NET strongly-typed DataSets are the gold standard example of explicit Record Sets.

**When it matters:** Only valuable when your platform provides data-aware UI tools that consume Record Sets (ADO.NET Windows Forms, legacy .NET controls). In modern React/Vue SPAs or REST APIs, the pattern is largely obsolete for UI binding — use domain objects and DTOs instead.

**Modern context:** In data science and analytics, Pandas DataFrames and R data.frames are essentially Record Sets. In web backends, the pattern's role is carried by ORM result sets, which are typically mapped immediately to typed domain objects.
