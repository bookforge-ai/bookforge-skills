---
name: seo-channel-strategy
description: "Select and execute an SEO strategy using the fat-head vs long-tail binary decision framework. Use whenever a founder or marketer is planning SEO, comparing organic search strategies, choosing between targeting high-volume category keywords or many low-volume long-tail terms, evaluating keyword difficulty, planning content production for SEO, or avoiding black-hat tactics. Activates on phrases like 'SEO strategy', 'SEO', 'search engine optimization', 'organic search', 'ranking on Google', 'keyword research', 'fat-head', 'long-tail', 'content for SEO', 'Moz', 'keyword difficulty', 'link building', 'SERP', 'backlinks'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/seo-channel-strategy
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [13]
domain: startup-growth
tags: [startup-growth, seo, organic-search, content-marketing, keyword-strategy]
depends-on: [bullseye-channel-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Product category, competitor list, current SEO metrics"
  tools-required: [Read, Write]
  tools-optional: [WebFetch, AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for SEO strategy and keyword plans"
discovery:
  goal: "Select fat-head vs long-tail SEO strategy and produce an executable plan"
  tasks:
    - "Determine whether existing search demand exists for the category"
    - "Evaluate fat-head keyword feasibility (page-1 ranking, 10% capture test)"
    - "Apply the binary fat-head vs long-tail decision"
    - "Design keyword evaluation process (Keyword Planner → volume → competition)"
    - "Plan content production pipeline for long-tail strategy"
    - "Avoid black-hat SEO tactics"
  audience:
    roles: [startup-founder, growth-marketer, content-marketer]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User is planning SEO for a new product"
      - "Current SEO strategy isn't producing traffic"
      - "User is choosing between fat-head and long-tail"
      - "Content production for SEO needs prioritization"
    prerequisites:
      - skill: bullseye-channel-selection
        why: "SEO should be selected via Bullseye, especially for new product categories"
    not_for:
      - "Products with no existing search demand (demand creation, not fulfillment)"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: false
  quality:
    scores:
      with_skill: null
      baseline: null
      delta: null
    tested_at: null
    eval_count: 0
    assertion_count: 11
    iterations_needed: 0
---

# SEO Channel Strategy

## When to Use

The startup is evaluating SEO as a channel or rebuilding an existing SEO strategy. Before starting, verify:

- There is some existing search demand for the category, OR the user accepts that long-tail-only is the path
- The user can commit to a months-long time horizon (SEO compounds slowly)
- A content production capability exists (in-house or freelance)

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Product category and target audience:** what people might search for
  → Check prompt for: product name, category description, ideal customer
  → If missing, ask: "What does your product do, and who searches for products like yours?"

- **Competitor list:** who else ranks for the relevant terms
  → Check prompt for: competitor names, category incumbents
  → If missing, ask: "Who are the main competitors already ranking for terms in your category?"

### Observable Context

- **Current organic traffic:** if any
- **Domain authority:** new domain vs established
- **Content production capacity:** in-house writers, freelance budget

### Default Assumptions
- Only 10% of clicks go beyond the first 10 search results — page 1 or nothing
- Test fat-head keywords via SEM first before committing to SEO investment
- Long-tail requires template + freelance production pipeline at scale

### Sufficiency Threshold

```
SUFFICIENT: category + audience + competitors known
PROCEED WITH DEFAULTS: category known, use Keyword Planner to discover competitors
MUST ASK: category or product is unknown
```

## Process

Use TodoWrite:
- [ ] Step 1: Check for existing search demand
- [ ] Step 2: Evaluate fat-head feasibility
- [ ] Step 3: Make the binary fat-head vs long-tail decision
- [ ] Step 4: Design keyword evaluation process
- [ ] Step 5: Plan content production pipeline
- [ ] Step 6: Avoid black-hat tactics

### Step 1: Check For Existing Search Demand

**ACTION:** Use Google Keyword Planner (or equivalent tool) to check search volume for category terms. If there's zero or near-zero volume, the category is too new for SEO to work via fat-head. Users need to already be searching for something.

Example disqualifier: Uber in its early days — nobody was searching for "alternatives to taxi cabs via phone app" because the category didn't exist yet. SEO couldn't create that demand.

**WHY:** SEO is demand fulfillment, not demand creation. No search demand = no SEO opportunity. Spending SEO resources on a category nobody searches for produces zero traffic regardless of how perfect the content is.

**IF** no existing search demand → SEO is not a primary channel. Return to Bullseye.

### Step 2: Evaluate Fat-Head Feasibility

**ACTION:** For the category terms with search demand, check:

1. **Monthly search volume** — is it meaningful? Use the 10% capture test: if you captured 10% of monthly searches, would that actually matter for your traction goal?
2. **Competitor strength** — use Open Site Explorer (Moz) or equivalent to check competitor backlink counts. High competitor link counts = very hard to rank on page 1.
3. **Page-1 feasibility** — realistic check. Only 10% of clicks go beyond page 1. Ranking 12 is worthless.

Test fat-head keywords via SEM first: buy a few hundred dollars of Google Ads on the target terms. If they convert well, SEO is worth pursuing. If they don't convert on paid, SEO won't rescue them.

**WHY:** Page-1 ranking is the actual goal, not "ranking." Ranking 2nd or 3rd page produces near-zero traffic. If the competition is too strong for page 1, long-tail is the better strategy. The SEM pre-test is cheap validation — it saves months of SEO work on keywords that wouldn't have converted anyway.

### Step 3: Make the Binary Fat-Head vs Long-Tail Decision

**ACTION:** Based on Steps 1-2, apply the binary decision:

**Fat-Head Strategy** if:
- Existing category search demand is high
- Your product directly describes what people search for
- Competition is beatable (you can plausibly rank on page 1)
- SEM pre-test showed those keywords convert

**Long-Tail Strategy** if:
- Fat-head is too competitive
- Your product has niche use cases or specific buyer personas
- You can produce large volumes of targeted content
- Long-tail aggregates to meaningful volume in your category

Write the strategy decision to `seo-strategy.md`.

**WHY:** The binary is not "do both" — at early stage, you have to commit resources to one or the other. Fat-head requires link building and authority; long-tail requires content production at scale. These are different operational patterns. Splitting effort means under-investing in both. Choose one, execute it, revisit in 6 months.

### Step 4: Design Keyword Evaluation Process

**ACTION:** For the chosen strategy, build a keyword evaluation pipeline:

**Fat-head process:**
1. Use Google Keyword Planner for volumes on category terms
2. Check Google Trends for trajectory and geography
3. Use Open Site Explorer for competitor backlink counts
4. Validate via SEM paid test ($500)
5. If all checks pass → pursue SEO

**Long-tail process:**
1. Use Keyword Planner for long-tail variants (add modifiers like location, use case, persona)
2. Check own analytics for existing long-tail traffic
3. Analyze competitors with `site:domain.com` to see their long-tail coverage
4. Create standard landing page template
5. Hire freelancers to produce targeted content per keyword bucket
6. Add geographic modifiers for local variants

**WHY:** Both strategies need rigorous keyword evaluation — but the rigor is different. Fat-head needs competitive analysis because you're attacking crowded terms. Long-tail needs scale tooling because you're producing hundreds of pages. Designing the process upfront prevents reactive keyword picking.

### Step 5: Plan Content Production Pipeline (Long-Tail)

**ACTION:** If pursuing long-tail, design the production pipeline:

- **Template:** a standard landing page layout that fits every long-tail keyword
- **Freelance sourcing:** Upwork, Elance, specialized content agencies
- **Quality control:** checklist for on-page SEO (title, H1, meta description, word count, internal links)
- **Geographic modifier system:** for local variants, use template + city-specific data
- **Content calendar:** weekly production targets

Long-tail strategy economics: $3-10 per article via freelancers, compounds over time as pages rank.

**WHY:** Long-tail doesn't work without scale. Writing 10 long-tail pages produces 10 visitors/month. Writing 1,000 produces meaningful traffic. The pipeline is what makes 1,000 possible without each page being bespoke. Founders who skip the pipeline write 20 pages manually and give up.

### Step 6: Avoid Black-Hat Tactics

**ACTION:** Document the anti-patterns to avoid — see [references/black-hat-seo.md](references/black-hat-seo.md).

The biggest: **don't buy links.** Buying links is against search engine guidelines and produces severe ranking penalties when detected (which is increasingly reliable).

Other black-hat tactics to avoid: cloaking, keyword stuffing, hidden text, doorway pages, content spinning, comment spam.

**WHY:** Black-hat tactics can work in the short term (which is why they're tempting), but search engines detect and penalize them. The penalty often destroys organic traffic entirely — not just reduces it. "I rarely see startups fail because they didn't have a good idea. Where I see 90% of startups fail is because they can't reach their customers." — Rand Fishkin. Black-hat shortcuts are one of the ways that "can't reach customers" happens.

## Inputs

- Product category
- Target audience
- Competitor list
- Content production capacity

## Outputs

Four markdown files:

1. **`seo-strategy.md`** — Fat-head vs long-tail decision with reasoning
2. **`seo-keyword-plan.md`** — Evaluated keywords with volumes and difficulty
3. **`seo-content-pipeline.md`** — Content production plan (long-tail only)
4. **`seo-avoid-list.md`** — Black-hat tactics to explicitly avoid

## Key Principles

- **SEO is demand fulfillment, not demand creation.** Without existing search volume, SEO can't work. WHY: If nobody searches for what you do, no amount of content will get you traffic. SEO depends on users already looking for something.

- **Page 1 or nothing.** Only 10% of clicks go beyond first 10 results. Ranking 12 is worthless. WHY: Organic click-through drops off precipitously by position. The game is page 1; second page is failure.

- **Test with SEM before investing in SEO.** SEM produces keyword validation in days. SEO takes months. Don't commit to SEO on keywords you haven't validated. WHY: Months of wasted SEO work on non-converting keywords is a common failure. $500 of SEM ads answers "does this convert?" in 2 weeks.

- **Fat-head vs long-tail is binary at early stage.** Pick one. Split effort = under-investment in both. WHY: These strategies have different operational patterns. Link building for fat-head is a different skill and tool set than content production at scale for long-tail.

- **Long-tail needs a pipeline, not one-off writing.** 1,000 pages beats 10 pages. Template + freelancers + quality control. WHY: Long-tail's value is aggregation. 10 pages produces a trickle; 1,000 pages produces traffic. The pipeline is what enables scale.

- **Never buy links.** The penalty is worse than the short-term benefit. WHY: Search engines detect paid links increasingly reliably. The penalty destroys traffic. The short-term gain is not worth the catastrophic long-term risk.

## Examples

**Scenario: New SaaS category with no search demand**

Trigger: "We built AI-powered contract review for small law firms. Nobody searches for 'AI contract review for small law firms'. How do we SEO this?"

Process: (1) Check Keyword Planner — zero volume on the specific term. (2) Broaden: "contract review software" has volume but competitors are $50M companies. (3) Long-tail path: "contract review software for small law firms", "AI contract review tool for solo attorneys", "NDA review software". (4) SEM pre-test on 3 long-tail clusters — 2 convert. (5) Long-tail strategy: template landing pages + freelancer pipeline for 50 specific long-tail pages in Q1.

Output: Clear decision that fat-head isn't viable, long-tail path with specific keyword clusters and production plan.

**Scenario: Established category with beatable competitors**

Trigger: "We make a note-taking app. 'Note taking app' has 50k searches/month. Competitors: Evernote, Notion, Apple Notes. Should we do SEO?"

Process: (1) Keyword Planner confirms 50k/month. (2) 10% capture test: 5k visits/month. Meaningful? Depends on conversion — probably yes for early stage. (3) Competitor check: Evernote has 300k backlinks, Notion has 500k, Apple Notes dominates. Page-1 for "note taking app" is impossible without years of link building. (4) Fat-head infeasible → long-tail it is. (5) Long-tail clusters: "note taking app for [profession]", "note taking app with [feature]", "Evernote alternative for [use case]".

Output: Long-tail strategy with specific cluster plan, acknowledgment that fat-head is a 3+ year play.

**Scenario: Buying links temptation**

Trigger: "An agency offered to sell us 100 backlinks from finance blogs for $2,000. Our SEO hasn't been growing. Should we do it?"

Process: (1) Identify this as the black-hat temptation. (2) Explain the penalty: if Google detects paid links (which is increasingly reliable), you lose rankings across the whole site, not just for these keywords. (3) Recovery from penalties takes 3-6 months of disavow work. (4) Calculate expected value: short-term gain 3-month boost × 20% chance it works + long-term penalty worth $50k of lost traffic × 60% chance of detection = catastrophically negative EV. (5) Alternative: invest the $2,000 in 2-3 guest posts on relevant blogs via legitimate outreach.

Output: Clear rejection with EV calculation, alternative white-hat plan.

## References

- For black-hat tactics to avoid and legitimate link-building alternatives, see [references/black-hat-seo.md](references/black-hat-seo.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select SEO via Bullseye deliberately
- `clawhub install bookforge-sem-performance-optimization` — Validate SEO keywords with SEM first
- `clawhub install bookforge-content-and-email-marketing` — Content is the long-tail SEO production system

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
