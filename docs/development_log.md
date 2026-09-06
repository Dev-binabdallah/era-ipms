# ERA-IPMS Development Log

## 2026-09-03 — Custom Authentication and Session Management

### Objective
Integrate Django authentication with the existing ERA-IPMS database without
recreating or modifying the existing users and roles schema.

### Work Completed
- Connected Django 5.2.17 to the existing MariaDB database.
- Generated Django models using `inspectdb`.
- Mapped the existing `users` and `roles` tables to Django models.
- Added compatibility methods/properties to the `Users` model.
- Implemented `UsersAuthenticationBackend`.
- Configured Django to use the custom authentication backend.
- Reset and verified the existing System Administrator password.
- Implemented authentication test and logout endpoints.
- Applied the Django sessions migration only.
- Disabled Django's incompatible `update_last_login` signal because the
  existing `users` table does not contain a `last_login` column.

### Verification
- `python backend/manage.py check` — PASSED
- `authenticate()` — PASSED
- `login()` — PASSED
- Session created — PASSED
- `_auth_user_id` stored correctly — PASSED
- Custom authentication backend stored in session — PASSED
- `logout()` — PASSED
- Session cleared — PASSED

### Database Decision
The existing ERA-IPMS database schema remains authoritative. The `core`
models remain `managed = False`. Django's default authentication migrations
were not applied.

### Next Step
Build the production login page, protected dashboard, logout interface,
and role-based authorization.

## 2026-09-04 — Project Documentation Baseline: README

### Objective

Align the project README with the approved ERA-IPMS Concept Note version 1.1 and the current documentation and architecture baseline before continuing with requirements and implementation work.

### Work Completed

* Updated `README.md` to reflect the current ERA-IPMS project baseline.
* Updated the project status from planning and requirements analysis to documentation and architecture baseline.
* Confirmed Python/Django as the backend technology direction.
* Confirmed MariaDB/MySQL as the database direction.
* Removed the outdated Java technology reference.
* Updated the initial user model to the five approved titles:

  * Admin
  * Director
  * Programme Coordinator
  * Finance
  * Member
* Clarified the distinction between:

  * Titles
  * Permissions
  * Responsibilities
* Documented the approved record-level access direction.
* Documented the approved project governance direction.
* Added the approved system modules and current scope.
* Added the poultry and small farm relationship.
* Added the basic finance direction, including sales and expenses.
* Added the documentation-first development process.
* Updated the project roadmap and repository structure.
* Added documentation change-control and data-protection guidance.

### Documentation Decision

The README now represents the current high-level project baseline and must remain consistent with the approved Concept Note and subsequent requirements documents.

The project will continue with documentation review and alignment before new application pages or database architecture changes are introduced.

### Verification

* README reviewed against the approved project baseline.
* README terminology aligned with the current title, permission, and responsibility model.
* Technology direction aligned with Django and MariaDB/MySQL.
* Documentation-first development sequence recorded.


## 2026-09-05 - Needs Assessment Documentation Baseline

### Objective

Review and align the ERA-IPMS Needs Assessment with the approved Concept Note and README documentation baseline before continuing to stakeholder analysis and detailed software requirements.

### Work Completed

* Reviewed the existing Needs Assessment.
* Updated the document from version 1.0 to version 1.1.
* Aligned the Needs Assessment with the approved five-title model:

  * Admin
  * Director
  * Programme Coordinator
  * Finance
  * Member
* Clarified the distinction between titles, permissions, and responsibilities.
* Added the approved record-level access direction.
* Aligned beneficiary and disability service requirements with the current project baseline.
* Expanded poultry needs to include poultry groups, purchases, production, feed, health, deaths, sales, expenses, and responsibilities.
* Aligned small farm requirements with the approved relationship between farm produce and poultry operations.
* Added the need to record farm produce transferred to support poultry.
* Aligned finance requirements with the approved basic finance direction, including income and sales where applicable.
* Clarified that ERA-IPMS is not intended to provide full accounting functionality in the initial scope.
* Added project and activity management requirements.
* Clarified search, dashboard, reporting, and controlled-access needs.
* Separated initial system needs from future capabilities.
* Added a requirements and change-control note to prevent unsupported assumptions from being implemented during later stages.
* Maintained the requirement that real beneficiary information must not be used for development or testing.

### Documentation Decision

The Needs Assessment now represents the current operational needs baseline and is aligned with the approved Concept Note and README.

Detailed software requirements, permissions, workflows, and database structures will be defined in subsequent documentation and must remain consistent with this baseline.

### Verification

* Needs Assessment reviewed against the approved Concept Note.
* Needs Assessment reviewed against the updated README.
* Five-title model aligned.
* Title, permission, and responsibility terminology aligned.
* Finance scope aligned with basic finance management.
* Poultry and small farm relationship aligned.
* Record-level access requirement retained.
* Future capabilities separated from initial requirements.
* No application or database architecture changes introduced.

### Next Step

Review and update the **Stakeholder Analysis** as the next documentation-baseline step.

## 2026-09-05 - Stakeholder Analysis Documentation Baseline

### Objective

Review and align the ERA-IPMS Stakeholder Analysis with the approved Concept Note, README, and Needs Assessment before proceeding to detailed software requirements.

### Work Completed

* Reviewed the existing Stakeholder Analysis.
* Updated the document from version 1.0 to version 1.1.
* Corrected the outdated treatment of operational functions as separate system roles.
* Aligned the stakeholder analysis with the five approved initial system titles:

  * Admin
  * Director
  * Programme Coordinator
  * Finance
  * Member
* Clarified the distinction between stakeholders, titles, permissions, and responsibilities.
* Defined field work, community support, poultry, farm, and M&E as responsibilities that may be assigned according to organisational requirements.
* Confirmed the Director's programme and M&E oversight position.
* Confirmed Finance as the initial financial management title.
* Confirmed Admin as the system administration title.
* Clarified that technical authority does not automatically provide programme decision-making authority.
* Preserved beneficiaries, persons with disabilities, vulnerable community members, partners, and service providers as important stakeholders without direct system access in the initial version.
* Added stakeholder influence and interest classifications.
* Added stakeholder communication and engagement guidance.
* Added stakeholder validation responsibilities.
* Added stakeholder risks and considerations.
* Confirmed that stakeholder categories must not be converted directly into database roles or permissions without further requirements analysis.

### Documentation Decision

The Stakeholder Analysis now represents the current stakeholder baseline and is aligned with the Concept Note, README, and Needs Assessment.

The document confirms that stakeholder identity, system title, permission, and operational responsibility are separate concepts.

Detailed permissions and access rules will be formalised in the Software Requirements Specification and User Roles and Permissions documents.

### Verification

* Stakeholder Analysis reviewed against the approved project baseline.
* Five-title model aligned.
* Stakeholder and role terminology aligned.
* Operational responsibilities separated from system titles.
* Beneficiary and external stakeholder access restrictions retained.
* Programme, finance, administration, and technical responsibilities clarified.
* No application or database architecture changes introduced.

### Next Step

Review and update the **Software Requirements Specification (SRS)** as the next documentation-baseline step.

## 2026-09-05 - Software Requirements Specification Documentation Baseline

### Objective

Review and align the ERA-IPMS Software Requirements Specification with the approved Concept Note, README, Needs Assessment, and Stakeholder Analysis before proceeding to detailed permissions, workflows, and database design.

### Work Completed

* Reviewed the existing Software Requirements Specification version 1.0.
* Identified outdated role definitions and requirements.
* Updated the SRS from version 1.0 to version 1.1.
* Replaced the outdated seven-role model with the five approved initial titles:

  * Admin
  * Director
  * Programme Coordinator
  * Finance
  * Member
* Clarified the distinction between:

  * Titles
  * Permissions
  * Responsibilities
* Added dynamic title and permission management requirements.
* Added record-level access requirements.
* Clarified that technical system administration authority does not automatically provide programme decision-making authority.
* Aligned project creation and management with the approved governance direction.
* Added referral submission and approval requirements.
* Added beneficiary archiving/inactivation requirements.
* Aligned poultry requirements with poultry groups, quantity tracking, production, feed, health, deaths, and sales.
* Added farm-to-poultry feed and produce transfer tracking.
* Aligned small farm requirements with crops, activities, harvests, transfers, and expenses.
* Expanded basic finance requirements to include relevant sales and income.
* Clarified that the initial finance module is basic financial management and not full accounting.
* Aligned staff and volunteer requirements with the title and responsibility model.
* Added permission-aware dashboards and reporting.
* Added backend-enforced record-level access requirements.
* Added auditability requirements for important system actions.
* Updated the technology direction to Python, Django, MariaDB/MySQL, HTML, CSS, and JavaScript.
* Confirmed VS Code as the primary development environment.
* Added requirements traceability and change-control guidance.
* Updated MVP requirements and acceptance criteria.
* Kept advanced mobile, notification, integration, external-access, and multi-organisation features outside the initial MVP.

### Documentation Decision

The SRS now represents the current detailed requirements baseline for ERA-IPMS.

The SRS confirms that operational functions such as field work, poultry, farm, and M&E are responsibilities that may be assigned to users and are not automatically separate system titles.

The SRS also confirms that access must be controlled using titles, permissions, responsibilities, and record-level rules rather than relying only on broad role-based access.

### Verification

* SRS reviewed against the approved project baseline.
* Five-title model aligned.
* Title, permission, and responsibility terminology aligned.
* Record-level access requirement added.
* Referral approval requirement aligned.
* Beneficiary archive/inactivation direction aligned.
* Poultry and farm requirements aligned.
* Farm-to-poultry transfer requirement aligned.
* Basic finance scope aligned.
* Technology direction aligned with Django and MariaDB/MySQL.
* Future scope separated from MVP requirements.
* No application or database architecture changes introduced.

### Commit

Planned commit message:

`Update software requirements specification baseline`

### Next Step

Review and update the **User Roles and Permissions** document as the next documentation-baseline step.

## Step 6 - User Roles and Permissions Baseline

**Date:** September 2026

### Work Completed

The ERA-IPMS User Roles and Permissions document was reviewed against the current Project Concept Note, README, Needs Assessment, Stakeholder Analysis, and Software Requirements Specification baseline.

The previous seven-role model was replaced with the approved five-title model:

1. Admin
2. Director
3. Programme Coordinator
4. Finance
5. Member

The document now distinguishes:

* Title
* Permission
* Responsibility

The revised access model also formalises:

* Least-privilege access.
* Record-level access.
* Responsibility-based access.
* Project and activity assignment.
* Technical administration versus programme authority.
* Dynamic/custom titles.
* Referral submission and approval separation.
* Beneficiary archive/inactivation principles.
* Financial access restrictions.
* Member contribution and beneficiary access rules.
* Audit and accountability requirements.

The revised permission matrix provides the baseline for the later application access-control implementation.

### Consistency Decisions

The old fixed roles for Field Staff / Volunteer, Farm Personnel, and Monitoring & Evaluation Personnel are no longer treated as initial system titles.

Those functions are represented through the Member title and assigned responsibilities where applicable, while Director, Programme Coordinator, and Finance retain their approved governance responsibilities.

Admin and Director are initially authorised for project creation.

The revised document is intended to remain consistent with the current SRS and README baseline.

### Status

Step 6 documentation is ready for review and commit.

No application code, database schema, or production permissions were changed during this step.

### Next Step

Proceed to **Step 7: System Workflows** only after Step 6 has been committed and pushed to GitHub.

## Step 7 - System Workflows Baseline

**Date:** September 2026

### Work Completed

The ERA-IPMS System Workflows document was reviewed and aligned with the current requirements baseline.

The previous workflow version contained several references to the obsolete seven-role model, including Field Staff / Volunteer terminology. The workflow model has now been aligned with the approved five-title architecture:

1. Admin
2. Director
3. Programme Coordinator
4. Finance
5. Member

The revised workflow baseline covers:

* Authentication.
* Access control.
* Beneficiary registration.
* Disability assessment.
* Home visits.
* Referrals.
* Referral approval.
* Referral follow-up.
* Projects.
* Activities.
* Activity assignment.
* Poultry management.
* Poultry stock.
* Egg production.
* Poultry feed.
* Poultry health.
* Poultry sales.
* Small farm operations.
* Farm harvests.
* Farm-to-poultry transfers.
* Finance.
* Financial approval.
* Staff and Member management.
* User access changes.
* Monitoring and evaluation.
* Dashboard.
* Reporting.
* Search and filtering.
* Notifications.
* Error correction.
* Data validation.
* Beneficiary archiving.
* Audit information.
* Record-level access.

The workflows now explicitly separate:

* Title from permission.
* Permission from responsibility.
* Data entry from approval.
* Operational quantities from financial transactions.
* Technical administration from programme authority.

### Consistency Decisions

The workflow model confirms that:

* Admin and Director are initially authorised for project creation.
* Programme Coordinator manages programme and project operations.
* Finance manages authorised financial transactions.
* Members operate according to assigned responsibilities and permissions.
* Beneficiary access is record-level and responsibility-aware.
* Referral creation and referral approval are separate actions.
* Farm-to-poultry transfers are traceable.
* Poultry stock is based on recorded stock movements.
* Financial records must not bypass access controls.
* Beneficiary records should normally be archived or made inactive rather than physically deleted.
* Audit information is required for important system actions.
* Reports and exports must respect permissions and record-level access.

### Outstanding Validation Items

The following require confirmation during later requirements validation:

* Exact referral approval authority.
* Exact project approval authority.
* Exact financial approval rules.
* Final workflow status values.
* Exact M&E indicators.
* Final MVP report list.
* Notification priority.
* Detailed project and activity assignment rules.
* Record correction and post-submission editing rules.

These items will not be silently resolved in code.

### Status

Step 7 documentation is ready for review and commit.

No application code or database structure was changed during this step.

### Next Step

Proceed to **Step 8: Database Entity Design** only after the Step 7 documentation has been committed and pushed to GitHub.

## Step 8: Database Entity Design Baseline

**Date:** September 2026
**Status:** Draft for review

### Work Completed

Developed the initial v1.1 database entity design for ERA-IPMS based on the approved Software Requirements Specification, User Roles and Permissions, and System Workflows.

The database design was aligned with the approved architecture and distinguishes:

* Titles from permissions.
* Permissions from responsibilities.
* Operational records from financial transactions.
* Activity assignments from activity participation.
* Beneficiary records from beneficiary service activities.
* Farm production from farm-to-poultry transfers.
* Poultry groups from individual stock movements.

### Main Entity Areas

The proposed database design covers:

* Users and authentication.
* Dynamic titles.
* Application permissions.
* Title-permission assignments.
* User responsibilities.
* Staff/member information.
* Project assignments.
* Beneficiaries.
* Disability assessments.
* Home visits.
* Referrals and referral follow-ups.
* Projects and activities.
* Activity assignments and participants.
* Poultry groups and stock movements.
* Egg production.
* Poultry feed.
* Poultry health records.
* Poultry sales.
* Farm crops and activities.
* Harvests.
* Farm-to-poultry transfers.
* Basic financial transactions.
* Monitoring and evaluation.
* Audit events.

### Important Design Decisions

The entity design establishes the following principles:

1. A user has a title, while permissions and responsibilities are represented separately.
2. Titles can be expanded by authorised administrators.
3. Permissions represent system actions such as View, Add, Edit, Delete, Approve, Export, Manage, and Administer.
4. Responsibilities represent functional areas assigned to users.
5. Beneficiary records should be archived rather than physically deleted.
6. Record-level access must be supported by appropriate relationships.
7. Project and activity access must be traceable to assignments.
8. Poultry stock should be based on stock movements rather than manually maintained totals.
9. Farm-to-poultry transfers must maintain traceability from harvest to poultry group.
10. Operational quantities and financial transactions remain separate.
11. Important system actions must be auditable.
12. The final SQL schema must be derived from the approved entity design.

### Validation Points

The following items remain subject to final validation before SQL implementation:

* Referral approval authority.
* Project approval authority.
* Financial approval rules.
* Final status values.
* M&E indicator definitions.
* Reporting requirements.
* Notification priorities.
* Detailed assignment rules.
* Post-submission correction rules.
* Beneficiary archive and restoration authority.
* Final poultry tracking requirements.
* Financial categories and payment methods.

### Implementation Impact

No production database migration or final SQL implementation was performed during this step.

The entity design will be used as the logical baseline for the next database-design stage, including the Entity Relationship Diagram and subsequent SQL schema.

### Next Step

**Step 9: Entity Relationship Diagram (ERD)**

The ERD will visually represent the approved entities, primary keys, foreign keys, cardinalities, junction entities, access-control relationships, farm-to-poultry traceability, finance relationships, and audit relationships.

## Step 9: Entity Relationship Diagram Baseline

**Date:** September 2026  
**Status:** Prepared for review and commit

### Work Completed

The existing ERA-IPMS ERD was audited against the approved Database Entity Design v1.1.

The previous ERD was identified as a legacy model because it still contained the old `roles`, `staff_volunteers`, and `poultry_transactions` structures. The v1.1 ERD was therefore prepared as a replacement baseline.

The updated ERD represents the approved database areas:

- User titles, permissions and responsibilities
- Staff members and project assignments
- Beneficiaries and disability assessments
- Home visits
- Referrals and referral follow-ups
- Projects and activities
- Activity assignments and participants
- Poultry groups and movement-based stock
- Egg production, feed, health and poultry sales
- Farm crops, activities and harvests
- Farm-to-poultry transfers
- Financial transactions
- M&E indicators and indicator records
- Audit events

### Design Decisions Preserved

- Title, permission and responsibility remain separate concepts.
- Titles remain expandable by administrators.
- Permissions remain application-defined.
- Beneficiary access remains record-level.
- Beneficiary deletion is treated as archive/inactivation.
- Activity assignment is separate from activity participation.
- Poultry stock is derived from stock movements.
- Farm-to-poultry transfer is explicitly traceable.
- Operational records remain separate from financial transactions.
- Audit events provide accountability.

### ERD Artifacts

The Step 9 baseline contains:

- `docs/database/entity_relationship_diagram.md`
- `docs/database/erd/era_ipms_erd.drawio`
- `docs/database/erd/era_ipms_erd.png`
- `docs/database/erd/era_ipms_erd.pdf`

The Draw.io file is the editable visual source. PNG and PDF are presentation artifacts.

### Validation

The ERD must be reviewed against the Database Entity Design v1.1 before the database schema is generated.

No Django model migration or production database change is included in Step 9.

### Next Step

After the ERD baseline is committed and verified clean, proceed to Step 10: `database/schema.sql`.

## Step 10 — Database Schema Baseline

**Status:** Validated in disposable MariaDB test database

### Work completed

- Replaced the legacy `database/schema.sql` structure with the approved v1.1 database schema.
- Preserved the existing `era_ipms` database by testing the schema in a separate disposable database:
  `era_ipms_schema_test`.
- Verified that the schema imports successfully into MariaDB 10.11.18.
- Verified that the schema creates 31 tables.
- Verified that the schema creates 56 foreign-key relationships.
- Verified that all 31 tables use InnoDB.
- Verified that all 31 tables use `utf8mb4_unicode_ci`.
- Verified key tables including:
  - `users`
  - `projects`
  - `poultry_stock_movements`
  - `financial_transactions`
  - `audit_events`

### Important schema decisions

- `users` uses `title_id` rather than the legacy `role_id`.
- Titles, permissions, and responsibilities remain separate concepts.
- Poultry inventory uses movement-based stock tracking.
- Financial transactions are separated from operational poultry/farm records.
- Audit events are included for traceability.
- Beneficiary records are designed for archival/inactivation rather than physical deletion.

### Validation results

| Validation | Result |
|---|---|
| Schema import | Passed |
| Tables created | 31 |
| Foreign keys | 56 |
| Storage engine | InnoDB |
| Table collation | utf8mb4_unicode_ci |
| Key table DDL checks | Passed |

### Safety

The schema was **not executed against the existing `era_ipms` database**. The existing database remains separate from the disposable schema test database.

The schema is a database design/install baseline and is **not a migration script** for the existing database.

### Next step

Proceed to application/database integration only after the schema baseline is committed and pushed.