---
name: diagnose-taking-control-gaps
description: |
  Diagnose a deal's taking-control posture: foil-RFP detection, passive/assertive/aggressive positioning, and misconception analysis.

  Trigger this skill when you need to:
  - Diagnose a stalled deal to find out why it isn't moving
  - Determine whether you're in a foil RFP (a verification exercise, not a real opportunity)
  - Assess whether a rep is too passive, appropriately assertive, or crossing into aggressive territory
  - Identify misconceptions about "taking control" that are limiting a rep's deal behavior
  - Understand why you're losing control of the sale or the customer conversation
  - Apply constructive tension without becoming combative
  - Evaluate whether a customer is verifying price with a competitor already chosen
  - Unblock a stalled pipeline deal by diagnosing the control gap
  - Coach a rep who is too passive or who conflates assertiveness with aggressiveness
  - Determine whether a rep is helping the customer navigate their own buying process (Lead and Simplify)

  NOT for: full negotiation planning — concession sequencing, the DuPont four-step negotiation roadmap, SSN pre-call templates (use plan-negotiation-with-constructive-tension for those).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-challenger-sale/skills/diagnose-taking-control-gaps
metadata:
  openclaw:
    emoji: "🎯"
    homepage: "https://github.com/bookforge-ai/bookforge-skills"
status: draft
source-books:
  - id: the-challenger-sale
    title: "The Challenger Sale"
    authors:
      - Matthew Dixon
      - Brent Adamson
    chapters:
      - 7
tags:
  - sales
  - b2b-sales
  - challenger-sale
  - deal-diagnosis
  - sales-control
  - negotiation-adjacent
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "deal-brief.md (required) — account, deal stage, stakeholder access granted so far, RFP context; call-transcript.md or discovery-notes.md (optional) — last meeting notes to diagnose control behaviors"
  tools-required:
    - Read
    - Write
    - AskUserQuestion
  works-offline: true
discovery:
  goal: "Diagnose a deal's taking-control posture: detect foil RFPs, classify rep behavior on the passive/assertive/aggressive spectrum, identify active misconceptions, and produce a taking-control-diagnosis.md with concrete next-action recommendations."
  triggers:
    - "diagnose stalled deal"
    - "am I in a foil RFP"
    - "losing control of the sale"
    - "passive assertive aggressive sales"
    - "take control of customer conversation"
    - "constructive tension"
    - "customer is verifying price"
    - "stalled pipeline deal"
    - "rep is too passive"
    - "why isn't my deal moving"
  audience:
    - B2B sales representatives diagnosing a live deal
    - Sales managers reviewing a rep's deal behavior
    - Sales enablement teams coaching assertiveness skills
  not_for:
    - Full negotiation planning → use plan-negotiation-with-constructive-tension
    - Building a commercial teaching pitch → use build-commercial-insight
    - Classifying rep profile type → use classify-rep-profile
---

# Diagnose Taking-Control Gaps

## Overview

Taking control of the sale is one of the three core Challenger behaviors — alongside teaching and tailoring. It is also one of the most misunderstood. Most reps either avoid it (passive posture) or confuse it with aggression. This skill diagnoses *where* a deal or rep behavior has a control gap and *why*.

The diagnosis covers four areas:
1. **Foil RFP detection** — is this opportunity a genuine purchase or a verification exercise?
2. **Behavioral spectrum classification** — passive, assertive, or aggressive?
3. **Misconception scan** — which of the three common control misconceptions are shaping behavior?
4. **Lead and Simplify assessment** — is the rep helping the customer navigate their own buying process, or passively following the customer's lead?

Output is a `taking-control-diagnosis.md` file with verdicts, evidence, and recommended next actions.

---

## When to Use

Use this skill when:
- A deal has stalled and you cannot identify why
- You received an inbound RFP and are unsure whether it's a real opportunity
- A rep's transcript or meeting notes show consistent pattern of deferring, over-agreeing, or proactively conceding
- A manager wants to coach a rep on taking-control behaviors but needs evidence from the deal record
- You want to verify whether a rep is leading the customer's buying process or following it

---

## Step 1 — Load Deal Artifacts

Read all available deal documents in the working directory.

**Required:**
- `deal-brief.md` — account overview, current deal stage, which stakeholders have been engaged, whether an RFP is present, deal size, budget confirmation status

**Optional but valuable:**
- `call-transcript.md` or `discovery-notes.md` — actual rep behavior evidence: language used, whether next steps were defined, whether pushback was maintained or dropped
- `stakeholder-map.md` — who has been granted access, what level (junior/senior), whether decision-makers have been met

If `deal-brief.md` is absent, ask the user to provide a description of the deal covering:
- Deal stage and age
- How the opportunity originated (inbound RFP, rep-generated, referral)
- Which contacts have been engaged and at what level (junior procurement, senior executive)
- Whether access to senior decision-makers has been requested and what the response was
- Key behaviors from the last 1–2 customer interactions

Why this matters: the diagnosis requires both deal context (foil detection) and behavioral evidence (spectrum classification). The more specific the evidence, the more actionable the output.

---

## Step 2 — Run the Foil RFP Detection

Roughly 20% of all sales opportunities are foil RFPs: situations where the customer has already selected a vendor but runs a formal RFP process as a verification exercise. These deals have confirmed budget, a ready contact, and real meetings — which is exactly why most reps love them. But the customer has no real intention of changing vendors.

**Apply the four foil signals:**

| Signal | Foil indicator present? |
|--------|------------------------|
| Opportunity originated as an inbound RFP or unsolicited request | Possible foil — confirm with signals below |
| Rep has only met with junior procurement or administrative contact | Strong foil signal |
| Requests for access to senior decision-makers have been vague, delayed, or denied | Strong foil signal |
| Customer sets unusually tight RFP timelines that compress meaningful evaluation | Supporting signal |

**Apply the access test:**

If the rep has not yet explicitly tested for access, flag this as a required immediate action. The access test works as follows:

At the close of the first substantive interaction, the rep should directly ask:
> "For this type of decision, our experience is that the right senior leaders need to be involved. Is that the case in your organization? When would I be able to meet with them?"

**Interpret the response:**

- Customer agrees and provides a specific timeline → not a strong foil signal; continue and revisit
- Customer hedges, says it's too early, or defers indefinitely → strong foil signal
- Customer explicitly denies access to senior leaders → foil confirmed; recommend disengage

**Foil verdict:**

Assign one of three verdicts. **In every diagnosis, state the base rate explicitly: roughly 20% of all inbound B2B sales opportunities are foil RFPs** — verification exercises where the customer has already selected a vendor but runs a formal process to validate price or satisfy procurement. This 20% base rate anchors the rep's prior before they read signals.

- **Foil — disengage:** Access denied or strongly hedged; multiple foil signals present. The rep's time is better spent on real opportunities. Recommend cutting the sales effort and redirecting resources.
- **Foil risk — access test required:** RFP is inbound and only junior contact engaged; access has not been explicitly tested. Rep must run the access test at the next interaction before investing further.
- **Not a foil:** Senior stakeholder access has been granted or a credible path exists; deal shows genuine evaluation intent.

**Required in every output:** the final `taking-control-diagnosis.md` MUST cite the ~20% foil base rate in the Foil Verdict section so the rep can calibrate against it.

---

## Step 3 — Classify Rep Behavior on the Spectrum

Using the call transcript, discovery notes, or rep's own description of recent interactions, classify observable behavior against the passive/assertive/aggressive spectrum.

See `references/control-rubric.md` for the full diagnostic checklist. Key signals:

**Passive signals:**
- Rep proactively offered a discount, extended timeline, or expanded scope without being asked
- Rep did not push for a defined next step after a positive meeting ("let's be in touch")
- Rep accepted the customer's stated next-step timeline without proposing an alternative
- Rep immediately backed down when the customer pushed back on the reframe or value case
- Rep asked "Who needs to be involved?" and waited for the customer to answer, rather than prescribing who should be

**Assertive signals (target zone):**
- Rep maintained the value position across multiple pushback rounds, citing specific evidence
- Rep defined the next step at the close of the meeting and secured agreement
- Rep pushed back on a customer assumption with a specific counter-argument, then invited the customer to explore further
- Rep proactively coached the customer on who should be involved and what steps to take next
- Rep demanded senior stakeholder access as a condition of continued investment of time and resources

**Aggressive signals (off-target):**
- Rep used language the customer described as threatening or antagonistic
- Rep continued pushing a position without reading or responding to the customer's signals
- Rep escalated in a way that damaged a key relationship without a clear value case

**Power perception check:**
A key reason reps go passive is a false belief that the customer holds all the power. Industry data consistently shows both sides perceive the other as more powerful. If the rep believes they have no leverage, they are most likely wrong — flag this in the diagnosis.

**Spectrum verdict:** Passive / Borderline passive / Assertive / Borderline aggressive / Aggressive

---

## Step 4 — Misconception Scan

Check whether any of the three named control misconceptions are shaping the rep's or team's behavior. These are not abstract — each produces specific, diagnosable behavior patterns.

**Misconception 1 — Taking control is only about negotiation (end-of-sale)**

*Diagnostic:* Rep applies pressure or holds firm only during formal pricing discussions. Earlier stages of the deal are handled passively. Rep has not run the foil access test. Rep has not maintained the reframe under pushback during discovery or pitch stages.

*Correction:* Taking control spans the entire sale. The foil access test at the first meeting is the clearest early-stage example. Controlling the buying process (Lead and Simplify) happens mid-sale. Negotiation is a subset, not the whole.

**Misconception 2 — Taking control is only about money**

*Diagnostic:* Rep holds firm on price but does not push for next steps, does not maintain the commercial teaching reframe under customer pushback, and defers on the question of who to involve and at what pace.

*Correction:* Control also means controlling how the customer thinks (maintaining the reframe), controlling deal momentum (next steps at every meeting), and controlling the buying process (prescribing steps rather than following the customer).

**Misconception 3 — Assertive equals aggressive**

*Diagnostic:* Rep (or manager) avoids any form of direct challenge or push because they fear it will damage the relationship. Any pushback is treated as "too aggressive." Alternatively, the diagnosis here can be the opposite — rep is actually aggressive (see Step 3) and using "assertive" as cover.

*Correction:* Assertive uses strong, purposeful language while sensing and responding to the customer. Aggressive pursues the rep's agenda without reading the customer's reaction. The more common failure is excessive passivity — reps who were told to take control almost never jump to aggressive; they stay passive.

Mark each misconception as: **Active / Not present / Unclear (more evidence needed)**

---

## Step 5 — Lead and Simplify Assessment

Evaluate whether the rep is helping the customer navigate their own buying process, or deferring to the customer's lead.

**Learn and React (passive — red flags):**
- Rep asked the customer "Who else needs to be involved?" and accepted whatever answer was given
- Rep followed the customer's stated timeline without proposing a more efficient path
- Rep mapped stakeholders by name and role but did not investigate what each stakeholder cares about or why
- Rep deferred to the customer's stated purchasing process even when it was clearly suboptimal

**Lead and Simplify (assertive — target behaviors):**
- Rep drew on past successful implementations to prescribe which stakeholders should be involved and why
- Rep proposed a specific next step with a date and named participants, then secured agreement
- Rep investigated stakeholder goals, biases, and personal objectives — not just job titles
- Rep simplified the customer's complex buying process by framing it in terms the customer had not articulated themselves

**Assessment verdict:** Learning and Reacting / Mixed / Leading and Simplifying

---

## Step 6 — Produce taking-control-diagnosis.md

Write `taking-control-diagnosis.md` to the working directory with the following structure:

```
# Taking-Control Diagnosis — [Deal Name / Rep Name]
Generated: [date]

## Foil RFP Verdict
[Verdict + key evidence + recommended action]

## Behavioral Spectrum Position
[Verdict + 3–5 specific behavioral observations from the deal record]

## Active Misconceptions
[List each misconception with status: Active / Not present]
[For each Active misconception: one concrete corrective action]

## Lead and Simplify Assessment
[Verdict + 2–3 specific examples from the deal record]

## Priority Next Actions
[Ordered list of 3–5 specific actions the rep should take in the next interaction]

## If Foil Confirmed — Disengage Protocol
[If foil verdict = Disengage: specific script for exiting gracefully and redirecting time]
```

**Important:** If the foil verdict is "disengage," make this the first and most prominent recommendation. Continuing to invest in a foil opportunity is the most expensive mistake in this framework — every hour spent on a foil is an hour not spent on a real opportunity.

---

## Reference Materials

- `references/control-rubric.md` — Full passive/assertive/aggressive diagnostic checklist, misconception detail, Lead and Simplify signal table, power perception gap data
- Negotiation planning (DuPont roadmap, SSN template) → `plan-negotiation-with-constructive-tension`

---

## Self-Check Before Delivering Diagnosis

Before writing the final `taking-control-diagnosis.md`, verify:

- [ ] Foil verdict is one of three defined options with evidence cited
- [ ] Spectrum verdict is based on at least 3 specific behavioral observations, not general impressions
- [ ] Each active misconception has a concrete corrective action, not just a label
- [ ] Lead and Simplify assessment is based on observable behavior from the deal record
- [ ] If foil = disengage, the first recommendation is to exit — not to try harder
- [ ] Priority next actions are specific (who does what in which interaction) — not generic advice
- [ ] No verbatim book passages appear in the output artifact

---

## Example Output Prompts (Skill-Tester Scenarios)

**Scenario A — Inbound RFP, junior contact only:**
> "I have a deal: enterprise logistics company sent us an RFP 3 weeks ago. Only contact is a procurement coordinator. We've had two calls. Deal size is $400K. They've told us 'the right people are involved' but haven't offered a meeting with anyone above director level. Decision is supposedly in 6 weeks."

Expected outputs: Foil risk verdict, access test language, misconception 1 flag, disengage-if-denied recommendation.

**Scenario B — Rep transcript with passive behavior pattern:**
> "Here is a call transcript. The rep gave a 20% discount offer on the first call without being asked. When the customer said 'our CFO isn't involved at this stage,' the rep said 'no problem, we can work with you.' Meeting ended with 'I'll be in touch next week.'"

Expected outputs: Passive spectrum verdict, misconceptions 2 and 3 flagged, Lead and Simplify deficit identified, three corrective next-step behaviors.

**Scenario C — Rep accused of being "too aggressive":**
> "My manager says I'm being too pushy with this prospect. I pushed back twice on their request for a 30% price cut, asked to meet the CFO directly, and told them if they can't give us access to their operations team we can't do a proper scoping. Now the customer says I'm hard to work with."

Expected outputs: Assertive-not-aggressive verdict, misconception 3 analysis (is the rep actually assertive or crossing into aggressive?), behavioral evidence review, guidance on sensing-and-responding to customer reaction signals.

## License

This skill is licensed under [CC-BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).

The skill was generated by the [BookForge](https://github.com/bookforge-ai/bookforge) pipeline from _The Challenger Sale_ by Matthew Dixon and Brent Adamson (Portfolio/Penguin, 2011). Content has been paraphrased and structured as an executable skill — it does not reproduce verbatim passages from the copyrighted work. Attribution required on redistribution.

## Related BookForge Skills

This skill is standalone (no dependencies). After running this diagnosis, the natural next step is to invoke `plan-negotiation-with-constructive-tension`, which consumes the `taking-control-diagnosis.md` artifact this skill produces.
