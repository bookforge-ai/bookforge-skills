---
name: credibility-evidence-selector
description: "Pick the strongest credibility evidence for a claim and kill weak evidence chains with the Sinatra Test. Use this skill whenever the user asks 'how do I prove this?', 'how do I make this more credible?', 'which statistic should I cite?', 'do I need a source for this?', 'how do I build trust?', 'this claim sounds unbelievable', 'they won't believe us', 'we need a case study', 'should I quote an expert?', 'is this testimonial strong enough?', 'which proof point should I lead with?', 'my pitch needs more evidence', 'the numbers aren't landing', 'how do I back this up without a credentials wall?', 'who should say this for maximum credibility?', or 'is one example enough or do I need data?'. Also invoke when the user has a marketing claim, sales pitch, fundraising ask, research finding, policy argument, product benefit, or security/reliability promise and must choose between authority quotes, customer stories, statistics, vivid details, testable demos, or a single hero example. This skill ranks evidence across six named credibility categories (external authority, antiauthority, testable credentials, vivid details, Sinatra Test hero example, statistics-as-illustration) and applies the Sinatra Test as a pass/fail filter to cut weak chains. Run BEFORE shipping any claim that a skeptical audience might doubt."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/made-to-stick/skills/credibility-evidence-selector
metadata: {"openclaw":{"emoji":"🔬","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: draft
source-books:
  - id: made-to-stick
    title: "Made to Stick: Why Some Ideas Survive and Others Die"
    authors: ["Chip Heath", "Dan Heath"]
    chapters: [9, 13]
tags: [credibility, evidence, persuasion, marketing, sales, messaging, sinatra-test, proof, bookforge]
depends-on: []
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: "The claim the user needs to support (one sentence)."
    - type: document
      description: "Evidence inventory — the proof points, stories, stats, testimonials, and demos the user has available."
    - type: document
      description: "Audience profile — who will judge the claim and what they are skeptical about."
  tools-required: [Read, Write]
  tools-optional: [Edit]
  mcps-required: []
  environment: "Operates on prose artifacts — claims, pitches, marketing copy, fundraising asks, research summaries. No codebase or tooling required."
discovery:
  goal: "Select the strongest credibility evidence for a claim and apply the Sinatra Test to kill weak evidence chains."
  tasks:
    - "Rank available evidence across six credibility categories"
    - "Run the Sinatra Test on a candidate hero example as a pass/fail gate"
    - "Decide whether to lead with an authority quote, a testable demo, a single hero case, or vivid details"
    - "Diagnose a claim that feels unconvincing and prescribe the missing credibility type"
    - "Convert an abstract statistic into a human-scale illustration"
  audience:
    roles: [marketer, founder, sales-professional, communicator, fundraiser, researcher, policy-writer]
    experience: any
  when_to_use:
    triggers:
      - "User has a claim that a skeptical audience might reject"
      - "User is choosing between stats, quotes, stories, and demos as proof"
      - "User is drafting a credibility paragraph and has too many options"
      - "A case study feels weak and the user is not sure why"
    prerequisites: []
    not_for:
      - "Fabricating evidence — this skill selects from what already exists"
      - "Running A/B copy experiments — use a testing skill"
      - "Extracting the core message itself — use core-message-extractor first"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores: {}
    tested_at: null
    eval_count: 0
    assertion_count: 0
    iterations_needed: 0
---

# Credibility Evidence Selector

## When to Use

You have a claim a skeptical audience might reject, and a bag of possible proof points (stats, quotes, stories, demos, details). You need to decide which evidence to lead with — and which to cut. This skill ranks evidence across six named credibility sources and applies the Sinatra Test as a pass/fail filter to kill weak chains before they reach the audience.

Run this skill when the user is about to ship a claim without thinking hard about *why* the audience would believe it. Run it BEFORE writing the final copy, not after — the choice of evidence type reshapes the whole paragraph.

**Preconditions to verify before starting:**
- You know the specific claim. If missing, ask: "What is the exact one-sentence claim you need the audience to believe?"
- You have an evidence inventory (even a rough list). If missing, ask: "What proof points do you have — stats, stories, customers, experts, demos, details?"
- You know the audience's default skepticism. If missing, ask: "Who is judging this, and what is the one thing they'd say to dismiss it?"

**Do NOT use this skill for:**
- Fabricating evidence. This skill ranks what exists; it never invents sources.
- Designing experiments or user studies.
- Extracting the core message (use `core-message-extractor` first — credibility is applied to a core, not in place of one).

## Context & Input Gathering

### Required Context (must have — ask if missing)
- **The claim:** the exact sentence the audience must believe.
  -> Check prompt for: a quoted claim, a pitch paragraph, a headline, a research finding.
  -> Check environment for: `claim.md`, `draft.md`, `pitch.md`, `core-message.md`.
  -> If still missing, ask: "What is the one-sentence claim — the thing the audience must believe?"
- **Evidence inventory:** the candidate proof points available.
  -> Check prompt for: lists of customers, stats, quotes, case studies, demos, testimonials.
  -> Check environment for: `evidence.md`, `proof-points.md`, `case-studies/`, `testimonials.md`, `customer-stories/`, a `data/` dir.
  -> If still missing, ask: "What evidence do you already have? Dump a rough list — customers, numbers, experts, stories, demos, details — I will rank them."
- **Audience skepticism profile:** who judges the claim, and their default objection.
  -> Check prompt for: role, domain, familiarity, prior objections.
  -> If missing, ask: "Who will read this, and what would they say to dismiss the claim?"

### Observable Context (gather from environment)
- **Prior credibility drafts:** existing "why trust us" copy, testimonial pages, case study PDFs.
  -> Look for: `about.md`, `trust.md`, `social-proof.md`, `testimonials.md`, `case-studies/`.
  -> If present: mine for candidate evidence; treat as raw material, not final answer.
- **Brand voice constraints:** legal review rules, claims guidelines.
  -> Look for: `brand-guide.md`, `legal/claims.md`.
  -> If present: note which evidence types are disallowed (e.g., "no unverified customer quotes").

### Default Assumptions
- Medium: short-form text (one paragraph, one slide, one email). State this assumption if used.
- Audience default: mildly skeptical professional, not a hostile expert. Upgrade to hostile if the user says so.
- Evidence claims are truthful — the skill trusts the user's inventory and does not fact-check.

### Sufficiency Threshold
- SUFFICIENT: claim + evidence inventory + audience known.
- PROCEED WITH DEFAULTS: claim + evidence known, audience inferable from context (state the inference).
- MUST ASK: claim is not a single sentence, OR evidence inventory is completely empty (cannot rank nothing).

## Process

### Step 1: Lock the Claim to a Single Sentence
**ACTION:** Write the claim as one sentence with a clear subject, verb, and measurable predicate. Reject hedges ("might," "could help," "in some cases"). Save it under a `## Claim` heading in `credibility-plan.md`.

**WHY:** Credibility attaches to a specific assertion, not a vibe. If the claim is "we help teams ship faster," no evidence can be strong or weak — the claim is too fuzzy to judge. Locking the sentence forces the later steps to pick evidence that actually answers the specific assertion. Fuzzy claims are where weak evidence hides; tightening the claim is half the work of ranking the proof.

**IF** the claim is still multi-part ("we are fast, cheap, and reliable") -> split into one file per claim and run this skill once per claim.
**ELSE** -> proceed.

### Step 2: Inventory Evidence Into the Six Categories
**ACTION:** Take every proof point the user has and sort it into one of six credibility categories. Some evidence fits multiple — list it under the strongest fit only. Write the result as a `## Evidence Inventory` section with six sub-headings.

**The Six Credibility Sources (from Chapter 4 CREDIBLE):**

1. **External Authority** — a recognized expert, institution, or celebrity endorsement. Example: a Nobel laureate, an industry analyst, a peer-reviewed study. *Strength:* borrows the audience's existing trust. *Weakness:* cheap to fake and audiences are now skeptical of expert voices; "analyst-quoted" pitches blur together.
2. **Antiauthority (Credible Victim / Lived Experience)** — an ordinary person who lived the consequences. Not an expert; their biography IS the proof. Example: Pam Laffin — age 29, mother of two, started smoking at 10, emphysema at 24, failed lung transplant — used for anti-smoking messaging because no statistic lands like a face that earned the cost. *Strength:* inverts expert fatigue. *Weakness:* emotionally heavy; must be ethical and consensual.
3. **Testable Credentials ("Try It Yourself")** — the audience can verify the claim in real time, with their own senses, before committing. Example: Wendy's "Where's the beef?" (you can see the tiny patty). Snickers "satisfies" (you can feel it). Barry Marshall drinking a beaker of *H. pylori* bacteria, inducing gastritis, then curing himself — a self-experiment as a public, falsifiable demonstration that ulcers are bacterial. *Strength:* collapses the skeptic's objection into a single observable act. *Weakness:* only works when real-time verification is possible.
4. **Vivid, Convincing Details** — specific sensory or biographical detail that an inventor could not have bothered to fake. Example: the juror study where jurors believed a mother who testified her child had a "Goofy toothbrush" he loved to brush with — the trivial detail signaled an observer telling the truth, not a litigant pitching a case. *Strength:* non-obvious signal that the speaker has been close to the thing. *Weakness:* easy to confuse with purple prose; the detail must be load-bearing, not decorative.
5. **Sinatra Test (One Overwhelming Hero Example)** — a single reference so dominant that the audience cannot doubt you afterward. Named after "If you can make it there, you'll make it anywhere." Example: Safexpress, an Indian logistics firm, won enterprise contracts by saying "we delivered the final Harry Potter book to 6,000 Indian bookstores in one day, sealed, no leaks" — one sentence that obliterates the due-diligence conversation. Fort Knox security contractor = you're in the running for every security contract. *Strength:* replaces a wall of credentials with one unforgettable story. *Weakness:* only works when the hero case is genuinely the hardest case in the domain.
6. **Statistics-as-Illustration (Human Scale)** — a number converted into a concrete, sensory comparison so the audience can feel the magnitude. Example: explaining US/Soviet nuclear arsenals not as "thousands of warheads" but as "if a BB represents the Hiroshima bomb, the world's nuclear stockpile is a garbage can full of BBs — and one BB can level a city." Stats as raw numbers are forgettable; stats as illustration are sticky. *Strength:* anchors an abstract scale to a physical image. *Weakness:* only works if the illustration is honest — if the analogy flatters the number, the audience will catch you.

**WHY:** Sorting forces you to see that you usually do not have six types of evidence — you have two or three, and one slot is empty. The empty slots are signals: if you have zero testable credentials, ask whether you can manufacture one (a free trial, a public benchmark, a demo). The inventory is also the cut list; evidence that does not fit any category is usually rationalization, not proof.

**Anti-pattern to flag:** *credentials wall.* If the entire inventory lands under "External Authority," the user is leaning on a stack of expert quotes. Audiences skim credentials walls and remember nothing. Go find one testable credential or one Sinatra hero and lead with that instead.

### Step 3: Rank by the Default Preference Order
**ACTION:** Apply the default preference order from strongest to weakest and rank the candidates. Write the result as a `## Ranked Evidence` section.

**Default preference order** (Chapter 4 CREDIBLE):
1. **Testable Credentials** — the audience verifies with their own senses.
2. **Sinatra Test Hero Example** — one overwhelming case.
3. **Vivid Convincing Details** — truthful trivia that signals firsthand knowledge.
4. **Antiauthority (Credible Victim)** — lived experience beats expertise for behavior change.
5. **Statistics-as-Illustration** — numbers rescued by human-scale analogy.
6. **External Authority** — expert quote as last resort, not first move.

**WHY:** The ordering is not arbitrary — it tracks how audiences actually process claims. Testable credentials short-circuit skepticism ("I just saw it"); Sinatra heroes override it ("if they did THAT, I believe the rest"); vivid details bypass it ("no one would bother to invent that"); antiauthorities reframe it ("a doctor would lie; this mother wouldn't"); illustrated stats make it tangible; and authorities — cheapest to fake, most diluted by overuse — come last. Inverting this order is the most common credibility mistake: leading with a quote from a Gartner report when you have a customer who would pass the Sinatra Test.

**Override rules** (apply when defaults don't fit):
- **IF** the audience is a domain of credentialed peers (scientists reviewing research, doctors reading a trial) -> External Authority moves up to #1 or #2, because the audience's own credential norms require it.
- **IF** the claim is a behavior-change ask aimed at the people who resist expert messaging (teens on smoking, developers on technical debt, users on security hygiene) -> Antiauthority moves to #1.
- **IF** the claim is about scale / magnitude / cost / risk that audiences cannot feel intuitively -> Statistics-as-Illustration moves up (nuclear-warheads-as-BBs was the only way to make that scale real).

### Step 4: Run the Sinatra Test as a Pass/Fail Gate
**ACTION:** Take the strongest candidate from Step 3 (especially if it's a case study, customer example, or hero story) and run the Sinatra Test as a binary pass/fail. Write the result as a `## Sinatra Test` section with verdict, reasoning, and — if failed — a replacement plan.

**The Sinatra Test, stated formally:**
> An example passes the Sinatra Test when ONE example alone is enough to establish credibility in a given domain — because the example represents the *hardest case* the domain can throw at you.

**The three questions:**
1. **Is this the hardest case?** If the audience heard only this one example and nothing else, would they concede the full category? (Fort Knox security = yes, any security contract follows. Harry Potter delivery for 6,000 bookstores in one day, sealed = yes, any logistics contract follows.)
2. **Is the hard part legible?** Can the audience *see* why it was hard without a paragraph of explanation? Sinatra examples are self-evidently difficult — "Fort Knox" and "Harry Potter launch day" need no setup. If you must explain why the case was hard, it is not Sinatra material.
3. **Is it verifiable?** Can the audience check the claim if they wanted to? A Sinatra hero that cannot survive a two-minute Google search is worse than no Sinatra at all — it becomes a credibility *liability* on discovery.

**WHY:** The Sinatra Test exists because one dominant example is cheaper and stickier than a capabilities deck, but a *weak* hero example is worse than a deck — the audience senses the cherry-picking and punishes you. The three questions are the diagnostic: hardest case, legibly hard, checkable. Any failure means replace, don't patch. The Marshall ulcer story passes because drinking a beaker of bacteria is unambiguous; a vendor's "we helped a Fortune 500 save 15%" fails because it is neither the hardest case nor self-evidently hard.

**IF** the candidate passes all three questions -> mark PASS, make it the lead evidence.
**ELSE IF** it fails one question -> mark FAIL, cut it from the lead, and either find a stronger example or fall back to the next category in the ranking (vivid details or testable credentials).
**ELSE IF** no candidate passes -> do NOT fabricate one. Accept that the claim has no Sinatra-grade proof and move to multi-source credibility (testable demo + vivid detail + illustrated stat).

**Anti-pattern to flag:** *Sinatra inflation.* The user wants their best customer to pass the Sinatra Test and is willing to argue for it. If you have to argue, it fails — the test is whether the audience recognizes the hardness instantly. Three extra sentences of framing is a flunk.

### Step 5: Check for the "Sound Bite / Credentials Wall" Failure Modes
**ACTION:** Review the ranked evidence against two named failure modes from the book and note any hits in a `## Diagnostic Notes` section.

**Failure mode A — The Credentials Wall.** Symptom: the evidence is a list of logos, titles, and expert quotes with no single piece of proof an audience can remember. Consequence: audience forgets everything and defaults to their prior belief. Fix: replace the wall with one Sinatra hero or one testable credential. If you cannot, your claim is stronger than your evidence — shrink the claim.

**Failure mode B — The Raw Statistic.** Symptom: a scary or impressive number without a human-scale translation ("we prevent 3.2M attacks per day"). Consequence: the number washes past the audience. Fix: apply the nuclear-warheads-as-BBs move — convert to a sensory comparison. "3.2M attacks per day = 37 attacks every second — one every time you blink."

**WHY:** Credibility is a negative-space problem. The right evidence makes the claim stick, but the *wrong* evidence actively weakens it — a credentials wall signals insecurity, and a raw statistic signals that the speaker never tested their own number on a human. Running these checks after ranking catches cases where the strongest evidence in the inventory still triggers a failure mode, and the fix is not ranking-higher but *rewriting* the evidence into a stronger form.

### Step 6: Write the Output Artifact
**ACTION:** Assemble the final `credibility-plan.md` with these sections, in order:

```
# Credibility Plan

## Claim
<one-sentence claim>

## Audience Skepticism
- Who: <role / segment>
- Default objection: <the one thing they'd say to dismiss this>

## Evidence Inventory (Six Sources)
### External Authority
- <evidence> — <one-line note>
### Antiauthority (Credible Victim)
- ...
### Testable Credentials
- ...
### Vivid Convincing Details
- ...
### Sinatra Test Hero Example
- ...
### Statistics-as-Illustration
- ...

## Ranked Evidence
1. <category> — <evidence> — <why it leads>
2. ...

## Sinatra Test
- Candidate: <the hero example tested>
- Hardest case? <yes/no + reasoning>
- Hard part legible? <yes/no + reasoning>
- Verifiable? <yes/no + reasoning>
- VERDICT: PASS | FAIL
- IF FAIL: <replacement plan>

## Diagnostic Notes
- Credentials wall? <yes/no + fix>
- Raw statistic? <yes/no + illustration>

## Recommendation
Lead with: <the one piece of evidence to put first>
Support with: <1-2 backup pieces>
Cut: <evidence that weakens the claim and should be removed>

## Assumptions
- <any inferred audience/claim/evidence assumption the user should confirm>
```

**WHY:** The artifact separates *ranking* (what I have) from *recommendation* (what to lead with) from *cut list* (what to remove). Users resist cuts; seeing them attached to specific failure modes ("this is a credentials-wall entry") makes the cut negotiable point-by-point rather than an all-or-nothing argument. The Sinatra Test section is kept verbatim (three questions, verdict, replacement) because it is the single most defensible step — a downstream reviewer who disagrees with the lead evidence has to disagree with a named, checkable test.

## Inputs

- The one-sentence claim that needs credibility.
- The evidence inventory (rough dump is fine — customers, stats, experts, stories, demos, details).
- The audience skepticism profile (who judges; their default objection).
- Optional: medium constraints (character limit, slide vs paragraph vs email), legal/brand guidelines on allowed evidence.

## Outputs

- `credibility-plan.md` — the artifact defined in Step 6, containing:
  - The locked claim.
  - Evidence sorted into the six categories.
  - Ranked evidence with an explicit lead.
  - A Sinatra Test block with pass/fail and reasoning.
  - Diagnostic notes on credentials-wall and raw-statistic failure modes.
  - A cut list of evidence that should be removed.
  - An assumptions block for anything inferred.

## Key Principles

- **One overwhelming example beats a wall of credentials.** — The Sinatra Test exists because audiences remember one hero case and forget ten expert quotes. When you have a genuine hardest-case reference, lead with it and cut the quote stack; when you don't, do not manufacture one — fall back to testable credentials or vivid details.
- **Testable credentials collapse skepticism into a single observable act.** — "Where's the beef?" works because the audience verifies with their own eyes. Barry Marshall drinking *H. pylori* works because the demonstration is public and falsifiable. When you can give the audience a way to check the claim themselves, nothing else in the evidence stack matters nearly as much.
- **Antiauthority beats authority for behavior change.** — The people most resistant to expert messaging — teens on smoking, developers on technical debt, users on security — are often best reached by someone who lived the consequences, not someone who studied them. Pam Laffin's biography outperformed any Surgeon General report because her body was the proof.
- **Raw statistics are forgettable; illustrated statistics are sticky.** — A number alone ("3.2M attacks per day") washes past. The same number translated to human scale ("37 every second — one every time you blink") lands. The nuclear-warheads-as-BBs move is not decoration; it is how abstract magnitude becomes emotionally real.
- **Vivid details signal firsthand observation.** — The juror who believed a mother because she mentioned a "Goofy toothbrush" did not decide on the toothbrush — she decided on the fact that no liar would bother inventing that detail. Load-bearing trivia is a credibility signal; decorative trivia is just prose.
- **Evidence ordering is a trust hierarchy, not a taste preference.** — The default preference order (testable > Sinatra > details > antiauthority > illustrated stats > authority) tracks how skepticism actually resolves. Inverting it — leading with a credentials wall — is the most common and most damaging credibility mistake in this book.
- **When the evidence fails, shrink the claim.** — If no evidence category produces a defensible lead, the claim is stronger than the proof supports. The fix is not to pad with weaker evidence; it is to tighten the claim until the available evidence is genuinely sufficient.

## Examples

**Scenario: B2B security startup with a credentials wall**
Trigger: Founder says "our homepage lists 14 analyst quotes and 40 customer logos but nobody books a demo. How do I make the security claim more credible?"
Process: (1) Lock claim: "Our system blocks every known credential-stuffing attack pattern." (2) Inventory — 14 entries under External Authority, 2 under Vivid Details (an incident-response write-up mentioning a specific attacker TTP), 1 under Sinatra (they run security for a top-3 global bank's consumer login). (3) Rank: the bank reference is Sinatra-grade; testable credentials missing; authority dominates inventory (credentials wall). (4) Sinatra Test on the bank reference — Hardest case? Yes (top-3 global bank, consumer login = highest-volume attack surface). Legibly hard? Yes (audience instantly recognizes). Verifiable? Partial — the bank will not be named publicly. VERDICT: PASS with anonymization ("a top-3 global bank, consumer login, 400M accounts, zero successful credential-stuffing incidents in 18 months"). (5) Diagnostic flags credentials-wall (14 analyst quotes). Fix: cut to 3. (6) Recommendation: lead with the anonymized bank Sinatra hero; back with two incident-response details; cut 11 of 14 analyst quotes.
Output: `credibility-plan.md` with the bank Sinatra as lead, the quote wall shrunk, and a note that the founder should push for a testable credential (open benchmark or public red-team) to upgrade the credibility stack further.

**Scenario: Nonprofit fundraising email, abstract statistics**
Trigger: Fundraiser has a draft saying "3.2 million children are affected by food insecurity each year" and asks "why isn't this landing?"
Process: (1) Lock claim: "Child food insecurity is a scale emergency in our region this year." (2) Inventory — 1 raw statistic (the 3.2M number), 1 External Authority (a public-health study), 0 Testable, 0 Sinatra, 0 Antiauthority, 0 Vivid Details. (3) Rank: only two entries, both weak; the statistic is a Raw Statistic failure mode and needs illustration. (4) Sinatra Test: no hero candidate exists. Do NOT fabricate. Instead: convert the statistic. "3.2M children = every elementary-school seat in the five largest school districts in the country, empty at breakfast." (5) Diagnostic: Raw Statistic HIT. Fix: the BB-translation above. Also: add one Antiauthority — a single named family from the region, their story, their specific morning (vivid-details pairing). (6) Recommendation: lead with the illustrated statistic AND the one-family Antiauthority story side-by-side (Mother Teresa effect — identifiable victim paired with illustrated scale). Cut the authority-study citation to a footnote.
Output: `credibility-plan.md` recommending a two-piece lead (illustrated stat + identifiable family) with a note that the fundraiser should recruit an antiauthority spokesperson BEFORE next campaign.

**Scenario: Academic publishing a counterintuitive research finding**
Trigger: Researcher has a finding that contradicts 20 years of prior consensus. Asks "how do I make this credible to reviewers who will dismiss it on sight?"
Process: (1) Lock claim: "Finding X contradicts prior consensus Y because of mechanism Z." (2) Inventory — External Authority is dominant (peer-reviewed replication); Testable Credentials possible (open data + reproducible pipeline); one Antiauthority candidate (a respected prior defender of Y who reversed position); no Sinatra hero. (3) Rank: override default — audience is credentialed peers, so External Authority upgrades to #1. But lead with the Testable Credentials (open data) because a reviewer who can reproduce the result in an hour is more convinced than one reading a methods section. Antiauthority (the reversed defender) comes next — a Barry-Marshall-pattern Sinatra hero by analogy: someone who publicly reversed position is the "hardest case" this audience responds to. (4) Sinatra Test on the reversed defender: Hardest case? Yes (they were a public critic). Legibly hard? Yes (the reversal is documented). Verifiable? Yes. VERDICT: PASS. (5) Diagnostic: no credentials wall, no raw-stat failure. (6) Recommendation: lead with the open-data link (testable), follow with the reversed-defender statement (Sinatra-pattern antiauthority), support with the peer-reviewed replication. Cut nothing.
Output: `credibility-plan.md` with a testable-credential lead, a named Sinatra-pattern antiauthority, and a note that the open dataset should be ready BEFORE submission — the credibility plan depends on it.

## References

- For long-form worked examples of each of the six credibility sources, see [credibility-sources-catalog.md](references/credibility-sources-catalog.md)
- For the Sinatra Test worksheet and replacement decision tree, see [sinatra-test-worksheet.md](references/sinatra-test-worksheet.md)

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — *Made to Stick: Why Some Ideas Survive and Others Die* by Chip Heath and Dan Heath.

## Related BookForge Skills

This skill is standalone (a Level 0 foundation skill in the Made to Stick skill set). It pairs well with `core-message-extractor` (run first to lock the claim) and with downstream Concrete, Emotional, and Story skills (which apply stickiness techniques once credibility is established).

Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
