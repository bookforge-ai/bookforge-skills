---
name: text-prospecting-sequence-builder
description: |
  Build a situation-appropriate text prospecting sequence with timing, tone, and per-touch templates.

  Trigger this skill when you need to:
  - Text a prospect after a networking event or trade show meeting ("text message prospecting", "text after meeting")
  - Follow up on a hot inbound lead via SMS ("text a prospect", "SMS sales")
  - Rescue a no-show appointment with a text ("post-no-show text")
  - Send a text after leaving a voicemail ("text after voicemail", "post-vm text")
  - Know when it is and is not appropriate to text a prospect ("when to text a prospect")
  - Build a text sequence with correct timing and cadence ("text sequence", "mobile outreach")
  - Check whether a draft text message violates the 7 professional text rules
  - Understand the Bridge-Because pattern adapted for short-form text

  NOT for: writing a cold text to a complete stranger (text requires permission earned through prior contact —
  use cold-call-opener-builder or prospecting-message-crafter first). This skill assumes you have a legitimate
  reason to text: you met the person, they engaged with your content, or they came in as a warm inbound lead.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/text-prospecting-sequence-builder
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
      - 20
tags:
  - sales
  - prospecting
  - text-messaging
  - sms
  - sdr
  - bdr
depends-on:
  - prospecting-message-crafter
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Prospect context + situation type (post-networking / hot-inbound / post-voicemail / post-no-show) + what has been agreed to so far (if anything)"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document directory — agent reads user-provided context file or inline description and writes the text sequence to text-sequence-output.md"
discovery:
  goal: "Produce a situation-appropriate text sequence with per-touch message copy, timing, and rationale that passes the 7-rule professional text check"
  tasks:
    - "Verify the permission/familiarity gate: confirm prior contact exists before building any sequence"
    - "Identify the situational protocol: post-networking / hot-inbound / post-voicemail / post-no-show"
    - "Draft each touch using the Bridge-Because pattern adapted for short-form text"
    - "Set timing and cadence per the protocol (not too soon, not too many, not too formal)"
    - "Run the 7-rule anti-pattern check on every message before finalizing"
    - "Write the sequence to text-sequence-output.md"
  audience:
    roles: [sdr, bdr, ae, founder-self-seller]
    experience: beginner
  when_to_use:
    triggers:
      - "Just left a networking event and want to follow up via text within 24 hours"
      - "A hot inbound lead came in and you want to text before the trail goes cold"
      - "Left a voicemail and want to reinforce with a text"
      - "A prospect missed a scheduled appointment and you want to rescue it"
      - "Someone asks what to say in a text to a prospect"
      - "Checking whether a drafted text is professional enough to send"
    prerequisites:
      - "Prior contact with the prospect through at least one other channel (meeting, phone call, email, social interaction)"
    not_for:
      - "Texting a cold prospect with zero prior contact (zero familiarity = spam, not prospecting)"
      - "Building multi-touch email cadences (use cold-email-writer)"
      - "Scripting a live phone call (use cold-call-opener-builder)"
      - "Repairing a message bridge or bridge type (use prospecting-message-crafter)"
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
      - "Enforces the familiarity gate — refuses to build a cold text sequence (no prior contact = no text)"
      - "Names the 4 situational protocols (post-networking / hot-inbound / post-voicemail / post-no-show) and routes to the correct one"
      - "Applies Bridge-Because pattern in short-form text: personalized context + because + direct ask"
      - "Enforces the 7 professional text rules: identify yourself, complete sentences, 1-4 sentences max, no abbreviations, full URLs only, proof before sending, track numbers"
      - "Sets correct timing per protocol (within 24 hours for networking; immediate for hot inbound)"
      - "Caps the sequence at 2 text attempts before shifting to phone/email"
      - "Checks for direct solicitation language in nurture/engagement texts and flags it"
    what_baseline_misses:
      - "Texts cold prospects without establishing familiarity first"
      - "Does not identify the situation type — writes one generic text for every scenario"
      - "Uses emoji, slang, abbreviations, or shortened links"
      - "Writes more than 4 sentences — texts that feel like emails"
      - "Does not identify themselves (assumes prospect has their number saved)"
      - "Sends texts three or four times when no response — creating ill will"
      - "Includes a direct solicitation in a nurture or engagement text"
---

# Text Prospecting Sequence Builder

## When to Use

Text is a **permission-earned channel**. You can call a stranger, email a stranger, and meet a stranger in person — but you almost never text a stranger. Text occupies the same mental space as family, friends, and close colleagues. When a salesperson lands there uninvited, they are not a prospector — they are spam.

This skill builds text sequences for situations where permission has already been established through prior contact:

- You met someone at a networking event, trade show, or conference and agreed to connect
- A warm inbound lead came in (download, demo request, referral) and you want to reach them while intent is high
- You left a voicemail and want to reinforce it on the same channel sweep
- A prospect missed a scheduled appointment and you want to quickly offer a rescue

**Do not use this skill to text a cold prospect.** If no prior contact exists, build a bridge first using `prospecting-message-crafter`, reach out by phone or email, and earn the familiarity that makes texting effective.

**Why text works when used correctly:** A Lead360 study of 3.5 million lead records found that a text sent alone converts at 4.8 percent. The same text sent after a phone contact increases conversion by 112.6 percent. Familiarity is the multiplier — not the message itself. (Blount, p. 256)

## Context and Input Gathering

Before building the sequence, gather or ask the user for:

**Required:**
1. Situation type — post-networking / hot-inbound / post-voicemail / post-no-show
2. What was agreed or communicated in the prior contact (vague "let's connect," confirmed appointment, inbound download, etc.)
3. Prospect's name and role
4. Anything personal or specific mentioned in the prior conversation (used to personalize)

**Recommended:**
5. What outcome you want from this text sequence (appointment / call / reschedule)
6. Any trigger event or relevant detail at the prospect's company (for hot-inbound or post-networking)

**If a draft text already exists:** read it, run the 7-rule check in Step 4, and revise before producing the sequence.

## Process

### Step 1 — Verify the Permission Gate

Before writing a single character, confirm prior contact exists. Ask:

> "Has there been at least one prior touchpoint with this prospect — an in-person meeting, a phone call, an email exchange, or a social media interaction?"

If the answer is no, **stop**. Direct the user to `cold-call-opener-builder` or `prospecting-message-crafter` to initiate contact through a more forgiving channel first. Texting a cold prospect creates immediate negative association and may result in the number being reported as spam.

**Why this gate matters:** The personal nature of the text channel is precisely what makes it powerful — and what makes unauthorized entry feel like a violation. A text from an unknown number asking for time feels like spam regardless of message quality. (Blount, p. 255)

### Step 2 — Identify the Situational Protocol

Route to the correct protocol based on what happened before this text:

| Situation | Protocol | Primary Goal |
|---|---|---|
| Met at networking event / trade show / conference | Post-Networking | Anchor the vague "let's get together" into a real appointment |
| Inbound lead (download, demo request, referral) | Hot-Inbound | Reach the lead while intent is high; set appointment or qualify |
| Left a voicemail and want to reinforce | Post-Voicemail | Increase the probability the prospect engages with your message |
| Prospect missed a scheduled appointment | Post-No-Show | Rescue the meeting without creating awkwardness |

Each protocol has a different timing, tone, and call-to-action. Do not mix them — a post-no-show text written in a hot-inbound tone feels pushy; a hot-inbound text written in a post-networking tone feels too casual for the urgency.

**Why situational routing matters:** Text messaging as a channel offers almost no room for error — a wrong tone at the wrong moment and the prospect ignores you permanently. Matching the text's energy to the situation's context maximizes the chance of a reply. (Blount, pp. 256-261)

### Step 3 — Draft the Sequence Using Bridge-Because in Short Form

For each touch in the sequence, build the message using the Bridge-Because pattern adapted for text constraints. Unlike a phone opener or email that has room for a full WIIFM-Bridge-Because-Ask arc, a text must compress this into 1-4 sentences.

**Text Bridge-Because structure:**
> [Identify yourself + company] + [personalized context that connects to their world] + [because: what's in it for them] + [specific ask]

Keep each message to **one to four sentences and under 250 characters when possible**. Complete sentences only — no abbreviations, no slang, no emoji.

**Protocol-specific sequence templates:**

---

**Post-Networking Protocol (5-step sequence):**

*Context: You met at an event, had a positive conversation, and made a vague agreement to connect.*

- **During the conversation (spoken, not texted):** Casually say: "Sounds good — I'll text you and we can get together." This pre-empts any later surprise that you are texting them. If the conversation was positive, they will not object.

- **Immediately after walking away (action, not text):** Send a personalized LinkedIn connection request from your phone. This anchors your name and face before the text arrives.

- **Touch 1 — Within 24 hours (text):**
  > "[Name], this is [Your Name] from [Company]. Great talking with you at [event] — [something specific from conversation]. I'd like to follow up on [what you discussed]. How about [specific day/time]?"

- **Touch 2 — One day later if no response (text):**
  > "[Name], [Your Name] from [Company] again — wanted to make sure my earlier text got through. How about [alternative specific day/time] to connect?"

- **If Touch 2 fails:** Shift to phone and email. Do not send a third text. Repeated texts without response create ill will. (Blount, p. 257)

- **Bonus action:** Send a handwritten note via mail within one week of the event. This stands out from everyone else who promised to follow up and didn't. (Blount, p. 257)

---

**Hot-Inbound Protocol (2-touch sequence):**

*Context: A warm lead came in via download, demo request, referral, or website form.*

- **Touch 1 — As soon as possible, ideally within minutes (text):**
  > "[Name], this is [Your Name] from [Company]. I saw you [downloaded / requested / were referred] — thanks for reaching out. I'd like to connect quickly. Are you available [specific day/time] for a brief call?"

- **Touch 2 — Next business day if no response (text):**
  > "[Name], [Your Name] from [Company]. Following up on my text from yesterday. I have time [specific day/time] — does that work for a quick call?"

- **If Touch 2 fails:** Move to phone and email follow-up. The inbound intent window closes fast — do not let text be your only channel for hot leads.

---

**Post-Voicemail Protocol (1-touch supplement):**

*Context: You just left a voicemail on the same prospecting sweep. The text reinforces the voicemail.*

- **Touch 1 — Immediately after leaving the voicemail (text):**
  > "[Name], this is [Your Name] from [Company] — I just left you a voicemail. [One-sentence reason for reaching out]. How about [specific day/time] for a brief call?"

Do not send a second text after a post-voicemail text. The voicemail and the text together are your combined touch. If neither gets a response, log it and move to the next prospect in your sequence.

---

**Post-No-Show Protocol (1-2 touch rescue):**

*Context: The prospect had a scheduled appointment and did not show up.*

- **Touch 1 — Within 15-30 minutes of the missed appointment (text):**
  > "[Name], this is [Your Name] from [Company] — I had us scheduled for [time] today. No worries if something came up. How about we reschedule to [specific day/time]?"

- **Touch 2 — Next day if no response (text):**
  > "[Name], [Your Name] from [Company]. Wanted to try once more on rescheduling our call — would [specific day/time] work?"

- **If Touch 2 fails:** Move to phone and email. Do not express frustration or passive-aggressiveness in any text. Tone in a no-show situation is especially fragile. (Blount, p. 257)

### Step 4 — Run the 7-Rule Anti-Pattern Check

Before finalizing any text in the sequence, check each message against these seven rules. Flag any violation and revise before outputting.

| Rule | What to check | Why it matters |
|---|---|---|
| 1. Identify yourself | Does the text start with your name and company? | Prospects rarely have your mobile number saved. Anonymity = spam. (Blount, p. 261) |
| 2. Professional tone, complete sentences | Are there fragments, sarcasm, or abrupt phrasing? | Text lacks vocal tone; incomplete sentences read as harsh or dismissive. (Blount, p. 261) |
| 3. 1-4 sentences, under 250 characters | Is the message longer than four sentences? | Text is not email. A wall of text signals lack of respect for the channel. (Blount, p. 261) |
| 4. No abbreviations or slang | Does the text include LOL, OMG, BTW, or any informal shorthand? | Abbreviations are unprofessional and may confuse the prospect. (Blount, p. 262) |
| 5. Full URLs only | If linking to an article or resource, is the full URL used? | Shortened URLs feel suspicious and reduce click trust. (Blount, p. 262) |
| 6. Proof before sending | Has the message been read aloud once before finalizing? | Text errors are irreversible and permanent. One re-read catches most mistakes. (Blount, p. 262) |
| 7. No direct solicitation in nurture or engagement texts | Does a nurture or engagement text ask for anything? | Nurture texts work because they give value with no ask. The moment you solicit, you break the pattern. (Blount, p. 261) |

**Additional anti-patterns to flag:**
- **Emoji** — do not use emoji in any prospecting text. The channel feels personal; emoji reads as unprofessional in a sales context. (Blount, p. 261)
- **Images or attachments** — text is not the channel for sending decks, images, or PDFs. This belongs in email.
- **More than 2 attempts without a response** — sending a third text signals desperation and creates ill will.

### Step 5 — Output the Sequence

Write the finalized sequence to `text-sequence-output.md` in the working directory. Include:

- The situation type and protocol selected
- Each touch with: message copy ready to send, timing instruction, and one-line rationale
- The 7-rule check result for each message (pass/flag)
- Any anti-patterns found in a user-provided draft and what was changed

## Inputs

| Input | Required | Source |
|---|---|---|
| Situation type (post-networking / hot-inbound / post-voicemail / post-no-show) | Yes | User states |
| Prior contact description (what was said, agreed to, or triggered) | Yes | User provides |
| Prospect name and role | Yes | User provides |
| Personalization detail from prior conversation | Recommended | User provides |
| Desired outcome (appointment / call / reschedule) | Recommended | User states |
| Existing draft text (if any) | No | User pastes inline |

## Outputs

| Output | Location | Description |
|---|---|---|
| `text-sequence-output.md` | Working directory | Complete sequence with per-touch copy, timing instructions, 7-rule check, and rationale |
| Anti-pattern diagnosis (if draft provided) | Inline in conversation | What was wrong, why, and what was changed |

## Key Principles

**1. Permission is everything.** Text is the most personal prospecting channel. Familiarity earned through prior contact is not a preference — it is a prerequisite. Without it, every text is spam regardless of message quality. (Blount, p. 255)

**2. Short-form only.** Text is not a delivery vehicle for pitches, case studies, or paragraphs. The constraint of 1-4 sentences forces the Bridge-Because pattern to its sharpest form: one personalized observation, one reason, one ask.

**3. Conversational, not salesy.** The tone that works in text is the same tone you would use with a recent acquaintance — warm, direct, low-pressure. Any hint of "buy now" language triggers the same reaction as a stranger texting you an ad.

**4. Two attempts maximum.** After two unreturned texts, shift channels. Repeated texts to someone who is not responding create resentment, not familiarity. The same prospect who ignores your second text may engage readily if you reach them by phone a week later.

**5. Reserve your best value-added content for text.** When nurturing a prospect over months, save the most relevant articles, insights, or news items for text rather than email. Text messages are read immediately; email competes with hundreds of others. (Blount, p. 260 — Matt case study)

## Examples

---

### Example 1 — Post-Networking Follow-Up (SDR / SaaS Event)

**Situation:** You met Jennifer, VP of Engineering at a mid-size fintech company, at a developer conference. You had a 10-minute conversation about her team's challenge with deployment reliability. She said "yeah, we should connect sometime." You did not explicitly agree on a time.

**During the conversation (spoken):** "Sounds great — I'll text you and we can find a time."

**Immediately after (action):** Send LinkedIn connection request from phone with a note: "Great meeting you at DevCon — looking forward to connecting."

**Touch 1 (within 24 hours):**
> "Jennifer, this is Alex from Reliably — great talking with you at DevCon about your deployment pipeline situation. I'd like to follow up on that. How about a 20-minute call Thursday at 2 PM?"

| Element | Content |
|---|---|
| Identify | Name + company in first line |
| Personalization | Event name + specific topic from conversation |
| Because | Implicit in the reference — she knows why connecting matters |
| Ask | Specific day and time, low-friction framing |
| 7-rule check | Pass: identifies self, complete sentences, under 4 sentences, no abbreviations, no links, proofed |

**Touch 2 (next day, no response):**
> "Jennifer, Alex from Reliably again — making sure my text got through. Also open Thursday at 4 PM or Friday morning if either of those works better."

**If no response after Touch 2:** Shift to phone call and email. Do not text again.

---

### Example 2 — Hot Inbound After Content Download (BDR / Marketing Automation)

**Situation:** Michael, Director of Marketing at a B2B software company, downloaded your guide on email deliverability at 9:47 AM. This is a warm inbound — intent is high right now.

**Touch 1 (within minutes of the download):**
> "Michael, this is Sarah from SendPath — I saw you downloaded our email deliverability guide. Happy to walk you through how we've helped marketing teams in your space improve send rates by 40+%. Are you free for a quick call today at 2 PM or tomorrow at 10?"

| Element | Content |
|---|---|
| Identify | Name + company |
| Bridge | References the specific download — shows you are paying attention |
| Because | Specific outcome (40%+ send rate improvement) relevant to their role |
| Ask | Two specific time options — assumptive, not passive |
| 7-rule check | Pass: complete sentences, under 250 chars, no slang, no shortened links, proofed |

**Touch 2 (next business day, no response):**
> "Michael, Sarah from SendPath. Following up on my text from yesterday — still happy to share what we're seeing with deliverability for B2B marketing teams. Does tomorrow at 10 AM or Thursday at 3 PM work for a quick call?"

---

### Example 3 — Post-No-Show Appointment Rescue

**Situation:** David, Operations Director at a logistics company, was scheduled for a 30-minute discovery call at 11 AM today. He did not join. You do not know why — it may have been an emergency, a calendar conflict, or he simply forgot.

**Touch 1 (15-30 minutes after the missed appointment):**
> "David, this is Marcus from FlowOps — I had us scheduled for 11 AM today. No worries if something came up. How about we reschedule to Thursday at 11 AM or Friday at 2 PM?"

| Element | Content |
|---|---|
| Tone | Neutral and low-pressure — no frustration, no passive aggression |
| Identify | Name + company, not assumed |
| Ask | Two specific alternatives, assumptive not apologetic |
| 7-rule check | Pass: identifies self, complete sentences, 2 sentences, no slang |

**Touch 2 (next day, no response):**
> "David, Marcus from FlowOps again. Wanted to try once more on rescheduling — would Thursday at 11 AM work, or should I reach out by email to find a better time?"

The offer to switch to email signals respect for their communication preference and often prompts a quick reply.

---

## References

Detailed supporting materials in the `references/` folder (if extended):

- `references/bridge-types-and-templates.md` — full Bridge-Because templates by situation type
- `references/7-rules-text-checklist.md` — printable pre-send checklist for the 7 professional text rules
- `references/multi-channel-sequence-map.md` — how text integrates within phone-email-social prospecting campaigns

**Source chapter:** Blount, Jeb. *Fanatical Prospecting*, Chapter 20 "Text Messaging" (pp. 253-262 / PDF pp. 253-262).

**Referenced research:** Lead360 study of 3.5 million lead records from 400+ companies — text following phone contact increases conversion by 112.6 percent vs. text sent alone at 4.8 percent (cited in Blount, p. 255-256).

**Case study reference:** Matt's 9-month text nurture campaign — reserve best value-added content for text, use non-product articles to maintain top-of-mind engagement without direct solicitation (Blount, pp. 259-260).

**Dependent skill:** This skill builds text sequences that implement the Bridge-Because pattern produced by `prospecting-message-crafter`. If you do not yet have a bridge or because for this prospect, build the message nucleus there first.

## License

Content derived from *Fanatical Prospecting* by Jeb Blount (Wiley, 2015). This skill is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt this material provided you give appropriate credit to Jeb Blount and BookForge, and distribute any derivative works under the same license.

## Related BookForge Skills

- `prospecting-message-crafter` — **prerequisite hub skill**: build the Bridge-Because message nucleus before deploying it via text. This skill is the channel adapter; message-crafter is the content engine.
- `cold-call-opener-builder` — deploys the Bridge-Because in the 5-step telephone framework; use when text fails to get a response after 2 attempts
- `cold-email-writer` — builds multi-touch email sequences; use alongside text in a balanced multi-channel prospecting system
- `prospecting-objective-setter` — defines the correct ask (appointment / qualifying info / close) that text sequences must end with
- `balanced-prospecting-cadence-designer` — maps text into a full multi-channel prospecting cadence so no single channel is over-relied upon
