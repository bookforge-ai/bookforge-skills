---
name: authority-signal-designer
description: |
  Design and audit authority signals in content, credentials, bios, and landing pages. Use this skill when building expert positioning, thought leadership content, professional bios, about pages, or any content where trust and credibility must be established quickly. Covers three authority symbol types — titles, clothes/uniforms, and trappings — with compliance data showing their real-world persuasion impact. Also covers the two-question defense framework for evaluating authority claims you encounter. Applies strategic self-deprecation to build credibility. Use when: writing a professional bio, building a consultant's about page, crafting thought leadership content, designing a speaker or expert landing page, positioning credentials in marketing copy, adding expert testimonials or social proof of expertise, auditing whether your content actually conveys authority, or when evaluating whether an authority claim you're reading is genuine. Relevant for: authority, credibility, expertise, thought leadership, credentials, trust signals, expert positioning, professional bio, about page, social proof of expertise, testimonials from experts, Milgram, obedience, compliance, persuasion.
model: sonnet
context: 200k
execution:
  tier: 1
  mode: hybrid
  inputs:
    - type: document
      description: "Marketing content, professional bios, landing pages, credentials list, or about pages to design or audit"
    - type: none
      description: "Skill also works from a verbal description of the expert or context"
  tools-required: [Read, Write, TodoWrite]
  tools-optional: [Grep]
  environment: "Run from any directory; document access enables concrete rewrites"
depends-on: []
---

# Authority Signal Designer

## When to Use

Use this skill when you are:
- **Writing or editing a professional bio or about page** — need to convey credentials and expertise in a way that activates trust, not just lists facts
- **Building a consultant, coach, or thought leader brand** — choosing which authority signals to emphasize across a website, social profiles, or marketing collateral
- **Creating expert-led marketing content** — articles, case studies, webinars, or campaigns where the author's or brand's expertise needs to be felt, not just stated
- **Auditing existing content for authority gaps** — reviewing a bio, landing page, or content set to identify where authority is being undersold or miscommunicated
- **Evaluating incoming authority claims** — receiving a pitch, reading a recommendation, or vetting an expert where you need to apply the two-question defense protocol

Preconditions: you have at least one of:
- A draft bio, landing page, about page, or content set to work from
- A description of the person, role, credentials, and audience
- An authority claim (from an expert, vendor, influencer, or advisor) you want to evaluate

**Agent:** Before starting, confirm whether you are in APPLICATION mode (designing authority signals for content) or DEFENSE mode (evaluating an authority claim someone is making). You can also do both in sequence if relevant.

## Context & Input Gathering

### Input Sufficiency Check

```
User prompt → Extract: whose authority? what content? what audience? which mode?
                    ↓
Environment → Scan for: bio drafts, landing page copy, credential lists, existing content
                    ↓
Gap analysis → Do I know: (1) whose authority is being designed, (2) what the content is for,
               (3) who the audience is, (4) application vs defense mode?
                    ↓
         Missing critical info? ──YES──→ ASK (one question at a time)
                    │
                    NO
                    ↓
              PROCEED
```

### Required Context (must have — ask if missing)

- **Whose authority, and in what domain:**
  → Check prompt for: name, title, role, field, credentials, years of experience
  → Check environment for: existing bios, LinkedIn content, website copy
  → If still missing, ask: "Who is this for, and what is their domain expertise? For example: 'a cybersecurity consultant with 12 years in enterprise security' or 'a marketing agency specializing in B2B SaaS.'"

- **Audience and context:**
  → Check prompt for: target reader, content format (landing page, bio, article), decision being made
  → If still missing, ask: "Who is the audience for this content, and what action should they take after encountering this person's authority? For example: 'enterprise buyers deciding whether to hire this consultant.'"

### Observable Context (gather from environment)

- **Existing content:** Read any draft bio, about page, or credential list present in the files.
  → Look for: how credentials are currently presented, what titles are used, what symbols of authority appear
  → If unavailable: work from user description

- **Competitor or peer positioning:** If other experts in the same field are named or linked, observe their authority signals for comparison.

### Default Assumptions

- If no audience specified: assume a skeptical professional evaluating this person for the first time, with no prior exposure
- If no content format specified: assume a professional bio or about page is the target output
- If no mode specified: assume APPLICATION mode (designing signals) with a brief defense check at the end

## Process

Use `TodoWrite` to track steps before beginning.

```
TodoWrite([
  { id: "1", content: "Analyze scenario: mode, audience, goal, existing signals", status: "pending" },
  { id: "2", content: "Audit existing authority signals across all three symbol types", status: "pending" },
  { id: "3", content: "Design authority strategy: titles, visual/contextual signals, trappings", status: "pending" },
  { id: "4", content: "Apply strategic self-deprecation where appropriate", status: "pending" },
  { id: "5", content: "Ethical check: are signals genuine or manufactured?", status: "pending" },
  { id: "6", content: "Defense mode: apply two-question protocol if evaluating a claim", status: "pending" }
])
```

---

### Step 1: Analyze the Scenario

**ACTION:** Determine mode (APPLICATION / DEFENSE / BOTH), identify the audience's knowledge state and trust threshold, and clarify the specific goal.

**WHY:** Authority signals work through automatic, nearly unconscious compliance — what Cialdini calls the "click, whirr" response. The audience rarely deliberates about whether to trust an authority; they react. Designing effective signals means understanding what will trigger that automatic response in THIS audience. A title that commands authority for physicians ("MD") carries no weight in venture capital. A luxury office that signals success to retail clients may signal excess to lean startup operators. The signal must match the audience's conditioned deference patterns.

**Key questions to resolve:**
- What does this audience automatically defer to? (academic titles, corporate rank, media credentials, peer recognition, track record data?)
- Is the goal initial credibility (getting read or engaged) or sustained trust (getting hired, followed, recommended)?
- Is this a single-channel deployment (one bio) or multi-channel (website, LinkedIn, speaking intro, byline)?

Mark Step 1 complete in TodoWrite.

---

### Step 2: Audit Existing Authority Signals

**ACTION:** Review all existing content through the lens of the three symbol types. Identify what is present, what is absent, and what is being communicated unintentionally.

**WHY:** Authority is communicated whether you plan it or not. An unpolished website, a vague title ("consultant"), or a sparse bio all communicate something — usually uncertainty or low status. The audit surfaces both gaps and noise. Noise is as harmful as gaps: listing irrelevant credentials (a food science degree for a marketing consultant) dilutes focus and signals a failure to curate.

**Symbol Type 1 — Titles:** What titles, designations, certifications, or role labels appear?
- Are titles specific or generic? ("Principal Consultant" vs "Consultant")
- Are academic or professional designations present where relevant?
- Is the title front-loaded (appears early, prominently) or buried?
- Audit for: titles that are undersold (real credential hidden behind modesty), titles that are overstated (vague claims), missing titles that would be recognized by this audience

**Symbol Type 2 — Visual and Contextual Authority Signals** (the clothes/uniform equivalent in digital content):
- In written content: does the language register match expert status? (precise terminology, confident assertion, absence of hedging)
- In visual content: professional photography, publication logos, event photography, stage/keynote images
- In digital presence: website design quality, publication outlets where work appears, association with known institutions
- Audit for: language that hedges authority away ("I think," "in my opinion," "maybe"), generic stock photography that signals inauthenticity, poor visual design undermining strong credentials

**Symbol Type 3 — Trappings:** Status markers that signal success and achievement.
- Client logos, press mentions, award badges, bestseller labels
- Social proof metrics (followers, subscribers, downloads) where significant
- Association with prestigious institutions, events, or publications
- Audit for: absent trappings that could be added, trappings that are outdated or no longer accurate, trappings that signal the wrong domain

**Output:** A structured gap and noise analysis table.

Mark Step 2 complete in TodoWrite.

---

### Step 3: Design the Authority Strategy

**ACTION:** Based on the audit, prescribe specific additions, removals, and repositioning across all three symbol types. Produce revised copy or specific recommendations for each channel.

**WHY:** The three symbol types work together as a system, not independently. A strong title with weak trappings reads as self-proclaimed. Strong trappings with a weak title reads as successful but undefined. The goal is convergence: all three types pointing to the same conclusion about expertise and trustworthiness. The Milgram research and its replications show that 65% of people will comply with a clearly-marked authority even in high-stakes situations — the symbols do real persuasive work, but only when they form a coherent signal.

**Titles strategy:**
- Lead with the most recognized, domain-relevant title — not the most impressive one to the person themselves
- For consultants and independents: specificity beats seniority ("Customer Acquisition Strategist for B2B SaaS" beats "Marketing Consultant")
- Include certifications, publications, or institutional affiliations that the target audience will recognize and respect
- Height-perception principle: the more specific and credentialed the title sounds, the more the audience fills in competence (the Cambridge study showed 2.5-inch height perception increase per status step — the same mechanism governs perceived expertise depth)

**Visual and contextual signals strategy:**
- Rewrite hedging language to authoritative assertion: "I believe companies should..." → "Companies that scale past $10M need..."
- Identify one or two institutional associations (past employers, academic institutions, known clients) that serve as shorthand credibility markers for this audience
- If original content (articles, talks, frameworks) exists, name and reference it — having a named methodology or published work activates the "expert has a system" authority heuristic
- For visual assets: professional context photography (speaking, consulting, in environment) beats portrait studio shots — context signals the expert in their domain

**Trappings strategy:**
- Select three to five highest-signal trappings for this audience — prioritize recognizability over impressiveness
- Format trappings as social proof near the primary authority claim: "Featured in [X]" or "Trusted by [Y] companies" placed close to the bio, not buried in a separate section
- Use specificity to strengthen trappings: "10,000 newsletter subscribers" > "large newsletter"; "Led growth from $2M to $18M ARR" > "drove significant growth"
- For new experts with thin trappings: community leadership, event roles (speaker, organizer, panelist), and peer recognition from respected names substitute effectively

**AGENT: EXECUTES** — produce revised bio copy or a marked-up version of the existing content with specific changes called out.

Mark Step 3 complete in TodoWrite.

---

### Step 4: Apply Strategic Self-Deprecation

**ACTION:** Identify one or two places where acknowledging a genuine limitation, counterargument, or constraint will increase overall credibility more than omitting it.

**WHY:** Compliance professionals use strategic self-deprecation to establish truthfulness on minor points so that their major claims receive less scrutiny. The mechanism is trust calibration: an expert who acknowledges limitations signals that their positive claims are honest, not sales-motivated. Cialdini documents this with Listerine ("the taste you hate three times a day"), Avis ("We're #2, but we try harder"), and L'Oreal ("a bit more expensive and worth it"). The waiter who says "the special isn't as good tonight as it usually is" and recommends a less expensive dish gets trusted when they later recommend expensive wine and desserts. The key rule: the limitation must be genuine, secondary, and easily overcome by the benefits being claimed.

**Where to apply:**
- In a bio or about page: acknowledge one constraint on scope ("I focus exclusively on [narrow domain], so if you need [adjacent area], I'm not your person")
- In a case study: briefly note where an approach has limits before explaining why it was right for this client
- In a pitch or proposal: acknowledge one alternative approach and why it was rejected — this signals the recommendation was considered, not reflexive

**What to avoid:** Self-deprecation on core competence claims, primary value propositions, or anything the audience might actually be deciding about. The minor concession must be clearly minor.

**AGENT: EXECUTES** — identify the best candidate location in the content and draft the self-deprecation language.

Mark Step 4 complete in TodoWrite.

---

### Step 5: Ethical Check

**ACTION:** Verify that all authority signals being designed represent genuine credentials, real experience, or actual achievements. Flag any that are manufactured, exaggerated, or misleading.

**WHY:** Authority symbols are the most easily faked of all influence mechanisms — Cialdini explicitly notes that con artists specifically exploit titles, uniforms, and trappings precisely because they're so powerful and so easy to counterfeit. The 95% nurse compliance rate in the Hofling hospital study happened in response to a phone caller claiming to be a doctor — nothing verified. Designing manufactured authority signals is not only unethical but creates compounding risk: audiences who discover the gap between signal and substance lose trust entirely and permanently. The goal is amplifying genuine authority, not fabricating it.

**Checklist:**
- [ ] Every title listed is a current or verifiable past credential
- [ ] Every trapping (award, press mention, client logo) is accurate and current
- [ ] Institutional affiliations are genuine and not misrepresented in scope
- [ ] No implied expertise in domains where the expert has thin actual credentials
- [ ] Self-deprecation in Step 4 is a real limitation, not theatrical modesty over an actual strength

**IF** any signal fails this check → remove it or reframe it accurately
**IF** the genuine credentials are thin → recommend building real authority assets (publish content, seek speaking opportunities, pursue relevant certifications) rather than manufacturing symbols

Mark Step 5 complete in TodoWrite.

---

### Step 6: Defense — Two-Question Protocol

**ACTION:** If in DEFENSE mode, apply the two-question framework to evaluate the authority claim being assessed. If in APPLICATION mode, run this as a brief self-check on the content just designed.

**WHY:** People grossly underestimate how much authority affects them. In Milgram's experiments, predictions about how many subjects would comply with the full shock sequence fell in the 1-2% range — the actual rate was 65%. In the luxury car study, students predicted they would honk at the prestige car faster than the economy car — the opposite was true. This systematic underestimation is the core vulnerability. The two questions force conscious deliberation into what would otherwise be automatic deference, making it far harder for symbols to substitute for substance.

**Question 1: "Is this authority truly an expert?"**
- What specific credentials are claimed, and are they verifiable?
- Is the expertise domain-matched to this specific claim? (A cardiologist claiming authority on nutrition policy is an authority mismatch — genuine credentials in the wrong domain)
- Is the title the substance or just the symbol? (The "M.D." in the Sanka commercial was an actor playing a doctor — the credential was the signal, not the reality)
- Decision: Confirmed expert in this domain / Credentials unverified / Credentials real but domain mismatch

**Question 2: "How truthful can we expect this authority to be here?"**
- What does this authority stand to gain if you comply with their recommendation?
- Is there a conflict of interest between their expertise and their recommendation?
- Are they arguing against their own apparent interest anywhere? (If yes — this is evidence of trustworthiness; if never — be more skeptical)
- Are they presenting the full picture, or only the evidence that supports compliance?
- Decision: High trustworthiness / Conflict of interest present / Truthfulness uncertain

**Output:** A clear verdict — "Follow this authority on this claim" / "Verify before acting" / "Authority signal is present but substance is unconfirmed" — with the specific reasoning.

**HANDOFF TO HUMAN** — the defense protocol produces an assessment; the human makes the final judgment call.

Mark Step 6 complete in TodoWrite.

---

## Inputs

- **Content to design or audit:** bio, about page, landing page, credentials list, marketing copy, pitch document
- **Expert description:** name, role, credentials, experience, domain, notable achievements
- **Audience context:** who reads this, what decision they're making, what authority markers they recognize
- **Mode:** APPLICATION (building signals), DEFENSE (evaluating a claim), or BOTH

## Outputs

- **Authority Signal Audit:** gap and noise table identifying missing, weak, or misdirected signals across all three symbol types
- **Revised content:** rewritten bio, about page copy, or annotated original with specific changes
- **Strategic self-deprecation:** one or two drafted language additions that increase credibility through honesty
- **Defense assessment** (if in DEFENSE mode): two-question verdict on the authority claim with reasoning

## Key Principles

- **Symbols work as powerfully as substance — but only on audiences who haven't checked** — the nurse compliance study (95%) and Milgram experiments (65%) demonstrate that authority symbols bypass deliberate evaluation. This is both the mechanism to use ethically and the vulnerability to guard against.

- **Convergence across all three symbol types beats any single strong signal** — a title without trappings reads as self-proclaimed. Trappings without a clear title reads as successful but undefined. Design all three to point at the same conclusion.

- **Specificity is authority** — vague titles and generic credential lists communicate low status. Specific, granular credentials signal that the expert has done enough real work to have earned precision. "Principal consultant" signals more than "consultant"; "10,400 newsletter subscribers in fintech operations" signals more than "large audience."

- **Audiences underestimate authority's effect on themselves** — Cialdini documents this consistently: people in Milgram-style studies, luxury car studies, and uniform experiments all predicted they would be less affected than they actually were. When designing or evaluating authority signals, assume the effect is larger than it appears from the inside.

- **Strategic self-deprecation earns permission to claim** — acknowledging one genuine limitation buys credibility for all the positive claims that follow. The limitation must be real, minor, and easily outweighed. Theatrical modesty over a real strength is dishonest and backfires when detected.

- **Authority in the wrong domain is worthless — or worse** — the first defense question explicitly targets domain match because this is the most common authority misfire. Real experts in adjacent fields carry a halo that misleads audiences. Design and evaluate authority signals with domain specificity as a primary filter.

## Examples

**Scenario: Cybersecurity consultant bio with thin authority signals**
Trigger: "I'm a freelance cybersecurity consultant. My bio just says 'I help companies stay secure.' Can you make it better?"
Process:
1. Mode: APPLICATION. Audience: enterprise IT buyers and CISOs.
2. Audit: No title specificity, no credentials mentioned, no trappings, no institutional associations, hedged language.
3. Design: Lead with specific title ("Penetration Testing Specialist — Enterprise Cloud Infrastructure"). Add CISSP or relevant certification. Identify two verifiable trappings (past employer names, notable client sectors). Rewrite language from hedged to authoritative assertion.
4. Self-deprecation: "My work focuses specifically on cloud-native environments; for legacy on-premise infrastructure audits, I typically partner with specialists who have deeper experience there."
5. Ethical check: Confirm all claims are real.
6. Defense: Not applicable.
Output: Revised bio with specific title, credentials front-loaded, two trappings added, self-deprecation for scope clarity. Estimated authority-signal improvement: from 1/3 symbol types represented to 3/3.

---

**Scenario: Marketing agency building a new website about page**
Trigger: "We're redoing our website. We're a 6-person B2B content marketing agency. What authority signals should go on our About page?"
Process:
1. Mode: APPLICATION. Audience: B2B marketing directors at mid-market companies evaluating agencies.
2. Audit (from description): No existing about page content provided; designing from scratch.
3. Design strategy: Titles — name the founders' specific backgrounds and past brand affiliations (not just "former marketers"). Visual signals — replace generic headshots with context photography showing client work or team in action. Trappings — identify three recognizable client logos to feature, one press mention or industry award, and a specific result metric ("73 clients, average 40% increase in qualified pipeline").
4. Self-deprecation: "We focus exclusively on long-form content and thought leadership — we don't do social media management or paid ads." This positions the agency as a specialist, not a generalist, which is a form of authority in itself.
5. Ethical check: Confirm all client logos approved and metrics accurate.
Output: About page copy with all three symbol types covered, specialist framing as authority signal, self-deprecation that doubles as positioning.

---

**Scenario: Evaluating a consultant's recommendation**
Trigger: "A consultant is recommending we switch our entire data stack to a specific vendor. He has impressive credentials. Should I trust this recommendation?"
Process:
1. Mode: DEFENSE.
2. Question 1 — Is this authority truly an expert? Credentials confirmed: 15 years in data engineering, published in relevant trade publications. Domain match: yes, data infrastructure is the specific domain. Verdict: genuine expert.
3. Question 2 — How truthful can we expect them to be here? Consultant is a certified implementation partner of the vendor they're recommending. This is a direct financial conflict of interest — implementation partner status pays a referral or implementation fee. They have not disclosed this relationship proactively. No evidence of arguing against their own interest anywhere in the recommendation.
4. Verdict: "Genuine expert, but significant undisclosed conflict of interest. Recommendation deserves scrutiny. Request vendor-agnostic analysis, ask directly about partner relationships, and obtain a second opinion from a consultant with no vendor ties before deciding."
Output: Verification recommendation with specific follow-up questions.

## References

- For detailed evidence tables and study citations for all three authority symbol types, see [authority-symbol-evidence.md](references/authority-symbol-evidence.md)
- For the two-question defense protocol with extended examples across domains, see [two-question-defense.md](references/two-question-defense.md)
- Source: *Influence: The Psychology of Persuasion*, Robert B. Cialdini, Chapter 6 "Authority: Directed Deference," pages 157–177

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — Influence Psychology Of Persuasion by Unknown.

## Related BookForge Skills

This skill is standalone. Browse more BookForge skills: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
