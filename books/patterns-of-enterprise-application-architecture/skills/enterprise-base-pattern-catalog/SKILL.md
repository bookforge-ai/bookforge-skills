---
name: enterprise-base-pattern-catalog
description: "Reference catalog for Fowler's 11 enterprise base patterns from Chapter 18 of PEAA. Use when another skill or user says 'we need a Gateway here', 'this should be a Value Object', 'replace nulls with a Special Case', 'use a Service Stub for testing', or 'separate this interface from its implementation'. Covers all 11 base patterns: Gateway pattern (wrapping external systems), Mapper pattern (decoupling subsystems), Layer Supertype (shared base class per layer), Separated Interface (dependency inversion packaging), Registry (service locator), Value Object (value-identity immutable objects), Money pattern (monetary arithmetic, no floats, allocate-by-ratio), Special Case / Null Object (replace null checks), Plugin pattern (runtime-bound implementation), Service Stub (test double for external services), Record Set (generic tabular data structure). Identifies which pattern fits a described problem, provides canonical definition and modern language parallels, distinguishes Gateway (generic external-access wrapper) from Table Data Gateway (data-access pattern), flags Registry vs DI container tradeoff, and produces a short design note with implementation sketch. Also routes to the appropriate family selector when the problem is not a base pattern."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/enterprise-base-pattern-catalog
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors: ["Martin Fowler", "David Rice", "Matthew Foemmel", "Edward Hieatt", "Robert Mee", "Randy Stafford"]
    chapters: [18]
domain: software-architecture
tags:
  - base-patterns
  - design-patterns
  - software-design
  - software-architecture
  - enterprise-patterns
  - value-object
  - gateway-pattern
  - null-object
  - dependency-inversion
  - service-stub
  - testing-patterns
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: text
      description: "A pattern name ('what is Special Case?'), a problem description ('I have null checks everywhere for missing customers'), or a cross-skill invocation ('we need a Gateway for the FedEx API here')"
    - type: codebase
      description: "Optional — the relevant file or snippet helps produce a language-specific implementation sketch"
  tools-required:
    - Read
    - Grep
  tools-optional:
    - Glob
  mcps-required: []
  environment: "Works offline and without a codebase. A codebase helps tailor the implementation sketch to the team's language and conventions."
discovery:
  goal: "Identify the correct PEAA base pattern for a described problem and produce a concise design note with definition, rationale, and implementation sketch"
  tasks:
    - "Match user description or pattern name to one of the 11 base patterns"
    - "Return canonical definition, why it exists, when to apply, and modern language parallel"
    - "Produce a design note with implementation sketch in the user's language"
    - "Distinguish adjacent patterns (Gateway vs Table Data Gateway, Value Object vs DTO, Special Case vs Null Object vs Optional)"
    - "Route to the appropriate PEAA family selector when the problem is not a base pattern"
  audience:
    roles:
      - software-architect
      - senior-backend-engineer
      - tech-lead
      - framework-designer
    experience: intermediate
  when_to_use:
    triggers:
      - "Another PEAA skill says 'introduce a Gateway', 'this is a Value Object', 'use a Service Stub', 'apply Separated Interface here'"
      - "User asks what a named base pattern is or when to use it"
      - "User describes a problem that a base pattern solves: external API wrapping, scattered null checks, monetary arithmetic bugs, test isolation from external services, runtime implementation switching"
      - "User wants to know the modern equivalent of a PEAA base pattern"
      - "Code review identifies a missing base pattern (floats for money, null checks scattered, no Gateway around external API)"
    prerequisites: []
    not_for:
      - "Choosing between data-source architectural patterns (Transaction Script, Data Mapper, Active Record) — use data-source-pattern-selector"
      - "Choosing domain logic patterns — use domain-logic-pattern-selector"
      - "Implementing Unit of Work, Lazy Load, or concurrency patterns — use the dedicated implementer skills"
      - "Full implementation walkthroughs — this skill provides sketches and references, not complete code"
  environment:
    codebase_required: false
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: null
    assertion_count: 13
    iterations_needed: null
---

# Enterprise Base Pattern Catalog

The 11 base patterns in Chapter 18 of *Patterns of Enterprise Application Architecture* are cross-cutting utility patterns that appear everywhere in enterprise application design. They are not architectural patterns (like Data Mapper or Front Controller) — they are the building blocks those patterns are built from. Every other PEAA skill references at least one of these.

This skill is a lookup-and-guide: identify the pattern by name or by problem description, then get the canonical definition, when to apply it, a modern language sketch, and any critical cautions.

---

## When to Use

Use this skill when:

- Another PEAA skill says "introduce a Gateway here" or "this is a Value Object" and you need the definition.
- You're describing a cross-cutting utility problem: wrapping an external API, replacing null checks, making monetary arithmetic correct, isolating tests from external services, or breaking a package dependency cycle.
- You want to name a pattern you already know exists but can't recall precisely.
- You want the modern equivalent of a 2002-era base pattern.

NOT for: choosing among data-source patterns, domain logic patterns, web presentation patterns, concurrency patterns, or session state patterns. For those, see the dedicated selector skills in this set.

---

## Context and Input Gathering

**Accept either:**
1. A pattern name: "What is Registry?", "Explain Special Case", "When do I use Separated Interface?"
2. A problem description: "I have floats for monetary amounts", "null checks for missing customers everywhere", "I want to swap a real tax service with a stub in tests"
3. A cross-skill invocation: "We need a Gateway for the Stripe API — what does that look like?"

**If a codebase is available**, read the relevant file to produce a language-specific sketch. If not, use a stack-agnostic pseudocode sketch.

**Sufficiency check:** The pattern name or problem description alone is sufficient to proceed. No codebase required.

---

## Process

### Step 1 — Identify the Pattern

Match the input against the quick-lookup table. Accept either exact name or problem-description.

WHY: The 11 base patterns have overlapping surface descriptions (Gateway, Mapper, and Adapter all "wrap" something). Disambiguation prevents recommending the wrong pattern.

**If a pattern name is given:** look it up directly.

**If a problem description is given:** match against these trigger signatures:

| Problem signature | Pattern |
|---|---|
| "Wrap a 3rd-party / external API / resource behind a clean interface" | **Gateway** |
| "Decouple two subsystems so neither knows about the other" | **Mapper** |
| "Many classes in the same layer share common behavior" | **Layer Supertype** |
| "Break a dependency cycle between packages / layers" | **Separated Interface** |
| "Global finder / locator for widely-needed objects" | **Registry** |
| "Equality should be based on value, not reference; small immutable object" | **Value Object** |
| "Monetary amounts — avoid rounding errors, multi-currency, allocation" | **Money** |
| "Null checks for the same condition scattered in many places" | **Special Case** |
| "Swap implementation at configuration time (test vs production)" | **Plugin** |
| "External service is unavailable / slow — need to test without it" | **Service Stub** |
| "Generic tabular in-memory data structure for data-aware UI tools" | **Record Set** |

**If multiple patterns could apply:** list them with selection criteria (see Gateway vs Mapper below).

**If no base pattern fits:** route to the appropriate selector. Examples:
- Data access architecture question → `data-source-pattern-selector`
- Domain logic organization → `domain-logic-pattern-selector`
- Web layer structure → `web-presentation-pattern-selector`
- Concurrency → `offline-concurrency-strategy-selector`

WHY: Routing prevents this skill from giving partial answers on topics covered better by other skills in the set.

---

### Step 2 — Deliver the Pattern Response

For the identified pattern, produce:

1. **One-sentence definition** (the PEAA intent statement).
2. **Why it exists** — the problem without the pattern.
3. **When to apply** — specific conditions and contra-indicators.
4. **Critical cautions** — the most common mis-application.
5. **Modern language parallel** — what this looks like in the user's stack today.
6. **Implementation sketch** — 10-20 lines in the user's language (or pseudocode if language is unknown).

WHY: Each component serves a different reader. The definition serves recall; the "why it exists" serves understanding; the cautions prevent misuse; the modern parallel prevents dismissing the pattern as obsolete.

**Always include these cautions by pattern:**
- **Gateway:** Distinguish from Table Data Gateway. Not the same thing.
- **Mapper:** Use only when BOTH subsystems must be unaware. Otherwise use Gateway (much simpler).
- **Separated Interface:** Fowler explicitly warns against applying to every class. Only use to break a specific dependency or support multiple independent implementations.
- **Registry:** Global data. Guilty until proven innocent. Prefer DI container in modern systems.
- **Value Object:** Must be immutable. Aliasing bugs from mutable Value Objects are subtle.
- **Money:** Never use floats. Use the allocate-by-ratio algorithm for splitting sums — simple rounding loses or gains pennies.
- **Special Case:** `Optional<T>` is not equivalent — it makes nullability explicit but doesn't eliminate branching at every call site.
- **Service Stub:** Keep stubs simple. Complexity defeats the purpose.

---

### Step 3 — Produce the Design Note Artifact

Output a short design note (a markdown block) suitable for pasting into a code review comment, ADR, or design doc:

```markdown
## Pattern: [Pattern Name]

**Applied to:** [the specific component in the user's system]

**Why this pattern:** [one sentence connecting the problem to the pattern's intent]

**Implementation shape:**
[10-20 line code sketch in the user's language]

**Cautions:**
- [most relevant caution for this usage]
```

WHY: A concrete artifact makes the guidance actionable. Without a sketch, the recommendation remains abstract. The cautions prevent the most common misapplication of the pattern in this specific context.

---

### Step 4 — Surface Adjacent Patterns (Optional)

If another base pattern complements or must be used alongside the primary recommendation:

- Gateway → mention Service Stub and Plugin (the testing triad).
- Plugin → mention Separated Interface (Plugin requires it).
- Service Stub → mention Gateway (stub replaces a Gateway, not raw code).
- Separated Interface → mention Plugin (for runtime wiring).
- Value Object → mention Money (if the value object involves monetary amounts).

WHY: The base patterns form a triad (Gateway + Plugin + Service Stub) and a pair (Value Object + Money). Mentioning them together prevents the user from applying one pattern while missing the pattern it depends on.

---

## Inputs

- Pattern name or problem description (required)
- Language/stack (optional — used to tailor the implementation sketch)
- Relevant code file or snippet (optional — used to make the design note concrete)

---

## Outputs

1. **Pattern identification** — which of the 11 base patterns matches
2. **Definition and rationale** — intent, why it exists, when to apply
3. **Critical cautions** — most important mis-application to avoid
4. **Modern parallel** — how the pattern appears in the user's language/framework today
5. **Design note artifact** — markdown block with implementation sketch and cautions

---

## Key Principles

**1. Gateway and Table Data Gateway are not the same.**
Table Data Gateway (Chapter 10) is a specific data-access pattern that accesses one database table and returns Record Sets. The generic Gateway (Chapter 18) is a broader pattern for wrapping any external resource. Every Table Data Gateway IS a Gateway, but not all Gateways are Table Data Gateways. Using "Gateway" to mean "database gateway that returns rows" is the most common PEAA vocabulary error.

WHY: Confusion between the two leads engineers to reject the generic Gateway pattern when they already know Table Data Gateway — or to misapply the pattern to a data-access context where Table Data Gateway is the correct choice.

**2. Money pattern means no floats, ever.**
`double` and `float` are binary floating-point types. They cannot exactly represent most decimal fractions. `0.1 + 0.1 + 0.1 != 0.3` in IEEE 754. For monetary arithmetic, use integer cents (`long`) or fixed-point decimal (`BigDecimal`, `decimal`, `Decimal`). The Money pattern wraps these with currency-awareness and safe allocation.

WHY: Float-based monetary arithmetic silently accumulates rounding errors. These errors surface as penny discrepancies in financial reports, which have compliance and audit consequences.

**3. Special Case chains, while Optional terminates.**
When you replace a null customer with a `NullCustomer` Special Case, `nullCustomer.contract` can return a `NullContract` (another Special Case) rather than null. This chain propagates polymorphism through the domain model without any null checks anywhere. `Optional<T>` requires the caller to handle the empty case at each `.get()` — it shifts the null-check burden rather than eliminating it.

WHY: The entire value of Special Case is eliminating branching. Understanding the chain behavior is essential to implementing Special Case correctly.

**4. Registry is service-locator style — prefer DI injection in modern systems.**
Fowler himself says Registry is "global data, guilty until proven innocent" and to use it only as a last resort. Modern DI containers (Spring, .NET DI, Guice) push dependencies into constructors at wiring time, making dependencies explicit, testable, and auditable. Registry is appropriate in a narrow set of cases: deeply nested utility code that cannot be wired via constructor, or lightweight applications without a DI framework.

WHY: Registry is commonly cargo-culted from older codebases into modern ones where DI would be simpler and safer. Flagging the tradeoff prevents this.

**5. Separated Interface has a cost — only use it to break specific dependencies.**
Each Separated Interface requires a factory with its own interface and implementation. Fowler explicitly warns against applying this to every class. For most classes, put the interface and implementation together. Separate them only when (a) you need to break a layer dependency cycle, (b) you need multiple independent implementations, or (c) you're working across team boundaries.

WHY: The pattern's benefit is targeted dependency management. Applied universally, it doubles the boilerplate without adding clarity.

---

## Examples

### Scenario 1: Wrapping a 3rd-Party Shipping API

**Trigger:** "We integrate with FedEx via their proprietary SDK. Every service class that needs shipping rates calls the SDK directly. I want to hide it behind a clean interface."

**Process:**
1. Identify: external resource with awkward API → **Gateway** pattern.
2. Check for confusion: is this a data-access gateway? No — it's a shipping service → generic Gateway (not Table Data Gateway).
3. Recommend: create `ShippingRateGateway` interface + `FedExShippingRateGateway` implementation. The interface reflects your application's needs, not FedEx's full SDK.
4. Surface adjacents: design the Gateway to be replaceable with a Service Stub for testing. Use Plugin or DI to wire the implementation.

**Output (design note):**
```markdown
## Pattern: Gateway

**Applied to:** FedEx shipping rate integration

**Why this pattern:** The FedEx SDK has a complex, proprietary API. Wrapping it in a
Gateway isolates all SDK coupling in one class, enables unit testing via a stub, and
makes future provider changes (FedEx → UPS) a single-class swap.

**Implementation shape (TypeScript):**
interface ShippingRateGateway {
  getRates(origin: Address, destination: Address, weight: kg): ShippingRate[];
}

class FedExShippingRateGateway implements ShippingRateGateway {
  getRates(origin, destination, weight) {
    // translate to FedEx SDK call + translate response
  }
}

class StubShippingRateGateway implements ShippingRateGateway {
  getRates() { return [{ carrier: "FedEx", service: "Ground", price: Money.dollars(12.50) }]; }
}

**Cautions:**
- This is a generic Gateway (Chapter 18), not a Table Data Gateway (Chapter 10).
  Table Data Gateway is for database table access specifically.
```

---

### Scenario 2: Money Stored as Floats

**Trigger:** "Our invoice totals sometimes show $0.01 discrepancies. We store monetary amounts as `double` in the database and in our Java domain objects."

**Process:**
1. Identify: monetary arithmetic with float → **Money** pattern.
2. Root cause: IEEE 754 floating-point cannot represent decimal fractions exactly.
3. Recommend: introduce a `Money` class with `long` (cents) + `Currency` field. Replace all `double`/`float` money fields.
4. Allocation warning: if they split amounts (tax splits, discount allocation), flag Foemmel's Conundrum — simple rounding can gain or lose pennies. Use the `allocate(ratios[])` method.

**Output:**
```markdown
## Pattern: Money

**Applied to:** Invoice total calculation

**Why this pattern:** `double` cannot represent most decimal fractions exactly in
IEEE 754. $0.01 discrepancies are the direct result. Money pattern wraps amount
(stored as integer cents) + Currency and enforces safe arithmetic.

**Implementation shape (Java):**
public record Money(long cents, Currency currency) {
    public Money add(Money other) {
        assertSameCurrency(other);
        return new Money(cents + other.cents, currency);
    }
    public Money[] allocate(int[] ratios) { /* use ratio algorithm, not rounding */ }
}

**Cautions:**
- Never use double/float for monetary amounts.
- For allocation (70/30 splits): use allocate-by-ratio, not simple rounding.
  Rounding 5 cents 70/30 loses or gains a penny. The ratio algorithm distributes
  remainders one cent at a time.
```

---

### Scenario 3: Null Checks for Missing Customer

**Trigger:** "When a customer hasn't been identified yet (occupant utility account), we return null from `findCustomer()`. Now we have null checks in 12 places, all doing the same fallback: name='Unknown', balance=0, lastBill=null."

**Process:**
1. Identify: repeated null checks with same fallback behavior → **Special Case** pattern.
2. Distinguish: Null Object (GoF) is Special Case specialized for null. This is the right pattern.
3. Recommend: create `UnknownCustomer extends Customer` with default implementations. Change `findCustomer()` to return `UnknownCustomer()` instead of null. Remove the 12 null checks.
4. Chain note: `unknownCustomer.lastBill` should return a `NullBill` Special Case, not null.

**Output:**
```markdown
## Pattern: Special Case (Null Object variant)

**Applied to:** findCustomer() returning null for unidentified occupant accounts

**Why this pattern:** 12 identical null-check blocks are code duplication. Special Case
eliminates the branching by making the missing case a valid polymorphic subtype.

**Implementation shape (Python):**
class UnknownCustomer(Customer):
    @property
    def name(self) -> str: return "Unknown"
    @property
    def balance(self) -> Decimal: return Decimal("0")
    @property
    def last_bill(self) -> Bill: return NullBill()

def find_customer(id: str) -> Customer:
    result = db.find_customer(id)
    return result if result else UnknownCustomer()

**Cautions:**
- last_bill should return NullBill(), not None — chain the Special Case pattern.
- Optional[Customer] shifts branching to call sites, not eliminating it.
  Special Case removes branching entirely.
```

---

## References

- `references/base-patterns-cheatsheet.md` — per-pattern deep-dive: full definitions, implementation sketches, modern parallels, and Fowler's cautions for all 11 patterns.

**Related PEAA skills that invoke base patterns:**
- `data-source-pattern-selector` — recommends Gateway (wrapping data sources) and Mapper.
- `domain-logic-pattern-selector` — recommends Service Stub for testing domain logic, Value Object, Special Case.
- `object-relational-structural-mapping-guide` — covers Embedded Value (persistence strategy for Value Object, Money).
- `distribution-boundary-designer` — recommends Separated Interface for distribution boundaries.
- `web-presentation-pattern-selector` — references Plugin for theme/environment-based view selection.

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler, David Rice, Matthew Foemmel, Edward Hieatt, Robert Mee, Randy Stafford.

---

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-data-source-pattern-selector`
- `clawhub install bookforge-domain-logic-pattern-selector`
- `clawhub install bookforge-distribution-boundary-designer`
- `clawhub install bookforge-object-relational-structural-mapping-guide`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
