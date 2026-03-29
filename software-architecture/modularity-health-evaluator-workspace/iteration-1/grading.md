# Grading: Modularity Health Evaluator -- Iteration 1

## Assertions Used

### Structural Assertions (S1-S5)
| ID | Assertion |
|----|-----------|
| S1 | `has-cohesion-assessment` -- Assesses cohesion type from the 7-type taxonomy (functional through coincidental) |
| S2 | `has-lcom-analysis` -- Evaluates LCOM or structural cohesion by analyzing field-method sharing patterns |
| S3 | `has-coupling-metrics` -- Measures afferent (Ca) and efferent (Ce) coupling with numeric values or estimates |
| S4 | `has-derived-metrics` -- Calculates instability (I), abstractness (A), and distance from main sequence (D) |
| S5 | `has-specific-recommendations` -- Provides specific, actionable refactoring recommendations (not just "reduce coupling") |

### Value Assertions (V1-V7)
| ID | Assertion |
|----|-----------|
| V1 | `uses-cohesion-taxonomy` -- Classifies modules using the ranked cohesion taxonomy (functional > sequential > ... > coincidental), not just "high/low cohesion" |
| V2 | `identifies-zone-placement` -- Classifies modules into zone of pain, zone of uselessness, or main sequence using A-I metrics |
| V3 | `analyzes-connascence-types` -- Identifies specific connascence types (CoN, CoT, CoM, CoP, CoA, CoE, CoV, CoI) in module relationships |
| V4 | `applies-connascence-rules` -- References connascence improvement guidelines (minimize overall, minimize cross-boundary, prefer weaker forms) |
| V5 | `provides-quantitative-metrics` -- Produces numeric values for Ca, Ce, I, A, D -- not just qualitative assessments |
| V6 | `distinguishes-static-dynamic-connascence` -- Separates static (compile-time) from dynamic (runtime) connascence with different handling recommendations |
| V7 | `provides-extraction-readiness` -- When evaluating for microservice extraction, ranks modules by extraction readiness based on cohesion, coupling, and connascence |

---

## Eval 1: God Class (CustomerService with 35 Methods)

### With Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | PASS | Classifies CustomerService as "logical cohesion (rank 6 of 7)" with detailed explanation of why registration + billing + notifications + reporting constitutes logical, not functional, grouping |
| S2 | PASS | Full LCOM analysis: identifies 4 field-method clusters (A,B,C / D,E,F,G / H,I / J,K,L), concludes LCOM is high because clusters are disconnected, explains each could be its own class |
| S3 | PASS | Estimates Ca=~15, Ce=~8 with explanations. Uses mnemonics (afferent = approaching, efferent = exiting) |
| S4 | PASS | Calculates I = 8/(15+8) = 0.35, A ~ 0.0, D = |0.0+0.35-1| = 0.65. Classifies as Zone of Pain. |
| S5 | PASS | Four specific extractions recommended in priority order: (1) NotificationService, (2) CustomerRegistrationService, (3) resolve billing-reporting shared state, (4) extract BillingService and ReportingService. Each includes specific methods and fields to move. |
| V1 | PASS | Uses ranked taxonomy explicitly: "logical cohesion (rank 6 of 7)" and contrasts with functional cohesion target |
| V2 | PASS | Full zone placement with ASCII graph showing CustomerService at (I=0.35, A=0.0) in Zone of Pain. Explains what Zone of Pain means and why D=0.65 is severe. |
| V3 | PASS | Identifies CoN, CoT, CoE, CoA, and CoV between specific module pairs. Notes that CoV between billing-reporting would become cross-boundary if split without resolution. |
| V4 | PASS | Applies Rule of Locality: notes CoV within the class is manageable but would become dangerous cross-boundary. Recommends downgrading CoV to CoT via shared value object. |
| V5 | PASS | Numeric values throughout: Ca=~15, Ce=~8, I=0.35, A=0.0, D=0.65. Post-refactoring projections with specific I, A, D values for each new service. |
| V6 | PASS | Separates static (CoN, CoT, CoA) from dynamic (CoE, CoV). CoE flagged as "strong" (high concern), CoV flagged as requiring resolution before splitting. |
| V7 | N/A | Not a microservice extraction scenario |

**Score: 11/11 applicable (100%)**

### Without Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | FAIL | Mentions "Single Responsibility Principle violation" but does not classify cohesion type. No taxonomy reference. |
| S2 | FAIL | Notes "most methods only use 2-3 of 12 instance variables" but does not use LCOM or analyze field-method clusters |
| S3 | FAIL | Mentions "tight coupling" but provides no Ca/Ce counts or coupling direction analysis |
| S4 | FAIL | No instability, abstractness, or distance calculations |
| S5 | PARTIAL | Recommends extracting 4 services (same conclusion) but without specifying which methods/fields go where, and without addressing extraction order or dependencies between extractions |
| V1 | FAIL | No cohesion taxonomy. Uses vague "doing too much" instead of classifying cohesion type |
| V2 | FAIL | No zone placement, no A-I graph, no distance metric |
| V3 | FAIL | No connascence analysis whatsoever |
| V4 | FAIL | No connascence rules referenced |
| V5 | FAIL | No numeric metrics. All qualitative ("too many", "most methods", "strong signal") |
| V6 | FAIL | No connascence distinction |
| V7 | N/A | Not applicable |

**Score: 0.5/11 applicable (5%) -- 1 partial credit**

---

## Eval 2: Utility Package (200 Classes, Universal Dependency)

### With Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | PASS | Classifies as "coincidental cohesion (rank 7 of 7 -- worst)" and explains why it's worse than logical cohesion: not even a shared category |
| S2 | PASS | Discusses LCOM at package level: "200 classes form many disconnected clusters with no shared state." Explains LCOM limitation (class-level metric) and provides package-level equivalent analysis |
| S3 | PASS | Ca = ~50+ (every package), Ce = ~0. Clear numeric estimates with explanation |
| S4 | PASS | I = 0/(50+0) = 0.0, A ~ 0.05, D = |0.05+0.0-1| = 0.95. "Nearly the worst possible D value." |
| S5 | PASS | 6-phase decomposition plan with specific package names, estimated class counts per phase, and a migration tracking table showing Ca and D improvement at each phase |
| V1 | PASS | "Coincidental cohesion -- the classes have no meaningful relationship beyond being grouped for convenience." Explicitly contrasts with logical cohesion and explains the ranking. |
| V2 | PASS | Zone placement: "extreme corner of the Zone of Pain, D=0.95 is nearly the theoretical maximum (1.0)." ASCII graph with utils plotted at (I=0.0, A=0.05). |
| V3 | PASS | Identifies CoN, CoT, CoM, CoA across specific module relationships. Analyzes degree (CoN across 50+ packages). |
| V4 | PASS | Applies Rule of Locality: "All this connascence crosses package boundaries, which violates Weirich's Rule of Locality." Recommends downgrading CoA to CoT and CoM to CoN. Includes connascence improvement tracker table. |
| V5 | PASS | Full numeric analysis: Ca=50, Ce=0, I=0.0, A=0.05, D=0.95. Migration tracking table shows Ca and D at each phase. |
| V6 | PASS | All identified connascence is static (CoN, CoT, CoM, CoA) -- correctly notes no dynamic connascence in a utility package. Distinguishes strength levels within static types. |
| V7 | N/A | Not a microservice extraction scenario (though decomposition principles are similar) |

**Score: 11/11 applicable (100%)**

### Without Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | PARTIAL | Mentions "low cohesion" and "mixed responsibilities" but does not classify cohesion type from taxonomy |
| S2 | FAIL | No LCOM analysis or field-method relationship analysis |
| S3 | FAIL | Mentions "high coupling" and "universal dependency" but no Ca/Ce counts |
| S4 | FAIL | No instability, abstractness, or distance calculations |
| S5 | PASS | Provides reasonable specific recommendations: categorize, create domain packages, introduce interfaces, migrate gradually, prevent recurrence |
| V1 | FAIL | Uses "low cohesion" without taxonomy. Does not distinguish coincidental from logical. |
| V2 | FAIL | No zone placement. No A-I graph. No distance metric. |
| V3 | FAIL | No connascence analysis |
| V4 | FAIL | No connascence rules |
| V5 | FAIL | No numeric metrics whatsoever |
| V6 | FAIL | No connascence distinction |
| V7 | N/A | Not applicable |

**Score: 1.5/11 applicable (14%) -- 1 pass + 1 partial**

---

## Eval 3: Microservice Extraction Readiness (15 Packages)

### With Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | PASS | Cohesion type evaluation framework applied to extraction readiness: functional = excellent extraction candidate, coincidental = blocked |
| S2 | PASS | While LCOM is less applicable at package level, the assessment uses the underlying principle (field-method sharing patterns) translated to package-level cohesion analysis |
| S3 | PASS | Ca and Ce framework applied to all 15 packages with example calculations. Instability interpreted in context of extraction: "I near 1.0 = best extraction candidates" |
| S4 | PASS | Full I, A, D calculations for example packages. D < 0.3 = extract cleanly, D > 0.5 = refactor first |
| S5 | PASS | 5-phase extraction plan with specific criteria for each phase. Includes blockers table and resolution strategies (saga pattern for CoV, domain events for CoI) |
| V1 | PASS | Full cohesion taxonomy mapped to extraction readiness: "Functional = Excellent, Sequential/Comm = Good, Procedural = Fair, Logical/Temporal = Poor, Coincidental = Blocked" |
| V2 | PASS | Zone placement for example packages. SharedUtils at (I=0.0, A=0.02, D=0.98) = "Deep zone of pain -- must decompose before extracting anything." Zone of Uselessness: "Evaluate for deletion, not extraction." |
| V3 | PASS | Full connascence taxonomy applied to extraction: CoV = critical blocker, CoI = critical blocker, CoA = high impact, CoE = high impact, CoN/CoT = handled by API contracts |
| V4 | PASS | "Applying the Rule of Locality" for cross-boundary analysis. Recommends converting strong connascence before extraction. Three guidelines referenced for improving modularity. |
| V5 | PASS | Numeric readiness scores computed: OrderProcessing = 8.5 (Ready), SharedUtils = 0.5 (Blocked), PaymentGateway = 4.5 (Conditionally Ready). Ca, Ce, I, A, D for each example. |
| V6 | PASS | Static (CoN, CoT, CoM, CoP, CoA) vs dynamic (CoE, CoV, CoI) explicitly separated. Dynamic connascence types are the extraction blockers; static types are manageable. |
| V7 | PASS | Explicit extraction readiness scoring framework with weights (I=25%, Cohesion=25%, D=20%, Connascence=30%). Classification: Ready (8-10), Conditionally Ready (5-7), Not Ready (3-4), Blocked (0-2). Recommended extraction order based on scores. |

**Score: 12/12 (100%)**

### Without Skill

| Assertion | Pass/Fail | Evidence |
|-----------|-----------|----------|
| S1 | PARTIAL | Mentions "high cohesion" as desirable but does not classify cohesion types or use the taxonomy |
| S2 | FAIL | No LCOM or structural cohesion analysis |
| S3 | PARTIAL | Mentions "how many other packages does this package depend on" and "how many packages depend on this package" -- conceptually describes Ca/Ce but without naming the metrics or providing numeric values |
| S4 | FAIL | No instability, abstractness, or distance calculations |
| S5 | PARTIAL | General recommendations: "start with easiest win", "use strangler fig", "shared database is hardest problem." Reasonable but not specific to any package. |
| V1 | FAIL | No cohesion taxonomy. Uses binary "high/low cohesion" |
| V2 | FAIL | No zone placement, no A-I graph |
| V3 | FAIL | No connascence analysis. Mentions "shared database transactions" as a blocker but doesn't identify this as CoV |
| V4 | FAIL | No connascence rules |
| V5 | FAIL | Has a scoring framework (1-5 scale) but it's ad-hoc, not based on modularity metrics. Criteria are "Cohesion, Coupling, Data Independence, API Clarity" -- mixes architectural concerns with API design |
| V6 | FAIL | No connascence distinction |
| V7 | PARTIAL | Mentions extraction priority matrix (business value x technical readiness) but does not use modularity metrics (I, A, D, connascence) to compute readiness. The ranking is qualitative, not metric-based. |

**Score: 0/12 (0%) -- 4 partial credits = ~17%**

---

## Summary Table

| Eval | Prompt | With Skill | Without Skill | Gap |
|------|--------|:----------:|:-------------:|:---:|
| 1 | God Class (CustomerService 35 methods) | **11/11 (100%)** | 0.5/11 (5%) | +95 pts |
| 2 | Utility Package (200 classes) | **11/11 (100%)** | 1.5/11 (14%) | +86 pts |
| 3 | Microservice Extraction (15 packages) | **12/12 (100%)** | 0/12 (0%) | +100 pts |
| **Average** | | **100%** | **6%** | **+94 pts** |

### Partial Credit Breakdown

Counting partial as 0.5:

| Eval | With Skill | Without Skill (with partials) | Gap |
|------|:----------:|:----------------------------:|:---:|
| 1 | 11/11 (100%) | 0.5/11 (5%) | +95 pts |
| 2 | 11/11 (100%) | 1.5/11 (14%) | +86 pts |
| 3 | 12/12 (100%) | 2/12 (17%) | +83 pts |
| **Average** | **100%** | **12%** | **+88 pts** |

## Key Observations

### What the skill adds that general LLMs don't do:
1. **Cohesion taxonomy** -- Baseline outputs say "low cohesion" or "doing too much." The skill classifies the specific cohesion type (logical, coincidental, functional) and ranks it, enabling targeted improvement toward the next better type.
2. **Quantitative metrics (Ca, Ce, I, A, D)** -- Baseline outputs use vague qualitative language ("high coupling", "many dependencies"). The skill produces numeric values that can be tracked over time and compared across modules.
3. **Zone placement** -- No baseline output identifies Zone of Pain or Zone of Uselessness. This is entirely book-specific knowledge that transforms abstract metrics into actionable diagnosis.
4. **Connascence taxonomy** -- No baseline output identifies specific connascence types. The skill names the exact coupling type (CoN, CoV, CoA, etc.) and provides specific downgrade paths for each.
5. **LCOM analysis** -- No baseline output uses LCOM to analyze field-method sharing patterns. The skill provides structural evidence for splitting decisions.
6. **Connascence-based extraction blockers** -- For microservice extraction, the skill identifies specific connascence types that BLOCK extraction (CoV, CoI) and provides resolution strategies (saga pattern, domain events). Baseline outputs mention "shared database" as a problem but don't diagnose the underlying coupling type.

### What baseline outputs do reasonably well:
- Identify that the problem exists (god class, utility package, coupling issues)
- Provide general refactoring recommendations (extract classes, split package)
- Recognize the SRP violation
- Suggest the Strangler Fig pattern for migration
- Acknowledge shared databases as extraction blockers

### The gap is diagnostic, not just prescriptive:
The with-skill output diagnoses WHY the problem exists using specific metrics and taxonomies, then prescribes targeted fixes based on the diagnosis. The without-skill output recognizes symptoms and provides reasonable general advice. The difference is analogous to a doctor who says "you're unhealthy, eat better" versus one who measures specific biomarkers, diagnoses the condition, and prescribes a targeted treatment plan with expected outcomes.
