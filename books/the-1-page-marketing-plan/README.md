# The 1-Page Marketing Plan

13 agent skills for direct response marketing — covering target market selection, messaging, offers, advertising, lead capture, nurturing, sales conversion, customer experience, lifetime value, and referrals, extracted from **The 1-Page Marketing Plan** by Allan Dib.

These skills teach AI agents how to apply Allan Dib's 9-square canvas framework — a systematic approach to acquiring customers, delivering value, and building a tribe of loyal clients for any small or medium business.

**Average quality delta: +75.6 points** (93.4% with-skill vs 17.8% baseline).

## Install

```
claude plugin add bookforge-ai/bookforge-skills/books/the-1-page-marketing-plan
```

## Skills

| Skill | Description | Tier | Mode | Delta |
|-------|-------------|------|------|------:|
| target-market-selection-pvp-index | Select the ideal target market using the PVP Index (Personal fulfillment, Value to marketplace, Profitability) — scoring and ranking market segments | 1 | full | +79 |
| marketing-metrics-dashboard | Build a marketing metrics dashboard tracking the 7 key numbers: Leads, Conversion Rate, ATV, Break-Even, Gross Margin, Churn Rate, and CLV | 1 | full | +61 |
| customer-experience-systems-design | Design and document the four core business systems (Marketing, Sales, Fulfillment, Administration) and create memorable customer experiences | 1 | full | +71 |
| customer-revenue-quality-audit | Classify every customer into Tribe, Churners, Vampires, or Snow Leopards archetypes — score with NPS and produce a fire/grow decision per customer | 1 | full | +92 |
| marketing-message-and-usp-crafting | Craft a differentiated USP, write a Problem/Solution/Proof elevator pitch, and engineer headlines that activate the 5 core emotional buying motivators | 1 | full | +64 |
| irresistible-offer-builder | Construct a complete irresistible offer using the 8-element checklist — Value Stack, Outrageous Guarantee, Scarcity, Payment Plan, and more | 1 | full | +92.9 |
| lead-capture-ethical-bribe-design | Design a lead-capture ad strategy using an ethical bribe that self-selects high-probability prospects | 1 | full | +71.4 |
| customer-lifetime-value-growth | Grow CLV using five levers — raise prices, upsell, ascension ladder, purchase frequency, and reactivation campaigns | 1 | full | +57.1 |
| referral-system-design | Design an active referral system with referral scripts, gift card mechanisms, joint venture partners, and bystander effect override | 1 | full | +71.4 |
| advertising-media-roi-framework | Select advertising media channels, calculate CAC per channel, and make stop/measure/scale decisions with concentration-risk checks | 1 | full | +85.7 |
| lead-nurture-sequence-design | Design a complete lead nurture system — shock-and-awe packages, drip sequences, CRM follow-up cadences, and trusted advisor positioning | 1 | full | +64.3 |
| sales-conversion-trust-system | Convert nurtured leads into customers — outrageous guarantees, risk reversal, 3-tier pricing, closing scripts, and post-sale wow | 1 | full | +92.9 |
| marketing-plan-canvas | Build, assemble, or audit a complete 9-square 1-Page Marketing Plan canvas integrating all upstream skills into a single strategy document | 1 | full | +78.6 |

## Dependency Graph

```
Level 0 (independent foundations):
  target-market-selection-pvp-index     <-- hub (4 direct dependents)
  marketing-metrics-dashboard
  customer-experience-systems-design
  customer-revenue-quality-audit

Level 1 (depends on Level 0):
  marketing-message-and-usp-crafting    ──> target-market-selection-pvp-index
  irresistible-offer-builder            ──> target-market-selection-pvp-index
  lead-capture-ethical-bribe-design     ──> target-market-selection-pvp-index
  customer-lifetime-value-growth        ──> customer-experience-systems-design
  referral-system-design                ──> customer-experience-systems-design

Level 2 (depends on Level 1):
  advertising-media-roi-framework       ──> target-market-selection-pvp-index
                                        ──> marketing-message-and-usp-crafting
                                        ──> lead-capture-ethical-bribe-design
  lead-nurture-sequence-design          ──> lead-capture-ethical-bribe-design
  sales-conversion-trust-system         ──> lead-nurture-sequence-design
                                        ──> irresistible-offer-builder

Level 3 (meta — integrates all):
  marketing-plan-canvas                 ──> all 10 content skills
```

## Quality Summary

| Metric | Value |
|--------|------:|
| Average with-skill score | 93.4% |
| Average baseline score | 17.8% |
| Average delta | +75.6 |
| Skills passed | 13/13 |
| Iterations required | 1 (all first pass) |

Highest delta: `irresistible-offer-builder` and `sales-conversion-trust-system` (+92.9 each).
Lowest delta: `customer-lifetime-value-growth` (+57.1) — baseline had partial instincts on price raises and reactivation.

## License

[CC-BY-SA-4.0](LICENSE) — skills are free to use with attribution. Source book is copyrighted by Allan Dib.
