---
name: gatekeeper-navigator
description: |
  Navigate any gatekeeper situation — choose bypass vs befriend, apply the right technique, and
  draft scripts that pass the anti-manipulation check.

  Trigger this skill when you need to:
  - Get past a receptionist or administrative assistant who is blocking access to a decision maker
  - Reach a decision maker when you don't know their name, title, or direct contact information
  - Figure out whether to bypass a gatekeeper or build a relationship with them
  - Apply the sales-help-sales hack to reach a hard-to-reach prospect
  - Use the calling-other-extensions (go-around-back) technique to extract a DM name
  - Draft respectful, transparent scripts for working with gatekeepers on recurring accounts
  - Check a gatekeeper approach for manipulation, pretending, or bulldozing anti-patterns
  - Decide whether LinkedIn flanking, early/late calls, or in-person approaches fit your situation
  - Stop getting hung up on or added to a do-not-help list
  - Turn a hostile receptionist into a calendar ally over multiple visits

  NOT for: turning around a reflex response after you've already reached the prospect (use
  prospecting-rbo-turnaround), building the full 5-step phone call script once you're through
  (use cold-call-opener-builder), or crafting the bridge and because for the call itself
  (use prospecting-message-crafter). This skill handles the access layer — getting to the
  person who can say yes.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/gatekeeper-navigator
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
      - 17
tags:
  - sales
  - prospecting
  - gatekeeper
  - cold-calling
  - sdr
  - bdr
depends-on:
  - prospecting-message-crafter
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Description of the gatekeeper situation + target prospect info + what has already been tried"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document directory"
discovery:
  goal: "Produce a recommended technique + scripts + anti-pattern warnings for the specific gatekeeper situation"
  tasks:
    - "Diagnose the gatekeeper situation: persona, level of resistance, prior attempts, account type"
    - "Decide bypass vs befriend using explicit criteria (one-shot vs ongoing, enterprise vs SMB)"
    - "Select the most appropriate technique from the technique library"
    - "Draft scripts using the Bridge-Because pattern from prospecting-message-crafter"
    - "Run anti-pattern audit: no manipulation, no pretending, no bulldozing"
    - "Write output to gatekeeper-navigator-output.md"
  audience:
    roles: [sdr, bdr, ae, founder-self-seller]
    experience: beginner
  when_to_use:
    triggers:
      - "Receptionist or admin is blocking access and won't connect you to the decision maker"
      - "You don't know the decision maker's name or contact information"
      - "You have been hung up on or told 'we don't give out that information'"
      - "Repeated calls are failing to get through to the right person"
      - "You want to know whether to call early/late, use LinkedIn, go in-person, or press the sales extension"
      - "You are prospecting an enterprise account and need a name before you can call"
      - "You want to befriend a receptionist on a recurring account you call regularly"
    prerequisites: []
    not_for:
      - "Handling a reflex response or brush-off after you've reached the prospect (use prospecting-rbo-turnaround)"
      - "Building the full 5-step phone call opening once you're through (use cold-call-opener-builder)"
      - "Crafting the WIIFM bridge and because for the conversation itself (use prospecting-message-crafter)"
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
      - "Names the sales-help-sales hack and explains when to use it"
      - "Names the calling-other-extensions hack and shows Evan's verbatim dialogue"
      - "Names the go-around-back technique for in-person prospecting"
      - "Rejects manipulation/pretending anti-patterns with explicit reasoning"
      - "Chooses bypass vs befriend using explicit account-type and access criteria"
      - "Uses respect-based engagement (connect, ask for help, hold the cheese) for ongoing accounts"
      - "Applies the Bridge-Because pattern from prospecting-message-crafter to gatekeeper scripts"
    what_baseline_misses:
      - "Treats gatekeeper navigation as a tricks problem — tries schemes that destroy credibility"
      - "Does not distinguish bypass (new conquest) from befriend (ongoing/recurring)"
      - "Does not know the sales-help-sales or calling-other-extensions hacks"
      - "Does not know the please-twice or hold-the-cheese rules"
      - "Produces a manipulative or deceptive approach without flagging the anti-pattern"
---

# Gatekeeper Navigator

## When to Use

You are trying to reach a decision maker and a gatekeeper — receptionist, administrative assistant, or automated phone system — is standing between you and the person who can say yes.

There are no tricks that reliably work. Gatekeepers are not obstacles to be defeated; they are people assigned the job of protecting someone's time. Your success depends on good manners, likeability, and people-savvy — and, when the direct path is blocked, on knowing which legitimate bypass technique fits the situation.

Use this skill when:
- You do not have the decision maker's name, title, or direct line
- A receptionist or admin is refusing to provide contact information or connect you
- You have been hung up on or added to the mental "do not help" list
- You need to decide whether to try a bypass route or invest in building the gatekeeper relationship
- You are calling a strategic account regularly and want to turn the gatekeeper into a calendar ally

**This skill handles the access layer.** Once you are through and speaking to the prospect, switch to `cold-call-opener-builder` for the 5-step telephone framework and `prospecting-message-crafter` for the bridge and because.

## Context & Input Gathering

Before proceeding, gather (or ask the user for) the following:

**Required:**
1. Target prospect's company, department, and suspected role (e.g., "VP of Procurement at a large grocery chain HQ")
2. What gatekeeper type is blocking you: receptionist/switchboard, personal administrative assistant, or automated phone system
3. What has already been tried (direct request to connect, pleas, online search, LinkedIn)
4. Account type: is this a new conquest (one-shot attempt), or an ongoing account you visit or call regularly?

**Recommended:**
5. Do you have any partial information — a department name, a first name, a title, or an employee name from a prior call?
6. What channels are available: phone, in-person access, LinkedIn, email?
7. Is the gatekeeper a blocker on the switchboard (lower-level) or a dedicated personal assistant to the decision maker?

## Process

### Step 1 — Diagnose the Gatekeeper Situation

Identify the gatekeeper's level of resistance and your information gap.

**Resistance levels:**
- **Soft block:** "I'm sorry, they're not available right now. Can I take a message?" — the gatekeeper is neutral and procedural. Respect and transparency can open this.
- **Active block:** "We don't give out that information." / "I cannot connect you if you don't have a name." — the gatekeeper has been trained to refuse. Direct frontal approach will fail.
- **Hostile block:** Gatekeeper has been hung up on mid-question or has explicitly stonewalled. Frontal approach is exhausted.

**Information gap:**
- Do you have a name? → Proceed to direct connection request with please-twice technique.
- Do you have a department but no name? → Calling-other-extensions hack.
- Do you have nothing except the main number? → Sales-help-sales hack or LinkedIn flanking.

**Why diagnose first:** The appropriate technique is determined by your resistance level and information gap. Using a bypass hack when a simple respectful request would have worked burns goodwill. Using a frontal approach when the gatekeeper has been trained to block wastes time and damages credibility.

### Step 2 — Decide: Bypass vs Befriend

This is a strategic decision based on account type and access difficulty. Neither path is always right.

**Choose Bypass when:**
- This is a new conquest account — you have never done business here and need a name or extension before you can prospect effectively
- The gatekeeper is a switchboard with no personal relationship to protect
- You have been actively and repeatedly blocked after transparent, respectful attempts
- The decision maker is walled in and direct approach has failed

**Choose Befriend when:**
- This is an ongoing account — you call or visit regularly and the gatekeeper sees you more than the decision maker does
- You have or want a long-term commercial relationship with this company
- The gatekeeper is a personal assistant who has genuine influence over the DM's calendar
- You are doing in-person territory prospecting and will return to this location repeatedly

**Why this matters:** Using bypass tactics on a recurring account destroys a relationship that could be your most reliable path to the calendar. Using befriend tactics on a cold conquest wastes time on relationship-building where a simple technique would work faster. (Blount, p. 213)

### Step 3 — Choose the Technique

Select the technique that fits your diagnosis from Step 1 and your decision from Step 2. Full technique details are in `references/gatekeeper-technique-library.md`.

**Bypass Techniques (conquest / blocked):**

**Sales-help-sales hack** — When you know the company has an outbound sales team but cannot get a name through the switchboard, call the sales department extension (usually "press 1 for sales"). Sales reps answer their phones, empathize with your situation, know who's who in the organization, and will often give you a direct line or mobile number. Be honest: "I wasn't having much luck going through the switchboard and figured as a fellow salesperson you could relate."

**Calling-other-extensions hack** — When you have partial information (a department name, a title, a vague description like "someone in corporate who handles that"), call random internal extensions. Employees are usually informal and helpful. Collect clues: "Jack in IT handles that." Use those clues when transferred back to reception — reception will often correct a close-but-wrong name ("Did you mean Zack Freedman?") and give you an extension. See Evan's case in Examples.

**LinkedIn flanking** — Gatekeepers rarely control the decision maker's social inbox. A personalized LinkedIn InMail with a specific bridge and because goes directly to the prospect.

**Early/late calls** — Decision makers often arrive before the gatekeeper and stay after. Call before 8 AM or after 5 PM.

**Email** — May bypass the switchboard entirely. Pair with `cold-email-writer` for the message.

**In-person go-around-back** — If prospecting in person and reception refuses information, try the back entrance, loading dock, or parking lot. Employees on break are often happy to help a transparent, non-aggressive stranger. Note: do not attempt this where security guards or explicit access controls are in place.

**Befriend Techniques (ongoing / recurring account):**

**Be likable and transparent** — Use your full name and company every time. Be polite, positive, and specific about why you are calling. Never give the gatekeeper a reason to put you on the do-not-help list.

**Use please twice** — "Would you please connect me to [name], please?" This is the single most effective courtesy technique for routine gatekeeper calls. (Blount citing Mike Brooks, p. 212)

**Connect genuinely** — Learn the gatekeeper's name. Ask how they are doing. Remember what they told you last time. Build the kind of relationship where they are taking your calls, not screening them.

**Ask for help directly** — A genuine, honest request — "I really need some help getting in to see [name]. I've been trying for weeks and I genuinely believe we can do something useful for your company. Can you help me?" — combined with a little self-deprecating humor can flip a skeptical gatekeeper into an advocate.

**Why the technique selection matters:** Each technique is designed for a specific access situation. Using the wrong one is not just inefficient — it can permanently close doors. The sales-help-sales hack is useless if the company has no outbound sales team. Befriend tactics on a hostile conquest gatekeeper give the blocker more opportunities to say no.

### Step 4 — Draft the Script

Once you have selected a technique, draft the exact words. Apply the Bridge-Because pattern from `prospecting-message-crafter`:

**For a sales-help-sales opener:**
> "Hi [name], my name is [your name] from [company]. The reason I'm calling is I'm trying to reach the person in your company who handles [decision area]. I wasn't having much luck going through the switchboard and I figured as a fellow salesperson you could relate and might give me a hand."

**For a transparent switchboard request:**
> "Hi, this is [full name] from [company]. Would you please connect me to [name or role], please?"

**For an ask-for-help approach with humor:**
> "I know — I keep coming back. I figured I hadn't gotten quite enough rejection today to fill my quota. [pause for laugh] Seriously though, I really need some help. I believe we can do something useful here. Would you be willing to make a quick call to [DM name] on my behalf?"

**For the calling-other-extensions handoff:**
> "Hey — I was talking to [made-up employee name] in [department] and they were transferring me to [partial name/role], but somehow I ended up with you. Would you mind sending me over?"

**Why draft the exact words:** Gatekeepers make decisions in the first three seconds of a call. A vague, halting opener signals amateur. A clear, confident, honest opener signals professional and worthy of passage. Draft before you dial, even if you never say it verbatim.

**Cross-reference:** Once you have the script structure, use `prospecting-message-crafter` to sharpen the bridge and because for the conversation with the decision maker once you are through.

### Step 5 — Anti-Pattern Audit

Before using any approach, run it against this checklist. Any yes answer is a red flag.

- [ ] **Pretending to be someone you are not.** Claiming to be a customer, a vendor partner, a colleague, or anyone other than yourself. This is deception. It destroys your credibility and the gatekeeper's goodwill permanently when (not if) it is discovered. (Blount, p. 213)
- [ ] **Using a trick or scheme.** Vague call purpose ("just calling to check in"), fake urgency ("it's regarding an important account matter"), calling a personal number without introduction. Tricks make you look foolish and land you on the do-not-help list. (Blount, p. 213)
- [ ] **Bulldozing or arguing.** Repeating the same request louder or more forcefully after the gatekeeper has said no. Arguing that the gatekeeper's refusal is wrong. Attempting to "overcome" their objection the way you would a prospect's. This generates hostility, not passage.
- [ ] **Going around without exhausting honest routes first.** Using the calling-other-extensions hack before trying a respectful direct request signals you are hiding something, even when you are not.
- [ ] **Disrespecting the gatekeeper's role.** Treating them as an obstacle, not a person. Dismissing them, cutting them off, or making them feel stupid. They have a job to do and a boss to protect. They also have a long memory.

**Why the anti-pattern audit:** Tricks work once at best. Honesty compounds. A gatekeeper you treated well remembers you. A gatekeeper you deceived will tell their boss. The bypass hacks in this skill work precisely because they are transparent and honest — they ask for help directly rather than circumventing anyone. (Blount, p. 213)

## Inputs

| Input | Required | Source |
|---|---|---|
| Company and suspected DM role | Yes | User provides |
| Gatekeeper type and resistance level | Yes | User describes situation |
| What has already been tried | Yes | User describes |
| Account type: conquest vs ongoing | Yes | User states |
| Partial info (name, department, title) | No | User provides if available |
| Available channels | No | User states or skill infers |

## Outputs

| Output | Location | Description |
|---|---|---|
| `gatekeeper-navigator-output.md` | Working directory | Bypass vs befriend decision + recommended technique + drafted scripts + anti-pattern audit results |
| Technique recommendation | Inline in conversation | Named technique with reason for selection |
| Anti-pattern flags | Inline in conversation | Any red flags from Step 5 with specific violations called out |

## Key Principles

**1. There are no tricks — only respect and technique.** Every bypass hack in this skill works because it is honest. The sales-help-sales hack succeeds because sales reps empathize with salespeople who are blocked. The calling-other-extensions hack works because a casual internal employee is willing to help a transparent stranger. Deception does not scale. (Blount, p. 212)

**2. Gatekeepers are powerful long-term allies.** A receptionist you know by name, whose kids you have asked about, who laughs at your self-deprecating humor — that person will get you on the calendar when cold callers are blocked. Long-term account relationships are won at the front desk, not by going around it. (Blount, p. 213)

**3. Respect is the multiplier.** Politeness costs nothing and compounds. Being rude, pushy, or dismissive guarantees failure. Being likable, transparent, and genuinely interested in the gatekeeper as a person is the single highest-ROI investment you can make on a recurring account.

**4. The bypass hacks are for access, not avoidance.** The sales-help-sales hack is not a way to avoid the gatekeeper — it is a way to get the information you need to call back and ask the right question. Once you have a name, you still work through reception with full transparency.

**5. Persistence is the foundation.** The most valuable prospects are the most heavily walled-in. Repeated, respectful, transparent attempts — using different techniques and channels — eventually open even the most resistant accounts. (Blount, p. 218)

## Examples

---

### Example 1 — Evan's Calling-Other-Extensions Hack (Enterprise, No Name, No Title)

**Situation:** Evan needs to reach the broadband decision maker at a large grocery chain HQ. He has no name, no title, and no direct line — only the main number. Repeated calls to reception have failed: "We don't give out that information."

**Step 1 diagnosis:** Active block. No name. Partial information (knows "someone in corporate").
**Step 2 decision:** Bypass — new conquest, no relationship to protect.
**Step 3 technique:** Calling-other-extensions hack — collect clues from internal employees.

**Execution:** Evan calls random internal extensions until a friendly employee says: "Yeah, I think a guy named Jack over in IT handles that." Evan returns to reception:

> "Hey, I was talking to Dale Jones in purchasing and he was transferring me to Jack in IT, but somehow I ended up with you. Would you mind sending me over?"

> Reception: "I'm not seeing a Jack. Did you mean Zack Freedman?"

> Evan: "Yes, sorry about that. I thought I said Zack."

> Reception: "Okay, no problem. I'll send you over now."

> Evan: "Before you do, would you mind giving me Zack's extension just in case we get disconnected?"

> Reception: "Sure, it's 5642."

**Anti-pattern check:** Evan did not claim to know Dale Jones personally — he used Dale's name as the transfer context, not as a false reference. He was honest that he was prospecting. No pretending, no tricks.

**Outcome:** Evan eventually reached Zack, established a relationship, and converted the account into his largest customer. (Blount, pp. 214-215)

---

### Example 2 — Blount's Sales-Help-Sales Hack (Conquest, Hostile Gatekeeper)

**Situation:** Jeb Blount identifies a company hiring 30 new sales reps — a perfect fit for Sales Gravy. He has no internal contact. The switchboard gatekeeper hangs up on him mid-qualifying question.

**Step 1 diagnosis:** Hostile block. No name. No title.
**Step 2 decision:** Bypass — new conquest, gatekeeper is actively hostile.
**Step 3 technique:** Sales-help-sales hack — call the sales department directly.

**Execution:** Blount calls the main number, selects the sales extension. Mike answers:

> "Hi, Mike, my name is Jeb Blount. The reason I'm calling is I'm trying to reach the person in your company who buys training programs. I wasn't having much luck going through the switchboard and I figured as a fellow salesperson you could relate and might give me a hand."

Mike immediately empathizes, gives Blount Jean's name, her mobile number, and background on the company's hiring situation.

**Why this worked:** Sales reps answer their phones. They know the organizational structure. They have stood in your shoes. Honesty and peer empathy replaced the gatekeeper entirely.

**Anti-pattern check:** No pretending. No tricks. Blount stated exactly who he was and what he wanted. He asked for help as a fellow salesperson, not as a fake vendor or internal contact.

**Outcome:** First call to Jean resulted in a meeting that included the company president and opened a formal proposal. (Blount, pp. 215-217)

---

### Example 3 — Receptionist-Befriend on a Recurring Territory Account

**Situation:** An outside sales rep sells payroll services. She calls on a mid-size manufacturing company monthly. The decision maker (VP Operations) is never available and the receptionist is the permanent gatekeeper. The rep has been told "I'll pass along your message" for three months with no callbacks.

**Step 1 diagnosis:** Soft to active block. Has DM name. Ongoing account.
**Step 2 decision:** Befriend — recurring account, long-term relationship value high.
**Step 3 technique:** Connect genuinely + ask for help.

**Script approach (calls):**
> "Hi Sarah, this is [rep name] from [company] — I'm the one who keeps calling about payroll. How are you holding up today? [Listens.] Listen, I know I keep trying to reach Mark, and I really appreciate your patience with me. I genuinely think what we're doing could save him a headache in Q3. Would you be willing to let him know I called? And — total long shot — any chance you could shoot me a five-minute window when he's actually accessible this week?"

**In-person approach (quarterly visit):**
On the third visit, bring a small, relevant value-add (a payroll compliance article from a trade publication, not a brochure). Ask about Sarah's family. Remember what she mentioned last time. The goal is not one appointment — it is becoming the rep whose calls Sarah mentions to Mark by name.

**Anti-pattern check:** No tricks. No pretending. No claiming a false relationship with Mark. The humor is self-deprecating, not manipulative.

**Long-term outcome:** Gatekeepers who genuinely like you will advocate for you. "Mark, there's a rep who's been really persistent and actually really polite about it. Do you want me to book her in?" is the outcome the befriend path is designed to produce.

## References

Supporting materials are in the `references/` folder:

- `references/gatekeeper-technique-library.md` — full technique details: sales-help-sales, calling-other-extensions, go-around-back, LinkedIn flanking, please-twice, connect/befriend protocol, with worked scripts for each
- `references/bypass-vs-befriend-decision-matrix.md` — decision matrix with account type, gatekeeper type, and prior attempt criteria
- `references/gatekeeper-anti-pattern-examples.md` — named anti-patterns (pretending, tricks, bulldozing) with detection criteria and why each backfires

**Source chapter:** Blount, Jeb. *Fanatical Prospecting*, Chapter 17 "The Secret Lives of Gatekeepers" (pp. 193-200 / PDF pp. 211-218). Case studies: Evan (pp. 196-197 / PDF pp. 214-215); Salespeople-help-Salespeople (pp. 197-199 / PDF pp. 215-217).

## License

Content derived from *Fanatical Prospecting* by Jeb Blount (Wiley, 2015). This skill is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt this material provided you give appropriate credit to Jeb Blount and BookForge, and distribute any derivative works under the same license.

## Related BookForge Skills

- `prospecting-message-crafter` — build the bridge and because for the conversation once you are through the gate; `clawhub install bookforge-ai/bookforge-skills/prospecting-message-crafter`
- `cold-call-opener-builder` — deploy the 5-step telephone framework (attention → identify → reason → bridge → ask) once you reach the decision maker
- `prospecting-rbo-turnaround` — handle reflex responses and brush-offs after the opener lands
- `in-person-prospecting-route-planner` — plan hub-and-spoke territory routes that include go-around-back opportunities
