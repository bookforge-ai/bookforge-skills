# Modularity Metrics Reference

This reference provides the complete metrics framework for evaluating code modularity. Read this when you need exact formulas, threshold values, or the full connascence taxonomy.

## Cohesion Types (Ranked Best to Worst)

| Rank | Type | Definition | Example | Signal |
|:----:|------|-----------|---------|--------|
| 1 | **Functional** | Every part relates to a single function; all parts are essential | A `PaymentProcessor` class that only handles payment authorization, capture, and refund | Methods share most fields; removing any method breaks the class |
| 2 | **Sequential** | One part's output becomes the next part's input | A data pipeline class where `parse()` feeds `validate()` feeds `transform()` | Clear input-output chain between methods |
| 3 | **Communicational** | Parts operate on the same data for different purposes | A class that both saves a customer record to the database and sends a confirmation email using the same customer data | Methods share input data but produce different outputs |
| 4 | **Procedural** | Parts must execute in a specific order | A deployment class where `stopServer()` must run before `deployArtifact()` before `startServer()` | Order matters but methods don't share data |
| 5 | **Temporal** | Parts are grouped by timing, not function | A `SystemStartup` class that initializes logging, opens DB connections, and starts background threads | Methods run at the same time but are functionally unrelated |
| 6 | **Logical** | Parts are logically related but functionally different | `StringUtils` with `toUpperCase()`, `trim()`, `parseDate()`, `formatCurrency()` | Methods operate on similar types but serve different purposes |
| 7 | **Coincidental** | Parts have no meaningful relationship | A `Helpers` class with random methods thrown in for convenience | No discernible reason why these methods are together |

### Cohesion Assessment Heuristic

Ask: "If I described this module's responsibility, how many sentences would it take?"
- 1 sentence -> likely functional cohesion
- 2-3 sentences with "and" -> likely communicational or sequential
- 4+ sentences or uses "and/or" -> likely logical or coincidental

## LCOM (Lack of Cohesion in Methods)

### Definition

LCOM measures the structural cohesion of a class by analyzing how methods share instance variables (fields).

**LCOM = The sum of sets of methods NOT shared via fields**

Practical interpretation:
- **LCOM = 0:** Perfect structural cohesion. All methods access the same fields.
- **LCOM low:** Good cohesion. Most methods share fields.
- **LCOM high:** Poor cohesion. Methods form separate groups that don't share state. The class is likely multiple classes combined.

### How to Estimate LCOM Without Tooling

1. List all instance variables (fields) in the class
2. For each method, note which fields it accesses
3. Group methods by shared field access
4. If you get multiple disconnected groups -> LCOM is high

**Quick check:** If a class has N fields but each method only uses 2-3 of them, and different methods use different subsets, LCOM is high. The class should probably be split along the field-access boundaries.

### Visual Interpretation

```
Class X (Low LCOM - Good)    Class Y (High LCOM - Bad)    Class Z (Mixed)
  Fields: A, B, C              Fields: A, B, C              Fields: A, B, C
  m1() uses A, B, C            m1() uses A                  m1() uses A, B
  m2() uses A, B               m2() uses B                  m2() uses A, B
  m3() uses B, C               m3() uses C                  m3() uses C
  -> All connected             -> All disconnected           -> Two groups: {m1,m2} and {m3}
  -> Keep as one class         -> Split into 3 classes       -> Consider extracting m3+C
```

### Limitations

LCOM measures **structural** lack of cohesion only. It cannot determine if a grouping is **logically** cohesive. A `MathUtils` class with static methods sharing no state has high LCOM but may be a reasonable design choice. Always combine LCOM with cohesion type analysis.

## Coupling Metrics

### Afferent Coupling (Ca) — Incoming

- **What it measures:** The number of external modules that depend on THIS module
- **Mnemonic:** **A**fferent = **A**pproaching = incoming arrows
- **High Ca means:** Many things break if you change this module. It has high responsibility.
- **Example:** A `DateUtils` class used by 50 other classes has Ca = 50

### Efferent Coupling (Ce) — Outgoing

- **What it measures:** The number of external modules THIS module depends on
- **Mnemonic:** **E**fferent = **E**xiting = outgoing arrows
- **High Ce means:** This module is fragile. Changes in any dependency can break it.
- **Example:** A `ReportGenerator` that imports from 12 other packages has Ce = 12

### Coupling Interpretation Table

| Ca | Ce | Profile | Risk |
|:--:|:--:|---------|------|
| High | Low | Foundation/library | Stable but painful to change |
| Low | High | Leaf/application | Volatile but safe to change |
| High | High | Hub/bottleneck | Dangerous — fragile AND high-impact |
| Low | Low | Isolated | Low risk but check if it's actually used |

## Derived Metrics

### Instability

```
I = Ce / (Ca + Ce)
```

| I Value | Meaning | Description |
|:-------:|---------|-------------|
| 0.0 | Maximally stable | Only dependents, no dependencies. Foundation code. |
| 0.5 | Balanced | Equal incoming and outgoing. |
| 1.0 | Maximally unstable | Only dependencies, no dependents. Leaf code. |

**Key insight:** Instability is not inherently bad. Leaf code SHOULD be unstable (I near 1) because it can change freely without affecting others. Foundation code SHOULD be stable (I near 0) because many things depend on it. The problem arises when stability doesn't match abstractness (see Distance).

### Abstractness

```
A = sum(abstract_elements) / sum(total_elements)
```

Where abstract elements = interfaces + abstract classes, total elements = all classes/modules.

| A Value | Meaning | Description |
|:-------:|---------|-------------|
| 0.0 | Fully concrete | No interfaces or abstract classes. All implementation. |
| 0.5 | Balanced | Half abstract, half concrete. |
| 1.0 | Fully abstract | All interfaces/abstract classes. No implementations. |

### Distance from Main Sequence

```
D = |A + I - 1|
```

| D Value | Meaning | Description |
|:-------:|---------|-------------|
| 0.0 | On the main sequence | Perfect balance of abstractness and instability. |
| 0.5 | Moderate deviation | Somewhat imbalanced. Worth investigating. |
| 1.0 | Maximum deviation | Severely imbalanced. In a danger zone. |

**Target:** D < 0.3 is generally healthy. D > 0.5 requires investigation.

## The Main Sequence Graph

```
Abstractness (A)
1.0 |  ZONE OF USELESSNESS
    |  (high A, high I)         /
    |  Too abstract,          /
    |  nobody uses it       /
    |                     /
0.5 |                   /  <-- Main Sequence (ideal)
    |                 /
    |               /
    |             /
    |           /    ZONE OF PAIN
    |         /      (low A, low I)
0.0 |       /        Too concrete, hard to change
    +----+----+----+----+----+-> Instability (I)
    0.0  0.2  0.4  0.6  0.8  1.0
```

### Zone of Pain (Bottom-Left Corner)

- **Metrics:** I near 0 (very stable) + A near 0 (very concrete)
- **What it means:** The module has many dependents (stable) but no abstractions (concrete). Changing it forces changes in all dependents. There's no interface to provide flexibility.
- **Common examples:** Utility libraries, core domain models, shared database schemas, configuration classes
- **Symptom:** "We're afraid to touch this because everything breaks"
- **Fix:** Introduce interfaces/abstractions so dependents couple to the interface, not the implementation. This increases A without changing I, moving toward the main sequence.
- **Caveat:** Some zone-of-pain modules are acceptable. The Java String class is concrete (A=0) and maximally stable (Ca=enormous), but it rarely needs to change. Non-volatile concrete libraries can safely live in this zone.

### Zone of Uselessness (Top-Right Corner)

- **Metrics:** I near 1 (very unstable) + A near 1 (very abstract)
- **What it means:** The module is all interfaces with no concrete use, and nobody depends on it. It was probably designed speculatively or is an abandoned abstraction layer.
- **Common examples:** Over-engineered framework interfaces, abandoned plugin systems, "just in case" abstractions
- **Symptom:** "Nobody actually implements this interface"
- **Fix:** Either find concrete uses or delete it. Dead abstractions add cognitive load without value.

## Connascence Taxonomy

### Static Connascence (Source-Level, Weaker)

| Type | Abbreviation | Definition | Example | Refactoring Ease |
|------|:------------:|-----------|---------|:----------------:|
| **Name** | CoN | Components agree on the name of an entity | Method names, variable names | Trivial (IDE rename) |
| **Type** | CoT | Components agree on the type of an entity | Parameter types, return types | Easy (type refactoring) |
| **Meaning** | CoM / CoC | Components agree on the meaning of values | `int TRUE = 1; int FALSE = 0;` or status code conventions | Moderate (replace magic values with named constants) |
| **Position** | CoP | Components agree on the order of values | Parameter order in method calls | Moderate (use named parameters or builder pattern) |
| **Algorithm** | CoA | Components must use the same algorithm | Client and server both use SHA-256 for auth tokens | Hard (algorithm change requires coordinated update) |

### Dynamic Connascence (Runtime, Stronger)

| Type | Abbreviation | Definition | Example | Refactoring Ease |
|------|:------------:|-----------|---------|:----------------:|
| **Execution** | CoE | Order of execution matters | Must call `init()` before `send()` | Hard (requires API redesign) |
| **Timing** | CoT | Timing of execution matters | Race conditions between threads | Very hard (requires synchronization redesign) |
| **Values** | CoV | Multiple values must change together | Distributed transaction: all or nothing | Very hard (may require saga pattern) |
| **Identity** | CoI | Components must reference the same entity | Two services sharing a distributed queue | Very hard (requires shared state management) |

### Connascence Strength Diagram

```
WEAKER (prefer)                                    STRONGER (avoid across boundaries)
    |                                                        |
    Name -> Type -> Meaning -> Position -> Algorithm -> Execution -> Timing -> Values -> Identity
    |<--- Static (compile-time) --->|                  |<--- Dynamic (runtime) ----------->|
    |<--- Easier to detect/fix ---->|                  |<--- Harder to detect/fix -------->|
```

### Connascence Properties

**Strength:** Weaker forms are easier to refactor. Always convert strong connascence to weaker forms when possible.

**Locality:** The same connascence form is more acceptable within a module boundary than across boundaries. Connascence of Meaning within one class is a code smell. Connascence of Meaning across microservices is an architectural crisis.

**Degree:** The number of components affected. Connascence of Values between 2 components is manageable. Between 20 components, it's a systemic problem.

### Three Guidelines for Improving Modularity via Connascence

1. **Minimize overall connascence** by breaking the system into encapsulated elements
2. **Minimize cross-boundary connascence** — coupling that crosses module boundaries should be as weak as possible
3. **Maximize within-boundary connascence** — strong coupling within a cohesive module is fine

### Weirich's Rules

- **Rule of Degree:** Convert strong forms of connascence into weaker forms
- **Rule of Locality:** As the distance between software elements increases, use weaker forms of connascence

## Unifying Coupling and Connascence

Structured Design coupling (afferent/efferent) and connascence are complementary views:
- **Coupling** tells you HOW MUCH coupling exists (Ca/Ce counts)
- **Connascence** tells you WHAT KIND of coupling exists (how they're coupled)

Both are needed for a complete picture. High Ca with CoN (name-based coupling) is far less concerning than moderate Ca with CoV (value-based coupling across a distributed system).

## Practical Tooling

| Language | Coupling Analysis | LCOM Analysis | Connascence |
|----------|------------------|---------------|-------------|
| Java | JDepend, SonarQube, ArchUnit | SonarQube LCOM4, Checkstyle | Manual / code review |
| .NET | NDepend, SonarQube | NDepend LCOM | Manual / code review |
| Python | import analysis, pydeps | Manual (dynamic typing limits) | Manual / code review |
| JavaScript/TypeScript | madge, dependency-cruiser | ESLint complexity rules | Manual / code review |
| Go | go vet, staticcheck | Manual (composition over inheritance) | Manual / code review |
| General | Graphviz for dependency visualization | Structural analysis from imports | Always requires human judgment |
