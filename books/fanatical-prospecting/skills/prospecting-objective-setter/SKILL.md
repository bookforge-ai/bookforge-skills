---
name: prospecting-objective-setter
description: |
  Set the correct primary, secondary, and tertiary objective for any prospecting touch — before you make the call, send the email, or walk in the door. Use this skill when someone asks "what is my goal for this call", "should I try to set an appointment or just qualify", "appointment vs close — what should I go for", "what's my objective for this prospecting block", "should I qualify or pitch on this outreach", "what is the four objectives framework", "how do I decide what to ask for on a cold call", "primary secondary tertiary prospecting objective", "what should I optimize for in my cold email", "I have a new territory what should my prospecting objective be", "should I set appointments or close on the phone", "when is build familiarity the right objective", "my prospects are all unqualified what should I do first", or "how does sale complexity change my prospecting goal". Also invoke whenever a rep has a prospecting block coming up and wants to ensure every touch has a defined target outcome. This skill applies the Four Objectives framework (Set Appointment / Gather Information and Qualify / Close a Sale / Build Familiarity) to the rep's specific situation — sale complexity, channel, prospect qualification state, territory tenure, buying-window status — and produces a decision matrix mapping prospect tiers to correct primary/secondary/tertiary objectives. The output is an Objective Call Plan the rep uses to set up their next prospecting block.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/prospecting-objective-setter
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
depends-on: []
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting: The Ultimate Guide to Opening Sales Conversations and Filling the Pipeline by Leveraging Social Selling, Telephone, Email, Text, and Cold Calling"
    authors: ["Jeb Blount"]
    chapters: [9]
tags: [sales, prospecting, objective-setting, sdr, bdr, sales-strategy, cold-calling, inside-sales, outside-sales, qualification, pipeline, outbound]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Situation brief — product/service description, sale complexity (complex vs. transactional), sales-cycle length, sales channel (inside/outside), territory ramp-state (new/established), and target prospect tier (pre-qualified, semi-qualified, cold)"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document set — reads user-provided situation brief; writes prospecting-objective-plan-{date}.md to the working directory"
discovery:
  goal: "Determine the correct primary, secondary, and tertiary prospecting objective for the rep's specific situation and produce a written Objective Call Plan covering each prospect tier in their upcoming prospecting block"
  tasks:
    - "Gather the rep's sale complexity, channel type, prospect qualification level, territory ramp-state, and buying-window status"
    - "Apply the six-scenario decision framework to map situation to primary/secondary/tertiary objectives"
    - "Where needed, apply the qualify-first vs. appointment-first decision test"
    - "Produce a prospect-tier decision matrix (Primary / Secondary / Tertiary per tier)"
    - "Write prospecting-objective-plan-{date}.md as the block planning artifact"
  audience:
    roles: [sdr, bdr, ae, inside-sales-rep, outside-sales-rep, founder-self-seller]
    experience: beginner-to-intermediate
  triggers:
    - "Rep is about to run a prospecting block and wants every touch to have a defined target"
    - "Rep is confused about whether to go for appointment vs. close vs. qualification on their next call"
    - "Rep has a new territory or new product and wants to know where to start"
    - "Rep's pipeline is stagnant because they are chasing unqualified prospects without a defined objective strategy"
    - "Manager is asking the team to align their prospecting objectives to sale type and channel"
  prerequisites: []
  not_for:
    - "Writing the actual call script or email copy — use fanatical-prospecting:cold-call-opener-builder"
    - "Turning around objections and push-backs once the call is in progress — use fanatical-prospecting:prospecting-rbo-turnaround"
    - "Prioritizing which prospects to call first — use fanatical-prospecting:prospect-prioritization-pyramid"
    - "Calculating how many prospecting touches are needed to hit quota — use fanatical-prospecting:pipeline-ratio-calculator"
  environment: "Document set — reads situation brief from working directory or user input; writes Objective Call Plan"
  quality: placeholder
---

# Prospecting Objective Setter

## When to Use

You are setting up a prospecting block — a phone block, an email session, a LinkedIn outreach push, or an in-person field day — and you need to answer one fundamental question before the first touch:

**What am I trying to get from this contact right now?**

This skill applies the Four Objectives framework to your specific situation and produces a written Objective Call Plan. Every touch in your block gets a defined primary objective, so you know exactly what to ask for — and when to stop.

**Who this skill is for:** SDRs, BDRs, inside sales reps, outside sales reps, and AEs who run outbound prospecting as part of their daily work. Especially valuable for reps in new territories, reps whose pipeline is full of unqualified prospects, and any rep who has been "winging it" and wondering why activity doesn't convert.

**Output:** `prospecting-objective-plan-{date}.md` — a decision matrix with Primary / Secondary / Tertiary objectives per prospect tier, plus a one-line objective statement for each touch type in the upcoming block.

---

## Context & Input Gathering

### Required

To apply the framework accurately, the skill needs:

1. **Sale complexity:** Is your product/service complex, high-risk, or high-cost — or transactional, low-risk, low-cost?
2. **Sales channel:** Are you inside sales (phone/email/social, no in-person), outside sales with in-person prospecting, or outside sales using remote channels only?
3. **Prospect qualification state:** Are your prospects pre-qualified (you know the decision maker, the buying window, and the budget), semi-qualified (some information but gaps), or cold (little to no information)?
4. **Territory or account ramp-state:** Are you new to this territory/product/startup, or established?
5. **Buying-window awareness:** Do you know when your prospects can actually buy — contract expiration dates, budgetary periods, trigger events — or is this unknown?

### Useful (read from working directory if available)

- **`icp.md`** — Ideal customer profile: decision-maker roles, account size thresholds, buying trigger criteria
- **`prospect-list.csv`** — CRM export with qualification tier if tagged
- **`account-notes.md`** — per-account buying-window and stakeholder data

### Defaults

If no documents are provided, the skill asks the rep directly for the five inputs above. A two-to-three sentence verbal description of the selling situation is sufficient to begin.

### Sufficiency threshold

Sale complexity + channel type together determine the primary objective for the majority of scenarios. All five inputs sharpen the full decision matrix. If the rep is genuinely unsure about their sale complexity, the skill will apply the qualify-first vs. appointment-first decision test (Step 3) to resolve it.

---

## Process

### Step 1: Classify Sale Type and Channel

**Action:** Using the provided situation brief, classify the rep's situation on two axes:

**Sale type:**
- Complex / high-risk / high-cost: long sales cycles, multiple stakeholders, contractual obligations, high-level decision making, defined budgetary periods — typical of enterprise SaaS, capital equipment, professional services, major accounts
- Transactional / low-risk / low-cost: single decision maker or consistent decision-maker role, no set budgetary period, non-contractual or low-exclusivity, high probability most prospects are buyers — typical of SMB software, consumables, lower-ticket professional services

**Channel:**
- Inside sales: phone, email, text, social — no in-person prospecting
- Outside sales, remote channel: phone, email, text, social to prospects the rep will also see in person
- Outside sales, in-person: physically knocking on doors or attending venues where prospects are present

**WHY:** Sale type and channel are the two primary inputs to the Four Objectives framework. The same product can have different primary objectives depending on channel (outside sales in-person → close; outside sales via phone → appointment). Classifying these first eliminates the majority of ambiguity before the nuanced scenario rules are applied.

**Output:** A two-word classification: e.g., "Complex / Inside Sales" or "Transactional / Outside Sales (Remote)".

---

### Step 2: Apply the Six-Scenario Framework

**Action:** Map the rep's situation to one or more of the six decision scenarios. Each scenario specifies the Primary (P), Secondary (S), and Tertiary (T) objective:

**Scenario 1 — Complex / high-risk / high-cost product (any channel)**
- P: Set an appointment with a qualified decision maker, influencer, or stakeholder
- S: Gather information and qualify
- T: Build familiarity
- *Logic: A single call cannot close a complex sale. The appointment is the only outcome that advances the deal. Gathering information is secondary because qualifying before spending time on deep discovery prevents chasing unqualified deals.*

**Scenario 2 — Transactional / low-risk / low-cost + inside sales (phone/remote)**
- P: Close the sale on the spot
- S: Gather information and qualify
- *Logic: The channel (phone) and the sale type (transactional) together create the conditions for a one-call close. Closing on the spot is more efficient than setting a separate appointment.*

**Scenario 3a — Transactional / low-risk / low-cost + outside sales, remote channel (phone/email/text/social)**
- P: Set an appointment
- S: Gather information and qualify
- *Logic: Outside reps use phone/email as a booking tool, not a closing tool. The actual close happens in person.*

**Scenario 3b — Transactional / low-risk / low-cost + outside sales, in-person**
- P: Close the sale on the spot
- *Logic: In-person contact with a transactional product — the highest-probability close situation. Do not book an appointment when you are already standing in front of the buyer.*

**Scenario 4 — Highly qualified CRM database (prospects known, buying window opening)**
- P: Set appointments as the buying window opens
- S: Build familiarity (to increase engagement probability when the buying window opens)
- *Logic: You have already qualified these prospects. The remaining work is timing — being in front of them when they are ready to buy. Familiarity drives the response rate that makes appointment-setting possible.*

**Scenario 5 — Contract/budget-gated product (buying windows are locked to specific periods)**
- P: Gather information to qualify the buying window (contract expiry, budgetary period)
- S: Build familiarity
- *Then, once buying window is identified:* shift primary to Set an Appointment
- *Logic: There is no point setting an appointment — or closing — with a prospect who contractually cannot buy. The buying window qualification must come first. Once it is known, the objective shifts immediately to appointment-setting.*

**Scenario 6 — New territory, new startup, or new division**
- P: Gather information (identify decision makers, qualify buying windows and budgets)
- S: Build familiarity
- *Logic: Without data on who the right people are and when they can buy, all other objectives are premature. Data-gathering builds the foundation every other objective depends on.*

**WHY:** These six scenarios cover the vast majority of prospecting situations a rep encounters. The framework prevents the most common failure mode: reps who default to appointment-setting regardless of context (e.g., trying to book appointments with contract-locked prospects) or who gather information indefinitely without ever shifting to appointment-setting once qualification is complete.

**Output:** Identify which scenario(s) apply to the rep's situation. Note that a single rep may have different scenarios active simultaneously across different prospect tiers.

---

### Step 3: Apply the Qualify-First vs. Appointment-First Decision Test (if needed)

**Action:** If the rep is selling a complex product and is uncertain whether to qualify prospects before booking appointments or simply book all appointments and qualify in the meeting, apply this test:

**Set the appointment regardless of qualification level (appointment-first) when all four conditions are true:**
1. Product or service is non-contractual (no exclusivity lock-in)
2. High probability that most prospects are buyers — the product is something most prospects use consistently
3. No defined budgetary period — purchases can happen anytime
4. Decision-maker role is consistent and typically a single person

**Qualify first, then set the appointment when any of the following are true:**
- Product or service is complex or contractual (especially exclusive-vendor contracts)
- Sales cycle is long
- Decision making happens at a high organizational level
- There is a defined budgetary period
- Budgets require advance approval

**WHY:** Some sales trainers advocate setting appointments with every prospect regardless of qualification, reasoning that qualification should happen in the meeting. This is valid when the conditions above are met — but it creates waste when the product is contractual, the budgetary period is fixed, or the decision-maker is not a consistent single role. Blount's position: qualify first when unqualified meetings are expensive (travel, multi-stakeholder preparation, long sales cycle). Set appointments universally when meetings are cheap (inside sales, transactional product, consistent DM).

**Output:** A one-line decision: "Qualify before setting appointments" or "Set appointments, qualify in meeting" — with the condition that triggered the decision.

---

### Step 4: Define the Strike Zone

**Action:** Before completing the Objective Call Plan, verify that the rep has defined (or can define) the qualification criteria that separate a prospect worth pursuing from one that should be eliminated or deprioritized. These are the "strike zone" criteria:

- Decision-maker roles for this product/service
- Account size or revenue threshold (too small / too large)
- Buying-window indicators: contract expiration timing, trigger events, budgetary periods
- Competitors or exclusion criteria (contracts with a competitor that prevent purchase)
- Industry verticals or geographic zones relevant to this territory

If these criteria are not yet defined, prompt the rep to identify them before the prospecting block. Chasing prospects outside the strike zone is the primary cause of low conversion and wasted time.

**WHY:** Qualification criteria define which prospecting calls are worth making. Without them, reps swing at every pitch — including the ones that will never close. Blount's baseball analogy is explicit: "Don't swing at nothin' ugly." The strike zone is the filter that makes every other objective decision meaningful.

**Output:** A brief strike-zone checklist embedded in the Objective Call Plan.

---

### Step 5: Build the Prospect-Tier Decision Matrix and Write the Objective Call Plan

**Action:** Segment the rep's prospect base into tiers (based on the qualification data available), then assign Primary / Secondary / Tertiary objectives to each tier. Write `prospecting-objective-plan-{date}.md`.

Apply the familiarity touch-count reference when setting expectations for build-familiarity objectives:

| Prospect Familiarity Level | Expected Touches to Engage |
|---|---|
| Inactive customer (knows you, no recent contact) | 1–3 touches |
| Prospect in buying window, familiar with you/brand | 1–5 touches |
| Prospect familiar with brand, NOT in buying window | 3–10 touches |
| Warm inbound lead | 5–12 touches |
| Prospect with some familiarity, buying-window uncertain | 5–20 touches |
| Cold prospect, no familiarity | 20–50 touches |

Use these benchmarks to set realistic expectations: a cold-prospect objective of "set an appointment" on the first touch will fail at high rates. Familiarity must be built over multiple touches before appointment-setting becomes productive.

**WHY:** The objective plan is the operational artifact. Without writing it down, reps default to their comfort channel and habitual ask regardless of what the framework says. A written plan also makes prospecting blocks faster to execute — the rep knows before touching the phone what they are trying to achieve on each tier, which eliminates hesitation and frees cognitive capacity for the call itself.

---

## Output Template

```markdown
# Prospecting Objective Plan
**Date:** [Date]
**Rep:** [Name]
**Block type:** [Phone / Email / LinkedIn / In-person / Mixed]
**Prepared by:** fanatical-prospecting:prospecting-objective-setter

---

## Situation Classification

- **Sale type:** [Complex / high-cost OR Transactional / low-cost]
- **Channel:** [Inside sales / Outside sales (remote) / Outside sales (in-person)]
- **Territory state:** [New / Established]
- **Qualify-first decision:** [Qualify before setting appointments / Set appointments, qualify in meeting]
- **Active scenario(s):** [Scenario 1 / 2 / 3a / 3b / 4 / 5 / 6 from framework]

---

## Strike Zone

| Criterion | Qualifier |
|---|---|
| Decision-maker role(s) | [e.g., VP of Operations, Procurement Manager] |
| Account size | [e.g., 50–500 employees] |
| Buying-window trigger | [e.g., contract expiry within 6 months, new office opening] |
| Exclusions | [e.g., locked into Competitor X for 18+ months] |
| Geographic / vertical filter | [e.g., manufacturing sector, Midwest territory] |

---

## Prospect-Tier Objective Matrix

| Prospect Tier | Qualification State | Primary Objective | Secondary Objective | Tertiary Objective |
|---|---|---|---|---|
| Tier A — Fully qualified, in buying window | Decision maker known, budget confirmed, contract expiry imminent | Set appointment | Build familiarity | — |
| Tier B — Qualified, NOT in buying window | Decision maker known, buying window 6–18 months out | Build familiarity | Gather information (refine window timing) | — |
| Tier C — Semi-qualified | Some contact data, DM role uncertain or incomplete | Gather information and qualify | Build familiarity | — |
| Tier D — Cold | Little or no data | Gather information and qualify | Build familiarity | — |
| Tier E — Bogus / out-of-scope | Out of business, too small, wrong industry | Eliminate | — | — |

*Customize tiers to match your actual CRM segmentation or prospect list.*

---

## Per-Touch Objective Statement

For each touch type in this block, the ask is:

| Touch Type | Prospect Tier | Primary Ask |
|---|---|---|
| Outbound phone call | Tier A | "I'd like to schedule [X] on [specific date/time]" |
| Outbound phone call | Tier C/D | "Can you help me understand who handles [X] and when your next review cycle is?" |
| Cold email | Tier A/B | Appointment request or familiarity-building content |
| Cold email | Tier C/D | Information-gathering or familiarity-building |
| LinkedIn / social | Any cold tier | Familiarity-building: connect, comment, engage — not a pitch |
| In-person (if outside sales, transactional) | Any | Close on the spot |

---

## Familiarity Benchmarks for This Block

Cold prospects (Tier D) in this block require an estimated **20–50 touches** before appointment-setting becomes productive. Set familiarity-building as the primary objective for these contacts and do not measure this block's success by appointment rates from cold prospects alone.

---

## Block Summary

**Total touches planned:** [N]
**Tier A (appointment-primary):** [N]
**Tier B (familiarity/nurture-primary):** [N]
**Tier C/D (info-gathering-primary):** [N]
**Expected appointment sets from this block:** [N — based on tier mix and historical conversion]
```

---

## Key Principles

**Every touch has exactly one primary objective.** Not "I'll see how it goes." Before each call, email, or social touch, the primary objective is defined and written. This is what separates a prospecting block from random activity.

**WHY:** Objective clarity makes you both efficient and effective. Efficient because you can group similar-objective touches into a single block (all appointment-setting calls together, all information-gathering calls together), moving faster with less context-switching. Effective because on each touch you know exactly what to ask for and how to bridge to the prospect's world to make them say yes.

**An appointment is only an appointment when it is on both calendars.** "Call me anytime," "just stop by," and "we'll connect soon" are not appointments. A confirmed date, time, and place (physical or virtual) with the prospect expecting your arrival — that is the only definition. Accepting ambiguous commitments as appointments inflates your pipeline with phantom meetings and destroys forecast accuracy.

**WHY:** A calendar invite that is not accepted is a wish, not a commitment. Blount's research shows that reps with 80% no-show rates almost universally have the same root cause: they accepted brush-offs as appointments. The stricter definition forces the rep to obtain a genuine commitment — which is harder to get but infinitely more valuable.

**Build familiarity is a legitimate primary objective — and the only path through a cold prospect.** Reps who set appointments as the universal objective for cold prospects fail because they are ignoring the touch-count reality. A cold prospect who does not know you or your brand requires 20–50 touches before they will reliably engage. Familiarity-building as a deliberate objective — through voicemail, email, LinkedIn engagement, conference presence — systematically reduces that number over time.

**WHY:** Each voicemail they hear, each email they see, each LinkedIn interaction incrementally increases the probability of engagement on the next touch. Treating familiarity-building as a waste of time produces reps who make 20 cold calls, get no appointments, and conclude that prospecting "doesn't work." Treating it as a named objective produces reps who run Strategic Prospecting Campaigns (SPCs) that convert cold prospects into warm ones over 60–90 day cycles.

**Qualify first when unqualified meetings are expensive.** The cost of a wasted appointment varies by product and channel. For an inside sales rep with a transactional product, a bad appointment costs 20 minutes. For a field rep selling capital equipment with a 6-month sales cycle, a bad appointment costs travel time, opportunity cost, multi-stakeholder preparation, and potentially a proposal. Qualification discipline scales with the cost of a wasted meeting.

---

## Examples

### Example 1: SDR Selling Enterprise HR Software (Complex / Inside Sales)

**Situation:** SDR at a mid-market HR tech company. Product: $80K/year platform requiring IT and HR sign-off. Inside sales only (no in-person). Prospect list: 200 companies sourced from ZoomInfo, ~40% have no CRM contact data.

**Framework application:**
- Sale type: Complex / high-cost → Scenario 1
- Channel: Inside sales
- Result: P = Set appointment (with qualified DM), S = Gather information, T = Build familiarity

**Objective matrix:**
- Fully qualified prospects (decision maker known, renewal coming): P = Set appointment
- Semi-qualified (HR Director name known, no IT contact): P = Gather information (identify IT stakeholder), S = Set appointment if HR director is available
- Cold (company only, no contact): P = Gather information (find HR Director), S = Build familiarity

**Key decision:** Because the product is contractual (annual commitment, IT + HR approval), qualify first — do not set appointments with contacts who cannot actually influence the purchase.

---

### Example 2: Outside Sales Rep Selling Janitorial Supplies (Transactional / Outside Sales)

**Situation:** Field rep covering a new territory. Product: consumable, $300–2,000/quarter per account. Prospects include office buildings, manufacturing plants, and retail chains. Mix of in-person cold calls and phone follow-ups.

**Framework application:**
- Sale type: Transactional / low-cost → Scenarios 3a and 3b
- Channel: Outside sales (in-person + remote)
- Territory state: New → Scenario 6 also active

**Objective matrix:**
- In-person cold call at a business: P = Close the sale on the spot (Scenario 3b)
- Phone outreach to businesses not yet visited: P = Set appointment for in-person visit (Scenario 3a)
- All contacts in new territory: P = Gather information (who orders supplies, how much, current vendor) — Scenario 6 applies until baseline data exists

**Key decision:** For new territory calls, even in-person, the rep may need to gather information (find the right buyer) before attempting a close. Scenario 6 takes priority for the first 60 days until a functional prospect list is built.

---

### Example 3: AE Selling Benefits Brokerage (Contract-Gated / Inside Sales)

**Situation:** AE at a benefits brokerage firm. Prospects renew benefits packages annually — typically in Q4 for a Jan 1 effective date. Switching is rare outside the renewal window due to carrier contracts.

**Framework application:**
- Sale type: Complex + contract-gated → Scenarios 1 and 5 both apply
- Buying window: Locked to Q4 renewal cycle

**Objective matrix (by quarter):**
- Q1–Q2 (far from renewal): P = Gather information (identify renewal date, current broker, decision maker), S = Build familiarity
- Q3 (renewal approaching): P = Set appointment (pre-renewal discovery meeting), S = Gather information (refine needs, stakeholders)
- Q4 (renewal window open): P = Set appointment / close — highest activity period

**Key decision:** Do not attempt to set appointments with prospects in Q1 whose renewal is in Q4. It wastes the rep's time and strains the relationship. The buying window qualification must come first. Once the window is identified, shift immediately to appointment-setting.

---

## References

| File | Contents |
|---|---|
| `references/four-objectives-decision-matrix.md` | Full six-scenario reference table with qualifying conditions, objective assignments, and the qualify-first vs. appointment-first decision checklist |
| `references/familiarity-touch-counts.md` | Touch-count benchmarks by familiarity level; Strategic Prospecting Campaign (SPC) design guidance for cold-to-warm conversion |

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fanatical Prospecting by Jeb Blount (Ch. 9).

## Related BookForge Skills

For prioritizing which prospects to call first within your tiers:
```
clawhub install bookforge-prospect-prioritization-pyramid
```

For writing the actual call opener once your objective is set:
```
clawhub install bookforge-cold-call-opener-builder
```

For handling push-back once the call is in progress:
```
clawhub install bookforge-prospecting-rbo-turnaround
```

For calculating how many touches are needed to hit pipeline targets:
```
clawhub install bookforge-pipeline-ratio-calculator
```

Browse the full Fanatical Prospecting skill set: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
