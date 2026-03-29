# Microservice Granularity Report: User Service Over-Split Diagnosis

## Current State
**Services:** 5 (UserProfile, UserPreferences, UserAuth, UserNotifications, UserAnalytics)
**Key pain points:** Every API call requires 3-4 inter-service calls, latency tripled, team suspects over-splitting

## Diagnosis: Over-Granular Services

This is a textbook case of over-splitting. The "User" domain was split along entity/function lines (the entity trap), creating 5 fine-grained services that cannot operate independently. Martin Fowler's warning applies directly: "microservice" is a label, not a description -- these services are too small.

## Disintegrator/Integrator Analysis

### Integrator Analysis (evaluating merge candidates)

### Service Pair: UserProfile + UserPreferences

| Integrator | Applies? | Evidence |
|-----------|:--------:|----------|
| Database transactions | YES | Updating a user's locale preference must atomically update their profile display settings. Currently requires distributed coordination. |
| Workflow coupling | YES | Every profile render requires a preferences lookup. 100% of UserProfile requests call UserPreferences. |
| Shared code | YES | Both share user validation logic, user entity models, and access control rules. |
| Data relationships | YES | Preferences are an attribute of a user profile -- they have a 1:1 data relationship. |
| **Integrator score** | **4/4** | **Must merge** |

**Decision: MERGE.** All four integrators apply strongly. UserPreferences is not a bounded context -- it's an attribute of the UserProfile bounded context.

### Service Pair: UserProfile + UserAuth

| Integrator | Applies? | Evidence |
|-----------|:--------:|----------|
| Database transactions | YES | Creating a new user must atomically create both profile and auth credentials. Currently uses a saga for user registration. |
| Workflow coupling | YES | Every authenticated request needs both auth token validation AND profile data. Login flow: Auth validates credentials, then Profile provides user context. |
| Shared code | YES | Both need user entity, email validation, account status checks. |
| Data relationships | YES | Auth needs profile data (email, account status) for every authentication. |
| **Integrator score** | **4/4** | **Must merge** |

**Decision: MERGE.** Every single integrator applies at maximum strength. A saga for user registration is absurd -- this was a simple database transaction before the split.

### Disintegrator Analysis: Does anything justify keeping services separate?

| Disintegrator | UserProfile | UserPreferences | UserAuth | UserNotifications | UserAnalytics |
|--------------|:---:|:---:|:---:|:---:|:---:|
| Scope/function | Part of User domain | Part of User domain | Part of User domain | Different domain (messaging) | Different domain (analytics) |
| Code volatility | Low | Low | Low | Medium (new channels) | High (new metrics weekly) |
| Scalability | Standard | Standard | Higher (auth checks on every request) | Higher (batch sends) | Standard |
| Fault tolerance | Critical | Non-critical | Critical | Non-critical | Non-critical |
| Security | PII | Low | HIGH (credentials, tokens) | Low | Low |
| Extensibility | Stable | Stable | Stable | Growing (SMS, push) | Growing (new events) |

**Key findings:**
- UserAuth has a security disintegrator (handles credentials/tokens) but the integrator score is 4/4. The security concern can be addressed within a merged service through encryption, access controls, and internal modularization rather than service separation.
- UserNotifications has legitimate disintegrators: different scalability (batch sends), fault tolerance (non-critical), and extensibility (growing channels). This should remain separate.
- UserAnalytics has code volatility and extensibility disintegrators. Changes weekly while other services are stable. Should remain separate.

## Recommended Service Boundaries

| # | Service | Domain | Merged from | Owns Data | Rationale |
|---|---------|--------|-------------|-----------|-----------|
| 1 | **UserService** | User identity, profile, preferences, authentication | UserProfile + UserPreferences + UserAuth | users, profiles, preferences, credentials, tokens, sessions | 4/4 integrators on every pair. Single bounded context. Auth security handled via internal module isolation + encryption. |
| 2 | **NotificationService** | Multi-channel notifications | UserNotifications | notification_templates, notification_log, delivery_status | Legitimate disintegrators: scalability (batch), fault tolerance (non-critical), extensibility (new channels). |
| 3 | **UserAnalyticsService** | User behavior analytics | UserAnalytics | user_events, metrics, aggregations | Legitimate disintegrators: code volatility (changes weekly), extensibility (new metrics). Can tolerate eventual consistency. |

## Communication Design

| Workflow | Services involved | Pattern | Reasoning |
|----------|------------------|---------|-----------|
| User registration | UserService only | N/A | Single service. Was previously a 3-service saga -- now a single ACID transaction. |
| User login | UserService only | N/A | Single service. Was previously 2 synchronous inter-service calls. |
| Get user profile | UserService only | N/A | Single service. Was previously 2-3 inter-service calls. |
| Send notification | UserService -> NotificationService | Choreography | UserService publishes "UserRegistered" event, NotificationService sends welcome email. Fire-and-forget. |
| Track user activity | UserService -> UserAnalyticsService | Choreography | UserService publishes "UserLoggedIn" events, Analytics consumes asynchronously. |

## Performance Impact

| Metric | Before (5 services) | After (3 services) | Improvement |
|--------|:---:|:---:|:---:|
| Inter-service calls per profile view | 3-4 | 0 | Eliminated |
| Inter-service calls per login | 2 | 0 | Eliminated |
| User registration latency | ~800ms (saga across 3 services) | ~50ms (single ACID transaction) | ~16x faster |
| P99 profile view latency | ~400ms (3 network hops) | ~80ms (single service) | ~5x faster |
| Saga patterns needed | 1 (registration) | 0 | Eliminated |

## Anti-Pattern Check
- [x] No shared databases between services
- [x] No distributed monolith (each of the 3 services deploys independently)
- [x] Not over-granular (0 of 3 workflows need saga -- 0%)
- [x] No entity trap (UserService models the user lifecycle, not just the "users" table)
- [x] No accidental front controllers
- [x] Each service can function if others degrade (notifications can queue, analytics can buffer)

## Characteristic Fit

| Characteristic | Rating | Meets needs? |
|---------------|:------:|:------------:|
| Deployability | 4 | Yes -- 3 services deploy independently |
| Elasticity | 5 | Yes -- NotificationService scales for batch sends |
| Fault tolerance | 4 | Yes -- analytics/notification failure doesn't affect auth |
| Performance | 2 | IMPROVED -- eliminated 3-4 inter-service calls per request |
| Simplicity | 1 | IMPROVED -- reduced from 5 to 3 services, eliminated saga |

## Root Cause Analysis

The over-splitting occurred because the team treated "microservice" as a size prescription and split along entity/function lines within a single bounded context (User). The User domain is a single bounded context -- profile, preferences, and authentication are all aspects of "user identity." Splitting them created a distributed monolith: all the complexity of microservices with none of the benefits, because the services could never operate independently.

**Rule applied:** "Don't do transactions in microservices -- fix granularity instead!" The user registration saga was the clearest indicator that the granularity was wrong.
