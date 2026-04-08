---
name: strategy-pattern-implementor
description: |
  Implement the Strategy pattern to encapsulate a family of interchangeable algorithms behind a common interface. Use when you have multiple conditional branches selecting between algorithm variants, when algorithms need different space-time trade-offs, when a class has multiple behaviors expressed as conditionals, or when you need to swap algorithms at runtime. Detects the key code smell — switch/if-else chains selecting behavior — and refactors to Strategy objects.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/design-patterns-gof/skills/strategy-pattern-implementor
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - behavioral-pattern-selector
source-books:
  - id: design-patterns-gof
    title: "Design Patterns: Elements of Reusable Object-Oriented Software"
    authors: ["Erich Gamma", "Richard Helm", "Ralph Johnson", "John Vlissides"]
    chapters: [5]
    pages: [48-50, 292-300]
tags: [design-patterns, behavioral, gof, strategy, refactoring, algorithms, composition]
execution:
  tier: 2
  mode: full
  inputs:
    - type: code
      description: "Existing code with conditional branches selecting between algorithm variants, or a description of the algorithmic variation that needs encapsulation"
  tools-required: [TodoWrite, Read]
  tools-optional: [Grep, Edit]
  mcps-required: []
  environment: "Any codebase. Language-agnostic — examples use Python but the pattern applies universally."
---

# Strategy Pattern Implementor

## When to Use

You have a class that selects between algorithm variants and need to refactor it so algorithms can vary independently from the clients that use them. This skill applies when:

- A class contains `switch` statements or `if/else` chains that select between behavioral variants — **the primary code smell**
- Multiple related classes differ only in their behavior (same structure, different computation)
- You need different space-time trade-offs for the same operation (fast-and-approximate vs. slow-and-precise)
- An algorithm uses data clients should not know about (complex internal data structures that would leak through the interface)
- You need to swap the algorithm at runtime without changing the client

Before starting, confirm:
- Is this a **client-selected** algorithm switch (Strategy) rather than an **object self-transitioning** based on internal state (State)? If unsure, use `behavioral-pattern-selector` first.
- Does the variation belong in the class itself, or is it better expressed via a superclass skeleton with subclass steps (Template Method via inheritance)? Strategy uses composition — the algorithm is a separate object, not a subclass.

---

## Process

### Step 1: Set Up Tracking and Identify the Conditional

**ACTION:** Use `TodoWrite` to track progress, then locate the conditional code that signals the need for Strategy.

**WHY:** The conditional block is the concrete artifact you are eliminating. Identifying it precisely — its location, what it selects between, and what data it touches — drives every subsequent decision about interface design and data passing. Without pinning this down first, the refactoring risks producing a Strategy structure that does not fit the actual variation.

```
TodoWrite:
- [ ] Step 1: Locate the conditional and characterize the variation
- [ ] Step 2: Define the Strategy interface
- [ ] Step 3: Implement ConcreteStrategy classes
- [ ] Step 4: Refactor the Context class
- [ ] Step 5: Validate and apply optional optimizations
```

Locate the conditional using `Read` or `Grep`, then document:

| Element | What to capture |
|---------|----------------|
| **Location** | File, class, method where the conditional lives |
| **Variants** | How many branches? What does each compute? |
| **Data required** | What data does each branch use from the context? |
| **Selection point** | Who chooses the variant — the caller, a config value, or a runtime condition? |
| **Change frequency** | How often are new variants added? Does this class change every time? |

If working from a description rather than existing code, draft a minimal "before" sketch showing the conditional structure.

---

### Step 2: Define the Strategy Interface

**ACTION:** Design the abstract Strategy interface — the single method (or small set of methods) that all ConcreteStrategies must implement.

**WHY:** The Strategy interface is the contract that decouples the Context from all algorithm implementations. If it is too narrow (missing data the strategy needs), ConcreteStrategies will have to reach into the Context through back-channels, increasing coupling. If it is too wide (exposing data no strategy uses), the communication overhead between Strategy and Context grows. The interface must be general enough that you will not have to change it when adding new ConcreteStrategies — this is the central design decision of the pattern.

**Two data-passing approaches — choose one:**

| Approach | How it works | When to prefer |
|----------|-------------|----------------|
| **Take data to the strategy** | Context passes all needed data as parameters to the strategy method | Algorithm needs a bounded, well-known set of inputs; keeps Strategy and Context decoupled |
| **Pass context as argument** | Strategy receives the Context object itself and requests what it needs | Algorithm needs variable or large amounts of context data; reduces parameter proliferation but couples Strategy to Context's interface |

Design the interface method signature:

```python
# Approach 1: explicit parameters (preferred when data set is bounded)
class SortStrategy:
    def sort(self, data: list) -> list:
        raise NotImplementedError

# Approach 2: context reference
class SortStrategy:
    def sort(self, context: "Sorter") -> None:
        raise NotImplementedError
```

**Check:** Will a new ConcreteStrategy ever need data this interface does not provide? If yes, revise — you should not need to change the interface when adding strategies.

---

### Step 3: Implement ConcreteStrategy Classes

**ACTION:** Extract each conditional branch into its own ConcreteStrategy class that implements the Strategy interface.

**WHY:** Each branch in the original conditional is an independently varying algorithm. Making each one a class gives it a name (making the code self-documenting), an isolated scope for its data structures (preventing algorithm-specific complexity from polluting the Context), and a testable boundary (each strategy can be tested in isolation without instantiating the full Context).

For each branch in the original conditional:

1. Create a class named after the algorithm it encapsulates (not after what it replaces — use domain terminology, e.g., `BubbleSortStrategy`, not `OldSortBranch`)
2. Implement the interface method with the branch's logic
3. Move any algorithm-specific private data into the ConcreteStrategy (not the Context)

```python
class BubbleSortStrategy(SortStrategy):
    """Simple sort — O(n²), stable, no extra memory."""
    def sort(self, data: list) -> list:
        result = data[:]
        n = len(result)
        for i in range(n):
            for j in range(0, n - i - 1):
                if result[j] > result[j + 1]:
                    result[j], result[j + 1] = result[j + 1], result[j]
        return result

class QuickSortStrategy(SortStrategy):
    """Fast sort — O(n log n) average, not stable, in-place."""
    def sort(self, data: list) -> list:
        result = data[:]
        self._quicksort(result, 0, len(result) - 1)
        return result

    def _quicksort(self, arr, low, high):
        if low < high:
            pi = self._partition(arr, low, high)
            self._quicksort(arr, low, pi - 1)
            self._quicksort(arr, pi + 1, high)

    def _partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        for j in range(low, high):
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        return i + 1
```

**Stateless strategies as Flyweights:** If a ConcreteStrategy holds no instance state (all data comes from parameters), it can be shared across multiple Context instances. A single shared instance replaces per-context allocation. This optimization applies when strategies are lightweight and stateless — do not force it if the strategy needs per-invocation state.

---

### Step 4: Refactor the Context Class

**ACTION:** Replace the conditional in the Context with a reference to a Strategy object and a delegation call.

**WHY:** This is the core structural change. The Context no longer *knows* how to perform the algorithm — it only knows *that* an algorithm exists and how to invoke it. The conditional disappears entirely, replaced by a single delegation call. The Context becomes open to extension (new strategies) without modification, satisfying the open-closed principle.

**Refactoring steps:**

1. Add a `strategy` attribute (initialized via constructor or setter)
2. Replace the entire conditional block with a single call to `self.strategy.algorithm_method(...)`
3. Remove any algorithm-specific data that has moved into ConcreteStrategy classes
4. Optionally provide a default strategy so clients that do not care about the choice are unaffected

```python
# BEFORE (conditional in Context)
class DataProcessor:
    def __init__(self, algorithm: str):
        self._algorithm = algorithm

    def process(self, data: list) -> list:
        if self._algorithm == "bubble":
            # bubble sort logic — 10 lines
            ...
        elif self._algorithm == "quick":
            # quicksort logic — 20 lines
            ...
        elif self._algorithm == "merge":
            # merge sort logic — 25 lines
            ...

# AFTER (Strategy delegation)
class DataProcessor:
    def __init__(self, strategy: SortStrategy = None):
        # Default strategy makes Strategy optional for clients
        self._strategy = strategy or BubbleSortStrategy()

    def set_strategy(self, strategy: SortStrategy) -> None:
        """Swap algorithm at runtime without reconstructing the context."""
        self._strategy = strategy

    def process(self, data: list) -> list:
        return self._strategy.sort(data)
```

**Making Strategy optional:** If it is meaningful for the Context to have no strategy, check before delegating and execute default behavior when none is set. This keeps clients that do not need strategy selection from having to deal with Strategy objects at all.

---

### Step 5: Validate and Apply Optional Optimizations

**ACTION:** Verify the refactoring is complete, then apply optimizations if warranted.

**WHY:** The refactoring is only complete when the original conditional is fully gone and all variants are covered. Partial migration — leaving one branch in the Context "for now" — defeats the pattern and re-introduces the code smell. Validation catches this before new code is written against the incomplete structure.

**Validation checklist:**

- [ ] The original conditional block is entirely removed from the Context
- [ ] Every branch of the original conditional has a corresponding ConcreteStrategy
- [ ] The Context delegates to the strategy via the interface — it imports no ConcreteStrategy class directly
- [ ] Each ConcreteStrategy can be instantiated and tested independently
- [ ] Adding a new algorithm requires only a new class, not a change to the Context

**Optional optimizations:**

| Optimization | When to apply |
|--------------|--------------|
| **Flyweight sharing** | ConcreteStrategies are stateless — share one instance across all Contexts instead of allocating per-Context |
| **Default strategy** | Most clients use one algorithm — set it as default so callers who do not care are unaffected |
| **Factory for selection** | Strategy selection logic is complex — extract it into a factory rather than leaving it scattered in callers |
| **Abstract base with shared logic** | Multiple ConcreteStrategies share common steps — add a base ConcreteStrategy class with shared implementation (not the interface) |

**Drawback awareness — address before finishing:**

- **Client awareness:** Clients must now know which ConcreteStrategy to instantiate. If this knowledge is non-trivial (depends on configuration, environment, or runtime data), introduce a factory or builder to centralize selection logic.
- **Communication overhead:** The Strategy interface is shared by all ConcreteStrategies regardless of complexity. Simple strategies may receive parameters they do not use (e.g., `ArrayCompositor` in the Lexi case ignores stretchability data). If this overhead is significant, consider tighter coupling between specific strategies and the context — but accept that this reduces generality.

---

## Examples

### Example 1: Payment Processing (Classic Conditional to Strategy)

**Scenario:** An e-commerce checkout has a `PaymentService` with a large `if/else` chain selecting between credit card, PayPal, and bank transfer logic. A new payment method is requested every quarter, and each addition requires modifying `PaymentService` directly.

**Trigger:** "Every time we add a payment provider, we touch the same `process_payment` method and it keeps growing."

**Before (the code smell):**
```python
class PaymentService:
    def process_payment(self, amount: float, method: str, details: dict):
        if method == "credit_card":
            # validate card, charge via Stripe, handle 3DS...
        elif method == "paypal":
            # OAuth flow, PayPal API call, webhook...
        elif method == "bank_transfer":
            # IBAN validation, SEPA/ACH routing...
        else:
            raise ValueError(f"Unknown method: {method}")
```

**After (Strategy):**
```python
class PaymentStrategy:
    def process(self, amount: float, details: dict) -> PaymentResult:
        raise NotImplementedError

class CreditCardStrategy(PaymentStrategy):
    def process(self, amount: float, details: dict) -> PaymentResult:
        # Stripe integration, 3DS, card validation

class PayPalStrategy(PaymentStrategy):
    def process(self, amount: float, details: dict) -> PaymentResult:
        # OAuth, PayPal API, webhook handling

class BankTransferStrategy(PaymentStrategy):
    def process(self, amount: float, details: dict) -> PaymentResult:
        # IBAN validation, SEPA/ACH routing

class PaymentService:
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy

    def process_payment(self, amount: float, details: dict) -> PaymentResult:
        return self._strategy.process(amount, details)

# Caller selects the strategy — PaymentService never changes
service = PaymentService(CreditCardStrategy())
result = service.process_payment(99.99, {"card_number": "..."})
```

**Output:** `PaymentService` is closed to modification. Adding `CryptoStrategy` requires zero changes to existing code.

---

### Example 2: Lexi Document Formatter (GoF Case Study)

**Scenario:** Lexi, a WYSIWYG document editor, must break text into lines. Several algorithms exist: a simple greedy line-breaker, a full TeX-quality algorithm optimizing paragraph-level color, and a fixed-interval breaker for icon grids. The algorithms have different speed-quality trade-offs and the user may switch between them.

**Trigger:** "The formatting algorithm needs to change at runtime depending on document type, and we need to add new algorithms without touching the document structure."

**Design (from GoF, pages 48-50 and 296-298):**

```
Context:     Composition  (holds content glyphs, line width)
Strategy:    Compositor   (abstract — Compose() interface)
ConcreteA:   SimpleCompositor    — greedy, line-at-a-time, fast
ConcreteB:   TeXCompositor       — paragraph-at-a-time, optimizes whitespace color
ConcreteC:   ArrayCompositor     — fixed interval, for icon grids
```

The Compositor interface takes all layout data as explicit parameters (Approach 1 — data to the strategy):

```cpp
virtual int Compose(
    Coord natural[], Coord stretch[], Coord shrink[],
    int componentCount, int lineWidth, int breaks[]
) = 0;
```

This interface is wide enough to support all three algorithms. `SimpleCompositor` ignores stretchability; `ArrayCompositor` ignores everything except component count. This is the **communication overhead trade-off** — some ConcreteStrategies receive data they do not use. The GoF accept this because the alternative (passing `this` as a context reference) would couple Compositor subclasses to Composition's full interface.

**Runtime swap:**
```cpp
// Switching quality at runtime — no reconstruction of Composition
composition->SetCompositor(new TeXCompositor());
composition->Repair();  // delegates to compositor->Compose(...)
```

**Output:** Adding a new linebreaking algorithm is a new `Compositor` subclass. Neither `Composition` nor the glyph classes are ever modified.

---

### Example 3: Report Exporter with Runtime Selection

**Scenario:** A reporting tool exports data as CSV, JSON, or PDF. The format is determined by user selection at runtime. Currently the export logic lives in a single `export()` method with a `format` string parameter driving a conditional.

**Trigger:** "Users can choose the export format from a dropdown — the format isn't known until they click Export."

**Strategy interface (data to strategy, Approach 1):**
```python
class ExportStrategy:
    def export(self, records: list[dict], output_path: str) -> None:
        raise NotImplementedError

class CsvExportStrategy(ExportStrategy):
    def export(self, records, output_path):
        import csv
        with open(output_path, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=records[0].keys())
            writer.writeheader()
            writer.writerows(records)

class JsonExportStrategy(ExportStrategy):
    def export(self, records, output_path):
        import json
        with open(output_path, "w") as f:
            json.dump(records, f, indent=2)

class PdfExportStrategy(ExportStrategy):
    def export(self, records, output_path):
        # reportlab or weasyprint integration
        ...

class ReportExporter:
    _STRATEGIES = {
        "csv": CsvExportStrategy,
        "json": JsonExportStrategy,
        "pdf": PdfExportStrategy,
    }

    def __init__(self):
        self._strategy: ExportStrategy = CsvExportStrategy()  # default

    def set_format(self, format_key: str) -> None:
        """Runtime swap — called when user selects format in UI."""
        cls = self._STRATEGIES.get(format_key)
        if not cls:
            raise ValueError(f"Unknown format: {format_key}")
        self._strategy = cls()

    def export(self, records: list[dict], output_path: str) -> None:
        self._strategy.export(records, output_path)
```

**Key decision:** The `_STRATEGIES` registry centralizes selection logic in the Context, keeping callers simple. An alternative is to move this registry to a factory, which is preferable when selection logic becomes complex (e.g., involving feature flags or user tier).

**Output:** The UI dropdown maps to `set_format()`. Adding XML export is a new `XmlExportStrategy` class plus one entry in `_STRATEGIES` — the rest of the system is unchanged.

---

## Strategy vs. Template Method — When to Use Which

Both patterns encapsulate algorithmic variation. The choice is **composition vs. inheritance**:

| Dimension | Strategy | Template Method |
|-----------|----------|----------------|
| Mechanism | Composition — context holds a strategy object | Inheritance — subclass overrides abstract steps |
| Runtime swap | Yes — install a different strategy object | No — fixed at class definition |
| Granularity | Entire algorithm is replaced | Only specific steps are replaced; skeleton is fixed |
| Class count | One class per algorithm variant | One subclass per algorithm variant |
| Coupling | Strategy and Context are loosely coupled | Subclass is tightly coupled to superclass skeleton |
| Evolution path | Start with Template Method → migrate to Strategy when inheritance becomes limiting | — |

**Choose Strategy when** the algorithm must be swappable at runtime, when you do not control the class hierarchy, or when the number of variants is large and growing.

**Choose Template Method when** the algorithm skeleton is fixed and only specific steps vary, and when compile-time binding is acceptable.

---

## Reference Files

| File | Contents |
|------|----------|
| `references/strategy-implementation-guide.md` | Participants, full consequences catalog, interface design decision tree, Flyweight optimization, language-specific notes |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Design Patterns: Elements of Reusable Object-Oriented Software by Erich Gamma, Richard Helm, Ralph Johnson, John Vlissides.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-behavioral-pattern-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
