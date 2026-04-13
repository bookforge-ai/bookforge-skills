# FAB Definitions and Edge Cases

This reference supplements the `fab-statement-classifier` skill. It provides the full definitions for Features, Advantages, and Benefits as derived from Rackham's SPIN Selling research, with edge cases that commonly trip up classifiers.

---

## Authoritative Definitions

### Feature
**What it is:** A neutral fact, data point, or characteristic about a product or service. Features do not explain use; they do not connect to customer outcomes.

**Research finding:** From analysis of 18,000 sales calls, Features are neutral overall — they neither help nor harm significantly. In large sales, Features used *early* in the call have a slight negative effect. Late in long selling cycles, technically sophisticated buyers may develop a "Features appetite" and respond positively to product detail — but this is an exception.

**Classification test:** Does the statement describe a product characteristic without explaining how it helps? → Feature.

**Examples:**
- "This system has 512K buffer storage."
- "Our consultants have a background in educational psychology."
- "The base configuration is $42,000."
- "It runs on a 32-bit processor."
- "There is a four-stage exposure control."

**Price sensitivity note:** Heavy use of Features increases the customer's sensitivity to price. For low-cost products this works in the seller's favor. For expensive products, it works against them — causing more price objections.

---

### Advantage (Rackham's "Type A Benefit")
**What it is:** A statement showing how a product feature *can be used* or *can help* the customer. More than a Feature — it links the capability to potential customer value. However, it does NOT meet a customer-expressed Explicit Need.

**The naming problem:** Most sales training (including the majority of programs over the past 60 years) teaches sellers to give "Benefits." What those programs actually describe and teach are Advantages in Rackham's taxonomy. The term "Benefit" has been so badly degraded in common usage that it is near-meaningless. Rackham's distinction is what separates his research from the consensus.

**Research finding:** From the 5,000-call Benefits study, Advantages had **no statistically significant relationship** to call success in large sales. In small sales, they have a moderate positive relationship. Early in a multi-call selling cycle, Advantages have some positive effect (they "run out of steam" as the cycle progresses). They create objections at higher rates than Benefits — Linda Marsh's correlation study showed that Advantages are the primary source of customer objections.

**Classification test:** Does the statement show how the product can help or be used, but without a prior customer-expressed Explicit Need? → Advantage.

**Examples:**
- "This means you won't lose data during power failures." (no Explicit Need for backup expressed)
- "Our system would eliminate that retyping for you." (only an Implied Need for less retyping expressed)
- "The low error rate means your operators spend less time on validation." (no Explicit Need for validation reduction stated)
- "Time-based coding means you can track when any entry was made." (no Explicit Need for tracking stated)
- "This would speed up your workflow significantly." (general capability claim, no specific Explicit Need stated)

**The Advantage-as-Benefit anti-pattern:** This is the single most prevalent error in B2B sales content. Sellers (and marketers) write statements that sound helpful, aspirational, and customer-facing — and label them "Benefits" — but no customer has ever expressed the underlying want. Examples include:
- "So you can focus on what matters most" (common deck filler — sounds beneficial, meets no stated need)
- "Giving your team the visibility they need" (who asked for visibility? no one, in this context)
- "Eliminating the guesswork from your process" (guesswork was described as a problem = Implied Need at best)

---

### Benefit (Rackham's "Type B Benefit")
**What it is:** A statement showing how the product meets an Explicit Need that the customer has expressed. Two conditions, both required:
1. The customer expressed a specific want, desire, or intention **before** the statement was made
2. The seller's statement **directly links the product capability to that specific expressed need**

**Research finding:** From the 5,000-call study, Benefits (Type B) were significantly higher in calls leading to Orders and Advances. Benefits are the only product statement type strongly linked to success in ALL sizes of sales. The Motorola Canada controlled study showed salespeople trained to use Benefits instead of Advantages increased dollar sales volume by 27%.

**Structural pattern:** A Benefit almost always has two components:
- A reference to what the customer said ("Since you need X..." / "You mentioned you want Y...")
- A demonstration that the product delivers it ("...our product does exactly that")

**Classification test:** Did the customer express this specific want in their own words before this statement? AND does this statement show the product meets that exact expressed want? → Benefit.

**Examples:**
- Customer: "I need to read source data straight into memory." → Seller: "Our direct memory access module does exactly that." → **Benefit**
- Customer: "We need error rates under 1 in 100,000." → Seller: "We're certified at 1 in 500,000, which meets your requirement." → **Benefit**
- Customer: "We'd like a single dashboard for all three regions." → Seller: "Our unified reporting module shows all regions in one view." → **Benefit**

**The development dependency:** You cannot give a true Benefit without first developing an Explicit Need. This is why Benefits cannot be "written in advance" without customer context. A pitch deck can contain Features and Advantages. It cannot contain Benefits — because Benefits require the customer to have spoken first. This is why pre-call deck audits typically find 0% true Benefits and why Rackham's training advice is: "Do a good job of developing Explicit Needs and the Benefits almost look after themselves."

---

## Edge Cases and Common Misclassifications

### Edge Case 1: "They mentioned a problem, then I showed the solution"
Situation: Customer says "Our reporting takes 2 days." Seller says: "Our system cuts reporting time to 2 hours."

**Classification: Advantage, NOT Benefit.**
Reason: "Takes 2 days" is an Implied Need — a problem statement, a dissatisfaction. The customer described a pain, not a want. To be a Benefit, the customer must have said "We need faster reporting" or "We want to get reporting down to under a day" (Explicit Need). Showing a solution to an Implied Need = Advantage.

To convert: Use Implication Questions to develop the consequences of the 2-day delay, then Need-payoff Questions to get the customer to articulate "We need reporting in under a few hours." Once they say it → you can give a Benefit.

---

### Edge Case 2: "I'm just assuming they want this"
Situation: Seller says "Since you're probably looking for something that scales with your business, our platform supports 10x growth without re-architecting."

**Classification: Advantage.**
Reason: "Probably looking for" is the seller's assumption. No Explicit Need for scalability was expressed. Even if this assumption turns out to be correct, the statement does not meet a *stated* need — it meets an *inferred* one.

---

### Edge Case 3: "The customer nodded and seemed interested when I mentioned it"
Buyer engagement, enthusiasm, or non-verbal cues do not convert an Advantage into a Benefit. Classification is based on words expressed, not inferred intent. A customer who seems interested in a capability they haven't asked for is responding to an Advantage. If they then say "Yes, that's exactly what we've been looking for," that statement IS an Explicit Need — and the next product statement you make that addresses it can be a Benefit.

---

### Edge Case 4: "We always include this in our deck as a Benefit"
Common in marketing-produced collateral. Statements like "Reduce costs by 30%" or "Cut time-to-insight in half" are Advantages — they show the product can help, but they do not meet an expressed Explicit Need. No prospect's Explicit Need is present in a deck that hasn't been customized to a specific buyer's stated requirements.

Exception: If you are auditing a deck against a specific deal's `needs-log.md` and a matching Explicit Need is documented, you can reclassify the statement as a Benefit in that context. Without that deal-specific Explicit Need, classify as Advantage.

---

### Edge Case 5: "The customer said they want to improve efficiency"
"Improve efficiency" is usually still vague enough to be borderline. If the customer said "We want to improve efficiency" with no specifics, it is a very general Explicit Need. A matching Benefit would need to show how the product improves efficiency in the specific way the customer described. If the product statement is specific and the customer's Explicit Need is general, look for closer matches.

**Rule of thumb:** The more specific the Explicit Need, the more clearly a matching product statement qualifies as a Benefit. "We need to cut our monthly close process from 5 days to 2" → a statement showing the product achieves this = unambiguous Benefit.

---

### Edge Case 6: "A cost fact followed by context"
"Our system costs $42,000 — which is 30% less than the industry average" — the first part is a Feature (cost fact), the second part is an Advantage (shows comparative value). If the customer had said "We need something under $50,000" before this, then "our system at $42,000 meets your budget" would be a Benefit.

---

## FAB Distribution Norms

From Rackham's research on typical sales calls:

| Behavior | Typical distribution | Impact in large sales |
|---|---|---|
| Features | ~40-50% of product statements | Neutral to mildly negative; creates price sensitivity |
| Advantages | ~40-50% of product statements | Not linked to success; creates objections |
| Benefits | ~5-15% of product statements | Strongly linked to success; generates approval |

A typical pitch deck audited against this framework will show 0-10% true Benefits, 40-60% Advantages, and 30-50% Features. This is normal — not a failure of the sales team, but a structural limitation of content created without specific deal context. The audit's purpose is to surface this gap and guide the seller on which Advantages to convert into Benefits before the next call.

---

## The FAB → Customer Response Chain (Chapter 6)

Rackham's colleague Linda Marsh identified the most probable customer responses to each type:

| Seller uses | Most probable customer response |
|---|---|
| Features | Price concerns / price sensitivity |
| Advantages | Objections (value challenges, "not worth it," "don't need that") |
| Benefits | Support, approval, positive buying statements |

This chain explains why objection-heavy calls are usually high-Advantage calls: the seller is offering solutions before the customer has expressed a want, so the customer raises the value question themselves. The prescription is not better objection-handling techniques — it is better need development so that product statements become Benefits rather than Advantages.

---

*Source: SPIN Selling by Neil Rackham (1988), Chapters 5–6. Part of the BookForge SPIN Selling skill set — licensed CC-BY-SA-4.0.*
