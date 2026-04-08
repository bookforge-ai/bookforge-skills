---
name: security-change-rollout-planning
description: |
  Plan and execute a security change rollout across a service or fleet: classify the change into a time horizon (short / medium / long-term), triage affected systems by risk tier, select the appropriate rollout strategy with canarying and staged deployment, define communication strategy (internal and external), set rollback and success criteria, and produce a written rollout plan. Use when you need to respond to a zero-day vulnerability, roll out a security posture improvement, or drive an ecosystem or regulatory compliance change. Handles timeline disruption scenarios: accelerate when an exploit goes public, slow down when patch instability is detected, delay when embargo, external dependency, or limited blast radius dictates caution. Produces a rollout plan with timeline, per-tier risk triage, communication strategy, and explicit rollback criteria. Examples covered: Shellshock emergency patch, hardware security key (FIDO/WebAuthn) company-wide deployment, and Chrome HTTPS migration.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/security-change-rollout-planning
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [7]
tags:
  - security
  - change-management
  - rollout-planning
  - patch-management
  - vulnerability-response
  - zero-day
  - incident-response
  - compliance
  - sre
  - reliability
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Description of the security change: what is changing, why, which systems or users are affected, and any known deadline or embargo constraints"
    - type: codebase
      description: "Optional: infrastructure config, dependency manifests, or service inventory if available — used to identify affected systems and their tier"
  tools-required: [Read, Write]
  tools-optional: [Grep, Bash]
  mcps-required: []
  environment: "Can run from any project directory. Asks structured questions if system context is not provided. Produces a written rollout plan document."
discovery:
  goal: "Produce a security change rollout plan: horizon classification, per-tier risk triage, phased timeline with success criteria, communication strategy, and rollback criteria"
  tasks:
    - "Classify the change into its time horizon: short-term (zero-day, hours–days), medium-term (posture improvement, weeks–months), or long-term (ecosystem/regulatory, months–years)"
    - "Triage affected systems by risk tier: identify which systems are highest risk and must be patched first"
    - "Design the rollout phases with canarying and staged deployment"
    - "Define per-phase success criteria that must be met before proceeding"
    - "Draft internal and external communication strategy and timeline"
    - "Define rollback criteria and rollback mechanism for each phase"
    - "Identify 'when plans change' scenarios and produce contingency branches"
  audience:
    roles: ["security-engineer", "site-reliability-engineer", "software-engineer", "platform-engineer", "tech-lead", "incident-commander"]
    experience: "intermediate — assumes familiarity with release engineering basics and production system concepts"
  triggers:
    - "A new vulnerability (zero-day or CVE) has been disclosed and patch readiness must be assessed"
    - "Planning a security posture improvement (e.g., new authentication mechanism, encryption upgrade)"
    - "Responding to a regulatory or ecosystem change with a compliance deadline"
    - "An ongoing rollout needs to be accelerated because an exploit became publicly available"
    - "An in-flight security patch is causing instability and needs to be slowed or rolled back"
    - "Deciding how to handle a vulnerability that is currently under embargo"
  not_for:
    - "Designing the security change itself (what to fix) — use adversary-profiling-and-threat-modeling for that"
    - "Active incident response once an exploit is in progress — use incident response runbooks for that"
    - "Compliance gap analysis or regulatory interpretation"
---

## When to Use

Use this skill when you have a security change to roll out and need a plan — not just a patch, but a structured rollout with appropriate speed, staged deployment, communication, and contingency handling.

The core decision the skill drives is: **how fast, and how?** Security changes impose a fundamental tradeoff: speed reduces exposure time but increases the risk of rolling out a broken patch that causes downtime or data loss. The right answer depends on whether the change is short-term (a zero-day requiring emergency response in hours), medium-term (a posture improvement that can proceed in weeks), or long-term (an ecosystem migration spanning months to years).

Invoke this skill when:
- A CVE or zero-day has been disclosed and you need to decide how quickly to patch which systems
- You are rolling out a new security control (new authentication method, encryption upgrade, policy enforcement) and need a phased plan
- A regulatory or compliance deadline requires a multiyear migration across systems you do not fully control
- An ongoing rollout is being disrupted — by an exploit going public, a patch causing errors, or an embargo being broken early

Do not use this skill to design what the fix should be (that is threat modeling) or to manage an active exploit in real time (that is incident response).

---

## Context and Input Gathering

Before producing the rollout plan, gather the following:

1. **Change description**: What is changing? Is it a patch to a library or binary, a configuration change, a new mandatory control, or a protocol migration?
2. **Triggering event**: Is this reactive (zero-day, active exploit, regulatory deadline) or proactive (internal security posture goal)?
3. **Embargo status**: Is the vulnerability currently under embargo? Is there a public announcement date? Has the embargo been broken?
4. **Affected systems**: Which services, hosts, binaries, or user populations are affected? Do you have an inventory, or must one be built?
5. **System diversity**: Are affected systems standardized (same OS, same distribution, same dependency version) or heterogeneous (different versions, inherited infrastructure, nonstandard configurations)?
6. **Team dependencies**: Does the rollout require other teams to act? Are you dependent on a vendor releasing a patch, or on client systems being updated before or after your server?
7. **Patch availability**: Is a patch or remediation available? Has it been verified against the actual vulnerability? Does it address all known variants?
8. **Existing release infrastructure**: Do you have automated testing, canarying, staged rollout tooling? Are your dependencies up to date and frequently rebuilt? Do you use containers or microservices that make patching independent?
9. **Success metrics**: How will you know the rollout succeeded? Is there instrumentation to detect unpatched systems? Can you measure whether the vulnerability is still present?

If a system inventory is not available, ask the engineer to describe: the three highest-risk systems that must be patched first, the number of systems in scope, and whether nonstandard or inherited infrastructure exists.

---

## Process

### Step 1 — Classify the Change Into Its Time Horizon

**WHY**: The time horizon determines everything that follows — the planning depth, rollout speed, communication strategy, and success criteria. A plan designed for a week-long rollout is wrong for a same-day emergency. A plan designed for a same-day emergency applied to a years-long ecosystem migration wastes time and breaks systems unnecessarily.

Classify the change using this taxonomy:

| Horizon | Trigger type | Target timeline | Primary risk |
|---|---|---|---|
| **Short-term** | Zero-day vulnerability, active exploit, critical CVE | Hours to days | Moving too slowly; exploit window grows |
| **Medium-term** | Security posture improvement, new control, proactive hardening | Weeks to months | Insufficient stakeholder buy-in; long tail of unpatched systems |
| **Long-term** | Ecosystem change, regulatory requirement, protocol migration | Months to years | Loss of momentum; leadership support eroding; documentation rot |

Classification inputs:
- **Severity**: Is the vulnerability actively exploited or being exploited in the wild? Is it critical (remote code execution, key disclosure) or informational?
- **Deadline**: Is there a compliance date, embargo lift date, or news embargo?
- **Dependent parties**: Does rollout require waiting for a vendor, for clients to patch first, or for other teams to implement prerequisites?
- **Sensitivity**: Is this a mandatory enforcement or a gradual opt-in? Can it roll out team by team?

Zero-day response almost always classifies as short-term. Before prioritizing same-day zero-day response, confirm that the "top hits" — the highest-impact vulnerabilities from recent years — are already patched. A zero-day response against a system that is unpatched for known critical vulnerabilities is the wrong priority order.

### Step 2 — Triage Affected Systems by Risk Tier

**WHY**: Not all systems carry the same risk from a given vulnerability. Treating a low-risk internal analytics server the same as a publicly exposed TLS endpoint wastes capacity and may slow the critical path. Triage directs limited remediation capacity to the highest-leverage systems first.

For each system or system group in scope, assess:

- **Exposure**: Is this system directly accessible from the internet, from partners, or only internally? Does it handle the specific protocol, library, or configuration that is vulnerable?
- **Exploitability in context**: Even if the vulnerability is critical in general, can it be triggered against this system? (A bash vulnerability doesn't affect a Go binary that never invokes bash.)
- **Blast radius**: What is the impact if this system is compromised? Does it hold customer data, encryption keys, authentication credentials, or production secrets?
- **Patchability**: Is the system running a standard distribution that already has a patched package? Does it require manual intervention, custom build, or vendor coordination?

Assign each system to a tier:

| Tier | Definition | Rollout approach |
|---|---|---|
| **Tier 1 — Critical** | Externally exposed, high blast radius, actively exploitable | Patch first; use accelerated rollout; accept faster-than-normal validation |
| **Tier 2 — High** | Internally exposed or high blast radius but not directly reachable | Patch in next wave; standard validation |
| **Tier 3 — Standard** | Low blast radius, standardized infrastructure | Patch via normal automated rollout |
| **Tier 4 — Nonstandard** | Inherited, heterogeneous, or vendor-dependent systems | Manual intervention; send per-team notifications with explicit action items |

Shellshock pattern: at Google, Tier 1 production servers (standard distribution, easy automated rollout) were patched first and fastest. Tier 2 workstations were easy to patch quickly but required different tooling. Tier 4 nonstandard servers required manual notifications with explicit follow-up actions per team.

### Step 3 — Design the Rollout Phases

**WHY**: Rolling a change out all at once maximizes exposure risk if the patch is broken or has unexpected interaction effects. A gradual rollout — with instrumentation for canarying — lets you detect problems before they affect your entire infrastructure. This principle holds even on accelerated timelines.

For each change, define rollout phases with explicit gates between them:

**Standard phased rollout structure**:

1. **Canary phase**: Apply the change to a small, monitored subset (e.g., 1–5% of systems or a single team). Run long enough to detect error rate changes, performance regressions, or unexpected behavior. For a zero-day, this phase may be compressed to minutes rather than days.
2. **Staged expansion**: Expand to progressively larger population segments, with monitoring confirmation between each stage. Prefer expansion by logical group (team, system tier, geographic region) rather than random percentage — this makes rollback bounded.
3. **Full rollout**: Apply to remaining systems. For Tier 4 nonstandard systems, issue per-team action items and track completion separately from the automated rollout.

**Per-phase definition**:
- Scope: which systems or users are included
- Duration: minimum time at this phase before advancing
- Success criteria: what must be true before advancing (error rate, patch confirmation, monitoring signal)
- Rollback trigger: what would cause an immediate rollback at this phase

**Change design properties that make every phase safer** (implement these before rollout, not during):
- **Incremental**: Keep the change as small and standalone as possible. Do not bundle security fixes with unrelated refactoring.
- **Documented**: Record the "how" and "why," the systems and teams in scope, lessons from any proof of concept, the rationale for key decisions, and points of contact.
- **Tested**: Cover the change with unit tests and, where possible, integration tests. Complete a peer review.
- **Isolated**: Use feature flags to isolate the change. The system should exhibit no behavior change with the flag off.
- **Qualified**: Use your normal binary release process — proceed through qualification stages before reaching production traffic.
- **Staged**: Instrument for canarying. You should be able to observe differences in behavior before and after your change.

### Step 4 — Set Per-Phase Success Criteria and Rollback Criteria

**WHY**: Advancing through phases without explicit criteria leads to either excessive caution (delayed rollout, extended exposure) or insufficient caution (rolling a broken patch to the full fleet). Pre-defined criteria remove the need for judgment calls under pressure.

**Success criteria** (must be satisfied before advancing to next phase):
- Error rate: less than X% increase in errors, latency, or failure rate after the change
- Patch confirmation: instrumentation or scanning confirms affected systems have the updated version
- Monitoring signal: no unexpected alerts or on-call pages directly attributable to the change
- User feedback: for user-facing changes, no significant increase in support tickets or failure reports

**Rollback criteria** (trigger immediate rollback):
- Error rate exceeds threshold (define the number: e.g., 5% increase in 5xx responses)
- On-call pages attributable to the change
- Patch introduces a regression that is worse than the original vulnerability's blast radius
- Critical dependency fails after the patch is applied

**Rollback mechanism**: Define how rollback works before the rollout begins. For binary patches: roll back to the previous version via the same release pipeline. For configuration changes: revert the config and push. For user enrollment changes: define the off-ramp (e.g., allow users to use the legacy path temporarily). If rollback requires significant manual effort, flag this as a risk before the rollout begins.

### Step 5 — Plan Internal and External Communication

**WHY**: A technically sound rollout can fail due to communication gaps. Internal teams that are not informed prepare no coverage and escalate incorrectly. Externally, users and partners who are surprised by behavior changes lose trust. Early and clear communication also prevents PR problems from becoming the bottleneck during a live vulnerability response.

**Internal communication**:
- Announce the change and its timeline to all affected teams before the rollout begins, not during
- For Tier 4 nonstandard systems: send per-team notifications with explicit action items, deadlines, and escalation contacts — do not rely on them to discover the requirement from a general announcement
- For embargoed vulnerabilities: communicate internally under NDA or internal secrecy protocols as permitted; plan internal communications so they are ready to send the moment the embargo lifts
- Provide a single dashboard or tracking sheet that shows patch progress by system tier — this allows leadership reporting and team self-service progress checking
- Establish a feedback loop: define how teams report completion and how issues are escalated

**External communication**:
- Prepare external communications (to customers, partners, and the public) before the rollout begins, not during — PR approval cycles are slow and incompatible with emergency response timelines
- For zero-day responses: draft the customer-facing message, the partner notification, and the public statement ahead of time. Be ready to send at embargo lift.
- For medium-term changes affecting users: give ample advance notice. Use all available outreach channels (email, developer mailing lists, help forums, partner relationships). Overcommunication maximizes reach.
- For long-term ecosystem changes: tailor outreach regionally and by stakeholder group. Data-driven targeting (identify which regions are lagging, which stakeholder types need different messaging) improves coverage.
- Tie the change to business value whenever possible. Security-only messaging fails to motivate organizations that are not already security-first. Link the change to business benefits (performance, new features, compliance relief, liability reduction).

### Step 6 — Produce the Rollout Plan Document

**WHY**: A written plan enables handoff continuity (individuals leave or rotate), provides a reference during the rollout to avoid judgment calls under pressure, and serves as the audit trail for leadership reporting and post-mortems.

The rollout plan document should include:

```
Security Change Rollout Plan
=============================
Change: [name / CVE / description]
Horizon: [short / medium / long-term]
Author(s): [points of contact]
Status: [draft / approved / in-progress / complete]

## Summary
[1–3 sentences: what is changing, why, and the target completion date]

## Affected Systems
[Table: System/tier | Risk tier | Patch method | Owner | Estimated effort]

## Phase Plan
[For each phase:]
  Phase N — [name]
  Scope: [systems or user population]
  Timeline: [start date / duration]
  Success criteria: [specific measurable conditions]
  Rollback trigger: [specific conditions]
  Rollback mechanism: [how to execute rollback]

## Communication Plan
  Internal: [who is notified, when, via what channel]
  External: [who is notified, when, via what channel]
  Embargo handling: [if applicable]

## Contingency Branches
  Accelerate trigger: [e.g., exploit goes public]
  → Accelerate action: [reorder tiers, prioritize Tier 1 only, accept reduced validation window]
  Slow-down trigger: [e.g., patch causing errors above threshold]
  → Slow-down action: [pause expansion, rollback canary, debug and reissue]
  Delay trigger: [e.g., vendor patch not available, external dependency not ready]
  → Delay action: [apply mitigations, set new target date, notify stakeholders]

## Success Metrics
[How will you confirm the rollout is complete and the vulnerability is mitigated?]
```

---

## Key Principles

**Classify before planning.** The time horizon is not an output of planning — it is the input. Get the horizon wrong and every downstream decision (speed, validation, communication) is calibrated incorrectly.

**Patch the top hits first.** Before prioritizing same-day zero-day response, confirm that known high-impact vulnerabilities from recent years are already remediated. Zero-day response against a system with unpatched known criticals is the wrong priority order.

**Gradual rollout applies even on emergency timelines.** Even for a zero-day, roll out in phases with canarying. The risk of deploying a broken patch — causing downtime across the fleet — can exceed the risk of the vulnerability itself during the patching window. On an accelerated timeline, "gradual" means hours rather than days, not "skip canarying."

**Standardization is leverage.** Rollout speed scales with how standardized your system fleet is. A single OS distribution and package format means a verified patch can be automated immediately. Heterogeneous infrastructure (different distributions, different versions, inherited systems) requires manual intervention that does not scale. Invest in standardization before the emergency.

**When plans change, do not panic — but do not be surprised.** Embed contingency branches in the plan from the start. Define in advance: what triggers acceleration, what triggers a slowdown, what triggers a full delay. When the trigger fires, execute the prepared branch rather than improvising.

**Overcommunicate externally, especially for long-term changes.** Organizations resistant to change (including security changes) respond to business-aligned messaging more than security messaging alone. Tie the change to business benefits. Use every available outreach channel. Expect a long tail of non-compliant systems and plan for it explicitly.

**Architecture as rollout enabler.** The ease of rolling out any security change is determined by architectural decisions made long before the change. Frequent builds and rebuilds ensure the latest patched dependencies are always available. Containers and immutable images allow patch-as-code-rollout. Microservices scope the blast radius of each change and enable independent rollout per service. Automated testing gives confidence to push faster. Build these before the emergency — they are not alternatives to a rollout plan, they are what makes any rollout plan executable.

---

## Examples

### Example 1 — Short-Term: Shellshock Zero-Day (Google, September 2014)

**Scenario**: On the morning of September 24, 2014, Google Security learned of a publicly disclosed, remotely exploitable vulnerability in `bash` that trivially allowed code execution on affected systems. Exploits appeared in the wild the same day.

**Horizon classification**: Short-term. Actively exploited the same day. Emergency response timeline.

**Triage**:
- Tier 1 (low risk to patch, automated rollout): Majority of production servers. Patched fastest, with reduced validation window once servers passed sufficient validation and testing.
- Tier 2 (higher risk, easy to patch quickly): Workstations. Patched quickly with different tooling.
- Tier 4 (high risk, nonstandard): Small number of nonstandard servers and inherited infrastructure. Required manual intervention. Per-team notifications sent with explicit action items to enable tracking progress at scale.

**Key execution decisions**:
- Parallel workstream: software was developed to detect vulnerable systems within the network perimeter, then integrated into standard security monitoring as a permanent capability.
- Communication: internal communication to all potentially affected teams; external communication to partners and customers prepared as early in the response as possible to avoid PR bottlenecks.

**Lessons**:
- Standardize software distribution to the greatest extent possible. Non-standard distributions made patching harder and slower.
- Use public distribution standards. Patches in standard format can be applied immediately without rework.
- Ensure your automated rollout mechanism can accelerate for emergency changes without skipping functional validation entirely.
- Have monitoring to track rollout progress and identify unpatched systems in real time.
- Prepare external communications before the response, not during it.

### Example 2 — Medium-Term: Hardware Security Keys (FIDO/WebAuthn) Company-Wide Deployment (Google, 2013–2015)

**Scenario**: One-time passwords (OTPs) were susceptible to phishing interception. Starting in 2011, Google evaluated stronger two-factor authentication methods. By 2013, hardware security keys (FIDO/WebAuthn) were selected and rollout began. Full OTP deprecation was completed in 2015.

**Horizon classification**: Medium-term. Proactive security posture improvement. Gradual, multi-year rollout.

**Rollout strategy**:
- Initially opt-in (easiest use case first): users who enrolled voluntarily reduced total authentication time — keys were simpler than OTPs, removing the need to type a code.
- Self-service enrollment: users registered via a web-based enrollment portal. Physical distribution at office IT helpdesks for first adopters and those needing assistance. Keys trusted on first use (TOFU).
- Application migration: systems using centrally generated OTPs were migrated application by application, tracked by monitoring which applications were still generating OTP requests. Long-tail applications were handled by working directly with vendors to add support.
- Enforcement: in 2015, users received reminders when they used OTPs instead of security keys, then eventually OTP access was blocked.
- Exception handling: for cases where security keys could not yet be used (mobile device setup), a web-based OTP generator was created requiring the user to authenticate with their security key first — a degraded but auditable fallback.

**Lessons**:
- Ensure the solution works for all users, including those with accessibility requirements.
- Make the change easier to adopt than the prior method — a self-service change with lower friction succeeds faster than a mandated change with friction.
- Make the feedback loop on noncompliance fast (minutes to hours, not days).
- Track progress and identify the long tail of use cases from the start, not after completion.
- Rotate encryption keys and other secrets regularly as a practice habit so emergency key rotation (e.g., after Heartbleed) is not a Herculean effort.

### Example 3 — Long-Term: HTTPS Migration (Chrome / Web Ecosystem, 2017–2019+)

**Scenario**: HTTPS provides confidentiality and integrity guarantees critical to the web. The Chrome team drove adoption across the entire web ecosystem through a combination of incentives, warnings, and coordination with standards bodies, certificate authorities, and other browser vendors.

**Horizon classification**: Long-term. External ecosystem change. Required new systems to be built. Target timeline: years.

**Rollout strategy**:
- Data-driven targeting: gathered data on HTTPS usage worldwide, surveyed end users on browser UI perception, measured site behavior to identify features that could be restricted to HTTPS, used case studies to understand developer concerns.
- Graduated warnings: Chrome warnings for insecure pages rolled out gradually over years, with user behavior telemetry monitored to confirm no unexpected negative effects (e.g., retention drop, engagement decline).
- Overcommunication: every available outreach channel used before each change — blogs, developer mailing lists, press, help forums, partner relationships. Regional tailoring (e.g., additional focus on Japan when adoption was lagging due to slow uptake by top sites).
- Business incentive linkage: enabled HTTPS-only features (Service Workers, push notifications, background sync) to give security-resistant organizations a business reason to migrate, not just a security reason.
- Industry consensus building: coordinated with other browser vendors and certificate authorities so HTTPS became an industry-wide trend, not a Chrome-specific imposition.

**Result**: Chrome users' time on HTTPS sites rose from approximately 70% (Windows) and 37% (Android) to over 90% on both platforms.

**Lessons**:
- Understand the ecosystem before committing to a strategy. Research stakeholder groups quantitatively and qualitatively before designing the rollout.
- Overcommunicate to maximize reach. Use every available channel.
- Tie security changes to business incentives. Security-only messaging fails to move organizations that are not already security-driven.
- Build industry consensus where possible. A change that is seen as an industry-wide trend is far easier to drive than one seen as a single vendor's imposition.
- Plan for 80–90% adoption as a meaningful success if 100% is not required — achieving near-complete adoption of a long-tail change is itself a significant risk reduction.

---

## References

- [three-horizon-classification.md](references/three-horizon-classification.md) — Full taxonomy: short / medium / long-term change triggers, timelines, planning depth, and success criteria
- [system-triage-matrix.md](references/system-triage-matrix.md) — Risk tier classification (Tier 1–4): exposure, exploitability, blast radius, patchability definitions
- [rollout-phase-template.md](references/rollout-phase-template.md) — Per-phase template: scope, duration, success criteria, rollback trigger, rollback mechanism
- [communication-strategy-guide.md](references/communication-strategy-guide.md) — Internal and external communication playbook for each time horizon; embargo handling guidance
- [when-plans-change.md](references/when-plans-change.md) — Contingency branches: accelerate, slow down, and delay triggers with corresponding tactics
- [architecture-as-enabler.md](references/architecture-as-enabler.md) — How frequent builds, containers, microservices, and automated testing reduce rollout friction for all future security changes

Cross-references:
- `adversary-profiling-and-threat-modeling` — determine what you are defending against before designing the change
- `resilience-and-blast-radius-design` — design system architecture to reduce the blast radius of any given change or compromise

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
