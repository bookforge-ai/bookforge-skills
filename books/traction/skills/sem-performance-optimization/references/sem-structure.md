# SEM Ad Group Structure Patterns

## Tight Ad Groups

Each ad group contains 5-10 closely related keywords. One ad template per group. One landing page per group.

**Example — tight:**
Ad group: "project management construction"
Keywords: project management software construction, construction project management tool, project management app for contractors, pm software construction company, construction pm software
Ad copy: Headline uses Dynamic Keyword Insertion → "{Keyword: Construction PM Software} Built For Contractors"
Landing page: /construction-project-management

## Broad Ad Groups (AVOID)

One ad group contains 50+ loosely related keywords. Generic ad copy. Generic landing page.

**Example — broad:**
Ad group: "project management"
Keywords: project management, pm software, project tools, manage projects, project planning, task tracker, etc.
Ad copy: "Manage Your Projects Better"
Landing page: /

**Why broad fails:** Relevance is low → Quality Score is low → CPC is high → CTR is low → doom loop.

## Dynamic Keyword Insertion (DKI)

Syntax: `{Keyword:Default Text}` in ad copy inserts the user's actual query (if it fits) or the default text.

**Example:**
- Ad headline: "{Keyword:Project Software} Built For Teams"
- User searches "construction project software" → Headline becomes "Construction Project Software Built For Teams"
- User searches "too long a query" → Headline falls back to "Project Software Built For Teams"

**When to use:** Tight ad groups where the keywords share a natural headline template.
**When to avoid:** Broad ad groups where DKI produces awkward headlines.

## Recommended Account Structure

```
Account
├── Campaign: Core Category Terms
│   ├── Ad group: [Main category] (5-10 keywords)
│   ├── Ad group: [Main category] - Modifier 1 (5-10)
│   └── Ad group: [Main category] - Modifier 2 (5-10)
├── Campaign: Long-Tail Expansion
│   ├── Ad group: Use case 1 (5-10 keywords)
│   ├── Ad group: Use case 2 (5-10)
│   └── Ad group: Use case 3 (5-10)
└── Campaign: Competitor Terms (if applicable)
    └── Ad group: Alternatives to [competitor]
```

## Keyword Match Types

- **Exact match** `[keyword]` — only exact match
- **Phrase match** `"keyword"` — phrase must appear
- **Broad match modifier** `+keyword +phrase` — all modified words must appear
- **Broad match** `keyword` — loose match, use sparingly

For tight control, default to exact and phrase match. Use broad match only in dedicated "discovery" campaigns where you're looking for new keyword ideas.

## Source

Chapter 8 ("Search Engine Marketing") of *Traction* by Gabriel Weinberg and Justin Mares.
