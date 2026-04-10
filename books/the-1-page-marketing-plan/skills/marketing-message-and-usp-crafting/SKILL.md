---
name: marketing-message-and-usp-crafting
description: "Use this skill to craft a differentiated Unique Selling Proposition
  (USP), write a Problem/Solution/Proof elevator pitch, and engineer headlines that
  activate the 5 core emotional buying motivators. Triggers when a user asks to write
  a USP, unique selling proposition, craft a marketing message, build an elevator
  pitch, differentiate from competitors, answer 'why buy from me', write headlines,
  write copywriting or marketing copy, fix positioning, escape me-too marketing,
  stop competing on price, apply emotional marketing, target fear/love/greed/guilt/
  pride in copy, identify pain points for messaging, write sales copy, or fill
  square #2 of the 1-Page Marketing Plan canvas. Also activates for 'quality and
  great service as USP', 'we offer the best service', 'how do I stand out',
  'nobody knows what makes us different', 'my ads are not working', or similar
  messaging and positioning questions."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/marketing-message-and-usp-crafting
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan"
    authors: ["Allan Dib"]
    chapters: [2]
tags:
  - marketing
  - copywriting
  - messaging
  - positioning
  - usp
  - small-business
depends-on:
  - target-market-selection-pvp-index
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: >
        Target market output (target-market.md from target-market-selection-pvp-index)
        OR a description of the business's primary customer segment and their top
        pain points, if target-market.md is not available.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set — business description and target market notes in markdown.
    No code execution required.
discovery:
  goal: >
    Help small business owners craft a marketing message that compels their target
    market to act — producing a USP statement, a Problem/Solution/Proof elevator
    pitch, and 3–5 headline drafts — all in a single marketing-message.md deliverable.
  tasks:
    - "Gather target market and pain point context"
    - "Draft USP candidates and select the strongest one using the logo-swap test"
    - "Build an elevator pitch using the Problem/Solution/Proof formula"
    - "Select one or more emotional buying motivators from the 5-motivator taxonomy"
    - "Draft 3–5 headlines that activate those motivators"
    - "Audit all outputs against anti-patterns (quality/service USP, price USP,
       me-too positioning)"
    - "Write marketing-message.md with the complete message system"
  audience:
    roles:
      - small-business-owner
      - solopreneur
      - entrepreneur
      - freelancer
      - startup-founder
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User wants to write or improve a USP"
      - "User is crafting a marketing message or sales copy"
      - "User wants to differentiate from competitors"
      - "User is writing headlines or ad copy"
      - "User is filling square #2 of the 1-Page Marketing Plan"
      - "User wants to stop competing on price"
    prerequisites:
      - "Primary target market known (from target-market-selection-pvp-index or
         provided directly)"
    not_for:
      - "Enterprise brand strategy requiring market research agencies and large
         positioning studies"
      - "Businesses without any product or service yet (message cannot precede offer)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 100
      baseline: 36
      delta: 64
    tested_at: "2026-04-09"
    eval_count: 1
    assertion_count: 14
    iterations_needed: 1
---

# Marketing Message and USP Crafting

A structured process for small business owners to stop blending in and start
standing out. Produces a Unique Selling Proposition (USP), a
Problem/Solution/Proof elevator pitch, and emotionally-engineered headline
drafts — the complete message system for square #2 of the 1-Page Marketing
Plan canvas.

Most small business ads are interchangeable: company name, logo, laundry list
of services, claim of "best quality and service," offer of a free quote. Swap
the name and logo — it could be any competitor. This skill eliminates that
failure by forcing explicit answers to the two questions every prospect asks
silently: "Why should I buy?" and "Why should I buy from you?"

---

## When to Use

Use this skill AFTER selecting your primary target market (via
`target-market-selection-pvp-index` or direct user input). Marketing message
depends entirely on knowing exactly who you are speaking to — the same business
must write completely different copy for different customer segments.

Also use it when:
- An existing business is getting price-shopped and doesn't know why
- Current ads produce no response or "me too" comparison shopping
- A business owner can't answer "What makes you different?" with a single clear
  sentence
- A new campaign is being built from scratch

Do NOT use this skill as a substitute for offer construction (pricing, bonuses,
guarantees). Message comes before offer in execution order, but the offer itself
is a separate skill.

---

## Context and Input Gathering

### Required (must have before proceeding)

**IF target-market.md exists** (output of `target-market-selection-pvp-index`):
  → Read it. Extract: primary target segment name, customer avatar, dominant
    emotion, biggest fears, daily frustrations, what they secretly want.

**IF target-market.md does not exist**:
  → Ask the user directly:
  1. "Who is your primary target customer? Be specific — describe a type of
     person, not a broad demographic."
  2. "What is the single biggest problem or frustration they face that your
     business can solve?"
  3. "What outcome do they actually want — not the feature you provide, but
     the result they are trying to achieve?"

Also gather:
- What the business sells (product/service description)
- 2–3 nearest competitors and what makes each of them different (or indistinct)
- Any existing USP attempts, taglines, or elevator pitch (to diagnose failures)

### Sufficiency check

You have enough to proceed when you can name: (1) who the customer is,
(2) what pain they are living with right now, and (3) what specific outcome the
business delivers. If any of these three is vague, ask before proceeding.

---

## Process

### Step 1: Identify the result the customer is actually buying

Ask: "What is the prospect buying — not the product or service, but the result
or outcome they want to achieve?"

A printer is not selling business cards. They are selling "more customers
walking through the door." A security system company is not selling cameras.
They are selling "the feeling that your family is safe when you are not home."
A management consultant is not selling advice. They are selling "operations
that scale without breaking."

Write a one-sentence outcome statement: "[Target customer] wants [specific
outcome], not [product/service feature]."

**WHY:** Selling features turns prospects into price shoppers who compare
specifications across competitors. Selling outcomes positions you as a problem
solver and pain reliever. Prospects are willing to pay far more for a cure than
for a feature — the same way someone with a splitting headache will pay double
or triple for pain relief without shopping around.

### Step 2: Draft 3–5 USP candidates

Answer these two questions for the business, in clear and quantifiable terms:

1. Why should they buy? (What problem exists if they do not act?)
2. Why should they buy from you? (What do you offer that no competitor offers
   in the same way — in the product, delivery, packaging, support, guarantee,
   or experience?)

For each candidate USP, write a single sentence that a prospect could read in
three seconds and immediately understand what is different and why it matters.
The uniqueness does not need to be in the product itself. It can be in:
- How it is delivered (e.g., installed and configured in your home vs. box
  in bag)
- How it is supported (e.g., dedicated account manager vs. support ticket queue)
- How it is packaged (e.g., flat monthly fee vs. hourly billing)
- What guarantee backs it (e.g., results in 30 days or full refund)
- What experience surrounds it (e.g., the CD Baby confirmation email)

**WHY:** Very few products are truly unique. The uniqueness must come from
somewhere — packaging, delivery, experience, or guarantee are all valid.
Generating 3–5 candidates prevents anchoring on the first idea, which is
usually the most generic.

### Step 3: Apply the logo-swap test to each candidate (gate)

For each USP candidate, ask: "If I removed the business name and logo from this
statement and placed it on a competitor's website, would it still make sense?"

**IF YES** (it passes to any competitor): the USP has failed. It is a "me too"
statement. Return to Step 2 and generate a more specific candidate.

**IF NO** (it could only belong to this specific business): the USP is viable.
Move to Step 4.

Common failures of the logo-swap test:
- "We provide quality service at competitive prices." → Fails. Any competitor
  can claim this.
- "We have 20 years of experience." → Fails. Generic credential.
- "We are locally owned and operated." → Fails. Every local competitor qualifies.
- "We offer free consultations." → Fails. Any competitor can match this tomorrow.

**WHY:** The logo-swap test is the single fastest diagnostic for a weak USP.
If a statement is interchangeable, it gives the prospect no reason to choose
you — they default to price comparison, which is the worst competitive position
for a small business. There will always be someone willing to go out of business
faster than you by discounting further. The only escape is a differentiated
position.

### Step 4: Select and sharpen the strongest USP

From the candidates that passed the logo-swap test, select the one that:
- Targets the most emotionally relevant pain or desired outcome for the avatar
- Is the hardest for competitors to copy quickly
- Can be stated in a single clear sentence without jargon

Sharpen it by:
- Making it specific: replace vague words with numbers, timeframes, or
  observable outcomes
- Making it outcome-focused: rewrite any feature language as a result statement
- Making it prospect-facing: use "you" language, not "we" language

**WHY:** Specificity is credibility. "We save small businesses an average of
12 hours per week on payroll administration" is more convincing than "We save
you time." Specific claims are harder to refute and easier to remember.

### Step 5: Build the elevator pitch using Problem/Solution/Proof

Use the formula: **"You know how [problem]? Well, what I do is [solution].
In fact, [specific proof or result example]."**

Fill each component:

**Problem:** Describe the pain the target market is currently experiencing.
Use their language. The problem should feel immediate and real — something they
are living with today, not a future risk they might face.

**Solution:** Describe the outcome you deliver, not the features or mechanism.
Focus on the transformation: before state → after state.

**Proof:** A single specific result that happened for a real customer. Include
a number, a timeframe, or a named outcome. "In fact, just last week a client of
mine..." is more compelling than "Our clients have seen great results."

The full pitch should be deliverable in 30–90 seconds. It is both a networking
tool and a clarity mechanism — if you cannot say it in 90 seconds, your message
is not clear enough to use in any marketing.

**WHY:** Bad elevator pitches are product-focused and self-focused — they talk
about the business, not the prospect. The Problem/Solution/Proof structure
forces customer-focus at every step. Prospects respond when they hear their own
situation described accurately; they tune out when they hear a business
describe itself.

### Step 6: Select emotional buying motivator(s) for headlines

Identify which of the 5 core emotional buying motivators are most active for
this target avatar:

1. **Fear** — especially fear of loss, fear of missing out, fear of a bad
   outcome. The most powerful motivator. The amygdala (the brain's survival
   center) processes threats first. "Fear of loss" consistently outperforms
   "desire for gain" in response rates.

2. **Love** — desire for connection, relationships, family protection,
   belonging. Activates when the product protects or enhances something the
   prospect loves deeply.

3. **Greed** — desire for more: more money, more time, more opportunity, more
   of what they value. "More for me" at lower cost or higher return.

4. **Guilt** — not doing right by family, employees, self, or others.
   Underutilized but powerful for audiences with clear obligations (parents,
   employers, professionals with a duty of care).

5. **Pride** — status, exclusivity, membership in an elite group, being seen
   as smart or successful. "People like you use this."

Select the 1–2 motivators that best match the avatar's dominant emotional state
(from the customer avatar built in `target-market-selection-pvp-index`). If the
avatar is not available, infer from the problem description.

**WHY:** People buy with emotion and justify with logic afterward. Copy that
fails to activate at least one of these five motivators is timid and
ineffective — it generates polite indifference, not action. Identifying the
correct motivator before writing headlines prevents generic copy that "sounds
professional" but triggers nothing.

### Step 7: Draft 3–5 headlines

Write 3–5 headline variants, each activating the selected motivator(s). A
headline's job is not to describe the product — it is to grab attention and
compel the reader to keep reading. Think of it as the ad for the ad.

Headline structures that consistently work (adapt to the business):
- Direct pain: "Attention [target market]: Are You Still [painful situation]?"
- Specific result: "How [business type] Clients [specific result] in [timeframe]"
- Fear of loss: "The [N] Most Expensive [mistakes/errors] [target market] Make
  — And How to Avoid Them"
- Social proof + fear: "Why [N] [target market] in [location] Have Switched to
  [solution]"
- Enemy in common: "[Problem] Is Costing You [specific loss] — Here's What
  to Do About It"
- Pride/exclusivity: "For [target market] Who Refuse to [accept painful status
  quo]"

Use emotionally charged words: Free, You, Save, Results, Proven, Money, New,
Easy, Safety, Guaranteed, Discovery. One word substitution can shift response.

**WHY:** The headline is read first and determines whether anything else gets
read. A weak headline means zero return on all other copy effort. Writing 3–5
variants allows testing — only real response data reveals which motivator
resonates most with this specific audience.

### Step 8: Audit all outputs against anti-patterns

Before finalizing, check each element against these failure modes:

| Anti-pattern | Test | Correct action |
|---|---|---|
| Quality/service USP | "Is 'quality' or 'great service' in the USP?" | Replace with specific, measurable differentiator |
| Price USP | "Does the USP rely on being cheapest?" | Shift to value, outcome, or experience-based differentiation |
| Me-too positioning | Does the logo-swap test fail? | Return to Step 3 |
| Feature language | Does copy describe specs rather than outcomes? | Rewrite as result statements |
| Prevention framing | Is copy selling future safety rather than current pain? | Reframe to address existing pain |
| Self-focused | Does copy say "we" more than "you"? | Flip to prospect perspective |

**WHY:** Anti-patterns are the default — they feel natural because they are how
most businesses talk about themselves. The audit step converts the instinctive
output into direct-response copy. Skipping this step typically means the final
document contains at least one critical failure that renders the whole message
generic.

### Step 9: Write marketing-message.md

Compile all outputs into a single deliverable. Save it as `marketing-message.md`
in the user's working directory.

**WHY:** Square #2 of the 1-Page Marketing Plan must be documented. Without a
written record, the message reverts under pressure to familiar but ineffective
patterns. The document also serves as the creative brief for all downstream
marketing: ads, landing pages, email sequences, and sales scripts.

---

## Inputs

| Input | Format | Required |
|-------|--------|----------|
| target-market.md (from target-market-selection-pvp-index) | .md | Preferred |
| Primary target segment + top pain points | direct user input | If no target-market.md |
| Business description (product/service) | text | Yes |
| Existing USP attempts or taglines | text | Recommended |
| 2–3 nearest competitors | text | Recommended |

---

## Outputs

Primary output: `marketing-message.md`

```markdown
# Marketing Message: [Business Name]

## Unique Selling Proposition

**USP Statement:**
[Single sentence. Outcome-focused. Passes logo-swap test.]

**Logo-swap test result:** PASS — [brief rationale for why this could only
belong to this business]

**Why it works:** [1–2 sentences connecting USP to target avatar's dominant
pain or desired outcome]

---

## Elevator Pitch (Problem/Solution/Proof)

**Problem:**
[1–2 sentences. Target market's current pain, in their language.]

**Solution:**
[1–2 sentences. Outcome delivered, not features provided.]

**Proof:**
[1 sentence. Specific result with a number, timeframe, or named outcome.]

**Full pitch (30–90 seconds):**
"You know how [problem]? Well, what I do is [solution]. In fact, [proof]."

---

## Headline Drafts

**Primary motivator(s) selected:** [Fear / Love / Greed / Guilt / Pride]
**Rationale:** [1 sentence connecting motivator to avatar's dominant emotion]

1. [Headline 1]
2. [Headline 2]
3. [Headline 3]
4. [Headline 4 — optional]
5. [Headline 5 — optional]

**Recommended first test:** Headline [N] — [brief reason]

---

## Anti-Pattern Audit

| Check | Result |
|-------|--------|
| Quality/service USP | CLEAR |
| Price USP | CLEAR |
| Logo-swap test | PASS |
| Feature vs. outcome language | CLEAR |
| Pain vs. prevention framing | CLEAR |
| Prospect-focused ("you" > "we") | CLEAR |

---

_Square #2 of the 1-Page Marketing Plan canvas: filled._
```

---

## Key Principles

**1. Logo-swap test is the gate.**
If your marketing message could belong to any competitor with a name swap, it
has failed — regardless of how professional it sounds. Every USP candidate must
pass this test before moving forward.

**2. Niching makes price irrelevant.**
A specialist commands higher fees than a generalist. A heart surgeon is not
compared to a general practitioner on price. The narrow niche that feels risky
is almost always more profitable than the broad positioning that feels safe.

**3. Emotional response drives purchasing; logic justifies afterward.**
"I bought the Porsche for safety and reliability." Sell to the emotion first.
Copy that leads with facts and specifications is selling to the wrong brain.

**4. Sell to existing pain, not future prevention.**
People pay far more for a cure than for prevention. Someone with a splitting
headache pays double without shopping around. Target the pain your prospect is
carrying today — not the risk they might face tomorrow.

**5. Selling features turns prospects into price shoppers.**
Once a prospect can compare you on a feature, they compare you on price.
Outcomes — "12 hours saved per week" — cannot be commodity-shopped the way
features can. Always translate features into results.

**6. Confusion kills sales silently.**
A confused prospect does not ask for clarification — they leave. Choose clarity
over cleverness in every element of your message.

---

## Examples

### Example 1: Wedding photographer (commodity service, emotional niche)

**Context:** Photographer serves four markets. PVP analysis selected family
portrait photography as primary. Avatar: Sarah, 34, new parent. Dominant
emotion: anticipation + anxiety about not capturing the moment perfectly.

**Weak USP (fails logo-swap):**
"Professional photography for families who want beautiful memories." — Any
photographer can claim this. Fails.

**Strong USP (passes):**
"Family portraits so vivid your kids will fight over who gets to hang them —
guaranteed or the session is free."
— Specific emotional outcome (kids fighting over prints = the photo is loved),
with a guarantee that removes risk. Could not belong to a competitor without
copying the exact guarantee.

**Elevator pitch:**
"You know how most family portrait photographers give you a USB drive of 300
photos and you pick through them yourself, then order prints from a box store
that look nothing like the preview? Well, what I do is guide the whole
experience from the session through to framed prints on your wall. In fact, my
last client told me her daughter cried when she saw her portrait and asked if
she could have it in her bedroom."

**Motivator selected:** Love (protecting and celebrating family)

**Headline drafts:**
1. "The Family Portrait Your Kids Will Actually Ask to Hang on Their Wall"
2. "Warning: This Photo Session May Cause Arguments Over Who Gets the Best Shot"
3. "For [City] Families Who Refuse to Settle for Generic Studio Portraits"
4. "What If Your Family Portrait Was So Good Your Kids Showed It Off at School?"

---

### Example 2: SaaS project management tool for agencies

**Context:** Digital agencies with 5–20 person teams. Avatar: agency owner
overwhelmed by missed deadlines. Dominant emotion: fear of losing clients.

**Weak USP (fails logo-swap):**
"Project management software that keeps your team organized and on track." —
Every competitor says this. Fails.

**Strong USP (passes):**
"The project management platform built exclusively for agencies that can't
afford to miss another client deadline — with automated client status updates
so you stop being the bottleneck."
— Specificity (agencies only, automated updates, bottleneck pain) prevents
any competitor from claiming this without copying the exact position.

**Elevator pitch:**
"You know how agency owners spend half their day answering client emails asking
'where are we on the project?' — while their team is actually making progress?
Well, what we do is send automated plain-English status updates to your clients
every Friday so you never have to write that email again. In fact, one of our
customers went from spending 8 hours a week on client communication to under
30 minutes — without a single client noticing the change."

**Motivator selected:** Fear (losing clients due to communication failures)

**Headline drafts:**
1. "Agency Owners: How Many Clients Have You Lost to Missed Deadlines This Year?"
2. "The Hidden Cost of Being Your Agency's Human Status Update System"
3. "Finally: Client Communication That Runs Itself — Even When You're in a Sprint"
4. "For Agencies Tired of Doing Great Work and Still Getting Blamed for Poor
   Communication"

---

### Example 3: Independent bookkeeper for small retail businesses

**Context:** Retail business owners with 1–5 staff. Avatar: shop owner doing
her own books at 11 PM. Dominant emotion: guilt + fear of getting it wrong.

**Weak USP (fails logo-swap):**
"Accurate, reliable bookkeeping for small businesses at affordable rates." —
Generic. Fails.

**Strong USP (passes):**
"Monthly bookkeeping for retail owners — done by the 5th of every month,
with a plain-English one-page summary you can actually read, or your money back."
— The deadline (5th of month), the deliverable format (one-page plain-English),
and the guarantee together create a position no generic competitor holds.

**Elevator pitch:**
"You know how retail shop owners end up doing their own books at 11 PM on a
Sunday because they can't trust that their bookkeeper understands their
inventory situation? Well, what I do is handle everything and send you a
one-page summary every month — in plain English, no jargon — by the 5th.
In fact, one of my clients told me it was the first time in three years she
felt like she actually understood her own numbers."

**Motivator selected:** Guilt + Fear

**Headline drafts:**
1. "Are You Still Doing Your Own Bookkeeping at 11 PM on Sundays?"
2. "What Would You Do With 6 Extra Hours Every Month?"
3. "Free Report: The 5 Bookkeeping Mistakes Most Retail Owners Make at Tax Time"

---

## References

- `target-market-selection-pvp-index/SKILL.md` — Dependency. Read before this
  skill if the primary target market has not been selected.
- `.meta/book-profile.json` — Full book metadata and chapter mappings
- `.meta/research/hunter-report.md` — sk-03 entry: messaging and USP content
  identified across the chapter
- Source: Ch 2 "Crafting Your Message," pp 59–79 (USP, elevator pitch) and
  pp 92–102 (emotional motivators, headlines, copywriting), Allan Dib

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-target-market-selection-pvp-index`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
