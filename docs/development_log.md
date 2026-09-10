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
## Step 11 — Django Application Model Baseline

**Status:** Validated against MariaDB schema v1.1

### Work completed

- Replaced the legacy Django model definitions in `backend/core/models.py`.
- Aligned the Django application models with the approved database schema v1.1.
- Replaced the legacy role-based model structure with the approved:
  - titles
  - permissions
  - responsibilities
  - user responsibilities
  - project assignments
- Replaced legacy staff/volunteer and poultry transaction structures with the approved v1.1 entities.
- Added the application model representations for:
  - beneficiaries and disability assessments
  - home visits
  - referrals and referral follow-ups
  - projects and activities
  - activity assignments and participants
  - poultry groups and stock movements
  - egg production, feed, health, and poultry sales
  - farm crops, activities, harvests, and farm-to-poultry transfers
  - financial transactions
  - M&E indicators and indicator records
  - audit events
- Updated the `Users` model to use `title_id` instead of the legacy `role_id`.
- Added Django authentication interface properties required by the custom authentication backend.
- Kept the application models unmanaged because the MariaDB schema remains the authoritative database structure and existing database migration requires a deliberate migration plan.

### Validation results

| Validation | Result |
|---|---|
| Django system check | Passed |
| Django model count | 31 |
| Database schema table count | 31 |
| Model/schema table mapping | Matched |
| Model/schema column mapping | Matched |
| Foreign-key mappings | Passed |
| Foreign-key constraints | 56 |
| Unique constraints | 15 |
| InnoDB tables | 31 |
| utf8mb4_unicode_ci tables | 31 |
| `managed = False` models | 31 |
| Model relationship `on_delete` audit | Passed |
| Legacy model check | Passed |

### Database validation

The v1.1 Django models were validated against the disposable MariaDB test database:

`era_ipms_model_test`

The existing `era_ipms` database was not used as the validation target because it contains the legacy database structure and requires a separate migration plan.

### Important implementation boundary

The Django model baseline does **not** constitute a migration of the existing database.

No Django migration was generated or applied for the v1.1 model baseline.

The existing MariaDB database must be migrated deliberately after the legacy-to-v1.1 migration strategy has been reviewed and approved.

### Next step

After Step 11 is committed, pushed, and verified clean, proceed to application/database integration and authentication alignment.

## Step 12A — Authentication Backend Alignment

**Status:** Validated against Django models and disposable MariaDB test database

### Work completed

- Updated the custom authentication backend to use the approved `Users` model structure.
- Replaced the legacy `role` relationship with the approved `title` relationship.
- Added authentication using either:
  - username
  - email address
- Added identifier trimming and empty-identifier rejection.
- Added safe handling for ambiguous username/email matches.
- Preserved inactive-user rejection.
- Updated `get_user()` to use the current `Users` model and `title` relationship.
- Kept authentication based on the existing MariaDB `users` table.
- Did not modify the database schema or generate Django migrations.

### Validation results

| Validation | Result |
|---|---|
| Django system check | Passed |
| Username authentication | Passed |
| Email authentication | Passed |
| Incorrect password rejection | Passed |
| Inactive user rejection | Passed |
| `get_user()` lookup | Passed |
| `Users.title` relationship | Passed |
| Legacy role references in `core/auth` | None |
| `git diff --check` | Passed |

### Database validation

Authentication behavior was tested against the disposable MariaDB database:

`era_ipms_model_test`

Temporary test users and titles were created for validation and removed after testing.

### Implementation boundary

This step aligns the authentication backend with the approved title-based user model.

It does **not** yet address:
- authentication views
- URL structure
- Django settings cleanup
- login/logout presentation
- authorization and permission enforcement
- record-level access enforcement

Those will be handled as separate logical development steps.

### Next step

Proceed to authentication view and URL alignment after Step 12A is committed and verified clean.

## 2026-09-06 — Step 13.14B: Record-Level Authorization Scope

### Objective

Complete the record-level authorization layer for ERA-IPMS by enforcing approved project and activity scope relationships across operational resources.

The authorization model must evaluate access through the approved layered sequence:

1. Authentication and active user status.
2. Active user title.
3. Required title permission.
4. Required responsibility.
5. Active responsibility assignment.
6. Applicable project scope.
7. Applicable activity scope where required.

Unknown resources must not receive authorization through an unrestricted scope fallback.

### Work Completed

* Extended `backend/core/authorization/service.py` to implement explicit record-level project/activity scope resolution.
* Added project-scope inheritance for activity participants through:
  `activity_participants → activities → projects`.
* Added project-scope enforcement for poultry groups through:
  `poultry_groups → projects`.
* Added project-scope inheritance for poultry operational records through their poultry group relationship:

  * poultry stock movements
  * egg production
  * feed records
  * poultry health records
  * poultry sales
* Added project-scope enforcement for farm crops through:
  `farm_crops → projects`.
* Added project-scope inheritance for farm activities through:
  `farm_activities → farm_crops → projects`.
* Added project-scope inheritance for harvests through:
  `harvests → farm_crops → projects`.
* Added cross-domain scope validation for farm-to-poultry transfers:

  * farm-side project is resolved through the harvest/crop relationship;
  * poultry-side project is resolved through the poultry group;
  * both projects must match;
  * the user must have active scope for that project.
* Added project-scope enforcement for financial transactions through their project relationship.
* Added project-scope enforcement for M&E indicators through their project relationship.
* Added project-scope inheritance for M&E indicator records through:
  `me_indicator_records → me_indicators → projects`.
* Preserved explicit handling for beneficiary and beneficiary-related resources where the current schema does not provide a project relationship.
* Changed the scope fallback so that unknown resources are denied rather than automatically granted scope.
* Removed the obsolete `backend/core/tests.py` Django placeholder because it conflicted with the real `backend/core/tests/` test package during Django test discovery.
* Preserved the actual authorization test package:
  `backend/core/tests/test_authorization_service.py`.
* Expanded authorization tests to cover record-level project inheritance, denial without project scope, cross-domain scope validation, and unknown-resource denial.

### Schema Alignment Supporting Authorization

The record-level authorization implementation was preceded by live-schema alignment required to support approved domain relationships.

The following relationships were aligned and verified:

* `egg_production.poultry_group_id`
* `feed_records.poultry_group_id`
* `poultry_health_records.poultry_group_id`
* `farm_crops.project_id`
* `me_indicators.project_id`
* `me_indicators.status`
* `me_indicators.updated_at`
* `referrals.updated_at`

The corresponding live foreign keys and indexes were verified.

The canonical Django models, MariaDB schema, and active database were subsequently checked for column alignment.

### Verification

Full Django test discovery and execution completed successfully:

```text
Found 63 test(s).
System check identified no issues (0 silenced).

Ran 63 tests in 0.179s

OK
```

Authorization coverage includes:

* authentication and active-user checks;
* active-title checks;
* title-permission checks;
* responsibility eligibility;
* active responsibility assignments;
* permission + responsibility integration;
* resource-to-responsibility mapping;
* project scope;
* activity scope;
* activity assignment;
* project inheritance for related records;
* cross-domain farm/poultry project matching;
* denial of records outside the user's project scope;
* denial of unknown resources.

Additional repository validation:

```text
git diff --check
```

passed with no errors.

The full Django suite completed without creating or modifying a test database:

```text
Skipping setup of unused database(s): default.
```

### Authorization Design Decision

Record-level authorization is now explicitly relationship-driven.

The service does not infer scope from arbitrary object attributes. Each supported resource has an explicit approved relationship through which project or activity scope is resolved.

Unknown resources are denied.

Project scope is required where the approved schema provides a project relationship. Activity resources additionally require both:

1. active project assignment; and
2. active activity assignment.

Responsibility assignment remains independent from project/activity scope. Possessing a responsibility does not grant access outside the user's assigned project or activity scope.

Administrative technical authority remains separate from programme responsibility.

### Current Limitation

Beneficiary and beneficiary-derived records such as disability assessments, home visits, referrals, and referral follow-ups do not currently inherit project scope because the approved current schema does not provide a project relationship from beneficiaries to projects.

This is therefore not treated as an implicit project-scope relationship.

Any future beneficiary/project scoping requirement must be addressed through an explicitly approved schema or policy change rather than inferred in the authorization service.

### Repository State

Step 13.14B is validated and ready for the documentation/commit checkpoint.

Current intended changes are limited to:

* `backend/core/authorization/service.py`
* `backend/core/tests/test_authorization_service.py`
* removal of obsolete `backend/core/tests.py`
* `docs/development_log.md`

No commit or push is included in this step.

### Next Step

Review the completed Step 13.14B documentation and working-tree diff.

After review, create the agreed logical commit for the authorization record-level scope implementation and documentation, then push it to the repository.

## Step 13.15 — Authorization Enforcement at Django View/API Boundary

### Objective

Establish a reusable Django authorization boundary that enforces authentication, permission, responsibility, and record-level scope checks before protected views execute.

### Work Completed

* Added `backend/core/authorization/decorators.py`.
* Implemented the `require_permission()` decorator as the Django view/API authorization boundary.
* Centralized authorization decisions through `AuthorizationService`.
* Added support for all approved permissions:

  * VIEW
  * ADD
  * EDIT
  * DELETE
  * APPROVE
  * EXPORT
  * MANAGE
  * ADMINISTER
* Added optional `record_getter` support for record-level authorization.
* Added optional `context_getter` support for project/activity authorization context.
* Enforced HTTP 401 responses for unauthenticated requests.
* Enforced HTTP 403 responses for authenticated but unauthorized requests.
* Kept `ADMINISTER` as a dedicated technical administration authorization check.
* Required a resource for all non-administration permissions.
* Updated the authorization service documentation to reflect the existing record-level project/activity scope implementation.
* Added dedicated authorization-boundary tests covering authentication, authorization denial, successful execution, record/context propagation, ADD handling, ADMINISTER handling, and decorator validation.

### Verification

The authorization boundary implementation passed:

* Python compilation checks.
* `git diff --check`.
* Authorization boundary test suite: **11 tests passed**.
* Full Django test suite: **74 tests passed**.
* Django system check: **clean**.
* No operational CRUD/API endpoints were introduced.
* No database migrations or data mutations were performed.

### Database Decision

No database schema changes are required for this step. The existing authorization schema and approved record-level relationships are consumed by the authorization service; the new decorator provides the Django boundary for applying those decisions.

### Design Decision

Authorization remains centralized in `AuthorizationService`. The Django boundary does not duplicate permission, responsibility, project, activity, or record-level policy logic. Views provide the appropriate resource, record, and/or context to the authorization service through the decorator.

### Current Limitation

Beneficiary-centered resources that do not have an approved project/activity relationship cannot inherit project scope from the current schema. They remain outside project-derived record-level scope until an explicit domain relationship is approved.

### Next Step

**Step 13.16 — Authorization-aware querysets and data filtering.**

The next step will address filtering querysets so users receive only records within their authorized project/activity scope, rather than relying solely on per-request boundary checks.

## 2026-09-08 — Referral Management API

### Objective
Implement the Referral Management API using the existing MariaDB/MySQL authoritative schema and project authorization architecture.

### Work completed
- Added Referral API support using the existing `Referrals` Django model.
- Added referral collection routing at `/referrals/`.
- Implemented `GET /referrals/` for authorized referral listing.
- Implemented `POST /referrals/` for authorized referral creation.
- Applied the existing `VIEW` and `ADD` authorization permissions for referrals.
- Used `authorized_queryset()` for referral retrieval.
- Added validation for JSON payloads, required fields, beneficiary ID, and referral date format.
- Set referral status server-side to `submitted` during creation so clients cannot arbitrarily set workflow status.
- Added 13 focused Referral API tests covering authentication, authorization, successful GET/POST behavior, validation errors, unsupported methods, and server-controlled referral status.

### Verification
- Django system check: passed.
- Focused Referral API tests: 13/13 passed.
- Full core test suite: 183/183 passed.
- `git diff --check`: passed.

### Database decision
No database migration or schema change was required. The existing authoritative `referrals` table is represented by the existing Django model.

### Workflow decision
Referral approval authority and final status-transition rules were not hard-coded because the current authoritative workflow documentation does not yet define them sufficiently. The approval workflow should be implemented only after those authorities and transitions are explicitly confirmed.

### Next step
Proceed to the Referral approval/workflow milestone once the required approval authority and status-transition rules are confirmed.

## 2026-09-08 — Referral Follow-Up Management API

### Objective

Extend the Referral Management API with referral follow-up creation and retrieval while enforcing the existing centralized authorization architecture and record-level access rules.

### Work completed

- Added `ReferralFollowUps` API support using the existing MariaDB/MySQL authoritative schema.
- Added referral follow-up collection routing at:
  `/referrals/<referral_id>/follow-ups/`
- Implemented `POST /referrals/<referral_id>/follow-ups/` for authorized follow-up creation.
- Implemented `GET /referrals/<referral_id>/follow-ups/` for authorized follow-up listing.
- Added referral lookup and validation for referral IDs.
- Added validation for JSON request bodies and required `follow_up_date`.
- Added ISO date validation for follow-up dates.
- Set `conducted_by` from the authenticated user rather than accepting it from the client.
- Set `created_at` server-side.
- Applied centralized `VIEW` and `ADD` authorization through `require_permission()`.
- Added referral-aware record-level authorization for referral follow-ups.
- Extended authorization scope handling so referrals inherit beneficiary record-level scope.
- Extended follow-up authorization so follow-ups inherit the authorization scope of their parent referral.
- Added focused tests for authorized and unauthorized follow-up creation and listing.
- Preserved the existing authoritative MariaDB/MySQL schema; no database migration was introduced.

### Verification

- Django system check: passed.
- Combined referral and authorization test suite: **96/96 passed**.
- `git diff --check`: passed.
- Working tree was clean after the Referral Follow-Up implementation was committed.
- Commit created: `6ac492e Implement referral follow-up management API`.

### Authorization decision

Referral follow-ups are authorized through their parent referral rather than being treated as independently scoped records.

The authorization chain is:

`Referral Follow-Up → Referral → Beneficiary`

This preserves the existing record-level authorization architecture and prevents a user from accessing a follow-up merely because they possess the general follow-up responsibility.

### Current limitation

A nonexistent parent referral may currently result in an authorization denial before the view-level existence check can return a `404` response. This behavior is intentionally left for a later refinement rather than mixing it into the completed Referral Follow-Up API milestone.

### Database decision

No database schema changes or migrations were required. The existing `referrals` and `referral_follow_ups` tables remain authoritative.

### Next step

Proceed to the Referral approval/workflow milestone only after the required referral approval authority and status-transition rules are explicitly confirmed.


## 2026-09-08 — Referral Submission Workflow (Step 14B)

### Objective

Separate referral creation from referral submission so that a newly created referral enters the `pending` state and must be explicitly submitted before it can proceed to approval.

### Work completed

- Changed referral creation so new referrals are created with `status="pending"` rather than `status="submitted"`.
- Added the referral submission endpoint: `POST /referrals/<referral_id>/submit/`.
- Applied the existing `PERMISSION_EDIT` authorization to referral submission.
- Used the existing referral record as the record-level authorization context.
- Restricted submission to referrals currently in the `pending` state.
- Implemented the workflow transition: `pending -> submitted`.
- Prevented repeated submission of an already submitted referral.
- Rejected submission from other referral statuses with HTTP `409`.
- Preserved `approved_by` and `approved_at` during submission so approval remains a separate action.
- Updated `updated_at` when a referral is submitted.
- Added six focused tests covering authentication, authorization, missing referrals, repeated submission, invalid source status, and successful submission.
- Updated existing referral creation tests to expect the new initial `pending` status.

### Authorization decision

Referral submission uses the existing centralized authorization architecture:

`PERMISSION_EDIT + referral record-level authorization`

No new title-specific submission authority was introduced.

### Status transition

The implemented referral workflow now separates creation, submission, and approval:

    Create Referral
          |
          v
       pending
          |
          | Submit
          v
      submitted
          |
          | Approve
          v
       approved

Referral approval remains a separate action governed by the existing `PERMISSION_APPROVE` authorization.

### Tests and verification

Local verification completed before committing:

- Focused Referral API tests: **23/23 passed**.
- Full Django `core` test suite: **199/199 passed**.
- Django system check: **clean**.
- `git diff --check`: **clean**.

### Database decision

No database schema changes or migrations were required. The existing authoritative referrals table already supports the required referral status and approval fields.

### Implementation commit

Implementation committed locally as:

`7113db5 Implement referral submission workflow`

### Next step

Continue with the next validated referral workflow increment, while preserving the requirement that referral creation/submission and referral approval remain separate actions.


## 2026-09-10 — Disability Assessment Beneficiary Validation

### Objective

Harden disability assessment creation by ensuring that every assessment references an existing beneficiary before the assessment record is created.

### Work completed

- Added explicit beneficiary existence validation to disability assessment creation.
- The API now looks up the beneficiary using the supplied `beneficiary_id` before creating the assessment.
- Added HTTP `404` handling when the beneficiary does not exist.
- Standardized the error response as:

      {"error": "Beneficiary not found"}

- Changed assessment creation to use the validated beneficiary object rather than assigning an unvalidated foreign-key ID.
- Updated the existing successful disability assessment creation test to mock and verify beneficiary lookup.
- Added a regression test covering creation with a missing beneficiary.
- Preserved the existing permission check before beneficiary validation.
- No database schema or migration changes were required.

### Validation decision

Beneficiary existence is now explicitly validated at the API boundary before a disability assessment can be created.

This prevents invalid beneficiary references from reaching the assessment creation operation and provides a clear client-facing `404` response.

### Tests and verification

Local verification completed:

- Missing-beneficiary regression test: **1/1 passed**.
- Complete disability assessment API tests: **12/12 passed**.
- Full Django `core` test suite: **257/257 passed**.
- Django system check: **clean**.
- `git diff --check`: **clean**.

The full `core` suite increased from 256 to 257 tests because of the new regression test, with no existing test failures.

### Database decision

No database schema changes or migrations were required. The existing `beneficiaries` and `disability_assessments` tables remain authoritative.

### Implementation status

The disability assessment creation endpoint and its tests are validated and ready to be committed together with this development-log update.

### Next step

Continue API validation hardening with the next beneficiary-related creation endpoint, applying the same controlled process:

1. Add a regression test.
2. Verify the test fails for the expected reason.
3. Implement the smallest production change.
4. Run focused tests.
5. Run the full `core` suite.
6. Update the development log.
7. Commit the complete verified increment.


## 2026-09-10 — Home Visit Beneficiary Validation

### Objective

Harden home visit creation by ensuring that every home visit references an existing beneficiary before the home visit record is created.

### Work completed

- Added explicit beneficiary existence validation to home visit creation.
- The API now looks up the beneficiary using the supplied `beneficiary_id` before creating the home visit.
- Added HTTP `404` handling when the beneficiary does not exist.
- Standardized the error response as:

      {"error": "Beneficiary not found"}

- Changed home visit creation to use the validated beneficiary object rather than assigning an unvalidated foreign-key ID.
- Updated the existing successful home visit creation test to mock and verify beneficiary lookup.
- Added a regression test covering creation with a missing beneficiary.
- Preserved the existing permission check before beneficiary validation.
- No database schema or migration changes were required.

### Validation decision

Beneficiary existence is now explicitly validated at the API boundary before a home visit can be created.

This prevents invalid beneficiary references from reaching the home visit creation operation and provides a clear client-facing `404` response.

### Tests and verification

Local verification completed:

- Missing-beneficiary regression test: **1/1 passed**.
- Complete home visit API tests: **12/12 passed**.
- Full Django `core` test suite: **258/258 passed**.
- Django system check: **clean**.
- `git diff --check`: **clean**.

The full `core` suite increased from 257 to 258 tests because of the new regression test, with no existing test failures.

### Database decision

No database schema changes or migrations were required. The existing `beneficiaries` and `home_visits` tables remain authoritative.

### Implementation status

The home visit creation endpoint and its tests are validated and ready to be committed together with this development-log update.

### Next step

Continue API validation hardening with the next beneficiary-related creation endpoint, applying the same controlled process:

1. Add a regression test.
2. Verify the test fails for the expected reason.
3. Implement the smallest production change.
4. Run focused tests.
5. Run the full `core` suite.
6. Update the development log.
7. Commit the complete verified increment.
