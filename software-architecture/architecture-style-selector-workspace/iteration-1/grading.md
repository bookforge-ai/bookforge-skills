# Architecture Style Selector — Grading Results (Iteration 1)

**Date:** 2026-03-27
**Assertions:** 12 (5 structural + 7 value)
**Files graded:** 6 (3 eval scenarios x with/without skill)

---

## File 1: eval-1/with_skill

**Scenario:** Real-Time Collaborative Document Editor

```json
{
  "file": "eval-1/with_skill",
  "assertions": [
    {"id": "evaluates-monolith-vs-distributed", "passed": true, "evidence": "Explicit 'Decision: Distributed' with reasoning about multiple quanta and characteristic mismatches with monolithic styles (scores cited: layered 2/1, pipeline 2/1, microkernel 3/1)."},
    {"id": "compares-multiple-styles", "passed": true, "evidence": "Evaluates 4 distributed styles: Service-Based, Event-Driven, Space-Based, Microservices — each with pros/cons."},
    {"id": "produces-scored-comparison", "passed": true, "evidence": "Candidate Evaluation table with X/5 ratings per criterion (e.g., Event-Driven: Performance 5/5, Scalability 5/5, Fault tolerance 5/5) plus totals and adjusted scores."},
    {"id": "has-recommendation", "passed": true, "evidence": "Selected style: Event-Driven Architecture (hybrid with Service-Based structure)"},
    {"id": "documents-trade-offs", "passed": true, "evidence": "Explicit 'Trade-offs accepted' (lower simplicity 1, testability 2, higher cost, learning curve) and 'Trade-offs rejected' naming Service-based (pure), Space-based, and Microservices with specific reasons."},
    {"id": "uses-star-ratings", "passed": true, "evidence": "1-5 numeric ratings throughout: Performance 5/5, Scalability 5/5, Fault tolerance 5/5 for Event-Driven; 3/5, 3/5, 4/5 for Service-Based; etc."},
    {"id": "checks-quantum-count", "passed": true, "evidence": "Identifies 4 quanta with different characteristic profiles: real-time sync engine, document storage/versioning, offline sync/conflict resolution, user/auth/permissions. States 'confirming multiple quanta'."},
    {"id": "checks-domain-isomorphism", "passed": true, "evidence": "'Domain isomorphism: Yes/No/Partial' in evaluation table. States 'the domain is inherently event-driven: every user action is an event... This is textbook domain/architecture isomorphism.'"},
    {"id": "checks-organizational-fit", "passed": true, "evidence": "Step 3: Organizational Fit table evaluates team size (12), no distributed experience (critical constraint), moderate budget — each with impact on style selection."},
    {"id": "considers-service-based", "passed": true, "evidence": "Service-Based evaluated as standalone candidate and forms the backbone of the hybrid recommendation ('service-based backbone with event-driven communication')."},
    {"id": "warns-anti-patterns", "passed": true, "evidence": "Step 4: Anti-Pattern Check names 4 specific anti-patterns: Distributed monolith, Broker/mediator mismatch, Too-fine-grained services, Transactions across boundaries — each with risk level and mitigation."},
    {"id": "respects-coupling", "passed": false, "evidence": "No explicit evaluation of domain coupling level. Does not assess whether domain coupling is high or low, nor flag potential coupling mismatches with the chosen architecture."}
  ],
  "pass_count": 11,
  "total": 12
}
```

---

## File 2: eval-1/without_skill

**Scenario:** Real-Time Collaborative Document Editor

```json
{
  "file": "eval-1/without_skill",
  "assertions": [
    {"id": "evaluates-monolith-vs-distributed", "passed": false, "evidence": "No explicit monolith vs distributed binary decision. Jumps directly to evaluating 6 styles (including monolithic) without framing the structural decision as a gate."},
    {"id": "compares-multiple-styles", "passed": true, "evidence": "Evaluates 6 styles: Monolithic, Microservices, Event-Driven, Space-Based, Service-Based, Peer-to-Peer — each with pros/cons and rating."},
    {"id": "produces-scored-comparison", "passed": true, "evidence": "X/10 ratings per style: Monolithic 4/10, Microservices 3/10, Event-Driven 8/10, Space-Based 5/10, Service-Based 7/10, P2P 5/10."},
    {"id": "has-recommendation", "passed": true, "evidence": "Primary Style: Service-Based Architecture + Event-Driven Communication"},
    {"id": "documents-trade-offs", "passed": true, "evidence": "Section 8 'Alternatives Considered but Rejected' covers Firebase, ShareDB, Pure P2P with specific rejection reasoning. Section 6 has risk analysis table."},
    {"id": "uses-star-ratings", "passed": true, "evidence": "Numeric X/10 ratings for each style (4/10, 3/10, 8/10, 5/10, 7/10, 5/10)."},
    {"id": "checks-quantum-count", "passed": false, "evidence": "No mention of 'quantum' or equivalent concept. Does not analyze whether different system parts need fundamentally different characteristics as a structural decision driver."},
    {"id": "checks-domain-isomorphism", "passed": false, "evidence": "No explicit discussion of domain-to-architecture topology mapping. Mentions the domain is 'inherently event-driven' but does not frame this as an isomorphism evaluation."},
    {"id": "checks-organizational-fit", "passed": true, "evidence": "Team size (12), no distributed systems background, and moderate budget cited as factors. Section 5.2 explicitly discusses 'Service-Based over Microservices' due to team constraints."},
    {"id": "considers-service-based", "passed": true, "evidence": "Service-Based explicitly evaluated (rated 7/10) and forms the backbone of the final hybrid recommendation."},
    {"id": "warns-anti-patterns", "passed": false, "evidence": "No specific architecture anti-patterns named (no 'sinkhole', 'distributed monolith', 'broker/mediator mismatch', etc.). Risk table covers operational risks but not style-specific anti-patterns."},
    {"id": "respects-coupling", "passed": false, "evidence": "No evaluation of domain coupling level or coupling mismatch analysis."}
  ],
  "pass_count": 7,
  "total": 12
}
```

---

## File 3: eval-2/with_skill

**Scenario:** FreelanceInvoice SaaS

```json
{
  "file": "eval-2/with_skill",
  "assertions": [
    {"id": "evaluates-monolith-vs-distributed", "passed": true, "evidence": "Explicit 'Decision: Monolith' with detailed reasoning: single quantum, solo developer, $50/month budget, 3-month timeline."},
    {"id": "compares-multiple-styles", "passed": true, "evidence": "Evaluates 3 monolithic styles: Layered, Microkernel, Pipeline — plus distributed styles explicitly rejected."},
    {"id": "produces-scored-comparison", "passed": true, "evidence": "Candidate Evaluation table with X/5 ratings: Layered (5/5, 5/5, 1/5 = 11), Microkernel (4/5, 5/5, 3/5 = 12), Pipeline (5/5, 5/5, 2/5 = 12)."},
    {"id": "has-recommendation", "passed": true, "evidence": "Selected style: Layered Architecture"},
    {"id": "documents-trade-offs", "passed": true, "evidence": "Trade-offs accepted: Scalability 1/5, Elasticity 1/5, Deployability 1/5. Trade-offs rejected: Microservices, Service-based, Event-driven, Microkernel — each with specific reasoning."},
    {"id": "uses-star-ratings", "passed": true, "evidence": "1-5 numeric ratings: Simplicity 5/5, Cost 5/5, Deployability 1/5 for Layered; etc."},
    {"id": "checks-quantum-count", "passed": true, "evidence": "'Architecture quanta: 1 — all components share the same quality attribute needs. No part of the system requires a fundamentally different scalability, availability, or performance profile.'"},
    {"id": "checks-domain-isomorphism", "passed": true, "evidence": "'Domain isomorphism: Yes/No/No' in table. 'Your invoicing domain is a textbook fit for layered architecture.' Pipeline eliminated because 'An invoicing system is not a linear data transformation pipeline... Pipeline has no domain isomorphism here.'"},
    {"id": "checks-organizational-fit", "passed": true, "evidence": "Solo developer, $50/month budget, 3-month timeline extensively used as selection criteria. 'team size <10 means avoid microservices. A team of 1 makes this even more definitive.'"},
    {"id": "considers-service-based", "passed": true, "evidence": "Service-based explicitly addressed in trade-offs rejected: 'Adds distribution complexity that provides no benefit for a single-quantum system with one developer.'"},
    {"id": "warns-anti-patterns", "passed": true, "evidence": "'Sinkhole (low risk at this scale)' named in anti-pattern risk row of evaluation table."},
    {"id": "respects-coupling", "passed": true, "evidence": "'All components share the same quality attribute needs' and 'tightly related features of a single invoicing workflow' — explicitly recognizes high coupling and uses it to argue against distributed styles."}
  ],
  "pass_count": 12,
  "total": 12
}
```

---

## File 4: eval-2/without_skill

**Scenario:** FreelanceInvoice SaaS

```json
{
  "file": "eval-2/without_skill",
  "assertions": [
    {"id": "evaluates-monolith-vs-distributed", "passed": true, "evidence": "'Do not use microservices. A modular monolith is the right architecture' — makes explicit monolith determination with 5 supporting reasons."},
    {"id": "compares-multiple-styles", "passed": false, "evidence": "Only evaluates microservices (rejected) vs modular monolith (recommended). Does not compare monolithic sub-styles (layered, microkernel, pipeline). The recommendation is 'modular monolith' without evaluating alternatives within the monolithic family."},
    {"id": "produces-scored-comparison", "passed": false, "evidence": "No numeric comparison table of candidates. Architecture characteristics table uses qualitative terms ('Excellent', 'Good', 'Adequate', 'Not needed') rather than scored ratings comparing candidates."},
    {"id": "has-recommendation", "passed": true, "evidence": "Clear recommendation: 'Modular Monolith'"},
    {"id": "documents-trade-offs", "passed": true, "evidence": "'When to Reconsider' section documents 4 conditions that would invalidate the choice. 'Biggest risk to avoid' names 'big ball of mud monolith'. Migration path section shows accepted limitations."},
    {"id": "uses-star-ratings", "passed": false, "evidence": "No numeric 1-5 or equivalent ratings. All evaluations use qualitative terms: 'Excellent', 'Good', 'Adequate', 'Not needed'."},
    {"id": "checks-quantum-count", "passed": false, "evidence": "No mention of quantum or equivalent analysis. Does not structurally analyze whether system parts have different characteristic needs."},
    {"id": "checks-domain-isomorphism", "passed": false, "evidence": "No discussion of how the domain's shape maps to the architecture's topology. Does not evaluate isomorphism."},
    {"id": "checks-organizational-fit", "passed": true, "evidence": "Solo developer, $50/month budget, 3-month timeline, early-stage scale — all extensively discussed as primary decision factors."},
    {"id": "considers-service-based", "passed": false, "evidence": "Service-based architecture is never mentioned or evaluated as an option."},
    {"id": "warns-anti-patterns", "passed": true, "evidence": "'Big ball of mud' anti-pattern named: 'Biggest risk to avoid? A big ball of mud monolith with no internal structure.'"},
    {"id": "respects-coupling", "passed": false, "evidence": "No explicit evaluation of domain coupling level or coupling mismatch analysis."}
  ],
  "pass_count": 5,
  "total": 12
}
```

---

## File 5: eval-3/with_skill

**Scenario:** E-Commerce Platform (monolith migration)

```json
{
  "file": "eval-3/with_skill",
  "assertions": [
    {"id": "evaluates-monolith-vs-distributed", "passed": true, "evidence": "Explicit 'Decision: Distributed' with reasoning: multiple quanta, payment cascading failures, 35 devs/4 teams, 4-hour deployment bottleneck."},
    {"id": "compares-multiple-styles", "passed": true, "evidence": "Evaluates 4 distributed styles: Service-Based, Event-Driven, Microservices, Space-Based — each with scored ratings and organizational fit."},
    {"id": "produces-scored-comparison", "passed": true, "evidence": "Two comparison tables: raw characteristic scores (Service-Based 11, Event-Driven 13, Microservices 13) and adjusted scores with organizational modifiers (Service-Based 12, Event-Driven 11, Microservices 10)."},
    {"id": "has-recommendation", "passed": true, "evidence": "Selected style: Service-Based Architecture"},
    {"id": "documents-trade-offs", "passed": true, "evidence": "Trade-offs accepted: Scalability 3/5, Elasticity 2/5, evolutionary flexibility 3/5. Trade-offs rejected: Event-Driven (org fit penalty), Microservices (immature DevOps), Space-Based (over-engineering)."},
    {"id": "uses-star-ratings", "passed": true, "evidence": "1-5 numeric ratings: Fault tolerance 4/5, 5/5, 4/5; Deployability 4/5, 3/5, 4/5; Scalability 3/5, 5/5, 5/5 across three styles."},
    {"id": "checks-quantum-count", "passed": true, "evidence": "'Architecture quanta: Multiple quanta. The payment module has fundamentally different quality attribute needs (high fault tolerance, high elasticity during flash sales) than the core catalog/browsing experience.'"},
    {"id": "checks-domain-isomorphism", "passed": true, "evidence": "'Domain isomorphism: Yes/No/Partial' in evaluation table. Isomorphism bonus of +1 applied to Service-Based in adjusted scoring."},
    {"id": "checks-organizational-fit", "passed": true, "evidence": "Detailed organizational fit section: 35 devs/4 teams mapped to services, no distributed tracing, basic CI/CD, no distributed experience. Organizational modifiers applied: Service-Based 0, Event-Driven -2, Microservices -3."},
    {"id": "considers-service-based", "passed": true, "evidence": "Service-Based is the primary recommendation, evaluated in detail and selected with highest adjusted score of 12."},
    {"id": "warns-anti-patterns", "passed": true, "evidence": "Step 4: Anti-Pattern Check names 4 specific anti-patterns: Too many services, Distributed monolith, Transactions across boundaries, Reuse coupling — each with risk level and mitigation."},
    {"id": "respects-coupling", "passed": true, "evidence": "'Keep payment and order creation in the same transaction scope initially. Only split when you have saga/eventual consistency experience.' Explicitly flags coupling between payment and orders and warns against premature decoupling."}
  ],
  "pass_count": 12,
  "total": 12
}
```

---

## File 6: eval-3/without_skill

**Scenario:** E-Commerce Platform (monolith migration)

```json
{
  "file": "eval-3/without_skill",
  "assertions": [
    {"id": "evaluates-monolith-vs-distributed", "passed": true, "evidence": "'Keep the Monolith' evaluated and explicitly rejected ('Not viable'). Distributed determined as necessary due to fault isolation, deployment bottleneck, and team coupling."},
    {"id": "compares-multiple-styles", "passed": true, "evidence": "5 styles evaluated: Keep Monolith, Modular Monolith, Microservices, Service-Based, Event-Driven — each with pros/cons/verdict."},
    {"id": "produces-scored-comparison", "passed": false, "evidence": "No numeric scored comparison. Uses qualitative verdicts ('Not viable', 'Valuable as stepping stone', 'High-risk', 'Best fit') and prose analysis. No comparison table with ratings."},
    {"id": "has-recommendation", "passed": true, "evidence": "Recommendation: Service-Based Architecture with Strategic Extraction"},
    {"id": "documents-trade-offs", "passed": true, "evidence": "Section 8 'What I Would NOT Do' lists 5 explicit rejections with reasoning (no fine-grained microservices, no big-bang rewrite, no service mesh early, no shared DBs long-term, no ignoring org change)."},
    {"id": "uses-star-ratings", "passed": false, "evidence": "No numeric 1-5 or equivalent ratings anywhere. All evaluations are qualitative prose descriptions."},
    {"id": "checks-quantum-count", "passed": false, "evidence": "No mention of quantum or equivalent concept. Identifies that payment needs different characteristics but does not frame this as a quantum analysis."},
    {"id": "checks-domain-isomorphism", "passed": false, "evidence": "No explicit evaluation of domain/architecture topology mapping. Notes team-to-service mapping (Conway's Law) but this is organizational fit, not domain isomorphism."},
    {"id": "checks-organizational-fit", "passed": true, "evidence": "Extensive organizational analysis: 35 devs/4 teams, no distributed tracing, basic CI/CD, team maturity alignment discussed in Section 3 'Why Service-Based Over Microservices'."},
    {"id": "considers-service-based", "passed": true, "evidence": "Service-Based is the primary recommendation with detailed justification and team mapping."},
    {"id": "warns-anti-patterns", "passed": true, "evidence": "'Distributed monolith' named explicitly in risk table (likelihood: High, impact: Critical) and in Section 8 point 1."},
    {"id": "respects-coupling", "passed": false, "evidence": "No explicit evaluation of domain coupling level. Mentions data consistency issues as a risk but does not assess domain coupling as a selection criterion."}
  ],
  "pass_count": 7,
  "total": 12
}
```

---

## Summary Table

| Assertion | E1-with | E1-without | E2-with | E2-without | E3-with | E3-without |
|-----------|:-------:|:----------:|:-------:|:----------:|:-------:|:----------:|
| **Structural** | | | | | | |
| evaluates-monolith-vs-distributed | PASS | FAIL | PASS | PASS | PASS | PASS |
| compares-multiple-styles | PASS | PASS | PASS | FAIL | PASS | PASS |
| produces-scored-comparison | PASS | PASS | PASS | FAIL | PASS | FAIL |
| has-recommendation | PASS | PASS | PASS | PASS | PASS | PASS |
| documents-trade-offs | PASS | PASS | PASS | PASS | PASS | PASS |
| **Value** | | | | | | |
| uses-star-ratings | PASS | PASS | PASS | FAIL | PASS | FAIL |
| checks-quantum-count | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| checks-domain-isomorphism | PASS | FAIL | PASS | FAIL | PASS | FAIL |
| checks-organizational-fit | PASS | PASS | PASS | PASS | PASS | PASS |
| considers-service-based | PASS | PASS | PASS | FAIL | PASS | PASS |
| warns-anti-patterns | PASS | FAIL | PASS | PASS | PASS | PASS |
| respects-coupling | FAIL | FAIL | PASS | FAIL | PASS | FAIL |
| | | | | | | |
| **Total** | **11/12** | **7/12** | **12/12** | **5/12** | **12/12** | **7/12** |

## Aggregate Scores

| Condition | Average Score | Range |
|-----------|:------------:|:-----:|
| **With skill** | **11.7 / 12** (97%) | 11-12 |
| **Without skill** | **6.3 / 12** (53%) | 5-7 |
| **Delta** | **+5.3** | +4 to +7 |

## Key Observations

1. **With-skill outputs consistently outperform without-skill** across all 3 evaluation scenarios, with a delta of +4 to +7 assertions per scenario.

2. **Without-skill outputs universally miss**: quantum analysis, domain isomorphism evaluation, and coupling assessment. These are book-specific concepts that general LLM knowledge does not naturally surface.

3. **Without-skill outputs pass on**: having a recommendation, documenting trade-offs, and checking organizational fit. These are general software architecture practices that LLMs handle without domain-specific guidance.

4. **Scored comparison is a differentiator**: with-skill outputs always produce numeric rated tables; without-skill outputs tend toward qualitative prose evaluation.

5. **Anti-pattern naming is mixed**: without-skill outputs sometimes name anti-patterns (eval-2 "big ball of mud", eval-3 "distributed monolith") but less systematically than with-skill outputs which have dedicated anti-pattern check steps.

6. **eval-2/with_skill achieved a perfect 12/12**, demonstrating the skill handles simple scenarios (solo dev, monolith) as rigorously as complex distributed scenarios.
