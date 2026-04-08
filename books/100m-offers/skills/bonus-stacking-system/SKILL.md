---
name: bonus-stacking-system
description: Build and present a bonus stack that makes your core offer feel irresistible by applying an 11-point bonus quality checklist, a before/after-objection deployment sequence for one-on-one sales, and a 3-step partner bonus system that sources free high-value bonuses from adjacent businesses. Use this skill when your grand slam offer is drafted and you need to increase perceived value without discounting the price; when prospects stall at close and you need a structured way to layer bonuses against their specific objections; when you want to source third-party bonuses at zero cost and turn them into affiliate revenue; or when you need a complete bonus stack document with named bonuses, assigned values, and a presentation sequence ready for use in sales conversations.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/100m-offers/skills/bonus-stacking-system
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: 100m-offers
    title: "$100M Offers: How To Make Offers So Good People Feel Stupid Saying No"
    authors: ["Alex Hormozi"]
    chapters: [14]
tags: [bonuses, offers, value-creation, sales]
depends-on: [grand-slam-offer-creation, value-equation-offer-audit]
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Completed grand slam offer or deliverables list from the grand-slam-offer-creation skill. Optionally: a list of prospect objections."
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Works from a finalized offer and a list of deliverables. Output: a bonus stack document with named bonuses, assigned values, and a presentation sequence."
discovery:
  goal: "Produce a complete bonus stack that eclipses the value of the core offer, addresses every anticipated objection, and includes at least one partner bonus sourced at zero cost."
  tasks:
    - "Audit every deliverable against the 11-point bonus quality checklist"
    - "Name each bonus with a benefit in the title"
    - "Assign a dollar value to each bonus with justification"
    - "Order bonuses by impact: strongest first, objection-busters held in reserve"
    - "Identify adjacent businesses and draft partner bonus outreach"
    - "Document the before/after-objection deployment sequence for sales conversations"
  audience: "beginner-to-intermediate entrepreneurs building or refining a premium offer"
  when_to_use: "When a core offer is drafted and needs bonus stacking to increase conversion, or when prospects are stalling at close and bonuses are needed to dissolve objections"
  environment: "A finalized offer with at least one deliverable and a known price point."
  quality: placeholder
---

# Bonus Stacking System

## When to Use

Your core offer exists — you know what you deliver and at what price — but conversion is lower than it should be, or you sense the offer feels thin relative to its price. This skill applies when:

- You have completed the grand slam offer framework and are now ready to present it in a way that makes the price feel small compared to the value
- You are preparing for a sales conversation and want bonuses ready to deploy if a prospect objects
- You want to increase perceived value without cutting your price (discounting is always the wrong move — it trains buyers that your price is negotiable)
- You want to source partner bonuses from adjacent businesses at zero cost and potentially earn affiliate commissions from them
- You need a written bonus stack document — named bonuses, assigned values, presentation sequence — that you or a salesperson can use consistently

**The core pattern:** A single offer presented as one thing is worth less than the same offer broken into its named component parts and stacked as bonuses. Enumeration creates value. Prospects cannot value what they cannot see. Bonuses make the invisible visible, and each additional bonus expands the price-to-value gap until buying feels like the obvious choice.

Before starting, confirm you have:
- A completed offer with at least one deliverable (use `grand-slam-offer-creation` first if not)
- A price point anchored to the core offer
- A basic sense of what obstacles prevent your prospect from buying (use `value-equation-offer-audit` to identify these if needed)

---

## Context and Input Gathering

### Required Context

- **Deliverables list:** Every product, service, or outcome included in your current offer — this is raw material for your bonus stack. Many items you already deliver are invisible to the buyer and need only be named and valued.
- **Core offer price:** The price you will anchor at the start of the sales conversation. Bonuses expand value around this anchor; the anchor must be set first.

### Observable Context

If a draft offer document is provided, scan for:
- Deliverables buried inside service descriptions — these are candidates to be extracted and named as standalone bonuses
- Outcomes that are fast, easy, or done-for-the-buyer — these score high on the value equation (low effort/time = high value) and make strong bonuses
- Problems the buyer will encounter after purchasing that you could pre-solve — these become "next logical need" bonuses

### Default Assumptions

- If the deliverables list is empty → use the grand slam offer creation skill first; you cannot stack what you have not built
- If the buyer's objections are unknown → assume the three most common: time, effort, and a secondary problem they expect to hit after solving the main one
- If you are unsure whether an item belongs in the core offer or as a bonus → make it a bonus; the "wow factor" rule applies: if it is short but high quality or value, it reads as more impressive as a bonus than as an implied inclusion
- If no partner bonuses have been negotiated yet → complete Steps 1-3 first, then run Step 4 as a separate effort

### Sufficiency Check

You have enough to proceed when:
1. You have at least three distinct deliverables or outcomes to work with
2. You know your core offer price
3. You can name at least two anticipated buyer objections or obstacles

---

## Process

### Step 1 — Audit Every Deliverable Against the 11-Point Bonus Quality Checklist

Take each deliverable and score it. High-scoring items become named bonuses. Low-scoring items either stay as silent inclusions in the core offer or get improved before presenting.

For each deliverable, check:

1. **Always offer it.** Every deliverable should be visible. If you are delivering it anyway, name it and give it a value. Unnamed value is invisible value.
2. **Give it a benefit-in-the-title name.** "Sales Script" is a deliverable. "The 7-Figure Close Script That Eliminates Price Objections In Under 60 Seconds" is a bonus. The name does selling before you say a word.
3. **Connect it to the buyer's specific issue.** State how this bonus directly addresses their problem. Generic bonuses feel like filler. Specific bonuses feel like gifts.
4. **Explain what it is.** State clearly what the buyer receives: a checklist, a template, a video, a live session, a report. Ambiguity reduces perceived value.
5. **Explain how you discovered or created it.** Origin story creates credibility. "I built this after losing $200k so you don't have to" is worth more than "here's a checklist."
6. **Explain how it makes their life faster, easier, or lower effort.** This is the value equation in action: value rises as time-to-result drops and effort required drops. Always frame bonuses through this lens.
7. **Provide proof.** A stat, a past client result, or a personal experience. Proof converts a claimed value into a believed value.
8. **Paint the mental image.** Describe the buyer's life after using this bonus as if they have already experienced the benefit. Future pacing converts abstract value into felt value.
9. **Assign a price tag and justify it.** Every bonus needs a dollar value — not arbitrary, but defensible. "This normally costs $X because Y" is the minimum. If you sell this item separately, use that price. If you do not, price it at what it would cost to hire someone to produce the equivalent outcome.
10. **Address a specific objection or anticipated obstacle.** The best bonuses do not add value generically — they dissolve the specific reason the buyer hesitates. Map each bonus to a "I can't or won't succeed because..." belief and show why that belief is wrong.
11. **Solve the next logical need.** After the buyer succeeds with your core offer, what problem do they hit next? Bonuses that pre-solve that next problem extend the buyer's loyalty and remove a reason to look elsewhere.

**Bonus format upgrade — tools and checklists beat trainings.** A checklist or template requires less effort and time from the buyer than a course or training. Per the value equation, lower effort means higher value. Prefer deliverables that are immediately usable over deliverables that require the buyer to invest time learning. If you have training content, record it once, then create a checklist or swipe file that extracts the core action without requiring the buyer to watch it.

**Value eclipsing rule.** The total stated value of your bonuses should exceed the price of the core offer. This is not deception — it is psychology. When bonuses alone are worth more than the price, the core offer reads as if it were free. The buyer's subconscious also reasons: "If these are the extras, the main thing must be even more valuable." Both effects work in your favor.

**Scarcity and urgency amplifiers (optional, apply carefully):**
- **Scarcity version:** "These bonuses are only available through this program — they are never sold separately." Limits access, not time. Works when true.
- **Urgency version:** "If you join today, I will add [bonus X] valued at $1,000. I do this to reward people who act quickly." Limits window, not access. Only use real urgency; manufactured urgency destroys trust.

---

### Step 2 — Name, Value, and Order the Stack

With your audited bonuses, build the stack document:

**For each bonus, write one entry:**

```
Bonus Name: [Benefit-in-the-title name]
What it is: [One sentence — format + content]
Why it matters: [How it addresses their specific issue or obstacle]
How you created it: [Origin — cost you paid, experience it encodes]
What it does for them: [Faster/easier/lower effort — value equation framing]
Proof: [Stat, client result, or personal experience]
Assigned value: $[amount] — because [justification]
Objection it destroys: [Specific belief it refutes]
```

**Ordering rule:** Place the strongest, most emotionally resonant bonus first — it sets the standard for what follows. Order remaining bonuses by perceived value, descending. Hold two or three bonuses in reserve; these are your objection-busters deployed only if the prospect does not buy on first ask (see Step 3). The buyer does not know these exist until they are needed.

**Total value calculation:** Sum all bonus values. Confirm the total exceeds the core offer price. If it does not, either add more bonuses or create a partner bonus (Step 4) to close the gap.

---

### Step 3 — Deploy the Before/After-Objection Sequence in Sales Conversations

The deployment sequence differs depending on whether the buyer says yes or no on first ask.

**First ask — always ask for the sale before presenting bonuses.**
State the core offer and price. Ask for the sale. Do not volunteer bonuses before the prospect has responded. Offering bonuses before the ask signals that you lack confidence in your core price.

**If the prospect says yes:**
- Complete the transaction
- Then reveal the additional bonuses they are going to receive
- Frame this as a reward for their decision: "Now that you're in, here's everything else you're getting..."
- This creates a post-purchase "wow experience" that reinforces the buying decision and reduces buyer's remorse

**If the prospect does not buy:**
1. Identify the objection — the specific reason they are not buying. Do not guess; ask: "What's holding you back?"
2. Match a held-in-reserve bonus to that exact objection. The bonus should directly address the concern, not just add general value.
3. Present the bonus: "I understand [their concern]. I actually have something that addresses exactly that. I'm going to add [Bonus Name] — normally $X — for free. Does that make this feel fair?"
4. Ask again. Do not apologize. Adding a bonus is a move from strength — you are giving more, not retreating on price.
5. If they still object, identify the new objection and match another bonus. Repeat once more if needed.

**The reciprocity mechanism:** Humans struggle to refuse someone who has just given them something. Each bonus added to address an objection creates social pressure toward yes. The buyer must actively reject goodwill — a much harder psychological position than simply declining a straightforward offer.

**Never discount the core price.** Discounting teaches the buyer that your prices are always negotiable, which is permanently damaging. Adding bonuses to close a deal increases value without undermining price integrity. You remain in a position of strength.

---

### Step 4 — Build the Partner Bonus System

Partner bonuses are high-value additions to your offer sourced from adjacent businesses at zero cost to you. The partner gets free exposure to your buyers (their ideal prospects). You get valuable bonuses that may also generate affiliate commissions.

**The three-step partner bonus system:**

**Step A — Identify adjacent businesses.**
Ask: What does my customer need next, after they start working with me? What businesses serve that need? List every category — these are your partner targets. The only constraint: partners must not be direct competitors.

Example for a business coaching client: bookkeeper, attorney, email marketing software, ad agency, copywriter, paid traffic specialist, productivity app.

**Step B — Negotiate the exchange.**
Approach each business with the same framing: "I send you my highest-quality prospects — people who have already bought, are motivated, and need exactly what you offer. In exchange, you give my clients a free session, a discount, or access to your product as a bonus. You pay nothing. I pay nothing. My clients get more value."

Target outcomes (aim for one or both):
- A group discount or free access to give your buyers
- An affiliate commission paid to you for each client you refer

**Step C — Create a grand slam offer with each partner.**
Once a partner relationship is established, apply the same offer-building logic to the partner's product. Help them create a compelling framing for the bonus so it reads as high-value, not as a promotional filler item. A well-framed partner bonus is worth more than a poorly-framed internal bonus.

**Revenue math:** Your bonuses can become direct revenue streams. If your offer is $400 and you negotiate affiliate commissions from five partners, those commissions can exceed the $400 price. The buyer acquisition cost you already paid then generates additional profit from referrals — at zero incremental effort.

---

### Step 5 — Assemble the Final Bonus Stack Document

Write the complete stack as a deliverable you can use in sales conversations, sales pages, or handoff documents for a sales team.

**Structure:**

```
OFFER PRICE: $[amount]

CORE DELIVERABLE: [One-sentence description of what you deliver]

BONUS STACK:

Bonus 1: [Name] — Value: $[amount]
[Two-sentence description: what it is + what it does for them]

Bonus 2: [Name] — Value: $[amount]
[Two-sentence description]

[Continue for all bonuses]

TOTAL BONUS VALUE: $[sum]
TOTAL OFFER VALUE: $[core + bonuses]
YOU PAY: $[price]

OBJECTION RESERVE (do not present unless prospect declines first ask):
Reserve Bonus A: [Name] — deploys against: [specific objection]
Reserve Bonus B: [Name] — deploys against: [specific objection]
```

This document is the deliverable. Review it against the value eclipsing rule before finalizing: total stated bonus value must exceed the core offer price.

---

## Examples

### Case Study: DFY-to-DWY Gym Business Pivot

A gym owner originally sold done-for-you (DFY) services at a high price with thin margins. Transitioning to a done-with-you (DWY) model meant the core deliverable changed from physical execution to coaching and systems.

The offer remained priced similarly, but the bonus stack allowed the pivot to succeed:

- The gym owner extracted every template, checklist, and script they had built over years of DFY work and packaged them as standalone bonuses: "The 6-Week Member Retention Email Sequence," "The Front Desk Revenue Script," "The Monthly Fitness Challenge Template."
- Each had been part of the invisible DFY execution. As named bonuses with assigned values, they made the DWY offer feel richer than the DFY offer even at a lower labor cost.
- Partner bonuses from a supplement company (group discount + commission to the gym owner) made the total stated bonus value exceed the offer price — fulfilling the value eclipsing rule.
- Objection reserve bonuses targeting "I don't have time to manage this myself" dissolved the main transition objection.

**The lesson:** Transitioning delivery models is also a re-presentation problem. Bonuses make the same underlying value visible in a new form, allowing a pivot without a price reduction.

### Partner Bonus Example: Pain Clinic

A pain clinic with a $400 offer negotiated partner bonuses from adjacent health businesses. The value of partner bonuses alone exceeded the $400 price:

- Chiropractor: 2 free adjustments ($100 value) + $100 affiliate commission per patient referred
- Low-inflammation food company: product discount ($50 savings) + free product affiliate benefit
- Orthotics company: discounts ($150 savings) + $100 per person referred
- Health club: free personal training session + one month pool membership ($100 value) + $50 per signup referred
- Pharmacy: $100/month in prescription savings

Total affiliate commissions on a single client: ~$350 — nearly covering the $400 offer price in downstream revenue.

---

## Key Principles

**Enumerate to create value.** Value that is not named does not exist in the buyer's mind. Every deliverable you provide silently is value you are giving away without receiving credit for. Bonuses make implicit value explicit.

**Bonuses over discounts, always.** Discounting tells the market your price was wrong. Adding bonuses tells the market your offer is generous. One undermines your positioning; the other reinforces it. When you feel pressure to close, add value — never subtract price.

**Tools and checklists over trainings.** Lower buyer effort equals higher perceived value. A one-page checklist that produces results in 15 minutes is worth more to a buyer than a 3-hour training covering the same ground. Build for usability, not impressiveness.

**Value eclipsing is psychological leverage.** When the stated bonus value exceeds the price, the buyer's subconscious concludes two things: (1) the bonuses alone are worth the price, so anything in the core offer is pure gain; (2) the core offer must be even more valuable than the bonuses, because these are just the extras. Neither conclusion requires you to say anything — the math communicates it.

**The bonus vault compounds over time.** Every recorded workshop, every client result, every tool you build becomes a bonus asset. Treat them as inventory. A library of 20 validated bonus assets means you can build and customize a stack for any new offer in under an hour.

---

## References

- `grand-slam-offer-creation` — Build the core offer that this skill enhances. The deliverables list from that skill is the raw material for your bonus stack.
- `value-equation-offer-audit` — Diagnose which elements of your offer feel high-effort or slow. These are the bonuses to prioritize: tools or shortcuts that address exactly those friction points score highest.
- `offer-naming-magic-formula` — Apply benefit-driven naming to each bonus. The bonus name does as much selling as the bonus itself.
- `guarantee-design-and-selection` — Guarantees and bonuses work together. A strong guarantee removes fear of loss; a strong bonus stack removes doubt about value. Pair them for maximum conversion impact.

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — $100M Offers: How To Make Offers So Good People Feel Stupid Saying No by Alex Hormozi.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-grand-slam-offer-creation`
- `clawhub install bookforge-value-equation-offer-audit`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
