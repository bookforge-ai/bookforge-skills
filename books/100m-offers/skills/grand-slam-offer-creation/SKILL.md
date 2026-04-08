---
name: grand-slam-offer-creation
description: |
  Build a complete, differentiated offer bundle from scratch using a 5-step process: define the target customer's dream outcome, map every obstacle they face, convert those obstacles into named solution components, select the highest-value delivery formats for each, then trim low-value items and stack the remainder into a final offer with assigned dollar values and a single price. Use this skill when starting a new offer, when an existing offer is being commoditized (competing on price), when conversion is poor despite genuine quality, or when a business needs to escape the "race to the bottom" pricing dynamic. Trigger phrases: "how do I create an offer", "build me a product", "what should I include in my offer", "how do I stop competing on price", "design a new service package", "make my offer irresistible", "what should my program include", "how do I package my services", "what should I charge for", "create an offer from scratch", "help me build a coaching program", "escape commoditization". Applies to: coaching, consulting, agencies, courses, productized services, gyms, clinics, SaaS, any business where the offer structure determines price and conversion. This is the hub skill for offer creation — run it before guarantee design, bonus stacking, scarcity/urgency framing, or offer naming.
tags: [offers, product-design, value-creation, sales, entrepreneurship]
depends-on: [value-equation-offer-audit, target-market-selection]
---

# Grand Slam Offer Creation

## When to Use

Use this skill when you need to build or rebuild a complete offer from scratch. Specifically:

- **Starting a new product or service** — you know what you do but not how to package it into an irresistible offer
- **Competing on price against cheaper alternatives** — your current offer looks identical to competitors and buyers negotiate you down
- **Low conversion despite genuine quality** — your service is good but prospects don't perceive the value before they buy
- **Existing offer lacks differentiation** — buyers can compare your price directly to others, which always ends badly for margins
- **After completing `value-equation-offer-audit`** — you've identified weak value drivers and need to build the offer components that address them

**What this skill produces:** A complete offer document with named components, assigned perceived dollar values, a stacked total value, and a single purchase price — structured so the buyer experiences a massive value-to-price gap that makes saying no feel irrational.

**What this skill does not cover:** Pricing, guarantee design, bonus stacking, scarcity/urgency, or naming. Run `premium-pricing-strategy`, `guarantee-design-and-selection`, `bonus-stacking-system`, `scarcity-and-urgency-tactics`, and `offer-naming-magic-formula` after completing this skill.

**Precondition:** You must know (1) who you serve and (2) what outcome they ultimately want. If you don't yet have a defined target market, run `target-market-selection` first.

## Context & Input Gathering

### Input Sufficiency Check

```
User prompt → Extract: who is the target customer? what is their dream outcome?
                    ↓
Environment → Scan for: existing offer docs, sales pages, service descriptions
                    ↓
Gap analysis → Do I know: (1) who the customer is, (2) what they most want to achieve,
               (3) what business/service is being offered?
                    ↓
         Missing critical info? ──YES──→ ASK (one question at a time, max 2 questions)
                    │
                    NO
                    ↓
              PROCEED with 5-step process
```

### Required Context (ask if missing)

- **Target customer:** Who buys this? What is their current situation?
  → If missing, ask: "Who is your ideal buyer and what is their current frustrating situation before they find you?"

- **Dream outcome:** What does the customer ultimately want to achieve — the destination, not the journey?
  → If missing, ask: "What specific result does your ideal customer most want? (e.g., 'lose 20 pounds in 6 weeks', 'sign 3 new clients per month', 'launch their first product')"

- **What you do / your core capability:** What do you know how to deliver?
  → Usually stated in the user's initial prompt. If not, ask: "What is the core service or expertise you are packaging?"

### Default Assumptions

- If no specific market is stated: infer from the offer description and flag the assumption
- If the user has an existing offer: treat it as the starting point for Step 1, not as the finished product
- If the user is unsure what to charge: build the offer first (Steps 1–5), then stack the component values — the price follows from perceived value, not from cost or habit

## Process

Use `TodoWrite` to track steps before beginning:
- Step 1: Define dream outcome | Step 2: Map all problems | Step 3: Convert to solution statements | Step 4: Generate delivery vehicles | Step 5a: Trim | Step 5b: Stack + assign values | Final: Output offer document

---

### Strategic Framing: The Sales-to-Fulfillment Continuum

Before building, establish the right mindset for offer design.

Every offer sits on a continuum between two extremes:

```
Easy to Sell  ←────────────────────────────────→  Hard to Sell
Hard to Fulfill ←──────────────────────────────→  Easy to Fulfill
```

- **Maximum sales ease** (over-delivering on everything) makes the offer irresistible but can make the business unsustainable
- **Maximum fulfillment ease** (bare-minimum delivery) makes the business easy to run but kills sales
- **The goal is a sweet spot:** an offer that is genuinely easy to sell because it over-delivers on perceived value, but structured using low-cost, high-leverage delivery vehicles so margins remain strong

**Practical guidance for new offers:** When building your first version, bias toward over-delivering. Generate demand first. Once you have buyers saying yes and cash flowing, optimize fulfillment. It is always easier to remove from an offer that is selling than to fix an offer that is not.

**Warning — AP-10 (Fulfillment Imbalance):** Do not design an offer so heavy that fulfillment destroys the business. If you cannot deliver the offer profitably at scale, you will either burn out or quietly stop honoring the promise. Every component you add in Step 4 must pass the filter in Step 5: is the cost-to-deliver acceptable at volume? The goal is high perceived value to the buyer at low actual cost to you. "One-to-many" delivery vehicles (guides, videos, templates, automated systems) are the highest-leverage format because they cost the same whether you serve 10 clients or 10,000.

---

### Step 1: Define the Dream Outcome

**ACTION:** Identify the specific end state the customer most wants to reach — not what your service does, but where the customer arrives.

1. Write down the customer's dream outcome in concrete, measurable terms:
   - What does "success" look like for them in specific numbers or observable states?
   - What is the largest result they could reasonably expect?
   - Add a time component: what is the minimum viable timeframe in which this result could occur?

2. Check: are you selling the flight or the vacation?
   → "A gym membership" = the flight (the mechanism)
   → "Lose 20 pounds in 6 weeks" = the vacation (the destination)
   Always sell the vacation. The mechanism is irrelevant to the buyer.

3. Write your dream outcome statement in this format:
   > "[Specific measurable result] in [timeframe]"
   > Example: "Lose 20 pounds in 6 weeks"
   > Example: "Get 20 new gym clients in 30 days"
   > Example: "Sign 3 enterprise software deals in 90 days"

**WHY:** Everything in Steps 2–5 is built to deliver this specific outcome. The more precise your dream outcome, the more precisely you can map the obstacles between the customer and that outcome, which is where all value in the offer comes from. A vague outcome ("grow your business") produces vague problems which produce vague solutions which produce a mediocre offer.

**IF/THEN:**
- If the user has multiple possible outcomes: pick the one that is most emotionally resonant and commercially significant to the target customer. You can always add variations later.
- If the dream outcome is vague: push one level deeper. "Lose weight" → "lose 20 pounds" → "fit into my wedding dress in 8 weeks." The deeper the specificity, the higher the perceived value of an offer that addresses it.

Mark Step 1 complete in TodoWrite.

---

### Step 2: List All Problems (Obstacle Mapping)

**ACTION:** Generate an exhaustive list of every obstacle the target customer faces on the path from where they are now to the dream outcome.

**The 4-bucket problem framework:** Every obstacle a customer faces falls into one of four categories — these map directly to the four drivers in the value equation. Use them as prompts, not constraints:

| Bucket | Core fear | Customer says... |
|--------|-----------|-----------------|
| **Dream Outcome** | "It won't be worth it financially" | "Is this even possible for someone like me?" |
| **Perceived Likelihood** | "It won't work for me specifically" | "I'll start and then quit. External factors will derail me." |
| **Effort & Sacrifice** | "It will be too hard / I'll hate it" | "This requires too much discipline / I'll suck at it." |
| **Time** | "It will take too long / I'm too busy" | "I don't have time for this. It's not convenient." |

**Technique:** For each thing the customer must *do* to reach the dream outcome, generate every reason they might not be able to do it, sustain it, or complete it. Think in sequence — what happens immediately before they start? What happens immediately after? What are the next steps after that?

**Gym example (Step 2 in action):**
- Dream outcome: Lose 20 pounds in 6 weeks
- Things they must do: buy healthy food → cook healthy food → eat healthy food → exercise regularly → stay consistent → handle social situations
- For "buy healthy food": it's hard and confusing / takes too much time / is expensive / is unsustainable when traveling or when family has different needs
- For "cook healthy food": hard, time-consuming, expensive, unsustainable, family conflicts, no idea what to do when traveling
- For "exercise": confusing, embarrassing, risk of injury, don't know what to do, don't like it, too busy
- (Repeat for every item they must do)

**Guidance:** Aim for exhaustiveness. More problems = more solutions = more components = more perceived value. Repetition across buckets is normal. Do not filter yet — filtering is Step 5.

**Output:** A written list organized by task (e.g., "Buying food: [list]", "Cooking: [list]"). Aim for 20–50+ problems.

**WHY:** The problems list is the complete map of every reason a prospect might say no or quit. If any one item on this list goes unsolved, it becomes a potential lost sale or a client who fails and cancels. Solving all of them makes the offer impossible to compare to commoditized alternatives that solve only some.

Mark Step 2 complete in TodoWrite.

---

### Step 3: Convert Problems into Solution Statements

**ACTION:** Take every problem from Step 2 and flip it into a positive solution statement using the frame: *"What would I need to show someone to solve this problem?"*

**The conversion formula:** Reverse each problem element into outcome-oriented language.
- "Buying healthy food is hard, confusing, I won't like it" → "How to make buying healthy food easy and enjoyable, so that anyone can do it"
- "Cooking takes too much time" → "How to cook meals in under 5 minutes"
- "This is expensive, it's not worth it" → "How eating healthy is actually cheaper than unhealthy food"
- "It's unsustainable" → "How to make eating healthy last forever"
- "My family's needs will get in the way" → "How to cook this despite your family's concerns"
- "I won't know what to do when I travel" → "How to travel and still eat healthy"

**Format for each conversion:**
> [Problem statement] → [Solution statement beginning with "How to..."]

**WHY:** The solutions list is not the offer yet — it is the *checklist* of what the offer must accomplish. Each solution statement tells you exactly what a buyer needs to believe you can deliver. This step transforms the creative chaos of Step 2 into a structured list of deliverables. It also prevents common offer-building errors: adding components based on what's easy to create rather than what solves a real obstacle.

**Critical rule:** Solve every problem. Do not self-censor — write all solutions even if unsure how to deliver them yet. Filtering for feasibility is Step 5. One unsolved obstacle can be the single reason a sale is lost.

**Output:** A solution list mirroring the problem list from Step 2, one "How to..." statement per problem. These become the offer component building blocks in Step 4.

Mark Step 3 complete in TodoWrite.

---

### Step 4: Generate Delivery Vehicles ("The How")

**ACTION:** For each solution statement from Step 3, brainstorm every possible way you could deliver that solution. This is the most important step in the process — this is what you will actually provide in exchange for money.

**Goal:** Generate the most expansive possible list before filtering. Think divergently: if money and time were no constraint, how many different ways could you deliver each solution?

**The 6-dimension delivery vehicle cheat codes:** For each solution, run through all six dimensions to generate variations:

| Dimension | Questions | Options |
|-----------|-----------|---------|
| **1. Level of attention** | How many people receive this at once? | 1-on-1 / Small group / One-to-many |
| **2. Customer effort level** | How much does the customer do themselves? | Do-It-Yourself (DIY) / Done-With-You (DWY) / Done-For-You (DFY) |
| **3. Live delivery medium** | If delivering live, what channel? | In-person / Phone / Email / Text / Video call / Chat |
| **4. Recorded consumption format** | If recorded, how does the customer consume it? | Video / Audio / Written |
| **5. Speed and availability** | When and how quickly is this available? | 24/7 / 9–5 / Within 5 minutes / Within 1 hour / Within 24 hours / Monday–Friday |
| **6. The 10x/1/10th test** | Expand the solution space in both directions: | If the customer paid 10x your price ($100,000), what would you provide? If they paid 1/10th the price and you still had to make them successful, what's the leanest possible version? |

**How to use the 10x/1/10th test:** This is a divergent thinking tool, not a commitment to delivery. Ask: "If this customer paid me $100,000, what would I do for them?" The answer pushes you toward ideas you wouldn't normally consider. Then ask: "If they paid $100, how could I still get them the result?" This often surfaces elegant, scalable, low-cost solutions. Both directions generate ideas. You keep the ones you will actually deliver in Step 5.

**Example (for the problem "Buying healthy food is hard and confusing"):**

*One-on-one delivery options:*
- In-person grocery shopping trip where I take the client to the store and teach them
- Personalized grocery list, taught 1-on-1
- Full-service shopping: I buy their food for them entirely
- Text support while they shop — they text me pictures and I guide them
- Phone call scheduled for when they're at the store

*Small group options:*
- Group grocery shopping trip
- Group class: how to build a weekly shopping list
- Shared grocery delivery service

*One-to-many / scalable options:*
- Recorded grocery store walkthrough video
- DIY grocery calculator tool (spreadsheet or app)
- Pre-made weekly grocery lists for each meal plan tier
- Grocery buddy system (pair clients together)
- Pre-made Instacart lists — one click delivers their week

**After generating:** You will have a monster list of 50–100+ delivery vehicle options. This is correct. Filtering happens in Step 5.

**WHY:** The same solution can cost 100 hours per client or 1 minute per client depending on delivery format. Most businesses default to one format without considering the full menu. This step surfaces all options so you can choose optimally in Step 5.

Mark Step 4 complete in TodoWrite.

---

### Step 5: Trim and Stack (Offer Optimization)

This step has two sub-parts: first trim the list to the optimal components, then stack them into the final offer with assigned values.

#### Step 5a: Trim — Apply the Cost-Value Filter

**ACTION:** Take the full list of delivery vehicles from Step 4 and apply a two-axis filter:

**The cost-value 2x2:**

```
                    HIGH VALUE
                         │
      KEEP ──────────────┼────────────── KEEP
  (low cost,             │           (high cost,
   high value)           │            high value)
                         │
LOW COST ────────────────┼──────────────── HIGH COST
                         │
      REMOVE ────────────┼────────────── REMOVE FIRST
  (low cost,             │           (high cost,
   low value)            │            low value)
                         │
                    LOW VALUE
```

**Remove first:** High cost, low value items — these drain resources without meaningfully moving the buyer's perceived value.

**Remove second:** Low cost, low value items — these add complexity without payoff and dilute the offer by making it look padded.

**Keep:** Both categories of high-value items:
- Low cost, high value = the best components in the offer. Prioritize these. Examples: templates, guides, recorded videos, automated systems — created once, delivered infinitely.
- High cost, high value = keep if the cost is acceptable at your scale, or if they are essential to the dream outcome and no lower-cost alternative exists. Reserve high-cost, high-touch components (1-on-1 sessions, DFY services) for premium tiers or use them sparingly.

**How to evaluate "high value":** Ask which components most directly:
1. Increase the customer's financial outcome
2. Increase their confidence they will succeed
3. Reduce the effort and sacrifice required
4. Reduce the time to first result

**The fulfillment imbalance check (AP-10):** After filtering, ask: "Can I deliver this profitably at 50 clients? 200?" If no, restructure high-cost components into scalable formats. Bias toward "one-to-many" components (videos, tools, templates, guides) — created once, delivered infinitely, highest value-to-cost ratio in the offer.

Mark Step 5a complete in TodoWrite.

#### Step 5b: Stack — Build the Final Offer Bundle

**ACTION:** Take the trimmed components and assemble them into a final offer bundle.

**Format:** For each component write: (1) the problem it solves, (2) a compelling outcome-oriented name (not a format description — "Foolproof Bargain Grocery System" beats "Grocery Guide" — see `offer-naming-magic-formula`), (3) perceived value — what a motivated buyer would pay to solve only this problem standalone, (4) the delivery vehicles from Step 4.

**Final stack format:**

```
OFFER COMPONENT LIST
─────────────────────────────────────────────────────
Problem solved → Named component → Perceived value
─────────────────────────────────────────────────────
[Problem 1] → [Component Name 1] ........... $[XXX]
[Problem 2] → [Component Name 2] ........... $[XXX]
[Problem 3] → [Component Name 3] ........... $[XXX]
...
─────────────────────────────────────────────────────
TOTAL PERCEIVED VALUE:              $[total stacked]
YOUR PRICE:                         $[price]
VALUE-TO-PRICE RATIO:               [ratio]:1
─────────────────────────────────────────────────────
```

**The grand slam threshold:** The value-to-price ratio should feel almost unreasonable to the buyer. 4:1 is a floor; 7:1–10:1 is common in well-structured offers. The bundle must accomplish three things: (1) solve *all* perceived problems — missing one can be the single reason someone doesn't buy, (2) give you conviction that what you sell is one-of-a-kind, (3) make direct price comparison to competitors impossible.

**WHY:** The stacked offer shifts the buyer's decision from "is this worth the price?" to "which of these problems am I willing to let stay unsolved?" — a fundamentally easier sales conversation.

Mark Step 5b complete in TodoWrite. Mark Step 7 (final output) in progress.

---

### Final Output: The Offer Document

After completing all steps, produce a clean offer document in this format:

```
OFFER: [Working title — will be refined with offer-naming-magic-formula]
Target customer: [who they are and their starting situation]
Dream outcome: [specific result + timeframe]

─────────────────────────────────────────────────────────────────────
WHAT THEY GET
─────────────────────────────────────────────────────────────────────

[Component 1 name]: [one-sentence description of what it does]
  Solves: [problem from Step 2]
  Consists of: [delivery vehicles]
  Perceived value: $[amount]

[Component 2 name]: [one-sentence description]
  Solves: [problem]
  Consists of: [delivery vehicles]
  Perceived value: $[amount]

[... all components]

─────────────────────────────────────────────────────────────────────
TOTAL PERCEIVED VALUE: $[stacked total]
PRICE: $[price]
VALUE-TO-PRICE MULTIPLE: [X]:1
─────────────────────────────────────────────────────────────────────

NEXT STEPS:
→ Guarantee: guarantee-design-and-selection (reduces risk perception, boosts Driver 2)
→ Bonuses: bonus-stacking-system (present components as bonuses to increase perceived value)
→ Scarcity/urgency: scarcity-and-urgency-tactics (add ethical urgency to accelerate decision)
→ Name: offer-naming-magic-formula (turn the working title into a compelling, memorable name)
```

**HANDOFF TO HUMAN:** Present the completed offer document. Ask: "Does this capture all the problems your customer faces? Are there obstacles we haven't solved yet? The goal is for a prospect to read this list and have no remaining reasons to say no."

Mark Step 7 complete in TodoWrite.

---

## Examples

### Example 1: Agency Comparison — Commodity vs. Grand Slam (Before/After)

This example illustrates the financial transformation from a commoditized offer to a differentiated one, using identical advertising spend.

**The scenario:** A lead generation agency serving brick-and-mortar businesses. Two versions of the same underlying service — same work, same team, same ad budget.

**Commodity offer (price-driven, "race to the bottom"):**
> "$1,000 down, then $1,000/month retainer for agency services."

The pitch is: "You pay us. We work. Maybe you get results. Maybe you don't."

This is a reasonable offer, but it is identical to every other agency. The client can compare it directly to 50 competitors. The pressure to match the cheapest competitor is permanent.

**Grand Slam Offer (value-driven, incomparable):**
> "Pay one time. No recurring fee. No retainer. Just cover ad spend. I'll generate and work your leads. Only pay me if people show up. I guarantee 20 clients in month one, or next month is free. Plus: daily sales coaching, tested scripts, tested price points, sales recordings — and the entire industry playbook, free."

This offer cannot be compared to the commodity offer. The decision is not "which agency is cheaper?" but "do I want these 20 guaranteed clients or not?"

**Results at the same $10,000 ad spend:**

| Metric | Commodity | Grand Slam | Change |
|--------|-----------|------------|--------|
| Response rate | 0.013% | 0.033% | 2.5x more respond |
| Appointments booked | 40 | 100 | Result |
| Show rate | 75% | 75% | Unchanged |
| Closing % | 16% | 37% | 2.3x more close |
| Sales closed | 5 | 28 | Result |
| Price | $1,000 | $3,997 | 4x higher price |
| Total collected | $5,000 | $112,000 | 22.4x more cash |
| Return on ad spend | 0.5:1 | 11.2:1 | Get paid to acquire customers |

**Breakdown:** Same eyeballs. 2.5x more respond (compelling offer). 2.3x more close (value is obvious). 4x higher price (no comparison point). 2.5 × 2.3 × 4 = **22.4x more cash**. The fulfillment is the same. Only the offer structure changed.

---

### Example 2: Gym Owner — Full 5-Step Walkthrough

This is the complete process applied to a real business that went from failing to sell a $99/month bootcamp to successfully selling a $599 bundle worth $4,351 in perceived value.

**Starting situation:** Gym owner can't sell $99/month memberships. "LA Fitness is $29/month. This is expensive." Even free trials failed.

#### Step 1: Dream Outcome

Realization: "I'm not selling a gym membership. I'm not selling the flight. I'm selling the vacation."

Dream outcome: **Lose 20 pounds in 6 weeks.**
- Big dream outcome: lose 20 pounds
- Time component: 6 weeks

#### Step 2: Problems List (partial, illustrative)

For "buying healthy food":
1. Hard, confusing, won't like it
2. Takes too much time
3. Expensive
4. Unsustainable (family needs, travel)

For "cooking healthy food":
1. Hard, time-consuming, confusing
2. Takes too much time
3. Expensive and not worth it
4. Unsustainable; family conflicts; travel

For "exercising regularly":
1. Hard, confusing, intimidating
2. Will injure myself
3. Too time-consuming
4. Don't know what to do; will plateau

For "sticking with it":
1. Will fall off when life gets hard
2. Embarrassing to be seen at the gym
3. No one keeps me accountable

For "social situations":
1. Can't eat out without ruining progress
2. Feels left out at social events

#### Step 3: Solution Statements (partial)

- Buying food is hard → How to buy healthy food fast, easy, cheaply
- Cooking takes too long → How to cook healthy meals in under 5 minutes
- Exercise is confusing → Easy-to-follow exercise system adjusted to your exact needs
- Sticking with it is hard → System that works without your permission, even for people who hate the gym
- Can't eat out → How to eat out 100% of the time and still hit your goal

#### Step 4: Delivery Vehicles (trimmed selection)

- 1-on-1 Nutrition Orientation (explain the full system)
- Recorded grocery store walkthrough video
- DIY Grocery Calculator
- Pre-made weekly grocery list for each plan
- Grocery Buddy System (pair clients together)
- Pre-made Instacart lists for one-click delivery
- Meal prep instructions + Meal prep calculator
- Personalized meal plan
- 5-minute meal guides (breakfast, lunch, dinner)
- Family size meal options
- Fat-burning workouts calibrated to individual needs
- Travel eating and workout blueprint
- Accountability system (check-ins, community)
- Eating-out guide for restaurants

#### Step 5: Final Stacked Offer

| Problem solved | Named component | Perceived value |
|----------------|-----------------|----------------|
| Buying food | Foolproof Bargain Grocery System — saves hundreds/month, takes less time than your current routine | $1,000 |
| Cooking | Ready-in-5-Minute Busy Parent Cooking Guide — eat healthy even with no time, get 200 hours/year back | $600 |
| Eating | Personalized "Lick Your Fingers Good" Meal Plan — easier to follow than eating what you used to cheat with | $500 |
| Exercise | Fat Burning Workouts Proven to Burn More Fat Than Doing It Alone — calibrated so you never plateau or risk injury | $699 |
| Traveling | Ultimate Tone-Up-While-You-Travel Eating and Workout Blueprint — amazing workouts with no equipment | $199 |
| Accountability | "Never Fall Off" Accountability System — works without your permission, even for people who hate coming to the gym | $1,000 |
| Social eating | "Live It Up While Slimming Down" Eating Out System — freedom to eat out and live life without feeling like the odd man out | $349 |
| **TOTAL VALUE** | | **$4,351** |
| **PRICE** | | **$599** |
| **VALUE MULTIPLE** | | **7.3:1** |

**Result:** The gym went from failing to sell $99/month memberships to selling $599 bundles. The facilities using this system eventually sold the same bundle for $2,400–$5,200 as they refined and added components over time.

---

## Key Principles

- **The offer is the product, not the service.** A commodity business does the same work as a Grand Slam Offer business. The fulfillment is the same. What changes is how that work is packaged, named, and valued. Packaging determines pricing — not quality, effort, or years of experience.

- **Solve every perceived problem, not just the obvious ones.** One unsolved obstacle can be the single reason someone doesn't buy. The goal is to design an offer where the prospect runs out of objections before they run out of reasons to say yes. If you find yourself insisting prospects must handle a problem themselves, you are leaving sales on the table.

- **The divergent phase must stay divergent.** Steps 2–4 are about generating the maximum possible list. Filtering is for Step 5. Self-censoring during generation produces a mediocre offer with the obvious components. The best offer components often emerge from pushing past the first ten ideas.

- **Perceived value is not cost plus margin.** Assign values based on what the market charges to solve that problem, or what the outcome is worth to the buyer — not how long the component takes to create. A template built in 2 hours that solves a $500 problem is a $500 component.

- **One-to-many components are the profit engine.** The offers with the best economics are built primarily from components that are created once and delivered infinitely: recorded training, automated tools, templates, reference guides, community systems. High-cost, high-touch components (1-on-1 sessions, DFY delivery) belong in the stack only where they are irreplaceable or in premium tiers.

- **Escaping commodity pricing is the entire point.** When your offer cannot be directly compared to a competitor's, you control the pricing conversation. When it can be compared, you will always be pressured to match the cheapest option in the market.

- **Build first, optimize later.** Bias the first version toward over-delivery. Create cash flow, serve clients, and learn what they value most. Then replace high-cost components with lower-cost alternatives. Optimization without a proven offer is premature.

## References

- For auditing the perceived value of the offer you just built: `value-equation-offer-audit`
- For designing a guarantee that boosts perceived likelihood of achievement: `guarantee-design-and-selection`
- For presenting selected offer components as bonuses to increase perceived value: `bonus-stacking-system`
- For adding ethical scarcity and urgency without manipulation: `scarcity-and-urgency-tactics`
- For turning the working offer title into a compelling, memorable name: `offer-naming-magic-formula`
- For setting and testing the right price for the completed offer: `premium-pricing-strategy`
- Source: *$100M Offers*, Alex Hormozi, Chapters 8–10, pages 97–127 (offer creation process) and pages 43–47 (agency commodity vs. Grand Slam comparison)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — 100M Offers by Unknown.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-value-equation-offer-audit`
- `clawhub install bookforge-target-market-selection`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
