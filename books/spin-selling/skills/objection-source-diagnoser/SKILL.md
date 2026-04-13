---
name: objection-source-diagnoser
description: "Diagnose WHY a deal is accumulating objections by tracing each one back to its root-cause seller behavior. Use this skill when a customer keeps pushing back, when you're getting too many price objections, when the prospect raised concerns you don't know how to address, when a rep asks 'why does my pitch generate so much resistance?', or when someone asks 'what's wrong with my presentation?'. Invoke when someone says 'diagnose these objections', 'we keep getting price objections', 'why does the customer keep saying it's not worth it', 'how do I stop getting so many objections', 'the prospect raised X — how should I respond?', 'my deal has too many concerns', 'objections are killing my pipeline', or 'what's causing all this pushback?'. The skill reads call notes or transcripts, extracts every objection, and maps each to its FAB-source root cause using Rackham's empirically-derived behavior→response chain: Features cause price concerns; Advantages cause value and capability objections; premature solution presentation causes early-call objections. The output is a prevention plan for the NEXT call — which seller behaviors to remove, and which SPIN questions to use to develop needs more thoroughly. This skill explicitly refuses to produce 'when they say X, respond with Y' objection-handling scripts. That approach treats symptoms. This skill treats causes. Backed by Rackham's analysis of 35,000+ sales calls and Linda Marsh's correlation study showing Advantages as the primary driver of objections. Applies to B2B AEs, enterprise sales reps, and sales managers debriefing a struggling rep."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/objection-source-diagnoser
metadata: {"openclaw":{"emoji":"🔍","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [6]
tags: [sales, b2b-sales, enterprise-sales, objection-prevention, spin-methodology, fab-methodology, call-diagnosis, deal-review]
depends-on:
  - fab-statement-classifier
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Call notes or transcript from one or more calls on this deal — the raw material for objection extraction"
    - type: document
      description: "Objections log (optional) — accumulated list of objections across the deal lifecycle if available"
    - type: document
      description: "FAB audit (optional) — if fab-statement-classifier has already been run on the seller's pitch content, its output is used to cross-reference objection sources"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Document set: call-notes-{date}.md, call-transcript-{date}.md, objections-log.md (if accumulated). Agent diagnoses and outputs objection-prevention-plan-{deal}.md; human applies the behavioral changes on the next call."
discovery:
  goal: "Trace each objection back to a specific seller behavior (Feature overuse, Advantage without developed need, premature solution) and produce a ranked prevention plan for the next call"
  tasks:
    - "Extract every objection raised by the customer from the provided call notes or transcript"
    - "Map each objection to its most probable FAB-source root cause using the behavior→response causal map"
    - "Identify which seller behaviors generated objections (Features used heavily, Advantages before Explicit Needs, solutions offered before value built)"
    - "Produce a prevention plan: behaviors to remove, SPIN questions to use instead"
    - "Explicitly decline to produce objection-handling response scripts"
  audience:
    roles: [account-executive, enterprise-sales-rep, sales-manager, solutions-consultant, founder-led-seller]
    experience: intermediate
  when_to_use:
    triggers:
      - "After a call where the customer raised multiple objections — diagnose before the next call"
      - "When price objections are piling up across multiple calls in a deal"
      - "Sales manager debriefing a rep who is generating excessive objections"
      - "When a rep asks 'how do I handle this objection?' — redirect to root cause first"
      - "Accumulated objections-log.md suggests a pattern worth diagnosing"
    prerequisites:
      - "fab-statement-classifier — provides the FAB definitions and the behavior→response chain needed to classify each objection's source; if not run separately, the definitions are embedded in this skill"
    not_for:
      - "Writing objection-handling response scripts ('when they say X, say Y') — this skill refuses to do that"
      - "Auditing pitch deck FAB distribution (use fab-statement-classifier)"
      - "Generating SPIN questions for the next call (use spin-discovery-question-planner — this skill recommends invoking it)"
      - "Pricing strategy or discount decisions"
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
      - "Recognizes price objections as caused by Feature overuse, not price sensitivity — rejects the symptom/treatment default"
      - "Maps 'it's not worth it' objections to Advantage-before-Explicit-Need pattern, not to poor articulation"
      - "Identifies early-call objections as premature solution presentation, not inadequate opening"
    what_baseline_misses:
      - "Baseline produces 'when they say X, respond with Y' scripts — treats symptoms, not causes"
      - "Baseline does not distinguish between objection types by FAB source"
      - "Baseline cannot recommend specific upstream behavioral changes to prevent recurrence"
---

# Objection Source Diagnoser

## When to Use

You have call notes or a transcript from a deal where the customer raised objections — price concerns, "it's not worth it" responses, capability doubts, or outright resistance — and you want to understand why those objections arose and how to prevent them on the next call.

**The central reframe:** Most sales training treats objections as a communication problem. The customer raised an objection; you need a better response. SPIN research — backed by analysis of 35,000+ calls and Linda Marsh's correlation study — shows that this is backwards. Objections are not a communication problem. They are a sequencing problem. The customer raised an objection because the seller offered a solution before building sufficient value. The fix is not a better response script; the fix is better behavior earlier in the call.

Use this skill:
- After any call where the customer raised more than one objection, before planning the next call
- When price objections have appeared more than twice across a deal — this is a signal of Feature overuse, not a price problem
- When a sales manager is reviewing a call where a rep received heavy pushback
- When your instinct is "I need better objection-handling techniques" — run this diagnosis first; the answer is almost always prevention, not handling

**IMPORTANT — What this skill will NOT do:** This skill will not produce "when they say X, respond with Y" objection-handling scripts. That approach treats symptoms. This skill treats causes. If you want handling scripts, you need a different tool. This skill will produce a prevention plan.

Do NOT use this skill to audit pitch-deck FAB distribution (use `fab-statement-classifier`), generate SPIN questions for the next call (use `spin-discovery-question-planner`), or make pricing decisions.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Call notes or transcript from the call(s) where objections arose**
  -> Check prompt for: pasted text, file path, or transcribed dialogue
  -> Check environment for: `call-notes-{date}.md`, `call-transcript-{date}.md`
  -> If missing, ask: "Can you paste the call notes or point me to the file where the objections occurred?"

- **What product or capability was being discussed**
  -> Check prompt for: product name, deal context, what was being presented
  -> Check environment for: `deal-brief.md`, `product-capabilities.md`
  -> If missing: infer from call notes OR ask: "What were you selling or presenting when the objections arose?"

### Observable Context (gather from environment)

- **Accumulated objections log**
  -> Look for: `objections-log.md` — if present, scan for patterns across multiple calls before diagnosing any single call
  -> If available: note recurring objection types as they suggest a systemic seller behavior pattern, not a one-call anomaly

- **FAB audit from fab-statement-classifier**
  -> Look for: `fab-audit-{deal}.md` — if the seller's pitch content has already been audited for FAB distribution, use it to cross-reference objection sources
  -> If unavailable: apply FAB definitions directly from the call notes themselves (Step 2 embeds the definitions)

- **Needs log from prior calls**
  -> Look for: `needs-log.md` — if available, it tells you which Explicit Needs have been developed; Advantages presented without a corresponding Explicit Need are the primary objection source
  -> If unavailable: note the absence and treat all capability statements as Advantage candidates

### Sufficiency Threshold

SUFFICIENT: Call notes or transcript with at least one objection present + product/deal context
PROCEED WITH DEFAULTS: Notes without a separate FAB audit (apply FAB definitions inline in Step 2)
MUST ASK: No call notes and no pasted objection text

## Process

### Step 1: Extract Every Objection

**ACTION:** Read the provided call notes or transcript and extract every customer objection — any statement where the customer expresses resistance, doubt, price concern, or skepticism about the seller's capability or value claim. List them individually.

**WHY:** Diagnosis requires a complete inventory. Sellers often remember the most painful objection and forget others. The diagnostic value comes from seeing the full pattern — three price objections plus two "not worth it" responses is a different diagnosis than one early resistance to a solution. Missing objections will produce an incomplete prevention plan.

**What counts as an objection:**
- Price concern: "It's too expensive," "I can't justify that cost," "That's a lot of money for what it does"
- Value doubt: "I don't think it's worth the trouble," "We're happy with our current system," "That seems like overkill"
- Capability doubt: "My people would never use that," "That wouldn't work in our environment"
- Resistance to change: "We tried something like this before and it didn't work"
- Early-call resistance: Any pushback or deflection that occurs in the first half of a call, often in response to a solution being mentioned too soon

**What does NOT count:** Questions ("How does that work?"), clarification requests ("Can you show me an example?"), or neutral fact-checks ("Is that compatible with our system?"). These are engagement, not objections.

**Step 1 output:** A numbered list of objections, each quoted or closely paraphrased from the call notes, with the approximate position in the call (early/mid/late) noted.

---

### Step 2: Map Each Objection to Its FAB-Source Root Cause

**ACTION:** Apply the behavior→response causal map to each objection. Determine which seller behavior most likely caused it, based on Rackham's three-part chain.

**WHY:** This is the diagnostic core of the skill. The causal map is not intuitive — most sellers assume objections reflect the customer's personality, budget situation, or competitor preference. The research evidence is different: in the overwhelming majority of cases, objections are seller-caused. Linda Marsh's correlation study found statistically significant links between FAB behavior patterns and specific objection types. Without this map, a seller diagnoses the wrong cause and applies the wrong remedy.

**The FAB→Response Causal Map:**

| Seller Behavior | Customer Response | Mechanism |
|---|---|---|
| **Heavy Feature use** | **Price concerns** ("It's expensive," "I don't know if it's worth the cost") | Features increase price sensitivity. For expensive products, this works against the seller — the customer is primed to scrutinize cost without having developed a sense of value. |
| **Advantages before Explicit Needs** | **Value objections** ("It's not worth the trouble," "We don't really need that," "We're fine with what we have") | An Advantage shows capability. But if the customer hasn't expressed a want for that capability, they evaluate it as a cost-to-benefit tradeoff — and in large sales the solution cost often outweighs an undeveloped problem. The customer raises an objection because the seller has not yet built sufficient value through need development. |
| **Premature solution presentation** | **Early-call objections** — any objection that arises in the first half of the call, often about price, fit, or necessity | Solutions offered before questions are asked generate resistance because the customer has not yet become invested in the problem. They haven't been led to see the problem's magnitude, so the solution feels unnecessary. |
| **Benefits meeting Explicit Needs** | **Support and approval** | When a seller presents a capability that meets a want the customer has already expressed, the natural response is endorsement, not objection. The absence of objections at this point is confirmation the sequencing was correct. |

**Classification steps for each objection:**

1. Look at what the seller said immediately BEFORE the objection arose. Find that seller statement in the call notes.
2. Classify that seller statement using FAB definitions:
   - Is it a **Feature** (describing the product's characteristics without linking to value)?
   - Is it an **Advantage** (showing how the product helps, but without a prior Explicit Need from the customer)?
   - Is it a **premature solution** (naming capabilities or solutions before the customer has developed the problem's importance)?
3. Match the objection type to the causal map above.
4. Note whether an Explicit Need had been developed before the Advantage or solution was offered. If a needs-log exists, cross-reference it. If not, scan the transcript for any prior customer statement expressing a specific want ("we need X," "I'd like Y," "we're looking for Z"). Absence of such a statement before the capability was presented = Advantage, not Benefit.

**Step 2 output:** A per-objection table:

| # | Objection (quoted) | Objection Type | Seller behavior that preceded it | FAB-source classification | Explicit Need present before offer? |
|---|---|---|---|---|---|
| 1 | "..." | Price concern / Value doubt / Early-call resistance | "..." | Feature / Advantage / Premature solution | Yes (quote it) / No |

---

### Step 3: Identify the Behavioral Pattern

**ACTION:** Scan the Step 2 table for patterns across all objections. Name the dominant seller behavior driving objections for this call or deal.

**WHY:** Individual objection sources tell you what happened moment-to-moment. The pattern tells you what behavior to change systematically. A rep with 5 Advantage-sourced objections has a different problem than one with 5 Feature-sourced price concerns. The pattern determines the prevention prescription.

**Common patterns and their implications:**

- **Majority of objections are price concerns** → Dominant behavior: Feature overuse. The seller is describing the product heavily without developing needs first. The customer is primed to scrutinize cost. Prevention: cut Features; shift to Problem and Implication Questions.
- **Majority are value doubts ("not worth it," "don't need it")** → Dominant behavior: Advantages before Explicit Needs. The seller is presenting capabilities before the customer feels the problem's importance. Prevention: stop presenting capabilities until Implication Questions have made the problem consequential and Need-payoff Questions have elicited the customer's own expression of wanting a solution.
- **Objections cluster in the first half of the call** → Dominant behavior: premature solution presentation. The seller is mentioning the product or capabilities before establishing the customer's problems and their consequences. Prevention: no solution mentions until at least the midpoint of the call, after thorough need development.
- **Objections appear despite good questioning early on** → May indicate a true objection (product gap or competitor advantage) rather than a seller-caused objection. Note this — true objections require honest gap acknowledgment, not prevention.

**Step 3 output:** A 2-3 sentence behavioral diagnosis naming the dominant pattern and its implication for prevention.

---

### Step 4: Produce the Prevention Plan

**ACTION:** Write a concrete, ranked prevention plan for the next call. Address what to stop doing and what to do instead. Recommend invoking `spin-discovery-question-planner` if need development is identified as the gap.

**WHY:** Diagnosis without prescription is incomplete. The seller needs to know specifically which behaviors to change and what to replace them with. The plan must be concrete enough to use as a pre-call brief — not abstract coaching ("build more value") but specific behavioral guidance ("do not present any product capability until you have asked at least two Implication Questions per problem area").

**Prevention plan format:**

**Behaviors to remove from the next call:**
- [Specific behavior, e.g.: "Do not list product Features in the opening 20 minutes of the call"]
- [Specific behavior, e.g.: "Do not present any capability before the customer has expressed a specific want in their own words"]
- [Specific behavior, e.g.: "Do not mention pricing until needs are fully developed and customer has expressed at least one Explicit Need"]

**Behaviors to add:**
- [e.g.: "Ask at least 2 Problem Questions before any capability mention"]
- [e.g.: "For each Implied Need expressed, ask at least 1 Implication Question to develop the consequence before moving forward"]
- [e.g.: "Use Need-payoff Questions ('If we could eliminate that, what would that mean for your team?') to get the customer to articulate their own want before presenting the solution"]

**SPIN question development gaps** (for each objection that traces to an undeveloped need):
- [Problem: what problem question was missing or too shallow]
- [Implication: what consequence was not explored]
- [Need-payoff: what customer-expressed want needs to be elicited before presenting this capability]

**Recommended next step:** IF the pattern shows systemic need-development gaps → invoke `spin-discovery-question-planner` with this deal context to build a targeted question bank before the next call.

**Step 4 output:** Written prevention plan with ranked behaviors and SPIN question gaps.

---

### Step 5: Write the Objection Prevention Plan

**ACTION:** Compile Steps 1-4 into a single structured document. Write it to `objection-prevention-plan-{deal}.md`.

**WHY:** The written plan persists across the conversation and can be used directly as pre-call preparation. It also creates a reference point for tracking whether the prevention behaviors are adopted in the next call.

**Report structure:**

```
# Objection Prevention Plan — {Deal Name} — {Date}

## Objections Extracted
{Numbered list from Step 1}

## Objection-to-Source Mapping
{Table from Step 2}

## Behavioral Diagnosis
{Pattern summary from Step 3}

## Prevention Plan
### Behaviors to Remove
{List from Step 4}

### Behaviors to Add
{List from Step 4}

### SPIN Question Gaps
{Per-gap items from Step 4}

## Recommended Next Step
{Invoke spin-discovery-question-planner or other specific action}
```

## Key Principles

- **Objections are seller-caused, not customer-caused.** Rackham's analysis of 35,000+ calls found that in a typical sales team, one rep receives 10x more objections per selling hour than another rep selling the same product to the same customers. The product is not the variable. The seller's behavior is. Objections cluster around sellers who use Advantages heavily — and they drop by 55% when those sellers are trained to develop Explicit Needs first.

- **Symptoms versus causes.** Price objections are not a price problem — they are a Feature-use problem. "Not worth it" objections are not a value communication problem — they are a need-development problem. Objection-handling training treats the symptom. This skill treats the cause. Teaching a seller to handle price objections when their Feature overuse is generating them is as effective as eating ice cream to prevent typhoid.

- **The Advantage trap.** The most common objection source is not poor product knowledge or bad closing technique. It is Advantages — showing how the product can help before the customer has expressed a want for that help. The customer evaluates the Advantage against an undeveloped problem and concludes it is not worth the cost. This is the Dallas word-processor pattern: every Advantage met with an objection, because the seller jumped to solution before building value.

- **Objection prevention is upstream, not downstream.** The question "how do I handle this objection?" is downstream. The right question is "what did I do 5 minutes ago that generated this objection?" This skill answers the right question.

- **Some objections are true objections.** Not every objection is seller-caused. If the customer has a genuine need your product cannot meet, or if a competitor has a clear advantage, those objections are real. Prevention techniques cannot eliminate true objections — only seller-caused ones. Approximately 55% of objections in a typical sales team can be prevented through better sequencing. The other 45% require honest acknowledgment and, where possible, product-level responses.

- **Never produce handling scripts.** If a seller asks "how do I respond to this objection?" — the first answer is always the prevention diagnosis. If after understanding the cause they still need help with a specific true objection, refer them to the appropriate resource. But producing a response script for a seller-caused objection is counterproductive: it makes the seller more confident about a behavior that is hurting them.

## Examples

**Scenario: AE with a deal accumulating price objections**

Trigger: AE says "We keep getting price objections on this deal. The customer is very price-sensitive. How do I handle it?"

Process:
- (Step 1) Read `call-notes-2025-03-12.md`. Extract 4 objections: "That's very expensive for what it does," "I'm not sure we can justify this cost," "Is there a cheaper version?", "The budget is tight — this is hard to sell internally."
- (Step 2) Examine seller statements immediately preceding each. Find: seller opened with a 5-minute product overview listing 8 product Features (processing speed, storage capacity, integration count, API options, support tier, uptime SLA, security certifications, deployment options). No Problem Questions asked in the first 15 minutes. Classify: Feature-heavy opening → price concerns.
- (Step 3) Pattern: All 4 objections are price concerns. Dominant behavior: Feature overuse before any need development. The customer's price sensitivity was amplified by the Feature dump, which primed them to ask "is this worth the cost?" before having any sense of what the cost of NOT solving their problem would be.
- (Step 4) Prevention plan: Remove the product overview from the first 15 minutes. Replace with 3-4 Problem Questions about the customer's current workflow and where they're losing time or quality. Add Implication Questions for each confirmed problem. Before any product mention, elicit at least one Explicit Need.
- (Step 5) Write `objection-prevention-plan-acme-corp.md`.

Output: Prevention plan showing that price sensitivity is seller-amplified (Feature dump), not inherent customer resistance. Recommendation: invoke `spin-discovery-question-planner` to build a question bank before the next call.

---

**Scenario: Sales manager reviewing a rep's call with repeated "not worth it" objections**

Trigger: Manager says: "Listen to this transcript — the prospect keeps saying it's not worth switching. What's going on?"

Process:
- (Step 1) Extract 3 objections from transcript: "We're really quite happy with our current system," "I don't see enough value to justify a switch," "It'd be a lot of hassle for marginal improvement."
- (Step 2) Find seller statements before each. All three are Advantages: "Our system would eliminate that manual reconciliation for you," "You'd get real-time visibility across all your accounts," "We integrate directly so there's no import step." Scan for prior customer-expressed Explicit Needs: buyer mentioned "our reconciliation takes longer than it should" (Implied Need — problem statement, not a want). No Explicit Need expressed before any Advantage was offered.
- (Step 3) Pattern: All 3 objections are value doubts. Dominant behavior: Advantages offered before Explicit Needs developed. The rep heard an Implied Need and jumped to the solution. The customer hasn't internalized the cost of the problem, so the solution seems unnecessary.
- (Step 4) Prevention: Rep should have used Implication Questions to develop the reconciliation problem ("What does that extra time cost you across 50 accounts per month?" "What happens when a reconciliation error reaches a client?") and then Need-payoff Questions to get the customer to express the want ("If reconciliation were automatic, what would you do with that time?"). Only after explicit want is expressed should the capability be presented.

Output: `objection-prevention-plan-prospect-review.md`. Coaching for manager: the rep has the Advantage habit — trained to give "Benefits" but actually giving Advantages. Recommend fab-statement-classifier audit of rep's standard pitch and then spin-discovery-question-planner session for this account.

---

**Scenario: Early-call objection pattern**

Trigger: AE says "The prospect shut down the conversation almost immediately — I barely got through my intro before they were resistant."

Process:
- (Step 1) Extract: "Look, I'm not sure I need to hear a whole pitch right now," "We're not really in the market for new tools this quarter," "Our budget is locked."
- (Step 2) Seller statement before first objection: "We help companies like yours cut their invoice processing time by up to 40% with our workflow automation platform." This is an opening benefit statement — a premature Advantage in the first 2 minutes of the call.
- (Step 3) Pattern: Early-call objections caused by premature solution presentation (opening benefit/Advantage statement).
- (Step 4) Prevention: Do not mention the product, its capabilities, or any value claims in the first third of the call. Open by establishing the right to ask questions. Use Problem Questions first. The customer needs to feel invested in the problem before hearing about the solution.

Output: Prevention plan showing this is a classic premature-solution pattern. Recommend `discovery-call-opening-planner` for the next call to redesign the opening.

## References

- [objection-source-causal-map.md](references/objection-source-causal-map.md) — Full behavior→response chain with research evidence, the Dallas word-processor dialogue annotated by objection source, and the Japanese-recruit case study

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill depends on:
- `clawhub install bookforge-fab-statement-classifier` — Classify seller statements as Features, Advantages, or Benefits; provides the FAB definitions and behavior→response chain that underpin objection diagnosis

Skills that work alongside this one:
- `clawhub install bookforge-spin-discovery-question-planner` — Build a SPIN question bank for the next call, addressing the specific need-development gaps identified by this diagnosis
- `clawhub install bookforge-benefit-statement-drafter` — Draft Benefit statements once Explicit Needs have been developed; the constructive step after removing Advantage-heavy selling
- `clawhub install bookforge-discovery-call-opening-planner` — Redesign the call opening when early-call objections indicate premature solution presentation

Or install the full SPIN Selling skill set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
