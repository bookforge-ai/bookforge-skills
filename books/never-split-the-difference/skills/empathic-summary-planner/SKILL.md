---
name: empathic-summary-planner
description: Build an active listening summary and emotional validation script before any negotiation, sales conversation, difficult conversation, conflict resolution, or persuasion attempt. Use this skill when you need to prepare a summary statement that triggers genuine agreement from a counterpart, create a listening script before a high-stakes conversation with an emotionally activated person, draft labels and paraphrasing language before a client call, build rapport with someone before making a request, prepare a stalled negotiation recovery plan using validation techniques, write an empathic opening before delivering difficult feedback, plan the listening sequence before a salary negotiation or sales discovery call, or generate a "that's right" trigger statement that signals real understanding — not just acknowledgment.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/never-split-the-difference/skills/empathic-summary-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: never-split-the-difference
    title: "Never Split the Difference: Negotiating as if Your Life Depended on It"
    authors: ["Chris Voss"]
    chapters: [2, 5]
tags: [negotiation, active-listening, emotional-validation, mirroring, labeling, summarizing, rapport, influence, tactical-empathy, that's-right]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Situation brief — a description of the conversation, the counterpart, what you want, and the emotional dynamics you expect"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Document set preferred: situation-brief.md, counterpart-profile.md, conversation-history.md. Works from a free-text description if no files provided."
discovery:
  goal: "Produce empathic-summary-script.md: a situation summary, a label bank, and a 'that's right' trigger statement that validates the counterpart's worldview and moves the conversation toward influence."
  tasks:
    - "Identify the counterpart's emotional state, core concerns, and underlying needs from available context"
    - "Select and sequence active listening techniques appropriate to the conversation stage"
    - "Draft a paraphrase of the counterpart's situation in their own value frame"
    - "Draft 2-3 emotion labels targeting their most activated feelings"
    - "Combine paraphrase + labels into a summary statement designed to trigger genuine validation"
    - "Flag 'you're right' warning patterns and provide detection criteria"
    - "Produce the empathic-summary-script.md artifact"
  audience: "salespeople, founders, managers, consultants, negotiators — anyone preparing for a conversation where trust and understanding must precede persuasion"
  when_to_use: "Before any high-stakes conversation where the counterpart's emotional state is a barrier to rational agreement"
  environment: "Document set (situation-brief.md, counterpart-profile.md, conversation-history.md) or free-text description"
  quality: placeholder
---

# Empathic Summary Planner

## When to Use

You are preparing for a conversation — or you are in a stalled one — where the counterpart does not feel fully understood, and that gap is blocking progress. This skill applies when:

- Entering a negotiation where the counterpart has previously felt dismissed or steamrolled
- Preparing a sales discovery call where trust must be established before the pitch
- Recovering a stalled deal where no progress has been made despite multiple conversations
- Preparing for a difficult conversation where emotions are high (performance review, conflict, complaint)
- Delivering a request that requires the counterpart to feel understood first
- Trying to shift a counterpart who is agreeing superficially but not actually moving ("you're right" responses that lead nowhere)

The core mechanism: **genuine agreement — "that's right" — is triggered when a counterpart hears their own worldview reflected back accurately, with their emotional state named.** This requires combining paraphrase (their situation in their words) with labeling (their feelings named neutrally), producing a summary that validates their perspective without endorsing or rejecting their position.

This is not about being agreeable or soft. It is about advancing through the influence arc in the correct sequence. Influence attempts that skip the listening and rapport stages fail — not because they lack logic, but because the counterpart's emotional brain (System 1) has not been calmed, and an activated System 1 blocks access to rational System 2 reasoning.

Before starting, confirm you have:
- Enough context to describe the counterpart's situation from their perspective
- An understanding of what they care about, fear, or feel frustrated about
- A goal for what you want the conversation to achieve

---

## Context & Input Gathering

### Required Context

- **The situation:** What is the conversation about? What do you want to achieve?
- **The counterpart:** Who are they, what do they care about, what is at stake for them?
- **Their emotional state:** What are they feeling — frustration, distrust, skepticism, anxiety, urgency?
- **Conversation history:** What has been said before? What did they respond to, positively or negatively?

### Observable Context

If documents are provided, read them for:
- Statements the counterpart has made about their concerns, goals, or frustrations
- Prior agreements or concessions that have not moved the conversation forward
- Repeated phrases or themes in their language (these are primary paraphrase material)
- Signs of superficial agreement: "you're right," "sure," "I hear you" — without follow-through

### Default Assumptions

- If no counterpart profile is provided → assume a skeptical, experienced counterpart who has heard similar pitches or requests before
- If no conversation history is provided → assume no trust has been established and start from Active Listening
- If the counterpart's emotional state is unclear → default to naming uncertainty and frustration as the primary labels

### Sufficiency Check

Before generating the script, confirm you can answer: "What does this person believe about their situation, and what are they most worried about?" If you cannot answer that, gather more context or ask the user.

---

## Process

### Step 1: Map the Counterpart's Worldview

**ACTION:** Write a brief internal summary (not the output artifact) of the counterpart's situation from their perspective. Answer: What do they think is happening? What do they need? What are they afraid of? What have they said that matters most to them?

**WHY:** Active listening begins before the conversation. A negotiator who enters unprepared defaults to their own frame of reference and misses signals. Mapping the counterpart's worldview first forces perspective-taking: you cannot produce an accurate paraphrase if you are still inside your own assumptions. This step also surfaces hidden concerns — needs that the counterpart has not stated explicitly but which are evident from their behavior or history. The goal is not to be right about their worldview; it is to make an informed hypothesis that the conversation can correct.

**Format:** 3-5 bullet points in third-person counterpart voice:
- "They believe they have been waiting too long for a resolution."
- "They feel their previous concessions were not recognized or reciprocated."
- "They are most worried about [specific risk] going unaddressed."

---

### Step 2: Select the Active Listening Techniques for This Conversation

**ACTION:** Review the six active listening techniques and select which are appropriate given where the conversation is. Not all six are needed every time — the right combination depends on the counterpart's current emotional state and how much rapport already exists.

**WHY:** The techniques operate in progression. Early in a conversation (or with an emotionally activated counterpart), starting with paraphrasing or summarizing before the counterpart feels heard creates resistance. Pausing and mirroring create space for the counterpart to elaborate before you interpret. Labeling names what emerges from that elaboration. Paraphrasing confirms you understood the content. Summarizing combines both into a validation statement. Choosing the wrong technique for the stage is like trying to run before the counterpart is willing to walk. See `references/active-listening-techniques.md` for full mechanics of each technique.

**The six techniques, in progression order:**

| # | Technique | What It Does | When to Use |
|---|-----------|-------------|-------------|
| 1 | **Effective Pause** | Silence after their statement — signals you are processing, not rushing | Always; especially after they say something emotionally significant |
| 2 | **Minimal Encouragers** | Short verbal affirmations ("yes," "I see," "right") | During any listening period; keeps them talking without interrupting |
| 3 | **Verbal Mirroring** | Repeat their last 1-3 words as a question → silence | Early rapport-building; when you want elaboration without interpretation |
| 4 | **Labeling** | Name their emotional state: "It seems like..." | When you can observe a feeling — anger, hesitation, relief, frustration |
| 5 | **Paraphrasing** | Restate their meaning in your own words | When you want to confirm understanding of their position |
| 6 | **Summarizing** | Paraphrase + label combined into one statement | When you are ready to trigger "that's right" — the full validation |

**Selection rule:** Match the technique to the stage. If no prior rapport exists, start with pauses and mirroring. If partial rapport exists, move to labeling and paraphrasing. Only produce the summary when you have enough context to reflect their full perspective accurately.

---

### Step 3: Draft the Verbal Mirror Script

**ACTION:** Write 2-3 verbal mirroring prompts based on key statements the counterpart has made or is likely to make. A mirror repeats the last 1-3 words of their statement, inflected slightly upward as a question. Follow each with a pause of at least 4 seconds.

**WHY:** Mirroring (repeating the last 1-3 words as a question) works because it extracts information without imposing a frame. Unlike direct questions which reveal what YOU think is important, a mirror invites the counterpart to elaborate on what THEY think is important. Under uncertainty — when you don't yet know what matters most to them — mirrors are safer than questions because they cannot lead the witness. When a counterpart elaborates in response to a mirror, they are revealing more than they planned — often the concern beneath the stated position. The upward inflection signals a question rather than a challenge. The silence that follows is not empty: it is pressure. The counterpart's brain processes the mirror as an implicit "tell me more," and fills the gap.

**Mirroring formula:**
- Counterpart says: "I've been waiting three weeks for a decision on this."
- Mirror: "Three weeks for a decision?" [Pause 4+ seconds]
- Counterpart: "Yes, and every time I follow up I get a different answer..." [elaboration revealed]

**Voice guidance:** Use the FM DJ voice — calm, measured, slightly slower than normal speech. Not flat or robotic, but unhurried. Never mirror with enthusiasm or urgency; it signals that you are pushing, not listening.

---

### Step 4: Draft the Label Bank

**ACTION:** Write 2-3 emotion labels targeting the counterpart's most activated feelings. Use the "It seems like..." / "It sounds like..." formula. Do not use "I feel" or "I think you feel." Sequence labels from most emotionally charged to least.

**WHY:** Labeling names a feeling rather than arguing with a position. When the counterpart's emotional state is unaddressed, it occupies their attention — they cannot engage with rational arguments because the emotional signal is still firing. Naming the feeling accurately turns the amygdala response down: research in affect labeling (Matthew Lieberman, UCLA) shows that verbalizing an emotional state reduces neural activation in the areas associated with threat response. The mechanism is not sympathy — you do not need to feel what they feel. You only need to demonstrate that you have accurately observed it. If the label is wrong, the counterpart corrects you, which opens dialogue. If it is right, they confirm it, and their guard comes down.

**Label formula:**
- "It seems like you've been carrying this situation longer than you expected."
- "It sounds like the timeline has been the most frustrating part."
- "It seems like you're not sure whether anything will actually change."

**Do not:** Move to paraphrasing or summarizing before labeling. A summary that skips the emotional acknowledgment is perceived as a pitch, not as listening.

---

### Step 5: Write the Paraphrase

**ACTION:** Restate the counterpart's situation in your own words — content only, no feelings. The paraphrase should be accurate enough that a neutral observer would recognize it as a fair representation of what the counterpart has communicated.

**WHY:** Paraphrasing proves comprehension. Labeling proves emotional attunement. Together, they form the components of the summary. Paraphrasing alone, without labeling, can feel clinical — "you understood the facts but not the feeling." Labeling alone, without paraphrasing, can feel vague — "you noticed the emotion but not the substance." The combination is what produces genuine validation.

**Paraphrase format:** 2-4 sentences in your own words that capture:
- Their stated situation or position
- What they care most about
- What has not been resolved from their perspective

---

### Step 6: Write the Summary Statement (the "That's Right" Trigger)

**ACTION:** Combine the paraphrase (their situation) and the strongest label (their feeling) into a single summary statement. Read it aloud (or internally) and ask: "Would a reasonable counterpart hear this and feel accurately understood — not agreed with, but understood?"

**WHY:** "That's right" is different from "you're right." "That's right" means: "You have accurately described my situation and how I feel about it." It is a genuine validation signal — the counterpart is not conceding to you, they are confirming that you see them. This is the trigger for the rapport stage of the influence arc. Until the counterpart feels genuinely understood, they are in a defensive posture. Once they reach "that's right," their emotional guard drops and influence becomes possible. The summary is the most powerful tool in the listening arsenal precisely because it is the synthesis: it shows the counterpart that you have both heard the content and felt the weight of their situation.

**Warning — the "you're right" trap:** "You're right" is the worst possible response to your summary. It means the counterpart is dismissing you, not confirming genuine understanding. Signs of a "you're right" dismissal:
- The conversation does not change after they say it
- They immediately return to their prior position
- Their tone does not shift — the statement is flat, not relieved
- They say it after you have made a lengthy argument (they are ending the argument, not agreeing with it)

If you receive "you're right" without behavioral change, do not proceed. Rebuild rapport with additional mirroring and labeling before attempting the summary again.

**Summary template:**
> "It sounds like [paraphrase of their situation — 2-3 sentences]. And on top of that, it seems like [strongest label — their emotional experience]."

---

### Step 7: Write the Empathic Summary Script

**ACTION:** Produce the `empathic-summary-script.md` artifact. This is the deliverable — a ready-to-use document the user can review, rehearse, or adapt for the conversation.

**WHY:** Writing the script makes the listening sequence a deliberate plan rather than improvisation. Under pressure, people default to pushing their own agenda. Having the mirroring prompts, labels, and summary written out prevents this. It also allows the user to identify gaps: if any component of the summary feels forced or inaccurate, that is a signal that more context about the counterpart is needed before the conversation.

---

## Inputs

| Input | Required | Format |
|---|---|---|
| Situation description | Yes | Any — markdown, plain text, verbal description |
| Goal for the conversation | Yes | One sentence minimum |
| Counterpart description | Yes | Role, stakes, emotional state, prior history if available |
| Conversation history or prior statements | Strongly recommended | Markdown or plain text |
| Counterpart's key phrases or repeated concerns | Optional | Any |

---

## Outputs

Produce `empathic-summary-script.md` with the following structure:

```markdown
# Empathic Summary Script

**Situation:** [One-sentence description]
**Counterpart:** [Who they are, what they care about, what they feel]
**Conversation Goal:** [What you want to achieve]
**Current Stage in Influence Arc:** [Active Listening / Empathy / Rapport / Influence]

---

## Counterpart's Worldview (Internal Map — Do Not Deliver)

- [What they believe about the situation]
- [What they need]
- [What they are afraid of]
- [What has frustrated them most]

---

## Verbal Mirrors (2-3)

**Mirror 1:** "[Last 1-3 words of a key statement]?"
*Pause. 4+ seconds. Do not fill the silence.*

**Mirror 2:** "[Last 1-3 words]?"
*Pause. 4+ seconds.*

[Mirror 3 if applicable]

---

## Label Bank (2-3 Labels, Sequenced Strongest to Lightest)

**Label 1 (Most Charged):**
> "It seems like [strongest emotional observation]."
*Pause. 3-5 seconds.*

**Label 2:**
> "It sounds like [second emotional observation]."
*Pause. 3-5 seconds.*

[Label 3 if applicable]

---

## Paraphrase

> "[Their situation in your words — 2-4 sentences capturing what they care about and what is unresolved]"

---

## Summary Statement ("That's Right" Trigger)

> "It sounds like [paraphrase of situation]. And on top of that, it seems like [strongest label]."

*Deliver slowly. Pause after. Wait for a full response — do not rush to your next point.*

---

## "That's Right" vs "You're Right" — Detection Guide

| Signal | "That's Right" (genuine) | "You're Right" (dismissal) |
|--------|--------------------------|---------------------------|
| Tone | Relieved, engaged | Flat, polite |
| What follows | New information, elaboration | Return to prior position |
| Body language | Relaxed, leans in | Unchanged or closed |
| Next move | Safe to move to influence | Rebuild rapport — more mirroring |

---

## Notes

- If you receive "that's right" → proceed to influence stage (share your perspective, make your ask)
- If you receive "you're right" → do not proceed; return to mirroring and labeling
- If the counterpart corrects a label → accept the correction and update your script: "You're right — help me understand what you're actually feeling about this"
- Do not skip to the summary before completing at least one mirroring exchange and one label delivery
```

---

## Key Principles

- **Influence requires rapport. Rapport requires empathy. Empathy requires listening.** This progression follows the FBI's Behavioral Change Stairway Model (BCSM): Active Listening → Empathy → Rapport → Influence → Behavioral Change. Each stage gates the next — attempting to influence before establishing rapport through empathic listening causes resistance, not compliance. The "That's right" moment signals the transition from Rapport to Influence: the counterpart has felt genuinely understood, and is now open to considering new possibilities. Skipping stages does not accelerate the process — it resets it. A counterpart who does not feel understood cannot be persuaded; they can only be pressured, and pressure produces resistance or false agreement.

  *WHY:* The BCSM was developed by the FBI's Crisis Negotiation Unit to explain why direct influence attempts fail in high-stakes situations. The stages are not philosophical — they describe a neurological sequence. The emotional brain (System 1) must be calmed before the rational brain (System 2) can engage. Labels and mirroring target System 1 directly. Without that, even perfectly logical arguments cannot be received.

- **"That's right" is the goal, not "yes."** A "yes" can be counterfeit (to escape the conversation), confirmatory (acknowledgment without commitment), or genuine. "That's right" is nearly always genuine — it means the counterpart has heard themselves accurately reflected back and confirmed it. It signals that rapport has been established and the conversation is ready for influence.

  *WHY:* The distinction matters because pursuing "yes" prematurely triggers the "you're right" pattern — the counterpart gives you the word you want while thinking something entirely different. "That's right" is harder to fake because it requires the counterpart to recognize their own worldview in your words.

- **Verbal mirroring extracts information without interpretation.** Repeating the last 1-3 words of a statement — with a slight upward inflection and then silence — causes the counterpart to elaborate. They fill the silence with what they actually think. This is more valuable than any question you could ask, because the counterpart is now revealing their reasoning rather than responding to your frame.

  *WHY:* Questions impose a frame (they define what kinds of answers are relevant). Mirrors impose no frame — they simply signal "tell me more about that." Under uncertainty, this is the safest tool: you cannot misinterpret what you have not yet heard.

- **Labels name the feeling; they do not agree with the position.** "It seems like this has been a frustrating process" does not mean you think the process was unfair, or that you caused the frustration, or that you will fix it. It means you observed a feeling and named it. This distinction protects you legally and professionally while still delivering the emotional validation the counterpart needs.

  *WHY:* Counterparts frequently mistake emotional validation for concession. They are not the same. You can fully acknowledge that a counterpart is frustrated without agreeing that their position is correct or their demand is reasonable. Separating these two things — and doing so cleanly — is what makes labeling a precision tool rather than appeasement.

- **The FM DJ voice is a physiological prerequisite, not a stylistic choice.** Deliver labels and summaries in the "late-night FM DJ voice" — calm, slow, with downward-inflecting tone. Downward inflection signals certainty and safety; upward inflection (question tone) invites challenge. The calm voice activates the counterpart's parasympathetic nervous system, reducing their threat response. This physiological calming is a prerequisite for emotional labels to land — a label delivered in an anxious or hurried voice triggers more defensiveness, not less. Voice tone accounts for 38% of the emotional signal in spoken communication (Mehrabian communication model). A label delivered in an urgent, high-energy voice reads as confrontation. The same label delivered slowly reads as understanding.

  *WHY:* The counterpart's threat-detection system is sensitive to vocal signals before it processes content. A calm voice signals that the speaker is not threatened and is not threatening. This is why the Late-Night FM DJ voice is the default for de-escalation: it is physiologically safe, and physiological safety is the container that makes labels and mirrors land as listening rather than interrogation.

- **A corrected label is still a successful label.** If you label incorrectly, the counterpart will correct you. "No, it's not that I'm frustrated — I'm just exhausted by how long this has taken." This is productive: you now have more accurate information, the counterpart has expressed themselves, and the act of correcting you has engaged them in the conversation. There is no way to lose on a label.

  *WHY:* Incorrect labels work because the mechanism is not accuracy — it is attention. By attempting a label, you signal that you are trying to understand. The counterpart's response to the attempt (whether confirmation or correction) always provides more information than silence.

---

## Examples

### Example 1: Stalled Sales Deal (Abu Sayyaf / Schilling kidnapping parallel)

**Scenario:** A software vendor has been in negotiations with a procurement team for four months. The procurement lead has been unresponsive for three weeks after verbally agreeing to terms. The vendor needs to restart the conversation without creating pressure.

**Trigger:** "This deal has been stalled for three weeks. The procurement lead agreed verbally but now won't respond. Help me plan how to restart the conversation without pushing them away."

**Process:**
- Counterpart worldview mapped: they likely have internal pressures (budget freeze, leadership review, other priorities) that have made the agreement harder to execute than expected. They may also feel embarrassed that they over-committed.
- Technique selection: start with mirroring (allow them to explain the delay), then labeling (name the difficulty they are in), then summary if rapport is established
- Labels drafted targeting the most likely feelings: pressure, embarrassment, uncertainty
- Summary written to reflect their constraints without applying pressure for commitment

**Output (`empathic-summary-script.md` excerpt):**
```
Mirror: "Three weeks since we last spoke?" [Pause 4+ seconds]

Label 1: "It seems like things have gotten more complicated on your end since we last talked."
[Pause 3-5 seconds]

Label 2: "It sounds like you might be in a situation where moving forward isn't fully in your hands right now."
[Pause 3-5 seconds]

Summary: "It sounds like this decision has more moving parts than it did when we first discussed it, and that some of those parts aren't resolved yet. And on top of that, it seems like the pressure to get this right might be making it harder to move at all."

[Wait for response. If "that's right" → proceed to: "I'd like to understand what would make it easier for you to move forward. What do you need from me?"]
[If "you're right" → mirror their response: "Easier to move forward?" — and restart labeling]
```

---

### Example 2: Pharma Sales Representative

**Scenario:** A pharmaceutical sales rep needs to get a doctor to consider prescribing a new medication. The doctor has been dismissive in prior visits — polite but not engaging. The rep suspects the doctor is skeptical of the efficacy data and tired of sales calls.

**Trigger:** "I have a 10-minute appointment with a doctor who has seen me three times and hasn't changed anything. Help me plan an approach that actually opens a conversation."

**Process:**
- Counterpart worldview: the doctor has heard the pitch and does not believe it adds enough value over their current prescribing habits. They are protecting their time and may be skeptical of vendor-provided data.
- Technique selection: open with a mirror on their skepticism (do not pitch), label the frustration with sales calls, paraphrase their actual clinical situation
- "That's right" trigger: a summary that reflects their patient-care goals, not the product features

**Output (`empathic-summary-script.md` excerpt):**
```
Opening (do not pitch): "I know you've heard a lot about this medication already."

Mirror: "Heard a lot already?" [Pause 4+ seconds — let them fill it]

Label 1: "It seems like a lot of these conversations end up being variations of the same pitch."
[Pause 3-5 seconds]

Label 2: "It sounds like what would actually matter to you is whether this changes outcomes for a specific type of patient — not just feature comparisons."
[Pause 3-5 seconds]

Summary: "It sounds like you've already evaluated a lot of options and you're not looking for another vendor's take on their own data. And on top of that, it seems like the only thing worth your time is something that addresses a patient population that isn't currently being served well."

[Wait for "that's right" before sharing any clinical data]
```

---

### Example 3: Chase Manhattan Bank Robbery — Verbal Mirroring Under Pressure

**Scenario:** A negotiator is dealing with a bank robber who claims he is not in charge and keeps deflecting decisions to "the others." The negotiator needs to identify who is actually in control without confronting the deception directly.

**Trigger:** "Help me plan a mirroring sequence to get the bank robber to reveal the actual decision-maker without accusing him of lying."

**Process:**
- Counterpart worldview: the robber is managing a deception (claiming multiple accomplices and shared control to confuse negotiators and buy time). He is calm and controlled — indicating he has a plan.
- Technique selection: mirroring only at this stage — no labels or summary. The goal is information extraction, not rapport.
- Mirrors targeted at the "others" language to reveal inconsistencies

**Output (`empathic-summary-script.md` excerpt):**
```
Robber: "I have to check with the others before we can agree to anything."
Mirror: "Check with the others?" [Pause 4+ seconds]

Robber: "Yeah, they're in charge of the timeline."
Mirror: "In charge of the timeline?" [Pause 4+ seconds]

Robber: "Look, I'm just the one talking to you — the decisions aren't mine."
Mirror: "Not yours to make?" [Pause 4+ seconds]

[Each mirror causes the robber to elaborate, revealing contradictions in the "multiple decision-makers" story. The negotiator collects information without confronting the lie — confrontation would end dialogue.]

Note: Do not advance to labeling or summary until the mirroring phase has produced enough information to form an accurate worldview map.
```

---

## References

- [references/active-listening-techniques.md](references/active-listening-techniques.md) — Full mechanics of all 6 techniques: rules, edge cases, common errors, examples for each
- [references/bcsm-influence-arc.md](references/bcsm-influence-arc.md) — Behavioral Change Stairway Model: 5 stages, gating conditions, failure modes at each stage
- [references/three-voices-guide.md](references/three-voices-guide.md) — FM DJ voice, positive/playful, and assertive: selection rules, inflection guidance, when each fails
- [references/thats-right-vs-youre-right.md](references/thats-right-vs-youre-right.md) — Detection criteria, recovery steps, case study examples

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Never Split the Difference: Negotiating as if Your Life Depended on It by Chris Voss.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
