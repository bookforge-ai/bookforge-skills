---
name: disaster-risk-assessment
description: Use when you need to assess disaster risk for a system or organization, perform structured risk analysis before disaster planning, identify which disasters to plan for, build a prioritized risk register, quantify probability and impact of failure scenarios, or answer "what disasters should we prepare for and in what order."
tags: [security, reliability, disaster-planning, risk-assessment, incident-readiness]
---

# Disaster Risk Assessment

Produces a scored, prioritized risk register using a quantitative Probability × Impact matrix. Covers 7 disaster types across 3 themes (Environmental, Infrastructure Reliability, Security) with 18+ pre-seeded scenarios. Output drives response plan prioritization, incident response team scoping, and disaster recovery test selection.

## When to Use

- Starting disaster planning for a new or existing system
- Preparing for a disaster recovery test or tabletop exercise
- Scoping an incident response team's charter and coverage
- Evaluating how a change in infrastructure (new datacenter, cloud migration) shifts risk exposure
- Conducting a per-site risk review for a multi-location organization
- Revisiting a prior assessment after a significant organizational or threat environment change

**Prerequisite:** Know your system's architecture and its key dependencies (networking, authentication, storage, third-party services). Risk ratings are only as good as the system inventory behind them.

## Context & Input Gathering

Before scoring, establish three inputs:

**1. System inventory with criticality classification**

Classify every system the risk could affect into one of three tiers. This classification determines how much impact a given disaster actually has on operations.

| Tier | Label | Definition |
|------|-------|------------|
| 1 | Mission-essential | Absence causes total operational disruption. Organization cannot function. |
| 2 | Mission-important | Absence significantly degrades operations but does not halt them. |
| 3 | Nonessential | Absence has minimal operational impact. Tolerable downtime. |

Ask: which services, if offline for 24 hours, would be catastrophic (Tier 1), serious (Tier 2), or acceptable (Tier 3)?

**2. Geographic and infrastructure context**

Risk ratings are location-dependent. A site in Los Angeles warrants a higher earthquake probability than one in Hamburg. A site in the southeastern US warrants higher hurricane probability. A single-ISP facility warrants higher internet connectivity loss probability than one with redundant circuits. Collect:

- Physical datacenter location(s)
- Existing fault-tolerance controls (redundant power, redundant ISP, UPS, generators)
- Known historical incidents at this site or in this region

**3. Scope boundary**

Decide whether you are assessing at the organizational level (global) or per site. Large organizations should do both — a site that hosts only Tier 3 systems warrants a different response plan than one hosting Tier 1 systems.

## Process

### Step 1 — Start with the pre-seeded risk taxonomy

The matrix in Appendix A of *Building Secure and Reliable Systems* groups disaster scenarios into three themes. Use these as your starting point rather than an empty list. Pre-seeded scenarios prevent the common failure mode of omitting non-obvious risks (e.g., emerging zero-day vulnerabilities, insider intellectual property theft).

**Environmental theme** (natural events that affect physical infrastructure)
- Earthquake
- Flood
- Fire
- Hurricane / severe storm

**Infrastructure Reliability theme** (component and service failures)
- Power outage
- Loss of internet connectivity
- Authentication system down
- High system latency / infrastructure slowdown

**Security theme** (adversarial and vulnerability-driven events)
- System compromise (external attacker gaining unauthorized access)
- Insider theft of intellectual property
- Distributed denial-of-service (DDoS) / denial-of-service (DoS) attack
- Misuse of system resources (e.g., cryptocurrency mining)
- Vandalism / website defacement
- Phishing attack
- Software security bug
- Hardware security bug
- Emerging serious vulnerability (e.g., Meltdown/Spectre, Heartbleed class)

Add organization-specific scenarios beyond this list. Examples: ransomware targeting backup systems, supply chain compromise of a build pipeline, regulatory action requiring emergency data deletion.

### Step 2 — Score each scenario using the P×I scales

For each scenario, assign two values independently, then compute the ranking.

**Probability of occurrence within a year (P)**

| Value | Label |
|-------|-------|
| 0.0 | Almost never |
| 0.2 | Unlikely |
| 0.4 | Somewhat unlikely |
| 0.6 | Likely |
| 0.8 | Highly likely |
| 1.0 | Inevitable |

Score probability based on your specific location, historical data, and existing controls. A site with a generator and UPS reduces power outage probability; a site on a flood plain increases flood probability.

**Impact to organization if risk occurs (I)**

| Value | Label |
|-------|-------|
| 0.0 | Negligible |
| 0.2 | Minimal |
| 0.5 | Moderate |
| 0.8 | Severe |
| 1.0 | Critical |

Score impact relative to the Tier 1/2/3 systems affected. If a disaster only affects Tier 3 systems, impact is at most Moderate. If it takes down a Tier 1 system with no failover, impact is Severe or Critical.

**Ranking = Probability × Impact**

A power outage scored P=0.6, I=0.8 produces Ranking=0.48. A hurricane at P=0.2, I=1.0 produces Ranking=0.20. Sort the completed register from highest to lowest ranking.

### Step 3 — Populate the risk register

Create one row per scenario. Minimum columns:

| Theme | Risk | Probability (P) | Impact (I) | Ranking (P×I) | Systems Impacted | Tier |
|-------|------|-----------------|------------|---------------|------------------|------|
| Environmental | Earthquake | — | — | — | — | — |
| Environmental | Flood | — | — | — | — | — |
| Environmental | Fire | — | — | — | — | — |
| Environmental | Hurricane | — | — | — | — | — |
| Infrastructure Reliability | Power outage | — | — | — | — | — |
| Infrastructure Reliability | Loss of internet connectivity | — | — | — | — | — |
| Infrastructure Reliability | Authentication system down | — | — | — | — | — |
| Infrastructure Reliability | High system latency / infrastructure slowdown | — | — | — | — | — |
| Security | System compromise | — | — | — | — | — |
| Security | Insider theft of intellectual property | — | — | — | — | — |
| Security | DDoS/DoS attack | — | — | — | — | — |
| Security | Misuse of system resources | — | — | — | — | — |
| Security | Vandalism / website defacement | — | — | — | — | — |
| Security | Phishing attack | — | — | — | — | — |
| Security | Software security bug | — | — | — | — | — |
| Security | Hardware security bug | — | — | — | — | — |
| Security | Emerging serious vulnerability | — | — | — | — | — |

Fill in scores, sort by Ranking descending.

### Step 4 — Review for outliers before finalizing

Sorting by ranking is a starting heuristic, not a final answer. Perform a manual outlier review:

- **Low-probability, high-impact outliers:** A scenario ranked 0.10 (P=0.1, I=1.0) may still demand a response plan because the consequence is catastrophic. Flag any scenario with I=1.0 regardless of ranking.
- **Hidden dependencies:** A seemingly low-impact risk may become critical if it disables a monitoring or logging system that other incident responses depend on.
- **Correlated risks:** An earthquake can simultaneously trigger power outage, connectivity loss, and fire. Assess whether scenarios cluster and whether the combined impact exceeds individual rankings.
- **Expert review:** Solicit review from someone outside the team who can identify risks with hidden factors or dependencies. Groupthink tends to underweight unfamiliar scenarios.

### Step 5 — Document scope, assumptions, and review cadence

Record alongside the register:
- Date of assessment
- Location(s) assessed
- Existing controls assumed (e.g., "assumes redundant ISP, UPS, and diesel generator")
- Owner responsible for next review
- Planned review cadence (minimum: annually; recommended: after any major infrastructure change or post-incident)

## Key Principles

**Quantification counters groupthink.** Intuitive risk assessment tends to weight salient scenarios (recent news events, memorable near-misses) over statistically more likely ones. A scored matrix forces explicit probability and impact estimates, making invisible assumptions visible and debatable.

**Probability is infrastructure-dependent, not universal.** A cloud-hosted system with multi-region failover has a different authentication system downtime probability than a single on-premises deployment. Score after accounting for existing controls — but also model what happens if a control fails.

**Ratings must evolve with the system.** Risk posture changes when the organization adds redundant internet circuits, migrates to a different cloud region, or discovers a new vulnerability class. Schedule reviews; do not treat the register as a one-time artifact.

**Low probability does not mean no plan.** Scenarios with I=0.8 or I=1.0 warrant response plans even if their ranking is low. The ranking guides where to invest preparation effort first, not which risks to ignore entirely.

**Assess dependencies alongside primary systems.** Key operational functions include their underlying dependencies — networking, authentication, application-layer components. A mission-essential service that depends on a Tier 3 authentication system effectively elevates that dependency to Tier 1 during an incident.

**Multi-location organizations need per-site assessments.** Global rankings mask site-specific exposure. A site in earthquake country has different environmental risk than headquarters. Run the matrix per site and aggregate.

## Examples

**Example: SaaS company, single US West Coast datacenter, no redundant power**

| Theme | Risk | P | I | Ranking | Systems Impacted |
|-------|------|---|---|---------|-----------------|
| Security | System compromise | 0.6 | 1.0 | 0.60 | Auth service (T1), API (T1) |
| Infrastructure | Power outage | 0.6 | 0.8 | 0.48 | All systems |
| Security | Software security bug | 0.6 | 0.8 | 0.48 | API (T1) |
| Security | Phishing attack | 0.8 | 0.5 | 0.40 | Email (T2), SSO (T1) |
| Infrastructure | Loss of internet connectivity | 0.4 | 1.0 | 0.40 | All externally facing (T1) |
| Security | DDoS/DoS attack | 0.4 | 0.8 | 0.32 | API (T1) |
| Environmental | Earthquake | 0.4 | 0.8 | 0.32 | All systems |
| Security | Emerging serious vulnerability | 0.2 | 1.0 | 0.20 | All systems |
| Environmental | Flood | 0.2 | 0.5 | 0.10 | On-prem equipment (T2) |

**Outlier flag:** Emerging serious vulnerability ranks 0.20 but Impact=1.0. Flag for mandatory response plan despite low ranking. Earthquake and internet connectivity loss are correlated — their combined impact may be higher than either alone.

**Example: Adjusting for existing controls**

After adding a backup ISP: Loss of internet connectivity drops from P=0.4 to P=0.2, Ranking drops from 0.40 to 0.20. After adding UPS and generator: Power outage drops from P=0.6 to P=0.2, Ranking drops from 0.48 to 0.16. Re-run the matrix when controls change to confirm prioritization remains valid.

## References

- *Building Secure and Reliable Systems* (Blank, Oprea et al., Google/O'Reilly, 2020)
  - Chapter 16 "Disaster Planning" — pp. 363–382: disaster type taxonomy (pp. 364), disaster risk analysis methodology (pp. 366), system criticality classification (pp. 366), dynamic response strategy phases (pp. 365)
  - Appendix A "A Disaster Risk Assessment Matrix" — pp. 499–500: Table A-1 with full probability scale, impact scale, pre-seeded scenario taxonomy, and Ranking = P×I formula
- Next steps after completing the register: incident response team setup (Chapter 16, pp. 367–375), response plan development (pp. 371–373), disaster recovery test planning (pp. 376–382)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure And Reliable Systems by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
