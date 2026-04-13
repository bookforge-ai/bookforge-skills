# Channel Comparison Spreadsheet Template

The universal CAC/LTV spreadsheet. Every channel tested should appear as a row.

## Minimum Columns

```csv
channel,test_spend,conversions,CAC,estimated_LTV,LTV_CAC_ratio,volume_available,quality_score,time_to_acquire_days,status,notes
```

## Definitions

- **channel** — Specific channel AND tactic (e.g., "SEM - category keywords" not just "SEM")
- **test_spend** — Total dollars spent during the validation test
- **conversions** — Customers acquired in the test (definition must match your product's conversion event)
- **CAC** — test_spend ÷ conversions
- **estimated_LTV** — rough lifetime value per customer (monthly price × average retention months)
- **LTV_CAC_ratio** — Rule of thumb: healthy channel has LTV:CAC of 3:1 or better
- **volume_available** — realistic ceiling of customers per month the channel can produce at CAC
- **quality_score** — 1-5 subjective rating of customer fit (do they stick, do they match ICP)
- **time_to_acquire_days** — days from first touch to conversion
- **status** — one of: testing / validated / optimizing / saturating / abandoned
- **notes** — any relevant context (saturation signals, test learnings, etc.)

## Example

```csv
SEM - category keywords,$487,9,$54,$1188,22:1,2000/mo,4,3,validated,good signal - scale next
Facebook Ads - lookalike,$500,2,$250,$1188,4.8:1,5000/mo,2,7,abandoned,quality low, churn 60d
Sponsored blog - industry niche,$400,31,$13,$1188,91:1,150/mo,5,1,optimizing,volume ceiling low
```

## Why This Shape

The book's central channel-comparison insight: CAC and LTV are the minimum columns needed to compare channels. Everything else is helpful context. If CAC is above LTV, the channel can't work. If CAC is below LTV, it can work — and then the question becomes volume.

## Source

Chapter 4 ("Traction Testing") of *Traction* by Gabriel Weinberg and Justin Mares.
