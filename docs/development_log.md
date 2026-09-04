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
