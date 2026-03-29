# Design Smell Catalog — OO Design Smell Detector

Complete detection reference for all 8 design smells. Each entry includes: definition, detection criteria, language-specific grep patterns, code examples showing the smell and the fix, severity calibration guidance, and pattern mapping.

Source: "Design Patterns: Elements of Reusable Object-Oriented Software" (Gamma, Helm, Johnson, Vlissides), Chapter 1, pages 34-36 (8 causes of redesign), pages 29-31 (inheritance vs composition).

---

## DS-01: Hardcoded Object Creation

### Definition
Object creation is coupled to a specific concrete class at the call site. Code that creates objects by naming a concrete class at instantiation commits to that implementation — changing the implementation requires changing every creation site.

### Why It Causes Redesign
When a new variant of the created object is needed (e.g., a mock for testing, a different database implementation, a platform-specific adapter), every call site must be updated. Systems with many creation sites cannot swap implementations without a large, risky multi-file edit.

### Detection Criteria
- `new ConcreteClass()` used outside a factory or builder class
- Variable declared as a concrete type: `StripeGateway gateway = new StripeGateway()` instead of `PaymentGateway gateway = ...`
- Constructor calls where the class name encodes a specific implementation choice (database vendor, external service, specific algorithm)

### Grep Patterns

**Java / Kotlin:**
```
grep -rn "= new [A-Z][a-zA-Z]*(" src/
grep -rn "new [A-Z][a-zA-Z]*Repository(" src/
grep -rn "new [A-Z][a-zA-Z]*Service(" src/
```

**Python:**
```
grep -rn "[a-z_]\+ = [A-Z][a-zA-Z]*(" src/
# Look for instantiation without a factory function
```

**TypeScript / JavaScript:**
```
grep -rn "= new [A-Z][a-zA-Z]*(" src/
```

**C#:**
```
grep -rn "= new [A-Z][a-zA-Z]*(" src/
```

### False Positive Filters
- Creation inside a class named `*Factory`, `*Builder`, `*Provider`, `*Creator` — these are intended creation sites
- Creation of value objects (String, Integer, simple DTOs) — these rarely need to vary
- Test setup code — concrete instantiation in tests is expected

### Code Example: Smell

```java
// Java — hardcoded creation scattered across service layer
public class OrderService {
    public void processOrder(Order order) {
        PaymentResult result = new StripePaymentGateway().charge(order.getTotal());
        // ^ commits to Stripe everywhere this method is called
        new SQLOrderRepository().save(order);
        // ^ commits to SQL everywhere
    }
}
```

### Code Example: Fixed (Factory Method)

```java
// Java — creation delegated to factory
public class OrderService {
    private final PaymentGateway gateway;       // interface type
    private final OrderRepository repository;  // interface type

    public OrderService(PaymentGateway gateway, OrderRepository repository) {
        this.gateway = gateway;
        this.repository = repository;
    }
    // Concrete classes chosen once at configuration time, not scattered at use sites
}
```

### Severity Calibration
- **Advisory:** 1-2 creation sites for an implementation that is unlikely to change
- **Warning:** 3-10 creation sites, or any creation site for an external dependency (database, payment, notification)
- **Critical:** 10+ creation sites, or if a change to the created class is already planned/needed

### Applicable Patterns
| Pattern | When to use |
|---------|-------------|
| **Abstract Factory** | Creating families of related objects (e.g., UI widgets for a platform, persistence objects for a database vendor) |
| **Factory Method** | Subclasses should decide which class to instantiate (e.g., a framework that lets users plug in their own creator) |
| **Prototype** | When the class to instantiate is specified at runtime (clone a prototype rather than naming a class) |

---

## DS-02: Operation Dependencies

### Definition
Code explicitly encodes which operations to perform using conditionals on operation type. Instead of dispatching requests polymorphically, the code names specific operations in if/switch branches.

### Why It Causes Redesign
Every new operation requires modifying the dispatch logic. There is a central point of knowledge about all possible operations, which becomes a change magnet. Operations cannot be reordered, added, or removed without editing the dispatcher.

### Detection Criteria
- Switch statements on an operation type, action name, command string, or event type
- Long if/else-if chains where each branch calls a different operation
- String-based dispatch: `if (action.equals("save")) ... else if (action.equals("delete")) ...`
- Integer/enum-based dispatch where the enum represents what to do (not what state to be in)

### Grep Patterns

**Java:**
```
grep -rn "switch.*action\|switch.*command\|switch.*event\|switch.*operation" src/
grep -rn "\.equals(\"save\")\|\.equals(\"delete\")\|\.equals(\"update\")" src/
```

**Python:**
```
grep -rn "if action ==\|elif action ==" src/
grep -rn "if command ==\|elif command ==" src/
```

**TypeScript:**
```
grep -rn "switch.*action\|switch.*type\|switch.*event" src/
grep -rn "case 'save'\|case 'delete'\|case 'update'" src/
```

### Code Example: Smell

```java
// Java — operation hardcoded as string dispatch
public class RequestHandler {
    public void handle(String action, Request request) {
        if (action.equals("save")) {
            saveRecord(request);
        } else if (action.equals("delete")) {
            deleteRecord(request);
        } else if (action.equals("validate")) {
            validateRecord(request);
        }
        // Adding "export" requires editing this class
    }
}
```

### Code Example: Fixed (Command)

```java
// Java — operations as objects
public interface Command {
    void execute(Request request);
}

public class SaveCommand implements Command { ... }
public class DeleteCommand implements Command { ... }

public class RequestHandler {
    private final Map<String, Command> commands;

    public void handle(String action, Request request) {
        Command command = commands.get(action);
        if (command != null) command.execute(request);
        // Adding "export" = register a new ExportCommand. No change here.
    }
}
```

### Severity Calibration
- **Advisory:** Switch on a stable, closed set of operations that will not grow
- **Warning:** Switch with 5+ cases, or cases that represent extensible operations
- **Critical:** Central dispatcher that all request handling flows through, with operations actively being added

### Applicable Patterns
| Pattern | When to use |
|---------|-------------|
| **Command** | Turn operations into first-class objects for queuing, undoing, logging, or dynamic registration |
| **Chain of Responsibility** | Operations should be tried in sequence until one handles the request; handlers don't need to know about each other |

---

## DS-03: Platform and Hardware Coupling

### Definition
Business logic classes contain direct references to platform-specific APIs: operating system interfaces, specific database drivers, file system calls, hardware APIs, or external service SDKs embedded in domain code.

### Why It Causes Redesign
Platform changes — cloud migrations, OS upgrades, switching ORMs, moving from local storage to S3 — require rewriting classes whose real job is not platform management. Platform-coupled code also resists testing: you cannot run unit tests without the real platform available.

### Detection Criteria
- Domain or service classes importing platform-specific packages (`java.io.File`, `os.path`, `System.IO`)
- Direct JDBC/SQL calls in domain classes (not in repository classes)
- OS-specific constructs: path separators, environment variable access, process spawning
- External service SDK calls (`stripe.charge()`, `s3.putObject()`) in classes whose primary responsibility is business logic

### Grep Patterns

**Java:**
```
grep -rn "import java.io\.\|import java.nio\." src/main/  # in non-IO classes
grep -rn "import com.mysql\.\|import org.postgresql\." src/domain/
grep -rn "System.getenv\|Runtime.getRuntime" src/domain/
```

**Python:**
```
grep -rn "import os\|import subprocess\|import sys" src/domain/
grep -rn "open(\|os.path\." src/domain/
```

**TypeScript / Node.js:**
```
grep -rn "require('fs')\|require('os')\|require('path')" src/domain/
grep -rn "import.*from 'fs'" src/domain/
```

### Code Example: Smell

```python
# Python — file system hardcoded in domain class
class ReportGenerator:
    def generate(self, report_data):
        result = self._build_report(report_data)
        with open(f"/tmp/reports/{report_data.id}.pdf", "wb") as f:
            f.write(result)
        # Cannot test without a real file system; cannot switch to S3 without changing this class
```

### Code Example: Fixed (Abstract Factory / Bridge)

```python
# Python — output destination abstracted
class ReportGenerator:
    def __init__(self, output_store: OutputStore):  # interface, not concrete
        self.output_store = output_store

    def generate(self, report_data):
        result = self._build_report(report_data)
        self.output_store.write(report_data.id, result)
        # FileOutputStore, S3OutputStore, InMemoryOutputStore (for tests) all work
```

### Severity Calibration
- **Advisory:** Platform calls in a dedicated infrastructure/adapter class (may be acceptable)
- **Warning:** Platform calls in a service class that has non-platform responsibilities
- **Critical:** Platform calls directly in domain model or business logic classes

### Applicable Patterns
| Pattern | When to use |
|---------|-------------|
| **Abstract Factory** | The platform difference involves families of related objects (UI widgets, persistence layer, messaging) |
| **Bridge** | The abstraction and implementation vary independently along separate dimensions |

---

## DS-04: Representation and Implementation Leaks

### Definition
A class exposes its internal data structure, concrete type, or implementation details to clients. Clients make decisions based on how the object is represented, not what it can do.

### Why It Causes Redesign
Any change to the internal representation requires changing every client that knows about it. This is how `ArrayList` to `LinkedList` migrations become 20-file changes. It is also how schema migrations break the entire application instead of staying in the persistence layer.

### Detection Criteria
- Public fields (non-final, non-constant) on domain objects
- Methods that return raw collection references (`List<Item>` returned directly, not a copy or unmodifiable view)
- Clients using `instanceof` to branch behavior based on concrete type
- Getter methods that expose internal implementation details (returning a connection object, an internal cache, a raw byte array)
- Clients knowing the concrete class behind an interface (e.g., casting an interface to its implementation)

### Grep Patterns

**Java:**
```
grep -rn "public [A-Za-z<>]* [a-z]" src/domain/  # public fields
grep -rn "instanceof [A-Z]" src/  # type-checking callers
grep -rn "return [a-z]*List\b\|return [a-z]*Map\b" src/  # returning internal collections
```

**TypeScript:**
```
grep -rn "public [a-z]" src/domain/  # public properties
grep -rn "instanceof [A-Z]" src/
```

### Code Example: Smell

```java
// Java — internal List exposed directly
public class ShoppingCart {
    public List<Item> items = new ArrayList<>();  // public field — clients can mutate internals
    // OR:
    public List<Item> getItems() {
        return items;  // returns live reference — external code can clear the list
    }
}

// Client — depends on ArrayList-ness
((ArrayList<Item>) cart.getItems()).trimToSize();  // casts to concrete type
```

### Code Example: Fixed

```java
// Java — representation hidden, behavior exposed
public class ShoppingCart {
    private List<Item> items = new ArrayList<>();

    public void addItem(Item item) { items.add(item); }
    public void removeItem(Item item) { items.remove(item); }
    public List<Item> getItems() { return Collections.unmodifiableList(items); }
    public int getItemCount() { return items.size(); }
    // Switching to LinkedList requires no client changes
}
```

### Severity Calibration
- **Advisory:** Representation leaks in internal utility classes not exposed across module boundaries
- **Warning:** Public fields or raw collection returns in domain objects
- **Critical:** Clients using `instanceof` or casting to concrete types — this breaks the moment the implementation changes

### Applicable Patterns
| Pattern | When to use |
|---------|-------------|
| **Abstract Factory** | Hide which concrete family of objects is in use |
| **Bridge** | Separate the interface from its implementation so each can vary independently |
| **Memento** | Expose object state through a controlled, opaque token rather than direct field access |
| **Proxy** | Control and mediate access to the underlying object |

---

## DS-05: Algorithmic Dependencies

### Definition
Algorithms are embedded inside classes whose primary responsibility is data or domain logic — not algorithm management. The class cannot change data structure without changing the algorithm, and the algorithm cannot be replaced without changing the class.

### Why It Causes Redesign
Algorithms are among the most frequently replaced things in software: sorting strategies change for performance, serialization formats change for compatibility, encryption algorithms change for security. When an algorithm is embedded in a class, any algorithm change requires modifying the class — even if the class's job has nothing to do with the algorithm.

### Detection Criteria
- Sort routines inside entity or model classes
- Serialization/deserialization logic in domain classes (not in serializer classes)
- Encryption, hashing, or compression routines in service classes with other responsibilities
- Data transformation logic (mapping, filtering, aggregating) duplicated across multiple classes
- Template methods that mix structural logic with variable algorithms in the same class

### Grep Patterns

**Java:**
```
grep -rn "\.sort(\|Collections.sort\|Comparator" src/domain/  # sorting in domain
grep -rn "serialize\|deserialize\|toJson\|fromJson\|marshal\|unmarshal" src/domain/
grep -rn "encrypt\|decrypt\|hash\|compress" src/service/  # look for mixed responsibilities
```

**Python:**
```
grep -rn "sorted(\|\.sort(\|json.dumps\|json.loads\|pickle" src/domain/
grep -rn "hashlib\|hmac\|cryptography" src/domain/
```

### Code Example: Smell

```python
# Python — sorting algorithm embedded in domain class
class ProductCatalog:
    def __init__(self, products):
        self.products = products

    def get_products(self):
        # Bubble sort hardcoded — changing algorithm requires changing this class
        items = self.products[:]
        for i in range(len(items)):
            for j in range(len(items) - 1 - i):
                if items[j].price > items[j+1].price:
                    items[j], items[j+1] = items[j+1], items[j]
        return items
```

### Code Example: Fixed (Strategy)

```python
# Python — sorting strategy injected
from abc import ABC, abstractmethod

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, items): ...

class PriceSortStrategy(SortStrategy):
    def sort(self, items):
        return sorted(items, key=lambda x: x.price)

class PopularitySortStrategy(SortStrategy):
    def sort(self, items):
        return sorted(items, key=lambda x: x.view_count, reverse=True)

class ProductCatalog:
    def __init__(self, products, sort_strategy: SortStrategy):
        self.products = products
        self.sort_strategy = sort_strategy

    def get_products(self):
        return self.sort_strategy.sort(self.products)
        # Changing the sort = swap the strategy, no change to ProductCatalog
```

### Severity Calibration
- **Advisory:** Algorithm embedded but the algorithm is fixed by the problem domain and will never change
- **Warning:** Algorithm embedded and has changed at least once, or is known to be implementation-specific
- **Critical:** Algorithm duplicated across multiple classes — any change must be made in multiple places

### Applicable Patterns
| Pattern | When to use |
|---------|-------------|
| **Strategy** | Choose an algorithm at runtime from a family of interchangeable algorithms |
| **Template Method** | Define the skeleton of an algorithm in a base class; let subclasses override specific steps |
| **Builder** | Construct complex objects step-by-step; separate construction algorithm from the representation |
| **Iterator** | Abstract iteration algorithm from the collection being iterated |
| **Visitor** | Add new operations to a class hierarchy without changing the classes |

---

## DS-06: Tight Coupling

### Definition
Classes depend directly on many other concrete classes, making it impossible to change, test, or reuse any class in isolation. Tightly coupled systems are monolithic in practice even if they appear modular in structure.

### Why It Causes Redesign
A class that imports 12 concrete collaborators cannot be unit-tested without instantiating all 12. Changing any one of the 12 may require changing the dependent. When coupling is bidirectional, the system becomes a dense graph where changes propagate unpredictably. GoF: "The system becomes a dense mass that's hard to learn, port, and maintain."

### Detection Criteria
- High import count (10+ concrete class imports in a single class)
- Classes that cannot be instantiated without setting up a full object graph
- Bidirectional dependencies (A imports B, B imports B)
- Concrete type references in method signatures (parameter types or return types are concrete classes, not interfaces)
- No use of dependency injection — all collaborators instantiated internally

### Grep Patterns

**Java:**
```
# Count imports per file — high counts (10+) warrant inspection
grep -c "^import" src/service/OrderService.java

# Find bidirectional dependencies
grep -rn "import com.example.serviceA" src/service/ServiceB.java
grep -rn "import com.example.serviceB" src/service/ServiceA.java
```

**Python:**
```
# Count imports
grep -c "^from\|^import" src/service/order_service.py

# Find non-interface dependencies
grep -rn "from services\." src/domain/
```

**Manual check:** Can this class be instantiated in a unit test without a database, network, or file system?

### Code Example: Smell

```java
// Java — tightly coupled service
public class OrderService {
    private StripePaymentGateway stripeGateway = new StripePaymentGateway();    // concrete
    private MySQLOrderRepository mysqlRepository = new MySQLOrderRepository();  // concrete
    private TwilioNotificationService twilioService = new TwilioNotificationService();  // concrete
    private PDFReportGenerator pdfGenerator = new PDFReportGenerator();  // concrete
    // Unit test requires Stripe, MySQL, Twilio, and PDF generation
}
```

### Code Example: Fixed (Dependency Injection + Interfaces)

```java
// Java — loosely coupled service
public class OrderService {
    private final PaymentGateway gateway;           // interface
    private final OrderRepository repository;       // interface
    private final NotificationService notifications; // interface
    private final ReportGenerator reports;           // interface

    public OrderService(PaymentGateway gateway, OrderRepository repository,
                        NotificationService notifications, ReportGenerator reports) {
        this.gateway = gateway;
        this.repository = repository;
        this.notifications = notifications;
        this.reports = reports;
    }
    // Unit test: inject mocks for all four interfaces — no real dependencies needed
}
```

### Severity Calibration
- **Advisory:** High import count but imports are all stable library types (collections, utils)
- **Warning:** Concrete imports of domain or infrastructure classes; any bidirectional dependency
- **Critical:** Bidirectional dependencies between core services; class cannot be tested without full infrastructure

### Applicable Patterns
| Pattern | When to use |
|---------|-------------|
| **Abstract Factory** | Decouple clients from concrete collaborator families |
| **Bridge** | Decouple an abstraction from its implementation |
| **Chain of Responsibility** | Decouple request senders from handlers |
| **Command** | Decouple operation invokers from operation implementors |
| **Facade** | Provide a simple interface to a complex, tightly coupled subsystem |
| **Mediator** | Centralize complex interactions between objects so they don't reference each other directly |
| **Observer** | Decouple subjects from observers — subjects don't know who is listening |

---

## DS-07: Subclass Explosion (Inheritance Overuse)

### Definition
Class hierarchies grow into an unmanageable number of subclasses because inheritance is used to encode combinations of independent variations. Each new variation along any dimension multiplies the number of subclasses required.

### Why It Causes Redesign
GoF (p. 36): "Customizing an object by subclassing often isn't easy. Every new class has a fixed implementation overhead. Subclassing can lead to an explosion of classes, because you might have to introduce many new subclasses for even a simple extension."

If a hierarchy varies along N independent dimensions, subclass count grows as the product of those dimensions. Adding a new dimension doubles (or multiplies) the hierarchy. This is unsustainable.

Also relevant (p. 30-31): "Designers overuse inheritance as a reuse technique, and designs are often made more reusable (and simpler) by depending more on object composition." Composition provides the same reuse without the class-count cost, and it allows variation at runtime rather than compile time.

### Detection Criteria
- More than 7 direct subclasses of a single base class
- Subclass names that encode combinations: `{Dimension1}{Dimension2}{BaseName}` (e.g., `LargeRedButton`, `SmallBlueButton`)
- Inheritance depth greater than 4 levels
- Abstract intermediate classes that add only naming, not behavior
- Hierarchies where adding a new "color" requires adding one new class per "shape"

### Grep Patterns

**Java:**
```
# Find all classes that extend a specific base
grep -rn "extends Button\|extends Widget\|extends Shape" src/
# Count subclasses per base class
grep -rh "extends [A-Z][a-zA-Z]*" src/ | sort | uniq -c | sort -rn | head -20
```

**Python:**
```
grep -rn "class [A-Z][a-zA-Z]*(Button)\|class [A-Z][a-zA-Z]*(Widget)" src/
```

**TypeScript:**
```
grep -rn "extends [A-Z][a-zA-Z]*" src/ | awk '{print $NF}' | sort | uniq -c | sort -rn
```

### Dimension Analysis
When subclass explosion is detected, identify the independent dimensions:

1. List all subclass names
2. Extract adjectives/modifiers (Large, Small, Red, Blue, Disabled, Loading)
3. Group modifiers by type (size group: Large/Small/Medium; color group: Red/Blue/Green; state group: Default/Disabled/Loading)
4. Count dimensions and their cardinalities
5. Current subclass count ≈ cardinality(dim1) × cardinality(dim2) × ... × cardinality(dimN)

**Example:** 27 Button subclasses = 3 sizes × 3 variants × 3 states. Adding a 4th state requires 9 new classes with inheritance, vs 1 new state implementation with composition.

### Code Example: Smell

```typescript
// TypeScript — 9 classes for 3x3 combination
class Button {}
class PrimaryButton extends Button {}
class SecondaryButton extends Button {}
class GhostButton extends Button {}
class LargeButton extends Button {}
class LargePrimaryButton extends LargeButton {}    // combining dimensions
class LargeSecondaryButton extends LargeButton {}
class SmallButton extends Button {}
class SmallPrimaryButton extends SmallButton {}
class SmallSecondaryButton extends SmallButton {}
// Adding "Disabled" state: 9 more classes. Adding "XL" size: 3 more classes.
```

### Code Example: Fixed (Bridge + Strategy composition)

```typescript
// TypeScript — dimensions composed, not subclassed
interface ButtonVariant { getStyles(): VariantStyles; }
interface ButtonSize { getDimensions(): SizeMetrics; }

class PrimaryVariant implements ButtonVariant { ... }
class SecondaryVariant implements ButtonVariant { ... }
class GhostVariant implements ButtonVariant { ... }

class LargeSize implements ButtonSize { ... }
class SmallSize implements ButtonSize { ... }

class Button {
    constructor(
        private variant: ButtonVariant,
        private size: ButtonSize,
        private disabled: boolean = false
    ) {}
    // Adding new variant: 1 new class. Adding new size: 1 new class.
    // Total: 3 + 2 = 5 classes instead of 9, and scales linearly not multiplicatively.
}
```

### Severity Calibration
- **Advisory:** Hierarchy with 5-7 subclasses, single dimension of variation
- **Warning:** Hierarchy with 8-20 subclasses or 2+ independent variation dimensions
- **Critical:** Hierarchy with 20+ subclasses, clear combinatorial pattern, actively growing

### Applicable Patterns
| Pattern | When to use |
|---------|-------------|
| **Bridge** | Two independent dimensions of variation: separate the abstraction from its implementation |
| **Decorator** | Adding responsibilities dynamically by wrapping, not subclassing |
| **Strategy** | Vary one dimension of behavior at runtime by injecting a strategy object |
| **Composite** | Tree structures where branches and leaves share an interface |
| **Observer** | Notify multiple dependents without subclassing the subject |

---

## DS-08: Inability to Alter Classes

### Definition
A class that needs new behavior or a different interface cannot be modified: source code is unavailable (third-party library), modification would require changing many existing subclasses, or the class is so widely depended upon that any change is too risky.

### Why It Causes Redesign
Sometimes change is not possible through the class itself. A commercial library provides a class with the wrong interface. An internal "foundation" class has 50 downstream dependents. The class was designed without extension points. Without patterns to address this, the team either freezes their design (no new behavior) or copies the class (maintenance nightmare).

### Detection Criteria
- Classes that inherit directly from third-party or framework classes to add behavior
- Classes in vendor/dependency directories being subclassed in application code
- Statements in the codebase that suggest fear: "don't touch this class," "this is from the library," "we can't change this"
- Classes with no extension points (no abstract methods, no strategy injection, no event hooks) that callers need to customize
- Large numbers of existing subclasses that would all need updating if the base class changed

### Grep Patterns

**Java:**
```
# Find classes extending vendor/library classes
grep -rn "extends com\.\|extends org\.\|extends javax\." src/main/
# Find classes from vendor directories being extended
grep -rn "import com\.thirdparty\." src/ | grep -v vendor/
```

**Python:**
```
# Find classes extending third-party bases
grep -rn "class [A-Z][a-zA-Z]*(django\.\|flask\.\|sqlalchemy\." src/app/
```

**General signal:** Any class in `node_modules/`, Maven dependencies, pip packages that application classes inherit from directly.

### Code Example: Smell

```java
// Java — extending a library class to change its behavior
// Library: ThirdPartyLogger — source unavailable, cannot modify
public class ApplicationLogger extends ThirdPartyLogger {
    // overriding to add our formatting
    @Override
    public void log(String message) {
        super.log("[APP] " + message);
    }
    // If ThirdPartyLogger changes its log() signature: our class breaks
    // If we need logging in tests: must have ThirdPartyLogger available
}
```

### Code Example: Fixed (Adapter + Decorator)

```java
// Java — wrap the library class, don't inherit it
public interface Logger {
    void log(String message);
}

public class ThirdPartyLoggerAdapter implements Logger {
    private final ThirdPartyLogger delegate;

    public ThirdPartyLoggerAdapter(ThirdPartyLogger delegate) {
        this.delegate = delegate;
    }

    @Override
    public void log(String message) {
        delegate.log("[APP] " + message);
    }
    // ThirdPartyLogger changes: only this adapter needs updating
    // Tests: mock the Logger interface — no dependency on the library
}
```

### Severity Calibration
- **Advisory:** Application extends a stable, well-maintained framework class for a well-defined extension point (e.g., extending a servlet, controller base class) — this is often intentional
- **Warning:** Application extends a third-party class to change behavior rather than use an extension point
- **Critical:** A class that many subclasses depend on needs to change, but changing it requires updating all subclasses; or vendor dependency is extended and the vendor is actively changing their API

### Applicable Patterns
| Pattern | When to use |
|---------|-------------|
| **Adapter** | Convert the interface of a class you can't change into the interface your code expects |
| **Decorator** | Add behavior to a class you can't modify by wrapping it, not subclassing it |
| **Visitor** | Add new operations to a class hierarchy without modifying the hierarchy's classes |

---

## Pattern Overuse Warning (from GoF p. 41)

Design patterns achieve flexibility and variability by introducing additional levels of indirection. This can complicate a design and cost performance.

**A design pattern should only be applied when the flexibility it affords is actually needed.**

Before recommending any pattern, apply this check:

| Question | If YES | If NO |
|----------|--------|-------|
| Does this code actually need to vary in the way the pattern enables? | Pattern is justified | Flag as low priority or skip |
| Has this code already needed to change in the way the smell predicts? | Raise priority | Keep as Advisory |
| Would a developer without pattern knowledge understand the result? | Acceptable trade-off | Consider simpler approach |
| Does the performance cost of indirection matter here? | Evaluate Consequences section of the pattern | Proceed |

The Consequences section of each GoF pattern entry describes its liabilities explicitly. Always review liabilities before recommending.

---

## Severity Reference Matrix

| Spread | Friction | Severity | Recommended Action |
|:------:|:--------:|:--------:|-------------------|
| Isolated (1-2 sites) | Low | Advisory | Document; address opportunistically |
| Isolated (1-2 sites) | High | Warning | Plan for next refactoring sprint |
| Moderate (3-10 sites) | Low | Warning | Plan for next refactoring sprint |
| Moderate (3-10 sites) | High | Critical | Address before next feature work |
| Pervasive (10+ sites) | Low | Warning | Plan phased refactoring |
| Pervasive (10+ sites) | High | Critical | Address immediately — blocking velocity |

**Friction:** How often does this smell cause actual change pain?
- Low: Code is stable; this area is rarely modified
- Medium: Code changes occasionally; smell has caused rework 1-2 times
- High: Code changes frequently; smell is actively slowing the team

---

## Pattern Quick Reference (smell-to-pattern mapping)

| Smell | Primary Patterns | Secondary Patterns |
|-------|-----------------|-------------------|
| DS-01 Hardcoded creation | Abstract Factory, Factory Method | Prototype |
| DS-02 Operation dependencies | Command, Chain of Responsibility | — |
| DS-03 Platform coupling | Abstract Factory, Bridge | — |
| DS-04 Representation leaks | Abstract Factory, Bridge | Memento, Proxy |
| DS-05 Algorithmic dependencies | Strategy, Template Method | Builder, Iterator, Visitor |
| DS-06 Tight coupling | Abstract Factory, Bridge, Mediator | Command, CoR, Facade, Observer |
| DS-07 Subclass explosion | Bridge, Decorator, Strategy | Composite, Observer |
| DS-08 Frozen classes | Adapter, Decorator | Visitor |
