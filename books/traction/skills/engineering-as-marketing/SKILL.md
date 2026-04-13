---
name: engineering-as-marketing
description: "Design free tools and micro-sites that acquire customers through engineering effort rather than ad spend. Use whenever a founder or marketer wants to build a free calculator, tool, widget, grader, or educational resource as a customer acquisition channel. Activates on phrases like 'engineering as marketing', 'free tool', 'marketing tool', 'calculator', 'grader', 'micro-site', 'widget', 'free app', 'HubSpot Marketing Grader', 'Moz tools', 'lead generator tool', 'utility for marketing', 'free resource for customers'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/engineering-as-marketing
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [16]
domain: startup-growth
tags: [startup-growth, engineering-as-marketing, free-tools, lead-generation, product-led-growth]
depends-on: [bullseye-channel-selection]
execution:
  tier: 2
  mode: full
  inputs:
    - type: document
      description: "Ideal customer problem, engineering capacity, existing product"
  tools-required: [Read, Write]
  tools-optional: [Bash, AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for tool design specs and lead capture plans"
discovery:
  goal: "Design and plan a free tool that captures leads from the ideal customer audience"
  tasks:
    - "Identify the ONE question the ideal customer asks before needing your product"
    - "Design the smallest possible tool that answers that question"
    - "Apply the single-input-field design pattern"
    - "Plan the lead capture after tool use"
    - "Avoid the engineering resource hoarding anti-pattern"
  audience:
    roles: [startup-founder, growth-marketer, engineering-lead]
    experience: intermediate
  when_to_use:
    triggers:
      - "Engineering team has spare capacity"
      - "User wants a scalable lead generation mechanism"
      - "Bullseye selected Engineering as Marketing"
      - "User's ideal customer has a specific quantifiable question"
    prerequisites:
      - skill: bullseye-channel-selection
        why: "Engineering as Marketing should be selected deliberately via Bullseye"
    not_for:
      - "Engineering team has no capacity and product is struggling"
  environment:
    codebase_required: false
    codebase_helpful: true
    works_offline: true
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: 0
    assertion_count: 10
    iterations_needed: 0
---

# Engineering as Marketing

## When to Use

The startup wants to use engineering effort to acquire customers rather than spending on ads. Use this skill when:

- Engineering team has spare capacity or the team is engineering-heavy
- The ideal customer has a specific, quantifiable question they'd pay to answer
- Bullseye Framework selected Engineering as Marketing
- A one-time engineering investment could produce ongoing lead generation

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Ideal customer description:** who the tool should attract
  → Check prompt for: customer profile, pain points
  → If missing, ask: "Who is your ideal customer, and what's the one question they ask before they're ready to pay for your product?"

- **Engineering capacity:** available hours/weeks
  → Check prompt for: team size, availability, prior free tools
  → If missing, ask: "How much engineering time can you budget for building the tool? Even 2-4 weeks is enough for a simple calculator."

### Observable Context

- **Existing product:** what the tool should funnel toward
- **Current lead generation:** what the tool would replace or complement

### Default Assumptions
- Single-input-field is the ideal pattern (paste URL, get report)
- The tool should be genuinely useful on its own, not a sales pitch
- Lead capture happens after the value is delivered, not before

### Sufficiency Threshold

```
SUFFICIENT: ideal customer + core question + engineering capacity known
PROCEED WITH DEFAULTS: customer known, brainstorm common category questions
MUST ASK: customer is too vague to identify the core question
```

## Process

Use TodoWrite:
- [ ] Step 1: Identify the core customer question
- [ ] Step 2: Design the smallest tool that answers it
- [ ] Step 3: Apply the single-input-field pattern
- [ ] Step 4: Plan lead capture flow
- [ ] Step 5: Set up distribution (SEO, blog integration, sharing)

### Step 1: Identify the Core Customer Question

**ACTION:** Find the ONE specific question the ideal customer asks before they're ready to pay for your product. Not "what should I do about marketing" but "is my marketing working well enough?" or "how does my site compare to competitors?"

Examples:
- **HubSpot:** "How good is my marketing?" → Marketing Grader (enter URL, get score)
- **Moz:** "Who follows my target audience on Twitter?" → Followerwonk
- **Moz:** "How many backlinks does a site have?" → Open Site Explorer
- **DuckDuckGo:** "How is Google tracking my searches?" → DontTrack.us micro-site

The question must be:
- Specific enough to answer definitively
- Valuable enough that the customer would actively seek an answer
- Related enough to your product that users who care about it are leads

**WHY:** Generic free tools produce generic leads. HubSpot's Marketing Grader attracts people who care about marketing quality — which is exactly HubSpot's ideal customer. A generic "business calculator" attracts everyone and converts no one. The tool must match the question, and the question must match the customer.

### Step 2: Design the Smallest Tool That Answers It

**ACTION:** Strip the tool to the minimum viable answer:
- One input field (URL, email, company name, Twitter handle)
- One clear output (score, report, comparison, list)
- No gates before the value is delivered
- No login required (or optional at most)

Budget: 2-4 weeks of engineering for a first version. Resist feature creep.

Write the design spec to `tool-design.md`.

**WHY:** Complexity is the enemy of adoption. HubSpot Marketing Grader succeeded partly because it was embarrassingly simple — paste a URL, get a grade. If it had required a 20-question survey first, 90% of users would have dropped off. The friction-to-value ratio is the core metric.

### Step 3: Apply the Single-Input-Field Pattern

**ACTION:** Design the landing page around a single input field, centered, with minimal distractions. The user types or pastes one thing and clicks one button. Everything else waits until after the result is shown.

Elements to include ON the landing page:
- Headline (what the tool does in 6 words)
- Single input field
- Single action button
- One line of credibility ("Used by 3M sites")

Elements to EXCLUDE from the landing page:
- Feature lists
- Pricing
- Multi-step signup
- Login wall
- Pop-ups before result

**WHY:** Every additional element on the landing page reduces conversion to first-use. The single-input pattern removes all friction between "user arrives" and "user gets value." The sales pitch happens after the value is delivered, when the user is in a "this is useful" state — not before, when they're evaluating whether to try.

### Step 4: Plan Lead Capture Flow

**ACTION:** Design what happens AFTER the user gets their result:

- Show the valuable result immediately (no email wall)
- Offer to email the result for future reference (email capture, optional)
- Offer a "deeper analysis" or "personalized report" in exchange for email (stronger capture)
- Show a product CTA that's relevant to the result ("Your score is 65. Our product can get you to 90.")
- Add social sharing (especially if the result is shareable, like a grade)

Write the flow to `tool-capture-flow.md`.

**WHY:** Gating value behind email collection kills conversion. Delivering value first and asking for email second (for "send me my report" or "notify me of improvements") captures email at 30-50% rates instead of 5%. The sequence matters: value → capture, not capture → value.

### Step 5: Distribution

**ACTION:** The tool is built — how do people find it?

Distribution channels for tools:
- **SEO:** the tool ranks for queries like "is my marketing working" (HubSpot's strategy)
- **Blog integration:** tool embedded in or linked from related blog posts
- **Share hooks:** results users share publicly (leaderboards, grades) drive viral growth
- **Partnership distribution:** tool offered as free addon to partners' audiences
- **Direct promotion:** launch on Product Hunt, Hacker News, Reddit

**WHY:** A great tool that nobody finds is worthless. Distribution is half the work. The tool's SEO properties (keyword-rich domain, targeted landing page) compound over time and often become the biggest traffic source.

## Inputs

- Ideal customer description and core question
- Engineering capacity
- Existing product to funnel toward

## Outputs

Three markdown files:

1. **`tool-design.md`** — Core question, input, output, scope constraints
2. **`tool-capture-flow.md`** — Post-result flow, email capture, product CTA
3. **`tool-distribution.md`** — Distribution channels and launch plan

## Key Principles

- **The question matters more than the tool.** A perfect tool for the wrong question produces zero leads. A simple tool for the right question produces millions. WHY: Tool quality is a secondary factor. Match to customer intent is the primary factor.

- **Single input field is the ideal pattern.** Less friction = more users. WHY: Every additional form field cuts conversion. The single-input pattern maximizes users-who-try, which is the top of the lead funnel.

- **Deliver value first, capture email second.** Gating kills conversion. WHY: Email capture rates are 5-10% when value is gated, 30-50% when value is delivered first. Users who got value are in a friendly state; users who hit a gate are in a hostile state.

- **Don't confuse "free tool" with "feature preview".** A free tool is a standalone utility that's valuable even if the user never buys your product. A feature preview is a crippled version of your product. Users can tell the difference. WHY: Standalone tools build trust; feature previews feel like bait-and-switch.

- **Avoid the engineering resource hoarding anti-pattern.** "Companies have a hard time using engineering resources for anything but product development." Most founders use all engineering time on product features. Don't. WHY: Engineering as marketing produces ongoing lead flow from a one-time investment. Product features produce incremental value per feature. The ROI comparison favors tools for most startups.

- **The tool's SEO compounds.** Unlike ads, a well-ranked tool produces traffic indefinitely. WHY: One-time engineering investment + long-lived traffic = asymmetric return. HubSpot Marketing Grader has generated leads for 15+ years from its initial build.

## Examples

**Scenario: B2B SaaS with spare engineering capacity**

Trigger: "We have 2 engineers on the bench for 4 weeks. We sell analytics software to marketers. What should we build?"

Process: (1) Core question: "Is my website's analytics setup correct?" — something marketers worry about. (2) Tool design: paste URL → crawl for Google Analytics, GTM, event tracking, UTM consistency → score report. (3) Single-input: URL field + "Check my site" button. (4) Capture: show score immediately, "email me the full report" capture. Product CTA: "Our tool fixes these 5 issues automatically." (5) Distribution: SEO on "analytics audit", launch on Product Hunt, embed on analytics blog.

Output: Complete tool spec, lead flow, distribution plan.

**Scenario: Consumer health app**

Trigger: "We have a meal tracking app. Want to use engineering-as-marketing. Ideas?"

Process: (1) Core question: "How healthy is my diet?" — universal question for target audience. (2) Tool: "Paste your last 3 days of meals → AI analyzes nutrition and grades your diet." (3) Single input: text area for meal entries. (4) Capture: show grade immediately, "Save your progress" (email capture for 7-day tracking). Product CTA: "Our app auto-tracks this every day." (5) Distribution: SEO on "healthy diet quiz", Instagram/TikTok shareable results.

Output: Tool concept, social-friendly result design, distribution plan.

**Scenario: Founder pulled between product and tool**

Trigger: "Engineering team has 3 weeks free. But I'm worried we should use that time to fix bugs in the product. Which is better?"

Process: (1) Engineering resource hoarding anti-pattern in action. (2) Frame the trade-off: 3 weeks of bug fixes = marginal improvement to existing users. 3 weeks building a free tool = ongoing lead flow for years. ROI comparison strongly favors the tool. (3) Caveat: if the bugs are P0/churn-causing, fix them first. If they're "nice to have", build the tool. (4) Tool recommendation based on customer question. (5) Commit to the decision: don't build half a tool and half a bug fix.

Output: Clear decision framing that breaks the engineering-hoarding default.

## References

- For lead capture flow variants and conversion benchmarks, see [references/tool-patterns.md](references/tool-patterns.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select Engineering as Marketing deliberately
- `clawhub install bookforge-seo-channel-strategy` — Tools rank for long-tail queries naturally
- `clawhub install bookforge-content-and-email-marketing` — Tools capture emails for lifecycle marketing

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
