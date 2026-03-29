# Architecture Style Comparison Matrix

> Source: Fundamentals of Software Architecture (Richards & Ford), Chapters 10-17
> Each characteristic rated 1-5 (1 = poorly supported, 5 = strongest feature)

## Complete Ratings Table

| Characteristic | Layered | Pipeline | Microkernel | Service-Based | Event-Driven | Space-Based | Microservices |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Partitioning** | Technical | Technical | Domain/Tech | Domain | Technical | Domain | Domain |
| **Quanta** | 1 | 1 | 1 | 1 to many | 1 to many | 1 | 1 to many |
| **Deployability** | 1 | 2 | 3 | 4 | 3 | 3 | 4 |
| **Elasticity** | 1 | 1 | 1 | 2 | 3 | 5 | 5 |
| **Evolutionary** | 1 | 3 | 3 | 3 | 5 | 3 | 5 |
| **Fault tolerance** | 1 | 1 | 1 | 4 | 5 | 3 | 4 |
| **Modularity** | 1 | 3 | 3 | 4 | 4 | 3 | 5 |
| **Overall cost** | 5 | 5 | 5 | 4 | 3 | 2 | 1 |
| **Performance** | 2 | 2 | 3 | 3 | 5 | 5 | 2 |
| **Reliability** | 3 | 3 | 3 | 4 | 3 | 4 | 4 |
| **Scalability** | 1 | 1 | 1 | 3 | 5 | 5 | 5 |
| **Simplicity** | 5 | 5 | 4 | 3 | 1 | 1 | 1 |
| **Testability** | 2 | 3 | 3 | 4 | 2 | 1 | 4 |

> Note: Orchestration-driven SOA is intentionally excluded. The book treats it as a historical pattern with known coupling problems. If evaluating SOA, see Chapter 16.

---

## Style Profiles

### Monolithic Styles

#### Layered Architecture
- **Topology:** Presentation → Business → Persistence → Database (closed layers by default)
- **Best for:** Small/simple applications, tight budgets, teams still analyzing requirements, starting points when style is undecided
- **Strengths:** Simplicity (5), cost (5), reliability (3)
- **Weaknesses:** Deployability (1), elasticity (1), scalability (1), fault tolerance (1), modularity (1), evolutionary (1)
- **Anti-pattern:** Architecture Sinkhole — requests pass through layers with no processing. Use the 80-20 rule: acceptable if <20% of requests are sinkholes. If >80%, this is the wrong style.
- **Key trade-off:** Easy to understand and build, but degrades quickly as applications grow larger

#### Pipeline Architecture
- **Topology:** Source → Filter → Filter → ... → Sink (unidirectional data flow)
- **Best for:** ETL tools, data transformations, orchestration engines, shell command chains, content processing
- **Strengths:** Simplicity (5), cost (5), modularity (3)
- **Weaknesses:** Elasticity (1), scalability (1), fault tolerance (1), performance (2)
- **Anti-pattern:** Forcing bidirectional data flow into a unidirectional pipeline
- **Key trade-off:** Excellent for linear processing workflows but cannot handle complex interaction patterns
- **Isomorphism:** Problems with linear data transformation stages naturally map to this style

#### Microkernel Architecture
- **Topology:** Core system + plug-in components (compile-time or runtime)
- **Best for:** Product-based applications with high customizability, IDE-like systems, insurance rules engines, tax software, workflow engines
- **Strengths:** Cost (5), simplicity (4), testability (3), deployability (3)
- **Weaknesses:** Elasticity (1), scalability (1), fault tolerance (1)
- **Anti-pattern:** Plug-in dependencies on each other (violates independence)
- **Key trade-off:** Excellent extensibility through plug-ins, but limited to single quantum (monolithic core)
- **Isomorphism:** Any problem requiring high customizability or regional/client variations naturally maps here

### Distributed Styles

#### Service-Based Architecture
- **Topology:** 4-12 coarse-grained domain services + shared database + separately deployed UI
- **Best for:** Pragmatic distributed systems, teams transitioning from monolith, domain-driven applications needing some distribution benefits without full microservices complexity
- **Strengths:** Deployability (4), fault tolerance (4), modularity (4), reliability (4), testability (4), cost (4)
- **Weaknesses:** Elasticity (2), scalability (3)
- **Anti-pattern:** Creating too many services (>12, becoming accidental microservices) or too few (<3, becoming a distributed monolith)
- **Key trade-off:** Best balance of distributed benefits vs operational complexity. The "pragmatic middle ground." ACID transactions still possible within services due to shared database.
- **Unique advantage:** Preserves database-level ACID transactions while gaining independent deployability

#### Event-Driven Architecture
- **Topology:** Broker topology (no central mediator, events flow freely) or Mediator topology (central orchestrator coordinates events)
- **Best for:** High-performance, highly scalable systems with complex event processing, real-time systems, IoT platforms
- **Strengths:** Performance (5), scalability (5), fault tolerance (5), evolutionary (5)
- **Weaknesses:** Simplicity (1), testability (2), overall cost (3)
- **Broker vs Mediator:**
  - **Broker:** Higher decoupling, better performance, but no central error handling or workflow control
  - **Mediator:** Better error handling and workflow control, but introduces coupling and potential bottleneck
- **Anti-pattern:** Using broker for complex workflows requiring error handling, or mediator for simple event notifications
- **Key trade-off:** Highest performance and scalability of any style, but hardest to test and reason about (eventual consistency, race conditions)

#### Space-Based Architecture
- **Topology:** Processing units with in-memory data grids, messaging grid, data pumps to persistent storage
- **Best for:** Systems with extreme and unpredictable scalability/elasticity needs — concert ticketing, auction systems, social media events
- **Strengths:** Elasticity (5), scalability (5), performance (5)
- **Weaknesses:** Simplicity (1), testability (1), overall cost (2)
- **Anti-pattern:** Using for systems with normal, predictable load patterns (massive over-engineering)
- **Key trade-off:** Can handle virtually unlimited scale through in-memory processing, but extremely expensive and complex to build and test
- **When it shines:** Variable load that would be cost-prohibitive to provision for peak with traditional architectures

#### Microservices Architecture
- **Topology:** Fine-grained, independently deployable services, each with its own database (bounded context), communicating via REST/messaging
- **Best for:** Maximum independent deployability, evolutionary architecture, large teams needing autonomy, systems requiring different technology stacks per service
- **Strengths:** Scalability (5), elasticity (5), evolutionary (5), modularity (5), deployability (4), fault tolerance (4), testability (4)
- **Weaknesses:** Overall cost (1), simplicity (1), performance (2)
- **Anti-patterns:**
  - Enforced heterogeneity (mandating different tech stacks per service)
  - Too fine-grained services (more communication overhead than benefit)
  - Transactions across service boundaries (fix granularity instead!)
- **Key trade-off:** Maximum flexibility and scalability, but maximum operational complexity and cost. Requires mature DevOps practices.
- **Granularity guidance:** "Microservice" is a label, not a description (Martin Fowler). Service boundaries should capture a domain or workflow — use Purpose, Transactions, and Choreography to find boundaries.

---

## Quick Selection Guide

### By Primary Driving Characteristic

| If you need... | Consider first | Consider second |
|---|---|---|
| **Scalability** | Microservices, Event-driven | Space-based |
| **Elasticity** | Space-based, Microservices | Event-driven |
| **Performance** | Event-driven, Space-based | Pipeline (for data processing) |
| **Simplicity** | Layered, Pipeline | Microkernel |
| **Low cost** | Layered, Pipeline, Microkernel | Service-based |
| **Deployability** | Microservices, Service-based | Event-driven |
| **Fault tolerance** | Event-driven, Microservices | Service-based |
| **Evolutionary** | Microservices, Event-driven | Service-based |
| **Testability** | Microservices, Service-based | Microkernel, Pipeline |
| **Customizability** | Microkernel | Service-based |
| **Reliability** | Service-based, Microservices | Space-based |

### By Domain Isomorphism

| Domain pattern | Natural fit |
|---|---|
| Linear data processing, ETL | Pipeline |
| High customization, plug-in rules | Microkernel |
| Small/simple CRUD application | Layered |
| Pragmatic business application | Service-based |
| Real-time event processing | Event-driven |
| Extreme/variable scalability needs | Space-based |
| Maximum team autonomy + independent scaling | Microservices |
| Highly coupled domain (e.g., multi-page forms) | Service-based or Layered (NOT microservices) |

### By Organizational Context

| Context | Recommended |
|---|---|
| Small team (<10), tight budget | Layered or Microkernel |
| Medium team, needs some distribution | Service-based |
| Large team (30+), mature DevOps | Microservices or Event-driven |
| Unknown requirements, starting point | Layered (then migrate) |
| Must deliver fast, iterate later | Service-based |
