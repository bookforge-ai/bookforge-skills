# Risk Matrix Template

## The 2D Risk Matrix

Architecture risk is quantified using two independent dimensions, each scored 1-3. The composite score (1-9) determines the risk classification.

### Dimension 1: Impact

How severe would it be if this risk materializes?

| Score | Level  | Description                                                    |
|:-----:|--------|----------------------------------------------------------------|
| 1     | Low    | Minor inconvenience. Easy recovery. No data loss. No revenue impact. |
| 2     | Medium | Significant disruption. Recoverable with effort. Partial degradation of service. Some user impact. |
| 3     | High   | Severe damage. Potential data loss. Major business impact. Revenue loss. Regulatory consequences. |

### Dimension 2: Likelihood

How probable is it that this risk materializes?

| Score | Level  | Description                                                    |
|:-----:|--------|----------------------------------------------------------------|
| 1     | Low    | Unlikely given current architecture and controls. Would require multiple simultaneous failures. |
| 2     | Medium | Possible under specific conditions: peak load, partial failures, edge cases. Has happened in similar systems. |
| 3     | High   | Probable or already occurring. Known issue. Architectural weakness actively exploitable. |

### Composite Risk Score Matrix

```
                    IMPACT
                 1       2       3
            +-------+-------+-------+
         1  |   1   |   2   |   3   |
            | (low) | (low) | (med) |
L        +-------+-------+-------+
I     2  |   2   |   4   |   6   |
K        | (low) | (med) | HIGH  |
E        +-------+-------+-------+
L     3  |   3   |   6   |   9   |
I        | (med) | HIGH  | HIGH  |
H        +-------+-------+-------+
O
O
D
```

### Risk Classification Thresholds

| Score Range | Classification | Color  | Response                                                 |
|:-----------:|:--------------:|:------:|----------------------------------------------------------|
| 1-2         | Low            | Green  | Acceptable. Monitor only. No immediate action required.  |
| 3-4         | Medium         | Yellow | Needs attention. Plan mitigation within current or next iteration. |
| 6-9         | High           | Red    | Requires immediate action or architectural change. Escalate to stakeholders. |

Note: Score 5 is not possible in a 3x3 matrix (no combination of 1-3 x 1-3 produces 5). This is intentional — it creates a clear gap between medium (max 4) and high (min 6).

## Standard Risk Criteria

These five criteria cover the most common architecture risk dimensions. Add domain-specific criteria as needed.

| Criterion        | What It Measures                                         | Common Risk Signals |
|------------------|----------------------------------------------------------|---------------------|
| **Scalability**  | Can the component handle increased load?                 | No auto-scaling, shared database bottlenecks, synchronous chains, single-threaded processing |
| **Availability** | What happens when the component goes down?               | No redundancy, single points of failure, no health checks, no circuit breakers |
| **Performance**  | Can the component meet latency/throughput requirements?  | Missing caching, N+1 queries, synchronous external calls in hot paths, no CDN |
| **Security**     | What is the exposure to breaches or unauthorized access? | Unencrypted data at rest/transit, missing auth, broad network exposure, unpatched dependencies |
| **Data Integrity** | What is the risk of data loss, corruption, or inconsistency? | No backups, eventual consistency without conflict resolution, shared mutable state, no validation |

## Risk Assessment Table Template

### Full View (for architecture team)

```markdown
| Risk Criteria    | Service A        | Service B        | Service C        | Total |
|------------------|------------------|------------------|------------------|-------|
| Scalability      | 6 (H) -         | 2 (L) =         | 4 (M) +         | 12    |
| Availability     | 3 (M) =         | 9 (H) -         | 1 (L) =         | 13    |
| Performance      | 2 (L) +         | 4 (M) =         | 6 (H) -         | 12    |
| Security         | 9 (H) =         | 3 (M) +         | 3 (M) =         | 15    |
| Data Integrity   | 6 (H) +         | 1 (L) =         | 9 (H) -         | 16    |
| **Total**        | **26**           | **19**           | **23**           |       |
```

### Filtered View (for stakeholder meetings — high-risk only)

```markdown
| Risk Criteria    | Service A        | Service B        | Service C        |
|------------------|------------------|------------------|------------------|
| Scalability      | 6 (H) -         | .                | .                |
| Availability     | .                | 9 (H) -         | .                |
| Performance      | .                | .                | 6 (H) -         |
| Security         | 9 (H) =         | .                | .                |
| Data Integrity   | 6 (H) +         | .                | 9 (H) -         |
```

Dots (.) replace low and medium scores to reduce noise and focus attention on what needs action.

## Direction Indicators

| Symbol | Meaning    | Description                                    |
|:------:|------------|------------------------------------------------|
| +      | Improving  | Risk is decreasing. Mitigation efforts working. Recent improvements made. |
| -      | Worsening  | Risk is increasing. New issues emerging. Previous mitigations insufficient. |
| =      | Stable     | No significant change since last assessment.   |

### How to Determine Direction

For first-time assessments (no previous baseline):
- **Recent incidents in this area** -> worsening (-)
- **Recent infrastructure improvements** -> improving (+)
- **No recent changes or incidents** -> stable (=)
- **New/unproven technology recently adopted** -> worsening (-)

For subsequent assessments:
- Compare directly to previous risk scores
- Consider whether mitigation actions from the last assessment were implemented

## Unproven Technology Rule

**For any technology that the team has NOT used in production, always assign the maximum risk score (9).**

This is not negotiable. Teams systematically underestimate the risk of unfamiliar technologies because:

1. **Unknown unknowns** — You don't know what failure modes exist until you've operated the technology under real load
2. **Optimism bias** — Technology evaluations tend to focus on features (benefits) rather than operational characteristics (risks)
3. **Vendor marketing** — Published benchmarks don't reflect your specific usage patterns, data shapes, or scale
4. **Support gap** — When the team can't diagnose production issues, mean time to recovery (MTTR) skyrockets

The score of 9 is a forcing function: it ensures unproven technologies get explicit attention, a proof-of-concept, and a rollback plan before being committed to production.

## Agile Story Risk Matrix

The same 2D matrix applies to user stories during sprint/iteration planning:

| Dimension   | Architecture Risk                        | Story Risk                                |
|-------------|------------------------------------------|-------------------------------------------|
| **Impact**  | Severity if risk materializes            | Business impact if story is NOT completed |
| **Likelihood** | Probability risk materializes         | Probability story will NOT be completed   |

### Story Risk Signals

| Factor                          | Impact on Likelihood |
|---------------------------------|---------------------|
| Complex story with many unknowns | Increases (2-3)    |
| Depends on external API/team    | Increases (2-3)     |
| Developer has done similar work | Decreases (1)       |
| Story is well-spiked/prototyped | Decreases (1)       |
| Requires new infrastructure     | Increases (2-3)     |

### Handling High-Risk Stories (6-9)

1. Start them on day 1 of the iteration — don't leave them until the end
2. Assign to the most experienced developer for that area
3. Break into smaller stories if possible to reduce likelihood
4. Identify and resolve dependencies before the iteration starts
5. Have a "plan B" scope reduction if the story is at risk mid-sprint

## Mitigation Documentation Template

For each high-risk cell in the assessment, document:

```markdown
### {Component} — {Risk Criterion} (Score: {N})

**Impact ({1-3}):** {Specific justification for impact level}
**Likelihood ({1-3}):** {Specific justification for likelihood level}
**Direction:** {+/-/=} — {Reason for trend}

**Root Cause:** {What architectural characteristic or decision creates this risk}

**Mitigation Options:**
1. {Option A} — Cost: {$X / complexity / time}
   - Post-mitigation score: {expected new score}
   - Trade-off: {what you give up}
2. {Option B} — Cost: {$X / complexity / time}
   - Post-mitigation score: {expected new score}
   - Trade-off: {what you give up}

**Recommended:** {Option N} because {justification tied to constraints}
```
