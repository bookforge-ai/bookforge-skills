---
name: oo-design-smell-detector
description: |
  Detect common OO design smells in a codebase and recommend corrective design patterns. Use when reviewing code for design quality, investigating why changes are difficult, or auditing coupling and inheritance depth. Scans for 8 categories of design fragility — hardcoded object creation, operation dependencies, platform coupling, representation leaks, algorithm dependencies, tight coupling, subclass explosion, and inability to alter classes — each mapped to specific GoF patterns that fix them. Trigger when the user asks about design review, code smells, design anti-patterns, why a class is hard to change, why adding a feature requires modifying many files, class hierarchy review, inheritance overuse, why changes cascade, tight coupling, poor encapsulation, object creation rigidity, platform-dependent code, algorithmic coupling, or difficulty extending a third-party class.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/oo-design-smell-detector
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [1]
    pages: [29-31, 34-36, 41]
tags: [design-patterns, design-smells, code-review, oo-design, refactoring, gof-patterns, inheritance, coupling, anti-patterns]
depends-on: []
execution:
  tier: 2
  mode: full
  inputs:
    - type: codebase
      description: "A software project or set of class/module descriptions to scan for design smells"
    - type: none
      description: "Alternatively, a textual description of a design problem or class structure"
  tools-required: [Read, Grep, Write, TodoWrite]
  tools-optional: [Glob, Bash]
  mcps-required: []
  environment: "Best results inside a codebase directory. Can also work from user-provided class descriptions."
---

# OO Design Smell Detector

## When to Use

You are auditing an object-oriented codebase — or a specific class or subsystem within one — for structural design problems that make change expensive. Typical triggers:

- "Every time I add a feature, I have to change 10 files"
- "This class hierarchy is getting out of control"
- "Changing the database means rewriting half the codebase"
- "I can't swap out this algorithm without touching everything that calls it"
- "We need to extend this library class but can't modify it"
- "New platforms require total rewrites"
- A pre-refactoring audit before a redesign sprint
- A code review specifically targeting design quality, not just style

Before starting, verify:
- Is there a specific class, subsystem, or entire codebase to scan?
- Is the user looking for an exhaustive audit or a targeted check on one smell category?

## Context & Input Gathering

### Required Context (must have before proceeding)

- **Scan target:** What is to be analyzed — a directory, a single class, a described design?
  -> Check prompt for: class names, package/directory references, file paths, language mentions
  -> Check environment for: src/ directories, class files, module structures
  -> If still missing, ask: "Which directory, class, or codebase should I scan for design smells?"

- **Programming language:** Determines what syntax patterns and idioms to look for.
  -> Check prompt for: language mentions ("Java", "Python", "C#", "TypeScript", etc.)
  -> Check environment for: file extensions (.java, .py, .cs, .ts), build files (pom.xml, setup.py)
  -> If still missing, ask: "What programming language is the codebase written in?"

### Observable Context (gather from environment if available)

- **Class hierarchy depth:** How deep is the inheritance tree?
  -> Look for: files with `extends`, `implements`, `: BaseClass` patterns; count hierarchy levels
  -> If unavailable: note as unobservable, flag for user to check manually

- **Object creation sites:** Where are concrete classes instantiated?
  -> Look for: `new ConcreteClass(`, constructor calls using specific class names (not interfaces)
  -> If unavailable: rely on user description

- **Platform or environment references:** Direct OS/API calls embedded in business logic?
  -> Look for: imports of platform-specific packages, direct file system or OS calls in domain classes
  -> If unavailable: assume unknown, flag for inspection

- **Algorithm implementations:** Are algorithms embedded inside data-holding classes?
  -> Look for: sort methods, transformation logic, parsing routines inside entity/model classes
  -> If unavailable: rely on user description

### Default Assumptions

- If no codebase is accessible -> perform assessment from user's description and produce a report with "described" rather than "observed" evidence
- If language cannot be determined -> ask (language affects detection patterns significantly)
- If no specific scope is given -> scan the primary source directory

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Scan target is identified (directory, class, or description)
- Programming language is known
- At least one source of evidence exists (code or description)

PROCEED WITH DEFAULTS when:
- Target is identified
- Language is known or strongly implied by file extensions
- Some source files are readable even if the full codebase is unavailable

MUST ASK when:
- No scan target is specified at all
- Language is ambiguous and detection patterns differ significantly between candidates
```

## Process

Use TodoWrite to track progress through the 8 smell categories. Complete all steps before producing the report.

### Step 1: Initialize Smell Scan Checklist

**ACTION:** Create a todo list tracking each of the 8 smell categories. Mark each as pending.

**WHY:** With 8 independent detection passes, it is easy to skip one when a particularly significant smell is found early. The checklist ensures systematic coverage and prevents the cognitive bias of stopping after the first hit. The final report is only credible if all 8 categories were actively checked, not just the ones that happened to be obvious.

Use TodoWrite to create tasks:
1. Detect hardcoded object creation (Smell DS-01)
2. Detect operation/request hardcoding (Smell DS-02)
3. Detect hardware/software platform coupling (Smell DS-03)
4. Detect representation and implementation leaks (Smell DS-04)
5. Detect algorithmic dependencies (Smell DS-05)
6. Detect tight coupling (Smell DS-06)
7. Detect subclass explosion from inheritance overuse (Smell DS-07)
8. Detect inability to alter classes (Smell DS-08)

### Step 2: Scan for Hardcoded Object Creation (DS-01)

**ACTION:** Search for `new ConcreteClass(` patterns (or language equivalent) outside of dedicated factory or builder classes. Look for concrete class names used as variable types instead of interface types. Note every location where object creation is hardwired to a specific implementation.

**WHY:** When code names a concrete class at instantiation, it commits to that implementation. If the class needs to change — for testing, configuration, or runtime variation — every call site must change too. This is not a hypothetical risk: it is one of the most common causes of "I can't write unit tests without running the whole stack." Detecting it now enables targeted introduction of Abstract Factory, Factory Method, or Prototype to centralize and isolate creation decisions.

**IF** codebase is accessible -> use Grep to search for `new [A-Z][a-zA-Z]+\(` patterns; filter out creation inside factory/builder classes; list remaining call sites
**ELSE** -> ask the user to describe how objects of key types are created in their design

Mark DS-01 todo item complete. Note findings.

### Step 3: Scan for Operation Dependencies (DS-02)

**ACTION:** Look for direct, hardcoded method calls that could instead be requests dispatched through a generic mechanism. Specifically: conditionals that branch on operation type (`if action == "save" ... else if action == "delete"`), hardcoded event handling with explicit method names per event type, or long chains of if/switch that encode what to do for each case.

**WHY:** Hardcoded request handling means every new operation requires a source change — you cannot add behavior at runtime or configuration time. This is how systems accumulate "god switches" where a central coordinator knows about every possible action. Chain of Responsibility and Command patterns address this by turning requests into objects and dispatching them polymorphically, which lets you add, remove, or reorder operations without touching existing code.

**IF** codebase accessible -> Grep for large switch/case blocks on operation type, long if/else-if chains on string or enum values representing actions
**ELSE** -> ask: "Are there places where the code explicitly branches on what operation to perform, using if/switch statements?"

Mark DS-02 complete. Note findings.

### Step 4: Scan for Platform Coupling (DS-03)

**ACTION:** Look for platform-specific imports, API calls, or OS dependencies embedded directly in business-logic classes. Examples: file system access in a domain model, direct database driver calls in a service class, OS-specific path constructions, platform API calls (Windows registry, Unix signals) in application code.

**WHY:** Platform coupling is the most expensive smell to fix late. Every time the operating environment changes — a cloud migration, a new OS target, a framework upgrade — classes that directly reference platform APIs require full rewrite rather than configuration. Abstracting platform access behind an interface (Abstract Factory for platform families, Bridge for independent variation) means platform changes stay contained to adapters, not spread across business logic.

**IF** codebase accessible -> Read key business/domain classes; check their import sections for OS, file system, or driver-level packages; Grep for direct platform API patterns
**ELSE** -> ask: "Do your domain or business-logic classes contain direct OS calls, file I/O, or database driver code?"

Mark DS-03 complete. Note findings.

### Step 5: Scan for Representation and Implementation Leaks (DS-04)

**ACTION:** Identify places where a class's internal data structure or implementation details are exposed to clients. Signs: returning internal collection references directly, public fields on objects that should be opaque, clients checking the internal state of an object to decide how to use it, or clients knowing which concrete implementation is behind an interface.

**WHY:** When clients know how an object is represented internally, any change to that representation requires changing every client. This is the classic encapsulation failure. It is also how simple refactors — "let's change from ArrayList to LinkedList" — become large multi-file changes. Patterns that address this: Abstract Factory (clients know only the interface), Bridge (separates interface from implementation), Memento (exposes state through a controlled opaque token), Proxy (controls access to the real object).

**IF** codebase accessible -> Look for public fields in domain classes; methods that return raw internal data structures (List, Map) rather than copies or views; clients using instanceof checks on returned objects
**ELSE** -> ask: "Do your classes expose internal data structures directly? Can clients see the concrete type behind an abstraction?"

Mark DS-04 complete. Note findings.

### Step 6: Scan for Algorithmic Dependencies (DS-05)

**ACTION:** Find algorithms embedded inside classes that are not specifically about algorithm management. Look for: sorting logic inside entity classes, serialization/parsing code mixed with domain logic, encryption or hashing routines inlined in services, data transformation code duplicated across multiple classes.

**WHY:** Algorithms change more often than the data they operate on. When an algorithm is embedded in a class, changing the algorithm means modifying the class — even if the class's real responsibility is elsewhere. This also prevents swapping algorithms at runtime (e.g., choosing a compression strategy based on data size). Strategy, Template Method, Iterator, Builder, and Visitor all isolate algorithms from the data they process, so algorithms can be extended, replaced, or composed without touching the data classes.

**IF** codebase accessible -> Grep for sort, parse, serialize, transform, encrypt, compress inside entity/model/domain classes; Read identified files to confirm algorithm embedding
**ELSE** -> ask: "Are there algorithms (sorting, parsing, serialization, encryption) embedded directly inside your data or entity classes?"

Mark DS-05 complete. Note findings.

### Step 7: Scan for Tight Coupling (DS-06)

**ACTION:** Identify classes with high fan-out (depending on many other concrete classes), classes that cannot be unit-tested without instantiating many collaborators, or classes that reference downstream classes by concrete type rather than interface. Also look for bidirectional dependencies between classes (A knows about B and B knows about A).

**WHY:** Tight coupling creates monolithic systems in disguise. Even if the code is in separate files, high concrete coupling means you cannot change, test, or reuse any class in isolation. The cost is paid every time: harder testing, cascading changes, inability to port or reuse components. The patterns that address this — Abstract Factory, Bridge, Chain of Responsibility, Command, Facade, Mediator, Observer — all share a common mechanism: they introduce an indirection layer that decouples the parties that need to collaborate.

**IF** codebase accessible -> Count imports in each class (high import counts with concrete class names are a signal); look for bidirectional references; identify classes that require many constructor arguments of concrete types
**ELSE** -> ask: "Which classes have the most dependencies on other concrete classes? Are there bidirectional references between classes?"

Mark DS-06 complete. Note findings.

### Step 8: Scan for Subclass Explosion (DS-07)

**ACTION:** Count the number of direct subclasses for key base classes. Flag any class with more than 5-7 direct subclasses as a candidate. Look for subclass names that suggest Cartesian products of features (e.g., `RedCircle`, `BlueCircle`, `RedSquare`, `BlueSquare`). Check whether inheritance is being used where composition or delegation would serve better.

**WHY:** This is the most common misuse of inheritance. When a class is extended to customize behavior for each variation of each dimension, the number of subclasses grows multiplicatively. Adding a new dimension (e.g., a new color when shapes already vary by size and color) requires doubling the number of subclasses. GoF describes this as inheritance "leading to an explosion of classes." The diagnostic: if subclass names look like they encode combinations of features, inheritance is doing work that composition (Bridge, Decorator, Strategy, Composite, Observer) should be doing. Delegation provides the same power as inheritance without the class-count explosion.

**IF** codebase accessible -> Glob for all class files; Grep for `extends BaseClass` or `: BaseClass` per base class; count subclass depth using a depth-first scan; flag hierarchies more than 3-4 levels deep or more than 7 direct subclasses
**ELSE** -> ask: "Are there base classes with many direct subclasses? Do subclass names suggest combinations of features?"

Also check: are there abstract classes with no behavior that exist solely to create a naming hierarchy? This is a sign of "classification for classification's sake" rather than behavior reuse.

Mark DS-07 complete. Note findings.

### Step 9: Scan for Inability to Alter Classes (DS-08)

**ACTION:** Identify classes that cannot be modified easily — either because they are third-party/library classes without source access, because any change would require modifying many existing subclasses in unison, or because the class is so entangled that isolating a change is risky. Look for: direct inheritance from library classes (rather than wrapping them), large numbers of subclasses that would all need updating, or classes referenced so widely that any change is feared.

**WHY:** Some classes simply cannot be changed: you lack source access, or changes would break a versioned API. When this happens, you need patterns that let you extend or adapt without modification. Adapter wraps the class to present a different interface. Decorator adds behavior by wrapping rather than subclassing. Visitor adds operations to a class hierarchy without changing the hierarchy. Detecting this smell early prevents teams from building deep inheritance chains on top of classes that cannot absorb change.

**IF** codebase accessible -> Grep for direct extension of library/framework classes; identify classes that appear in many files as imports but whose source is in a vendor or dependency directory
**ELSE** -> ask: "Are there classes (from libraries or elsewhere) that you need to extend or modify behavior for, but cannot change directly?"

Mark DS-08 complete. Note findings.

### Step 10: Assess Severity and Produce Report

**ACTION:** For each detected smell, assess severity using the two-factor rubric:
- **Spread:** How many locations in the codebase exhibit this smell? (1-2: isolated / 3-10: moderate / 10+: pervasive)
- **Friction:** How often does this smell cause actual change pain? (Low: rarely touched / Medium: touched occasionally / High: changed frequently)

Severity = Spread x Friction:
- Low spread + Low friction = **Advisory** (document, address opportunistically)
- Any Moderate combination = **Warning** (plan to address in next refactoring sprint)
- High spread + High friction = **Critical** (address before next feature work, blocks velocity)

Produce the Design Smell Report (see Outputs section).

**WHY:** Not all smells deserve equal urgency. A class instantiated concretely in 100 places that nobody ever needs to swap out is less urgent than a tightly coupled pair of classes that must change together every sprint. Severity assessment prevents the common failure mode of fixing cosmetically obvious smells while ignoring the high-friction ones that actually slow the team down.

### Step 11: Apply Pattern Overuse Warning

**ACTION:** For each recommended pattern, add a calibration note: is the flexibility the pattern provides actually needed? If the smell affects code that is stable and rarely changes, note this explicitly and downgrade the recommendation to "low priority."

**WHY:** Design patterns introduce indirection. Indirection adds complexity and performance overhead. A pattern should only be applied when the flexibility it provides is genuinely needed — not as a demonstration of pattern knowledge. GoF explicitly states: "A design pattern should only be applied when the flexibility it affords is actually needed." If a class creates a concrete object that will never need to be swapped, wrapping it in an Abstract Factory adds complexity with zero benefit. The report must distinguish between smells that need fixing now (high friction) versus theoretical smells in code that works fine (leave alone).

## Inputs

- Source directory or class files to scan
- Programming language of the codebase
- Optionally: specific concerns from the user (e.g., "focus on coupling" or "we're seeing subclass explosion")

## Outputs

### Design Smell Report

```markdown
# OO Design Smell Report: {System/Scope Name}

**Date:** {date}
**Scope:** {what was scanned}
**Language:** {language}
**Scan method:** {codebase analysis / description-based / hybrid}

## Executive Summary

{1-3 sentence summary of overall design health and top priority smell}

## Smell Findings

### DS-01: Hardcoded Object Creation
**Status:** {Detected / Not detected / Unable to assess}
**Severity:** {Advisory / Warning / Critical}
**Locations:** {list of specific files/classes/line ranges}
**Evidence:** {what was found — e.g., "new OrderRepository() called in 14 places across service layer"}
**Recommended patterns:** {Abstract Factory / Factory Method / Prototype}
**Justification:** {why this pattern fits this specific instance}
**Pattern overuse check:** {Is this flexibility actually needed? If the object never varies, note this.}

### DS-02: Operation Dependencies
**Status:** {Detected / Not detected / Unable to assess}
**Severity:** {Advisory / Warning / Critical}
**Locations:** {list of files/classes}
**Evidence:** {e.g., "45-line switch statement on event type in EventDispatcher.java"}
**Recommended patterns:** {Chain of Responsibility / Command}
**Justification:** {why this pattern fits}
**Pattern overuse check:** {If operations are fixed and never extended, flag as low priority.}

### DS-03: Platform Coupling
[same structure]

### DS-04: Representation Leaks
[same structure]

### DS-05: Algorithmic Dependencies
[same structure]

### DS-06: Tight Coupling
[same structure]

### DS-07: Subclass Explosion
**Status:** {Detected / Not detected / Unable to assess}
**Severity:** {Advisory / Warning / Critical}
**Hierarchy map:** {BaseClass -> list of subclasses, depth}
**Feature dimensions identified:** {e.g., "Shape x Color x Size"}
**Inheritance vs composition diagnosis:** {are subclasses encoding combinations?}
**Recommended patterns:** {Bridge / Decorator / Strategy / Composite / Observer}
**Refactoring sketch:** {high-level approach — e.g., "extract Color as a strategy, inject into Shape"}
**Pattern overuse check:** {If hierarchy is stable and combinations are fixed, note it.}

### DS-08: Inability to Alter Classes
[same structure]

## Priority Matrix

| Smell | Spread | Friction | Severity | Action |
|-------|:------:|:--------:|:--------:|--------|
| DS-01 Hardcoded creation | {isolated/moderate/pervasive} | {low/medium/high} | {Advisory/Warning/Critical} | {action} |
| DS-02 Operation coupling | ... | ... | ... | ... |
| DS-03 Platform coupling | ... | ... | ... | ... |
| DS-04 Representation leak | ... | ... | ... | ... |
| DS-05 Algorithmic dependency | ... | ... | ... | ... |
| DS-06 Tight coupling | ... | ... | ... | ... |
| DS-07 Subclass explosion | ... | ... | ... | ... |
| DS-08 Frozen classes | ... | ... | ... | ... |

## Top 3 Recommended Actions

1. **[Highest priority smell]** — {specific refactoring action} using {pattern}
   Expected benefit: {what changes become easier once this is addressed}

2. **[Second priority]** — {specific action}
   Expected benefit: {concrete improvement}

3. **[Third priority]** — {specific action}
   Expected benefit: {concrete improvement}

## What NOT to Fix (Pattern Overuse Caution)

{List any detected smells that do not warrant pattern application because the flexibility is not needed, the code is stable, or the cost of introducing indirection exceeds the benefit.}
```

## Key Principles

- **Smells signal future pain, not present failure** — A design smell does not mean the code is broken today. It means that when the inevitable change arrives, this code will resist it. Severity must account for how frequently that change arrives. Dead code with every smell is still lower priority than a hot path with even one moderate smell.

- **Fix the cause of redesign, not the symptom** — Each smell maps to a reason why the system will require redesign. The goal is not to apply patterns everywhere but to remove the specific fragility that the pattern addresses. Always state which redesign risk is being mitigated.

- **Favor composition over inheritance for variation** — Inheritance is a compile-time, white-box relationship. When classes vary along multiple independent dimensions, composition lets each dimension vary independently without class proliferation. Detect this early: subclass names that combine attributes are the clearest signal that inheritance is doing composition's job.

- **Program to interfaces, not implementations** — The consistent thread across all 8 smells is coupling to concrete things: concrete classes, concrete operations, concrete platforms, concrete representations, concrete algorithms. Every pattern recommendation in this skill reduces coupling to concrete things and raises it to abstract interfaces.

- **Do not apply patterns when flexibility is not needed** — Patterns introduce indirection. Indirection adds complexity. The pattern is justified only when the design needs to vary in a specific way. An Abstract Factory for an object that will never change is engineering overhead, not engineering quality. Always evaluate need before recommending.

- **Inheritance depth is a risk multiplier** — Every level of inheritance depth increases the probability that a change in the parent ripples unexpectedly to a descendant. Hierarchies deeper than 3-4 levels should be examined for whether intermediate levels are adding behavior or merely classification names. Classification-only intermediate classes are candidates for removal.

- **Detection evidence must be specific** — A smell report that says "this class might have coupling issues" is useless. A report that says "CustomerService.java imports 12 concrete classes and cannot be instantiated in a unit test without a real database connection" is actionable. Always produce file names, line references, or concrete observations — not impressions.

## Examples

**Scenario: E-commerce codebase pre-refactoring audit**
Trigger: "We're about to add a second payment provider. Before we start, can you review our checkout code for design problems?"
Process: Scanned the checkout directory. DS-01: Found `new StripePaymentGateway()` called in 5 places across CheckoutService, OrderService, and RefundService — Critical. DS-02: Found switch on `paymentMethod` string in PaymentRouter — Warning. DS-06: CheckoutService imports 9 concrete classes including specific gateway, tax calculator, and inventory service — Warning. DS-07: No subclass explosion detected. DS-04: PaymentResult returned as raw HashMap to callers — Advisory. Applied pattern overuse check: flexibility in payment provider is confirmed needed (stated goal), so Abstract Factory recommendation is fully justified.
Output: Report flagging DS-01 as Critical (5 sites, high friction as gateway swap is imminent), recommending Abstract Factory for payment gateway creation with a sketch showing PaymentGatewayFactory interface with StripeGatewayFactory and the new provider's factory as implementations.

**Scenario: UI component library hierarchy review**
Trigger: "We have Button, PrimaryButton, SecondaryButton, DisabledButton, LargeButton, LargePrimaryButton, SmallButton, SmallPrimaryButton... the list keeps growing. Something is wrong."
Process: Mapped the hierarchy. Base: Button (1 class). Dimension 1: Size (Small, Medium, Large). Dimension 2: Variant (Primary, Secondary, Ghost). Dimension 3: State (Default, Disabled, Loading). Current subclass count: 27 and growing multiplicatively. DS-07 detected as Critical. Inheritance encodes combinations of independent dimensions. Adding any new size requires 9 new subclasses; any new state requires 9 new subclasses. Recommended Bridge pattern: separate Button from its rendering variant; use composition (size strategy + variant strategy + state strategy) instead of subclassing each combination. Applied pattern overuse check: combinations do grow (stated), so the flexibility is needed.
Output: Report with hierarchy map showing the combinatorial explosion, Bridge pattern sketch reducing 27 classes to Button + 3 strategy interfaces + concrete strategy implementations.

**Scenario: Targeted single-class review**
Trigger: "I think our ReportGenerator class is badly designed. Can you look at it?"
Process: Read ReportGenerator.java. Found: direct instantiation of PDFWriter (DS-01, isolated), Excel export logic embedded in the class alongside SQL query building (DS-05, isolated), direct file system calls to write output paths (DS-03, isolated), and formatter class imported concretely (DS-06, isolated). All smells are isolated but co-located in one class. Assessed friction: this class is modified every time a new report format or output destination is added — high friction despite low spread. Applied pattern overuse check: format and output destination do vary (confirmed by the user's change pattern), so the flexibility is genuinely needed. Recommended: Strategy for report formatting (isolates Excel/PDF/CSV algorithms), Abstract Factory for output destination (file system vs S3 vs email), Builder for report construction.
Output: Report for a single class showing 4 smells all rated Warning (isolated but high friction), with a refactoring roadmap prioritizing the algorithm extraction first as it affects the most frequent changes.

## References

- For the complete 8-smell detection catalog with grep patterns, code examples in multiple languages, and full pattern mapping tables, see [references/design-smell-catalog.md](references/design-smell-catalog.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
