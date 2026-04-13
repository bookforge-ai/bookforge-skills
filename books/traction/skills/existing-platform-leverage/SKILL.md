---
name: existing-platform-leverage
description: "Leverage existing platforms with large user bases (App Stores, browser extensions, social networks, super-platforms) for startup customer acquisition via parasitic growth patterns. Use whenever a founder is planning to distribute via app stores, building browser extensions, targeting Facebook or Twitter as a channel, launching on a new platform Day-1, exploiting an unsatisfied need on a larger platform, or mapping platform gap opportunities. Activates on phrases like 'App Store strategy', 'Chrome extension', 'browser extension', 'Facebook platform', 'Apple ecosystem', 'existing platforms', 'distribution platform', 'Product Hunt launch', 'Airbnb Craigslist', 'YouTube MySpace', 'Zynga Facebook', 'parasitic growth'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/existing-platform-leverage
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [21]
domain: startup-growth
tags: [startup-growth, platform-strategy, app-stores, viral-distribution, parasitic-growth]
depends-on: [bullseye-channel-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Product description, target platforms, platform gap hypothesis"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for platform strategy and launch plans"
discovery:
  goal: "Identify and exploit unsatisfied needs on larger platforms to drive startup acquisition"
  tasks:
    - "Map platforms where the target audience spends time"
    - "Identify platform gaps and unsatisfied needs"
    - "Design a minimal solution that bridges user to the platform"
    - "Plan Day-1 launch strategy for new platforms"
    - "Mitigate platform dependency risk"
  audience:
    roles: [startup-founder, growth-marketer, product-manager]
    experience: intermediate
  when_to_use:
    triggers:
      - "A larger platform has an unsatisfied need your product could serve"
      - "New platform launching soon (Day-1 opportunity)"
      - "User is planning an App Store or extension strategy"
      - "Bullseye selected Existing Platforms as inner circle"
    prerequisites:
      - skill: bullseye-channel-selection
        why: "Existing Platforms should be selected deliberately"
    not_for:
      - "Products that don't complement any existing platform"
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

# Existing Platform Leverage

## When to Use

The startup could grow by leveraging an existing platform with a large user base. Use this skill when:

- A big platform (App Store, browser, social network) has a gap your product could fill
- A new platform is launching that you could be on Day-1
- Your target customers already spend time on a specific platform
- You want to reach millions of users without building your own distribution

Common platforms to leverage: iOS/Android App Stores, Chrome/Firefox Web Stores, Facebook/Twitter APIs, Slack app directory, Shopify/WordPress plugins, VS Code extensions, Product Hunt.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Target audience:** who you want to reach
  → Check prompt for: customer profile, demographics
  → If missing, ask: "Who are your target customers, and which platforms do they already spend time on?"

- **Product form factor:** can your product live on another platform, or does it require its own app/site
  → Check prompt for: product type, technical form factor
  → If missing, ask: "What form does your product take? Mobile app, web app, browser extension, Slack bot, etc?"

### Observable Context

- **Existing platform presence:** any existing listings, integrations
- **Technical feasibility:** can the team ship platform-specific versions

### Default Assumptions
- Parasitic growth requires identifying an unsatisfied need on the larger platform
- Day-1 launches on new platforms get featured in launch marketing
- Platform dependency is a real risk — have an exit plan

### Sufficiency Threshold

```
SUFFICIENT: target audience + product form factor + candidate platforms known
PROCEED WITH DEFAULTS: audience known, infer platform candidates
MUST ASK: audience is completely unknown
```

## Process

Use TodoWrite:
- [ ] Step 1: Map platforms where target audience spends time
- [ ] Step 2: Identify unsatisfied needs (platform gaps)
- [ ] Step 3: Design the minimal bridge solution
- [ ] Step 4: Plan Day-1 strategy (if applicable)
- [ ] Step 5: Mitigate platform dependency risk

### Step 1: Map Platforms Where Target Audience Spends Time

**ACTION:** List every platform with substantial presence of your target audience. Include:

- **App stores:** iOS App Store, Google Play, Mac App Store, Microsoft Store
- **Browser stores:** Chrome Web Store, Firefox Add-ons, Safari Extensions, Edge
- **Social networks:** Facebook, Twitter, LinkedIn, Reddit, Instagram, TikTok
- **Developer platforms:** GitHub, VS Code Marketplace, JetBrains plugins
- **Work platforms:** Slack App Directory, Microsoft Teams apps, Zoom marketplace
- **E-commerce platforms:** Shopify apps, WordPress plugins, BigCommerce apps
- **Aggregators:** Product Hunt, Hacker News, Reddit (category-specific)

Write to `platform-map.md` with estimated audience presence per platform.

**WHY:** Founders default to "the App Store" and miss the 10 other platforms their customers use. A developer-tool company targets VS Code Marketplace, not the Apple App Store. A productivity tool for remote teams targets Slack App Directory. Mapping reveals the best-fit platforms, not just the biggest ones.

### Step 2: Identify Unsatisfied Needs (Platform Gaps)

**ACTION:** For each promising platform, identify what the platform's users need that the platform itself doesn't provide well. These gaps are the parasitic growth opportunities.

Classic examples:
- **Airbnb on Craigslist:** Craigslist users needed safer, better-designed alternatives for room rentals. Airbnb was the better solution.
- **PayPal on eBay:** eBay sellers needed a trusted payment method eBay didn't provide. PayPal filled the gap.
- **YouTube on MySpace:** MySpace users needed video hosting MySpace didn't offer. YouTube embed code bridged the gap.
- **Zynga on Facebook:** Facebook users needed games. Zynga dominated before competition.
- **Imgur on Reddit:** Reddit users needed image hosting. Imgur was built specifically for Reddit.
- **Bit.ly on Twitter:** Twitter users needed link shortening. Bit.ly filled the need.

The pattern: **find what users of the big platform are struggling with, and provide the solution.**

**WHY:** Platforms can't fix every user need — their priorities are constrained. Gaps are persistent. A startup that solves a real gap becomes the default solution for that gap and rides the platform's growth.

**IF** no clear gap exists → the platform isn't the right channel.

### Step 3: Design the Minimal Bridge Solution

**ACTION:** Build the smallest product that bridges platform users to your solution. The bridge should:

- Work entirely within the platform's context (no platform switch required)
- Require minimal friction to try
- Deliver value on the first use
- Drive users back to your core product over time (or monetize in-platform)

Airbnb's "Post to Craigslist" feature: one button that cross-posted Airbnb listings to Craigslist. Users didn't need to leave Craigslist to discover Airbnb. This drove tens of thousands of Craigslist users to Airbnb.

**WHY:** A full standalone product requires users to switch platforms and learn new interfaces. A bridge meets users where they are. Bridges have higher conversion because they reduce context-switching cost.

### Step 4: Plan Day-1 Strategy for New Platforms

**ACTION:** When a new platform launches, being on Day-1 produces:

- **Launch marketing feature** — platform launch announcements often highlight partner apps
- **Less competition** — fewer apps in the store = higher visibility per app
- **Platform goodwill** — the platform maker remembers partners who supported them early

Evernote's strategy: launched on every new platform on Day-1 (iPhone, iPad, Android, Kindle Fire). Phil Libin: "We really killed ourselves to always be in all of the App Store launches on day one."

Prepare:
- Technical readiness 4-6 weeks before platform launch
- Launch-day assets (screenshots, demo video, press release)
- Developer relations contact at the platform

**WHY:** Platform launch days are high-attention moments. Being in the launch-day lineup produces outsized awareness for minimal cost. Missing the window means competing with hundreds of late-arriving apps. Evernote's Day-1 strategy made the company a household name on iOS specifically because they were first.

**IF** no new platform is launching soon → focus on Step 3's bridge strategy on existing platforms.

### Step 5: Mitigate Platform Dependency Risk

**ACTION:** Platform leverage is powerful but risky. Platforms change rules, APIs, and access policies. Mitigate:

- **Diversify across platforms** — don't rely on one platform for >50% of traffic
- **Build direct relationships with users** — capture email, build community, drive repeat visits outside the platform
- **Monitor platform policy changes** — watch for warning signs early
- **Have an exit plan** — if the platform cuts off access, what's your fallback?

Cautionary tale: Zynga's Facebook dependency. When Facebook changed its platform policies and algorithm, Zynga's growth cratered. Similar issues for companies dependent on Google's SEO algorithm, Twitter's API, Facebook's News Feed.

Airbnb's Craigslist dependency: eventually Craigslist blocked the "Post to Craigslist" feature. Airbnb had by then built its own brand and growth, but the dependency was always a risk.

**WHY:** Platform dependency creates tail risk. The platform giveth and the platform taketh away. Mitigation isn't paranoia — it's the standard practice of any company with substantial platform exposure.

## Inputs

- Target audience description
- Product form factor
- Candidate platform list

## Outputs

Four markdown files:

1. **`platform-map.md`** — Platforms where target audience spends time
2. **`platform-gaps.md`** — Unsatisfied needs per platform
3. **`bridge-solution.md`** — Minimal solution design bridging platform to product
4. **`platform-dependency-plan.md`** — Dependency risk mitigation plan

## Key Principles

- **Find gaps, don't build parallel platforms.** Leverage works because the platform's users are already there. Don't try to replicate the platform. WHY: Replicating a platform competes with it; filling a gap complements it. Gaps are welcomed; replicas are blocked.

- **Meet users where they are.** The best bridge requires no platform switching. Airbnb posted listings to Craigslist; users discovered Airbnb inside Craigslist. WHY: Every required context switch loses users. The bridge should work in the platform's native environment.

- **Day-1 matters disproportionately.** New platform launches are rare marketing moments. Being first produces outsized results. WHY: Launch-day attention is finite and concentrated. Day-100 attention is diffused. Same app, radically different outcomes by timing.

- **Platform dependency has tail risk.** The platform can cut you off. Plan for it. WHY: Platforms change rules without warning. Companies with one-platform dependency are betting their existence on that platform's continued goodwill.

- **Parasitic is not pejorative.** Using an existing platform's user base is a legitimate strategy. PayPal, YouTube, and Airbnb all did it. WHY: "Parasitic" describes the mechanics, not ethics. All three became beloved products despite starting parasitically.

## Examples

**Scenario: Developer tool for VS Code**

Trigger: "We built a code quality tool for JavaScript developers. How do we get users?"

Process: (1) Platform map: VS Code Marketplace is where JavaScript devs live. Secondary: GitHub Marketplace, Chrome Web Store (for dev tools extensions). (2) Platform gaps: VS Code doesn't have integrated AI code quality checking — gap. (3) Bridge solution: VS Code extension that installs with one click, runs in the background, shows issues inline. (4) Day-1 strategy: watch for VS Code's next major release and be ready to integrate with new APIs. (5) Dependency risk: build a parallel web version and capture emails.

Output: Platform-native strategy with VS Code Marketplace as primary channel.

**Scenario: Consumer app exploring Product Hunt**

Trigger: "We're launching a new consumer app next month. Should we launch on Product Hunt?"

Process: (1) Yes, Product Hunt is an aggregator for early-adopter consumer audiences. (2) Gap: not a traditional gap, but Product Hunt is where new products get discovered. (3) Bridge: simple launch with demo video, founder story, 24-hour engagement. (4) Day-1 strategy: coordinate launch with Hacker News submission, Reddit (if appropriate subreddit), and Twitter thread. (5) Dependency: Product Hunt alone is not sustainable — use it as a launch moment, not an ongoing channel.

Output: Multi-platform launch plan with Product Hunt as the focal day-1 event.

**Scenario: Chrome extension opportunity**

Trigger: "Our web research tool could work as a Chrome extension. Worth the effort?"

Process: (1) Platform map: Chrome Web Store has 3B+ users, strong discovery for productivity tools. (2) Gap: Chrome's default search and bookmarking don't help with research workflows — clear gap. (3) Bridge: extension that works inline in the browser without requiring a separate app. One-click install, zero onboarding. (4) Day-1: not a new platform but consider launching via Hacker News and r/productivity as the first 48 hours. (5) Dependency: Chrome Web Store has removed extensions before (policy changes). Build a web app fallback and capture emails.

Output: Chrome extension as primary channel, web fallback for dependency mitigation.

## References

- For case studies of parasitic growth patterns (Airbnb/Craigslist, etc), see [references/parasitic-growth-cases.md](references/parasitic-growth-cases.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select Existing Platforms via Bullseye
- `clawhub install bookforge-viral-growth-loop-design` — Embedded virality overlaps with platform leverage
- `clawhub install bookforge-engineering-as-marketing` — Tools on platforms are a parallel pattern

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
