# Modularity Health Report: CustomerService Class

## Assessment Scope
- **Date:** 2026-03-27
- **Modules assessed:** 1 (with 4 identified sub-groups)
- **Assessment method:** Description-based analysis
- **Tools used:** Manual estimation from user-provided description

## Module Catalog

| Module | Responsibility | Methods | Fields | Ca (est.) | Ce (est.) |
|--------|---------------|:-------:|:------:|:---------:|:---------:|
| CustomerService | Registration + Billing + Notifications + Reporting | 35 | 12 | ~15 | ~8 |

**Responsibility statement test:** "CustomerService handles customer registration, billing operations, notification delivery, and reporting." -- Four distinct functions connected by "and" = strong indicator of poor cohesion.

## Cohesion Assessment

| Module | Cohesion Type | LCOM Estimate | Rating |
|--------|-------------|:-------------:|:------:|
| CustomerService | **Logical** (rank 6 of 7) | **High** | **Poor** |

### Cohesion Details

**CustomerService:** Classified as **logical cohesion** -- the methods are logically related (they all deal with "customers") but are functionally different. Registration, billing, notifications, and reporting are separate functions that happen to operate on the same entity.

**LCOM Analysis:**
The user reports 12 instance variables with most methods using only 2-3. This reveals clear field-method clusters:

| Responsibility Group | Est. Methods | Est. Fields Used | Shared Fields with Other Groups |
|---------------------|:-----------:|:----------------:|:------------------------------:|
| Registration | ~8 | Fields A, B, C | Minimal (customer name/ID only) |
| Billing | ~10 | Fields D, E, F, G | Minimal (customer ID only) |
| Notifications | ~7 | Fields H, I | Minimal (customer contact info) |
| Reporting | ~10 | Fields J, K, L | Minimal (aggregation fields) |

**LCOM interpretation:** With 4 disconnected field-method clusters, LCOM is high. Each cluster could exist as its own class. The few shared fields (customer ID, name) indicate these groups are connected by the entity they operate on, not by functional necessity -- this is the hallmark of logical cohesion.

**WHY this matters:** High LCOM means the class is structurally multiple classes forced into one file. Any change to billing fields or methods risks accidental interaction with notification or reporting code. Testing requires instantiating all 12 fields even when testing a single responsibility group.

## Coupling & Derived Metrics

| Module | Ca | Ce | Instability (I) | Abstractness (A) | Distance (D) | Zone |
|--------|:--:|:--:|:---------------:|:-----------------:|:-------------:|------|
| CustomerService | ~15 | ~8 | 0.35 | ~0.0 | **0.65** | **Zone of Pain** |

### Metric Calculations

- **Instability:** I = Ce / (Ca + Ce) = 8 / (15 + 8) = 0.35
  - Moderately stable -- many modules depend on CustomerService
- **Abstractness:** A ~ 0.0
  - The class is entirely concrete (no interfaces, no abstract methods)
- **Distance from Main Sequence:** D = |0.0 + 0.35 - 1| = 0.65
  - **Significantly off the main sequence** -- a D value of 0.65 indicates severe imbalance

## Zone Placement Map

```
Abstractness (A)
1.0 |  Zone of
    |  Uselessness        /
    |                   /
    |                 /
    |               /
0.5 |             /  <-- Main Sequence (ideal)
    |           /
    |         /
    |       /
    |     /
    |   /
0.0 | * CustomerService    ZONE OF PAIN
    +-------------------------> 1.0
              Instability (I)
    * = (I=0.35, A=0.0, D=0.65)
```

**Diagnosis:** CustomerService sits deep in the **Zone of Pain**. It is moderately stable (Ca=15, many dependents) but fully concrete (A=0, no interfaces). This means:
- 15 other modules couple directly to the concrete implementation
- Any internal change risks breaking those 15 dependents
- There is no interface to provide flexibility or enable substitution

## Connascence Analysis

| From -> To | Type | Strength | Across Boundary? | Concern Level |
|-----------|------|----------|:----------------:|:-------------:|
| Callers -> CustomerService (registration) | CoN (Name) | Weak | Yes | Low |
| Callers -> CustomerService (billing) | CoN (Name) | Weak | Yes | Low |
| CustomerService -> Database | CoT (Type) | Weak | Yes | Low |
| CustomerService -> EmailService | CoE (Execution) | Strong | Yes | **High** |
| Billing methods -> external payment API | CoA (Algorithm) | Moderate | Yes | **Medium** |
| Reporting -> Billing (shared state) | CoV (Values) | Strong | Within class | **Medium** (would become High if split) |

**Key finding:** The reporting methods likely share billing state (CoV -- connascence of values). If these methods are extracted into separate services without addressing this, the connascence becomes cross-boundary CoV, which is much more dangerous. This must be resolved before splitting.

## Health Summary

| Module | Health | Primary Concern | Recommended Action |
|--------|:------:|-----------------|-------------------|
| CustomerService | **Unhealthy** | Logical cohesion + Zone of Pain (D=0.65) | Extract into 4 focused services with interfaces |

## Prioritized Refactoring Recommendations

### 1. Extract NotificationService (Lowest risk, immediate win)
**Action:** Extract `notifyCustomer()`, `sendEmail()`, `formatNotification()` and related methods + fields H, I into a `NotificationService` class.
**WHY:** Notification methods have the weakest connascence to other groups (CoN only). They share the fewest fields with other responsibility groups. This is the cleanest extraction boundary.
**Expected improvement:**
- CustomerService LCOM drops (one disconnected cluster removed)
- NotificationService achieves functional cohesion (rank 1)
- CustomerService Ca decreases as notification callers migrate

### 2. Extract CustomerRegistrationService (Clean boundary)
**Action:** Extract registration methods + fields A, B, C into `CustomerRegistrationService`. Introduce a `CustomerRegistration` interface.
**WHY:** Registration methods form a self-contained cluster with few dependencies on other groups. The interface increases A for the registration component, moving it toward the main sequence.
**Expected improvement:**
- New service: I ~ 0.7, A ~ 0.5, D ~ 0.2 (on main sequence)
- CustomerService D improves as Ca decreases

### 3. Resolve Billing-Reporting shared state BEFORE extracting either
**Action:** Identify the shared fields between billing and reporting methods. Create a `BillingData` value object or read model that both can consume independently.
**WHY:** Currently billing and reporting have connascence of values (CoV) within the class. Splitting them without resolving this creates cross-boundary CoV, which is architecturally dangerous -- any billing data change requires coordinated reporting changes. By introducing a shared value object, we downgrade CoV to CoT (connascence of type), a much weaker form.
**Expected improvement:**
- Billing and reporting can then be extracted independently
- Cross-boundary connascence reduced from CoV to CoT

### 4. Extract BillingService and ReportingService (after step 3)
**Action:** Once shared state is resolved, extract billing (fields D, E, F, G) and reporting (fields J, K, L) into separate services.
**Expected improvement:**
- Final CustomerService may be eliminated entirely or reduced to a thin facade
- Each new service achieves functional cohesion
- All new services have D < 0.3 (near main sequence)

## Final Metrics Projection (Post-Refactoring)

| Module | I (est.) | A (est.) | D (est.) | Zone |
|--------|:--------:|:--------:|:--------:|------|
| NotificationService | 0.8 | 0.0 | 0.2 | Main Sequence |
| CustomerRegistrationService | 0.6 | 0.5 | 0.1 | Main Sequence |
| BillingService | 0.5 | 0.3 | 0.2 | Main Sequence |
| ReportingService | 0.9 | 0.1 | 0.0 | Main Sequence |
