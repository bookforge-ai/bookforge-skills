---
name: web-presentation-pattern-selector
description: "Select the right web presentation pattern combination for any server-side web layer under design or refactor. Covers MVC (Model View Controller) decomposition, all three view patterns (Template View, Transform View, Two Step View), all three controller patterns (Page Controller, Front Controller, Application Controller), and when to layer Application Controller above the others for wizard or state-machine flows. Use when designing a new web layer, refactoring a tangled web controller, diagnosing fat controller or Template View scriptlet anti-patterns, mapping legacy JSP/ERB/ASP patterns to modern equivalents (Spring DispatcherServlet = Front Controller, Rails Router = Front Controller, JSP/ERB/Jinja = Template View), or deciding whether a wizard flow needs an Application Controller above a Front Controller. Applies to any language/framework: Java Spring MVC, Ruby on Rails, Python Django/Flask, ASP.NET Core, Node.js Express, PHP Laravel. Produces a web presentation design record with pattern selections, anti-pattern audit, and framework-specific implementation notes. Relevant keywords: web controller pattern, MVC, Model View Controller, Page Controller, Front Controller, Application Controller, Template View, Transform View, Two Step View, web presentation pattern, web framework architecture, refactor controllers, fat controller, server-side rendering, server-side MVC."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/patterns-of-enterprise-application-architecture/skills/web-presentation-pattern-selector
metadata: {"openclaw":{"emoji":"🌐","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: patterns-of-enterprise-application-architecture
    title: "Patterns of Enterprise Application Architecture"
    authors:
      - Martin Fowler
      - David Rice
      - Matthew Foemmel
      - Edward Hieatt
      - Robert Mee
      - Randy Stafford
    chapters:
      - "Chapter 4. Web Presentation (narrative)"
      - "Chapter 14. Web Presentation Patterns"
domain: software-architecture
tags:
  - web-presentation
  - mvc
  - web-application
  - controllers
  - design-patterns
  - software-architecture
  - server-side-rendering
  - enterprise-patterns
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: codebase
      description: "Web layer source files (controllers, views, templates, routing config). Optional but significantly improves anti-pattern detection."
    - type: description
      description: "Natural-language description of the web layer shape, framework in use, pain points, and workflow complexity."
  tools-required:
    - Read
    - Glob
    - Grep
    - Write
  tools-optional:
    - Edit
  mcps-required: []
  environment: "Enterprise web application codebase with a web layer (controllers, views, templates). Framework detection from pom.xml, Gemfile, package.json, requirements.txt, or *.csproj. Works with description-only when no codebase is available."
discovery:
  goal: "Route a web layer to the right combination of view pattern, controller pattern, and optional Application Controller for workflow features."
  tasks:
    - "Detect the framework and what patterns it already mandates"
    - "Select view pattern: Template View, Transform View, or Two Step View"
    - "Select controller pattern: Page Controller or Front Controller (or confirm framework default)"
    - "Decide whether Application Controller is warranted for any wizard or state-machine flows"
    - "Audit existing code for scriptlet and fat-controller anti-patterns"
    - "Produce a web presentation design record with implementation notes"
  audience:
    roles:
      - software-architect
      - senior-backend-engineer
      - tech-lead
      - framework-designer
    experience: intermediate
  when_to_use:
    triggers:
      - "Designing the web layer of a new enterprise application"
      - "Refactoring a tangled or overgrown controller layer"
      - "Controllers contain domain logic (fat controller symptom)"
      - "Templates contain conditionals, loops, or database calls (scriptlet symptom)"
      - "A multi-step wizard or approval flow is being added to an existing app"
      - "Migrating from one web framework to another and mapping old patterns to new"
      - "Code review of web-layer architecture raises questions about pattern choice"
      - "Team argument over Front Controller vs Page Controller style"
    prerequisites: []
    not_for:
      - "Single-page applications with no server-rendered HTML (though the API backend still benefits from controller-pattern advice)"
      - "Selecting a persistence pattern (use enterprise-architecture-pattern-stack-selector or data-source-pattern-selector)"
      - "Selecting a session state strategy (use session-state-location-selector)"
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

# Web Presentation Pattern Selector

## When to Use

Use this skill when designing or refactoring the web layer of a server-side enterprise application. It applies pattern-level decision heuristics from Fowler's *Patterns of Enterprise Application Architecture* — specifically the three view patterns (Template View, Transform View, Two Step View), three controller patterns (Page Controller, Front Controller, Application Controller), and the server-side MVC framework that holds them together.

**Typical triggers:** new web layer design, fat controller refactor, scriptlet cleanup, adding a wizard flow, framework migration, or a team disagreement about controller structure.

**NOT for:** selecting persistence or session-state patterns (see Related Skills). For SPA-only frontends, apply this skill to the API backend — the patterns translate cleanly (Front Controller = API router, Transform View = JSON serializer).

**Prerequisites:** none. Works with codebase or description alone.

---

## Context & Input Gathering

Before selecting patterns, gather the following. Ask if not provided.

**Required:**
- Language and framework (Spring MVC, Rails, Django, Express, ASP.NET Core, Laravel, Flask, other)
- Rendering mode: server-rendered HTML, API-only (JSON), or hybrid (server HTML + API endpoints)
- Brief description of the web layer's current shape (controllers, views, templates)
- Most acute pain point (fat controllers, scriptlet mess, duplicated cross-cutting logic, wizard complexity)

**Observable from codebase:**
- Build file (`pom.xml`, `Gemfile`, `package.json`, `*.csproj`, `requirements.txt`) for framework detection
- `src/web/` or `src/controllers/` or `app/controllers/` for controller shapes
- `src/views/` or `app/views/` or `templates/` for view/template shapes
- Routing config (`routes.rb`, `urls.py`, `*.routes.ts`, `WebMvcConfigurer`, `Startup.cs`) for dispatcher shape

**Defaults if unknown:**
- Assume Template View if server pages (JSP/ERB/Jinja/Razor) are present
- Assume Front Controller if the framework has a central dispatcher (almost all modern frameworks do)
- Assume no Application Controller unless wizard/approval flows exist

**Sufficiency check:** proceed when you know the framework, rendering mode, and at least one pain point. The codebase improves precision but is not required.

---

## Process

### Step 1 — Identify What the Framework Already Mandates

*WHY: Most modern frameworks ship with Front Controller built in. The decision between Page Controller and Front Controller is often already made. Starting here prevents recommending a pattern the framework makes impossible or redundant.*

1a. Detect the framework from build files or imports.
1b. Map the framework to its built-in controller pattern:

| Framework | Built-in controller pattern |
|---|---|
| Spring MVC | Front Controller (DispatcherServlet) |
| Rails | Front Controller (Router) + Page Controller (controller actions) |
| Django | Front Controller (URL dispatcher) + Page Controller (views) |
| ASP.NET Core MVC | Front Controller (middleware pipeline + MVC middleware) |
| Express / Koa | Front Controller (app.use middleware chain) |
| Laravel | Front Controller (Router) |
| Flask | Hybrid — route decorators approach Page Controller; Blueprints add Front Controller behavior |

1c. Note: in frameworks with a built-in Front Controller, the real decision shifts to *how to structure the command/action layer* (Page Controller style within the Front Controller) and *which view technology to use*.

---

### Step 2 — Clarify the Rendering Mode

*WHY: Rendering mode determines which view pattern is relevant. API-only backends still use view patterns — the "view" is the JSON serializer or response transformer.*

- **Server-rendered HTML:** all three view patterns apply.
- **API-only (JSON):** Transform View applies to the serializer/presenter layer. Template View and Two Step View are not relevant for HTML, but Two Step View logic applies to multi-format response shaping.
- **Hybrid:** choose view patterns per endpoint group.

For SPA frontends with a server API: proceed with Front Controller for the API router and Transform View for the JSON response shaping; note that the client-side SPA uses a browser-MVC variant (React/Vue/Angular) that is a different pattern instantiation.

---

### Step 3 — Select the View Pattern

*WHY: The view pattern determines how domain data becomes the response. Wrong choice leads to scriptlet accumulation (Template View scriptlets), unmaintainable XSLT (Transform View overuse), or unnecessary complexity (Two Step View when layout is not shared).*

**Decision tree:**

```
Is the output HTML?
├── YES
│   ├── Are designers (non-programmers) editing the templates?
│   │   └── YES → Template View (keep business logic out via helper objects)
│   ├── Is the domain data already XML or trivially convertible?
│   │   └── YES, and you need testable pure-function rendering → Transform View
│   ├── Do many screens share the same layout structure and you need
│   │   global HTML changes to touch ONE place?
│   │   └── YES → Two Step View
│   └── Default (no special constraint) → Template View
└── NO (JSON / XML API)
    └── Transform View (serializer/presenter is the transform)
```

**Template View (default for HTML):**
- Embed markers in a static HTML page; markers are resolved at request time.
- Use with a helper object to keep logic out of the template.
- Modern equivalents: ERB, Jinja2, Razor, Thymeleaf, Blade, Handlebars.
- Watch for: scriptlet anti-pattern (see Step 6).

**Transform View (for clean separation or multi-format):**
- Write a transform that walks domain data and produces output (HTML, JSON, XML).
- Organized around *input element types*, not output page structure.
- Classic XSLT; modern equivalents: React/Vue render functions, JSON serializer classes, GraphQL resolvers.
- Pro: deterministic, testable. Con: alien syntax (XSLT); requires domain data in a traversable structure.

**Two Step View (for site-wide consistency):**
- Stage 1: per-screen component produces a logical screen (fields, tables, headers — no HTML).
- Stage 2: single application-wide component converts logical screen to HTML.
- Use when: many screens share the same layout AND you need one-place global HTML control.
- Modern equivalents: layout components (Next.js layouts, Rails application layout), design-system primitive libraries.
- Do NOT use when screens are highly design-intensive and differ significantly.

---

### Step 4 — Select the Controller Pattern

*WHY: The controller pattern determines where HTTP request handling, cross-cutting concerns (auth, logging, i18n), and flow decisions live. Wrong choice leads to duplicated cross-cutting logic (Page Controller without helpers) or untraceable routing (Front Controller with too much dispatch logic).*

**If the framework mandates Front Controller (most frameworks):** confirm and document it. Focus instead on how action-level handlers are structured (Page Controller style actions within the Front Controller).

**If the framework is flexible (CGI, raw servlets, simple HTTP handlers):**

```
Does the site have many similar cross-cutting concerns
(auth, logging, i18n, CSRF) across all or most requests?
├── YES → Front Controller
│   └── Use Intercepting Filter (decorator chain) for cross-cutting concerns
└── NO, or team wants simpler per-page ownership →  Page Controller
    └── Factor cross-cutting into a common base class or helper
```

**Page Controller:**
- One handler per logical action/page.
- Responsibilities: decode URL + form data → invoke model (no HTTP leakage into model) → forward to view.
- Scale: works well when team members own separate page areas; minimal coupling.
- Add a base class or before-filter mechanism for shared behavior.
- Modern pattern: Rails controller actions, Django class-based views (each action IS a Page Controller).

**Front Controller:**
- Single Web Handler receives all requests, dispatches to Command objects.
- Command objects have no Web knowledge (testable independently).
- Static dispatch: explicit URL → command mapping (compile-time checked, flexible URL shapes).
- Dynamic dispatch: URL contains command class name or properties-file lookup (extensible without changing the handler).
- Use Intercepting Filter / middleware pipeline for auth, logging, CSRF.

---

### Step 5 — Decide Whether Application Controller Is Warranted

*WHY: Application Controller removes duplicated flow logic from individual page controllers. Without it, wizard-style features get partially re-implemented in each step's controller, and changing step order touches multiple files.*

**Trigger check — answer YES to any of these to proceed with Application Controller:**
- Does any feature follow a fixed or conditional ordered sequence of screens (wizard, checkout, onboarding)?
- Do multiple controllers need to share the decision of which screen to show next?
- Is navigation state (current step, earlier answers) being passed between controllers manually?
- Would reordering or adding a step in a flow require changing multiple controller files?

**If YES:** introduce an Application Controller that holds:
- A collection of domain commands (which service/domain method to invoke for each step)
- A collection of view references (which view to show after each step)
- The flow/state-machine logic (what comes next given current state + input)

Input controllers (Page or Front) ask the Application Controller for commands and views rather than deciding themselves.

Prefer: Application Controller with no direct dependencies on HTTP/UI machinery — keeps it testable.

Modern equivalents: step-based wizard routers (React Router with step state), BPM/workflow engines (Temporal, Camunda), Next.js parallel routes with step orchestration.

**If NO:** Application Controller is not warranted. Keep flow decisions simple and local.

---

### Step 6 — Audit for Anti-Patterns

*WHY: Identifying existing anti-patterns grounds the recommendation in concrete code symptoms and provides a refactoring roadmap.*

If a codebase is available, grep for:

**Template View scriptlets:**
```
# JSP: <% ... %> blocks with logic
Grep: "<%[^=!@]" in *.jsp
# ERB: <% ... %> with conditionals, queries
Grep: "<%[^=]" with if/ActiveRecord in *.erb
# Jinja: {% if %} containing service calls or SQL
Grep: "{% if\|{% for" in templates/*.html — check body for data calls
```
Symptom: template contains `if`, `for`, database access, or business rules.
Fix: extract to helper object / view model; controller populates a DTO; template only renders.

**Fat Controller:**
```
Grep: SQL strings, repository calls, calculation logic inside controller action methods
Grep: action methods > ~20 lines of non-HTTP logic
```
Symptom: controller action contains domain logic (calculations, validation beyond input format, business rules).
Fix: move to service layer or domain object; controller decodes input → calls service → forwards to view.

**Domain Logic in Front Controller Dispatch:**
Symptom: Web handler / router contains `if` blocks for business rules (not routing decisions).
Fix: move to Command objects or domain layer; keep the handler purely routing.

---

### Step 7 — Produce the Web Presentation Design Record

*WHY: A concise written record makes the pattern decision reviewable, shareable with the team, and referenceable during implementation.*

Write a `web-presentation-design.md` in the project root or architecture docs folder with:

```markdown
# Web Presentation Design Record

## Framework
[Framework name + version]

## Rendering Mode
[Server-rendered HTML | API-only JSON | Hybrid]

## View Pattern
**Selected:** [Template View | Transform View | Two Step View]
**Rationale:** [1-2 sentences]
**Implementation:** [specific technology — ERB, Jinja2, XSLT, React SSR, etc.]
**Guard against:** [scriptlet accumulation | XSLT complexity | layout rigidity]

## Controller Pattern
**Selected:** [Front Controller | Page Controller | Framework Default (Front Controller)]
**Rationale:** [1-2 sentences]
**Implementation:** [Spring DispatcherServlet + command objects | Rails Router + controller actions | etc.]
**Cross-cutting concerns:** [middleware chain | base controller | before_action filters]

## Application Controller
**Decision:** [Warranted | Not warranted]
**Rationale:** [1-2 sentences]
**Features requiring it:** [list of wizard/workflow features, or "none"]
**Implementation:** [step router | BPM engine | custom state machine | n/a]

## Anti-Pattern Audit
| Anti-pattern | Found? | Location | Fix |
|---|---|---|---|
| Template View scriptlets | [Yes/No] | [files] | [action] |
| Fat controller | [Yes/No] | [controllers] | [action] |
| Domain logic in dispatcher | [Yes/No] | [location] | [action] |

## Open Questions
[Any unresolved decisions for team discussion]
```

---

## Inputs

- **Framework name and version** (required)
- **Rendering mode** (server HTML / JSON API / hybrid)
- **Web layer source files** (`controllers/`, `views/`, `templates/`) — optional
- **Description of pain points** — optional but recommended
- **Workflow features list** — needed for Application Controller decision

---

## Outputs

- `web-presentation-design.md` — pattern selection record with rationale + anti-pattern audit
- Inline code snippets for controller/view refactoring (if codebase available)
- Framework-specific implementation notes

---

## Key Principles

**1. Server-side MVC is not browser MVC.**
Fowler's MVC places the model on the server; the view produces HTML; the controller handles HTTP. Browser-side MVC (React, Angular, Vue) is a different instantiation of the same idea on the client. Conflating them causes design confusion — especially when teams debate whether to "add MVC" to a Rails or Spring app that already has it.

**2. Most frameworks ship Front Controller — confirm, don't debate.**
Spring DispatcherServlet, Rails Router, Django URL dispatcher, Express middleware chain, ASP.NET Core pipeline — all are Front Controllers. The debate between Page Controller and Front Controller is already settled by the framework choice. Document this and move to the more meaningful decisions (view technology, Application Controller).

**3. Template View is the default; keep logic out of templates.**
Template View is appropriate for almost all HTML output. The risk is scriptlet accumulation — business logic creeping into templates. Prevent this with helper objects / view models: the controller populates a clean data structure; the template only renders. Scriptlets are a symptom of missing helper discipline.

**4. Transform View enables testable, format-agnostic output.**
A Transform View is organized around input elements, not output structure. This makes it deterministic and testable without a browser. XSLT is the classic implementation; modern equivalents are React render functions (client-side) and JSON serializer classes (API layer). Prefer Transform View when the same domain data must be rendered in multiple formats.

**5. Two Step View pays off only when layout is truly shared.**
The second-stage bottleneck is also the second-stage advantage: one place controls all HTML. This is valuable for site redesigns and theme changes, but harmful when screens need unique layouts. Design-system component libraries are the modern equivalent.

**6. Application Controller belongs to workflow, not every app.**
Application Controller is worth its indirection only when multiple features share navigation-state decisions. For simple request/response apps, it adds complexity without benefit. The trigger is: multiple controllers need to agree on which screen comes next based on shared state.

**7. Fat controllers signal domain logic displacement.**
When a controller action grows beyond input decoding + model invocation + view forwarding, domain logic has leaked. The controller is the wrong place for business rules: it's not reusable, not testable without HTTP, and not visible to domain developers. Move the logic to a service or domain object.

---

## Examples

### Example 1 — Rails App with Fat Controllers

**Scenario:** A Rails e-commerce app (Rails 7, ERB templates, PostgreSQL) where product and order controller actions each contain pricing calculation logic, discount rule evaluation, and direct ActiveRecord queries. Developers report tests requiring full request stacks.

**Trigger:** "Our Rails controllers are too fat — business logic is in the actions and tests are slow and fragile."

**Process:**
1. Framework: Rails 7 — Front Controller (Router) already in place. Rails controller actions = Page Controller style.
2. Rendering: Server-rendered ERB — Template View confirmed.
3. No wizard flows → Application Controller not warranted.
4. Anti-pattern audit: Grep `app/controllers/` for ActiveRecord queries and pricing logic in actions → found in `OrdersController#create` (82 lines, discount calculation) and `ProductsController#show` (direct SQL for related products).
5. Two Step View not needed — ERB templates + Rails application layout already handle shared structure.
6. Fix: extract `OrderPricingService` and `ProductQueryService`; controller actions become: decode params → call service → assign `@result` → render.

**Output design record:**
- View Pattern: Template View (ERB) — no change needed; add view models to prevent future scriptlet creep
- Controller Pattern: Front Controller (Rails Router) + Page Controller (controller actions) — confirmed, no change
- Application Controller: Not warranted
- Anti-pattern fixes: Move `OrdersController#create` pricing logic to `OrderPricingService`; move `ProductsController#show` query to `ProductRepository`

---

### Example 2 — Spring MVC App Adding a Checkout Wizard

**Scenario:** A Spring MVC app (Java 17, Thymeleaf templates) with a working product catalog. Adding a 5-step checkout wizard: (1) cart review, (2) address, (3) shipping options, (4) payment, (5) confirmation. Steps may conditionally skip (digital products skip shipping).

**Trigger:** "We need to add a multi-step checkout. How do we structure the controllers and avoid scattered navigation logic?"

**Process:**
1. Framework: Spring MVC — DispatcherServlet = Front Controller already in place.
2. Rendering: Server-rendered Thymeleaf — Template View confirmed.
3. Wizard flow with conditional step skipping → Application Controller IS warranted.
4. Application Controller holds: step sequence definition, which service method per step, which view per step, skip conditions (digital product → skip shipping step).
5. `CheckoutController` becomes thin: delegate to `CheckoutApplicationController.nextStep(session, input)` → get command + view; execute command; forward to view.
6. Anti-pattern check: ensure no business logic in the Thymeleaf templates (`th:if` on business conditions is the scriptlet equivalent — move conditions to view model).

**Output design record:**
- View Pattern: Template View (Thymeleaf) with view models (one per step)
- Controller Pattern: Front Controller (DispatcherServlet) + `CheckoutController` (Page Controller style for the wizard entry point)
- Application Controller: Warranted — `CheckoutApplicationController` owns step sequence + conditional skipping
- Anti-pattern prevention: Thymeleaf templates receive pre-computed view models; no business conditions in templates

---

### Example 3 — ASP.NET Core API Backend for a React SPA

**Scenario:** ASP.NET Core 8 Web API serving a React frontend. Team debating whether the "MVC pattern" applies — some say it's API-only so MVC doesn't matter.

**Trigger:** "We're building an API for our SPA. Does any of this web presentation pattern stuff apply to us?"

**Process:**
1. Framework: ASP.NET Core — middleware pipeline = Front Controller already in place.
2. Rendering: JSON API (no HTML).
3. MVC does apply to the API backend: Model = domain/service layer, View = JSON response shape (handled by serializer), Controller = API controller actions.
4. View pattern: Transform View — the JSON serializer/presenter walks domain objects and transforms them to JSON response DTOs. This is identical in structure to XSLT-based Transform View: input element types (domain objects) → output elements (JSON fields).
5. Controller pattern: Front Controller (ASP.NET Core pipeline) + Page Controller style actions in API controllers.
6. Application Controller: check for multi-step API flows (e.g., an onboarding flow across multiple API calls with server-side session state) — not present here → not warranted.
7. Anti-pattern note: "fat controller" still applies — business logic in API controller actions is the same problem as in HTML controllers.

**Output design record:**
- View Pattern: Transform View (JSON serializers / response DTOs) — model → DTO transformation in a dedicated presenter layer
- Controller Pattern: Front Controller (ASP.NET Core pipeline) + Page Controller style (API controller actions)
- Application Controller: Not warranted (stateless REST; no server-side wizard flows)
- SPA browser MVC: noted as separate concern — React's component model is a browser-side MVC variant; not Fowler's server-side MVC

---

## References

- `references/view-pattern-decision-matrix.md` — detailed decision matrix for Template View vs Transform View vs Two Step View with scoring criteria
- `references/controller-pattern-comparison.md` — Page Controller vs Front Controller trade-off table and base-class patterns for cross-cutting concerns
- `references/application-controller-triggers.md` — checklist of when to introduce Application Controller with flow-state modeling guidance
- `references/anti-pattern-detection-guide.md` — grep patterns, code smells, and fix recipes for scriptlet and fat-controller anti-patterns
- `references/framework-pattern-map.md` — complete mapping of modern web frameworks to PEAA controller and view patterns

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Patterns of Enterprise Application Architecture by Martin Fowler et al.

---

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-enterprise-architecture-pattern-stack-selector`
- `clawhub install bookforge-session-state-location-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
