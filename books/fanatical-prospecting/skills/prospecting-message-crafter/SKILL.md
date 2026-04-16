---
name: prospecting-message-crafter
description: |
  Craft or repair a prospecting message for any channel using the WIIFM → Bridge → Because → Ask framework from Blount's Fanatical Prospecting.

  Trigger this skill when you need to:
  - Write a cold call opener, cold email, LinkedIn message, or text prospecting message
  - Figure out "what should I say" to a prospect on any outbound channel
  - Build a bridge or reason ("because") that gives a prospect a compelling reason to meet
  - Diagnose why a current script or email is getting rejected and fix it
  - Answer "what's my value prop for this call?" or "how do I frame WIIFM?"
  - Check a draft for pitch vomit, cheesy openers, weak asks, or "I'd love to" language
  - Understand the difference between Targeted and Strategic bridge types and choose the right one
  - Write a Power Statement that answers "why should they choose me over the competition?"
  - Craft a message that leads with emotional value, insight/curiosity value, or tangible/logic value
  - Stop getting hit with "not interested" the second you open your mouth
  - Improve connect-to-conversation or email reply rates across any outbound channel

  NOT for: turning around an objection or brush-off after the opener (use prospecting-rbo-turnaround),
  building a full 5-step phone call script (use cold-call-opener-builder), or writing a multi-touch
  email cadence (use prospecting-email-writer). This skill produces the core message nucleus that
  all channel skills inherit — the bridge and because that make the prospect say yes.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/prospecting-message-crafter
metadata:
  openclaw:
    emoji: "📨"
    homepage: "https://github.com/bookforge-ai/bookforge-skills"
status: published
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting"
    authors:
      - Jeb Blount
    chapters:
      - 14
tags:
  - sales
  - prospecting
  - messaging
  - copywriting
  - outbound
  - sdr
  - bdr
depends-on: []
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "User's current script, email draft, or message copy (paste inline or provide as .md/.txt file), plus their ICP description, value proposition, and target prospect situation. If no draft exists yet, the skill builds from scratch with gathered context."
  tools-required: [Read, Write, Grep]
  tools-optional: []
  mcps-required: []
  environment: "Markdown or text file directory with user's prospecting materials (call-script.md, email-sequence.md, value-prop.md, icp.md). Agent reads user-provided files, analyzes the draft, and writes an improved message to prospecting-message-output.md."
discovery:
  goal: "Produce a refined prospecting message with explicit WIIFM → Bridge → Because → Ask structure that passes the 'So what?' test and contains zero anti-patterns"
  tasks:
    - "Gather the user's situation: target prospect role/industry, product value prop, bridge type needed (Targeted vs Strategic), desired outcome (appointment / info / close)"
    - "Diagnose current draft (if provided) against anti-pattern checklist"
    - "Select value category: emotional, insight/curiosity, or tangible/logic"
    - "Build or refine the bridge using the prospect empathy checklist"
    - "Apply the 'So what?' test before finalizing"
    - "Produce the revised message with element labels and a brief rationale"
    - "Write output to prospecting-message-output.md"
  audience:
    roles: [sdr, bdr, ae, founder-self-seller]
    experience: beginner
  when_to_use:
    triggers:
      - "Writing a cold call opener for the first time"
      - "Cold email reply rate is under 3% and you want to diagnose why"
      - "Someone asks 'what should I say?' or 'what's my bridge?' for a target segment"
      - "A current script is generating too many 'not interested' RBOs in the first 5 seconds"
      - "Preparing to target a new ICP vertical or decision-maker role"
      - "A C-level prospect requires a researched Strategic bridge"
      - "Wanting to add emotional or curiosity hooks instead of feature dumps"
    prerequisites: []
    not_for:
      - "Turning around a reflex response or brush-off after the opener has been delivered (use prospecting-rbo-turnaround)"
      - "Building the full 5-step phone framework including pauses and silence (use cold-call-opener-builder)"
      - "Multi-touch email cadence sequencing (use prospecting-email-writer)"
      - "Diagnosing pipeline math or activity ratios (use pipeline-health-diagnostic)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 0
      baseline: 0
      delta: 0
    tested_at: ""
    eval_count: 0
    assertion_count: 0
    iterations_needed: 0
    what_skill_catches:
      - "Uses WIIFM-Bridge-Because structure, not just any value proposition"
      - "Distinguishes Targeted bridges (inferred, high-volume) from Strategic bridges (researched, conquest/C-level)"
      - "Detects and removes 'How are you today?' opener with pause — the #1 call-killer"
      - "Detects and removes 'I'd love to / I want to tell you about' self-centered framing"
      - "Detects pitch vomit: feature lists, company bragging, data dumps with no prospect relevance"
      - "Applies Langer's because principle: giving any reason is more powerful than giving none"
      - "Applies the 3-category value framework: emotional / insight-curiosity / tangible-logic"
      - "Applies the 18-question prospect empathy checklist to surface emotional triggers"
      - "Forces a 'So what?' test before finalizing — kills weak bridges before they hit a prospect"
      - "Writes an assumptive ask, not a passive hedge ('How about Thursday at 2?' vs 'Would it be okay if maybe we met?')"
    what_baseline_misses:
      - "Produces generic value propositions without bridging to the prospect's emotional world"
      - "Does not distinguish Targeted from Strategic bridge types"
      - "Includes 'How are you today?' pause — triggering the prospect's escape instinct"
      - "Uses self-centered framing ('I'd love to / I want to show you / we are the best')"
      - "Does not run the 'So what?' test — leaves weak bridges in the message"
      - "Does not know the Langer copy-machine study or why 'because' works even with weak reasons"
      - "Produces a passive ask ('What do you think?' vs 'How about Thursday at 2?')"
---

# Prospecting Message Crafter

## When to Use

You are about to call, email, message on LinkedIn, or text a prospect and you need to answer the hardest question in outbound sales: *What do I say?*

This skill applies to any outbound prospecting channel — phone, email, LinkedIn, text, or in-person — because every channel shares the same message nucleus: **WIIFM → Bridge → Because → Ask**.

Use this skill when:
- Writing your first cold call opener for a new prospect segment
- Your current script is getting too many "not interested" responses in the first 5 seconds
- You need a bridge for a C-level or conquest account that requires research
- An email is going out to a high-value prospect and you want to be sure it passes the "So what?" test
- You want to move from feature dumping to emotional/curiosity framing

**This skill is the hub.** The phone, email, and social channel skills inherit the bridge and because patterns produced here. Build the message nucleus first; then deploy it through the channel skill.

## Context & Input Gathering

Before building the message, gather (or ask the user for) the following:

**Required:**
1. Target prospect's role and industry (e.g., "VP of Sales at a 200-person SaaS company")
2. Your product/service and its strongest outcome (e.g., "cuts new-rep ramp time by 50%")
3. Channel you are targeting (phone / email / LinkedIn / text / in-person)
4. Desired outcome of this touch (appointment / qualifying information / direct sale)

**Recommended:**
5. Current draft of the script or email (paste inline or point to file path)
6. Any known trigger event at this account (hiring surge, funding, competitor churn, etc.)
7. Bridge type: Targeted (large pool, similar prospects, inferred pain) or Strategic (conquest, C-level, limited-access — requires research)?

**If no current draft exists:** proceed directly to Step 3 (Bridge Selection).

## Process

### Step 1 — Diagnose the Current Draft (if one exists)

Read the user's existing message and flag every anti-pattern from the checklist below. Mark each finding with its failure type so the user can see exactly what was broken.

**Anti-pattern checklist:**
- [ ] "How are you today?" opener followed by a pause — this hands control of the call to the prospect's escape instinct. The moment they realize you are a salesperson, they object. (Blount, p. 185)
- [ ] "I'd love to / I want to tell you about / I want to show you" — self-centered framing. The prospect subconsciously hears: "I want to waste your time talking about me." (Blount, p. 151)
- [ ] Pitch vomit — feature/benefit monologue, company bragging ("we're the #1 provider of..."), marketing data dumps unrelated to the prospect's world (Blount, pp. 151-152)
- [ ] No "because" — asking for time without giving a reason. Langer's copy-machine study: giving *any* reason increases yes rate from 60% to 93-94%. No because = lowest possible close rate. (Blount, p. 158-159)
- [ ] Passive ask — "What do you think?", "Would it be okay if...", "Is this a good time?" These signal low confidence and produce 30% success vs. 70% for assertive asks. (Blount, p. 166)
- [ ] "So what?" failure — the bridge is about your company's capabilities, not the prospect's situation. The prospect's internal response is "so what?" and they disengage.

**Why diagnose first:** Reps improve faster when they can see the exact line that triggers rejection. Label each failure so the user understands the root cause, not just the rewrite.

### Step 2 — Identify the Bridge Type

Decide which bridge type fits the situation. This is a risk/reward tradeoff:

**Targeted Bridge** — appropriate when:
- You have a large pool of similar prospects (50+ with similar roles/industries)
- Doing deep research on each one is not time-efficient
- You can infer a high-probability pain from industry trends, competitor behavior, or common decision-maker anxieties

*Process:* Infer the pain. Use the empathy checklist in Step 3 to surface emotional language. Iterate as you hear real responses in the field.

**Strategic Bridge** — appropriate when:
- The prospect is a C-level executive, conquest account, or limited-access contact
- You may get only one shot
- The prospect's time is so valuable that a generic bridge will be dismissed

*Process:* Research first. Pull from Google Alerts, LinkedIn profile, company press releases, CRM notes, trade articles. Look for: jargon they use, core values, recent awards/initiatives, trigger events, problems they reference publicly. Then craft a bridge using *their* language. (See `references/strategic-bridge-research-checklist.md`)

**Why distinguish these:** Using a Strategic bridge workflow on a 10,000-SMB database is economically irrational and destroys prospecting velocity. Using a Targeted bridge on a Fortune 100 CRO is lazy and will get you ignored.

### Step 3 — Choose the Value Category

Every effective bridge delivers value in at least one of three categories. Pick the category that fits the prospect's world, or combine two:

**Emotional value** — connects to a painful emotion and offers relief
- Target emotions: stress, worry, anxiety, frustration, anger, insecurity, distrust, fear
- Relief offered: peace of mind, options, lower stress, security, hope
- Use when: the prospect's role is high-stress and problems are emotionally loaded (e.g., a Sales VP whose reps are missing quota, a CISO post-breach)

**Insight/curiosity value** — offers information that gives the prospect competitive leverage
- Trigger: "Your competitors may already have this. Do you?"
- Use when: the prospect cares about maintaining a competitive edge or fears being left behind
- Requires credible third-party data or real client outcomes as proof

**Tangible/logic value** — data, case studies, specific ROI numbers
- Use when: the prospect is in a technical, data-centric, or finance role and makes decisions on evidence
- Requires specific numbers (e.g., "cut ramp time by 50%", "41% improvement over last launch")

**Why categorize:** Pitching logic to an emotionally driven prospect (or pitching anxiety to an analyst who wants numbers) causes the bridge to miss entirely. Match the value category to the role, not to your marketing department's preferred messaging.

### Step 4 — Build the Bridge Using the Empathy Checklist

Stand in the prospect's shoes. Before writing a word, answer these questions from the prospect's perspective for their specific role:

- What causes them stress or anxiety on a daily basis?
- What competitive unknown would worry them if a rival had it and they didn't?
- What failure would put their job or reputation at risk?
- What wastes their time, money, or resources?
- What would give them a meaningful win or relief right now?
- What information would they fear getting into a competitor's hands?

Use emotional language in the bridge: *frustrated, stressed, overwhelmed, concerned, behind, at risk, falling behind, peace of mind, save, protect, gain an edge.*

**Then apply the "So what?" test:** Read your bridge aloud and ask: "If the prospect heard this, would their internal response be 'So what? That's about you, not me'?" If yes, rewrite.

The bridge structure is:
> *[State what you know or have observed about their world] + [because] + [what you can offer that is relevant to their situation]*

**Why empathy first:** People make decisions based on emotion first and justify with logic. Pitching features doesn't work because it asks logical brain to evaluate before emotional brain has said yes. The bridge must land emotionally before the logical value prop adds credibility. (Blount, pp. 162-163)

### Step 5 — Write the Ask (Assumptive, Direct, Specific)

Every prospecting touch must end with a direct ask. There are three steps:
1. Ask assertively — assume you will get yes
2. Shut up — silence gives the prospect room to say yes
3. Be ready for reflex responses, brush-offs, and early objections (RBOs)

**Assumptive ask examples (use these patterns):**
- "How about we meet Thursday at 2:00 PM?" (not: "Would it be okay if we maybe got together sometime?")
- "I'll be near your office Monday. Can you do lunch?" (not: "I have the whole day open, whenever works for you.")
- "Tell me about your process for selecting vendors." (not: "I was wondering if maybe you could share...")

The ask must match the prospecting objective:
- Appointment: "How about Thursday at 2:00 PM?"
- Qualifying info: "Can you tell me more about your situation and when the decision process begins?"
- Direct sale (transactional): "Let's go ahead and get that set up."

**Why an assumptive ask:** Sales teams tracked across thousands of calls show assertive asks produce ~70% yes rates vs. ~30% for non-assertive asks. The ask is the only mechanism that produces an answer; without it, nothing happens. (Blount, p. 166)

### Step 6 — Assemble and Output the Final Message

Assemble the message in WIIFM → Bridge → Because → Ask order. Label each element inline so the user can see the structure and adapt it.

Write the output to `prospecting-message-output.md` in the working directory. Include:
- The revised message (channel-ready)
- Element labels (WIIFM / Bridge / Because / Ask)
- A brief note on which anti-patterns were removed from the original draft
- The value category used (Emotional / Insight-Curiosity / Tangible-Logic)
- Bridge type (Targeted or Strategic)
- The "So what?" test result

## Inputs

| Input | Required | Source |
|---|---|---|
| Target prospect role and industry | Yes | User provides |
| Product/service and key outcome | Yes | User provides or `value-prop.md` |
| Prospecting channel | Yes | User states |
| Desired outcome of the touch | Yes | User states |
| Current draft of the message | No (will build from scratch) | User pastes inline or provides file path |
| Known trigger events at the account | No (enhances Strategic bridges) | User provides or research |
| Bridge type preference | No (skill will recommend) | User states or skill decides |

## Outputs

| Output | Location | Description |
|---|---|---|
| `prospecting-message-output.md` | Working directory | Final message with labeled elements, anti-pattern removal notes, value category, and "So what?" test result |
| Anti-pattern diagnosis | Inline in conversation | Labeled list of what was wrong with the original draft and why |

## Key Principles

**1. Because beats everything.** Langer's copy-machine study: giving *any* reason ("because I have to make copies") raised yes rates from 60% to 93%. The word "because" triggers compliance. You don't need a perfect value prop — you need a direct, simple because. (Blount, p. 158-159)

**2. Prospects give time for their reasons, not yours.** No one cares what you want, what you'd love to do, or what your company claims to be the best at. The only message that works is the one that answers *their* WIIFM — the most pressing question on any busy person's mind. (Blount, p. 155)

**3. Emotion first, logic second.** Decisions are made emotionally and justified with logic. Bridges that connect to anxiety, stress, fear, or competitive insecurity open doors. Feature lists close them. (Blount, pp. 162-163)

**4. Simple and direct beats complex and clever.** Prospecting messages are designed for a single purpose: to quickly persuade the prospect to give you their time. Elaborate scripts overcomplicate and telegraph insecurity. A 10-second because that sounds natural outperforms a two-minute polished pitch. (Blount, p. 158)

**5. The ask determines everything.** Without a direct, assumptive ask the message has no output. Fear of rejection leads reps to hedge, qualify, and meander — which produces silence and kills momentum. Ask, then shut up. (Blount, pp. 165-166)

**6. The bridge has two types for a reason.** Spending 30 minutes researching an SMB from a 10,000-prospect database is wasteful. Sending a generic bridge to a Fortune 100 CFO is disrespectful. Match research depth to prospect value and access difficulty. (Blount, pp. 159-161)

## Examples

---

### Example 1 — Repairing a Failing Cold Call Opener (SDR / SaaS / VP Sales Target)

**Situation:** SDR at a sales enablement platform targeting VP of Sales at 100-500 person SaaS companies. Current message getting too many "not interested" in the first three seconds.

**Current failing message:**
> "Hi Mark, this is Sarah from TechStack Pro. How are you doing today? [pause] I wanted to reach out because we have an amazing new platform that helps sales teams with onboarding and enablement. We've worked with some of the biggest companies in the space and I'd love to get 30 minutes on your calendar to show you everything we can do."

**Trigger:** "How are you doing today?" + pause — hands control to the prospect's escape mechanism. "I'd love to" + feature dump — self-centered, no bridge to prospect's world. Passive ask — "get 30 minutes... to show you" signals pitch not value.

**Process:**
- Bridge type: Targeted (large pool of similar VP Sales targets, inferred pain)
- Value category: Emotional (VP Sales anxiety = new reps not producing fast enough)
- Empathy check: VP Sales is stressed when new reps miss quota for the first 90 days; fears losing good hires because onboarding is disorganized
- "So what?" test: "We have an amazing platform" → So what? Fails. Rewrite around their stress.

**Output:**
> "Hi Mark, this is Sarah with TechStack. The reason I'm calling is I work with several SaaS VP Sales teams who are frustrated that new reps take 4-6 months to hit quota — and by the time they ramp, half of them are already questioning their decision to join. We've helped companies like [similar company] cut that ramp time by over 50 percent. I don't know if it's a fit in your situation, but I'd like to find out. How about 15 minutes on Thursday at 2 PM?"

| Element | Content |
|---|---|
| WIIFM bridge | New rep ramp anxiety (emotional value — their stress, not your product) |
| Because | Specific outcome (50% ramp reduction) + social proof (similar companies) |
| Ask | Specific day/time, low-risk framing ("I don't know if it's a fit") |
| Anti-patterns removed | "How are you today?", pause, "I'd love to", feature dump |

---

### Example 2 — Building a Strategic Bridge for a C-Level Prospect (AE / Enterprise / CFO Target)

**Situation:** Enterprise AE targeting the CFO at a 1,200-person manufacturing company. LinkedIn shows they recently announced a plant expansion and are hiring aggressively. No prior contact.

**Trigger:** High-value conquest prospect, C-level, limited access — Strategic bridge required.

**Process:**
- Research: press release mentions 200 new hires across 3 facilities; LinkedIn shows CFO posted about "scaling without losing cost discipline"
- Bridge type: Strategic — use their language ("cost discipline"), reference the trigger event (expansion)
- Value category: Tangible/logic + Emotional (CFO will need evidence AND anxiety hook around cost control during growth)
- Empathy check: CFO fears that aggressive hiring creates runaway overhead and reduces EBITDA

**Output:**
> "Hi David, this is Alex from WorkForce Analytics. The reason I'm calling is I read about your expansion to three new facilities and the 200 hires you're bringing on. I imagine keeping cost discipline during that kind of growth is a real challenge — especially when onboarding overhead scales faster than productivity. I've helped CFOs at similar manufacturers maintain a tight cost-per-hire-to-productivity ratio during expansion phases. While I don't know if we'd be a fit, I have some benchmarks from your industry I thought might be useful. How about a short call Thursday at 10 AM to see if it's worth exploring?"

| Element | Content |
|---|---|
| WIIFM bridge | Uses their language ("cost discipline"), references trigger event (expansion) |
| Because | Industry benchmarks = insight/curiosity value; cost-per-hire risk = emotional |
| Ask | Specific time, assumptive, low-risk framing |
| Bridge type | Strategic — researched trigger event and their own stated priorities |

---

### Example 3 — Building from Scratch: Targeted Bridge (BDR / IT Security / CISO Target)

**Situation:** BDR at a security awareness training company. No current message. Building a Targeted bridge for the CISO segment.

**Trigger:** "What should I say to CISOs?" with no draft.

**Process:**
- No research per individual (Targeted bridge — large CISO segment)
- Empathy check: CISO anxiety = employees clicking phishing links, regulatory audit failures, board-level exposure
- Value category: Emotional (fear of breach + career exposure)
- "So what?" test: any message about "training modules" or "platform features" fails — rewrite around board-level fear

**Output:**
> "Hi Jennifer, this is Ryan with SecureForce. The reason I'm calling is most CISOs I work with tell me that phishing training is their biggest headache — not because they don't have a program, but because click rates aren't improving and the board is asking questions. We've worked with teams in your industry to cut employee click rates by over 60 percent in 90 days. I'm not sure if it's relevant to your situation, but I'd like to find out. How about 20 minutes next Tuesday at 3 PM?"

## References

Detailed supporting materials are in the `references/` folder:

- `references/bridge-types-and-templates.md` — full worked examples of Targeted vs Strategic bridges by industry and decision-maker role; template library with fill-in slots
- `references/strategic-bridge-research-checklist.md` — the full 18-question empathy checklist plus research sources (Google Alerts, LinkedIn, CRM, press, trade publications) with worked examples
- `references/value-category-examples.md` — emotional, insight/curiosity, and tangible/logic value examples by role (CISO, VP Sales, CFO, COO, CTO, Ops Director, Small Business Owner)
- `references/anti-pattern-library.md` — full examples of each anti-pattern with before/after rewrites and the psychological mechanism that makes each one fail

**Source chapter:** Blount, Jeb. *Fanatical Prospecting*, Chapter 14 "Message Matters" (pp. 132-153 / PDF pp. 150-171). Calibration references: Chapter 15 "Telephone Prospecting Excellence" (pp. 165-170 / PDF pp. 183-187); Chapter 19 "E-Mail Prospecting" (PDF pp. 239-243).

**Referenced frameworks:**
- Langer, E.J. (1978). Copy-machine compliance study — the "because" effect (cited in Blount, p. 158)
- Konrath, Jill. *SNAP Selling* — three-part value proposition: measurable objective, status quo disruption, proof (cited in Blount, p. 156)
- Weinberg, Mike. *New Sales. Simplified.* — Power Statement: prospect issues + offerings + competitive differentiators (cited in Blount, p. 157)

## License

Content derived from *Fanatical Prospecting* by Jeb Blount (Wiley, 2015). This skill is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt this material provided you give appropriate credit to Jeb Blount and BookForge, and distribute any derivative works under the same license.

## Related BookForge Skills

This is the **hub skill** for the Fanatical Prospecting message framework. Six channel skills depend on the bridge and because patterns produced here:

- `cold-call-opener-builder` — deploys this message in Blount's 5-step telephone framework (attention → identify → reason → bridge → ask)
- `prospecting-email-writer` — wraps this message in the AMMO plan + Hook-Relate-Bridge-Ask email structure
- `prospecting-rbo-turnaround` — handles reflex responses and brush-offs after the opener has been delivered
- `in-person-prospecting-route-planner` — applies this message in the 5-step in-person prospecting call process
- `text-prospecting-sequence-builder` — adapts this message for text-based prospecting protocols
- `prospecting-objective-setter` — defines the correct ask (Step 5) by mapping product type and prospect qualification to the right prospecting objective

**Build this skill's output first. Then pass the bridge and because to the channel skill you need.**
