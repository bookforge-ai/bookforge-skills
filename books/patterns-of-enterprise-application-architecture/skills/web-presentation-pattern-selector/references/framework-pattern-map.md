# Framework-to-PEAA Pattern Map

Source: Patterns of Enterprise Application Architecture, Ch 4 + Ch 14 (Fowler 2002)
Modern mappings added by BookForge.

## Controller Pattern by Framework

| Framework | Front Controller | Page Controller style |
|---|---|---|
| Spring MVC (Java) | DispatcherServlet | `@Controller` / `@RestController` methods |
| Ruby on Rails | Router (`config/routes.rb`) | Controller actions (`def show`, `def create`) |
| Django (Python) | URL dispatcher (`urls.py`) | View functions / Class-Based Views |
| ASP.NET Core | Middleware pipeline + MVC middleware | Controller action methods |
| Express (Node.js) | `app.use()` middleware chain | Route handler functions |
| Koa (Node.js) | Middleware stack | Route handler functions |
| Laravel (PHP) | Router (`routes/web.php`) | Controller methods |
| Flask (Python) | Blueprints + route decorators (hybrid) | `@app.route()` decorated view functions |
| FastAPI (Python) | Application + router | Route handler functions |
| Gin (Go) | Engine middleware chain | Handler functions |

**Key insight:** every mainstream web framework ships Front Controller by default. The Page Controller vs Front Controller debate is pre-decided by framework selection. Teams using these frameworks should document "Front Controller (framework default)" and focus decisions on: view technology, command/action structure, and Application Controller need.

## View Pattern by Technology

| Technology | PEAA View Pattern |
|---|---|
| JSP (Java) | Template View |
| Thymeleaf (Java) | Template View |
| FreeMarker (Java) | Template View |
| ERB (Rails/Ruby) | Template View |
| Jinja2 (Django/Flask/Python) | Template View |
| Django templates | Template View |
| Razor (.NET) | Template View |
| Blade (Laravel/PHP) | Template View |
| Handlebars / Mustache | Template View |
| Twig (PHP) | Template View |
| XSLT | Transform View |
| React SSR (server-side render) | Transform View (render function = element-by-element transform) |
| Vue SSR | Transform View |
| JSON serializer classes / DTO presenters | Transform View |
| GraphQL resolvers | Transform View |
| Next.js layouts + page components | Two Step View (layout = stage 2; page = stage 1) |
| Rails application layout + partials | Two Step View (application.html.erb = stage 2) |
| Design-system component library | Two Step View (component library = stage 2) |

## Application Controller Modern Equivalents

| PEAA concept | Modern equivalent |
|---|---|
| Application Controller (wizard flows) | React Router with step-state + form wizard libraries |
| Application Controller (approval flows) | BPM engines: Camunda, Activiti |
| Application Controller (long-running workflows) | Temporal, AWS Step Functions |
| Application Controller (onboarding flows) | Next.js App Router parallel routes + intercepting routes |
| Application Controller (domain commands collection) | Command pattern or service method map |
| Application Controller (view references collection) | Route name → component map |

## SPA + API Architecture Note

When a React/Vue/Angular SPA calls a JSON API backend:
- **Backend:** Front Controller (API router) + Transform View (JSON serializer) — Fowler's server-side MVC fully applies
- **Frontend:** Browser-side MVC — React component model, Vue reactivity system, Angular services are all browser-side MVC variants
- These are SEPARATE instances of the MVC idea. Do not conflate them.
- The "model" is different: server model = domain objects; client model = component state or store (Zustand, Redux, Pinia)
