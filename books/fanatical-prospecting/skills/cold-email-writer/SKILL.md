---
name: cold-email-writer
description: |
  Write a complete cold prospecting email — subject line, body, and send-time recommendation — using Blount's AMMO planning framework and Hook-Relate-Bridge-Ask body structure from Fanatical Prospecting.

  Trigger this skill when you need to:
  - Write a cold email, prospecting email, or sales introduction email
  - Write an email to a prospect you have never contacted before
  - Improve an existing prospecting email that is not getting replies
  - Apply the AMMO framework (Audience / Method / Message / Outcome) to email planning
  - Build a Hook-Relate-Bridge-Ask email body that converts
  - Fix a subject line that is too long, uses a question mark, or is getting ignored
  - Check an email against the Three Cardinal Rules: Get Delivered / Get Opened / Get Converted
  - Improve email open rate, reply rate, or click-to-response conversion
  - Write a subject line under 50 characters with an action word, not a question
  - Understand what spam trigger words to avoid in a prospecting email
  - Run an email deliverability pre-check before sending
  - Write a post-trigger-event email to a prospect who just changed jobs, raised funding, or announced growth
  - Write a new-territory introduction email to a segment you have never contacted
  - Produce a complete send-ready email draft the user can send as-is or edit minimally
  - Apply the "AMMO email", "three cardinal rules email", or "Hook-Relate-Bridge-Ask" frameworks
  - Increase reply rate or reduce the number of cold emails going unanswered
  - Understand why "Hi [Name], I was browsing LinkedIn" emails get deleted immediately

  NOT for: building the core WIIFM bridge and because message nucleus that feeds this email
  (use prospecting-message-crafter first), or setting the email objective before writing
  (use prospecting-objective-setter). This skill produces a complete, send-ready email — not
  just the message component.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/cold-email-writer
metadata:
  openclaw:
    emoji: "📚"
    homepage: "https://github.com/bookforge-ai/bookforge-skills"
status: published
source-books:
  - id: fanatical-prospecting
    title: "Fanatical Prospecting"
    authors:
      - Jeb Blount
    chapters:
      - 19
tags:
  - sales
  - prospecting
  - cold-email
  - copywriting
  - sdr
  - bdr
  - email-marketing
depends-on:
  - prospecting-objective-setter
  - prospecting-message-crafter
execution:
  tier: 2
  mode: full
  inputs:
    - type: document
      description: "Target prospect context (role, company, industry, any known trigger events), user's value prop or ICP, desired objective (appointment / qualifying info / referral / direct sale), and optionally a current email draft to improve. Paste inline or point to a .md or .txt file."
  tools-required: [Read, Write]
  tools-optional: [WebFetch]
  mcps-required: []
  environment: "Document directory — reads user-provided context files; writes cold-email-draft-{prospect}.md to the working directory"
discovery:
  goal: "Produce a complete, send-ready prospecting email with subject line, annotated body using Hook-Relate-Bridge-Ask structure, and send-time recommendation — that passes all Three Cardinal Rules (Delivered / Opened / Converted)"
  tasks:
    - "Gather prospect context, value prop, objective, and any existing draft"
    - "Build or confirm the AMMO plan: Audience / Method / Message / Outcome"
    - "Run deliverability pre-check: no bulk, no images, no attachments, limited URLs, no spam triggers, scrub bounces"
    - "Craft subject line: 40-50 characters, action word, no question mark, prospect-centric"
    - "Draft body with Hook-Relate-Bridge-Ask structure"
    - "Run Three Cardinal Rules quality gate and anti-pattern check"
    - "Produce final annotated email plus send-time suggestion"
    - "Write output to cold-email-draft-{prospect}.md"
  audience:
    roles: [sdr, bdr, ae, founder-self-seller]
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "Writing the first prospecting email to a new prospect or segment"
      - "Cold email reply rate is below 3% and you want to diagnose and fix it"
      - "Someone asks 'write an email to a prospect' or 'can you draft a sales email'"
      - "A trigger event just occurred (funding, new hire, expansion) and you want to send a timely email"
      - "Entering a new territory and need an introduction email template for a segment"
      - "Current email has a long subject line, contains a question in the subject, or starts with 'Hi [Name], I was...'"
      - "User wants to apply AMMO, Hook-Relate-Bridge-Ask, or Three Cardinal Rules to a draft"
    prerequisites:
      - "Prospect role, company, and industry — minimum required"
      - "Your value proposition or the outcome you help deliver — required"
      - "Desired outcome of this email touch — required"
    not_for:
      - "Building the underlying WIIFM bridge and because message (use prospecting-message-crafter)"
      - "Defining which objective to target before emailing (use prospecting-objective-setter)"
      - "Handling objections or non-replies in an email sequence (use prospecting-rbo-turnaround)"
      - "Multi-touch email cadence design — this skill writes the first email; sequence design is a separate skill"
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
    what_skill_catches:
      - "Applies AMMO planning framework (Audience / Method / Message / Outcome) before writing"
      - "Produces subject line that is 40-50 characters with an action word, no question mark"
      - "Uses Hook-Relate-Bridge-Ask body structure throughout"
      - "Runs Three Cardinal Rules quality gate (Delivered / Opened / Converted) before finalizing"
      - "Removes self-centered framing ('Hi [Name], I was browsing LinkedIn', 'I'd love to')"
      - "Removes feature dumps and replaces with prospect-centric bridge and WIIFM answer"
      - "Includes a 'because' reason that answers WIIFM — not just a value prop statement"
      - "Writes an assumptive, specific ask with a proposed day/time"
      - "Uses disruption in the ask ('I don't know if we're a fit') to reduce resistance"
      - "Checks and removes spam trigger words from subject and body"
      - "Enforces one-to-one send discipline and no attachments / images / multiple links"
      - "Addresses prospect by name only — no 'Hi', 'Hello', or 'Dear' salutations"
    what_baseline_misses:
      - "Produces a subject line with 70+ characters or a question mark"
      - "Opens with 'Hi [Name], I wanted to reach out' or 'I was browsing LinkedIn'"
      - "Writes a feature dump or company cheerleader paragraph as the email body"
      - "Does not give a 'because' reason — just states capabilities"
      - "Puts the burden on the prospect to schedule: 'let me know what works for you'"
      - "Includes images, attachments, or multiple links that trigger spam filters"
      - "Does not check spam trigger words — includes 'free', 'guaranteed', or ALL CAPS"
      - "Does not apply AMMO planning — sends the same template regardless of audience or objective"
---

# Cold Email Writer

## When to Use

You need to send a cold prospecting email to a prospect — and you want it to actually get a reply.

The average business executive receives 200+ emails per day (Harvard Business Review). Your email will be scanned in under three seconds. It will be deleted unless the subject line is compelling, the opening sentence is about the prospect (not you), and the body answers one question: *What's in it for me?*

This skill writes the complete email — subject line through closing ask — using three interlocking frameworks from Blount's *Fanatical Prospecting*:

1. **AMMO plan** — audience, method, message, outcome — before writing a word
2. **Deliverability pre-check** — so the email reaches the inbox, not the spam folder
3. **Hook-Relate-Bridge-Ask body** — the four-element structure that converts

**This skill is downstream of two dependencies:**
- `prospecting-objective-setter` — defines what you are asking for (appointment / info / referral / close)
- `prospecting-message-crafter` — builds the bridge and WIIFM nucleus that feeds the email body

If you have not run those skills, this skill will gather the required context itself. The AMMO plan subsumes both.

## Context & Input Gathering

Before writing, gather (or ask the user for):

**Required:**
1. **Prospect context** — role, company, industry; any known trigger events (funding, expansion, new hire, press coverage, competitor churn)
2. **Your value prop** — the one outcome you deliver that is most relevant to this prospect's world
3. **Desired outcome** — what action do you want the prospect to take? (schedule a call / give qualifying info / agree to a meeting / download / reply)
4. **Familiarity level** — have you called, connected on LinkedIn, or met in person before sending this email? (affects open probability and subject line strategy)

**Helpful (read from working directory if available):**
- `icp.md` — ideal customer profile with decision-maker roles and pain points
- `value-prop.md` — your value proposition and strongest client outcomes
- `prospect-notes.md` — any research on this specific prospect
- `current-draft.md` — an existing email draft to diagnose and improve

**Defaults:** If no files are provided, the skill asks the user directly. Two to three sentences about the prospect and what you sell is enough to begin.

## Process

### Step 1 — Build the AMMO Plan

**WHY:** Most prospecting emails fail because the sender skipped planning. A good email begins with a clear plan, not a blank subject line. AMMO prevents generic outreach that wastes time and burns sender reputation.

Answer the four AMMO questions before writing:

**A — Audience**
- Who is this person? Role, title, seniority, industry
- How busy are they? An executive receiving 200+ emails/day needs a shorter, more compelling email than a mid-level manager
- What do you know about their style? Do they post publicly on LinkedIn? Do they respond to data or to emotional language?
- How familiar are they with you? (Zero familiarity = prioritize subject line and hook. Some familiarity = you have more latitude in the opening)
- What problems are they likely sitting with right now?

**M — Method**
- Is this a standalone cold email, or part of a multi-touch Strategic Prospecting Campaign (SPC)?
- What tone fits: direct and brief? Soft and value-led? Hard-hitting with data?
- Should this be personalized 1:1 (conquest or C-level) or mass-customized from a template (large similar-prospect pool)?

**M — Message**
- What is the bridge? The *because* that connects their world to what you offer
- What value category fits: emotional (anxiety/relief), insight/curiosity (competitive edge), or tangible/logic (specific ROI data)?
- What language does this prospect use? Speak their jargon — COOs talk about *growth, risk, complexity, regulatory surprises*; CISOs talk about *exposure, board accountability, click rates, audit findings*

**O — Outcome**
- What is the exact action you want them to take?
- Make the outcome specific: *schedule a 20-minute call on Thursday at 3 PM* — not *connect sometime*
- Desired outcomes for prospecting email: appointment / qualifying information / introduction to a decision maker / download or webinar registration / reply that opens a sales conversation

**Output of Step 1:** A four-line AMMO summary that shapes every word of the email.

---

### Step 2 — Deliverability Pre-Check

**WHY:** An email that reaches the spam folder converts at zero. Deliverability failures are silent — the prospect never sees the message and you never know why. Run this check before writing a single word of body copy.

Run through the deliverability checklist. Each item is binary pass/fail:

- [ ] **One-to-one only** — this email goes from your address to one individual. Never bulk-send a prospecting email from a personal address. This alone clears 90% of spam hurdles
- [ ] **No images** — spam filters treat embedded images as potential malware vectors. Avoid them entirely in prospecting emails
- [ ] **No attachments** — same reason. Hackers use attachments to install malware; spam filters know this
- [ ] **Minimal hyperlinks** — ideally zero. If you must include a link: use the full URL (no shortened URLs), avoid embedding it in hyperlink text, and include at most one link total including your signature
- [ ] **No spam trigger words** — see `references/spam-trigger-wordlist.md` for the full list. Key offenders: *free, amazing, guaranteed, 100% guaranteed, do it today, increase sales, cash, save $, act now, click here*, ALL CAPS, excessive exclamation points
- [ ] **Not sending to multiple people at the same company simultaneously** — if you are emailing several contacts at one company, stagger them throughout the day
- [ ] **Scrub bounced addresses** — if an address has bounced before, remove it from your list and update your CRM before sending. Repeated sends to dead addresses trigger blacklisting
- [ ] **Extra caution for sensitive industries** — financial institutions, defense contractors, healthcare: use plain text only with no links, no images, no attachments

**If any item fails, fix it before proceeding.**

---

### Step 3 — Craft the Subject Line

**WHY:** The subject line is the gatekeeper. More than 50% of emails are opened on mobile, where the subject line is often the only thing visible. Subject lines over 50 characters see exponentially lower open rates. The three most common subject line mistakes — too long, contains a question, generic/impersonal — all send the email to the delete pile before the prospect reads a word.

**Subject line rules:**
- **Length:** 3–6 words or 40–50 characters including spaces. Under 50 characters is the hard ceiling
- **No question marks** — questions in subject lines consistently underperform across major email studies. Use action words and directive statements instead
- **Action word or pattern** — strong subject line patterns that work:
  - List-based: *"3 Reasons ABC Corp Chose Us"*
  - Referral: *"[Mutual Contact] Said We Should Talk"*
  - Role + problem: *"COO — The Toughest Job in the Bank"*
  - Trigger event: *"Your Q3 Expansion — One Risk to Watch"*
  - Compliment: *"Loved Your Post on [Topic]"*
- **Prospect-centric** — the subject line is about their world, not your product. "Cloud Based Software" is about you. "COO — The Toughest Job in the Bank" is about them
- **No salutation words** — never open the email body with "Hi", "Hello", or "Dear". No one in business uses these except salespeople. Address the prospect by name only: "Lawrence,"

**After drafting the subject line:** Count the characters. If it is over 50, cut it. If it ends with a question mark, rewrite it as a statement. If it contains your company name or product name, reconsider — the subject is about the prospect, not the sender.

---

### Step 4 — Draft the Body Using Hook-Relate-Bridge-Ask

**WHY:** Each of the four elements serves a specific conversion function. Skipping or collapsing any element breaks the sequence. The Hook earns the read. The Relate earns the emotional connection. The Bridge earns the time. The Ask earns the action.

**Hook — the opening sentence and subject line working together**

The subject line gets the email opened. The first sentence must keep them reading. You have about three seconds.

Rules for the opening sentence:
- About the prospect, not you
- Use a credible third-party source if possible (industry report, research data, peer group insight)
- No "I was browsing LinkedIn and wanted to reach out" — this is about you, not them
- No "Hi [Name]," salutation
- Connect immediately to something they care about

Example: *"Ernst & Young recently reported that the COO has the toughest role in the C-suite."* — this hooks a COO because it validates their daily reality with a credible source.

**Relate — demonstrate that you understand their world**

Show empathy. Demonstrate that you have done enough research to understand their situation. You are not pitching yet — you are showing that you get them.

Rules:
- Step into their shoes before writing this section
- If you have never been in their role, use surrogate credibility: *"The [role]s I work with tell me that..."*
- Avoid feature dumps — this section is not about your product
- Use emotional language: *harder, more stressful, more complex, overwhelming, at risk*

Example: *"The COOs I work with tell me that the increasing complexity of the banking environment has made their job harder and more stressful than ever."*

**Bridge — answer WIIFM (What's In It For Me)**

This is the most important sentence in the email. It answers the prospect's most pressing question: if I give you my time, what do I get?

Rules:
- Connect their specific problem (from the Relate section) to the specific outcome you deliver
- Use their language — speak the jargon of their role and industry
- Include a value proof point when possible: a client name, an outcome number, a relevant industry result
- Do not brag about your company, your awards, or your growth — "so what?" test: if the prospect's internal response is "so what?", rewrite

Bridge structure: *[I help] [people like you] [achieve specific outcome] [by/with specific approach]*

Example: *"My team and I help COOs like you reduce complexity and stress with strategies to optimize growth and profit, mitigate credit risk, allocate resources effectively, and minimize regulatory surprises."*

**Ask — direct, specific, low-resistance**

Every prospecting email must end with a direct ask. Make it easy for the prospect to say yes. Make it hard for them to avoid responding.

Rules:
- Propose a specific day and time: *"How about next Thursday at 3:00 PM?"* — not *"let me know when you're available"*
- Use assumptive framing: "How about..." assumes the meeting will happen. It is not asking if the meeting can happen
- Use disruption to lower resistance: *"While I don't know if we're a good fit for your situation..."* — this unexpected admission of uncertainty disarms the prospect's defenses and pulls them toward you instead of pushing them away
- Keep it short — the ask is one or two sentences, not a paragraph
- Do not add a second ask or a list of options. One ask only

Example: *"While I don't know if we are a good fit for your bank, why don't we schedule a short call to help me learn more about your unique challenges? How about next Thursday at 3:00 PM?"*

---

### Step 5 — Quality Gate: Three Cardinal Rules + Anti-Pattern Check

**WHY:** Before writing the final email, run the completed draft through a structured quality gate. Most prospecting emails fail one of these three rules. Catching the failure before sending saves your sender reputation and the prospect's patience.

**Rule 1: Will it get delivered?**
Re-run the deliverability checklist from Step 2 against the drafted email. Confirm no images, no attachments, no bulk send, no spam trigger words have crept into the body or subject.

**Rule 2: Will it get opened?**
- Subject line is 40–50 characters or fewer ✓/✗
- No question mark in subject line ✓/✗
- Subject line is about the prospect, not the sender ✓/✗
- No "Hi", "Hello", or "Dear" salutation ✓/✗

**Rule 3: Will it convert?**
Check the body against the five worst email patterns (immediate disqualifiers):
- [ ] Long, important-sounding pitch using incomprehensible jargon — no meaning, all words
- [ ] Feature dump — list of product capabilities with no prospect relevance
- [ ] Company cheerleader — "we are the #1 provider / we've been voted most innovative / we have 3 years on the INC 5000"
- [ ] Wrong name or missing name (Lawrence vs. Jim)
- [ ] Eye-glazing length — if the email requires scrolling on mobile, it is too long

**Hook-Relate-Bridge-Ask completeness check:**
- Does the opening sentence hook the prospect? Is it about them, not you? ✓/✗
- Does the Relate section show genuine empathy for their situation? ✓/✗
- Does the Bridge answer their WIIFM question? ✓/✗
- Does the Ask propose a specific day/time with assumptive framing? ✓/✗

**Fix any failures before moving to Step 6.**

---

### Step 6 — Produce Final Email + Send-Time Recommendation

**WHY:** The formatted, annotated final email is the artifact the user sends. Annotations explain the "why" behind each element so the user can adapt the structure to future emails. The send-time recommendation increases the probability the email is read when it arrives.

**Output format:**

Write the final email with each section labeled (for the user's reference, to be stripped before sending):

```
Subject: [40-50 chars, action word, no question mark]

[Prospect last name],

[HOOK — opening sentence using credible source or prospect-relevant trigger, about them not you]

[RELATE — 1-2 sentences showing you understand their specific problem, using their language]

[BRIDGE — 1-2 sentences connecting their problem to the outcome you deliver; answers WIIFM; uses their industry jargon]

[ASK — 1-2 sentences with disruption framing + specific proposed day/time]

[Your name]
[Title]
[Company]
```

**Send-time guidance:**
- **B2B prospects:** first thing in the morning to mid-morning — prospects are fresh and handling email
- **B2C prospects:** adjust to when your prospect is most likely to take immediate action on your request
- **Schedule ahead:** write emails outside Golden Hours (prime selling time) and schedule them to send during peak reading windows, so your selling hours stay on the phone and in meetings

**Write the output to `cold-email-draft-{prospect-name}.md`** in the working directory. Include:
- The send-ready email with labels stripped
- An annotated version showing each Hook / Relate / Bridge / Ask element with a one-line explanation
- The AMMO plan summary
- The deliverability check result
- The Three Cardinal Rules gate result

---

## Inputs

| Input | Required | Source |
|---|---|---|
| Prospect role, company, industry | Yes | User provides or prospect-notes.md |
| Your value prop / outcome delivered | Yes | User provides or value-prop.md |
| Desired outcome of this email | Yes | User provides or prospecting-objective-setter output |
| Known trigger events at this account | No — strengthens the Hook | User provides or WebFetch research |
| Current draft email to improve | No — skill builds from scratch | User pastes inline or file path |
| Familiarity level with this prospect | No — affects subject line strategy | User states |

## Outputs

| Output | Location | Description |
|---|---|---|
| `cold-email-draft-{prospect}.md` | Working directory | Send-ready email + annotated version + AMMO plan + deliverability and quality gate results |
| Inline diagnosis | Conversation | If a draft was provided: labeled list of what failed and why, before the rewrite |

---

## Key Principles

**1. The Three Cardinal Rules are a funnel, not a checklist.** An email that does not get delivered converts at zero. An email that gets delivered but not opened converts at zero. Only an email that clears all three rules has a chance to convert. Apply them in sequence — deliverability first, open rate second, conversion third.

**2. AMMO before writing.** The fastest path to a bad prospecting email is opening a blank message and typing. The fastest path to a good one is spending two minutes on AMMO: who is this person, what method fits, what message will connect, what outcome am I after. Planning takes two minutes. Rewriting a bad email that burned a prospect takes permanently.

**3. Subject lines over 50 characters get deleted.** Over 50% of emails are opened on mobile. A subject line cut off at character 40 on a mobile screen defeats itself. Three to six words is the target. Less is more — always.

**4. Never use a question mark in a subject line.** Every major email study confirms this. Questions doom emails to the delete pile. Use action words and directive statements. *"COO — The Toughest Job in the Bank"* outperforms *"Can we help reduce your complexity?"* on every metric.

**5. The email is about the prospect, not you.** The subject line is about them. The opening sentence is about them. The relate section is about their problems. The bridge connects their world to your solution. The ask makes it easy for them. Only the signature is about you. Read your draft and count the sentences that start with "I" or "We" — each one is a red flag.

**6. Disrupt expectations in the ask.** Blount's COO example uses a counterintuitive ask: *"While I don't know if we are a good fit for your bank..."* This disarms the prospect. They expect a pushy pitch. Getting the opposite — honesty about uncertainty — pulls them toward you instead of triggering resistance. Disruption plus a specific proposed time outperforms a confident pitch every time.

**7. One-to-one only — always.** Bulk-sending a prospecting email from your personal address is the fastest path to being blacklisted and looking like a beginner. One email. One recipient. One send. That discipline alone clears 90% of spam hurdles.

---

## Examples

---

### Example 1 — Bad-to-Good Rewrite (Based on Dave vs. Brandon, Fanatical Prospecting pp. 246–250)

**Situation:** Software sales rep sending a cold email to the CEO of a growing software consultancy.

**Original (Brandon's approach — fails all three rules):**

> Subject: Cloud Based Software
>
> Hi Jeb,
>
> I was browsing LinkedIn and wanted to reach out to you.
>
> We build custom software solutions; web, cloud, mobile, desktop. Whether you have need to modernize outdated software, build something new from scratch, or augment your team to meet a critical deadline, I'm confident we can help.
>
> We've been able to figure out how to maintain high quality and keep our rates competitive. It's a model that has led us to three straight years on the INC 5000.
>
> I'd love to schedule a time to connect and outline how we're able to do this while discussing any projects or plans you might have. Just let me know a time that works with your schedule for a free consultation & quote.

**What fails:**
- Subject line: "Cloud Based Software" — about the sender, not the recipient; contains a spam-adjacent term; says nothing about the prospect's world
- "Hi Jeb" — "Hi" is a sales turnoff; no one in business uses this except salespeople
- "I was browsing LinkedIn and wanted to reach out" — about the sender; "wanted" is past tense and self-focused; gives the prospect zero reason to keep reading
- Body: feature dump — *web, cloud, mobile, desktop* — answers nobody's question
- Relate attempt: company cheerleading about INC 5000 — "so what?" — why does the prospect care?
- Ask: "I'd love to..." — self-centered; "just let me know a time" puts the burden on the prospect; "free consultation" signals desperation
- No AMMO planning visible; same email could be sent to anyone

**Rewritten (applying AMMO + Hook-Relate-Bridge-Ask):**

> Subject: Custom Software Risk in a Scaling Firm
>
> Jeb,
>
> Gartner reports that 72% of custom software projects at growing firms run over budget or miss deadlines — most often because augmentation decisions are made under deadline pressure rather than strategic fit.
>
> The CEOs I work with at software consultancies tell me that managing build vs. augment decisions while keeping delivery quality consistent is one of the most stressful parts of scaling.
>
> My team works specifically with growing software firms to reduce delivery risk and keep margins intact as headcount scales — without the 3-month ramp time of traditional augmentation.
>
> While I don't know if we're dealing with the same issues at your firm, I'd like to spend 20 minutes finding out. How about Thursday at 2:00 PM?
>
> Brandon
> Senior Account Executive
> SoftCo

**Annotation:**
- Subject: 43 characters, action word ("Risk"), prospect-centric, no question mark
- Hook: third-party data, relevant to CEO's world, no "Hi"
- Relate: surrogate empathy ("The CEOs I work with tell me..."), emotional language ("most stressful"), speaks CEO language
- Bridge: answers WIIFM with specific outcome (delivery risk + margins + ramp time), uses their jargon
- Ask: disruption framing ("I don't know if..."), specific day/time, assumes the meeting happens

---

### Example 2 — New Territory Introduction Email (SDR / SaaS / VP of Operations Target)

**Situation:** SDR at a logistics software company entering the mid-market manufacturing vertical. No prior contact with any prospect in this segment.

**AMMO plan:**
- Audience: VP Operations, 200-500 person manufacturer, likely managing inventory and fulfillment
- Method: standalone cold email, Targeted bridge (large pool, inferred pain from industry trends)
- Message: operational complexity during inventory unpredictability is their primary stress point
- Outcome: 20-minute discovery call

**Email:**

> Subject: Inventory Visibility — 3 Patterns We See in Manufacturing
>
> [Prospect first name],
>
> A recent APICS report found that mid-size manufacturers lose an average of 11% of annual revenue to inventory errors — most of them invisible until they hit the production floor.
>
> Operations leaders I work with in manufacturing describe the same pain: they have data in three different systems and still can't tell in real-time where a delay is coming from.
>
> We help VP Operations teams at mid-market manufacturers get a single real-time view across procurement, warehousing, and fulfillment — which typically cuts emergency-order costs by 20–40% in the first quarter.
>
> I don't know if inventory visibility is a priority right now, but I've been working in this segment and have some benchmarks from your industry I thought might be worth a quick conversation. How about 20 minutes next Tuesday at 10 AM?
>
> [Name]
> [Title]
> [Company]

**Annotation:**
- Subject: 45 characters, "3 Patterns" creates curiosity, prospect-centric
- Hook: APICS data + manufacturing-specific (not generic software pitch)
- Relate: "Operations leaders I work with tell me..." — surrogate empathy + their language (three systems, real-time, production floor)
- Bridge: specific outcome (20–40% emergency-order cost reduction) + connects to their role jargon
- Ask: disruption framing, "benchmarks from your industry" adds curiosity value, specific Tuesday at 10 AM

---

### Example 3 — Post-Trigger-Event Email (AE / HR Tech / New CHRO at a Growth-Stage Company)

**Situation:** AE at an HR platform company. LinkedIn shows a new CHRO just joined a 300-person SaaS company that recently raised a Series B. The company is publicly hiring aggressively.

**AMMO plan:**
- Audience: newly appointed CHRO, starting fresh at high-growth company with mandate to build
- Method: strategic 1:1 email, personalized to trigger event
- Message: new CHROs in high-growth environments face hiring speed vs. quality tradeoff under board pressure
- Outcome: 30-minute discovery call

**Email:**

> Subject: New CHRO + Series B — One Decision That Compounds
>
> Lisa,
>
> Congratulations on joining Acme and on the Series B. A CHRO stepping in at this stage faces a specific challenge: you need to scale the team fast enough to satisfy the board while building the infrastructure that prevents a bad-hire crisis at 500 employees.
>
> New CHROs I work with at Series B companies tell me the first 90 days are critical — whatever hiring system is in place when headcount doubles tends to harden into permanent process, good or bad.
>
> We help CHROs at growth-stage companies build a scalable hiring system in the first 90 days — so that adding 100 people doesn't add 100 points of chaos.
>
> I know you're early and still finding your footing, but I've worked with several CHROs at this stage and have a framework I think would be useful to share. Would 30 minutes on Friday at 9 AM work?
>
> [Name]
> [Title]
> [Company]

**Annotation:**
- Subject: 42 characters, two trigger events (New CHRO + Series B) connected with an outcome word ("Compounds")
- Hook: congratulates without being sycophantic, immediately pivots to their challenge
- Relate: new-CHRO-specific empathy, 90-day language reflects her reality
- Bridge: "100 people doesn't add 100 points of chaos" — speaks her language, emotional + logical value
- Ask: "I know you're early" — disruption, respects her onboarding reality; specific Friday at 9 AM

*Note: this example bends the usual "no question mark" rule in the ask — the ask sentence uses "work?" which is acceptable when embedded in a two-sentence ask block with disruption framing. The subject line contains no question mark, which is the high-stakes rule. Applies judgment accordingly.*

---

## References

Detailed supporting materials are in the `references/` folder:

- `references/spam-trigger-wordlist.md` — full 200+ word/phrase list that triggers spam filters in subject lines and body copy (sourced from Comm100 research cited by Blount, p. 235)
- `references/deliverability-checklist.md` — expanded deliverability pre-check with per-industry notes (sensitive industries: financial, defense, healthcare)
- `references/subject-line-patterns.md` — library of subject line patterns with character counts, use cases, and tested examples: list-based, referral, role + problem, trigger event, compliment
- `references/email-examples-library.md` — complete annotated email examples by prospect role (COO, CFO, VP Sales, CISO, Operations Director, CHRO) and scenario type (new territory, post-trigger, re-engagement, referral introduction)
- `references/ammo-planning-worksheet.md` — AMMO planning worksheet with decision prompts for Audience, Method, Message, and Outcome; includes Targeted vs. Strategic bridge selection guide

**Source chapter:** Blount, Jeb. *Fanatical Prospecting*, Chapter 19 "E-Mail Prospecting" (pp. 232–252 / PDF pp. 232–252). Subject line data: pp. 238–241. AMMO framework: pp. 242–245. Hook-Relate-Bridge-Ask: pp. 245–252. Three Cardinal Rules: pp. 234–241. Dave vs. Brandon annotated contrast: pp. 246–250.

**Referenced external sources:**
- Harvard Business Review: average business executive receives 200+ emails per day (cited by Blount, p. 236)
- Gao, Kevin, CEO of Comm100: 200 spam trigger words/phrases (cited by Blount, p. 235)
- Lee, Kendra. *The Sales Magnet* — "glimpse factor" concept for opening sentences (cited by Blount, p. 247)

---

## License

Content derived from *Fanatical Prospecting* by Jeb Blount (Wiley, 2015). This skill is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt this material provided you give appropriate credit to Jeb Blount and BookForge, and distribute any derivative works under the same license.

---

## Related BookForge Skills

**Upstream dependencies — use these before or alongside this skill:**

The message nucleus (WIIFM bridge and because) that feeds this email:
```
clawhub install bookforge-prospecting-message-crafter
```

The objective that drives the Ask in this email:
```
clawhub install bookforge-prospecting-objective-setter
```

**Downstream or parallel skills:**

For handling non-replies, brush-offs, or "send me more info" responses:
```
clawhub install bookforge-prospecting-rbo-turnaround
```

For building the full 5-step telephone follow-up after this email is sent:
```
clawhub install bookforge-cold-call-opener-builder
```

Browse the full Fanatical Prospecting skill set: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
