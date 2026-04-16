---
name: code-smell-diagnosis
description: |
  Scan a codebase or code fragment for the 22 named code smells from Fowler's refactoring catalog and produce a prioritized diagnosis report with the specific refactoring prescription for each smell. Use when: a developer wants to know what is wrong with existing code before touching it; a code review reveals structural problems but no clear fix; a class or method feels wrong but the exact smell is hard to name; a refactoring effort needs a starting point and a prioritized order of attack; a code author wants to justify a refactoring to a team by naming the specific smell and the prescribed remedy. Covers all 22 smells: Duplicated Code, Long Method, Large Class, Long Parameter List, Divergent Change, Shotgun Surgery, Feature Envy, Data Clumps, Primitive Obsession, Switch Statements, Parallel Inheritance Hierarchies, Lazy Class, Speculative Generality, Temporary Field, Message Chains, Middle Man, Inappropriate Intimacy, Alternative Classes with Different Interfaces, Incomplete Library Class, Data Class, Refused Bequest, Comments. Maps each smell to its Fowler-prescribed refactoring(s) including conditional branches (same class vs. sibling subclasses vs. unrelated classes for Duplicated Code; few cases vs. type code vs. null for Switch Statements; etc.).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/refactoring/skills/code-smell-diagnosis
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: refactoring
    title: "Refactoring: Improving the Design of Existing Code"
    authors: ["Martin Fowler", "Kent Beck"]
    chapters: [3]
tags: [refactoring, code-quality, code-smells, software-design]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Source code files or directories to scan for smells — the primary input"
    - type: document
      description: "Code snippet, class description, or pull request diff if no live codebase is accessible"
  tools-required: [Read, Grep, Write]
  tools-optional: [Bash]
  mcps-required: []
  environment: "Run inside a project directory. Reading and grepping source files is the primary analysis method."
discovery:
  goal: "Identify all named code smells present in the target code; map each smell to its prescribed refactoring(s) with correct conditional branching; produce a prioritized findings report the developer can act on immediately"
  tasks:
    - "Read and understand the structure of the target code"
    - "Check each of the 22 smells against the code systematically"
    - "Name each smell using Fowler's exact terminology"
    - "Select the correct refactoring prescription based on the specific context (location, cause, severity)"
    - "Prioritize findings by impact and ease — quick wins first, structural rework last"
    - "Write the diagnosis report with smell name, evidence, prescription, and rationale"
  audience:
    roles: ["software-developer", "senior-developer", "tech-lead", "code-reviewer"]
    experience: "intermediate — assumes working knowledge of object-oriented programming and reading code"
  triggers:
    - "Code feels wrong but the exact problem is hard to name"
    - "Pre-refactoring audit: what should be fixed and in what order"
    - "Code review reveals structural problems without a clear fix"
    - "Inherited codebase needs a quality baseline before feature work begins"
    - "A team needs to justify a refactoring effort with specific named problems"
  not_for:
    - "Performance profiling — use profiling-driven-performance-optimization instead"
    - "Security vulnerability scanning — different concern from structural code quality"
    - "Executing the refactoring transformations themselves — this skill diagnoses; sibling skills execute"
    - "New code that hasn't been written yet — smells appear in existing code"
---

# Code Smell Diagnosis

## When to Use

You have existing source code — a class, a module, a method, or an entire service — and you need to know what is structurally wrong with it before deciding how to improve it.

This skill applies when:
- A developer says "this code is a mess" but cannot name what exactly is wrong
- A code review surfaces problems that need specific names and specific fixes, not just "clean this up"
- A refactoring effort is starting and needs a prioritized list of what to address first
- Code keeps breaking in the same places — a smell is likely attracting bugs
- A pull request adds complexity to already-complex code and needs a targeted intervention

**The core insight from Fowler and Beck:** Refactoring without diagnosis is guesswork. When you can name the smell precisely, the refactoring prescription follows directly. "This is Feature Envy" immediately implies Move Method. "This is a Switch Statement on a type code" immediately implies Replace Type Code with Subclasses or Replace Type Code with State/Strategy followed by Replace Conditional with Polymorphism. The name unlocks the remedy.

**This is the hub skill.** Sibling skills execute specific remedies once a smell is diagnosed:
- `type-code-refactoring-selector` — when Primitive Obsession or Switch Statements are present
- `conditional-simplification-strategy` — when Switch Statements or complex conditionals are present
- `class-responsibility-realignment` — when Feature Envy, Inappropriate Intimacy, or Shotgun Surgery are present
- `big-refactoring-planner` — when multiple smells indicate a systemic design problem
- `data-organization-refactoring` — when Data Clumps, Primitive Obsession, or Data Class are present

---

## Context and Input Gathering

### Required Input (must have — ask if missing)

- **The code to diagnose.** Either a directory path to scan, specific files, a class name, or a pasted code fragment. Why: the diagnosis is grounded in actual code — general impressions are insufficient for naming specific smells and prescribing specific refactorings.
  - If a full codebase: start with the files the user identifies as problematic, or grep for common smell signals (methods > 20 lines, classes > 200 lines, parameter lists > 4 parameters)
  - If a code snippet is provided directly: work from the snippet

- **Language and framework.** Why: smell signals differ by language. Long parameter lists are more prevalent in procedural-style Python than in Java with builder patterns. Switch statements in Java suggest polymorphism; pattern matching in a language with first-class ADTs is different.
  - Check: file extensions, import statements, build files (`pom.xml`, `package.json`, `pyproject.toml`)
  - If unclear, infer from file extensions

### Observable Context (gather before asking)

Scan the environment to orient the diagnosis:

```
Size signals (quick grep targets):
  - Long methods:        functions/methods exceeding 20-30 lines
  - Long parameter lists: functions with 4+ parameters
  - Large classes:       classes exceeding 200 lines or with 10+ instance variables
  - Duplicated code:     identical or near-identical blocks appearing in multiple places
  - Switch/if-elif chains: switch statements or long if/elif chains on the same variable

Structure signals:
  - Classes with only getters/setters and no behavior → Data Class
  - Methods referencing another class's data more than their own class → Feature Envy
  - Subclasses that override many parent methods without using the parent's data → Refused Bequest
  - Long chains like a.getB().getC().getD() → Message Chains
```

### Default Assumptions

- If scope is unclear: start with the files the user directly mentioned, then expand if needed
- If a smell is borderline: flag it as "weak signal" rather than omitting it — the developer decides whether to act
- If the codebase is large: focus on the highest-traffic, most-changed, or most-complained-about areas first

---

## Process

### Step 1: Read and Orient

**ACTION:** Read the target code — structure first, then detail.

**WHY:** Smell detection is pattern recognition, not line-by-line parsing. A structural read (class names, method names, field names, file organization) surfaces most smells before reading any implementation. Diving into implementation first causes you to miss forest-level smells (Large Class, Divergent Change, Shotgun Surgery) while fixating on method-level detail.

Structural questions to answer:
- How many classes/files? How large are they?
- What are the class names and their responsibilities? Do they have a clear single purpose?
- What are the method names? Are they long, numerous, or oddly named?
- What are the fields? Many instance variables? Clusters that appear together?
- What imports/dependencies exist? Does a class depend on many others?

Then read method bodies for the classes flagged as problematic.

---

### Step 2: Check Each of the 22 Smells

**ACTION:** Systematically evaluate each smell against the code. Do not skip smells — the ones you expect to be absent are often the most revealing when present.

**WHY:** Unsystematic diagnosis produces a partial list. Developers naturally notice some smells (long methods, duplication) and miss others (Divergent Change, Speculative Generality, Refused Bequest). Checking all 22 takes 10 minutes and prevents prescribing the wrong refactoring because a deeper smell was missed.

Use the full smell catalog in the reference file (`references/smell-catalog.md`) for detailed detection criteria. The diagnostic decision tree below gives the key signal and the prescribed remedy for each smell:

---

#### Group A: Bloaters — Code That Has Grown Too Large

**1. Duplicated Code**
- Signal: The same code structure appears in more than one place
- Branch by location:
  - Same class, two methods → Extract Method; invoke from both places
  - Sibling subclasses → Extract Method in both; Pull Up Field or Pull Up Method to parent. If code is similar but not identical: Extract Method to separate the similar from different parts, then consider Form Template Method
  - Unrelated classes → Extract Class in one class; use the new component in the other. Or decide the method belongs in only one class and have the other invoke it
  - Same method, different algorithm doing the same thing → Substitute Algorithm (choose the clearer one)

**2. Long Method**
- Signal: Method body exceeds 10-20 lines; comments precede blocks of code; conditionals and loops are nested
- Primary remedy: Extract Method — find clumps of code that go together and give them a name. Do this aggressively; the name is the value, not the line savings
- If extracting creates too many parameters: Replace Temp with Query to eliminate temporaries; Introduce Parameter Object or Preserve Whole Object to slim the parameter list
- If parameter/temp problem persists after those: Replace Method with Method Object — turn the method into its own class
- Conditionals → Decompose Conditional
- Loops → extract the loop and its body into its own method

**3. Large Class**
- Signal: Class has too many instance variables (10+), too many methods (20+), or too many lines (200+); prefixes or suffixes group variables logically
- Common variable groups → Extract Class (e.g., `depositAmount` and `depositCurrency` belong together)
- Subsets of variables not used all the time → Extract Class or Extract Subclass
- Too much code with redundancy → eliminate redundancy first; five 100-line methods with overlap can become five 10-line methods with ten 10-line extracted helpers
- GUI class with behavior → move data and behavior to a domain object; use Duplicate Observed Data to sync if needed
- Identifying use patterns → Extract Interface for each major use cluster; this reveals natural subclass boundaries

**4. Long Parameter List**
- Signal: Method takes 4+ parameters; parameters change frequently as caller needs change
- If a parameter's value can be gotten by making a request of an object the method already knows → Replace Parameter with Method (eliminate the parameter)
- If parameters are a data cluster from an existing object → Preserve Whole Object (pass the object, not its individual fields)
- If parameters have no natural home object → Introduce Parameter Object (create one)
- Exception: when you deliberately do NOT want to create a dependency between the called and calling objects — in those cases, passing parameters explicitly is correct even if the list is long

---

#### Group B: Object-Oriented Abusers — Wrong Use of OO Concepts

**5. Switch Statements**
- Signal: switch/case statement or long if-else-if chain that recurs in multiple places; the same type-code value drives branching throughout the code
- Most cases: consider polymorphism — Extract Method to extract the switch, Move Method to the class with the type code value, then decide:
  - Type code does not affect behavior → Replace Type Code with Class
  - Type code affects behavior and subclassing is possible → Replace Type Code with Subclasses; then Replace Conditional with Polymorphism
  - Type code affects behavior but subclassing is not possible (class already subclassed or type changes at runtime) → Replace Type Code with State/Strategy; then Replace Conditional with Polymorphism
- Switch affects only a single method and type changes are not expected → Replace Parameter with Explicit Methods
- One of the cases is null → Introduce Null Object

**6. Parallel Inheritance Hierarchies** (special case of Shotgun Surgery)
- Signal: Every time you subclass one class, you must also subclass another; the two hierarchies share the same class name prefix
- Remedy: Make instances of one hierarchy refer to instances of the other; use Move Method and Move Field until one hierarchy disappears

**7. Refused Bequest**
- Signal: Subclass inherits methods and data from parent but does not use most of them; subclass overrides the parent's methods and throws exceptions or does nothing
- Weak form (ignoring implementation, supporting interface): usually acceptable — the hierarchy is used for code reuse. Only nine times in ten is this smell faint enough to ignore
- Strong form (subclass refuses to support the superclass interface): Push Down Method and Push Down Field to create a sibling class; let the parent hold only what is genuinely common
- If subclass is reusing behavior but should not be in an is-a relationship → Replace Inheritance with Delegation

**8. Alternative Classes with Different Interfaces**
- Signal: Two classes do the same thing but have different method names for the same operations
- Rename Method to make signatures match; Move Method to bring behavior into alignment; if you have to redundantly move code → Extract Superclass

---

#### Group C: Change Preventers — Code That Makes Change Difficult

**9. Divergent Change**
- Signal: One class is changed in different ways for different reasons — adding a database changes methods A, B, C; adding a financial instrument changes methods D, E, F. The same class absorbs multiple axes of change
- Remedy: Identify everything that changes for a particular cause and Extract Class to put it all together

**10. Shotgun Surgery**
- Signal: One change requires making many small changes in many different classes; a single logical change is scattered across the codebase
- Remedy: Move Method and Move Field to consolidate the behavior into a single class. If no existing class is a good home, create one (Inline Class to bring scattered behavior together)
- Divergent change vs. Shotgun Surgery: Divergent Change = one class, many changes. Shotgun Surgery = one change, many classes. Either way, you want one logical change to map to one class.

---

#### Group D: Couplers — Excessive Coupling Between Classes

**11. Feature Envy**
- Signal: A method seems more interested in another class than the one it belongs to; it calls half a dozen getter methods on another object to calculate some value
- Remedy: Move Method to the class whose data the method uses most
- If only part of the method has envy: Extract Method on the envious part; then Move Method
- Exception: patterns that intentionally violate this rule — Strategy and Visitor are designed to break Feature Envy to enable flexible behavior changes; the fundamental test is which class has the data the behavior needs

**12. Data Clumps**
- Signal: The same 3-4 data items appear together repeatedly — in field lists, parameter lists, and method signatures; deleting one of the items from the group would make the others meaningless
- First step: look for where the clumps appear as fields → Extract Class to turn the clumps into an object
- Then: check method signatures using Introduce Parameter Object or Preserve Whole Object to slim them down
- Test: delete one item from the group — if the others don't make sense without it, you have an object waiting to be born

**13. Message Chains**
- Signal: `a.getB().getC().getD().getValue()` — a client asks one object for another, then asks that object for another, navigating a chain. Any change to the intermediate structure requires changing the client
- Remedy: Hide Delegate — at various points in the chain, introduce a delegation method
- But avoid over-applying: turning every intermediate object into a middle man creates Middle Man smell. Use Extract Method to take a piece of code that uses the chain; then Move Method to push it down the chain closer to the data

**14. Middle Man**
- Signal: A class delegates half or more of its methods to another class; the interface is hollow — it does nothing itself
- If too many methods delegate: Remove Middle Man; talk directly to the object that knows
- If only a few methods delegate: Inline Method to inline the delegation
- If there is additional behavior attached to the delegation: Replace Delegation with Inheritance to make the middle man a subclass of the real object

**15. Inappropriate Intimacy**
- Signal: Two classes know too much about each other's private parts; one class accesses another's private fields directly or depends heavily on its internal implementation
- Remedy: Move Method and Move Field to separate the pieces and reduce intimacy
- If a bidirectional association exists: Change Bidirectional Association to Unidirectional
- If common interests exist: Extract Class to put the common behavior in a safe shared place; use Hide Delegate to let another class act as go-between
- Inheritance overintimacy: if a subclass knows more about its parent than appropriate → Replace Delegation with Inheritance

**16. Incomplete Library Class**
- Signal: A library class doesn't do exactly what you need; you can't modify it (it's not your code); the workaround is scattered through your code
- A few missing methods: Introduce Foreign Method — add the needed method to your own class; document that it belongs conceptually to the library class
- Lots of extra behavior needed: Introduce Local Extension — create a subclass or wrapper of the library class with all the needed additions

---

#### Group E: Dispensables — Unnecessary Code That Should Not Exist

**17. Lazy Class**
- Signal: A class that isn't doing enough to justify its existence — it was added speculatively, was refactored down to almost nothing, or is a subclass that barely differs from its parent
- Subclasses not doing enough → Collapse Hierarchy
- Nearly useless components → Inline Class

**18. Speculative Generality**
- Signal: Abstract classes, hooks, special cases, and parameters added for future use that no current code actually exercises; the only callers are test cases
- Abstract classes not doing much → Collapse Hierarchy
- Unnecessary delegation → Inline Class
- Methods with unused parameters → Remove Parameter
- Methods with odd abstract names → Rename Method
- Detection: if the only users of a method or class are test cases, delete it and the test case that exercises it (but keep it if it tests functionality that is legitimately exercised by real code through a test)

**19. Temporary Field**
- Signal: An instance variable is set only in certain circumstances — it's only valid during some algorithms and is otherwise empty or null; understanding why it's there when it seems unused is confusing
- Remedy: Extract Class to create a home for the orphan variables; put all the code that concerns those variables into the new class
- Use Introduce Null Object to create an alternative component for when the variables aren't valid
- Common pattern: a complicated algorithm that needs several fields but only during computation → those fields belong in a Method Object, not in the host class

---

#### Group F: Comments — A Diagnostic Signal, Not a Smell Itself

**20. Comments** (used as deodorant)
- Signal: Comments that explain what a block of code does (not why); comments that compensate for confusing code; thickly commented code that would be unnecessary if the code were clearer
- Comments are not a smell themselves — they can be a sweet smell. The signal is comments used as deodorant to mask other smells
- If a comment explains what a block does → Extract Method; name the method after what the comment says
- If the method is extracted but still needs a comment to explain what it does → Rename Method
- If you need to state rules about required system state → Introduce Assertion
- Appropriate comments: explaining why something is done, noting uncertainty, documenting constraints that cannot be expressed in code

**The remaining two smells appear in object hierarchy design:**

**21. Data Class**
- Signal: A class with fields, getters, and setters — and nothing else. It exists only as a data holder; other classes manipulate it in far too much detail
- Public fields → Encapsulate Field immediately; check collection fields → Encapsulate Collection
- Fields that should not change → Remove Setting Method
- Find where getters and setters are used → Move Method to move behavior into the Data Class
- If you can't move a whole method → Extract Method; then Move Method
- Goal: the Data Class should take on responsibility rather than just being manipulated

**22. Refused Bequest** — covered under Group B (Object-Oriented Abusers) above.

---

### Step 3: Prioritize Findings

**ACTION:** Rank all identified smells for the diagnosis report.

**WHY:** Not all smells are equal. Treating a cosmetic smell (Lazy Class) with the same urgency as a change-blocking smell (Shotgun Surgery) wastes time and de-prioritizes what matters. Prioritization makes the report actionable — the developer knows where to start.

**Prioritization criteria (apply in order):**

1. **Change preventers first** (Divergent Change, Shotgun Surgery, Parallel Inheritance Hierarchies) — these make every future feature harder. Fix them before adding new behavior.
2. **Couplers second** (Feature Envy, Inappropriate Intimacy, Message Chains, Middle Man) — high coupling spreads bugs. Fixing coupling makes subsequent refactorings easier.
3. **Bloaters third, starting with the most impactful** — Long Method and Large Class are the most common bug attractors. Long Parameter List follows.
4. **OO abusers** (Switch Statements, Refused Bequest) — significant structural investment but high payoff.
5. **Dispensables last** (Lazy Class, Speculative Generality, Temporary Field) — these are cleanup; do them after the structural work.

**Severity tiers for the report:**
- **HIGH** — the smell is actively making the code fragile, bug-prone, or difficult to change; address before the next feature
- **MEDIUM** — the smell is a real problem but not immediately blocking; address in the current cleanup cycle
- **LOW** — weak signal or borderline; flag for awareness; no immediate action required

---

### Step 4: Write the Diagnosis Report

**ACTION:** Produce the structured diagnosis report as the skill's deliverable.

**WHY:** The report is what the developer acts on. It must be specific enough to be actionable (naming the exact smell and the exact refactoring) and organized enough to be usable as a task list or review checklist. Vague reports ("this code needs work") produce no change. Named smells with prescribed remedies produce refactoring plans.

**Output format:**

```markdown
# Code Smell Diagnosis — [Target: class/module/directory name]

## Summary

Files scanned:    [count]
Smells found:     [N total — X HIGH, Y MEDIUM, Z LOW]
Primary cluster:  [the dominant smell group — e.g., "Change Preventers + Bloaters"]

---

## Priority Findings

### Finding #N — [Smell Name] — [HIGH | MEDIUM | LOW]

**Location:** [file:line or class/method name]
**Evidence:** [what in the code signals this smell — be specific]
**Prescription:** [the Fowler-prescribed refactoring(s)]
**Why this prescription:** [the specific conditional branch that applies — e.g., "duplication is in sibling subclasses, not the same class, so Pull Up Method rather than just Extract Method"]
**Next step:** [the single first action to take]

---

[repeat per finding]

---

## Refactoring Sequence

[Ordered list of the prescribed refactorings in the recommended sequence.
Change preventers first. Dependencies between refactorings noted.]

## Related Skills

[Which sibling skills to invoke for execution]
```

---

## Key Principles

**1. Name the smell before prescribing the remedy.**
A generic prescription ("extract this into a method") without naming the smell misses the diagnostic value. The smell name carries the full decision tree with it. "Feature Envy" tells a developer exactly what class the method belongs in. "Switch Statement on a type code" tells them exactly which three refactorings to apply in sequence.

**2. Follow the conditional branches precisely.**
Most smells have context-dependent prescriptions. Duplicated Code in the same class has a different remedy than Duplicated Code in sibling subclasses. Switch Statements affecting a single method have a different remedy than Switch Statements scattered across the codebase. Getting the branch wrong produces the wrong refactoring.

**3. One smell often hides another.**
Data Clumps often reveal Feature Envy once turned into objects. Long Method is often Divergent Change in disguise. Shotgun Surgery is often caused by a missing class that Data Clumps would reveal. When you name one smell, check whether it points to a deeper one.

**4. Smells are not rules — they are signals.**
Fowler and Beck explicitly decline to give precise metrics. A 25-line method might be fine; a 10-line method might reek. The judgment is: does this code make the next change harder? Does it attract bugs? Is it difficult to understand? The smell is an indicator, not a verdict.

**5. Comments are a diagnostic tool, not a finding.**
Heavy commenting often signals other smells. Use comments as a guide to where Extract Method and Rename Method are needed — the smell is what the comment is masking, not the comment itself.

---

## Examples

### Example 1: Service Class Audit

**Scenario:** A developer inherits a `PaymentService` class (280 lines, 12 methods, 9 instance variables) and asks for a diagnosis before adding a new payment gateway.

**Step 1 — Structural read:**
- 280 lines, 12 methods: candidate for Large Class
- 9 instance variables: some look like they form clusters (`gatewayUrl`, `gatewayApiKey`, `gatewayTimeout` → Data Clumps candidate)
- Method names: `processPayment`, `validateCard`, `logTransaction`, `formatCurrency`, `sendWebhook`, `retryWebhook`, `buildGatewayRequest`, `parseGatewayResponse` — some methods clearly work on gateway concerns, others on local concerns

**Step 2 — Smell check (selected findings):**

*Divergent Change (HIGH):* The class changes when the gateway changes (3 methods: `buildGatewayRequest`, `parseGatewayResponse`, `processPayment`) AND when the webhook logic changes (2 methods: `sendWebhook`, `retryWebhook`) AND when logging changes (1 method: `logTransaction`). Three axes of change in one class.

*Data Clumps (MEDIUM):* `gatewayUrl`, `gatewayApiKey`, `gatewayTimeout` appear together in every gateway-related method signature. Deleting `gatewayUrl` makes the others meaningless.

*Long Method (MEDIUM):* `processPayment` is 55 lines with embedded comments marking sections ("// validate", "// build request", "// process", "// log").

**Step 3 — Prioritize:** Divergent Change first (it's a change preventer). Data Clumps second (will simplify gateway extraction). Long Method third (the extracted sections will become methods in the new class).

**Diagnosis report excerpt:**

```markdown
### Finding #1 — Divergent Change — HIGH

Location: PaymentService (entire class)
Evidence: The class changes for at least three distinct reasons:
  (1) Gateway integration changes → buildGatewayRequest, parseGatewayResponse, processPayment
  (2) Webhook delivery changes → sendWebhook, retryWebhook
  (3) Logging changes → logTransaction
Prescription: Extract Class for each axis of change.
  - Extract GatewayClient (gateway request/response)
  - Extract WebhookDispatcher (send + retry logic)
  - PaymentService retains orchestration only
Why this prescription: Divergent Change calls for Extract Class on each axis.
  The test: "I have to change these N methods every time X happens."
  Three different values of X = three different classes needed.
Next step: Extract GatewayClient first — it's the largest axis and will expose
  the Data Clumps smell for remedy.
```

---

### Example 2: Single Method Diagnosis

**Scenario:** A code reviewer asks what's wrong with this Python method:

```python
def calculate_charge(customer_type, base_price, quantity, discount_code,
                     loyalty_years, is_weekend, tax_rate):
    if customer_type == 'enterprise':
        price = base_price * quantity * 0.85
    elif customer_type == 'retail':
        price = base_price * quantity
    elif customer_type == 'wholesale':
        price = base_price * quantity * 0.7
    else:
        price = base_price * quantity

    if discount_code == 'SUMMER10':
        price *= 0.90
    elif discount_code == 'VIP20':
        price *= 0.80

    if loyalty_years > 5:
        price *= 0.95

    if is_weekend:
        price *= 1.05

    return price * (1 + tax_rate)
```

**Step 2 — Smell check:**

*Long Parameter List (HIGH):* 7 parameters. Why this branch: there is no obvious existing object that holds these — `customer_type`, `loyalty_years` suggest a Customer object; `base_price`, `quantity`, `discount_code` suggest an Order. Two Introduce Parameter Object applications.

*Switch Statements (HIGH):* The `customer_type` branching recurs — any new customer type requires finding every switch on `customer_type` and adding a case. Why this branch: type code affects behavior, and customer type is unlikely to change at runtime → Replace Type Code with Subclasses on Customer, then Replace Conditional with Polymorphism for the pricing logic.

**Diagnosis report excerpt:**

```markdown
### Finding #1 — Switch Statements — HIGH

Location: calculate_charge(), lines 2-9 (customer_type branching)
Evidence: A switch on customer_type determines pricing multiplier.
  This switch will exist wherever customer pricing is computed.
  Every new customer type requires finding every such switch.
Prescription: Replace Type Code with Subclasses (EnterpriseCustomer,
  RetailCustomer, WholesaleCustomer); then Replace Conditional with
  Polymorphism (each subclass implements its own price multiplier method).
Why this branch: type code affects behavior; customer type doesn't change
  at runtime for a given customer → subclassing is appropriate.
  (If type changed at runtime, use Replace Type Code with State/Strategy instead.)
Next step: Introduce Parameter Object first (Finding #2) to create a
  Customer object; then apply type code replacement on that object.

### Finding #2 — Long Parameter List — HIGH

Location: calculate_charge() signature (7 parameters)
Evidence: customer_type, loyalty_years → Customer data cluster.
  base_price, quantity, discount_code → Order data cluster.
  Deleting customer_type makes loyalty_years ambiguous without context.
Prescription: Introduce Parameter Object twice — Customer(customer_type,
  loyalty_years) and Order(base_price, quantity, discount_code).
  Then: Preserve Whole Object — pass Customer and Order, not their fields.
Next step: Define Customer and Order dataclasses; update the signature.
  This unblocks the Switch Statement refactoring (Finding #1).

Refactoring sequence:
  1. Introduce Parameter Object: Customer, Order
  2. Replace Type Code with Subclasses on Customer
  3. Replace Conditional with Polymorphism for pricing
  4. Preserve Whole Object in calculate_charge signature
```

---

### Example 3: Inheritance Hierarchy Diagnosis

**Scenario:** A codebase has `Animal`, `Dog`, `Cat`, `Bird` hierarchy. A developer notices that every time a new animal species is added, a parallel set of `AnimalSound`, `DogSound`, `CatSound`, `BirdSound` classes must also be added.

**Step 2 — Smell check:**

*Parallel Inheritance Hierarchies (HIGH):* Subclassing `Animal` always requires subclassing `AnimalSound`. The prefix pattern is exact (Dog/DogSound, Cat/CatSound).

*Prescription:* Make instances of one hierarchy refer to instances of the other (Strategy pattern). Move Method and Move Field from `AnimalSound` hierarchy into `Animal` hierarchy using a sound strategy object. Once all behavior is moved, the `AnimalSound` hierarchy disappears.

---

## References

| File | Contents | When to read |
|------|----------|--------------|
| `references/smell-catalog.md` | Full detection criteria for all 22 smells with code examples per language; borderline cases; false positive filters | Step 2 — systematic smell check |
| `references/refactoring-prescriptions.md` | Full prescription tree per smell with all conditional branches; cross-references to Fowler catalog chapters | Step 2 — selecting the correct refactoring |

**Hub skill relationships:**
- `type-code-refactoring-selector` — when Switch Statements or Primitive Obsession (type code variant) are diagnosed
- `conditional-simplification-strategy` — when Switch Statements or deeply nested conditionals are present
- `class-responsibility-realignment` — when Feature Envy, Inappropriate Intimacy, Divergent Change, or Shotgun Surgery are the primary findings
- `big-refactoring-planner` — when the diagnosis reveals systemic design problems requiring coordinated multi-step refactoring
- `data-organization-refactoring` — when Data Clumps, Primitive Obsession, or Data Class are primary findings

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Refactoring: Improving the Design of Existing Code by Martin Fowler and Kent Beck.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-type-code-refactoring-selector`
- `clawhub install bookforge-conditional-simplification-strategy`
- `clawhub install bookforge-class-responsibility-realignment`
- `clawhub install bookforge-big-refactoring-planner`
- `clawhub install bookforge-data-organization-refactoring`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
