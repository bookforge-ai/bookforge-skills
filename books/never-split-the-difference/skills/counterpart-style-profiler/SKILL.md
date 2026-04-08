---
name: counterpart-style-profiler
description: |
  Profile a negotiation counterpart's communication style and generate a tailored adaptation strategy. Use when asking "how should I approach this person?", "what communication style does my counterpart prefer?", "why is this negotiation not working?", "how do I adapt to this person's personality in negotiation?", or "what type of negotiator am I dealing with?" Also use for: diagnosing why previous conversations stalled or backfired; identifying whether warmth, data, or directness will land better; assessing self-type to avoid projecting your preferences onto the counterpart; preparing counterpart profiles for a negotiation one-sheet. Classifies counterparts into one of three communication archetypes (Analyst, Accommodator, Assertive) using observable behavioral signals, then produces a specific adaptation strategy covering communication tempo, information delivery, relationship style, and risk areas. Works from conversation history, emails, meeting notes, colleague descriptions, or any observable behavior data.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/never-split-the-difference/skills/counterpart-style-profiler
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: never-split-the-difference
    title: "Never Split the Difference: Negotiating as if Your Life Depended on It"
    authors: ["Chris Voss"]
    chapters: [9]
tags: [negotiation, counterpart-profiling, communication-style, negotiator-types, analyst, accommodator, assertive, personality-assessment, adaptation-strategy, bargaining, conflict-resolution, sales, stakeholder-management]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Observable counterpart behavior — conversation history, emails, meeting notes, colleague descriptions, or a written situation brief describing how the counterpart has communicated"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Works from pasted text, document files, or a verbal description of counterpart behavior."
discovery:
  goal: "Classify a counterpart's communication archetype and produce an actionable adaptation strategy that changes how you communicate — tempo, information density, relationship-building approach, and risk areas to avoid"
  tasks:
    - "Collect behavioral signals from counterpart history"
    - "Score counterpart against three archetype profiles"
    - "Identify the dominant archetype (and any secondary blend)"
    - "Assess user's own type to flag projection risk"
    - "Produce a counterpart-profile.md with classification, adaptation strategy, and risk areas"
  audience:
    roles: ["salesperson", "founder", "manager", "consultant", "recruiter", "lawyer", "freelancer", "anyone-who-negotiates"]
    experience: "any — no formal negotiation training required"
  triggers:
    - "User describes a counterpart and asks how to approach them"
    - "User reports that their usual style isn't working with a specific person"
    - "User is preparing a negotiation and wants to tailor their communication approach"
    - "User wants to understand why a previous negotiation stalled or went sideways"
    - "User asks whether to lead with data, relationship-building, or directness"
  not_for:
    - "Generating the full negotiation one-sheet — use negotiation-one-sheet-generator"
    - "Designing calibrated questions — use calibrated-questions-planner"
    - "Planning the Ackerman offer sequence — use ackerman-bargaining-planner"
    - "Discovering hidden constraints or unknown unknowns — use black-swan-discovery"
---

# Counterpart Style Profiler

## When to Use

You are preparing for a negotiation, sales conversation, or difficult discussion and need to tailor your communication approach to the specific person you are dealing with. You have some observable data about how they communicate — emails, meeting behavior, prior conversation history, or secondhand descriptions — and want to translate that into a concrete adaptation strategy before the conversation begins.

This skill works in two scenarios:

1. **Pre-negotiation preparation:** You have some information about the counterpart and want a communication blueprint before first contact or before a critical conversation.
2. **Mid-negotiation diagnosis:** A conversation has stalled, or your usual approach isn't working, and you need to identify why and adjust.

**Do not use this skill if:** You have no information about the counterpart whatsoever. The profile requires at least a few observable signals to be reliable. Proceed with the Analyst archetype defaults (data-driven, slow pace, minimal warmth) as a low-risk starting posture when blind.

---

## Context & Input Gathering

### Required
- **Observable behavior:** At least 2–3 signals about how the counterpart communicates. Examples:
  - Written: email tone, response time, level of detail, use of pleasantries
  - Spoken: speaking pace, tendency to interrupt, whether they ask questions or make statements
  - Meeting behavior: how they react to silence, whether they bring data or tell stories
  - Colleague descriptions: "He's all business," "She wants to be your friend," "He always needs to think before answering"

### Important
- **Context of the relationship:** First contact, existing working relationship, adversarial history?
- **Stakes and setting:** High-pressure price negotiation, collaborative partnership discussion, employment offer?
- **Your own communication style:** What type are you? This is needed to flag projection risk.

### Defaults
- If communication history is available, use it as primary evidence.
- If only secondhand description is available, treat the classification as provisional and note it in the output.
- If no information is available at all, use Analyst defaults as a conservative starting posture — explain this choice in the output.

### Sufficiency check
If you have fewer than 2 behavioral signals, ask the user to describe one specific interaction with the counterpart before proceeding. A single data point is not enough to classify reliably.

---

## Process

### Step 1: Extract Behavioral Signals

**Action:** Read all available input about the counterpart. List every observable behavioral signal that relates to communication style. Separate signals into three categories: *pace and silence*, *relationship and warmth*, *directness and information style*.

**WHY:** Different archetypes manifest across different behavioral dimensions. An Analyst's signature is silence and deliberate pace. An Accommodator's signature is warmth and relationship emphasis. An Assertive's signature is time pressure and directness. Grouping signals by dimension prevents one strong signal from drowning out contradictory evidence in other dimensions. Missing any category risks misclassification.

Signals to look for:
- **Pace and silence:** Response time to emails/messages; comfort with pauses in conversation; how often they rush to fill silence; whether they make fast or slow decisions
- **Relationship and warmth:** How much time they spend on small talk; whether they ask personal questions; how they open and close communications; whether they express appreciation or warmth spontaneously
- **Directness and information style:** Whether they lead with conclusions or build up to them; how they react to detailed data vs. summaries; whether they interrupt or let others finish; how they express disagreement

---

### Step 2: Score Against Three Archetype Profiles

**Action:** For each of the three archetypes below, score the counterpart 1–5 based on how well the behavioral signals match. A score of 5 means strong match across all three signal dimensions. A score of 1 means signals contradict this archetype.

**WHY:** Scoring all three archetypes — not just the most obvious one — prevents premature commitment to a misclassification. Many counterparts show partial signals from two archetypes (especially Analyst/Assertive blends). Scoring explicitly surfaces mixed profiles and prevents the most common error: projecting your own type onto the counterpart.

**Archetype profiles:**

**Analyst**
- *Pace and silence:* Responds slowly, needs time to think, comfortable with long silences — does not rush to fill them. May not respond to messages immediately. Makes decisions carefully and slowly.
- *Relationship and warmth:* Reserved about personal topics. Not cold, but does not initiate small talk or express warmth readily. Relationship is built through reliability and demonstrated competence, not social bonding.
- *Directness and information style:* Leads with data, facts, and logic. Distrusts assertions without supporting evidence. Asks probing questions. Prefers comprehensive information before committing. May seem skeptical or unemotional. Does not like surprises.
- *Vulnerability:* Silence is thinking time, not a signal to be pushed. Rushing an Analyst or providing insufficient data produces resistance. Surprises feel like ambushes and create distrust.
- *Self-type note:* If you are an Analyst, watch for projecting your preference for data and deliberation onto counterparts who communicate very differently.

**Accommodator**
- *Pace and silence:* Conversationally active — tends to fill silences, enjoys dialogue, will often prolong conversations. Moves at a relationship pace rather than a task pace.
- *Relationship and warmth:* Leads with relationship. Uses first names, expresses genuine interest in your life and situation, sends friendly messages, may bring up personal topics before business. The relationship is the goal, not just a means.
- *Directness and information style:* Often agrees verbally without following through. Says "yes" or "sounds good" easily — watch for confirmation without commitment. Dislikes conflict and will often signal agreement to avoid tension, even if they haven't actually committed. May overpromise.
- *Vulnerability:* Their verbal agreement is often aspirational, not contractual. Pushing an Accommodator too hard or fast damages the relationship, which is their primary concern. Silence from an Accommodator is unusual and signals something is wrong.
- *Self-type note:* If you are an Accommodator, you may read warmth as commitment and miss the gap between their verbal enthusiasm and actual follow-through.

**Assertive**
- *Pace and silence:* Fast communicators. Gets to the point quickly. May interrupt. Treats time as money — long preambles or relationship-building before getting to the point feel like waste. Responds to emails quickly and expects quick responses.
- *Relationship and warmth:* Not relationship-first, but not hostile — they are direct because they respect your time. They value being heard and understood above being liked. Getting to "yes" is the goal; the relationship is a by-product.
- *Directness and information style:* States positions clearly and bluntly. Does not hedge. Reacts poorly to perceived evasion or over-explanation. Expects you to be equally direct. Needs to feel that they have been heard and understood before they will listen to your position.
- *Vulnerability:* They need to feel heard before they can hear you. Launching directly into your position or counter-argument before acknowledging theirs produces defensiveness and entrenchment. Warmth without substance reads as weakness or manipulation.
- *Self-type note:* If you are an Assertive, you may project bluntness as a universal virtue and come across as aggressive with Analysts and Accommodators.

**Scoring template:**
```
Analyst:       [1–5] — [one-sentence rationale citing specific signals]
Accommodator:  [1–5] — [one-sentence rationale citing specific signals]
Assertive:     [1–5] — [one-sentence rationale citing specific signals]
```

---

### Step 3: Classify the Dominant Archetype

**Action:** Identify the highest-scoring archetype as the primary classification. If two scores are within 1 point of each other, classify as a blend and name both (e.g., "Analyst-Assertive blend"). If all three scores are similar, classify as adaptive and note that this counterpart may shift style by context.

**WHY:** A single dominant classification generates cleaner, more actionable adaptation guidance. Blends are real and common — acknowledging them prevents the user from forcing a misfit strategy. Adaptive counterparts require a different approach: observe first, adapt to the style they present in the specific conversation rather than relying on a fixed profile.

**Blend rules:**
- Analyst + Assertive: Data-driven and direct. Give them facts quickly, without preamble. They want comprehensive information delivered efficiently.
- Analyst + Accommodator: Methodical and warm. Build relationship slowly through competence and follow-through. Don't rush.
- Accommodator + Assertive: Relationship-forward but decisive. Lead with genuine warmth, then be direct about what you need. Watch for the Accommodator tendency to say yes without follow-through despite the Assertive pace.

---

### Step 4: Assess User's Own Type and Flag Projection Risk

**Action:** Ask the user to identify their own communication style (or infer it from how they have described the situation and their frustration with the counterpart). Score the user's self-described type against the same archetypes. Compare user type to counterpart type. Flag any projection risks.

**WHY:** The most common counterpart profiling error is projecting your own style. Analysts assume everyone needs time and data. Accommodators assume everyone wants relationship before business. Assertives assume directness is universally respected. Identifying the user's own type enables a specific warning: "You are an Assertive; your counterpart is an Analyst. Your instinct to get to the point quickly will feel like pressure to them. Pause and give them time to process."

**Projection risk table:**

| Your Type | Their Type | Risk |
|-----------|-----------|------|
| Analyst | Accommodator | You may neglect relationship-building that they require before they trust your data |
| Analyst | Assertive | You may over-explain; they want conclusions first, supporting data on request |
| Accommodator | Analyst | Your warmth may feel irrelevant; they need evidence, not rapport |
| Accommodator | Assertive | Your tendency toward lengthy relationship conversations will frustrate them |
| Assertive | Analyst | Your pace will feel like pressure; they will shut down or become evasive |
| Assertive | Accommodator | Your bluntness may damage the relationship they need before saying yes |

---

### Step 5: Generate Adaptation Strategy

**Action:** Produce a concrete adaptation strategy for the classified counterpart type. The strategy must cover four areas: communication tempo, information delivery, relationship approach, and risk areas to avoid. Include 2–3 specific do/don't examples for the classified type.

**WHY:** Generic advice ("communicate clearly," "build rapport") does not change behavior. Specific, type-matched rules do. An Analyst needs to hear "send supporting data before your ask, not after" — not "be thorough." An Assertive needs to hear "lead with a label that shows you understand their position before making your counter" — not "be direct." The adaptation strategy should be specific enough that the user can change what they say in the next conversation.

**Strategy template by type:**

*Analyst adaptation:*
- Tempo: Slow down. Build in response time. Do not follow up immediately after sending information.
- Information delivery: Front-load data and evidence. Provide supporting materials before or with your ask, not after they push back. Do not surprise them with new information mid-conversation.
- Relationship: Build trust through reliability and accuracy, not warmth. Follow through on every commitment you make.
- Risk areas: Do not interpret silence as resistance or discomfort — it is processing time. Do not pressure for a decision before they are ready. Avoid vague assertions ("this is a great deal") without supporting evidence.

*Accommodator adaptation:*
- Tempo: Match their conversational pace. Allow for relationship talk before business. Do not skip to the ask.
- Information delivery: Frame information in terms of relationship impact ("I want to make sure this works for both of us") and how it helps them achieve their goals. They respond to being seen and understood.
- Relationship: Invest in genuine relationship-building. Ask about them. Remember prior personal details. Express appreciation explicitly.
- Risk areas: Treat verbal agreement as a starting point, not a commitment — verify with specific follow-up ("So just to confirm, you'll have this done by Friday?"). Do not misread warmth as a "yes." Silence from an Accommodator is unusual and warrants gentle inquiry.

*Assertive adaptation:*
- Tempo: Match their pace. Get to the point. Do not open with pleasantries if they haven't. Respond to messages promptly.
- Information delivery: Lead with your conclusion, then offer supporting data if they ask. Do not build up slowly to a point — state it.
- Relationship: Earn their respect by being direct and competent, not by being warm. They will respect you more for pushing back on something wrong than for agreeing.
- Risk areas: Do not launch into your position before acknowledging theirs — they need to feel heard first. Use a brief label before making a counter-offer ("It sounds like timeline is the main concern — here's what I can do on that"). Avoid anything that reads as weakness: excessive hedging, premature concessions, apologetic framing.

---

### Step 6: Write the Output Artifact

**Action:** Produce a `counterpart-profile.md` document containing the full classification, scoring, adaptation strategy, projection risk note, and the user's self-type assessment.

**WHY:** The output artifact must be written to disk, not just explained in the conversation. It serves as a reference document the user reads immediately before a conversation. A mental note of "they're probably an Analyst" will not survive the pressure of a live negotiation. A one-page document they review beforehand will.

---

## Inputs / Outputs

### Inputs
- Behavioral observations about the counterpart (required — at minimum 2–3 signals)
- Communication history: emails, meeting notes, conversation transcripts (optional but improves accuracy)
- User's own communication style / self-assessment (optional — used for projection risk check)
- Relationship context: first contact, ongoing relationship, adversarial history (optional)

### Outputs

**Primary output:** `counterpart-profile.md`

```markdown
# Counterpart Profile: [Name / Role]

**Date:** [date]
**Situation:** [brief context — what negotiation, what's at stake]

---

## Classification

**Primary Type:** [Analyst / Accommodator / Assertive]
**Confidence:** [High / Medium / Provisional — note if based on limited signals]
**Blend:** [If applicable — e.g., "Analyst-Assertive blend"]

### Scoring
| Archetype | Score (1–5) | Key Signals |
|-----------|------------|-------------|
| Analyst | [X] | [signals cited] |
| Accommodator | [X] | [signals cited] |
| Assertive | [X] | [signals cited] |

---

## Behavioral Signals Observed

- [Signal 1 — with source: email on [date], meeting on [date], etc.]
- [Signal 2]
- [Signal 3]
- [Add as many as available]

---

## Adaptation Strategy

### Communication Tempo
[Specific guidance — slow down / match pace / etc.]

### Information Delivery
[What to lead with, what to defer, how to structure asks]

### Relationship Approach
[How to build trust with this specific type]

### Language to Use
- "[Example phrase or framing that works for this type]"
- "[Example phrase or framing that works for this type]"

### Language to Avoid
- "[Example phrase or pattern that backfires for this type]"
- "[Example phrase or pattern that backfires for this type]"

---

## Risk Areas

- [Risk 1 — specific to this type and this situation]
- [Risk 2]
- [Risk 3 — self-type projection risk if applicable]

---

## Self-Type Assessment

**Your Type:** [Analyst / Accommodator / Assertive / Unknown]
**Projection Risk:** [Specific warning based on your type vs. their type]

---

## Next Steps

- [ ] Review this profile immediately before the conversation
- [ ] Use [skill reference] for calibrated question design
- [ ] Use [skill reference] for offer sequencing
```

---

## Key Principles

**Observable behavior overrides assumptions.** Do not classify based on role, title, culture, or demographic. Classify based on what the counterpart has actually said and done. A senior executive may be an Accommodator; a junior analyst may be an Assertive. The signals are in the behavior, not the position.

**Your own type is the biggest source of profiling error.** You will naturally notice and weight signals that match your own communication preferences. An Assertive user will remember the counterpart's blunt moments and underweight their warmth. Explicitly identifying your own type and running the projection risk check is not optional — it corrects the most common classification failure.

**Type mismatches cause avoidable failures.** Treating an Analyst like an Assertive (rushing, pushing for quick decision) produces evasion and withdrawal. Treating an Assertive like an Accommodator (leading with warmth, taking time for relationship) reads as weakness or evasion. These failures are entirely preventable once the counterpart's type is known. The adaptation is not subtle — it changes what you say in the first 60 seconds.

**Accommodate the counterpart's style, not your comfort.** Adapting to an Assertive when you are an Accommodator may feel unnatural. Slowing down for an Analyst when you are an Assertive may feel like wasted time. This discomfort is the adaptation working correctly. The goal is not comfortable communication — it is effective communication for this specific person.

**The Assertive needs to be heard before they can hear you.** This is the most consistently violated rule for Assertive counterparts. Launching into your position before acknowledging theirs triggers defensiveness, not engagement. A single label ("It sounds like timeline is the main issue here") before your counter costs nothing and changes everything.

**Silence means different things for each type — misreading it is one of the most common type-mismatch failures.** For an Analyst, silence means they are processing — wait patiently and do not rush to fill it. For an Accommodator, silence means discomfort or suppressed disagreement — gently label it ("It seems like something's on your mind") rather than letting it sit. For an Assertive, silence from you is interpreted as having nothing to say — they will fill it with their own position, which is actually useful (let them talk). Applying the wrong silence response to the wrong type causes immediate damage: rushing an Analyst's silence reads as pressure; ignoring an Accommodator's silence lets the unspoken objection harden; filling silence too quickly with an Assertive robs you of information.

**When dealing with an Assertive counterpart, always acknowledge their position with a label BEFORE presenting your counter-position.** Assertives do not process new information until they feel heard. If you counter before acknowledging, they will simply repeat their position louder. The sequence is: label their position ("It sounds like you feel strongly that X"), wait for confirmation, THEN present your alternative. Skipping the label and going straight to the counter is the single most consistent source of escalation with Assertive counterparts.

---

## Examples

### Example 1: Pricing Negotiation with a Procurement Manager

**Scenario:** A sales rep preparing for a final pricing negotiation with a procurement manager. The manager has sent three highly detailed emails with numbered questions, requested a full pricing breakdown with line items, took five days to respond to the last message, and opened the first meeting with "Let's get right to the numbers."

**Trigger:** "How should I approach this negotiation? He's very analytical but also seems impatient."

**Process:**
- Step 1: Signals — detailed numbered questions (directness, information style), full pricing breakdown requested (data preference), 5-day response time (deliberate pace), "get right to the numbers" (time-efficient, task-focused)
- Step 2: Analyst=4 (data-driven, detailed, deliberate pace), Assertive=3 (direct opener, time-efficiency signal), Accommodator=1 (no warmth signals)
- Step 3: Primary type: Analyst with Assertive secondary — classify as Analyst-Assertive blend
- Step 4: User self-identifies as Accommodator → projection risk: user will want to build warmth before numbers; counterpart wants numbers immediately
- Step 5: Tempo — be prompt but don't rush decision. Information — lead with a complete pricing breakdown before the meeting, not in response to pushback. Relationship — skip extended small talk; open with "I've prepared the full breakdown you asked for." Risk — don't interpret slow response time as doubt; don't pad with warmth that reads as evasion

**Output:** `counterpart-profile.md` classifying as Analyst-Assertive blend, adaptation strategy leading with data delivery, projection risk warning for Accommodator user, language examples ("Here's the complete breakdown — happy to walk through any line item you want to dig into" vs. avoid "I just want to make sure we have a good relationship here before we get into numbers").

---

### Example 2: Salary Negotiation with a Hiring Manager

**Scenario:** A candidate preparing for salary negotiation with a hiring manager who has been very friendly throughout the interview process, asked personal questions about the candidate's family and career journey, said "I'm sure we can make this work" multiple times, but has not yet made a concrete offer after three conversations.

**Trigger:** "She keeps saying yes but nothing is moving. How should I approach asking for a number?"

**Process:**
- Step 1: Signals — personal questions (high warmth), "sure we can make this work" (verbal agreement without commitment), three conversations without concrete offer (avoidance of conflict), friendly throughout (relationship emphasis)
- Step 2: Accommodator=5 (all signals match), Analyst=1 (no data or deliberation signals), Assertive=1 (no directness or pace signals)
- Step 3: Primary type: Accommodator (high confidence)
- Step 4: User self-identifies as Analyst → projection risk: user may over-explain rationale and data for the salary ask; the manager needs to feel the relationship is good before committing
- Step 5: Tempo — allow relationship talk before business; don't rush. Information delivery — frame the ask in terms of the relationship and mutual success, not market data. Relationship — acknowledge the warmth explicitly before making the ask. Risk — verbal "yes" from an Accommodator is not a commitment; close with a specific follow-up: "So can we agree to [specific number] and have an offer letter by [date]?" Silence means something is wrong — check in.

**Output:** `counterpart-profile.md` classifying as Accommodator, adaptation strategy prioritizing relationship acknowledgment before the ask, specific language for closing ("I really appreciate how collaborative this process has been — I'd love to confirm the number and timeline so I can get excited about next steps"), and explicit warning that "I'm sure we can make this work" is not a commitment.

---

### Example 3: Partnership Negotiation with a Co-founder

**Scenario:** A founder trying to negotiate equity terms with a potential co-founder. The potential co-founder responds to messages within minutes, jumps to conclusions quickly, stated his equity expectations in the first meeting ("I need at least 30%"), interrupted twice when the founder was explaining the rationale, and pushed back hard when the founder said "let me think about it."

**Trigger:** "Every time I try to explain my reasoning, he cuts me off. What am I doing wrong?"

**Process:**
- Step 1: Signals — minute-level response time (fast pace), stated position immediately (direct, no preamble), interrupted twice (impatient with build-up), pushed back on "let me think about it" (time-is-money, wants momentum)
- Step 2: Assertive=5 (all signals match strongly), Analyst=1, Accommodator=1
- Step 3: Primary type: Assertive (high confidence)
- Step 4: User self-identifies as Analyst → projection risk: user's instinct to explain full rationale before stating position is exactly what causes the interruptions
- Step 5: Tempo — respond quickly, match his pace. Information delivery — lead with the number, offer rationale only if asked. Relationship — respect is earned by being direct and holding a position, not by explaining it. Risk — do not launch into rationale before acknowledging his 30% position; use a label first: "It sounds like you see your contribution as worth 30% of the outcome — I want to make sure I understand what's driving that before responding." Then state your position directly.

**Output:** `counterpart-profile.md` classifying as Assertive, adaptation strategy emphasizing label-first approach before counter-positions, explicit example language ("It sounds like timeline is the main concern — here's what I can do on that"), and projection risk warning for the Analyst user to front-load conclusion, not rationale.

---

## References

| File | Contents |
|------|----------|
| `references/type-profiles.md` | Full behavioral signal inventory per type; diagnostic question bank; cross-cultural considerations; blend profiles; adaptation scripts by context (email, phone, in-person, high-stakes vs. routine) |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Never Split the Difference: Negotiating as if Your Life Depended on It by Chris Voss.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
