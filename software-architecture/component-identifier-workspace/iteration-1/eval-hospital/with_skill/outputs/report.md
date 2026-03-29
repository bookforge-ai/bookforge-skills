# Component Design: Hospital Management System

## Input Gathering Process

The initial request was deliberately vague: "patient records, appointment scheduling, billing, lab results, and pharmacy management." Following the skill's input gathering guidelines, the following clarifying questions were identified and answered before proceeding.

### Questions Asked (Simulated)

**Q1: "Who are the main types of users of this hospital management system?"**
A1: Doctors, Nurses, Receptionists/Front Desk Staff, Lab Technicians, Pharmacists, Billing/Finance Staff, Hospital Administrators, Patients (via a portal), and External Systems (insurance providers, external labs).

**Q2: "What are the most important things each user type does with the system?"**
A2: Doctors review patient records and order labs/prescriptions. Nurses update vitals and manage care plans. Receptionists schedule appointments and register patients. Lab techs process lab orders and enter results. Pharmacists dispense medications and check drug interactions. Billing staff generates invoices and processes insurance claims. Patients view their records, book appointments, and pay bills online.

**Q3: "Are there parts of the system with different performance, availability, or security needs?"**
A3: The patient portal must be highly available (24/7). Billing/insurance has strict HIPAA compliance requirements. Appointment scheduling experiences peak loads during morning hours. Lab results require real-time notification delivery. Pharmacy needs very low latency for drug interaction checks.

---

## Step 1: Partitioning Style

**Domain Partitioning** -- chosen for these reasons:

- A hospital management system has clearly distinct business domains (clinical care, scheduling, billing, pharmacy, lab) that map naturally to components.
- Different domains have very different quality attribute needs (availability for patient portal vs. compliance for billing vs. low latency for pharmacy), making domain partitioning essential for independent scalability and deployment.
- Domain partitioning aligns with how hospital departments actually operate, making it intuitive for stakeholders.
- If the system eventually moves to a distributed architecture (likely given the scale of a hospital), domain-partitioned components migrate cleanly into services.

Technical partitioning (presentation/business/persistence layers) would smear clinical, billing, and scheduling logic across every layer, making it extremely difficult to enforce HIPAA boundaries or scale domains independently.

---

## Step 2: Actors and Actions

| Actor | Actions |
|-------|---------|
| **Doctor** | View patient record, review medical history, order lab tests, write prescriptions, add clinical notes, review lab results, update diagnosis, refer to specialist |
| **Nurse** | Record vitals, update care plan, administer medication (record), triage incoming patients, view patient schedule, flag critical results |
| **Receptionist** | Register new patient, schedule appointment, reschedule/cancel appointment, check patient in, verify insurance, manage waitlist |
| **Lab Technician** | Receive lab order, process specimen, enter lab results, flag abnormal results, send results notification |
| **Pharmacist** | Receive prescription, check drug interactions, dispense medication, manage pharmacy inventory, flag contraindications, process refill requests |
| **Billing Staff** | Generate invoice, apply insurance coverage, submit insurance claim, process patient payment, handle claim denial, issue refund, generate financial reports |
| **Hospital Admin** | Manage staff accounts, view operational reports, configure departments, manage system settings, audit access logs |
| **Patient (Portal)** | View own medical records, book/cancel appointment, view lab results, pay bills online, request prescription refill, message care team |
| **External: Insurance Provider** | Receive claim submission, send claim adjudication response, provide eligibility verification |
| **External: Lab System** | Receive outbound lab orders, send inbound results (for outsourced tests) |

---

## Step 3: Identified Components

Actions grouped by cohesive workflows:

| Component | Responsibility | Key Actions | Architecture Characteristics |
|-----------|---------------|-------------|----------------------------|
| **Patient Registration** | Onboarding and managing patient demographic and insurance data | Register patient, verify insurance, update patient info, check in | Data integrity, HIPAA compliance |
| **Appointment Scheduling** | Managing the scheduling lifecycle across all provider types | Schedule/reschedule/cancel appointment, manage waitlist, check-in, view schedule | Elasticity (peak morning loads), availability |
| **Clinical Records** | Maintaining the longitudinal patient medical record | View/update patient record, add clinical notes, update diagnosis, record vitals, review medical history | High availability, HIPAA compliance, data integrity |
| **Clinical Orders** | Processing orders from clinicians to labs and pharmacy | Order lab test, write prescription, refer to specialist | Reliability, auditability |
| **Lab Processing** | End-to-end lab workflow from order receipt to result delivery | Receive lab order, process specimen, enter results, flag abnormals, send result notification | Real-time notification, reliability |
| **Pharmacy Management** | Prescription fulfillment and medication safety | Receive prescription, check drug interactions, dispense medication, manage pharmacy inventory, process refills, flag contraindications | Low latency (interaction checks), reliability, HIPAA compliance |
| **Billing & Claims** | Financial lifecycle: invoicing, insurance claims, payments | Generate invoice, apply insurance, submit claim, process payment, handle denial, issue refund | HIPAA compliance, auditability, fault tolerance |
| **Patient Portal** | Patient-facing self-service access | View records, book appointments, view lab results, pay bills, request refill, message care team | High availability (24/7), security, usability |
| **Notification Service** | Cross-cutting delivery of alerts and messages | Send lab result notification, appointment reminders, billing alerts, care team messages | Reliability, delivery guarantees |
| **Administration & Audit** | System configuration, staff management, compliance | Manage staff accounts, configure departments, audit access logs, view operational reports, manage settings | Security, auditability |
| **Reporting** | Operational and financial analytics | Generate financial reports, view operational reports, compliance reporting | Batch processing, data aggregation |

---

## Step 4: Requirement Mapping

| Requirement Area | Component(s) | Notes |
|------------------|-------------|-------|
| Patient records management | Patient Registration, Clinical Records | Registration handles demographics; Clinical Records handles medical data. Clear separation. |
| Appointment scheduling | Appointment Scheduling | Self-contained. Patient Portal delegates to this component for patient-initiated bookings. |
| Billing and insurance | Billing & Claims | Receives triggers from Clinical Orders (when service is rendered). Integrates with external insurance systems. |
| Lab results | Clinical Orders, Lab Processing | Orders originate in Clinical Orders, execution and results in Lab Processing. Two-component span is acceptable -- it reflects the real handoff. |
| Pharmacy management | Clinical Orders, Pharmacy Management | Prescriptions originate in Clinical Orders, fulfillment in Pharmacy Management. Same handoff pattern as labs. |
| Patient self-service | Patient Portal | Delegates to Scheduling, Clinical Records, Billing, Lab Processing for data. Acts as a facade/gateway. |
| Drug interaction safety | Pharmacy Management | Must be low-latency. May call external drug database. Critical patient safety requirement. |
| HIPAA compliance | Clinical Records, Billing & Claims, Pharmacy Management, Administration & Audit | Multiple components share this characteristic -- but each enforces it within its own domain. Audit component provides cross-cutting compliance logging. |
| Real-time notifications | Notification Service, Lab Processing | Lab Processing triggers; Notification Service delivers. Clean separation of concerns. |
| Staff and system admin | Administration & Audit | Self-contained for internal operations. |

No requirements are unassigned. No components lack requirements.

---

## Step 5: Entity Trap Check

**PASS** -- The design avoids the Entity Trap.

Evidence:
- Components are named after workflows and capabilities (Appointment Scheduling, Clinical Orders, Lab Processing, Pharmacy Management), NOT after entities (PatientManager, AppointmentManager, BillManager).
- Each component encapsulates behavioral logic, not just CRUD: Pharmacy Management checks drug interactions, Lab Processing flags abnormals, Clinical Orders coordinates referrals.
- Components do NOT map 1:1 to database tables. For example, "patient" data is split between Patient Registration (demographics) and Clinical Records (medical history) based on workflow boundaries, not data structure.
- The one component that could look entity-like -- Patient Registration -- is justified because patient onboarding IS a distinct workflow (verify insurance, collect demographics, assign MRN), not just a CRUD wrapper.

---

## Step 6: Granularity Assessment

**Assessment: Appropriately sized, with one area to monitor.**

- **Appointment Scheduling:** 5 actions, single cohesive workflow. Good size.
- **Clinical Records:** Could grow large as it handles vitals, notes, diagnoses, and history. Monitor for splitting into sub-components (e.g., Vitals Capture vs. Clinical Documentation) if it becomes unwieldy.
- **Clinical Orders:** Lightweight coordination component (labs, prescriptions, referrals). Could be merged into Clinical Records if the overhead of a separate component isn't justified. Keep separate for now because it has different reliability characteristics.
- **Patient Portal:** Acts as a facade -- delegates to other components. Does not contain its own business logic. Correct granularity for a gateway/BFF pattern.
- **Notification Service:** Cross-cutting utility. Appropriately separated since multiple components need it.
- **Reporting:** Separated from Administration because it has fundamentally different characteristics (batch vs. interactive).

No single user action requires calling more than 2-3 components. No single component handles more than 7 unrelated actions. Granularity is in the sweet spot.

---

## Step 7: Characteristic Variance

| Component | Primary Characteristics | Differs from Others? |
|-----------|----------------------|:---:|
| Patient Registration | Data integrity, compliance | No |
| Appointment Scheduling | Elasticity, availability | **Yes** -- peak load elasticity |
| Clinical Records | High availability, compliance | **Yes** -- highest availability need |
| Clinical Orders | Reliability, auditability | No |
| Lab Processing | Real-time notification, reliability | **Yes** -- real-time processing |
| Pharmacy Management | Low latency, reliability | **Yes** -- sub-second interaction checks |
| Billing & Claims | Compliance, fault tolerance, auditability | **Yes** -- strict regulatory requirements |
| Patient Portal | High availability (24/7), security | **Yes** -- public-facing, always-on |
| Notification Service | Reliability, delivery guarantees | No |
| Administration & Audit | Security, auditability | No |
| Reporting | Batch throughput | **Yes** -- batch vs. interactive |

**Significant characteristic variance detected.** Six components have distinct quality attribute profiles. This strongly suggests the system should NOT be a single monolith. Recommended next step: use `architecture-quantum-analyzer` to determine deployment units (quanta). Likely quantum candidates:

- **Clinical Quantum:** Clinical Records + Clinical Orders (shared high-availability, compliance needs)
- **Scheduling Quantum:** Appointment Scheduling (independent elasticity)
- **Patient Portal Quantum:** Patient Portal (public-facing, 24/7, separate security boundary)
- **Financial Quantum:** Billing & Claims (regulatory isolation)
- **Lab Quantum:** Lab Processing (real-time processing)
- **Pharmacy Quantum:** Pharmacy Management (low-latency interaction checks, patient safety critical)
- **Back-Office Quantum:** Patient Registration + Administration & Audit + Reporting + Notification Service (standard internal workloads)

---

## Component Relationship Map

```
                          +-------------------+
                          |  Patient Portal   |  (facade -- delegates to others)
                          +--------+----------+
                                   |
              +--------------------+--------------------+
              |                    |                     |
              v                    v                     v
    +---------+--------+  +-------+--------+  +---------+--------+
    |   Appointment    |  | Clinical       |  | Billing &        |
    |   Scheduling     |  | Records        |  | Claims           |
    +------------------+  +-------+--------+  +--------+---------+
                                  |                     ^
                                  v                     |
                          +-------+--------+            |
                          | Clinical       +------------+
                          | Orders         |  (triggers billing on service rendered)
                          +---+-------+----+
                              |       |
                    +---------+       +---------+
                    v                           v
           +-------+--------+         +--------+----------+
           | Lab             |         | Pharmacy          |
           | Processing      |         | Management        |
           +-------+---------+         +-------------------+
                   |
                   v
           +-------+---------+
           | Notification    |  (also used by Scheduling, Billing, Portal)
           | Service         |
           +-----------------+

    +-------------------+     +-------------------+
    | Patient           |     | Administration    |
    | Registration      |     | & Audit           |
    +-------------------+     +-------------------+

    +-------------------+
    | Reporting         |  (reads from all domains)
    +-------------------+
```

Key relationships:
- **Patient Portal** delegates to Scheduling, Clinical Records, Billing, Lab Processing, and Pharmacy.
- **Clinical Orders** is the hub connecting clinicians to Lab Processing and Pharmacy Management. It also triggers Billing when a service is rendered.
- **Notification Service** is used by Lab Processing (results ready), Scheduling (reminders), Billing (payment due), and Patient Portal (messages).
- **Reporting** reads from all domains but writes to none -- purely consumptive.
- **Patient Registration** feeds demographic data to Clinical Records and Billing.

---

## Summary and Recommended Next Steps

This analysis identified **11 domain-partitioned components** for the hospital management system, organized around real workflows rather than data entities. The design passes the Entity Trap check and has appropriate granularity.

**Key architectural insight:** There is significant characteristic variance across components -- six components have distinct quality attribute profiles. This means a single monolithic deployment will force trade-offs (e.g., the Patient Portal's 24/7 availability requirement would constrain deployment of the entire system). A modular or distributed architecture is strongly recommended.

**Recommended next steps:**
1. **Run architecture-characteristics-identifier** -- formalize the driving characteristics for each component with stakeholder input.
2. **Run architecture-quantum-analyzer** -- use the characteristic variance data above to determine the optimal number of deployment units (quanta) and select an architecture style.
3. **Validate with stakeholders** -- present the actor/actions table and component map to hospital staff. They should recognize their workflows in the component names.
4. **Iterate** -- this is a first-pass hypothesis. After requirement refinement, expect Clinical Records and Pharmacy Management to be the most likely candidates for restructuring.
