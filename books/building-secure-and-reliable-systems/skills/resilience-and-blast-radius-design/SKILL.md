---
name: resilience-and-blast-radius-design
description: Design or audit a system's resilience posture using a layered framework — defense in depth, controlled degradation (load shedding vs. throttling), blast radius compartmentalization (role/location/time), failure domains, 3-tier component reliability hierarchy, and continuous validation. Use this skill when designing a new system for failure, reviewing an existing architecture for single points of failure, limiting blast radius of a potential attack or outage, deciding fail-open vs. fail-closed behavior for a component, or building an incident-response-ready compartmentalization strategy.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/resilience-and-blast-radius-design
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [8]
tags: [security, reliability, resilience, blast-radius, defense-in-depth, fault-tolerance, compartmentalization, load-shedding, failure-domains]
depends-on: []
execution:
  tier: 2
  mode: full
  inputs:
    - type: context
      description: "System architecture description, component list, or incident post-mortem. May also be a design proposal or existing runbook."
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Works from a system description, architecture diagram, or design document. Output: resilience assessment report with failure domain map, component tier assignments, compartmentalization recommendations, and prioritized implementation roadmap."
discovery:
  goal: "Produce a resilience assessment that identifies single points of failure, assigns component reliability tiers, maps blast radius exposure, recommends compartmentalization boundaries, and delivers a cost-ordered implementation roadmap."
  tasks:
    - "Audit defense-in-depth coverage across all attack stages"
    - "Identify degradation control strategy (load shedding vs. throttling) and fail-open/closed posture for each critical component"
    - "Map compartmentalization axes: role, location, and time separation"
    - "Assign each component to a reliability tier: high-capacity, high-availability, or low-dependency"
    - "Define failure domains and evaluate redundancy strategy"
    - "Design or review continuous validation coverage"
    - "Produce a prioritized implementation roadmap using the cost-ordered sequence"
  audience: "engineers, SREs, security engineers, and architects at intermediate-to-advanced level"
  when_to_use: "When designing a new system for resilience, reviewing an existing architecture for weaknesses, limiting blast radius, deciding fail-open vs. fail-closed policy, or preparing for incident response"
  environment: "System architecture or design document. Knowledge of critical user-facing features and their dependencies is needed for degradation planning."
  quality: placeholder
---

# Resilience and Blast Radius Design

## When to Use

Apply this skill when:

- Designing a new system and want to build resilience in from the start
- Reviewing an existing architecture for single points of failure, over-broad blast radius, or missing degradation controls
- Deciding whether a component should fail open (availability) or fail closed (security)
- Planning compartmentalization to limit the impact of a security breach or operational outage
- Preparing an incident response strategy that requires quarantining a subsystem without taking everything offline
- Evaluating whether alternative/backup components are likely to work when actually needed

**The core pattern:** resilience is not a single mechanism — it is five cooperating layers: (1) defense in depth across attack stages, (2) controlled degradation under load, (3) blast radius compartmentalization, (4) failure domains with component-tier redundancy, and (5) continuous validation that the other four still work.

Before starting, confirm you have:
- A description of the system's architecture or the component under review
- An understanding of which features are critical to users (needed for degradation planning)
- A sense of the organization's risk tolerance and operational capacity (needed for tier selection)

---

## Context and Input Gathering

### Required Context

- **System description:** Architecture diagram, design document, or prose description of the system's components and their dependencies.
- **Critical features list:** Which capabilities must stay available even under severe degradation? Which can be throttled or disabled?
- **Threat model (if available):** What types of attackers or failure modes are most likely? This shapes compartmentalization priorities.

### Observable Context

If a system description is provided, scan for:
- Components that are dependencies of many other components — single points of failure
- Components with no alternative implementation — missing redundancy tiers
- Features that require the same network, credentials, or configuration as security controls — fail-open risk
- Backup or alternative components that are never exercised in production — zombie backup risk
- No log-based boundary validation — compartmentalization that cannot be verified

### Default Assumptions

- If fail-open vs. fail-closed is unspecified: ask — this is a security-vs-reliability tradeoff that requires a deliberate organizational decision
- If no degradation strategy exists: default to identifying the top 3 most expensive operations and the top 3 most critical operations as starting points
- If no component tiers are defined: assign all components to high-capacity tier initially, then identify candidates for high-availability and low-dependency promotion
- If no compartmentalization exists: start with role separation (cheapest) before location or time separation

### Sufficiency Check

You have enough to proceed when:
1. You can enumerate the system's major components and their dependencies
2. You know which features are non-negotiable under load
3. You know whether the primary risk is availability (prefer fail-open) or integrity/security (prefer fail-closed)

---

## Process

### Step 1 — Audit Defense in Depth Coverage

Defense in depth protects systems by establishing multiple independent defense layers, so that a failure in any single layer does not result in a complete compromise.

Map the system against the four stages of an attack or failure:

| Stage | What defenders must address |
|---|---|
| Threat modeling and vulnerability discovery | Limit information exposed to attackers; detect reconnaissance signals |
| Deployment / delivery of an exploit | Validate and inspect anything entering the system boundary (supply chain, third-party dependencies, user-supplied content) |
| Execution | Sandbox, isolate, and limit blast radius so execution cannot escape to adjacent systems |
| Compromise | Ensure detection and response are possible; limit how long an attacker can maintain access |

**For each stage, ask:** What defensive measures exist? If this layer fails, what catches the next stage?

**Why:** Each layer buys time and increases attacker cost. Layers should be complementary — each should anticipate the likely failure modes of the layer before it. A single perimeter with no inner defenses is brittle; inner defenses should assume the outer perimeter has been breached.

**Supply chain dependency note:** Arbitrary third-party dependencies entering a trusted execution environment (e.g., untrusted code running alongside internal services) require an independent sandbox layer. If the sandbox fails, a second containment layer (such as syscall filtering) should catch what the sandbox missed.

**Output for this step:** A per-stage defense inventory with gaps marked.

---

### Step 2 — Design Controlled Degradation

When a system exceeds capacity or loses components, unplanned degradation typically causes a cascading failure. Controlled degradation replaces chaotic collapse with a pre-planned sequence of graceful reductions in service.

#### 2a — Classify Features by Criticality

Rank features by their value and their cost:
- **Non-negotiable under load:** Keep these active regardless of resource pressure (security controls, core user data access)
- **Throttleable:** High-value but not critical; delay or slow rather than drop
- **Sheddable:** Low-value or high-cost; return an error rather than serve

**Security and reliability tradeoff:** Security-critical operations should generally fail closed, not open. If a system cannot verify its integrity (e.g., ACLs fail to load), the safer default is "deny all," not "allow all." Determine the organization's minimum nonnegotiable security posture before designing degradation thresholds.

#### 2b — Choose: Load Shedding or Throttling

**Load shedding** (returning errors for excess requests):
- Goal: stabilize a component at maximum load, prevent crash
- When to use: when a component is approaching capacity and any excess request should be rejected rather than risk crashing the whole server
- How it works: assign request priority and cost; shed low-priority or high-cost requests first; security-critical functions get the highest shed priority (shed last)

**Throttling** (delaying responses to slow future request rate):
- Goal: reduce the rate at which clients send follow-up requests
- When to use: when clients will retry on failure and retries would compound the load problem
- How it works: introduce delay before responding so clients naturally slow their request cadence

**Automation controls:** Avoid allowing automation to make unsupervised large-magnitude changes (e.g., a single policy change affecting all servers). Implement a change budget: when automation exhausts its budget, a human must approve the next action. Prevent automated degradation controls from disabling emergency access paths (breakglass mechanisms, SSH fallback routes).

**Output for this step:** Feature criticality ranking, selected degradation mechanism per component, and automation budget policy.

---

### Step 3 — Map Compartmentalization (Blast Radius Control)

Compartmentalization divides the system into isolated units so that a breach or failure in one compartment does not jeopardize the others. Use three axes, applied in order of increasing implementation cost:

#### 3a — Role Separation (lowest cost)

- Run distinct services as distinct identities (service accounts / roles)
- A compromise of one role's credentials cannot be used to impersonate another role's services
- Even services developed and operated by the same team should use different roles if they access different classes of data

**Why:** Credential compromise is the most common attack escalation path. Role separation limits how far a single stolen credential can propagate.

#### 3b — Location Separation (medium cost)

- Run service instances in distinct physical or logical locations (datacenters, cloud regions, network segments)
- Ensure no service has a critical dependency on a backend that is homed in only one location
- Use location-bound cryptographic certificates: compromise of one location's keys should not expose other locations' data

**Physical location as a natural boundary:** Natural disasters, fiber cuts, and physical-presence attacks (tailgating, hardware implants) are all location-confined. Design so that a localized impact stays within its region while the multiregional system continues operating.

**Align physical and logical boundaries:** Segment networks on both network-level risk (internet-facing vs. internal) and physical risk (datacenter vs. office). Distribute secrets, credentials, and encryption keys per-location rather than sharing a single global secret across all servers.

#### 3c — Time Separation (ongoing discipline)

- Rotate credentials and encryption keys on a regular schedule and expire old ones
- Rotation forces an attacker who has stolen a credential to repeatedly re-acquire it, creating more opportunities for detection
- Regularly rotating keys also validates that rotation works — uncovering services that were never designed to handle rotation before an emergency requires it

**Key rotation validation targets:**
- *Key rotation latency:* How long does a full rotation cycle take? This is your incident response clock.
- *Verified loss of access:* Confirm old keys are fully revoked, not just replaced.

#### 3d — Compartment Granularity Tradeoff

Finer compartments (per-RPC-method) give tighter control but create N×M complexity in access policies. Coarser compartments (per-server) are easier to manage but offer less precision. The right granularity balances security benefit against operational overhead — consult incident management and operations teams when setting boundaries.

**Imperfect compartments still add value:** Any delay imposed on an attacker trying to escape a compartment is time for the incident response team to detect and react.

**Output for this step:** A compartmentalization map with role, location, and time boundaries identified. Flag any compartment violations that should be validated by log analysis.

---

### Step 4 — Define Failure Domains and Assign Component Tiers

Compartmentalization limits blast radius from attacks and operational failures. Failure domains extend this further by partitioning the system into independent functional copies, so that complete failure of one partition does not bring down the entire system.

#### 4a — Design Failure Domains

A failure domain is an independent partition that:
- Looks like the whole system to its clients
- Can take over for other partitions during an outage (at reduced capacity)
- Has its own data copy, isolated from other domains' data

**Practical minimum:** Even splitting into two failure domains provides significant value — it enables A/B regression isolation, limits blast radius of a configuration change to one domain, and enables geographic disaster isolation. Use one domain as a canary; enforce a policy that prohibits simultaneous updates to both domains.

**Data isolation within failure domains:**
- Restrict how new data enters a failure domain (validate before accepting)
- Preserve last-known-good configuration to disk so the domain can operate if its configuration API is unavailable
- Rate-limit global configuration changes to prevent a single bad push from affecting all domains simultaneously

#### 4b — Assign Component Reliability Tiers

Three tiers, each suited to different resilience requirements:

**Tier 1 — High-Capacity (standard production)**
- The main fleet serving normal user load
- Focus: capacity planning, rollout procedures, feature development
- Where to invest first — these components carry the most user impact

**Tier 2 — High-Availability (reduced-dependency copy)**
- A copy of a critical component configured with fewer dependencies and slower update cadence
- Uses locally cached data rather than remote databases; runs older (more stable) code versions
- Goal: provably lower probability of outage than the high-capacity version
- Operational cost: additional resource allocation proportional to fleet size

**Tier 3 — Low-Dependency (minimal fallback)**
- An alternative implementation with minimal dependencies, designed to survive infrastructure failures that would take down Tier 1 and Tier 2
- Supports only the most critical subset of features
- Dependencies must themselves be low-dependency; the alternative component and its critical dependency must not share a failure domain with the primary

**Anti-pattern — zombie backup:** Any component that grows to be treated as part of normal operation will be overloaded during an actual outage. Any component that is never exercised in normal operation will fail unexpectedly when needed. Both are backup drift problems. Mitigation: route a small fraction of real traffic through high-availability and low-dependency components continuously.

**Output for this step:** Component tier assignments table. Flag any component with no Tier 2 or Tier 3 fallback that has no acceptable outage window.

---

### Step 5 — Design Continuous Validation

Resilience mechanisms degrade silently over time. New features introduce dependencies that violate compartment boundaries. Backup components accumulate drift. Validation is the compounding interest on all other resilience investments — without it, the other four layers decay.

**Validation is distinct from chaos engineering:** Chaos engineering is exploratory. Validation confirms that specific, known-good properties still hold under controlled conditions.

**Core validation strategy:**
1. Discover new failures (from incident logs, bug reports, fuzzing, expert judgment)
2. Implement validators for each discovered failure mode
3. Execute all validators repeatedly on a schedule
4. Retire validators when the relevant feature or behavior no longer exists

**Validation techniques by component tier:**

| Situation | Technique |
|---|---|
| High-capacity and high-availability components | Request mirroring: send duplicate traffic to both, alert on unexpected response differences |
| Low-dependency components | Route on-call engineers through low-dependency paths as part of their normal duties — this validates readiness and builds familiarity |
| Compartment boundary enforcement | Log analysis: any operation that crosses a role, location, or time boundary should fail; unexpected successes should alert |
| Load shedding and throttling behavior | Inject simulated load or artificial behavior changes into servers; observe propagation through clients and backends |
| Key rotation | Measure rotation latency and confirm verified loss of access for old keys on a regular schedule |
| Resource release under oversubscription | Periodically exercise the actual resource rebalancing process — not a simulation — to confirm the SLO holds |

**Human factors in validation:** Recovery actions necessarily involve humans. Validate recovery instructions for readability. Validate that on-call engineers can actually execute emergency procedures — including using low-dependency systems — under realistic conditions.

**Output for this step:** Validation plan with method, trigger, and frequency per resilience property. Flag any resilience mechanism that has no associated validator.

---

### Step 6 — Produce the Resilience Assessment and Implementation Roadmap

Synthesize findings from Steps 1–5 into a structured report.

**Report sections:**
1. **Defense-in-depth gap inventory** — per-stage coverage and identified gaps
2. **Feature criticality ranking and degradation policy** — which features shed first, which stay active, fail-open vs. fail-closed decisions
3. **Compartmentalization map** — role, location, and time boundaries; compartment violations
4. **Failure domain map** — current domains, tier assignments per component, data isolation status
5. **Continuous validation coverage** — validators in place, gaps, and recommended additions
6. **Prioritized implementation roadmap** (see Key Principles below)

---

## Key Principles

### Prioritized Implementation Order (by cost-effectiveness)

When starting from scratch or limited in capacity, apply resilience improvements in this order:

1. **Failure domains and blast radius controls** — lowest ongoing cost due to their static nature; significant improvement in containment; make future bad designs harder to introduce
2. **High-availability component copies** — next most cost-effective; cheap to deploy, easy to abandon if not needed; provide a concrete measure of how much availability improvement is available
3. **Load shedding and throttling** — justified when organizational scale or risk aversion makes automation cost-effective; critically important for defending against denial-of-service attacks
4. **Denial-of-service defenses** — evaluate effectiveness of degradation controls against DoS scenarios specifically
5. **Low-dependency components** — most expensive; before investing, calculate how long it would take to bring up all dependencies of the business-critical service; compare that recovery time against the cost of the alternative

When budget or time runs out, streamline the efficiency of already-deployed mechanisms before adding new ones.

### Fail-Open vs. Fail-Closed Decision Framework

Resolve this per component using the organization's minimum nonnegotiable security posture:

- **Fail open** (availability priority): Serve what you can even if configuration is incomplete. Suitable when service interruption causes more harm than degraded security posture. Never acceptable for security-critical operations.
- **Fail closed** (security priority): Lock down fully when integrity cannot be verified. Suitable for ACL enforcement, authentication, and any component whose failure could allow unauthorized access.

**Resolution:** Define the minimum security posture first. Then design reliability controls to meet that posture's requirements — for example, tag security-oriented RPC traffic with high quality-of-service priority so it survives load shedding.

### Why Compartment Redundancy Beats Global Defense

A single strong perimeter, if breached, exposes the entire system. Compartments ensure that a breach or failure is contained. Incident management teams can take proportional actions — quarantining one compartment — rather than taking the whole system offline. Compartments also naturally create the boundaries needed for failure domain isolation and backup component separation.

### The Backup Drift Anti-Pattern

Two failure modes destroy backup component value:
- **Overreliance drift:** The backup gets treated as part of normal operation. During an actual outage, it is already saturated.
- **Zombie backup:** The backup is never touched. When needed, it fails because it was never maintained or tested.

Mitigation: route a small, constant fraction of real traffic through alternative components. This both validates them continuously and prevents them from becoming a surprise source of denial of service.

---

## Examples

### Example 1 — Fail-Open vs. Fail-Closed: Two-Factor Authentication

A service uses two-factor authentication (2FA) in the login flow. 2FA infrastructure becomes unavailable.

- **Fail-open decision:** Allow logins without 2FA. Users can still access their accounts. Acceptable during early 2FA adoption or for low-sensitivity accounts.
- **Fail-closed decision:** Disable all logins when 2FA is unavailable. A bank with custody of financial accounts would typically choose this — unauthorized access is a worse outcome than a service outage.

**Applying the framework:** Determine the minimum security posture first. The 2FA service itself should be protected against load shedding (high QoS priority) to reduce the frequency of this decision.

### Example 2 — Multi-Layer Defense in Depth: Multi-Tenant Compute Platform

A platform runs untrusted user code alongside trusted internal services.

Defense layers (each designed to catch what the previous layer misses):
1. API surface reduction — remove or replace built-in APIs that allow dangerous operations
2. Runtime compilation to constrained bytecode — eliminates large classes of memory corruption and control-flow attacks
3. System call filtering — catches exploitable conditions that bypass the bytecode layer; violations terminate the runtime immediately and alert

Over five years, this layered approach caught exploitable conditions that each individual layer would have missed. No single layer was assumed sufficient; each anticipated the failure of the previous one.

### Example 3 — Failure Domain with Canary Deployment

A configuration management system splits into two failure domains. Policy: no simultaneous updates to both domains.

- Domain A receives a new configuration push first (canary)
- Monitoring compares behavior between Domain A and Domain B
- If Domain A shows unexpected errors, the push is halted before Domain B is affected
- Blast radius of a bad configuration change: one failure domain, not the whole system

### Example 4 — Zombie Backup Prevention: On-Call Low-Dependency Validation

On-call engineers are routed through low-dependency system paths as part of their normal on-call rotation. Benefits:
- Continuously validates that low-dependency components are operational
- Engineers build familiarity with emergency paths before they need them under stress
- Reduces risk of misconfiguration surprise during an actual incident

---

## References

- Chapter 8: Design for Resilience, *Building Secure and Reliable Systems* (pp. 143–181)
- Chapter 9: Design for Recovery (recovery after resilience fails)
- Chapter 10: Denial-of-Service attacks (DoS defense evaluation, Step 4 of roadmap)
- Chapter 13: Testing for Reliability and Security (fuzzing, failure injection)
- Chapter 15: Measuring System Properties (choosing what to validate)
- *Site Reliability Engineering* book, Chapters 21 (throttling), 22 (load shedding), 20 (lame-duck mode)
- See `references/component-tier-definitions.md` for detailed tier configuration parameters
- See `references/compartmentalization-matrix.md` for a role/location/time decision matrix template

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
