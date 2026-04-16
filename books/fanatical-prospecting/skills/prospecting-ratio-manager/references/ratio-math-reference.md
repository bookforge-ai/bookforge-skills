# Ratio Math Reference

Supporting reference for `prospecting-ratio-manager` — full worked examples at variable close rates and the complete formula chain from quota to daily dials.

---

## Pipeline Replacement Rate Table

| Close Rate | Replacement Rate | Monthly adds per 1 close target | Monthly adds per 3 close target | Monthly adds per 5 close target |
|-----------|-----------------|--------------------------------|--------------------------------|--------------------------------|
| 5%        | 20              | 20                             | 60                             | 100                            |
| 10%       | 10              | 10                             | 30                             | 50                             |
| 15%       | 6.7             | 7                              | 20                             | 33                             |
| 20%       | 5               | 5                              | 15                             | 25                             |
| 25%       | 4               | 4                              | 12                             | 20                             |
| 33%       | 3               | 3                              | 9                              | 15                             |

**Key insight:** A rep with a 5% close rate who must close 3 deals per month needs to add 60 new qualified prospects per month — just to keep the pipeline static. That is 14 per week, or 2.8 per day on a 5-day week.

---

## Becky's Math (Law of Replacement Proof)

*Source: Blount, Fanatical Prospecting, Chapter 5*

Becky has 30 prospects in her pipeline. Her close rate is 10%. She closes 1 deal.

**Common (wrong) answer:** 29 prospects remain.

**Correct answer:** 20 prospects remain.

**Why:** Becky's 10% close rate means she closes 1 out of every 10 prospects she works. When she closes 1 deal, the statistical cohort that deal came from contained 10 prospects. The other 9 are not viable — they either lost interest, went with a competitor, were disqualified, or stalled indefinitely. They are consuming pipeline real estate without advancing.

Net effect: 30 − 10 = 20 remaining viable prospects.

This is a statistical argument. In any single cohort, some of those 9 might surprise you. Over time, however, your close rate predicts that you will close 1 in 10, and the rest will fall away. Planning pipeline health based on the optimistic "29 remain" view guarantees a future shortage.

---

## Full Formula Chain: Quota to Daily Dials

Worked example: SDR, $300k ARR annual quota, $50k average deal.

```
Step 1 — Deals needed per year
  $300,000 ARR / $50,000 avg deal = 6 deals/year

Step 2 — Deals needed per month
  6 / 12 = 0.5 deals/month
  (rounds to 1 deal every 2 months in practice)

Step 3 — New prospects needed per month (at 10% close rate)
  0.5 × 10 = 5 new prospects/month

Step 4 — New prospects needed per week
  5 / 4.3 = 1.2 new prospects/week

Step 5 — Conversations needed per week
  Assume meeting-set rate = 15% (1 meeting per 6.7 conversations)
  1.2 / 0.15 = 8 conversations/week = 1.6/day

Step 6 — Dials needed per day
  Assume connect rate = 12% (1 conversation per 8.3 dials)
  1.6 / 0.12 = 13.3 → ~14 dials/day minimum
```

**For a higher-volume SDR role** (monthly quota: 20 meetings set, not deals closed):

```
Meetings needed per month:  20
At 15% set rate:            20 / 0.15 = 133 conversations/month
At 12% connect rate:        133 / 0.12 = 1,108 dials/month = ~53 dials/day
```

This is close to Blount's "50 dials/day" benchmark for a standard phone-heavy SDR role.

---

## Efficiency + Effectiveness = Performance (E+E=P)

*Source: Blount, Fanatical Prospecting, Chapter 6*

**Efficiency** = Activity volume per time block (dials per hour)
**Effectiveness** = Ratio of activity to meaningful outcome (conversations per dial; meetings per conversation)

Both matter. The failure modes are symmetric:

| Scenario | Efficiency | Effectiveness | Result |
|----------|-----------|---------------|--------|
| 100 dials/hour, 0 appointments | High | Low | Wasted time — activity without outcome |
| 10 calls/hour, 1 high-quality appointment | Low | High | Suboptimized — better outcomes per call but pipeline fills too slowly |
| 50 dials/hour, 2 solid appointments | Balanced | Balanced | Target state |

The rep who made 12 calls "all day" had a dual failure: low efficiency (12 dials in 7 hours = 1.7/hour) AND low effectiveness (no appointments from 12 dials). Tracking both metrics separately pinpoints which variable to fix.

---

## Hourly Worth Calculation

*Source: Blount, Fanatical Prospecting, Chapter 8 (Time Equalizer)*

```
Worth per Hour = Annual Income Goal / (Working Weeks × Golden Hours per Week)

Example:
  $75,000 goal / (48 weeks × 30 hours/week) = $52/hour

Use case: If a task can be delegated, deferred, or batched into Platinum Hours
(before/after prime selling time) and it pays less than $52/hour in value,
executing it during Golden Hours costs the difference.

Example: Spending 3 hours on CRM data entry at $10/hour effective value
during $52/hour selling time costs $126 in opportunity, for a $30 task.
```

---

## 30-Day Rule Severity Thresholds

| Gap in prospecting activity | Expected consequence | Time to impact |
|---------------------------|---------------------|----------------|
| Miss 1 day | Minor dip, recoverable in days | ~90 days |
| Miss 1 week | Noticeable pipeline thinning | ~60-90 days |
| Miss 1 full month | Pipeline drains, slump likely | ~90 days |
| Miss 2+ months | Severe slump, desperation territory | ~90-120 days |

**Recovery benchmark:** ~30 days of consistent daily prospecting to begin pipeline recovery from a full-month gap. Results are not immediate — the 30-Day Rule applies to recovery too.

---

## Connect Rate and Meeting-Set Rate Benchmarks

These vary significantly by industry, list quality, channel, and rep experience. Use actual data whenever possible. Defaults for cold phone outreach (B2B):

| Metric | Low | Typical | High |
|--------|-----|---------|------|
| Connect rate (conversations per dial) | 6-8% | 10-14% | 18-22% |
| Meeting-set rate (meetings per conversation) | 8-12% | 15-20% | 25-35% |
| Show rate (meetings attended / set) | 60-70% | 75-85% | 90%+ |

**SDR benchmark from Blount:** 29 dials in 30 minutes → 2 appointments = ~3.5% direct-to-appointment rate (not all dials become conversations). Implies efficiency of ~58 dials/hour with solid effectiveness.
