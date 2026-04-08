---
name: influence-defense-analyzer
description: |
  Detect and counter manipulation attempts using Cialdini's 6 influence principles. Use when you feel pressured to comply with a request, sense a sales tactic at work, want to audit a document for manipulation, or ask "is this legitimate or am I being played?" Also use for: analyzing a sales pitch, marketing email, negotiation transcript, or contract for exploitative influence tactics; identifying which compliance trigger is being activated and whether it's real or manufactured; deciding whether to comply with a request you feel uneasy about; auditing your own persuasive content for ethical compliance; training yourself to recognize manipulation in consumer, negotiation, or organizational contexts. Applies all 6 per-principle defense protocols (reciprocity, commitment/consistency, social proof, liking, authority, scarcity) plus the epilogue meta-framework to classify practitioners as fair (real evidence) or exploitative (manufactured triggers) and prescribe a principle-specific response strategy. Works on document sets — sales pitches, marketing claims, negotiation transcripts, contracts, advertising — as well as live compliance scenarios described in text.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/influence-psychology-of-persuasion/skills/influence-defense-analyzer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - influence-principle-selector
source-books:
  - id: influence-psychology-of-persuasion
    title: "Influence: The Psychology of Persuasion"
    authors: ["Robert B. Cialdini"]
    chapters: [2, 3, 4, 5, 6, 7, "Epilogue"]
tags: [persuasion, defense, protect, manipulation, detect, recognize, resist, compliance, persuasion-tactics, sales-pressure, say-no, ethical-boundary, exploitation, reciprocity, commitment, social-proof, liking, authority, scarcity, cialdini, consumer-protection, negotiation-defense]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "The compliance situation to analyze — a sales pitch, marketing email, negotiation transcript, advertisement, contract excerpt, or a plain-text description of the situation you are in"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Works with pasted text or document files."
discovery:
  goal: "Identify which influence principle(s) are active in a compliance situation, classify them as legitimate or exploitative, apply the principle-specific defense protocol, and produce an actionable response strategy"
  tasks:
    - "Detect which of the 6 principles are being activated in the situation"
    - "Classify each activation as legitimate (real evidence) or exploitative (manufactured/falsified triggers)"
    - "Apply the per-principle defense protocol with its specific diagnostic questions and response steps"
    - "Produce a response strategy calibrated to legitimate vs exploitative classification"
    - "Identify vulnerability conditions (rushed, stressed, uncertain, distracted, fatigued) that heighten risk"
  audience:
    roles: ["consumer", "negotiator", "employee", "citizen", "procurement-officer", "investor", "donor", "anyone in a compliance situation"]
    experience: "any — no psychology background required"
  triggers:
    - "User feels pressured to comply and wants to understand whether the pressure is legitimate"
    - "User is reviewing a sales pitch, marketing message, or contract and suspects manipulation"
    - "User wants to audit a document for exploitative influence tactics"
    - "User has already complied and wants to understand what happened and why"
    - "User wants to train themselves to recognize manipulation patterns across all 6 principles"
  not_for:
    - "Applying influence principles to persuade others — use influence-principle-selector or the dedicated principle skills"
    - "Auditing your own content for ethical compliance — use persuasion-content-auditor"
    - "Deep understanding of how a single principle works offensively — use the dedicated principle skill"
---

# Influence Defense Analyzer

## When to Use

You are in a compliance situation — someone is trying to get you to say yes — and you want to know whether the pressure is legitimate or exploitative, and how to respond.

This skill covers all 6 compliance principles from the defensive side. It is the counterpart to `influence-principle-selector`, which helps you apply influence; this skill helps you resist it.

**Do not use this skill if:** You want to apply influence tactics yourself. Use `influence-principle-selector` or the dedicated principle skills for that.

---

## Context and Input Gathering

Before running the defense analysis, collect:

### Required
- **The situation:** What is being asked of you? What happened before the request?
- **The document or pitch:** If analyzing written material, provide the text.

### Important
- **Timeline and pressure cues:** Is there a deadline? A countdown? A stated limited supply?
- **The relationship:** Do you know this person or organization? How did the relationship start?
- **Your current state:** Are you rushed, stressed, uncertain, or fatigued? (These conditions increase vulnerability — see Step 1.)

### Optional
- **Prior interactions:** Was there an initial gift, favor, or concession before the request?
- **What you already committed to:** Any prior statements, signatures, or small actions taken?

If the situation is not yet described, ask for it before proceeding.

---

## Process

### Step 1: Assess Vulnerability Conditions

**Action:** Check whether any of these conditions are present: rushed, stressed, uncertain, distracted, fatigued, facing a deadline.

**WHY:** These are the precise conditions under which cognitive processing collapses to single-trigger shortcut responses. Compliance practitioners — both legitimate and exploitative — deploy their tactics knowing that these conditions make their triggers maximally effective. A rushed buyer, a stressed negotiator, a fatigued employee: all are more likely to comply automatically. Recognizing that you are in a vulnerable state is the first defensive move — it activates deliberate override of the automatic response.

**Output:** Flag any present vulnerability conditions. If multiple are present, note that the risk of automatic compliance is elevated and that extra deliberation is warranted.

---

### Step 2: Identify Which Principles Are Active

**Action:** Scan the situation for trigger features associated with each of the 6 principles. For each principle detected, note the specific trigger element present.

**WHY:** Each principle activates via a single trigger feature. Identifying the trigger — not just naming the principle — is what enables a targeted defense. "They are using scarcity" is less actionable than "They introduced a deadline after I showed interest, which activates scarcity; I need to check whether the deadline is real." Multiple principles may be active simultaneously, which amplifies compliance pressure; stacked principles require recognizing each one separately.

**Principle trigger checklist:**

| Principle | What to look for in the situation |
|-----------|-----------------------------------|
| Reciprocity | An initial gift, favor, concession, or "free" offer before the main request |
| Commitment/Consistency | A prior statement, action, or small agreement being referenced to justify the current request |
| Social Proof | Claims about what others are doing, buying, or believing — testimonials, numbers, crowd behavior |
| Liking | Unusual warmth, flattery, shared interests, or friendliness from the requester |
| Authority | Credentials, titles, uniforms, trappings of expertise, or claims of superior knowledge |
| Scarcity | Deadlines, limited supply, competition for the item, or phrases like "act now" or "only X left" |

Note every principle trigger present. Do not stop at the first one found.

---

### Step 3: Classify Each Trigger — Legitimate or Exploitative

**Action:** For each active principle, apply the classification test: Is the trigger evidence real or manufactured?

**WHY:** This is the single most important step. The 6 principles work because they are reliable signals — social proof, authority, scarcity, and the rest normally do indicate a correct decision. Fair practitioners present real evidence (genuine scarcity, authentic testimonials, actual credentials) and help you make a correct decision efficiently. Exploitative practitioners manufacture fake triggers (fake deadlines, paid testimonials presented as organic, counterfeit authority symbols) to fire the compliance response when the evidence does not support it. Distinguishing these two is the core of defense: cooperation is appropriate for fair practitioners; counter-aggression is warranted against exploitative ones.

**Classification rule:**
- Trigger evidence is real and verifiable → **Fair practitioner.** Principle is being used legitimately.
- Trigger evidence is manufactured, falsified, or cannot be verified → **Exploitative practitioner.** Treat the trigger as void.

---

### Step 4: Apply the Per-Principle Defense Protocol

**Action:** For each identified principle, apply the specific defense protocol. See `references/defense-protocols.md` for the complete per-principle quick-reference.

**WHY:** Each principle exploits a different automatic response, and each requires a different defense move. A generic "be skeptical" instruction does not work because each principle operates through a distinct mechanism. The stomach-signal approach that defeats commitment/consistency does nothing against manufactured social proof. The per-principle protocols give you the exact diagnostic question and response step for each trigger type.

#### Reciprocity Defense

The trigger is a prior gift, favor, or concession. The mechanism is obligation — a deep social rule that says favors are to be met with favors.

**Detection question:** Was this initial offer genuinely given, or was it a sales device designed to create obligation?

**Response steps:**
1. Accept the initial offer for what it fundamentally is — not for what it was presented as.
2. If you determine it was a sales device (the "favor" was the opener of a pitch, not a genuine gift), mentally redefine it as a compliance tactic. A favor rightly follows a favor — not a sales strategy.
3. Once redefined, the reciprocity obligation is void. You may decline the request freely without the pull of obligation.

**Key principle:** Redefining the initial "gift" as a sales device is not cynicism — it is accurate perception. The reciprocity rule creates obligation between people who give genuine favors to each other. It does not require that tricks be met with favors.

For deeper understanding of how reciprocity is applied offensively, see `reciprocity-strategy-designer`.

---

#### Commitment and Consistency Defense

The trigger is a prior statement, action, or agreement being used to pressure continued compliance.

**Detection signals — register both:**
1. **Stomach signal:** A tight feeling in the gut when you realize you are being pushed to comply with something you do not actually want to do. This is the clearest early warning that the consistency mechanism is being exploited.
2. **Heart signal:** A sense, when you examine your true feelings, that the reasons you have been giving yourself for staying committed do not match your actual preferences.

**Diagnostic question:** "Knowing what I know now, if I could go back in time, would I make the same commitment?"

**Response steps:**
1. Listen to the stomach signal. It registers when automatic consistency is pulling you toward an unwanted action. Do not dismiss it.
2. If uncertain, ask the diagnostic question and attend to the first feeling that surfaces — before rationalization engages.
3. If the answer is no, you have detected foolish consistency. Wise consistency (aligned with your true values and current knowledge) is worth maintaining. Foolish consistency (continuing a course because you started it, not because it is correct) is worth breaking.
4. Name what is happening. Stating explicitly that you recognize the commitment-as-trap frequently disrupts the exploit.

**Key principle:** Distinguishing wise consistency from foolish consistency is the entire defense. Automatic, unthinking consistency is the vulnerability; deliberate, knowledge-updated reconsideration is the protection.

For deeper understanding of how commitment is applied offensively, see `commitment-escalation-architect`.

---

#### Social Proof Defense

The trigger is evidence of what others are doing or believing, presented to suggest you should do the same.

**Two failure modes — identify which is present:**
1. **Falsified evidence:** Social proof that was manufactured by exploiters — canned laughter, paid actors posing as ordinary customers, staged crowds, fake testimonials. The evidence was created to create the impression of popularity.
2. **Incorrect data:** Genuine social evidence that is nonetheless misleading — pluralistic ignorance, where everyone privately doubts but publicly complies, creating a false picture of consensus. The evidence is real but inaccurate.

**Detection question:** Is this social evidence genuinely emergent (arising organically from independent behavior) or manufactured (staged, paid, or the result of a collective false signal)?

**Response steps:**
1. Check whether the social evidence source can be verified independently. Can you identify who these people are? Did they choose to endorse independently, or were they paid or prompted?
2. For online reviews, testimonials, and crowd behavior: look for the structural hallmarks of manufactured evidence — uniform tone, absence of specific detail, timing patterns, incentivized submission.
3. If evidence appears falsified: treat the trigger as void and proceed as if the social proof data point did not exist.
4. If evidence appears genuine but potentially driven by pluralistic ignorance: seek independent information sources to verify that the consensus reflects actual experience, not collective uncertainty.

For deeper understanding of how social proof is applied offensively, see `social-proof-optimizer`.

---

#### Liking Defense

The trigger is the practitioner's personal appeal — attractiveness, flattery, similarity, familiarity, association with pleasant things — creating a sense of warmth toward them.

**Universal detection criterion:**
"Have I come to like this person more than I would have expected given the circumstances and the amount of time we have spent together?"

**Response steps:**
1. Do not attempt to prevent liking from happening. Liking operates unconsciously through attractiveness, familiarity, and association, and cannot be reliably blocked in advance.
2. Instead, redirect vigilance to the effect, not the cause. The signal to act on is the feeling of unexpected or disproportionate liking — not the specific tactic that produced it.
3. When you detect unexpected liking: consciously separate the person from the proposal. The question is not whether you like the practitioner but whether the deal itself is good.
4. Do not actively dislike the practitioner as a counter-move. Some people are genuinely likable, and an unfair negative reaction is both unjust and harmful to you. Simply bracket the liking and evaluate the offer on its merits.

**Key principle:** The defense is not "stop liking people." It is "do not let liking substitute for evaluating the deal." Maintain the distinction between the requester and the request.

For deeper understanding of how liking is applied offensively, see `liking-factor-engineer`.

---

#### Authority Defense

The trigger is the appearance of expertise or legitimate authority — credentials, titles, uniforms, specialized knowledge — creating automatic deference.

**Two-question sequence — apply in order:**

**Question 1:** "Is this authority truly an expert?" Check credentials against the domain at hand. A medical doctor recommending a financial product is an authority in medicine, not finance. A celebrity endorsing a supplement has no relevant expertise. Distinguish between the label "authority" and actual domain-relevant knowledge.

**Question 2:** "How truthful can we expect this authority to be?" Even genuine experts may not present information honestly if they have conflicts of interest. Ask: What does this authority gain from my compliance? Does their incentive align with giving me accurate information, or with getting me to say yes?

**Red flag — strategic self-deprecation:** When an authority figure mentions a minor flaw or limitation before making their main claim, they may be using a credibility-building tactic (establishing honesty on a small point to be believed on a large one). Recognize this pattern: the conceded flaw is always minor and easily overcome; the claim it sets up is the one they want you to accept.

**Response steps:**
1. Identify the claimed authority and verify domain relevance (Question 1).
2. Check for conflicts of interest (Question 2).
3. If both tests pass, the authority input is trustworthy and may be weighted accordingly.
4. If either test fails, treat the authority claim as an unverified signal and seek independent verification before complying.

For deeper understanding of how authority is applied offensively, see `authority-signal-designer`.

---

#### Scarcity Defense

The trigger is limitation — a deadline, limited quantity, or competition for the item — creating urgency and desire.

**Two-stage response — execute in sequence:**

**Stage 1 — Recognize arousal as a warning signal, not a decision driver.**
When you feel a rising sense of urgency, the desire to act before missing out, or competitive agitation when others want the same thing: recognize that feeling as a warning signal, not a guide to action. The physiological arousal produced by scarcity suppresses deliberate analysis. Stop before acting.

**Stage 2 — Ask the possession vs. utility question.**
Once you have paused: "Do I want this item for its utility (to use it, eat it, drive it, deploy it) or for its possession value (to own something rare)?"
- If utility: remember that scarce items do not perform better because they are scarce. A rare product delivers the same function as an abundant one. The scarcity adds no value to what you will actually experience from it.
- If possession value: scarcity is a legitimate signal. The item's rarity is genuinely part of what you value about it.

**Key principle:** The cookies in the scarcity experiment were rated as more desirable — but not as better-tasting — when scarce. Scarcity affects perceived value, not actual utility. This distinction, held clearly in mind during the arousal state, dissolves most of scarcity's power over non-collectors.

For deeper understanding of how scarcity is applied offensively, see `scarcity-framing-strategist`.

---

### Step 5: Classify the Practitioner and Formulate the Response

**Action:** Based on the classification in Step 3, determine the appropriate response category and formulate the specific response.

**WHY:** The appropriate response to a fair practitioner differs fundamentally from the response to an exploitative one. Cooperating with fair practitioners is not weakness — they are offering real value that a shortcut correctly identifies. Counter-aggression against exploitative practitioners is not hostility — it is an appropriate response to deliberate fraud that corrupts the cognitive shortcuts everyone depends on.

**Response framework:**

| Classification | Response | Rationale |
|----------------|----------|-----------|
| Fair practitioner (real triggers) | Cooperate. Use the shortcut as intended. | Real scarcity, genuine social proof, actual authority — these are valuable signals. Complying is efficient and correct. |
| Exploitative practitioner (manufactured triggers) | Reject the trigger. Name the tactic. Withdraw compliance. | Manufactured triggers corrupt the shortcut. Counter-aggression is warranted — boycott, challenge, refusal, or public naming of the tactic. |
| Uncertain (cannot verify) | Pause. Seek independent verification before deciding. | Do not comply under time pressure when trigger legitimacy cannot be verified. Request time to check. |

---

## Inputs / Outputs

### Inputs
- Compliance situation description or document (required)
- Description of what was asked and what preceded the request (required)
- Any prior interactions, gifts, or commitments (optional)

### Outputs
- Vulnerability condition flags
- Active principle identification with trigger elements named
- Fair vs. exploitative classification per principle
- Per-principle defense protocol application
- Response strategy (cooperate, counter, or pause-and-verify)

---

## Key Principles

**The real opponent is the rule, not the requester.** When someone uses a compliance principle against you, they are deploying a social rule — reciprocity, consistency, authority — that has genuine force. The person is a jujitsu warrior who has aligned themselves with that force. Defusing the exploit means defusing the rule's energy, not attacking the person.

**Fair practitioners are allies.** Compliance professionals who present real trigger evidence are helping you use a reliable shortcut correctly. They are not the target of counter-aggression. The appropriate response is cooperation. Counter-aggression is warranted only when triggers are manufactured or falsified.

**Vulnerability conditions multiply risk.** Being rushed, stressed, uncertain, distracted, or fatigued suppresses the deliberate processing that defenses depend on. These states are exactly when compliance is most automatic and when manipulators most prefer to push. Recognizing your own vulnerability state is the first defense.

**Detect the trigger, not just the principle.** "They used scarcity" is insufficient. The operative question is: what is the specific trigger element, and is it real? Finding the trigger element directs you to the right defense protocol.

**Liking works unconsciously; defend at the effect, not the cause.** Unlike authority symbols or false testimonials — which can be checked — liking often operates below awareness through physical attractiveness and association. You cannot reliably block it. Defend by noticing the effect: unexpected, disproportionate warmth toward the requester.

**The commitment defense is internal.** Stomach signal (gut discomfort when trapped) and heart signal (recognizing stated reasons don't match true feelings) are the only reliable detectors of commitment exploitation. External analysis alone is insufficient. The diagnostic question "Would I make this same commitment knowing what I know now?" must be answered at the feeling level, before rationalization runs.

---

## Examples

### Example 1: Sales Pitch with Multiple Active Principles

**Scenario:** A software vendor sends a free consultation report analyzing your company's "inefficiencies" (unsolicited), followed by a pitch deck. The pitch includes logos of 40 named customers, a quote from a Gartner analyst, and an "end-of-quarter pricing" that expires Friday.

**Trigger:** "Should I take this deal? The analyst quote seems credible and a lot of companies I recognize are using them."

**Process:**
- Step 1: Deadline (Friday) creates time pressure — vulnerability condition flagged.
- Step 2: Reciprocity (free consultation = initial gift), Social Proof (40 customer logos + testimonials), Authority (Gartner analyst), Scarcity (end-of-quarter pricing expiry). Four principles active simultaneously.
- Step 3: Reciprocity — was the consultation genuinely valuable, or designed to create obligation? Check: did they tailor it to your specific situation or was it templated? If templated, redefine as a sales device, not a gift. Social proof — are the 40 logos verifiable reference customers or logos placed without permission? Can you call two of them? Authority — is the Gartner analyst quote from a paid research relationship or an independent analysis? Scarcity — is end-of-quarter pricing real (sales team quota pressure) or a manufactured false deadline?
- Step 4: Apply per-principle protocols for each.
- Step 5: If consultation is genuine AND logos are verifiable AND analyst quote is independent AND pricing expiry is real → fair practitioner; engage on merits. If any trigger is manufactured → classify as exploitative; request extended timeline and verify independently before committing.

**Output:**
```
Active principles: Reciprocity (free report), Social Proof (logos), Authority (analyst), Scarcity (deadline)
Vulnerability: Friday deadline = time pressure — elevated risk of automatic compliance
Reciprocity: Pending classification — verify if report is templated or tailored
Social Proof: Pending — call 2 reference customers before Friday
Authority: Pending — verify Gartner relationship is independent, not paid
Scarcity: Pending — ask directly whether pricing can be extended; test the deadline's reality
Response: Pause-and-verify. Request 2-week extension. Any refusal to extend signals manufactured scarcity.
```

---

### Example 2: Commitment Trap in a Negotiation

**Scenario:** You are in a procurement negotiation. Three months ago you signed a letter of intent. The vendor is now presenting terms 30% above the original estimate, citing "scope changes." You feel obligated to continue because of the time invested and the letter you signed.

**Trigger:** "We've put so much into this already. And we did sign the letter of intent. I feel like we have to see this through."

**Process:**
- Step 1: Sunk cost framing and prior commitment — stomach signal check warranted.
- Step 2: Commitment/consistency is the primary active principle. The letter of intent + 3 months of time = effortful prior commitment being used as consistency anchor.
- Step 3: Is the commitment legitimate? The letter of intent was real — but the terms presented now differ substantially from those anticipated when it was signed.
- Step 4: Apply commitment defense. Diagnostic question: "Knowing what I know now about the final pricing, would I have signed the letter of intent on these terms?" Register the first honest answer. If no, this is foolish consistency — the commitment to the original terms does not extend to accepting 30% scope creep without renegotiation.
- Step 5: Fair practitioner if scope genuinely changed and documentation supports it. Exploitative if scope was understated deliberately to lock in the commitment first.

**Output:**
```
Active principle: Commitment/Consistency
Stomach signal: Yes — discomfort about the gap between original and current terms
Diagnostic question answer: No — would not have signed at current terms
Classification: Pending — request scope change documentation
Defense: The commitment was to the original terms, not to any terms the vendor chooses to present after the letter is signed. Renegotiate or withdraw.
```

---

### Example 3: Consumer Scarcity + Social Proof Stack

**Scenario:** You are shopping for a hotel for a family trip. The booking site shows "Only 2 rooms left at this price!" and "17 people are looking at this right now."

**Trigger:** "I need to book now before it's gone."

**Process:**
- Step 1: Rushing to book = time pressure induced by the display — vulnerability condition present.
- Step 2: Scarcity (2 rooms, price expiry implied) + Social Proof (17 people looking) — two principles stacked.
- Step 3: Both are frequently manufactured on booking platforms. "17 people looking" figures are often fabricated or algorithmically inflated. "2 rooms left" may reflect inventory management, not genuine scarcity.
- Step 4: Scarcity defense — Stage 1: recognize arousal (urgency to book) as warning signal, pause. Stage 2: utility question — do I want this hotel to stay in it, or to "win" it? Answer: utility. Scarce hotel rooms provide the same night's sleep as abundant ones. Social proof defense — verify: open the hotel's own site and check availability; search elsewhere. If availability is identical, the scarcity was manufactured.
- Step 5: Exploitative if room availability shows the same rooms on direct booking. Counter: book directly or check an alternative platform. Do not reward manufactured urgency with a booking.

**Output:**
```
Active principles: Scarcity ("2 rooms left"), Social Proof ("17 looking")
Vulnerability: Urgency to book — elevated risk
Classification: Likely exploitative — verify via direct hotel site
Defense: Check direct. If available there, the platform manufactured urgency. Book direct or on a platform without the pressure display.
```

---

## References

| File | Contents |
|------|----------|
| `references/defense-protocols.md` | Per-principle defense quick-reference: detection criteria, diagnostic questions, response steps, and classification tests for all 6 principles |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Influence: The Psychology of Persuasion by Robert B. Cialdini.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-influence-principle-selector`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
