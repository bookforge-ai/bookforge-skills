---
name: benefit-statement-drafter
description: "Draft Benefit statements that link product capabilities to specific customer-expressed Explicit Needs. Use this skill when preparing follow-up emails, proposals, or demos after a discovery call, when someone asks 'how should I frame our solution for this customer?', 'draft Rackham-style benefits for my proposal', 'write the value section of my deck', 'the customer said X — what should I say back?', 'help me write benefits for this deal', 'turn our capabilities into benefits for this account', or 'I have a needs log — help me write the customer-facing statements'. This skill REFUSES to draft a Benefit when no matching Explicit Need exists in the customer record — it redirects to spin-discovery-question-planner instead. That refusal is not a flaw; it is the skill's core protection against the most common error in B2B sales: presenting capabilities before needs are confirmed. The output is a short, grounded set of draft statements (one per matched pair) that the user can adapt into a proposal section, a follow-up email, or a demo opening. Also applies the new-product-launch sub-flow: when the user is launching a new product and has no needs log yet, the skill shifts focus to problem identification and need development before drafting any Benefits — the approach that produced 54% higher sales in a controlled medical diagnostics experiment. Applies to B2B account executives, solutions consultants, and founder-led sellers preparing for follow-up conversations after discovery calls."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/benefit-statement-drafter
metadata: {"openclaw":{"emoji":"✍️","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [5]
tags: [sales, b2b-sales, enterprise-sales, fab-methodology, benefit-statements, proposal-writing, spin-methodology, capability-presentation, new-product-launch]
depends-on:
  - fab-statement-classifier
  - spin-discovery-question-planner
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "needs-log.md — Explicit Needs the customer has expressed, ideally produced by need-type-classifier after discovery calls"
    - type: document
      description: "product-capabilities.md — the seller's product capabilities (what problems it solves, what it can and cannot deliver)"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Document set: needs-log.md, product-capabilities.md. Agent produces benefit-statements-{deal}.md. Human reviews, adapts, and incorporates into proposals, emails, or demos."
discovery:
  goal: "Produce one draft Benefit statement per matched (Explicit Need, capability) pair — and refuse to produce statements where no matching Explicit Need exists"
  tasks:
    - "Read needs-log.md and extract only the Explicit Needs (not Implied Needs)"
    - "Match each Explicit Need to a capability in product-capabilities.md"
    - "Draft one Benefit statement per matched pair"
    - "Flag Explicit Needs with no capability match (coverage gaps)"
    - "Refuse to draft Benefits for unmatched capabilities and redirect to spin-discovery-question-planner"
    - "Apply new-product-launch sub-flow when no needs log exists"
  audience:
    roles: [account-executive, solutions-consultant, enterprise-sales-rep, founder-led-seller]
    experience: intermediate
  when_to_use:
    triggers:
      - "After a discovery call — customer has expressed Explicit Needs and the seller wants to frame the solution"
      - "Preparing a follow-up email, proposal section, or demo opening"
      - "The user has a needs-log.md from need-type-classifier with confirmed Explicit Needs"
      - "Preparing to present at the Demonstrating Capability stage of the sales call"
    prerequisites:
      - "At least one Explicit Need in needs-log.md — the skill will refuse to draft if no Explicit Needs are present"
      - "product-capabilities.md describing what the product can solve"
    not_for:
      - "Auditing existing sales content for FAB distribution (use fab-statement-classifier)"
      - "Generating discovery questions (use spin-discovery-question-planner)"
      - "Pricing or packaging decisions"
      - "Writing complete proposals or emails (this skill produces statement-level drafts to incorporate into longer content)"
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
      - "Refuses to draft a Benefit for a capability with no matching Explicit Need in the customer record"
      - "Distinguishes Explicit Needs from Implied Needs in the needs-log and acts only on the former"
      - "Flags capability gaps (Explicit Needs the product cannot meet)"
      - "Applies problem-first framing for new product launches rather than feature dumping"
    what_baseline_misses:
      - "Produces aspirational capability claims without checking whether the customer has expressed a need"
      - "Treats Implied Needs (problems, difficulties) as sufficient anchors for Benefit statements"
      - "Does not distinguish capabilities from needs — produces a feature dump labeled 'Benefits'"
      - "Has no concept of capability gap analysis"
---

# Benefit Statement Drafter

## When to Use

You have completed a discovery call or series of calls. The customer has expressed specific Explicit Needs (wants, desires, or intentions — not just problems). You have product capabilities that can meet some of those needs. Now you need to draft the statements that link your capabilities to what the customer actually said they want.

This skill drafts one Benefit statement per matched (Explicit Need, capability) pair. Each statement follows a simple structure: the customer stated they need X; our product delivers X in this way.

**Use this skill when:**
- Preparing a follow-up email after a discovery call where Explicit Needs were surfaced
- Writing the value section of a proposal or deck for a specific account
- Drafting a demo opening that references what the customer told you they needed
- Moving from "here's what our product does" to "here's why it matters for this customer"

**Critical gate:** This skill requires a `needs-log.md` with at least one confirmed Explicit Need. If you ask this skill to draft Benefits before Explicit Needs exist, it will decline and redirect you to `spin-discovery-question-planner` to develop needs first. This is intentional — Rackham's 5,000-call study found that statements meeting Explicit Needs (true Benefits) are strongly linked to call success, while statements showing how a product can help (Advantages) have no statistically significant relationship to success in large sales.

**Do NOT use this skill to:** audit existing sales content (use `fab-statement-classifier`), generate discovery questions (use `spin-discovery-question-planner`), or write full proposals or emails (this skill produces statement-level drafts you incorporate into longer content).

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Needs log with Explicit Needs:** The customer-expressed wants or intentions from prior discovery
  -> Check environment for: `needs-log.md` (ideally produced by `need-type-classifier`)
  -> If missing, ask: "Do you have a needs log or notes from the discovery call? What specific needs did the customer say they wanted to solve?"
  -> If the user provides only Implied Needs (problems, difficulties): **apply the Refusal Protocol** in Step 2

- **Product capabilities:** What the seller's product can actually deliver
  -> Check environment for: `product-capabilities.md`
  -> If missing, ask: "What capabilities does your product offer? What problems does it solve, and what can it NOT do?"

### Observable Context (gather from environment)

- **Deal context:** Account name, deal stage, contact role
  -> Look for: `deal-brief.md`
  -> If absent: proceed with needs log alone; name the output generically

- **New product flag:** Is the user launching a product so new that no needs log exists yet?
  -> Signal: user says "we're launching X" or "there's no needs log yet — we just got this product"
  -> If flagged: apply the **New-Product-Launch Sub-flow** in Step 3 before any drafting

### Sufficiency Threshold

SUFFICIENT: needs-log.md with at least one Explicit Need + product-capabilities.md
PARTIAL: needs-log.md with only Implied Needs → apply Refusal Protocol, redirect to discovery
NEW PRODUCT: no needs log, new product → apply New-Product-Launch Sub-flow
MUST ASK: no needs information AND no new-product context

## Process

### Step 1: Extract Explicit Needs from the Needs Log

**ACTION:** Read `needs-log.md` (or the user-provided notes). Separate Explicit Needs from Implied Needs. List only the Explicit Needs — these are the valid anchors for Benefit drafting.

**WHY:** The single most important distinction in this skill is between Implied Needs and Explicit Needs. Implied Needs are statements of problem, difficulty, or dissatisfaction: "Our reporting takes too long," "We struggle with operator turnover." Explicit Needs are statements of want, desire, or intention: "We need to cut reporting time to one day," "We want a system our operators can learn in a week." Only Explicit Needs anchor a true Benefit. Using an Implied Need as the anchor produces an Advantage — a statement that shows how the product can help but does not meet a confirmed customer want. Advantages have no statistically significant relationship to success in large sales (Rackham, 5,000-call study).

**Classification test:**
- Explicit Need: customer used words like "we need," "we want," "we're looking for," "I'd like," "our goal is," "it's important that we have" → valid anchor
- Implied Need: customer said "we struggle with," "it's a problem when," "we're not happy with," "it takes too long" → NOT a valid anchor for Benefits; needs development first

**Step 1 output:** Two lists:
1. Confirmed Explicit Needs (with customer's words quoted or paraphrased)
2. Implied Needs present (noted for Step 2 — the refusal check)

### Step 2: Apply the Refusal Protocol

**ACTION:** For each capability in `product-capabilities.md`, check whether a matching Explicit Need exists in the Step 1 output. If a capability has no matching Explicit Need, do NOT draft a Benefit for it.

**WHY:** The default behavior of any language model given a product spec is to produce aspirational statements: "Our solution drives 30% productivity gains for teams like yours." These are Advantages at best — they claim value the customer has not asked for. In large sales (Huthwaite's analysis of 18,000+ calls), presenting capabilities to unconfirmed needs causes customers to evaluate whether the stated value is worth the cost. Their answer, in large-sale contexts, is often "not worth it" — generating value objections. Refusing to draft unanchored Benefits is the primary protection against this pattern.

**REFUSAL PROTOCOL:**

If the needs log contains ONLY Implied Needs (no Explicit Needs):

> STOP. No Explicit Needs are documented in the needs log. This skill drafts Benefits only when the customer has expressed a specific want or desire. What you have are Implied Needs — problems or difficulties the customer mentioned. These are valuable, but they are not yet ready to anchor a Benefit statement.
>
> **What to do instead:** Run `spin-discovery-question-planner` to plan Implication and Need-payoff Questions that develop these Implied Needs into Explicit Needs on the next call. Once the customer has expressed a confirmed want, return here to draft the Benefits.

If the needs log contains some Explicit Needs and some unmatched capabilities:

> Note: [Capability X] has no matching Explicit Need in the current record. No Benefit will be drafted for it. If you want to develop a need for this capability, use `spin-discovery-question-planner` to plan the appropriate Need-payoff Question sequence.

**Step 2 output:** A mapping table:

| Capability | Explicit Need Present? | Action |
|---|---|---|
| [Capability A] | Yes — "[customer's words]" | Draft Benefit |
| [Capability B] | No | Refused — redirect to discovery |
| [Capability C] | Yes — "[customer's words]" | Draft Benefit |

### Step 3: New-Product-Launch Sub-flow (if applicable)

**ACTIVATE WHEN:** The user is launching a new product and has no `needs-log.md` — or explicitly says "we just got this product, I haven't run discovery yet."

**WHY:** When a product is new, salespeople tend to shift from need-development to feature presentation. Rackham's Huthwaite research tracked this behavior: during new-product launches, salespeople give more than 3 times the level of Features and Advantages compared to when selling established products. This "bells-and-whistles" approach consistently underperforms. In a controlled medical diagnostics experiment, a group launched with the conventional feature-dump approach was outsold by 54% by a group that received no product demonstration at all — only a list of the problems the machine solved and the SPIN questions to develop those problems with customers. The 54%-higher group's attention was on customer needs, not product features.

**New-Product-Launch Sub-flow:**

**Step 3a — Identify problems the product solves:**
Ask the user (or read the product documentation): "What specific problems is this product designed to solve? What are the pain points it was built for?"
Output: A list of 3-6 problem types the product addresses.

**Step 3b — Map problems to likely customer types:**
For each problem, identify which customer roles or segments are most likely to experience it. This determines who to target in discovery.

**Step 3c — Plan the discovery-first approach:**
Produce a brief plan: "Before drafting any Benefits, run discovery on these accounts using questions that surface these problem types. When customers confirm they have these problems AND express a want for the solution, return to this skill to draft the Benefits."
Point the user to `spin-discovery-question-planner` with the problem list as input.

**Step 3d — Draft provisional benefit templates (clearly labeled PROVISIONAL):**
Draft one placeholder Benefit statement per problem type — clearly marked as PROVISIONAL and not to be used until the customer has expressed the matching Explicit Need in their own words. These are targeting templates, not presentation-ready statements.

**Step 3 output:** Problem list + discovery plan + PROVISIONAL benefit templates with explicit instruction not to use them until Explicit Needs are confirmed on a call.

### Step 4: Draft the Benefit Statements

**ACTION:** For each matched (Explicit Need, capability) pair from Step 2, draft one Benefit statement. Each statement has three components: what the customer said they need, what the product delivers, and how that delivery meets the stated need.

**WHY:** A Benefit statement structured this way gives the seller something they can deliver verbatim or adapt. It also serves as an internal proof: if the seller cannot fill in "what the customer said they need," the statement is an Advantage, not a Benefit. The three-component structure enforces this check and makes the drafts auditable.

**Benefit statement structure:**
```
EXPLICIT NEED: "[Customer's words — their want or desire]"
CAPABILITY: [What the product delivers]
BENEFIT STATEMENT: "You mentioned that [restate the customer's need in their words].
  [Product/feature] does [X], which means [that specific need is met in this way]."
```

**Drafting guidelines:**
- Use the customer's language, not your marketing language
- Keep each statement to 1-3 sentences — it is a draft building block, not a paragraph
- Do not chain multiple Explicit Needs into one statement; one pair per statement
- Avoid aspirational embellishment ("and this will transform your business") — stay grounded in the specific need expressed
- If the customer quantified their need ("we need to cut close time from 5 days to 2"), include the customer's number, not a generic claim

**Step 4 output:** Numbered list of draft Benefit statements, each labeled with the Explicit Need it meets and the capability it draws on.

### Step 5: Coverage Gap Analysis

**ACTION:** List any Explicit Needs in the needs log that no capability in `product-capabilities.md` can meet. Flag these clearly.

**WHY:** Capability gaps discovered now, before the follow-up meeting, are far less damaging than gaps discovered mid-presentation. An AE who goes into a proposal knowing there is one unmet need can plan for it: acknowledge the gap honestly, redirect to what is covered, or explore whether a partner integration addresses it. An AE who discovers the gap live gives the customer the impression of poor preparation — which erodes trust at the moment it matters most.

**Coverage gap format:**
> CAPABILITY GAP: The customer expressed a need for [X]. Our current product capabilities do not cover this. Do not draft a Benefit for this need. Recommended action: [acknowledge honestly in the meeting / explore partnership / check product roadmap / confirm this is out of scope].

**Step 5 output:** Coverage gap list (may be empty).

### Step 6: Write the Output File

**ACTION:** Compile the Benefit statements, coverage gaps, and any refusals into a single file: `benefit-statements-{deal}.md`. Include a short summary table at the top.

**WHY:** A written artifact carries forward. The AE reads it before the follow-up meeting, pastes appropriate statements into the proposal, and uses the summary table to confirm coverage. The file also feeds `commitment-and-advance-planner` for the Four Successful Actions step ("summarize Benefits before proposing commitment").

**Output file structure:**
```
# Benefit Statements — {Deal/Account Name} — {Date}

## Coverage Summary
| Explicit Need | Capability | Benefit Drafted? |
|---|---|---|
| [Need 1] | [Capability A] | Yes |
| [Need 2] | [none] | GAP — no capability match |
| [Implied Need 3] | n/a | REFUSED — Implied Need only |

## Draft Benefit Statements

### Benefit 1 — [Short label, e.g., "Monthly close time"]
EXPLICIT NEED: "[Customer's words]"
BENEFIT STATEMENT: "[Draft text]"

### Benefit 2 — [Short label]
...

## Coverage Gaps
{If any: description and recommended action per gap}

## Refused Statements
{If any: list capabilities with no Explicit Need match, with redirect to spin-discovery-question-planner}

## Recommended Next Step
{One paragraph: how to use these statements — e.g., incorporate into proposal section, use in demo opening, include in follow-up email summary}
```

## Key Principles

- **No Explicit Need, no Benefit.** Rackham's research is unambiguous: statements that meet Explicit Needs are strongly correlated with orders and advances in large sales; statements showing how a product can help (Advantages) have no statistically significant relationship to large-sale success. This skill enforces that distinction by refusing to draft Benefits where no Explicit Need is recorded.

- **The customer's words are the anchor.** The correct structure of a Benefit statement begins with what the customer said, not with what the seller wants to say. If you cannot quote or closely paraphrase the customer's expressed want, you do not have the material to write a Benefit. You have the material to write an Advantage — which is a step backward.

- **Implied Needs are not sufficient.** A customer who said "our reporting takes too long" has expressed an Implied Need — a dissatisfaction. That is valuable for discovery (it is the foundation for Implication questioning). But it does not authorize a Benefit statement. The customer has not yet said they want or need a faster reporting solution. Until they do, any capability statement you make about your reporting product is an Advantage, not a Benefit.

- **Develop first, then benefit.** Rackham's principle: "Do a good job of developing Explicit Needs and the Benefits almost look after themselves." If you are returning here and finding few or no Explicit Needs in the log, the right response is not to lower the standard — it is to plan better discovery for the next call.

- **New products demand problem-first thinking.** The impulse to communicate a new product by listing its features and advantages ("bells and whistles") is understandable — it is exactly how product marketing communicates internally. Resist it. Identify the problems the product solves, develop those problems into Explicit Needs through SPIN questioning, and then draft Benefits. This sequence produced 54% higher sales in a controlled experiment compared to the conventional feature-led approach.

- **Benefits are building blocks.** The output of this skill is statement-level drafts, not finished proposals or emails. The AE's job is to select the relevant Benefits, sequence them appropriately for the communication channel, and write the connective tissue. This skill does not write the entire follow-up email; it writes the core statements that give the email its substance.

- **Stay within scope.** Do not audit existing content (use `fab-statement-classifier`). Do not generate discovery questions (use `spin-discovery-question-planner`). When a gap appears or a refusal fires, name the right skill to handle it.

## Examples

**Scenario: Follow-up email after a discovery call with confirmed Explicit Needs**

Trigger: AE says — "I had a great call with a VP of Finance. My needs-log shows she said 'we need to cut our monthly close from 7 days to 2 days' and 'we need a single dashboard all three regional controllers can see.' Help me draft the Benefits for my follow-up email."

Process:
- (Step 1) Read needs-log.md: Two Explicit Needs confirmed: "cut close from 7 to 2 days" and "single dashboard for three regions."
- (Step 2) Match to product-capabilities.md: Automated close workflow matches Need 1. Unified multi-entity dashboard matches Need 2. No gaps.
- (Step 4) Draft Benefit 1: "You mentioned you need to cut monthly close from 7 days to 2. Our automated close workflow runs the period-end reconciliation and approval chain in parallel rather than sequentially, which is how clients in your situation have reduced their close to 1-3 days." Draft Benefit 2: "You said you need a single dashboard your three regional controllers can all see. Our multi-entity view consolidates all three regions into one real-time view with role-based access — each controller sees the same live data, and you see the consolidated view above them."
- (Step 6) Write benefit-statements-vp-finance-acme.md.

Output: Two grounded Benefit statements ready to be pasted into the follow-up email, anchored to the customer's own words. No aspirational claims.

---

**Scenario: Refusal — only Implied Needs in the record**

Trigger: AE says — "I have a call transcript. The customer mentioned they're frustrated with their current system and said approvals take forever. Help me write Benefits."

Process:
- (Step 1) Read the transcript: "frustrated with current system" = Implied Need. "approvals take forever" = Implied Need. No Explicit Needs (no "we need," "we want," "we're looking for").
- (Step 2) **Refusal Protocol fires:** No Explicit Needs present.

Output:
> STOP. The customer has expressed problems and frustrations (Implied Needs) but has not yet stated what they want or need. This skill cannot draft Benefits without confirmed Explicit Needs — drafting now would produce Advantages, which have no statistically significant relationship to large-sale success.
>
> Run `spin-discovery-question-planner` before your next call. Input: the Implied Needs above. The planner will build Implication Questions to develop these into felt problems, and Need-payoff Questions to get the customer to articulate the want. Once they do, return here with the updated needs log.

---

**Scenario: New product launch**

Trigger: Solutions consultant says — "We just launched a new security monitoring tool. We don't have any customer conversations yet. How do I use Benefits with this product?"

Process:
- (Step 3) New-Product-Launch Sub-flow activates.
- (Step 3a) Ask: "What problems is this tool designed to solve?" User provides: insider threat detection, compliance audit trail, real-time alert on anomalous access.
- (Step 3b) Map to likely customer types: security directors, compliance officers, CISOs in regulated industries.
- (Step 3c) Draft discovery plan: "Before presenting any capabilities, plan Problem → Implication → Need-payoff question chains for each of these three problems. Use `spin-discovery-question-planner` with this problem list. Only after customers have expressed wants related to these problems should you draft Benefits."
- (Step 3d) Draft three PROVISIONAL benefit templates, labeled clearly: "PROVISIONAL — do not use until customer has confirmed this need."

Output: `benefit-statements-new-security-tool-provisional.md` — problem list, discovery plan, three provisional templates with explicit instruction to develop needs first.

## References

- [new-product-launch-sub-flow.md](references/new-product-launch-sub-flow.md) — The problem-first approach, the +54% Kodak/medical diagnostics experiment details, and step-by-step launch planning workflow

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill depends on:
- `clawhub install bookforge-fab-statement-classifier` — Classify existing seller statements as Features, Advantages, or true Benefits (defines the Benefit standard this skill enforces)
- `clawhub install bookforge-spin-discovery-question-planner` — Plan SPIN questions to develop Implied Needs into Explicit Needs before drafting Benefits

Skills that build on this one:
- `clawhub install bookforge-commitment-and-advance-planner` — The Four Successful Actions for obtaining commitment include "summarize Benefits" — use this skill's output as the Benefits input to that step
- `clawhub install bookforge-objection-source-diagnoser` — If Benefits generate objections, diagnose whether the root cause is Advantage overuse or premature capability demonstration

Or install the full SPIN Selling skill set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
