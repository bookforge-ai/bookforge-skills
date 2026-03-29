# Architecture Characteristics Taxonomy

Complete list of architecture quality attributes organized by category. Use this as a reference when identifying characteristics — but remember, this list is never exhaustive. Any system may define custom characteristics based on unique factors.

## Operational Characteristics

These affect how the system runs in production.

| Characteristic | Definition |
|---------------|-----------|
| **Availability** | How long the system needs to be available (e.g., 24/7 with quick recovery from failure) |
| **Continuity** | Disaster recovery capability |
| **Performance** | Response times, throughput, capacity under stress |
| **Recoverability** | How quickly the system returns to normal after disaster |
| **Reliability / Safety** | Fail-safe behavior, mission-critical impact, financial cost of failure |
| **Robustness** | Handling error and boundary conditions (internet down, power outage, hardware failure) |
| **Scalability** | Ability to handle growing number of users or requests |
| **Elasticity** | Ability to handle sudden BURSTS of traffic (distinct from scalability which handles GROWTH) |

## Structural Characteristics

These affect how the codebase is organized and evolved.

| Characteristic | Definition |
|---------------|-----------|
| **Configurability** | End-user ability to easily change software configuration |
| **Extensibility** | How easy to plug in new functionality |
| **Installability** | Ease of installation on all necessary platforms |
| **Leverageability / Reuse** | Common components usable across multiple products |
| **Localization** | Multi-language, multi-currency, multi-unit support |
| **Maintainability** | Ease of applying changes and enhancements |
| **Portability** | Ability to run on multiple platforms |
| **Supportability** | Logging, debugging, and technical support facilities |
| **Upgradeability** | Ease of upgrading to newer versions |

## Cross-Cutting Characteristics

These span operational and structural concerns.

| Characteristic | Definition |
|---------------|-----------|
| **Accessibility** | Support for users with disabilities |
| **Archivability** | Data retention, archival, and deletion policies |
| **Authentication** | Verifying user identity |
| **Authorization** | Controlling access to functions by role, rule, or field |
| **Legal** | Legislative constraints (data protection, GDPR, SOX) |
| **Privacy** | Hiding transactions from internal employees (encryption beyond external threats) |
| **Security** | Database/network encryption, authentication for remote access, threat protection |
| **Usability** | Training requirements, user goal achievement |

## ISO Quality Characteristics

Additional standardized definitions:

- **Performance efficiency:** time behavior, resource utilization, capacity
- **Compatibility:** coexistence, interoperability
- **Usability:** recognizability, learnability, error protection, accessibility
- **Reliability:** maturity, availability, fault tolerance, recoverability
- **Security:** confidentiality, integrity, nonrepudiation, accountability, authenticity
- **Maintainability:** modularity, reusability, analyzability, modifiability, testability
- **Portability:** adaptability, installability, replaceability

## Custom Characteristics

Lists are always incomplete. Any system may define custom characteristics based on unique domain factors. The "Italy-ility" example: after a freak communication outage severed connections with Italian branches, a client required that all future architectures support "Italy-ility" — a unique combination of availability, recoverability, and resilience specific to their geography.
