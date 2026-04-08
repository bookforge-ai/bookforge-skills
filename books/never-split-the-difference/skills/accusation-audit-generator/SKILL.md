---
name: accusation-audit-generator
description: Generate a preemptive objection audit and emotion-label bank before any high-stakes negotiation, difficult conversation, salary discussion, sales pitch, or conflict resolution. Use this skill when you need to defuse anticipated resistance before speaking, prepare labels for counterpart objections before a job offer negotiation, neutralize defensive reactions before presenting bad news, write preemptive acknowledgments before a pitch to a skeptical audience, prepare for a difficult performance review or client escalation, anticipate accusations before a contract renegotiation, build a delivery script for labeling counterpart frustrations, or create an accusation audit for a negotiation one-sheet.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/never-split-the-difference/skills/accusation-audit-generator
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: never-split-the-difference
    title: "Never Split the Difference: Negotiating as if Your Life Depended on It"
    authors: ["Chris Voss"]
    chapters: [3, 23]
tags: [negotiation, emotion-labeling, accusation-audit, tactical-empathy, objection-handling, conflict-resolution, sales, difficult-conversations]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Situation brief — a description of the negotiation or conversation, the counterpart, what you want, and what tensions or objections you expect"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Document set preferred: situation-brief.md, counterpart-profile.md. Works from a free-text description if no files provided."
discovery:
  goal: "Produce a ready-to-deliver accusation audit: a list of 3-5 emotion labels anticipating the counterpart's worst-case feelings, plus a delivery script."
  tasks:
    - "Anticipate the counterpart's negative emotions and unstated objections"
    - "Convert each anticipated negative into a label statement using the 'It seems like...' formula"
    - "Sequence labels from strongest to lightest for opening delivery"
    - "Add a pause instruction after each label"
    - "Produce the accusation-audit.md artifact"
  audience: "salespeople, founders, managers, consultants, freelancers — anyone preparing for a high-stakes or difficult conversation"
  when_to_use: "Before any conversation where you expect resistance, defensiveness, or negative emotions from your counterpart"
  environment: "Document set (situation-brief.md, counterpart-profile.md) or free-text description"
  quality: placeholder
---

# Accusation Audit Generator

## When to Use

You are preparing for a conversation where your counterpart is likely to feel resistance, frustration, suspicion, or resentment — and you want to defuse those emotions before they derail the discussion. This skill applies when:

- Entering a salary, rate, or price negotiation where you expect pushback
- Delivering difficult news (restructuring, scope reduction, price increase, rejection)
- Opening a sales call with a skeptical or burned prospect
- Re-entering a stalled or previously contentious negotiation
- Managing a client escalation or complaint situation
- Preparing a difficult performance conversation with a direct report

The core pattern: **you name the counterpart's worst-case feelings first, before they do.** This drains the emotional charge from anticipated objections and signals that you understand their perspective — making it safe for them to listen instead of defend.

This is distinct from sympathy. Sympathy is feeling what they feel (joining them in the emotion). Active listening with emotional validation (tactical empathy) is recognizing and naming what they feel without being swept into it. Naming the emotion is the action; feeling it with them is not required or useful.

Before starting, confirm you have:
- A clear description of the situation and what you want
- Enough knowledge of the counterpart to anticipate their concerns (profile, history, stakes for them)

---

## Context & Input Gathering

### Required Context

- **The situation:** What is the conversation about? What do you want out of it?
- **The counterpart:** Who are they, what do they care about, what's at stake for them?
- **The anticipated negatives:** What do you expect them to feel — anger, fear, distrust, resentment, embarrassment, overwhelm?

### Observable Context

If documents are provided, read them for:
- Prior friction points or unresolved complaints in conversation history
- Explicit objections or concerns the counterpart has raised before
- Power dynamics and what the counterpart stands to lose
- Any promises made and not kept, or expectations set and not met

### Default Assumptions

- If no counterpart profile is provided → assume a skeptical, experienced counterpart who has been in similar conversations before (most challenging scenario)
- If no prior history is provided → assume the counterpart has generic concerns about fairness, respect, and getting a bad deal
- If fewer than 3 anticipated negatives can be identified → ask the user to describe the worst-case accusations they fear the counterpart might make

### Sufficiency Check

Before generating the audit, confirm you have enough to answer: "What is this person most afraid of, most frustrated about, and most suspicious of?" If you cannot answer that, gather more context first.

---

## Process

### Step 1: List Every Anticipated Accusation

**ACTION:** Write out every negative feeling or accusation the counterpart might have — stated as a raw complaint in their voice. Do not filter. Include the accusations that feel embarrassing or extreme.

**WHY:** The most dangerous objections are the ones that go unsaid — they fester and resurface as deal-killers. This step forces you to surface the worst-case perspective. Research in affect labeling (UCLA, Matthew Lieberman) shows that naming a negative emotion reduces its intensity by engaging the prefrontal cortex and dampening the amygdala response. You cannot label what you have not named. Including extreme accusations is deliberate: counterparts who hear their harshest unspoken thought voiced aloud by you often respond with surprise, then relief. The defusion effect is strongest for the most emotionally charged accusations.

**Format:** Write each in first-person counterpart voice:
- "You're only here because you want to take advantage of me."
- "This is a waste of my time."
- "You don't actually care about solving my problem."
- "You're going to lowball me."
- "I've heard this pitch before and it always disappoints."

Target: 5-10 raw accusations, more is better at this stage.

---

### Step 2: Convert Each Accusation into a Label Statement

**ACTION:** Rewrite each accusation as a third-person observation using the label formula. Select the 3-5 most charged accusations to convert.

**WHY:** The label formula shifts the statement from personal claim to neutral observation. "I think you feel cheated" implies judgment from you. "It seems like you feel this isn't fair" reflects back the counterpart's likely experience without endorsing or denying it. If the label is wrong, the counterpart corrects you — still valuable because it opens dialogue. If it is right, the counterpart feels understood — which reduces the emotional activation driving resistance. The third-person framing ("It seems like...") also protects you: you are not admitting fault or agreeing, you are naming what you observe.

Use third-person observation ("It seems like...") rather than first-person claim ("I think you feel..."). Third-person phrasing is safer because if the label is wrong, the counterpart corrects you without feeling confronted. First-person claims ("I feel that you're frustrated") make the conversation about YOUR perception rather than THEIR reality — which triggers defensiveness because the counterpart now has to argue with your feelings instead of reflecting on theirs.

**Label formula:**
- "It seems like..." (primary — most neutral)
- "It sounds like..." (for labels based on what they have said)
- "It looks like..." (for labels based on observable behavior)

**Never use:** "I feel..." or "I think you feel..." — these make the label about you, not the counterpart. They also trigger the counterpart to argue with your feelings rather than reflect on theirs.

**Conversion examples:**

| Raw Accusation | Label Statement |
|---|---|
| "You're going to lowball me." | "It seems like you're worried this conversation will waste your time without a real offer." |
| "You don't care about my situation." | "It sounds like you feel your concerns haven't been taken seriously in the past." |
| "This is a bait-and-switch." | "It seems like you've had experiences where the final terms didn't match the original pitch." |
| "You're only here for your own benefit." | "It seems like you're concerned this deal benefits us more than it benefits you." |
| "I've already decided — this won't change my mind." | "It looks like you've put a lot of thought into your position and you're not looking to be talked out of it." |

---

### Step 3: Sequence for Maximum Defusion

**ACTION:** Order the 3-5 selected labels from most emotionally charged to least. The most provocative accusation goes first.

**WHY:** Counterparts enter difficult conversations with their emotional guard up. Opening with the mildest label first leaves the biggest charge untouched — it remains the elephant in the room, distracting them from what you say next. Opening with the strongest label signals courage and transparency: "I know what you're thinking, and I'm not afraid to say it." This establishes credibility and disarms the defensive posture before you have asked for anything. After the heaviest label lands and is acknowledged (or corrected), lighter labels feel easy by comparison.

**Sequencing rule:** If you are uncertain which label is most charged, choose the one that most directly names a fear about your motives or fairness — those trigger the strongest defensive reactions.

---

### Step 4: Add Delivery Instructions

**ACTION:** For each label, append a pause instruction. Add a voice guidance note for the opening of the delivery.

**WHY:** The label only works if the counterpart has space to respond. Rushing past the label with the next sentence signals that you are not actually listening — you are just performing empathy. The silence after the label is where the counterpart processes recognition ("they understand what I'm feeling") and decides to lower their guard. A minimum 3-5 second pause is required. Do not fill it. If the silence feels uncomfortable, let it sit — that discomfort is the counterpart processing. Additionally, voice delivery matters: a calm, slow, downward-inflecting tone (not questioning, not tentative) signals confidence and safety. An upward-inflecting delivery sounds like you are seeking approval, which undermines the label.

**Voice guidance:**
- **Default delivery tone:** Warm, even, measured. Not apologetic. Not overly soft.
- **For the opening label (most charged):** Slow down. Downward inflection at the end of the sentence — it lands as a statement, not a question. This signals that you are calm and not threatened by naming it.
- **Avoid:** Uptalk, rushed delivery, apologetic hedges ("I don't know if this is right, but..."). These undermine the authority of the label.

---

### Step 5: Write the Accusation Audit

**ACTION:** Produce the `accusation-audit.md` artifact with the full label sequence and delivery script.

**WHY:** Having the labels written out in delivery order prevents in-the-moment improvisation under stress. Skilled practitioners rehearse the labels before high-stakes conversations. The written artifact also surfaces gaps: if you cannot write a label that feels honest and non-manipulative, that is a signal the label is either too vague or the situation requires more preparation.

---

## Inputs

| Input | Required | Format |
|---|---|---|
| Situation description | Yes | Any — markdown, plain text, verbal description |
| What you want from the conversation | Yes | One sentence minimum |
| Counterpart description | Yes | Role, stakes, prior history if available |
| Prior objections or stated concerns | Optional | Any |
| Conversation history | Optional | Markdown or plain text |

---

## Outputs

Produce `accusation-audit.md` with the following structure:

```markdown
# Accusation Audit

**Situation:** [One-sentence description]
**Counterpart:** [Who they are and what they care about]
**Goal:** [What you want from this conversation]

---

## Anticipated Accusations (Raw)

1. [Counterpart's worst-case thought, in their voice]
2. [Second accusation]
3. [Third accusation]
4. [Fourth accusation]
5. [Fifth accusation — include more if identified]

---

## Label Bank (3-5 Labels, Sequenced)

**Label 1 (Most Charged):**
> "It seems like [strongest anticipated negative]."
*Pause. Wait 3-5 seconds. Do not fill the silence.*

**Label 2:**
> "It sounds like [second anticipated negative]."
*Pause. Wait 3-5 seconds.*

**Label 3:**
> "It seems like [third anticipated negative]."
*Pause. Wait 3-5 seconds.*

[Label 4 and 5 if applicable]

---

## Delivery Script

**Opening (before any ask or proposal):**

Deliver the labels in sequence. Use a calm, even, downward-inflecting tone. Do not apologize for naming the feelings. Do not move to your ask until the counterpart has responded to at least one label.

Sample opening sequence:
[Insert Label 1]
[Wait for response]
[Insert Label 2 if still needed]
[Wait for response]
[Transition: "I want to make sure I understand your situation before I tell you what I'm thinking."]

---

## Notes

- If a label is wrong, the counterpart will correct you. Accept the correction: "You're right — help me understand what you're actually concerned about." Wrong labels are still productive.
- If the counterpart responds with "That's right" or "Exactly" — you have a genuine confirmation of understanding. Proceed.
- Do not use more than 3-5 labels in a single opening. More than 5 becomes a recital, not a conversation.
```

---

## Key Principles

- **Name the accusation before they do.** Counterparts who feel their worst-case thinking has been preemptively acknowledged have no reason to raise it defensively. The emotional charge dissipates before it fires.

  *WHY:* The brain's threat-detection system (amygdala) stays activated while a negative emotion is unnamed. Naming it triggers the prefrontal cortex — the reasoning brain — which reduces the intensity of the emotional response. This mechanism is called affect labeling: when you say "It seems like you're frustrated," the counterpart's brain shifts from emotional reaction to cognitive processing. Affect labeling research (UCLA, Matthew Lieberman) shows that even brief verbal labeling measurably reduces amygdala reactivity. This is why labeling de-escalates: it literally moves neural activity from the threat-response center to the rational-thinking center. You cannot label what you have not named — which is why Step 1 requires surfacing every accusation first.

- **Use "It seems like..." — never "I feel..."** The formula keeps the label as an observation about their experience, not a claim about yours. This prevents the counterpart from arguing with your feelings and keeps the focus on understanding theirs.

  *WHY:* "I feel you're upset" centers the speaker. "It seems like you're upset" centers the counterpart's experience. The distinction signals that you are observing, not projecting. It also protects you legally and professionally — you are not admitting fault, only reflecting what you observe.

- **Wrong labels still work.** If you mislabel the emotion, the counterpart corrects you — which opens dialogue, reveals their actual concern, and demonstrates that you are genuinely listening rather than following a script.

  *WHY:* A corrected label is still valuable because: (1) it produces more information about what the counterpart actually feels, (2) the act of correction engages the counterpart actively instead of passively, and (3) the willingness to be corrected signals humility, not weakness.

- **Pause after every label.** The label requires a response to function. Filling the silence prevents the counterpart from processing the recognition and expressing their feeling. The pause is not empty — it is where the emotional defusion happens.

  *WHY:* The mechanism requires the counterpart to internally confirm or deny the label. That internal process takes 3-5 seconds minimum. Interrupting it with more words cancels the effect.

- **Tactical empathy (active listening with emotional validation) is not sympathy.** You do not need to feel what they feel, agree with their position, or validate their conclusions. You only need to demonstrate that you understand their emotional state. These are separable. Sympathy means feeling the counterpart's pain and making concessions to relieve it. Tactical empathy means understanding and labeling their emotions while maintaining your position. The label "It seems like you feel this is unfair" acknowledges their emotion without agreeing that it IS unfair — you are naming their experience, not endorsing their conclusion.

  *WHY:* Sympathy draws you into the counterpart's emotional frame and impairs your judgment. Emotional validation keeps you grounded while demonstrating understanding. The counterpart does not need you to suffer with them — they need evidence that you see their situation accurately. Once they believe you see it, they can engage rationally.

- **The accusation audit opens the conversation — it is not the pitch.** Labels come first, before any proposal, ask, or argument. Moving to your ask before the counterpart has felt heard activates resistance, not receptiveness.

  *WHY:* The behavioral change model (Active Listening → Empathy → Rapport → Influence → Behavioral Change) treats empathy as a prerequisite for influence. Skipping to influence before rapport is established reliably produces defensiveness.

---

## Examples

### Example 1: Salary Negotiation

**Scenario:** A marketing manager is negotiating a 20% raise with a manager who has signaled budget constraints. The manager expects pushback about timing and the company's cost situation.

**Trigger:** "Help me prepare for tomorrow's salary conversation. I'm asking for a 20% raise and I know my manager is going to push back hard."

**Process:**
- Raw accusations identified: "You're asking too much given the budget freeze," "You're being greedy," "You don't understand how tight things are," "You're threatening to leave if we don't pay you," "Why now — the timing is terrible."
- Top 3 labels selected and sequenced: strongest first (fairness accusation, then timing, then motives)
- Delivery script drafted with pause instructions and transition to the actual ask

**Output (`accusation-audit.md` excerpt):**
```
Label 1: "It seems like this is a difficult time to be having a conversation about compensation."
[Pause 3-5 seconds]

Label 2: "It sounds like you might be concerned that I'm not aware of the pressures the team is facing."
[Pause 3-5 seconds]

Label 3: "It seems like you might wonder whether this is an ultimatum rather than a conversation."
[Pause 3-5 seconds]

Transition: "I want to be straightforward about what I'm thinking and why, and I'm genuinely open to how we get there."
```

---

### Example 2: Apartment Subletting Request

**Scenario:** A renter wants to sublet their apartment for six months while working abroad. They expect the landlord to refuse based on liability and lease terms.

**Trigger:** "I need to ask my landlord to let me sublet for six months. He's going to say no. Help me prepare."

**Process:**
- Raw accusations: "You're trying to get around the lease," "You'll get a stranger into my property," "I'll be liable for anything that goes wrong," "You're making this my problem," "You're going to cause damage and disappear."
- Labels converted using the formula, ordered from most to least charged
- Delivery script prepared for the phone call

**Output (`accusation-audit.md` excerpt):**
```
Label 1: "It seems like the idea of someone you don't know in your property is a real concern."
[Pause 3-5 seconds]

Label 2: "It sounds like you might be worried this would create liability issues for you."
[Pause 3-5 seconds]

Label 3: "It seems like this request might feel like I'm trying to get around the terms we agreed to."
[Pause 3-5 seconds]

Transition: "I'd like to walk you through exactly what I'm proposing and how I want to protect your interests throughout."
```

---

### Example 3: Sales Call with a Burned Prospect

**Scenario:** A SaaS sales rep is calling a prospect who tried a competitor's product, had a bad experience, and has been unresponsive to outreach for two months. The rep got a reluctant 20-minute call booked.

**Trigger:** "This prospect got burned by our competitor and I think they'll shut me down in the first two minutes. Help me prepare an opening."

**Process:**
- Raw accusations: "You're just like the last vendor," "This is going to waste my time," "Whatever you say will sound like the last pitch," "I've already made up my mind," "You're going to overpromise."
- Labels generated; strongest accusation (past bad experience → distrust) goes first
- Voice guidance added: FM DJ tone — slow, calm, no enthusiasm, no salesperson energy

**Output (`accusation-audit.md` excerpt):**
```
Label 1: "It seems like you've had experiences with vendors that didn't deliver what they promised."
[Pause 3-5 seconds]

Label 2: "It sounds like the last time you invested time in evaluating a new tool, it didn't go well."
[Pause 3-5 seconds]

Label 3: "It seems like you might be wondering whether this call is going to be different or just more of the same."
[Pause 3-5 seconds]

Transition: "I'm not going to pitch you today. I want to understand what actually happened and whether what we do is even relevant to your situation."
```

---

## References

- [references/emotion-labeling-mechanics.md](references/emotion-labeling-mechanics.md) — Affect labeling research, labeling formula variations, common mistakes
- [references/five-label-templates.md](references/five-label-templates.md) — All 5 fill-in-the-blank label templates with example completions
- [references/tactical-empathy-vs-sympathy.md](references/tactical-empathy-vs-sympathy.md) — Distinction between validation and sympathy; why sympathy undermines negotiation
- [references/three-voices-guide.md](references/three-voices-guide.md) — FM DJ voice vs positive/playful vs assertive: when to use each, inflection rules

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Never Split the Difference: Negotiating as if Your Life Depended on It by Chris Voss.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
