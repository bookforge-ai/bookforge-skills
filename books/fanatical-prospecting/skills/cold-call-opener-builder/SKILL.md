---
name: cold-call-opener-builder
description: |
  Build a complete, annotated cold call opener script using the Five-Step Telephone Prospecting
  Framework from Blount's Fanatical Prospecting.

  Trigger this skill when you hear or ask:
  - "cold call opener" or "phone script" or "what do I say when they pick up"
  - "telephone prospecting" or "sales phone call" or "cold calling script"
  - "five-step opener" or "phone opener" or "voice mail opener"
  - "prospecting call framework" or "how do I open a cold call"
  - "write me a call script" or "SDR call opener" or "BDR phone script"
  - "what do I say on a cold call" or "cold call introduction script"
  - "how to start a sales call" or "telephone prospecting framework"
  - "call opener template" or "sales call opening lines"
  - "how to not fumble the first 10 seconds" or "call structure for outbound"
  - "voicemail script" or "gatekeeper script"

  This skill produces a fully annotated, ready-to-use 5-line phone opener script in
  Name → Identify → Reason → Bridge → Ask order — plus a voicemail variant and a gatekeeper
  variant. It enforces no "How are you today?" pause, silence after the ask, and an explicit
  "because" in the bridge. Output is an annotated script, not abstract advice.

  NOT for: building the underlying bridge/because message (use prospecting-message-crafter first),
  setting the call objective (use prospecting-objective-setter), or handling objections after the
  opener (use prospecting-rbo-turnaround).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/cold-call-opener-builder
metadata:
  openclaw:
    emoji: "📚"
    homepage: "https://github.com/bookforge-ai/bookforge-skills"
status: published
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting"
    authors:
      - Jeb Blount
    chapters:
      - 15
tags:
  - sales
  - prospecting
  - cold-calling
  - phone-scripts
  - sdr
  - bdr
depends-on:
  - prospecting-objective-setter
  - prospecting-message-crafter
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "User's product/value prop, target prospect info, stated call objective. Can also accept output files from prospecting-objective-setter (prospecting-objective-plan-{date}.md) and prospecting-message-crafter (prospecting-message-output.md)."
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document directory with prospect notes and value prop. If upstream skill outputs exist in the working directory, read them first."
discovery:
  goal: "Produce a complete, annotated 5-step phone opener script with a voicemail variant and a gatekeeper variant, ready to use on a live call"
  tasks:
    - "Gather or read upstream skill outputs: call objective and bridge/because"
    - "Confirm no prohibited patterns (How are you today?, pause, pitch vomit) are in any draft"
    - "Draft Line 1: prospect name only, no pause"
    - "Draft Line 2: your name + company, immediate and transparent"
    - "Draft Line 3: 'The reason I'm calling is...' — direct statement of intent"
    - "Draft Line 4: bridge using the because from prospecting-message-crafter output"
    - "Draft Line 5: assumptive ask matched to the objective, then silence"
    - "Write annotated opener + voicemail variant + gatekeeper variant to cold-call-opener-script.md"
  audience:
    roles: [sdr, bdr, ae, founder-self-seller]
    experience: beginner-to-intermediate
  triggers:
    - "Rep is building a cold call opener for a new product or prospect segment"
    - "Current opener is generating 'not interested' in the first 3 seconds"
    - "Rep wants a script they can actually say out loud without sounding scripted"
    - "Preparing for a cold calling block and needs a repeatable framework"
    - "Voicemail return rate is near zero and rep needs a better structure"
  prerequisites: []
  not_for:
    - "Building the bridge/because message from scratch — run prospecting-message-crafter first for the message nucleus"
    - "Deciding what objective to go for on the call — run prospecting-objective-setter first"
    - "Handling the RBO that comes after the opener — use prospecting-rbo-turnaround"
    - "Writing a full email cadence — use prospecting-email-writer"
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
      - "Uses the 5-step Name→Identify→Reason→Bridge→Ask structure verbatim"
      - "Never inserts 'How are you today?' pause — the #1 control-killer on cold calls"
      - "Enforces silence after the ask — does not fill the pause with pitch vomit"
      - "Produces an annotated script, not abstract advice about what to do"
      - "Includes the word 'because' explicitly in the bridge line"
      - "Ask matches the stated call objective (appointment / qualifying info / direct sale)"
      - "Provides voicemail and gatekeeper variants alongside the live-answer script"
      - "Natural tone — does not sound scripted or robotic"
    what_baseline_misses:
      - "Inserts 'How are you today?' pause, handing control to the prospect's escape instinct"
      - "Does not structure the call in the 5-step order — wanders into pitch before stating reason"
      - "No explicit 'because' in the bridge — gives the prospect no reason to keep listening"
      - "Keeps talking after the ask instead of going silent — generates resistance and gives an easy out"
      - "Does not produce a voicemail variant or gatekeeper variant"
      - "Produces advice about calling instead of a ready-to-use script"
---

# Cold Call Opener Builder

## When to Use

You are about to pick up the phone and call someone who is not expecting your call. You have
10 seconds to establish why they should keep listening instead of getting off the phone.

This skill applies to any outbound phone touch where the prospect has not requested the call —
cold calls, warm calls, follow-up dials, and calls to inbound leads that haven't been spoken to
yet. It produces a **complete, annotated script** you can read aloud during a live call, not a
framework you have to interpret.

Use this skill when:
- You are building a call opener for a new product or prospect segment
- Your current opener is getting "not interested" before you finish your second sentence
- You want a voicemail you can leave that actually gets returned
- You are running a prospecting block and want a repeatable, confident structure
- You just ran `prospecting-objective-setter` and/or `prospecting-message-crafter` and are
  ready to assemble the final call script

**Dependency chain:** This skill is most effective when run after `prospecting-objective-setter`
(which determines your call objective and the ask you make in Step 5) and
`prospecting-message-crafter` (which produces the bridge and because for Step 4). If you do not
have those outputs, this skill will gather the same inputs directly.

## Context & Input Gathering

Before building the opener, collect the following. Read from working directory files if available,
otherwise ask the user directly.

**From `prospecting-objective-plan-{date}.md` (prospecting-objective-setter output) or ask:**
1. Call objective — what are you going for? Appointment / qualifying information / direct sale
2. The prospect's role, company, and industry (or a 1-sentence profile)

**From `prospecting-message-output.md` (prospecting-message-crafter output) or ask:**
3. Bridge type — Targeted (large prospect pool, inferred pain) or Strategic (conquest/C-level,
   researched)
4. The bridge sentence — the prospect-facing reason you are calling (their world, not yours)
5. The explicit "because" — the specific trigger event, insight, or outcome that earns their time
6. Your name and company name

**If no upstream outputs exist:** Ask the user for items 1–6 directly. A two-to-three sentence
verbal description of the selling situation is sufficient to proceed.

**Sufficiency threshold:** Items 1, 2, 4, and 6 are required. Items 3 and 5 can be derived from
item 4 if the user has a clear bridge statement.

## Process

### Step 1 — Confirm the Call Objective

**Action:** State the call objective explicitly and confirm it matches the correct scenario from
Blount's Four Objectives framework:

| Objective | When to use |
|---|---|
| Set an appointment | Complex/high-cost product, any channel; transactional product via outside-sales remote channel |
| Gather qualifying information | Unqualified prospects; contract-gated products; new territory |
| Close the sale directly | Transactional/low-cost product, inside sales channel or outside-sales in-person |
| Build familiarity | Cold prospects requiring 20–50 touches; secondary objective on most calls |

The objective drives the ask in Step 5. A mismatch here — for example, going for a close with a
complex product — wastes the call and confuses the prospect.

**WHY:** The ask is the only mechanism that produces a result. If the ask does not match what is
actually possible given the product, channel, and prospect qualification state, the call succeeds
technically (you delivered the opener) but fails commercially (you cannot get a yes). Confirming
the objective before writing Line 5 prevents this mismatch. (See `prospecting-objective-setter`
for the full Four Objectives decision framework.)

---

### Step 2 — Draft Line 1: Get Their Attention with Their Name

**Action:** Write Line 1 as exactly: `Hi, [Prospect First Name].`

No more. No "How are you today?" No pause. No preamble. Say their name and immediately
move to Line 2 without stopping.

**Why no "How are you today?" pause:** When you interrupt someone's day and then say
"How are you today?" and pause, the prospect has a split second to realize you are a salesperson
and that they made a mistake answering the phone. Their escape instinct kicks in — they hit you
with "Not interested" or "Who is this?" before you have said anything meaningful. That pause
transfers control of the call to the prospect's fight-or-flight response. (Blount, p. 185)

**Why the name works:** Saying another person's name is the fastest attention-getter in human
communication. For a split second, the prospect's brain stops what it was doing and registers
your call. That window is your only chance to get to Lines 2–5 uninterrupted. (Blount, p. 185)

---

### Step 3 — Draft Line 2: Identify Yourself Immediately

**Action:** Write Line 2 as: `My name is [Your Name] and I'm with [Company Name].`

Say it immediately after the name. No pleasantries. No "I was hoping to catch you." No "Sorry
to bother you" (apologetic framing signals you expect rejection and lowers confidence before
you've said anything).

**WHY:** Transparency has two benefits. First, it establishes that you are a professional who
respects the prospect's time — idle chitchat before establishing who you are signals that you
are about to pitch. Second, telling prospects who you are reduces their stress because people are
more comfortable when they know what to expect. Not knowing who is calling is itself a source
of resistance. (Blount, p. 186)

---

### Step 4 — Draft Line 3: State the Reason You Are Calling

**Action:** Write Line 3 as: `The reason I'm calling is [direct statement of intent].`

The intent statement should be a plain, honest statement of purpose — not a pitch, not a feature
claim, and not a vague "I'd love to connect." Examples:

- `The reason I'm calling is to set up a brief meeting to learn about your sales recruiting situation.`
- `The reason I'm calling is I read that you are building a new restaurant location and I wanted to learn more about your equipment selection process.`
- `The reason I'm calling is you downloaded our white paper on landing page optimization and I'd like to understand what triggered your interest.`

**WHY:** Stating the reason clearly and early does two things. First, it continues the transparency
that Line 2 started — prospects are people who do not want to be tricked or manipulated, and
telling them why you called is the single most respectful thing you can do with their interrupted
time. Second, it gives their logical brain a foothold before their emotional resistance peaks. The
prospect knows what is happening and can evaluate whether to keep listening. (Blount, p. 186)

---

### Step 5 — Draft Line 4: Bridge — Give Them a Because

**Action:** Write Line 4 using the bridge/because from `prospecting-message-crafter` output
(or build it now if not available). The bridge connects what you want with why the prospect
should care — in their language, about their world.

The bridge must:
- Include the word "because" or an equivalent connector (e.g., "I've found that...", "I've been
  working with...") that gives them a concrete reason
- Reference their world: their industry, their role, a trigger event, a known pain, a competitive
  concern — not your product features
- Pass the "So what?" test: if the prospect heard this line and thought "So what? That's about
  you, not me" — rewrite it

Bridge patterns that work:
- Trigger event: `I saw that your company just announced [event] and I've been working with several [role] teams navigating [related challenge].`
- Inferred industry pain: `Most [role]s I work with tell me that [specific pain] is their biggest challenge right now, and I have [specific outcome] that my clients are using to address it.`
- Social proof: `I work with several [similar companies] and they've been getting [specific result], and I thought it might be relevant to your situation.`

Avoid at all costs:
- `I want to tell you about our product.`
- `I'd love to show you what we have to offer.`
- `We're the number one provider of...`
- Any statement that is about you, your company, or your quota.

**WHY:** People give up their time for their reasons, not yours. The bridge is the only part of
the opener where you can earn a yes before you ask for one. Without a because, you are
interrupting someone's day and asking them to give you their time for no stated reason. Langer's
copy-machine study established that giving any reason — even a weak one — increases compliance
from 60% to 93–94%. The bridge is where that reason lives. (Blount, pp. 168, 186; Langer cited
in prospecting-message-crafter)

---

### Step 6 — Draft Line 5: Ask for What You Want, Then Go Silent

**Action:** Write Line 5 as a direct, assumptive ask matched to the call objective, then stop
talking.

Ask patterns by objective:
- **Appointment:** `How about we meet [Day] at [Time]?` or `I'd like to set a short [15/20/30]-minute call — how does [Day] at [Time] work for you?`
- **Qualifying information:** `Can you tell me more about [specific situation] and when [decision process] typically begins?`
- **Direct sale:** `Let's go ahead and get you set up — I just need [two quick pieces of information].`

After the ask: **stop talking.** Do not fill the silence. Do not apologize for the call. Do not add
"I know you're busy" or "I don't want to take up too much of your time." Do not start explaining
your product. Say the ask, then go quiet and let the prospect respond.

**WHY:** The single biggest mistake on prospecting calls is continuing to talk after the ask.
When you keep talking, you give the prospect reasons to say no, you create objections that
haven't surfaced yet, and you signal that you are not confident in your ask. The silence is
where the yes lives. Silence after an assumptive ask is uncomfortable for the caller and
comfortable for the prospect — that discomfort is the signal that you are doing it correctly.
(Blount, p. 170)

**Why assumptive:** Assertive asks produce significantly higher yes rates than passive or hedging
asks. "Would it be okay if maybe sometime we could possibly get together?" signals that you
expect rejection. "How about Thursday at 2 PM?" signals that you expect yes. The prospect's
answer is heavily influenced by the confidence level embedded in the question. (Blount, p. 170;
prospecting-message-crafter Key Principles)

---

### Self-Check Before Writing Output

Before finalizing, verify the assembled script passes all five checks:

- [ ] **No "How are you today?" pause** — Line 1 is the prospect's name and nothing else
- [ ] **Explicit "because" in Line 4** — the bridge contains a reason in the prospect's world
- [ ] **Ask matches objective** — Line 5 is asking for the thing identified in Step 1
- [ ] **No pitch vomit in Lines 3–4** — no product features, company bragging, or self-centered framing
- [ ] **Script ends at the ask** — nothing after Line 5 except [silence]

If any check fails, revise the failing line before writing output.

---

### Write Output

Write the annotated script to `cold-call-opener-script.md` in the working directory. The output
must include:

1. **Live-answer script** — all 5 lines assembled and ready to read aloud, with each line labeled
2. **Voicemail variant** — 5-step voicemail framework (see below)
3. **Gatekeeper variant** — transparent, respectful gatekeeper opener (see below)
4. **Anti-pattern notes** — a brief list of anything removed or avoided and why

## Inputs

| Input | Required | Source |
|---|---|---|
| Call objective (appointment / info / close) | Yes | `prospecting-objective-plan-{date}.md` or user states |
| Prospect name, role, company | Yes | User provides |
| Your name and company | Yes | User provides |
| Bridge/because sentence | Yes | `prospecting-message-output.md` or user provides |
| Bridge type (Targeted vs Strategic) | Recommended | `prospecting-message-output.md` or user states |
| Known trigger event or industry pain | Recommended | User provides; enhances Line 4 significantly |

## Outputs

| Output | Location | Description |
|---|---|---|
| `cold-call-opener-script.md` | Working directory | Annotated live-answer script + voicemail variant + gatekeeper variant |
| Anti-pattern removal notes | Inline in conversation | What was avoided and why |

## Key Principles

**1. No pauses. No chitchat. Get to the point in 10 seconds.** The Five-Step framework is designed
to deliver the opener end-to-end without pausing. Any pause transfers control of the call to the
prospect's escape instinct. A focused, deliberate, no-pause delivery is more respectful of the
prospect's time than a chatty one — and more effective. (Blount, p. 184)

**2. Natural tone over scripted delivery.** The framework is a guide, not a word-for-word recitation.
A script read in a robotic monotone defeats its purpose. The opener should sound like a confident
professional delivering a clear, prepared message — not an actor reading lines. Internalize the
structure; adapt the words to your voice.

**3. The bridge earns the ask.** Lines 1–3 get you through the door; Line 4 earns the right to
make the ask in Line 5. A weak bridge produces RBOs before you reach Line 5. A strong bridge —
one that connects to the prospect's actual world — reduces resistance because the prospect now
has a reason to keep listening. (Blount, pp. 168–169)

**4. Silence is a close technique.** Shutting up after the ask is not passive — it is the
active mechanism that converts a pitch into a conversation. The prospect cannot say yes if you
are still talking. (Blount, p. 170)

**5. Consistency enables improvement.** A repeatable framework means you can isolate what is
working. If your bridge is weak, you will hear it in the RBOs. If your ask is passive, you will
hear it in the hesitation. A framework you stick to is a framework you can improve. (Blount, p. 183)

## Examples

### Example 1 — SaaS Enterprise Seller: Appointment Objective

**Situation:** SDR at a sales enablement platform. Target: VP of Sales at 100–500 person SaaS
companies. Objective: set a 20-minute discovery meeting. Bridge: ramp time anxiety (Targeted,
Emotional). Bridge/because from `prospecting-message-crafter`.

**Live-answer script:**

| Line | Step | Script |
|---|---|---|
| 1 | Get attention | `Hi, Mark.` |
| 2 | Identify | `This is Sarah with TechStack Pro.` |
| 3 | Reason | `The reason I'm calling is to set up a short meeting about your sales onboarding process.` |
| 4 | Bridge/Because | `I work with several SaaS VP Sales teams who are frustrated that new reps take 4 to 6 months to hit quota — and by the time they ramp, half of them are already questioning their decision to join. We've helped companies like Acme cut that ramp time by over 50 percent.` |
| 5 | Ask + silence | `I don't know if it's a fit in your situation, but I'd like to find out. How about 20 minutes on Thursday at 2 PM?` — [silence] |

**What was avoided:** "How are you today?" pause; "I'd love to show you"; product feature list.

---

### Example 2 — Restaurant Supply to SMB: Information-Gathering Objective

**Situation:** Outside sales rep at a commercial kitchen equipment company. Target: owner/operator
of a new restaurant under construction. Objective: gather information on their equipment selection
process and timeline. Bridge: trigger event (building permit in local paper).

**Live-answer script:**

| Line | Step | Script |
|---|---|---|
| 1 | Get attention | `Hi, Ian.` |
| 2 | Identify | `This is Jeb with Acme Restaurant Supply.` |
| 3 | Reason | `The reason I'm calling is I read in the paper that you're building a restaurant over on the 44 bypass, and I wanted to learn more about your process for selecting kitchen equipment.` |
| 4 | Bridge/Because | `I realize I'm calling a little early in the process. What I've found is that when our design team works with restaurant owners before critical decisions about kitchen layout are finalized, you end up with more options and can often save significant money in construction costs and future labor with a more efficient setup.` |
| 5 | Ask + silence | `Can you tell me how you typically make those decisions and when the selection process will begin?` — [silence] |

**What was avoided:** Leading with product features; pause after name; passive ask ("would it be
okay if maybe...").

---

### Example 3 — Benefits Broker to HR Director: Appointment Objective (Strategic Bridge)

**Situation:** AE at a benefits brokerage. Target: HR Director at a 300-person manufacturer.
LinkedIn shows they recently posted about rising healthcare costs. Renewal is in Q4 (identified
via prospecting-objective-setter). Objective: set a pre-renewal discovery appointment. Bridge:
Strategic (researched trigger event).

**Live-answer script:**

| Line | Step | Script |
|---|---|---|
| 1 | Get attention | `Hi, Patricia.` |
| 2 | Identify | `This is Alex with Meridian Benefits Group.` |
| 3 | Reason | `The reason I'm calling is to schedule a brief meeting before your Q4 benefits renewal.` |
| 4 | Bridge/Because | `I noticed you recently shared something about managing healthcare cost increases — that's exactly what I've been helping HR Directors at manufacturers address. I work with several companies your size who've reduced their cost per employee by 15 to 20 percent without cutting plan quality, and I have some benchmarks from your industry I thought might be worth a look.` |
| 5 | Ask + silence | `I don't know if we'd be a fit, but it seems worth a 20-minute conversation to find out. How about next Tuesday at 10 AM?` — [silence] |

**What was avoided:** Generic "I'd love to tell you about our services"; "How are you doing?";
self-centered framing around what the rep wants.

---

## Voicemail Variant

When the call goes to voicemail, use this 5-step structure. Target: 20–30 seconds total.

1. **Identify yourself** — name and company up front
2. **Say your phone number twice** — slowly, before the message body
3. **State the reason for your call** — `The reason for my call is...`
4. **Give them a reason to call back** — a curiosity hook or specific insight they'd want
5. **Repeat name and phone number twice** — close every voicemail this way

**Voicemail example (Example 1 scenario):**
> "Hi, this is Sarah with TechStack Pro. My number is 555-0182 — 555-0182. The reason for my call is I've been working with a few VP Sales teams at SaaS companies who've cut new-rep ramp time by over 50 percent, and I have some data on how they did it that might be relevant to your team. Sarah with TechStack — 555-0182. Thanks, Mark."

Leave a voicemail when: the prospect is a high-value conquest account, their buying window is
opening, or you are running a deliberate familiarity-building campaign. Skip voicemail on cold
unqualified lists — at 20–30 seconds per voicemail, it destroys phone block efficiency for
contacts who do not know you and are unlikely to call back. (Blount, pp. 189–190)

---

## Gatekeeper Variant

When a gatekeeper answers, do not use tricks or deceptive tactics — they backfire and land you
on the do-not-help list. Use transparent, professional, direct language:

> `Hi, my name is [Name] with [Company]. I'm hoping to speak with [Decision Maker Name] —
> could you let me know if they're available?`

If the gatekeeper asks what it is regarding:
> `I'm calling about [honest 1-sentence description of reason]. I'd appreciate any help you can
> give me in connecting with [Decision Maker].`

Never pretend to be someone you are not. Never claim a relationship that does not exist.
Gatekeepers are people — treat them as such, ask for their help directly, and you will get more
of it than any clever scheme will ever produce. (Blount, Ch. 17)

---

## References

Detailed supporting materials are in the `references/` folder:

- `references/five-step-framework-examples.md` — extended example library across industries
  and call objectives; additional worked examples for inside sales, field sales, and founder
  self-seller scenarios
- `references/voicemail-callback-guide.md` — when to leave voicemail vs. dial without;
  callback rate benchmarks; voicemail templates by prospect tier; five-step voicemail framework
  with timing guidance
- `references/gatekeeper-transparency-guide.md` — gatekeeper engagement principles; what to say
  when asked "what is this regarding"; legitimate bypass tactics (alternate extensions, email,
  LinkedIn, events)
- `references/anti-pattern-library-phone.md` — phone-specific anti-patterns with before/after
  examples: "How are you today?" pause mechanics, pitch vomit triggers, apologetic openers,
  passive ask patterns, and silence-filling failures

**Source chapter:** Blount, Jeb. *Fanatical Prospecting*, Chapter 15 "Telephone Prospecting
Excellence" (PDF pp. 181–195). Five-Step Framework: pp. 183–188. Voicemail framework:
pp. 189–195. Bridge/Because foundational framework: Chapter 14 "Message Matters"
(PDF pp. 159–165).

**Cross-references:**
- *prospecting-message-crafter* — builds the bridge and because that powers Line 4
- *prospecting-objective-setter* — determines the call objective that drives Line 5
- *prospecting-rbo-turnaround* — Anchor-Disrupt-Ask framework for handling pushback after
  the opener (Ch. 16, pp. 196–210)

## License

Content derived from *Fanatical Prospecting* by Jeb Blount (Wiley, 2015). This skill is licensed
under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
You are free to share and adapt this material provided you give appropriate credit to Jeb Blount
and BookForge, and distribute any derivative works under the same license.

## Related BookForge Skills

Build the message nucleus before running this skill:
```
clawhub install bookforge-prospecting-message-crafter
```

Set the right call objective before building the opener:
```
clawhub install bookforge-prospecting-objective-setter
```

Handle push-back after the opener is delivered:
```
clawhub install bookforge-prospecting-rbo-turnaround
```

Browse the full Fanatical Prospecting skill set:
[bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
