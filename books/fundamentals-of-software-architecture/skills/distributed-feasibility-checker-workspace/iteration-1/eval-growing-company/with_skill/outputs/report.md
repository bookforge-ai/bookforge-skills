# Feasibility Assessment: Java Monolith (Growing Company)

## Motivation Analysis

**Stated motivation:** Deployments take 90 minutes (twice a week), and the search feature needs to handle 10x more traffic than the rest of the application.

**Validated motivation:** Valid

**Underlying problem:** Two distinct, legitimate pain points: (1) deployment coupling — all 35 developers across 4 teams must coordinate around a single 90-minute deployment window, which limits deployment frequency and creates risk; (2) differential scaling — search has a quantifiably different scaling requirement (10x) from the rest of the system, meaning the monolith forces over-provisioning the entire application or under-serving search. These are textbook drivers for distribution.

## 8 Fallacies Evaluation

| # | Fallacy | Team Awareness | Mitigations in Place | Risk Level |
|---|---------|:-:|:-:|:-:|
| 1 | **Network Is Reliable** | No | None evident. Running as a monolith means no inter-service calls today. No mention of circuit breakers, retry policies, or timeout strategies. | **High** |
| 2 | **Latency Is Zero** | No | None. All calls are currently in-process (local method calls with near-zero latency). The team has no experience measuring or managing network call latency. If search is extracted, every query becomes a network hop. | **High** |
| 3 | **Bandwidth Is Infinite** | No | None. As a monolith, data passes by reference in memory. Distribution would require serializing data across the wire. Risk of stamp coupling (sending full objects when only IDs are needed) is high for a team new to distributed design. | **Medium** |
| 4 | **Network Is Secure** | Uncertain | Kubernetes provides some network isolation via namespaces/network policies, but there's no mention of service-to-service authentication (mTLS), API gateway security, or secrets management beyond what K8s offers by default. | **Medium** |
| 5 | **Topology Never Changes** | Partially | Kubernetes handles service discovery and topology changes natively (DNS-based service discovery, pod rescheduling). This is a genuine advantage of their existing infrastructure. However, the team may not understand K8s networking deeply enough to troubleshoot failures. | **Low** |
| 6 | **There Is Only One Administrator** | Partially | 4 teams exist, suggesting some organizational separation. However, with a single monolith and single Jenkins pipeline, there is effectively one deployment administrator. Distribution would require coordinating infrastructure ownership across teams. | **Medium** |
| 7 | **Transport Cost Is Zero** | No | None. No experience budgeting for service mesh, API gateways, load balancers between services, or the additional compute/memory overhead of serialization/deserialization. Current infrastructure costs reflect monolith-level simplicity. | **Medium** |
| 8 | **Network Is Homogeneous** | N/A | Running on Kubernetes in a single environment suggests homogeneous networking. Low risk unless they go multi-cloud or hybrid. | **Low** |

**Fallacy readiness score: 1/8 mitigated** (only Fallacy #5 partially addressed by Kubernetes)

## Operational Readiness

| Capability | Status | Gap |
|-----------|:-:|-----|
| **Distributed logging** | Not Ready | ELK stack exists but is described as "basic." No mention of correlation IDs, structured logging, or cross-service log correlation. ELK can be extended, but it needs intentional work to support distributed tracing of requests across services. |
| **Distributed tracing** | Not Ready | No distributed tracing infrastructure (no Jaeger, Zipkin, or Datadog APM mentioned). This is the single biggest operational gap — without tracing, debugging a request that spans services becomes guesswork. |
| **CI/CD per service** | Not Ready | Jenkins CI is in place, but for a monolith. No per-service pipelines, no independent versioning, no canary/blue-green deployment strategy mentioned. Jenkins can support multi-pipeline setups, but it requires significant reconfiguration. |
| **Service discovery** | Ready | Kubernetes provides built-in service discovery via DNS. This is a genuine strength — K8s-native service discovery eliminates the need for a separate service registry. |
| **Contract management** | Not Ready | No API versioning strategy, no consumer-driven contract tests, no schema registry. With 4 teams, breaking changes between services will cause outages without contract management. |
| **Monitoring & alerting** | Not Ready | Basic ELK for logs but no per-service health checks, no SLO dashboards, no service-level alerting. Cannot detect when one service is degrading vs. overall system health. |

**Operational readiness score: 1/6 capabilities in place** (service discovery via Kubernetes)

## Simpler Alternatives Considered

| Alternative | Solves the Problem? | Why / Why Not |
|------------|:-:|-------------|
| **Modular monolith** | Partially | Would solve the deployment pain if modules can be built and tested independently, reducing the 90-minute build. Would improve team autonomy by establishing clear module boundaries. However, does NOT solve the 10x search scaling requirement — the entire monolith still deploys and scales as one unit. |
| **Single service extraction (search only)** | Yes | Extracting ONLY the search feature as a separate service directly addresses both problems: (1) search scales independently to handle 10x traffic, (2) remaining monolith deployments become faster without search code, and search deploys on its own cadence. This is the strangler fig pattern — low risk, high impact, and a learning opportunity for the team. |
| **Better code boundaries** | No | Code organization improvements would help team autonomy but do not address the scaling disparity or deployment duration. The problems are architectural, not organizational. |

## Recommendation

**Conditional Go — Extract Search as a Single Service (Strangler Fig Pattern)**

- **Do NOT attempt full microservices.** With only 2 developers who have prior (not current) distributed experience, a fallacy readiness of 1/8, and operational readiness of 1/6, a broad migration to microservices would almost certainly produce a distributed monolith — the worst possible outcome.

- **The search extraction is justified and contained.** The 10x scaling requirement is a concrete, measurable need that cannot be solved by a modular monolith. Search is a natural bounded context — it reads data but rarely writes, making it an ideal first extraction with minimal data coupling concerns.

- **The deployment pain has a simpler partial fix.** Modular monolith restructuring (build parallelization, independent module testing) can reduce the 90-minute deployment significantly. Pursue this in parallel with the search extraction rather than using deployment pain as justification for broader distribution.

- **Two experienced developers are an asset, but not enough.** They should lead the search extraction and use it to train 2-3 others. Do not proceed without at least a 4-person team that understands distributed operations.

## If Proceeding: Readiness Roadmap

1. **Implement distributed tracing (4-6 weeks).** Deploy Jaeger or similar on Kubernetes. Instrument the monolith with tracing headers NOW, before extraction. This way, when search becomes a separate service, you can trace requests end-to-end from day one. This is non-negotiable — without it, you cannot debug distributed failures.

2. **Upgrade ELK to support correlation IDs (2-3 weeks, parallel with #1).** Add a correlation ID to every request at the API gateway level. Propagate it through logs. This transforms "basic ELK" into distributed-aware logging.

3. **Build a per-service CI/CD pipeline for search (3-4 weeks).** Set up an independent Jenkins pipeline (or migrate search to a modern CI like GitHub Actions) with its own build, test, and deploy stages. Include canary deployment capability on Kubernetes.

4. **Establish API contract between search and the monolith (2-3 weeks).** Define a versioned API. Implement consumer-driven contract tests. This prevents the #1 cause of distributed system outages: uncoordinated API changes.

5. **Extract the search service using the strangler fig pattern (6-8 weeks).** Route search traffic to the new service via an API gateway or Kubernetes ingress rules. Keep the old search code in the monolith as a fallback. Gradually shift traffic (10% → 50% → 100%).

6. **Operate the two-service system for 3-6 months before considering further extraction.** Use this period to build team muscle memory for distributed operations, refine monitoring, and validate that the operational overhead is manageable. Only then evaluate whether further distribution is warranted.

**Total estimated timeline to search extraction: 4-5 months** (steps 1-4 in parallel where possible, step 5 sequential, step 6 is observation period).

**Key risk to monitor:** If the search extraction takes longer than 5 months or requires more than 6 developers, it signals the team is not ready for further distribution. Consolidate and strengthen the two-service architecture before expanding.
