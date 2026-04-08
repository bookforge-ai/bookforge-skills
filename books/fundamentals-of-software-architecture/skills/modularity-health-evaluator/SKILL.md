---
name: modularity-health-evaluator
description: Assess code modularity health using quantitative metrics — cohesion (LCOM), coupling (afferent/efferent), abstractness, instability, distance from main sequence, and connascence taxonomy. Use this skill whenever the user asks about module quality, code coupling analysis, cohesion measurement, class decomposition, package dependency analysis, LCOM scores, afferent/efferent coupling, connascence, zone of pain, zone of uselessness, extracting microservices from a monolith, evaluating module boundaries, dependency analysis, or wants to know if a class or package is well-structured — even if they don't use the term "modularity."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fundamentals-of-software-architecture/skills/modularity-health-evaluator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: fundamentals-of-software-architecture
    title: "Fundamentals of Software Architecture"
    authors: ["Mark Richards", "Neal Ford"]
    chapters: [3]
tags: [software-architecture, modularity, cohesion, coupling, connascence, LCOM, metrics, refactoring]
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "A software project or module descriptions to analyze for modularity health"
    - type: none
      description: "Alternatively, a textual description of classes, packages, and their dependencies"
  tools-required: [Read, Write]
  tools-optional: [Grep, Glob, Bash]
  mcps-required: []
  environment: "Best results inside a codebase directory. Can also work from user-provided descriptions."
---

# Modularity Health Evaluator

## When to Use

You need to assess the structural health of code modules — classes, packages, components, or services — using quantitative modularity metrics. Typical triggers:

- The user has a class with too many methods or responsibilities and wants to evaluate it
- The user has a utility package that everything depends on and wants to understand the risk
- The user is planning to extract microservices and needs to evaluate which modules are cleanly bounded
- The user mentions coupling, cohesion, or dependency problems
- The user sees cascading breakage when changing one module and wants to diagnose why
- The user wants to evaluate whether a codebase is ready for architectural migration

Before starting, verify:
- Is there a specific module, class, or package to evaluate? (At minimum, a description of the component and its dependencies)
- Does the user have access to dependency analysis tooling, or will this be a manual/descriptive assessment?

## Context & Input Gathering

### Required Context (must have before proceeding)

- **Target module(s):** What class, package, or component needs evaluation?
  -> Check prompt for: class names, package names, module descriptions, dependency complaints
  -> Check environment for: src/ directories, package structures, build files
  -> If still missing, ask: "Which specific class, package, or module would you like me to evaluate for modularity health?"

- **Dependency information:** What depends on this module, and what does it depend on?
  -> Check prompt for: import lists, dependency descriptions, "everything depends on X" statements
  -> Check environment for: import statements, package.json, pom.xml, go.mod, build.gradle
  -> If still missing, ask: "Can you describe what other modules depend on this one (incoming), and what this module depends on (outgoing)?"

### Observable Context (gather from environment if available)

- **Codebase structure:** How is the code organized?
  -> Look for: directory structure, package naming conventions, module boundaries
  -> If unavailable: rely on user description

- **Class/method details:** Method counts, field usage, abstract vs concrete elements
  -> Look for: source files, interface definitions, abstract classes
  -> If unavailable: ask the user for approximate counts

- **Existing metrics:** Any existing static analysis reports (SonarQube, JDepend, etc.)
  -> Look for: build reports, CI artifacts, quality gate configs
  -> If unavailable: compute metrics manually from code or descriptions

### Default Assumptions

- If no specific metrics tools available -> perform manual analysis from code structure and user descriptions
- If method-field mapping is unknown -> estimate LCOM from class description and responsibility count
- If exact dependency counts unknown -> use the user's qualitative description to estimate Ca/Ce ranges
- If abstractness ratio unknown -> assume low abstractness (A ~ 0.1) for typical application code unless interfaces are explicitly described

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- At least one target module is identified with enough detail to assess
- Dependency direction (incoming/outgoing) is known or estimable
- Module responsibilities are described or observable from code

PROCEED WITH DEFAULTS when:
- Target module is identified
- Dependencies are partially known
- Exact counts can be estimated from qualitative descriptions

MUST ASK when:
- No target module is identified (cannot assess modularity without a subject)
- The user's description is too vague to estimate any metrics
- It's ambiguous whether the problem is cohesion, coupling, or both
```

## Process

### Step 1: Identify and Catalog Target Modules

**ACTION:** List all modules (classes, packages, components) to be evaluated. For each, document: name, primary responsibility, approximate method/function count, and any known dependencies.

**WHY:** Modularity assessment requires concrete targets. Vague discussions about "coupling" without naming specific modules produce generic advice. By naming each module and its responsibility, you establish the scope for all subsequent metrics. A module's responsibility statement also serves as the baseline for evaluating cohesion — if the responsibility can't be stated in one sentence, the module likely has poor cohesion.

**IF** a codebase is available -> **AGENT: EXECUTES** — scan directory structure, count files per package, identify key classes
**ELSE** -> use the user's description to build the module catalog

### Step 2: Evaluate Cohesion

**ACTION:** For each target module, assess cohesion type and estimate LCOM:

**Cohesion type** (ranked best to worst):
1. **Functional** — every part relates to a single, well-defined function. All elements are essential.
2. **Sequential** — one part's output feeds the next part's input (pipeline within the module).
3. **Communicational** — parts operate on the same data to produce different outputs.
4. **Procedural** — parts must execute in a specific order but aren't otherwise related.
5. **Temporal** — parts are grouped because they run at the same time (e.g., initialization code).
6. **Logical** — parts are logically related but functionally different (e.g., StringUtils).
7. **Coincidental** — parts have no relationship; they're in the same module by accident.

**LCOM estimation:**
- Count the instance variables (fields) in the class
- For each method, note which fields it accesses
- LCOM = the sum of sets of methods NOT sharing fields. Higher LCOM = worse cohesion.
- Practical shortcut: if most methods use only 2-3 of 12 fields, LCOM is high (bad). If most methods share most fields, LCOM is low (good).

**WHY:** Cohesion determines whether a module is a natural grouping or an artificial one. Low cohesion (logical or coincidental) means the module is really multiple modules crammed together — any change risks unintended side effects on unrelated functionality. LCOM gives a structural measure: a class where methods don't share fields is structurally disconnected, meaning each field/method group could be its own class. This is the single most important indicator for "should I split this class?"

**IF** source code is available -> **AGENT: EXECUTES** — analyze field-method relationships, calculate approximate LCOM
**ELSE** -> estimate from the user's description of what the class/module does

### Step 3: Measure Coupling (Afferent and Efferent)

**ACTION:** For each target module, count:

- **Afferent coupling (Ca):** Number of modules that depend on THIS module (incoming connections — "who uses me?")
- **Efferent coupling (Ce):** Number of modules THIS module depends on (outgoing connections — "who do I use?")

Mnemonic: **a**fferent = **a**pproaching (incoming), **e**fferent = **e**xiting (outgoing).

**WHY:** Coupling metrics reveal risk exposure. High Ca means many modules break if you change this one — it's a high-responsibility position. High Ce means this module is fragile because it depends on many others — any upstream change can break it. Neither is inherently bad, but the combination determines the module's stability profile (Step 4). A utility package with Ca=50 and Ce=0 is stable but painful to modify. A service with Ca=0 and Ce=15 is volatile but safe to change.

**IF** codebase is available -> **AGENT: EXECUTES** — analyze imports, build dependency graph, count Ca and Ce per module
**ELSE** -> estimate from user's description of dependency directions

### Step 4: Calculate Derived Metrics

**ACTION:** From the coupling measurements, calculate three derived metrics:

1. **Instability: I = Ce / (Ca + Ce)**
   - Range: 0 to 1
   - I = 0: maximally stable (only incoming dependencies, no outgoing — e.g., a foundational library)
   - I = 1: maximally unstable (only outgoing dependencies, no incoming — e.g., a leaf application)

2. **Abstractness: A = abstract_elements / total_elements**
   - Range: 0 to 1
   - Count interfaces, abstract classes as abstract elements
   - Count all classes/modules as total elements
   - A = 0: fully concrete (no abstractions)
   - A = 1: fully abstract (all interfaces, no implementations)

3. **Distance from Main Sequence: D = |A + I - 1|**
   - Range: 0 to 1
   - D = 0: perfectly balanced (on the ideal main sequence line)
   - D = 1: maximally imbalanced

**WHY:** These derived metrics reveal architectural health that raw coupling counts miss. The main sequence represents the ideal balance: highly stable modules should be abstract (so dependents rely on interfaces, not implementations), and highly unstable modules should be concrete (they change freely since nobody depends on them). Distance from the main sequence quantifies how far a module deviates from this ideal, identifying the two danger zones.

### Step 5: Identify Zone Placement

**ACTION:** Plot each module on the Abstractness-Instability graph and classify:

- **Zone of Pain** (lower-left: I near 0, A near 0): Highly stable AND highly concrete. Many modules depend on it, but it has no abstractions. Painful to change because changes ripple to all dependents, and there are no interfaces to provide flexibility.
  -> Examples: utility libraries, core data models, shared database schemas
  -> Signal: "We're afraid to touch this because everything breaks"

- **Zone of Uselessness** (upper-right: I near 1, A near 1): Highly unstable AND highly abstract. Few modules depend on it, and it's all interfaces with no concrete use.
  -> Examples: over-engineered frameworks nobody uses, abandoned abstraction layers
  -> Signal: "Nobody actually uses this interface hierarchy"

- **Main Sequence** (diagonal from upper-left to lower-right): The healthy zone. Stable modules are abstract (changeable via interfaces). Unstable modules are concrete (free to change).

**WHY:** Zone placement converts abstract metrics into actionable diagnosis. A module in the zone of pain needs abstraction (introduce interfaces so dependents don't couple to concrete implementation). A module in the zone of uselessness needs evaluation for removal or consolidation. Modules near the main sequence are healthy. This visualization makes the metrics tangible for stakeholders who can't interpret raw Ca/Ce numbers.

### Step 6: Analyze Connascence

**ACTION:** For each significant coupling relationship between modules, classify the connascence type:

**Static connascence** (source-level, weaker, easier to fix):
- **Name (CoN):** Components agree on names. Weakest, most desirable.
- **Type (CoT):** Components agree on types. Standard in typed languages.
- **Meaning/Convention (CoM):** Components agree on value meanings (e.g., magic numbers, status codes).
- **Position (CoP):** Components agree on parameter order.
- **Algorithm (CoA):** Components must use the same algorithm (e.g., hashing on both client and server).

**Dynamic connascence** (runtime, stronger, harder to fix):
- **Execution (CoE):** Order of execution matters between components.
- **Timing (CoT):** Timing of execution matters (race conditions).
- **Values (CoV):** Multiple values must change together (distributed transactions).
- **Identity (CoI):** Components must reference the same entity instance.

**Three guidelines for improvement:**
1. Minimize overall connascence by encapsulating
2. Minimize connascence that crosses module boundaries
3. Maximize connascence within module boundaries

**Rules from Jim Weirich:**
- **Rule of Degree:** Convert strong connascence to weaker forms
- **Rule of Locality:** As distance between modules increases, use weaker connascence forms

**WHY:** Connascence provides a vocabulary for discussing coupling quality, not just quantity. Two modules with the same Ca/Ce scores can have very different coupling health. Connascence of Name is trivially refactorable (rename a method). Connascence of Values across a distributed system (distributed transactions) is architecturally significant and may require redesigning service boundaries. Identifying connascence type tells you HOW hard the coupling is to address, while Ca/Ce tell you HOW MUCH coupling exists.

**HANDOFF TO HUMAN** for runtime connascence analysis — dynamic connascence (execution order, timing, values, identity) requires production observation, distributed tracing, or load testing to fully assess.

### Step 7: Synthesize Assessment and Recommend Actions

**ACTION:** Produce the Modularity Health Report combining all metrics, zone placements, and connascence findings. For each module, provide:
- Overall health rating (Healthy / At Risk / Unhealthy)
- Primary concern (cohesion, coupling, zone placement, or connascence)
- Specific refactoring recommendation with expected improvement

**WHY:** Individual metrics are useful but can be misleading in isolation. A high LCOM is meaningless if the class has low coupling and few dependents. The synthesis step weighs all factors together and prioritizes what to fix first. The recommendation must be specific enough to act on — "improve cohesion" is useless; "extract the notification methods (notifyCustomer, sendEmail, formatNotification) into a NotificationService" is actionable.

**IF** the user's goal is microservice extraction -> prioritize recommendations that create clean boundaries (low Ce, functional cohesion, weak cross-boundary connascence)
**IF** the user's goal is code quality improvement -> prioritize LCOM reduction and connascence simplification

## Inputs

- Target module(s) to evaluate: class names, package names, or component descriptions
- Dependency information: what depends on the module and what it depends on
- Optionally: source code access, existing static analysis reports, module responsibility descriptions

## Outputs

### Modularity Health Report

```markdown
# Modularity Health Report: {System/Component Name}

## Assessment Scope
- **Date:** {date}
- **Modules assessed:** {count}
- **Assessment method:** {codebase analysis / description-based / hybrid}
- **Tools used:** {JDepend, SonarQube, manual analysis, etc.}

## Module Catalog

| Module | Responsibility | Methods | Fields | Ca | Ce |
|--------|---------------|:-------:|:------:|:--:|:--:|
| {name} | {one-line responsibility} | {count} | {count} | {count} | {count} |

## Cohesion Assessment

| Module | Cohesion Type | LCOM Estimate | Rating |
|--------|-------------|:-------------:|:------:|
| {name} | {functional/sequential/.../coincidental} | {low/medium/high} | {good/warning/poor} |

### Cohesion Details
**{Module name}:** {detailed cohesion analysis with field-method groupings}

## Coupling & Derived Metrics

| Module | Ca | Ce | Instability (I) | Abstractness (A) | Distance (D) | Zone |
|--------|:--:|:--:|:---------------:|:-----------------:|:-------------:|------|
| {name} | {n} | {n} | {0-1} | {0-1} | {0-1} | {pain/uselessness/healthy} |

## Zone Placement Map

```
Abstractness (A)
1 |  Zone of         /
  |  Uselessness   /
  |              / [Module C]
  |            /
  |          /  <-- Main Sequence
  |        /
  |      /
  | [Module B]
  |  /   [Module A: Zone of Pain]
0 +----------------------------> 1
                    Instability (I)
```

## Connascence Analysis

| From -> To | Type | Strength | Across Boundary? | Concern Level |
|-----------|------|----------|:----------------:|:-------------:|
| {module A -> module B} | {CoN/CoT/CoM/...} | {weak/moderate/strong} | {yes/no} | {low/medium/high} |

## Health Summary

| Module | Health | Primary Concern | Recommended Action |
|--------|:------:|-----------------|-------------------|
| {name} | {Healthy/At Risk/Unhealthy} | {concern} | {specific action} |

## Prioritized Refactoring Recommendations

1. **{Highest priority}** — {specific action} -> Expected improvement: {metric change}
2. **{Second priority}** — {specific action} -> Expected improvement: {metric change}
3. **{Third priority}** — {specific action} -> Expected improvement: {metric change}
```

## Key Principles

- **Cohesion is subjective, coupling is structural** — Cohesion type requires judgment about whether groupings are "functional" or "logical." LCOM provides a structural proxy but can't distinguish essential complexity from accidental grouping. Use LCOM to flag suspects, then apply cohesion type analysis to confirm. Never rely on a single metric.

- **High coupling is not inherently bad — directionality matters** — A stable foundation library with Ca=100 and Ce=0 is healthy architecture. The problem is when high Ca combines with low abstractness (zone of pain) or when high Ce makes a module fragile. Always interpret coupling in context of instability and abstractness.

- **Connascence strength increases with distance** — Connascence of Name within a module is perfectly fine. Connascence of Values across distributed services is an architectural crisis. The same form of coupling becomes more dangerous as the distance between modules increases. Always evaluate connascence relative to module boundaries.

- **Metrics require interpretation, not just calculation** — All code-level metrics have limitations. LCOM detects structural lack of cohesion but can't distinguish essential complexity from poor design. Cyclomatic complexity can't distinguish inherent problem complexity from accidental code complexity. Calculate the metrics, then apply architectural judgment to interpret what they mean in context.

- **Zone of pain is more dangerous than zone of uselessness** — Code in the zone of uselessness wastes effort but doesn't block progress. Code in the zone of pain actively resists change and creates cascading failures. Prioritize moving modules out of the zone of pain (by introducing abstractions) over cleaning up the zone of uselessness.

- **Prefer weaker forms of connascence** — When you can't eliminate coupling, downgrade it. Convert connascence of meaning (magic numbers) to connascence of name (named constants). Convert connascence of algorithm (shared hashing) to connascence of type (shared library). Each downgrade makes the coupling cheaper to maintain and less likely to cause bugs.

## Examples

**Scenario: God class evaluation**
Trigger: "I have a CustomerService class with 35 methods, 12 instance variables, and methods spanning registration, billing, notifications, and reporting. Is this well-designed?"
Process: Cataloged the class. Identified 4 distinct responsibility groups from the method descriptions. Assessed cohesion as logical (methods related by entity, not by function). Estimated LCOM as high — registration methods use fields A,B,C; billing methods use fields D,E,F; notification methods use fields G,H; reporting methods use fields I,J,K,L. Few fields shared across groups. Measured Ca=15 (many dependents), Ce=8. Calculated I=0.35, A=0.0, D=0.65 — deep in zone of pain. Recommended extracting into 4 focused services: CustomerRegistrationService, BillingService, NotificationService, CustomerReportingService. Expected improvement: each new class achieves functional cohesion, LCOM drops to low, and D approaches 0.
Output: Modularity health report showing the class is Unhealthy with a specific 4-way decomposition plan.

**Scenario: Utility package dependency analysis**
Trigger: "Our utils package has 200 classes and every other package depends on it. We're afraid to change anything."
Process: Identified the utils package as having Ca=high (every package depends on it), Ce=low (it depends on nothing), I=0.0, A~0.05 (almost no interfaces). Plotted directly in zone of pain. Cohesion type: coincidental — date formatters, database helpers, and email templates have no functional relationship. Analyzed connascence: mostly CoN (name-based) from the rest of the codebase, but some CoM (magic numbers shared via utility constants). Recommended: (1) Extract date/time utilities into a DateTimeUtils package with an interface, (2) Move database helpers into a persistence package close to where they're used, (3) Extract email templates into a notification package. Each extraction reduces Ca on the remaining utils and moves code to functionally cohesive homes.
Output: Modularity health report with 3-phase decomposition plan and expected zone migration from pain to main sequence.

**Scenario: Microservice extraction readiness assessment**
Trigger: "We have 15 top-level packages in our monolith. Which are ready to extract as microservices?"
Process: For each package, measured Ca, Ce, calculated I and A. Assessed cohesion type. Analyzed cross-package connascence. Found 4 packages with functional cohesion, low Ce, and weak cross-boundary connascence (good candidates). Found 3 packages in zone of pain with high Ca (extract last — need abstraction first). Found 2 packages with high CoV (shared transactions — cannot extract without addressing data consistency). Ranked all 15 by extraction readiness score. Recommended extraction order: start with the 4 clean candidates, then refactor the zone-of-pain packages by introducing interfaces, then address shared-transaction packages using saga pattern or shared database strategy.
Output: Ranked extraction readiness report with specific blockers and prerequisites for each package.

## References

- For the complete modularity metrics reference with formulas, cohesion taxonomy, connascence types, and zone definitions, see [references/modularity-metrics-reference.md](references/modularity-metrics-reference.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fundamentals of Software Architecture by Mark Richards, Neal Ford.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
