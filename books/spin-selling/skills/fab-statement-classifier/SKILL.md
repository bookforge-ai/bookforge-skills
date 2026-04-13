---
name: fab-statement-classifier
description: "Classify seller statements as Features, Advantages, or true Benefits using Rackham's strict FAB definitions. Use this skill to audit a pitch deck, sales email, demo script, or call transcript for FAB distribution. Invoke when someone asks 'are these benefits or advantages?', 'is this a feature or a benefit?', 'review my sales deck for FAB', 'audit my pitch for Rackham FAB', 'classify these statements', 'are my slides benefit-focused?', 'why am I getting objections to my deck?', 'does this qualify as a benefit?', or 'I call these benefits but I'm not sure'. The skill enforces Rackham's empirically-derived definition: a statement is a Benefit ONLY if it meets a customer-expressed Explicit Need — not if it sounds helpful, not if it shows the product can help, and not if it meets a problem (Implied Need). In typical B2B sales content, 40-50% of statements labeled 'Benefits' by the seller are actually Advantages. This skill catches that. Also includes Rackham's 10-item FAB classification quiz for self-testing. Applies to B2B account executives auditing their own decks, sales managers reviewing team content, and marketers producing collateral for large-sale contexts."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/fab-statement-classifier
metadata: {"openclaw":{"emoji":"🔬","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [5, 6]
tags: [sales, b2b-sales, enterprise-sales, fab-methodology, pitch-deck-review, content-audit, spin-methodology, objection-prevention]
depends-on:
  - need-type-classifier
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Seller content to audit — pitch deck export (.md, .pdf, .txt), sales email, demo script, or call transcript with seller statements extracted"
    - type: document
      description: "Deal context (optional) — needs-log.md or deal-brief.md identifying Explicit Needs the customer has expressed"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Document set: pitch-deck-{deal}.md, sales-email.md, demo-script.md, or call-transcript-{date}.md. Agent classifies and produces audit report; human acts on the coaching."
discovery:
  goal: "Determine whether each seller statement is a Feature, Advantage, or true Benefit — and surface the dominant error: statements labeled Benefits that are actually Advantages"
  tasks:
    - "Classify each statement from provided seller content as Feature, Advantage, Benefit, or unclassifiable"
    - "Flag the Advantage-as-Benefit anti-pattern when present"
    - "Produce a count summary by FAB type"
    - "Provide coaching guidance on converting Advantages into Benefits by first developing Explicit Needs"
    - "Run interactive FAB practice using Rackham's 10-item quiz"
  audience:
    roles: [account-executive, sales-manager, solutions-consultant, marketer, founder-led-seller]
    experience: intermediate
  when_to_use:
    triggers:
      - "Before a major demo or proposal — check whether the deck has any true Benefits or only Advantages"
      - "After a call with objections — diagnose whether the content generated them by offering Advantages"
      - "Marketing reviewing collateral for large-sale context — most 'Benefits' in decks are Advantages"
      - "Sales coaching — showing a rep why their 'benefits-focused' deck actually contains zero Benefits"
      - "Self-training using the 10-item FAB quiz"
    prerequisites:
      - "need-type-classifier — needed to verify whether an Explicit Need is present before classifying as Benefit"
    not_for:
      - "Drafting new Benefit statements (use benefit-statement-drafter)"
      - "Generating SPIN questions to develop Explicit Needs (use spin-discovery-question-planner)"
      - "Diagnosing objection causes in full (use objection-source-diagnoser)"
      - "Pricing strategy"
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
      - "Marks aspirational claims ('so you can focus on what matters') as Advantages, not Benefits"
      - "Correctly requires a prior customer-expressed Explicit Need before allowing Benefit classification"
      - "Flags the industry-wide pattern of labeling Advantages as Benefits"
    what_baseline_misses:
      - "Calls any statement showing value a 'Benefit' without checking for an Explicit Need"
      - "Treats implied needs ('they mentioned this problem') as sufficient basis for a Benefit"
      - "Does not distinguish between Type A and Type B definitions or flag the naming confusion"
---

# FAB Statement Classifier

## When to Use

You have seller content — a pitch deck, sales email, demo script, or call transcript — and you need to know: are these statements Features, Advantages, or true Benefits?

This matters because the most common error in B2B sales content is calling Advantages "Benefits." Rackham's 5,000-call study found that Advantages (what most training calls "Benefits") had no statistically significant relationship to success in large sales — but true Benefits were strongly linked to Orders and Advances. The distinction is not semantic. It predicts whether your content will close deals or generate objections.

Use this skill:
- Before a major demo or proposal, to verify the content contains true Benefits (not just Advantages)
- After a call where you received value objections or "it's not worth it" responses — these are the customer response most correlated with Advantage-heavy selling
- When marketing reviews collateral for use in large-sale contexts
- When coaching a rep who claims their deck is "benefit-focused"

**Interactive practice mode:** If you want to self-test your FAB classification ability, ask the skill to run Rackham's 10-item quiz. The full quiz with answer key is in [references/fab-classification-quiz.md](references/fab-classification-quiz.md).

Do NOT use this skill to draft new Benefit statements (use `benefit-statement-drafter`) or to generate questions to develop needs (use `spin-discovery-question-planner`).

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Seller content to audit:** The actual statements you want classified
  -> Check prompt for: pasted text, file path, or slide content
  -> Check environment for: `pitch-deck-{deal}.md`, `sales-email.md`, `demo-script.md`, `call-transcript-{date}.md`
  -> If missing, ask: "Paste or point me to the seller statements you want me to classify."

- **Sale context (large vs small):** Determines how strictly to apply the Benefit gate
  -> Check prompt for: enterprise/SMB label, deal size, multi-stakeholder mention
  -> Check environment for: `deal-brief.md`
  -> If missing: default to large-sale context (conservative — prevents overstating Benefits)

### Observable Context (gather from environment)

- **Needs log or deal brief:** Explicit Needs the customer has expressed
  -> Look for: `needs-log.md` from `need-type-classifier`, `deal-brief.md`
  -> If available: use it to verify Benefit candidates — a statement meets an Explicit Need only if that need is documented as expressed by the customer
  -> If unavailable: note the absence; any statement claiming to meet a need will be classified as Advantage unless the customer's Explicit Need is visible in the content itself (e.g., in a call transcript where both sides speak)

- **Mode check:** Is this an audit of existing content, or an interactive quiz?
  -> Audit mode: read the provided content, classify each statement, produce `fab-audit-{artifact}.md`
  -> Quiz mode: deliver the 10-item Rackham quiz, collect answers, give scored feedback

### Sufficiency Threshold

SUFFICIENT: Seller content + sale context (or default to large)
PROCEED WITH DEFAULTS: Content present, no needs log (classify all statements without confirmed Explicit Needs as Advantages with a note)
MUST ASK: No seller content provided AND no quiz mode requested

## Process

### Step 1: Establish the Classification Framework

**ACTION:** Before classifying any statement, confirm the three definitions below. Apply them exactly as written.

**WHY:** The entire value of this audit depends on using Rackham's strict definitions, not the common-usage definitions. Most sellers have been trained that "a Benefit is anything that shows how a feature can help the customer" — this is what Rackham calls an Advantage. If this step is skipped, every subsequent classification defaults to the casual definition and the audit produces no new information.

**The three definitions:**

**Feature** — A fact, data point, or characteristic about the product or service. Does not explain use or link to customer outcomes. Neutral in impact.
- Test: "Is this just describing what the product is or what it includes?" → Feature

**Advantage** — A statement showing how a product feature can be used or can help the customer. More than a Feature — links capability to potential value. BUT: does not meet a customer-expressed Explicit Need.
- This is what most sales training calls a "Benefit." It is not a Benefit in Rackham's taxonomy.
- Test: "Does this show how the product helps, but without a prior customer-expressed want?" → Advantage

**Benefit (Rackham's Type B)** — A statement showing how the product meets an Explicit Need that the customer has expressed. Both conditions required:
1. The customer stated a specific want, desire, or intention before this statement
2. This statement shows the product meets that specific expressed need
- Test: "Did the customer explicitly say they need/want this? AND does this statement show we can deliver it?" → Benefit

**Unclassifiable** — A statement that cannot be evaluated without more context (e.g., a question, a transition phrase, a non-product statement).

**Step 1 output:** Confirm the three definitions are loaded before proceeding.

### Step 2: Identify Explicit Needs in the Context

**ACTION:** Before classifying individual statements, scan the available context (needs-log, deal brief, or transcript) for any customer-expressed Explicit Needs. List them. These are the only valid anchors for Benefit classifications.

**WHY:** The classification of any statement as a Benefit requires a prior customer-expressed Explicit Need. Without identifying those first, there is no reference point — every statement defaults to Feature or Advantage. This step also prevents the common error of using Implied Needs (problems, difficulties) as Benefit anchors. If you need to verify whether a specific customer statement is an Explicit Need, invoke `need-type-classifier` or apply its definitions directly: an Explicit Need is a statement of want, desire, or intention ("we need X," "we're looking for Y," "I'd like Z") — not a statement of problem or dissatisfaction.

**IF** a `needs-log.md` exists from a prior `need-type-classifier` run → read it and extract the Explicit Needs column
**ELSE IF** the content being audited is a call transcript (both sides visible) → scan buyer statements for Explicit Need language
**ELSE** → note that no confirmed Explicit Needs are available; proceed with the understanding that Benefit classifications will be rare or absent

**Step 2 output:** A short list of confirmed Explicit Needs available in context (may be empty).

### Step 3: Classify Each Statement

**ACTION:** For each seller statement in the provided content, apply the definitions from Step 1, anchoring to the Explicit Needs from Step 2. Produce a per-statement classification table.

**WHY:** Showing the classification evidence per statement makes the output auditable. The seller needs to see exactly which words triggered each classification — especially for statements they labeled Benefits that are actually Advantages. Without this granularity, coaching is abstract; with it, the seller can rewrite specific statements.

**For each statement, output:**
1. Statement (quoted or paraphrased if long)
2. Classification: Feature / Advantage / Benefit / Unclassifiable
3. Explicit Need present: Yes (quote it) / No
4. Rationale: one sentence explaining the classification

**The dominant pattern to flag:** Statements containing phrases like "so you can," "which means you'll," "helping your team," "giving you the ability to," "enabling you to" are structural markers of Advantages. They show use or help — but unless paired with a prior customer-expressed want, they are Advantages, not Benefits. Flag these explicitly when the seller has labeled them Benefits.

**Step 3 output:** Classification table, one row per statement.

### Step 4: Produce the Count Summary and Anti-Pattern Flag

**ACTION:** Summarize the classification results. Count Features, Advantages, Benefits, and Unclassifiable. Flag the Advantage-as-Benefit anti-pattern if present.

**WHY:** The count summary makes the FAB distribution visible at a glance. Most sellers are surprised by how few true Benefits their content contains. A deck with 15 statements that the seller calls "benefit-focused" typically contains 0-2 true Benefits, 8-10 Advantages, and 4-5 Features. Showing this quantitatively is more persuasive than qualitative criticism.

**Count summary format:**
- Total statements audited: N
- Features: N (N%)
- Advantages: N (N%)
- **True Benefits (Rackham): N (N%)**
- Unclassifiable: N (N%)

**Advantage-as-Benefit flag:** If any statement was labeled a "Benefit" by the seller (in the deck or script) but classified as an Advantage by this audit, call this out explicitly:
> "WARNING: N statements labeled 'Benefits' in this content are Advantages by Rackham's definition. They show how the product can help but do not meet a customer-expressed Explicit Need. In large sales (5,000-call study), Advantages have no statistically significant relationship to call success. True Benefits require a prior Explicit Need from the customer."

**Step 4 output:** Count summary + anti-pattern flag (if applicable).

### Step 5: Coaching — Converting Advantages to Benefits

**ACTION:** For each statement classified as Advantage, provide a one-line coaching note: what Explicit Need the customer would need to express before this Advantage could become a Benefit, and how to develop that need.

**WHY:** The audit is only useful if it tells the seller what to do next. "This is an Advantage, not a Benefit" is a diagnosis. The prescription — "here's the Explicit Need you'd need to develop before presenting this" — is what makes the content actionable. Without this step, the seller knows their deck is weak but not how to fix it.

**Coaching note format (per Advantage):**
> Statement: "[statement]"
> To become a Benefit, your customer would need to have said something like: "[example Explicit Need in customer's words]"
> How to develop it: Ask [Problem Question to surface Implied Need] → [Implication Question to build consequence] → [Need-payoff Question to get the customer to articulate the want]. Then present this capability as directly meeting their stated need.

**Step 5 output:** Per-Advantage coaching notes.

### Step 6: Write the Audit Report

**ACTION:** Compile Steps 3-5 into a single structured report. Write it to `fab-audit-{artifact}.md` (e.g., `fab-audit-q2-deck.md`, `fab-audit-discovery-email.md`).

**WHY:** A written report persists across the conversation and can be shared with the team. It also feeds downstream skills: `benefit-statement-drafter` reads a needs log and the audit to draft Benefits for the confirmed Explicit Needs; `objection-source-diagnoser` reads the audit to trace objections back to FAB source.

**Report structure:**
```
# FAB Audit — {Content Name} — {Date}

## Sale Context
{Large / Small / Unknown}

## Explicit Needs Available
{List, or "None confirmed — all Benefits require Explicit Need development first"}

## Statement-by-Statement Classification
| # | Statement | Classification | Explicit Need Present | Rationale |
|---|---|---|---|---|

## FAB Distribution Summary
- Features: N (N%)
- Advantages: N (N%)
- True Benefits: N (N%)

## Advantage-as-Benefit Flag
{If applicable: which statements were miscategorized, and why it matters}

## Coaching: Converting Advantages to Benefits
{Per-Advantage coaching notes}

## Recommended Next Step
{One paragraph: what the seller should do before the next call/send}
```

### Optional: Interactive Practice Mode

**ACTION:** If the user asks to test their own FAB classification ability, deliver Rackham's 10-item quiz from [references/fab-classification-quiz.md](references/fab-classification-quiz.md). Present all 10 statements, collect the user's answers, then score and explain each one.

**WHY:** The quiz uses a real selling dialogue with deliberate classification traps (especially #7 and #10, which sound like Benefits but are Advantages). Users who pass it — especially #7 — have internalized the Type A/Type B distinction. The quiz also grounds future audits in shared vocabulary.

## Key Principles

- **A Benefit requires customer speech first.** No matter how aspirational, customer-focused, or value-oriented a statement sounds, it is an Advantage unless the customer has expressed the underlying want in their own words before the statement was made. Pitch decks, by their nature, cannot contain true Benefits — they are written before the customer has spoken. They contain Features and Advantages at best.

- **The naming confusion is the problem.** Decades of sales training have used the word "Benefit" to mean what Rackham calls an Advantage. Sellers who were well-trained in "Feature-Benefit selling" are actually Feature-Advantage sellers. Rackham's 5,000-call study showed that what most people call Benefits have no statistical relationship to large-sale success. True Benefits — those meeting customer-expressed Explicit Needs — are strongly correlated with Orders and Advances.

- **Advantages create objections in large sales.** Linda Marsh's correlation study showed that Advantages are the most probable source of customer objections. When a seller presents a capability the customer hasn't asked for, the customer evaluates whether it's worth the cost — and in large sales, "not worth it" is a likely response. This is why objection-heavy calls are typically Advantage-heavy calls.

- **More Features → more price sensitivity.** From the 18,000-call Features study: heavy use of Features increases customer sensitivity to price. In expensive products, this works against the seller. When classified Features are high, advise shifting from description to need development.

- **Development precedes Benefits.** Rackham's advice: "Do a good job of developing Explicit Needs and the Benefits almost look after themselves." You cannot manufacture Benefits from content alone — you develop them from customer conversations. The audit's purpose is to show what's missing and guide what needs to be developed before the content can be benefit-loaded.

- **Stay in scope.** This skill classifies existing content. It does not draft new statements (use `benefit-statement-drafter`), generate questions to develop needs (use `spin-discovery-question-planner`), or diagnose objections in depth (use `objection-source-diagnoser`). When the audit points to a development gap, name the right skill.

## Examples

**Scenario: Pitch deck audit before a major enterprise demo**

Trigger: AE says: "I'm presenting a 15-slide deck tomorrow. Can you check if it's benefit-focused?"

Process:
- (Step 1) Load FAB definitions.
- (Step 2) Read needs-log.md — 2 Explicit Needs documented: "We need to cut monthly close from 5 days to 2" and "We need a single dashboard for all 3 regions."
- (Step 3) Classify all 15 slides' key statements. Find: 6 Features (product specs, pricing, company stats), 8 Advantages ("helps your team move faster," "gives you complete visibility," "reduces guesswork"), 1 Benefit (the single-dashboard claim meets the stated Explicit Need), 0 unclassifiable.
- (Step 4) Count: 40% Features, 53% Advantages, 7% Benefits. Flag: 8 statements the seller labeled "Benefits" in the deck are Advantages.
- (Step 5) For each of the 8 Advantages, provide a coaching note on what Explicit Need to develop.
- (Step 6) Write `fab-audit-q2-demo-deck.md`.

Output: Audit report showing 1 confirmed Benefit, 8 Advantages mislabeled as Benefits, 6 Features. Recommendation: develop 1-2 more Explicit Needs on the pre-call before tomorrow — at minimum, convert the "monthly close" Advantage into a Benefit by confirming the need directly.

---

**Scenario: Sales email review**

Trigger: SDR asks: "Is this prospecting email too feature-heavy? I'm not getting replies."

Process:
- (Step 1) Load definitions.
- (Step 2) No needs log — cold outreach, no prior customer speech. Note: no Explicit Needs available → no Benefits possible.
- (Step 3) Read the email. Find: 3 Features (product specs), 4 Advantages ("so you can close deals faster," "giving your team complete pipeline visibility," "cutting your reporting time by 50%"), 0 Benefits (no customer has spoken).
- (Step 4) Count: 43% Features, 57% Advantages, 0% Benefits. Flag: a cold email structurally cannot contain Benefits — the customer hasn't spoken yet. All value claims are Advantages.
- (Step 5) Coach: the email is Advantage-heavy, which in cold outreach is normal but not maximally effective. Recommend opening with a Problem Question or a specific Implied Need trigger ("If your team is finding that...") to earn a reply, then developing needs in the first call before giving Benefits.

Output: `fab-audit-prospect-email.md`. Coaching: shift the email to problem-focused language (what problem do they probably have?) rather than solution-focused language (what can our product do?). Follow up with `spin-discovery-question-planner` for the first call.

---

**Scenario: Interactive quiz practice**

Trigger: "I want to test my FAB classification. Give me the quiz."

Process: Present the 10-item dialogue from [references/fab-classification-quiz.md](references/fab-classification-quiz.md). Collect answers. Score. For any misclassified items, explain the rule that applies — especially items 7 and 10, which are the traps (they sound like Benefits, but no Explicit Need was expressed).

Output: Score (X/10). Detailed feedback on any misses. Particular emphasis if the user called #7 or #10 a Benefit — these are the most common errors and map directly to the Advantage-as-Benefit anti-pattern in real sales content.

## References

- [fab-classification-quiz.md](references/fab-classification-quiz.md) — Rackham's 10-item FAB classification exercise with full answer key and scoring guide
- [fab-definitions-and-edge-cases.md](references/fab-definitions-and-edge-cases.md) — Complete FAB definitions, research findings, edge cases, and the FAB-to-customer-response chain (Features → price concerns; Advantages → objections; Benefits → approval)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill depends on:
- `clawhub install bookforge-need-type-classifier` — Classify customer statements as Implied or Explicit Needs (needed to verify whether an Explicit Need exists before classifying a statement as a Benefit)

Skills that build on this one:
- `clawhub install bookforge-benefit-statement-drafter` — Draft Benefit statements that link product capabilities to customer-expressed Explicit Needs (the constructive complement to this audit skill)
- `clawhub install bookforge-objection-source-diagnoser` — Trace objections back to their FAB-behavior root cause (Feature → price concerns; Advantage → value objections)

Or install the full SPIN Selling skill set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
