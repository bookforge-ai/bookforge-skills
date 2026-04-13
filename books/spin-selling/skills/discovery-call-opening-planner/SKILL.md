---
name: discovery-call-opening-planner
description: "Plan a discovery call opening that earns the right to ask questions — without leading with product details or personal rapport fishing. Use this skill whenever a B2B rep is preparing for a sales call and needs to know what to say in the first 60-90 seconds, when someone asks 'how should I open this call?', 'what should I say first in my meeting with [company]?', 'how do I start a discovery call with a senior executive?', 'draft an opening for my call tomorrow', 'what's the best way to open a follow-up call?', or 'how do I avoid the awkward opener?'. This skill applies Rackham's empirically-validated framework for call openings in major sales: establish who you are, state why you're there (without product details), and earn the buyer's consent to ask questions. It explicitly prevents the two conventionally taught but research-debunked patterns: personal rapport fishing ('talk about the yacht photo on their wall') and opening benefit statements ('I'm here to show you how X saves you 30%'). Output is a call-prep script and checkpoint review the rep can read 5 minutes before the meeting. Invoke whenever any sales call opening needs to be planned, scripted, reviewed, or adapted to a specific call context."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/spin-selling/skills/discovery-call-opening-planner
metadata: {"openclaw":{"emoji":"🎤","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: spin-selling
    title: "SPIN Selling"
    authors: ["Neil Rackham"]
    chapters: [7]
domain: b2b-sales
tags: [sales, b2b-sales, enterprise-sales, discovery, call-opening, spin-methodology, call-preparation, meeting-prep]
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "Deal brief or call context: account name, contact name/role, call objective, whether this is a new account or follow-up. A deal-brief.md file is ideal; a brief verbal description is sufficient."
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Document set: deal-brief.md, account-research.md, previous call-notes (if follow-up). Agent produces call-opening-{date}.md. Human delivers the opening."
discovery:
  goal: "Produce a 60-90 second opening script that establishes who you are, why you're there (without product details), and earns the buyer's consent to ask questions — avoiding the two debunked conventional patterns"
  tasks:
    - "Draft a 60-90 second opening script for a specific call (new account, follow-up, senior buyer, multi-stakeholder)"
    - "Apply the 3-point objective framework: who I am / why I'm here / right to ask questions"
    - "Review an existing opening plan against the 3 structural checkpoints"
    - "Adapt a generic opening to a specific buyer role (C-suite, procurement, technical buyer)"
    - "Identify whether a planned opening falls into the two debunked patterns and replace it"
  audience:
    roles: [account-executive, enterprise-sales-rep, sdr, solutions-consultant, founder-led-seller]
    experience: intermediate
  when_to_use:
    triggers:
      - "Rep is preparing for a first meeting with a new account"
      - "Rep is preparing for a follow-up call and wants to open purposefully rather than just recapping last time"
      - "Rep is meeting a senior executive and unsure how to open without wasting their time"
      - "Rep has been taught to open with rapport-building or benefit statements and wants an evidence-based alternative"
      - "Manager is coaching a rep on call openings"
    prerequisites: []
    not_for:
      - "The SPIN questions themselves (use spin-discovery-question-planner)"
      - "Deciding what advance to target at end of the call (use commitment-and-advance-planner)"
      - "Cold outreach or prospecting (this skill assumes the meeting is already booked)"
      - "Demo or proposal scripting"
      - "Negotiation tactics (see Never Split the Difference skills)"
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
      - "Output that opens with product/solution details rather than earning permission to ask questions"
      - "Personal rapport fishing (family photo, sports trophy, weekend small talk)"
      - "Opening benefit statements that trap the seller into product details before needs are established"
      - "Openings that spend more than 20% of estimated call time on pleasantries"
    what_baseline_misses:
      - "Recommends personal rapport (family, sports, shared interests) as an opening tactic"
      - "Recommends 'hook them with a benefit' as an opening technique"
      - "Does not establish the seller's role as questioner / investigator before discovery begins"
      - "Does not account for buyer seniority, new vs follow-up context, or multi-stakeholder dynamics"
---

# Discovery Call Opening Planner

## When to Use

You are preparing for a B2B sales call — first meeting or follow-up — and need a concrete plan for the first 60-90 seconds. You want to open in a way that earns the buyer's engagement and consent to be asked questions, rather than launching into product details or small talk.

This skill is for major sales contexts: high-value deals, multiple stakeholders, long cycles. If you are running a transactional or retail sale, the opening matters less and conventional techniques may suffice.

Use this skill:
- Before any discovery call to prepare a purposeful, crisp opening
- When adapting your opening for a senior executive, procurement buyer, or technical evaluator
- When coaching a rep whose calls stall because the buyer takes over the questioning role immediately
- When you have been trained to open with benefit statements or rapport-building and want a research-backed alternative

Do NOT use this skill to plan the SPIN questions themselves (use `spin-discovery-question-planner`), to decide what advance to target at end of the call (use `commitment-and-advance-planner`), or to script a cold outreach.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Account and contact:** Who is this call with? Company name, contact name, their role/seniority.
  -> Check for: `deal-brief.md` (company, contact, deal size, stage)
  -> If missing, ask: "Who is the call with — company name, contact name, and their role?"

- **Call type:** Is this a first meeting with a new account, or a follow-up with an existing contact?
  -> Check for: `deal-brief.md` deal stage, or previous `call-notes-{date}.md`
  -> If missing, ask: "Is this your first meeting with this person, or have you spoken before?"

- **Call objective:** What do you need to accomplish? What would constitute a successful advance from this call?
  -> Check for: `deal-brief.md` objective field, or `next-call-plan.md`
  -> If missing, ask: "What's the goal of this call? What specific outcome would make it a success?"

### Observable Context (gather from environment)

- **Buyer seniority:** C-suite, VP, director, manager, technical buyer, procurement
  -> Read from `deal-brief.md` or `stakeholder-map.md`
  -> Senior buyers are more time-sensitive; the opening must get to business even faster
- **Previous call notes:** What was discussed last time? Any commitments made?
  -> Look for `call-notes-{date}.md` — reference the last agreed topic or question to re-establish context in a follow-up
- **Multi-stakeholder situation:** Are there multiple people on this call?
  -> Look for `stakeholder-map.md` — if so, the opening must address the group, not just one person

### Default Assumptions

- Default to treating this as a large sale requiring careful opening. Overshooting rigor costs little; under-preparing costs deals.
- Default to first-meeting format if call type is ambiguous — it is the more constrained case.

### Sufficiency Threshold

SUFFICIENT: Account/contact name + call type (new vs follow-up) + call objective
PROCEED WITH DEFAULTS: Objective unknown — assume "earn the right to ask discovery questions"
MUST ASK: No account or contact information at all

## Process

### Step 1: Gather and Confirm Call Context

**ACTION:** Read the available context files (`deal-brief.md`, `account-research.md`, previous call notes if follow-up). Confirm the four context variables: (1) buyer name and role, (2) call type, (3) call objective, (4) buyer seniority level. If any are missing, ask before proceeding.

**WHY:** The opening script is a short, high-leverage piece of communication. Every word is visible to the buyer. An opening drafted without knowing whether you're speaking to a VP of Engineering vs a procurement manager, or whether this is a first call or a fourth, will feel generic and erode trust. Senior buyers in particular read imprecision as wasted time.

### Step 2: Check for the Two Debunked Patterns

**ACTION:** Before drafting, check whether any existing opening notes, phrases, or habits from the user contain either of the two patterns that research shows do NOT improve major-sale call success:

**Pattern 1 — Personal rapport fishing:** Opening by referencing something from the buyer's personal life (family photos, sports trophies, hobbies, weekend activities) to build relationship before getting to business.

**Pattern 2 — Opening benefit statement:** Opening with a statement about what your product can do for the buyer ("I'm here to show you how X reduces your costs by Y%") before any needs have been established.

**WHY:** Both patterns are explicitly taught by conventional sales training and both are debunked by Rackham's research. Personal rapport fishing fails for two reasons: in large urban/enterprise accounts (vs small rural accounts), there is no relationship between personal references and sales success; and senior professional buyers often resent it. The BP buyer's yacht-photo example illustrates the trap — a professional buyer kept a yacht photo specifically to waste the time of reps who fished for personal openers, responding "I hate sailing. What did you want to see me about?" Opening benefit statements fail because they trigger the buyer to ask product questions before you have established any needs — the seller gets drawn into product details, pricing, and objections before they have earned the right to ask a single discovery question.

**IF** the user's existing plan contains either pattern -> flag it explicitly and replace it in Step 4.
**ELSE** -> proceed to Step 3.

### Step 3: Apply the 3-Point Opening Objective

**ACTION:** Structure the opening around the three objectives Rackham's research identifies for effective call openings in large sales:

1. **Who you are** — Establish your name and role clearly. In follow-up calls, briefly re-establish who you are and what your company does if the buyer may not remember from a previous call (especially true with senior executives who have many vendor conversations).

2. **Why you're there** — State the purpose of this call in terms of what you want to learn or understand, NOT in terms of what your product does. The purpose framing should be investigative, not promotional. "I'd like to understand how you're currently handling X and whether there are areas where we might be relevant" — not "I'm here to show you how we can solve Y."

3. **Right to ask questions** — Explicitly or implicitly earn the buyer's consent to be in the asking role. This is the pivot that gets you into the Investigating stage. The buyer should leave the opening understanding that you are going to ask them questions — not that you are about to deliver a presentation.

**WHY:** These three objectives form the minimum functional unit of a call opening in major sales. The goal of the Preliminaries stage is simply to get the customer's consent to move to the Investigating stage — nothing more. The common mistake is treating the opening as an opportunity to make an impression or establish credibility through product knowledge. The opening is not the place for that. The durable impression is made during the Investigating stage, when the quality of your questions demonstrates competence.

### Step 4: Draft the Opening Script

**ACTION:** Write a 60-90 second opening script (approximately 120-180 words when spoken at a normal pace) tailored to the specific call context. Format as a draft the user can read, internalize, and adapt — not a rigid script to be read verbatim.

**Adapt based on call type:**

**New account / first meeting:**
```
"[Name], thanks for making the time. I'm [Your Name] from [Company] — [one sentence: what your company does at the category level, not product level]. The reason I wanted to speak is [framing as a question or area to explore, not a pitch]. Before I tell you more about what we do, I'd find it really useful to understand [your situation / how you currently approach X / what's on your plate in this area]. Would it be OK if I asked you a few questions first?"
```

**Follow-up call (existing contact):**
```
"[Name], thanks for picking this back up. Last time we talked, you mentioned [brief reference to the most relevant thing from previous notes — 1 sentence]. I've been thinking about what you said about [X], and I'd like to understand [area to explore further]. Before I go into anything on our side, could I ask a few more questions to make sure I'm thinking about this correctly?"
```

**Senior executive (C-suite, VP):**
- Compress the opening further. Get to the investigative framing in one sentence.
- Avoid any preamble about your company history, market position, or product roadmap.
- State that you will be brief and ask focused questions: "I only need 20 minutes and most of it I'd like to spend asking you questions rather than talking about us — is that alright?"

**Multi-stakeholder (multiple people on the call):**
- Open by briefly acknowledging the group composition: "I know we have [role A], [role B], and [role C] on this call — that's helpful because I want to understand [X] from multiple angles."
- Establish your questioning role for the group, not just one person.
- Avoid opening by addressing only one person in the room.

**WHY:** The script must be tailored because the opening's function — establishing permission to ask questions — is delivered differently depending on the buyer's seniority and the call's relationship history. A first-meeting C-suite opening that spends 30 seconds on company background will lose the executive before you get to the question. A follow-up call that does not reference the last conversation treats the buyer as a stranger and wastes the accumulated context.

### Step 5: Apply the 3 Pre-Call Checkpoints

**ACTION:** Review the drafted opening against the three checkpoints drawn from Rackham's effective-opening criteria. Each checkpoint is a yes/no test.

**Checkpoint 1: Get to business within 20% of call time**
- Estimate the total call length. Calculate 20% (e.g., 40-minute call → 8 minutes max for opening).
- Does the opening script complete in well under that threshold?
- Typical target: opening completes in 60-90 seconds for a 40-minute call (< 4% of call time).
- IF the opening script runs longer than 3 minutes when read aloud -> trim. The complaint Rackham documented consistently from senior executives and professional buyers is that salespeople waste time with idle chatter. There is no recorded complaint that a seller got down to business too quickly.

**Checkpoint 2: No solutions or product details in the first half of the call**
- Does the opening mention any product name, feature, benefit, capability, or case study?
- IF yes -> remove it. The opening must NOT introduce solutions before needs have been established.
- Does the opening leave a clear path for you to ask questions before you discuss your product?
- IF the buyer could reasonably leave the opening asking "so what does your product do?" and you have not answered that yet -> pass. IF you have answered it -> revise.

**Checkpoint 3: Role as questioner is established**
- Does the opening make it clear — explicitly or by strong implication — that you are going to ask the buyer questions, and that the buyer's information matters before you say anything about your product?
- IF not clear -> add a single explicit line: "Before I tell you anything about what we do, I'd like to ask you a few questions about how you're currently handling X."

**WHY:** These three checkpoints reflect Rackham's three guidance points for effective Preliminaries. Checkpoint 1 prevents the time-drain pattern that frustrates senior buyers. Checkpoint 2 is the primary structural guard against premature solution presentation — one of the highest-correlation behaviors with call failure in large sales. Checkpoint 3 is the mechanism by which you maintain the questioning role; without explicitly establishing it, buyers often step into that role themselves, asking about your product before you have gathered any needs.

### Step 6: Produce the Call Opening Plan

**ACTION:** Write the final call-prep document to `call-opening-{YYYY-MM-DD}.md`. The document should be scannable in 2-3 minutes before the call.

**Document format:**

```markdown
# Call Opening Plan — {Account Name} — {Date}

## Call Context
- Contact: {Name}, {Role}
- Call type: {New account / Follow-up}
- Objective: {What this call needs to accomplish}
- Estimated length: {X} minutes

## Anti-Pattern Check
- [ ] No personal rapport fishing in this opening
- [ ] No opening benefit statements in this opening

## Opening Script (~60-90 seconds)
{Tailored script from Step 4}

## 3 Checkpoints
- [ ] Get to business within 20% of call time (~{X} minutes for this call)
- [ ] No product/solution details in first half of call
- [ ] Buyer understands I will be asking questions before I pitch

## If It Goes Off-Script
{One sentence: if the buyer jumps immediately to "what does your product do?" — how to redirect back to the questioning role}
```

**WHY:** A written plan creates an artifact the user can review 5 minutes before the call. The checklist format makes the anti-pattern guards fast to verify. The "if it goes off-script" note prepares for the most common opening disruption: the buyer who asks about your product before you have asked a single question.

## Key Principles

- **The goal of the opening is permission, not impression.** The Preliminaries stage has one functional purpose in a major sale: get the buyer's consent to answer your questions. Trying to also establish credibility, build rapport, or plant a compelling vision in the opening is overloading it. The impression that matters is made during the Investigating stage, when the quality of your questions signals your understanding of the buyer's world.

- **First impressions in large sales are less important than most sales training claims.** Rackham's research found no reliable relationship between opening smoothness and call success in major sales. Successful calls start awkwardly; well-polished openings lead nowhere. The experienced observation from hundreds of observed calls: "I no longer believe that first impressions can make or break your sales success in larger sales." The call's trajectory is set by the quality of investigation, not by the opening.

- **Personal rapport fishing has a measurable ceiling.** The Imperial Group rural/urban study found that personal references correlate with sales success in small rural accounts (where reps had long tenure and buyers had time) but show no relationship in large urban accounts. The dynamic has also shifted: where buyers once said "I buy from Fred because I like him," they now say "I like Fred, but I buy from his competition because they're cheaper." Personal loyalty is no longer an adequate commercial basis. The BP buyer's yacht-photo technique — designed specifically to deflect rapport-fishing openers — illustrates the professional buyer's response to this tactic.

- **Opening benefit statements hand control to the buyer.** When you open with "we help companies like yours reduce costs by X%," you invite the buyer to ask "what does that cost?" and "how does it work?" — before you have established any needs. You are now answering questions about your product rather than asking questions about their situation. The seller in Rackham's example (the Executype typewriter scenario) starts by establishing a product benefit, gets pulled into pricing within 30 seconds, and has lost the questioning role before the call has begun.

- **Variety matters more than technique in multi-call sales.** Rackham's research found that less effective sellers opened every call the same way. More effective sellers varied their openings. If you have used the same opening benefit statement with the same buyer twice in a row, it has already shifted from a positive to an irritant — as illustrated by the office products rep whose second visit with the identical opener drew visible annoyance from the same executive who had praised it a week earlier.

- **Get to business quickly; you will not offend anyone.** Rackham noted that senior executives and professional buyers consistently complain about sellers who dwell on non-business topics before getting to the point. He recorded zero complaints from buyers about sellers who moved too quickly to business. The asymmetry is decisive: you can only lose time by dwelling; you lose nothing by moving briskly.

## Examples

**Scenario 1: First meeting with a new account, mid-level manager**

Trigger: Rep is preparing a first discovery call with the Director of Operations at a mid-sized manufacturing company. The rep has a deal brief but no prior relationship.

What a baseline agent typically produces:
> "Hi Sarah, great to meet you! I saw from your LinkedIn that you were at [previous company] — I know some people there. How's the team been treating you since you joined? [... 3 minutes of small talk ...] Anyway, I'm here today because our platform has helped companies like yours reduce operational downtime by 30-40%, which I know is always top of mind for ops teams. Does that sound like something that would be relevant to you?"

Why this fails Checkpoint 2 and 3: Opens with personal rapport fishing (LinkedIn connection bait), then launches into an opening benefit statement ("reduce downtime by 30-40%"). The buyer is now in the asking role: "How do you do that? What does it cost? Who else have you worked with?" The seller has lost the questioning role and introduced product details before understanding a single need.

What this skill produces:
> "Sarah, thank you for the time. I'm [Name] from [Company] — we work with manufacturing teams on operational reliability. The reason I wanted to speak is that I've been hearing from a number of ops directors that the way they manage [area] has been changing significantly, and I'm genuinely curious whether you're seeing the same thing. Before I tell you anything about what we do, I'd like to ask you a few questions about how you're currently handling [relevant area] — would that be OK?"

Checkpoint review:
- Completes in ~30 seconds (well under 20% of a 45-minute call)
- No product features, benefits, or case studies mentioned
- "Before I tell you anything about what we do, I'd like to ask you a few questions" — questioning role explicitly established

---

**Scenario 2: Follow-up call with a VP who has attended one previous call**

Trigger: Rep is returning to a VP of Finance after an initial meeting where the VP raised concerns about their month-end close process. The rep wants to continue discovery.

What a baseline agent typically produces:
> "Thanks for having me back. Last time we had a great conversation about your finance operations. I wanted to follow up and also share some slides on how our platform handles month-end consolidation. I think you'll find it really relevant to what you described."

Why this fails Checkpoint 2: Immediately introduces product ("slides on how our platform handles month-end consolidation") before re-establishing the questioning role. The call is about to become a presentation, not a discovery session — even though the rep has not yet fully understood the scope of the problem or whether there is an Explicit Need.

What this skill produces:
> "Alex, good to pick this back up. Last time you mentioned the month-end close was taking longer than it should and there were reconciliation issues across the regional entities. I've been thinking about that — I'd like to understand that a bit more before I tell you anything about what we do. Specifically, I want to understand what the downstream effects look like when the close runs late. Could I ask you a few questions on that before we go into anything on our side?"

Checkpoint review:
- References prior context (establishes continuity, not a restart)
- Opens with a desire to understand, not to present
- "Before I tell you anything about what we do" — questioning role explicitly re-established
- "I want to understand the downstream effects" — frames toward Implication territory without revealing it

---

**Scenario 3: C-suite meeting, 20-minute slot, senior stakeholder new to the deal**

Trigger: Rep is joining a call where the CFO is attending for the first time. Two previous calls were with the VP of IT. The CFO has 20 minutes and is known to be direct.

What a baseline agent typically produces:
> "Thank you for joining us. I know your time is valuable, so I'll start with why we think we're uniquely positioned to help a company at your scale. We've worked with [reference company] and [reference company 2], and in both cases we were able to deliver [benefit statement]. I'd love to show you a few slides and then we can take questions."

Why this fails all three checkpoints: Starts with a product/capability claim, references case studies before understanding any CFO-specific needs, and immediately moves toward a presentation — the seller has become the answerer, not the questioner.

What this skill produces:
> "[Name], thanks for joining — I know your time is short. We've been having productive conversations with [IT VP name]. I wanted to meet you briefly because any decision of this scale obviously has a financial and risk dimension that I want to understand from your perspective. I have three questions for you; they should take about 15 minutes. Does that work?"

Checkpoint review:
- Opens in under 15 seconds
- Acknowledges relationship history (prior calls) without over-explaining
- No product claims, benefits, or case studies
- "I have three questions for you" — questioning role established immediately and explicitly
- Respects time constraint by naming it directly

## References

For an opening-template library with variants by call type (new account, follow-up, C-suite, multi-stakeholder, procurement buyer), see [references/opening-templates.md](references/opening-templates.md).

For an anti-pattern catalog with detection criteria and replacement phrases, see [references/opening-anti-patterns.md](references/opening-anti-patterns.md).

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — SPIN Selling by Neil Rackham.

## Related BookForge Skills

This skill is standalone. Skills that follow in the call sequence:

- `clawhub install bookforge-spin-discovery-question-planner` — Plan the SPIN questions for the Investigating stage (reads the call context this opening has established)
- `clawhub install bookforge-commitment-and-advance-planner` — Plan the specific advance to target at the end of the call (depends on call-outcome-classifier)
- `clawhub install bookforge-need-type-classifier` — Classify what the buyer says during discovery as Implied or Explicit Needs

Or install the full SPIN Selling skill set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
