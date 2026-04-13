# New Product Launch Sub-flow Reference

Source: SPIN Selling by Neil Rackham, Chapter 5 ("Giving Benefits in Major Sales"), section "Selling New Products"

---

## The Problem: Why New Product Launches Underperform

When a product is new, the default communication path creates a predictable failure:

1. Product marketing explains the product to the sales force using Features and Advantages — "the bells and whistles."
2. The sales force becomes enthusiastic and goes out to sell.
3. In front of customers, they communicate the product exactly as it was communicated to them: Features and Advantages.
4. The average level of Features and Advantages given when selling new products is more than 3 times the level given when selling established products.
5. Sales are slow early in the launch. Management asks, "What's wrong?"

The root cause: seller attention is on the product, not on the customer. Features and Advantages cannot produce Benefits because the customer has not yet expressed a want. Without Explicit Needs, there are no Benefits — only a product presentation that requires the customer to figure out for themselves whether it is worth the cost.

## The Empirical Anchor: The +54% Medical Diagnostics Experiment

Huthwaite was invited to run a controlled experiment on a new-product launch in a medical diagnostics company. The product was sophisticated, expensive diagnostic equipment — clearly a large-sale context.

**Conventional group:** launched in the standard way — a high-key presentation of Features and Advantages by the product marketing team.

**Experimental group (small):** launched differently:
- The group was NOT shown the product
- They were told: "What is important is that this machine is designed to solve problems for the doctors who use it"
- They were given a list of the problems the machine solved and the needs it met
- They made a list of accounts where these problems could exist
- They planned the Problem, Implication, and Need-payoff Questions they would ask when visiting those accounts

**Result:** The experimental group averaged **54% higher sales** than the conventional group during the product's first year.

The experimental group's attention was on customer needs, not product features. They went into accounts asking questions to develop Explicit Needs before presenting any capability. Because they presented capabilities as Benefits (meeting confirmed Explicit Needs), their presentations were far more effective.

## Why Conventional Launches Fail Then Recover

A common pattern: a new product launches to poor results, and then — often 6-12 months in — sales suddenly improve. The explanation is behavioral, not market-based.

When the product is new, the sales force is excited. Excitement = product-centered selling = Features and Advantages = poor results.

As the initial enthusiasm fades and the "it's just another product" mentality sets in, sellers stop talking about the product and start paying attention to customer needs again. They return to discovery habits. That shift — from product-centered to need-centered — is what drives the improvement, not any change in the market.

The lesson: do not wait for enthusiasm to fade. Build the problem-first discipline into the launch from day one.

## Step-by-Step: Problem-First Launch Workflow

### Step 1: List the Problems the Product Solves

Before any product demonstration or feature explanation, ask: "What specific problems is this product designed to solve?"

Output: A list of 3-6 named problem types. Each should be a problem a specific type of customer would recognize in their own operation.

Example format:
```
Problem 1: [Name] — [Description of the problem in customer terms, not product terms]
Problem 2: ...
Problem 3: ...
```

### Step 2: Identify Target Accounts by Problem Fit

For each problem, identify which customer roles, industries, or segments are most likely to experience it. This determines who to prioritize for discovery calls and which accounts to target with which problem questions.

### Step 3: Plan SPIN Questions for Each Problem

For each problem:
- Write Problem Questions to surface the problem (if the customer has it)
- Apply the Implication chain (problem → consequences → questions) to build urgency
- Write Need-payoff Questions to get the customer to articulate the want — the Explicit Need

Use `spin-discovery-question-planner` with the problem list as input.

### Step 4: Run Discovery Calls — Develop Explicit Needs

Go into accounts with the problem list and SPIN question bank. Do NOT show the product, describe Features, or present Advantages. Ask questions. When a customer confirms they have one of these problems AND articulates a want for the solution ("we need," "we're looking for," "I'd like"), record that as an Explicit Need in `needs-log.md`.

### Step 5: Draft Benefits — Now

Return to `benefit-statement-drafter` with the populated `needs-log.md`. Now you have the anchors to draft true Benefits — one per confirmed (Explicit Need, capability) pair.

---

## Common Failure Modes to Avoid

**Bells-and-whistles presentation:** Showing all the product's Features and Advantages in the first meeting. The customer's first exposure to the product should be through questions about their problems, not a product demonstration.

**Premature Benefits:** Drafting "Benefits" from the product spec without running discovery. These are Advantages at best — they meet presumed needs, not expressed ones. Provisional templates (Step 3d of the sub-flow) are placeholders only.

**Enthusiasm-driven feature dumping:** The excitement of a new product naturally pulls sellers toward it. Recognize this impulse and redirect it toward problem-focused questions.

**Skipping Implication Questions:** For a new product, the customer may not yet see why the problem it solves is large enough to justify the cost. Implication Questions do the work of showing the true size of the problem. Without them, the customer hears the price and says "not worth it."

---

## Key Quote

> "Instead of showing them the product and describing its Features and Advantages, we didn't even let them see what they would be selling. 'It's not important,' we explained. 'What is important is that this machine is designed to solve problems for the doctors who use it.'"

— Neil Rackham, SPIN Selling, Chapter 5

The result: 54% higher sales in year one, compared to the conventional feature-led group.
