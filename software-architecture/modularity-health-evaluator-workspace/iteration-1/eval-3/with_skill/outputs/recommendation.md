# Modularity Health Report: Microservice Extraction Readiness Assessment

## Assessment Scope
- **Date:** 2026-03-27
- **Modules assessed:** 15 top-level packages in monolith
- **Assessment method:** Description-based framework analysis (actual codebase metrics would improve precision)
- **Objective:** Rank packages by extraction readiness using modularity metrics

## Assessment Framework

For each of the 15 packages, I need the following to produce a complete assessment. Since the user described 15 packages without naming them, I'll demonstrate the framework with representative package archetypes and show how to apply it to each package.

**To complete this assessment for your specific packages, provide for each:**
1. Package name and primary responsibility
2. Approximate number of classes
3. Which other packages import from it (Ca) and which it imports from (Ce)
4. Whether it defines interfaces/abstract classes
5. Whether it shares database tables with other packages

## Modularity Metrics Applied to Extraction Readiness

### Step 1: Measure Coupling for Each Package

For each package, count:
- **Ca (afferent):** How many of the other 14 packages import from this one?
- **Ce (efferent):** How many of the other 14 packages does this one import from?

| Package | Ca | Ce | I = Ce/(Ca+Ce) | Interpretation |
|---------|:--:|:--:|:--------------:|---------------|
| High Ca, Low Ce | 10 | 1 | 0.09 | Foundation package -- stable, many dependents |
| Low Ca, Low Ce | 1 | 2 | 0.67 | Isolated -- few connections in either direction |
| Low Ca, High Ce | 0 | 8 | 1.0 | Leaf package -- depends on many, nobody depends on it |
| High Ca, High Ce | 8 | 6 | 0.43 | Hub -- both depended on and dependent. Hardest to extract. |

**Extraction readiness by instability:**
- **I near 1.0 (unstable, leaf):** Best extraction candidates -- nobody depends on them, so extraction doesn't break other packages
- **I near 0.5:** Moderate candidates -- some impact on extraction
- **I near 0.0 (stable, foundation):** Worst extraction candidates -- many packages depend on them, extracting breaks everything

### Step 2: Evaluate Cohesion Type per Package

| Cohesion Type | Extraction Readiness | Why |
|-------------|:-------------------:|-----|
| Functional | **Excellent** | Package is self-contained around one function -- maps directly to a microservice boundary |
| Sequential | **Good** | Pipeline within the package -- may extract as one service or split into pipeline stages |
| Communicational | **Good** | Operates on shared data -- service owns its data naturally |
| Procedural | **Fair** | Order dependencies may cross service boundaries |
| Temporal | **Poor** | Time-based grouping doesn't map to service boundaries |
| Logical | **Poor** | Mixed responsibilities would create a service that does too many things |
| Coincidental | **Blocked** | No natural service boundary exists -- must refactor first |

### Step 3: Calculate Abstractness and Distance

| Package Profile | A | I | D | Zone | Extraction Impact |
|----------------|:--:|:--:|:--:|------|-------------------|
| Clean leaf service | 0.2 | 0.8 | 0.0 | Main Sequence | **Extract freely** |
| Well-designed core | 0.6 | 0.3 | 0.1 | Main Sequence | Extract with interface preservation |
| Utility foundation | 0.0 | 0.0 | 1.0 | Zone of Pain | **Do NOT extract** -- decompose first |
| Abandoned abstraction | 0.9 | 0.9 | 0.8 | Zone of Uselessness | Evaluate for deletion, not extraction |

### Step 4: Analyze Cross-Package Connascence

This is the critical step for extraction readiness. For each package pair, identify connascence type:

| Connascence Type | Extraction Impact | Resolution |
|-----------------|:-----------------:|-----------|
| CoN (Name) | Low | Service API replaces method names -- trivially handled |
| CoT (Type) | Low | Shared DTOs or API contracts replace shared types |
| CoM (Meaning) | Medium | Shared constants must be documented in API contracts |
| CoP (Position) | Medium | Named parameters in API eliminate position dependency |
| CoA (Algorithm) | **High** | Shared algorithms must be extracted into shared libraries or each service must maintain its own copy |
| CoE (Execution) | **High** | Execution order must be replaced with choreography or orchestration |
| CoV (Values) | **Critical** | Shared transactions must be replaced with saga pattern or eventual consistency |
| CoI (Identity) | **Critical** | Shared entity references require a consistent identity service or event-driven sync |

**Extraction blocker rule:** Any cross-package connascence of Values (CoV) or Identity (CoI) must be resolved BEFORE extraction. These indicate shared transactions or shared state that cannot survive a network boundary without explicit distributed data management.

### Step 5: Composite Extraction Readiness Score

For each package, compute a readiness score:

| Factor | Weight | Score Range | Scoring |
|--------|:------:|:----------:|---------|
| Instability (I) | 25% | 0-10 | I > 0.7 = 10, I 0.4-0.7 = 5, I < 0.4 = 2 |
| Cohesion Type | 25% | 0-10 | Functional = 10, Sequential/Comm = 7, Procedural = 4, Logical/Temporal = 2, Coincidental = 0 |
| Distance (D) | 20% | 0-10 | D < 0.2 = 10, D 0.2-0.5 = 6, D > 0.5 = 2 |
| Cross-boundary Connascence | 30% | 0-10 | No CoV/CoI = 10, CoA/CoE = 5, CoV = 2, CoI = 0 |

**Readiness Classification:**
- **Score 8-10: Ready** -- Extract with confidence
- **Score 5-7: Conditionally Ready** -- Extract after addressing specific concerns
- **Score 3-4: Not Ready** -- Requires refactoring within the monolith first
- **Score 0-2: Blocked** -- Fundamental restructuring needed before extraction is possible

## Example Assessment (Archetypal Packages)

### Package: OrderProcessing (Functional Cohesion, Leaf)
| Metric | Value | Notes |
|--------|-------|-------|
| Ca | 2 | Only UI and ReportingService call it |
| Ce | 4 | Uses CustomerData, ProductCatalog, PaymentGateway, InventoryService |
| I | 0.67 | Moderately unstable -- good for extraction |
| A | 0.3 | Has OrderService interface |
| D | 0.03 | On the main sequence |
| Cohesion | Functional | Single clear responsibility: process orders |
| Cross-boundary Connascence | CoN, CoT only | Clean API boundaries |
| **Readiness Score** | **8.5** | **Ready for extraction** |

### Package: SharedUtils (Coincidental Cohesion, Foundation)
| Metric | Value | Notes |
|--------|-------|-------|
| Ca | 14 | Every other package depends on it |
| Ce | 0 | Depends on nothing |
| I | 0.0 | Maximally stable |
| A | 0.02 | Almost no interfaces |
| D | 0.98 | Deep zone of pain |
| Cohesion | Coincidental | Random utility classes |
| Cross-boundary Connascence | CoA (algorithm coupling), CoM (magic values) | Dangerous coupling types |
| **Readiness Score** | **0.5** | **Blocked -- must decompose before extracting anything** |

### Package: PaymentGateway (Functional Cohesion, Hub)
| Metric | Value | Notes |
|--------|-------|-------|
| Ca | 5 | OrderProcessing, Subscriptions, Refunds, Invoicing, AdminPanel |
| Ce | 3 | ExternalPaymentAPI, CustomerData, AuditLog |
| I | 0.375 | Moderately stable -- some dependents |
| A | 0.5 | Has PaymentProcessor interface |
| D | 0.125 | Near main sequence |
| Cohesion | Functional | Single responsibility: payment processing |
| Cross-boundary Connascence | CoV with OrderProcessing (shared transaction) | **Blocker** |
| **Readiness Score** | **4.5** | **Conditionally Ready -- resolve CoV first** |

## Recommended Extraction Order

Based on the framework above:

### Phase 1: Extract High-Readiness Packages (Score 8-10)
These packages have functional cohesion, low Ca, no dangerous cross-boundary connascence. Extract them first to establish patterns, build deployment infrastructure, and gain confidence.

### Phase 2: Decompose Blockers
Address the SharedUtils package (and any similar foundation packages) by decomposing them into domain-specific packages. This is prerequisite work -- you're not extracting these as services, you're cleaning up the monolith so other extractions become possible.

### Phase 3: Resolve Cross-Boundary Connascence
For packages scored 5-7 (conditionally ready), resolve the specific connascence blockers:
- CoV (shared transactions) -> implement saga pattern or shared database with eventual splitting
- CoI (shared identity) -> implement domain events for identity sync
- CoA (shared algorithms) -> extract into shared library or duplicate with tests

### Phase 4: Extract Conditionally Ready Packages
Once blockers are resolved, extract the next tier of packages.

### Phase 5: Evaluate Remaining Packages
Packages that scored 0-4 may be better left in the monolith (as a "modular monolith") rather than forced into microservices. Not every module needs to be a separate service.

## Connascence-Based Extraction Blockers Summary

| From Package -> To Package | Connascence Type | Blocker? | Resolution Required Before Extraction |
|---------------------------|-----------------|:--------:|--------------------------------------|
| {Package A -> Package B} | CoV (Values) | **YES** | Implement saga pattern or event-driven consistency |
| {Package C -> Package D} | CoI (Identity) | **YES** | Implement identity service or domain events |
| {Package E -> SharedUtils} | CoA (Algorithm) | Partial | Extract shared algorithm into library or duplicate |
| {Package F -> Package G} | CoE (Execution) | Partial | Implement async communication or orchestrator |
| {All -> SharedUtils} | CoN/CoT (Name/Type) | No | Handled naturally by API contracts |

## Key Principles for Extraction Readiness

- **High instability (I near 1) = easiest to extract** -- leaf packages with few dependents cause the least disruption when extracted
- **Zone of Pain packages must NOT be extracted first** -- decompose them within the monolith before touching extraction
- **Connascence of Values is the hardest blocker** -- shared transactions between packages mean those packages cannot be separated by a network boundary without implementing distributed transaction patterns
- **Functional cohesion is the minimum for extraction** -- a package with logical or coincidental cohesion will become a "mini-monolith" microservice that gains none of the benefits of extraction
- **Distance from main sequence predicts extraction pain** -- D < 0.3 extracts cleanly, D > 0.5 needs refactoring first
