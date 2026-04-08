---
name: security-reliability-design-review
description: |
  Review a system design for security and reliability tradeoffs before implementation begins. Use when: evaluating an architecture proposal or design document and need to identify where security and reliability requirements conflict with feature or cost requirements; auditing a proposed design to determine whether security and reliability are designed in from the start or likely to require expensive retrofitting later; deciding whether to build payment processing or sensitive data handling in-house versus delegating to a third-party provider; assessing whether a microservices framework or platform incorporates security and reliability by construction rather than by convention; or producing a design review report for a security review, production readiness review, or architecture decision record. Applies the emergent property test (security and reliability cannot be bolted on — they must arise from the whole design), the initial-versus-sustained-velocity model (early neglect accelerates to later slowdown), and the Google design document evaluation checklist covering scalability, redundancy, dependency, data integrity, SLA, and security/privacy considerations. Produces: a design review report with identified tensions between feature, security, and reliability requirements; tradeoff recommendations; and prioritized security/reliability improvements. Distinct from threat modeling (which focuses on adversary scenarios) and code review (which audits existing implementation). Applicable at any stage where design decisions are still open.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/security-reliability-design-review
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [4]
tags:
  - security
  - reliability
  - design-review
  - tradeoffs
  - requirements-analysis
  - nonfunctional-requirements
  - emergent-properties
  - build-vs-buy
  - microservices
  - velocity
execution:
  tier: 2
  mode: full
  inputs:
    - type: document
      description: "System design document, architecture proposal, design doc draft, or structured description of the system being reviewed — including its primary feature requirements, data it will handle, and any known constraints"
    - type: context
      description: "Optional: existing security policies, SLA commitments, compliance requirements (PCI-DSS, GDPR, HIPAA), or third-party integration plans that constrain the design"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Runs in conversation or project context. Works from a design document or description provided by the user. Produces a structured design review report."
discovery:
  goal: "Produce a design review report: identified requirement tensions, emergent property assessment, tradeoff recommendations, Google design doc checklist responses, and prioritized security/reliability improvements"
  tasks:
    - "Classify requirements into feature (functional) and nonfunctional (security, reliability) categories"
    - "Apply the emergent property test to assess whether security and reliability are designed in or bolted on"
    - "Run the Google design document evaluation checklist"
    - "Analyze build-vs-buy tradeoffs for any sensitive data handling or third-party dependencies"
    - "Assess whether platform or framework choices provide security-by-construction"
    - "Apply the initial-vs-sustained-velocity model to evaluate deferral risk"
    - "Produce a prioritized improvement list with tradeoff recommendations"
  audience:
    roles: ["software-engineer", "architect", "tech-lead", "site-reliability-engineer", "security-engineer", "engineering-manager"]
    experience: "intermediate — assumes familiarity with software design but not necessarily with formal security or reliability engineering"
  triggers:
    - "User has a design document or architecture proposal and wants a security and reliability review"
    - "User is deciding whether to handle sensitive data in-house or delegate to a third party"
    - "User wants to assess whether their design has security or reliability requirements baked in or bolted on"
    - "User is preparing a design doc for a production readiness review or security review"
    - "User wants to understand the long-term velocity implications of deferring security and reliability work"
    - "User is choosing a microservices framework or platform and wants to know if it provides security-by-construction"
  not_for:
    - "Identifying specific vulnerabilities in existing code — use a secure code review process"
    - "Mapping attacker profiles and threat scenarios — use adversary profiling and threat modeling"
    - "Reviewing code in a pull request — use a code review checklist"
    - "Planning incident response — use an incident response skill"
---

# Security and Reliability Design Review

## When to Use

You are helping a user evaluate, write, or improve a system design — a document or proposal that describes what a system will do, how it will be structured, and what constraints it will operate under. The design review is happening before implementation is locked in.

This skill examines the design from the perspective of security and reliability as emergent properties: properties that cannot be added to a finished design but must be considered throughout the design process, because they arise from the totality of architectural decisions — component decomposition, communication patterns, data handling, dependency structure, monitoring, and testing practices.

The output is a structured design review report, not a list of security warnings. The goal is to help the user understand where feature requirements, security requirements, and reliability requirements are in tension, and to recommend tradeoffs that satisfy all three at reasonable cost.

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

**1. What is the system's primary purpose and what are its critical feature requirements?**

Why: Critical feature requirements are the subset of feature requirements without which the system has no viable product. They set the baseline against which security and reliability tradeoffs must be weighed — you cannot recommend eliminating a critical feature requirement to satisfy a security goal. Distinguishing critical requirements from other feature requirements also reveals where tradeoffs are genuinely available versus where they are not.

- Check prompt or environment for: design document, user stories, use cases, product requirements document, README describing what the system does
- If missing, ask: "What does this system do and what are the features that absolutely must work for the product to be viable? For example: 'Users must be able to purchase items and complete checkout — the payment flow is a critical requirement.'"

**2. What data does the system handle and who has access to it?**

Why: The security requirements for a system are primarily determined by the sensitivity of the data it handles and who can access it. A system that processes payment card data is in scope for PCI-DSS compliance and faces regulatory obligations. A system holding personally identifiable information faces GDPR or equivalent requirements. A system with sensitive user communications attracts adversaries with different motivations and capabilities than a system holding only public data. The data profile sets the floor for security investment.

- Check prompt or environment for: data classification, privacy policy, compliance requirements, what user data is stored, whether payment or health data is involved
- If missing, ask: "What types of data will this system store or process? For example: user accounts with PII, payment card data, health records, financial transactions, or only non-sensitive application data?"

**3. What are the system's availability and reliability commitments?**

Why: Reliability requirements determine what the system must do when things go wrong — how it handles component failures, dependency outages, data loss, and surges in load. These commitments directly shape architectural decisions about redundancy, fallback mechanisms, and data integrity. A system with no stated SLA has made an implicit reliability decision that will constrain its options when it fails in production.

- Check prompt or environment for: service level objectives (SLOs), uptime requirements, SLA commitments, business impact of downtime
- If missing, ask: "What are the availability requirements for this system? For example: 99.9% uptime, sub-100ms p99 latency, or 'downtime is acceptable during off-hours.' What is the business impact if the system is unavailable for an hour? A day?"

### Optional Context (enriches the review)

- **Third-party dependencies:** Any external services, APIs, or libraries the system will integrate with — each is a reliability and security dependency.
- **Team size and operational model:** Smaller teams face tighter constraints on the security and reliability complexity they can maintain. A two-person team cannot staff a 24/7 on-call rotation.
- **Phase or stage:** Early-stage design vs. pre-launch review vs. post-incident redesign changes the emphasis of the review.
- **Regulatory or compliance requirements:** PCI-DSS, GDPR, HIPAA, SOC 2 each impose specific security and reliability obligations that must appear in the design.

---

## Core Principles

### The Emergent Property Test

Security and reliability are not modules or features — they are emergent properties of the entire system design. There is no `--enable_high_reliability_mode` flag. No single component in a system's source code "implements" security or reliability.

Reliability emerges from: how the service decomposes into components; how component availability relates to dependency availability; what communication mechanisms are used (RPCs, message queues, event buses); how load balancing, load shedding, and routing are implemented; how testing is integrated into the development and deployment workflow; and what monitoring and alerting infrastructure exists to detect anomalies.

Security posture emerges from: how the system decomposes into subcomponents and the trust relationships between them; the implementation languages, platforms, and frameworks used; how security design reviews, security testing, and code review are integrated into the workflow; and the forms of security monitoring, audit logging, and anomaly detection available to responders.

**Test to apply:** Can a well-specified module or flag be added to the design after the fact to satisfy the security or reliability requirement? If yes — it is a feature requirement, not an emergent property requirement. If no — it is an emergent property requirement that must be addressed in the design now, not retrofitted later. Apply this test to each identified security and reliability concern to determine whether it can be deferred or must be resolved in the current design.

### The Cost of Retrofitting

Design choices related to security and reliability are often similar in nature to foundational architectural choices like whether to use a relational or NoSQL database, or whether to use a monolithic or microservices architecture. Retrofitting these choices onto an existing system often requires significant design changes, major refactoring, or even partial rewrites, and can become very expensive and time-consuming.

Furthermore, such changes might have to be made under time pressure in response to a security or reliability incident — and making invasive late-stage changes to a deployed system in a hurry comes with significant risk of introducing additional flaws. The review should identify which requirements, if deferred, will impose the highest retrofitting cost.

### Initial Velocity Versus Sustained Velocity

Teams commonly justify ignoring security and reliability as early and primary design drivers in the name of "velocity" — the concern that addressing these requirements will slow down initial development. The correct distinction is between initial velocity and sustained velocity.

Choosing not to account for security, reliability, and maintainability early in the project cycle may indeed increase initial velocity. However, it also usually slows the project down significantly later. The late-stage cost of retrofitting a design to accommodate emergent property requirements can be very substantial. Furthermore, making invasive late-stage changes to address security and reliability risks can itself introduce additional security and reliability risks.

Evaluate each deferred security or reliability requirement against this model: What is the realistic late-stage cost of addressing this after the system is deployed? Is there a plausible remediation path that does not require significant redesign under time pressure?

---

## Process

### Step 1 — Classify Requirements

Identify and classify all stated and implied requirements in the design document.

**Why:** Security and reliability requirements have fundamentally different characteristics from feature requirements. Feature requirements map directly to specific code — a user story for profile editing maps to a handler, structured types, and a UI. Security and reliability requirements are emergent — there is no specific module in the codebase that "implements" reliability. Conflating the two categories leads to underinvestment in security and reliability because they appear to be addressed when they are not.

Produce a requirements table with three columns:

| Requirement | Category | Critical? |
|---|---|---|
| Users can purchase items | Feature | Yes — critical |
| Support team can view order history | Feature | No |
| All PII encrypted at rest | Security (nonfunctional) | Yes |
| Service available 99.9% per month | Reliability (nonfunctional) | Yes |
| Checkout completes in <2s at p99 | Performance (nonfunctional) | No |

**Categories:**
- **Feature / functional:** Describe specific behaviors a user can observe. Express as use cases, user stories, or user journeys. Identify which are critical (failure means no viable product).
- **Security (nonfunctional):** Define the exclusive circumstances under which sensitive data may be accessed, what protections are required for that data, and what compliance standards apply.
- **Reliability (nonfunctional):** Define SLOs for uptime, latency, and error rates; how the system responds to dependency failures; and data integrity and recovery requirements.
- **Development efficiency:** How implementation language, frameworks, and build processes affect the team's ability to iterate.
- **Deployment velocity:** How long from code complete to user-visible feature.

Surface any implied requirements that are not stated — particularly nonfunctional ones that are typically assumed (e.g., "we won't lose user data" is a reliability requirement even if unstated).

**Output of this step:** A requirements classification table with all stated and implied requirements, their category, and whether they are critical.

---

### Step 2 — Apply the Google Design Document Checklist

Run the Google design document evaluation questions against the design. Each question should be answered with the design's current response and an assessment of whether the response is adequate.

**Why:** Google uses this design document template to guide new feature design and to collect feedback from stakeholders before starting an engineering project. The reliability and security sections remind teams to think about the implications of their project and kick off production readiness or security review processes early — sometimes multiple quarters before engineers officially start thinking about the launch stage. These questions surface the requirements that teams most commonly neglect until they become incidents.

#### Scalability

- How does the system scale? Consider both data size increase and traffic increase.
- What are the current hardware or infrastructure constraints? Adding more resources might take much longer than expected, or might be too expensive for the project. What initial resources will be needed? Plan for high utilization, but be aware that using more resources than needed will block expansion.

#### Redundancy and Reliability

- How will the system handle local data loss and transient errors (e.g., temporary outages), and how does each affect the system?
- Which systems or components require data backup? How is the data backed up? How is it restored? What happens between the time data is lost and the time it is restored?
- In the case of a partial loss, can the system keep serving? Can only missing portions of backups be restored to the serving data store?

#### Dependency Considerations

- What happens if dependencies on other services are unavailable for a period of time?
- Which services must be running for the application to start? (Do not forget subtle dependencies like DNS resolution or time synchronization.)
- Are there dependency cycles — systems that block on each other in ways that prevent either from starting independently?

#### Data Integrity

- How will data corruption or loss in data stores be detected?
- What sources of data loss are covered? (User error, application bugs, storage platform bugs, site/replica disasters.)
- How long will it take to notice each type of loss? What is the recovery plan for each?

#### SLA Requirements

- What mechanisms are in place for auditing and monitoring the service level guarantees of the application?
- How can the stated level of reliability be guaranteed?

#### Security and Privacy

- What are the potential attacks relevant to this design, and what is the worst-case impact of each attack? What countermeasures are in place to prevent or mitigate each?
- What are the known vulnerabilities or potentially insecure dependencies?
- If the application has no security or privacy considerations, explicitly state so and explain why.

For each question, record: the design's current answer (or "not addressed"), and a gap assessment (Adequate / Needs attention / Not addressed).

**Output of this step:** A completed checklist table with current design response and gap assessment for each question.

---

### Step 3 — Identify Requirement Tensions

Map the tensions between feature requirements and nonfunctional requirements identified in Steps 1 and 2.

**Why:** Because security and reliability requirements are emergent properties, they interact with feature requirements and with each other in non-obvious ways. The classic example from payment processing illustrates this: attempting to mitigate a security risk (by outsourcing payment handling) introduces a reliability risk (third-party service dependency); attempting to mitigate that reliability risk (by adding a message queue fallback) reintroduces the security risk (sensitive data on disk). Tensions compound. Identifying them explicitly prevents the team from solving one tension while inadvertently creating another.

For each identified tension, produce a tension entry:

```
Tension: [short name]
Feature requirement affected: [the user story or functional requirement at risk]
Security/reliability concern: [the nonfunctional requirement in conflict]
How they conflict: [one paragraph describing the interaction]
Current design response: [how the design currently resolves or ignores this tension]
Assessment: [Resolved / Partially resolved / Unresolved]
```

Common tension patterns to look for:

- **Availability vs. data minimization:** Reliability mechanisms like message queues and local caching require data to be stored locally or in fallback systems, which may conflict with requirements to not hold sensitive data at rest.
- **Third-party dependency for data minimization vs. reliability:** Delegating sensitive data handling to a third party reduces in-house security obligation but adds a dependency failure mode. Mitigating that reliability risk often reintroduces the security concern.
- **Developer velocity vs. security controls:** Frameworks and languages that enforce security properties add constraints on what developers can do — the tradeoff is reduced developer freedom for reduced vulnerability surface.
- **Complexity vs. testability:** Resilience mechanisms (fallback paths, queues, retries) introduce code paths exercised only in failure scenarios. These paths are less tested and more likely to harbor bugs.
- **Cost of redundancy vs. availability commitment:** Meeting a 99.99% SLA may require geographic redundancy and hot standby systems — costs that must be weighed against the SLA commitment's actual business value.

**Output of this step:** A tensions table with one entry per identified tension, including the current design response and resolution status.

---

### Step 4 — Evaluate Build-vs-Buy for Sensitive Data Handling

For any component that handles sensitive data (PII, payment card data, health records, credentials), evaluate whether to build the handling in-house or delegate to a third-party service provider.

**Why:** Often, the best way to mitigate security concerns about sensitive data is to not hold that data in the first place. Third-party service providers can be arranged so that sensitive data never passes through your systems, or at least so that your systems do not persistently store it. This is a design-level tradeoff with significant downstream security, reliability, and cost implications — and it must be decided at design time, not retrofitted later.

For each sensitive data component, assess the following:

**Benefits of third-party delegation:**
- Your systems no longer hold the sensitive data, reducing the risk that a vulnerability in your systems results in a data compromise.
- Compliance obligations (e.g., PCI-DSS scope for payment card data) may be significantly simplified.
- You do not need to build and maintain infrastructure to protect the data at rest in your systems.
- Many third-party providers offer countermeasures against fraud and risk assessment services that would be expensive to build in-house.

**Costs and risks of third-party delegation:**
- The provider will charge fees. Beyond a certain transaction volume, in-house processing may be more cost-effective.
- Engineering cost of integrating with and maintaining the vendor API — including tracking API changes on the vendor's schedule.
- Your user story "user can complete purchase" now fails if the payment provider's service is down or unreachable. This is an additional dependency failure mode outside your control.
- You are entrusting sensitive customer data to a third-party vendor. You must carefully evaluate the vendor's security stance during selection and on an ongoing basis.
- Integrating with a vendor-supplied library introduces the risk that a vulnerability in that library, or its transitive dependencies, results in a vulnerability in your systems. Prefer vendors who expose their API via open protocols (REST+JSON, XML, SOAP, gRPC) rather than requiring a proprietary linked library.

**Reliability mitigation risks:**
Mitigating the reliability risk of a third-party dependency (e.g., adding a message queue to buffer transactions during outages) can reintroduce the security risk you were trying to eliminate (e.g., sensitive payment data written to persistent local storage). Subsystems exercised only in rare failure scenarios are less tested and more likely to harbor hidden bugs — including security vulnerabilities that are never triggered in normal operation.

Produce a recommendation: delegate, build in-house, or hybrid, with rationale.

**Output of this step:** A build-vs-buy assessment for each sensitive data component, with a recommendation and the key risks of each option.

---

### Step 5 — Evaluate Framework and Platform Security-by-Construction

Assess whether the implementation framework or platform chosen for the system provides security and reliability properties by construction — meaning the framework actively prevents developers from introducing common vulnerabilities or reliability failures, rather than relying on developer discipline.

**Why:** The Google microservices framework example illustrates the win-win scenario: a framework adopted primarily because it simplifies application development and automates common chores can simultaneously provide out-of-the-box security and reliability enforcement. When security and reliability best practices are woven into the fabric of the framework — not bolted on at the end — the framework takes responsibility for handling many common concerns. This makes security and production readiness reviews much more efficient: if continuous builds are green, the application is not affected by the common security concerns already addressed by the framework. Bug fixes in the centrally maintained framework propagate automatically to all applications when they are rebuilt and deployed.

Evaluate the proposed framework or platform against the following criteria:

**Static conformance checks:** Does the framework enforce that values passed between components meet type constraints at compile time? (Example: immutable types passed between concurrent contexts prevent concurrency bugs by construction — a conformance check that eliminates a class of bugs rather than relying on developer awareness.)

**Isolation enforcement:** Does the framework enforce isolation constraints between components so that a change in one component cannot cause a bug in another? This is a reliability property: well-defined and understandable interfaces between components reduce both vulnerability to bugs and attack surface.

**Security vulnerability class elimination:** Does the framework actively prevent common vulnerability classes — cross-site scripting, SQL injection, cross-site request forgery — by construction rather than by guideline? A framework that provides `SafeHtml` and `SafeUrl` types that the compiler enforces cannot be bypassed by mistake eliminates those vulnerability classes structurally, not by convention.

**Automated operational setup:** Does the framework automatically configure monitoring for operational metrics, health checks, and SLA compliance? Manual configuration of these operational concerns is a reliability risk because it is inconsistently applied across services.

**Error budget integration:** Does the deployment automation incorporate reliability gates (e.g., stopping releases when the error budget is consumed) so that SLA adherence is a structural property of the deployment pipeline rather than a manual process?

If the current design relies on developer discipline rather than framework enforcement for security or reliability properties, flag this as a design risk and recommend frameworks or patterns that provide the property by construction.

**Output of this step:** A framework/platform assessment against the five criteria, with a recommendation on whether the current choice provides adequate security-by-construction coverage.

---

### Step 6 — Apply the Initial-vs-Sustained-Velocity Assessment

Assess the velocity implications of deferring each unresolved security or reliability requirement identified in previous steps.

**Why:** Teams are tempted to defer security and reliability work in the name of "moving fast." This is a coherent trade if initial velocity is the primary goal and the late-stage cost is understood and accepted. The problem is that the late-stage cost is routinely underestimated and the retrofitting work routinely happens under the worst possible conditions — under time pressure, in response to a security or reliability incident, in a mature and complex codebase with many dependencies. Making invasive late-stage changes under those conditions introduces new risks. The goal of this step is to make the deferred cost explicit and help the team decide deliberately, not by default.

For each unresolved requirement from the tensions analysis, assess:

1. **Retrofitting complexity:** Can this requirement be addressed by adding a new component, or does it require redesigning existing architectural boundaries? (Example: adding a logging interceptor to an RPC framework is additive — it does not require changing existing handlers. Redesigning from a monolith to microservices to achieve isolation is a structural change affecting everything.)

2. **Incident risk:** What is the probability and impact of a security or reliability incident caused by this gap before it is addressed? Deferring a requirement that has a high probability of causing a production incident within 12 months is a different decision from deferring a requirement that affects a low-traffic, low-sensitivity code path.

3. **Remediation pressure:** If this gap causes an incident, what is the likely time-pressure under which the fix must be made? Incident-driven remediation under time pressure is a significant source of new security and reliability bugs.

4. **Early investment cost:** What is the actual engineering cost of addressing this requirement now, at design time? Early investments in security and reliability are typically modest when made early in a product's lifecycle and require only incremental ongoing effort to maintain. The same investment made after launch typically requires a lot of work all at once.

**Output of this step:** A velocity impact table with each deferred requirement, its retrofitting complexity (Low/Medium/High), incident risk level (Low/Medium/High), and a recommended resolution timing (address now / address before first production load / can defer to later milestone).

---

### Step 7 — Produce the Design Review Report

Compile the outputs of Steps 1–6 into a structured design review report.

**Why:** A design review is only useful if it is documented, shareable, and actionable. The report becomes the shared reference for design decisions, security review filings, production readiness reviews, and architecture decision records. Without a written artifact, the review has no lasting impact.

**Report structure:**

```
1. Executive Summary
   - System overview (one paragraph)
   - Overall assessment: Adequate / Needs attention / Significant gaps
   - Top 3 prioritized recommendations

2. Requirements Classification
   - Table from Step 1

3. Google Design Document Checklist
   - Completed checklist from Step 2, with gap column

4. Identified Requirement Tensions
   - Tension entries from Step 3

5. Build-vs-Buy Recommendations
   - Assessments from Step 4 (omit if no sensitive data handling)

6. Framework/Platform Assessment
   - Evaluation from Step 5

7. Initial-vs-Sustained-Velocity Assessment
   - Table from Step 6

8. Prioritized Improvement List
   - Ranked list of recommended changes
   - Each entry: recommendation, rationale, timing, estimated effort

9. Open Questions
   - Design decisions not yet made that affect this review
   - Information that would change the assessment if available
```

**Output of this step:** A completed design review report. Write it to the project directory or present it as a structured response, depending on the user's preference.

---

## Key Principles

**1. Security and reliability cannot be bolted on.**
They are emergent properties of the entire system design — including component decomposition, communication mechanisms, data handling, trust relationships, testing practices, and operational workflow. Apply the emergent property test to every security and reliability concern: if there is no specific module or flag that implements it, it must be addressed at the design level, not deferred to implementation.

**2. Tradeoffs compound.**
The payment processing example illustrates a common pattern: solving one security or reliability tension creates another. A security mitigation (not holding sensitive data) introduces a reliability risk (third-party dependency). Mitigating that reliability risk (local message queue) reintroduces the security risk (sensitive data on persistent storage). Identifying tensions explicitly prevents teams from solving one without noticing they have created another.

**3. Initial velocity is not the same as sustained velocity.**
Deferring security and reliability work typically accelerates the start but decelerates the project as a whole. The late-stage cost of retrofitting emergent property requirements can be very substantial, and remediation work done under incident pressure is itself a source of new security and reliability failures. Make the deferred cost explicit before treating it as acceptable.

**4. Security-by-construction beats security-by-convention.**
A framework that makes common vulnerability classes structurally impossible (via type constraints enforced by the compiler) is more reliable than one that relies on developer awareness and code review. When choosing between frameworks or design patterns, prefer options that make the secure behavior the default and the insecure behavior a compile-time or structural error.

**5. Security and reliability reviews must happen at design time.**
Google's design document template kicks off production readiness and security review processes early — sometimes multiple quarters before engineers start thinking about the launch stage. Design reviews sometimes happen multiple quarters before the launch stage. Late-stage security and reliability reviews that discover fundamental design problems are costly and disruptive. This review is most valuable when design decisions are still open.

---

## Examples

### Example 1 — Payment processing: build-vs-buy analysis

**Context:** An e-commerce service needs to accept credit card payments. The product team's critical requirement is "users can complete checkout." The team is considering whether to handle payment card processing in-house or delegate to a third-party payment service API.

**Requirement tension identified:**
- Delegating to a third-party service eliminates the need to hold PCI-DSS-regulated card data, reducing compliance scope and data breach risk.
- However, the third-party service becomes a critical dependency. If the payment service is unavailable, "users can complete checkout" fails — a critical requirement is now dependent on an SLA outside the team's control.
- Adding a message queue to buffer transactions during outages reintroduces storage of payment data (on disk or in memory), which partly re-creates the PCI-DSS scope the delegation was meant to eliminate.
- Using volatile-memory-only storage for the queue avoids the PCI concern but means transactions are lost during host restarts — a data integrity failure.

**Recommendation:** Delegate to a third-party payment service; do not add a local queue fallback. Accept the reliability dependency on the payment provider and mitigate by selecting a provider with a strong SLA and evaluating a secondary provider for failover. Avoid the queue fallback because the security/compliance risk it reintroduces outweighs the reliability benefit at typical transaction volumes.

**Emergent property test result:** The PCI-DSS compliance requirement cannot be satisfied by adding a module after the design is implemented — it requires that the data never enters the system in the first place. This is an emergent property requirement that must be resolved at design time.

---

### Example 2 — Microservices framework: security-by-construction assessment

**Context:** A team is building a new microservices-based web application and choosing between a minimal framework and a full-featured internal framework with conformance checks.

**Framework/platform assessment:**
- The minimal framework provides no conformance checks. Security properties (input validation, output encoding, authentication, authorization) must be implemented correctly in each service by each developer. These properties are verified by code review and security guidelines — by convention, not by construction.
- The full-featured framework enforces conformance checks: all values passed between concurrent contexts must be immutable types (eliminating concurrency bugs by construction); isolation constraints between components prevent cross-component bug propagation; web application support handles common vulnerability classes (cross-site scripting, cross-site request forgery) by construction, not by guideline.

**Sustained velocity implication:** Applications built on the security-by-construction framework are verified by green continuous integration builds — if the build passes framework conformance checks, the application is not affected by the security concerns the framework addresses. Security and production readiness reviews are much more efficient. Bug fixes and security patches in the framework propagate automatically to all applications at next build and deploy.

**Recommendation:** Choose the full-featured framework. The up-front learning cost is offset by the structural elimination of common vulnerability classes and the efficiency gain in security reviews over the system's lifetime. This is a design-time decision; migrating later requires significant refactoring of every service.

---

## References

See `references/` for:
- `google-design-doc-checklist.md` — Full text of the reliability and security sections of the Google design document template, with guidance on how to interpret each question
- `requirement-classification-guide.md` — Worked examples of feature vs. nonfunctional requirement classification, including implied nonfunctional requirements teams commonly miss
- `tension-catalog.md` — Common security-vs-reliability tension patterns with worked analysis from the payment processing and microservices case studies
- `build-vs-buy-assessment-template.md` — Blank template for third-party delegation tradeoff analysis, including vendor security evaluation criteria
- `velocity-impact-assessment.md` — Guidance on assessing retrofitting complexity and incident risk for deferred requirements

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
