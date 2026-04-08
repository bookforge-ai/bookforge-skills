---
name: least-privilege-access-design
description: |
  Analyze a system's access patterns and design least-privilege controls: classify data and APIs by risk, select the narrowest API surface for each operation, define authorization policies with multi-party approval for sensitive actions, establish emergency access override procedures, and optionally introduce a controlled-access production proxy. Use when reviewing access controls for an existing system, designing authorization for a new service, auditing whether engineers have more permissions than their roles require, deciding whether to use a bastion or proxy for privileged operations, or hardening administrative API surfaces against insider mistakes and external compromise. Produces an access classification report, API surface recommendations, authorization policy decisions, and emergency override guidelines.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/least-privilege-access-design
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [3, 5]
tags:
  - security
  - access-control
  - least-privilege
  - authorization
  - zero-trust
  - multi-party-authorization
  - audit-logging
  - api-design
  - administrative-api
  - breakglass
  - proxies
  - sre
  - reliability
execution:
  tier: 2
  mode: full
  inputs:
    - type: codebase
      description: "Service codebase, infrastructure config, IAM policy files, or API definitions revealing current access patterns and permission grants"
    - type: document
      description: "Architecture diagram, role/permission inventory, runbook, or written system description if no codebase is directly accessible"
  tools-required: [Read, Write]
  tools-optional: [Grep, Bash]
  mcps-required: []
  environment: "Run inside a project directory with codebase, config, or architecture artifacts. Falls back to structured interview with the engineer."
discovery:
  goal: "Produce a written access classification report: data/API risk ratings, API surface recommendations, authorization policy decisions, emergency override guidelines, and a controlled-access proxy recommendation if applicable"
  tasks:
    - "Inventory all data stores and APIs; classify each by Public / Sensitive / Highly Sensitive"
    - "Classify each access type (read / write / infrastructure) and assign a risk level per cell"
    - "Evaluate current API surface against least-privilege: identify oversized APIs and recommend narrow functional replacements"
    - "Select authorization controls for each risk level: ACL, multi-party authorization, temporary access, structured business justification"
    - "Define emergency access override policy: who can invoke it, under what conditions, and how it is audited"
    - "Recommend a controlled-access production proxy if fine-grained controls are unavailable or insufficient"
    - "Design audit log strategy: granularity, structured justification, auditor selection"
  audience:
    roles: ["security-engineer", "software-engineer", "site-reliability-engineer", "platform-engineer", "tech-lead", "software-architect"]
    experience: "intermediate-to-advanced — assumes familiarity with IAM concepts, API design, and distributed systems"
  triggers:
    - "Reviewing or auditing access controls for an existing system"
    - "Designing authorization for a new service or administrative API"
    - "Deciding whether a bastion host or production proxy is needed for privileged operations"
    - "Hardening a system where engineers have more permissions than their roles require"
    - "Post-incident review reveals an outage caused by an overly permissive admin operation"
    - "Preparing for a security review or compliance audit"
    - "Reducing the blast radius of a potential account compromise"
  not_for:
    - "Authentication mechanism selection (e.g., OAuth vs. mTLS) — covered separately"
    - "Network topology and firewall rule design"
    - "Application-layer threat modeling — use adversary-profiling-and-threat-modeling"
---

## When to Use

Use this skill when you need to systematically reduce the damage any one user, automation, or compromised credential can cause — by granting only the access needed and no more.

Invoke it for:
- Any service where an engineer with a production role could accidentally or maliciously cause an outage or data breach
- Systems where admin tooling uses broad, interactive APIs (SSH to hosts, root shells, POSIX-level access) rather than narrow functional APIs
- Designing new administrative APIs for a service where the access model hasn't been explicitly defined
- Hardening automation credentials: automation roles often accumulate unnecessary permissions over time
- Evaluating whether an emergency override (breakglass) policy is necessary and properly governed

Do not invoke it for selecting the cryptographic authentication mechanism, designing network segmentation, or full threat modeling — those are separate concerns.

---

## Context and Input Gathering

Before designing least-privilege controls, gather the following:

1. **Data inventory**: What data stores does the system hold or access? What is in each? Who currently has access?
2. **API inventory**: What interfaces does the system expose — user-facing, administrative, setup/teardown, maintenance/emergency? For each: what can a caller read, write, or modify?
3. **Role inventory**: What human roles (engineers, SREs, support staff, on-call) and automated roles (CI/CD, batch jobs, monitoring agents) access the system? What do they actually need?
4. **Current access breadth**: Are any roles granted interactive shell access, broad IAM policies, or "owner"-level credentials? Does any automation run as a privileged user beyond what its task requires?
5. **Authorization mechanism in place**: ACL? IAM policy? Role-based groups? Is there a shared authorization library or each service rolls its own?
6. **Audit coverage**: Are administrative actions logged? Is each log entry attributable to a specific person and action? Is there a review process?
7. **Emergency access story**: How do on-call engineers recover from a bad policy update or auth system failure? Is there a procedure, and is it tested?

If a codebase is available, search for:
- SSH ForceCommand entries, sudo rules, or `.authorized_keys` files
- IAM policy documents, role bindings, or service account configurations
- Any invocation of root, admin, or infrastructure-level APIs in automation scripts
- Logging calls around sensitive operations — are they structured or freeform?

---

## Process

### Step 1 — Classify Data and APIs by Risk

**WHY**: Not all data and actions carry the same blast radius. Treating everything uniformly either over-controls low-risk operations (hurting productivity) or under-controls high-risk ones (accepting unnecessary exposure). A classification framework makes the trade-off explicit and consistently applied.

Classify each data store and API using the access classification matrix. For each resource, determine its sensitivity category and then assess risk by access type:

**Sensitivity categories**:

| Category | Definition |
|---|---|
| **Public** | Open to anyone in the organization; limited business impact if exposed |
| **Sensitive** | Limited to groups with a documented business purpose; medium impact if exposed or corrupted |
| **Highly Sensitive** | No permanent access; high impact if exposed, corrupted, or deleted (PII, cryptographic secrets, billing data, user credentials) |

**Risk by access type** (per Table 5-1, Chapter 5):

| | Read access | Write access | Infrastructure access |
|---|---|---|---|
| **Public** | Low risk | Low risk | High risk |
| **Sensitive** | Medium/high risk | Medium risk | High risk |
| **Highly Sensitive** | High risk | High risk | High risk |

Infrastructure access — the ability to change ACLs, reduce logging levels, gain direct shell access, restart services, or otherwise affect service availability — is high risk for all sensitivity levels. A read of publicly available data can still enable catastrophic abuse if it bypasses normal access controls.

Output of this step: a classification table listing each data store, API group, and role, with its assigned sensitivity category and the risk level per access type.

### Step 2 — Evaluate and Narrow the API Surface

**WHY**: A large API surface is the root cause of most over-privilege. When users or automation connect via a broad interface (an interactive shell, a general-purpose admin API, a root-level process), the system can't distinguish what they actually need from what they could do. Narrowing the API to the minimum set of operations required makes it possible to grant the minimum permission and to audit actions precisely.

For each administrative API or access pathway, assess:

- **API surface size**: How many distinct operations can a caller perform? An interactive SSH session exposes the entire POSIX API. A custom RPC method that pushes a validated config file exposes exactly one operation.
- **Auditability**: Can you capture what the caller did in a meaningful way? "User opened an SSH session" is not auditable. "User pushed config hash `abc123`" is.
- **Ability to express least privilege**: Can you grant access to exactly this action for exactly this resource without granting broader access?
- **Preexisting infrastructure**: Does a narrow API already exist (e.g., a software update mechanism, a config push API)?

Use the API selection tradeoff matrix (per Table 5-2, Chapter 5 — configuration distribution example):

| API approach | API surface | Auditability | Can express least privilege | Complexity |
|---|---|---|---|---|
| POSIX API via SSH | Large | Poor | Poor | High |
| Software update / package manager API | Varies | Good | Varies | High, but reusable |
| Custom scoped command (e.g., SSH ForceCommand) | Small | Good | Good | Low |
| Custom HTTP/RPC sidecar | Small | Good | Good | Medium |

**Design rule**: Make each API endpoint do one thing well. When you need a new operation, build a new narrow endpoint rather than extending an existing broad one. This applies equally to user-facing APIs and administrative APIs.

**For existing systems with broad APIs** (e.g., SSH access to all hosts):
1. Identify the specific operations that are actually performed through the broad interface
2. Build a narrow API for each operation category, with input validation and structured logging
3. Restrict the broad interface to a controlled emergency override path (see Step 5)
4. Progressively migrate callers to the narrow API

### Step 3 — Select Authorization Controls Per Risk Level

**WHY**: The appropriate authorization control depends on the risk of the action. Binary yes/no ACLs are sufficient for low-risk reads; high-risk writes on sensitive data require additional controls that distribute trust across multiple parties and create an auditable record.

Match each classified operation to one or more of the following controls:

**Access control list (ACL) / group membership** — appropriate for:
- Low and medium risk reads
- Operations where a single authorized user making the decision is acceptable
- Implementation: role-based group membership checked at the API boundary; prefer a shared authorization library over per-service custom logic

**Multi-party authorization (multi-person approval)** — appropriate for:
- High-risk writes and all infrastructure-level operations
- Sensitive operations where unilateral action by a single person (even authorized) is unacceptable
- Benefits: prevents unintentional mistakes, deters insider abuse, increases attacker cost (must compromise multiple accounts or craft a request that passes peer review), provides an audit trail that is tamper-resistant
- Design requirement: ensure the authorization system and social dynamics both allow approvers to say no. If approvers feel unable to reject suspicious requests from managers or senior engineers, the control provides no security value. Provide an escalation path to a security team.
- Pitfall: ensure approvers have enough context to make an informed decision. Show the specific action, target, and parameters — not just a generic "approve this request."

**Business justification (structured)** — appropriate for:
- Access to sensitive customer data by support staff (tie to a specific ticket or case number)
- Operations that are permitted but should be associated with a documented business need
- Implementation: require a structured reference (ticket ID, incident number, customer case ID) rather than free-text, so access can be programmatically correlated to the justification and flagged when it doesn't match

**Temporary access** — appropriate for:
- All sensitive and highly sensitive operations where continuous standing access is unnecessary
- On-call rotations, time-bounded task assignments
- Benefit: reduces ambient authority — if a user never holds continuous access to sensitive resources, a credential compromise has a limited time window of damage
- Implementation: expiring group memberships, on-demand access request workflows, scheduled access windows tied to on-call shifts

**Three-factor authorization** — appropriate for:
- Extremely high-risk operations where broad workstation compromise is a realistic threat model
- Requires authorization from a separate, hardened device (e.g., a managed mobile device) that an attacker who has compromised the primary workstation cannot easily also control
- Note: this protects against broad infrastructure compromise, not against insider threats (the same person controls both approvals)

For highly sensitive infrastructure operations, combine controls: multi-party authorization + temporary access + structured business justification.

### Step 4 — Design the Audit Strategy

**WHY**: Authorization controls are only as effective as the audit mechanism that detects when they are circumvented or abused. The value of a narrow API comes not just from preventing misuse, but from making every action attributable and reviewable. Without deliberate audit design, audit logs become noise that nobody reviews.

**Audit log requirements**:
- Each log entry must answer: **Who** did **what** to **which resource**, **when**, and **why** (structured justification)
- Use structured data, not free-text — this enables programmatic analysis and correlation across events
- Associate audit events with structured justifications (ticket IDs, incident numbers) so that access patterns can be verified against documented need

**Granularity**: Small functional APIs provide the largest audit advantage. "User pushed config with hash `abc123` to host group `web-frontend`" enables strong assertions. "User opened SSH session" does not. Interactive session transcripts (bash history, `script(1)`) appear comprehensive but can be bypassed by any user who is aware of their existence.

**Auditor selection**:
- For best-practice audits (are controls being followed correctly?): use team-level peer review. Teammates have context to identify unusual patterns and create cultural pressure to use proper channels rather than emergency overrides. Distribute this responsibility broadly.
- For security breach detection (has an adversary compromised an account?): use a centralized security team with cross-team visibility. Individual teams may not notice the connection between anomalous actions across different services.

**Emergency override audit**: Emergency override (breakglass) events must always be reviewed. Weekly team review of all emergency override usage from the previous shift is a practical pattern — it creates cultural accountability and signals when the narrow API is insufficient for real operational needs (which should trigger a fix to the normal API, not normalization of emergency override use).

### Step 5 — Define the Emergency Access Override Policy

**WHY**: Any authorization system can fail. A bad policy update, a misconfigured ACL, or an urgent production incident may require access that the normal authorization path cannot provide in time. Without a pre-defined, tested emergency access mechanism, engineers will improvise — which introduces uncontrolled risk. With a well-designed one, you get a controlled escape valve that is tightly audited.

Define the emergency access override policy with the following properties:

**Access restriction**: Emergency override access should be available only to the team directly responsible for the service's operational SLA (typically the SRE team). It should not be broadly available to all engineers.

**Location restriction** (for zero trust network access): If the service uses zero trust network access (access based on user and device credentials, not network location), the emergency override for bypassing the zero trust control should be available only from specific, physically secured locations with additional physical access controls — sometimes called "panic rooms." This is an intentional exception to the "network location doesn't grant trust" principle, offset by physical controls.

**Monitoring**: All uses of emergency override must be logged and reviewed. Emergency override use should be rare and surprising. Routine use signals that the normal API is inadequate and must be fixed.

**Testing**: The emergency override mechanism must be tested regularly by the team responsible for the service. A mechanism that has never been tested may not work when it is needed.

**Graceful failure**: Design the authorization system to fail in a known, diagnosable way. When a caller is denied access, the denial message should include information proportional to the caller's privilege level — nothing for unprivileged callers (no information disclosure), remediation steps for authorized callers who are incorrectly denied. Provide a denial token that can be used to open a support ticket rather than requiring the caller to describe the failure from memory.

### Step 6 — Evaluate Whether a Controlled-Access Production Proxy Is Needed

**WHY**: When fine-grained controls for backend services are not available — because the service is third-party, legacy, or too costly to modify — a controlled-access production proxy can layer authorization, auditing, rate limiting, and multi-party approval on top of the existing interface without requiring changes to the underlying system.

A controlled-access production proxy is appropriate when:
- Direct modification of the target system to add authorization controls is impractical
- Multiple teams need audited, rate-limited access to the same production infrastructure
- You need multi-party approval for specific operations without changing each service
- You want to enforce that no human directly accesses a production system except through the proxy

A controlled-access production proxy provides:
- **Single audit point**: every operation against the fleet is logged at the proxy, regardless of which tool or engineer initiates it
- **Multi-party authorization enforcement**: the proxy checks for peer approval before forwarding the request
- **Rate limiting**: restricts the blast radius of mistakes (e.g., limiting the rate at which machine restarts can be issued)
- **Compatibility**: works with third-party systems that cannot be modified, by controlling behavior at the proxy layer

Proxy risks and mitigations:
- **Single point of failure**: run multiple instances for redundancy; ensure all dependencies have acceptable SLAs and documented emergency contacts
- **Policy configuration errors**: generate policy templates or auto-generate settings that are secure by default; review changes to policy config with the same rigor as code changes
- **Circumvention pressure**: engineers will attempt to bypass the proxy for convenience. Address this by working closely with the team to ensure emergency override paths are available for genuine emergencies, while maintaining that the proxy is the required channel for normal operations

---

## Key Principles

**Least privilege applies to humans, automation, and machines equally.** The objective extends through all authentication and authorization layers. Automation credentials often accumulate permissions over time — review them with the same rigor as human roles.

**Avoid ambient authority.** Users and automation should not hold standing access to sensitive resources they do not currently need. Temporary access that expires is always preferable to permanent standing access.

**Design for the realistic threat model, not the idealized one.** Engineers make typos. Accounts get compromised. Credentials are phished. A system that requires perfect human execution to remain secure is not secure. Design to limit the damage of realistic failure modes.

**Small APIs make everything else possible.** Narrow, functional APIs are the prerequisite for meaningful audit logs, meaningful least privilege, and meaningful multi-party authorization. A system built on broad interactive APIs cannot be audited or constrained effectively regardless of other controls.

**Authorization infrastructure should be shared, not per-service.** Separate authorization logic into a shared library or service. This enables org-wide controls (multi-party authorization, multi-factor authorization) to be added at a single layer rather than requiring changes to every service. Standardization also enables team mobility and consistent policy reasoning.

**Culture enforces what technology cannot.** Multi-party authorization only works if approvers feel genuinely empowered to reject suspicious requests. Emergency override use only remains rare if teams review it regularly and treat frequent use as a signal that the normal API needs improvement. Controls without cultural reinforcement become rubber stamps.

---

## Examples

### Example 1 — Controlled-Access Production Proxy (Safe Proxy Pattern)

**Scenario**: An infrastructure team runs a fleet of production servers. Engineers use command-line tools directly against the fleet for administrative tasks. These tools are potentially dangerous — an incorrect scope selector could stop multiple service frontends simultaneously. Centralized logging and authorization are not enforced.

**Problem**: No audit trail. Engineers can issue arbitrary commands to production. A single engineer account compromise or fat-finger mistake could take down significant fleet capacity.

**Least-privilege design**:

1. **Classify**: The fleet's command-line interface is an infrastructure-level API. By the classification matrix: high risk for all sensitivity levels.
2. **Narrow the API**: Introduce a controlled-access production proxy that exposes a defined set of RPCs. Each RPC corresponds to a specific administrative action (restart a job, push a config, check status). The underlying servers are reconfigured to accept connections only from the proxy — not directly from engineer workstations.
3. **Authorization policy**: The proxy enforces an ACL per RPC. For sensitive operations (e.g., stopping a job in production), the proxy triggers multi-party authorization — an engineer in the `admin` group must have a peer in `admin-leads` approve before the command executes.
4. **Audit**: The proxy logs every RPC, the identity of the caller, the parameters, and whether it was approved. Log entries are structured and associated with the requester's ticket or incident number.
5. **Emergency override**: Engineers who genuinely need direct access during an incident can invoke an emergency override mechanism. All emergency override uses are reviewed weekly by the team.

**Result**: ~13% of production outages that would have been caused by direct human access to production become preventable. The blast radius of any single mistake or compromise is bounded by the rate limiter and multi-party approval requirements.

**Proxy policy structure** (conceptual):
```
config {
  proxy_role = 'admin-proxy'
  tools {
    restart_job {
      allow = ['group:admin']
      require_approval_from = ['group:admin-leads']
      rate_limit = { max_per_minute = 5 }
    }
    status_check {
      allow = ['group:admin', 'group:sre']
      # No approval required — read-only, low risk
    }
  }
}
```

### Example 2 — Configuration Distribution API Design

**Scenario**: An automation system needs to push a validated configuration file to all web servers in a fleet. The naive approach: SSH to each host as the user the web server runs as, write the file, restart the process.

**Problem**: The SSH approach exposes the entire POSIX API. The automation role can read any data on the host, stop the web server permanently, start arbitrary binaries, or cause a coordinated outage of the entire fleet. A compromise of the automation credential is equivalent to a compromise of every web server.

**Least-privilege design using Table 5-2 logic**:

1. **Classify**: Web server configuration write is a write operation on a public service — medium risk. Infrastructure access (ability to restart the service) is high risk.
2. **Evaluate API options**:
   - POSIX API via SSH: large surface, poor auditability, poor least-privilege expression — reject
   - Software update API (e.g., package manager): good auditability, reusable infrastructure, but complexity is high and convergence timing may not meet requirements
   - Custom SSH ForceCommand: small surface, good auditability, low complexity — viable
   - Custom HTTP receiver (sidecar): small surface, good auditability, medium complexity — preferred for scale
3. **Design the narrow API**: A small sidecar process accepts a configuration payload via an authenticated RPC, validates its structure and signature, writes the file to the correct path, and restarts the web server. The automation role is authorized only to call this single RPC — it cannot read other files or run other processes.
4. **Segment trust further**: The signing of the configuration is performed by a separate role (the code review / release system), independent from the automation role that pushes it. Even if the push automation is compromised, it cannot push an arbitrary config — only content that has been signed by the release system.
5. **Audit**: Each push logs the config hash, the target host group, and the result. Rejected configs (invalid signature, schema validation failure) are logged for investigation.

**Result**: A compromise of the push automation credential cannot write arbitrary content to hosts or run arbitrary processes. The blast radius is limited to pushing a valid (signed) config — which itself requires compromise of the signing system.

### Example 3 — Support Staff Access to Customer Data

**Scenario**: Customer support representatives need to access customer account records to resolve tickets. Currently, all support staff have read access to all customer records for all customers at all times.

**Problem**: Overly broad read access to highly sensitive data. A support staff compromise, or a malicious insider, can exfiltrate all customer data without any specific trigger.

**Least-privilege design**:

1. **Classify**: Customer records are highly sensitive. Read access is high risk.
2. **Authorization control**: Replace standing read access with structured business justification — access to a customer's record is only permitted when a support case for that customer is open and assigned to this representative.
3. **Implementation path** (incremental):
   - Phase 1: Require a support ticket ID for any customer data access. Log the association between the ticket and the access event.
   - Phase 2: Validate that the ticket exists, is open, and is assigned to the requesting representative before granting access.
   - Phase 3: Restrict access to only the specific customer's data associated with the open ticket, rather than all customers.
   - Phase 4: Add time bounds — access expires when the ticket is closed.
4. **Audit**: Every customer data access is logged with the associated ticket ID. A programmatic check verifies that access events correspond to open tickets. Anomalies (access with no ticket, access after ticket closure, bulk reads) trigger alerts.

**Result**: The data surface exposed to any single support interaction is the minimum needed to resolve that case. A compromised support account can only access data for currently open tickets assigned to it — not the entire customer database.

---

## References

- [access-classification-matrix.md](references/access-classification-matrix.md) — Full access classification matrix (Public/Sensitive/Highly Sensitive × Read/Write/Infrastructure) with risk ratings and control recommendations
- [api-selection-tradeoffs.md](references/api-selection-tradeoffs.md) — API design options for administrative operations with tradeoff analysis (API surface, auditability, least-privilege expressibility, complexity)
- [authorization-policy-framework.md](references/authorization-policy-framework.md) — How to design and ship authorization policies: shared library patterns, policy language tradeoffs, pitfalls
- [controlled-access-proxy-design.md](references/controlled-access-proxy-design.md) — Detailed design guide for controlled-access production proxies: architecture, policy structure, failure modes, redundancy
- [emergency-override-policy-template.md](references/emergency-override-policy-template.md) — Template for defining an emergency access override policy: eligibility, invocation, monitoring, testing schedule
- [audit-log-design.md](references/audit-log-design.md) — Audit log design: structured justification, granularity, auditor selection, programmatic verification

Cross-references:
- `adversary-profiling-and-threat-modeling` — identify which adversaries and attack paths make least-privilege controls most valuable

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
