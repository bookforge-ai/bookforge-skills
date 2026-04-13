---
name: startup-pr-outreach
description: "Guide startup PR and unconventional PR outreach using the media chain, pitch templates, and amplification tactics. Use whenever a founder or marketer needs to pitch reporters, plan a PR campaign, land media coverage, run a publicity stunt, amplify a press story, use HARO, build reporter relationships, or avoid common PR mistakes. Also covers unconventional PR (stunts, customer appreciation) for startup launches. Activates on phrases like 'press release', 'PR campaign', 'media coverage', 'reporter outreach', 'pitch email', 'TechCrunch', 'HARO', 'product launch', 'PR strategy', 'publicity stunt', 'get coverage', 'press pitch', 'media pitch', 'journalist outreach'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/traction/skills/startup-pr-outreach
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: traction
    title: "Traction: A Startup Guide to Getting Customers"
    authors: ["Gabriel Weinberg", "Justin Mares"]
    chapters: [7, 8]
domain: startup-growth
tags: [startup-growth, public-relations, media-outreach, press-pitching, launch-marketing]
depends-on: [bullseye-channel-selection]
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Company milestones, target media outlets, pitch angles, launch details"
  tools-required: [Read, Write]
  tools-optional: [AskUserQuestion]
  mcps-required: []
  environment: "Plain-text working directory for pitch drafts and media outreach tracker"
discovery:
  goal: "Produce a PR campaign plan with pitch drafts, target outlet list, and amplification sequence"
  tasks:
    - "Identify a milestone worth PR coverage"
    - "Build a media chain starting with small blogs"
    - "Draft pitches using the two proven templates"
    - "Apply the emotional angle criteria"
    - "Avoid the 6 named PR pitching mistakes"
    - "Plan the amplification sequence after coverage lands"
  audience:
    roles: [startup-founder, head-of-marketing, pr-lead]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "Product launch approaching"
      - "Startup has a newsworthy milestone"
      - "Previous PR attempts produced no coverage"
      - "Bullseye selected PR as inner-circle channel"
    prerequisites: []
    not_for:
      - "Phase I startups with nothing newsworthy yet (use targeting blogs instead)"
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

# Startup PR Outreach

## When to Use

The startup needs media coverage or is planning a PR campaign. Use this skill when:

- A newsworthy milestone has happened or is about to happen (funding, launch, usage threshold, partnership)
- The user wants to reach a broad audience via trusted intermediaries (reporters)
- Previous PR attempts produced no coverage
- Planning a publicity stunt or unconventional PR tactic

PR is typically a Phase II+ channel. Phase I startups without newsworthy milestones should use targeting blogs instead.

## Context & Input Gathering

### Required Context (must have — ask if missing)

- **Milestone / angle:** what's actually newsworthy
  → Check prompt for: "launching", "raised", "hit X users", "partnership with"
  → If missing, ask: "What specific milestone are you trying to get coverage for? Launches, funding, user thresholds, and industry partnerships typically work. Vague product announcements don't."

- **Target audience:** who the story should reach
  → Check prompt for: developer, consumer, enterprise buyer, specific vertical
  → If missing, ask: "Who is the ideal reader? That determines which outlets and reporters to target."

### Observable Context

- **Existing media relationships:** prior coverage, reporter connections
- **Spokesperson availability:** founder, press-ready team members

### Default Assumptions
- Start with small blogs, not top-tier outlets (media chain principle)
- Founders pitch better than PR firms for early-stage startups
- Bundle smaller announcements into bigger ones when possible

### Sufficiency Threshold

```
SUFFICIENT: milestone + target audience known
PROCEED WITH DEFAULTS: milestone known, infer target from context
MUST ASK: no milestone exists (not newsworthy)
```

## Process

Use TodoWrite:
- [ ] Step 1: Identify/bundle the newsworthy angle
- [ ] Step 2: Build the media chain (small → top)
- [ ] Step 3: Build reporter relationships via Twitter/HARO
- [ ] Step 4: Draft pitches using proven templates
- [ ] Step 5: Plan amplification sequence

### Step 1: Identify and Bundle the Newsworthy Angle

**ACTION:** Determine what's actually newsworthy. Strong angles include:
- Funding round (especially with notable investors)
- Product launch with a specific unique hook
- Usage threshold crossed (1M users, 100k searches, etc.)
- Partnership with a recognizable brand
- A stunt or unconventional event (see unconventional PR)
- An industry report or data set only you have

**Bundle smaller announcements.** Jason Kincaid's advice: don't pitch small milestones individually if they can be combined. "Launched feature X" is weak. "Launched feature X + hit 10k users + signed partnership with Y" is strong.

The **emotional angle test**: ask "will this elicit an emotion in readers beyond satisfaction?" Satisfaction is a non-viral emotion. Stories that make readers share need to produce surprise, delight, outrage, or curiosity.

**WHY:** Reporters receive 50+ pitches daily. The first filter is "is this actually a story?" Bundled, emotionally-engaging milestones clear the filter. Single-milestone pitches get ignored. This isn't about hype — it's about giving the reporter enough material to write an interesting article.

**IF** no angle emerges → delay PR, build more milestones first, or pivot to targeting blogs for content-led coverage.

### Step 2: Build the Media Chain (Small → Top)

**ACTION:** Stories filter UP the media chain. Small blogs → TechCrunch → New York Times. Start small, not at the top.

Identify the chain for your category:
- **Level 1 (entry):** Hacker News, Reddit, Product Hunt, niche industry blogs, HARO responses
- **Level 2 (mid-tier):** TechCrunch, The Verge, Wired, industry publications
- **Level 3 (top-tier):** NYT, WSJ, mainstream TV, national podcasts

Target Level 1 first. Top outlets (Level 2-3) often pick up stories from Level 1. DuckDuckGo's Time Magazine feature came via a Twitter relationship with a reporter who then included DDG in a Top 50 list — not via a cold pitch to Time.

**WHY:** Cold-pitching top outlets has near-zero success rate. Most top reporters scan Hacker News, Reddit, and small blogs looking for stories. Starting at Level 1 puts the story where top reporters are already looking. This is how stories naturally filter up — respecting the mechanic dramatically increases success.

### Step 3: Build Reporter Relationships

**ACTION:** Before pitching, identify and engage reporters who cover your category. Twitter is the easiest channel — many reporters have surprisingly few followers and engage with thoughtful replies.

Tactics:
- Follow reporters who cover your space
- Reply to their tweets with genuine context (not pitches)
- Respond to HARO (Help A Reporter Out) queries — this creates mentions and warm introductions
- Bookmark reporters' email addresses before you need them

**WHY:** Cold pitches to strangers have 1-2% response rates. Pitches from people a reporter recognizes from prior Twitter interactions have dramatically higher response rates. The relationship doesn't need to be deep — recognition alone is often enough. HARO is a fast path to a first mention, which then becomes social proof for the next outreach.

**IF** there's no time to build relationships organically → HARO is the fastest substitute. Answer 3-5 relevant queries weekly.

### Step 4: Draft Pitches Using Proven Templates

**ACTION:** Use one of the two templates from [references/pitch-templates.md](references/pitch-templates.md):

1. **Direct pitch:** Subject line with exclusive hook, short paragraphs (hook + product + demo link + exclusive offer), direct contact info at bottom.
2. **Ryan Holiday template:** Subject "Quick question", reference their prior work, tease the exclusive, give specific results ("25,000 paying customers in 2 months"), ask for their process.

Critical criteria for any pitch:
- Short — reporters scan, don't read
- Emotional hook — not "we built a product"
- Concrete specifics — numbers, names, dates
- One clear angle — not 3 competing ones
- Exclusive offer when possible (first access, embargo, data)

Run the **6 PR mistakes check** — see [references/pr-mistakes.md](references/pr-mistakes.md).

**WHY:** Pitch format matters more than most founders realize. The difference between a 50-word pitch and a 500-word pitch is a 10x response rate difference. Templates prevent founders from writing the "wall of text" mistake. The mistakes check prevents the most common failure modes (wall of text, bad timing, no emotional angle, PR firm via, unclear launch timing, bundling failures).

### Step 5: Plan the Amplification Sequence

**ACTION:** Coverage is step 1. Amplification is what turns coverage into traction. For each piece of coverage that lands:

1. **Submit to community sites:** Hacker News, Reddit, Product Hunt, Slashdot (category-appropriate), Digg
2. **Share on social:** Twitter, LinkedIn, Facebook, with founder personal accounts amplifying
3. **Pay to boost:** Run social ads pointing to the coverage page (often cheaper than ads pointing to landing pages)
4. **Email your list:** Point subscribers to the coverage
5. **Contact tier 2 reporters:** Share the coverage as evidence that the story has traction, invite follow-up

Write the amplification plan to `pr-amplification.md`.

**WHY:** A TechCrunch feature sends traffic for 24-48 hours. Amplification extends the half-life and creates the chain reaction that drives stories up to top-tier outlets. Founders who skip amplification get coverage but not the compounding effect coverage enables.

## Inputs

- Newsworthy milestone or bundled announcement
- Target audience
- Media chain for the category
- Reporter contact list (or plan to build one)

## Outputs

Four markdown files:

1. **`pr-angle.md`** — The story, bundled milestones, emotional hook
2. **`pr-media-chain.md`** — Target outlets by tier
3. **`pr-pitches.md`** — Draft pitches (direct + Ryan Holiday variants)
4. **`pr-amplification.md`** — Post-coverage amplification sequence

## Key Principles

- **Stories filter UP the media chain.** Don't start at the top. WHY: Top reporters get their ideas from small blogs. Starting at the top means cold-pitching someone who doesn't know you. Starting small means your story shows up where top reporters are already looking.

- **Bundle, don't drip.** One big announcement beats five small ones. WHY: Reporters want material. A bundled announcement gives them enough for a real article. Drip announcements get ignored individually.

- **Emotional angle trumps feature list.** Reporters need readers to share the story. Shares come from emotion, not features. WHY: "Satisfaction is a non-viral emotion." Stories worth sharing produce surprise, outrage, delight, or curiosity.

- **Founders pitch better than PR firms at early stage.** Most reporters ignore PR firm pitches. Founder pitches are more personal and show the founder cares. WHY: PR firms cost money and produce lower response rates for early-stage companies. Save the money, do it yourself, and learn the skill.

- **Amplification is mandatory.** Coverage without amplification is wasted potential. WHY: A single piece of coverage produces 24-48 hours of attention. Amplification extends it by weeks and creates the chain reaction to top-tier outlets.

- **Twitter is the reporter relationship channel.** Many reporters have accessible Twitter follower counts. WHY: LinkedIn and email are crowded. Twitter engagement is casual enough that reporters actually read replies. A month of thoughtful replies beats 50 cold emails.

## Examples

**Scenario: B2B SaaS product launch**

Trigger: "We're launching our analytics tool in 4 weeks. Want TechCrunch coverage. What should we do?"

Process: (1) Bundle milestones: launch + seed funding + 3 pilot customers = one big story. (2) Media chain: Product Hunt launch, Hacker News post, targeted tier-1 analytics blogs → tier-2 TechCrunch/VentureBeat → tier-3 coverage unlikely for early-stage. (3) Relationships: 4 weeks isn't enough to build organic relationships, so HARO + Twitter engagement with 5 reporters who cover analytics. (4) Pitches: direct pitch template, emphasize exclusive access, specific pilot customer results. (5) Amplification: day-of Hacker News + Product Hunt submission, founder Twitter thread, paid social boost to coverage URL.

Output: Week-by-week PR plan with pitch drafts, specific reporters, and amplification checklist.

**Scenario: Previous PR attempts failed**

Trigger: "We sent 30 pitches to TechCrunch reporters last month and got zero responses. What's wrong?"

Process: (1) Diagnose: cold-pitching top outlets directly is the most common PR mistake. Show the media chain — stories filter up, not down. (2) Review the pitches — apply the 6 mistakes check. Usually at least 3 apply (wall of text, no emotional hook, no clear angle, unclear timing). (3) Re-strategy: start at small blogs and HARO. Build Twitter relationships with 3-5 TechCrunch reporters over 4-6 weeks BEFORE any pitch. (4) Rewrite pitches using the Ryan Holiday template. (5) Amplification plan for when coverage lands.

Output: Diagnosis of why previous approach failed, corrected approach, and new pitch drafts.

**Scenario: Unconventional PR stunt**

Trigger: "We want to do a publicity stunt like Dollar Shave Club's video or Half.com renaming a town. What makes these work?"

Process: (1) Analyze the pattern: unique + surprising + shareable + on-brand. (2) Generate stunt ideas tied to the company's actual product (not random). (3) Evaluate each against emotional angle test. (4) Pick one and plan execution: budget, timing, amplification plan. (5) Have a backup: stunts have binary outcomes (viral or ignored) — have a secondary launch angle ready.

Output: Stunt plan with clear success criteria and backup launch angle.

## References

- For the two proven pitch templates, see [references/pitch-templates.md](references/pitch-templates.md)
- For the 6 PR pitching mistakes, see [references/pr-mistakes.md](references/pr-mistakes.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Traction: A Startup Guide to Getting Customers by Gabriel Weinberg and Justin Mares.

## Related BookForge Skills

Install related skills from ClawhHub:

- `clawhub install bookforge-bullseye-channel-selection` — Select PR via Bullseye deliberately
- `clawhub install bookforge-startup-traction-strategy-by-phase` — PR is typically Phase II+
- `clawhub install bookforge-content-and-email-marketing` — Content-led coverage is a parallel path

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
