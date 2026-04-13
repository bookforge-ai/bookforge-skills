---
name: content-and-email-marketing
description: "Design content marketing and email lifecycle programs that work together as an acquisition engine. Use whenever a founder or marketer is planning a blog, newsletter, content calendar, email sequences, lead magnets, drip campaigns, onboarding emails, activation emails, retention emails, or any combination of content creation and email marketing. Also covers the acquisition → activation → retention → revenue lifecycle. Activates on phrases like 'content marketing', 'blog strategy', 'newsletter', 'email marketing', 'drip campaign', 'onboarding emails', 'lifecycle emails', 'activation email', 'email list', 'lead magnet', 'nurture sequence', 'email automation'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/content-and-email-marketing
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [14, 15]
domain: startup-growth
tags: [startup-growth, content-marketing, email-marketing, lifecycle-marketing, customer-activation]
depends-on: [bullseye-channel-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Product description, target audience, activation definition, existing content/email assets"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for content plans and email sequence drafts"
discovery:
  goal: "Produce an integrated content + email plan spanning the 4-stage customer lifecycle"
  tasks:
    - "Define activation threshold for the product"
    - "Plan content topics that attract the target audience"
    - "Design the 4-stage email lifecycle (acquisition → activation → retention → revenue)"
    - "Create activation email sequences for each drop-off point"
    - "Set up retention emails for infrequent-use products"
    - "Avoid the email spam trap"
  audience:
    roles: [startup-founder, content-marketer, email-marketer]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User is starting a blog or newsletter"
      - "User has users who sign up but don't activate"
      - "User wants to increase retention via email"
      - "User is planning a lead magnet or content upgrade"
    prerequisites:
      - skill: bullseye-channel-selection
        why: "Content/email should be selected via Bullseye"
    not_for:
      - "Product has no retention to speak of (fix product first)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: 0
    assertion_count: 12
    iterations_needed: 0
---

# Content and Email Marketing

## When to Use

The startup needs a content strategy, an email strategy, or both integrated. Use this skill when:

- Starting a blog or newsletter from scratch
- Users sign up but don't activate (need activation emails)
- Product-market fit exists but growth isn't compounding (need lifecycle emails)
- A content channel was selected via Bullseye

Content and email are tightly coupled — content builds the email list, email converts the list. This skill covers both as one system.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product description and target audience**
  → Check prompt for: product name, category, ideal customer
  → If missing, ask: "What does your product do, and who's the target audience?"

- **Activation definition:** what action defines an "activated" user
  → Check prompt for: "active user", "first upload", "created project"
  → If missing, ask: "What's the first valuable action a user takes? For Dropbox it's uploading a file, for Twitter it's following 5 people. What's yours?"

### Observable Context

- **Existing content/email assets:** prior blog posts, current email list size, current sequences
- **Conversion funnel:** signups vs activations vs retention

### Default Assumptions
- 4-stage lifecycle: Acquisition → Activation → Retention → Revenue
- CEO personal email 30 minutes after signup (Colin Nederkoorn pattern)
- Never buy email lists — organic only (avoid the spam trap)

### Sufficiency Threshold

```
SUFFICIENT: product + audience + activation definition known
PROCEED WITH DEFAULTS: product + audience known, use "first valuable action" as activation proxy
MUST ASK: product is unknown
```

## Process

Use TodoWrite:
- [ ] Step 1: Define activation threshold
- [ ] Step 2: Plan acquisition content topics
- [ ] Step 3: Design activation email sequence
- [ ] Step 4: Design retention emails
- [ ] Step 5: Design revenue/upsell emails
- [ ] Step 6: Avoid the spam trap

### Step 1: Define Activation Threshold

**ACTION:** Identify the specific action that defines an "activated" user. This must be:
- Specific (not vague engagement)
- Measurable (trackable in analytics)
- Predictive (users who hit it stick; users who don't, churn)

Examples: Twitter — follow 5 people. Dropbox — upload 1 file. Facebook — friend 7 people in 10 days. Slack — send 2,000 messages. These are the actual activation thresholds from real products.

Write the threshold to `activation-definition.md`.

**WHY:** Without a clear activation threshold, email sequences can't target drop-offs. "Send onboarding emails" without knowing the activation event produces generic welcome emails that don't move the needle. The threshold is the foundation for the entire activation email strategy.

**IF** retention data doesn't exist → pick a reasonable first-value action as a hypothesis. Measure and refine.

### Step 2: Plan Acquisition Content Topics

**ACTION:** Design content topics that attract the target audience, especially BEFORE they're ready to buy. Content marketing is list-building as much as it is brand-building.

Topics by type:
- **Awareness-stage content:** problems the audience has that your product solves
- **Consideration-stage content:** comparisons, case studies, how-to guides
- **Decision-stage content:** product-specific content (pricing analyses, specific use cases)

Every content piece should have a **lead magnet** — a free resource (checklist, template, mini-ebook) that captures the email in exchange. This is how content becomes an email list.

**WHY:** Content without a capture mechanism builds awareness but doesn't build a list. The list is the asset. A blog post with 10,000 views and no email captures is 10,000 visits wasted. The lead magnet is what converts anonymous traffic into named leads you can nurture.

**IF** no content capacity exists → budget for 2-4 freelance articles per month as a baseline.

### Step 3: Design Activation Email Sequence

**ACTION:** For each step from signup to activation, identify potential drop-off points. Create an email triggered when a user fails to complete each step within N days.

Colin Nederkoorn's (Customer.io founder) pattern:
1. Map the ideal user experience step-by-step from signup to activation
2. Identify every step where users drop off
3. Create an automated email triggered when a user fails to complete that step within N days
4. Each email nudges the user back to the ideal path
5. Add a personal "CEO email" 30 minutes after signup — this one email opened communication and produced 17% reply rates for Colin

Example sequence for a Dropbox-like product:
- Day 0 (30min): CEO personal email, no sales pitch
- Day 1: "Here's how to upload your first file" (if not uploaded)
- Day 3: "Users who upload 5+ files stick around 10x longer"
- Day 7: "Having trouble? Here's a video walkthrough"

**WHY:** Users don't churn because they disliked the product — they churn because they never got to the valuable moment. Activation emails close the gap between signup and value. Each drop-off point has a specific email that addresses that specific reason.

### Step 4: Design Retention Emails

**ACTION:** For infrequent-use products (the most common case), retention emails keep the product top-of-mind:

- **Weekly/monthly value summary** — Mint's weekly financial summary. BillGuard's monthly credit card report. Reminds users why they signed up.
- **Re-engagement triggers** — "Someone mentioned you" (Twitter), "New reply to your question" (Stack Overflow).
- **"You are so awesome" emails** — Patrick McKenzie's pattern. Usage summaries that make the user feel good about using the product.
- **Memory-anchored emails** — Photo site anniversaries, "A year ago today..." hooks.

Write the retention sequence to `retention-emails.md`.

**WHY:** Retention is about presence. Products the user loves but forgets about cease to exist in their life. Retention emails are not about selling — they're about reminding. Mint's weekly summary isn't pitched as retention, it's pitched as value. The retention effect is a byproduct.

### Step 5: Design Revenue / Upsell Emails

**ACTION:** For users who are activated and retained, design sequences that drive expansion revenue:

- **Referral emails** — Dropbox's storage-for-referral. Incentivizes word-of-mouth.
- **Upsell sequences** — WP Engine's 7-email upsell sequence from free tool to paid.
- **Cart abandonment retargeting** — for e-commerce/pricing page abandonment.
- **Feature-gate upgrade prompts** — for freemium products.

These are typically 3-7 email sequences triggered by specific behavior (not time).

**WHY:** Users who are retained but not expanding are leaving revenue on the table. Upsell sequences capture the willing-to-pay tier that wouldn't upgrade without a prompt. Referral emails turn happy users into new-user acquisition. These are pure expansion revenue that wouldn't exist without the email.

### Step 6: Avoid the Spam Trap

**ACTION:** Document the email marketing anti-patterns:

**Never buy email lists.** "Some companies will buy email lists and send people unsolicited email. That is the very definition of spam. Spam makes recipients angry, hurts future email deliverability efforts, and harms your company in the long run."

Other spam patterns:
- Unclear subject lines that trip spam filters
- Missing unsubscribe link
- Using "noreply@" as the from address
- Blast schedules unrelated to user behavior
- Purchased email lists labeled as "leads"

**WHY:** Email deliverability is a reputation asset built over years. One spam complaint rate over 0.3% can cause deliverability issues that take months to recover from. Buying lists is the fastest way to destroy the asset you're trying to build.

## Inputs

- Product description and target audience
- Activation threshold definition
- Current content/email assets (if any)
- Funnel metrics (if available)

## Outputs

Five markdown files:

1. **`activation-definition.md`** — Specific activation threshold
2. **`content-plan.md`** — Content topics by funnel stage + lead magnets
3. **`activation-emails.md`** — Triggered sequences per drop-off point
4. **`retention-emails.md`** — Value summaries, re-engagement, memory-anchored
5. **`revenue-emails.md`** — Referral, upsell, cart recovery, feature gates

## Key Principles

- **The list is the asset, not the blog.** Content without email capture wastes traffic. WHY: Traffic is ephemeral; email is compounding. Without a capture mechanism, every blog post leaves the audience one step removed from the relationship.

- **Activation defines the email target.** Without a threshold, sequences are generic welcomes. WHY: Activation is the handoff from "signup" to "customer." Every email either moves users toward activation or moves them away from churn.

- **Retention emails reinforce value, not sell.** Mint's weekly summary is valuable; a "we miss you" email is annoying. WHY: Users who love the product but forget it churn. Retention emails exist to remind, not convince.

- **Behavioral triggers beat schedule blasts.** Email when users do (or don't do) something, not on Tuesday morning. WHY: Relevance is the single biggest factor in open rates. Behavior-triggered emails are inherently relevant.

- **CEO email 30 minutes after signup.** One personal email opens communication more than 5 automated ones. WHY: Users expect automation. A human email is unexpected and memorable. Colin Nederkoorn's 17% reply rate proves this.

- **Never buy lists.** Deliverability is a multi-year reputation asset. WHY: One spam complaint surge can destroy deliverability for months. Organic list-building is slower but compounds; bought lists are fast and destructive.

## Examples

**Scenario: SaaS with high signup, low activation**

Trigger: "We get 500 signups per month to our project management tool but only 50 actually create a project. Help."

Process: (1) Activation threshold: "create first project with 2+ tasks." (2) Content plan: 2 articles/month on project management best practices → lead magnets with templates → activation follow-through. (3) Activation sequence: Day 0 CEO email, Day 1 "create your first project in 2 minutes" video, Day 3 "5 project templates to copy", Day 5 "need help? Book a 10min call". (4) Retention: weekly team summary emails. (5) Revenue: upsell to paid when team hits 10 users.

Output: Full lifecycle plan with drop-off-triggered emails.

**Scenario: Blog with no email capture**

Trigger: "Our blog gets 50k visits/month but we only have 200 email subscribers. Ratio is terrible."

Process: (1) Diagnosis: no lead magnets. 50k visits × 2% capture = 1,000 new subs/month achievable. (2) Lead magnet plan: 3 downloadable resources (checklist, template, mini-guide) placed on the top 5 articles. (3) Activation emails for new subscribers: welcome sequence with value, not pitches. (4) Retention: weekly newsletter with curated industry content. (5) Revenue: after 4 weeks of nurture, introduce product.

Output: Content-to-email capture strategy with specific lead magnets and follow-through.

**Scenario: Retention problem for infrequent-use product**

Trigger: "Our expense tracking app has good ratings but users sign up and then forget about it. How do we fix retention?"

Process: (1) Retention is the core problem — infrequent-use product. (2) Weekly value summary: "Here's what you spent this week." Even users who haven't used the app for 2 weeks get reminded of the value. (3) Memory-anchored: "A month ago you saved $47 by noticing your subscription charges." (4) Re-engagement: "You have 3 new transactions to categorize." (5) CEO email on signup + milestone emails ("You've tracked $1,000 in expenses!").

Output: Retention-first email plan that reinforces product value without sales pressure.

## References

- For the 4-stage lifecycle mapping with examples, see [references/lifecycle-stages.md](references/lifecycle-stages.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select content/email via Bullseye
- `clawhub install bookforge-seo-channel-strategy` — SEO and content are tightly coupled
- `clawhub install bookforge-viral-growth-loop-design` — Referral emails are part of viral loops

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
