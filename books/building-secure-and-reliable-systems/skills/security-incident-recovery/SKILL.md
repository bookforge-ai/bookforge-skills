---
name: security-incident-recovery
description: Use when you need to recover from a security incident, build an incident recovery plan, execute post-breach remediation, rotate credentials after a breach, scope attacker impact across systems, build a recovery checklist, decide when to eject an attacker vs. continue observing, or run a post-incident postmortem with short-term and long-term action items.
tags: [security, incident-recovery, post-incident, credential-rotation, postmortem]
depends_on: [security-incident-command]
---

# Security Incident Recovery

Guides post-incident recovery from security breaches using a 4-phase process: appoint a Remediation Lead in parallel with investigation, scope the full blast radius, build a structured recovery checklist, and execute remediation — including isolation, clean rebuilds, credential rotation, and postmortem. Incorporates a decision framework for eject-vs-mitigate-vs-rebuild choices, four key adversarial-thinking questions, and technical debt tracking for short-term bypasses. Covers three worked scenarios ranging from opportunistic cloud compromise to targeted APT with financial backdoor. Output: recovery checklist, credential rotation plan, and postmortem with prioritized action items.

**Prerequisite:** The Incident Management at Google (IMAG) process must be running with an Incident Commander (IC) and an Operations Lead (OL) already staffed (`security-incident-command`). This skill picks up from the point at which enough is known about the attack to begin parallel recovery planning.

## When to Use

- Executing recovery after a confirmed security breach, intrusion, or account compromise
- Scoping which systems, accounts, and data are affected and need remediation
- Building the recovery checklist before executing cleanup
- Deciding whether to eject the attacker now or continue observing their activity
- Rotating credentials, secrets, and cryptographic keys following a breach
- Conducting a postmortem that distinguishes overnight tactical fixes from strategic long-term changes
- Recovering from attacks where the attacker may still be present and watching the response

## Process

### Phase 1 — Appoint a Remediation Lead (parallel track)

As soon as the incident is confirmed and investigation begins, the IC and Operations Lead should appoint a **Remediation Lead (RL)**. Do not wait until investigation is complete.

**Why parallel tracks:** Investigation is time-consuming and detail-heavy; recovery planning requires a different skill set (system knowledge, operations expertise) than forensic investigation. Separate teams feed information to each other bidirectionally rather than handing off sequentially — this prevents the investigation team from being exhausted by the time recovery begins, and it allows recovery planning to stay current with newly discovered attacker activity.

**Who the RL assembles:** The people who build and run the affected systems every day — SREs, developers, system administrators, helpdesk staff, and the security specialists who manage routine processes like code audits and configuration reviews. Recovery engineers do not need to be security professionals; they need deep system knowledge.

**Information management during recovery:**

Store all recovery documentation — raw incident trails, scratch notes, recovery checklists, new operational documentation — in systems inaccessible to the attacker. Use air-gapped computers or services clearly outside the attacker's potential scope. Start with notecards and add an independent service provider once you are confident no recovery team member machines are compromised.

If the attacker has access to your email or instant messaging system, they can read your recovery plans in real time, observe your mitigations, and take pre-emptive action. In a large-scale phishing scenario where employee accounts are compromised, set up a completely new communication system — for example, inexpensive Chromebooks on a fresh network — before coordinating recovery steps.

Assign dedicated note-takers or documentation specialists. An audit trail of what happened during recovery helps fix mistakes and satisfies postmortem requirements.

### Phase 2 — Scope the Recovery

Before building the recovery checklist, establish the complete picture of what is affected and what the attacker can do.

**Required inputs from the investigation team:**

1. **Complete affected system list:** Every system, network, and dataset directly or indirectly impacted. If a configuration distribution system is compromised, every system that received configurations from it is in scope. Track indirect impact chains.

2. **Attacker tactics, techniques, and procedures (TTPs):** Understanding how the attacker operates lets you identify related resources that may be impacted and anticipate their next moves. Build a list of attacker behaviors and possible defenses — this becomes operational documentation for why specific new defenses are introduced.

3. **Variant analysis:** Identify whether other systems are susceptible to variations of the same attack. If a buffer overflow was exploited on one web server and 20 others run the same flawed software, all 20 are in scope even if not yet compromised. Check for related vulnerability classes in the same infrastructure or the same vulnerability in different software using the same shared libraries.

**The four key recovery questions — ask these before proceeding:**

**1. How will your attacker respond to the recovery effort?**
There is a human on the other side of the attack who is reacting to your incident response. Your recovery plan must include severing all attacker connections to your resources and ensuring they cannot return. A mistake here leads the attacker to take additional actions you may not have anticipated or have visibility into. An attacker who is still active when you take six systems offline can see your actions and may destroy the remaining infrastructure.

**2. What does complete remediation require?**
Understand the full scope of what the attacker has done — not just what is known. Plan for the possibility that the attacker is still present and watching your actions. Inform the investigation team of your recovery plans; they must be confident your plans will stop the attack before you execute.

**3. What variants of the attack exist?**
Address the known compromised system, but also consider whether variants of the vulnerability exist elsewhere in the infrastructure and how you will mitigate those for the future.

**4. Will your recovery reintroduce attack vectors?**
Recovery methods that restore systems to a known good state using system images, source code, or configurations may reintroduce the vulnerability that enabled the attack. Update golden images and delete compromised snapshots before systems come back online. Determine the attack timeline — when did the attacker make modifications, and how far back must you revert to reach a genuinely uncompromised state?

**On the timing of ejection — the consensus principle:**

Security incident responders generally agree that you should wait until you have a full understanding of the attack before ejecting the attacker. This prevents the attacker from observing your mitigations and helps you respond defensively.

Apply this carefully: if your attacker is actively doing something dangerous — exfiltrating sensitive data, destroying systems, stealing money — you may choose to act before you have a complete picture. Ejecting early while the attacker still has unknown footholds means entering a chess game. Prepare accordingly: know the steps you must take to reach checkmate before you make your opening move.

### Phase 3 — Build the Recovery Checklist

The recovery checklist is the single authoritative document for executing remediation. Build it before you start any cleanup work.

**Why a written checklist is mandatory:** Recovery from a complex incident is a choreographed operation with many individuals whose actions affect each other. A well-documented checklist lets the recovery team identify parallelizable work, coordinate across teams, and give the IC confidence that all completed steps have actually been verified. It also provides an audit trail.

**Checklist structure (Figure 18-1 template):**

```
INSTRUCTIONS:
- Highlight GREEN when COMPLETED
- Highlight ORANGE for TO-DO items
- Highlight RED if task cannot be completed (must be replaced with equivalent action)
- Highlight BLUE if task will not be completed because it is operationally risky (adjustments needed)

Incident Commander:
- Give "hands off keyboards" briefing
- Provide overview of tasks and constraints
- Notify everyone of the exact time remediation begins

In order of operations, the Remediation Lead initiates:
  1. [Team name]: Description of task
     a. Detailed commands or steps
  2. [Team name]: Description of task
     a. Detailed commands or steps
  ...
```

**What each checklist item must include:** the specific team responsible, detailed commands or exact steps (not just descriptions), the order of execution, rollback procedures if the plan fails, and any cleanup steps that follow remediation. Thorough documentation means every team member has unambiguous, agreed-upon guidance without needing to interpret intent under pressure.

**Parallelization:** Structure the checklist to identify which tasks can run concurrently. For complex incidents with multiple affected systems, create separate checklists per workstream (email team, source code team, SSL keys team, customer data team) that a single RL coordinates.

**Technical debt tracking for short-term mitigations:**

Some recovery steps will bypass normal procedures to eject the attacker quickly — for example, manually adding firewall deny rules outside your version control system, or disabling automatic configuration pushes. Accept this technical debt deliberately, but set explicit remediation reminders.

For each bypass, ask:
- How quickly can we replace this short-term mitigation?
- Is the team that owns this technical debt committed to paying it off through later improvements?
- Will this mitigation affect system uptime or exceed error budgets?
- How can future engineers recognize this as temporary (comments in code, descriptive commit messages, tagging)?
- How can a future engineer with no domain expertise prove the mitigation is no longer needed and remove it safely?
- What happens if this short-term mitigation is left in place for months instead of weeks?

Tag technical debt visibly so it cannot be forgotten.

### Phase 4 — Execute the Recovery

#### Isolation and Quarantine

Isolate compromised assets before or during remediation to prevent the attacker from using remaining access to undermine recovery.

**Quarantine methods:**
- Disable switch ports or networking at the host level to isolate individual machines
- Use network segmentation to isolate entire networks of compromised machines
- Move malicious binaries to quarantine folders with restricted permissions (antivirus-style quarantine)
- For mission-critical systems that cannot be taken fully offline: isolate on a separate network with restricted traffic rules limiting what it can send and receive

**BeyondCorp / zero-trust architecture advantage:** Zero-trust environments that validate asset security posture before granting access to corporate services — like Google's BeyondCorp architecture — provide a natural isolation boundary during recovery. Because access is controlled via proxy infrastructure with strong credentials that can be revoked at any time, isolating a compromised asset does not require network-level reconfiguration. Lateral movement (attacker moving between machines on the same network) is also suppressed by default because there is little implicit trust between assets.

**Leaving compromised assets online is technical debt.** If a mission-critical database cannot be rebuilt immediately, isolate it and mark it clearly — use highly visible physical stickers on devices, maintain a list of MAC addresses of quarantined systems and monitor for those addresses on the network. Include explicit remediation of all quarantined assets in the recovery checklist and postmortem. Someone new to the organization or the incident must not accidentally unquarantine a compromised resource.

#### Clean Rebuilds from Known-Good Sources

For systems where the attacker may have installed malware, modified software, or tampered with configurations, reinstalling from scratch with known-good images is typically the best solution. Deleting malware in place risks missing additional malware types the attacker installed.

**Eject vs. mitigate vs. rebuild decision:**
- If the affected systems are mission-critical and difficult to rebuild: deleting malware and patching is tempting but risky if the attacker installed multiple malware types
- If you have reliable and secure design principles in place (hardware-backed boot verification, cryptographic chain of trust, automated release systems): rebuilding is straightforward — it is simply a power cycle or container replacement
- In cloud environments: replace compromised instances with clean images from known-good sources

**Checksum verification:** Obtain known-good copies of source code, binaries, images, and configurations from original sources (open source providers, commercial software vendors, uncompromised version control systems). Perform checksum comparisons against known good states. If your good copies are hosted on compromised infrastructure, determine exactly when the attacker began tampering before using them.

**Attack timeline analysis for golden images:** Review your golden images. Delete compromised snapshots. Update images before systems come back online. If restoring from backups, determine whether the backup predates the attacker's first modification — logs may identify an inflection point where the attack began, giving you an independent lower bound for which backups are safe.

**Mark compromised code explicitly:** During the rebuild, clearly mark known compromised code, libraries, and binaries. Create tests that prevent inadvertent reuse of compromised code by recovery team members working in parallel.

#### Credential and Secret Rotation

Credential rotation is one of the most critical and most frequently incomplete recovery actions.

**What to rotate — comprehensive scope:**
- User account passwords (all accounts with access to affected systems; if attacker had wide access or access is unclear, rotate all users)
- Service and application account credentials
- SSH keys (including the `authorized_keys` file)
- Network device credentials
- Out-of-band management system credentials
- SSL/TLS keys (if frontend web infrastructure was accessible to the attacker — failure to rotate enables man-in-the-middle attacks)
- Encryption keys for data at rest (rotate keys and re-encrypt if the key lived on a compromised server)
- API keys for cloud services (attackers who accessed source code or local config files may have found these; rotate conservatively and often even where you cannot prove access occurred)
- SaaS application credentials

**Execution order matters:** Prioritize administrator credentials, then known compromised accounts, then accounts that grant access to sensitive resources. In large organizations where thousands of users must change passwords simultaneously, single sign-on (SSO) services can simplify coordinated resets — but introducing SSO during an incident is time-consuming and may not be viable short-term.

**Pass-the-hash risk:** Attackers can obtain and replay hashed credentials (NTLM or LanMan hashes) without needing cleartext passwords. If your environment is vulnerable, include credential hash rotation and review of authentication protocols in the checklist.

**Pattern-based password prediction:** If your environment stores password history (LDAP, Active Directory), an attacker with access to hashed passwords can infer patterns (password2019, password2020...) and predict the next password in a sequence. Consult security specialists about whether forced password resets are sufficient or whether two-factor authentication must be enabled simultaneously to prevent the attacker from leveraging their historical knowledge.

**Two-factor authentication as a quick win:** Adding two-factor authentication — especially for less-protected entry points like email — is a fast short-term mitigation. It also provides a detection benefit: if an attacker attempts to log in with stolen credentials after rotation, the attempt appears as an account login failure, alerting the investigation team to continued attacker activity.

### Phase 5 — After the Recovery: Postmortem

Begin post-recovery actions as soon as recovery is complete. Waiting lets incident details fade and postpones necessary medium- and long-term fixes.

**Postmortem structure:**

Every postmortem must contain a list of action items that address the underlying problems found during the incident. A strong postmortem:
- Covers the technology issues the attacker exploited
- Recognizes opportunities for improved incident handling
- Documents the time frames and efforts associated with each action item
- Explicitly separates short-term tactical mitigations from long-term strategic changes

**Short-term overnight items** (low-hanging fruit — quick to implement, small in scope):
- Patch known vulnerabilities exploited in the attack
- Add two-factor authentication to entry points that lacked it
- Set up a vulnerability discovery program
- Enable two-factor authentication for additional services
- Lower the time to apply patches

**Long-term strategic items** (fundamental changes to how systems and processes work):
- Deploy backbone encryption
- Start a dedicated security team
- Implement BeyondCorp / zero-trust network architecture
- Alter operating system choices to enable hardware-verified boot
- Establish ongoing vulnerability management programs
- Pursue widespread FIDO-based security key adoption for authentication

**Security-focused postmortem questions:**
- What were the main contributing factors? Are there variants and similar issues elsewhere?
- What testing or auditing processes should have detected these factors earlier?
- Was this incident detected by an expected technology control (e.g., intrusion detection system)? If not, how do you improve detection?
- How quickly was the incident detected and responded to? Is this within an acceptable range?
- Was important data sufficiently protected to deter attacker access? What new controls should be introduced?
- Was the recovery team able to use versioning, deployment, testing, backup, and restoration tools effectively?
- What normal procedures (testing, deployment, release) did the team bypass during recovery? What remediation must happen now?
- Were any infrastructure changes made as temporary mitigations that now need refactoring?
- What bugs were filed during the incident and recovery that still need to be addressed?

**Action item format:** Lay out action items with explicit owners, sorted by short-term vs. long-term. The period of routine steady state after an incident is simultaneously the window before the next incident — use it to identify new threats and prepare.

## Worked Examples

### Example A: Compromised Cloud Instances (Opportunistic)

**Scenario:** A web-based software package running on cloud VMs has a common vulnerability. An opportunistic attacker discovers it with scanning tools and takes over the VMs, using them to launch new attacks.

**Recovery approach:**
The RL uses investigation notes to build a checklist with four ordered workstreams:

1. **Security specialists:** Set up vulnerability scanning — includes scanning other software on the cloud instances to identify additional necessary fixes
2. **Web developer team:** Patch vulnerable software — includes specific source location, which versions to deploy, and deployment steps
3. **SRE team:** Deploy new clean cloud instances in parallel with compromised ones — test and validate before routing traffic
4. **SRE team:** Disable compromised cloud instances — includes specific shutdown steps and archive or deletion to prevent reuse

**Postmortem outcome:** Identifies need for a formal vulnerability management program to proactively discover and patch known issues before attackers find them.

### Example B: Large-Scale Phishing Attack (70% Employee Compromise)

**Scenario:** Over seven days, an attacker launches a password phishing campaign against an organization without two-factor authentication. 70% of employees fall for it. The attacker reads email and leaks sensitive information to the press. The attacker has stated they will take more action in the coming days.

**Complexities:** The investigation team determines the attacker has not yet tried to access systems other than email — but many employees share passwords between email and VPN/cloud services, meaning the attacker could pivot. Ejecting from email quickly is urgent, but uncoordinated password resets that tip off the attacker before all entry points are locked could trigger immediate escalation.

**Recovery checklist — four ordered workstreams:**

1. **System administrators / SREs:** Implement two-factor authentication infrastructure for email (specific enrollment steps for all employees)
2. **Email SREs:** Lock all email accounts (specific steps to lock until reset and 2FA enrollment — consider locking all accounts simultaneously rather than a rolling window, since the attacker is active)
3. **IT staff (Helpdesk):** Enact two-factor authentication and password resets (help users change email, VPN, and cloud-based passwords; may involve an all-hands meeting)
4. **System administrators / SREs:** Adopt two-factor authentication for VPN and cloud systems

**Postmortem outcome:** Two-factor authentication for all critical communication and infrastructure systems; SSO solution; employee phishing awareness education; engage an IT security specialist for ongoing best-practice guidance.

### Example C: Targeted APT — Financial Backdoor, SSL Theft, Executive Monitoring

**Scenario:** An attacker has had undetected access for over a month. They inserted a backdoor into source code siphoning $0.02 from every transaction, stole SSL keys protecting customer web communications, and monitored executive email. The investigation team does not know how the attack began or how the attacker maintains access. The attacker can modify and deploy source code to production, access SSL key infrastructure, and read executive email including incident response coordination.

**Complexities:** This attack requires full parallelization across five independent recovery workstreams:

- **Email team:** Sever attacker's email access — reset passwords, introduce two-factor authentication (the attacker is actively reading your recovery plans)
- **Source code team:** Determine when the attacker modified source code, identify all affected binaries deployed, sanitize affected source files, redeploy clean code. Confirm the attacker has not modified version control history and cannot make additional changes.
- **SSL keys team:** Deploy new SSL keys to web serving infrastructure. Determine how the attacker gained access to key storage and prevent future unauthorized access.
- **Customer data team:** Determine what customer information the attacker accessed. Perform customer password changes or session resets as needed. Coordinate with customer support, legal, and related staff.
- **Reconciliation team:** Address the $0.02-per-transaction siphoning. Determine whether database records must be amended for long-term financial recording. Coordinate with finance and legal.

**Key lesson:** Complex incidents require less-than-ideal choices. Severing email access may mean turning off the email system entirely, locking all accounts, or bringing up a parallel email system — each option alerts the attacker, impacts the organization differently, and may not address the initial access vector. The recovery and investigation teams must work together closely to find a path that fits the situation.

## Key Principles

**Parallelization is essential, not optional.** Recovery and investigation must run as separate parallel tracks from the start. Investigation fatigue makes sequential handoff unreliable, and delayed recovery planning allows attacker footholds to persist.

**The attacker is watching.** Your recovery plan must account for the possibility that the attacker can see your actions — through compromised communication systems, compromised investigation machines, or retained system access. Use out-of-band, attacker-inaccessible communication channels for all recovery coordination.

**Ejection timing requires consensus.** Wait for full understanding before ejecting — but act early if the attacker is doing active damage. These two principles are in tension; resolve the tension by ensuring the investigation team concurs that your recovery plan will actually stop the attack before you execute it.

**Technical debt must be tracked explicitly.** Short-term bypasses are sometimes necessary. Accept them deliberately, tag them visibly, and set explicit remediation reminders — or they become permanent vulnerabilities.

**Zero-trust architecture simplifies recovery.** Environments that validate asset posture before granting access (BeyondCorp pattern) provide natural quarantine boundaries and suppressed lateral movement, reducing the blast radius of a compromise and simplifying isolation during recovery.

**Credential rotation scope is always larger than it looks.** Include SSL keys, API keys, service accounts, and infrastructure credentials — not just user passwords. A missed credential is a door left unlocked.

**Postmortem action items must be separated by time horizon.** Overnight tactical fixes and multi-year strategic changes belong in the same postmortem but must be clearly delineated with explicit owners, or the strategic work never gets done.

## References

- *Building Secure and Reliable Systems* (Blank, Oprea et al., Google/O'Reilly, 2020)
  - Chapter 18 "Recovery and Aftermath" (pp. 417–442)
    - "Recovery Logistics" (pp. 418–420): parallel tracks, Remediation Lead appointment, information management, air-gapped documentation
    - "Recovery Timeline" (pp. 420–421): when to start recovery planning, not before some plan exists
    - "Planning the Recovery / Scoping the Recovery" (pp. 421–422): complete affected system list, TTP analysis, postmortem doc
    - "Recovery Considerations" (pp. 423–427): four key questions, ejection timing consensus, infrastructure compromise, variant analysis, attack vector reintroduction, mitigation options and technical debt framework
    - "Recovery Checklists" (pp. 428–429): Figure 18-1 template structure
    - "Initiating the Recovery" (pp. 429–435): isolation/quarantine, BeyondCorp sidebar, system rebuilds, data sanitization, credential and secret rotation, SSO consideration
    - "After the Recovery / Postmortem" (pp. 435–437): short-term vs. long-term action items, security-focused postmortem questions
    - "Examples" (pp. 437–442): compromised cloud instances (Figure 18-2), large-scale phishing (Figure 18-3), targeted APT with parallel workstreams
  - Depends on: `security-incident-command` (IMAG process running, IC/OL/RL roles staffed)
  - Related: `recovery-mechanism-design` (design-time recovery architecture), `incident-response-team-setup` (IR team structure and postmortem process)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure And Reliable Systems by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
