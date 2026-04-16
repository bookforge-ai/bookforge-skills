---
name: prospect-list-tiering
description: Tier and prioritize a prospect list using the six-level Prospecting Pyramid framework — sorting every account from unknown contacts at the base to active buying-window prospects at the tip, then producing a daily action plan that specifies which tier to call first, what to do with each tier, and how to move prospects upward through the pyramid over time. Use this skill when the user has a raw prospect list and wants to know who to call first, asks how to prioritize their accounts, wants to rank or tier their CRM, wants to tier accounts, asks about the prospecting pyramid, needs an account prioritization framework, wants to identify which prospects are in the buying window, is building or cleaning up their CRM list, wants to stop randomly dialing and start with a system, wants qualified prospects separated from cold names, asks who should be top of their daily call list, has a mix of inbound leads and cold accounts and needs an order, wants to set up a conquest account list, or says their prospecting blocks feel unproductive and they need a better structure — even if they do not use the words "pyramid," "tiering," or "prioritization."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/prospect-list-tiering
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting"
    authors: ["Jeb Blount"]
    chapters: [10, 11]
tags: [sales, prospecting, account-prioritization, crm, pipeline, sdr, bdr]
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Prospect list (CSV or markdown table) plus known qualification data (lead source, company size, buying window status, trigger events) and optionally an Ideal Customer Profile"
  tools-required: [Read, Write, Grep]
  tools-optional: []
  mcps-required: []
  environment: "Directory containing prospect list files (CSV, markdown) and optionally ICP or account notes files"
discovery:
  goal: "Tier a prospect list into six pyramid levels and produce a daily action plan with the correct call order and action directive per tier"
  tasks:
    - "Classify each prospect into one of six pyramid tiers based on qualification state"
    - "Assign the correct action directive to each tier"
    - "Build a daily execution sequence (tip-first, then conquest, then lower tiers)"
    - "Identify which filters to apply when building focused batch lists"
    - "Flag data gaps that prevent accurate tiering and recommend remediation"
  audience:
    roles: [sdr, bdr, ae]
    experience: beginner-to-intermediate
  triggers:
    - "who should I call first"
    - "prioritize my prospect list"
    - "tier my accounts"
    - "prospecting pyramid"
    - "account prioritization"
    - "CRM list cleanup"
    - "qualified prospects"
    - "buying window"
    - "my prospecting blocks feel unproductive"
  prerequisites: []
  not_for:
    - "Evaluating a single prospect in isolation (no list to tier)"
    - "Writing call scripts or email copy (use prospecting-message-crafter)"
    - "Setting a prospecting objective for a specific call (use prospecting-objective-setter)"
    - "Calculating pipeline ratios or quota math"
  environment: "Any agent environment with access to a prospect list file or pasted prospect data"
  quality:
    minimum_tiers_classified: "all prospects assigned to a tier"
    required_outputs: ["tiered-prospect-list", "daily-action-plan"]
    completeness: "every tier must carry its action directive in the output"
---

# Prospect List Tiering

## When to Use

You have a prospect list — whether 20 accounts or 2,000 — and need to stop treating every name identically. Treating every prospect the same is statistically inefficient: only a small fraction of your database is in a buying window at any given moment, so random dialing guarantees most of your energy goes to prospects who cannot buy yet.

This skill applies the six-tier Prospecting Pyramid framework to sort every prospect by qualification state and buying-window proximity, then produces a daily action plan so you always start each prospecting block with the highest-probability prospects.

Typical triggers:
- You have a CRM export and need to decide who to call tomorrow morning
- You have a mix of inbound leads, referrals, and cold accounts and want a ranked order
- Your prospecting blocks feel unfocused or produce mostly dead-end conversations
- You want to identify your conquest accounts and give them dedicated attention
- You are setting up or cleaning your CRM and want a systematic tiering logic

**This skill does NOT cover:**
- Writing call scripts or email sequences (use `prospecting-message-crafter`)
- Setting the right objective for a specific call (use `prospecting-objective-setter`)
- Calculating pipeline ratios or quota math

---

## Context and Input Gathering

### Required Context (must have — ask if missing)

- **Prospect list:** The accounts and contacts to tier. Accepted formats: CSV file, CRM export, markdown table, or pasted text.
  -> Check the working directory for: `prospect-list.csv`, `accounts.csv`, `leads.csv`, any `.csv` file with company or contact columns
  -> If not found, ask: "Can you share your prospect list? A CSV export, pasted markdown table, or even a simple list of company names with any notes you have will work."

- **Known qualification data per prospect:** At minimum, the user should know *something* about each prospect beyond the name. Even partial data (lead source, company size, whether a contract is expiring) enables accurate tiering.
  -> Check prompt for: mentions of "inbound," "referral," "contract expiration," "trade show," "they reached out," "no info," "cold list," company revenue or headcount
  -> If still missing, ask: "For each prospect, what do you know? Even rough notes — things like 'they filled out our form,' 'referred by a client,' 'expiring contract in Q3,' or 'we have no info yet' — help me assign the right tier."

- **Ideal Customer Profile (ICP):** Criteria defining a qualified prospect — industry, revenue range, headcount, decision-maker role, geography, or use-case fit.
  -> Check for: `icp.md`, `icp.txt`, or ICP details in the prompt
  -> If missing: proceed with whatever qualification data exists and note which tiers may need ICP validation before calling

### Observable Context (gather from environment)

- **Account notes files:** Any per-account research documents (trigger events, stakeholder maps, competitor info) that enable more precise tiering
  -> Look for: `account-notes/`, `research/`, individual company markdown files
  -> If found: read and incorporate into tier assignments

- **CRM fields in the prospect list:** Fields like `Lead Source`, `Last Activity`, `Deal Stage`, `Contract Renewal Date`, `Account Size`, `Decision Maker Identified` are direct tier signals

### Default Assumptions

- If qualification data is entirely absent for a prospect: assign Tier 1 (Unknown) and flag the data gap
- If a prospect is a confirmed inbound lead or referral but has no further qualification data: assign Tier 5 (Hot Inbound/Referral) — lead source trumps data completeness
- If ICP fit is unknown: tier by qualification state alone; add an ICP validation note to the action directive

### Sufficiency Threshold

```
SUFFICIENT when:
- Prospect list is available (any format)
- At least some qualification signal exists for each prospect (even "no info" = Tier 1)
- ICP is known OR user confirms they will apply it manually

NOT sufficient:
- No list at all (ask user to provide one before proceeding)
```

---

## Process

### Step 1: Ingest and normalize the prospect list

Read the prospect list file. Parse it into a working table with at minimum: company name, contact name (if available), and any qualification fields present.

**Why:** Normalization reveals which data fields exist across the list and which are missing — this determines how confidently each prospect can be tiered. A list with "Lead Source" and "Contract Renewal Date" fields can be auto-tiered; a list with only company names requires the user's manual input.

For CSV files, check for these high-signal fields:
- `Lead Source` / `Source` (inbound, referral, cold, trade show)
- `Last Activity Date` / `Last Contact`
- `Contract Expiration` / `Renewal Date`
- `Deal Stage` / `Pipeline Stage`
- `Decision Maker Identified` (boolean or name)
- `Budget Confirmed`
- `Account Size` / `Revenue` / `Employees`

### Step 2: Classify each prospect into a pyramid tier

Apply the six-tier framework. The primary sort axis is **qualification state** — how much is known and how close the prospect is to a buying window.

| Tier | Name | Classification Criteria | Action Directive |
|------|------|--------------------------|-----------------|
| **T1** | Unknown | Company name only; contact info unverified or missing; no competitive/budget/stakeholder data | Correct and confirm data; begin qualifying process |
| **T2** | Basic Data Confirmed | Verified contact info including email; some competitive, budget, or demographic data; partial stakeholder map | Identify buying window and all stakeholders |
| **T3** | Buying Window Identified | Complete decision-maker and influencer contact records including social profiles; future buying window known | Implement nurturing campaigns; stay visible until window opens |
| **T4** | Conquest | Top 10-100 highest-value or largest opportunities in territory; strategic priority regardless of immediate buying window | Nurture + regular touches + trigger-event monitoring + stakeholder mapping + familiarity building |
| **T5** | Hot Inbound / Referral | Prospect contacted you (web form, trade show, referral, inbound call); recency matters — window of interest fades | Immediate follow-up to qualify and move to pipeline; do not let more than 24-48 hours pass |
| **T6** | In Buying Window | Highly qualified; buying window is open NOW due to immediate need, contract expiration, trigger event, or budget cycle | Call today; goal is to advance to a qualified opportunity or set appointment |

**Tier assignment decision logic:**
1. Is this an inbound lead or referral? → T5 (or T6 if fully qualified AND in active buying window)
2. Is the prospect confirmed in an active buying window (contract expiring, trigger event, stated need)? → T6
3. Is this a strategic conquest account (top of territory list)? → T4 (regardless of buying window status)
4. Are decision-maker contacts confirmed and a future buying window identified? → T3
5. Are basic contact details verified and some qualification data present? → T2
6. None of the above — name/company only or insufficient data → T1

**Why:** Tier assignment drives every downstream action. A Tier 1 prospect called with a closing pitch wastes both the rep's time and the prospect's goodwill. A Tier 6 prospect left un-called because they appear lower on an alphabetical list is a missed revenue opportunity. The tier is the instruction.

### Step 3: Apply list construction filters (optional refinement)

If the list is large (50+ prospects) or the user wants batch-focused prospecting blocks, apply secondary filters to create focused sub-lists for specific blocks. Use combinations from:

- **Objective:** What action do you want from this block — set appointment, gather qualification data, build familiarity, or close?
- **Channel:** Phone, email, LinkedIn, text, in-person, networking
- **Territory plan:** Geographic cluster (zip code, city, region) for field reps
- **Industry vertical:** Same-sector batching improves relevance and social proof
- **Decision-maker role:** Economic buyer vs. technical buyer vs. champion
- **Seasonal / inactive / trade-show:** Time-sensitive segments

**Why:** Channel-switching between calls burns cognitive energy. Batching by industry means you build sector-specific knowledge and pattern recognition within a single block. Territory batching reduces travel time for field reps.

### Step 4: Build the daily action plan

Produce a prioritized daily sequence that walks the pyramid from tip to base:

1. **Block 1 — Tier 6 (In Buying Window):** Call these first, while energy and confidence are highest. These prospects convert more readily, producing early wins that create momentum for the rest of the day.
2. **Block 2 — Tier 5 (Hot Inbound / Referral):** If not yet called, follow up immediately. Inbound interest decays fast.
3. **Block 3 — Tier 4 (Conquest):** Systematic nurturing and trigger monitoring for strategic accounts. Even without an open window, regular touches build familiarity.
4. **Block 4 — Tiers 1-3 (Qualifying work):** Data gathering, stakeholder identification, and nurturing campaigns for the bulk of the database. This work populates tomorrow's Tier 6 list.

**Why:** Starting with the highest-probability prospects is not just efficiency math — it is psychological architecture. Early wins create confidence. Confidence fuels the energy needed to power through the harder, lower-tier calls later in the block. Reversing the order (starting with cold names) produces friction-first blocks that most reps abandon early.

### Step 5: Flag data gaps and tier-up opportunities

Scan for:
- Prospects stuck in T1 for a long time (data gap — what would it take to move them to T2?)
- Prospects in T2 or T3 with no recent activity (nurture lapsed?)
- Conquest accounts (T4) with no stakeholder map (immediate research priority)
- Inbound leads (T5) older than 48 hours (urgency flag)

**Why:** The pyramid is a living system, not a one-time sort. Its value compounds when reps systematically advance prospects upward by filling in qualification data over time. Flagging stagnant accounts creates an explicit "move-up" task list.

### Step 6: Write outputs to file

Produce two output files:
1. `tiered-prospect-list.md` (or `.csv`) — the full list with tier assignment, tier name, action directive, and any data-gap flags
2. `daily-action-plan.md` — the sequenced call plan for the next prospecting block, grouped by tier

**Why:** Externalizing the output means the rep can execute without re-deriving priority from scratch tomorrow. The tiered list can be imported back into the CRM as a custom field or tag.

---

## Inputs

| Input | Required | Format | Notes |
|-------|----------|--------|-------|
| Prospect list | Yes | CSV, markdown table, or pasted text | Must contain at minimum company names |
| Qualification data per prospect | Recommended | Inline in list or separate notes | Lead source, buying window, stakeholder info |
| Ideal Customer Profile (ICP) | Recommended | `icp.md` or described in prompt | Used to validate fit at Tier 2+ |
| Account notes | Optional | Per-account markdown files | Improves tier accuracy for T3/T4 |

---

## Outputs

| Output | Format | Description |
|--------|--------|-------------|
| `tiered-prospect-list.md` | Markdown table | Every prospect with: tier number, tier name, action directive, data-gap flags |
| `daily-action-plan.md` | Markdown | Sequenced call plan grouped by tier, with action directives and any specific notes per account |

---

## Key Principles

**The pyramid is a qualification map, not a ranking by company size.** A small company with a known contract expiration date belongs in Tier 6. A Fortune 500 with no contact info belongs in Tier 1.

**Tier 6 prospects are scarce and time-sensitive.** At any given time, only a small fraction of your database is in an active buying window. Missing them because you worked alphabetically is an invisible but expensive mistake.

**The pyramid is a living system.** The goal of every Tier 1-3 call is to gather information that moves the prospect one tier up. Over weeks, a well-managed list produces a growing Tier 6 pool from systematic qualification work.

**Conquest accounts (Tier 4) require consistent attention.** These are strategic enough to warrant regular touches even without an open window. The Law of Familiarity says prospects buy from people they recognize. Tier 4 is where familiarity is built.

**Inbound leads (Tier 5) have a half-life.** The window of interest from a trigger event or inbound inquiry fades within 24-48 hours. Tier 5 accounts that age into Tier 3 or 4 without follow-up represent a preventable loss.

**List quality is the single biggest lever on prospecting block productivity.** A well-tiered list that puts the right prospect first has more impact on results than technique, script quality, or channel choice.

---

## Examples

### Example 1: SDR with a 300-account territory list

**Situation:** An SDR at a B2B SaaS company has 300 accounts in their CRM from a data vendor. No qualification has been done. The morning prospecting block starts in 30 minutes.

**Inputs provided:** CSV export with fields: Company, Contact Name, Email, Phone, Industry, Employee Count, Lead Source (all "Data Provider")

**What the skill does:**
- All 300 accounts start as Tier 1 (Unknown) — lead source is cold data, no qualification data present
- Identifies no Tier 5 or Tier 6 prospects in the current list
- Builds a batch-focused daily plan: pick an industry vertical, run a block calling for data gathering (confirm decision-maker name, ask one qualifying question about current vendor)
- Flags that the list needs qualification work before the pyramid can produce Tier 6 accounts
- Recommends adding these CRM fields: `DM Confirmed`, `Buying Window`, `Trigger Event`, `Budget Confirmed` to enable future tiering

**Daily action plan output:** Single block — Tier 1 qualification calls. Objective: data gathering. 20-30 calls. Goal: confirm contact, get one piece of qualification data per account.

---

### Example 2: AE with 50 strategic accounts, mixed qualification states

**Situation:** An Account Executive manages 50 named accounts. Three have contracts expiring in the next 90 days. Eight submitted an inbound demo request this week. Twelve are flagged as strategic conquest accounts. The rest are partially qualified.

**Inputs provided:** CSV with fields: Company, Contact, Stage, Contract Renewal Date, Lead Source, Decision Maker, Budget Confirmed

**What the skill does:**
- **Tier 6:** 3 accounts — contract expiration in <90 days AND decision maker known AND budget confirmed. Action: call today.
- **Tier 5:** 8 accounts — inbound demo requests this week. Action: follow up within 24 hours; qualify on the call.
- **Tier 4:** 12 accounts — conquest list, varying qualification states. Action: nurturing sequence + trigger-event check.
- **Tier 3:** 14 accounts — DM known, future buying window identified. Action: nurturing touchpoints.
- **Tier 2:** 8 accounts — contact info confirmed, no buying window yet. Action: stakeholder mapping calls.
- **Tier 1:** 5 accounts — minimal data. Action: data gathering.

**Daily action plan:** Block 1 (first 45 min) — 3 Tier 6 calls. Block 2 — follow up with 8 inbound leads. Block 3 — conquest account check-ins. Blocks 4+ — lower-tier qualifying work.

---

### Example 3: SDR cleaning up a stale CRM with 150 contacts

**Situation:** An SDR inherited a territory with 150 contacts logged by a previous rep. Last activity date is 3-18 months ago. No consistent tiering. Many records have outdated contact info.

**Inputs provided:** CRM export with Last Activity Date, Stage, partial notes

**What the skill does:**
- Identifies 4 accounts with notes indicating upcoming contract renewals → tentatively Tier 6 (needs confirmation call)
- Finds 2 accounts where notes say "referral from customer" → Tier 5 (aged, but still prioritize follow-up)
- Identifies 8 accounts with complete stakeholder maps but stale last-activity dates → Tier 3 (reactivate nurture)
- Remaining 136 accounts have incomplete or aged data → Tier 1 or 2
- Flags all Tier 1 accounts with "last activity > 6 months" for data-verify calls before any pitch attempt
- Produces a 2-week cleanup plan: 10 accounts per day, starting with the 4 potential Tier 6s

---

## References

Full tier definitions with classification criteria checklist: see inline table in the Process section above.

List construction filter reference: 14 filters enumerated in Step 3.

Source chapter: Blount, Jeb. *Fanatical Prospecting.* Wiley, 2015. Chapter 10: "Leveraging the Prospecting Pyramid" (pp. 102-109); Chapter 11: "Own Your Database" (pp. 110-113).

---

## Related BookForge Skills

- **prospecting-objective-setter** — Once you know which tier to call, use this skill to select the right objective (set appointment, gather information, build familiarity, or close) for each prospecting block.
- **prospecting-message-crafter** — Build the actual phone opener, email, or LinkedIn message for a specific prospect tier and objective.

---

## License

[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) — BookForge Skills. Source framework: *Fanatical Prospecting* by Jeb Blount (Wiley, 2015).
