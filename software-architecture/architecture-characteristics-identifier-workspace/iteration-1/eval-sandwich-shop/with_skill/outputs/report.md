# Architecture Characteristics: National Online Sandwich Ordering Platform

## Domain Concerns

| Concern | Source | Mapped Characteristics |
|---------|--------|----------------------|
| Thousands to potentially millions of users | Business stakeholder (growth projection) | Scalability, performance |
| Mealtime rush traffic (11:30-1:00 daily) | Business stakeholder (operational pattern) | Elasticity, performance, availability |
| Franchise-specific menu customization (200 locations, different owners) | Business stakeholder (franchise model) | Customizability/configurability, extensibility |
| Online payment processing | Business stakeholder (revenue model) | Security, reliability |
| European expansion next year | Business stakeholder (growth strategy) | Localization, legal, scalability, data residency |
| Keep labor costs low | Corporate stakeholder (cost reduction) | Simplicity, feasibility, maintainability |
| Transition from phone to online orders | Business stakeholder (digital transformation) | Availability, usability |

## Identified Characteristics

### Explicit (from requirements)

| Characteristic | Source Requirement | Reasoning |
|---------------|-------------------|-----------|
| **Scalability** | "Thousands of users initially, maybe millions" | The system must handle a user base that could grow by 2-3 orders of magnitude. This isn't a vague aspiration — they've stated a concrete growth trajectory that requires architectural support for horizontal scaling. |
| **Elasticity** | "Everyone orders between 11:30-1:00" | This is NOT the same as scalability. Scalability handles growth over time; elasticity handles spikes within a single day. A 90-minute lunch rush means the system goes from low traffic to peak traffic and back in a short window. The architecture must burst resources up and release them, not just scale permanently. This is the most architecturally significant requirement because it combines time pressure (mealtime) with business criticality (peak revenue window). |
| **Customizability / Configurability** | "Each franchise wants their own specials and menu customization" with "200 franchise locations, each with a different owner" | 200 independent franchise owners each need to control their own menus, specials, and pricing. This isn't a simple config file — it's a multi-tenant customization problem where each tenant has autonomy. This influences architecture: do you use a microkernel with franchise-specific plugins? A template system? A rules engine? The answer shapes the entire system structure. |
| **Performance** | "Mealtime rush" + online ordering expectations | During the 90-minute lunch rush, users expect sub-second response times for browsing menus and placing orders. Slow ordering during the only window that matters (lunch) directly translates to lost revenue. Combined with elasticity, this means the system must be fast WHILE scaling up. |
| **Localization** | "Plans to expand to Europe next year" | European expansion means multi-language support, multi-currency (EUR, GBP, etc.), date/time formatting, and potentially different menu regulatory requirements (allergen labeling laws differ by country). This must be considered now at the architecture level — retrofitting localization into a system designed for US-only is extremely expensive. |
| **Legal** | "Plans to expand to Europe next year" + "accept payments online" | GDPR compliance for European users, PCI-DSS for payment processing, and potentially different food safety/labeling regulations per country. These aren't just policy decisions — they require structural support for data residency, consent management, and audit trails. |

### Implicit (from domain knowledge)

| Characteristic | Reasoning |
|---------------|-----------|
| **Availability** | An online ordering platform that goes down during lunch rush is worse than useless — it's actively harmful because users have been redirected from phone ordering. If the system is unavailable during the 90-minute revenue window, the franchise loses that day's online orders entirely. High availability during peak hours is non-negotiable even though no one explicitly stated it. |
| **Reliability** | Orders involve real money and real food preparation. A dropped order means a customer doesn't get lunch, a franchise prepares food no one pays for, or a customer pays for food they never receive. Order integrity — ensuring every placed order is accurately received and processed — requires reliability at the architecture level. |
| **Security** | Online payment processing is explicitly mentioned. While payment processing itself is typically handled by a third-party processor (Stripe, Square, etc.), the system still handles personally identifiable information, delivery addresses, and payment tokens. The question is whether security rises to architecture level or stays at design level (evaluated in Step 4). |

## Three-Criteria Validation

| Characteristic | Nondomain? | Influences Structure? | Critical? | Verdict |
|---------------|:---:|:---:|:---:|---------|
| **Scalability** | Yes | Yes — requires decisions about stateless services, database sharding/partitioning, caching layers, load balancing strategy | Yes — system must handle 1000x growth | **Include** |
| **Elasticity** | Yes | Yes — requires auto-scaling infrastructure, queue-based load leveling, circuit breakers for burst absorption | Yes — the entire revenue model depends on the lunch rush window | **Include** |
| **Customizability** | Yes | Yes — requires multi-tenant architecture with per-franchise configuration (microkernel pattern, feature flags, or template engine). This is NOT solvable with just good code design. | Yes — 200 independent franchise owners each needing control is a core business requirement | **Include** |
| **Performance** | Yes | Partially — performance tuning is often a design/implementation concern (caching, query optimization). However, at this scale during burst traffic, performance requires structural support (CDN strategy, read replicas, async processing). | Yes — slow ordering during lunch rush = lost revenue | **Include** |
| **Availability** | Yes | Yes — requires redundancy, health checks, failover strategies, multi-AZ deployment | Yes — downtime during lunch = total revenue loss for that window | **Include** |
| **Reliability** | Yes | Yes — requires idempotent order processing, message durability, transaction management, dead-letter queues | Yes — lost or duplicated orders destroy customer trust | **Include** |
| **Security** | Yes | Partially — payments are handled by third-party processors (Stripe, etc.), which means the heaviest security burden is externalized. The system needs standard security practices (HTTPS, token management, input validation) but these don't require SPECIAL architectural structure beyond standard best practices. | Yes, but handled primarily by the payment processor | **Design-only** — Standard security best practices at the design/implementation level. Does not require special architectural structure because payment processing is delegated to a certified third-party. |
| **Localization** | Yes | Yes — requires internationalization framework baked into the UI layer, multi-currency support in the pricing engine, locale-aware data formatting | Important but not yet critical — expansion is "next year" | **Include** (but lower priority — design the hooks now, implement later) |
| **Legal** | Yes | Yes — GDPR requires data residency decisions, consent management, right-to-deletion support at the data layer | Important for European expansion | **Include** (but lower priority — same timeline as localization) |
| **Simplicity** | Yes | Yes — simpler architectures are cheaper to operate and maintain | Desired (cost reduction) but conflicts with other drivers | **Acknowledged** — Cannot be a driver given the complexity demands of elasticity, customizability, and scalability. Pursue simplicity within each component, not as a system-level constraint. |

## Categorization

| Category | Characteristics |
|----------|----------------|
| **Operational** | Scalability, elasticity, performance, availability, reliability |
| **Structural** | Customizability/configurability, localization |
| **Cross-Cutting** | Legal, security (design-level) |

**Balance check:** The list skews operational, which makes sense for a high-traffic, burst-pattern consumer platform. The structural category has customizability, which is arguably the most architecturally interesting characteristic here (it drives the choice between microkernel, multi-tenant patterns, etc.). Cross-cutting is light because the system delegates payment security to third parties and legal concerns are deferred to the European expansion phase.

## Top 3 Driving Characteristics

1. **Elasticity** — This is the single most architecturally significant characteristic. The lunch rush pattern (low traffic -> extreme spike -> low traffic, every day, predictably) is the defining technical challenge. Scalability handles growth over months; elasticity handles the daily 11:30-1:00 tsunami. If the architecture can't burst to handle peak lunch traffic and release those resources after, the platform fails at its most critical moment. Every architectural decision (stateless services, queue-based ordering, auto-scaling groups, caching strategy) flows from this requirement.

2. **Scalability** — The system must grow from thousands to potentially millions of users. This isn't just "add more servers" — it requires architectural decisions about data partitioning (per-franchise? per-region?), stateless service design, database strategy (read replicas, sharding), and CDN usage. Scalability and elasticity are related but distinct: scalability is the long-term growth trajectory, elasticity is the daily burst pattern. Both must be addressed architecturally.

3. **Customizability / Configurability** — 200 franchise owners, each with different menus, specials, and pricing, each wanting control. This is the characteristic that most influences the system's internal structure. It pushes toward a microkernel architecture (core ordering engine + franchise-specific plugins/configuration) or a sophisticated multi-tenant configuration system. Without architectural support for customizability, every franchise change becomes a code deployment — which at 200 locations is operationally untenable. This is where the architecture-vs-design trade-off is most interesting: a Template Method pattern (design level) might suffice for simple menu differences, but a microkernel (architecture level) is needed if franchises want fundamentally different workflows.

### Acknowledged but not driving

- **Availability:** Critical during lunch rush, but availability is largely an infrastructure concern (multi-AZ deployment, health checks, auto-scaling) that follows naturally from elasticity design. It doesn't independently drive architecture decisions beyond what elasticity already demands.
- **Reliability:** Important for order integrity, but handled through standard patterns (idempotent APIs, message queues with guaranteed delivery, database transactions). These are strong design practices that don't require a fundamentally different architecture.
- **Performance:** Closely coupled with elasticity. If the system handles burst traffic correctly (elasticity), performance during peak hours follows. Performance tuning (caching, query optimization, CDN) is primarily a design/implementation concern.
- **Localization:** Important for European expansion but not yet a driver. The architecture should be localization-ready (externalized strings, locale-aware formatting, multi-currency data model) but full implementation is deferred.
- **Legal:** GDPR and data residency matter for European expansion. Design the data layer to support regional isolation, but don't let it drive current architecture decisions.

## Characteristics NOT Included (and why)

- **Security:** Failed criterion 2 (doesn't require special architectural structure) for this system. Payment processing is delegated to a PCI-DSS-compliant third-party processor. The system needs standard security best practices (HTTPS, input validation, secure token storage, OWASP compliance) but these are design/implementation concerns, not architecture drivers. If the company were building its own payment processing, security would absolutely be an architecture characteristic.
- **Simplicity:** Conflicts with the driving characteristics. A system that must be elastic, scalable, AND customizable per-franchise is inherently complex. Simplicity is a goal within each component (keep individual services simple) but cannot be a system-level architecture driver without compromising the top 3.
- **Usability:** Important for user adoption but is a design concern (UI/UX), not an architecture characteristic. It doesn't influence the system's structural decisions.
- **Deployability:** Desirable (faster deployments = faster franchise customization updates) but doesn't independently drive architecture decisions. It's a secondary benefit of the microkernel/modular approach driven by customizability.

---

## Notes for Next Steps

This characteristics report serves as input for:
- **Architecture style selection:** The combination of elasticity + scalability + customizability strongly suggests evaluating microkernel (for franchise customization) combined with event-driven or microservices (for elasticity/scalability). A monolithic approach would struggle with all three drivers simultaneously.
- **Fitness function design:** Define measurable fitness functions for each driving characteristic (e.g., "system must scale from baseline to 10x within 2 minutes of load increase" for elasticity, "new franchise menu configuration deployable in <1 hour without code changes" for customizability).
- **Trade-off analysis:** The customizability driver presents the most interesting trade-off: microkernel architecture provides maximum franchise flexibility but adds operational complexity. A simpler template-based approach reduces complexity but may not satisfy franchise owners who want fundamentally different workflows.
