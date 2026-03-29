# Evaluating Module Readiness for Microservice Extraction

## Overview

Before extracting microservices from your monolith with 15 top-level packages, you need to evaluate which modules are well-structured enough to extract cleanly. Here's a systematic approach using modularity metrics.

## Assessment Criteria

For each of the 15 packages, evaluate:

### 1. Cohesion
- Does the package have a single, clear responsibility?
- Are the classes within the package related to each other?
- A package with high cohesion is easier to extract because it's already self-contained

### 2. Coupling
- How many other packages does this package depend on?
- How many packages depend on this package?
- Low coupling to other packages means fewer dependencies to manage during extraction

### 3. Data Dependencies
- Does this package have its own database tables, or does it share tables with other packages?
- Shared database tables are the biggest blocker for microservice extraction
- You may need to duplicate data or use eventual consistency

### 4. API Surface
- How many public methods/classes does this package expose?
- A smaller API surface means a cleaner service boundary

## Evaluation Framework

Rate each package on a 1-5 scale for each criterion:

| Package | Cohesion (1-5) | Coupling (1-5) | Data Independence (1-5) | API Clarity (1-5) | Total |
|---------|:-----------:|:-----------:|:-------------------:|:------------:|:-----:|
| Package A | ? | ? | ? | ? | ? |
| ... | | | | | |

### Scoring Guide
- **5:** Excellent — clean, independent, ready to extract
- **4:** Good — minor issues, extractable with small effort
- **3:** Fair — some concerns, extractable with moderate effort
- **2:** Poor — significant dependencies, needs refactoring first
- **1:** Blocked — deeply entangled, cannot extract without major rework

## Extraction Priority Matrix

Plot packages on two axes:
- **X-axis:** Business value of independent deployment
- **Y-axis:** Technical readiness (from the scoring above)

Focus on packages in the upper-right quadrant: high business value AND high technical readiness.

## General Recommendations

1. **Start with the easiest win** — Extract the package with the highest readiness score first to build confidence and establish patterns
2. **Use the Strangler Fig pattern** — Gradually route traffic to the new service while the monolith still handles the remaining packages
3. **Shared database is the hardest problem** — Plan for database decomposition early
4. **Don't extract everything** — Some packages may be better left in the monolith
5. **Establish service contracts early** — Define APIs before extracting

## Red Flags (Do Not Extract)

- Packages that share database transactions with 3+ other packages
- Packages that are imported by every other package (utility/shared packages)
- Packages with circular dependencies with other packages
- Packages where extraction would require duplicating more than 30% of their code

## Conclusion

Focus on packages with high cohesion, low coupling, independent data, and clear APIs. These are your best candidates for microservice extraction. Packages that score low should be refactored within the monolith first to improve their boundaries before attempting extraction.
