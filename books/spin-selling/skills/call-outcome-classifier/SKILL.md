---
name: call-outcome-classifier
description: |
  Classify whether a sales call outcome was an Order, an Advance, a Continuation, or a No-sale — and flag when the seller has misread a Continuation as success. Use when someone asks "did this call go well?", "was this a successful call?", "classify this call outcome", "is this a Continuation or an Advance?", "the prospect said they were impressed but didn't commit to anything specific", "they said 'fantastic presentation, let's meet again' — is that progress?", "I'm not sure if we moved the deal forward", "how do I score this call?", or "the customer seemed positive but I don't know if we advanced." Also invoke when someone shares call notes or a transcript and wants to know whether the deal progressed, whether to update their CRM with a pipeline advance, or whether a next call is needed because this one stalled. Works on raw call notes, transcripts (Gong, Chorus, Zoom exports), or recalled summaries. Reads the call; identifies the specific customer action committed (or the absence of one); classifies the outcome against SPIN Selling's four-outcome framework; flags the classic Continuation-as-success misread; and outputs a written deal-tracking assessment. Pair with commitment-and-advance-planner (SPIN Selling) to plan a better Advance objective for the next call when this one ended in Continuation.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/call-outcome-classifier
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [2]
tags: [sales, b2b-sales, enterprise-sales, call-review, call-outcome, advance, continuation, deal-tracking, commitment, complex-sales, spin-selling, post-call-analysis, pipeline-management]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "call-notes-{date}.md or call-transcript-{date}.md — raw notes or transcript from the call being classified"
    - type: document
      description: "deal-brief.md (optional) — provides deal context (stage, prior advances, account name) for a richer assessment"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "document_set — reads call notes or transcript from the working directory; writes call-outcome-{date}.md"
discovery:
  goal: "Determine whether a sales call resulted in a specific customer action commitment that moves the deal forward (Advance), a firm purchase decision (Order), an explicit rejection (No-sale), or a non-committal continuation with no agreed next step (Continuation) — and surface the Continuation-as-success misread if present"
  tasks:
    - "Read the call notes or transcript and identify every statement the customer made that could constitute a commitment"
    - "Apply the four-outcome framework to classify the call: Order / Advance / Continuation / No-sale"
    - "Name the specific customer action if classified as Advance, or state explicitly that no action was committed"
    - "Flag if positive seller language or customer pleasantries are masking a Continuation"
    - "Detect classic Continuation phrases and distinguish them from genuine Advance commitments"
    - "Write call-outcome-{date}.md with the classification, rationale, and deal-tracking note"
  audience:
    roles: ["account-executive", "enterprise-sales-rep", "sales-development-representative", "solutions-consultant", "founder-led-seller"]
    experience: "intermediate — has run sales calls but may have been classifying Continuations as success throughout their career"
  triggers:
    - "User shares call notes or transcript and asks whether the call went well or moved the deal forward"
    - "User is unsure whether to update the CRM with a pipeline advance after a call"
    - "User got positive verbal feedback from the buyer but has no specific next step agreed"
    - "User wants to classify a call outcome against the SPIN four-outcome framework"
    - "User suspects they may have accepted a Continuation when they needed an Advance"
    - "User preparing post-call review and needs a structured outcome assessment"
  not_for:
    - "Planning the Advance objective for the next call — use commitment-and-advance-planner for that"
    - "Diagnosing why the call ended in Continuation (root cause in SPIN question quality or FAB presentation)"
    - "Classifying customer need statements as Implied or Explicit — use need-type-classifier"
    - "Forecasting deal probability or win likelihood"
  quality: placeholder
---

# Call Outcome Classifier

## When to Use

You have just completed a B2B sales call and want to know whether it represented real progress. You have call notes or a transcript. You want a rigorous answer — not a gut-feel read of buyer positivity, but a classification grounded in whether the customer committed to a specific action.

This skill is most valuable when your honest answer to "how did the call go?" is "pretty well, they seemed interested" — that phrasing is a red flag. Rackham's research on 35,000+ sales calls found that salespeople routinely classify calls as successful when the customer expressed enthusiasm but agreed to nothing concrete. The skill forces you to find the customer action; if there isn't one, it classifies the call as a Continuation regardless of how positive the tone was.

**Input this skill needs:** Call notes or a transcript. Deal context (account name, stage, what happened on prior calls) improves the assessment but is not required.

**Do not use this skill to plan the next call.** If the outcome is a Continuation, use `commitment-and-advance-planner` to define a better Advance objective before the next call.

---

## Context & Input Gathering

### Required
- **Call document:** `call-notes-{date}.md` or `call-transcript-{date}.md` — the record of what happened on this call.
- **What was the call's intended objective?** (Even if just recalled aloud: "I was trying to get them to agree to a demo" or "I was going in for the order.")

### Useful
- **Deal context:** Account name, deal stage, what previous calls achieved — helps distinguish a first Advance from a fallback Advance.
- **What the seller said at the close:** The exact words used to ask for next steps, if present. This helps distinguish whether a Continuation happened because no commitment was sought vs. because the buyer declined one.

### Defaults (used if not provided)
- If deal context is absent, classify based on the call notes alone and note the context gap in the output.
- If call objective is absent, infer from the call content (e.g., if a proposal was presented, the objective was likely order or advance toward sign-off).

### Sufficiency check
Call notes or transcript alone is sufficient to classify. Ask the user for context only if the call notes are too sparse to identify whether a customer action was committed.

---

## Process

### Step 1: Read the Call and Extract Customer Action Statements

**Action:** Read the call notes or transcript. Extract every statement the customer made that could represent a commitment, agreement, or next step. List them verbatim or as close to verbatim as the notes allow.

Also note statements of enthusiasm, interest, or approval that do not include a specific action — these will be examined in Step 3.

**WHY:** The entire classification hinges on one question: did the customer commit to a specific action? Sellers read the whole call as a gestalt ("it went well"). This step forces a granular pass — separating customer words from seller words, and action commitments from expressions of opinion. An expression of opinion from the buyer ("we're very impressed") is not an action. A commitment is specific: a named next step, an agreed access point, a scheduled event, or a purchase decision.

---

### Step 2: Apply the Four-Outcome Framework

**Action:** Apply Rackham's four call outcomes to classify the call. Choose exactly one.

**Order** — The customer made a firm commitment to buy. "We're 99% likely to buy" is not an Order. To qualify as an Order, the customer showed an unmistakable intention to purchase — typically by signing paperwork, issuing a PO, or stating explicitly "we're buying this." In most major-account B2B sales, fewer than 10% of calls result in an Order.

**Advance** — An event took place, either during the call or agreed to happen after it, that moves the sale forward toward a decision. The defining criterion is a specific customer action. Typical Advances:
- Customer agreed to attend an off-site demonstration on a specific date
- Customer agreed to arrange a meeting with a higher-level decision-maker
- Customer agreed to run a pilot or product trial
- Customer agreed to introduce the seller to a previously inaccessible stakeholder or department
- Customer agreed to submit a formal evaluation request internally

An Advance must involve the **customer** doing something. A seller saying "I'll follow up next week" is not an Advance — that is the seller taking an action. The customer must commit.

**Continuation** — The sale will continue, but no specific customer action was agreed to move it forward. The call ended without either a purchase decision or a concrete next step from the buyer. Continuations are often disguised by positive buyer language. Classic Continuation phrases (Rackham's verbatim examples):
- "Thank you for coming. Why don't you visit us again the next time you're in the area."
- "Fantastic presentation, we're very impressed. Let's meet again some time."
- "We liked what we saw and we'll be in touch if we need to take things further."

These phrases share a pattern: the buyer is expressing a positive feeling, not committing to an action. The visit, the meeting, and the being-in-touch are all conditional, vague, or seller-initiated. No specific customer action = Continuation.

**No-sale** — The customer explicitly declined to proceed. A clear "we're not going forward," a cancellation, or an unambiguous rejection. No-sales are uncommon in major B2B sales — most calls that don't result in an Order end in either Advance or Continuation.

**Decision rule:** If you cannot name a specific customer action in the notes, classify the outcome as Continuation. The burden of proof falls on the Advance — it must be nameable and specific.

**WHY:** Rackham's research classified Continuations as unsuccessful calls. This may feel harsh when the buyer said positive things. But from the standpoint of pipeline progress, a call that ended with "we're impressed, let's stay in touch" has the same deal value as a call that never happened — no concrete step was taken. The classification is not a moral judgment about call quality; it is a factual statement about whether the deal moved.

---

### Step 3: Check for the Continuation-as-Success Misread

**Action:** If the call contains positive buyer language — enthusiasm, compliments, expressions of interest — and you have classified it as an Advance, re-examine your classification. Ask: is there a specific named customer action in the notes, or did the call simply feel positive?

Apply the Continuation test: "Did the customer agree to do something specific?" If yes — name it. If no — re-classify as Continuation.

Also flag if any of the following patterns are present in the notes:
- The seller summarized the call as "went really well" or "great meeting" with no specific next step named
- The buyer used phrases from the Continuation phrase list above (or close variants)
- The agreed "next step" is the seller's action only (e.g., "I'll send a proposal," "I'll follow up")
- The next meeting is vague ("sometime next month," "let's reconnect in Q3") without a date, attendees, or agenda confirmed

**WHY:** This is the most common failure mode in B2B sales. Rackham found that salespeople — trained on conventional "positive attitude" selling — routinely interpret buyer enthusiasm as progress. Buyers are often genuinely enthusiastic and still not ready to commit to an action. The seller who classifies "fantastic presentation, let's meet again" as an Advance has an inflated pipeline and no real progress. The misread compounds over the sales cycle: each Continuation that is miscounted as an Advance delays the recognition that the deal is stalled.

---

### Step 4: Write the Output Artifact

**Action:** Write `call-outcome-{date}.md` with the following structure.

**WHY:** A written classification creates a record for CRM entry, deal-tracking, and post-call review. It also forces the precision that avoids the Continuation-as-success misread — it is harder to write "Advance" in a document when you cannot supply the specific customer action.

---

## Output Template

```markdown
# Call Outcome Classification: [Account Name]

**Call date:** [Date]
**Call type:** [Discovery / Follow-up / Proposal / Demo / Other]
**Participants:** [Names / roles if known]
**Classified by:** call-outcome-classifier

---

## Classification

**Outcome: [ORDER / ADVANCE / CONTINUATION / NO-SALE]**

### Customer Action Identified

[For ADVANCE or ORDER: State the specific customer action verbatim or near-verbatim from the notes.
Example: "Customer agreed to arrange a meeting with VP of Finance — date TBD, seller to email calendar invite."]

[For CONTINUATION: State explicitly — "No specific customer action was committed on this call."]

[For NO-SALE: State the explicit rejection or withdrawal.]

---

## Rationale

[2-4 sentences explaining why the classification was assigned. Cite the customer's specific words where available.
For CONTINUATION: explain what positive language was present and why it does not constitute an Advance.]

---

## Continuation / Misread Flag

[If CONTINUATION: Flag any positive seller language or buyer compliments that could be misread as success.
Example: "The buyer said 'fantastic presentation' and 'we're very impressed' — these are expressions of sentiment, not commitments. No specific action was agreed."]

[If ADVANCE: State "No misread risk detected — specific customer action is named above."]

[If ORDER or NO-SALE: Not applicable.]

---

## Deal-Tracking Note

**CRM update:** [What to enter in the CRM — stage, next step, advance or not]
**Next call objective:** [If ADVANCE: confirm or extend the advance. If CONTINUATION: target a specific Advance — use commitment-and-advance-planner to define it before the next call. If ORDER: proceed to fulfillment. If NO-SALE: close opportunity.]

---

## References

- Relevant section: SPIN Selling, Chapter 2 (Obtaining Commitment), Four Call Outcomes framework
- For planning the next Advance: spin-selling:commitment-and-advance-planner
```

---

## Key Principles

**An Advance requires a customer action, not a seller action.** The seller saying "I'll send you the proposal" or "I'll follow up next week" is the seller taking an action — that is not an Advance. An Advance is when the customer agrees to do something: attend, introduce, approve, test, escalate. Seller-only next steps are Continuations.

**WHY:** The distinction matters for pipeline accuracy. A seller who believes the deal advanced because they are sending a proposal is treating their own future effort as deal progress. The deal only advances when the customer moves — not when the seller does. This reframe shifts the focus from selling activity to buyer commitment, which is the correct leading indicator in major B2B sales.

**Positive buyer language is noise, not signal.** "Fantastic presentation," "we're very impressed," and "let's meet again sometime" are social pleasantries. Buyers express these in calls they intend to act on and calls they intend to ignore. They have almost no predictive value for deal progress. The only reliable signal is a specific customer action committed.

**WHY:** Rackham's research found that salespeople who equate buyer enthusiasm with deal progress have systematically inflated pipeline views and delayed recognition of stalled deals. Enthusiasm is a necessary but insufficient condition for progress — a buyer must be willing to do something as well as feel something. Training yourself to ignore compliments until they are accompanied by specific actions is one of the highest-leverage behavioral changes available in major-sale selling.

**In major B2B sales, Continuations are the dominant outcome.** Fewer than 10% of calls in a major-account sales force result in an Order or No-sale. The working reality is that most calls end in Advance or Continuation — and the critical discipline is distinguishing between them. An Advance-heavy pipeline is healthy; a Continuation-heavy pipeline is stalled regardless of how "positive" individual calls feel.

**WHY:** The Advance/Continuation distinction is not a formality — it is a diagnostic. A pipeline where most calls are classified as Continuations is a pipeline where deals are not progressing. Recognizing this early allows corrective action: better Advance objectives, stronger commitment-seeking behavior, earlier qualification exits. The seller who classifies Continuations as Advances delays that recognition by entire deal cycles.

**The classification should be able to name the specific action or it is not an Advance.** This is the single hardest rule to apply in practice. After a warm call, the instinct is to see progress. The rule overrides that instinct: if you cannot write down "the customer agreed to [specific action]," it is a Continuation. No exceptions.

**WHY:** Vague "advances" — "they'll think about it," "they seemed interested in a pilot" — are not advances. A customer who "seems interested in a pilot" has not agreed to a pilot. The specificity requirement protects against wishful interpretation and creates a clear, verifiable record.

---

## Examples

### Example 1: Genuine Advance — Specific Action Named

**Scenario:** Enterprise AE reviewing notes from a second discovery call with a logistics software prospect.

**Trigger:** "I think we moved forward but want to make sure before I update the CRM."

**Call notes excerpt:** *"End of call: Marcus said he wants to loop in his VP of Operations before they go further. He offered to set up a three-way call for next Thursday and asked me to send him a one-pager to share internally ahead of time. I said I'd have it to him by Wednesday."*

**Process:**
- Step 1: Customer action statements: "He offered to set up a three-way call for next Thursday" — customer is taking action (setting up the call). "Asked me to send a one-pager" — seller action.
- Step 2: Advance. The customer agreed to arrange access to a higher-level decision-maker (VP of Operations) and set a specific date (next Thursday).
- Step 3: No misread risk. The customer action (three-way call with VP) is specific, dated, and customer-initiated.

**Output:** `call-outcome-2024-03-12.md` — ADVANCE. Customer action: "Marcus agreed to arrange three-way call with VP of Operations for Thursday 2024-03-14; confirmed before call." CRM update: advance to next stage, log VP of Operations introduction as next-step objective.

---

### Example 2: Continuation Disguised as Success

**Scenario:** Mid-market AE reviewing notes from a demo call that felt like a breakthrough.

**Trigger:** "The demo went great. They were really engaged and the VP said it was exactly what they needed. Should I move this to 'proposal stage' in the CRM?"

**Call notes excerpt:** *"Fantastic demo — they loved the reporting module. VP said 'this is exactly the kind of solution we've been looking for.' Everyone was nodding. At the end, Sarah (champion) said 'we're definitely interested, let's circle back after we've had some time to digest this.' I said I'd follow up next week."*

**Process:**
- Step 1: Customer action statements: "Let's circle back after we've had some time to digest this" — no specific action, conditional and buyer-initiated in form only. "I'd follow up next week" — seller action only.
- Step 2: Continuation. No customer action committed. "Circling back" is buyer-conditional with no date, no agenda, no confirmed attendees.
- Step 3: Continuation-as-success misread present. The VP's phrase "this is exactly the kind of solution we've been looking for" is an expression of sentiment, not a commitment. "Let's circle back" matches the classic Continuation pattern. Flag raised.

**Output:** `call-outcome-2024-03-15.md` — CONTINUATION. No specific customer action committed. Flag: "The VP's enthusiasm and Sarah's 'we're definitely interested' are positive sentiment signals, not Advance commitments. 'Let's circle back after we've had some time to digest' is a Continuation — no date, no agreed agenda, no access to additional stakeholders. Do not advance CRM stage. Use commitment-and-advance-planner to define a specific Advance objective before the next contact."

---

### Example 3: Order — Clear Purchase Commitment

**Scenario:** Field sales rep reviewing notes from a closing call.

**Trigger:** "They signed the MSA, right? Just documenting the outcome."

**Call notes excerpt:** *"Jeff signed the MSA on the spot. 3-year contract, $180K ARR. CC'd their procurement lead on the confirmation email."*

**Process:**
- Step 1: Customer action: Signed MSA. Procurement loop-in confirming.
- Step 2: Order. Unmistakable intention to purchase, paperwork signed.
- Step 3: No misread risk.

**Output:** `call-outcome-2024-03-18.md` — ORDER. Customer action: MSA signed, $180K ARR, 3-year term. CRM: move to Closed Won, initiate onboarding.

---

## References

| File | Contents |
|------|----------|
| `references/continuation-phrase-guide.md` | Verbatim Continuation phrases from SPIN Selling research; variants and near-miss examples; how to distinguish Continuation language from genuine Advance language; detection checklist |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

```
clawhub install bookforge-commitment-and-advance-planner
```

For need classification on the same call, also:
```
clawhub install bookforge-need-type-classifier
```

Browse the full SPIN Selling skill set: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
