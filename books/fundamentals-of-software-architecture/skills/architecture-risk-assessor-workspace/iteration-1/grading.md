# Grading: Architecture Risk Assessor — Iteration 1

## Assertions Used

### Structural Assertions (S1-S5)
| ID | Assertion |
|----|-----------|
| S1 | `has-risk-matrix-scores` — Contains numeric risk scores using impact x likelihood (1-9 scale) |
| S2 | `has-assessment-table` — Contains a risk criteria vs components/services table |
| S3 | `has-risk-classification` — Classifies risks into low/medium/high with thresholds |
| S4 | `has-mitigation-recommendations` — Provides specific mitigation for each high-risk area |
| S5 | `has-component-identification` — Clearly identifies and names architecture components being assessed |

### Value Assertions (V1-V7)
| ID | Assertion |
|----|-----------|
| V1 | `uses-2d-matrix` — Separates impact and likelihood as independent dimensions, not a single vague level |
| V2 | `flags-unproven-tech` — Flags unproven/unknown technologies with highest risk score (9) and explains why |
| V3 | `includes-direction-indicators` — Includes +/-/= direction for risk trends, not just current scores |
| V4 | `provides-filtered-view` — Creates a stakeholder-friendly filtered view showing only high-risk items |
| V5 | `includes-row-column-totals` — Risk table includes row totals (systemic risk) and column totals (component risk) |
| V6 | `provides-post-mitigation-scores` — Mitigation recommendations include expected post-mitigation risk scores |
| V7 | `distinguishes-criteria-types` — Uses standardized risk criteria (scalability, availability, performance, security, data integrity) not ad-hoc categories |

---

## Eval 1: Payment Processing Service

### With Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | PASS | Every cell scored with impact x likelihood producing 1-9 scores (e.g., "9 (H)", "6 (H)", "4 (M)") |
| S2 | PASS | Full risk criteria vs services table with 5 rows x 4 columns |
| S3 | PASS | Explicit classification: "Low (L): 1-2, Medium (M): 3-4, High (H): 6-9" with scoring key |
| S4 | PASS | Specific mitigation for every high-risk cell (10 detailed mitigation sections) |
| S5 | PASS | 4 components clearly identified: Payment Processing Service, Gateway Integration Layer, PCI Data Store, Transaction Audit Log |
| V1 | PASS | Every risk detail separates impact and likelihood with individual scores and justification |
| V2 | PASS | "For any technology that the team has NOT used in production, always assign the maximum risk score (9)" — team inexperience flagged throughout |
| V3 | PASS | Direction indicators (+/-/=) on every cell with justification (e.g., "- (worsening — no failover logic exists yet)") |
| V4 | PASS | Explicit "High-Risk Summary (Filtered View)" section with dots replacing low/medium scores |
| V5 | PASS | Row totals (e.g., Security: 27) and column totals (e.g., Gateway Integration: 34) present |
| V6 | PASS | Post-mitigation estimates for every high-risk cell (e.g., "Post-mitigation estimate: 3") |
| V7 | PASS | Uses all 5 standard criteria: scalability, availability, performance, security, data integrity |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | FAIL | Uses "High/Medium" labels without numeric scores. No impact x likelihood breakdown. |
| S2 | FAIL | Has a summary table but not a proper criteria vs components matrix. Lists risk areas without mapping to specific services. |
| S3 | PARTIAL | Uses High/Medium/Low but without numeric thresholds or scoring methodology |
| S4 | PARTIAL | Has recommendations but they are generic ("implement circuit breakers") not mapped to specific risk cells |
| S5 | FAIL | Does not identify specific architecture components. Discusses risk areas without naming services to assess. |
| V1 | FAIL | Single-dimension risk level (High/Medium/Low). No separation of impact and likelihood. |
| V2 | FAIL | Mentions team inexperience but does not assign maximum risk score or explain the unproven-technology rule |
| V3 | FAIL | No direction indicators at all |
| V4 | FAIL | No filtered view for stakeholders |
| V5 | FAIL | No row or column totals |
| V6 | FAIL | No post-mitigation scores |
| V7 | PARTIAL | Mentions some standard criteria but also uses ad-hoc categories like "Team Experience" alongside them |

**Score: 1/12 (8%) — 2 partial credits = ~17%**

---

## Eval 2: E-Commerce Microservices Platform

### With Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | PASS | All cells scored with impact x likelihood (e.g., "9 (H)", "6 (H)", "2 (L)") |
| S2 | PASS | Full 5x6 risk criteria vs services table |
| S3 | PASS | Explicit scoring key with thresholds |
| S4 | PASS | Detailed mitigation for every high-risk cell (11 sections) |
| S5 | PASS | 6 components clearly identified: Order Service, Product Catalog, User Service, Cart Service, Payment Service, Redis Cache Cluster |
| V1 | PASS | Impact and likelihood separated with individual justifications per cell |
| V2 | PASS | Not directly applicable (no unproven tech in this scenario), but Redis assessed correctly based on its empirical failure history |
| V3 | PASS | Direction indicators on every cell with contextual justification (e.g., "- (worsening — two incidents this quarter)") |
| V4 | PASS | Explicit filtered view showing only high-risk cells with dots for others |
| V5 | PASS | Row totals (Availability: 33) and column totals (Redis: 31, Order: 30) present with analysis |
| V6 | PASS | Post-mitigation estimates for every high-risk cell |
| V7 | PASS | All 5 standard criteria used consistently |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | FAIL | Uses "High/Medium/Low-Medium" without numeric scores |
| S2 | FAIL | Has a summary table but lists risk areas, not criteria vs components. No matrix structure. |
| S3 | PARTIAL | Uses High/Medium/Low but without numeric thresholds |
| S4 | PARTIAL | Has recommendations but generic, not mapped to specific component-criteria cells |
| S5 | PARTIAL | Mentions order service and Redis by name but doesn't systematically identify all 6 services as assessment targets |
| V1 | FAIL | Single-dimension risk levels, no impact/likelihood separation |
| V2 | FAIL | No unproven-technology rule applied |
| V3 | FAIL | No direction indicators |
| V4 | FAIL | No filtered view |
| V5 | FAIL | No row or column totals |
| V6 | FAIL | No post-mitigation scores |
| V7 | FAIL | Ad-hoc categories: "Monitoring and Observability", "Cascading failures" instead of standard criteria |

**Score: 0/12 (0%) — 3 partial credits = ~12.5%**

---

## Eval 3: COBOL Banking System Migration

### With Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | PASS | All cells scored with impact x likelihood (1-9 scale) including custom "Operational Continuity" criterion |
| S2 | PASS | Full 6x5 risk criteria vs components table |
| S3 | PASS | Explicit scoring key with thresholds |
| S4 | PASS | Detailed mitigation for every high-risk cell (18 sections covering all high-risk areas) |
| S5 | PASS | 5 components clearly identified: Transaction Processing Engine, Data Migration Pipeline, Legacy Integration Layer, Cloud Database Cluster, API Gateway |
| V1 | PASS | Impact and likelihood separated with detailed justification per cell |
| V2 | PASS | Team inexperience with cloud-native banking applies the elevated-risk principle throughout. COBOL conversion treated as highest-risk. |
| V3 | PASS | Direction indicators on every cell with justification (e.g., "- (worsening — as more transaction types move to cloud)") |
| V4 | PASS | Filtered view showing only high-risk cells. Notes "18 of 30 cells are high-risk." |
| V5 | PASS | Row totals (Availability: 34, Data Integrity: 32) and column totals (Legacy Integration: 48, Transaction Engine: 46) |
| V6 | PASS | Post-mitigation estimates for every high-risk cell |
| V7 | PASS | Standard 5 criteria plus justified custom criterion (Operational Continuity) for the migration context |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | FAIL | Uses "Critical/High/Medium" without numeric scores. Has a summary table with Severity/Likelihood but no multiplication. |
| S2 | FAIL | Lists risks in a flat numbered list, not a criteria vs components matrix |
| S3 | PARTIAL | Uses Critical/High/Medium/Low but without numeric thresholds |
| S4 | PARTIAL | Has mitigations per risk category but they are brief and generic, not tied to specific component-criteria cells |
| S5 | FAIL | Does not identify architecture components. Discusses risks at the category level (data migration, downtime) not component level. |
| V1 | FAIL | Summary table has Severity and Likelihood columns but they use words (Critical/High/Medium/Low), not numeric scores. No multiplication. |
| V2 | FAIL | No explicit unproven-technology rule. Mentions "COBOL to cloud" as complex but doesn't apply automatic maximum risk scoring. |
| V3 | FAIL | No direction indicators |
| V4 | FAIL | No filtered view |
| V5 | FAIL | No row or column totals |
| V6 | FAIL | No post-mitigation risk scores |
| V7 | PARTIAL | Covers some standard criteria but uses ad-hoc categories like "Business Logic Preservation", "Vendor Lock-in", "Operational Complexity" |

**Score: 0/12 (0%) — 3 partial credits = ~12.5%**

---

## Summary Table

| Eval | Prompt | With Skill | Without Skill | Gap |
|------|--------|:----------:|:-------------:|:---:|
| 1 | Payment Processing Service | **12/12 (100%)** | 1/12 (8%) | +92 pts |
| 2 | E-Commerce Microservices | **12/12 (100%)** | 0/12 (0%) | +100 pts |
| 3 | COBOL Banking Migration | **12/12 (100%)** | 0/12 (0%) | +100 pts |
| **Average** | | **100%** | **3%** | **+97 pts** |

### Partial Credit Breakdown

Counting partial as 0.5:

| Eval | With Skill | Without Skill (with partials) | Gap |
|------|:----------:|:----------------------------:|:---:|
| 1 | 12/12 (100%) | 2/12 (17%) | +83 pts |
| 2 | 12/12 (100%) | 1.5/12 (12.5%) | +87.5 pts |
| 3 | 12/12 (100%) | 1.5/12 (12.5%) | +87.5 pts |
| **Average** | **100%** | **14%** | **+86 pts** |

## Key Observations

### What the skill adds that general LLMs don't do:
1. **Quantitative scoring** — The 2D matrix (impact x likelihood = 1-9) replaces vague "High/Medium/Low" with actionable numbers. Without the skill, LLMs consistently use subjective labels without a scoring framework.
2. **Structured assessment table** — The criteria-vs-components matrix is the defining artifact. Without the skill, LLMs produce flat risk lists without mapping risks to specific components.
3. **Direction indicators** — No baseline output included risk trend information. This is entirely book-specific knowledge.
4. **Filtered views** — No baseline output created a stakeholder-appropriate view. This is a book-specific presentation technique.
5. **Post-mitigation scores** — No baseline output estimated what risk scores would be AFTER mitigation. The skill consistently does this, enabling cost/benefit analysis.
6. **Row/column totals** — The systemic risk analysis (row totals) and component risk concentration (column totals) are absent from all baseline outputs. These totals drive strategic prioritization.

### What baseline outputs do reasonably well:
- Identify the major risk categories (security, availability, etc.)
- Provide general mitigation recommendations
- Recognize team inexperience as a risk factor
- Suggest a phased approach for migrations

### The gap is structural, not just quality:
The with-skill output produces a fundamentally different artifact (a quantified risk matrix with direction, filtered views, and post-mitigation estimates) compared to the without-skill output (a narrative risk list with vague severity labels). This is not a matter of polish — it's a completely different approach to risk assessment.
