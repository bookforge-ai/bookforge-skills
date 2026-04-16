---
name: social-selling-touch-planner
description: |
  Plan and execute a multi-touch social selling strategy that builds familiarity across LinkedIn, Twitter, and other social channels — layered on top of phone and email to increase open rates, response rates, and appointment conversion.

  Trigger this skill when you need to:
  - Build a social selling plan using the Law of Familiarity and the Five Levers framework
  - Design a LinkedIn prospecting cadence for a target account list
  - Create a multi-touch familiarity plan for cold, warm, or conquest prospects
  - Generate connection request templates and social touch messages that don't pitch
  - Warm up prospects before phone or email outreach to increase engagement
  - Understand how to use social touches as a layer alongside phone/email (not a replacement)
  - Set up a daily social selling time block that fits inside the prospecting schedule
  - Build a personal branding content calendar for social channels
  - Understand the Five Levers of Familiarity: Persistent Prospecting, Referrals, Networking, Brand, Personal Branding
  - Design a referral engine that systematically asks for introductions
  - Create a social cadence for 20-50 cold prospect touches, or 1-10 for warm prospects
  - Apply the Five Cs of social selling: Connecting, Content Creation, Content Curation, Conversion, Consistency
  - Identify which social channels to prioritize based on where prospects hang out
  - Build a Strategic Prospecting Campaign (SPC) for conquest accounts using social + outbound

  NOT for: writing a cold call script (use cold-call-opener-builder), building a multi-touch email cadence
  (use cold-email-writer), or diagnosing pipeline math (use prospecting-ratio-manager). This skill produces
  the social layer plan and templates; the actual message nucleus is built in prospecting-message-crafter.
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/fanatical-prospecting/skills/social-selling-touch-planner
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
      - 12
      - 13
tags:
  - sales
  - prospecting
  - social-selling
  - linkedin
  - multi-touch
  - sdr
  - bdr
depends-on:
  - prospecting-message-crafter
  - prospect-list-tiering
execution:
  tier: 2
  mode: hybrid
  inputs:
    - type: document
      description: "Target account list (CSV, markdown table, or pasted text) plus the user's active social channels (LinkedIn, Twitter, etc.) and optional notes on current brand/content activity and existing familiarity level per account"
  tools-required:
    - Read
    - Write
  tools-optional:
    - WebFetch
  mcps-required: []
  environment: "Document directory containing the prospect list and any account notes. Agent reads input files, builds the Five-Lever allocation table, weekly social cadence, and connection/message templates, then writes outputs to the working directory."
discovery:
  standard
---

# Social Selling Touch Planner

## When to Use

You have a list of target accounts and you want to make your phone calls and emails land better. The problem is that cold prospects with zero familiarity with you or your company require 20 to 50 touches before they will engage — and most of those touches, delivered by phone alone, will hit voicemail and silence.

Social selling does not replace phone or email. Contact and conversion rates from phone and email dwarf conversion rates from social channels alone. What social selling does is reduce the number of touches needed to cross the **Familiarity Threshold** — the point at which a prospect recognizes your name, trusts you enough to take your call, open your email, and eventually agree to a meeting.

Use this skill when:
- You want to build a systematic familiarity-building plan before calling a cold list
- You are managing 20-100 strategic accounts that need consistent multi-channel touches
- You want LinkedIn outreach cadences that do not pitch on the first message
- You are running a Strategic Prospecting Campaign (SPC) on conquest accounts
- You need templates for connection requests, content engagement, and social inbox messages
- You want to build a referral engine into your existing accounts and professional network

**This skill does not:**
- Write your cold call script (use `cold-call-opener-builder`)
- Build a multi-touch email sequence (use `cold-email-writer`)
- Build your prospecting message nucleus (use `prospecting-message-crafter`)
- Tier your accounts or build your call priority order (use `prospect-list-tiering`)

Build the message nucleus in `prospecting-message-crafter` first. Then use this skill to deploy it as a social layer on top of your phone and email cadence.

---

## Context and Input Gathering

### Required (must have — ask if missing)

- **Target account list:** The accounts and contacts to plan social touches for. Accepted formats: CSV file, markdown table, or pasted text. At minimum: company name and contact name.
  - Check the working directory for: `prospect-list.csv`, `accounts.csv`, `tiered-prospect-list.md`, or any account list file.
  - If not found, ask: "Can you share your target account list? Even a simple list of names, companies, and their LinkedIn profile URLs will work."

- **Social channels in use:** Which platforms are you active on or willing to use? LinkedIn is the default for B2B. Twitter, Instagram, and Facebook may apply depending on the audience.
  - Ask if not stated: "Which social channels do you currently use or plan to use for prospecting?"

### Recommended (improves plan quality)

- **Current familiarity level per account:** Are these cold contacts (zero prior interaction), warm contacts (met at an event, replied to an email), or existing customers and referral sources?
- **Account tiers from `prospect-list-tiering`:** If the user has already tiered their list, import tier assignments directly. Conquest accounts (Tier 4) get the most intensive social plan. Lower tiers get a lighter automated cadence.
- **Existing content or brand activity:** Does the company or the rep have content being published? What is the current posting frequency?
- **Value proposition and ICP:** Used to design a content curation strategy that resonates with the right audience.

### Default Assumptions

- If no tier data is available, treat all accounts as cold (Tier 1-2) and design for the 20-50 touch benchmark.
- If only LinkedIn is mentioned, default to a LinkedIn-primary plan with a note that Twitter/other channels can be added.
- If no content activity exists, default to curation-first (sharing others' content) with a placeholder for original content over time.

---

## Process

### Step 1 — Audit Current Familiarity by Account

Before assigning social touches, establish a baseline: how familiar are these prospects with the rep or brand already? The number of touches required drops sharply as familiarity increases.

**Familiarity tiers (from the Law of Familiarity):**

| Familiarity State | Touch Estimate to Engage | Typical Source |
|---|---|---|
| Zero familiarity | 20–50 touches | Cold list, data vendor, no prior contact |
| Low familiarity | 10–20 touches | Met once, saw a post, same group |
| Moderate familiarity | 5–10 touches | Spoke by phone, replied to email, referral |
| High familiarity | 1–5 touches | Existing customer, warm referral, regular engager |

**Why audit first:** Applying a 20-touch social cadence to a prospect who already knows the rep is wasteful and annoying. Applying a 3-touch cadence to a cold stranger is statistically insufficient. Calibrating to current familiarity level sets the right cadence length and intensity from the start. (Blount, Ch. 12, pp. 96-97)

**For each prospect, record:**
- Familiarity state (zero / low / moderate / high)
- Evidence (e.g., "met at trade show," "opened 3 emails," "cold — no prior contact")
- Which of the Five Levers has already been applied (see Step 2)

If a tiered prospect list from `prospect-list-tiering` is available, map the pyramid tiers to familiarity states: Tier 1-2 = zero/low, Tier 3-4 = low/moderate, Tier 5-6 = moderate/high.

---

### Step 2 — Assign the Five Levers of Familiarity by Account Segment

The Five Levers are the mechanisms through which familiarity is built over time. Each lever operates differently and requires a different investment. Not every lever applies to every account — assign based on account tier and available resources.

**The Five Levers:**

| Lever | What It Is | Best For | Investment |
|---|---|---|---|
| **Persistent Prospecting** | Consistent daily multi-channel touches: calls, emails, voicemails, social interactions | All accounts — the baseline lever | Low time per touch, high volume |
| **Referrals** | Customer referrals, personal referrals, professional referrals from your network | Conquest accounts, hard-to-reach decision-makers | Medium — requires discipline to ask |
| **Networking** | Face-to-face events, chambers, trade shows, associations — the "real social prospecting" | Local territory or vertical-specific accounts | Medium-high — requires presence |
| **Brand** | Company marketing machine: advertising, content, events, trade shows | Large company reps benefit; small company reps must actively contribute | Low to rep (leverage marketing); high if building brand yourself |
| **Personal Branding** | Building your own reputation as a subject matter expert through content, public speaking, social media | Long-term play — all segments benefit; especially powerful for conquest and enterprise | Medium-high — ongoing commitment |

**Lever assignment logic:**

- **Conquest accounts (Tier 4):** Deploy all five levers. Request referrals from existing customers at the account. Attend events where their stakeholders appear. Engage them on social across multiple channels. Build personal brand content that addresses their specific problems.
- **Cold accounts (Tier 1-2):** Start with Persistent Prospecting + Personal Branding (social content and engagement). Add Referrals if a connection path exists.
- **Warm/inbound accounts (Tier 5-6):** Persistent Prospecting + social connection anchoring. Referrals if applicable.

**Why assign levers explicitly:** Reps who don't have a lever plan default to either phone-only (missing the familiarity compound effect of social) or social-only (missing the conversion power of outbound). The Five Levers ensure the full familiarity-building toolkit is deployed strategically, not randomly. (Blount, Ch. 12, pp. 97-104)

**Output for this step:** A Five-Lever allocation table — one row per account segment with lever assignments marked.

---

### Step 3 — Design the Multi-Touch Social Cadence

Build the weekly social touch schedule for each account segment. The cadence sequences touch types across a 4-6 week period designed to move the prospect across the Familiarity Threshold before a direct outbound contact.

**Touch sequence framework (LinkedIn-primary, 4-week cold prospect cadence):**

| Week | Day | Touch Type | Action | Note |
|---|---|---|---|---|
| 1 | Mon | Profile view | View the prospect's LinkedIn profile | Triggers a profile view notification |
| 1 | Thu | Follow | Follow the prospect on LinkedIn/Twitter | Visibility in their notifications |
| 2 | Mon | Engage content | Like or comment on a post they shared | Genuine, brief comment — not pitchy |
| 2 | Wed | Share content | Share an article relevant to their world | No direct mention of the prospect |
| 2 | Fri | Engage content | Comment on their company page post | Establishes pattern of presence |
| 3 | Mon | Connection request | Send personalized connection request | See template in Step 4 |
| 3 | Thu | Share content | Share second relevant article | Shows consistency, not one-off |
| 4 | Mon | Engage content | Comment on their post or reshare | Deepen presence |
| 4 | Thu | Social inbox message | Send first direct message after connection | Bridge-Because pattern (see Step 4) |
| 4 | Fri | Phone/email | First outbound call or email | Now anchored by social presence |

**Why this sequence matters:** Connection requests sent to cold strangers get ignored or declined. Spending 2-3 weeks engaging with the prospect's content before sending a connection request dramatically increases acceptance rates. By the time the direct message arrives, the prospect has seen your name 5-8 times and the interaction doesn't feel cold. (Blount, Ch. 13, p. 123)

**Cadence adjustments by familiarity state:**

| Familiarity | Weeks Before Direct Outreach | Touches Before Connection Request |
|---|---|---|
| Zero | 3-4 weeks | 4-6 touches |
| Low | 1-2 weeks | 2-3 touches |
| Moderate | Same week | 1 touch (or none) |
| High | Immediate | Skip cadence — connect and message same day |

**Daily time block:** Schedule 30-45 minutes per day for social prospecting activities — before or after the Golden Hours (the primary phone block). This is the only time social gets. Do not let it bleed into calling time. (Blount, Ch. 13, p. 128)

**Channel selection principle:** Go where your prospects hang out. For B2B, LinkedIn is the primary channel. If prospects are active on Twitter or other platforms, add those. Do not try to manage more than two to three channels consistently — effort dilutes beyond that. (Blount, Ch. 13, pp. 112-113)

---

### Step 4 — Draft Connection and Message Templates Using the Bridge-Because Pattern

Every outbound social message — whether a connection request or a direct inbox message — must follow the same principle as all prospecting messages: lead with what is in it for the prospect, not with what you want.

**Connection request template (personalized):**

> "Hi [Name] — I've been following your posts on [topic/industry]. Your recent piece on [specific topic] resonated with what I'm seeing with [relevant context]. I work with [role type] who are dealing with [relevant problem]. I'd like to add you to my network. — [Your name]"

**What NOT to do in a connection request:**
- Do not pitch a product or service
- Do not ask for a meeting
- Do not send a generic "I'd like to add you to my professional network" message
- Do not paste your email template into LinkedIn

**First inbox message template (post-connection, Bridge-Because pattern):**

> "Hi [Name] — Thanks for connecting. I noticed [specific observation about their company or a post they shared]. Most [role type] I work with are [dealing with / focused on / concerned about] [specific problem]. Because [specific insight or outcome you've helped similar people achieve], I thought it might be worth a quick conversation. How does [specific day + time] work for you?"

This template uses the **Bridge-Because pattern** from `prospecting-message-crafter`:
- Bridge: the observation about their specific situation
- Because: the reason they should give time (outcome, insight, or social proof)
- Ask: specific, direct, assumptive time request — not "let me know if you'd ever like to chat"

**Social inbox message rules:**
1. Never pitch in the first message after connecting. (Blount, Ch. 13, p. 111)
2. Wait until the prospect has seen your name at least 3-5 times before sending a direct message.
3. Only send a direct social message after connection is established — unsolicited LinkedIn InMail to cold strangers is expensive and low-conversion.
4. After crossing the Familiarity Threshold with a prospect, the social inbox becomes a valid supplement to email for brief, low-stakes messages.

**Referral ask template (for existing customers):**

> "[Name], thanks again for your business — I'm glad it's going well. I'm working to add more customers like you. Would you be able to introduce me to [specific person or type of person] in your network who might benefit from what we've done together?"

The referral ask formula: give a great experience → ask with a specific introduction target. The discipline to ask is more important than the technique. (Blount, Ch. 12, p. 100)

**Why these templates follow Bridge-Because:** Social buyers don't want to be pitched. They want to connect, interact, and learn. A message that opens with the prospect's problem and offers a reason for the conversation gets a response. A message that opens with your product gets you blocked. (Blount, Ch. 13, pp. 110-111)

---

### Step 5 — Schedule Social Touches into the Time Block

Map the social cadence onto the daily prospecting time block so it executes consistently without displacing phone and email activity.

**Daily social block structure (30-45 minutes, before or after Golden Hours):**

| Minutes | Activity |
|---|---|
| 0-10 | News stream scan: monitor LinkedIn/Twitter feed for trigger events and engagement opportunities from prospect list |
| 10-20 | Engage: like, comment, reshare 3-5 posts from prospects on the active cadence |
| 20-30 | Connect: send 2-3 new connection requests to prospects who have received 3+ touches |
| 30-40 | Message: send 1-2 social inbox messages to prospects who connected in prior weeks |
| 40-45 | Content: share or post one piece of curated or original content to feed |

**Why time-block social:** The social channel is designed to be addictive. Without a hard time limit, reps lose 2-3 hours of calling time to scrolling and liking. The cumulative impact of 30 disciplined daily minutes compounds over weeks into a meaningful familiarity effect. The individual sessions do not feel like much — the pattern is what works. (Blount, Ch. 13, p. 128)

**Content curation for the daily block:**

The social channel must be fed daily to maintain presence. Curating others' content is far more sustainable than creating original content and still produces familiarity and expert-positioning effects. Three sources for curation:
1. Industry publications and trade media (set up Google Alerts or RSS)
2. Thought leaders your prospects follow (reshare their content with a brief comment)
3. Company marketing content (approved — check with marketing first for brand compliance)

**Original content (optional, high-leverage):**

If time and appetite exist, original content — articles, short-form LinkedIn posts, videos, presentations — compounds faster than curation because it creates passive connections. Prospects who find your content relevant and follow you based on it represent inbound familiarity at scale. For most reps starting out, begin with curation; add original content after the curation habit is established.

**Personal branding checkpoint:** Before anything is posted, answer two questions:
1. Does this support my reputation as someone who solves problems and can be trusted?
2. Does this help prospects recognize my name in a positive way?

If either answer is "no" or "unsure," do not post it. (Blount, Ch. 13, p. 114)

---

### Step 6 — Write Outputs to File

Produce three output files:

1. **`five-lever-allocation-table.md`** — One row per account segment, with familiarity state, touch-count target, and active lever assignments for each account.
2. **`weekly-social-cadence.md`** — The 4-6 week touch sequence by day and activity type, customized to the user's channel mix and account list size.
3. **`social-templates.md`** — Connection request templates, first inbox message templates, referral ask templates, and content sharing examples — labeled with Bridge-Because element markers.

**Why externalize outputs:** The plan fails if it lives only in the rep's head. A written cadence creates a daily execution checklist. Written templates eliminate the "what do I say?" pause that causes reps to skip social touches. The allocation table lets the rep calibrate effort-per-account rationally. (Blount, Ch. 12, pp. 115-116)

---

## Inputs

| Input | Required | Format | Notes |
|---|---|---|---|
| Target account list | Yes | CSV, markdown, or pasted text | Company + contact name minimum |
| Social channels in use | Yes | User states | LinkedIn default; add others as relevant |
| Account tiers (from `prospect-list-tiering`) | Recommended | `tiered-prospect-list.md` | Enables calibrated lever assignment |
| Current familiarity notes | Recommended | Per-account notes or user description | Adjusts touch-count targets |
| Value prop / ICP | Recommended | `value-prop.md` or stated inline | Powers content curation and message bridges |
| Existing content activity | Optional | User description | Affects content lever recommendation |

---

## Outputs

| Output | Format | Description |
|---|---|---|
| `five-lever-allocation-table.md` | Markdown table | Per-segment lever assignments + familiarity state + touch target |
| `weekly-social-cadence.md` | Markdown table | 4-6 week day-by-day touch plan by channel |
| `social-templates.md` | Markdown | Connection requests, inbox messages, referral asks — Bridge-Because labeled |

---

## Key Principles

**Social is a layer, not a primary channel.** Phone and email produce contact and conversion rates that dwarf social media alone. Social selling's job is to reduce the number of outbound touches needed by building familiarity before the call. The rep who uses social as a layer on top of balanced prospecting outperforms the one who goes social-only every time. (Blount, Ch. 13, pp. 108-110)

**20 to 50 touches for cold prospects — not 3.** Most reps give up after 5-8 attempts. The data says cold prospects with zero familiarity require 20-50 touches before they engage. Social touches count. Each profile view, content engagement, and connection builds toward the Familiarity Threshold. Persistence is the first lever for a reason. (Blount, Ch. 12, pp. 96-97)

**Never pitch in the first social touch.** Social buyers want to connect, interact, and learn. A pitch in a connection request or first inbox message signals low trust and produces blocking, reporting, and damaged reputation. Lead with observation, offer insight, build enough familiarity before asking for anything. (Blount, Ch. 13, p. 111)

**The Five Levers compound.** A prospect who has seen your LinkedIn content, been introduced via a referral, met you briefly at a trade show networking event, and has received a few emails over 6 weeks will answer your phone call. No single lever gets you there alone. Stack them deliberately on your highest-value accounts. (Blount, Ch. 12, pp. 97-104)

**Consistency beats volume.** 30 disciplined daily minutes produces more than 3-hour binge sessions once a week. Social algorithms, notification patterns, and human memory all reward consistency. Build the daily block and protect it. (Blount, Ch. 13, p. 128)

**Familiarity is a two-edged sword.** Negative impressions (inflammatory posts, a poorly written profile, too-personal sharing) create familiarity that works against you. Every post, comment, like, and share is visible to prospects. Manage the message as carefully as the cadence. (Blount, Ch. 13, pp. 119-120)

**Balance familiarity-building with prospecting today.** It is easy to spend all day building familiarity instead of making calls. Familiarity building is an investment in the future — it does not pay today's quota. Protect Golden Hours for direct outbound activity and keep social in its time block. (Blount, Ch. 12, p. 104)

---

## Examples

---

### Example 1 — SDR Running LinkedIn on 100 Enterprise Accounts

**Situation:** An SDR at a SaaS company has 100 enterprise accounts in their territory. All are cold — no prior contact. LinkedIn is the primary research and familiarity channel. Phone and email are the primary outbound channels.

**Inputs:** Tiered prospect list (100 accounts, all Tier 1-2). LinkedIn only. No existing content activity.

**What the skill produces:**

- **Lever allocation:** Persistent Prospecting (all 100) + Personal Branding (LinkedIn content curation). Referrals and Networking flagged as a future layer once Tier 4 conquest accounts are identified.
- **Cadence design:** A 4-week social cadence with 30 accounts per week cycling through view → follow → engage → connect → message. At any given time, 20-30 accounts are in active social cadence.
- **Time block:** 30 minutes daily, before the morning calling block. 10 minutes of news scan and engagement, 15 minutes of connection requests and inbox messages, 5 minutes of content sharing.
- **Templates:** Personalized connection request that references the prospect's industry role and a specific post they shared; first inbox message using Bridge-Because pattern with the SDR's value proposition; no pitch language in either template.

**Output files:** Five-lever allocation table with 100 accounts (all marked Persistent + Personal Branding), weekly social cadence (week 1: observe and follow, week 2: engage content, week 3: connect, week 4: message + first call), and a social-templates.md with 3 connection variants and 2 inbox message templates.

---

### Example 2 — AE Warming 30 Strategic Accounts

**Situation:** An Account Executive manages 30 named accounts. Twelve are conquest Tier 4 accounts — high value, no prior relationship. The other 18 are Tier 2-3 with some qualification data but no open buying windows.

**What the skill produces:**

- **Lever allocation for Tier 4 (12 conquest accounts):** All five levers. Social cadence runs for 8 weeks (longer, because Tier 4 accounts warrant deeper investment). Referral mapping is included — who in the rep's existing customer base has connections at these accounts? Networking events in the industry vertical where these buyers appear are flagged.
- **Lever allocation for Tier 2-3 (18 accounts):** Persistent Prospecting + Personal Branding. Monthly social engagement touch keeps the rep's name visible while qualification work continues on other channels.
- **Templates:** Strategic bridge inbox message for conquest accounts — references a trigger event from LinkedIn (funding, expansion, hiring) and offers a specific insight, not a product pitch.
- **Referral ask:** A template for the rep's top 3 existing customers, asking for introductions to specific named contacts at the conquest accounts.

---

### Example 3 — Founder Building Personal Brand While Prospecting

**Situation:** A founder-seller is prospecting a mix of 50 SMB accounts while also trying to build enough personal brand presence on LinkedIn to start generating inbound leads over a 6-month horizon.

**What the skill produces:**

- **Lever allocation:** Persistent Prospecting (immediate, all 50 accounts) + Personal Branding (LinkedIn content, primary lever for long-term inbound). Networking (attend two local chamber or industry events per month). Referrals (systematic ask process built into every closed deal).
- **Content plan:** Week 1-4: curate 1 article per day from industry sources with a 1-sentence insight comment. Month 2 onward: 2 original short posts per week (problem-focused, no product mention). Over 6 months, build toward 1 original article per week.
- **Cadence:** Social block is 45 minutes daily. In the near term, 80% of time goes to engagement and connection; 20% to content. By month 3, the ratio shifts to 60% engagement / 40% content as the content habit is established.
- **Benchmark:** Building from zero on LinkedIn takes 6 months to 2 years to develop enough following to produce meaningful inbound leads. The founder sets a 6-month review point: if personal brand content is not generating 2-3 inbound inquiries per month by month 6, double outbound volume to compensate. (Blount, Ch. 13, p. 131)

---

## References

Detailed supporting materials:

- `references/five-levers-taxonomy.md` — Full definitions and tactics for each of the Five Levers of Familiarity, including sub-types of referrals (customer, personal, professional) and personal branding channels (LinkedIn content, public speaking, podcasts, webinars)
- `references/social-cadence-templates.md` — Full template library: connection request variants by industry, inbox message variants by value category (emotional / insight-curiosity / tangible-logic), referral ask scripts, content curation examples with commentary
- `references/five-cs-of-social-selling.md` — Full definitions and execution guidance for Connecting, Content Creation, Content Curation, Conversion, and Consistency, including tool categories (engagement tools, creation tools, curation tools, distribution tools, intelligence tools)
- `references/channel-selection-guide.md` — Decision framework for choosing primary and secondary social channels based on where the ICP hangs out; LinkedIn-primary guidance for B2B

**Source chapters:** Blount, Jeb. *Fanatical Prospecting.* Wiley, 2015.
- Chapter 12: "The Law of Familiarity" (pp. 96-104)
- Chapter 13: "Social Selling" (pp. 105-131)

**Depends on:**
- `prospecting-message-crafter` — Bridge-Because pattern used in all social inbox messages; must be run first to build the message nucleus
- `prospect-list-tiering` — Pyramid tier assignments drive lever allocation and cadence intensity per account

---

## License

Content derived from *Fanatical Prospecting* by Jeb Blount (Wiley, 2015). This skill is licensed under [Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/). You are free to share and adapt this material provided you give appropriate credit to Jeb Blount and BookForge, and distribute any derivative works under the same license.

---

## Related BookForge Skills

Install dependencies via clawhub:

```
clawhub install fanatical-prospecting/prospecting-message-crafter
clawhub install fanatical-prospecting/prospect-list-tiering
```

- **`prospecting-message-crafter`** (required) — Build the Bridge-Because nucleus that powers all social inbox messages before writing any social templates
- **`prospect-list-tiering`** (required) — Tier your account list before assigning levers; tier assignments drive cadence intensity and lever deployment
- **`cold-call-opener-builder`** — Deploy the message nucleus in the 5-step telephone framework for the outbound call that follows the social warm-up
- **`cold-email-writer`** — Build the multi-touch email cadence that runs in parallel with the social cadence
- **`prospecting-time-block-planner`** — Schedule the social selling time block within the full prospecting day alongside Golden Hour calling blocks
- **`balanced-prospecting-cadence-designer`** — Design the full multi-channel cadence of which this social layer is one component
