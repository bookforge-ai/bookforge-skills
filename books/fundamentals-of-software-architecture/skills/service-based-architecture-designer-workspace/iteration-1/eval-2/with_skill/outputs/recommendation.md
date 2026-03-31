# Service-Based Architecture Design: HR Platform

## Design Context
**System:** HR platform covering employee management, payroll, benefits, time tracking, and reporting
**Team:** Not specified — assuming moderate size (10-20)
**Key drivers:** Payroll needs high availability during pay periods; shared database desired with potential future split; service-based architecture explicitly requested

## Domain Services (5 services)

| # | Service | Domain | Key Components | Instances |
|---|---------|--------|---------------|:---------:|
| 1 | EmployeeService | Employee lifecycle management | Employee Onboarding, Profile Management, Org Structure, Employee Search | 1 |
| 2 | PayrollService | Payroll processing & calculations | Pay Calculation, Deductions, Tax Withholding, Direct Deposit, Pay Stubs | 3 (HA during pay periods) |
| 3 | BenefitsService | Benefits administration | Plan Management, Enrollment, Eligibility, Life Events, COBRA | 1 |
| 4 | TimeTrackingService | Time and attendance | Time Entry, Approvals, PTO Management, Overtime Calculation | 1 |
| 5 | ReportingService | Analytics and compliance reports | Standard Reports, Custom Reports, Compliance Reports (EEO, ACA), Data Export | 1 |

### Service Detail: PayrollService
**Domain:** All payroll computation from time data through pay distribution
**Internal design:** Layered (API facade -> business logic -> persistence) — payroll logic is complex but linear (calculate -> deduct -> withhold -> distribute)
**Components:**
- Pay Calculator: Gross pay computation from time records and salary data
- Deductions Engine: Benefits deductions, garnishments, voluntary deductions
- Tax Withholder: Federal, state, local tax computation and withholding
- Distribution Manager: Direct deposit file generation, check printing
- Pay Stub Generator: Employee-facing pay documentation

**High availability strategy:** Run 3 instances during pay periods (bi-weekly/monthly). Load balancer distributes payroll processing across instances. Other periods can run 1 instance for cost efficiency.

### Service Detail: TimeTrackingService
**Domain:** All time and attendance recording
**Internal design:** Domain-partitioned (API facade -> sub-domain components for time entry, PTO, overtime)
**Components:**
- Time Entry Manager: Clock-in/out, timesheet submission
- Approval Workflow: Manager approvals, escalations
- PTO Manager: Leave balance tracking, accrual rules, leave requests
- Overtime Calculator: Overtime computation per jurisdiction rules

## Database Topology
**Strategy:** Logically partitioned shared database (with migration path to domain-partitioned)
**Reasoning:** The user wants a shared database now with potential future split. Starting with logical partitioning through federated entity libraries establishes clean domain boundaries that make future physical separation straightforward. Payroll needs ACID transactions with time tracking data (approved time records must atomically feed into pay calculation), and with benefits data (deductions must be current). A shared database preserves these ACID guarantees.

**Logical partitions:**

| Partition | Key Tables | Used by services |
|-----------|-----------|-----------------|
| employee | employees, departments, positions, org_hierarchy | EmployeeService, PayrollService, BenefitsService |
| payroll | pay_runs, pay_records, deductions, tax_records, direct_deposits | PayrollService |
| benefits | benefit_plans, enrollments, eligibility, life_events | BenefitsService, PayrollService |
| time | time_entries, approvals, pto_balances, overtime_records | TimeTrackingService, PayrollService |
| reporting | report_definitions, scheduled_reports, report_cache | ReportingService |
| common | users, roles, audit_log, lookup_codes, calendar | All services |

**Entity libraries:**
- `employee_entities_lib` — used by EmployeeService, PayrollService, BenefitsService
- `payroll_entities_lib` — used by PayrollService
- `benefits_entities_lib` — used by BenefitsService, PayrollService
- `time_entities_lib` — used by TimeTrackingService, PayrollService
- `reporting_entities_lib` — used by ReportingService
- `common_entities_lib` — used by all (DBA-managed, locked in VCS)

**Future split migration path:**
When ready to split, the logical partitions become the physical split boundaries:
1. **First split candidate:** ReportingService — its data is read-heavy, write-rare, and not needed by other services for ACID transactions. Can move to a read replica or separate analytical database.
2. **Second split candidate:** TimeTrackingService — if time data is needed by PayrollService only during pay runs, a batch sync approach can replace the shared-DB join.
3. **Keep together:** PayrollService + BenefitsService need shared access for deduction calculations. Splitting these requires SAGA for every pay run — high complexity, low benefit.

## User Interface Topology
**Strategy:** Single monolithic UI
**Reasoning:** HR staff use a single portal for all HR functions. Role-based access controls which sections are visible (HR admins see everything, managers see time approvals and reports, employees see self-service).

## API Layer
**Decision:** Include
**Reasoning:** HR platforms typically integrate with external systems (payroll providers, benefits carriers, government reporting portals). An API layer provides centralized integration management, and consolidates authentication for the employee self-service portal vs admin portal.

## Transaction Boundaries

| Workflow | Domains involved | Services | Transaction type | Notes |
|----------|-----------------|----------|:----------------:|-------|
| Employee onboarding | employee, benefits, payroll | EmployeeService, BenefitsService, PayrollService | ACID | Shared DB: atomically create employee record, default benefit enrollment, payroll setup |
| Time submission | time | TimeTrackingService | ACID | Self-contained |
| Time approval | time | TimeTrackingService | ACID | Self-contained |
| Pay run processing | payroll, time, benefits, employee | PayrollService | ACID | PayrollService reads time and benefits data via shared DB joins, writes pay records atomically |
| Benefits enrollment | benefits, employee, payroll | BenefitsService, PayrollService | ACID | Shared DB: enrollment update + payroll deduction update atomically |
| Employee termination | employee, payroll, benefits, time | EmployeeService | ACID | Shared DB: atomically deactivate across all domains |
| Report generation | reporting (reads all) | ReportingService | Read-only | No transaction concerns — read-only queries across all partitions |

## Architecture Quanta
**Count:** 1
**Reasoning:** Single UI, single shared database, all services share the same deployment infrastructure. The PayrollService scaling during pay periods is handled by multiple instances, not a separate quantum.

## Characteristic Fit

| Characteristic | Rating | Meets needs? |
|---------------|:------:|:------------:|
| Deployability | 4 | Yes — payroll rule changes deploy independently of time tracking |
| Elasticity | 2 | Acceptable — payroll scaling is predictable (pay period schedule), not bursty |
| Fault tolerance | 4 | Yes — ReportingService outage doesn't block payroll processing |
| Modularity | 4 | Yes — benefits changes isolated from payroll processing logic |
| Overall cost | 4 | Yes — HR platform doesn't justify microservices operational cost |
| Reliability | 4 | Yes — critical for payroll accuracy; fewer distributed transactions = fewer failure points |
| Testability | 4 | Yes — PayrollService can be tested with mock time/benefits data |

## Anti-Pattern Check
- [x] Service count in 4-12 range (5 services)
- [x] No inter-service direct calls (PayrollService reads time/benefits through shared DB, not by calling TimeTrackingService)
- [x] Database topology supports required ACID transactions (shared DB preserves payroll atomicity)
- [x] Federated entity libraries (6 domain-scoped + common)
- [x] No premature database splitting (user explicitly wants shared DB first; migration path documented)

## Getting Started
1. Define the logical database partitions and create federated entity libraries — this is the foundation that enables both the current shared-DB approach and future migration
2. Implement PayrollService first — it has the highest business value and the most complex domain; proving it works independently validates the architecture
3. Set up load balancing for PayrollService with scaling rules tied to pay period schedule — 3 instances during pay runs, 1 instance otherwise
