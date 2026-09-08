
## 2026-09-07 — Authentication API Contract

### Objective
Complete and verify the backend authentication API contract using the existing ERA-IPMS users and roles architecture.

### Work Completed
- Implemented `POST /auth/login/`.
- Implemented `GET /auth/me/`.
- Implemented `POST /auth/logout/`.
- Authentication supports username or email address.
- Invalid credentials return HTTP 401.
- Missing credentials return HTTP 400.
- Unsupported HTTP methods return HTTP 405.
- Successful login creates a Django authenticated session.
- Logout clears the authenticated session.
- Removed the temporary `/auth/test/` endpoint.
- Added dedicated authentication API tests.
- Converted authentication API tests to `SimpleTestCase` so they do not require creation of a MariaDB test database.

### Verification
- Authentication API tests — **8/8 PASSED**
- Complete `core` test suite — **95/95 PASSED**
- Django system check — **PASSED**
- `git diff --cached --check` — **PASSED**
- Working tree — **CLEAN**
- GitHub push — **SUCCESSFUL**

### Commit
- `0cc35d2` — `Implement authentication API contract`

### Current Git State
- Local `main` and `origin/main` are synchronized at `0cc35d2`.

### Known Next Backend Issue
The `/projects/` endpoint currently applies the authorized queryset but does not yet enforce the API authentication/authorization boundary before querying. An unauthenticated request can therefore receive an empty `200` response instead of an appropriate authentication/authorization response.

### Next Step
Strengthen the `/projects/` API boundary with explicit authentication/authorization enforcement, add boundary tests, and verify the complete test suite again.

## 2026-09-07 — Projects API Authorization Boundary

### Objective
Strengthen the `/projects/` API endpoint with explicit authentication and authorization enforcement while retaining record-level filtering through the centralized authorization queryset.

### Work Completed
- Applied the existing `require_permission()` authorization boundary to `projects_list`.
- Required the `VIEW` permission for the `projects` resource.
- Unauthenticated `/projects/` requests now return HTTP 401.
- Authenticated but unauthorized `/projects/` requests now return HTTP 403.
- Authorized requests continue to use `authorized_queryset()` for project-level scope filtering.
- Added dedicated `/projects/` API tests covering authentication, authorization, and authorized queryset usage.

### Verification
- Projects API tests — **3/3 PASSED**
- Complete `core` test suite — **98/98 PASSED**
- Django system check — **PASSED**

### Current Git State
- Previous commit: `fce2f77` — `Add ERA-IPMS development log`
- Changes for this milestone are ready for review.

### Next Step
Review the complete diff, commit the Projects API authorization boundary milestone, and push it to GitHub.

## 2026-09-07 — Projects API Detail Endpoint

### Objective
Extend the authorized Projects API with a record-level project detail endpoint while preserving the existing authentication and authorization boundary.

### Work Completed
- Added `projects_detail()` endpoint for individual projects.
- Added `/projects/<int:project_id>/` URL route.
- Reused the existing `require_permission()` authorization decorator.
- Applied the existing project authorization scope to project detail access.
- Added 404 handling for nonexistent projects.
- Added focused API tests covering:
  - unauthenticated detail requests,
  - unauthorized detail requests,
  - authorized detail requests,
  - nonexistent project requests.
- Kept the existing `/projects/` list endpoint and authorization-aware queryset behavior unchanged.

### Verification
- `python -m py_compile backend/core/tests/test_projects_api.py` — passed.
- `python backend/manage.py test core.tests.test_projects_api` — **7/7 passed**.
- `python backend/manage.py test core` — **102/102 passed**.
- Django system check — **no issues**.

### Status
Project detail API implementation and regression tests are complete and passing.

### Next Step
Review the working-tree diff, commit the completed Projects API detail milestone, and push it to GitHub.

## 2026-09-07 — Projects API Create Endpoint

### Objective
Extend the authorized Projects API with a project creation endpoint while preserving the centralized authentication, responsibility, and record-level authorization model.

### Work Completed
- Added `projects_create()` for `POST /projects/`.
- Added `projects_collection()` to dispatch:
  - `GET /projects/` to the existing project list endpoint.
  - `POST /projects/` to the project creation endpoint.
  - unsupported methods to HTTP 405.
- Updated `/projects/` URL routing to use the collection dispatcher.
- Required `project_name` for project creation.
- Added JSON body validation.
- Added ISO `YYYY-MM-DD` validation for `start_date` and `end_date`.
- Made `created_by` server-controlled from the authenticated user.
- Made `project_id` server-controlled by the database.
- Made `created_at` and `updated_at` server-generated.
- Added HTTP 201 project creation response.
- Added creation API tests covering:
  - unauthenticated requests,
  - unauthorized requests,
  - authorized project creation,
  - malformed JSON,
  - non-object JSON,
  - missing project name,
  - invalid dates,
  - unsupported request methods.
- Adjusted the authorization service so top-level `ADD` operations do not require an existing record-level project/activity scope when no record or parent context exists.
- Preserved scope enforcement for `ADD` operations when a parent record/context is supplied.
- Preserved existing `VIEW`, `EDIT`, `DELETE`, `APPROVE`, `EXPORT`, `MANAGE`, and `ADMINISTER` authorization behavior.

### Verification
- `python -m py_compile backend/core/views.py` — passed.
- `python -m py_compile backend/core/tests/test_projects_api.py` — passed.
- Projects API tests — **15/15 PASSED**.
- Complete `core` test suite — **111/111 PASSED**.
- Django system check — **no issues**.

### Status
Projects API create implementation, authorization adjustment, routing, and regression tests are complete and passing.

### Next Step
Review the complete working-tree diff, verify the development log entry, commit the completed milestone, and push it to GitHub.

## 2026-09-07 — Projects API Update/Edit Endpoint

### Objective
Extend the authorized Projects API with a record-level project update endpoint using HTTP PATCH while preserving centralized authentication, responsibility, and record-level authorization.

### Work Completed
- Added `projects_update()` for `PATCH /projects/<project_id>/`.
- Reused the existing `require_permission()` authorization decorator with `PERMISSION_EDIT`.
- Applied record-level project authorization before allowing updates.
- Added `projects_detail_collection()` to dispatch:
  - `GET /projects/<project_id>/` to the existing detail endpoint.
  - `PATCH /projects/<project_id>/` to the update endpoint.
  - unsupported methods to HTTP 405.
- Added JSON request validation.
- Added partial-update support for:
  - `project_name`
  - `description`
  - `start_date`
  - `end_date`
  - `objectives`
  - `status`
- Prevented modification of server-controlled fields:
  - `project_id`
  - `created_by`
  - `created_by_id`
  - `created_at`
  - `updated_at`
- Rejected unknown fields.
- Required at least one editable field.
- Prevented blank project names.
- Added ISO `YYYY-MM-DD` date validation.
- Allowed nullable/empty date values to clear existing dates.
- Updated `updated_at` server-side on successful updates.
- Restricted database updates to the approved editable fields plus `updated_at`.
- Added comprehensive Projects API update tests covering:
  - unauthenticated requests,
  - unauthorized requests,
  - nonexistent projects,
  - authorized partial updates,
  - protected fields,
  - unknown fields,
  - empty payloads,
  - blank project names,
  - valid dates,
  - invalid dates,
  - clearing dates,
  - malformed JSON,
  - non-object JSON,
  - unsupported request methods.

### Verification
- `python -m py_compile backend/core/views.py backend/config/urls.py` — passed.
- `python -m py_compile backend/core/tests/test_projects_api.py` — passed.
- Projects API tests — **30/30 PASSED**.
- Complete `core` test suite — **126/126 PASSED**.
- Django system check — **no issues**.
- `git diff --check` — passed.

### Status
Projects API update/edit implementation, routing, authorization enforcement, validation, and regression tests are complete and passing.

### Next Step
Review the final staged diff, commit the completed Projects API update milestone, push it to GitHub, and verify the working tree is clean and synchronized.

## 2026-09-07 — Project Assignment Management API

### Objective

Implement controlled project-user assignment management while preserving the
existing ERA-IPMS authorization model and authoritative MariaDB schema.

### Work Completed

- Added dedicated project assignment authorization.
- Required both `MANAGE` permission and `PROJECT_COORDINATION` responsibility
  for project assignment management.
- Added project assignment listing endpoint:
  `GET /projects/<project_id>/assignments/`
- Added project assignment creation endpoint:
  `POST /projects/<project_id>/assignments/create/`
- Added project assignment update endpoint:
  `PATCH /projects/<project_id>/assignments/<assignment_id>/`
- Restricted assignment creation to existing active users.
- Implemented reactivation of existing inactive assignments instead of
  creating duplicate records.
- Recorded the assigning user and assignment timestamp.
- Restricted assignment updates to the `is_active` field.
- Used deactivation instead of physical assignment deletion.
- Added URL routing for all assignment endpoints.
- Added focused API tests covering authentication, authorization,
  listing, creation, reactivation, inactive users, deactivation, and
  protected-field rejection.

### Verification

- Project assignment tests — 8/8 PASSED
- Projects API tests — 38/38 PASSED
- Full `core` test suite — 134/134 PASSED
- `python backend/manage.py check` — PASSED
- `python -m py_compile backend/config/urls.py` — PASSED
- `git diff --check` — PASSED

### Database Decision

No production database migration was performed. The existing
`user_project_assignments` table remains authoritative, and Django models
remain `managed = False`.

### Next Step

Continue implementation of the next validated ERA-IPMS core module while
preserving the established authorization boundary and development log.

## 2026-09-07 — Beneficiary Record-Level Authorization

### Objective

Implement controlled beneficiary record-level access while preserving the
existing ERA-IPMS authorization model and authoritative MariaDB schema.

### Work Completed

- Added beneficiary-specific record-level authorization.
- Restricted Member beneficiary visibility to records with a direct
  operational relationship:
  - personally registered beneficiaries;
  - beneficiaries personally assessed; or
  - beneficiaries personally visited.
- Allowed Director and Programme Coordinator broader beneficiary visibility.
- Prevented unrelated roles from receiving beneficiary scope through this
  record-level authorization layer.
- Added database-level beneficiary queryset filtering using Django `Q`
  conditions.
- Removed beneficiaries from the previously unscoped resource list.
- Preserved the existing beneficiary responsibility requirement:
  `BENEFICIARY_REGISTRATION`.
- Added service-level tests for registration, assessment, home visit, and
  unrelated beneficiary access.
- Added queryset-level tests verifying direct-relationship filtering and
  broader Director access.
- Did not introduce a project foreign key or otherwise alter the authoritative
  database schema.

### Verification

- Beneficiary authorization service tests — PASSED
- Authorization service tests — 68/68 PASSED
- Authorization queryset tests — 14/14 PASSED
- Full `core` test suite — 139/139 PASSED
- `python backend/manage.py check` — PASSED
- `git diff --check` — PASSED

### Database Decision

No production database migration was performed. The existing MariaDB schema
remains authoritative, and Django models remain `managed = False`.

### Next Step

Continue implementation of the next validated ERA-IPMS core module while
preserving the established authorization boundary and development log.

## 2026-09-07 — Beneficiary Management API

### Objective

Implement the beneficiary registration and listing API while preserving
the established authorization boundary and authoritative MariaDB schema.

### Work Completed

- Added beneficiary registration through `POST /beneficiaries/`.
- Preserved beneficiary listing through `GET /beneficiaries/`.
- Applied centralized `PERMISSION_ADD` authorization to beneficiary
  registration.
- Preserved centralized `PERMISSION_VIEW` authorization for beneficiary
  listing.
- Added validation for required beneficiary fields:
  - `beneficiary_code`
  - `first_name`
  - `last_name`
- Added ISO `YYYY-MM-DD` validation for:
  - `date_of_birth`
  - `registration_date`
- Set the authenticated user as `created_by`.
- Set `created_at` and `updated_at` using the current application time.
- Defaulted beneficiary status to `active` when not supplied.
- Added API tests covering successful registration, authorization denial,
  invalid JSON, missing required fields, invalid dates, and unsupported
  methods.
- Preserved the existing beneficiary record-level authorization model.
- Added a collection dispatcher so `GET` uses `PERMISSION_VIEW` and
  `POST` uses `PERMISSION_ADD` independently.
- Did not introduce a project foreign key or otherwise alter the
  authoritative database schema.

### Verification

- Beneficiary API tests — 9/9 PASSED
- Full `core` test suite — 148/148 PASSED
- `python backend/manage.py check` — PASSED
- `git diff --check` — PASSED

### Database Decision

No production database migration was performed. The existing MariaDB
schema remains authoritative, and Django models remain `managed = False`.

### Next Step

Review the complete Git diff, commit and push the Beneficiary Management API
milestone, then continue with the next validated ERA-IPMS core module.

## 2026-09-07 — Disability Assessment Management API

### Objective

Implement the disability assessment registration and listing API while
preserving the established authorization boundary and authoritative
MariaDB schema.

### Work Completed

- Added disability assessment registration through
  `POST /disability-assessments/`.
- Added disability assessment listing through
  `GET /disability-assessments/`.
- Applied centralized `PERMISSION_ADD` authorization to assessment
  registration.
- Applied centralized `PERMISSION_VIEW` authorization to assessment
  listing.
- Added validation for required fields:
  - `beneficiary_id`
  - `assessment_date`
- Added positive-integer validation for `beneficiary_id`.
- Added ISO `YYYY-MM-DD` validation for `assessment_date`.
- Supported optional assessment fields:
  - `assessment_type`
  - `disability_type`
  - `needs`
  - `assessment_notes`
- Set the authenticated user as `assessed_by`.
- Set `created_at` using the current application time.
- Applied `authorized_queryset()` to disability assessment listing.
- Added a collection dispatcher so `GET` uses `PERMISSION_VIEW` and
  `POST` uses `PERMISSION_ADD` independently.
- Added API tests covering successful creation, authorization denial,
  authentication denial, invalid JSON, missing required fields, invalid
  beneficiary IDs, invalid dates, authorized listing, denied listing,
  and unsupported methods.
- Preserved the existing unscoped disability assessment authorization
  model.
- Did not introduce a project foreign key or otherwise alter the
  authoritative database schema.

### Verification

- Disability Assessment API tests — 11/11 PASSED
- Full `core` test suite — 159/159 PASSED
- `python -m py_compile` — PASSED
- `python backend/manage.py test core` — PASSED
- Django system check — PASSED
- `git diff --check` — PASSED

### Database Decision

No production database migration was performed. The existing MariaDB
schema remains authoritative, and Django models remain `managed = False`.

### Next Step

Review the updated Git diff, stage the Disability Assessment Management API
changes, commit and push the milestone, then continue with the next
validated ERA-IPMS core module.

## 2026-09-08 — Home Visit Management API

### Objective
Implement the Home Visit Management API using the existing MariaDB/MySQL authoritative schema and project authorization architecture.

### Work completed
- Added `HomeVisits` to the Django model layer as a `managed = False` model.
- Added Home Visit collection routing at `/home-visits/`.
- Implemented `GET /home-visits/` for authorized Home Visit listing.
- Implemented `POST /home-visits/` for authorized Home Visit creation.
- Applied the existing `VIEW` and `ADD` authorization permissions for `home_visits`.
- Used `authorized_queryset()` for Home Visit retrieval.
- Added validation for JSON payloads, required fields, beneficiary ID, and visit date format.
- Added 11 focused Home Visit API tests covering authentication, authorization, successful GET/POST behavior, validation errors, and unsupported methods.

### Verification
- Django system check: passed.
- Focused Home Visit API tests: 11/11 passed.
- Full core test suite: 170/170 passed.
- `git diff --check`: passed.

### Database decision
No database migration or schema change was required. The existing authoritative `home_visits` table is represented by a Django `managed = False` model.

### Next step
Review the complete Home Visit milestone changes, commit them, and push to GitHub.
