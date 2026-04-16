---
name: in-person-prospecting-route-planner
description: Plan a Hub-and-Spoke in-person prospecting route for a field sales day — mapping drop-by prospect visits around preset appointments to eliminate random driving and maximize face-to-face touches. Use this skill when planning in-person prospecting, field sales route, territory routing, door to door sales, drop-by visits, hub and spoke territory, T-call technique, cold in-person visit, outside sales route, in-person prospecting calls, field rep territory planning, IPP route, mapping prospects around appointments, drop-in sales calls, walking your territory, outside sales day planning, maximizing field time, face-to-face prospecting plan, or when a rep says "I'm just going to drive around my territory today" (which is exactly the anti-pattern this skill prevents). Takes a field rep's preset appointments, prospect list with addresses, and available driving time, then produces a Hub-and-Spoke 5-step territory routing plan, a per-stop action plan with opener scripts, and T-call technique instructions for opportunistic walk-ins.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/in-person-prospecting-route-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting"
    authors: ["Jeb Blount"]
    chapters: [18]
tags: [sales, prospecting, field-sales, territory-management, in-person, sdr, bdr]
depends-on: [prospect-list-tiering, prospecting-objective-setter]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Territory map/prospect list with addresses, scheduled appointments for the day, and daily available driving time"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document/map directory"
discovery:
  goal: "Produce a Hub-and-Spoke daily route plan — hubs from preset appointments, spokes from nearby prospects — with per-stop opener scripts and T-call instructions"
  tasks:
    - "Identify hubs (preset appointments) for the day"
    - "Search prospect list by proximity to each hub to build spokes (3-5 per hub)"
    - "Classify each spoke prospect by tier to assign the correct objective"
    - "Sequence stops by geography to minimize windshield time"
    - "Draft in-person opener scripts and T-call technique instructions"
    - "Produce a route sheet with time blocks and per-stop action plan"
  audience:
    roles: [outside-sales-rep, field-ae, territory-manager, account-manager]
    experience: beginner-to-intermediate
  triggers:
    - "in-person prospecting"
    - "field sales route"
    - "territory routing"
    - "door to door sales"
    - "drop-by visits"
    - "hub and spoke territory"
    - "T-call technique"
    - "cold in-person visit"
    - "outside sales route"
    - "planning my field day"
    - "driving around my territory"
  prerequisites:
    - "prospect-list-tiering — to have a tiered prospect list with addresses"
    - "prospecting-objective-setter — to have defined the correct objective per tier before walking in"
  not_for:
    - "Inside sales reps who do not make in-person calls"
    - "Account management visits to existing customers (no prospecting element)"
    - "Writing phone or email scripts — use prospecting-message-crafter"
    - "Calculating how many calls are needed to hit quota — use prospecting-ratio-manager"
  environment: "Directory containing prospect list file (CSV or markdown) with address fields, plus appointment calendar data (pasted or in a file)"
  quality:
    required_outputs: ["route-sheet.md"]
    completeness: "Every stop must have: address, prospect tier, call objective, opener script snippet, estimated time allocation"
---

# In-Person Prospecting Route Planner

## When to Use

You are a field sales rep or outside sales representative with a day of in-person activity ahead. You have one or more preset appointments on your calendar, a list of prospects in your territory, and a finite amount of driving time. The question is: how do you fill every available minute between appointments with purposeful prospecting calls — without burning the day aimlessly driving from one random stop to the next?

This skill applies the Hub-and-Spoke territory routing system to turn your preset appointments into anchors, then maps the most geographically efficient set of drop-by prospect visits around each one. The result is a single-page route sheet you can execute with confidence.

**Who this skill is for:** Outside sales reps, field AEs, territory managers, and account managers whose role includes in-person prospecting as part of a balanced prospecting approach. Works for both B2B reps calling on businesses and reps managing geographic territories (industrial parks, food service districts, healthcare corridors, retail strips).

**When NOT to use this skill:**
- You have no preset appointments (the whole system depends on hubs — if you have none, set phone appointments first, then run this skill)
- You are doing account management visits with no prospecting component
- You are an inside sales rep with no field activity

**Output:** `route-sheet-{date}.md` — a sequenced list of stops with map-order addresses, tier/objective per stop, opener script snippets, and T-call reminders.

---

## Context and Input Gathering

### Required Inputs

**Preset appointments for the day:**
- Company name, address, and estimated duration for each scheduled meeting
- Look for: `appointments.md`, `calendar-export.csv`, or ask: "What appointments do you have confirmed on your calendar today? Give me the company name, address, and how long each meeting is expected to run."

**Prospect list with addresses:**
- A list of prospects in the territory with physical addresses (or at minimum zip codes)
- Look for: `prospect-list.csv`, `territory-accounts.csv`, any `.csv` with address/zip fields
- If using the `prospect-list-tiering` skill output: look for `tiered-prospect-list.md`
- If missing: ask: "Can you share your territory prospect list? I need company names and addresses (or zip codes) to map spokes around your appointments."

**Daily available driving time:**
- Total hours available for field prospecting (subtract appointment durations and commute)
- If not stated: ask: "How many hours do you have available today for field calls, accounting for your scheduled appointments?"

### Useful Inputs

**Tier assignments from prospect-list-tiering:** If already tiered, read `tiered-prospect-list.md` to inherit tier labels and use them to assign call objectives per stop.

**CRM notes or account research files:** Per-account notes (decision-maker names, LinkedIn profiles, previous call history) enable personalized opener scripts. Look for: `account-notes/`, individual company markdown files, or CRM export fields like `Last Activity`, `Decision Maker`, `Notes`.

**Objective call plan from prospecting-objective-setter:** If already created, read `prospecting-objective-plan-{date}.md` to confirm the correct primary/secondary objective per prospect tier before assigning per-stop actions.

### Default Assumptions

- If no tier assignments exist: treat all drop-by prospects as semi-qualified (use "gather information" as the primary objective)
- If no CRM notes are available: use the prospect's website and LinkedIn profile to prepare a personalized approach before each stop
- If available driving time is not stated: assume a standard 8-hour field day minus appointment time
- If only zip codes are available (no street addresses): use zip-code proximity to hub appointments as the spoke selection criteria

### Sufficiency Threshold

```
SUFFICIENT when:
- At least one preset appointment (hub) exists for the day
- A prospect list with at minimum zip codes is available
- Daily available hours are known or can be estimated

NOT sufficient — ask for more before proceeding:
- No appointments at all (advise running a phone block first to set hubs)
- No prospect list with any location data
```

---

## Process

### Step 1: Identify the Day's Hubs

**Action:** List every preset appointment confirmed for the day. For each hub, record:
- Company name and full address
- Appointment time window (start + estimated end)
- Buffer availability: how much time is free before and after (30–60 minutes is ideal for spoke calls)

Arrange hubs in chronological order. These are the fixed anchors around which the entire day is built.

**Why:** In-person prospecting is the least time-efficient prospecting channel. A rep who drives randomly can spend 80% of their day behind the wheel and make fewer than 10 calls. The hub anchors the rep's geography — every other stop flows from the hub's location rather than from a random pick off the list. Kelly, a top rental uniform rep, sets 2–3 phone appointments first every morning precisely so he has fixed hubs to map around. Without hubs, the hub-and-spoke system collapses into an aimless drive.

**Output:** A numbered hub list with addresses and time blocks, e.g.:
```
Hub 1 — Acme Manufacturing, 123 Industrial Dr, Springfield | 9:00–10:00 AM | Buffer: 30 min before, 45 min after
Hub 2 — Riverside Services, 450 Commerce Blvd, Riverside | 1:00–2:00 PM | Buffer: 45 min before, 60 min after
```

---

### Step 2: Build Spokes — Nearby Prospects Around Each Hub

**Action:** For each hub, search the prospect list for 3–5 prospects whose addresses are geographically close. Use zip code proximity as the primary filter when no mapping tool is available:
1. Identify the hub's zip code
2. Filter the prospect list for matching or adjacent zip codes
3. If the list includes full addresses, look for same street, same industrial park, or same business district
4. Select 3–5 prospects per hub (do not exceed 5 — more spoke candidates than that creates route complexity and over-commitment)

Assign each spoke to its nearest hub. If a prospect could belong to two hubs, assign it to the hub with more available buffer time.

**Why:** Geographic clustering is the engine behind the volume numbers that make in-person prospecting worthwhile. Kasey, a restaurant supply rep, maps 3–5 prospects around each of her 4 daily account visits, producing 15–20 in-person prospecting touches per day — and opened more new accounts than any account manager in her company. Without geographic clustering, that same rep might make 4–6 calls total. The spoke selection is not about choosing the "best" prospects first — it is about choosing the most geographically proximate ones from within your prioritized tiers.

**Note on tier priority within spokes:** If you have already run `prospect-list-tiering`, prefer higher-tier prospects (Tier 4 Conquest and Tier 6 In Buying Window) when multiple geographically similar options exist. But never extend driving time significantly to reach a higher-tier prospect over a closer lower-tier one — geography governs the spoke, tier governs the objective.

**Output:** A spoke list per hub, e.g.:
```
Hub 1 spokes:
  - Spoke 1A: Midwest Textiles, 145 Industrial Dr (same park) | Tier 4 Conquest
  - Spoke 1B: Springfield Fabrication, 200 Industrial Dr | Tier 2
  - Spoke 1C: Crown Packaging, 78 Mill Rd (adjacent) | Tier 2
```

---

### Step 3: Classify Each Spoke and Assign Call Objectives

**Action:** For each spoke prospect, assign:
1. **Tier** (from `prospect-list-tiering` output, or assign manually using basic criteria)
2. **Primary objective** for this stop (from `prospecting-objective-setter` logic or the defaults below)
3. **Carry-to-close readiness:** Confirm whether you have close materials with you (order forms, contracts, sample materials, presentation deck) in case the stop converts to an immediate sales conversation

**Default objective assignments by tier:**

| Tier | Name | In-Person Primary Objective |
|------|------|-----------------------------|
| T6 | In Buying Window | Attempt close or set appointment for formal presentation |
| T5 | Hot Inbound / Referral | Set appointment or close on the spot |
| T4 | Conquest | Build familiarity + gather decision-maker intelligence |
| T3 | Buying Window Identified | Build familiarity + confirm buying window timeline |
| T2 | Basic Data Confirmed | Gather qualifying information — decision-maker name, competitive info, budget cycle |
| T1 | Unknown | Gather basic qualifying data — confirm decision-maker role, business type, size estimate |

**Why:** Walking into a prospect without a defined objective is the single fastest way to waste an in-person call. Carl, a business services rep, once walked into a prospect who was ready to close on the spot — but Carl was unprepared to present. The prospect signed with a competitor two weeks later. The objective, assigned before you walk in the door, determines what you ask for, what you carry in, and when you stop the conversation. An underprepared rep in front of a ready buyer is a more costly mistake than a well-prepared rep in front of a cold prospect.

**Output:** An annotated spoke list with tier + objective + carry-in materials check, e.g.:
```
Spoke 1A: Midwest Textiles | T4 Conquest | Objective: Build familiarity, get decision-maker name on record | Materials: business card, one-pager
Spoke 1B: Springfield Fabrication | T2 | Objective: Gather info — who handles uniform purchasing, current vendor | Materials: business card
```

---

### Step 4: Build the Opener Scripts and T-Call Technique

**Action:** For each planned spoke stop, draft a 2–3 sentence opener. For every hub visit, add a T-call reminder.

**In-Person Opener Script Template:**
```
"Hi, my name is [Your Name], I'm with [Company].
The reason I stopped by is [transparent, specific reason — leverage nearby customer, recent trigger, or relevant service].
I wanted to [primary objective: introduce myself / ask [Decision Maker] a couple of quick questions / see if there's a fit]."
```

**Opener examples by situation:**

*Neighbor leverage (most effective):*
"Hi, my name is [Name], I'm with [Company]. We've been working with [Customer Next Door] for three years — they introduced us to some of the other businesses in this park. I wanted to stop in and introduce myself to [Decision Maker] and ask a couple of quick questions about how you handle [relevant need]."

*Research-personalized:*
"Hi, I'm [Name] from [Company]. I noticed on your LinkedIn page that you recently [relevant event — expansion, new hire, new location]. We work with companies going through exactly that kind of growth. I wanted to ask [DM name] a quick question about your current [relevant area]."

*Cold walk-in (no prior research):*
"Hi, my name is [Name], I'm with [Company]. The reason I stopped in is I provide [service/product] to several businesses in this area and I wanted to learn more about your company and situation to see whether working together might be a good fit."

**What to avoid in all openers:**
- Tricks designed to mislead the gatekeeper about your purpose
- Claiming to be "just dropping something off" when you are not
- Pitching your product in the opener — gather first, pitch when invited

**T-Call Technique:**
After every hub appointment (and every spoke stop), before returning to your car: look left, look right, look behind you. Any business you have not visited that is visible from where you stand is a T-call candidate. Walk in. Use the cold walk-in opener above. T-calls are by definition unplanned — you have not done pre-research — so keep the opener simple, the objective tight (gather DM name and basic qualifier), and log everything before you drive away.

**Why:** Gatekeepers and receptionists are not obstacles — they are information sources and future allies. A rep who is transparent ("I stopped by to see if there's a fit") earns more goodwill than a rep who uses deception. Blount is explicit: "You are a professional, so be straightforward and transparent about your purpose for being there. Never use cheesy lines designed to trick gatekeepers." T-calls convert the time between hub and spoke into additional prospecting volume with zero pre-planning overhead. Kelly generates 10–20 face-to-face touches daily using T-calls as the fill layer on top of planned spokes.

**Output:** Opener scripts embedded in the route sheet per stop, plus a T-call reminder block after each hub.

---

### Step 5: Produce the Route Sheet and Time Blocks

**Action:** Assemble all hubs and spokes into a single sequenced route sheet, ordered by the most geographically efficient driving sequence (not by tier priority — geography governs sequencing). Write the output to `route-sheet-{date}.md`.

**Route sheet structure per time block:**
```
## Time Block 1: [HH:MM – HH:MM]

### Hub: [Company Name]
- Address: [Full address]
- Appointment: [Start] – [End]
- Carry in: [What you need for this meeting]

### Spoke 1A: [Company Name]
- Address: [Full address]
- Tier: [T1–T6] | Objective: [Primary objective]
- Opener: "[Opener script text]"
- Time allocation: 10–15 min
- Materials to carry: [List]

### Spoke 1B: [Company Name]
...

### T-Call Zone: After Hub 1 appointment
- Look left, right, behind. Walk into any visible business not on your list.
- Objective: Gather DM name + one qualifying fact
- Log before leaving the parking lot

---
```

**Time allocation guidelines:**
- Hub appointment: per calendar entry
- Planned spoke (T1–T3): 10–15 minutes
- Planned spoke (T4–T6): 15–25 minutes (more time if buying window is open)
- T-call (unplanned): 5–10 minutes
- Between-stop driving: 3–7 minutes within same industrial park/district; 10–15 minutes between geographic clusters
- CRM logging at end of day: 15–30 minutes — non-negotiable

**Why:** A sequenced route sheet eliminates the "what do I do next" decision cost that eats into field time. The rep leaves the car with a defined next action, re-enters with a complete record of what happened, logs it in the CRM, and drives to the next stop. Without this structure, reps waste time deciding, double-back on geography, and skip logging — which means the day's prospecting produces zero lasting database value. The route sheet is also the artifact that proves the day was productive: every stop has an outcome logged.

**Final step — CRM logging reminder:** Before leaving the last stop of the day (or on-the-spot after each call if time allows), log every stop: outcome, decision-maker name confirmed/not confirmed, next action, follow-up task date. This converts face-to-face touches into database intelligence and pipeline entries.

**Output:** `route-sheet-{date}.md` with all time blocks, hubs, spokes, opener scripts, and T-call reminders.

---

## Inputs

| Input | Required | Format | Notes |
|-------|----------|--------|-------|
| Preset appointments | Yes | Calendar export, markdown list, or pasted text | Must include company name, address, time |
| Prospect list with addresses | Yes | CSV or markdown table | Zip code minimum; full address preferred |
| Daily available hours | Yes | Number or time range | Used to determine how many spokes are realistic |
| Tiered prospect list (from prospect-list-tiering) | Recommended | `tiered-prospect-list.md` | Enables tier-based objective assignment per spoke |
| Objective call plan (from prospecting-objective-setter) | Recommended | `prospecting-objective-plan-{date}.md` | Ensures correct primary objective per tier |
| Account notes / CRM export with DM names | Optional | Per-account markdown files or CSV | Enables personalized openers |

---

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `route-sheet-{date}.md` | Markdown | Sequenced stop list with hub/spoke structure, opener scripts, T-call reminders, time blocks, and CRM logging reminder |

---

## Key Principles

**Geographic sequence, not priority sequence.** The route is ordered by geography to minimize windshield time — not by tier priority. You may call on a Tier 2 prospect before a Tier 4 conquest account if the Tier 2 prospect is physically between your hub and the Tier 4. Tier priority governed which prospects made it onto the spoke list; geography governs the order you visit them.

**Never waste between-appointment time.** The interval between a hub appointment ending and the next hub starting is the most underutilized resource in field sales. Three to five spoke calls fit comfortably in a 45-minute window within the same industrial park or business district. The mindset shift: every minute not on the road or in a meeting is a prospecting opportunity.

**Familiarity builds through repeated geographic exposure.** A prospect who says no today recognizes your name on the phone next week. A gatekeeper who has seen your face twice is more likely to help you get to the decision maker on the third visit. In-person prospecting builds familiarity faster than any other channel because 80% of human communication is non-verbal. This is why Tier 4 (Conquest) accounts belong on the spoke list even when no buying window is open — every face-to-face touch advances the familiarity score.

**Always be prepared to close.** Even on a "gather information" call, carry your close materials — order forms, contracts, sample kit, or a demo device. You cannot predict when a decision maker will be present and ready. Carl's missed close (p. 224) is the permanent warning: "Sometimes you only get one chance with a prospect." The cost of carrying materials you do not use is zero. The cost of not having them when you need them is the deal.

**Respect the gatekeeper.** The receptionist is not an obstacle — she is an intelligence source, a future advocate, and a human being. Transparency ("I stopped by to see if there's a fit") builds goodwill that compounds over time. Deception burns the relationship permanently. The rep who goes in the back door claiming to be lost is the rep who never gets a warm introduction to the decision maker.

**T-calls are not optional.** Putting on your "sales goggles" — looking left, right, and behind after every appointment — is a trained behavior, not a personality trait. Every stop produces T-call candidates. The reps who make 10–20 daily in-person touches almost all report that T-calls account for 3–7 of those touches. T-calls also surface prospects who are not yet in the CRM database, which means they are otherwise invisible.

**In-person prospecting supplements, it does not replace, other channels.** On the best day, a field rep makes 15–20 in-person touches. A phone block can produce 25–50 contacts per hour. In-person prospecting is powerful for qualification, familiarity-building, and gatekeeper navigation — but it is not a substitute for the phone. The hub-and-spoke system makes in-person prospecting maximally efficient precisely so it can serve its role within a balanced prospecting cadence.

---

## Examples

### Example 1: B2B Outside Rep — Software for Industrial Businesses

**Situation:** Sarah sells equipment monitoring software to manufacturing and fabrication companies. She has two preset appointments in the same industrial corridor: 9:30 AM at Acme Machining and 1:00 PM at Crown Metal Works. She has a tiered prospect list with 40 accounts in the territory and 6 hours of field time.

**What the skill produces:**
- Hub 1: Acme Machining, 9:30–10:30 AM. Buffer: 45 min after.
  - Spoke 1A: Riverside Fabrication (same park, T4 Conquest) — Objective: build familiarity, confirm plant manager name
  - Spoke 1B: Midwest Precision Parts (same park, T2) — Objective: gather info, confirm decision-maker role
  - Spoke 1C: Atlas Components (2 blocks north, T2) — Objective: qualify — who handles software decisions?
  - T-call zone: 3 businesses visible from Acme parking lot, not in CRM
- Hub 2: Crown Metal Works, 1:00–2:00 PM. Buffer: 60 min after.
  - Spoke 2A–2D: 4 prospects within 1 mile on the same industrial road
  - T-call zone: adjoining business park

**Total planned stops:** 2 hubs + 7 spokes + estimated 4–6 T-calls = 13–15 face-to-face touches for the day.

---

### Example 2: Restaurant Supply Rep — Food Service District

**Situation:** Kasey sells restaurant supplies and is required to visit 4 existing accounts daily (these become her hubs). Her territory is a dense urban food service district — dozens of restaurants, delis, and catering companies within walking distance of her hub accounts.

**What the skill produces:**
- 4 hub accounts mapped chronologically across the district
- 3–5 prospects per hub drawn from her CRM by zip code and street proximity
- Opener script leverages her existing relationships: "We work with [nearby restaurant] — they mentioned you run a similar operation and suggested I stop by."
- T-calls in the same block: food trucks parked outside her hub accounts, new restaurant signage spotted during transit

**Total stops:** 4 hubs + ~16 planned spokes + T-calls = 20+ in-person touches per day (matching Kasey's actual reported daily volume from the source case study).

---

### Example 3: Rural Territory Rep — Low-Density Geography

**Situation:** Marcus sells pest control services to agricultural businesses in a rural territory. Appointments are spread 20–40 miles apart. He has 3 preset appointments and his prospect list has 80 accounts spread across a 3-county area.

**What the skill produces:**
- Hubs ordered on a geographic north-to-south route to minimize backtracking
- Spokes selected from prospects along the driving corridor between hubs (not by zip code, but by route proximity — flagged in the route sheet)
- T-call note: grain elevators, equipment dealers, and co-ops visible from main highways are prime T-call candidates even without a CRM record
- Time allocation adjusted: longer driving segments mean fewer spokes per hub (2–3 rather than 5), but total daily touches can still reach 10–12 with T-calls

**Key adaptation:** In low-density rural territories, "proximity" means along the driving route, not same-zip. The skill notes this and instructs the rep to use a highway map or route planner to identify prospects within a 5–10 minute detour off the direct path between hubs.

---

## References

Detailed script library (extended opener variations, RBO turnaround scripts for in-person push-back, gatekeeper navigation scripts): see `references/in-person-opener-scripts.md` (to be created if needed).

Route template (blank `route-sheet.md` template for reuse): see `references/route-sheet-template.md` (to be created if needed).

Source chapter: Blount, Jeb. *Fanatical Prospecting.* Wiley, 2015. Chapter 18: "In-Person Prospecting" (pp. 219–231).

T-call technique: pp. 220, 229.
Hub-and-Spoke five-step system: pp. 222–223.
Five-step in-person call process: pp. 226–228.
Preparation framework: pp. 225–226.
Kelly case study (rental uniform rep): pp. 219–220.
Kasey case study (restaurant supply rep): pp. 222–223.
Carl missed-close vignette: p. 224.

---

## Related BookForge Skills

Install the dependencies that feed into this skill:

```
clawhub install bookforge-prospect-list-tiering
```
Tier and prioritize your territory prospect list before building spokes. Output (`tiered-prospect-list.md`) is the primary spoke candidate source for this skill.

```
clawhub install bookforge-prospecting-objective-setter
```
Assign the correct primary/secondary/tertiary objective per prospect tier before your field day. Output (`prospecting-objective-plan-{date}.md`) drives per-stop objective assignments in the route sheet.

Coming soon:
```
clawhub install bookforge-gatekeeper-navigator
```
Handle in-person gatekeeper scenarios with specific response scripts for the receptionist block, the "he's not available" brush-off, and the warm handoff request.

Browse the full Fanatical Prospecting skill set: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)

---

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — BookForge Skills. Source framework: *Fanatical Prospecting* by Jeb Blount (Wiley, 2015).
