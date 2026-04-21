# Pattern Stack Decision Table

Quick-reference routing table for the enterprise-architecture-pattern-stack-selector skill.

## Domain Logic → Data Source Routing

| Domain Logic Pattern | Data Source Pattern(s) | Behavioral Patterns Needed | Notes |
|---|---|---|---|
| **Transaction Script** | Table Data Gateway (when platform has Record Set tooling) | Optional: Unit of Work | Keep scripts thin; extract DB access to a Gateway |
| **Transaction Script** | Row Data Gateway (typed, explicit interface per row) | Optional: Unit of Work | Use when no Record Set tooling; each row = one object |
| **Table Module** | Table Data Gateway | Rarely needed — Record Set carries state | Natural match; Record Set IS the in-memory representation |
| **Domain Model (simple)** | Active Record (object persists itself) | None required | Works when schema closely mirrors the object model |
| **Domain Model (complex)** | Data Mapper (separate mapping layer; use ORM) | **Unit of Work** (required), **Identity Map** (required), Lazy Load (recommended) | ORM (Hibernate, EF Core, SQLAlchemy) provides all three |

## Concurrency Strategy Selection

| Scenario | Pattern |
|---|---|
| Multi-request edit → save (default) | Optimistic Offline Lock (version column / ETag) |
| High conflict rate + late failure unacceptable | Pessimistic Offline Lock (check-out / record lock) |
| Lock an aggregate root + all children | Coarse-Grained Lock (with either optimistic or pessimistic) |
| Team must not forget to acquire locks | Implicit Lock (framework-enforced) |

## Session State Selection

| Scenario | Pattern |
|---|---|
| Small payload; stateless servers; maximum scalability | Client Session State (cookie / JWT / URL token) |
| Large payload; sensitive data; server affinity acceptable | Server Session State (server-memory session) |
| Session must survive server restart / failover | Database Session State (persisted to DB) |

## Web Presentation Routing

| Navigation Complexity | Controller Pattern | View Pattern |
|---|---|---|
| Simple, document-oriented site | Page Controller | Template View |
| Complex navigation, shared pre/post-processing | Front Controller | Template View |
| Multi-step workflows / state machine navigation | Front Controller + Application Controller | Template View |
| Multiple site skins / layouts from single content | Front Controller | Two Step View |
| XSLT-savvy team; high testability priority | Front Controller | Transform View |

## Fowler's First Law of Distributed Object Design

> "Don't distribute your objects." — Ch. 7

Only introduce a process boundary when forced by:
- Different security domains
- Different deployment lifecycles (separate teams deploying independently)
- Hard hardware constraints (separate machines required)
- Integration with external systems (use Remote Facade + DTO at the boundary)

When a boundary IS required:
- Wrap the domain layer with **Remote Facade** (coarse-grained service methods only)
- Use **Data Transfer Object** to carry data across the boundary
- Never expose fine-grained domain objects to a remote caller
