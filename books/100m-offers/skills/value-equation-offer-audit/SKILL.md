---
name: value-equation-offer-audit
description: |
  Audit and score an existing offer or service using the four-driver perceived value formula (Hormozi's "Value Equation"): Dream Outcome × Perceived Likelihood of Achievement ÷ (Time Delay × Effort & Sacrifice). Use this skill when an offer is underpriced relative to its actual value, getting price objections, or failing to convert despite being genuinely good. Scores each driver on a binary 0/1 rubric, identifies which drivers are dragging value down, and produces concrete improvement actions for each weak driver. Triggers include: "why won't people pay for this?", "how do I raise my price?", "my offer isn't converting", "I need to make my service more compelling", "how do I justify my premium", "should I be charging more?", "what makes my offer valuable?", "how do I compete against cheaper alternatives?". Applies to: consulting, coaching, courses, agencies, productized services, physical products, SaaS, any offer where perceived value determines willingness to pay.
model: sonnet
context: 200k
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Offer description, sales page, service overview, pricing page, or pitch deck"
    - type: none
      description: "Skill also works from a verbal description of the offer and target customer"
  tools-required: [Read, Write, TodoWrite]
  tools-optional: [Grep]
  environment: "Run from any directory; document access enables concrete rewrite suggestions"
depends-on: []
---

# Value Equation Offer Audit

## When to Use

Use this skill when you are:

- **Diagnosing why an offer isn't converting** — leads are interested but not buying, or price objections are frequent
- **Preparing to raise prices** — need to identify which value drivers to strengthen before justifying a higher price point
- **Comparing your offer to a cheaper competitor** — two similar offers at different prices; need to understand the perceived value gap
- **Designing a new offer from scratch** — want to build in all four value drivers before launching
- **Reviewing existing marketing copy or sales messaging** — checking whether the language communicates each driver clearly or leaves value on the table
- **Evaluating a Done-For-You vs. Do-It-Yourself vs. Done-With-You pricing structure** — deciding which delivery model to use for a given customer segment

Trigger phrases users commonly say:
- "Why won't people pay what I'm asking?"
- "I keep getting 'too expensive' — but I know we deliver results."
- "How do I make my offer more compelling without discounting?"
- "What's missing from this offer?"
- "My competitor charges less, how do I justify my premium?"
- "I want to raise my price — where do I start?"

Preconditions: you have at least one of:
- A written description of the offer, service, or product
- A sales page, landing page, or pitch deck
- A verbal description from the user of what they sell, who they sell to, and what outcome they deliver

**Agent:** Before starting, identify whether you are auditing an existing offer (AUDIT mode) or designing a new one (DESIGN mode). The process below covers AUDIT mode with design guidance embedded. For a full build-out of a new offer, use `grand-slam-offer-creation` after completing this audit.

## Context & Input Gathering

### Input Sufficiency Check

```
User prompt → Extract: what is the offer? who is the customer? what outcome is promised?
                    ↓
Environment → Scan for: sales pages, offer docs, pricing docs, pitch materials
                    ↓
Gap analysis → Do I know: (1) what the offer is, (2) who buys it, (3) what outcome is delivered,
               (4) current price or target price?
                    ↓
         Missing critical info? ──YES──→ ASK (one question at a time)
                    │
                    NO
                    ↓
              PROCEED
```

### Required Context (must have — ask if missing)

- **Offer description:**
  → Check prompt or files for: what the customer receives, how it is delivered, what the core promise is
  → If missing, ask: "Can you describe what you offer, how it's delivered, and what specific result your customer gets? For example: 'a 12-week coaching program for freelance designers that helps them go from $3k/mo to $10k/mo clients.'"

- **Target customer and their dream outcome:**
  → Check for: who buys this, what they ultimately want, what "success" looks like for them
  → If missing, ask: "Who is your ideal buyer, and what is the single result they most want from this offer?"

### Observable Context (gather from environment)

- **Existing offer materials:** Read any sales pages, proposal templates, or offer documents present.
  → Look for: how the outcome is described, what objections are preemptively addressed, what proof is offered, what friction is mentioned or unaddressed

- **Pricing context:** Note current price if stated, or ask for it if needed to calibrate the audit.

### Default Assumptions

- If no price is given: proceed with the audit; note that pricing recommendations will be directional, not absolute
- If no customer segment is specified: infer from the offer description and flag the assumption
- If delivery format is ambiguous: ask whether this is Done-For-You (DFY), Done-With-You (DWY), or Do-It-Yourself (DIY) — this directly affects the Effort & Sacrifice score

## Process

Use `TodoWrite` to track steps before beginning.

```
TodoWrite([
  { id: "1", content: "Extract offer core: outcome, customer, delivery, price", status: "pending" },
  { id: "2", content: "Score Driver 1: Dream Outcome (0 or 1)", status: "pending" },
  { id: "3", content: "Score Driver 2: Perceived Likelihood of Achievement (0 or 1)", status: "pending" },
  { id: "4", content: "Score Driver 3: Time Delay (0 or 1)", status: "pending" },
  { id: "5", content: "Score Driver 4: Effort & Sacrifice (0 or 1)", status: "pending" },
  { id: "6", content: "Identify top improvement actions per weak driver", status: "pending" },
  { id: "7", content: "Check delivery model alignment (DFY/DWY/DIY)", status: "pending" },
  { id: "8", content: "Produce scored audit summary and priority action list", status: "pending" }
])
```

---

### Step 1: Extract the Offer Core

**ACTION:** From the offer description or documents, extract and write down:
1. The specific result or transformation promised (the Dream Outcome in concrete terms)
2. Who the customer is and what their current state is
3. How the offer is delivered (Done-For-You / Done-With-You / Do-It-Yourself)
4. Current price (if known) or target price range
5. Time from purchase to first result, and time to full result

**WHY:** The four value drivers operate on the customer's *perception*, not objective reality. Before scoring, you need to know both what is actually delivered AND how it is currently communicated — because the gap between those two is often where value is being lost. A genuinely excellent offer can score poorly if it fails to communicate its drivers clearly. Equally, a weak offer cannot be saved by communication alone. Separating "what it is" from "how it is communicated" is essential for diagnosing the right problem.

**Output:** A single-paragraph offer summary in this format:
> "[Offer name] helps [customer segment] go from [current state] to [dream outcome] via [delivery method], in [time to first result / full result], at [price]. Delivery requires [what the customer must do]."

Mark Step 1 complete in TodoWrite.

---

### Step 2: Score Driver 1 — Dream Outcome

**Definition:** The dream outcome is the gap between where the customer is now and where they most want to be. It is not a feature list — it is the *feeling* and *status* the customer expects to experience after achieving the result. Offers that tap into status, respect, security, love, or freedom score higher than offers framed around features or mechanics.

**Scoring rubric:**
- **1 (value achieved):** The offer is clearly framed around a specific, emotionally resonant outcome the customer deeply wants. The outcome increases their status in some meaningful way (professionally, socially, financially, physically). The customer would describe the outcome in their own words, not the seller's jargon.
- **0 (missing):** The offer is described in terms of what is included ("8 modules," "weekly calls," "template library") rather than what the customer becomes or achieves. The outcome is vague ("grow your business," "feel better") or framed in seller-centric language.

**ACTION:**
1. Read the current offer description.
2. Ask: "Does this description make a customer *feel* the outcome, or just list what they receive?"
3. Identify the deepest desire the offer actually addresses. Probe one level deeper than the surface: weight loss → feeling attractive and confident → increased status among peers. The deeper the desire the offer connects to, the higher its dream outcome score.
4. Assign score: 0 or 1.

**IF score = 0:** Note the specific language changes needed to reframe the offer around the outcome. The fix is almost always repositioning, not rebuilding the offer.

**Levers for increasing Dream Outcome:**
- Name the specific end state in the customer's language, not the seller's
- Quantify the outcome where possible: "$10k/month" beats "more revenue"; "close your first enterprise deal" beats "improve your sales"
- Connect the outcome to status: describe how the customer will be perceived by peers, family, or clients once they achieve it
- Address the *real* desire beneath the stated desire (the minivan example: a customer who "doesn't care about status" still chose the option that increased status among the people they care about)

Mark Step 2 complete in TodoWrite.

---

### Step 3: Score Driver 2 — Perceived Likelihood of Achievement

**Definition:** Perceived likelihood of achievement is the customer's belief that *they specifically* will get the promised result if they buy this offer. It is not about whether the result is real — it is about the customer's confidence that it will happen for them. People pay for certainty. A surgeon's 10,000th patient pays more than their first, even if both receive the same procedure, because the perceived likelihood of a good outcome is higher.

**Scoring rubric:**
- **1 (value achieved):** The offer includes strong, specific social proof that the target customer identifies with (case studies from similar people, testimonials with specific outcomes, before/after data). It pre-answers the customer's internal objection: "But will this work for *me*?" It reduces perceived risk through guarantees, proof of track record, or credentialing. The customer leaves the offer description more confident than when they arrived.
- **0 (missing):** The offer relies on general claims without proof. Testimonials are vague ("This was amazing!") or from customers who don't resemble the target buyer. No mechanism is explained for why this works. The customer is expected to take the result on faith.

**ACTION:**
1. Identify all proof elements currently in the offer: testimonials, case studies, data, credentials, methodology explanations.
2. Evaluate each for specificity and relatability to the target customer.
3. Ask: "Would a skeptical, first-time buyer read this and think: 'Yes, this will work for someone like me'?"
4. Assign score: 0 or 1.

**IF score = 0:** Identify the fastest path to adding specific, credible proof. If proof is thin, the offer needs structural components that increase confidence: money-back guarantees, risk reversal, detailed methodology explanation, or a visible track record. See `guarantee-design-and-selection` for specific guarantee structures.

**Levers for increasing Perceived Likelihood of Achievement:**
- Testimonials from customers who match the target buyer (same role, same problem, similar starting point)
- Specific outcome data: "14 out of 17 clients hit $10k/month within 90 days" beats "many clients see great results"
- Mechanism explanation: explain *why* this works (the system, the process, the proprietary method) — customers who understand the mechanism trust the outcome more
- Risk reversal: guarantees do not just reduce risk, they signal that the seller is confident enough to stake money on the result
- Credentials and track record: years in domain, number of clients served, recognizable past clients or employers

Mark Step 3 complete in TodoWrite.

---

### Step 4: Score Driver 3 — Time Delay

**Definition:** Time delay is the gap between when a customer pays and when they first experience meaningful value. Two components matter: (1) the long-term outcome (the ultimate result they bought for) and (2) short-term wins that occur on the path to that outcome. Customers *buy* for the long-term outcome but *stay* for the short-term wins. The shorter the gap to first value, the higher the perceived value of the offer.

**Critical insight — fast beats free:** Speed is so valuable that many companies have built entire businesses by charging for what others give away — simply by delivering it faster. FedEx vs. USPS. Uber vs. walking. Private DMV renewal vs. waiting in line. If an offer competes in a market that has a free alternative, the winning strategy is almost always speed, not price reduction.

**Scoring rubric:**
- **1 (value achieved):** The offer delivers a meaningful quick win within the first 24–72 hours of purchase — an emotional confirmation that the customer made the right decision. The path to the long-term outcome includes visible milestones that reassure the customer they're on track. The time to full result is clearly stated and is competitive for the category.
- **0 (missing):** Value delivery begins slowly, with no early wins designed in. The customer must wait weeks or months before seeing any evidence the offer is working. No milestones are communicated. The time to full result is vague or long without justification.

**ACTION:**
1. Map the current delivery timeline: when does the customer first experience something? When do they first see a result?
2. Ask: "What is the fastest meaningful win I could deliver within the first 7 days?"
3. Check: is the time to full result competitive with alternatives in this market? (Including doing nothing, DIY, or competing offers)
4. Assign score: 0 or 1.

**IF score = 0:** Design a specific fast-win component to add to the offer. This is often the highest-leverage improvement available — it costs little to deliver, dramatically increases retention and referrals, and raises perceived value without changing price. Examples: a quick-start guide that delivers one concrete result on day one; a first-session output that gives the customer something immediately usable; a 48-hour diagnostic that shows the customer exactly where they are and what to do next.

**Gym example:** A gym client's long-term goal (adding $239k/year in revenue) takes months to achieve. The fast-win solution was getting their first ad live and closing a $2,000 sale within their first 7 days. This immediate win reinforced their purchase decision and built the trust needed to follow through the full program.

**Levers for decreasing Time Delay:**
- Design an explicit "fast win" deliverable for the first 24–72 hours (not just onboarding paperwork)
- Structure the delivery sequence so the customer experiences value *while* progressing toward the full outcome
- Communicate milestones clearly: "By week 2 you will have X; by week 6 you will have Y"
- Consider whether a higher-touch delivery option (DFY vs. DWY) reduces the customer's wait time enough to justify premium pricing
- If the full outcome genuinely takes time, make the short-term experience vivid: what will they feel, see, and receive along the way?

Mark Step 4 complete in TodoWrite.

---

### Step 5: Score Driver 4 — Effort & Sacrifice

**Definition:** Effort & Sacrifice is everything the customer must give up, endure, or do in order to receive the outcome — beyond simply paying the price. This includes time, energy, learning curves, lifestyle changes, social discomfort, and risk. Done-For-You services command premium prices primarily because they eliminate this driver almost entirely. The customer's ideal scenario is to say yes, hand over money, and wake up with the outcome — zero effort on their part.

**Warning — AP-5: the beginner marketer top-of-equation trap:** Most new offer designers focus exclusively on Drivers 1 and 2 (Dream Outcome and Perceived Likelihood) because they are easy to work on — you simply make bigger claims. This is the lazy approach, and it produces an arms race of promises that becomes increasingly easy to ignore. The companies that dominate their markets — Apple, Amazon, Netflix — win by obsessing over the *bottom* of the equation: making delivery faster, more seamless, and more effortless than anyone else. When your offer has strong top drivers but weak bottom drivers, raising Drivers 3 and 4 is almost always the highest-leverage move available, because it is harder for competitors to copy and more unique in most markets.

**Scoring rubric:**
- **1 (value achieved):** The customer's required effort is minimal, clearly bounded, and feels worth the outcome. Every friction point in the delivery process has been addressed or removed. The offer anticipates what customers find hard or uncomfortable and either eliminates it (DFY) or makes it easy (DWY). The marketing honestly names the sacrifice required and frames it as minimal compared to alternatives.
- **0 (missing):** The offer requires significant ongoing effort from the customer, and this is either unaddressed in the marketing or presented as a virtue ("hard work pays off"). Friction points are hidden and only discovered after purchase. The customer's experience of getting to the outcome is harder than they expected.

**ACTION:**
1. List every action, change, and discomfort the customer must endure to receive the full outcome. Be exhaustive — include: time, scheduling, learning new tools or concepts, lifestyle changes, social friction, emotional discomfort, administrative tasks.
2. For each item on that list, ask: "Can this be eliminated? Can it be reduced? Can it be done for them?"
3. Compare your list to what the marketing currently communicates about required effort.
4. Assign score: 0 or 1.

**Fitness vs. liposuction comparison:** Both deliver the same outcome (reduced body fat). Fitness requires: waking up earlier, 5–10 hours/week, dietary restriction, physical discomfort, embarrassment, risk of injury, meal prep, new food costs. Liposuction requires: falling asleep and being sore for 2–4 weeks. This is why liposuction commands $25,000 while gym memberships struggle to hold $29/month. The outcome is identical; the effort and sacrifice differential is enormous.

**Levers for decreasing Effort & Sacrifice:**
- Move from DIY to DWY to DFY where feasible — each step dramatically reduces customer effort and justifies a price increase
- Eliminate administrative friction: intake forms, scheduling complexity, and onboarding steps are all effort costs before value is received
- Anticipate and pre-solve the most common points where customers get stuck or give up
- Reframe necessary effort as trivially small compared to the alternative (as liposuction marketing does against gym memberships)
- Consider psychological solutions over logical ones: reducing the *perception* of effort is often as powerful as reducing actual effort (the London Underground dotted map increased rider satisfaction more than faster trains — at a fraction of the cost)

Mark Step 5 complete in TodoWrite.

---

### Step 6: Identify Improvement Actions per Weak Driver

**ACTION:** For each driver scored at 0, produce 2–3 specific, concrete actions the user can take to improve it. Prioritize actions by:
1. Speed of implementation (can this be done this week?)
2. Leverage (does fixing this likely unlock price increases or conversion improvements?)
3. Cost (does it require building new delivery infrastructure or just repositioning existing content?)

**Prioritization guidance:**
- If Drivers 3 or 4 (Time Delay and Effort & Sacrifice) are scored 0: prioritize these first. They are harder to fake, more competitively durable, and are where most markets are weakest. This is the antidote to AP-5.
- If Driver 2 (Perceived Likelihood) is scored 0: this is often the fastest fix — adding specific case studies and testimonials is low-cost and high-impact.
- If Driver 1 (Dream Outcome) is scored 0: this is a messaging and positioning problem, not a product problem. The fix is rewriting, not rebuilding.

Mark Step 6 complete in TodoWrite.

---

### Step 7: Evaluate Delivery Model Alignment

**ACTION:** Assess whether the current delivery model (DFY / DWY / DIY) is optimally aligned with the target customer's preferences and willingness to pay.

**WHY:** The delivery model is one of the highest-leverage decisions in offer design. It directly affects all four value drivers simultaneously: DFY maximizes Perceived Likelihood (experts do it) and minimizes Effort & Sacrifice (the customer does almost nothing), while DWY and DIY shift those drivers in the opposite direction. Most businesses default to one delivery model without consciously choosing it — which means they often leave money on the table by not offering a DFY tier, or price-compress themselves by not offering a DIY tier for price-sensitive buyers.

**DFY / DWY / DIY pricing ladder:**
- **Done-For-You (DFY):** Highest price. Customer pays for expertise, speed, and zero personal effort. Best for customers whose time is expensive or whose confidence in DIY is low. Perceived Likelihood is highest because an expert handles execution.
- **Done-With-You (DWY):** Mid-tier. Customer learns and participates, but with guidance. Balances price sensitivity with personal involvement. Appropriate for customers who want to build capability, not just get the outcome.
- **Do-It-Yourself (DIY):** Lowest price. Customer receives tools, systems, and knowledge. High Effort & Sacrifice score. Appropriate for price-sensitive buyers or those who value developing the skill themselves.

**Questions to resolve:**
- Is there a DFY option for customers willing to pay a premium? If not, is there a reason to add one?
- If the current offer is DWY or DIY, is the pricing reflecting the customer's burden (high Effort & Sacrifice)?
- Would a tiered structure (DIY / DWY / DFY at different price points) capture more of the market without cannibalizing the premium tier?

Mark Step 7 complete in TodoWrite.

---

### Step 8: Produce the Scored Audit Summary

**ACTION:** Write the final audit output.

**Format:**

```
VALUE EQUATION AUDIT — [Offer Name]

Offer summary: [one-paragraph summary from Step 1]

DRIVER SCORES:
┌─────────────────────────────────────┬───────┬──────────────────────────┐
│ Driver                              │ Score │ Status                   │
├─────────────────────────────────────┼───────┼──────────────────────────┤
│ 1. Dream Outcome                    │  /1   │ [Strong / Needs work]    │
│ 2. Perceived Likelihood             │  /1   │ [Strong / Needs work]    │
│ 3. Time Delay (lower = better)      │  /1   │ [Strong / Needs work]    │
│ 4. Effort & Sacrifice (lower = better)│ /1  │ [Strong / Needs work]    │
├─────────────────────────────────────┼───────┼──────────────────────────┤
│ OVERALL                             │  /4   │ [Verdict]                │
└─────────────────────────────────────┴───────┴──────────────────────────┘

OVERALL VERDICT:
4/4 — Strong perceived value. Offer is positioned to command premium pricing. Review messaging and guarantee structure.
3/4 — Good foundation. One driver is limiting value. Fix the weak driver before raising price.
2/4 — Significant value gap. Two drivers are dragging conversion and price tolerance down. Priority improvements required.
1/4 or below — Fundamental offer problem. Perceived value is low regardless of quality. Consider offer redesign using grand-slam-offer-creation.

PRIORITY ACTIONS:
1. [Driver X — specific, concrete action, estimated effort: low/medium/high]
2. [Driver Y — specific, concrete action, estimated effort: low/medium/high]
3. [Driver Z — specific, concrete action, estimated effort: low/medium/high]

DELIVERY MODEL NOTE:
[Assessment of whether current DFY/DWY/DIY structure is appropriate, and whether a pricing ladder is warranted]

NEXT STEPS:
[If score < 3/4]: Use grand-slam-offer-creation to rebuild offer components around weak drivers.
[If score = 3/4]: Address priority actions above, then re-audit.
[If score = 4/4]: Use premium-pricing-strategy to identify the price ceiling for this offer.
[If Driver 2 is weak]: Use guarantee-design-and-selection to add risk-reversal that boosts perceived likelihood.
```

**HANDOFF TO HUMAN** — present the scored audit and priority action list. Ask: "Which of these actions do you want to tackle first? I can help you rewrite the offer framing, design a fast-win component, or work on proof elements."

Mark Step 8 complete in TodoWrite.

---

## Examples

### Example 1: Photography Studio — 5x Ticket Increase

**Trigger:** "I run a photography studio. My average client pays $300 per session. I want to charge $1,500 but I don't know how to justify it."

**Offer summary:** Portrait photography sessions for families and professionals. 1-hour session, 20 edited photos delivered in 2 weeks. Customer selects prints or digital files. Price: $300.

**Audit:**

| Driver | Score | Finding |
|---|---|---|
| Dream Outcome | 0 | Offer is described as "photos" and "editing." The actual dream outcome — looking beautiful, feeling proud, capturing a milestone — is absent from all marketing. |
| Perceived Likelihood | 1 | Portfolio is strong with clear before/after quality evidence. Customer can see the output they will receive. |
| Time Delay | 0 | 2-week delivery with no interim touchpoints. Customer pays and then waits with no confirmation they made the right decision. |
| Effort & Sacrifice | 0 | Customer must schedule around studio hours, travel to the studio, manage children during the session, and wait 2 weeks for any value. No guidance on how to prepare, what to wear, or what to expect. |

**Overall: 1/4**

**Priority actions:**
1. **Dream Outcome (messaging reframe, low effort):** Rewrite all copy to center on the outcome: "Family portraits that stop you in your tracks — the kind your kids will find in a drawer 30 years from now and cry over." Frame every package around the memory and status the photo creates, not the technical specs.
2. **Time Delay (fast win design, medium effort):** Send a preview of 3 favorite shots within 24 hours of the session. This gives the customer an immediate emotional win and confirmation. Full gallery at 2 weeks, but the customer stops waiting after day one.
3. **Effort & Sacrifice (friction removal, medium effort):** Add a preparation guide ("What to wear, how to prep kids, what to expect") to eliminate the anxiety of not knowing. Offer a mobile session option to eliminate travel. These changes reduce the perceived effort of booking, not just the session itself.

**Result:** Implementing all three actions removes the drivers that were suppressing price tolerance. The offer's actual quality (1/4 → 3–4/4 after changes) supports a $1,500 price. The studio's profitability transformation followed: same hours, higher value delivered, dramatically higher revenue per client.

---

### Example 2: Business Coaching — First 7-Day Fast Win

**Trigger:** "I'm a business coach for gym owners. I charge $2,000/month but I'm getting a lot of churn after month 2. People say they're not seeing results fast enough."

**Offer summary:** Monthly coaching program for gym owners targeting $239k/year incremental revenue. Weekly calls, strategy sessions, and ad setup guidance. Full results expected over 6–12 months. Price: $2,000/month.

**Audit:**

| Driver | Score | Finding |
|---|---|---|
| Dream Outcome | 1 | "$239k additional annual revenue" is specific, quantified, and highly motivating to gym owners. |
| Perceived Likelihood | 1 | Coach has track record of achieving this with multiple clients. Case studies present. |
| Time Delay | 0 | 6–12 months to full outcome. No explicit fast-win milestones designed in. Customer is left wondering "is this working?" after month 1. Churn at month 2 is the direct symptom. |
| Effort & Sacrifice | 0 | Gym owners must implement ad strategies, manage campaigns, change sales conversations, and train staff — all while running their existing business. Required effort is high and largely unaddressed. |

**Overall: 2/4**

**Priority actions:**
1. **Time Delay — design a 7-day fast win (medium effort):** Within the first week, get the gym owner's first ad live and close a $2,000 membership sale using the new sales framework. This is the single highest-leverage change available. It answers "is this working?" before the customer has time to doubt their decision. Churn at month 2 drops because the customer already has evidence they are on the right path.
2. **Effort & Sacrifice — reduce implementation friction (medium effort):** Provide done-for-you ad templates, scripts for sales conversations, and a week-by-week implementation calendar. The coaching should move from "here's what to do" to "here's the exact thing to copy and use today." Consider adding a monthly DFY ad management option at a higher tier for owners who do not want to manage campaigns.
3. **Effort & Sacrifice — acknowledge and reframe required effort (low effort):** In the sales conversation, be explicit: "Here is exactly what you will need to do in the first 30 days, and here is what we do for you. Most owners tell us it takes 3–4 hours per week." Naming the effort honestly, and showing it is bounded, is more effective than hiding it and having customers discover it post-purchase.

---

### Example 3: Software Tool — Competing Against Free

**Trigger:** "We have a project management tool for freelancers. There are free alternatives. How do we justify charging $49/month?"

**Offer summary:** Project management SaaS for freelancers. Features include time tracking, invoice generation, client portal, and project templates. Onboarding takes 2–3 hours. Price: $49/month.

**Audit:**

| Driver | Score | Finding |
|---|---|---|
| Dream Outcome | 0 | Tool is described by features ("time tracking," "invoices"), not by outcome ("get paid faster," "look more professional to clients," "spend less time on admin"). |
| Perceived Likelihood | 0 | No case studies showing specific results (e.g., "freelancers using this tool get paid 8 days faster on average"). Free tools have more social proof by volume. |
| Time Delay | 0 | 2–3 hour onboarding before any value is experienced. Competitor free tools can be used in minutes. |
| Effort & Sacrifice | 0 | Migration from existing tools, learning curve, ongoing 2–3 hour setup, and no automation of existing workflow. High friction relative to free alternatives. |

**Overall: 0/4**

**Fast beats free principle in action:** When competing against free tools, the winning strategy is never price reduction — it is speed and effortlessness. FedEx vs. USPS. Uber vs. walking. The free alternative is available; the question is: which customers will pay for faster, easier delivery of the same outcome?

**Priority actions:**
1. **Time Delay — reduce onboarding to under 15 minutes (high effort, high leverage):** Free tools win on friction-of-starting. If the paid tool can deliver a working setup faster than the free alternative, it wins on time delay. Build an onboarding wizard that imports existing projects from common tools (Trello, Notion) and generates a first invoice template in under 10 minutes.
2. **Dream Outcome — reframe around professional status (low effort):** Change all copy from features to outcomes: "Send invoices that make clients say 'this feels like a real agency'" and "Get paid in 3 days instead of 30." Both are about status and money — the real dream outcomes for freelancers.
3. **Perceived Likelihood — add specific proof (medium effort):** Add one prominent case study with data: "Julia, freelance designer, reduced time on invoicing from 4 hours/week to 20 minutes and got paid 11 days faster." This is the kind of proof that makes the $49/month feel like a bargain against the outcome.

---

## Key Principles

- **Perception is the only currency.** Improving the actual offer matters only if the improvement is perceived by the customer. The London Underground's dotted arrival-time map increased rider satisfaction more than faster trains — at a fraction of the cost. Always ask: "How will the customer *perceive* this change?" before investing in building it.

- **The bottom of the equation is where markets are most underdeveloped.** Most competitors focus on Dream Outcome and Perceived Likelihood — making bigger promises and stacking social proof. Very few systematically address Time Delay and Effort & Sacrifice. This is where durable competitive advantage lives. The best companies in every category win by making their delivery faster, more seamless, and more effortless than anyone else.

- **Fast beats free.** When competing in a market with free alternatives, the winning move is speed and effortlessness — not price reduction. People pay for the elimination of waiting and effort. Any offer that delivers faster or requires less work than the free alternative has a viable premium.

- **Done-For-You always commands a premium — even for the same outcome.** The reason DFY services cost 10–100x more than DIY versions of the same result is Effort & Sacrifice and Perceived Likelihood operating together: the customer does nothing (effort = 0) and trusts an expert to deliver (likelihood = high). If your offer is currently DWY or DIY and you are struggling to hold price, the highest-leverage option is adding a DFY tier.

- **Binary scoring forces honest diagnosis.** Rating each driver 0 or 1 — not 0.7 or "pretty good" — forces a clear verdict on whether each driver is actually contributing to perceived value. Partial credit is how weak offers justify staying unchanged. If a driver is not clearly and confidently delivering value to the customer, score it 0 and fix it.

## References

- For building out a new offer from scratch after identifying gaps: `grand-slam-offer-creation`
- For designing guarantees that improve Driver 2 (Perceived Likelihood of Achievement): `guarantee-design-and-selection`
- For setting and justifying premium prices once all four drivers are strong: `premium-pricing-strategy`
- Source: *$100M Offers*, Alex Hormozi, Chapter 6 "Value Offer: The Value Equation," pages 78–93

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — 100M Offers by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
