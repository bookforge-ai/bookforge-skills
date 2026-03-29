# Grading Summary: Architecture Quantum Analyzer — Iteration 1

## Overall Scores

| Test | With Skill | Baseline | Delta |
|------|:---:|:---:|:---:|
| Test 1: Auction Codebase (env-grounded) | **9/9** | 8/9 | +1 |
| Test 2: Healthcare Greenfield (text-only) | **9/9** | 3/9 | +6 |
| Test 3: Simple Monolith (text-only) | **9/9** | 4/9 | +5 |
| **Total** | **27/27** | **15/27** | **+12** |

With-skill average: **9.0/9 (100%)**
Baseline average: **5.0/9 (55.6%)**

---

## Per-Assertion Pass Rates

| # | Assertion | With Skill (3 runs) | Baseline (3 runs) | Discriminating? |
|---|-----------|:---:|:---:|:---:|
| 1 | identifies-deployable-units | 3/3 | 3/3 | No |
| 2 | produces-quantum-map | 3/3 | 3/3 | No |
| 3 | has-monolith-vs-distributed-recommendation | 3/3 | 3/3 | No |
| 4 | analyzes-communication-patterns | 3/3 | 1/3 | **Yes** |
| 5 | applies-3-criteria-definition | 3/3 | 1/3 | **Yes** |
| 6 | identifies-different-characteristics-per-quantum | 3/3 | 1/3 | **Yes** |
| 7 | uses-connascence-for-boundaries | 3/3 | 1/3 | **Yes** |
| 8 | warns-uniform-characteristics | 3/3 | 1/3 | **Yes** |
| 9 | quantum-count-drives-style | 3/3 | 2/3 | Moderate |

### Structural assertions (1-4): With Skill 12/12, Baseline 10/12
### Value assertions (5-9): With Skill 15/15, Baseline 5/15

---

## Discriminating Assertions (Strongest Skill Signal)

Five assertions showed a 3/3 vs 1/3 split — these are the behaviors the skill reliably produces that baseline LLM reasoning does not:

1. **applies-3-criteria-definition** — The skill enforces the formal 3-criteria AND test (independently deployable + high functional cohesion + synchronous connascence). Baselines mention some criteria loosely but never apply all three as a unified framework.

2. **uses-connascence-for-boundaries** — The skill uses synchronous connascence (fate-sharing, sync coupling) as the *technical* criterion for quantum boundaries. Baselines use ad-hoc criteria (compliance boundaries, team size, shared database) without the connascence lens.

3. **identifies-different-characteristics-per-quantum** — The skill produces structured characteristic comparison tables showing uniformity or non-uniformity. Baselines note differences in prose but skip the systematic comparison.

4. **warns-uniform-characteristics** — The skill explicitly checks whether characteristics are uniform and warns appropriately. Baselines never frame the analysis in these terms.

5. **analyzes-communication-patterns** — The skill maps every communication path with sync/async classification. Baselines mention communication in passing but skip systematic mapping.

---

## Non-Discriminating Assertions

Assertions 1-3 (identifies-deployable-units, produces-quantum-map, has-monolith-vs-distributed-recommendation) passed in all 6 runs. These are baseline LLM capabilities — any competent model can identify components, produce tables, and make recommendations. They are necessary for structural completeness but do not measure skill value.

---

## Environment-Grounded vs Text-Only Test Performance

### Test 1 (Auction Codebase — environment-grounded)
The baseline scored **8/9** — only 1 point below the with-skill run. When the model can read actual code (docker-compose.yml, Python files with `httpx`, `pika`, etc.), it naturally discovers sync/async patterns and connascence from the evidence. The codebase itself acts as a partial substitute for the skill's framework.

The single miss (quantum-count-drives-style) shows the baseline can analyze well but fails to state the *decision formula* — it shows the work but doesn't articulate the principle.

### Tests 2-3 (Healthcare Greenfield, Simple Monolith — text-only)
Baselines scored **3/9** and **4/9**. Without a codebase to inspect, the model falls back on generic architecture advice (team size, operational overhead, pragmatic tradeoffs). It lacks the structured analytical framework the skill provides.

**Key insight:** The skill's value is highest on text-only / greenfield scenarios where there is no code to guide the analysis. On codebase-grounded tests, the code itself provides much of the structure, narrowing the gap.

---

## Baseline Behavior Patterns

The baseline runs exhibited consistent patterns:

1. **Pragmatic over principled.** Baselines reason about team size, operational cost, and practical tradeoffs rather than applying architecture quantum theory. The healthcare baseline recommended 2-3 units based on "costs outweigh benefits" logic — a reasonable answer, but not quantum analysis.

2. **Correct conclusions, wrong reasoning.** All 3 baselines reached defensible architecture recommendations. But the *path* to those conclusions relied on experience-based heuristics, not the formal quantum framework. This matters because heuristics break on edge cases where the framework would still hold.

3. **Missing vocabulary.** Baselines rarely or never used: "connascence," "synchronous connascence," "high functional cohesion" (as a criterion), "characteristic uniformity," or "quantum count drives style." The skill embeds this vocabulary into the output.

---

## Verdict

**The skill works.** Perfect 27/27 across all with-skill runs. The skill produces consistently structured, theory-grounded quantum analysis regardless of input type.

**Discrimination is strong on value assertions.** The 5 value assertions separate skill-guided from baseline outputs with a 15/15 vs 5/15 split (100% vs 33%).

**Discrimination is weak on structural assertions.** 12/12 vs 10/12 — the model already knows how to identify components and make recommendations.

**The skill adds the most value on text-only / greenfield inputs** where there is no codebase to anchor the analysis. On code-grounded inputs, the gap narrows but the skill still ensures the formal framework is applied.

**Recommendation for iteration 2:** The 5 discriminating value assertions are the right ones to keep. Consider dropping or combining the 3 non-discriminating structural assertions (1-3) into a single "structural completeness" check to reduce grading overhead. Assertion 4 (analyzes-communication-patterns) bridges structural and value — keep it.
