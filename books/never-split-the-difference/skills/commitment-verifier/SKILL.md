---
name: commitment-verifier
description: |
  Verify whether a counterpart's agreement is a real commitment or a polite escape. Use when someone asks "how do I know if they really mean yes?", "they agreed but I'm not sure they'll follow through", "my counterpart said yes but something feels off", "how do I tell if someone is stringing me along?", or "they said you're right — is that agreement?" Also use for: detecting when a verbal commitment won't survive contact with implementation, distinguishing genuine alignment from social pressure compliance, spotting deception signals in a counterpart's language or delivery, checking whether the decision-maker in the room actually has authority to commit, or preparing verification questions before a closing conversation. Analyzes an agreement interaction — conversation transcript, notes, or recalled exchange — and classifies each yes-type, flags verbal deception indicators, surfaces channel mismatches (words vs. tone vs. body language), and generates Rule of Three follow-up questions to confirm genuine commitment. Works for sales closes, contract negotiations, vendor agreements, hiring decisions, partnership deals, project sign-offs, and any high-stakes conversation where the difference between a real yes and a polite yes determines whether effort is wasted. Pair with calibrated-questions-planner (to design verification questions) and empathic-summary-planner (to build the rapport that makes genuine commitment possible).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/never-split-the-difference/skills/commitment-verifier
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: never-split-the-difference
    title: "Never Split the Difference: Negotiating as if Your Life Depended on It"
    authors: ["Chris Voss"]
    chapters: [4, 5, 8]
tags: [negotiation, commitment, verification, deception-detection, yes-types, rule-of-three, pinocchio-effect, body-language, tone, baseline-deviation, closing, sales, agreement-quality, counterpart-analysis]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Conversation transcript, notes, or recalled exchange — the interaction in which the agreement was made, including any relevant context leading up to it"
    - type: document
      description: "Agreement statements — the specific things the counterpart said that constitute the 'yes' (exact words matter for deception signal analysis)"
    - type: document
      description: "Behavioral observations (optional) — anything you noticed about their tone, body language, energy, eye contact, posture, or pace during or after the agreement"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Works with pasted notes, recalled conversations, or written transcripts."
discovery:
  goal: "Classify the quality of each agreement made, flag deception signals in language and delivery, and produce verification questions that will reveal whether commitment is genuine before you invest further resources"
  tasks:
    - "Classify each identified agreement as Counterfeit, Confirmation, or Commitment yes"
    - "Analyze verbal deception indicators: word count inflation, pronoun avoidance, sentence complexity, third-person distancing"
    - "Check for 7-38-55 channel mismatches between words, tone, and observed body language"
    - "Identify baseline deviations from the counterpart's normal communication style"
    - "Generate Rule of Three verification sequence for each unconfirmed commitment"
    - "Flag any behind-the-table stakeholders whose absence makes the commitment structurally unreliable"
    - "Write commitment-assessment.md with full analysis and verification action plan"
  audience:
    roles: ["salesperson", "founder", "manager", "consultant", "account-executive", "procurement", "recruiter", "negotiator", "partnerships-manager"]
    experience: "beginner to intermediate — no prior negotiation training required"
  triggers:
    - "User has received a yes but is uncertain whether it will translate to action"
    - "User wants to verify commitment before investing significant time or resources in implementation"
    - "User noticed a mismatch between what the counterpart said and how they said it"
    - "User is dealing with a counterpart who tends to agree verbally without following through"
    - "User needs to distinguish between social compliance and genuine decision-maker commitment"
    - "User wants to design closing questions that surface real objections before they appear as cancellations"
  not_for:
    - "Generating the initial negotiation preparation document — use negotiation-one-sheet-generator"
    - "Designing the questions to ask during negotiation — use calibrated-questions-planner"
    - "Building the empathic summary that produces genuine alignment — use empathic-summary-planner first"
    - "Profiling a counterpart's communication style — use counterpart-style-profiler"
  quality: placeholder
---

# Commitment Verifier

## When to Use

You have received an agreement — a "yes," a verbal commitment, a signed-off plan, or an "I'm on board" — and something makes you uncertain whether it will survive contact with reality. The counterpart was agreeable, but you are not sure if they were agreeing to get out of the conversation, acknowledging a point without committing to act on it, or making a genuine commitment they intend to honor.

This skill works both pre-close (verifying before you proceed) and post-close (diagnosing why a commitment is stalling). You bring the conversation notes or transcript; the skill classifies what kind of yes you received, flags signals of deception or hedging, and produces a verification sequence to confirm genuine commitment or surface the real objection.

**Input this skill needs:** What was said (the agreement statements), how it was said (tone, energy, body language if observed), and any context about the relationship and interaction.

**Do not use this skill if:** You have not yet had the commitment conversation — first build rapport using `empathic-summary-planner` and generate your question bank using `calibrated-questions-planner`. This skill works on agreements already made, not on conversations yet to happen.

---

## Context & Input Gathering

### Required
- **The agreement statements:** The specific words the counterpart used to agree. Exact phrasing matters — "absolutely" and "yeah, sure" carry different signals.
- **What was agreed to:** The substance of the commitment — what they said they would do, decide, or approve.
- **When and how it came up:** Was it volunteered or prompted? After pressure or naturally? At the end of a long conversation or early?

### Important
- **Their tone and energy during agreement:** Did they sound enthusiastic, flat, distracted, over-eager? Any notable change from their normal pattern?
- **Body language if observed:** Eye contact, posture, pace of response, physical engagement or withdrawal.
- **What came before the agreement:** Were there unresolved objections, pending approvals, or stakeholders mentioned who weren't present?

### Observable
- **Follow-through signals:** Have they taken any action since agreeing — sent a follow-up, copied colleagues, initiated next steps?
- **Pronoun patterns:** Did they use "I will" or "we'll need to," "I'm committed" or "that sounds good"? Pronoun choice is a key deception signal.
- **Word count:** Did their agreement come with an unusually long explanation? Did they over-justify?

### Defaults (used if not provided)
- **Baseline behavior:** Assume the current sample is the only behavioral data available — flag deviations from internal consistency within the conversation itself.
- **Stakeholder completeness:** Assume that unless the decision-maker's identity and authority have been explicitly confirmed, at least one unconfirmed approver exists.

### Sufficiency check
If you have the agreement statements and a basic description of how the conversation went, proceed. Behavioral observations enrich the analysis but are not required.

---

## Process

### Step 1: Classify Each Agreement as One of Three Yes Types

**Action:** For each statement the counterpart made that constitutes a "yes," classify it as one of three types based on its diagnostic signals:

**Counterfeit Yes** — an agreement to escape the conversation, not to commit. The counterpart has no intention of following through. Signals: vague phrasing ("sounds good," "we'll see," "let's circle back"), no specifics on next steps, agreement came under pressure or was given quickly to end the discussion, tone flat or rushed.

**Confirmation Yes** — an acknowledgment that a fact is true, not a commitment to act. The counterpart understands and agrees with what you said but has not agreed to do anything. Signals: "yes, that's right," "I understand," "correct" — statements that confirm a point without specifying action. Often follows a question that asks for confirmation rather than action.

**Commitment Yes** — a genuine agreement to take a specific action. Signals: specific next steps named ("I'll send the contract by Friday"), ownership language ("I will," "I'm going to," "I'll handle"), the counterpart introduced details or logistics without being asked, their energy level rose with the agreement.

**WHY:** Most negotiations are lost not at the objection stage but at the false close — when you treat a Counterfeit or Confirmation yes as a Commitment and stop working the deal. The counterpart who says "yes" to make you feel good and then goes quiet is not deceiving maliciously — they are following the social instinct to avoid conflict. Distinguishing yes types before you invest in implementation protects your time and prevents the confusion of wondering why a "committed" counterpart has gone dark.

**IF** the agreement statement is ambiguous → mark it as unclassified and flag it for Rule of Three verification in Step 4.
**IF** the agreement was made under time pressure or at the end of a long conversation → weight toward Counterfeit or Confirmation until verified.

---

### Step 2: Analyze Verbal Deception Indicators (Pinocchio Effect)

**Action:** Read the counterpart's agreement statements and flag the presence of any of these four verbal deception indicators:

1. **Word count inflation** — Did they use significantly more words than necessary to express agreement? Genuine commitment tends to be direct ("I'll do it"). Deceptive or uncertain agreement often comes with elaborate justification, qualifications, or tangential explanation.

2. **First-person pronoun avoidance** — Did they use "I" or avoid it? Statements like "we'll get that sorted" or "that will happen" or "it should be fine" distance the speaker from ownership of the commitment. Genuine commitments tend to be first-person: "I will," "I'm going to," "I'll take care of that."

3. **Third-person distancing** — Did they refer to themselves in the third person, or refer to "the company" / "the team" / "our process" as the actor rather than themselves? This diffuses responsibility and signals they are not personally committed to the outcome.

4. **Sentence complexity increase** — Did the agreement come out in compound, qualified sentences full of conditionals ("as long as everything goes smoothly," "assuming the timeline holds," "provided nothing changes")? Genuine commitment is usually simple and direct. Complexity at the commitment moment is a hedge.

**WHY:** When people are not telling the whole truth — whether they're actively deceiving or simply uncertain — their language changes in predictable ways. They use more words because they're constructing rather than recalling. They avoid first-person pronouns because committing the "I" feels more psychologically binding. They add complexity and qualifiers because they're leaving themselves escape routes. These signals do not prove deception; they flag uncertainty worth verifying. Even when the counterpart is not consciously lying, these patterns often signal that they're not fully committed — they may not know yet whether they can actually deliver on what they're agreeing to.

**Flag each signal found.** A single signal is a soft flag. Two or more signals in the same statement is a strong flag requiring Rule of Three verification.

---

### Step 3: Check for 7-38-55 Channel Mismatches

**Action:** If you have tone or body language observations, apply the 7-38-55 communication channel framework:

- **7% of meaning is carried by words** — what was literally said
- **38% is carried by tone** — the pace, volume, energy, warmth, or flatness of delivery
- **55% is carried by body language** — posture, eye contact, physical engagement or withdrawal

**Mismatch rule:** When the words say yes but the tone is flat, rushed, or disengaged — discount the words. When the words say yes but the body language shows withdrawal (leaning back, reduced eye contact, closed posture) — discount the words. Alignment across all three channels is the strongest signal of genuine commitment.

**If observations are available, rate each channel:**
- Words: what they said (positive/neutral/negative)
- Tone: how they sounded (engaged/flat/rushed/warm)
- Body language: how they appeared (open/closed/distracted/energized)

**If channels conflict** — flag as a channel mismatch and escalate to Rule of Three verification.

**WHY:** The 7-38-55 framework reflects a well-documented asymmetry in communication: people have conscious control over their words but significantly less control over their tone and body language under stress or uncertainty. A counterpart who has decided to say yes to end a difficult conversation will choose positive words — but their voice and body often betray the discomfort or lack of conviction underneath. The channels where people have less conscious control carry more signal about their actual internal state than the channel (words) where they have the most control.

**IF** no behavioral observations are available → skip this step and note "channel data unavailable — rely on verbal signals only."

---

### Step 4: Apply the Rule of Three Verification Protocol

**Action:** For each agreement that was classified as Counterfeit or Confirmation, or flagged by deception indicators or channel mismatch, design a three-confirmation sequence using three different techniques:

**Confirmation 1 — Direct restatement:** Ask the counterpart to restate the commitment in their own words. "Just so we're aligned — can you walk me through what you're planning to do from here?" A genuine commitment can be restated easily. A Counterfeit yes often produces vague or deflecting answers.

**Confirmation 2 — Implementation framing:** Ask a "how" question about the mechanics of execution. "How are you planning to handle [the specific commitment]?" This forces them to think through implementation. If they can't describe the implementation, they haven't actually committed.

**Confirmation 3 — Obstacle surfacing:** Ask what could get in the way. "What obstacles do you see on your end?" or "What would make this harder to pull off than expected?" A Commitment yes engages with this question practically — the counterpart thinks about obstacles and discusses them. A Counterfeit yes often deflects: "Oh, I don't think there'll be any issues."

**WHY:** A genuine commitment is stable under three different framings. Counterfeit and Confirmation yeses, being social rather than substantive, tend to crack under even mild re-examination — not because the counterpart is malicious, but because the commitment was never solidly formed. The Rule of Three works because it's too cognitively expensive to maintain an uncommitted yes across three differently-structured confirmation requests. Each time you ask, they must reconstruct the same false commitment from a different angle — and the cracks show. Three confirmations also create a record: if a counterpart confirms three times and still doesn't follow through, the issue is execution capacity or external constraint, not intent — and that changes how you respond.

**Space the three confirmations out** — do not ask them in a row in one conversation. Use them across different touchpoints (end of meeting, follow-up email, kick-off call) unless urgency requires otherwise.

---

### Step 5: Detect Behind-the-Table Stakeholders via Pronoun Analysis

**Action:** Review the agreement statements for pronouns that signal the presence of decision-makers who were not at the table.

**Signals to flag:**
- "We'll need to..." (who is "we"?)
- "That should be fine with us" (who else is "us"?)
- "Our process requires..." (whose process? Who controls it?)
- Absence of "I" ownership with substituted organizational pronouns ("the company needs," "our team would have to")

**If plural or organizational pronouns appear**, generate a stakeholder confirmation question: "When you say 'we' — who else is involved in this decision?"

**WHY:** In most organizational negotiations, the person agreeing is not the only person whose buy-in is required. When a counterpart uses collective pronouns at the commitment moment, it often signals — consciously or not — that they are speaking for a group they have not yet actually consulted. Detecting this before you proceed prevents the most common form of deal collapse: a genuine-seeming yes from someone who then has to "check with" people who say no. The pronoun pattern is often an involuntary signal: the counterpart is using "we" because they know they haven't secured internal alignment, and the language reflects that uncertainty.

---

### Step 6: Special Case — "You're Right" vs. "That's Right"

**Action:** If the counterpart said "you're right" — flag it immediately as a non-commitment signal.

**"You're right"** = dismissal. The counterpart is agreeing with your position to end the point, not agreeing to do something. It is a way of acknowledging your argument without accepting your conclusion. It typically signals that you have been pushing your position rather than drawing out theirs, and they are placating you to move the conversation forward.

**"That's right"** = genuine acknowledgment. The counterpart is saying that your summary or paraphrase of their position is accurate. This is a signal of felt understanding — they believe you have correctly represented their perspective — which creates the conditions for genuine movement.

**WHY:** The distinction matters because "you're right" is often followed by no change in behavior — the counterpart has given you a verbal win that costs them nothing. "That's right" is usually preceded by an accurate empathic summary, which means you have done the work of understanding them first. The sequence that produces "that's right" (active listening → paraphrase → label) is what builds the platform for genuine Commitment yes. If you got "you're right," the path to real commitment runs through empathic listening first.

**If "you're right" was the key agreement statement** → do not treat as commitment. Route to `empathic-summary-planner` to rebuild rapport, then re-approach the commitment.

---

### Step 7: Write the Output Artifact

**Action:** Write `commitment-assessment.md` with the full analysis: yes-type classifications, deception signal flags, channel analysis, verification questions, and a summary action plan.

**WHY:** A written artifact converts subjective impressions ("something felt off") into structured evidence that supports a clear decision about how to proceed. It also creates a record — if the counterpart later claims they never committed, the assessment documents what was said and how it was evaluated.

---

## Inputs / Outputs

### Inputs
- Agreement statements — what the counterpart said (required)
- Conversation context — how and when the agreement was made (required)
- Behavioral observations — tone, body language, energy (optional)
- Stakeholder context — who was and wasn't in the room (optional)

### Outputs

**File:** `commitment-assessment.md`

**Template:**

```markdown
# Commitment Assessment: [Situation / Deal Name]

**Prepared:** [Date]
**Counterpart:** [Name / role / organization]
**Interaction:** [Meeting, call, email, etc. — date and context]

---

## Agreement Inventory

| # | Agreement Statement (verbatim or recalled) | Yes Type | Confidence | Flags |
|---|-------------------------------------------|----------|------------|-------|
| 1 | "[exact words]" | Counterfeit / Confirmation / Commitment | High / Medium / Low | [signal flags] |
| 2 | "[exact words]" | Counterfeit / Confirmation / Commitment | High / Medium / Low | [signal flags] |

---

## Deception Signal Analysis

### Verbal Indicators (Pinocchio Effect)
- [ ] Word count inflation: [describe if present]
- [ ] First-person pronoun avoidance: [describe if present]
- [ ] Third-person distancing: [describe if present]
- [ ] Sentence complexity / over-qualification: [describe if present]

**Overall verbal signal rating:** Clean / Soft flags / Strong flags

---

## Channel Analysis (7-38-55)

| Channel | Observation | Signal |
|---------|-------------|--------|
| Words (7%) | [what they said] | Positive / Neutral / Negative |
| Tone (38%) | [how they sounded] | Engaged / Flat / Rushed / N/A |
| Body language (55%) | [how they appeared] | Open / Closed / Distracted / N/A |

**Channel alignment:** Aligned / Mismatch detected
**Mismatch notes:** [describe any conflict between channels]

---

## Stakeholder Completeness

- Decision-maker confirmed in room: Yes / No / Unknown
- Plural pronoun signals: [list any "we" / "our" / "the team" usage at commitment moment]
- Stakeholder confirmation question needed: Yes / No
  - Question: "[How does this decision involve the rest of your team?]"

---

## Rule of Three Verification Plan

*For each unconfirmed commitment, three confirmations required across different touchpoints.*

**Commitment 1:** [Agreement statement to verify]

| Confirmation | Technique | Question to Ask | Touchpoint |
|-------------|-----------|-----------------|------------|
| #1 | Direct restatement | "[Can you walk me through what you're planning to do from here?]" | End of next meeting |
| #2 | Implementation framing | "[How are you planning to handle X?]" | Follow-up email |
| #3 | Obstacle surfacing | "[What obstacles do you see on your end?]" | Kick-off call |

---

## Verdict and Action Plan

**Overall commitment quality:** Genuine / Uncertain / Likely Counterfeit

**Recommended next step:**
- [ ] Proceed — commitment signals are strong across all channels
- [ ] Verify — run Rule of Three sequence before investing further
- [ ] Rebuild — route to empathic-summary-planner to rebuild rapport before re-approaching commitment
- [ ] Surface stakeholders — confirm who else must approve before treating this as closed

**Notes:**
[Any additional context or observations]
```

---

## Key Principles

**Three types of yes require three different responses.** Treating a Counterfeit or Confirmation yes as a Commitment is the most common reason follow-through fails. Counterfeit yes needs rebuilding — find the real objection underneath the escape. Confirmation yes needs extension — the counterpart understood; now you need to move them from acknowledgment to action. Only Commitment yes allows you to proceed.

**WHY:** Most "commitment failures" are actually classification errors. A salesperson who loses a "closed" deal was usually working with a Counterfeit yes without knowing it. Misclassification causes the wrong intervention: you reinvest in a relationship that needs a different kind of attention, or you disengage from a counterpart who was genuinely committed but needed operational support to execute.

**Verbal deception indicators are signals of uncertainty, not lies.** When a counterpart's language inflates in word count, avoids first-person pronouns, or adds qualifiers at the commitment moment, they are not necessarily deceiving you — they may be uncertain themselves. The signals flag that the commitment is not fully formed, whether the reason is social pressure compliance, unresolved internal objections, or genuine inability to commit on behalf of others.

**WHY:** Treating deception signals as moral failures produces the wrong response — confrontation or withdrawal. Treating them as uncertainty signals produces the right response — Rule of Three verification that gives the counterpart a chance to surface the real constraint or solidify their commitment. The goal is not to catch them lying; it is to understand what is actually true.

**The channel with the least conscious control carries the most signal.** Words are chosen deliberately. Tone is semi-conscious. Body language is largely automatic. When these channels conflict, the channel the counterpart controls least — body language, then tone — is usually closer to their actual internal state. This asymmetry means that a flat, rushed voice delivering an enthusiastic "absolutely" is telling you more with the tone than with the word.

**WHY:** Under social pressure to agree, people default to positive words because that is the path of least resistance. But the emotional state underneath — discomfort, uncertainty, lack of conviction — surfaces in channels they are not consciously managing. The 7-38-55 framework is not a precise formula; it is a reminder to weight the channels that are harder to fake.

**"You're right" ends conversations; "that's right" advances them.** A counterpart who says "you're right" is closing down a thread that makes them uncomfortable. A counterpart who says "that's right" in response to your summary of their position is opening up — they feel understood, and that feeling creates movement. The difference tells you whether you've been pushing your position (producing escape responses) or drawing out theirs (producing genuine alignment).

**WHY:** Negotiation is lost at the point of pushing, not at the point of asking. When you make your case and the counterpart says "you're right" — you have pushed them into a corner where agreement costs them nothing and signals nothing. When you summarize their position accurately and they say "that's right" — they have moved toward you voluntarily, which is the only movement that sticks.

**The Rule of Three is too cognitively expensive to fake three times.** A Counterfeit yes can survive one confirmation request. It rarely survives three differently-framed requests across different touchpoints. The effort required to maintain the same false commitment under restatement, implementation questioning, and obstacle surfacing exceeds the social benefit of avoiding the conversation — so the real position surfaces.

**WHY:** This is why spacing the three confirmations across touchpoints (rather than asking them in sequence in one conversation) produces better information. In a single conversation, a counterpart can maintain a false commitment through social pressure. Across multiple touchpoints — when they have had time to think — the gap between what they said and what they're actually able to deliver becomes harder to bridge.

---

## Examples

### Example 1: Sales Close — Distinguishing Counterfeit from Commitment

**Scenario:** An account executive has been working a $200K software deal for four months. At the end of the final demo, the VP of Finance says: "This looks great. I think we can make this work. I don't see why we wouldn't move forward." The executive wants to know whether to treat this as a closed deal.

**Trigger:** "They said yes but I want to make sure before I start onboarding."

**Process:**
- Step 1: Classify — "I think we can make this work" is Confirmation at best. "I don't see why we wouldn't" is a double negative hedge, not a positive commitment. No specific action stated. No ownership pronoun ("I will"). Classify as Confirmation/Unverified.
- Step 2: Pinocchio check — "I don't see why we wouldn't" is over-complex for what a simple yes would be. No first-person commitment pronoun. Word count above what a genuine commitment requires. Two soft flags.
- Step 3: Channel check — the executive noted the VP's energy was lower at the end of the meeting than during the demo. Channel mismatch between positive words and reduced energy.
- Step 4: Rule of Three — Confirmation 1: "To make sure I have this right — can you walk me through what the path to signing looks like from here?" Confirmation 2: "How does your procurement process handle something at this contract size?" Confirmation 3: "What could slow this down on your end?"
- Step 5: Stakeholder check — "we" usage flagged. Question: "When you say 'we' — who else will be involved in the final sign-off?"

**Output:** `commitment-assessment.md` classifies the agreement as Unverified, flags two deception signals and a channel mismatch, generates the Rule of Three sequence and a stakeholder confirmation question. The follow-up reveals that legal approval is required — a two-week process the executive can now plan around rather than be surprised by.

---

### Example 2: Vendor Commitment — Detecting Scope Creep Risk Before It Happens

**Scenario:** A project manager has just finished a scope definition meeting with a new vendor. The vendor's lead said: "Absolutely, we can handle all of that. Our team does this kind of thing all the time. I'll make sure the team is fully aligned before we kick off." The PM wants to verify before approving the contract.

**Trigger:** "How do I know they can actually deliver what they committed to?"

**Process:**
- Step 1: Classify — "Absolutely, we can handle all of that" has positive energy but no specifics. "I'll make sure the team is fully aligned" is a process commitment (aligning the team), not a delivery commitment. Classify Agreement 1 as Confirmation, Agreement 2 as Commitment (to an internal action), flag for verification.
- Step 2: Pinocchio check — "Our team does this kind of thing all the time" is unsolicited justification at the commitment moment — word count inflation signal. "I'll make sure the team is fully aligned" uses first-person ownership — clean signal. Mixed result.
- Step 3: Channel check — PM noted the vendor lead spoke faster after the scope list was read. Pace increase = possible stress signal. Mild channel flag.
- Step 4: Rule of Three for Agreement 1 — Confirmation 1: "Can you describe how your team would approach the [most complex deliverable] specifically?" Confirmation 2: "How have you handled situations like this in previous projects?" Confirmation 3: "What would make delivery on this harder than expected?"
- Step 5: No plural pronouns at commitment. Stakeholder concern low.

**Output:** `commitment-assessment.md` flags word count inflation and mild pace mismatch, requests implementation framing in kick-off call. The implementation question reveals the vendor has not done one component of the scope before — surfacing before contract signing.

---

### Example 3: Internal Alignment — Verifying "You're Right" from a Reluctant Stakeholder

**Scenario:** A product manager needs sign-off from the VP of Engineering before launching a feature. After presenting the plan, the VP said: "You're right, we can't keep delaying this. I'll support it." The PM is uncertain whether this means the VP will actively support the launch or just stop blocking it.

**Trigger:** "I need to know if she's actually on board or just agreeing to end the conversation."

**Process:**
- Step 1: Classify — "You're right" is the diagnostic red flag. Per the "you're right" rule: this is a dismissal response, not a Commitment yes. "I'll support it" uses first-person and specifies action — classify that component as Commitment/Unverified.
- Step 2: Pinocchio check — "You're right, we can't keep delaying this" has a complaint embedded (the delay frustration) that was not addressed — a sign the underlying concern is unresolved. The "I'll support it" is short and direct — clean signal.
- Step 3: Channel check — the PM noted the VP did not make eye contact when saying "you're right." Maintained eye contact during "I'll support it." Channel mismatch on first statement, alignment on second.
- Step 4: The "you're right" component is a dismissal — route to empathic summary first. The "I'll support it" component is worth verifying. Rule of Three — Confirmation 1: "What specifically would your support look like during the launch period?" Confirmation 2: "How would you want to handle it if the launch surfaces issues?" Confirmation 3: "What concerns about the plan would you want us to address before we go?"
- Step 5: No stakeholder flags.

**Output:** `commitment-assessment.md` identifies the "you're right" as dismissal and separates it from the "I'll support it" commitment. Recommends a 10-minute empathic summary conversation to resolve the underlying delay frustration before the Rule of Three verification. The follow-up reveals the VP's real concern: resource allocation during the launch window — which the PM can now address directly.

---

## References

| File | Contents |
|------|----------|
| `references/yes-type-guide.md` | Diagnostic signal checklist for all three yes types; common statement patterns with classifications; edge cases and ambiguous examples; escalation criteria |
| `references/deception-signal-reference.md` | Full Pinocchio Effect signal library with examples; 7-38-55 channel weight rationale and application; baseline deviation detection method; pronoun analysis guide; "you're right" vs "that's right" full case breakdown |
| `references/rule-of-three-library.md` | 15+ ready-to-use verification questions across all three confirmation types; sequencing guide for different contexts (sales, internal, vendor, partnership); timing recommendations for distributed confirmation |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Never Split the Difference: Negotiating as if Your Life Depended on It by Chris Voss.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
