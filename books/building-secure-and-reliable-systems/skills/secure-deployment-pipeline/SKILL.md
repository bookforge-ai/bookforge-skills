---
name: secure-deployment-pipeline
description: |
  Secure a software deployment pipeline against supply chain attacks from benign insiders (mistakes), malicious insiders, and external attackers: map pipeline threats to mitigations using the three-adversary threat model, generate binary provenance requirements for each build stage, define provenance-based deployment policies with choke-point enforcement, design verifiable build architecture (trusted build service, rebuild service, or hybrid), and produce a staged hardening roadmap with breakglass controls. Use when assessing supply chain security for a CI/CD pipeline, implementing binary provenance to trace artifact origins, designing deployment policies that verify what is deployed rather than who initiated deployment, hardening build infrastructure against insider threats, or establishing breakglass procedures that remain auditable. Requires secure-code-review as a prerequisite control (code review is the first mitigation layer against malicious or accidental code changes before they enter the pipeline). Produces a deployment pipeline security assessment with threat-mitigation mapping, provenance schema, policy rules, and a phased hardening plan.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/secure-deployment-pipeline
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - secure-code-review
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [14]
tags:
  - security
  - deployment
  - supply-chain
  - ci-cd
  - binary-provenance
execution:
  tier: 3
  mode: full
  inputs:
    - type: pipeline_description
      description: "Description or diagram of current CI/CD pipeline: source control system, build tooling, test infrastructure, deployment mechanism, and any existing signing or policy controls"
    - type: threat_context
      description: "Organizational context: size, insider risk tolerance, regulatory requirements, and which of the three adversary types are in scope"
  outputs:
    - type: security_assessment
      description: "Threat-mitigation mapping using Tables 14-1/14-2, binary provenance schema, deployment policy rules, verifiable build architecture recommendation, and phased hardening roadmap"
---

# Secure Deployment Pipeline

## When to Use

Use this skill when:
- You need to verify that the code running in production is the code you assume it is
- You are designing or auditing a CI/CD pipeline for insider threat resistance
- You want to implement binary provenance so artifact origins are traceable after security incidents
- You are moving from signature-based to provenance-based deployment policies
- You need to establish breakglass procedures that are auditable and rare enough to distinguish from attacks

**Prerequisite:** The `secure-code-review` skill must already be applied. Code review is the foundational mitigation — it is the multi-party authorization control that increases the cost of introducing malicious changes before they reach the pipeline. All pipeline controls assume reviewed code enters the source control system.

---

## Step 1: Define Your Adversary Scope

Before mapping threats to mitigations, identify which adversary types apply to your organization. The threat model has three types:

| Adversary | Definition | Example |
|-----------|-----------|---------|
| **Benign insider** | Engineer who makes mistakes | Accidentally builds from locally modified code with unreviewed changes |
| **Malicious insider** | Insider who tries to exceed authorized access | Deploys a modified binary that exfiltrates customer credentials |
| **External attacker** | Compromises machine or account of one or more insiders | Uses a compromised engineer account to push a backdoored build script |

**Why this matters:** Mitigations have different effectiveness profiles against each adversary type. Code review deters malicious insiders but does not protect against collusion or external attackers who compromise multiple accounts simultaneously. Automation eliminates benign-insider build mistakes but introduces its own attack surface if not locked down. Knowing your adversary scope lets you prioritize controls and document known limitations honestly.

**Output:** A written adversary scope statement: which adversary types are in scope, which are out of scope and why, and any known limitations.

---

## Step 2: Map Your Pipeline Threats (Table 14-1)

Walk through each threat category and record: the threat, your current mitigation, and the limitation of that mitigation.

**Threat-mitigation mapping (Table 14-1 — basic best practices):**

| Threat | Mitigation | Known Limitation |
|--------|-----------|-----------------|
| Engineer accidentally introduces a vulnerability | Code review + automated testing | Does not catch all vulnerabilities |
| Malicious insider submits a change with a backdoor | Code review (increases cost; adversary must craft change to pass review) | Does not protect against collusion or external attackers compromising multiple accounts |
| Engineer accidentally builds from locally modified unreviewed code | Automated CI/CD system always pulls from the correct source repository | None if CI/CD is properly locked down |
| Engineer deploys a harmful configuration (e.g., debug features enabled in production) | Treat configuration as code: require configuration changes to be checked in, reviewed, and tested like any code change | Not all configuration can be treated as code |
| Malicious insider deploys a modified binary that exfiltrates data | Production environment requires proof that the CI/CD system built the binary; CI/CD pulls only from the correct source repository | Adversary may exploit breakglass procedures; mitigated by logging and auditing |
| Malicious insider modifies cloud bucket ACLs to exfiltrate data | Treat resource ACLs as configuration; restrict changes to the deployment process only | Does not protect against collusion |
| Malicious insider steals the integrity signing key | Store signing key in a key management system accessible only to the CI/CD system; require key rotation | See "Advanced Mitigation Strategies" for build-specific hardening |

For each row, fill in your current state. Threats with no mitigation or with significant limitations are your highest-priority gaps.

**Why configuration-as-code is non-negotiable:** Engineers understand they should not build a production binary from a locally modified source copy. But many do not apply the same discipline to configuration. Treating configuration as code — version-controlled, peer-reviewed, tested before deployment — reuses all existing supply chain controls at no additional architectural cost.

---

## Step 3: Verify Artifacts, Not Just People

The key principle: deployment environments should verify **what** is being deployed, not only **who** initiated the deployment. An actor can make a mistake or may be intentionally deploying a malicious change regardless of authorization level.

**Implementation:**
- Deployment environments must require proof that each automated step of the deployment process occurred
- Humans must not be able to bypass automation unless some other mitigating control checks that bypass action (logging, alerting, post-deployment audit)
- Place deployment decisions at proper **choke points** — points through which all deployment requests must flow. In Kubernetes, the master node is the choke point; configure worker nodes to accept requests only from the master. Add an Admission Controller webhook or Binary Authorization for policy enforcement.

**Two choke point architectures:**
1. **Direct enforcement:** The choke point itself evaluates the policy (e.g., Kubernetes Admission Controller)
2. **Proxy enforcement:** A proxy in front of the choke point evaluates the policy — but the admission point must be configured to accept access only via the proxy, or adversaries bypass it directly

---

## Step 4: Design Binary Provenance for Each Build Stage

Every build stage must produce **binary provenance**: a cryptographically authenticated record of exactly how the artifact was built — inputs, transformation, and the entity that performed the build.

**Why provenance is required beyond auditing:** Without provenance, you cannot know what source code a deployed binary came from. During a security incident, reverse engineering a binary is prohibitively expensive; inspecting version-controlled source is fast. Provenance is also the prerequisite for provenance-based deployment policies (Step 5).

**Binary provenance schema — required fields:**

| Field | Required | Description |
|-------|----------|-------------|
| **Authenticity** | Yes | Cryptographic signature covering all other fields. Verifies which system produced the provenance and establishes integrity. Usually a signing key accessible only to the CI/CD system. |
| **Outputs** | Yes | The output artifacts this provenance applies to, each identified by a cryptographic hash of the artifact content (SHA-256). |
| **Inputs: Sources** | Recommended | The top-level input artifacts — e.g., "Git commit `270f...ce6d` from `https://github.com/org/repo`" or "file `foo.tar.gz` with SHA-256 `78c5...6649`". Each input should have both an identifier (URI) and a version (cryptographic hash). |
| **Inputs: Dependencies** | Recommended | All other artifacts needed for the build — libraries, build tools, compilers — that are not fully specified in sources. Each can affect build integrity. |
| **Command** | Recommended | The command used to initiate the build, structured for automated analysis. Example: `{"bazel": {"command": "build", "target": "//main:hello-world"}}` |
| **Environment** | Optional | Architecture details, environment variables, and any other information needed to reproduce the build. |
| **Input metadata** | Optional | Metadata about inputs that downstream systems will find useful (e.g., source commit timestamp used by a policy evaluation system). |
| **Debug info** | Optional | Information useful for debugging but not required for security (e.g., machine on which the build ran). |
| **Versioning** | Recommended | Build timestamp and provenance format version number, enabling format changes without rollback attack susceptibility. |

**Attack surface awareness:** Any input not checked by the build system (and therefore not implied by the signature) and not included in the sources (and therefore not peer reviewed) is a vector. If users can specify arbitrary compiler flags, the verifier must validate those flags explicitly.

**Propagation guidance:** Strongly prefer propagating provenance inline with the artifact (e.g., as a Kubernetes annotation passed to the Admission Controller webhook) rather than storing in a separate database keyed by artifact hash. Database-keyed lookup causes ambiguity when the same artifact hash appears in multiple provenance records, produces unactionable error messages, and introduces latency that may exceed deployment SLOs.

---

## Step 5: Define Provenance-Based Deployment Policies

A deployment policy describes the intended properties of each deployment environment. The deployment environment matches this policy against the binary provenance of each artifact at deployment time.

**Why provenance-based policies outperform pure code signing:**
- Reduces implicit assumptions throughout the supply chain, making each step's contract explicit and auditable
- Clarifies the responsibility of each pipeline stage, reducing misconfiguration
- Allows a single signing key per build step (not per deployment environment), because the provenance record carries the environment-specific information

**Example policy rules to implement (tailor to your threat model):**

1. Source code was submitted to version control and peer reviewed
2. Source code came from an approved repository (specific URI and build target)
3. Build was performed through the official CI/CD pipeline (not a local workstation)
4. Tests passed (the test result is an artifact in the provenance chain)
5. The binary type is explicitly allowed for this environment (no "test" binaries in production)
6. The code version or build is sufficiently recent (blocks rollback to versions with known vulnerabilities)
7. Code passed a security vulnerability scan within the last N days

**Three-step policy implementation:**
1. **Verify provenance authenticity** — cryptographically validate the signature to prevent tampering or forgery
2. **Verify provenance applies to the artifact** — compare the cryptographic hash of the artifact to the hash in the provenance payload, preventing "good provenance applied to bad artifact" attacks
3. **Verify provenance meets all policy rules** — evaluate each rule in the deployment policy against provenance field values

**Design rules:**
- Make provenance unambiguous: one artifact, one provenance record per build
- Make policies unambiguous: one policy applies to any given deployment. If two policies could apply, resolve it as a meta-policy (require both to pass) rather than leaving it ambiguous
- Provide actionable error messages: when a deployment is rejected, the message must explain what went wrong and how to fix it (e.g., "source URI was X, policy requires Y; rebuild from Y or update the policy to allow X")

---

## Step 6: Address Advanced Threats (Table 14-2)

Four threats remain unaddressed by basic best practices alone. Apply these advanced mitigations for high-security or large organizations:

**Threat-mitigation mapping (Table 14-2 — advanced):**

| Threat | Advanced Mitigation |
|--------|-------------------|
| Engineer deploys an old version of code with a known vulnerability | Deployment policy requires the code to have undergone a security vulnerability scan within the last N days |
| CI system misconfigured to allow builds from arbitrary source repositories; malicious adversary builds from a repo containing malicious code | CI system generates binary provenance recording which source repository it pulled from; production deployment policy requires provenance proving the artifact originated from an approved repository |
| Malicious adversary uploads a custom build script that exfiltrates the signing key, then signs and deploys a malicious binary | Verifiable build system uses privilege separation: the component that runs custom build scripts (the worker) has no access to the signing key. Only the trusted orchestrator process holds the key. |
| Malicious adversary tricks the CD system into using a backdoored compiler or build tool | Hermetic builds require developers to explicitly specify the compiler and build tool in the source code (fully pinned, peer-reviewed like any other code change). The orchestrator fetches these tools; the worker has no ability to substitute them. |

**Verifiable build architecture — three options:**

| Architecture | How it works | Best for |
|-------------|-------------|---------|
| **Trusted build service** | A central service the verifier trusts signs provenance with a key only it holds. Build once; no reproducibility required. | Most organizations; used by Google internally |
| **Rebuild service** | Verifier reproduces the build and checks bit-for-bit identical output. Requires full reproducibility. | Not scalable (builds take minutes; deployments need milliseconds) |
| **Rebuilding service** | A quorum of independent rebuilders attest to provenance. Hybrid of the two above. | Open source projects (Debian model) where central authority is infeasible |

**Hermetic build requirements (prerequisite for the advanced mitigations above):**
- All inputs to the build (sources, compilers, libraries) are fully specified up front, outside the build process, with unambiguous versions (cryptographic hashes or fully resolved version numbers)
- The orchestrator fetches all inputs; the worker executes build steps in isolation with no network access to arbitrary sources
- Benefits: enables CVE scanning against the full dependency graph, guarantees third-party import integrity, enables cherry-picking (patch + rebuild without extraneous behavior changes from a different compiler version)

---

## Step 7: Design Breakglass Controls

In emergencies (e.g., an outage requiring an immediate configuration change that would take too long through the normal pipeline), engineers may need to bypass the deployment policy.

**Breakglass design requirements:**

- **Every breakglass deployment must raise an alarm immediately** — not after the fact, but at the moment of use
- **Every breakglass deployment must be audited quickly** — the audit must occur while the context is fresh
- **Breakglass events must be rare** — if there are too many breakglass events, it becomes impossible to differentiate malicious activity from legitimate emergency use. The rarity threshold is your primary security property: if breakglass is routine, it provides no security
- **Log sufficient information** — logs must capture enough state to reconstruct the full policy decision after the fact, including the state of any external systems the policy depended on at decision time

**Post-deployment verification (required even with enforcement):**
Even when deployment policies are enforced at the choke point, run post-deployment verification because:
- Policies can change; existing deployments must be re-evaluated against new policy versions
- The enforcement decision service may have been unavailable, causing a "fail open" deployment
- Breakglass may have been used
- Dry-run mode surfaces policy violations without blocking deployment (useful when first rolling out enforcement)
- Forensic investigators need the deployment record after incidents

---

## Step 8: Staged Hardening Roadmap ("Take It One Step at a Time")

Implementing the full supply chain security model requires many changes. Attempting all of them simultaneously risks disrupting engineering productivity and causing outages. Secure one aspect of the supply chain at a time.

**Recommended sequence:**

| Phase | Focus | Key Actions |
|-------|-------|------------|
| **Phase 1: Foundational** | Eliminate human-in-the-loop build steps | Automate all build, test, and deploy steps; script everything so humans and automation execute identical steps; establish code review as mandatory (depends on `secure-code-review`) |
| **Phase 2: Configuration control** | Extend supply chain discipline to configuration | Treat all configuration as code: check in, review, and test before deployment; restrict direct configuration changes to the deployment process only |
| **Phase 3: Artifact verification** | Verify what is deployed, not just who deploys | Add binary provenance to CI/CD output; configure deployment choke points to require provenance; implement basic deployment policies |
| **Phase 4: Advanced hardening** | Address insider and sophisticated external threats | Implement privilege separation in build system (orchestrator + isolated worker); require hermetic builds; add provenance-based policies covering source repository, scan recency, and version recency |
| **Phase 5: Breakglass and monitoring** | Close the auditability gap | Implement breakglass with immediate alerting; enable post-deployment verification; run dry-run mode before enforcing new policies |

**Lock down the automated system itself:** For each path where an administrator can make a change without review — configuring the CI/CD pipeline directly, using SSH to run commands on the build machine — implement a mitigation that requires peer review for that path. This is the hardest step and the one most commonly skipped.

---

## Output Format

Produce a deployment pipeline security assessment with these sections:

1. **Adversary scope** — which of the three adversary types are in scope and why
2. **Threat-mitigation gap table** — current mitigations and limitations for each threat in Tables 14-1 and 14-2, with gaps highlighted
3. **Binary provenance schema** — which fields are required for your pipeline stages, with specific values for the Outputs and Sources fields
4. **Deployment policy rules** — ordered list of policy rules for each deployment environment, with the provenance fields each rule inspects
5. **Verifiable build architecture recommendation** — which of the three architectures fits your organization, with rationale
6. **Phased hardening roadmap** — which phase you are currently in, what changes Phase N+1 requires, and acceptance criteria for each phase
7. **Breakglass policy** — who can invoke breakglass, what is logged, how quickly audits must occur, and what the expected rarity threshold is

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-secure-code-review`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
