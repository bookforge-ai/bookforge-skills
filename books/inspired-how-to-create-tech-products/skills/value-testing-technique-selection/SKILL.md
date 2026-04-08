---
name: value-testing-technique-selection
description: "Select and execute the right value testing technique for product discovery. Use when you have a prototype and need to know if customers will actually choose or buy the product, when deciding between a fake door test, usability test, A/B test, or invite-only program, when someone asks 'how do we test if users want this?' or 'should we run an A/B test?', or when setting up analytics instrumentation before launch. Also use when validating demand before building anything, when choosing between qualitative vs. quantitative value testing, or when the team is unsure whether 'people said they liked it' is enough evidence. Covers the 3-level value testing hierarchy (demand / qualitative / quantitative), the usability-then-value session protocol, and the analytics instrumentation checklist. For prototype selection, use discovery-prototype-selection. For finding product-market fit with reference customers, use customer-discovery-program. For stakeholder viability sign-off, use business-viability-stakeholder-testing."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/inspired-how-to-create-tech-products/skills/value-testing-technique-selection
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: inspired-how-to-create-tech-products
    title: "INSPIRED: How to Create Tech Products Customers Love"
    authors: ["Marty Cagan"]
    chapters: [50, 51, 52, 53, 54]
tags: [product-management, product-discovery, user-research, testing]
depends-on: [product-discovery-risk-assessment, discovery-prototype-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Risk assessment output or product/feature description including traffic volume, risk tolerance, and prototype readiness"
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: "Document-based product management environment"
discovery:
  goal: "Select the correct value testing technique and produce an executable test plan"
  tasks:
    - "Apply the 3-level value testing hierarchy to select the appropriate technique"
    - "Design and run a usability test session as a prerequisite to value testing"
    - "Execute the specific value test (demand, qualitative, or quantitative)"
    - "Select among A/B, invite-only, and customer discovery program for quantitative work"
    - "Define the analytics instrumentation plan for the feature"
  audience:
    roles: [product-manager, product-designer, tech-lead, startup-founder]
    experience: any
  when_to_use:
    triggers:
      - "You have a high-fidelity prototype and need to know if customers will choose the product"
      - "Risk assessment has identified value risk as Medium or High"
      - "You need to decide whether to use A/B testing, invite-only, or customer discovery program"
      - "You are launching a new feature and need to define what analytics to instrument"
      - "Sales is hearing demand signals but you have no quantitative evidence"
    prerequisites:
      - "product-discovery-risk-assessment completed (value risk identified)"
      - "discovery-prototype-selection completed (prototype type selected)"
    not_for:
      - "Usability testing alone — this skill uses usability testing as a prerequisite step, not the goal"
      - "Feasibility testing — use engineer-led feasibility spikes"
      - "Business viability review — use stakeholder review process"
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
---

# Value Testing Technique Selection

## When to Use

Apply this skill when you have evidence of a product idea worth testing and need to determine whether customers will actually choose it. This skill answers three questions:

1. Which level of value testing does this situation call for — demand, qualitative, or quantitative?
2. How do I execute the right session protocol?
3. What analytics must be instrumented before or alongside any test?

Do NOT use this skill as a substitute for usability testing alone, feasibility spikes, or business viability stakeholder review. Those are handled by separate skills. This skill assumes a prototype exists or can be built quickly.

**The core insight:** Just because someone can use your product doesn't mean they will choose to use it. Feature parity is not enough. Customers must perceive your product as substantially better to endure the switching costs from their current solution.

## The 3-Level Value Testing Hierarchy

Before selecting any technique, apply this hierarchy in order. Start at Level 1 and only advance if the prior level is satisfied.

| Level | Question Answered | Technique | When to Use |
|-------|------------------|-----------|-------------|
| **1 — Demand** | Do customers care about this problem enough to act? | Fake door test / landing page demand test | Unknown if customers want this at all; new product or feature; before building anything |
| **2 — Qualitative** | Do customers see real value when they experience it? Why or why not? | Interview + usability + specific value tests | You know demand exists but need to understand whether your solution is compelling and why |
| **3 — Quantitative** | Is there statistically meaningful behavioral evidence of value? | A/B test / invite-only / customer discovery program | Usability and qualitative value are confirmed; you need evidence to justify full build investment |

**Why this ordering matters:** Level 1 prevents wasted engineering effort on solutions nobody wants. Level 2 explains what Level 3 will measure and provides the "why" that quantitative data alone cannot. Skipping to Level 3 without Level 2 leaves you with data that tells you something is wrong but not how to fix it.

## Step 1: Determine Which Level to Enter

Read the risk assessment and answer these questions in order:

**Is demand established?**
- No clear evidence anyone wants this → start at Level 1 (demand testing)
- Demand signals exist (sales reports, customer interviews, competitor market) → skip to Level 2

**Is qualitative value confirmed?**
- Have fewer than 5 customers experienced the solution and responded positively → start at Level 2
- 5+ users have tested the prototype and shown genuine value signals → consider Level 3

**What is the risk/traffic profile?**
- New product or startup with low traffic → Level 1 or Level 2; skip quantitative until demand exists
- Established product with traffic but high risk sensitivity → Level 3 invite-only or customer discovery program
- Established product with significant traffic and moderate risk tolerance → Level 3 A/B test

**WHY:** Jumping to A/B testing before qualitative value is confirmed produces data that shows whether a product works, but provides no insight into why it doesn't work or how to fix it. Conversely, stopping at qualitative testing without moving to quantitative leaves the team making claims that cannot be defended to stakeholders.

## Step 2: Execute the Selected Level

### Level 1 — Demand Testing

Use a fake door test (for features on an existing product) or a landing page demand test (for new products).

**Fake door test:**
1. Add the button or menu item to the product interface exactly where users would expect to find it
2. When clicked, redirect to a page explaining you are studying the possibility of adding this feature and inviting them to volunteer for a conversation
3. Collect email addresses or phone numbers from volunteers
4. Measure the click-through rate and compare to baseline feature interaction rates
5. Follow up with volunteers for qualitative interviews

**Landing page demand test:**
1. Build a landing page that describes the new offering exactly as if it were live
2. Drive traffic via existing channels, search engine marketing, or email
3. When users click the call to action, redirect to a page explaining you are studying this offering and would like to speak with them
4. Collect volunteer contact information and measure click-through rate

**What success looks like:** Meaningful click-through rate relative to other features/products, and a list of users actively willing to discuss the problem. The demand test does not prove customers will pay — only that they care enough to investigate.

**WHY:** Building a complete product only to discover nobody wants it is the most avoidable failure in product development. Demand testing takes hours to days, not months. The fake door specifically reveals whether real users in actual context care about this, not just users asked hypothetically in a survey.

See `references/qualitative-value-test-protocol.md` for the follow-up interview protocol after collecting volunteer contacts.

### Level 2 — Qualitative Value Testing

This is the single most important discovery activity for most product teams. Run at minimum two to three qualitative value sessions per week during active discovery.

**The session structure has four parts, always in this sequence:**

**Part A — Interview First (5–10 minutes)**
Confirm the user has the problem you think they have. Ask how they solve it today and what it would take for them to switch. This grounds the value test in actual context.

**WHY:** If the user does not actually have the problem, their response to your solution is meaningless. The interview prevents you from treating a non-customer as a customer.

**Part B — Usability Test (15–20 minutes)**
Before testing value, the user must understand how to use the product. Run a full usability test first. The value test is only valid once the user has operated the prototype and understands what it does.

**WHY:** Without usability testing first, a value session becomes a focus group where users comment hypothetically on something they have never operated. Focus groups produce polite opinions that do not predict behavior. Operate the prototype first, then test value.

See `references/usability-test-protocol.md` for the complete four-phase usability test protocol.

**Part C — Specific Value Tests (10–15 minutes)**
After usability, apply one or more of these four value tests. They are designed to detect genuine enthusiasm, not polite agreeableness.

| Value Test | What to Do | Signal |
|-----------|-----------|--------|
| **Money test** | Ask if they would pay for it right now; request credit card or letter of intent | Willingness to make a financial commitment |
| **Time test** | Ask if they would schedule significant time with you to work on this | Willingness to invest their most scarce resource |
| **Access test** | Ask for login credentials to the competing product they would switch from | Willingness to commit to switching right then |
| **Referral test** | Ask for Net Promoter Score (0–10 likelihood to recommend); ask for their boss's or colleague's email | Willingness to stake their reputation on this |

Use whichever tests fit the context. For consumer products, money and referral tests are most practical. For business products, all four apply. The goal is not to collect the credit card or email — it is to observe whether the user is willing to make a commitment, which reveals genuine perceived value versus politeness.

**Part D — Iterate the Prototype**
As soon as you see a problem or want to try a different approach, update the prototype and test it in the next session. There is no law that says you must keep the test identical across all subjects. Qualitative testing is about rapid learning, not proving anything.

**Cadence:** Target two to three sessions per week throughout discovery. As product manager, you must be present at every session. Do not delegate this.

### Level 3 — Quantitative Value Testing

Quantitative testing collects behavioral evidence. Use it to prove that a solution works, not to discover what to build. The technique depends on your traffic volume and risk tolerance.

**Technique selection:**

| Situation | Technique | Why |
|-----------|-----------|-----|
| High traffic, moderate risk tolerance | **A/B test at 1% exposure** | Gold standard; users don't know which version they see; most predictive data |
| Lower traffic or higher risk aversion | **Invite-only test** | Identifies a willing set of early adopters; less predictive due to opt-in bias, but generates real usage data |
| Maximum risk sensitivity (regulated, enterprise, brand-sensitive) | **Customer discovery program** | Participants under non-disclosure agreement; pre-existing close relationship; most conservative |

**A/B testing (discovery variant):**
Run the live-data prototype against the current product. Show the live-data prototype to 1% or fewer of users. Monitor closely. This differs from optimization A/B testing (which tests surface-level changes at 50/50 splits). Discovery A/B testing tests fundamentally different approaches with minimal user exposure.

**Invite-only testing:**
Identify users to contact directly and invite them to try an experimental version. They know it is experimental, so they are effectively opting in. The data is less predictive than a blind A/B test because early adopters are not representative of the full user base. When quantitative results are negative, follow up immediately with qualitative sessions to understand why.

**Customer discovery program:**
Use your existing customer discovery program members. They have already opted in to testing new versions and are under a non-disclosure agreement. For business-to-business products, this is the primary recommended quantitative technique during discovery. Compare their usage data to the broader customer base.

**WHY for technique selection:** A/B tests produce the most predictive data because users are blind to the test. But they require sufficient traffic to achieve statistical significance, and they expose some users to potentially inferior experiences. Invite-only and customer discovery program reduce exposure risk at the cost of predictive power. Match the technique to what your traffic and risk profile can actually support.

## Step 3: Analytics Instrumentation (Non-Negotiable)

Every feature shipped must have usage analytics instrumented before or at launch. Not doing this is the "flying blind" anti-pattern — a non-negotiable failure.

**The flying blind anti-pattern:** Teams that ship features without instrumentation cannot know whether those features are working, whether users are adopting them, or whether they should be removed. This prevents data-informed decisions and makes roadmap prioritization guesswork.

**Rule:** If you are not willing to instrument a feature to know immediately whether it is working and whether there are significant unintended consequences, do not ship it.

**Minimum instrumentation checklist for any new feature:**
- [ ] Feature adoption rate (are users finding and using it?)
- [ ] Task completion rate (are users completing the intended workflow?)
- [ ] Error/abandonment points (where are users dropping off?)
- [ ] Impact on key business metric (conversion, retention, revenue, or the metric the feature was designed to move)

**Broader analytics strategy:** Product managers must track analytics across all seven categories. Most teams only track user behavior and miss the rest.

| Category | Examples |
|----------|---------|
| User behavior | Click paths, feature engagement, session flow |
| Business | Active users, conversion rate, lifetime value, retention |
| Financial | Average selling price, billings, time to close |
| Performance | Load time, uptime, latency |
| Operational | Storage, hosting costs |
| Go-to-market | Acquisition cost, cost of sales |
| Sentiment | Net Promoter Score, customer satisfaction, survey responses |

See `references/analytics-strategy.md` for the full five uses of analytics and implementation guidance.

## Outputs

After completing this skill, produce:

```
# Value Test Plan: [Feature / Product Name]

## Level Selected
[ ] Level 1 — Demand   [ ] Level 2 — Qualitative   [ ] Level 3 — Quantitative
Rationale: [why this level]

## Technique Selected
[Fake door / Landing page / Qualitative session / A/B test / Invite-only / Customer discovery program]

## Test Plan
[For demand: where the fake door appears, what the redirect page says, how CTR will be measured]
[For qualitative: session structure, value tests selected, target users, weekly cadence]
[For quantitative: traffic %, exposure duration, primary metric, statistical significance threshold or evidence threshold]

## Usability Test Required First?
[ ] Yes — complete usability-test-protocol before value test
[ ] No — user already understands the product

## Value Tests to Apply (qualitative)
[ ] Money test   [ ] Time test   [ ] Access test   [ ] Referral test

## Analytics Instrumentation Plan
[List the specific events and metrics to instrument before launch]

## Success Criteria
[What signal means this test produced sufficient evidence to move to next level or to full build?]

## Next Step
[If positive: proceed to Level 3 / proceed to full build / present to stakeholders]
[If negative: iterate prototype / reconsider problem framing / stop and preserve capacity]
```

## Key Anti-Patterns

**Prototype-as-value-proof:** Showing a high-fidelity prototype to users who say they love it does not validate value. People are polite. Use the specific value tests (money, time, access, referral) to detect genuine commitment, not stated enthusiasm.

**Flying blind:** Shipping features without instrumentation. Non-negotiable failure. Every feature needs basic usage analytics before launch.

**Skipping qualitative before quantitative:** Running an A/B test before qualitative value is confirmed produces data that tells you something is wrong but not how to fix it.

**Focus group substitution:** Asking users to comment on a prototype they have never operated produces hypothetical opinions, not behavioral insight. Always run usability testing before value testing.

**Delegating qualitative sessions:** As product manager, you must attend every qualitative value test. The firsthand exposure to customer reactions is a core part of the role and cannot be substituted with written summaries.

## References

- `references/usability-test-protocol.md` — Complete four-phase usability test protocol (recruit, prepare, test, summarize) with the parrot technique and use-mode guidance
- `references/qualitative-value-test-protocol.md` — Full qualitative value session structure including interview-first approach, all four specific value tests, and iteration cadence
- `references/analytics-strategy.md` — Five uses of analytics in product teams, seven analytics categories, flying blind anti-pattern detail, and instrumentation implementation guidance

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — INSPIRED: How to Create Tech Products Customers Love by Marty Cagan.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-product-discovery-risk-assessment`
- `clawhub install bookforge-discovery-prototype-selection`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
