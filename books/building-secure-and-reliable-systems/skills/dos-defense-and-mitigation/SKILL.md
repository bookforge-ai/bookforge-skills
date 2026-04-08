---
name: dos-defense-and-mitigation
description: Design DoS-resistant systems or respond to an active denial-of-service attack. Use this skill when designing a new service and want to evaluate its attack surface and build in layered defenses, assessing whether a production system's architecture is DoS-hardened, investigating a traffic spike to determine whether it is an attack or a self-inflicted surge, detecting a client retry storm and needing to apply backoff and jitter fixes, building or reviewing a DoS mitigation system (detection + response pipeline), or deciding how to respond strategically to an ongoing attack without leaking information about your defenses to the adversary.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/building-secure-and-reliable-systems/skills/dos-defense-and-mitigation
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: building-secure-and-reliable-systems
    title: "Building Secure and Reliable Systems"
    authors: ["Heather Adkins", "Betsy Beyer", "Paul Blankinship", "Piotr Lewandowski", "Ana Oprea", "Adam Stubblefield"]
    chapters: [10]
tags: [security, reliability, dos-mitigation, load-management, resilience]
depends-on: [resilience-and-blast-radius-design]
execution:
  tier: 2
  mode: full
  inputs:
    - type: context
      description: "System architecture description, traffic anomaly report, incident alert, or design proposal. For active attacks: include available traffic telemetry (request rates, source IPs, User-Agent distribution, affected endpoints)."
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Works from a system description or active incident context. Output: DoS defense assessment with architectural recommendations and mitigation playbook, OR active incident response plan."
discovery:
  goal: "Produce a DoS defense assessment that identifies attack surface weaknesses, evaluates architectural and service-layer defenses, designs monitoring and graceful degradation behavior, and delivers a strategic response plan — including self-inflicted surge detection."
  tasks:
    - "Model the attacker's strategy: identify the weakest link in the request dependency chain"
    - "Audit layered defense coverage across shared infrastructure (edge, network LB, application LB)"
    - "Evaluate service-level design for caching, request minimization, and egress bandwidth controls"
    - "Define monitoring and alerting thresholds that minimize false positives and maximize actionability"
    - "Design graceful degradation modes and quality-of-service priorities for attack conditions"
    - "Design or review the DoS mitigation system (detection + response pipeline, fail-static behavior)"
    - "Plan a strategic response that avoids leaking defense fingerprints to the adversary"
    - "Detect and fix self-inflicted surges: client retry storms and organic traffic misidentification"
  audience: "engineers, SREs, security engineers, and architects at intermediate-to-advanced level"
  when_to_use: "When designing a new service for DoS resilience, reviewing a system's attack posture, responding to an active traffic anomaly, fixing client retry behavior, or building a DoS mitigation system"
  environment: "System architecture description or active incident telemetry. Knowledge of service capacity and traffic baselines is needed for monitoring thresholds."
  quality: placeholder
---

# DoS Defense and Mitigation

## When to Use

Apply this skill when:

- Designing a new service and want to evaluate its attack surface and choose cost-effective layered defenses
- Auditing an existing system's DoS posture before a launch or after an incident
- Responding to an active traffic anomaly — including determining whether it is an attack or a legitimate surge
- Clients are caught in retry loops that compound a server outage into a denial of service
- Building or reviewing an automated DoS mitigation system (detection + response pipeline)
- Deciding how to respond to an attack without teaching the attacker how your defenses work

**The core economic model:** A DoS attack is a supply-and-demand imbalance. The adversary drives demand above your supply capacity. Simply absorbing all attacks by overprovisioning is rarely the most cost-effective approach. Instead, eliminate as much attack traffic as possible at each successive layer, so the expensive inner layers only have to handle what the cheap outer layers could not stop.

**Dependency note:** This skill builds on load shedding, throttling, and graceful degradation concepts from `resilience-and-blast-radius-design`. If those mechanisms are not yet defined for the system under review, complete that skill first.

Before starting, confirm you have:
- A description of the system's architecture or active traffic telemetry
- Traffic baselines (normal request rate, peak request rate, request cost distribution)
- Ownership of the affected service layers, or contacts for layers you cannot change

---

## Context and Input Gathering

### Required Context

- **System description or traffic telemetry:** Architecture diagram or prose describing how requests flow through the system, or — for active incidents — current traffic metrics, source IP distribution, and User-Agent samples.
- **Capacity baseline:** What is the normal request rate? What rate causes degradation? What rate causes outright failure?
- **Service dependency chain:** What external services does this service depend on? (DNS, databases, third-party APIs)

### Observable Context

If a system description is provided, scan for:
- A single constrained resource (network bandwidth, CPU, memory, a database backend) that an attacker could saturate
- Missing defenses at one or more layers: edge, network load balancer, application load balancer, service frontend
- No caching proxy between the edge and the application backend
- Client libraries that retry on error without exponential backoff or jitter
- No request rate monitoring at the service level — only CPU or memory

For active traffic anomalies, additionally scan for:
- Requests all sharing the same User-Agent, character set, or access pattern
- Traffic bursts correlated with an external event (news story, earthquake, live broadcast)
- Traffic originating from a geographically concentrated set of IPs or ASNs
- DNS retry rate spiking at 30x normal — a classic sign of recursive DNS retry storms

### Default Assumptions

- If the system has no existing DoS defenses: start with shared infrastructure defenses before service-layer changes — they are cheaper and protect multiple services at once
- If the traffic anomaly is ambiguous (attack or legitimate): do NOT immediately block; investigate the request distribution before taking action
- If the DoS mitigation system does not exist: design it to fail static (policy unchanged on controller failure) rather than fail open or fail closed
- If client retry behavior is uncontrolled: treat exponential backoff + jitter as a mandatory fix, not an optimization

### Sufficiency Check

You have enough to proceed when:
1. You can trace a request from the internet through all dependency layers to the backend
2. You know the system's capacity at each layer
3. You know whether traffic anomaly investigation is needed (active incident) or this is a design review

---

## Process

### Step 1 — Model the Attacker's Strategy

Understanding how an attacker would approach the system lets you find its weakest points before they do.

**Map the request dependency chain** for a typical user request:

1. DNS query resolves the IP address of the service
2. Network carries the request to service frontends
3. Service frontends interpret and route the request
4. Service backends (databases, caches, third-party APIs) generate the response

An attack that disrupts any link in this chain disrupts the service. The attacker will target the link with the lowest cost-to-disrupt.

**Attacker resource efficiency:** A sophisticated attacker will not flood with simple requests — they will generate requests that are more expensive to answer than to send. Examples: triggering search functionality, initiating sessions that exhaust connection state, or exploiting high-cost API endpoints.

**Attack types by scale requirement:**

| Attack type | How it works | Primary defense |
|---|---|---|
| Volumetric flood | Saturate bandwidth or CPU with high packet/request rate | Edge throttling, anycast dispersal |
| Amplification (DDoS) | Spoof victim IP; small requests generate large responses from third-party servers (DNS, NTP, memcache) | Router ACLs blocking UDP from abusable protocols; network-layer filtering |
| Application-layer | Legitimate-looking requests targeting expensive operations | Application-layer rate limiting; CAPTCHA challenges |
| Botnet / DDoS | Distributed attack from many machines — cannot be blocked by single-source filtering | Shared infrastructure defenses; collaboration with upstream providers |

**Threat model priority:** Use the number of machines an attacker would need to control to cause user-visible disruption as a proxy for attack cost. Prioritize defending the attack vectors that are cheapest for an adversary to mount against your specific architecture.

**Output for this step:** Dependency chain map with the weakest link annotated. Attack type assessment ranked by attacker cost-to-mount.

---

### Step 2 — Audit Layered Defense Coverage (Defendable Architecture)

Layered defenses eliminate attack traffic as early as possible, protecting expensive inner layers from having to absorb what cheaper outer layers can stop.

**The three-layer stack to evaluate:**

```
Internet traffic
       |
  [Edge routers]            ← throttle high-bandwidth attacks; drop suspicious traffic via ACLs
       |
  [Network load balancers]  ← throttle packet-flood attacks; protect application load balancers
       |
  [Application load balancers] ← throttle application-specific attacks; protect service frontends
       |
  [Service frontends]
       |
  [Backends / databases]
```

**For each layer, ask:**
- Does it have a mechanism to throttle or drop attack traffic before passing it downstream?
- Can it be overwhelmed by a style of attack the outer layer allows through?
- Is it stateless or stateful? Stateful components (firewalls with connection tracking) are vulnerable to state exhaustion attacks — use router ACLs instead.

**Shared infrastructure advantage:** Defenses at the network and load-balancer layers protect every service behind them. A single investment covers a broad range of services. This is the most cost-effective place to deploy defenses — do not skip it in favor of service-level-only fixes.

**Anycast for geographic distribution:** If a large DDoS targets a single datacenter, anycast routing automatically disperses traffic across all locations announcing the same IP address. No reactive system is needed — traffic is naturally absorbed across the global footprint.

**Caching proxies near the edge:** Deploy caching proxies close to the edge with correct `Cache-Control` headers. Cached responses require zero backend processing. This reduces both attack impact and normal operating costs.

**Amplification defense:** Router ACLs that throttle or block UDP traffic from protocols used for amplification (DNS, NTP, memcache) stop reflected amplification attacks at the edge. These attacks are identifiable by their well-known source ports.

**Output for this step:** Layer-by-layer defense inventory table. Mark each layer: defended / partially defended / undefended. Identify the first undefended layer that attack traffic reaches.

---

### Step 3 — Evaluate Service-Level Design (Defendable Services)

Service and application design choices have a significant impact on how well a service survives a DoS attack — and how much it costs to run in normal operation.

**Three design levers to evaluate:**

**Caching proxies (highest impact)**
- Use `Cache-Control` and related headers so proxy servers can serve repeated requests without hitting the application backend
- Applies to static images, CSS, JavaScript, and often the homepage itself
- Why: every cached response served at the edge is one less request reaching the backend; this reduces DoS impact proportionally to cache hit rate

**Minimize application requests**
- Reduce the number of requests a page requires: combine multiple small images into a single sprite; serve bundled assets
- Fewer legitimate requests per session = cleaner signal for anomaly detection (bots making many more requests than real users stand out more clearly)
- Why: each request consumes server resources; reducing the baseline consumption increases the margin available to absorb attack traffic

**Minimize egress bandwidth**
- Resize images to the minimum size needed for display; serve appropriately compressed formats
- Rate-limit or deprioritize responses to requests for unavoidably large resources
- Why: while most attacks target ingress bandwidth, egress saturation attacks (requesting a large resource repeatedly) are possible; minimizing response sizes limits exposure

**Output for this step:** Service-level defense checklist with gap annotations. Estimate the cache hit rate for the highest-traffic endpoints.

---

### Step 4 — Define Monitoring and Alerting

Outage resolution time is dominated by mean time to detection (MTTD) and mean time to repair (MTTR). A DoS attack may appear as a spike in CPU, memory exhaustion, or error rate — not obviously as a traffic anomaly — unless request-rate monitoring is in place.

**Minimum monitoring requirements:**

- Request rate per endpoint (not just aggregate) — attack traffic often concentrates on specific endpoints
- CPU utilization and memory usage at service frontends
- Network bandwidth in and out at each layer
- DNS query rate (for detecting recursive retry storms — a 30x spike is a strong signal)
- Syncookie trigger rate (synflood indicator)

**Alerting principles:**

- Alert when demand exceeds service capacity AND automated DoS defenses have engaged — not before. Pre-capacity alerts create noise and lead teams to absorb attacks that would resolve without human intervention.
- For network-layer attacks: alert only if a link becomes saturated, not for all high-bandwidth events
- For synflood: alert if syncookies are triggered, not for all new connection attempts
- Do NOT page on request rate alone if the service is still healthy — distinguish "high traffic" from "service degradation"

**Why this matters:** Noisy alerts that fire before human action is required train teams to ignore pages. Alert only when human intervention may actually change the outcome.

**Output for this step:** Monitoring metric list with alert thresholds and escalation conditions. Flag any layer with no request-rate visibility.

---

### Step 5 — Design Graceful Degradation Under Attack

When absorbing an attack is not feasible, the goal is to reduce user-facing impact to the minimum. This step relies on the load shedding and throttling mechanisms defined in `resilience-and-blast-radius-design`.

**Throttle, do not block outright:**
- Use network ACLs to throttle (not hard-block) suspicious traffic during an active attack
- Retain visibility into blocked traffic so you can identify legitimate users caught in the filter and adjust
- Hard-blocking makes you invisible to the threat and risks impacting legitimate users who share an IP or network path with attackers

**Quality-of-service (QoS) prioritization:**
- Assign higher QoS to critical user-facing traffic and security-critical operations
- Deprioritize batch copies, background sync, and other low-value traffic during attack conditions
- Released bandwidth from lower-priority queues becomes available to high-priority traffic

**Application degraded modes:**
- Define explicit degraded operating modes ahead of time — not during an incident
- Examples from Google production:
  - Blogger: serve read-only mode, disable comments
  - Web Search: serve reduced feature set (disable spelling correction, related search)
  - DNS: answer as many queries as possible; designed to never crash under any load

**CAPTCHA as a mitigation bridge:**
- Automated defenses (IP throttling, CAPTCHA challenges) provide immediate mitigation while giving the incident response team time to analyze and design a custom response
- CAPTCHA challenges should issue browser cookies with a long-term exemption to avoid repeatedly challenging legitimate users
- Exemption cookies should contain: pseudo-anonymous identifier, challenge type, timestamp, solving IP address, and a signature (to prevent forgery and botnet sharing)
- False positives are unavoidable when blocking by IP — NAT and shared addresses are common. CAPTCHA is the lowest-friction way to allow legitimate users behind a blocked address to bypass the block

**Output for this step:** Degraded mode definitions per service component. QoS priority assignments for critical traffic. CAPTCHA/challenge strategy if applicable.

---

### Step 6 — Design or Review the DoS Mitigation System

An automated DoS mitigation system provides fast, consistent response that does not depend on human reaction time. It must be designed to handle its own failure modes safely.

**Two required components:**

**Detection:**
- Statistical traffic sampling at all endpoints, aggregated to a central control system
- Control system identifies anomalies (traffic volume, distribution, request patterns) that may indicate attacks
- Works in conjunction with load balancers that understand service capacity — so the system can determine whether traffic volume warrants a response
- Requires sampling, not full logging — at attack volumes, full logging is itself a resource exhaustion risk

**Response:**
- Ability to implement a defense mechanism against detected anomaly — most commonly, providing a set of IP addresses or traffic patterns to block or challenge
- Response must be fast: seconds, not minutes. Attacks cause immediate outages; the mitigation system must respond at machine speed

**Failure mode design:**

- **Fail static:** If the controller fails, the policy does not change. This allows the system to survive an attack that also targets the control plane — a real risk when the control plane uses the same infrastructure. Fail static is preferable to fail open (attack traffic flows) or fail closed (all traffic blocked, service outage).
- **Canary deployment:** Apply new automated responses to a subset of production infrastructure before deploying everywhere. Because attacks cause immediate outages, the canary window can be very short — as little as 1 second — but it must exist to guard against configuration errors.
- **Resilient control plane:** The DoS mitigation system itself must not depend on infrastructure that may be impacted by the attack. This extends to the incident response team's communication tools — if Slack or Gmail are under attack, have backup communication channels and playbook storage.

**Output for this step:** Detection + response component design. Failure mode policy (fail static confirmed). Canary deployment plan for automated responses.

---

### Step 7 — Plan a Strategic Response

Responding purely reactively — filtering the attack traffic signature immediately — teaches the adversary what your defenses can see. A strategic response exploits the adversary's uncertainty about your capabilities.

**Do not expose your detection method:**

Example: An attack arrived with `User-Agent: I AM BOT NET`. Rather than dropping all traffic with that string (which would teach the attacker to change User-Agents), enumerate the IPs sending that traffic and intercept all of their requests with CAPTCHAs — including any future requests, even with a changed User-Agent. This blocked the botnet's A/B testing capability.

**Adversary capability inference:**
- Small amplification attack → attacker likely has a single server, limited to spoofed packets
- HTTP DDoS fetching the same page repeatedly → attacker likely has a botnet
- Traffic that looks exactly like legitimate users → attacker may be a scraper, not a volumetric attacker

**When the adversary may not be an attacker:**
- Unexpected traffic that matches real user behavior (browser distribution, geographic location) may be legitimate surge, not an attack
- Before applying adversarial defenses, verify the traffic profile against the "self-inflicted attack" patterns in Step 8

**Collaboration and escalation:**
- DoS mitigation providers can scrub certain traffic types upstream, before it reaches your infrastructure
- Network providers can perform upstream filtering closer to the attack source
- Network operator communities can coordinate to identify and filter attack sources
- Do not treat DoS defense as a problem to solve alone at the service layer

**Output for this step:** Response plan that avoids revealing the detection method. Adversary capability assessment. Escalation path to upstream providers if needed.

---

### Step 8 — Detect and Fix Self-Inflicted Surges

Not all traffic spikes are attacks. During an incident, the natural instinct is to look for an adversary — but a self-inflicted surge can look identical to a volumetric attack and will be worsened by adversarial countermeasures.

**Two categories of self-inflicted surge:**

**Organic traffic surge (synchronized user behavior):**
- Cause: an external event synchronizes user actions — a natural disaster (earthquake, storm) drives users to check news, social media, or safety services simultaneously; a live broadcast or game show drives viewers to interact with a service in unison
- Signal: traffic matches real user browser distribution, geographic distribution, and request patterns
- Key example: In 2009, Google Web Search received a burst of traffic for German words with identical character prefixes, arriving in three waves. SREs initially suspected a botnet conducting a dictionary attack. Investigation revealed the traffic matched real German browsers from Germany. Root cause: a televised game show challenged contestants to find word completions that returned the most Google search results. Viewers at home played along simultaneously. The "attack" was addressed with a design change — launching a word-completion suggestion feature — rather than a security response.
- Response: design changes that reduce the demand spike (precomputation, caching, autocompletion); NOT rate limiting or blocking

**Client retry storm (misbehaving software):**
- Cause: a server returns errors; clients retry immediately; when many clients are in the retry loop simultaneously, the resulting demand prevents the server from recovering
- This is especially severe for services like authoritative DNS servers, where recursive DNS clients controlled by other organizations retry aggressively and can reach 30x normal traffic during an outage
- Fix — exponential backoff + jitter (mandatory, not optional):
  - **Exponential backoff:** double the wait period after each failed attempt (e.g., 1s → 2s → 4s → 8s). This limits the total request rate from any single client.
  - **Jitter:** add a random duration to each wait period. Without jitter, all clients in the retry loop synchronize on the same retry cadence — producing synchronized bursts. Jitter de-synchronizes retries, smoothing demand into a constant low rate.
  - Both are required: backoff alone does not prevent synchronization; jitter alone does not prevent escalating load from a single client
- If you do not control the client: the best response is to answer as many requests as possible while keeping the server healthy via upstream request throttling. Each successful response allows one client to escape its retry loop.

**Distinguishing attack from self-inflicted surge — diagnostic checklist:**

| Signal | Suggests attack | Suggests self-inflicted surge |
|---|---|---|
| Requests match real browser/OS distribution | No | Yes |
| Requests originate from expected geographic regions | No | Yes |
| Requests target a diverse set of queries/endpoints | No (attacks are focused) | Yes |
| Traffic arrives in correlated waves | Possible (botnet scanning) | Yes (event-driven) |
| Traffic correlates with a known external event | No | Yes |
| DNS retry rate is 30x normal | No | Yes (retry storm) |

**Output for this step:** Self-inflicted surge assessment: organic event or retry storm. Fix: design change (organic) or backoff + jitter implementation (retry storm).

---

## Deliverable

Produce a DoS defense assessment report with the following sections:

1. **Attack surface map** — dependency chain with weakest link annotated; attack type assessment by attacker cost
2. **Layered defense inventory** — coverage at edge, network LB, application LB, and service layer; gaps marked
3. **Service-level design assessment** — caching, request minimization, egress bandwidth findings
4. **Monitoring and alerting plan** — metrics, thresholds, alert conditions
5. **Graceful degradation design** — degraded operating modes, QoS priorities, CAPTCHA strategy
6. **DoS mitigation system design** — detection + response architecture, fail-static policy, canary plan
7. **Strategic response plan** — response approach, adversary capability inference, escalation path
8. **Self-inflicted surge assessment** — organic event or retry storm diagnosis, fix recommendations

---

## Key Principles

### The Economics of DoS Defense

Simply absorbing attacks by overprovisioning is not cost-effective at scale. The defender's strategy is to eliminate attack traffic at each layer for the minimum cost, so the expensive inner layers see only residual attack volume. Shared infrastructure defenses (edge, network LB) are the highest-leverage investment because they protect all services at once.

### Layered Defense: Eliminate Early, Protect Deep

Each defense layer should be able to handle the attack traffic that breaches the outer layer. Defenses near the edge are cheap (bandwidth is shared); defenses deep in the stack are expensive (CPU, database connections). Drop as early as possible.

### Fail Static — Never Fail Open or Closed in the Mitigation System

A DoS mitigation controller that fails open lets attack traffic through. One that fails closed creates a self-inflicted outage. Failing static — freezing the current policy — is the correct tradeoff: the system continues functioning at whatever state it was in when the controller went down, without making things worse in either direction.

### Strategic Response: Do Not Teach the Adversary

Immediately dropping traffic matching the attack signature reveals exactly what your detection sees. Instead, respond in ways that do not fingerprint your detection method — for example, challenging all traffic from identified sources rather than only traffic matching the current attack signature. This blocks the adversary's ability to A/B test your defenses.

### Self-Inflicted Surges Require Different Responses Than Attacks

Applying rate limiting and blocking to an organic surge or a client retry storm will worsen the situation. Always verify the traffic profile before applying adversarial countermeasures. The correct response to a retry storm is to serve as many requests as possible while backoff + jitter propagates; the correct response to an organic surge is a design change that reduces demand.

### Backoff and Jitter Are Both Required

Exponential backoff without jitter still produces synchronized bursts when many clients fail simultaneously. Jitter without backoff limits per-client load but does not prevent total load from remaining high. Both are necessary. At Google, exponential backoff with jitter is standard in all client software.

---

## Examples

### Example 1 — Strategic Response: The User-Agent Botnet

Google received an attack where all traffic contained `User-Agent: I AM BOT NET`. Rather than dropping that User-Agent (which would immediately teach the attacker to use `User-Agent: Chrome`), SREs enumerated all IPs sending that traffic and applied CAPTCHA challenges to all of their requests — regardless of User-Agent. This prevented the attacker from using A/B testing to discover which signals the defense was keying on, and blocked future requests even after the User-Agent changed.

### Example 2 — Self-Inflicted Surge: The German TV Game Show

In 2009, Google Search received a burst of traffic for German words with identical character prefixes, arriving in three waves roughly 10 minutes apart. Initial suspicion: a botnet conducting a dictionary attack. Investigation found the traffic originated from machines in Germany and matched real browser distributions. Root cause: a televised game show challenged contestants to find word completions with the most Google search results — and viewers at home searched along. The response was a design change: adding word-completion suggestions as users type, which reduced the number of queries users submitted. No adversarial countermeasures were needed.

### Example 3 — Client Retry Storm: DNS Outage

An authoritative DNS server experiences an outage. Recursive DNS servers controlled by external organizations immediately begin retrying, escalating to 30x normal traffic. This prevents the server from recovering — each attempted recovery is overwhelmed by the retry flood. The correct response is to serve as many requests as possible (each successful answer lets one DNS resolver escape its retry loop) while applying upstream request throttling to preserve server health. The long-term fix is to ensure all clients implement exponential backoff with jitter — but this cannot be controlled externally.

### Example 4 — CAPTCHA Exemption Cookie Design

When blocking by IP, legitimate users behind the same NAT as an attacker are blocked. A CAPTCHA challenge allows them to prove they are human and receive a browser-based exemption cookie. The cookie must contain: a pseudo-anonymous identifier (allows abuse detection and revocation), the challenge type (allows requiring harder challenges for suspicious behaviors), a timestamp (allows expiring old cookies), the solving IP address (prevents botnets from sharing a single exemption across many machines), and a cryptographic signature (prevents forgery).

---

## References

- Chapter 10: Mitigating Denial-of-Service Attacks, *Building Secure and Reliable Systems* (pp. 217–229)
- Chapter 8: Design for Resilience (load shedding, throttling, graceful degradation — prerequisite concepts)
- Chapter 9: Design for Recovery (recovery after a DoS causes an outage)
- *Site Reliability Engineering* book, Chapter 22: Addressing Cascading Failures (retry storms, load shedding)
- Project Shield (Google): shared DoS defense infrastructure illustrating economy-of-scale defense
- See `resilience-and-blast-radius-design` skill for load shedding and throttling implementation

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Building Secure and Reliable Systems by Heather Adkins, Betsy Beyer, Paul Blankinship, Piotr Lewandowski, Ana Oprea, Adam Stubblefield.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-resilience-and-blast-radius-design`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
