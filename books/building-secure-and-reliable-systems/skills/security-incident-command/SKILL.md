---
name: security-incident-command
description: |
  Command and manage an active security incident from declaration through remediation handoff using the incident management framework (Google's IMAG, derived from ICS). Use when: you have a confirmed or suspected security incident and need to take command; someone says "we have a security incident" or "we may have been compromised"; you need to stand up an incident command structure with staffing roles; you are running forensic investigation and need to coordinate parallel tracks; an incident has grown large enough to require shift rotation and formal handovers; or you need to decide when investigation is complete enough to move to ejection and remediation. Distinct from incident response team setup (which designs the team and IR capability before incidents) — this skill executes the live response. Applies the seven-step incident command process: declare, staff, establish operational security, run forensic investigation loop, scale with rotation, apply the lead-rate decline signal to decide ejection timing, and hand off with a structured brief. Produces: incident state document, forensic timeline, communication plan, and remediation handoff package.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/security-incident-command
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - incident-response-team-setup
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [17]
tags:
  - security
  - incident-response
  - crisis-management
  - incident-command
  - forensics
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: context
      description: "Alert, detection signal, or report that triggered escalation — describes what was observed, when, and on which systems"
    - type: context
      description: "Organization's IR team charter and severity/priority model from incident-response-team-setup"
  tools-required: [Read, Write]
  tools-optional: [Bash, Grep]
  mcps-required: []
  environment: "Runs during a live incident. IC executes Steps 1–3 immediately; Steps 4–7 are iterative throughout incident lifecycle."
discovery:
  goal: "Manage a security incident from initial detection through remediation handoff: declare, staff, secure the investigation environment, complete the forensic investigation loop, scale the response sustainably, apply the lead-rate decline signal to decide ejection, and execute a structured handover"
  tasks:
    - "Issue a formal incident declaration using the exact IMAG formula"
    - "Staff the four core roles: IC, OL, CL, RL"
    - "Establish operational security: new channels, clean machines, domain obfuscation"
    - "Run forensic investigation loop across forensics, reversing, and hunting sub-tracks"
    - "Monitor lead-rate decline signal to determine when investigation is complete enough to eject"
    - "Implement shift rotation and formal handover briefs to sustain multi-day response"
    - "Produce remediation handoff: incident state document, forensic timeline, communication plan"
  audience:
    - "Incident commander (IC) running an active security incident"
    - "Security engineers and operations leads on IR teams"
    - "Engineering managers who may be pulled into IC role during a crisis"
---

# Security Incident Command

Guides managing a security incident from declaration through remediation handoff using the incident management framework (Google's IMAG, derived from ICS). The seven-step process transforms a chaotic escalation into a controlled, parallelized investigation with clear role assignments, operational security discipline, and a principled stopping rule.

**Prerequisite:** Assumes your team has completed `incident-response-team-setup` — specifically that IC/OL/CL/RL roles are defined, severity and priority models exist, and a communications plan is in place.

## When to Use

- A detection alert, customer report, or engineer escalation suggests a targeted compromise or active attacker
- Someone in the organization says "we have a security incident" or "we think we've been breached"
- An escalation has passed triage and requires organized, multi-person incident management
- A running incident needs handover to a fresh team due to fatigue
- You are the first responder and need to decide whether to declare and take command
- A critical vulnerability (e.g., Shellshock-class severity) requires incident-level coordination even without confirmed exploitation

**Scope boundary:** This skill governs the command and investigation phases. Remediation execution and postmortem writing are downstream; the RL begins drafting the cleanup plan in parallel during investigation, and the postmortem begins once the incident closes.

## Process

### Step 1 — Don't panic. Triage first.

Before declaring, take five minutes. Breathe. Resist the instinct to immediately lock accounts or take systems offline — those actions alert an attacker who may still be present, destroying your visibility.

**Why this matters:** Unlike a reliability incident (where the system won't resist being fixed), in a security compromise the attacker may be paying close attention to your actions. Premature response actions can cause an attacker to go quiet, eliminating your visibility into the full scope of their foothold, or trigger destructive exit behavior. Postmortems rarely show that responding five minutes sooner made the difference — additional planning up front adds more value than immediate action.

**Triage assessment:** Estimate the potential severity by asking:
- What data is accessible from the potentially compromised system, and what is its criticality?
- What trust relationships does this system have with other systems (lateral movement risk)?
- Are there compensating controls the attacker would also need to defeat to extend their reach?
- Does this appear to be opportunistic commodity malware, or a targeted attack crafted for your organization?

**Ransomware triage example — same threat, three very different responses:**

| Organization | Security posture | Response required |
|---|---|---|
| Org 1 | Cryptographically signed software allowlist, mature detection | Alert fires; single engineer handles it via standard process. No crisis response needed. |
| Org 2 | Automated wipe-and-replace of compromised cloud demo instances | Automated mitigation contains the risk. Minimal human response needed. |
| Org 3 | Fewer layered defenses, limited visibility | Ransomware can spread network-wide. Significant forensic and coordination effort required. Crisis response is warranted. |

Same ransomware attack, three different required response levels. Your layered defenses and process maturity determine whether this is a crisis that needs incident command or a playbook-driven standard process.

If the escalation is a complex and potentially damaging problem — targeted compromise, active attacker, or a critical vulnerability with imminent exploitation risk — proceed to Step 2.

### Step 2 — Declare the incident and take command

The first step in IMAG is taking *command*. Issue a formal declaration using this exact formula:

> **"Our team is declaring an incident involving X, and I am the incident commander."**

Replace X with a concise description of the known or suspected issue. This declaration may seem unnecessary, but it is essential: it aligns everyone's expectations, signals that normal processes can be bypassed, and notifies executives that teams may need to reprioritize. Incidents are complex, high-tension situations that happen fast — being explicit about who is in command removes all ambiguity.

**The IC explicitly accepts the assignment.** The person designated as IC must verbally confirm they are taking command. This eliminates the dangerous ambiguity of an assumed command structure under pressure.

**Why declaring matters before you know everything:** You do not need certainty to declare. Use a worst-case assumption at triage time. If the security team's suspicions are correct and an engineer's account is compromised, you should declare immediately even if the full scope is unknown. Declaration is the mechanism that assembles the people and removes the organizational friction needed to investigate.

### Step 3 — Staff the four core roles

Under IMAG, four roles must be explicitly assigned. One person can hold multiple roles on small teams, but every role must be assigned — never assumed.

| Role | Responsibility |
|------|---------------|
| **Incident Commander (IC)** | Strategic direction. Keeps the response on track. Does NOT perform hands-on technical work — if you find yourself checking logs, step back. |
| **Operations Lead (OL)** | Tactical counterpart to the IC. Directs technical investigation. All forensics and engineering staff report to the OL. |
| **Communications Lead (CL)** | Owns all internal and external communications. Prepares briefs for executives, legal, regulators, customers. Keeps responders from making conflicting public statements. |
| **Remediation Lead (RL)** | Begins studying confirmed compromise areas as the forensics team discovers them. Builds the cleanup plan in parallel so it is ready when ejection is decided. |

**Additional leads depending on incident scope:**
- **Management liaison:** Authorizes high-impact decisions (shutting down revenue-generating services, revoking engineer credentials) that the IC cannot make unilaterally.
- **Legal lead:** Guides actions requiring legal permission (examining employee browser history, assessing regulatory disclosure obligations under GDPR or similar frameworks).

**The IC's ongoing job is control, not investigation.** The IC operates a while-loop against the incident:

```
While incident is ongoing:
  1. Check in with each lead: status, new info, roadblocks, personnel needs, fatigue level
  2. Update status documents and dashboards
  3. Ensure executives, legal, and PR are appropriately informed
  4. Identify tasks that can run in parallel
  5. Assess whether enough information exists for remediation decisions
  6. Ask: is the incident over?
Loop.
```

If the IC is performing hands-on tasks, the incident is unmanaged. Step back and assign the task to the OL.

### Step 4 — Establish operational security

Before investigation begins, lock down the communication and investigation environment. Operational security means keeping your response activity secret from the attacker — and from tools that might inadvertently expose it.

**Why operational security cannot wait:** An attacker who detects that you have discovered their presence has two options: go quiet (hiding remaining footholds) or destroy as much of your environment as possible on the way out. Either outcome is bad. Every action your team takes should be evaluated against the question: what would a shrewd attacker conclude if they observed this action?

**Operational security setup checklist:**

- [ ] **New communication channels:** Stand up fresh chat rooms and document stores on infrastructure the attacker cannot access. If the email server or primary chat system may be compromised, do not use it to coordinate the response. Build a new temporary cloud environment with accounts not associated with your organization; distribute clean machines (e.g., Chromebooks) for responders to use.
- [ ] **Clean machines only:** Do not use workstations that may be compromised for investigation work. Log collection and analysis must happen from trusted endpoints.
- [ ] **No direct login to compromised servers:** Logging into a compromised machine with administrative credentials hands those credentials to the attacker. Use pre-deployed remote forensic agents or key-based access methods to collect artifacts without revealing credentials.
- [ ] **Domain obfuscation in all written artifacts:** Write attacker-controlled domains as `example[dot]com` rather than `example.com`. Many collaboration tools (chat clients, spreadsheets, document editors) automatically fetch URLs they detect — a chat window containing `malware_c2[dot]gif` will not silently reach out to the attacker's command-and-control server, but `malware_c2.gif` might. Make this a habit in all documents, even outside incidents.
- [ ] **No port scans or domain lookups against attacker infrastructure:** These actions appear in the attacker's logs as unusual and alert them to your investigation. Do not interact with attacker command-and-control systems.
- [ ] **No premature account lockouts or password resets:** Locking a compromised account before you understand the full scope signals your discovery and may cause the attacker to destroy evidence or pivot to undetected footholds.
- [ ] **No taking systems offline before scoping is complete:** Taking systems offline prematurely destroys forensic evidence and reveals your timeline to the attacker.
- [ ] **Brief every team member explicitly on confidentiality rules:** People do not know information is confidential unless you tell them. Each responder should review and acknowledge the operational security guidelines before starting work.

**The one exception — imminent risk:** If a system is so critical and the vulnerability so easily exploited (e.g., Shellshock-class) that vital data, systems, or lives are at immediate risk, the cost of making your discovery obvious is outweighed by stopping ongoing harm. This decision belongs to executives with IC advisory input, not the IC alone.

### Step 5 — Run the forensic investigation loop

Digital forensics means backtracking through each phase of the attack to reconstruct the attacker's steps. The goal is to identify all affected parts of the organization and understand the full attack path.

**Forensic investigation methods:**

- **Forensic imaging:** Create read-only copies (with checksums) of storage from compromised systems before touching them. Preserves evidence for potential legal proceedings.
- **Memory imaging:** Capture system memory to recover process trees, running executables, and passwords to encrypted files that attackers may have used.
- **File carving:** Recover deleted files from disk — many operating systems only unlink filenames rather than zeroing disk contents. Attackers who delete logs may leave recoverable artifacts.
- **Log analysis:** Reconstruct event sequences from system and network logs to determine who talked to what and when.
- **Malware analysis:** Analyze attacker tools to determine capabilities, communication patterns, and indicators of compromise (IOCs) that the hunting sub-track can search for across the environment.

**The forensic timeline** is the central artifact of the investigation: a chronologically ordered list of events proving correlation and causation of attacker activity. Build it continuously throughout the investigation.

**Shard the investigation into three parallel sub-tracks** when you have sufficient staff:

```
Forensics group  →  finds artifacts on known-compromised systems
       ↓
Reversing group  →  analyzes attacker tools, extracts IOCs
       ↓
Hunting group   →  searches all systems for IOC fingerprints
       ↓
(feeds new leads back to Forensics group)
```

The OL maintains the tight feedback loop between these three groups. Each lead discovered by the forensics or hunting groups becomes a *pivot point*: a new question that spawns a fresh forensic investigation. For example, once the team discovers an attack progressed from a workstation to a file share, the file share becomes the subject of a new forensic investigation.

**Parallelizing beyond forensics:** While investigation continues, assign available staff to tasks that can run ahead:
- If you may need to share forensic findings with law enforcement or external firms, assign someone to prepare a redacted and shareable indicators list now — your raw investigation notes will not be shareable later.
- Assign the RL to begin studying confirmed compromise areas and drafting the cleanup plan as findings accumulate.
- Assign someone to begin the postmortem structure if staff allows.

### Step 6 — Apply the lead-rate decline signal to decide ejection timing

The most difficult decision in a security incident is knowing when to stop investigating and start remediating. You will never know everything. The question is whether you know enough to successfully remove the attacker and protect the data they are after.

**The lead-rate decline signal:** Monitor the rate at which new investigative leads are being discovered. When the interval between new discoveries noticeably increases — when new leads are slowing the way popcorn slows down as a bag finishes popping — the picture is likely complete enough to act. You have probably learned all you need to remove the attacker and protect your data.

Do not wait for certainty. The decision is: have we learned enough to successfully execute remediation? Prior to deciding, the IC should confirm:

- [ ] Does the RL have a complete cleanup plan covering all confirmed compromise areas?
- [ ] Has legal reviewed and approved proceeding to remediation?
- [ ] Do executives understand and approve the remediation plan?
- [ ] Has the CL prepared external communication drafts for any stakeholder notifications that may be required?

### Step 7 — Scale with rotation and hand off with a structured brief

No human can sustain peak performance through a long incident without fatigue degrading their judgment. Beyond 12 hours of continuous work, responders will start making more mistakes than progress — the law of diminishing returns applies to humans. Limit all shifts (including IC shifts) to no more than 12 continuous hours.

**Follow-the-sun rotation for multi-day incidents:** Split the response team into regional groups so fresh responders cycle onto the incident continuously. A team with Americas, Asia-Pacific, and European staff can staff the response 24 hours a day without anyone working unsustainable hours.

**Handover preparation — the outgoing IC should:**

1. Update all tracking documentation, evidence notes, and written records before the handover meeting.
2. Ask themselves: **"If I weren't handing this investigation over, what would I work on for the next 12 hours?"** The incoming IC must have an answer to this question before the handover meeting ends.
3. Run the handover meeting in this sequence:
   1. Delegate a note-taker (preferably from the incoming team).
   2. Summarize current incident state and investigation direction.
   3. Outline the tasks the outgoing IC would have worked on over the next 12 hours.
   4. Open discussion — all attendees.
   5. Incoming IC outlines their planned tasks for the next 12 hours.
   6. Incoming IC establishes the time(s) of the next sync meeting(s).

Each lead (OL, CL, RL) should deliver a corresponding handover to their incoming counterpart before the IC-level handover is complete.

**Maintaining morale during long incidents:**

The IC is responsible for the team's emotional state, not just technical progress. Incidents are stressful. Some engineers rise to the challenge; others find the combination of intensity and ambiguity deeply draining. Watch for:

- **Fatigue:** People who don't recognize their own need for rest still need to take breaks. Leaders may need to intervene.
- **Burnout signals:** Increasing cynicism or "this is unwinnable" statements from critical engineers. Address these directly and frankly — explain expectations, offer a relief period if staff allows.
- **Lead by example:** If you (as IC or OL) visibly take breaks and eat, the team will believe it is actually encouraged.

## Outputs

| Artifact | Description |
|----------|-------------|
| **Incident state document** | Current status, known compromise scope, assigned roles, open leads, decisions made |
| **Forensic timeline** | Chronologically ordered list of confirmed attacker actions with evidence citations |
| **Communication plan** | Stakeholder list, what each group knows, draft external notifications |
| **Remediation handoff package** | RL's cleanup plan covering all confirmed compromise areas, approved by legal and executives |

## Anti-Patterns

**Rushing:** The extra few seconds gained by acting before planning are eclipsed by the consequences of acting without a plan. Security response requires investigation before remediation.

**Semantic misunderstandings:** "We can turn the service back on when the attack is mitigated" means different things to different teams. To the product team: delete the malware and the system is safe. To the security team: the system is not safe until the attacker can no longer exist in or return to the environment. Always be explicit and overcommunicate. The responsibility for ensuring the intended message was received belongs to the communicator, not the listener.

**Hedging:** "We're pretty sure we found all the malware" is a weak answer. The IC needs actionable certainty about specific sub-systems: "We are confident about servers, NAS, email, and file shares; we are not confident about hosted systems because log visibility there is limited." Replace qualifiers with bounded scope statements.

**Overstuffed meetings:** If most attendees are listening rather than contributing, the invite list is too large. Incident leads attend syncs; everyone else works tasks and gets updates from their lead.

**Operational security failures:** Communicating about the incident over potentially compromised channels; logging into compromised servers with privileged credentials; downloading attacker malware from an investigation workstation; performing port scans or domain lookups against attacker infrastructure. Each of these actions may appear in attacker logs and reveal your investigation.

**Hero mode:** Small teams working extra-long hours in "hero mode" is unsustainable and produces lower-quality work. Use it very sparingly, and never beyond 12 hours per shift.

**IC doing technical work:** If the IC is checking logs or performing forensics, no one is managing the incident. Step back.

## Key Principles

**Investigate before remediating.** Unlike a reliability outage (where the system won't resist being fixed), an attacker may be watching your actions. Premature remediation destroys evidence and may trigger destructive exit behavior.

**Declare explicitly.** Saying "this is an incident and I am the IC" is not redundant — it removes ambiguity under high stress when normal processes are bypassed.

**Operational security is a prerequisite, not an afterthought.** Set up clean channels and machines before investigation begins. Once a secret is lost, it is hard to regain.

**The IC's job is control, not investigation.** If the IC is doing hands-on work, the incident is unmanaged.

**The lead-rate decline signal is the ejection signal.** You will never know everything. Know enough to remove the attacker and protect the data they are after — then act.

**Shifts cap at 12 hours.** Fatigue produces more mistakes than progress. Rotation is not a luxury; it is a reliability control applied to humans.

## References

- *Building Secure and Reliable Systems* (Adkins, Beyer, Blankinship, Lewandowski, Oprea, Stubblefield; Google/O'Reilly, 2020)
  - Chapter 17 "Crisis Management" (pp. 387–415):
    - "Is It a Crisis or Not? / Triaging the Incident" (pp. 388–390): three-org ransomware triage comparison
    - "Taking Command of Your Incident / Beginning Your Response" (pp. 391–393): IMAG declaration formula
    - "Establishing Your Incident Team" (pp. 393–394): IC/OL/CL/RL roles
    - "Operational Security" (pp. 394–397): OpSec setup, common mistakes, domain obfuscation
    - "The Investigative Process / Sharding the Investigation" (pp. 398–400): forensics, reversing, hunting sub-tracks; pivot points; forensic timeline
    - "Keeping Control of the Incident / Parallelizing the Incident" (pp. 401–402): IC while-loop, OODA loop, RL parallelization
    - "Handovers" (pp. 402–405): 12-hour shift cap, follow-the-sun rotation, handover meeting agenda, "12-hour question"
    - "Morale" (pp. 405–406): fatigue, burnout, lead-by-example
    - "Communications / Misunderstandings / Hedging / Meetings" (pp. 406–409): semantic misunderstanding example; hedging anti-pattern; kickoff and sync meeting agendas
    - "Putting It All Together" (pp. 410–414): end-to-end worked example (cloud service account compromise)
  - Depends on: `incident-response-team-setup` (roles, severity/priority models, communications plan, playbooks assumed to exist before incident)
  - Feeds into: remediation execution (Chapter 18), postmortem writing

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-incident-response-team-setup`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
