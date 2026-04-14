---
name: tailor-pitch-by-stakeholder
description: |
  Tailor a Commercial Teaching pitch to each stakeholder role using Functional Bias Cards and route the pitch to avoid the C-suite elevation trap.

  Trigger this skill when you need to:
  - Tailor a sales pitch to different roles in a buying committee
  - Build stakeholder-specific messaging for a multi-stakeholder sale
  - Create a different message for VP Engineering vs CFO vs procurement
  - Use a Functional Bias Card to map what each role cares about
  - Build a stakeholder map for an enterprise deal
  - Understand who to pitch to first and in what order
  - Adapt a pitch for different audience roles without losing the core insight
  - Tailor for resonance with a buying committee
  - Create per-role pitch variants from a single base pitch script
  - Build consensus across a buying group before reaching the decision-maker

  NOT for: building the base pitch (use author-commercial-teaching-pitch first),
  building the underlying commercial insight (use build-commercial-insight),
  or diagnosing an existing pitch's structure (use diagnose-pitch-for-commercial-teaching-fit).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/tailor-pitch-by-stakeholder
metadata:
  openclaw:
    emoji: "🧭"
    homepage: "https://github.com/bookforge-ai/bookforge-skills"
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors:
      - Matthew Dixon
      - Brent Adamson
    chapters:
      - 6
tags:
  - sales
  - b2b-sales
  - challenger-sale
  - stakeholder-mapping
  - pitch-tailoring
  - sales-messaging
depends-on:
  - author-commercial-teaching-pitch
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "pitch-script.md (from author-commercial-teaching-pitch) and stakeholder-map.md with the roles and titles present in this buying group"
  tools-required:
    - Read
    - Write
    - AskUserQuestion
  works-offline: true
discovery:
  goal: "Tailor a Commercial Teaching pitch to each stakeholder role using Functional Bias Cards and route the pitch to avoid the C-suite elevation trap. Outputs tailored-pitch-variants.md with per-role Functional Bias Cards, per-role pitch variants, and a routing plan."
  triggers:
    - "Tailor my pitch to different stakeholders"
    - "I need different messaging for the CFO vs the VP Engineering"
    - "Who should I pitch to first in a consensus sale?"
    - "Build a Functional Bias Card for my buyer roles"
    - "How do I adapt my commercial teaching pitch for multiple roles?"
    - "Create per-role pitch variants for my buying committee"
    - "Help me build stakeholder-specific messaging"
  audience:
    - Sales reps and account executives managing multi-stakeholder enterprise deals
    - Sales enablement teams building role-based message libraries
    - Product marketing managers translating pitch scripts into role-specific assets
    - Sales managers coaching reps on stakeholder engagement strategy
  prerequisites:
    - "Run author-commercial-teaching-pitch first to produce pitch-script.md — this skill adapts that artifact, not a generic pitch"
  not_for:
    - Building the base pitch — use author-commercial-teaching-pitch
    - Building the commercial insight — use build-commercial-insight
    - Diagnosing pitch structure — use diagnose-pitch-for-commercial-teaching-fit
---

# tailor-pitch-by-stakeholder

Adapt a completed Commercial Teaching pitch to each role in a buying committee. The base pitch from `author-commercial-teaching-pitch` contains the right insight — this skill changes the language, data points, concerns, and framing for each person who needs to hear it. Outputs `tailored-pitch-variants.md` with per-role Functional Bias Cards, adapted pitch variants, and a routing plan that builds bottom-up consensus before reaching the decision-maker.

---

## When to Use

Use this skill after `author-commercial-teaching-pitch` has produced `pitch-script.md`. The base pitch was built for a target segment, not for every individual in a buying group. In complex B2B sales, multiple people participate in a purchase but each one evaluates the deal through a different lens — their own role, metrics, concerns, and career objectives.

A pitch that lands with a VP of Operations will confuse a CFO. The same Reframe can either energize or alienate depending on whether it maps to what that person measures. This skill ensures the core insight reaches every stakeholder in their own language.

---

## Context and Input Gathering

### Load the prerequisite artifacts

Read `pitch-script.md` from `author-commercial-teaching-pitch`. Extract:
- The Reframe headline (the core insight that must remain consistent across all variants)
- The unique strength anchor (what only your solution can deliver)
- The target segment and the Rational Drowning data already in the pitch
- The New Way framing (the organizational change the customer agrees to in Step 5)

If `pitch-script.md` does not exist, ask the user to run `author-commercial-teaching-pitch` first. Do not proceed without it — this skill adapts an existing pitch; it does not build one from scratch.

### Load or elicit the stakeholder map

If `stakeholder-map.md` exists, read it. Extract:
- Each unique role / title present in the buying group
- Whether each person is a decision-maker (signs the agreement) or an influencer/end-user (participates but does not sign)
- Any known priorities, concerns, or history already gathered through discovery

If `stakeholder-map.md` does not exist, use `AskUserQuestion` to collect:
1. What roles are involved in this purchase? (e.g., "CFO, VP Engineering, Head of IT, procurement manager")
2. Which of these people ultimately signs the agreement?
3. What industry and company context applies?
4. What is already known about each person's priorities or concerns?

---

## Process

### Step 1 — Apply the Four-Layer Tailoring Frame

Before adapting language per role, establish the shared outer layers that apply to all stakeholders.

**Layer 1 — Industry context:**  
What trends, competitive events, or regulatory pressures are active in this customer's sector? Name 2-3 that are undeniable. These provide the backdrop all stakeholders share.

**Layer 2 — Company context:**  
What does this specific company's recent history show? Recent earnings themes, strategic priorities, announced initiatives, or market position shifts. Pull from public sources: press releases, earnings calls, investor day materials.

**Layer 3 — Role context (Functional Bias):**  
For each unique role, build a Functional Bias Card (see Step 2 below).

**Layer 4 — Individual context:**  
Anything known specifically about this person: career stage, past decisions, internal political position, stated priorities, any history with your company. Fill in from discovery notes where available; leave as a gap to fill during live conversation where not.

**Why:** The vast majority of sales messaging is not contextualized at any level. Industry and company layers are table stakes — they establish that the rep has done their homework. Role-level and individual-level tailoring are what differentiate Challenger reps from core performers and are the layers most likely to produce the reaction "you understand my world."

---

### Step 2 — Build a Functional Bias Card for Each Unique Role

For each role in the stakeholder map, complete the following four-component card. This is the operational unit of tailoring.

**The Functional Bias Card pattern comes from the Solae case** — the food-ingredients supplier that operationalized role-level tailoring across their entire sales force using pre-built cards per buyer role. The skill's output MUST cite the Solae pattern by name so the user understands this is a proven, scaled approach — not an improvised artifact. Include a one-line attribution ("Functional Bias Cards as implemented at Solae") in the `tailored-pitch-variants.md` output.

**Card format:**

```
ROLE: [Title]
STAKEHOLDER TYPE: [Decision-maker | Influencer/End-user]

(a) DECISION CRITERIA — What does this role define as success?
    What are they measured on? What outcomes make this person look good?
    Format outcomes as: "[verb] [metric] by [magnitude] in [context]"

(b) FOCUS — What metrics does this person monitor daily or weekly?
    These are the numbers they pull up, the dashboards they check.
    Use these metrics when you cite data in the pitch for this role.

(c) KEY CONCERNS — What does this person worry about?
    What questions do they ask themselves day-to-day?
    What risks can keep them from saying yes?

(d) POTENTIAL VALUE AREAS — What levers can this person pull?
    What actions, investments, or decisions are within their authority?
    This is the vocabulary to use when presenting your solution to this person.
```

**Why each field matters:** Decision criteria tell you which outcomes anchor the pitch. Focus fields tell you which data will be credible. Key concerns allow you to open with empathy — you already know what they're worried about, so you do not need to ask. Potential value areas are the language layer: they tell you how to translate your capability into this person's world.

**Scale note:** Role-level outcomes are predictable (a CFO's top concerns at one company predict a CFO's concerns at another), stable over time, and finite (3-5 outcomes per role). A central marketing or enablement team can build these cards once and deploy them across the entire sales force.

See `references/functional-bias-card.md` for the full template, the Solae case walkthrough, and the outcome statement format.

---

### Step 3 — Map the Pitch to Each Role's Functional Bias Card

Return to `pitch-script.md` and work through each step of the pitch for each role:

For each role's Functional Bias Card, identify:

- **Warmer adaptation:** Which of the 2-3 challenge hypotheses are most relevant to this role's key concerns? Swap out challenges that do not match this person's world.
- **Reframe adaptation:** The core insight stays the same. What changes is the language — restate the Reframe using this role's decision criteria vocabulary. A CFO hears the Reframe in revenue/cost terms; a VP Engineering hears it in system reliability terms; a procurement officer hears it in supplier risk terms.
- **Rational Drowning adaptation:** Which data points from the pitch match this role's focus metrics? Replace generic data with the numbers this person monitors. A CFO cares about margin impact; an operations director cares about throughput and cycle time.
- **Emotional Impact adaptation:** Does the story in the pitch feature a character in a similar role? If not, adapt the scenario protagonist to this role. The story must feature someone this stakeholder can recognize as "like me."
- **New Way adaptation:** Which capabilities in the New Way directly map to this role's potential value areas? Lead with those. The CFO hears about the financial control capability; the head of operations hears about workflow efficiency.
- **Your Solution adaptation:** Which of your unique capabilities map to this role's specific value areas? Do not present every feature — present only the features that resolve this person's specific concerns and outcomes.

Document the changes per role. Not every step requires a different script — sometimes only the data points change, sometimes only the story protagonist changes. But every role should have at least one adapted element that would not have landed without the Functional Bias Card.

---

### Step 4 — Apply the Decision-Maker vs. Influencer Routing Rule

Classify each stakeholder:

**Decision-makers** (people who sign the agreement — typically senior executives or procurement):
- What they care about most: "widespread support for this supplier across my organization"
- What drives their loyalty: the overall sales experience of the buying group, not individual rep performance
- They think of themselves as buying from an organization, not from a person
- **Pitch goal:** Show that the team believes in this. Build a case for consensus, not a polished solo performance.
- **Pitch content:** Emphasize organizational outcomes, ease of doing business, ability to collaborate across functions.

**Influencers and end-users** (people who participate but do not sign):
- What they care about most: the individual rep's professionalism, unique perspectives, and ability to teach them something new
- They buy from people, not organizations
- The top drivers of their loyalty are insight and education — discovering something they did not know about how to be more effective in their role
- **Pitch goal:** Teach them something genuinely new. The Reframe lands hardest here — if they have never considered this angle before, they become your most effective internal advocates.
- **Pitch content:** Emphasize the insight, the fresh perspective, the specific outcome for their role.

**Why this split matters:** The research underlying this framework found that for decision-makers, organizational sales experience attributes are nearly twice as important as individual rep attributes — the reverse is true for influencers. The same pitch strategy cannot optimize for both simultaneously. Sequence and framing must differ.

---

### Step 5 — Anti-Pattern Check: C-Suite Elevation Trap

Before finalizing the routing plan, apply this check:

**The trap:** Conventional sales training emphasizes getting direct access to the senior decision-maker as quickly as possible. The logic: "If we can just get in that door, that's going to help us close the deal."

**Why it fails:** Decision-makers' top loyalty driver is "widespread support for the supplier across my organization." They are not willing to go out on a limb for a supplier on a large purchase without team consensus behind it. A polished top-down pitch from a sales rep carries far less weight with the decision-maker than confirmation from their own team.

**The stronger path:** Build genuine value with influencers and end-users first. Teach them something they did not know. When they become convinced, they evangelize upward — and their word carries more weight than anything the rep says directly to the executive.

**Flag if the current plan includes any of the following:**
- Prioritizing an executive meeting before any team-level conversations
- Using team interactions primarily to gather intelligence rather than deliver insight
- Planning to present a "finely tuned pitch" to the senior decision-maker using information pulled from stakeholders — rather than using those interactions to genuinely teach the stakeholders something valuable

**If flagged:** Reorder the routing plan so influencer/end-user conversations precede the decision-maker conversation. The goal is not to avoid the decision-maker — it is to arrive at that meeting with documented consensus already in place.

---

### Step 6 — Build the Value Planning Tool (Optional — Recommended for Late-Stage Deals)

Once stakeholder conversations are progressing, use this stage-gate template to document per-stakeholder buy-in before the final close conversation:

**For each stakeholder:**

| Stakeholder Role | Specific Outcome Addressed | Strongest Concern / Objection | Capability Response | Sign-Off |
|-----------------|---------------------------|------------------------------|-------------------|----------|
| [Role] | [Outcome in their vocabulary] | [Their concern, stated as they would say it] | [Specific thing you will do or deliver] | [Optional signature] |

**How to use this with the decision-maker:**  
When the rep sits down to close, place this document on the table. Every stakeholder's specific outcome, concern, and agreed response is visible in one view. The decision-maker does not need to take the rep's word for team support — it is documented on one page.

**Optional best practice:** Ask each stakeholder to initial their column as conversations progress. This is not a formal contract. It is a working alignment tool that creates a micro-commitment, making reversal harder when the full deal reaches the decision-maker.

---

### Step 7 — Write tailored-pitch-variants.md

Create the output artifact with the following structure:

```markdown
# Tailored Pitch Variants
**Base pitch:** [link or reference to pitch-script.md]
**Deal/account:** [Customer name or deal identifier]
**Date:** [Date]

---

## Layer 1: Industry Context (all stakeholders)
[2-3 industry trends or events that apply to everyone in this buying group]

## Layer 2: Company Context (all stakeholders)
[2-3 company-specific facts: strategic priorities, recent announcements, market position]

---

## Stakeholder 1: [Title]
**Type:** Decision-maker | Influencer/End-user

### Functional Bias Card
**(a) Decision Criteria:**
- [Outcome 1]
- [Outcome 2]

**(b) Focus (monitored metrics):**
- [Metric 1]
- [Metric 2]

**(c) Key Concerns:**
- "[Worry 1]"
- "[Worry 2]"

**(d) Potential Value Areas:**
- [Lever 1]
- [Lever 2]

### Pitch Adaptations (what changes from the base)
- **Warmer:** [Challenge hypotheses most relevant to this role]
- **Reframe:** [How the core insight is re-stated in this role's vocabulary]
- **Rational Drowning:** [Data points that match this role's focus metrics]
- **Emotional Impact:** [Scenario protagonist adjusted to this role]
- **New Way:** [Capabilities emphasized that match this role's value areas]
- **Your Solution:** [Features to lead with for this stakeholder]

### Routing Priority: [Early / Mid / Final]
[1-2 sentences on when and why to engage this person in the sequence]

---

[Repeat per stakeholder]

---

## Routing Plan
**Sequence:**
1. [Stakeholder A] — [why first]
2. [Stakeholder B] — [why second]
3. [Decision-maker] — [deliver after documented consensus is in place]

**C-suite elevation check:** [PASSED / FLAG — describe if flagged]

---

## Value Planning Tool (when deal is in late stage)
| Role | Outcome Addressed | Concern | Capability Response | Sign-Off |
|------|------------------|---------|-------------------|----------|
| [Role] | | | | |
```

---

## Inputs

| Input | Required | Description |
|-------|----------|-------------|
| `pitch-script.md` | Yes | Output of `author-commercial-teaching-pitch` — base six-step pitch with Reframe, Rational Drowning data, and unique strength anchor |
| `stakeholder-map.md` | Yes (or elicit) | Roles, titles, and decision-maker / influencer classification for this buying group |
| Discovery notes | Optional | Known priorities, concerns, and history for specific individuals — used to populate Layer 4 (individual context) |

---

## Outputs

| Output | Path | Description |
|--------|------|-------------|
| `tailored-pitch-variants.md` | `./tailored-pitch-variants.md` | Per-role Functional Bias Cards, per-role pitch adaptations, routing plan, and Value Planning Tool template |

---

## Key Principles

**The Reframe stays constant; the language changes.** The core commercial insight must remain consistent across all role variants — if the insight is correct, it applies to the whole organization. What changes is the vocabulary, the metrics cited, the story protagonist, and the capabilities emphasized. Never dilute the Reframe to make it less challenging for a specific role.

**Decision-makers buy from organizations; influencers buy from people.** These are not personality types — they are structural differences in how these two groups evaluate a purchase. Organizational-level attributes (widespread support, ease of doing business) dominate for decision-makers; individual rep insight and education dominate for influencers. Pitch strategy must reflect this split.

**The path to the C-suite runs through the team, not directly to the executive.** Reps who bypass stakeholders to reach the decision-maker faster undermine themselves. The decision-maker's top priority is team consensus — which the rep cannot provide but which the team, once taught something valuable, absolutely can.

**Functional Bias Cards are role-level, not person-level.** A card for "VP of Operations" at one company predicts with reasonable accuracy what a VP of Operations at a comparable company cares about. This is what makes tailoring scalable — a central team builds the cards once; every rep uses them across the portfolio.

**Teaching influencers is how you build the consensus decision-makers require.** Influencers advocate most powerfully for suppliers who taught them something genuinely new. Mining them for intelligence makes them vendors; teaching them something valuable makes them advocates.

---

## References

- `references/functional-bias-card.md` — Full template, four-component walkthrough, Solae case study (head of manufacturing card + Value Planning Tool), and outcome statement format

**Source:** *The Challenger Sale* by Matthew Dixon and Brent Adamson. Chapter 6 (Tailoring for Resonance). Solae case study: functional bias card and value planning tool implementation. Loyalty driver data from CEB Customer Loyalty Survey (2011).

---

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You are free to use, adapt, and redistribute with attribution.

Source book content is copyrighted by the authors. This skill contains no verbatim passages — all content is paraphrased, structured, and extended for agent execution.

---

## Related BookForge Skills

| Skill | Relationship |
|-------|-------------|
| `author-commercial-teaching-pitch` | Run before this skill — produces the pitch-script.md that this skill adapts |
| `build-commercial-insight` | Run before author-commercial-teaching-pitch — validates the Reframe this pitch chain is built on |
| `diagnose-pitch-for-commercial-teaching-fit` | Alternative entry — audit an existing pitch before building or tailoring |
| `plan-negotiation-with-constructive-tension` | Run after tailoring — manages the negotiation dynamic once stakeholders are engaged |
