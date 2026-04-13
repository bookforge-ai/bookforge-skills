---
name: commitment-and-advance-planner
description: |
  Plan the specific commitment to target on a B2B sales call, and script how to obtain it without using closing pressure. Use this skill when someone asks "how do I close this deal", "what should I ask for at the end of the call?", "should I push for the close on Tuesday?", "how do I get this prospect to commit?", "what's a realistic next step to aim for?", "they keep saying they're interested but won't commit", "my manager wants me to close harder but I don't think that's working", "I need to plan my commitment strategy before tomorrow's call", "how do I avoid getting a non-answer at the end of the meeting?", "what's the difference between a real commitment and a polite brush-off?", "I keep getting Continuations instead of Advances", "how do I know what level of commitment to ask for?", or "what do I do when the prospect says 'let's stay in touch'?" Also invoke when someone is prepping for any major B2B sales call and wants a written plan for how to end it — even if they don't use the word "close" or "commitment." This skill produces a pre-call commitment plan with a primary Advance target, a fallback Advance, a Four Successful Actions script, and a Continuation guard. It explicitly replaces closing-technique training with Advance-targeting, grounded in empirical research showing that pressure closing reduces success rates in large sales. After the call, run spin-selling:call-outcome-classifier to verify whether the planned Advance was actually obtained.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/commitment-and-advance-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on:
  - call-outcome-classifier
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [2]
tags: [sales, b2b-sales, enterprise-sales, commitment, advance, closing, call-planning, pre-call-prep, complex-sales, spin-selling, deal-progression, pipeline-management, anti-closing]
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "deal-brief.md — company, contact, deal size, current stage, what is known so far"
    - type: document
      description: "stakeholder-map.md (optional) — decision-makers, influencers, and their access levels"
    - type: document
      description: "call-notes-{date}.md (optional) — notes from the most recent prior call; shows what advances have already been obtained"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "document_set — reads deal context from the working directory; writes commitment-plan-{deal}-{date}.md"
discovery:
  goal: "Produce a pre-call commitment plan naming a specific primary Advance, a fallback Advance, and a scripted sequence to obtain commitment without pressure techniques — so the seller walks into the call knowing exactly what customer action they need and how to ask for it"
  tasks:
    - "Read deal-brief.md and prior call notes to understand deal stage, what has already been agreed, and what access is still needed"
    - "Determine what specific customer action would meaningfully move this deal forward (primary Advance)"
    - "Determine a smaller but still valid Advance to fall back to if the primary is not obtainable"
    - "Script the Four Successful Actions sequence for this specific call and deal"
    - "Embed a Continuation guard: phrases to watch for that signal the buyer is offering a Continuation disguised as a commitment"
    - "Write commitment-plan-{deal}-{date}.md as the pre-call planning artifact"
  audience:
    roles: ["account-executive", "enterprise-sales-rep", "solutions-consultant", "founder-led-seller"]
    experience: "intermediate — has run B2B sales calls; may have been trained on classic closing techniques; this skill replaces that training with Advance-targeting"
  triggers:
    - "User is preparing for a key B2B sales call and wants to plan the commitment strategy"
    - "User has been getting Continuations and wants a plan to obtain real Advances instead"
    - "User is being pressured by their manager to close harder and wants an evidence-based alternative"
    - "User wants to know what specific action to ask for on the next call"
    - "User wants to understand the difference between an Advance and a Continuation before planning"
  not_for:
    - "Generating SPIN discovery questions for the Investigating stage — use spin-selling:spin-discovery-question-planner"
    - "Drafting Benefit statements for the summary step — use spin-selling:benefit-statement-drafter"
    - "Closing-attitude self-introspection — use spin-selling:closing-attitude-self-assessment"
    - "Classifying whether last call's outcome was an Advance or Continuation — use spin-selling:call-outcome-classifier"
    - "Multi-call deal forecasting or probability modeling"
  quality: placeholder
---

# Commitment and Advance Planner

## When to Use

You are preparing for a significant B2B sales call and need to know:
1. **What specific customer action should I target at the end of this call?**
2. **How do I ask for it without triggering defensive pressure reactions?**

This skill is for pre-call planning. The human runs the actual call; the agent helps plan the commitment strategy before it.

**Who this skill is for:** B2B account executives, solutions consultants, or founder-led sellers — particularly those who have been trained on traditional closing techniques (assumptive close, alternative close, ABC/Always-Be-Closing) or who keep getting polite non-commitments ("we'll be in touch") at the end of calls.

**Prerequisite knowledge:** This skill assumes you understand the Advance vs Continuation distinction. If not, run `spin-selling:call-outcome-classifier` on your last call first — that skill will make the distinction concrete before you plan the next one.

**Outputs:** `commitment-plan-{deal}-{date}.md` — a written pre-call plan naming your primary Advance, fallback Advance, and a scripted Four Successful Actions sequence for this specific call.

---

## Context & Input Gathering

### Required
- **Deal stage:** Where is this deal in the cycle? What advances have already been obtained? What stakeholders have been accessed?
- **What specific action would move this deal forward?** If you don't know yet, this skill will help you work through it.

### Useful (read from working directory if available)
- **`deal-brief.md`** — account name, contact, deal size, current stage, timeline, known information
- **`stakeholder-map.md`** — who the decision-makers are, who hasn't been accessed yet, who the champion is
- **`call-notes-{date}.md`** — most recent prior call notes; what was the last Advance obtained?

### Defaults (used if not provided)
- If no call notes are available, ask the user to describe the deal stage in two sentences.
- If no stakeholder map is available, ask: "Who is in the room on Tuesday, and who isn't that should be?"

### Sufficiency threshold
A deal-brief or brief verbal deal summary is sufficient to begin. The more context available, the more specific the Advance targets will be.

---

## Process

### Step 1: Establish Deal Stage and What Has Already Been Committed

**Action:** Read `deal-brief.md` and the most recent `call-notes-{date}.md`. Identify:
- The specific Advance(s) already obtained (e.g., "they agreed to a technical review with their IT lead on the previous call")
- What stakeholders have been accessed and which have not
- What the stated or implied decision criteria are
- Any explicit needs the customer has expressed (these are used in Step 4's Benefit summary)

If no documents are available, ask the user to describe these points directly.

**WHY:** An Advance must move the sale forward from its current position — you cannot define "forward" without knowing where the deal currently stands. An Advance that was realistic two calls ago (e.g., "get a meeting with the department head") may already be achieved. Planning an Advance below the current stage results in a wasted call; planning one above achievable limits pushes the buyer past their readiness and produces pressure resistance.

**Output:** A brief written summary (3-5 lines) of current deal state and last Advance obtained.

---

### Step 2: Define the Primary Advance

**Action:** Define a primary Advance that meets both criteria for a valid Advance:
1. **The commitment advances the sale** — as a result of this customer action, the deal will move closer to a decision.
2. **The commitment is the highest realistic action the customer can give** — do not push beyond achievable limits, but do not settle for less than what is achievable.

A valid Advance is a specific, named customer action. Apply the **"name the action" test**: can you complete this sentence with a concrete noun phrase?

> *"By the end of this call, the customer will have agreed to ___."*

**Advance examples that pass the name-the-action test:**
- "…attend a 90-minute product demonstration at our offices with CFO present"
- "…arrange a technical evaluation session with their IT security lead by next Friday"
- "…submit an internal request to procurement to begin contract review"
- "…introduce us to the VP of Operations who is the final decision-maker"
- "…run a 30-day pilot of the integration module with two real accounts"

**Advance examples that fail the test (too vague):**
- "…consider moving forward" — no specific action
- "…stay interested" — no action at all
- "…follow up" — this is a seller action, not a customer action

**Large-sale gating check:** Is this a deal where the customer is a sophisticated buyer with an ongoing post-sale relationship? If yes, use the Advance framing. Pressure techniques are especially counterproductive in these contexts.

**WHY:** Rackham's research on major-account sales forces showed that fewer than 10% of calls result in an Order or No-sale. The dominant outcome is either an Advance or a Continuation — and the difference between pipeline health and pipeline stagnation is consistently whether each call ends in a named Advance or a polite non-commitment. Sellers who plan for vague objectives ("build a relationship," "keep the conversation going") are planning for Continuations. Writing the specific action into your pre-call plan forces the discipline before the call, not after.

**Output:** One sentence: "Primary Advance: [specific customer action]."

---

### Step 3: Define a Fallback Advance

**Action:** Define a fallback Advance — a smaller but still valid customer action — to use if the primary Advance cannot be obtained on this call. The fallback must also pass the name-the-action test.

Ask: if the primary Advance proves unachievable, what smaller but genuine customer commitment would still represent real forward progress?

**Example:** Primary = "CFO attends product demo on Tuesday." Fallback = "Customer agrees to send us the evaluation criteria document so we can tailor the demo agenda."

**WHY:** Without a fallback, sellers under pressure to "get a commitment" will often accept a Continuation disguised as an Advance rather than leave empty-handed. A buyer saying "let's reconnect next month" feels like progress; a pre-written fallback Advance gives you a specific alternative to counter-offer with: "I understand the timeline is tight — would it help if we started with a 30-minute technical overview for your IT lead this week instead?" The fallback prevents collapse into Continuation.

**Output:** One sentence: "Fallback Advance: [specific customer action]."

---

### Step 4: Script the Four Successful Actions Sequence

**Action:** For this specific call and deal, write out how you will apply Rackham's Four Successful Actions — the behaviors consistently observed in successful major-sale commitment situations. Write this as a scripted sequence you can refer to before and during the call.

**The Four Successful Actions:**

**Action 1 — Invest in the Investigating stage**
The single most reliable predictor of obtaining commitment is doing an outstanding job in the discovery (Investigating) stage. Customers who clearly perceive a need for what you offer will often close the sale themselves. If the discovery has been thorough, the commitment is easier to obtain.

For this call: note what Investigating is still needed. Do not rush through discovery to get to commitment. If the customer does not yet clearly perceive the need, commitment-seeking is premature.

*Script:* [Note what questions or discovery you still need to complete in this call before moving toward commitment.]

**Action 2 — Check that key concerns are covered**
Before moving to commitment, ask the buyer directly whether there are areas you haven't covered or questions they still have. Do not use closing techniques to surface concerns — that creates antagonism.

*Script:* "Before we go further, I want to make sure I've covered everything that's important to you. Are there areas you'd like to explore more, or questions I haven't addressed?"

Effective alternative phrasings:
- "Is there anything else I should be telling you about before we talk about next steps?"
- "What are the biggest open questions from your side right now?"

**Action 3 — Summarize Benefits**
In a major sale, the call has likely covered significant ground. Before proposing commitment, briefly pull together the Benefits that are most relevant to this buyer — specifically, capabilities that match Explicit Needs the customer has expressed (not Features or Advantages you want to present).

*Script:* "Let me summarize where we are. You mentioned that [Explicit Need 1] is a priority — and we've seen how [Capability A] addresses that directly. You also raised [Explicit Need 2], and [Capability B] handles that by [specific mechanism]. Based on what you've shared, there seem to be meaningful gains for you from [the change / the solution]."

Note: Do not present Features or Advantages as Benefits unless the customer has explicitly stated the underlying need. If you are unsure whether you have genuine Explicit Needs to summarize, note this as a gap and adjust the Investigating plan for Action 1.

**Action 4 — Propose a commitment**
Successful sellers in Rackham's research did not "ask" for commitment — they proposed a specific next step. This is an important distinction: "asking" invites the buyer to evaluate whether they want to commit; "proposing" describes a logical next step that flows from what has been established.

*Script:* "Based on everything we've discussed, the most logical next step seems to be [Primary Advance]. Does [specific date/format] work on your end?"

If the buyer hesitates or the primary Advance is not achievable:
- Do not escalate to pressure techniques.
- Offer the fallback Advance directly: "Alternatively, we could start with [Fallback Advance] — that would give us [specific value]."
- If neither is possible: ask what the buyer's constraints are, rather than applying pressure. Understanding the constraint is more valuable than forcing a premature commitment.

**WHY:** The Four Successful Actions replace closing techniques with behaviors that are empirically associated with commitment success in large sales. The sequence works because: Action 1 ensures the buyer perceives a genuine need (making commitment natural, not forced); Action 2 clears residual doubts before they become antagonistic objections; Action 3 re-grounds the decision in the buyer's own stated needs; Action 4 proposes rather than pressures. The sequence removes the conditions that make closing techniques feel necessary — if the buyer clearly perceives a need and has no unresolved concerns, they will often agree to a next step without pressure.

**Output:** The Four Successful Actions script, tailored to this call (fill in the bracketed sections with deal-specific content).

---

### Step 5: Embed the Continuation Guard

**Action:** Before writing the final plan document, add a Continuation guard — a list of buyer phrases and patterns that signal a Continuation is being offered, and the redirect response.

**Classic Continuation phrases** (Rackham's research verbatim and near-variants):
- "Thank you for coming. Why don't you visit us again the next time you're in the area."
- "Fantastic presentation, we're very impressed. Let's meet again some time."
- "We liked what we saw and we'll be in touch if we need to take things further."
- "We'll definitely keep you in mind."
- "Interesting — we'll have to discuss it internally and come back to you."
- "Let's reconnect in Q3." (with no confirmed date, agenda, or attendees)
- "Send me the proposal and we'll take a look."

**What these phrases have in common:** The buyer is expressing a positive feeling, not committing to an action. The next step is conditional, vague, or seller-initiated only. No specific customer action is named.

**How to redirect when you hear a Continuation phrase:**
1. Do not accept the Continuation as success. Recognize it for what it is.
2. Do not apply closing pressure — that escalates resistance.
3. Offer a specific, smaller Advance: "I'd love to set that up — what if we blocked a specific 30 minutes next week? I can work around your schedule."
4. If the buyer resists even that: ask a diagnostic question — "Is there something you need to see or understand before that next step makes sense?" This surfaces concerns that can be addressed rather than forcing a non-committal closure.

After the call, run `spin-selling:call-outcome-classifier` to verify whether the outcome was a genuine Advance or a Continuation. This closes the learning loop and prevents the most common failure mode: leaving a Continuation call feeling like it went well.

**WHY:** Buyers — especially sophisticated professional buyers in major accounts — are skilled at ending calls warmly without committing to anything. This is not deception; it is how professional procurement operates. Sellers who classify these warm endings as advances have systematically inflated pipelines and delayed recognition of stalled deals. The Continuation guard is a pre-call inoculation: if you have named the Continuation phrases before the call, you are less likely to mistake them for Advances in the moment.

**Output:** Continuation guard section embedded in the final plan document.

---

### Step 6: Write the Commitment Plan Document

**Action:** Write `commitment-plan-{deal}-{date}.md` with the structure below.

**WHY:** A written plan creates pre-call clarity and serves as a post-call reference for outcome classification. The act of writing out the specific Advance in advance forces precision that does not survive the heat of the call without it. A plan document also enables the seller to review it in the five minutes before the meeting.

---

## Output Template

```markdown
# Commitment Plan: [Account Name]
**Call date:** [Date]
**Stage:** [Current deal stage]
**Prepared by:** commitment-and-advance-planner

---

## Current Deal State

[3-5 sentences: what has been established, what Advances have been obtained, who has been accessed, what Explicit Needs the customer has expressed]

---

## Advance Targets

**Primary Advance:**
[Specific customer action — passes the name-the-action test]

**Fallback Advance:**
[Smaller but still valid customer action — also passes the name-the-action test]

**Name-the-action check:**
- Primary: "By end of call, customer will have agreed to ___." ✓
- Fallback: "By end of call, customer will have agreed to ___." ✓

---

## Four Successful Actions Script

### Action 1 — Investigating (Discovery to complete first)
[What discovery is still needed before moving toward commitment on this call]

### Action 2 — Check key concerns
Script: "Before we go further, is there anything I haven't covered that's important to you, or any questions I should address?"

[Add deal-specific variants if needed]

### Action 3 — Summarize Benefits
Script: "Let me summarize what we've established. You mentioned [Explicit Need 1] — [Capability A] addresses that by [mechanism]. You also raised [Explicit Need 2] — [Capability B] handles that with [mechanism]. There seem to be real gains from [the solution/change] based on what you've shared."

[Fill in from needs-log.md or prior call notes]

### Action 4 — Propose commitment
Primary: "[Date/format of Primary Advance] — does that work for you?"
Fallback: "Alternatively, we could start with [Fallback Advance]. That would give us [specific value] without requiring [the constraint]."

---

## Continuation Guard

If you hear any of these phrases, recognize them as Continuations and redirect:
- "We'll be in touch" → Redirect: "Would it make sense to put a specific date on the calendar now so we don't lose momentum?"
- "Let's reconnect in Q3" → Redirect: "Happy to — could we block a 30-minute call in the first week of July?"
- "Send us the proposal and we'll look at it" → Redirect: "Absolutely — to make the proposal as specific as possible, it would help to first spend 20 minutes with [stakeholder/function]. Could you arrange that?"
- "Fantastic presentation — let's meet again sometime" → Redirect: "Glad it was useful. What would be the most valuable next step — a technical deep-dive for your IT team, or a commercial conversation with [decision-maker]?"

---

## Post-Call Verification

After the call, run **spin-selling:call-outcome-classifier** on your call notes to verify:
- Was the outcome classified as an Advance or a Continuation?
- If an Advance: does the classification name the specific customer action obtained?
- If a Continuation: what was the phrase that masked it, and what redirect could have been used?

CRM update guidance: do not advance the pipeline stage until call-outcome-classifier confirms a genuine Advance was obtained.
```

---

## Key Principles

**An Advance is a customer action, not a seller action.** "I'll send them the proposal" is a seller action — it is not an Advance, no matter how much effort it represents. An Advance is when the customer agrees to do something. This distinction is the single most important reframe in the methodology.

**WHY:** Sellers who track their own actions as pipeline progress create a false picture of deal health. The deal advances when the customer moves — not when the seller does. Reorienting planning toward "what customer action do I need?" rather than "what do I need to do?" produces fundamentally different call objectives.

**Plan the Advance before the call, not after.** The Advance target must be written down before the call. In the call itself, buyer enthusiasm and the social pressure to end warmly can override the discipline to hold out for a real commitment. A pre-written plan is much harder to rationalize away than an in-the-moment judgment.

**WHY:** Rackham found that sellers without pre-call Advance objectives reliably ended up with Continuations — the call's warm social ending felt like success. The pre-call plan is the structural defense against the Continuation-as-success misread.

**Pressure closing reduces success rates in large sales — empirical evidence.** A seller who pushes back with "but my manager says I need to close harder" can be shown:
- *Photo-Store study:* Closing training increased success on low-value goods (72% → 76%), but reduced success on high-value goods (42% → 33%). The same technique that works in small sales actively reduces success in large ones.
- *54-buyer questionnaire:* Of 54 professional buyers asked whether closing techniques affected their likelihood of buying: 2 said more likely, 18 said indifferent, 34 said less likely. The buyers who are most important to major-account sellers are the ones most put off by closing techniques.
- *190-call study:* In a large office-equipment firm, the 30 calls where sellers closed most often produced 11 sales; the 30 calls where sellers closed least often produced 21 sales.

For deeper treatment of each empirical study, see `references/closing-anti-patterns.md`.

**The Four Successful Actions are not a script — they are an emphasis sequence.** They do not guarantee commitment will be obtained. They ensure the conditions under which commitment is most likely: genuine need development, concern clearance, benefit summary, and a logical proposed next step. If a buyer still will not commit after these four actions, the most productive response is a diagnostic question, not more closing pressure.

**Sophisticated buyers have defenses against closing techniques.** Professional procurement staff often keep cards cataloging common closing techniques and are trained to recognize and penalize their use. The most important deals in a B2B portfolio involve exactly these kinds of buyers. Closing technique training is not neutral in these accounts — it is actively counterproductive.

---

## Examples

### Example 1: AE Preparing for a Third Call — Moving from Champion to Economic Buyer

**Scenario:** Enterprise AE has had two discovery calls with a logistics VP (champion). She has obtained Advances on both prior calls (agreement to technical evaluation, then agreement to a product pilot scoping session). Now she needs to get in front of the CFO who controls budget.

**Trigger:** "I have a third call with the logistics VP next week. The pilot was positive but I need to get to the CFO. How do I plan this?"

**Process:**
- Step 1: Current stage — pilot scoping complete, champion is supportive, CFO not yet accessed.
- Step 2: Primary Advance — "VP agrees to arrange a 30-minute introductory meeting between seller and CFO, scheduled within 2 weeks."
- Step 3: Fallback Advance — "VP agrees to share pilot results summary with CFO and copy seller on the email."
- Step 4: Four Successful Actions script — Action 1: complete remaining pilot ROI discussion; Action 2: "Before we talk about next steps, are there any concerns from the CFO's side that I should know about?"; Action 3: "We've seen [Explicit Need 1] and [Explicit Need 2] addressed — the pilot confirmed that both are achievable in your environment."; Action 4: "Given that, the most useful next step seems to be looping in [CFO name] — could you arrange a 30-minute session in the next couple of weeks?"
- Step 5: Continuation guard — "If she says 'I'll mention it to the CFO,' that is a Continuation. Redirect: 'Happy to have you mention it — and to make it as easy as possible for her to say yes, could we set a specific time now while we're both here?'"

**Output:** `commitment-plan-acme-logistics-2024-06-18.md` with specific Advance targets and tailored Four Successful Actions script. AE walks into the call knowing exactly what she needs.

---

### Example 2: SDR Over-relying on Assumptive Closes

**Scenario:** Inside sales rep has been trained to use assumptive and alternative closes. His manager says he needs to "close harder." He keeps getting warm-sounding responses that don't turn into booked meetings.

**Trigger:** "I need to close harder on calls but I feel like pushing is making it worse. What should I do instead?"

**Process:**
- Context: This is a major-account scenario (enterprise SaaS) — closing techniques are empirically counterproductive here.
- The skill surfaces the empirical evidence (Photo-Store, 54-buyer questionnaire, 190-call study) and explains why the manager's instinct is correct for small sales but wrong for major accounts.
- Primary Advance for his next call: "Prospect agrees to a 30-minute product discovery call with their operations lead, booked on a specific date."
- Fallback: "Prospect agrees to receive and review a 2-page case study from a similar company."
- Four Successful Actions script adapted for the SDR's calling context.
- Continuation guard: "If they say 'send me some info and I'll take a look,' that is a Continuation. Respond: 'Happy to send it — to make it as relevant as possible, could we spend 10 minutes first so I can tailor it to your situation?'"

**Output:** `commitment-plan-techcorp-2024-06-20.md` — a pre-call plan the SDR can use before his next outreach. Plus: a one-paragraph explanation he can share with his manager showing why low-pressure Advance-targeting outperforms pressure closing in enterprise deals.

---

### Example 3: Founder Prepping for a High-Stakes Pilot Conversation

**Scenario:** Founder-led B2B SaaS startup. Founder has had two good calls with a potential pilot customer. The prospect has been enthusiastic but has not committed to anything concrete. The founder is unsure what to ask for next.

**Trigger:** "They seem really interested. I have a call Thursday. How do I turn this into something real?"

**Process:**
- Current stage: Enthusiasm confirmed, no Advance yet obtained.
- Primary Advance: "Prospect agrees to a 60-day paid pilot with 3 specific user accounts, starting the first week of next month."
- Fallback Advance: "Prospect agrees to a specific date (within 2 weeks) for a technical scoping session with their IT lead to assess integration requirements."
- Step 4 — Action 2 (check concerns): "Before we talk about next steps, what would need to be true for a pilot to make sense from your perspective?"
- Continuation guard: "If they say 'we're definitely interested — let's reconnect after we've had some time to digest this,' that is a classic Continuation. Don't end the call there. Respond: 'I hear you — what would it take to get a specific next step agreed today? I want to make sure we're not creating a delay that doesn't serve either of us.'"

**Output:** `commitment-plan-{company}-2024-06-22.md`. Founder walks into the call knowing the enthusiasm is not an Advance, what a real Advance looks like, and how to propose it without pressure.

---

## References

| File | Contents |
|------|----------|
| `references/four-successful-actions-detail.md` | Expanded treatment of each of the Four Successful Actions; additional dialogue examples; how to adapt the sequence for different call lengths and deal stages |
| `references/closing-anti-patterns.md` | Full empirical evidence for why pressure closing fails in major sales; Photo-Store study data; 54-buyer questionnaire; 190-call study; named closing techniques and their specific failure modes |

---

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill depends on:
```
clawhub install bookforge-call-outcome-classifier
```

For pre-call discovery question planning (the Investigating stage this skill references):
```
clawhub install bookforge-spin-discovery-question-planner
```

For drafting Benefit statements (used in Action 3 of the Four Successful Actions):
```
clawhub install bookforge-benefit-statement-drafter
```

For post-call learning and plan-do-review cycle:
```
clawhub install bookforge-sales-call-plan-do-review-coach
```

Browse the full SPIN Selling skill set: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
