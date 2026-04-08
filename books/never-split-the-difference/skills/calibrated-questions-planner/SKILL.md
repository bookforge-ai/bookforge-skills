---
name: calibrated-questions-planner
description: |
  Generate a bank of open-ended strategic questions (how/what questions) for a negotiation, sales conversation, difficult discussion, or conflict situation. Use when someone asks "what questions should I ask in my negotiation?", "how do I get more information without seeming pushy?", "how do I find out who else is involved in this decision?", "what should I ask to understand their constraints?", or "how do I stop the other side from stonewalling me?" Also use for: designing interview questions that reveal unstated priorities, discovering hidden stakeholders who could kill a deal, identifying deal-breaking issues before they surface, uncovering the real decision-making process behind a stated position, or preparing questions for any high-stakes conversation where you need the other party to think and talk. Produces a situation-specific question bank organized by category (value-revealing, behind-the-table stakeholder, deal-killing issue), with follow-up label templates and deployment sequencing. Works for sales calls, job negotiations, vendor negotiations, partnership discussions, client discovery, conflict resolution, and any scenario where understanding the counterpart's full picture is critical. Pair with accusation-audit-generator (to defuse objections before asking) and commitment-verifier (to verify answers reveal real commitment).
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/never-split-the-difference/skills/calibrated-questions-planner
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
depends-on: []
source-books:
  - id: never-split-the-difference
    title: "Never Split the Difference: Negotiating as if Your Life Depended on It"
    authors: ["Chris Voss"]
    chapters: [7, 8, 23]
tags: [negotiation, questions, open-ended-questions, stakeholder-discovery, deal-killers, how-what-questions, active-listening, information-gathering, sales, conflict-resolution, strategic-questions, decision-makers, hidden-constraints]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Situation brief describing the negotiation, deal, or conversation — what you want, who is involved, what you know about their position and constraints"
    - type: document
      description: "Goals and constraints — your target outcome, your walk-away point, any known constraints on either side"
    - type: document
      description: "Stakeholder map (optional) — known decision-makers and influencers, especially those not directly at the table"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment. Works with pasted briefs or document files."
discovery:
  goal: "Produce a situation-specific bank of open-ended strategic questions that shift problem-solving to the counterpart, reveal hidden constraints and stakeholders, and uncover deal-killing issues before they surface"
  tasks:
    - "Analyze the situation to identify information gaps and unknown constraints"
    - "Generate 5-8 how/what questions organized across three categories"
    - "Map behind-the-table stakeholders and generate questions to surface them"
    - "Identify likely deal-killing issues and generate diagnostic questions"
    - "Produce follow-up label templates for each question"
    - "Sequence the questions into deployment groups of 2-3"
  audience:
    roles: ["salesperson", "founder", "manager", "consultant", "recruiter", "procurement", "negotiator", "account-executive", "product-manager"]
    experience: "beginner to intermediate — no negotiation training required"
  triggers:
    - "User is preparing for a negotiation, sales call, or difficult conversation and needs questions to ask"
    - "User is stuck and needs the other party to think about solutions rather than just objecting"
    - "User needs to find out who else is involved in the decision without being confrontational"
    - "User wants to uncover hidden constraints, budget limits, or approval requirements"
    - "User needs to diagnose whether a deal-killing issue exists before it surfaces too late"
    - "User wants to avoid yes/no questions that shut down conversation"
  not_for:
    - "Generating the full negotiation preparation document — use negotiation-one-sheet-generator for the complete 5-section prep"
    - "Designing price negotiation offers — use ackerman-bargaining-planner"
    - "Verifying whether the counterpart's yes is genuine — use commitment-verifier"
    - "Defusing hostility before questions can land — use accusation-audit-generator first"
  quality: placeholder
---

# Calibrated Questions Planner

## When to Use

You are preparing for a negotiation, sales conversation, discovery call, partnership discussion, or any high-stakes conversation where you need to understand the full picture on the other side — their priorities, constraints, decision process, and the stakeholders who are not in the room.

You want to ask questions that make the counterpart think and talk, rather than questions they can deflect with a yes or no. You need information without seeming demanding. You may also need to surface hidden stakeholders or deal-blocking issues before they derail the deal.

**Input this skill needs:** A situation brief (what the deal is, who is involved, what you know so far) and your goals. If you have a stakeholder map or conversation history, include them.

**Do not use this skill if:** You need to write a complete negotiation plan — use `negotiation-one-sheet-generator`. You need to handle an accusatory or hostile counterpart before questions can land — run `accusation-audit-generator` first to defuse the situation.

---

## Context & Input Gathering

### Required
- **The situation:** What is the negotiation or conversation? (Deal type, stakes, industry context)
- **What you want:** Your target outcome. Be specific — vague goals produce vague questions.
- **What you know about the other side:** Their stated position, what they've said they want, any known constraints.

### Important
- **Who is visible at the table:** The person(s) you are directly speaking with and their role.
- **What you don't know:** Information gaps — what you suspect exists but haven't confirmed (budget, authority, timeline, competing priorities, internal politics).

### Observable (tell the skill what you can observe)
- **Their communication style so far:** Are they forthcoming? Evasive? Technical? Relationship-focused?
- **Any signals of constraint:** Have they said things like "I need to check with someone," "that's not something I can decide," or "we have some internal considerations"?

### Defaults (used if not provided)
- **Stakeholder map:** Assume at least one decision-maker exists who is not present in the conversation.
- **Deal-killing issues:** Assume budget approval, authority limits, and internal alignment are all potentially unresolved unless confirmed.

### Sufficiency check
If you have the situation, your goal, and at least one known information gap, proceed. Missing stakeholder map or conversation history is acceptable — the skill will generate exploratory questions to fill these gaps.

---

## Process

### Step 1: Identify the Information Gaps

**Action:** Read the situation brief and list 4-6 specific things you do not know but need to know to reach your goal. Organize them into three buckets:
- (A) What does this situation actually mean to them — their real priorities and what success looks like for their side?
- (B) Who else is involved in making or blocking this decision?
- (C) What issues could kill this deal that have not been raised yet?

**WHY:** Open-ended strategic questions must be targeted at real unknowns, not asked generically. A question that reveals something you already know wastes conversation time. A question that hits a genuine unknown produces information you can act on. Mapping unknowns first prevents generic question generation and ensures every question has a purpose.

**IF** you have a stakeholder map → cross-check it: identify any decision-makers not confirmed as participants in the conversation.
**IF** you have conversation history → scan for deflections, vague answers, or mentions of "internal" considerations — these signal bucket B and C unknowns.
**IF** you have nothing → default to all three buckets as unknown territory.

---

### Step 2: Generate Bucket A — Value-Revealing Questions

**Action:** Write 2-3 open-ended how/what questions that surface what this situation means to the counterpart — their priorities, what they value most, and what a successful outcome looks like on their side.

**WHY:** You cannot negotiate effectively toward the counterpart's real interests unless you know what they are. Stated positions ("we need a 20% discount") often conceal real interests ("we need to hit budget before Q3 close"). Questions that make the counterpart articulate their own success criteria reveal negotiating room that a pure price-focused approach misses. Phrasing as "how" or "what" — not "why" — keeps the question open without triggering defensiveness. "Why" sounds accusatory; "what" and "how" sound collaborative.

**Question starters to use:**
- "What does success look like for you here?"
- "How does this fit into what you're trying to accomplish?"
- "What matters most to you in how this gets resolved?"
- "What would need to happen for this to work for your side?"
- "How will you know this was the right decision?"

**Constraint:** Every question must start with "how" or "what." Never "why." Never a closed yes/no question.

---

### Step 3: Generate Bucket B — Behind-the-Table Stakeholder Questions

**Action:** Write 2-3 questions that surface decision-makers, approvers, and deal-killers who are not visibly present in the conversation.

**WHY:** In most organizational negotiations, the person across the table is rarely the only person whose approval matters. Budget owners, legal teams, senior executives, technical reviewers, and implementation teams can all veto a deal from off-stage. Discovering these stakeholders before the final negotiation moment — when they would otherwise appear as a surprise "we need to check with..." — lets you address their concerns proactively. Asking about the team's perspective rather than demanding to speak to the boss keeps the question collaborative, not threatening.

**Ready-to-use questions (adapt as needed):**
- "How does this affect the rest of your team?"
- "What do the people not on this call see as their main concerns?"
- "How on board are the colleagues who aren't part of this conversation?"
- "What does your [manager/board/legal team] need to see to feel comfortable with this?"
- "Who else will be involved in making this final?"

**IF** you already know the decision structure → tailor questions to specific roles (e.g., "What does your CFO need to see?").
**IF** you do not know the decision structure → use the broadest versions to surface the structure first.

---

### Step 4: Generate Bucket C — Deal-Killing Issue Discovery Questions

**Action:** Write 1-2 questions that surface potential deal-blocking issues — budget constraints, approval limits, timing problems, competing priorities, or internal resistance — before they appear as a final objection.

**WHY:** Deal-killing issues that surface at the end of a negotiation, when you believe agreement is close, are far more damaging than issues surfaced early. A budget problem discovered in week one can be worked around; the same problem discovered in week eight, after both sides have invested time and built commitment, often causes the deal to collapse with hard feelings. Questions that invite the counterpart to raise potential problems early signal collaborative intent and protect both sides from wasted effort.

**Ready-to-use questions (adapt as needed):**
- "What could get in the way of this moving forward?"
- "What are the biggest obstacles you see on your side?"
- "How does this fit with your current priorities and budget cycle?"
- "What would make this impossible to approve?"
- "What concerns do you have that we haven't addressed yet?"

---

### Step 5: Add Follow-Up Label Templates

**Action:** For each question, write a follow-up label — a "It seems like..." or "It sounds like..." statement to use after the counterpart answers, before asking the next question.

**WHY:** A question without a follow-up creates a rapid-fire interrogation feeling. After the counterpart answers, pausing to reflect their answer back as a label — "It seems like the timeline pressure is the real constraint here" — demonstrates that you heard them, builds rapport, and often prompts deeper elaboration without requiring another question. Labels after answers are as important as the questions themselves.

**Label template format:**
```
After [Question]: "It seems like [paraphrase of what they said or implied]..."
```

**IF** you don't yet know what they'll say → write a label template with a blank: "It seems like [X] is the real concern here..." — fill in X after you hear their answer.

---

### Step 6: Sequence into Deployment Groups

**Action:** Organize the full question bank into groups of 2-3, ordered from rapport-building to deal-diagnostic. Indicate which group to ask first, second, and third.

**WHY:** Asking multiple questions in sequence without pausing for answers overwhelms the counterpart and signals an interrogation rather than a conversation. Grouping into 2-3 question sets with natural breaks — where you use a label or summary before continuing — keeps the pacing conversational. Starting with value-revealing questions (bucket A) builds understanding and rapport before surfacing potential problems (bucket C). This sequencing also ensures that if the conversation is cut short, you've gathered the most important information first.

**Deployment order:**
1. Group 1: 2 Bucket A questions (value-revealing) + labels
2. Group 2: 2 Bucket B questions (stakeholder discovery) + labels
3. Group 3: 1-2 Bucket C questions (deal-killer discovery) + labels

**IF** the relationship is new → open with the most rapport-friendly bucket A question.
**IF** the relationship is established → you can move to bucket B earlier.

---

### Step 7: Write the Output Artifact

**Action:** Write `calibrated-questions.md` with all questions organized by category, numbered, with follow-up label templates and deployment group markers.

**WHY:** A written document that the user can refer to during the conversation prevents forgetting key questions under pressure, allows adaptation in real time, and creates a record for post-conversation analysis. The format (numbered, categorized, with labels) mirrors how the questions should be deployed — it is not just a list but a deployment script.

**Output format:** See Outputs section below.

---

## Inputs / Outputs

### Inputs
- Situation brief (required)
- Your goals and constraints (required)
- Stakeholder map (optional)
- Conversation history (optional)

### Outputs

**File:** `calibrated-questions.md`

**Template:**

```markdown
# Calibrated Questions: [Situation Name]

**Prepared for:** [Your name / role]
**Counterpart:** [Name / role / organization]
**Goal:** [Your target outcome in one sentence]

---

## Deployment Group 1 — Value-Revealing Questions
*Ask these first. Pause and label after each answer before asking the next.*

**Q1.** [Question — starts with How or What]
→ Follow-up label: "It seems like [blank]..."

**Q2.** [Question — starts with How or What]
→ Follow-up label: "It sounds like [blank]..."

---

## Deployment Group 2 — Behind-the-Table Stakeholder Questions
*Ask these after establishing understanding. Listen for signs of hidden approvers.*

**Q3.** [Question about team or colleagues]
→ Follow-up label: "It seems like [blank] has a stake in this..."

**Q4.** [Question about who else is involved]
→ Follow-up label: "It sounds like there are people not in this conversation who matter..."

---

## Deployment Group 3 — Deal-Killing Issue Discovery
*Ask these once rapport is established. Surface problems now, not at the end.*

**Q5.** [Question about obstacles or concerns]
→ Follow-up label: "It seems like [blank] could be the real challenge here..."

**Q6.** [Optional: question about internal constraints or approvals]
→ Follow-up label: "It sounds like [blank] is what would make this hard to move forward..."

---

## Anti-Patterns to Avoid During the Conversation

- Do not ask "Why" questions — they trigger defensiveness. Every "Why" question contains an implicit accusation. "Why did you choose that vendor?" sounds like "Justify your decision." Rewrite: "What led you to choose that vendor?" — same information, zero accusation. The shift from "Why" to "What/How" removes the judgment while preserving the inquiry.
- Do not ask multiple questions without pausing for the answer
- Do not ask yes/no questions when you need understanding
- Do not skip the label after the answer — it signals you heard them

---

## Notes
[Space for observations made during the conversation]
```

---

## Key Principles

**How and What questions shift the problem-solving burden.** When you ask "How am I supposed to do that?" after a counterpart makes an unreasonable demand, you are not accepting the demand or outright rejecting it — you are returning the problem to them. They must now think about how to solve a problem they created. This shifts mental effort and often produces creative solutions you would never have discovered by presenting your own counter-proposal immediately. "How am I supposed to do that?" is the single most powerful calibrated question in negotiation: instead of arguing against the counterpart's position, you ask them to solve your constraint. This forces them to consider your perspective and often leads them to propose a solution that works for both sides. At Harvard, this single question defeated two negotiation professors in a mock hostage scenario.

**WHY:** The counterpart works harder on a problem they were invited to solve than one they were handed. When people create solutions, they feel ownership over those solutions — making them far more likely to follow through than if you had suggested the same solution yourself.

**"Why" is an accusation in disguise.** Even well-intentioned "why" questions — "Why is that a problem for you?" — activate defensiveness because they implicitly challenge the counterpart's judgment or motives. "What" and "how" questions ask the counterpart to describe rather than justify, which keeps them in a collaborative frame.

**WHY:** "Why" forces the counterpart to defend a position, which causes them to entrench it. "What" and "how" invite the counterpart to explain a situation, which often reveals more information and opens more options.

**Behind-the-table stakeholders are the most common deal-killers.** In organizational negotiations, the person you are talking to almost never has full authority. Budget owners, legal counsel, senior executives, and technical approvers all have veto power and are frequently not in the conversation. Discovering them early through collaborative questions prevents the "I need to check with someone" surprise that kills deals in their final hours.

**WHY:** A counterpart who says "I need to check with my boss" at the final stage is not being evasive — they may genuinely lack authority. But discovering this in hour one versus hour forty saves enormous time and effort on both sides and allows you to design the conversation to address the hidden stakeholders' concerns proactively.

**Questions in groups of 2-3 with labels in between.** Never ask a string of questions without pausing to acknowledge the answer. Each answer deserves a label — a reflection of what you heard — before the next question. This sequencing signals that you are listening, not interrogating, and often produces more complete answers than the next question would have generated.

**WHY:** Labels after answers serve two functions: they confirm understanding (reducing misinterpretation risk) and they create a moment of feeling heard, which makes the counterpart more willing to continue sharing. An interrogation-style rapid-fire sequence closes people off; a listen-label-question rhythm opens them.

**Calibrated questions create the illusion of control — and that illusion is the point.** Solutions the counterpart proposes themselves are implemented at far higher rates than solutions imposed on them. Calibrated questions work because they create the illusion of control — the counterpart believes the answer was their idea. This ownership effect means they will fight harder to implement "their" solution than to comply with yours.

**WHY:** When people feel they arrived at a decision through their own reasoning, they commit to it. When they feel a solution was handed to them, they comply at best — and resist at worst. Calibrated questions engineer the conditions for the counterpart to reach your preferred conclusion on their own terms.

**Surface deal-killers early, not late.** Asking "What could get in the way of this?" in the first conversation feels collaborative and signals you care about making the deal work. Discovering the same obstacle in week eight, after both parties have invested time and emotion, triggers frustration and often derails deals that could have been saved with early awareness.

**WHY:** Early discovery of problems gives both sides time to problem-solve. Late discovery, after commitment has built, creates loss — both parties feel like they are losing something, and loss aversion makes that hurt more than the deal was worth. Early questions protect both sides from this dynamic.

---

## Examples

### Example 1: Enterprise Software Sales — Uncovering Hidden Budget Constraints

**Scenario:** An account executive is closing a $120K annual contract. The prospect's main contact (a VP of Operations) has been enthusiastic throughout three months of evaluation. Two days before the expected close, the VP says "we need a bit more time." The executive suspects a budget approval issue but has not confirmed it.

**Trigger:** "What questions should I ask to find out what's really going on without being pushy?"

**Process:**
- Step 1: Gaps — unknown whether VP has budget authority, unknown who else must approve, unknown whether there's a competing priority or budget freeze
- Step 2: Bucket A — "What does success look like for your organization if this goes live in Q1?"
- Step 3: Bucket B — "What does your finance team or CFO need to see before something like this moves forward?" / "How on board are the colleagues who haven't been part of our conversations?"
- Step 4: Bucket C — "What could get in the way of moving forward by end of quarter?" / "What would make this impossible to approve right now?"
- Steps 5-6: Sequence — start with bucket A to rebuild rapport, then bucket B to surface the approval process, then bucket C to name the obstacle directly

**Output:** `calibrated-questions.md` with 6 questions across 3 groups, each with a follow-up label template. The bucket C question ("What would make this impossible to approve right now?") surfaces the budget freeze directly, allowing the executive to offer flexible payment terms rather than losing the deal.

---

### Example 2: Salary Negotiation — Discovering Real Constraints and Decision Structure

**Scenario:** A candidate is negotiating a job offer. The recruiter has offered $115K. The candidate's target is $130K. The recruiter says "that's the top of the band." The candidate does not know whether this is a firm limit or an opening position, or who has authority to go above the band.

**Trigger:** "How do I find out if there's any real flexibility without ruining the relationship?"

**Process:**
- Step 1: Gaps — unknown whether band is truly fixed or negotiable, unknown who has authority to approve exceptions, unknown what the full package looks like (equity, bonus, title)
- Step 2: Bucket A — "What does the full compensation picture look like at this level?" / "How does the company think about the tradeoff between base and total compensation?"
- Step 3: Bucket B — "What would need to happen for an exception to the band to be considered?" / "How does a decision like that typically get made?"
- Step 4: Bucket C — "What would make this offer impossible to adjust?" 
- Steps 5-6: Sequence — open with bucket A (expands the conversation beyond base salary, may reveal equity or bonus levers), then bucket B to understand decision process, save bucket C as a last probe

**Output:** `calibrated-questions.md` with 5 questions. The bucket B question ("What would need to happen for an exception to be considered?") reveals that the hiring manager can approve exceptions with VP sign-off — and the recruiter offers to make that call.

---

### Example 3: Partnership Negotiation — Surfacing Deal-Killing Misalignment Early

**Scenario:** A startup founder is negotiating a distribution partnership with a large retail chain. After two months of discussion, both sides appear aligned. The founder is about to present final terms and suspects there may be exclusivity requirements from the retailer's side that would conflict with other distribution agreements — but nothing has been said.

**Trigger:** "Before I present final terms, what questions should I ask to make sure there are no surprises?"

**Process:**
- Step 1: Gaps — unknown whether retailer requires exclusivity, unknown who in the retailer's organization must approve the deal, unknown whether procurement or legal has different requirements than the business development contact
- Step 2: Bucket A — "What does a successful partnership look like for your team 12 months from now?" / "What matters most to your organization in how this gets structured?"
- Step 3: Bucket B — "Who else in your organization will be involved in finalizing this?" / "What does your legal or procurement team typically need to review?"
- Step 4: Bucket C — "What would make this structure impossible for your side to agree to?" / "What concerns do you have that we haven't discussed?"
- Steps 5-6: Sequence — start with bucket A to reinforce shared vision, move to bucket B to surface legal and procurement review (rather than discovering it after terms are presented), use bucket C to explicitly invite deal-killing issues to the surface now

**Output:** `calibrated-questions.md` with 6 questions. The bucket C question surfaces the retailer's exclusivity requirement before final terms are presented, allowing both sides to redesign the agreement structure rather than walking away after a failed close.

---

## References

| File | Contents |
|------|----------|
| `references/question-bank.md` | Full library of 15+ ready-to-use calibrated questions across all three categories; anti-pattern reference table; "why" vs "how/what" rewrites for common questions; follow-up label templates; deployment sequencing guide; Harvard mock hostage case study breakdown |

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Never Split the Difference: Negotiating as if Your Life Depended on It by Chris Voss.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
