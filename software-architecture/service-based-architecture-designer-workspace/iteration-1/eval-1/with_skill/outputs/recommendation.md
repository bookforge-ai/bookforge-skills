# Service-Based Architecture Design: Healthcare Patient Management System

## Design Context
**System:** Healthcare patient management covering registration, appointments, medical records, billing, and lab results
**Team:** 15 developers
**Key drivers:** ACID transactions needed between billing and medical records; deployment takes 3 hours (need to reduce); distributed benefits without microservices complexity

## Domain Services (5 services)

| # | Service | Domain | Key Components | Instances |
|---|---------|--------|---------------|:---------:|
| 1 | PatientService | Patient registration & demographics | Registration, Demographics, Insurance Verification, Patient Search | 1 |
| 2 | SchedulingService | Appointment management | Appointment Booking, Calendar Management, Provider Availability, Reminders | 1 |
| 3 | ClinicalService | Medical records & clinical data | Medical Records, Clinical Notes, Diagnoses, Prescriptions, Allergies | 2 |
| 4 | BillingService | Billing & financial operations | Charge Capture, Claims Processing, Payment Processing, Invoicing | 2 |
| 5 | LabService | Lab orders & results | Lab Order Entry, Specimen Tracking, Results Processing, Results Notification | 1 |

### Service Detail: ClinicalService
**Domain:** All clinical and medical record data
**Internal design:** Domain-partitioned (API facade + sub-domain components for records, notes, prescriptions)
**Components:**
- Medical Records Manager: CRUD for patient medical histories
- Clinical Notes Engine: Progress notes, visit summaries
- Prescription Manager: Medication orders, refills, interactions
- Allergy Tracker: Patient allergy records and alerts

### Service Detail: BillingService
**Domain:** All financial operations from charge capture through payment
**Internal design:** Layered (API facade -> business logic -> persistence)
**Components:**
- Charge Capture: Records billable services from clinical encounters
- Claims Processor: Generates and submits insurance claims
- Payment Processor: Handles patient payments, co-pays
- Invoice Generator: Creates patient statements

## Database Topology
**Strategy:** Logically partitioned (single shared database with domain-scoped entity libraries)
**Reasoning:** ACID transactions are required between BillingService and ClinicalService — when a clinical encounter generates charges, the charge record and the clinical documentation must be atomically consistent. A shared database preserves this ACID guarantee. Logical partitioning through federated entity libraries controls schema change blast radius.

**Logical partitions:**

| Partition | Key Tables | Used by services |
|-----------|-----------|-----------------|
| patient | patients, demographics, insurance_info | PatientService, ClinicalService, BillingService |
| scheduling | appointments, provider_availability, calendar_slots | SchedulingService |
| clinical | medical_records, clinical_notes, prescriptions, allergies, diagnoses | ClinicalService |
| billing | charges, claims, payments, invoices | BillingService |
| lab | lab_orders, specimens, lab_results | LabService |
| common | users, audit_log, notifications, lookup_codes | All services |

**Entity libraries:**
- `patient_entities_lib` — used by PatientService, ClinicalService, BillingService
- `scheduling_entities_lib` — used by SchedulingService
- `clinical_entities_lib` — used by ClinicalService
- `billing_entities_lib` — used by BillingService
- `lab_entities_lib` — used by LabService
- `common_entities_lib` — used by all services (locked in VCS, DBA-managed)

## User Interface Topology
**Strategy:** Single monolithic UI
**Reasoning:** All 15 developers serve the same user group (clinical staff and billing staff at healthcare facilities). A single UI with role-based access is simpler to maintain and ensures consistent UX across the patient workflow.

## API Layer
**Decision:** Include
**Reasoning:** Healthcare systems require centralized security enforcement (HIPAA compliance), audit logging, and will likely need to expose APIs to external systems (insurance clearinghouses, lab systems, pharmacy systems). The API layer consolidates these cross-cutting concerns and provides a single enforcement point for PHI (Protected Health Information) access controls.

## Transaction Boundaries

| Workflow | Domains involved | Services | Transaction type | Notes |
|----------|-----------------|----------|:----------------:|-------|
| Patient registration | patient | PatientService | ACID | Self-contained within one service |
| Schedule appointment | scheduling, patient | SchedulingService | ACID | Patient lookup is read-only; scheduling writes are self-contained |
| Clinical encounter | clinical, billing | ClinicalService, BillingService | ACID | **Critical:** Charge capture must be atomic with clinical documentation. Shared DB enables this via cross-schema transaction |
| Lab order | lab, clinical | LabService, ClinicalService | ACID | Lab orders reference clinical context; shared DB enables atomic order creation |
| Lab results filing | lab, clinical | LabService, ClinicalService | ACID | Results must atomically update both lab records and patient clinical record |
| Claims submission | billing | BillingService | ACID | Self-contained |
| Payment processing | billing, patient | BillingService | ACID | Patient balance update is within shared DB |

## Architecture Quanta
**Count:** 1
**Reasoning:** All services share a single database and a single UI. Despite being separately deployed, they form a single quantum because they share the same deployment characteristics. If the customer-facing portal is added later (patient self-service), this could split into 2 quanta.

## Characteristic Fit

| Characteristic | Rating | Meets needs? |
|---------------|:------:|:------------:|
| Deployability | 4 | Yes — reduces 3-hour monolith deploy to ~20 min per service |
| Elasticity | 2 | Acceptable — healthcare traffic is predictable, not bursty |
| Fault tolerance | 4 | Yes — BillingService outage won't block clinical documentation |
| Modularity | 4 | Yes — each domain is independently modifiable |
| Overall cost | 4 | Yes — much cheaper than microservices for 15-person team |
| Reliability | 4 | Yes — fewer network hops than microservices, ACID preserved |
| Testability | 4 | Yes — can test BillingService independently of ClinicalService |

## Anti-Pattern Check
- [x] Service count in 4-12 range (5 services)
- [x] No inter-service direct calls (all coordination through shared DB or UI)
- [x] Database topology supports required ACID transactions (shared DB with logical partitioning)
- [x] Federated entity libraries (6 domain-scoped libraries + common)
- [x] No premature database splitting (shared DB preserves billing-clinical ACID)

## Getting Started
1. Define the API facade contracts for each of the 5 services — start with PatientService as it has the simplest domain
2. Implement the federated entity library structure — create the 6 domain-scoped libraries and common library, enforce through build system
3. Set up independent deployment pipelines for each service — verify that deploying BillingService doesn't require redeploying ClinicalService
