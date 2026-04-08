---
name: adversary-profiling-and-threat-modeling
description: |
  Profile the likely adversaries targeting a system and produce a structured threat model with prioritized threat scenarios. Use when: designing a new system or service and need to identify who might attack it and how; evaluating whether existing security controls address the right threats; preparing a threat model document for a security review, compliance audit, or architecture decision record; assessing insider risk for a system that handles sensitive data or privileged operations; or mapping attack lifecycle stages to defensive controls. Applies the three adversary frameworks — attacker motivations, attacker profiles, and attack lifecycle stages — alongside a four-dimension actor-motive-action-target threat scenario matrix to produce ranked threat scenarios. Distinct from vulnerability assessment (which audits specific technical flaws) and penetration testing (which actively exploits weaknesses). Produces: adversary profile summary, insider risk matrix, threat scenario list ranked by likelihood and impact, and per-stage defensive control recommendations.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/adversary-profiling-and-threat-modeling
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [2]
tags:
  - security
  - threat-modeling
  - adversary-analysis
  - risk-assessment
  - insider-threat
  - attack-lifecycle
  - kill-chain
  - threat-intelligence
  - security-design
  - nation-state
  - criminal-actors
  - hacktivism
  - vulnerability-research
  - tactics-techniques-procedures
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "System design document, architecture diagram, or description of the system being modeled — including what data it stores, what services it exposes, and who uses it"
    - type: codebase
      description: "Optional: existing codebase, infrastructure config, or security policies to enrich the threat model with concrete system context"
  tools-required: [Read, Write]
  tools-optional: [Grep, Bash]
  mcps-required: []
  environment: "Runs in conversation or project context. Works from a system description provided by the user. Produces a threat model document."
discovery:
  goal: "Produce a structured threat model: adversary profile summary, insider risk matrix, prioritized threat scenario list, and per-stage defensive control recommendations"
  tasks:
    - "Identify the system's assets, data types, and exposure surface"
    - "Apply motivation framework to determine which attacker motivations are relevant"
    - "Match system profile to attacker profiles and assess each profile's likelihood"
    - "Map insider categories (first-party, third-party, related) and generate insider threat scenarios using the actor-motive-action-target matrix"
    - "Build external threat scenarios using the same four-dimension matrix"
    - "Plot prioritized scenarios against attack lifecycle stages"
    - "Recommend per-stage defensive controls"
  audience:
    roles: ["software-engineer", "site-reliability-engineer", "security-engineer", "architect", "tech-lead"]
    experience: "intermediate-to-advanced — assumes familiarity with system design but not necessarily with formal threat modeling"
  triggers:
    - "User is designing a new system and wants to identify who might attack it"
    - "User needs a threat model document for a security review or compliance process"
    - "User wants to understand what defenses to prioritize given their likely adversaries"
    - "User is assessing insider risk for a system with privileged access or sensitive data"
    - "User wants to map their system's threat landscape before designing security controls"
    - "User is preparing for a red team exercise or penetration test scope definition"
  not_for:
    - "Auditing specific technical vulnerabilities in code — use a vulnerability assessment process"
    - "Actively exploiting or testing defenses — use a penetration testing skill or red team process"
    - "Responding to an active incident — use an incident response skill"
---

# Adversary Profiling and Threat Modeling

## When to Use

You are helping a user build, design, or secure a system and need to produce a structured threat model — a document that identifies who is likely to attack the system, what motivates them, how they would proceed, and what defenses to prioritize.

This skill applies when the threat landscape is undefined (new system), underexamined (inherited system with no documented threats), or needs to be formalized (security review, compliance, architecture decision). It produces a concrete threat model document with ranked threat scenarios, not a general discussion of security concepts.

Threat modeling complements, but does not replace, vulnerability assessment (which finds specific technical flaws) and penetration testing (which validates exploitability). Run this skill first, then use the outputs to scope those activities.

---

## Context & Input Gathering

### Required Context (must have — ask if missing)

**1. What does the system do and what data does it handle?**

Why: The system's purpose and data profile are the primary signals for which attacker motivations apply. A payment processor attracts financially motivated criminals. A government contractor attracts nation-state actors. A messaging platform with political users attracts hacktivists. A system with no sensitive data and low public profile may realistically attract only hobbyists and automated scanners. Without this, the threat model cannot be grounded.

- Check prompt or environment for: system description, architecture docs, README, data classification labels, privacy policy, API surface description
- If missing, ask: "What does this system do, what data does it store or process, and who uses it? For example: a financial transaction API storing customer payment data, used by 500k retail customers."

**2. Who has privileged access to the system (insiders)?**

Why: Insider threats are statistically among the most impactful risk categories because insiders already have access — they bypass the entry stage of an attack entirely. Every system has insiders. The categories are: first-party (employees, interns, executives, board), third-party (contractors, vendors, open-source contributors, API partners), and related (family members, roommates, household members with physical access to devices). Skipping insider modeling produces an incomplete threat model.

- Check prompt or environment for: org chart references, team descriptions, third-party integrations, open-source contribution policy, remote work / work-from-home context
- If missing, ask: "Who has trusted access to this system or its data? This includes employees, contractors, third-party vendors with API access, and open-source contributors if applicable."

**3. Is this system or organization potentially a target of interest to sophisticated actors?**

Why: Determines whether nation-state adversaries belong in the threat model. Signals include: processing data that intelligence agencies value (communications, location, financial), supplying technology used by governments or militaries, operating in a regulated or politically sensitive sector, or being a supplier to a higher-value target. Organizations often do not realize they are attractive targets — a fitness app may reveal military base locations; a software vendor may be targeted to reach its downstream customers.

- Check prompt or environment for: customer or partner descriptions, industry sector, any government or defense relationships, supply chain position
- If missing, ask: "Does your organization handle data that a government or intelligence agency would value (user communications, location data, financial records)? Do you supply technology to government or defense customers, or to other companies that do?"

### Optional Context (enriches the model)

- **Known security incidents or near-misses:** Existing incident history is the strongest signal of which attacker profiles are already active.
- **Regulatory or compliance requirements:** GDPR, SOC 2, HIPAA, PCI-DSS often mandate specific threat categories be addressed.
- **Current security posture:** Existing controls (MFA, logging, access reviews) determine which attack lifecycle stages are already partially defended.
- **Public exposure:** Is the system internet-facing? Does it have a public bug bounty program? High public exposure attracts hobbyists and vulnerability researchers.

---

## Process

### Step 1 — Profile the System's Attractiveness to Each Attacker Motivation

Assess the system against all eight attacker motivations to determine which are plausible.

**Why:** Attackers are primarily human and their actions are goal-directed. Knowing which motivations apply eliminates implausible threat actors and focuses the model on realistic scenarios. A hobbyist is unlikely to target an obscure internal tool; a nation-state actor is unlikely to target a small consumer app with no sensitive data or geopolitical relevance. Eliminating implausible motivations prevents the threat model from becoming so broad it is useless.

Work through each motivation and rate it: **High** (a primary attacker motivation given this system), **Medium** (plausible but not primary), or **Not applicable**.

| Motivation | What it drives attackers to do | Assess for this system |
|---|---|---|
| **Fun** | Undermine security for the challenge of it | Public-facing systems with any technical complexity; hobbyists; low-barrier automated scanning |
| **Fame** | Gain notoriety by demonstrating technical skill | Systems where a breach would be publicly visible or embarrassing |
| **Activism** | Make a political statement; disrupt or deface | Systems operated by organizations with political opponents or controversial products/customers |
| **Financial gain** | Steal money, data for sale, or enable fraud | Any system handling payments, credentials, PII, or data with resale value |
| **Coercion** | Force the victim to act against their interest | Systems where disruption (ransomware, DDoS) is severely damaging and payment is preferable to downtime |
| **Manipulation** | Spread misinformation; alter data or behavior | Systems that publish content, display search results, or make automated decisions at scale |
| **Espionage** | Steal secrets; long-term persistent access for intelligence | Systems with proprietary IP, research data, user communications, or government relationships |
| **Destruction** | Sabotage; data deletion; taking the system offline | Critical infrastructure, competitors, or systems operated by organizations with powerful enemies |

**Output of this step:** A table listing each motivation with a High/Medium/Not Applicable rating and a one-sentence justification.

---

### Step 2 — Match Attacker Profiles to the System

Map the applicable motivations to attacker profiles and assess each profile's likelihood.

**Why:** Motivations identify the *why*; profiles identify the *who*. Different profiles have different capabilities, resources, and behaviors that directly determine which attack methods are feasible and which defenses are effective. A criminal actor gravitates toward the lowest-cost approach and will move to an easier target if you raise the cost of attacking you. A nation-state actor will invest significant resources and cannot be deterred by cost alone. Knowing the profile shapes the defensive strategy.

Assess each of the following profiles:

**Hobbyists and automated scanners**
Curious technologists motivated by fun or learning. Generally follow personal ethics; rarely cross into criminal behavior. However, their discoveries may be picked up by more motivated actors. Automated scanners (bots, vulnerability scanners for sale) now amplify the effective capability of low-skill actors.
- Likely for: any internet-facing system.
- Defensive priority: patch known vulnerabilities promptly; implement rate limiting; use CAPTCHA or behavioral analysis to distinguish bots from humans.

**Vulnerability researchers**
Security professionals who find and report flaws, motivated by financial reward (bug bounties) or professional reputation. Operate within disclosure norms; typically notify the organization before going public. Can be allies if engaged constructively.
- Likely for: systems with a public bug bounty program, or systems operated by organizations with public security commitments.
- Defensive priority: run a Vulnerability Reward Program; have a clear disclosure policy; respond quickly to reports.

**Governments and law enforcement (nation-state actors)**
Intelligence agencies, military cyber units, and law enforcement with the goal of intelligence gathering, military disruption, or policing. Have significant resources and can sustain long-term operations. Typically use sophisticated methods but also rely on simple techniques (phishing) when those work.
- Likely for: organizations handling user communications, location data, financial records, or government/military supply chains.
- Defensive priority: invest in long-term defense in depth; protect the most sensitive assets even at high cost; build layered detection that catches persistent access, not just initial compromise.

**Activists (hacktivists)**
Groups or individuals using technical attacks to advance political or social causes. Methods range from website defacement and DDoS to data theft and publication. Vocal and often seek public credit. Do not always have high technical skill — DDoS-for-hire services are inexpensive.
- Likely for: organizations with politically controversial products, customers, or public positions.
- Defensive priority: DDoS mitigation; backup and rapid restore; hardened content delivery.

**Criminal actors**
Motivated by financial gain. Use the most cost-effective attack methods available, including social engineering, phishing, ransomware, and credential stuffing. Will move to easier targets if attack cost exceeds expected return. Operate alone or are hired by organizations (political campaigns, competitors, criminal enterprises).
- Likely for: any system handling money, credentials, or data with resale value.
- Defensive priority: raise attack cost; implement MFA; make your system a more expensive target than alternatives.

**Automation and AI-assisted attacks**
Emerging category: automated systems that discover and exploit vulnerabilities without direct human control. Currently most relevant for large-scale credential stuffing, vulnerability scanning, and opportunistic exploitation of known CVEs.
- Likely for: any internet-facing system; grows more relevant over time.
- Defensive priority: automated configuration management; resilient-by-default system design; continuously updated vulnerability patching.

**Output of this step:** A profile assessment table with likelihood rating (High/Medium/Low/Not applicable) for each profile and 1–2 sentences on what that attacker would target in this specific system.

---

### Step 3 — Build the Insider Threat Scenario Matrix

Apply the four-dimension actor-motive-action-target framework to insider categories to generate concrete insider threat scenarios.

**Why:** Insider threats are frequently undermodeled because security thinking defaults to external attackers. Yet insiders already have access — they skip the entry stage of an attack entirely. Insider actions span the full range from deliberate malice to accidental damage, and the defenses (least privilege, multi-party authorization, business justifications, auditing) are the same regardless of intent. Planning for both malicious and accidental insider actions is essential because intent is often impossible to determine after the fact.

**The three insider categories:**

- **First-party insiders:** Employees, interns, executives, board members — those brought in to meet business objectives and granted direct system access.
- **Third-party insiders:** Contractors, vendors, open-source contributors, commercial partners, auditors — insiders whom few or no people in the organization have met personally. Open-source contributors who submit malicious code changes are a growing subcategory.
- **Related insiders:** Friends, family, roommates — people with physical access to an insider's device or workspace. Remote and work-from-home arrangements expand this category.

**Build a scenario matrix using four dimensions:**

| Dimension | Example values |
|---|---|
| **Actor/Role** | Engineering, Operations, Legal, Marketing, Executives, Contractor, Vendor, Open-source contributor, Family member |
| **Motive** | Accidental, Negligent, Compromised (account takeover), Financial, Ideological, Retaliatory, Vanity |
| **Action** | Data access (read), Exfiltration (copy/send), Deletion, Modification, Injection (malicious code/config), Leak to press |
| **Target** | User data, Source code, Documents, Logs, Infrastructure, Services, Financial records |

Generate at least 5 concrete scenarios by combining one item from each dimension. Include both malicious and accidental scenarios. Examples:

- An **engineer** with source code access is **dissatisfied after a negative performance review** and **injects a backdoor** into production that **exfiltrates user credentials**.
- An **SRE** preparing an emergency change is **working without enough sleep** and **accidentally deletes** the production **database**.
- A **contractor** with API access is **compromised** by a third-party phishing campaign and their credentials are used to **exfiltrate** **source code**.
- An **open-source contributor** submits a malicious change list that **injects** a dependency backdoor affecting **all downstream users**.
- A **family member** uses an employee's unlocked laptop and **accidentally installs malware** that **prevents the employee from responding** to an on-call incident.

**Output of this step:** A table of 5–8 insider threat scenarios, each with Actor, Motive, Action, Target, and a brief impact statement.

---

### Step 4 — Build External Threat Scenarios

Apply the same four-dimension matrix to external attacker profiles from Step 2.

**Why:** Combining attacker profiles (who) with the actor-motive-action-target framework produces concrete, testable threat scenarios rather than abstract risk statements. Concrete scenarios map directly to defensive controls — each scenario implies specific technical and procedural mitigations. Abstract risk statements ("we might be hacked") cannot drive security investment decisions.

For each High or Medium attacker profile from Step 2, generate at least one scenario:

| Dimension | Values for external threats |
|---|---|
| **Actor** | Criminal gang, Hacktivist collective, Nation-state intelligence agency, Automated scanner, Former employee (acting externally), Hired attacker |
| **Motive** | Financial gain (ransomware, credential theft), Espionage (IP theft, data collection), Activism (defacement, disruption), Coercion (DDoS for ransom), Destruction (sabotage) |
| **Action** | Phishing to credential theft, Exploiting unpatched CVE, Supply chain compromise, Social engineering of support staff, DDoS, Injecting malicious dependency |
| **Target** | User accounts, Admin credentials, Payment data, Source code, Cryptographic keys, API endpoints, Third-party integrations |

**Output of this step:** A table of 5–8 external threat scenarios covering the relevant attacker profiles.

---

### Step 5 — Map Scenarios to Attack Lifecycle Stages and Assign Defenses

Plot prioritized threat scenarios against the five attack lifecycle stages and identify the defensive controls that interrupt each stage.

**Why:** Attackers must succeed at every stage in sequence to achieve their goal — defenders only need to interrupt one stage. Mapping scenarios to lifecycle stages identifies where in the attack chain a defense can be applied most cost-effectively. A multi-stage attack also provides multiple detection opportunities; building detection into each stage maximizes the chance of catching an attacker before they reach their goal.

**The five attack lifecycle stages:**

| Stage | What the attacker does | Example attack action |
|---|---|---|
| **Reconnaissance** | Surveys target to understand weak points | Search for employee email addresses, enumerate public APIs, read job postings to infer tech stack |
| **Entry** | Gains initial access to systems, accounts, or the network | Sends phishing emails leading to credential compromise; exploits a known CVE in a public endpoint |
| **Lateral movement** | Moves from initial access point to higher-value systems | Logs into internal systems using stolen credentials; pivots from compromised workstation to production servers |
| **Persistence** | Ensures ongoing access survives detection and remediation | Installs a backdoor; creates a secondary admin account; modifies startup scripts |
| **Goal execution** | Takes the action that achieves the attack objective | Exfiltrates data; encrypts files for ransom; deletes production systems; publishes stolen documents |

For each high-priority scenario from Steps 3 and 4, identify which stage is the natural intervention point and what defense interrupts it:

**Reconnaissance defenses:** Employee security awareness training; minimize public information exposure (job postings, error messages that reveal tech stack); monitor for public OSINT gathering.

**Entry defenses:** Multi-factor authentication (hardware security keys for high-privilege accounts); restrict VPN access to organization-managed devices; patch known vulnerabilities promptly; phishing-resistant authentication.

**Lateral movement defenses:** Enforce least privilege — employees can only access systems required for their role; require re-authentication for sensitive system access; segment the network; implement zero-trust network access (no implicit trust based on network location alone).

**Persistence defenses:** Application allowlisting (only permit authorized software to run); monitor for unexpected new accounts or scheduled tasks; automated integrity checking of critical system files.

**Goal execution defenses:** Least-privilege access to sensitive data; data loss prevention controls; monitoring for large data transfers or bulk deletions; enable rapid recovery (tested backups, runbooks for data restoration).

**Output of this step:** A table mapping each prioritized threat scenario to the stage where intervention is most effective and the specific defensive control recommended.

---

### Step 6 — Produce the Threat Model Document

Compile the outputs of Steps 1–5 into a structured threat model document.

**Why:** A threat model is only useful if it is documented, shareable, and actionable. The document becomes the shared reference for security investment decisions, architecture reviews, penetration test scoping, and compliance evidence. Without a written artifact, the modeling exercise has no lasting impact.

**Threat model document structure:**

```
1. System Summary
   - System name and purpose
   - Key assets (data, services, infrastructure)
   - Exposure surface (internet-facing endpoints, privileged user count)

2. Attacker Motivation Assessment
   - Table: motivation × High/Medium/Not Applicable × justification

3. Attacker Profile Assessment
   - Table: profile × likelihood × what they would target in this system

4. Insider Threat Scenarios
   - Matrix table: Actor | Motive | Action | Target | Impact

5. External Threat Scenarios
   - Matrix table: Actor | Motive | Action | Target | Impact

6. Prioritized Threat Scenario List
   - Ranked by: (likelihood × impact)
   - Top 5–10 scenarios with priority ranking

7. Attack Lifecycle Defensive Map
   - Table: Scenario | Stage | Recommended Defense

8. Open Questions and Assumptions
   - What information would change this model?
   - What is assumed but not verified?
```

**Output of this step:** A completed threat model document written to the project directory or presented to the user as a structured response.

---

## Key Principles

**1. Assume you are a target before you know why.**
Organizations routinely do not realize they are attractive targets until after a breach. A small company may hold data that a nation-state wants, or may be a stepping stone to a higher-value target in the supply chain. Assess attractiveness from the adversary's perspective, not the organization's self-assessment.

**2. Attack sophistication does not predict success.**
Even well-resourced attackers choose the simplest available path to their goal. Phishing remains one of the most effective entry techniques regardless of the attacker's technical sophistication. Prioritize defenses against simple, proven attack methods (MFA, patching, access controls) before investing in defenses against exotic scenarios.

**3. Plan for both malicious and accidental insider actions.**
Insider intent is often impossible to determine after the fact. An accidental database deletion and a retaliatory one have the same impact. Design defenses (least privilege, multi-party authorization, auditing) that protect against both simultaneously.

**4. Focus on attacker methods when attribution is uncertain.**
Attackers can disguise their identity and motivation (NotPetya appeared to be ransomware but was sabotage). Do not build defenses that depend on knowing who the attacker is. Instead, map defenses to the attacker's *methods* (tactics, techniques, and procedures) — these are harder to disguise and more stable across attribution changes.

**5. Raising attack cost is a legitimate and measurable defense.**
Criminal actors choose the easiest target. If you make your system significantly more expensive to attack than alternatives, they shift to easier targets. Nation-state actors cannot be deterred by cost, but forcing them to spend significant resources increases their risk of detection and attribution. "Make the attack more expensive than the reward" is a concrete design goal.

---

## Examples

### Example 1 — Payment processing API

**User request:** "We're building a payment processing API. We need to understand who might attack it and what we should prioritize."

**Step 1 — Motivation assessment (abbreviated):**
- Financial gain: **High** — payment data and transaction manipulation are direct paths to money.
- Coercion: **High** — ransomware or DDoS against a payment processor causes immediate revenue loss; operators are likely to pay to restore service.
- Espionage: **Medium** — customer payment data has resale value; transaction patterns could be valuable to competitors.
- Destruction: **Low** — no obvious political or military motive unless the client base includes sanctioned entities.

**Step 2 — Profile assessment (abbreviated):**
- Criminal actors: **High** — direct financial return from credential theft, card data, or ransomware.
- Nation-state: **Medium** — if processing cross-border transactions or serving government clients; intelligence agencies value financial data.
- Hobbyists/automated: **High** — any public API endpoint will face automated scanning.

**Step 3 — Key insider scenarios:**
- A **payment operations engineer** is **compromised** via phishing and their admin credentials are used to **exfiltrate** bulk **card data**.
- An **executive** with access to financial reporting **accidentally leaks** quarterly **revenue data** before public disclosure.
- A **contractor** building the reconciliation module **injects fraudulent transaction records** to redirect small amounts to an external account over months.

**Step 4 — Key external scenarios:**
- A **criminal gang** motivated by **financial gain** uses **credential stuffing** against merchant API keys to **initiate fraudulent transactions**.
- An **automated scanner** exploits a **known CVE** in an unpatched dependency to gain **initial access** to the payment gateway.

**Step 5 — Top defensive priorities:**
- Entry: Hardware MFA for all admin accounts; phishing-resistant authentication for operations staff.
- Lateral movement: Least privilege — payment engineers cannot access bulk card data outside of specific, logged operations.
- Goal execution: Data loss prevention on bulk card data exports; anomaly detection on transaction velocity.
- Insider: Multi-party authorization for any operation affecting more than N transactions; business justification logging for bulk data access.

---

### Example 2 — Internal developer platform

**User request:** "We run an internal platform where engineers submit code that gets deployed to production. What threats should we be designing for?"

**Step 1 — Motivation assessment (abbreviated):**
- Espionage: **High** — source code is proprietary IP; the deployment pipeline is a high-value target for supply chain attacks.
- Destruction: **Medium** — a disgruntled insider or external attacker could disrupt production deployments.
- Financial gain: **Medium** — source code may be sold; credentials to the deployment system could be used for ransomware.

**Step 2 — Profile assessment (abbreviated):**
- Nation-state: **High** (if company has proprietary technology) — source code is prime espionage target.
- Criminal actors: **Medium** — ransomware via supply chain compromise is increasing.
- Hobbyists/researchers: **Low** — internal-only system with no public exposure.
- Insider threat: **High** — all engineers are first-party insiders with significant access.

**Step 3 — Key insider scenarios:**
- An **engineer** with a **retaliatory** motive (fired for cause) uses retained credentials to **delete** production **infrastructure** before access is revoked.
- A **third-party open-source contributor** **injects a malicious dependency** into a shared library that **exfiltrates environment variables** from production containers.
- An **SRE** working a late-night incident is **negligent** and **accidentally modifies** the wrong **production configuration**, causing an outage.

**Step 4 — Key external scenarios:**
- A **nation-state actor** uses **spear-phishing** against a senior engineer to steal their credentials and gain **persistent access** to the source code repository.
- A **criminal actor** compromises a **third-party dependency** in the build pipeline (supply chain attack) to inject malware into production artifacts.

**Step 5 — Top defensive priorities:**
- Entry: Hardware MFA for all engineers; device health checks before VPN access.
- Lateral movement: Zero-trust network access — production access requires per-session authorization, not standing access.
- Persistence: Code review requirements for all changes; dependency pinning and integrity verification; automated build provenance.
- Insider/retaliatory: Access revocation runbook with sub-hour SLA for departing employees; audit logs for all production access.

---

### Example 3 — Consumer fitness tracking app

**User request:** "We run a fitness app with GPS route tracking. We're small and not a bank or defense contractor — do we really need to threat model?"

**Step 1 — Motivation assessment:**
This illustrates the "you may not realize you're a target" principle. The fitness app collected GPS routes from users who happened to be active-duty military personnel. In 2018, a public heatmap of user activity routes revealed locations of undisclosed military bases. A fitness app with location data may attract intelligence agency interest it would never anticipate.

- Espionage: **Medium** (unexpected) — aggregated location data has intelligence value.
- Financial gain: **High** — user accounts with PII and payment data are resale targets.
- Coercion: **Low** — service disruption is inconvenient but not mission-critical for most users.

**Key insight for the user:** Even organizations that do not consider themselves high-value targets may hold data that is attractive to nation-state actors, criminal gangs, or others. The fitness app scenario demonstrates that the adversary's view of your data's value differs from your own view. Run the motivation assessment from the adversary's perspective, not yours.

---

## References

See `references/` for:
- `attacker-motivation-worksheet.md` — Guided worksheet for systematically rating each motivation against a system's profile
- `attacker-profile-reference.md` — Detailed capability, resource, and behavioral descriptions for each profile
- `insider-category-taxonomy.md` — Extended insider category taxonomy with worked examples of related-insider scenarios
- `threat-scenario-matrix-template.md` — Blank actor-motive-action-target matrix for generating scenarios
- `attack-lifecycle-defense-map.md` — Comprehensive per-stage defense catalog drawn from the book's chapters on access controls, logging, and incident response

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
