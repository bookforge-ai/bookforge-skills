---
name: prospecting-objection-handler
description: |
  Classify prospect pushback and produce a scripted Anchor-Disrupt-Ask turnaround for any sales
  objection, reflex response, or brush-off using Blount's RBO Turnaround Framework.

  Trigger this skill when you hear or ask:
  - "objection handling" or "turn around a no" or "prospect said no"
  - "cold call objection" or "reflex response" or "brush off"
  - "not interested" or "happy with current" or "too busy"
  - "anchor disrupt ask" or "RBO turnaround" or "sales rejection"
  - "prospect pushed back" or "how do I respond to no"
  - "they said send me some information" or "call me later"
  - "they said they're happy with their current provider"
  - "turnaround script" or "handling a brush-off" or "dealing with rejection on a cold call"
  - "2-RBO rule" or "when to give up on a prospect" or "dead horse checkpoint"
  - "disrupt vs defeat" or "don't say I understand" or "never overcome objections"

  This skill classifies the pushback type (Reflex Response / Brush-Off / Objection), explains why
  each requires a different intervention, then produces a complete Anchor-Disrupt-Ask script for
  the specific pushback — including a fallback script for the second attempt and a dead-horse
  checkpoint for when to gracefully exit.

  NOT for: writing the initial cold call opener before pushback occurs (use cold-call-opener-builder),
  building the underlying bridge/because message (use prospecting-message-crafter), or planning
  a multi-touch email cadence.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/prospecting-objection-handler
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
      - 16
tags:
  - sales
  - prospecting
  - objection-handling
  - cold-calling
  - sdr
  - bdr
depends-on:
  - cold-call-opener-builder
  - prospecting-message-crafter
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Verbatim prospect pushback + context (channel, prior statement, your call objective)"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document directory"
discovery:
  goal: "Produce a complete Anchor-Disrupt-Ask turnaround script, a fallback script, and a dead-horse checkpoint for the given prospect pushback"
  tasks:
    - "Gather the verbatim pushback and call context from the user"
    - "Classify the pushback as Reflex Response, Brush-Off, or Objection using the three-type taxonomy"
    - "Draft the Anchor statement (neurological buy-time mechanism)"
    - "Draft the Disrupt statement (unexpected, non-combative pull response)"
    - "Draft the Ask (assumptive, specific, no pause)"
    - "Prepare a fallback script for the second RBO attempt"
    - "Apply the 2-RBO dead-horse checkpoint"
    - "Write the complete output to rbo-turnaround-script.md"
  audience:
    roles: [sdr, bdr, ae, founder-self-seller]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "Prospect just said 'I'm not interested' and the rep doesn't know what to say"
      - "Rep is building a script library for the 6 most common pushback types before a call block"
      - "Current response to 'we're happy with our provider' is 'oh, well, sorry to bother you'"
      - "Rep knows they're arguing with prospects instead of disrupting expectations"
      - "Rep is unsure whether to keep pushing or move on after two failed turnarounds"
      - "Rep says 'I understand' repeatedly and wonders why it isn't working"
    prerequisites: []
    not_for:
      - "Writing the initial cold call opener (use cold-call-opener-builder)"
      - "Building the bridge/because message nucleus (use prospecting-message-crafter)"
      - "Handling gatekeeper access blocks — those are structural, not RBOs (use gatekeeper-navigator)"
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
      - "Classifies pushback as Reflex Response, Brush-Off, or Objection — three types with different response logic"
      - "Produces Anchor-Disrupt-Ask structure, not a generic objection rebuttal"
      - "Names the neurological rationale for the Anchor (amygdala / fight-or-flight buy-time)"
      - "Enforces the 2-RBO rule: attempt twice, then gracefully disengage"
      - "Rejects 'I understand' as insincere filler with explicit rationale"
      - "Uses Judo/disrupt metaphor — pull not push, yielding way not combat"
      - "Includes a fallback script for the second turnaround attempt"
      - "Provides the dead-horse checkpoint and the 'NEXT' recovery trigger"
    what_baseline_misses:
      - "Treats all pushback the same — no distinction between habitual script vs conscious avoidance vs genuine objection"
      - "Responds to 'not interested' by explaining the product or arguing value — which creates resistance"
      - "Uses 'I understand' as an empathy filler, which signals insincerity not listening"
      - "Has no rule for when to stop — either gives up too early or fights past two RBOs"
      - "Does not produce a ready-to-use script — gives advice instead of a turnaround template"
      - "Does not know the amygdala / neocortex rationale for why the Anchor works neurologically"
---

# Prospecting Objection Handler

## When to Use

Your prospect just said something that made you want to hang up. "I'm not interested." "I'm really
busy." "We're happy with who we have." "Just send me some information."

This skill takes that exact pushback, classifies it, and produces a complete three-step
**Anchor-Disrupt-Ask** turnaround script you can deliver in the next five seconds — plus a fallback
script for if the first attempt doesn't work, and a clear checkpoint for when to gracefully exit.

Use this skill when:
- You are about to run a prospecting block and want scripted turnarounds for the six most common
  pushback types before you pick up the phone
- You just got a pushback you didn't handle well and want to know what you should have said
- You are unsure whether what you heard was a real objection or just an automatic reflex
- You keep "I understand"-ing your way through calls and it isn't working
- You need to know when two failed turnarounds means it is time to move on

**Where this skill fits in the call:** `cold-call-opener-builder` delivers your Five-Step opener.
The moment you finish the ask in Line 5, silence follows. If the prospect breaks that silence with
pushback, this skill takes over.

## Context & Input Gathering

Before building the turnaround, gather the following from the user:

**Required:**
1. The prospect's exact words (verbatim if possible — phrasing determines classification)
2. Your call objective (appointment / qualifying information / direct sale)
3. Channel (phone / in-person / email reply / social reply)

**Recommended:**
4. What you said just before the pushback (the opener line that triggered the response)
5. Whether you have spoken to this prospect before (first contact vs. follow-up)

**If no prior call context exists:** Proceed directly to Step 1 with the pushback text alone.

## Process

### Step 1 — Classify the Pushback

Read the verbatim pushback and assign it to one of three types. The type determines your entire
response strategy — using the wrong intervention for the wrong type will either escalate resistance
or miss the opening entirely.

**Type 1: Reflex Response**
The prospect is running an automatic script. They do not consciously mean what they said. The
words come from conditioned habit — the same phrase they use every time a salesperson calls.

*Behavioral signatures:* fast delivery, no reasoning, no "because," often not literally true
("I'm just running out the door" when they are sitting at their desk).

*Common examples:* "I'm not interested." / "We're all set." / "I'm too busy." / "We're happy."

*Why it is not a real objection:* Blount's opening illustration — he walked into a store and told
the salesperson "I'm just looking" when he actually needed help finding a product. The reflex fires
before the logical brain engages. (Blount, Ch. 16, p. 199)

**Type 2: Brush-Off**
The prospect is consciously trying to end the interaction without confrontation. They are not
lying because they disrespect you — they are lying because past salespeople have punished
honest responses with argument. The brush-off is a kindness disguised as a deferral.

*Behavioral signatures:* polite deferral tone, future-promise language, no commitment date, vague
action item.

*Common examples:* "Call me later." / "Get back to me in a month." / "Just send me some information."

*Why it is not a real commitment:* Seth Godin's diagnosis, cited by Blount: "Prospects lie because
salespeople have trained them to." Honest responses are met with pressure; deferral is safer.
(Blount, Ch. 16, p. 200)

**Type 3: Objection**
The prospect is giving you a truthful, logical rebuttal. It comes with a "because." It is rarer
than Types 1 and 2, and it actually opens a door — real objections reveal real information about
the prospect's world.

*Behavioral signatures:* slower delivery, specific reasoning, named constraint, logical structure.

*Common examples:* "We just signed a two-year contract with your competitor because they gave us a
major discount." / "Our budgets are frozen until Q3 because we just completed an acquisition." /
"I can't meet next week because I'll be at a conference."

*Why this type is different:* A genuine objection is a prospect telling you the truth. That earns
a different response — one that acknowledges the constraint, reframes the timing or stakes, and
asks for something appropriate given the reality they just described. (Blount, Ch. 16, p. 201)

**Why classify first:** A reflex response needs disruption of an automatic pattern. A brush-off
needs a challenge to a false commitment. A genuine objection needs engagement with a real
concern. The same turnaround does not work across all three. Misclassifying causes you to argue
with a habit (useless), accept a fake deferral as a real promise (self-defeating), or dismiss real
information (damaging). (Blount, Ch. 16, pp. 199–202)

---

### Step 2 — Draft the Anchor

The Anchor is the first thing you say after the pushback. Its job is neurological, not rhetorical.

When a prospect says no, your amygdala (the brain's threat-detection system) fires a fight-or-
flight response before your logical brain (neocortex) can evaluate the situation. This is the same
physiological cascade that would fire if you encountered a bear on a trail. The prospect saying no
and a bear on the trail feel identical to your nervous system — your logical brain cannot
distinguish between them fast enough to prevent the emotional reaction.

The Anchor gives your neocortex a millisecond to catch up. It is a brief, low-conflict statement
that you have rehearsed until it fires automatically — buying the moment your emotional brain
needs to stand down so your logical brain can take over the call.

**Anchor principles:**
- One line. Calm tone. No argument. No sarcasm.
- Agree with the prospect or acknowledge their statement without resistance
- Should feel like you expected this response — because you did
- Must be rehearsed until it sounds natural, not scripted

**Anchor patterns by type:**
- Reflex ("I'm busy"): "That's exactly why I called." / "I figured you would be."
- Brush-Off ("Send me info"): "Happy to. Let me ask you one quick thing first."
- Objection ("We just signed with a competitor"): "That makes perfect sense given that."

**Why the Anchor is not a tactic:** It is a neurological mechanism. You are not agreeing with the
prospect to manipulate them — you are giving your own brain the time it needs to operate from
logic rather than fear. Without the Anchor, you stumble, overexplain, or go defensive. The Anchor
is self-regulation before persuasion. (Blount, Ch. 16, pp. 204–205)

---

### Step 3 — Draft the Disrupt

The Disrupt is the core of the turnaround. It is a statement or question that does something the
prospect has been conditioned not to expect from a salesperson: it does not fight.

Every prospect who has dealt with salespeople carries a mental model of what happens when they
say no: the salesperson argues, pushes harder, asks "why not?", or tries to rationalize them out
of their position. The Disrupt breaks that pattern entirely. It is verbal judo — "the gentle or
yielding way" — achieving your objective without causing injury or generating resistance.

**The mechanism:** When humans encounter something that violates their expectation, they pause
and pay attention. That pause is your opening.

**Disrupt patterns by type:**

*For Reflex Responses — agree and reframe:*
- "I'm not interested" → "That makes sense. Most people aren't until they see [specific outcome]."
- "I'm happy with who I have" → "Awesome. If you're happy, you shouldn't even think about
  changing. All I want to do is [low-stakes request that isn't 'sell you something']."
- "I'm too busy" → "I figured you would be, so I want to find a time that's more convenient."

*For Brush-Offs — call the bluff, force engagement:*
- "Send me some information" → "Tell me specifically what you're looking for and I'll make sure
  what I send is actually relevant to your situation."
- "Call me in a month" → "Happy to. What will be different in a month that makes it a better time?"

*For Objections — acknowledge, reframe the stakes:*
- "We're locked into a contract" → "That's fair. Most of the clients I work with now were in the
  same situation when we first talked. I'm not looking to disrupt anything — I'd just like to be
  the one you call when the renewal comes up. Could we spend 10 minutes so you have a reference
  point when that happens?"

**Words to avoid:** "I understand." When you say "I understand," you sound like every other
salesperson who uses that phrase as insincere filler before launching the next pitch. It signals
you are not listening and do not care. Your prospect's brain is not ready for you to agree with
them — it is ready for you to argue. Use that expectation; do not confirm it. (Blount, Ch. 16, p. 206)

**Why disrupt not defeat:** You cannot argue another person into believing they are wrong. Every
salesperson who has "overcome objections" by pushing has either gotten a yes in spite of the
argument, or — far more often — generated more resistance and lost the prospect permanently.
Overcoming creates animosity. Disrupting creates curiosity. Pull, do not push. (Blount, Ch. 16, pp. 203–205)

---

### Step 4 — Draft the Ask

Immediately after the Disrupt, ask again for what you originally came for. No hesitation, no
pause, no preamble. The Ask in the turnaround is structurally identical to the Ask in your opener:
assertive, specific, assumptive.

**Why no pause between Disrupt and Ask:** A pause signals that you are waiting for their
permission to continue. You are not asking permission — you are assuming yes and asking for a
specific commitment. The absence of hesitation is itself a confidence signal that influences the
prospect's response. (Blount, Ch. 16, p. 206)

**Ask patterns:**
- Appointment: "How about we get together Thursday at 3:00 PM instead?"
- Qualifying information: "Can you tell me more about your situation and when [decision process]
  typically kicks off?"
- Low-stakes request: "Can I get 10 minutes on your calendar next Tuesday at 10 AM?"

**Match the Ask to your objective and the pushback type:** After a genuine objection, do not ask
for the same full meeting you originally wanted — that reads as tone-deaf. Ask for something
smaller that fits the constraint they described.

---

### Step 5 — Prepare the Fallback and Apply the 2-RBO Rule

About half the time, your first turnaround will produce a second RBO instead of a yes. This is
normal — and it is often useful. The second RBO tends to be closer to the truth than the first.
If the first was "I'm not interested" (reflex), the second might be "We actually just renewed with
a competitor" (objection). That is information.

**Fallback preparation:**
- Draft a second Anchor-Disrupt-Ask for the most likely second pushback
- The second Disrupt should be lighter — lower stakes, shorter ask, less pressure
- The tone shifts from "get the meeting" to "get the permission to come back"

**The 2-RBO Rule:** If you have attempted two full Anchor-Disrupt-Ask turnarounds and the
prospect has not moved, do not attempt a third. Gracefully disengage.

*Graceful exit script:* "I completely understand — I clearly caught you at a bad time. I'll reach
back out when the timing is better. Have a great day."

**Why stop at two:** After two turnarounds, continuing communicates that you did not hear
them, that you will ignore their stated preferences, and that future contact will feel like
harassment. Pushing past two RBOs destroys the relationship and poisons future contact attempts
with the same prospect. The prospect will move on the moment you hang up — they will not
remember this interaction the way you will. (Blount, Ch. 16, pp. 206, 208–210)

**The Dead-Horse Checkpoint:** Before attempting a second turnaround, ask yourself: is there
any signal in what they said that indicates genuine openness, or is this person actively ending the
conversation? If they are hanging up, screaming, or have explicitly said "never call me again" —
that is a dead horse. Dismount immediately. Log it, say NEXT, and dial the next number. The
horse is dead; beating it costs you money, time, and emotional reserves. (Blount, Ch. 16, pp. 208–210)

---

### Self-Check Before Writing Output

Before finalizing, verify the turnaround script passes all five checks:

- [ ] **Pushback is classified** — explicitly labeled as Reflex Response, Brush-Off, or Objection with rationale
- [ ] **Anchor is present and brief** — one line, non-argumentative, rehearsal-ready
- [ ] **Disrupt does not argue** — agrees, reframes, or calls the bluff; does not explain why the prospect is wrong
- [ ] **"I understand" is absent** — not in the Anchor, not in the Disrupt, not anywhere in the script
- [ ] **Ask is specific and assumptive** — day/time or concrete request; no hedging or passive phrasing

If any check fails, revise the failing element before writing output.

---

### Write Output

Write the complete turnaround to `rbo-turnaround-script.md` in the working directory. Include:

1. **Classification** — pushback type + one-sentence rationale
2. **Primary turnaround** — Anchor, Disrupt, and Ask labeled separately, assembled into a read-aloud script
3. **Fallback script** — a second lighter Anchor-Disrupt-Ask for the most likely second pushback
4. **Dead-horse checkpoint** — explicit note on when to exit and the graceful exit line
5. **Anti-pattern notes** — any phrases avoided and why

## Inputs

| Input | Required | Source |
|---|---|---|
| Verbatim prospect pushback | Yes | User pastes or describes |
| Call objective | Yes | User states or from `prospecting-objective-plan-{date}.md` |
| Channel (phone / in-person / email / social) | Yes | User states |
| What you said before the pushback | Recommended | User describes |
| Prior contact history | Recommended | User states |

## Outputs

| Output | Location | Description |
|---|---|---|
| `rbo-turnaround-script.md` | Working directory | Classification + primary Anchor-Disrupt-Ask + fallback + dead-horse checkpoint |
| Anti-pattern notes | Inline in conversation | What was avoided and why |

## Key Principles

**1. Classify before responding.** A reflex response, a brush-off, and a genuine objection each
requires a different intervention. Treating them identically means you will argue with a habit,
accept a fake promise, or dismiss real information. Classification takes two seconds and changes
everything. (Blount, Ch. 16, pp. 199–202)

**2. The Anchor is neurological, not tactical.** You are not agreeing with the prospect to be
clever. You are giving your own amygdala a millisecond to stand down so your neocortex can
run the call. Without the Anchor, fight-or-flight produces stumbling, over-explaining, and
defensive tone — all of which telegraph weakness and generate more resistance. (Blount, Ch. 16, p. 205)

**3. Disrupt, do not defeat.** The universal law: you cannot argue another person into believing
they are wrong. Pushing creates counter-pressure. Disrupting creates a gap in the expected
pattern — and in that gap, curiosity and movement become possible. Verbal judo: the gentle,
yielding way wins without combat. (Blount, Ch. 16, pp. 203–205)

**4. Never say "I understand."** It signals insincerity. Every prospect has heard "I understand"
from a salesperson who immediately launched into a pitch about why they are wrong. The phrase
has been conditioned into meaninglessness. Avoid it entirely. Use the Anchor instead — it does
the same emotional work without the baggage. (Blount, Ch. 16, p. 206)

**5. The 2-RBO rule protects the relationship.** Two attempts is professional persistence.
Three attempts is harassment. After two failed turnarounds, disengage gracefully, log accurately,
and prospect again on a future date. Prospects do not remember the call the way you do — what
feels like a permanent failure is usually a bad timing issue that a future call can reset.
(Blount, Ch. 16, pp. 206–210)

**6. Scripts must be rehearsed until they sound natural.** A turnaround read robotically
from memory is worse than no turnaround at all. Politicians read teleprompters fluently because
they rehearse until the words become their own. Practice the Anchor and Disrupt aloud, with a
recorder or a role-play partner, until they flow without hesitation. The script is the raw
material; rehearsal turns it into a weapon. (Blount, Ch. 16, p. 202)

## Examples

---

### Example 1 — "I'm busy" (Reflex Response)

**Prospect says:** "Look, I'm busy."

**Classification:** Reflex Response. The prospect is running an automatic script. This response
fires before their logical brain evaluates the call. "Busy" may be literally true, but the
response is not a considered decision — it is a habit. Do not argue that you won't take long.
That confirms their expectation of a fight.

**Primary Turnaround:**

| Element | Script |
|---|---|
| Anchor | "That's exactly why I called." |
| Disrupt | "I figured you would be — I want to find a time that's actually convenient for you, not interrupt you right now." |
| Ask | "How about we set something for Thursday at 3:00 PM instead?" |

**Read-aloud (no pause between elements):**
> "That's exactly why I called. I figured you would be — I want to find a time that's actually
> convenient for you, not interrupt you right now. How about Thursday at 3:00 PM?"

**Fallback (if they push back again):**
> "Absolutely. I won't keep you. Can I just get two minutes on Thursday to introduce myself — if
> it's not relevant, I'll let you go immediately. How about 3:00 PM?"

**Dead-horse checkpoint:** If after two attempts they say "No, really, I'm not interested in
anything right now" with finality — disengage. "No problem at all. I'll reach back out when the
timing is better. Have a great rest of your day."

---

### Example 2 — "We're not interested" (Reflex Response — stronger flavor)

**Prospect says:** "We're not interested."

**Classification:** Reflex Response. The stronger version of the same automatic script. This fires
before any evaluation of what is being offered. The prospect is not saying they have evaluated
your proposition — they are saying "I don't want a conversation with a salesperson right now."

**Primary Turnaround:**

| Element | Script |
|---|---|
| Anchor | "You know, that's what a lot of my current clients said the first time I called." |
| Disrupt | "Most people aren't interested before they see how much I can help them. I don't know if what I do is relevant to your situation — but doesn't it make sense to spend 15 minutes to find out?" |
| Ask | "How about Friday at 2:00 PM?" |

**Read-aloud:**
> "You know, that's what a lot of my current clients said the first time I called. Most people
> aren't interested before they see how much I can help them. I don't know if what I do is
> relevant to your situation — but doesn't it make sense to spend 15 minutes to find out?
> How about Friday at 2:00 PM?"

**Fallback (if second RBO):**
> "I completely understand. What if we kept it to a 10-minute call — just enough so you can tell
> me it's not a fit? How does Thursday morning look?"

---

### Example 3 — "We're really happy with our current provider" (Reflex Response / Brush-Off)

**Prospect says:** "We're really happy with our current provider."

**Classification:** Reflex Response with Brush-Off characteristics. The "we're happy" script is
among the most common automatic responses in business-to-business prospecting. The prospect is
not reporting a result of comparing you to their current provider — they are signaling they want
to end the conversation without conflict.

**Primary Turnaround:**

| Element | Script |
|---|---|
| Anchor | "That's fantastic!" |
| Disrupt | "Anytime you're getting great rates and great service, you should never think about changing. All I want to do is come by and get to know you a little better — and even if it doesn't make sense to do business with me right now, I can at least give you a competitive benchmark that will help keep your current provider honest." |
| Ask | "How about I stop by on Tuesday at 11:30 AM?" |

**Read-aloud:**
> "That's fantastic! Anytime you're getting great rates and great service, you should never
> think about changing. All I want to do is come by and get to know you a little better — and
> even if it doesn't make sense to do business with me right now, I can at least give you a
> competitive benchmark that will help keep your current provider honest. How about I stop by
> on Tuesday at 11:30 AM?"

**Fallback (if they push back again):**
> "Fair enough. I'll check back in with you at renewal time — when does your current contract
> come up? I'd like to make sure you have options when the time is right."

**Dead-horse checkpoint:** After two clean attempts, if they indicate no appetite for any contact,
log the renewal date if revealed, note "happy with provider — recontact at renewal," and say
NEXT.

---

## References

The full RBO library (20+ common objections with Anchor-Disrupt-Ask templates organized by type)
is in `references/rbo-turnaround-library.md`. Use that file to build a complete script library
before a call block.

Additional supporting material:
- `references/rbo-classification-guide.md` — extended classification examples and edge cases
  (how to handle ambiguous pushbacks, gatekeeper-adjacent RBOs, hybrid type responses)
- `references/dead-horse-protocol.md` — when to disengage, how to log, and how to re-approach
  the same prospect in a future cycle without poisoning the relationship

**Source chapter:** Blount, Jeb. *Fanatical Prospecting*, Chapter 16 "Turning Around RBOs:
Reflex Responses, Brush-Offs, and Objections" (PDF pp. 196–210). Three-type RBO taxonomy:
pp. 199–202. Anchor-Disrupt-Ask framework: pp. 204–206. Three annotated example scripts:
pp. 207–208. Dead-horse principle: pp. 208–210.

**Referenced frameworks:**
- Brown, Brené. *The Power of Vulnerability* — uncertainty and emotional exposure as the root
  of sales vulnerability (cited in Blount, Ch. 16, p. 196)
- Godin, Seth — prospects lie because salespeople have trained them to; honest responses are
  punished with argument (cited in Blount, Ch. 16, p. 200)
- Judo metaphor: "gentle or yielding way" — achieving objective without combat (Blount, Ch. 16,
  p. 204)

## License

Content derived from *Fanatical Prospecting* by Jeb Blount (Wiley, 2015). This skill is licensed
under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/).
You are free to share and adapt this material provided you give appropriate credit to Jeb Blount
and BookForge, and distribute any derivative works under the same license.

## Related BookForge Skills

This skill handles pushback that occurs after the opener is delivered. Build the opener first:

```
clawhub install bookforge-cold-call-opener-builder
```

Build the message nucleus that powers the opener:

```
clawhub install bookforge-prospecting-message-crafter
```

Browse the full Fanatical Prospecting skill set:
[bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
