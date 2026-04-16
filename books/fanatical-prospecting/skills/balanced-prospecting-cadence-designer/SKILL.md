---
name: balanced-prospecting-cadence-designer
description: |
  Design a balanced multi-channel prospecting cadence that prevents single-channel-obsession — the career-limiting habit of defaulting to the one channel you are most comfortable with while avoiding the channels that generate friction. Use this skill when someone asks about "prospecting cadence", "channel mix", "balanced prospecting", "multi-channel outreach", "how much phone vs email", "sales sequence design", "cadence template", "which channels should I use", "prospecting strategy", "should I be doing more phone calls", "how to balance in-person and remote outreach", "what percent of my prospecting should be social", "I'm better in person than on the phone", "am I too dependent on email", "how to structure my outreach across channels", "mix of prospecting methods", "single channel prospecting problem", or "how to diversify my prospecting approach". This skill gathers the user's product, sales cycle length, territory type, quota state, territory tenure, and current channel habits — then produces three artifacts: (1) a recommended channel-mix with explicit percentages (e.g., 40% phone / 25% email / 20% social / 10% in-person / 5% text) tuned to the user's specific situation, (2) a day-by-day weekly cadence template with time slots assigned to each channel, and (3) an anti-pattern audit that checks for single-channel-obsession and the "I'm so much better at X" rationalization. Based on Chapters 3 and 4 of Fanatical Prospecting by Jeb Blount.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/balanced-prospecting-cadence-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting: The Ultimate Guide to Opening Sales Conversations and Filling the Pipeline by Leveraging Social Selling, Telephone, Email, Text, and Cold Calling"
    authors: ["Jeb Blount"]
    chapters: [3, 4]
tags: [sales, prospecting, cadence-design, multi-channel, sdr, bdr, sales-strategy]
depends-on: [prospecting-objective-setter, prospect-list-tiering, prospecting-time-block-planner]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "User's product or service description, sales cycle length, territory description (geographic density, industry vertical), prospect universe size, quota gap (on-target vs. behind), territory tenure (new/established), and current channel usage breakdown if known"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document directory — reads user-provided situation brief; writes balanced-prospecting-cadence-{date}.md to the working directory"
discovery:
  goal: "Produce a channel-mix recommendation with explicit percentages, a day-by-day weekly cadence template, and an anti-pattern audit identifying any single-channel-obsession patterns in the user's current approach"
  tasks:
    - "Profile the seller's situation across seven situational variables"
    - "Identify which channels are viable given the ICP and territory"
    - "Proportion the channel mix with explicit percentages adjusted to the situation"
    - "Design a Monday-through-Friday daily cadence template assigning each channel to time slots"
    - "Audit for single-channel-obsession and the 'I'm so much better at X' rationalization"
  audience:
    roles: [sdr, bdr, ae, inside-sales-rep, outside-sales-rep, founder-self-seller]
    experience: beginner-to-intermediate
  triggers:
    - "Rep is relying on one channel (usually email or social) and not hitting their number"
    - "Rep is new to a territory and needs to know how to distribute prospecting effort across channels"
    - "Rep says they are 'better at' one channel and is avoiding others"
    - "Manager wants to implement a structured multi-channel outreach standard across the team"
    - "Rep is transitioning from inside to outside sales (or vice versa) and needs a new channel mix"
    - "Rep's pipeline has dried up and they want to diagnose whether single-channel over-reliance is the cause"
  prerequisites: []
  not_for:
    - "Writing the actual call opener or email copy — use fanatical-prospecting:cold-call-opener-builder or cold-email-writer"
    - "Setting the objective for each individual touch — use fanatical-prospecting:prospecting-objective-setter"
    - "Prioritizing which specific prospects to call first — use fanatical-prospecting:prospect-list-tiering"
    - "Blocking and protecting the time for prospecting — use fanatical-prospecting:prospecting-time-block-planner"
    - "Calculating how many total touches are needed to hit quota — use fanatical-prospecting:prospecting-ratio-manager"
  environment: "Document set — reads situation brief from working directory or user input; writes cadence plan"
  quality: placeholder
---

# Balanced Prospecting Cadence Designer

## When to Use

You need to decide how to distribute your prospecting effort across channels — phone, email, social, text, in-person, and referral — and you want a concrete weekly cadence rather than a vague directive to "use multiple channels."

This skill applies the Balanced Prospecting methodology from Jeb Blount's *Fanatical Prospecting* to your specific situation: your product, your sales cycle, your territory, your quota state, and where you are in your territory tenure. It produces a channel mix with explicit percentages and a day-by-day cadence template you can execute starting Monday.

**The core problem this skill solves:** Single-channel obsession — the habit of defaulting to the one prospecting channel you are most comfortable with while rationalizing away the channels you find uncomfortable. As Blount states directly: "Putting all your prospecting eggs into a single basket is stupid. It's career suicide." The most common rationalization is "I'm so much better at X" — a phrase Blount identifies as a reliable predictor of underperformance.

**Who this skill is for:** SDRs, BDRs, inside sales reps, outside sales reps, AEs, and founder-sellers who run outbound prospecting. Especially valuable for reps whose pipeline has stalled despite feeling busy, reps moving into new territories, and reps who have become heavily dependent on one channel (usually email or social).

**Output:** `balanced-prospecting-cadence-{date}.md` — channel-mix percentages, daily cadence template (Monday–Friday), and anti-pattern audit.

**Dependency context:** This skill is upstream of the other planning skills in this set. Once the channel mix is designed here, use `prospecting-objective-setter` to set the right goal for each touch, `prospect-list-tiering` to decide which prospects get which channel treatment, and `prospecting-time-block-planner` to protect the time slots the cadence requires.

---

## Context & Input Gathering

### Required

To proportion the mix accurately, the skill needs:

1. **Product or service:** What are you selling? The nature of the product drives which channels are viable and which are the primary relationship-builders.
2. **Sales cycle length:** Days, weeks, or months? Short cycles favor phone-and-close channels; long cycles require relationship-building channels alongside appointment-setting ones.
3. **Territory description:** Industry vertical, geographic density (urban/suburban/rural), account size range, and the typical decision-maker role.
4. **Quota state:** Are you currently on target, ahead, or behind? A rep who is 30% behind quota needs a different channel intensity than one who is on pace.
5. **Territory tenure:** Are you new (less than 12 months in this territory), mid-tenure (1–3 years), or established (3+ years with a qualified database)?
6. **Current channel usage:** How are you spending your prospecting time today — even approximately? A rough breakdown by channel (or "mostly email, some LinkedIn, rarely phone") is enough.

### Useful (read from working directory if available)

- **`icp.md`** — Ideal customer profile for channel selection (e.g., if the ICP is a C-suite executive at a large enterprise, phone + LinkedIn + in-person outweigh cold email)
- **`prospect-list.csv`** — Geography and account-size distribution calibrates the in-person and density-driven channel weighting
- **`pipeline-ratios.csv`** — Historical activity-to-outcome rates by channel reveal which channels are already working and which are underutilized

### Defaults

If no documents are provided, the skill asks for the six inputs above. Two or three sentences per item is sufficient to start. If tenure or quota state is uncertain, the skill defaults to "new territory" and "on target" and flags the assumption for confirmation.

---

## Process

### Step 1: Profile the Seller's Situation

**Action:** Assess the user's situation across seven variables drawn from the Balanced Prospecting framework. For each variable, determine the directional signal it sends for channel weighting.

| Variable | What to assess | Channel signal |
|---|---|---|
| **Industry vertical** | What industries are the prospects in? | Some verticals require in-person; referral networks dominate others; trade shows deliver the highest-quality prospects in some |
| **Product or service type** | Consulting vs. software vs. physical product | Social selling heavier in consulting; inbound and email heavier in certain software categories |
| **Deal complexity** | Complex/contractual vs. transactional | Complex → phone + in-person dominate; transactional → email + phone often sufficient |
| **Company size and stage** | Large with existing database vs. startup building one | Large: phone + email most efficient; startup: must balance database-building (long-term) with pipeline-filling (short-term) |
| **Territory tenure** | New (< 12 mo) vs. mid (1–3 yr) vs. established (3+ yr) | New: heavy phone to build the database; established: referrals + social + timed calls to buying-window prospects become primary |
| **Geographic density** | High-density urban vs. suburban vs. rural/dispersed | High-density (downtown Manhattan, Chicago Loop): in-person more efficient than phone; rural/dispersed: phone and remote channels dominate |
| **Quota state** | On target vs. behind | Behind quota: increase phone intensity and in-person; ahead: can sustain current mix |

**WHY:** No single channel-mix formula works for every seller. Blount is explicit: "There isn't a one-size-fits-all formula for balanced prospecting. Every territory, industry, product, service, and prospect base is different." Profiling across all seven variables before prescribing a mix prevents the common error of copying another rep's cadence without accounting for situational differences — the specific failure mode of a new rep emulating a 20-year veteran whose database is already fully qualified.

**Output:** A one-paragraph situation summary that names the directional signals identified for each variable. This becomes the rationale for the channel-mix percentages in Step 3.

---

### Step 2: Identify Viable Channels for the ICP

**Action:** Determine which of the six prospecting channels are viable given the prospect's role, industry, and reachability. Not all channels are equally accessible for every ICP.

**The six channels:**

| Channel | Best when | Caution when |
|---|---|---|
| **Phone (outbound call)** | Decision maker has a direct line or reachable mobile; transactional or complex deal requiring conversation | Gatekeeper-heavy environments with no DM direct contact |
| **Email** | Prospect has a professional email address; deal requires time-to-think rather than immediate response; high-density prospect lists where one-to-one phone volume is impractical | Low open rates in spam-heavy industries; commoditized email reputation in the vertical |
| **Social (LinkedIn, etc.)** | Prospect is active on the platform; consulting/advisory sales where thought leadership drives trust; ICP title is well-represented on platform | Prospects in industries with low social adoption; executive titles who do not manage their own inboxes |
| **Text** | Prior familiarity has been established (prior call, email, in-person contact); short-cycle transactional products; field reps with a recurring customer base | Cold outreach to prospects who have never been contacted; violates familiarity threshold |
| **In-person** | High-density geography enables efficient territory routing; relationship-intensive industries; outside sales with established routes | Geographically dispersed territory; long drive times between prospects; inside sales model |
| **Referral** | Established relationship network; tenured territory with satisfied customers; high-trust industries | New rep with no network in the territory; startup with no customer base yet to source referrals from |

**WHY:** Proportioning a channel that is not viable for the ICP produces zero results regardless of how much time is allocated to it. A SaaS SDR calling mid-market ops directors does not need to account for in-person drop-ins; a uniform rental sales rep covering an industrial park should not be treating LinkedIn as a primary channel. Identifying viable channels first prevents wasted allocation.

**Output:** A named list of 3–5 viable channels for the user's ICP, with one-sentence notes on why each is viable or limited.

---

### Step 3: Proportion the Channel Mix

**Action:** Using the situation profile (Step 1) and viable channels (Step 2), assign a percentage of total prospecting time to each channel. The percentages should sum to 100% of prospecting activity time (excluding meetings, discovery calls, and closing activity).

**Reference starting mix (inside sales, complex deal, mid-tenure):**

| Channel | Starting % | Adjust up when | Adjust down when |
|---|---|---|---|
| Phone | 40% | Behind quota; new territory; transactional deal; high-density geography | Established tenure with qualified database; highly gatekeeper-heavy environment |
| Email | 25% | High-density prospect list; asynchronous-preferred ICP; deal requires time-to-think | Very warm territory where calls convert directly; email open rates below 15% |
| Social | 20% | Consulting/advisory sale; thought-leadership-driven ICP; mid-to-established tenure | Non-professional social users; industries with low LinkedIn adoption |
| In-person | 10% | High-density geography; relationship-intensive industry; outside sales territory | Geographically dispersed; inside sales model; long drive times |
| Text | 5% | Established familiarity with prospects; field rep recurring customer base | Cold territory; no prior contact established; legal or compliance restrictions |
| Referral (active ask) | 0–10% | Tenured rep with existing customers; high-NPS customer base | New rep; startup with no installed base |

The full channel-mix matrix with 12 scenario variants (enterprise SaaS, transactional SMB, field rep, consulting, startup, and others) is in `references/channel-mix-matrix.md`.

**WHY:** The percentage-based mix forces a concrete answer to the question that most prospecting plans leave vague: not "use multiple channels" but "40% of my prospecting time this week is phone, 25% is email." Without percentages, the tendency is to allocate effort based on comfort rather than strategy — which is precisely how single-channel obsession forms. Blount's investment diversification analogy is deliberate: just as a financial advisor does not tell you to "diversify" without giving you an actual asset allocation, a prospecting plan without explicit percentages is not a plan.

**Output:** A channel-mix table with named percentages, one-sentence rationale per channel, and the situation-profile signals that drove each adjustment.

---

### Step 4: Design the Daily Cadence Template

**Action:** Translate the channel-mix percentages into a Monday-through-Friday daily schedule, assigning each channel to specific time slots. Coordinate with the `prospecting-time-block-planner` output if available — channel blocks should fit within Golden Hours.

**Daily cadence design principles:**

- **Phone first.** Schedule the phone block at the start of the prospecting day. Calls require the most cognitive energy and the highest rejection-tolerance. Deferring the phone block until later in the day allows lower-effort channels (email, social) to absorb the entire day through inertia.
- **Email immediately after the phone block.** Follow-up emails sent within 30 minutes of a voicemail or a brief conversation have materially higher open rates than emails sent cold. Use the post-phone Platinum Hour window for email.
- **Social in off-peak windows.** LinkedIn engagement, content commenting, and connection requests do not require prospects to be at their desks. Schedule social in early morning or early afternoon — never during peak phone windows.
- **In-person on dedicated territory days.** If in-person is part of the mix, assign dedicated territory days (typically mid-week) and plan hub-and-spoke routes the night before in Platinum Hours. Do not mix drive time with phone blocks on the same day.
- **Referral asks embedded in close calls and customer conversations.** Referral prospecting is not a separate block — it is an action embedded in existing customer interactions. Schedule a standing prompt: ask one existing customer or close contact for a referral each day.
- **Text as a follow-up trigger.** Text messages belong after a prior touch establishes familiarity — not as a cold-open channel. If text is in the mix, it fires after phone voicemail or email, not before.

The extended example cadences for three selling archetypes (enterprise SaaS, SMB inside sales, and field rep) are in `references/example-daily-cadences.md`.

**WHY:** A cadence template converts the channel-mix percentages from a planning document into executable daily behavior. Without a day-by-day schedule, the channel mix exists only on paper — the rep still defaults to the comfortable channel because no specific time is blocked for the uncomfortable ones. The order of channels within the day matters as much as the allocation: phone first prevents the pattern where email and social fill the morning and the phone block is perpetually deferred.

**Output:** A Monday–Friday daily cadence table with named time slots and channel assignments.

---

### Step 5: Anti-Pattern Audit

**Action:** Audit the user's current or intended prospecting approach for the three most common single-channel-obsession patterns. For each pattern present, name it explicitly and provide the rebalancing action.

**Anti-Pattern 1: The "I'm So Much Better at X" Rationalization**

*Detection:* The user states or implies a strong preference for one channel ("I'm a relationship person, I do better in person," "Email is more professional in my industry," "My clients don't answer the phone"). This phrase, in any form, signals that a comfortable channel is being used to avoid an uncomfortable one.

*Blount's diagnosis:* "The 'I'm so much better at...' excuse is just that: an excuse to avoid other prospecting techniques that salespeople find unpalatable. More often than not, it's an excuse to avoid phone prospecting. The pipeline always reveals the truth." When this phrase appears, Blount states, that salesperson is underperforming against their number and "cheating themselves out of thousands of dollars in commissions."

*Janice's case:* Janice told Blount emphatically, "But I'm so much better in person!" She is the archetype of this pattern — using a genuine strength (in-person relationship building) to rationalize a genuine avoidance (phone prospecting). The fix is not to abandon the preferred channel; it is to add the avoided channel back into the mix at its appropriate percentage.

*Rebalancing action:* Name the avoided channel. Set a floor percentage for it — even 20% — and schedule it as the first block of the day for 30 days.

**Anti-Pattern 2: The One-Size-Fits-All Guru Channel**

*Detection:* The user's prospecting approach was shaped by a single book, course, or training program that advocated one method as the universal answer (social selling only, email sequencing only, inbound-only, cold calling only).

*Blount's diagnosis:* "There is an expert or so-called sales guru on every corner preaching to salespeople that their method is the one way to prospecting salvation... 'Do it my way and you'll get unlimited qualified leads.'" The guru's method may work for a specific situation but fails as a universal prescription because every territory, product, and prospect base is different.

*Rebalancing action:* Identify which channels the program excluded. Test each excluded channel for 30 days and track activity-to-outcome ratios. Let the numbers — not the dogma — determine the final mix.

**Anti-Pattern 3: The Rookie Imitating the Veteran**

*Detection:* The user is new to the territory (less than 12–18 months) and has modeled their prospecting approach on a tenured rep who appears to work low volume with high results.

*Blount's diagnosis:* "In fact, this is how many rookies get themselves into big trouble. They see Joe, the 20-year veteran, generating million-dollar months with what appears to be little effort. Then they emulate this behavior. On their way to failure, they miss the fact that Joe spent years qualifying his database and now he is tuned into his prospects' buying windows and knows exactly when to engage them."

*The structural difference:* Joe's low-effort phone volume is possible because his database is already qualified. He knows who to call and exactly when to call them. A new rep in the same territory has none of that infrastructure. Emulating Joe's channel mix without Joe's database leads directly to an empty pipeline.

*Rebalancing action:* New reps should treat heavy phone outreach as the database-building investment. As the database qualifies over 12–24 months, the mix can shift toward referrals, social, and timed calls — but not before.

**Output:** For each anti-pattern present: a named diagnosis, supporting evidence from the user's situation, and a specific rebalancing action.

---

## Output Template

```markdown
# Balanced Prospecting Cadence Plan
**Date:** [Date]
**Rep:** [Name]
**Prepared by:** fanatical-prospecting:balanced-prospecting-cadence-designer

---

## Situation Summary

[One paragraph profiling the seven variables and their channel signals]

---

## Viable Channels

| Channel | Viable? | Notes |
|---|---|---|
| Phone | Yes / Limited / No | [one sentence] |
| Email | Yes / Limited / No | [one sentence] |
| Social | Yes / Limited / No | [one sentence] |
| Text | Yes / Limited / No | [one sentence] |
| In-person | Yes / Limited / No | [one sentence] |
| Referral | Yes / Limited / No | [one sentence] |

---

## Recommended Channel Mix

| Channel | % of Prospecting Time | Daily Minutes (based on [X] prospecting hours/day) | Rationale |
|---|---|---|---|
| Phone | [%] | [min] | [one sentence] |
| Email | [%] | [min] | [one sentence] |
| Social | [%] | [min] | [one sentence] |
| In-person | [%] | [min/day average] | [one sentence] |
| Text | [%] | [min] | [one sentence] |
| Referral | [%] | [min] | [one sentence] |

---

## Weekly Cadence Template

| Time Slot | Monday | Tuesday | Wednesday | Thursday | Friday |
|---|---|---|---|---|---|
| [SLOT 1] | Phone block | Phone block | Phone block | [In-person / Phone] | Phone block |
| [SLOT 2] | Email follow-up | Email follow-up | Email follow-up | [In-person] | Email + Social |
| [SLOT 3] | Social | Social | Social | [In-person] | Social |
| [SLOT 4] | [Other channel] | [Other channel] | [Other channel] | [Other channel] | [Other channel] |
| End of day | Referral ask (1 per day) | Referral ask | Referral ask | Referral ask | Referral ask |

*Customize start/end times using your Golden Hours window from prospecting-time-block-planner.*

---

## Anti-Pattern Audit

| Anti-Pattern | Present? | Evidence | Rebalancing Action |
|---|---|---|---|
| "I'm so much better at X" rationalization | Yes / No | [quote or behavior observed] | [specific action] |
| One-size-fits-all guru channel | Yes / No | [program or influence identified] | [specific action] |
| Rookie imitating veteran | Yes / No | [tenure and behavior noted] | [specific action] |

---

## 30-Day Rebalancing Commitment

If any anti-pattern was flagged:

- [ ] [Avoided channel] is scheduled as the FIRST block of the day every day for 30 days
- [ ] [Avoided channel] floor: [X]% of prospecting time — not negotiable for 30 days
- [ ] Results tracked by channel at the end of each week: dials/sends → connects → meetings
```

---

## Key Principles

**Balance means actual percentages, not vague intent.** Saying "I'll use multiple channels" without assigning percentages is not a prospecting strategy — it is a plan to use whichever channel feels easiest that day. The investment analogy Blount uses is exact: a financial advisor who tells you to "diversify" without giving you an asset allocation has not advised you. The channel-mix percentages in this skill are the asset allocation for your prospecting portfolio.

**WHY:** Without percentages, the rep's actual channel usage is determined by comfort, not strategy. After two straight hours of cold calls with poor results, the instinct is to shift to email or LinkedIn because they feel less rejecting. The percentage constraint forces the phone block to run to completion even when the phone feels hard — which is precisely when it needs to run.

**The pipeline always reveals the truth about single-channel obsession.** A rep who insists they are getting results from one channel will have a pipeline that reflects it — either genuine results if the channel is appropriate for the ICP, or a shallow pipeline if the channel is over-relied on. Blount's observation is diagnostic, not punitive: "Salespeople who gravitate to a single prospecting methodology seriously sub-optimize their productivity." The pipeline is the evidence; the cadence is the fix.

**WHY:** Self-assessment of channel effectiveness is unreliable because reps naturally remember the successes from their preferred channel and attribute failure to external factors ("prospects just aren't responding to email right now"). Pipeline metrics — opportunities created per channel, conversion rate per channel, average deal size per channel — are objective. Tracking activity by channel for 30 days and comparing to pipeline outcomes is the only way to know whether the current mix is working.

**Territory tenure changes the optimal mix — but does not change the principle.** A new rep needs heavy phone to build a qualified database. An established rep can shift toward referrals, social, and timed calls. The balance point moves; the principle of balance does not. Blount states: "Striking a balanced approach with prospecting is the most effective means of filling your sales pipeline no matter your industry, product, or service."

**WHY:** The failure mode for established reps is the mirror image of the new rep's failure mode. A new rep who avoids the phone has no database and no pipeline. An established rep who abandons phone and email in favor of referral-only stops generating new-to-database prospects and allows the qualified tier of the pyramid to thin out. Both ends of the tenure spectrum require active management of channel balance.

---

## Examples

### Example 1: Enterprise SaaS AE (Inside Sales, Complex Deal, Mid-Tenure)

**Situation:** AE at an enterprise SaaS company selling a $75K/year platform to VP of Operations at companies with 200–2,000 employees. Sales cycle: 90–120 days. Inside sales only (no in-person). Two years in the role, qualified database of ~400 accounts. Currently at 85% of quota with one quarter to close.

**Situation profile signals:**
- Complex deal + contractual → phone + email are primary appointment-setting channels
- Inside sales model → in-person at 0%; text only for warm follow-ups
- Mid-tenure → database partially qualified; referrals emerging but not yet dominant
- Behind quota slightly → increase phone intensity

**Recommended mix:**
- Phone: 45% | Email: 30% | Social (LinkedIn): 20% | Text: 5% | In-person: 0% | Referral: embedded in customer calls

**Daily cadence:**
- 7:30–8:30 AM (Platinum): List prep, LinkedIn engagement, CRM review
- 9–10:30 AM: Phone block (Power Hour)
- 10:30–11:15 AM: Email follow-up to voicemails left in phone block
- 11:15 AM–12 PM: LinkedIn — connection requests + personalized InMail to target accounts
- 12–1 PM: Discovery calls / demos / lunch
- 1:30–2:30 PM: Phone block (Power Hour)
- 2:30–3 PM: Email sequences + LinkedIn follow-ups
- End of day: One referral ask embedded in a customer check-in call

**Anti-pattern check:** None flagged. Rep is using phone as primary — correct for complex inside sales.

---

### Example 2: SMB Inside Sales Rep (Transactional, New Territory)

**Situation:** Inside sales rep selling a $3,000/year SMB accounting tool to owners of businesses with 5–50 employees. Sales cycle: 1–2 weeks. One call can close. Six months in the role, territory database largely uncalled. Currently 60% of quota.

**Situation profile signals:**
- Transactional + inside sales → close on the phone; phone is highest-leverage channel
- New territory → must build the database fast; phone-heavy outreach is the database-qualification tool
- Behind quota → maximize phone intensity immediately
- SMB owner ICP → email has moderate effectiveness; LinkedIn has limited adoption in this segment

**Recommended mix:**
- Phone: 55% | Email: 30% | Social (LinkedIn): 10% | Text: 5% | In-person: 0%

**Anti-pattern check:** Rep reports "I'm better at email — I get more responses." Flagged as "I'm so much better at X" rationalization. The phone block must run first. Email response rates without phone warming are measuring a biased sample. Schedule phone as a mandatory first block for 30 days and measure phone-to-close ratios before adjusting the mix.

---

### Example 3: Field Rep in Rural Dispersed Territory (Outside Sales, Established)

**Situation:** Outside sales rep selling commercial maintenance contracts to manufacturing facilities in a rural 3-state territory. Accounts are 40–90 minutes apart. Sales cycle: 30–60 days. Five years in the territory, strong referral network, database fully qualified.

**Situation profile signals:**
- Outside sales + complex deal → phone for appointment-setting; in-person for close
- Rural/dispersed geography → in-person is resource-intensive; hub-and-spoke routing essential; phone call replaces spontaneous drop-ins
- Established tenure → referrals are a primary channel; social is secondary; phone is for buying-window calls, not cold database-building
- Strong referral network → referral should be an explicit channel with time allocation

**Recommended mix:**
- Phone: 30% | In-person: 25% | Referral (active ask): 20% | Email: 15% | Social: 10% | Text: 0% (not adopted in this industry)

**Cadence adjustment:** In-person allocated to 2 dedicated field days per week with routes planned in Platinum Hours the evening before. Phone block runs on the 3 office days. Referral asks embedded in every in-person meeting and customer check-in.

**Anti-pattern check:** None flagged. Five-year tenure with qualified database justifies the referral-heavy mix. However, if the rep were new to this territory, this mix would be flagged as the Rookie Imitating the Veteran pattern — the referral network took five years to build and cannot be replicated by a new rep on day one.

---

## References

| File | Contents |
|---|---|
| `references/channel-mix-matrix.md` | Full matrix of 12 scenario variants with recommended channel-mix percentages for each: enterprise SaaS inside sales, transactional SMB inside sales, field rep rural, field rep urban, consulting advisory, startup building-database, benefits/insurance, staffing, capital equipment, real estate, financial services, and SaaS mid-market |
| `references/example-daily-cadences.md` | Day-by-day cadence templates for three archetypes — enterprise inside sales AE, transactional SMB rep, and outside field rep — with time slots, activity descriptions, and output benchmarks per block |

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Fanatical Prospecting by Jeb Blount (Ch. 3–4).

## Related BookForge Skills

For setting the right objective (appointment vs. qualify vs. close) for each touch in the cadence:
```
clawhub install bookforge-prospecting-objective-setter
```

For tiering your prospect list so each channel touches the right prospect at the right time:
```
clawhub install bookforge-prospect-list-tiering
```

For blocking and protecting the time slots the cadence requires:
```
clawhub install bookforge-prospecting-time-block-planner
```

Browse the full Fanatical Prospecting skill set: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
