---
name: viral-loop-designer
description: "Use this skill to design a viral or referral loop for a post-PMF product by extracting the PATTERN (not the tactic) from canonical case studies — Dropbox bilateral-incentive referral, Hotmail email-signature instrumented virality, Airbnb Craigslist cross-posting, LinkedIn public-profile SEO virality — and adapting it to the user's product. Classifies the mechanism type (word-of-mouth amplification, instrumented virality, embedded referral), models K-factor (invitations × conversion rate) and cycle time, and produces a viral-loop-design.md with the loop diagram plus a referral-test-plan.md for experiment execution. Flags the viral spam trap (when sharing becomes annoying and hurts the brand). Triggers when a growth PM asks 'how do I build a referral program like Dropbox?', 'viral loop design', 'how do I make my product viral', 'referral program', 'word of mouth growth', 'K-factor', 'viral coefficient', 'invite mechanism', 'should I offer referral rewards', 'bilateral incentive', 'Hotmail email signature', 'Airbnb Craigslist hack', 'LinkedIn public profiles', or 'viral loop testing'. Also activates for 'our referral program isn't working', 'viral spam trap', or 'refer a friend program design'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/hacking-growth/skills/viral-loop-designer
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: hacking-growth
    title: "Hacking Growth"
    authors: ["Sean Ellis", "Morgan Brown"]
    chapters: [5, 9]
tags:
  - growth
  - viral-growth
  - referral
  - acquisition
  - startup-ops
depends-on:
  - acquisition-channel-selection-scorer
  - north-star-metric-selector
execution:
  tier: 1
  mode: plan-only
  inputs:
    - type: document
      description: >
        Product brief (product-brief.md) with description and ideal customer profile.
        Optional: current-referral-data.md describing any existing referral mechanism,
        referral send rate, activation rate, and opt-out/spam complaint rate.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set. Plan-only — produces a viral loop design document and a
    referral test plan. No code execution required.
discovery:
  goal: >
    Produce a viral-loop-design.md with a loop diagram, K-factor model, and
    mechanism classification, plus a referral-test-plan.md for experiment
    execution — tailored to the user's product, not a generic referral template.
  tasks:
    - "Read product brief and optional referral data"
    - "Assess viral capability"
    - "Classify best mechanism type"
    - "Map matching case-study pattern"
    - "Draft loop diagram with K-factor model"
    - "Design first experiment"
    - "Flag the viral spam trap"
    - "Emit deliverables"
---

# Viral Loop Designer

Structured design of a viral or referral loop for a post-PMF product. Classifies the
mechanism type, maps the closest canonical pattern (Dropbox, Hotmail, Airbnb, LinkedIn)
to the user's product, models K-factor and cycle time, and produces a loop diagram with
a test plan — all grounded in pattern extraction, not tactic copying.

---

## When to Use

Use this skill when:

- You want to design or redesign a referral or viral growth mechanism
- Your team is asking "how do we grow like Dropbox?" or "should we build a referral program?"
- A referral program exists but isn't producing measurable results
- You want to evaluate whether your product has viral potential before investing in a loop
- You need to choose between word-of-mouth amplification, instrumented virality, and
  explicit bilateral incentives

**Prerequisites:**
- Product/market fit confirmed (must-have score ≥ 40% "very disappointed" or stable
  retention curve). Virality on a product that doesn't deliver the aha moment accelerates
  churn, not growth — users arrive, experience nothing, leave, and tell no one to join.
  See `product-market-fit-readiness-gate` to confirm before proceeding.
- A defined North Star Metric. The viral loop must compound the metric that reflects real
  value delivered — not invites sent or accounts created. See `north-star-metric-selector`.

---

## Context and Input Gathering

Read the following before beginning:

1. **product-brief.md** (required) — Product description, ideal customer profile,
   core value proposition, current growth stage, and any referral history.
2. **current-referral-data.md** (optional) — Existing referral mechanism description,
   referral send rate, activation rate from referrals, and opt-out or spam complaint rate.
   If not provided, note its absence and proceed with product-brief analysis only.

If either document is missing critical information (no ICP, no value proposition, no
growth stage), ask one targeted question before proceeding. Do not design a loop for
an underspecified product — mechanism choice depends on product structure, not generic
best practices.

---

## Process

### Step 1 — Read the Product Brief

Read product-brief.md and optional referral data. Extract:
- What the product does and for whom
- What triggers the aha moment (the first experience of core value)
- Whether the product has any existing sharing or invite behavior
- Current acquisition channels and growth stage

**Why:** Viral loop design is downstream of product understanding. The mechanism type
you choose (Step 3) depends entirely on whether the product naturally creates sharing
occasions, whether it benefits from more users joining, and whether its core value can
be embedded in an invite.

---

### Step 2 — Assess Viral Capability

Evaluate whether the product has structural conditions for viral growth. Answer these
three questions explicitly:

1. **Network effect?** Does the product become more valuable as more users join?
   (Social networks, marketplaces, and messaging apps: yes. Grocery store apps,
   single-player tools: typically no.)
2. **Natural sharing occasions?** Does using the product create moments where users
   would naturally tell others or share an output? (File sharing, event tickets, payments,
   content — yes. Personal productivity tools — often no.)
3. **Incentive alignment?** Can a referral incentive be tied directly to the product's
   core value rather than bolted on as unrelated cash?

**Verdict:** If all three are weak, flag this explicitly. Virality is possible through
word-of-mouth amplification, but embedded referral or instrumented virality will
require heavy investment for modest returns. Recommend focusing on organic and paid
channels (see `acquisition-channel-selection-scorer`) and returning to viral design
after retention has stabilized further.

**Why:** Not every product goes viral. The mechanism must match the product's structure.
Designing an embedded referral loop for a product with no network effect and no natural
sharing occasion wastes engineering cycles and can damage user trust if the incentive
feels misaligned.

---

### Step 3 — Classify the Mechanism Type

Based on the viral capability assessment, classify the best-fit mechanism:

**Word-of-Mouth Amplification**
- Organic sharing driven by genuine product delight — not engineered
- Can be accelerated through Net Promoter Score programs, testimonials, community
  building, and public-facing content seeding (e.g., Upworthy's catchy headline system)
- Best for: products with exceptional product/market fit but low natural sharing occasion
- K-factor impact: low to moderate, but high lifetime value per referred user
- Cycle time: long (unpredictable)

**Instrumented Virality**
- Product features engineered to mechanically expose new users to the product as a
  side-effect of core usage
- The invite is embedded in the product's output — users need do nothing extra
- Best for: products whose output is inherently shareable or distributable
  (email, documents, event listings, payments, design files)
- K-factor impact: can be very high due to high frequency; payload is often low
- Cycle time: short (continuous, passive)
- Examples: Hotmail email signature, Airbnb Craigslist cross-posting

**Embedded Referral**
- Explicit "invite friends" program with a designed incentive — bilateral (both parties
  rewarded) or unilateral (only the referrer rewarded)
- Requires active user participation — users must consciously invite
- Best for: products with network effects or storage/capacity mechanics where users
  genuinely benefit from more people joining
- K-factor impact: moderate, controlled by incentive quality and program visibility
- Cycle time: moderate (days to weeks from invite to activation)
- Example: Dropbox free storage for both referrer and referee

**Why:** Mechanism classification determines the build complexity, the experiment
sequence, and the failure modes to watch for. Choosing instrumented virality for a
product without shareable output produces expensive engineering work with zero result.
Choosing embedded referral for a product without incentive alignment produces low
conversion and user annoyance.

---

### Step 4 — Map the Closest Case-Study Pattern

Match the product to the canonical pattern that is structurally closest. Extract the
pattern — the structural logic — not the tactic.

**Dropbox Pattern (Bilateral Embedded Referral)**
- Structural logic: collaborative product + network effect + product-native incentive
  (more storage = more value to the user) + near-zero marginal cost of the incentive.
- Apply when: users collaborate with non-users using your product; giving more product
  resource as reward costs you little; incentive is hard to compare to cash effort.
- Key insight: the incentive must be product-native. Storage feels more generous than
  its cost because users can't easily price it. Cash is easy to benchmark against effort.

**Hotmail Pattern (Passive Instrumented Virality)**
- Structural logic: every use generates output that reaches non-users; embed the
  conversion invitation in that output; make signup require one click and thirty seconds.
- Apply when: the product's output (email, document, invoice, form, booking) is
  inherently visible to non-users.
- Key insight: friction at the invitation collapses the funnel. The Hotmail link resolved
  to immediate value — free email — in under a minute. Zero user action required to share.

**Airbnb Pattern (Cross-Platform Distribution)**
- Structural logic: your content lives on your platform; insert it into a higher-traffic
  adjacent platform where the target audience already searches; no user action required.
- Apply when: your product has user-generated listings or content; an adjacent platform
  hosts your target audience's searches; cross-posting carries manageable platform risk.
- Key insight: instrumented virality through platform arbitrage. Build it, measure it,
  but treat it as a channel — not a permanent acquisition architecture.

**LinkedIn Pattern (SEO-Driven Profile Virality)**
- Structural logic: users create data inside your product; making it publicly indexable
  converts your user base into a permanent SEO acquisition surface.
- Apply when: your product has user-generated data others search for by name, expertise,
  or topic; making it public does not violate privacy expectations or compliance.
- Key insight: this is a distribution architecture decision, not a referral program.
  Loop: user creates data → indexed → non-user finds via search → converts. Cycle time
  is long (months) but compounding is durable and zero marginal cost.

**Why:** Copying tactics without understanding structural logic produces failure.
Dropbox worked not because bilateral incentives are magic, but because file storage
benefits from more users joining, the incentive was product-native, and marginal cost
was near zero. Map the structural logic — then validate fit — before committing to build.

---

### Step 5 — Draft the Loop Diagram with K-Factor Model

Produce a written loop diagram (steps with arrows) and a K-factor model.

**Loop diagram format:**

```
[Trigger] → [Share Action] → [Recipient Exposure]
→ [Recipient Conversion] → [New User Activates] → [Loop Repeats]
```

Label each step with: who acts, what they do, where friction exists, and the drop-off
risk at each transition.

**K-factor model (fill in estimates before any engineering is committed):**

```
K = (avg invites per active user) × (invitation-to-signup conversion rate)
Virality = Payload × Conversion Rate × Frequency

K > 1.0 — compounding (rare); K 0.5–1.0 — strong supplement; K < 0.1 — redesign first
```

**Cycle time:** How many days from signup to first invite sent? Shorter cycles compound
faster than a higher K with long cycles.

**Why:** Teams that skip modeling discover after building that K = 0.048 and wonder why
growth did not change. Model first — the estimates reveal whether the mechanism is worth
building or whether the incentive needs redesigning before engineering begins.

---

### Step 6 — Design the First Experiment

Choose the lowest-cost test that validates the most important assumption in the loop.

Hierarchy of testability (cheapest first):
1. **Incentive/message test** — Does the incentive resonate before building? Test with
   a landing page or email offer. Compare product-resource reward vs. cash discount.
2. **Invite mechanic stub** — Can you test the sharing flow manually before engineering
   it? Have users email friends manually; track conversion.
3. **Minimum loop build** — One sharing path, one incentive, one recipient landing page.
   No gamification, no optimization. Just measure K.

Specify: hypothesis ("If we offer [incentive] to both parties, [X]% of active users will
send at least one invite within 14 days"), success K threshold, and three metrics to
track: referral send rate, referral-to-activation rate, time-to-first-invite.

**Why:** Dropbox discovered the collaboration framing outperformed the storage framing
only through testing — not predictable in advance. LinkedIn found four invites optimal
vs. two or six through experiment. Building the full system before testing the incentive
produces an expensive loop with an unvalidated conversion assumption at its core.

---

### Step 7 — Flag the Viral Spam Trap

Explicitly assess whether the proposed loop design risks crossing from helpful to
annoying. Check all three signals:

**Spam trap indicators:**
- The mechanism increases payload by requiring or tricking users into sending invites
  to their full contact list rather than selected people
- The recipient experience hits a hard authentication wall before delivering value
- Referral activation rate is below 5% (most invites generate no engagement)
- App store reviews or social media mention "spam" in connection with the product

**Rules:**
- Never increase payload by adding friction-removing dark patterns (pre-checked contact
  lists, repeated prompts, misleading invite copy). Short-term volume gains produce
  long-term brand damage that is expensive to recover from.
- Measure the recipient experience explicitly before scaling invite volume. An invite
  that annoys the recipient destroys two relationships: the recipient's potential
  conversion and the referrer's trust in the brand.
- If opt-outs or spam complaints rise while referral volume rises, cut invite frequency
  immediately. Growth at the cost of brand is negative-value growth.

**Why:** BranchOut bypassed Facebook's invite limit and grew from 4M to 25M users in
three months through engineered viral spam. Then lost 4%+ of monthly active users per
day as users experienced a hollow product and their spammed contacts never engaged.
Despite $50M in funding, BranchOut never recovered. The viral spam trap compounds:
every spammed contact is a burned conversion opportunity and a brand impression that
signals low quality.

---

### Step 8 — Emit Deliverables

Write two files:

**viral-loop-design.md** — Contains:
- Mechanism type (word-of-mouth amplification / instrumented virality / embedded referral)
- Matched case-study pattern and structural logic
- Loop diagram (steps with friction labels)
- K-factor model with estimates for payload, conversion rate, frequency
- Cycle time estimate
- Viral capability assessment verdict (GREEN / YELLOW / RED)

**referral-test-plan.md** — Contains:
- First experiment hypothesis and success/failure threshold
- Testability hierarchy decision (why this experiment before the full build)
- Measurement plan (metrics, sample size, timeline)
- Spam trap checklist (pre-flight check before scaling any invite volume)

**Why:** Separating the design document from the test plan allows the design to be
reviewed and revised independently of the experiment setup — and allows the experiment
to be handed to an engineer or growth PM who doesn't need to re-read the full design
reasoning to set up the test.

---

## Key Principles

**Virality requires product-level fit — not every product goes viral.**
Network-effect and sharing-native products have structural virality advantage. Products
without these characteristics can still grow through word-of-mouth, but embedded
referral loops will underperform unless the product is genuinely must-have and the
incentive is deeply product-native.

**Bilateral incentives consistently outperform unilateral.**
If only the referrer benefits, the referral is a transaction the recipient did not agree
to. If both parties benefit, the referrer is doing their contact a favor. The social
dynamic changes from extraction to generosity, and conversion improves accordingly.
Dropbox's bilateral storage offer worked because both sides received something they
genuinely wanted — not a promotional discount on something they hadn't asked for.

**Cycle time compounds — shorter cycles beat bigger incentives.**
A K of 0.6 with a 3-day cycle time produces more compounding over 90 days than a K of
0.8 with a 25-day cycle time. Invest in reducing the time from new-user-signup to
first-invite-sent. Friction in the share flow (too many steps, unclear incentive,
buried UI) extends cycle time. Visibility and integration (Uber's referral prompt on
the active ride screen, LinkedIn's connect prompt at sign-up) compresses it.

**K > 1 means compounding growth; K < 1 is an acquisition supplement, not an engine.**
K > 1.0 is rare and typically short-lived. A K of 0.5 consistently is excellent — it
means 50% of your growth comes from the loop. Communicate this clearly with leadership.
"Referral" does not mean "free growth that replaces paid acquisition" — it means one
cost-efficient acquisition channel that should be part of a diversified mix.

**The viral spam trap destroys brand faster than it acquires users.**
Every spammed contact is a burned conversion and a negative brand impression. Dark
patterns (pre-checked contact lists, deceptive invite copy, forced bulk sharing) produce
short-term volume spikes and long-term brand damage. BranchOut is the named cautionary
case. Measure recipient activation rate before scaling invite volume; if it is below 5%,
improve the incentive quality, not the send frequency.

**Extract the pattern, not the tactic — then validate the fit.**
Dropbox's bilateral storage incentive worked because of four specific structural
conditions: collaborative product, network effect, product-native incentive, near-zero
marginal cost. Copying the bilateral incentive structure without those conditions
produces an expensive referral program with low conversion. Map the structural logic to
your product before committing to any mechanism.

---

## Examples

### Example A: Embedded Referral for a B2B SaaS Project Management Tool

**Product:** A post-PMF project management SaaS. Teams use it together — inviting
teammates is a natural part of onboarding. Network effect is strong: more team members
using it makes it more valuable for the person who invited them.

**Viral capability assessment:** GREEN. Strong network effect (collaborative by design).
Natural sharing occasion (teammate invitation is required for core use). Incentive
alignment possible (free seats / extra storage / premium features as reward).

**Mechanism type:** Embedded Referral (bilateral incentive).

**Pattern match:** Dropbox. The product is collaborative; getting others on the platform
improves the referrer's experience; giving away additional seats has near-zero marginal
cost at volume.

**Loop diagram:**
```
[User A joins and activates] → [Prompted to invite teammates during onboarding]
→ [Teammate receives email with credit offer for both A and teammate]
→ [Teammate signs up, activates, experiences aha moment]
→ [Teammate is prompted to invite their own team members]
→ [Loop repeats]
```

**K-factor model:**
- Payload: 3.2 (average teammates invited per active inviter)
- Conversion rate: 22% (teammates who accept and activate)
- K = 3.2 × 0.22 = 0.70
- Frequency: once per new user at onboarding (low frequency, but high conversion)
- Virality = 3.2 × 0.22 × 1.0 = 0.70

**Cycle time:** ~7 days (invite sent day 1, teammate activates by day 7 on average).

**First experiment:** Test the incentive without building the full system. Email the
top 20% most active users. Offer one extra seat free (bilateral: both users get the
seat) if they invite a teammate this week. Track invite send rate and acceptance rate.
Success threshold: ≥ 30% invite rate from active users contacted, ≥ 15% teammate
acceptance. If below threshold, test a premium feature unlock instead.

**Spam trap check:** PASS. Invite is addressed to specific teammates by name. Recipient
receives a clear benefit. No dark patterns. Activation rate from teammates is expected
to be high because they are already working with the referrer.

---

### Example B: Instrumented Virality for a Content Publishing Platform

**Product:** A platform where professionals publish articles and case studies. Each
article is a public page. Non-users can read articles without signing up. The platform
has no social graph or network effect — reading an article is not improved by more
users joining.

**Viral capability assessment:** YELLOW. No network effect. Strong natural sharing
occasion (articles are meant to be shared). Incentive alignment is weak (bilateral
storage/credits feel disconnected from publishing). Instrumented virality is a better
fit than embedded referral.

**Mechanism type:** Instrumented Virality (LinkedIn pattern + Hotmail pattern hybrid).

**Pattern match:** LinkedIn public profiles. Every published article is already a public
page. The growth action is to make those pages fully searchable and to embed a conversion
call-to-action for non-authenticated readers.

**Loop diagram:**
```
[User A publishes article] → [Article is indexed by search engines (SEO surface)]
→ [Non-user B finds article via Google search]
→ [Non-user B reads article → sees "Write your own case study" CTA with free account]
→ [Non-user B signs up and publishes their first article]
→ [Article is indexed → new loop pass begins]
```

**K-factor model (adapted — this is SEO-driven, not invite-driven):**
- Payload: 0 (no explicit invite; distribution is passive)
- Conversion rate: 2.8% (non-authenticated readers who create an account)
- Frequency: articles are published ~2 times/month per active user; each article
  receives on average 340 unique readers per month
- Estimated new signups per active user per month: 340 × 0.028 = ~9.5 new signups/month
- K (monthly, per active user): ~9.5 (a very different K calculation for SEO loops —
  the payload is replaced by organic traffic volume)

**Cycle time:** Long (3–6 months for new articles to rank meaningfully). Invest in
on-page SEO optimization of article templates to compress this.

**First experiment:** Enable public indexing for the top 100 most-viewed articles.
Check Google Search Console in 30 days for impressions and clicks. Success threshold:
≥ 500 new organic sessions to those articles within 30 days. If yes, make all articles
public by default and instrument the "sign up to publish" CTA prominently on article pages.

**Spam trap check:** NOT APPLICABLE. This loop has no invite mechanism and generates
no unsolicited contact. Monitor for content quality degradation as sign-ups increase —
a different quality trap, not a spam trap.

---

## References

- `references/viral-loop-mechanics.md` — Detailed K-factor formula derivations, Sean
  Parker's virality equation (Payload × Conversion Rate × Frequency), and cycle time
  compounding models.
- `references/case-study-patterns.md` — Full structural analysis of the Dropbox,
  Hotmail, Airbnb, and LinkedIn patterns with applicability criteria.
- `references/viral-spam-trap.md` — Detailed BranchOut case study, dark pattern
  taxonomy, and detection checklist with metric thresholds.

---

## License

This skill is licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source book content is referenced under fair use for educational purposes. Attribution:
Ellis, Sean and Brown, Morgan. *Hacking Growth*. Crown Business, 2017.

---

## Related BookForge Skills

- `clawhub install bookforge-acquisition-channel-selection-scorer` — viral loops are
  one acquisition channel category; score them against organic and paid alternatives
  before committing engineering resources.
- `clawhub install bookforge-north-star-metric-selector` — viral loops must compound
  the North Star Metric, not a vanity metric like invites sent or accounts created.
- `clawhub install bookforge-product-market-fit-readiness-gate` — virality on a
  product that people don't find must-have accelerates churn, not growth. Confirm PMF
  before designing any viral loop.
- `clawhub install bookforge-growth-experiment-prioritization-scorer` — use the
  experiment scorer to rank the viral loop experiment against other growth bets in
  the team's backlog before committing build resources.
