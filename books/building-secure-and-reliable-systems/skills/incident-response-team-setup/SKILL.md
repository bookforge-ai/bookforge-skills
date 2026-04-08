---
name: incident-response-team-setup
description: Use when you need to set up an incident response team from scratch, design an IR team charter, define severity and priority models for incidents, create IR playbooks, build a structured testing program, design tabletop exercises, or answer "how do we build and validate our incident response capability."
tags: [security, incident-response, disaster-planning, team-design, tabletop-exercise]
---

# Incident Response Team Setup

Guides building an incident response (IR) team and testing program from zero using a 7-phase process: staffing model selection, role catalog definition, team charter writing, severity and priority model design, operating parameters, response plan development, playbook creation, and a 3-tier testing program. Consumes the risk register produced by `disaster-risk-assessment` to calibrate severity levels against real exposure. Output: IR team charter, severity/priority models, response plan templates, playbook structure, and a testing program design.

## When to Use

- Building an IR team for the first time or formalizing an ad hoc response function
- Redesigning an existing IR team after a significant organizational or threat environment change
- Establishing severity and priority models before the next incident season
- Designing a tabletop exercise or a disaster recovery test program
- Scoping which incidents to handle in-house vs. outsource
- Establishing IR training requirements and response decision criteria

**Prerequisite:** A completed risk register from `disaster-risk-assessment`. The P×I rankings and scenario list from that register feed directly into severity model calibration in Step 4. Without it, severity thresholds will be guesswork rather than evidence-based.

## Process

### Step 1 — Choose a staffing model

Select one of three models or a hybrid based on budget, organizational size, and incident complexity:

| Model | Description | Trade-offs |
|-------|-------------|------------|
| Dedicated full-time IR team | Employees whose primary role is incident response | Always available, appropriately trained, has system access; higher cost |
| Dual-hat (existing staff + IR duties) | Engineers handle regular work plus IR when incidents arise | Lower cost, leverages domain knowledge; responders may be unavailable or fatigued |
| Outsourced | Third parties perform IR activities | Access to specialist skills (e.g., forensics) without headcount; external responders may not be immediately available and lack system context |

**Why this matters:** Outsourcing response time can add appreciable delay during active incidents. Response time is a function of staffing model choice — decide it deliberately rather than by default. Many organizations use a hybrid: in-house for most IR, outsourced for specialized functions like forensics where full-time staff is not cost-effective.

**Avoid single points of failure regardless of model.** Incidents do not respect vacation schedules or time zones. Establish on-call rotations, empower deputies to approve emergency code fixes and configuration changes, and appoint delegates across time zones for multinational organizations.

### Step 2 — Define the role catalog

Identify which roles your team needs. Roles are not individuals — one person may hold multiple roles during an incident, and rotational staffing across shifts is recommended to reduce fatigue.

**Core command roles** (detailed in the incident-command skill):
- **Incident commander (IC):** Leads the response to an individual incident. Coordinates all responders and owns the overall response direction.
- **Operational lead (OL):** Directs technical response operations — the engineering execution arm of the IC.
- **Communications lead (CL):** Owns all internal and external communications during the incident.
- **Reliability lead (RL):** Coordinates site reliability and infrastructure responders.

**Supporting roles:**
- **Site reliability engineers (SREs):** Reconfigure impacted systems or implement code fixes.
- **Security engineers:** Review the security impact and work with SREs and privacy engineers to secure the system.
- **Forensic specialists:** Perform event reconstruction and attribution — determine what happened and how.
- **Privacy engineers:** Address impact on technical privacy matters.
- **Legal:** Provide counsel on applicable laws, statutes, regulations, and contracts.
- **Customer support:** Respond to customer inquiries or proactively reach out to affected customers.
- **Public relations:** Respond to public inquiries and coordinate with the communications lead on media statements.

**Why define roles explicitly:** Knowing who holds each role before an incident eliminates the coordination overhead of figuring it out under pressure. An individual may hold multiple roles, but the roles must be assigned — not assumed.

**Identify a champion:** Designate a person with sufficient organizational seniority to commit resources and remove roadblocks. The champion helps assemble the team and resolves competing priorities between IR work and regular operational commitments.

### Step 3 — Write the team charter

The charter is the IR team's governing document. It must contain three elements:

**Mission statement (one sentence):** A single sentence describing the types of incidents the team handles. This allows anyone to quickly understand what the team does without reading the entire charter.

**Scope:** Describe the environment the team covers — technologies, end users, products, and stakeholders. Clearly define:
- Which incidents are handled by internally staffed resources
- Which incidents are assigned to outsourced teams
- What is explicitly out of scope (e.g., individual customer inquiries about firewall configurations may belong to customer support, not the IR team)

**Definition of success:** How does the organization know when an incident response is complete and can be declared done? Define the done criteria explicitly. Without it, incident close is ambiguous and teams may disengage prematurely.

**Team morale consideration:** Review scope and workload together when establishing the charter. Overworked teams experience productivity drops and attrition. For dedicated or cross-functional virtual response teams alike, sustainable workload must be part of the charter conversation.

### Step 4 — Establish severity and priority models

Use both models concurrently — they are related but serve different purposes. Calibrate severity thresholds against the risk register from `disaster-risk-assessment`: scenarios with high P×I rankings should map to severity 0 or 1.

**Severity model** — categorizes incidents by their impact on the organization:

| Severity | Label | Example |
|----------|-------|---------|
| 0 | Most severe | Unauthorized access across production network |
| 1 | High | Confirmed breach of a single critical system |
| 2 | Medium | Temporary unavailability of security logs |
| 3 | Low | Suspected (unconfirmed) anomalous access |
| 4 | Least severe | Informational alert with no confirmed impact |

Assign severity ratings using the risk register categories. Not every incident deserves a critical or moderate severity rating — accurate ratings ensure incident commanders can correctly prioritize when multiple incidents are reported simultaneously.

**Priority model** — defines how quickly personnel must respond:

| Priority | Response tempo |
|----------|----------------|
| 0 | Immediate response; team members drop all other work |
| 1 | Urgent; respond before end of current shift |
| 2 | High; respond within the business day |
| 3 | Normal; handle within the week |
| 4 | Routine; handle as operational work allows |

**Critical distinction — severity is fixed, priority changes:**

Severity reflects the incident's actual impact on the organization and typically remains fixed throughout the incident's lifecycle. Priority reflects operational tempo and can change as the situation evolves. During early triage and implementation of a critical fix, priority may be 0. Once the fix is in place, priority can lower to 1 or 2 as engineering teams perform cleanup work. Misaligned priority ratings across teams cause coordination failures — one team responding at priority 0 tempo while another treats the same incident as priority 2 will operate at different speeds, delaying proper response.

### Step 5 — Define operating parameters

Operating parameters describe the day-to-day functioning of the IR team and ensure that severity 0 and priority 0 incidents receive timely responses.

Define at minimum:
- **Initial response time target:** How quickly must someone acknowledge a reported incident? (e.g., within 5 minutes, 30 minutes, 1 hour, or next business day — set per severity level)
- **Triage time target:** How quickly must the team complete initial triage and develop a response schedule?
- **Service level objectives (SLOs):** When must incident response interrupt regular day-to-day engineering work? This keeps IR from being deprioritized during busy operational periods.
- **On-call rotation structure:** How are on-call duties load-balanced across the team?

**Why operating parameters matter for distributed or virtual teams:** When an IR team includes members from multiple organizations or outsourced partners, each group may have different assumptions about response speed. Explicit operating parameters force alignment before an incident, not during one.

### Step 6 — Develop response plans

Response plans guide decision-making during severe incidents when responders are working quickly with limited information. Develop plans covering:

- **Incident reporting:** How does an incident get reported to the IR team? Who are the reporting channels for engineers, customers, administrators, and automated alerts?
- **Triage:** Who responds to the initial report and begins triaging? What is the handoff process?
- **Service level objectives:** Reference the SLOs established in Step 5 so responders know the expected tempo.
- **Roles and responsibilities:** Clear definitions for each role during the response.
- **Outreach:** How does the IR team reach engineering teams and participants who may need to assist?
- **Communications plan:** Communication during an incident does not happen without advance planning. The plan must specify:
  - How to inform leadership (email, text, phone call — and what information to include)
  - How to conduct intra-organization communication (chat rooms, videoconferencing, bug tracking tools)
  - How to communicate with external stakeholders such as regulators or law enforcement (partner with legal; maintain an index of contact details and communication methods per external stakeholder)
  - How to communicate with customer-facing teams without tipping off an adversary if the primary communication system is compromised or unavailable

**Backup communication channels are not optional:** Adversaries who compromise an email or instant messaging server can monitor IR coordination threads, sidestep detection, and observe mitigation efforts. If the communication system is offline, the team may be unable to contact stakeholders at other sites. The communications section of every response plan must cover backup communication methods.

Each response plan should contain high-level procedures referencing specific playbooks for detailed execution. Outline the overarching approach for each class of incident — the playbook contains step-by-step instructions.

### Step 7 — Create detailed playbooks

Playbooks complement response plans with specific, procedural instructions from beginning to end. They are team-specific, procedural in nature, and must be frequently revised. Examples of what playbooks cover:

- How to grant responders emergency temporary administrative access (breakglass procedures)
- How to output and parse particular logs for analysis
- How to fail over a system and when to implement graceful degradation
- Criteria for when to notify senior leadership and when to work with localized engineering teams

**Access and currency:** Store playbooks and response plans in a location accessible during a disaster — if company servers go offline, cloud-hosted documentation or printed offline copies must remain available. Set a review cadence (minimum: annually; after any significant infrastructure or configuration change) because threat postures change and new vulnerabilities emerge.

**Incident tracking:** Identify a suitable system for tracking information and retaining incident data. Security and privacy incident teams may want a system with need-to-know access controls; reliability response teams may prefer broader company access for coordination.

**Training for all engineers, not just IR team members:** Train all engineers who may assist the IR team on the IR roles and their responsibilities. Use the Incident Management at Google (IMAG) framework, which is based on the Incident Command System, as a reference structure for role assignments (incident commander, operational lead, communications lead). Establish a finite time limit — such as 15 minutes — for a first responder to grapple with an incident before escalating to the IR team. Pre-establish decision criteria for high-pressure choices (e.g., whether to take a compromised system offline vs. preserve it for forensics) so responders are not making gut decisions under stress.

### Step 8 — Build the testing program

Testing validates that your materials work before a real incident. Run tests at a minimum annually. The program has three tiers:

**Tier 1 — Automated system auditing**

Audit all critical systems and their dependencies (backup systems, logging systems, software updaters, alert generators, communication systems) to verify they are operating correctly. A full audit confirms:

- Backups are created, stored safely, stored for the appropriate retention period, and stored with correct permissions — conduct data recovery and validation exercises periodically
- Event logs are stored correctly and for a period appropriate to the organization's risk level (the industry average for detecting intrusions is approximately 200 days; logs deleted before detection cannot be used for investigation)
- Critical vulnerabilities are patched in a timely fashion — audit both automatic and manual patch processes
- Alerts fire correctly — validate each alert rule, and account for dependencies (e.g., how are alerts impacted if an SMTP server goes offline during a network outage?)
- Communication tools retain failover capability and message history needed for postmortems

**Tier 2 — Nonintrusive tabletop exercises**

Tabletop exercises test documented procedures and team decision-making without taking systems offline. They can also serve as a proxy when end-to-end production testing is not feasible (e.g., testing an earthquake response without causing an earthquake).

Design parameters for a standard tabletop exercise:
- **Duration:** 60 minutes
- **Decision points:** 10–20 storyline branch points structured like a "choose your own adventure" — each participant decision affects the subsequent scenario state (e.g., if the team takes a compromised email server offline, participants cannot send email notifications for the rest of the scenario)
- **Believability:** Base scenarios on realistic attack vectors and known vulnerabilities so participants engage without suspending disbelief
- **Artifacts:** Provide realistic artifacts — log files, customer reports, alert screenshots — to increase immersion and realism
- **Participants:** Include the full range: frontline engineers following playbooks, senior leadership making business-level decisions, public relations professionals coordinating external communications, and legal providing guidance on public statements
- **Active demonstration:** Participants should demonstrate procedures, not just describe them. If a playbook calls for escalating to forensics and blocking hostile traffic, the responder should carry out those steps during the exercise — building muscle memory
- **Facilitator preparation:** The facilitator must be deeply familiar with the scenario and typical responses in order to improvise and nudge responders in the right direction as the exercise unfolds
- **Outcomes:** Conclude with actionable feedback — what worked, what did not, and concrete improvement recommendations with assigned owners. Create action items to address each recommendation. An exercise without implemented lessons is entertainment, not preparation.

**Tier 3 — Fault injection and disaster recovery testing**

Production-environment testing validates that systems handle failure modes correctly under real-world constraints. This is where IR teams observe how their responses affect actual production environments.

Sub-types to include in the program:

- **Single-system fault injection:** Inject faults at the component level without disrupting the entire system. Use fault injection frameworks (e.g., the Envoy HTTP proxy fault injection filter) to return arbitrary errors for a percentage of traffic or delay requests for a specific time period. This tests timeout handling and isolates team dependencies.
- **Human resource testing:** Test what happens when key personnel are unavailable. IR teams that rely on individuals with institutional knowledge rather than documented processes are fragile — validate that documented processes function when those individuals are absent.
- **Multicomponent testing:** Test simultaneous failure of multiple dependent components. When failovers occur, verify that the system respects existing access control lists and that authorization services fail closed (not open).
- **System-wide failovers:** Test full failover to secondary or disaster-recovery datacenters. Until you actually fail over, you cannot confirm that your failover strategy will protect your business and security posture. For cloud-hosted services, test what happens when an entire availability zone or region fails.

**Google's disaster recovery test (DiRT) program — combined reliability and security test:**

During one annual disaster recovery test (part of Google's DiRT program), site reliability engineers tested whether breakglass credentials — emergency credentials that can bypass normal access controls when standard access control list services are down — actually worked to gain emergency access to the corporate and production networks. The DiRT team simultaneously looped in the signals detection team. When engineers engaged the breakglass procedure, the detection team was able to confirm that the correct alert fired and that the access request was recognized as legitimate. This combined test validated both the reliability of the emergency access path and the integrity of the security alerting system in a single exercise — demonstrating that reliability and security testing can be designed to reinforce each other rather than running as separate programs.

### Step 9 — Establish a feedback loop

Testing without feedback is entertainment. After every test and every live incident:

- Measure responses: track time taken at each stage of the response to identify corrective measures
- Write blameless postmortems focused on process and system improvement
- Create feedback loops for improving existing plans and developing new ones
- Collect artifacts from exercises and feed gaps back into signal detection
- Save logs and relevant materials from security exercises for forensic analysis
- Evaluate even "failed" tests — what partial successes can you build on?

## Key Principles

**Severity is fixed; priority is variable.** Confusing the two causes teams to treat the same incident at different operational tempos. Severity describes what happened; priority describes how fast to respond right now.

**Roles are not individuals.** One person can hold multiple roles. The goal is to ensure every role is explicitly assigned, not that every role maps to a unique person.

**Communication plans must survive compromise of primary channels.** Design backup communication methods before an incident, not during one when an adversary may be monitoring your primary channels.

**Testing has diminishing returns when it stays comfortable.** Automated audits catch configuration drift; tabletops build decision-making muscle memory; fault injection and disaster recovery tests expose the gaps that neither audit nor simulation reveals. All three tiers are necessary.

**The risk register drives severity calibration.** High P×I scenarios from `disaster-risk-assessment` should map to severity 0 and 1 — this connects the abstract risk model to the operational response model.

**Training extends beyond the IR team.** Any engineer who may encounter an incident first is part of the response system. Train them on escalation criteria and time limits (15-minute window before escalating) so the IR team is engaged at the right time.

## References

- *Building Secure and Reliable Systems* (Blank, Oprea et al., Google/O'Reilly, 2020)
  - Chapter 16 "Disaster Planning" — pp. 367–385
    - "Setting Up an Incident Response Team" (pp. 367–373): staffing models, role catalog, team charter, severity/priority models, operating parameters, response plan structure, playbook guidance
    - "Prestaging Systems and People Before an Incident" (pp. 373–376): configuring systems, training, processes and procedures
    - "Testing Systems and Response Plans" (pp. 376–382): automated auditing, tabletop exercises (design parameters pp. 378–379), production environment testing (pp. 379–381), evaluating responses (pp. 382)
    - "Google Examples" (pp. 383–385): disaster recovery test (DiRT) breakglass + security alerting combined test (p. 384)
  - Depends on: `disaster-risk-assessment` (risk register feeds severity model calibration)
  - Related: `incident-command` (IMAG framework, IC/OL/CL/RL role execution detail)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure And Reliable Systems by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
