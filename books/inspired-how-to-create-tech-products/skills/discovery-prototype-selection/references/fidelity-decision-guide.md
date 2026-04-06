# Fidelity Decision Guide

Source: INSPIRED by Marty Cagan, Chapters 45 and 47

## Core Principle

There is no such thing as one appropriate level of fidelity for a prototype. Fidelity primarily refers to how realistic the prototype looks. The principle is to create the right level of fidelity for the intended purpose, knowing that lower fidelity is faster and cheaper than higher fidelity — so only do higher fidelity when you need to.

## Decision Tree

**What is the testing purpose?**

### 1. Value testing (qualitative) — "Does the user perceive value when they see this?"

Required fidelity: **High**

Why: Value perception depends on realism. If users can tell the prototype is fake — through low-quality visuals, placeholder data, or missing interactions — their reactions are not valid signal. People react to what they actually see and experience. A low-fidelity prototype triggers "this doesn't look real" responses that contaminate the value signal. High fidelity is required so users can genuinely assess whether they would want this product.

Warning: Even high-fidelity user prototypes cannot prove purchase behavior. They test perceived value — "this seems useful" — not behavioral value — "I will pay money for this." Do not mistake positive reactions to a high-fidelity prototype for validated demand.

### 2. Usability testing — "Can the user complete the workflow without help?"

Acceptable fidelity: **Low to medium**

Why: Usability testing is primarily about information architecture, workflow sequencing, and interaction clarity — not visual design. A low-fidelity prototype (interactive wireframe) is often more than adequate for identifying where users get stuck, what labels confuse them, or where the workflow breaks down. Moving to high fidelity before resolving major usability issues wastes time on polish that may be discarded.

Exception: If the usability question involves visual design specifically (e.g., "is the call-to-action button visible?"), medium to high fidelity may be needed.

Low-fidelity prototypes do not capture:
- The impact of visual design on user confidence
- Differences caused by actual data (vs. placeholder content)
- The impact of visual hierarchy on attention

If those dimensions matter for the usability question, increase fidelity accordingly.

### 3. Demand validation — "Will users buy or sign up for this?"

Required approach: **Live-data prototype or fake door (demand test) — not a user prototype**

Why: A user prototype is a simulation. It cannot generate real behavioral data. Showing a user prototype to users and asking "would you buy this?" produces stated preference, not revealed preference. People say all kinds of things and then do something different. Demand validation requires users to actually take an action with real consequences — visiting a real landing page, attempting a real sign-up, or clicking a real "buy" button. A live-data prototype or demand-testing technique is the right tool for this, not a user prototype at any fidelity level.

### 4. Stakeholder communication — "Does leadership understand and support what we are building?"

Acceptable fidelity: **Medium to high**

Why: Stakeholders and business partners need to experience the product concept clearly enough to make decisions. A low-fidelity wireframe often fails to communicate the vision — stakeholders struggle to project what the finished product will look and feel like. Medium to high fidelity bridges this gap. The prototype does not need to be pixel-perfect, but it needs to be representative enough that stakeholders can give informed feedback and alignment.

### 5. Internal team alignment — "Are we all thinking about the same thing?"

Acceptable fidelity: **Low**

Why: For internal team thinking, speed matters more than realism. Creating a prototype (even a low-fidelity one) forces the team to think through the problem at a substantially deeper level than talking about it. Low-fidelity prototypes expose major issues that would otherwise remain hidden in conversations. Create quickly; iterate quickly.

---

## Fidelity by Prototype Type

| Prototype Type | Fidelity Concept | Notes |
|---|---|---|
| Feasibility | Not applicable | It is code, not a UI simulation |
| User (low) | Interactive wireframe | Fast; tests workflow, not visual design |
| User (medium) | Styled but not pixel-perfect | Balances speed and realism |
| User (high) | Looks and feels real | Required for value testing |
| Live-data | Actual implementation | Real data, limited scope, real users |
| Hybrid / Wizard of Oz | High visual fidelity + human backend | Looks real; backend is manual |

---

## Common Fidelity Mistakes

**Starting with high fidelity when low would suffice.** Teams that jump to high-fidelity prototypes for early usability testing spend time on polish before resolving fundamental workflow issues. Iterate at low fidelity until the workflow is sound, then increase fidelity for value testing.

**Using low fidelity for value testing.** Showing users a wireframe and asking if they value the concept produces unreliable signal. Users cannot properly evaluate value through placeholder-filled sketches.

**Treating any prototype fidelity as proof of demand.** The fidelity level of a user prototype does not change its fundamental limitation: it cannot prove purchase behavior. This is a category error, not a fidelity error.
