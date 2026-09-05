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
