---
name: question-importance-prioritizer
description: Prioritize which assumptions to validate first and produce focused learning goals before customer conversations — classifying risks as product risk versus market risk. Use this skill whenever the user has many assumptions or unknowns and needs to decide which to test first, wants to identify the 3 most important learning goals for their next conversation batch, needs to figure out what the riskiest parts of their business idea are, wants to separate must-validate assumptions from safe ones, is preparing strategic learning goals but not the specific interview questions, or suspects they are avoiding the scary questions that actually matter — even if they don't mention "prioritization" or "learning goals." Do NOT use this skill to write or rewrite the actual conversation questions (use conversation-question-designer) or to analyze notes from a completed conversation (use conversation-data-quality-analyzer).
version: 1
status: verified
source-books:
  - id: the-mom-test
    title: "The Mom Test"
    authors: ["Rob Fitzpatrick"]
    chapters: [3]
domain: customer-discovery
tags: [customer-discovery, question-prioritization, learning-goals, risk-classification, pre-conversation-planning]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Product idea description and list of assumptions or unknowns to validate"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Any agent environment with file read/write access."
---

# Question Importance Prioritizer

## When to Use

You need to decide what to learn before customer conversations — not just which questions pass quality rules, but which questions actually matter for your business survival. Typical situations:

- The user has many assumptions to validate and needs to prioritize which 3 to focus on next
- The user is preparing for a batch of customer conversations and needs focused learning goals
- The user has been having conversations but feels stuck because they are asking safe, comfortable questions
- The user needs to determine whether their biggest risks can even be validated through conversations (product risk vs market risk)
- The user wants to identify the "scary questions" they have been avoiding
- The user has a long list of unknowns and does not know where to start

Before starting, verify:
- Does the user have a product idea or business concept? (If not, this skill cannot help yet)
- Does the user have at least a rough sense of who their customers might be? (Different customer types need different learning goals)

**Mode: Hybrid** — The agent produces the prioritized learning goals and prepared questions. The human conducts the actual conversations.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product idea or business concept:** What is the user building or exploring? This is the foundation for identifying risks and learning goals.
  - Check prompt for: product descriptions, startup ideas, feature concepts, problem statements
  - Check environment for: `product-idea.md`, `README.md`, pitch documents
  - If still missing, ask: "What product or business idea are you working on? A few sentences describing what it does and who it is for."

- **Assumptions or unknowns to validate:** What does the user believe but has not yet proven? This is the raw material for prioritization.
  - Check prompt for: hypotheses, assumptions lists, "I think...", "I believe...", "I assume...", risk lists
  - Check environment for: `learning-log.md`, `assumptions.md`, previous conversation notes
  - If still missing, ask: "What are the key assumptions your business depends on? List everything you believe to be true but have not yet validated — about your customers, the problem, the market, pricing, distribution, anything."

### Observable Context (gather from environment)

- **Customer segment:** Who is the user targeting? Different segments need different learning goals.
  - Look for: `customer-segments.md`, persona descriptions, target market references
  - If unavailable: ask "Who are your target customers? Be as specific as you can."

- **Current stage:** How far along is the user? Pre-idea, pre-product, has a prototype, has paying customers?
  - Look for: references to prototypes, MVPs, revenue, launch dates
  - If unavailable: assume pre-product (exploring the problem space)

- **Previous conversation learnings:** What has already been validated or invalidated?
  - Look for: `conversation-notes/`, `learning-log.md`
  - If unavailable: assume first round of conversations

### Default Assumptions

- If no customer type specified, design learning goals generic enough for early exploration but note this limitation
- If no stage specified, assume pre-product (learning phase)
- If no prior conversations, assume all assumptions are unvalidated

### Sufficiency Threshold

```
SUFFICIENT when ALL of these are true:
- Product idea or business concept is known
- At least 3 assumptions or unknowns are identified
- Customer type is known or defaulted

PROCEED WITH DEFAULTS when:
- Product idea is known but assumptions are vague ("I'm not sure what I don't know")
- Customer type is approximate ("probably restaurant owners")

MUST ASK when:
- No product idea at all
- User provides questions but no context on the business they are building
```

## Process

### Step 1: Surface All Business Risks

**ACTION:** List every assumption the business depends on — both the ones the user stated and the ones they may have missed. Use two diagnostic questions to uncover hidden risks:

1. "If this company were to fail, why would it have happened?" — list every plausible failure reason
2. "What would have to be true for this to be a huge success?" — list every condition required

**WHY:** Most founders focus on the risks they find interesting (usually the product or technology) and ignore the ones that scare them (usually the market, pricing, or distribution). The two diagnostic questions systematically surface hidden risks that the user is unconsciously avoiding. The most important questions to ask customers are precisely the ones that feel most uncomfortable.

**IF** the user provided a list of assumptions, review it against the diagnostic questions and add any missing risks
**IF** the user did not provide assumptions, generate the risk list entirely from the diagnostic questions

**OUTPUT:** A comprehensive list of business risks, grouped loosely by area (customer/problem, market/pricing, product/technology, distribution/growth, team/operations).

### Step 2: Classify Each Risk as Product Risk or Market Risk

**ACTION:** For each risk from Step 1, classify it into one of two categories:

| Risk Type | Definition | Key Questions | Can Conversations Validate? |
|-----------|-----------|---------------|---------------------------|
| **Market risk** | Do they want it? Will they pay? Are there enough of them? | Demand, willingness to pay, market size, problem severity | Yes — customer conversations are the primary validation tool |
| **Product risk** | Can I build it? Can I grow it? Will they keep using it? | Technical feasibility, scalability, retention, network effects, critical mass | Limited — you need to build something to prove these |

**WHY:** This classification determines how much weight to give conversation-based validation for each risk. If the user's biggest risk is product-side (like building a marketplace that needs critical mass, or a video game that needs to be fun), customer conversations alone cannot validate it — the user will need to start building earlier with less certainty. Mistaking product risk for market risk leads to months of conversations that "validate" obvious things (e.g., asking farmers if they want more money, asking bar owners if they want more customers).

**Detection test for product risk masquerading as market risk:** If customer responses consistently sound like "Yes, if you can actually build that, I would pay" — the risk is in the product, not the market. The customer is restating the obvious.

**IF** the majority of risks are product-side, warn the user: "Your biggest unknowns are about whether you can build and grow this, not whether people want it. Customer conversations will give you a starting point, but you will need to start building earlier to validate the core risks. Focus conversations on understanding the problem depth and current workarounds, not on confirming demand."

**OUTPUT:** Each risk annotated with its type (market/product) and whether conversations can validate it.

### Step 3: Prioritize into the Top 3 Learning Goals

**ACTION:** From the classified risk list, select the 3 most important learning goals for the next batch of conversations. Prioritize using these criteria:

1. **Business-criticality:** Could this risk, if wrong, kill the entire business? Risks that would require a complete pivot outrank risks that would require a feature adjustment.
2. **Current uncertainty:** How much evidence does the user already have? Prioritize the murkiest unknowns — the ones where the user has the least data.
3. **Conversational reach:** Can customer conversations actually answer this? Deprioritize pure product risks that need building, not talking.
4. **Scariness:** Is this a question the user has been avoiding? If a question makes the user uncomfortable, that is a signal it is important. A question you are not terrified of is probably not important enough.

**WHY:** Without prioritization, conversations wander across too many topics and produce shallow data on everything, deep data on nothing. Three is the right number because it is small enough to focus a conversation but large enough to make each conversation worthwhile. Choose the murkiest and most important questions — they will give you the firmest footing and clearest sense of direction for the next batch.

**Scary question test:** Review the final list and verify that at least one learning goal makes the user uncomfortable. If all three feel safe and easy to ask about, the list is wrong — the user is avoiding the hard questions. Flag this explicitly: "None of these learning goals seem scary. What question are you most afraid to ask? That one probably belongs on this list."

**IF** the user has multiple customer types, create a separate list of 3 for each type — learning goals differ by audience
**IF** this is not the first batch of conversations, review previous learnings and update: drop validated goals, promote the next murkiest unknowns

**OUTPUT:** A numbered list of exactly 3 learning goals, each with:
- The learning goal stated as a concrete question to answer
- Why it matters (what changes if the answer is negative)
- The risk type (market or product)
- A scariness rating (comfortable / uncomfortable / terrifying)

### Step 4: Check for Premature Zoom

**ACTION:** Review each learning goal and assess whether it assumes something that has not yet been validated. Apply the premature zoom diagnostic:

- Does this goal zoom into a specific problem area without first confirming that area matters to the customer?
- If you ask about this topic, will the customer give you detailed answers just because you asked — regardless of whether they actually care?
- Would the customer have raised this topic on their own if you asked broad questions about their life?

**WHY:** Premature zoom is one of the most dangerous patterns in customer discovery. When you ask "What is your biggest problem with X?", you assume X matters. The person gives you an answer because you asked, not because they care. This creates data that looks like validation but is actually worthless. Even if you learn everything there is to know about a trivial problem, you still do not have a business. The fix is to start broad and only zoom in when the customer independently signals that this area is a top priority for them.

**FOR EACH** learning goal:
- **IF** the goal assumes problem importance → flag it and add a broader "does this even matter?" goal that should come first
- **IF** the goal is already about confirming importance → mark it as properly scoped
- **IF** previous conversations have already confirmed importance → mark it as safe to zoom

**"Does-this-problem-matter" diagnostic questions** (use these to validate importance before zooming in):
- "How seriously do you take [area]?"
- "Do you make money from it?"
- "Have you tried making more money from it?"
- "How much time do you spend on it each week?"
- "Do you have any major aspirations for [area]?"
- "Which tools and services do you use for it?"
- "What are you already doing to improve this?"
- "What are the 3 big things you are trying to fix or improve right now?"

**OUTPUT:** Each learning goal annotated with its zoom-level safety status and, where needed, a broader prerequisite question.

### Step 5: Produce the Prioritized Learning Goals Deliverable

**ACTION:** Compile the final output document containing the prioritized learning goals with risk classification and prepared questions for each goal.

**WHY:** The deliverable must be immediately usable before conversations. The user should be able to glance at it and know exactly what they need to learn, why each goal matters, and which questions to ask. This is the "list of 3" that they carry into every conversation with this customer type.

**Output format:**

```markdown
# Prioritized Learning Goals

## Context
- **Product/Business:** [from input]
- **Target Customer:** [from input]
- **Stage:** [from input or default]
- **Date Prepared:** [today]
- **Batch:** [first / updated after N conversations]

## Risk Overview
- **Total risks identified:** [N]
- **Market risks (conversation-validatable):** [N]
- **Product risks (need building to validate):** [N]
- **Biggest overlooked risk:** [the one the user was probably avoiding]

## Top 3 Learning Goals

### 1. [Learning Goal as Question]
- **Risk type:** Market / Product
- **Why it matters:** [what changes if the answer is negative — be specific]
- **Scariness:** Comfortable / Uncomfortable / Terrifying
- **Zoom-level check:** [Safe to zoom / Needs importance confirmation first]
- **Prepared questions:**
  - [Broad opener to confirm importance]
  - [Specific past-focused depth question]
  - [Commitment/severity signal question]
- **What a negative answer looks like:** [concrete signal that disproves this]
- **What a positive answer looks like:** [concrete signal that validates this]

### 2. [Learning Goal as Question]
[same structure]

### 3. [Learning Goal as Question]
[same structure]

## Questions You Might Be Avoiding
- [Scary question 1 — and why it matters]
- [Scary question 2 — and why it matters]

## Premature Zoom Warnings
- [Any goals that assume unvalidated importance, with the broader question to ask first]

## Risk Classification Summary
| Risk | Type | Conversation Can Validate? | Priority |
|------|------|---------------------------|----------|
| [risk 1] | Market | Yes | In top 3 |
| [risk 2] | Product | Limited | Deferred |
| ... | ... | ... | ... |

## Next Steps
- After this conversation batch, review which goals are answered
- Drop answered goals, promote next-murkiest unknowns
- Update this document with new top 3
```

**IF** the user provided a file path or working directory, write the output to `learning-goals.md`
**ELSE** present the output directly in the conversation

## Examples

### Scenario 1: SaaS Founder with a Long Assumption List

**Trigger:** "I'm building a tool that helps restaurant owners manage their online reviews across Google, Yelp, and TripAdvisor. Here are my assumptions: (1) Restaurant owners care about online reviews, (2) Managing multiple platforms is painful, (3) They would pay $50/month, (4) They check reviews daily, (5) Negative reviews cause real revenue loss, (6) They want AI-generated review responses, (7) They struggle to get customers to leave reviews."

**Process:**
1. Surface all risks: The user listed 7 assumptions, but diagnostic questions reveal hidden ones — distribution (how will they find this tool?), competition (existing tools like Podium?), buyer (is the owner the one managing reviews or a manager?), and time (do they have bandwidth to use yet another tool?)
2. Classify risks: Assumptions 1-5, 7 are market risks (conversationally validatable). Assumption 6 is product risk (AI quality). Distribution and competition are market risks.
3. Prioritize top 3:
   - Goal 1: "Do restaurant owners actually manage reviews themselves, and is it painful enough to pay to fix?" (market risk, terrifying — could invalidate the whole idea)
   - Goal 2: "What tools or workarounds are they using today, and what do they spend?" (market risk, uncomfortable — might reveal strong competitors)
   - Goal 3: "How do they currently respond to negative reviews, and what is the real cost of not responding?" (market risk, comfortable — validates severity)
4. Premature zoom check: Goal 3 assumes negative reviews matter enough to act on — needs importance confirmation first

**Output (abbreviated):**
```
### 1. Do restaurant owners personally manage reviews — and is it painful enough to pay $50/month?
- Risk type: Market
- Why it matters: If owners delegate review management or don't care, there is no buyer
- Scariness: Terrifying
- Zoom-level check: Safe — this IS the importance check
- Prepared questions:
  - "Walk me through what you did the last time you got a negative review online."
  - "How much time do you spend on review-related tasks in a typical week?"
  - "What are you currently paying for any marketing or reputation tools?"
- What a negative answer looks like: "My manager handles that" or "I don't really check them"
- What a positive answer looks like: Specific stories of time spent, emotional frustration, existing workarounds
```

---

### Scenario 2: Technical Founder with Pure Product Risk

**Trigger:** "I'm building a multiplayer mobile game where players collaborate to solve environmental puzzles. I want to validate whether people would play this. My assumptions: (1) People enjoy collaborative puzzle games, (2) Environmental themes attract players, (3) Mobile is the right platform, (4) Players will invite friends to join."

**Process:**
1. Surface risks: Diagnostic questions reveal the elephant — nearly all risk is product-side (Is it fun? Can it retain players? Can it achieve network effects for multiplayer?)
2. Classify risks: All 4 stated assumptions are product risks. "Do people enjoy collaborative puzzle games?" is like asking "Do you like having fun?" — the answer is always yes.
3. Prioritize: Warn the user that conversations cannot validate the core risks. Redirect toward the few market risks that exist: Are there enough puzzle game enthusiasts in this niche? What games do they currently play? How much do they spend on mobile games?

**Output (abbreviated):**
```
## Risk Overview
- Total risks identified: 8
- Market risks: 2 (audience size, spending habits)
- Product risks: 6 (fun factor, retention, multiplayer matchmaking, network effects, art quality, puzzle design)
- Biggest overlooked risk: Nearly all your risk is product-side. Customer conversations cannot tell you whether your game is fun. You need to build a prototype and watch people play.

### 1. Are there enough people who actively seek out collaborative puzzle games — and where do they congregate?
- Risk type: Market
- Why it matters: Even a great game fails if the target audience is too small or unfindable
- Scariness: Uncomfortable
- Prepared questions:
  - "What puzzle games have you played in the last month? Tell me about the most recent session."
  - "How do you discover new games? Walk me through the last game you downloaded."
  - "Have you ever specifically searched for a game where you could play with friends?"

## Questions You Might Be Avoiding
- "Could I actually build a multiplayer puzzle game that is fun and retains players?" — This is your real risk, and conversations cannot answer it. Start prototyping.
```

---

### Scenario 3: Founder Updating Learning Goals After First Batch

**Trigger:** "I just finished 5 conversations about my invoice factoring tool for freelancers. I learned that freelancers definitely have cash flow problems (validated) and they mostly use spreadsheets to track invoices (validated). But I still don't know if they would trust a third party with their invoices, and I realize I never asked about pricing. What should I focus on next?"

**Process:**
1. Surface risks: Cash flow pain (validated), current tools (validated), trust with financial data (unvalidated), willingness to pay (unvalidated), plus hidden risks — do they invoice enough volume to justify a tool? Are there regulatory issues?
2. Classify: Trust and pricing are market risks. Invoice volume is market risk. Regulatory is mixed.
3. Prioritize top 3 for next batch:
   - Goal 1: "Would freelancers trust a third-party service to handle their invoice payments?" (market risk, terrifying — deal-breaker if no)
   - Goal 2: "How much money is stuck in late invoices per month, and what would they pay to get it faster?" (market risk, uncomfortable)
   - Goal 3: "Do they invoice enough clients per month for factoring to be worthwhile?" (market risk, comfortable)
4. Note that the user explicitly identified they "never asked about pricing" — this was a scary question they avoided in the first batch

**Output (abbreviated):**
```
## Questions You Might Be Avoiding
- "Would you hand over control of your invoices to a service you found online?" — You avoided this in 5 conversations. That avoidance is a signal that this is your scariest and most important question.
- "What would you pay for this?" — You explicitly noted you avoided pricing. Ask about current spending on financial tools first, then explore willingness to pay.
```

## Key Principles

- **The questions you are avoiding are the ones you most need to ask** — Fear of bad news causes founders to ask comfortable questions that feel productive but do not de-risk anything. If you are not terrified of at least one question in every conversation, you are wasting the conversation. The cost of not asking is always higher than the cost of hearing a bad answer. One founder avoided asking lawyers about legal ambiguities and it cost half a million dollars.

- **Product risk and market risk require different validation methods** — When the customer says "If you can build it, I will pay," that is not validation — it is restating the obvious. Customer conversations validate market risk (Do they want it? Will they pay? Are there enough of them?). Product risk (Can I build it? Can I grow it? Will they keep using it?) requires building. Misclassifying your risk type leads to months of conversations that prove things nobody doubted.

- **Start broad before zooming in — always** — Most people have many problems they will happily discuss if you ask about them. Zooming into your specific problem area before confirming it is a top priority creates false validation. The person answers your detailed questions because you asked, not because they care. Start with "What are the big things you are trying to fix right now?" and only zoom in when they raise your area themselves. If they do not mention it unprompted, they probably do not care enough to pay for a solution.

- **Three learning goals is the right number** — Too few and each conversation covers too little ground. Too many and the conversation scatters across topics without going deep on any. Three goals lets you focus while remaining flexible enough to follow interesting threads. After each batch of conversations, drop answered goals and promote the next murkiest unknowns.

- **Lukewarm signals are more reliable than enthusiastic ones** — When someone says "That is pretty neat" or "I am not so sure about that," the instinct is to pitch harder until they say something nice. Resist this. A lukewarm response is perfectly reliable information — this person does not care enough. You cannot build a business on a lukewarm response. The only thing you gain from "convincing" them is a false positive.

## References

- For designing specific questions that pass customer conversation quality rules, use the `conversation-question-designer` skill
- For narrowing broad customer segments into specific, findable who-where pairs, use the `customer-segment-slicer` skill
- For the complete "does-this-problem-matter" diagnostic question set and risk classification details, see [risk-classification-guide.md](references/risk-classification-guide.md)
