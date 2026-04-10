---
name: lead-nurture-sequence-design
description: "Use this skill to design a complete lead nurture system for a small
  business. Triggers when a user wants to set up a nurture sequence, email sequence,
  drip campaign, CRM follow-up system, shock and awe package, marketing calendar,
  or lead nurturing automation. Also activates for 'fill square 5', 'square #5 of
  the 1-Page Marketing Plan', 'how do I follow up with leads', 'CRM setup', 'email
  marketing', 'repeat customers', 'Joe Girard', 'drip campaign', 'marketing
  calendar', 'event-triggered automations', 'the money is in the follow-up',
  'shock and awe package', 'physical mail marketing', 'nurture leads', 'prospect
  database', or 'I captured leads but don't know what to do with them'."
version: 1.0.0
homepage: https://github.com/bookforge-ai/bookforge-skills/tree/main/books/the-1-page-marketing-plan/skills/lead-nurture-sequence-design
metadata: {"openclaw":{"emoji":"📚","homepage":"https://github.com/bookforge-ai/bookforge-skills"}}
status: published
source-books:
  - id: the-1-page-marketing-plan
    title: "The 1-Page Marketing Plan"
    authors: ["Allan Dib"]
    chapters: [5]
tags:
  - marketing
  - lead-nurture
  - email-marketing
  - crm
  - automation
  - small-business
depends-on:
  - lead-capture-ethical-bribe-design
execution:
  tier: 1
  mode: full
  inputs:
    - type: document
      description: >
        Business description, target market, captured lead list or CRM platform
        in use, and any existing email sequences or follow-up process. The lead
        capture system (from lead-capture-ethical-bribe-design) should already
        be in place, or the user should describe their current lead sources.
  tools-required: [Read, Write]
  tools-optional: []
  mcps-required: []
  environment: >
    Document set — business description, target market, and lead capture
    context. No code execution required.
discovery:
  goal: >
    Help the user build a complete lead nurture infrastructure: CRM selection,
    a 5-part 30-day email sequence, a shock and awe package (for inbound
    inquiries), a 5-cadence marketing calendar, an event-trigger map, and
    role assignments. Produces a nurture-sequence.md document with all
    components ready to implement.
  tasks:
    - "Inventory current nurture state and identify gaps"
    - "Confirm or select CRM platform"
    - "Design 5-part email sequence over 30 days (value-first)"
    - "Plan shock and awe package contents and delivery trigger"
    - "Build marketing calendar (daily / weekly / monthly / quarterly / annual)"
    - "Map event triggers to automated responses"
    - "Assign roles: Entrepreneur, Specialist, Manager"
    - "Write nurture-sequence.md with all outputs"
  audience:
    roles:
      - small-business-owner
      - solopreneur
      - entrepreneur
      - freelancer
      - startup-founder
    experience: beginner-to-intermediate
  when_to_use:
    triggers:
      - "User has captured leads but has no follow-up system"
      - "User is filling square #5 of the 1-Page Marketing Plan"
      - "User wants to set up automated email sequences or drip campaigns"
      - "User wants to design a shock and awe package for inbound inquiries"
      - "User wants to build a marketing calendar with recurring activities"
      - "User wants to map event-triggered automations in their CRM"
    prerequisites:
      - "Lead capture system in place (use lead-capture-ethical-bribe-design first)"
    not_for:
      - "Enterprise marketing automation teams with dedicated platforms already running"
      - "Businesses with no lead list — build that first with lead-capture-ethical-bribe-design"
  environment:
    codebase_required: false
    codebase_helpful: false
    works_offline: true
  quality:
    scores:
      with_skill: 100
      baseline: 35.7
      delta: 64.3
    tested_at: "2026-04-09"
    eval_count: 1
    assertion_count: 14
    iterations_needed: 1
---

# Lead Nurture Sequence Design

A structured process for small business owners to turn a captured lead list into
a revenue-generating relationship system. Based on the principle that 50% of
salespeople give up after one contact, 65% after two, and 79.8% after three —
meaning the business that keeps showing up with value wins by default. Produces
a complete nurture-sequence.md with CRM choice, email sequence outline, shock and
awe package plan, a 5-cadence marketing calendar, an event-trigger map, and role
assignments. Required content for square #5 of the 1-Page Marketing Plan canvas.

---

## When to Use

Use this skill immediately after lead capture is set up. The job of square #5 is
to convert interested prospects — who are not yet ready to buy — into raving fan
customers through consistent, value-first contact over time.

Also use it when:
- Leads are being captured but no one is following up consistently
- Email sequences exist but are pitch-heavy and getting ignored
- The business has no marketing calendar — every week starts from scratch
- A shock and awe package for inbound inquiries has not been designed
- The business is growing but marketing feels like random acts rather than a system

**Dependency check:** If leads are not yet being captured, invoke
`lead-capture-ethical-bribe-design` first — OR ask the user to describe their
current lead sources (business card collection, website forms, referrals, etc.)
before proceeding. This skill requires a list to nurture.

---

## Context & Input Gathering

### Required (must have before proceeding)
- Target market: who the business serves and their top pain points
- Current lead sources: how leads arrive (website form, events, referrals, ads)
- CRM platform in use (or willingness to choose one)

### Observable / inferrable
- Content assets available (blog posts, videos, guides, testimonials)
- Whether inbound inquiries are high enough volume to justify a physical shock
  and awe package
- Whether a Manager-type role exists or needs to be filled or outsourced

### Defaults (apply if not provided)
- CRM: recommend ActiveCampaign (automation), ConvertKit (content-first), or
  HubSpot free tier (all-in-one) based on business type
- Email sequence: default to 5-part, 30-day cadence (Days 1, 3, 7, 14, 30)
- Shock and awe package: recommend for any business with inbound inquiries and
  customer lifetime value above $500
- Marketing calendar: apply the 5-cadence default (daily/weekly/monthly/
  quarterly/annual) from the book verbatim

### Sufficiency check
Proceed when you can name: (1) the target market and their top pain point,
(2) how leads currently arrive, (3) a CRM or email platform to anchor the system.

---

## Process

### Step 1: Inventory the current nurture state

Ask the user to describe what happens after a lead is captured today. Map the
answer against the five infrastructure components: CRM, email sequences, physical
mail, shock and awe package, and event-triggered automations.

For each component, mark: Exists / Partial / Missing.

**WHY:** Most small businesses have one or two pieces in place (usually an email
platform and an occasional newsletter) but none of the components are connected
into a system. The inventory reveals which gaps are causing the most revenue
leakage. A business with no CRM cannot automate anything — fix that first.
A business with a CRM but no sequences is nurturing manually (or not at all).
The inventory sets the build order.

**Anti-pattern to watch for:** A single follow-up call after the lead capture,
followed by nothing. This is the most common broken pattern — and statistically,
79.8% of competitors stop at three contacts. Persistence beyond three contacts
puts you in the top 20.2% of all follow-up effort.

### Step 2: Confirm or select the CRM platform

The CRM is the nerve center of the entire nurture system. Every sequence, trigger,
contact record, and calendar task runs through it. Without a CRM, none of the
steps below can be automated or tracked.

**Selection criteria:**

| Platform | Best for | Automation depth |
|----------|----------|-----------------|
| ActiveCampaign | Service businesses, complex sequences | High |
| ConvertKit | Content creators, solopreneurs | Medium |
| HubSpot (free) | Small teams wanting all-in-one | Medium |
| Mailchimp | Simple lists, budget-constrained start | Low |
| Keap (Infusionsoft) | High-volume, complex funnels | Very high |

Recommendation rule: if customer lifetime value is above $1,000, invest in
ActiveCampaign or Keap. If under $500, ConvertKit or Mailchimp is sufficient
to start.

**WHY:** The CRM is not a cost — it is the infrastructure that makes every other
marketing activity compound over time. A business without a CRM is doing
marketing by hand, which means marketing stops the moment the owner stops.
Automation is what makes the system recur without owner involvement.

### Step 3: Design the email sequence (5-part, 30-day default)

Build a value-first email sequence triggered immediately when a new lead enters
the CRM. The default structure is 5 emails over 30 days.

**The 90/10 rule:** 90% of emails should deliver value (education, insight,
relevant content). Only 10% should make an offer. Pitch-heavy sequences erode
trust and increase unsubscribes.

**Default 5-part sequence structure:**

| Day | Email purpose | Tone |
|-----|--------------|------|
| 1 | Welcome + deliver the ethical bribe | Warm, helpful |
| 3 | Insight or tip relevant to their pain point | Educational |
| 7 | Case study or story of a problem like theirs solved | Story-driven |
| 14 | Address the most common objection or fear | Trust-building |
| 30 | Soft offer or invitation (not a hard sell) | Conversational |

**WHY:** The sequence is spaced to match the typical buying cycle, not the
business's impatience. A prospect who requested a free guide on Day 1 is not
ready to buy on Day 2. The sequence builds familiarity, establishes authority,
and keeps the business top-of-mind so that when the prospect IS ready to buy,
they think of this business first — not a competitor.

**Subject line principle:** The subject line determines whether the email gets
opened. It must be specific, relevant, and curiosity-inducing. A good test: would
you open it if it arrived in your inbox from a stranger?

**Length principle:** Length is irrelevant. Relevance is the criterion. A 1,000-
word email that is interesting will be read. A 200-word email that is boring
will not.

### Step 4: Plan the shock and awe package

A shock and awe package is a physical box mailed to high-probability inbound
prospects — people who have specifically reached out to inquire about the
business's product or service.

**When to use:** Triggered by an inbound sales inquiry (not applied to every
lead). It is the response to "send me more information" — the business sends a
physical package via a tracked courier service rather than a PDF link.

**Delivery method:** Send via FedEx or a tracked courier. A FedEx box on a desk
gets opened. A PDF email gets ignored. No one ignores a package with their name
on it.

**Contents to include (select 4–6 relevant to the business):**

| Item | Purpose |
|------|---------|
| A book (ideally one you authored) | Positions as expert; books are rarely discarded |
| DVD or USB with video introduction | Shows personality; demonstrates problem-solving |
| Testimonials (video, audio, or printed) | Social proof at the moment of highest interest |
| Media clippings or feature articles | Third-party authority |
| Brochures or sales letters | Specific offer details |
| Independent report or white paper | Demonstrates expertise |
| Product sample or gift card | Tangible value, motivates trial |
| Handwritten note | Personal touch; cuts through digital noise |

**Three jobs the package must do:**
1. Give unexpected value — the prospect should think "wow" not "brochure"
2. Position the business as the expert authority — not just another option
3. Move the prospect further down the buying cycle than they would otherwise be

**Budget check:** Calculate customer lifetime value first. If a new customer is
worth $5,000, a $50 shock and awe package is a 1% acquisition investment. The
numbers must make sense, but for most service businesses, they do.

**WHY:** Most businesses respond to inbound inquiries with the cheapest possible
reply: a link, a PDF, or a call. That is a same-same or crappy impression. A
shock and awe package creates a mind-blowingly amazing first impression at the
highest-intent moment in the buying process. Competitors almost never do this —
making it a durable competitive advantage.

### Step 5: Build the marketing calendar

A marketing calendar enforces consistency by treating marketing activities as
non-negotiable scheduled commitments, the same way tax deadlines are
non-negotiable. Set activities at five cadences:

| Cadence | Activity | Owner |
|---------|----------|-------|
| Daily | Check social media for mentions; respond appropriately | Manager |
| Weekly | Write one blog post; send link in email broadcast to list | Specialist |
| Monthly | Mail customers and prospects a printed newsletter or postcard | Manager |
| Quarterly | Send reactivation letter to past customers who haven't purchased recently | Specialist |
| Annually | Send all customers a gift basket thanking them for their business | Entrepreneur approves, Manager executes |

**Customize the table** for the business's specific channels and resources. The
cadences above are the book's defaults — adapt them, but do not reduce the
number of cadences. All five are required for a functioning marketing calendar.

**WHY:** Without a calendar, marketing happens when the business owner "has time"
— which means it happens rarely. The calendar creates the forcing mechanism.
Joe Girard sent 13,000 cards per month, every month, for over a decade. He did
not do it when he felt inspired. He did it because it was his system.

### Step 6: Map event-triggered automations

In addition to the scheduled calendar, certain business events should trigger
specific marketing responses automatically. Map each trigger to its response:

| Trigger event | Automated / assigned response |
|--------------|-------------------------------|
| Prospect met at networking event | Enter CRM; add to monthly newsletter list |
| Inbound sales inquiry received | Send shock and awe package via courier |
| New email subscriber from blog or ad | Start 5-part video or email series (30 days) |
| Customer complaint resolved | Send handwritten apology note + $100 gift voucher |
| Customer makes first purchase | Send welcome gift or onboarding sequence |
| Prospect has not responded in 90 days | Reactivation email: new offer or fresh angle |

Add business-specific triggers as appropriate (e.g., annual contract renewal,
seasonal buying patterns, product launch).

**WHY:** Triggers eliminate decision fatigue. When a specific event happens, the
response is predetermined and automated. The business does not have to remember
to follow up — the CRM does it. Event-triggered automations are the highest-
leverage element of the nurture system because they fire at the moments of
highest prospect attention (an inquiry, a complaint, a first purchase).

### Step 7: Assign roles — Entrepreneur, Specialist, Manager

Every recurring marketing activity needs an owner. The three types are:

- **Entrepreneur (makes it up):** Designs the strategy, chooses campaigns,
  writes the vision for what the nurture system should accomplish.
- **Specialist (makes it real):** Executes specific tasks — writes email copy,
  designs the shock and awe package, builds CRM automations.
- **Manager (makes it recur):** Ensures the calendar activities happen on
  schedule, monitors CRM health, checks that sequences are running.

**The missing role in most small businesses is the Manager.** The entrepreneur
had the idea. The specialist set up the system. But without a Manager, newsletters
don't go out, shock and awe packages don't get sent, and the calendar exists only
as a document.

For sole operators: outsource or part-time hire for the Manager role first.
Even 5–10 hours per week of admin support to run the marketing calendar is
more valuable than another tool or campaign.

**WHY:** The marketing system fails not because the ideas are wrong but because
the operational execution is inconsistent. A marketing infrastructure that runs
80% of the time beats a perfect strategy that runs 10% of the time. The Manager
role is the operational backbone that turns strategy into revenue.

### Step 8: Write nurture-sequence.md

Save the complete output as `nurture-sequence.md` in the user's working directory.
The document must contain all six components: CRM choice, email sequence outline,
shock and awe package plan, marketing calendar table, event-trigger map, and
role assignments.

**WHY:** Square #5 of the 1-Page Marketing Plan must be documented. Without a
written system, the nurture infrastructure lives only in intention — and intention
does not follow up with leads.

---

## Inputs

| Input | Format | Required |
|-------|--------|----------|
| Target market profile | text / .md | Yes |
| Current lead sources and volume | text | Yes |
| CRM or email platform in use | tool name | Recommended |
| Content assets available (guides, videos, testimonials) | list | Recommended |
| Customer lifetime value | dollar amount | Recommended (for shock and awe decision) |
| Existing email sequences or campaigns | text / file | Optional |

---

## Outputs

Primary output: `nurture-sequence.md`

```markdown
# Lead Nurture Sequence: [Business Name]

## CRM Choice
**Platform:** [Name]
**Reason:** [One sentence on why this fits]

## Email Sequence (5-part, 30 days)
| Day | Subject | Purpose |
|-----|---------|---------|
| 1   | [Subject line] | Welcome + deliver ethical bribe |
| 3   | [Subject line] | Value / insight |
| 7   | [Subject line] | Case study / story |
| 14  | [Subject line] | Address top objection |
| 30  | [Subject line] | Soft offer |

## Shock and Awe Package
**Trigger:** Inbound sales inquiry
**Delivery:** FedEx / tracked courier
**Contents:**
- [ ] [Item 1 — e.g., book]
- [ ] [Item 2 — e.g., testimonial compilation]
- [ ] [Item 3 — e.g., handwritten note]
- [ ] [Item 4 — e.g., sample or gift card]
**Estimated cost per package:** $[X]
**Customer lifetime value:** $[Y] → package is [X/Y]% of acquisition cost

## Marketing Calendar
| Cadence | Activity | Owner |
|---------|----------|-------|
| Daily | [social monitoring activity] | [role] |
| Weekly | [blog + email broadcast] | [role] |
| Monthly | [printed newsletter / postcard] | [role] |
| Quarterly | [reactivation letter] | [role] |
| Annually | [customer gift / thank-you] | [role] |

## Event-Trigger Map
| Trigger | Response | Automated? |
|---------|----------|-----------|
| Networking prospect met | CRM entry + newsletter | Manual → CRM |
| Inbound inquiry | Shock and awe package | Manual → fulfilled |
| New email subscriber | 5-part email series | Automated |
| Complaint resolved | Handwritten note + voucher | Manual |
| [Business-specific trigger] | [Response] | [Y/N] |

## Role Assignments
- **Entrepreneur:** [Name / Owner] — designs campaigns, approves calendar
- **Specialist:** [Name / contractor] — writes copy, builds CRM flows
- **Manager:** [Name / VA / outsourced] — runs the calendar, checks sequences

_Square #5 of the 1-Page Marketing Plan canvas: filled._
```

---

## Key Principles

**1. The money is in the follow-up.**
50% of salespeople give up after one contact. 65% give up after two. 79.8% give
up after three. At Contact #4, you are already ahead of 89.8% of all competitors.
At Contact #9, a prospect who is finally ready to buy will call you — you are the
only person who has stayed in touch. Persistence is not pestering; it is
positioning.

**2. Value first, offer rarely.**
90% of nurture communications should deliver genuine value: insights, tips, case
studies, industry news. Only 10% should contain an offer. Inverted ratios — where
every email is a pitch — train the prospect to ignore your messages. A prospect
who looks forward to your emails will buy from you when they are ready.

**3. Physical mail cuts through digital noise.**
Email inboxes are crowded. A hand-addressed envelope or a FedEx package on a desk
commands attention that a PDF cannot. Joe Girard built the world's greatest sales
record with monthly greeting cards — hand-addressed, varying envelope colors,
always with the message "I like you." By the end of his career, two-thirds of
his 13,001 car sales were to repeat customers who had to set appointments to buy
from him. Physical mail, used deliberately, is a premium channel.

**4. The Manager role is critical — and usually missing.**
Most small business marketing systems fail not from bad strategy but from missing
operational execution. The entrepreneur had the idea. The specialist built the
tools. But without someone whose job is to make it recur — send the newsletter,
pack the shock and awe box, enter the business card, check the CRM — the system
sits idle. Identify and fill this role before building a more sophisticated system.

**5. Event-triggered automations are the highest-leverage moves.**
Scheduled calendar activities are important for ongoing presence. But triggered
automations fire at the moments of highest prospect attention — an inbound
inquiry, a resolved complaint, a first purchase. These moments are the most
persuasive because the prospect is already engaged. Automating the right response
to these triggers is worth more than any amount of cold outreach.

---

## Examples

### Example 1: Joe Girard — Monthly Greeting Cards (verbatim from source)

Joe Girard is listed in the *Guinness World Records* as "the world's greatest
salesman." Between 1963 and 1978, he sold 13,001 cars at a Chevrolet dealership —
more retail big-ticket items, one at a time, than any other salesperson in
recorded history. His stats: 13,001 cars total, 18 on his best day, 174 in his
best month, 1,425 in his best year. He sold more cars by himself than 95% of all
dealerships in North America.

His core nurture system: a personalized greeting card mailed every month to his
entire customer list. In January, it was a Happy New Year card. In February, a
Valentine's Day card. The message inside was always the same: "I like you." He
would vary the size and color of the envelope — this was critical to bypassing
the postal equivalent of spam filters, where people stand over the trash can and
discard anything that looks like an ad or junk mail. By the end of his career, he
was sending 13,000 cards per month and needed to hire an assistant.

By the time he was a decade into his career, almost two-thirds of his sales were
to repeat customers. It got to the point where customers had to set appointments
in advance to come in and buy from him — contrast that with other car salespeople
who stood around waiting and hoping for walk-in traffic.

**The lesson:** Consistent, personal, low-pitch contact over years builds a
pipeline that sells itself. The content of the card was not about cars. It was
about the relationship.

---

### Example 2: Shock and Awe Package — Professional Services Firm

**Trigger:** A prospective client emails asking about accounting services.

**Standard response (same-same):** Email back a PDF brochure of services and a
link to the website.

**Shock and awe response:**
- FedEx package arrives within 48 hours containing:
  - A copy of a relevant book on small business finance (positions firm as expert)
  - A printed compilation of 5 client testimonials (one from a similar industry)
  - A one-page media clipping from a local business publication featuring the firm
  - A handwritten note: "Thank you for reaching out. Inside is everything you
    need to know about how we work and why our clients stay with us for years."
  - A gift card to a local coffee shop: "Have a coffee on us while you read."

**Result:** The prospect is not evaluating three accounting firms from their inbox.
They have a physical box on their desk from one firm that went out of its way to
impress them before a single dollar was spent. At a customer lifetime value of
$8,000/year, a $60 package is 0.75% of first-year value.

---

### Example 3: Local Physiotherapy Clinic — Full Nurture System

**CRM:** ActiveCampaign (patient records + email automation)

**Email sequence (new inquiry, 30 days):**
- Day 1: Welcome + link to free stretching guide (ethical bribe delivered)
- Day 3: "The most common mistake people make after a sports injury"
- Day 7: Patient story — back pain resolved in 6 sessions
- Day 14: FAQ — "How many sessions will I need? What should I expect?"
- Day 30: "Book your first appointment — this week only, we have 3 openings"

**Shock and awe package:** Triggered for inbound referrals from GPs or surgeons
(high-value patients). Contents: clinic brochure, testimonials, a printed copy
of a patient recovery guide, and a handwritten note from the lead physiotherapist.

**Marketing calendar:**
- Daily: monitor Google reviews and Facebook mentions; reply within 2 hours
- Weekly: publish one injury-prevention tip on the blog; send to email list
- Monthly: mail a postcard to lapsed patients ("It's been 6 months — how is your
  recovery going?")
- Quarterly: send a reactivation letter to patients not seen in 12+ months
- Annually: send a small gift basket to top 20 referring GPs

**Event triggers:**
- New patient books first appointment → welcome email sequence starts
- Patient cancels appointment → reschedule email + 15% discount on next booking
- 5-star Google review posted → thank-you email + referral ask

**Roles:** Owner (Entrepreneur) designs campaigns. Admin coordinator (Manager)
runs the calendar. Outsourced copywriter (Specialist) writes email content.

---

## References

- Research summary: `.meta/research/lead-nurture-sequence-design.md`
- Hunter report: `.meta/research/hunter-report.md` (sk-07 entry)
- Dependency: `skills/lead-capture-ethical-bribe-design/SKILL.md`
- Previous skill in sequence: `lead-capture-ethical-bribe-design` (square #4)
- Canvas meta-skill: `marketing-plan-canvas` (square #5 slot)
- Book profile: `.meta/book-profile.json`

## License

This skill is licensed under [CC-BY-SA-4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Source: [BookForge](https://github.com/bookforge-ai/bookforge-skills) — The 1-Page Marketing Plan by Allan Dib.

## Related BookForge Skills

Install related skills from ClawhHub:
- `clawhub install bookforge-lead-capture-ethical-bribe-design`

Or install the full book set from GitHub: [bookforge-skills](https://github.com/bookforge-ai/bookforge-skills)
