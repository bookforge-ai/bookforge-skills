# Enforcing Database Isolation Across Microservices

## The Problem

You have an architecture decision that says "no service should directly depend on another service's database." This is a fundamental microservices principle -- each service should own its data.

## Approaches to Enforce This

### 1. Code Review Process

Make this a code review checklist item. Reviewers should check that:
- No service has connection strings to another service's database
- No repository class queries tables owned by another service
- All cross-service data access goes through APIs

### 2. Database User Permissions

Create separate database users for each service with access limited to only their own schema:

```sql
-- Order service can only access order schema
CREATE USER order_service WITH PASSWORD '...';
GRANT ALL ON SCHEMA order_schema TO order_service;
REVOKE ALL ON SCHEMA payment_schema FROM order_service;
```

### 3. Separate Databases

The strongest enforcement is to use separate database instances per service. This makes cross-service database access physically impossible.

### 4. Static Analysis

Use tools like SonarQube or custom linting rules to detect:
- JDBC connection strings pointing to the wrong database
- SQL queries referencing tables from other services
- Entity classes mapping to tables outside the service's domain

### 5. Integration Testing

Write integration tests that verify each service only connects to its own database. Mock external service databases and verify the service functions correctly with only its own data.

## Recommendation

Start with database user permissions (quick win) and code review checklists. Then move to separate databases per service as your infrastructure matures. Add static analysis rules as a long-term investment.
