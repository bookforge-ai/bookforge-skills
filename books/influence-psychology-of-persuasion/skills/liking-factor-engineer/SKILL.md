---
name: liking-factor-engineer
description: >
  Analyze and engineer liking to increase rapport, persuasion, and compliance in marketing, sales, and communication contexts.
  Use this skill when the user wants to improve how much an audience likes them, their brand, or their message — including writing sales copy,
  designing onboarding flows, crafting brand voice, building personal brand, creating relationship-based sales strategy, writing endorsement copy,
  structuring ad creative, designing UX that builds trust, or preparing for any high-stakes pitch or persuasion scenario.
  Also use when the user suspects they are being manipulated by a compliance professional through manufactured rapport, flattery, or contrived similarity.
  Trigger keywords: liking, rapport, trust, relationship building, brand personality, personal brand, similarity, compliments, familiarity, association,
  endorsement, halo effect, attractive design, influence, persuasion, likability, warm, friendly, relatable, connection.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/influence-psychology-of-persuasion/skills/liking-factor-engineer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: influence-psychology-of-persuasion
    title: "Influence: The Psychology of Persuasion"
    authors: ["Robert B. Cialdini"]
    chapters: [5]
    pages: "126-156"
tags: [persuasion-psychology, liking, rapport, persuasion, marketing, sales, brand, halo-effect, similarity, association, endorsement, compliance, defense]
depends-on: []
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Brand voice guidelines, marketing content, sales pitches, or scenario description provided by the user"
  tools-required: [Read, Write]
  tools-optional: [Grep]
  mcps-required: []
  environment: "Any agent environment. Document inputs preferred but not required — user's verbal description is sufficient."
---

# Liking Factor Engineer

## When to Use

You are in one of two modes:

**APPLICATION mode** — The user wants to increase how much a target audience likes their brand, product, communication, or themselves as a salesperson or professional. This includes: brand messaging, sales copy, outreach emails, onboarding flows, endorsement strategy, ad creative, personal brand content, UX microcopy, pitches, and relationship-based selling.

**DEFENSE mode** — The user is evaluating a situation where they may be on the receiving end of manufactured liking — a sales conversation, a negotiation, or any context where a compliance professional is trying to get them to say yes.

Before starting, determine the mode by asking: "Are you trying to build liking (application) or protect against it (defense)?" Both modes can be run in the same session.

## Context and Input Gathering

### Required Context

- **Target audience or counterpart:** Who is this for? (Consumer segment, specific buyer, brand persona, the user themselves as a buyer)
  → Check prompt for: audience description, persona, customer type
  → If missing, ask: "Who is the person you need to like you / your brand / your message?"

- **What needs to be liked:** The brand, the product, the salesperson, the message, the content?
  → Check prompt for: existing copy, scenario description, content type

- **Mode (application vs defense):** Already described above.

### Observable Context

- **Existing brand voice or content:** If files are provided, read them to identify which liking factors are already present and which are absent.
  → Look for: warmth/personality signals (compliments), visual/aesthetic polish (physical attractiveness), shared values with audience (similarity), partnership language (association), repeated touchpoints (familiarity)
  → If unavailable: proceed from user's verbal description

### Default Assumptions

- If no audience described → assume a consumer-facing marketing context
- If no existing content provided → generate strategy recommendations the user can apply
- If mode is ambiguous → default to APPLICATION, flag DEFENSE considerations at the end

## Process

### Step 1: Analyze the Scenario and Content

**ACTION:** Read all provided content (brand docs, copy, pitch, messages). Identify: Who is the requester? Who is the target? What is the compliance goal (buy, sign up, agree, trust, refer)?

**WHY:** Liking is a compliance tool — the endgame is a "yes." Understanding the specific yes being sought determines which liking factors carry the most leverage. A Tupperware-style social purchase is different from a B2B sales close; a personal brand play is different from a product endorsement. The goal shapes the strategy.

### Step 2: Audit Against All Five Liking Factors

**ACTION:** Evaluate the current scenario or content against each of the five research-validated liking factors. Score each factor as: **Active** (clearly present), **Weak** (present but underdeveloped), or **Absent** (no presence).

The five factors (see [references/liking-factors-evidence.md](references/liking-factors-evidence.md) for full research data):

1. **Physical Attractiveness** — Does the brand/product/person project quality through visual and aesthetic signals? Does the design, presentation, photography, or formatting create a halo effect (good-looking = good product)?
   - The halo effect is automatic: attractive candidates get 2.5x more votes, attractive defendants are twice as likely to avoid jail, attractive job applicants are hired based on appearance even when interviewers deny it.
   - In brand contexts: design quality, imagery polish, spokesperson attractiveness, and even grooming/professionalism of sales representatives all trigger this factor.

2. **Similarity** — Does the communication reflect shared opinions, values, background, personality, or lifestyle with the target audience?
   - Compliance rates jump from under 50% to over 67% when a requester appears similarly dressed.
   - Car salespeople are trained to scan trade-ins for camping gear, golf balls, and out-of-state plates — then mirror those interests in conversation.
   - Even small, trivial similarities (same hometown, same name, same age) are effective.

3. **Compliments** — Does the communication express genuine appreciation for the audience? Does it make them feel seen, valued, or admired?
   - Joe Girard sent 13,000+ "I like you" cards per month to former customers — and became the world's greatest car salesman (Guinness World Records). His formula: a fair price + someone they liked.
   - Flattery works even when obviously insincere. North Carolina study: pure praise produced maximum liking even when the recipient knew the flatterer stood to benefit and even when the praise was objectively false.

4. **Familiarity and Contact** — Has the audience seen, heard, or experienced this brand/person/product repeatedly under positive conditions?
   - Mere exposure increases liking — but ONLY under non-competitive, cooperative conditions.
   - Critical distinction: contact under rivalry or frustration worsens liking (Robbers Cave experiment: competition between groups produced name-calling, raids, and fights). Contact under cooperation improves it (jigsaw classroom: cooperative tasks converted rivals into allies).
   - Application: repeated positive touchpoints (email sequences, retargeting, helpful content) build familiarity. Competitive framing ("we're better than X") destroys it.

5. **Association** — Is the brand/person/message linked to things the audience already likes, admires, or values?
   - Razran's luncheon technique (1930s): political statements presented during a meal became more liked — the positive feeling of food transferred to the ideas.
   - Association works for both positive and negative connections. Weathermen are disliked for bad weather they didn't cause. Brand spokespersons transfer their personal qualities to products.
   - Basking in reflected glory: people display connections to winners and hide connections to losers. After wins, fans say "we won"; after losses, "they lost."

### Step 3: Identify the Strongest Liking Factor Opportunities

**ACTION:** From the audit, identify which 1-3 factors are (a) currently weakest and (b) most relevant to the specific audience and goal. Prioritize interventions that will move the needle most.

**WHY:** Not all five factors are equally applicable in every context. Physical attractiveness matters enormously in consumer product ads but less in B2B whitepapers. Association dominates celebrity endorsement strategy but may be irrelevant for a solo freelancer. Similarity is the most reliable and universally applicable factor — it should almost always be a primary lever. Focusing improvement on the highest-leverage absent factors produces more ROI than polishing already-active ones.

**Prioritization heuristics:**
- Similarity is the most universally powerful factor — default priority if weak or absent
- Familiarity is a compounding factor — it grows over time; start early
- Compliments require authenticity to sustain — insincere praise works short-term but erodes trust long-term
- Physical attractiveness is most impactful at first impression (homepage, ad creative, LinkedIn profile)
- Association is most powerful for credibility transfer and social proof

### Step 4: Design the Application Strategy

**ACTION:** For each prioritized liking factor, generate specific, actionable interventions. Map each intervention to a concrete touchpoint in the user's context (email, landing page, social post, sales call, product UI, etc.).

**WHY:** Abstract advice ("be more relatable") produces no change. Specific interventions at specific touchpoints do. The goal is to give the user something they can act on immediately.

**Intervention templates by factor:**

**Similarity interventions:**
- Research audience demographics, values, and lifestyle markers → reflect them in language, imagery, and examples
- Use audience-native vocabulary (industry jargon, regional phrases, generational references)
- Reference shared challenges, frustrations, or aspirations before presenting solutions
- In sales: scan for and mirror background, interests, values early in conversation

**Compliment interventions:**
- Open copy or conversations by acknowledging something specific and genuine about the audience
- Use second-person affirmations ("You're the type of person who...") that reflect audience self-image
- Send appreciation touchpoints that do not ask for anything (Joe Girard's monthly card model)
- Validate the audience's existing choices before presenting alternatives

**Familiarity interventions:**
- Design a repeated positive touchpoint cadence: helpful content, check-ins, updates that carry no ask
- Ensure every touchpoint is cooperative in tone — position brand as ally, not competitor
- Retargeting should feel like a friendly reminder, not a pursuit
- Create rituals (weekly newsletters, consistent brand voice, recurring formats) that become familiar patterns

**Association interventions:**
- Identify what the audience already loves/trusts → find authentic connection points
- Use testimonials and social proof from people the audience looks up to
- Present the product alongside aspirational contexts (events, lifestyles, values)
- Partnerships, co-marketing, and celebrity or expert endorsement explicitly transfer liking
- Avoid association with anything the audience dislikes — even tangential connections stick

**Physical attractiveness / halo interventions:**
- Invest in design quality — visual polish triggers automatic "good = good" inference
- Use professional, high-quality photography for products, teams, and spokespersons
- Grooming and presentation guidelines for sales representatives and brand representatives
- In UX: clean interfaces, consistent design systems, and premium aesthetic signals all trigger halo effects

### Step 5: Check Ethical Boundaries

**ACTION:** Review the proposed strategy against the distinction between authentic rapport and manufactured compliance. Flag any intervention that crosses from genuine relationship-building into deception.

**WHY:** Liking factors work even when artificial — but manufactured rapport that the audience later perceives as fake backfires catastrophically. Authentic rapport compounds over time and generates referrals (Tupperware's model relied on genuine friendship networks — the liking had to be real for the hostess relationship to hold). Manufactured rapport creates fragile compliance that dissolves under scrutiny.

**The authentic vs manufactured line:**
- Authentic: Genuinely finding and reflecting real shared values → builds lasting relationship
- Manufactured: Inventing false similarities ("I'm from Ohio too!" when you're not) → deception
- Authentic: Sending appreciation that reflects genuine positive feeling → builds goodwill
- Manufactured: Automated "I like you" messages with no genuine basis → hollow, erodes trust over time
- Authentic: Associating brand with values the brand genuinely embodies → credibility
- Manufactured: Celebrity endorsement where celebrity has no real connection to product → can work short-term but audiences increasingly see through it

Flag and revise any intervention that relies on false claims, invented similarities, or associations the brand cannot authentically sustain.

### Step 6: Defense — Separation Protocol (run in DEFENSE mode or append to APPLICATION)

**ACTION:** When evaluating whether you (the user) are being influenced by manufactured liking, apply the single-criterion detection test and the separation protocol.

**WHY:** There are too many liking tactics to detect each one individually — many operate unconsciously (physical attractiveness, familiarity, association all work below awareness). Trying to spot the specific tactic being used is a losing game. The elegant defense focuses on the effect, not the cause.

**The detection test (ask yourself exactly this):**
> "Have I come to like this person more than I would have expected given only the time I've spent with them and the circumstances?"

If the answer is yes — regardless of why — that feeling is the signal. You don't need to know whether it was the compliments, the similarity claims, the food they served, or their attractive appearance. The anomalous liking itself is the trigger.

**The separation protocol (three steps):**
1. **Notice the feeling.** Acknowledge that you like this person more than the circumstances warrant.
2. **Mentally separate the person from the deal.** Ask: "Would I buy this car / accept this offer / agree to this request if a stranger offered it to me?" Evaluate the offer on its independent merits — price, terms, quality, fit for your needs.
3. **Do not actively dislike the person.** The goal is not to reverse the liking — that would be unfair and counterproductive. The goal is to bracket the liking and make the decision based on the deal alone.

**Reference case:** Car salesman "Dealin' Dan" — in 25 minutes he fed you coffee and doughnuts, complimented your color choices, mirrored your interests, and cooperated with you against the sales manager. The question is not "did he use liking tactics?" — the question is "if a stranger offered this car at this price, would I take it?" That's the only question that matters.

## Inputs

- Brand voice guidelines, marketing copy, sales pitch scripts, or outreach messages (preferred but optional)
- User's verbal description of the scenario, audience, and goal
- In defense mode: description of the interaction the user is evaluating

## Outputs

### Liking Factor Audit Report

```
# Liking Factor Audit: {Brand/Scenario Name}

## Goal
{What compliance outcome is being sought — buy, sign up, agree, trust, refer?}

## Audience
{Who is the target? What do they value?}

## Factor Coverage

| Factor                    | Status  | Evidence from content | Priority |
|---------------------------|---------|----------------------|----------|
| Physical Attractiveness   | Active / Weak / Absent | {observation} | High / Med / Low |
| Similarity                | Active / Weak / Absent | {observation} | High / Med / Low |
| Compliments               | Active / Weak / Absent | {observation} | High / Med / Low |
| Familiarity / Contact     | Active / Weak / Absent | {observation} | High / Med / Low |
| Association               | Active / Weak / Absent | {observation} | High / Med / Low |

## Top 3 Intervention Opportunities
1. **{Factor}** — {specific intervention} → {touchpoint}
2. **{Factor}** — {specific intervention} → {touchpoint}
3. **{Factor}** — {specific intervention} → {touchpoint}

## Ethical Review
{Any interventions flagged as crossing authentic/manufactured line, with revision}

## Defense Check (if applicable)
{Detection test result + separation protocol application}
```

## Key Principles

- **Liking operates on all five factors simultaneously** — compliance professionals use multiple factors at once (Tupperware parties deploy all six of Cialdini's principles, with liking as the centerpiece). Audit all five even if only one is the primary lever, because gaps in coverage leave liking on the table.

- **Similarity is the universal lever** — across all contexts, similarity is the most reliably applicable liking factor. When in doubt about where to start, mirror the audience's values, language, and lifestyle first.

- **Contact requires cooperation to build liking** — repeated exposure under competitive or frustrating conditions worsens liking, not improves it. This is the most commonly misapplied insight: simply exposing someone to your brand more often does not build liking unless every touchpoint is positive and cooperative in tone.

- **Detect the effect, not the cause** — in defense contexts, do not try to catalog which specific tactic was used. Ask only: "Do I like this person more than I should given the circumstances?" That single question bypasses the entire problem of unconscious influence.

- **Separate the person from the deal** — liking the salesperson is irrelevant to whether the deal is good. The separation protocol makes this distinction explicit and allows you to preserve the relationship while making a clear-headed decision.

- **Authentic rapport compounds; manufactured rapport collapses** — liking built on genuine similarity, real compliments, and true associations sustains itself and generates referrals. Liking built on artifice works once and leaves a bad taste. Design for the long game.

## Examples

**Scenario: SaaS onboarding email sequence lacks warmth**
Trigger: "Our trial-to-paid conversion is low. Users say the product is great but they don't feel connected to us."
Process: Audited email sequence — Physical Attractiveness (Active: good design), Similarity (Absent: generic copy doesn't reflect user persona), Compliments (Absent: no appreciation for user's choice to try), Familiarity (Weak: irregular cadence), Association (Weak: no social proof from similar companies). Top interventions: (1) Similarity — rewrite onboarding emails in the language of the target persona (startup founders), reflect their specific frustrations; (2) Compliments — add Day 1 email that genuinely appreciates them for joining and recognizes the courage of starting a company; (3) Familiarity — establish a consistent weekly cadence of helpful tips that carry no ask.
Output: Rewritten 5-email sequence with persona-specific language, appreciation touchpoint, and weekly value cadence. Ethical review: all similarities based on real persona research, not invented.

**Scenario: Sales rep preparing for a high-stakes enterprise pitch**
Trigger: "I have 45 minutes with the VP of Operations at a company I really want to close. What should I do?"
Process: Similarity — research the prospect's LinkedIn, company About page, and recent press; identify shared professional values or background to reference authentically. Compliments — open by acknowledging something specific and genuine about their organization's approach. Familiarity — confirm whether prior touchpoints have been positive; if not, warm up with a useful insight before the pitch. Association — identify which of their respected peers or competitors already use the product; lead with that reference. Physical Attractiveness — ensure professional presentation aligns with their company culture.
Output: Pre-call research checklist, opening conversational moves for each factor, and a reminder to evaluate the prospect's response to similarity/compliment moves as an indicator of receptivity.

**Scenario: User evaluating a car purchase after a charming sales conversation**
Trigger: "I spent 2 hours with this salesman and I genuinely love the guy. He's offering me a deal. Should I take it?"
Process: Defense mode. Detection test: "In 2 hours, did you come to like him more than the time and circumstances would normally produce?" Answer: yes — he fed them snacks, complimented their taste, mentioned he's also from their home state, and worked with them against the manager. Separation protocol: bracket the liking. Ask: "If this exact car at this exact price were being offered online by a stranger, would you take it?" Evaluate price against market comps, terms against industry standards, and car specs against stated needs — entirely independently.
Output: Defense evaluation report. Car decision based on deal merits, not salesman liking. Explicitly note: the user can still like Dan and even refer him later — the goal is not to dislike, but to decide on the deal alone.

## References

- For research evidence behind all five factors with full statistics and study citations, see [references/liking-factors-evidence.md](references/liking-factors-evidence.md)
- For commercial model case studies (Joe Girard, Tupperware, Shaklee, MCI Calling Circle), see [references/commercial-models.md](references/commercial-models.md)
- For the Good Cop/Bad Cop mechanics as a multi-principle compliance model, see [references/good-cop-bad-cop.md](references/good-cop-bad-cop.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Influence: The Psychology of Persuasion by Robert B. Cialdini.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
