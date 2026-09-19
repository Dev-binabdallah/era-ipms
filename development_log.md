## 2026-09-15 — Assignment Authorization Boundary Tests

### Objective
Strengthen regression coverage for activity and project assignment
authorization boundaries.

### Work Completed
- Added an unauthenticated activity assignment creation test verifying
  HTTP 401.
- Added an unauthenticated activity assignment update test verifying
  HTTP 401.
- Added an unauthenticated project assignment creation test verifying
  HTTP 401.
- Added an unauthorized project assignment creation test verifying
  HTTP 403.
- Added an unauthenticated project assignment update test verifying
  HTTP 401.
- Added an unauthorized project assignment update test verifying
  HTTP 403.
- Confirmed that the tests exercise the existing authorization decorators
  without changing production authorization logic.

### Validation
- Activity assignment API tests: passed
- Project API tests: passed
- Full `core` test suite: passed
- Django system check: clean
- `git diff --check`: clean

### Database Decision
No database schema changes or migrations were required. This increment
contains test-only changes.

### Implementation Status
**Complete.**

## 2026-09-14 — Activity Collection Authentication Boundary Tests

### Objective
Strengthen regression coverage at the activity collection API boundary by
verifying that unauthenticated requests are still rejected when requests
enter through the collection dispatcher.

### Work Completed
- Added a GET collection-boundary test for `/activities/` verifying that an
  unauthenticated request returns HTTP 401.
- Added a POST collection-boundary test for `/activities/` verifying that an
  unauthenticated request returns HTTP 401.
- Tests execute the real `activities_collection` dispatcher rather than
  mocking the delegated handlers, confirming that the dispatcher preserves
  the existing authorization path.
- Confirmed that no production application code was changed.

### Validation
- Activity API tests: **34/34 passed**
- Full `core` test suite: **317/317 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Database Decision
No database schema changes or migrations were required. This increment
contains test-only changes.

### Implementation Status
**Complete.**

## 2026-09-14 — Activity List API Endpoint

### Objective
Implement and validate the protected Activity List API endpoint while
preserving the existing Activity Creation API behavior.

### Work completed
- Added `GET /activities/` through a dedicated `activities_list()` endpoint.
- Protected activity listing with the existing `PERMISSION_VIEW` authorization
  path for the `activities` resource.
- Applied `authorized_queryset()` to activity listing so returned activities
  remain restricted by the user's authorization scope.
- Added an `activities_collection()` dispatcher for the `/activities/`
  collection endpoint:
  - `GET` requests are routed to `activities_list()`;
  - `POST` requests continue to use the existing `activities_create()` flow;
  - unsupported methods return HTTP `405`.
- Updated the main URL configuration to route `/activities/` through the
  collection dispatcher.
- Added API regression tests covering:
  - unauthenticated activity listing;
  - unauthorized activity listing;
  - authorized activity listing and queryset authorization;
  - GET collection dispatch;
  - POST collection dispatch; and
  - unsupported collection methods.

### Verification
- Full Django `core` test suite — **301/301 PASSED**
- Django system check — **PASSED**
- `git diff --check` — **PASSED**

### Database decision
No database migration or schema change was required. The endpoint reads from
the existing `activities` table and uses the existing authorization/queryset
infrastructure.

### Implementation status
**Complete.**

### Next step
Review the development-log update and final Git diff, then stage the Activity
List API implementation, its tests, and `development_log.md` together for
commit.

## 2026-09-13 — Activity Edit Authorization and Role-Based Activity Querysets

### Objective
Add dedicated authorization for editing activities and correct activity queryset
scoping so Programme Coordinators and Members receive access according to their
roles and assignment scope.

### Work completed
- Added `AuthorizationService.can_edit_activity()` for existing activity edits.
- Required active authentication and an active user title before activity editing.
- Required the `PROJECT_ACTIVITIES` responsibility for activity editing.
- Allowed Programme Coordinators to edit activities when they have:
  - the `MANAGE` permission; and
  - active scope over the activity's parent project.
- Allowed Members to edit activities when they have:
  - the `EDIT` permission; and
  - active scope over the activity; including an active assignment to that
    activity and active scope over its parent project.
- Denied activity editing for Directors and unsupported roles through the
  dedicated activity edit authorization path.
- Denied activity editing for inactive users and inactive titles.
- Updated `authorized_queryset()` for activities so:
  - Programme Coordinators receive activities within their active project scope;
  - Members receive only activities within their active project scope and with
    an active assignment to the activity; and
  - other roles receive an empty queryset.
- Added authorization regression tests covering Programme Coordinator,
  Member, Director, inactive-user, inactive-title, permission, responsibility,
  project-scope, and activity-assignment cases.
- Added queryset regression tests covering Programme Coordinator project scope,
  Member activity assignment scope, and unsupported roles.

### Verification
- Authorization service tests — 105/105 PASSED
- Authorization queryset tests — 18/18 PASSED
- Activity API tests — 11/11 PASSED
- Activity assignment API tests — 19/19 PASSED
- Full `core` test suite — 280/280 PASSED
- Django system check — PASSED
- `git diff --check` — PASSED

### Database decision
No database migration or schema change was required. This increment changes
authorization logic and queryset filtering only.

### Implementation status
**Complete.**

### Next step
Review the development log and final Git diff, then stage the activity
authorization changes and `development_log.md` together for commit.


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

## 2026-09-09 — Activity Management API

### Objective

Implement the Activity creation API using the existing MariaDB/MySQL authoritative
schema and project-scoped authorization architecture.

### Work completed

- Added Activity creation at `POST /activities/`.
- Added project-based authorization for Activity creation.
- Required `ADD` permission and `PROJECT_ACTIVITIES` responsibility.
- Required the authenticated user to have an active assignment to the parent project.
- Added validation for JSON payloads, project ID, activity name, responsible user ID,
  and activity date.
- Validated that the responsible user exists and is active.
- Added a dedicated Activity creation authorization decorator because the Activity
  record does not exist at authorization time.
- Added Activity creation authorization service tests covering permission,
  responsibility, and project-scope requirements.
- Added Activity creation decorator tests covering authentication, authorization,
  project resolution, and invalid project input.
- Added Activity API tests covering authentication, authorization, validation,
  successful creation, and responsible-user validation.
- Added the Activity creation route to the Django URL configuration.
- Did not introduce a database migration or alter the authoritative MariaDB schema.

### Verification

- Activity API tests — 10/10 PASSED
- Activity creation decorator tests — 7/7 PASSED
- Activity authorization service tests — 4/4 PASSED
- Full `core` test suite — 226/226 PASSED
- Django system check — PASSED
- `git diff --check` — PASSED

### Database decision

No database migration or schema change was required. The existing authoritative
`activities` table is represented by the existing Django `managed = False` model.

### Next step

Review the complete Activity Management milestone, verify the development log,
then stage and commit the validated changes before continuing with the next
ERA-IPMS core module.

## Activity Assignment Authorization

- Added `AuthorizationService.can_assign_activity()` to enforce authorization for activity assignment.
- Restricted activity assignment to active users with an active `Programme Coordinator` title.
- Required `MANAGE` permission and `PROJECT_ACTIVITIES` responsibility.
- Required active project scope over the activity's parent project.
- Intentionally did not require an existing activity assignment because the operation creates or changes the assignment.
- Added authorization tests covering successful assignment authorization and denial for missing permission, missing responsibility, missing project scope, incorrect title, inactive user, and inactive title.
- Full test suite verified with `python backend/manage.py test core.tests -v 2`: 234 tests passed.

## Activity Assignment Workflow

- Added activity assignment management endpoints for listing, creating, reactivating, and updating activity assignments.
- Added dedicated activity-assignment authorization enforcement at the view boundary.
- Restricted activity assignment management to authorized Programme Coordinators with the required MANAGE permission, PROJECT_ACTIVITIES responsibility, and active parent-project scope.
- Added activity assignment routes under the activity resource.
- Implemented inactive-target-user validation and 404 handling for missing activities, users, and assignments.
- Implemented reactivation of existing assignments using status='assigned', with updated assignment timestamp and assigning user.
- Implemented PATCH status updates while preventing modification of other assignment fields.
- Added 18 activity assignment API tests covering authorization, validation, creation, reactivation, listing, updating, error handling, and method restrictions.
- Full regression verified with `python backend/manage.py test core.tests -v 2`: 252 tests passed.

## 2026-09-09 — Referral Approval Authorization Verification

### Objective
Verify referral approval authorization against the authoritative referral workflow,
role permissions, beneficiary scope rules, and existing approval endpoint.

### Work completed
- Confirmed the User Roles and Permissions documentation requires referral approval to be performed by an authorised person with the appropriate `APPROVE` permission.
- Confirmed Members may create and submit referrals but do not receive approval authority automatically.
- Verified the existing authorization service applies referral responsibility, permission, and beneficiary scope checks.
- Added authorization service tests confirming an authorized Director can approve referrals, including referrals for unrelated beneficiaries.
- Added tests confirming Members and Programme Coordinators without `APPROVE` permission cannot approve referrals.
- Reviewed the referral approval endpoint tests and confirmed the existing workflow transition is `submitted -> approved`.
- Reviewed the requirements and workflow documentation and retained the existing `pending -> submitted -> approved` implementation because the requirements explicitly include `Submitted`, while the workflow documentation does not define a sufficiently precise replacement transition.
- Confirmed no production code or database schema changes were required for this verification.

### Verification
- Referral authorization service tests — 88/88 PASSED
- Referral approval API tests — 6/6 PASSED
- Full `core` test suite — 256/256 PASSED
- Django system check — PASSED

### Documentation decision
The requirements list `Pending`, `Submitted`, and `Approved` as supported referral statuses,
while the workflow diagram shows `Submit -> Pending -> Authorised Reviewer`. The documentation
does not provide enough additional detail to justify changing the implemented `pending -> submitted
-> approved` lifecycle, so no status-transition change was made.

### Next step
Review the updated development log and Git diff, then stage, commit, and push the validated
referral approval authorization tests before continuing with the next ERA-IPMS workflow milestone.

## 2026-09-11 — Activity Assignment Status Validation

### Objective
Ensure activity assignment status updates accept only documented controlled status values.

### Work completed
- Added validation for the activity assignment `status` field during status updates.
- Allowed assignment statuses are:
  - `assigned`
  - `completed`
  - `cancelled`
- Rejected missing, empty, non-string, and unsupported status values.
- Preserved the existing restriction that only the `status` field can be modified through the assignment update endpoint.
- Added a regression test confirming an unsupported status returns HTTP `400`.
- Confirmed an invalid status does not modify the assignment or call `save()`.

### Verification
- Activity Assignment API tests — 19/19 PASSED
- Full `core` test suite — 261/261 PASSED
- Django system check — PASSED
- `git diff --check` — PASSED

### Database decision
No database migration or schema change was required. The existing
`activity_assignments.status` column already supports the controlled status values.

### Implementation status
**Complete.**

### Next step
Review the final Git diff, then stage, commit, and push the validated
activity assignment status changes before continuing with the next
ERA-IPMS API validation increment.

## 2026-09-13 — Project Assignment Management Authorization Tests

### Objective
Add focused authorization regression coverage for project assignment management.

### Work completed
- Added tests for `AuthorizationService.can_manage_project_assignments()`.
- Confirmed project assignment management is allowed when the user has:
  - the `MANAGE` permission; and
  - the `PROJECT_COORDINATION` responsibility.
- Confirmed project assignment management does not require an existing assignment
  to the project being managed.
- Confirmed access is denied when the required `MANAGE` permission is missing.
- Confirmed access is denied when the required `PROJECT_COORDINATION`
  responsibility is missing.
- Confirmed inactive users cannot manage project assignments.
- Confirmed users with inactive titles cannot manage project assignments.
- Updated the shared authorization scope test helper so tests can explicitly
  represent authenticated state, user activity, title name, and title activity.

### Verification
- Authorization scope tests — 48/48 PASSED
- Full `core` test suite — 267/267 PASSED
- Django system check — PASSED
- `git diff --check` — PASSED

### Database decision
No database migration or schema change was required. This increment adds
authorization regression coverage only.

### Implementation status
**Complete.**

### Next step
Review the development log and final Git diff, then stage the authorization
tests and `development_log.md` together for commit.

## 2026-09-13 — Project Assignment Management API

### Objective
Implement and validate the project assignment management API with dedicated
authorization, project scoping, and safe assignment lifecycle handling.

### Work completed
- Added a dedicated project assignment management authorization path through
  `AuthorizationService.can_manage_project_assignments()`.
- Required the `MANAGE` permission and `PROJECT_COORDINATION` responsibility
  for project assignment management.
- Intentionally did not require existing project membership because the
  operation may create the first project assignment.
- Added protected project assignment endpoints for:
  - listing project assignments;
  - creating or reactivating a project assignment; and
  - updating the assignment active state.
- Ensured assignment updates are scoped to the requested project so an
  assignment belonging to another project cannot be modified through the
  endpoint.
- Rejected inactive target users when creating project assignments.
- Reactivated an existing inactive user-project assignment instead of creating
  a duplicate assignment, consistent with the database unique constraint.
- Restricted assignment PATCH operations to the `is_active` field.
- Added API regression coverage for authorization, creation, reactivation,
  listing, deactivation, invalid target users, and project-scoped updates.

### Verification
- Project API tests — 38/38 PASSED
- Full `core` test suite — 267/267 PASSED
- Django system check — PASSED
- `git diff --check` — PASSED

### Database decision
No database migration or schema change was required. The implementation
uses the existing `user_project_assignments` schema and its unique
`(user_id, project_id)` constraint.

### Implementation status
**Complete.**

### Next step
Review the final Git diff and development log, then stage the project
assignment implementation and `development_log.md` together for commit.

## 2026-09-13 — Activity Edit API Endpoint and Authorization Enforcement

### Objective
Implement and validate the protected Activity Edit API endpoint using the
dedicated activity edit authorization path.

### Work completed
- Added a dedicated `require_activity_edit` decorator.
- Enforced `AuthorizationService.can_edit_activity()` before an existing
  activity can be modified.
- Added explicit HTTP behavior for:
  - unauthenticated requests — `401`;
  - unauthorized activity edits — `403`; and
  - missing activities — `404`.
- Added `PATCH /activities/<activity_id>/` for updating existing activities.
- Restricted updates to approved editable activity fields.
- Protected the activity ID, parent project, audit timestamps, and direct
  responsible-user object field from modification.
- Added validation for:
  - activity name;
  - activity date format;
  - responsible user ID;
  - responsible user existence and active status; and
  - controlled activity status values.
- Updated the activity `updated_at` timestamp on successful edits.
- Registered the Activity Edit endpoint in the main URL configuration.
- Added API regression tests covering authorization, protected fields,
  unknown fields, invalid JSON, validation failures, responsible-user
  validation, method restrictions, and successful authorized updates.

### Verification
- Activity API tests — 26/26 PASSED
- Full `core` test suite — 295/295 PASSED
- Django system check — PASSED
- `git diff --check` — PASSED

### Database decision
No database migration or schema change was required. The implementation
updates the existing `activities` model fields and uses the existing
responsible-user relationship.

### Implementation status
**Complete.**

### Next step
Review the final development log and staged Git diff, then commit and push
the validated Activity Edit API implementation together with
`development_log.md`.

## 2026-09-14 — Collection Dispatcher Regression Test Coverage

### Objective
Strengthen API regression coverage for collection endpoints by explicitly
verifying that HTTP methods dispatch to the correct list or create handler.

### Work Completed
- Added explicit GET dispatcher tests for collection endpoints:
  - projects;
  - beneficiaries;
  - disability assessments;
  - home visits;
  - referrals; and
  - referral follow-ups.
- Added explicit POST dispatcher tests for the same collection endpoints.
- Added explicit unsupported-method (`405`) coverage for:
  - projects; and
  - referral follow-ups.
- Verified that each dispatcher calls only the expected delegated handler
  and passes the original request and referral ID where applicable.
- Added the missing `referral_follow_ups_collection` test import.
- No production application code was changed.

### Validation
- Targeted API tests: **141/141 passed**
- Full `core` test suite: **315/315 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Database Decision
No database schema changes or migrations were required. This increment
contains test-only changes.

### Implementation Status
**Complete.**

### Next Step
Review the updated development log and complete staged-diff verification,
then commit the dispatcher regression coverage and `development_log.md`
together.

## 2026-09-14 — Poultry Stock Movement API Endpoints

### Objective

Implement protected API endpoints for recording and listing poultry stock movements while enforcing the existing poultry responsibility and project-scope authorization rules.

### Work Completed

- Added a protected `POST /poultry-stock-movements/create/` endpoint for creating poultry stock movements.
- Added a protected `GET /poultry-stock-movements/` endpoint for listing poultry stock movements.
- Enforced the existing `POULTRY_OPERATIONS` responsibility through the authorization system.
- Required the appropriate `ADD` permission when creating a stock movement.
- Required the appropriate `VIEW` permission when listing stock movements.
- Added poultry group lookup before creating a stock movement.
- Added project-scope validation to ensure the selected poultry group belongs to a project within the user's authorized scope.
- Used the existing authorized queryset mechanism to restrict stock movement listings to the user's authorized poultry and project scope.
- Added validation for required `poultry_group_id`, `movement_date`, `movement_type`, and `quantity` fields.
- Added `404` handling when the requested poultry group does not exist.
- Added `405` handling for unsupported HTTP methods.
- Added `400` handling for invalid JSON and missing required data.
- Added stock movement API regression tests covering authorized creation, missing poultry groups, missing required data, project-scope restrictions, authentication, authorization, and authorized listing.
- Verified the targeted stock movement test suite with 9 passing tests.
- Verified the complete `core` test suite with 340 passing tests.
- Verified Django system checks with no issues.
- Verified the working tree changes with `git diff --check`.

### Verification

- `python backend/manage.py test core -v 2` → 340 tests passed.
- `python backend/manage.py check` → no issues.
- `git diff --check` → clean.

### Review

The implementation uses the existing authorization and queryset patterns and keeps the stock movement endpoints simple and consistent with the poultry group API. No unrelated project changes were included in this increment.

## 2026-09-14 — Poultry Group API Endpoints

### Objective

Implement the first poultry operational API endpoints for creating and listing poultry groups while enforcing the existing poultry responsibility and project-scope authorization rules.

### Work Completed

- Added a protected `POST /poultry-groups/create/` endpoint for creating poultry groups.
- Added a protected `GET /poultry-groups/` endpoint for listing poultry groups.
- Enforced the existing `POULTRY_OPERATIONS` responsibility through the authorization system.
- Required the appropriate `ADD` permission when creating a poultry group.
- Required the appropriate `VIEW` permission when listing poultry groups.
- Added project-scope validation before poultry group creation.
- Used the existing authorized queryset mechanism to restrict poultry group listings to projects within the user's authorized scope.
- Added validation for required `project_id` and `group_name` fields.
- Added `404` handling when the requested project does not exist.
- Added `405` handling for unsupported HTTP methods.
- Added `400` handling for invalid JSON.
- Added `409` handling when a poultry group with the same name already exists in the same project.
- Added API regression tests covering:
  - unauthenticated requests;
  - unauthorized requests;
  - authorized poultry group creation;
  - project-scope restrictions;
  - authorized poultry group listing; and
  - duplicate poultry group creation.
- No database schema or migration changes were required because the existing `poultry_groups` table and its unique `(project_id, group_name)` constraint already support the implementation.

### Validation

Local verification completed:

- Poultry API tests: **8/8 passed**
- Full Django `core` test suite: **331/331 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Poultry group operations continue to use the existing authorization architecture rather than introducing a separate poultry-specific permission system.

The poultry group resource is mapped to the existing `POULTRY_OPERATIONS` responsibility, and project scope is inherited from the poultry group's parent project.

### Database Decision

No database schema changes or migrations were required.

The existing `poultry_groups` table remains authoritative, including its unique constraint preventing duplicate group names within the same project.

### Implementation Status

**Complete.**

### Next Step

Review the updated development log and complete the final Git staging and verification process. The poultry API implementation and the corresponding development-log update should be committed together.

## 2026-09-17 — Egg Production API Endpoints

### Objective

Implement protected API endpoints for recording and listing egg production for poultry groups while using the existing poultry responsibility, permission, and project-scope authorization rules.

### Work Completed

- Added a protected `POST /egg-production/create/` endpoint for recording egg production.
- Added a protected `GET /egg-production/` endpoint for listing egg production records.
- Required the existing `ADD` permission when recording egg production.
- Required the existing `VIEW` permission when listing egg production.
- Used the existing `egg_production` resource authorization and poultry project-scope rules.
- Added poultry group lookup before recording egg production.
- Added project-scope validation to ensure the selected poultry group belongs to a project within the user's authorized scope.
- Added validation for required `poultry_group_id`, `production_date`, `eggs_produced`, `eggs_used`, and `eggs_sold` fields.
- Added `404` handling when the requested poultry group does not exist.
- Added `400` handling for missing or invalid egg production data.
- Added validation to prevent negative egg quantities.
- Added validation to prevent eggs used and sold from being greater than eggs produced.
- Calculated `eggs_remaining` automatically from the production, used, and sold quantities.
- Recorded the user responsible for entering the production record.
- Added API regression tests covering authentication, authorization, project scope, validation, creation, and authorized listing.
- No database schema or migration changes were required because the existing `egg_production` table and Django model already support the implementation.

### Validation

Local verification completed:

- Egg Production API tests: **12/12 passed**
- Full Django `core` test suite: **352/352 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Egg production operations continue to use the existing authorization architecture.

The `egg_production` resource uses the existing `POULTRY_OPERATIONS` responsibility, and production records inherit project scope through their related poultry group.

### Database Decision

No database schema changes or migrations were required.

The existing `egg_production` table remains authoritative, including its relationship to `poultry_groups` and `users`.

### Implementation Status

**Complete.**

### Next Step

Review the final changes, stage the Egg Production API implementation and development-log updates together, and complete the Git commit after final verification.

## 2026-09-17 — Feed Records API Endpoints

### Objective

Implement protected API endpoints for recording and listing feed records for poultry groups while using the existing poultry responsibility, permission, and project-scope authorization rules.

### Work Completed

- Added a protected `POST /feed-records/create/` endpoint for recording feed records.
- Added a protected `GET /feed-records/` endpoint for listing feed records.
- Required the existing `ADD` permission when creating feed records.
- Required the existing `VIEW` permission when listing feed records.
- Used the existing `feed_records` resource authorization and poultry project-scope rules.
- Added poultry group lookup before creating a feed record.
- Added project-scope validation to ensure the selected poultry group belongs to a project within the user's authorized scope.
- Added validation for required `poultry_group_id`, `record_date`, and `quantity` fields.
- Added validation for numeric quantity and cost values.
- Added validation to prevent negative quantity and cost values.
- Added `404` handling when the requested poultry group does not exist.
- Added `400` handling for missing or invalid feed record data.
- Recorded the user responsible for entering the feed record.
- Added API regression tests covering authentication, authorization, project scope, validation, creation, and authorized listing.
- No database schema or migration changes were required because the existing feed records table and Django model already support the implementation.

### Validation

Local verification completed:

- Feed Records API tests: **13/13 passed**
- Full Django `core` test suite: **365/365 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Feed record operations continue to use the existing authorization architecture.

The `feed_records` resource uses the existing `POULTRY_OPERATIONS` responsibility, and feed records inherit project scope through their related poultry group.

### Database Decision

No database schema changes or migrations were required.

The existing feed records table remains authoritative, including its relationship to `poultry_groups` and `users`.

### Implementation Status

**Complete.**

### Next Step

Review the final Feed Records API changes, stage the API implementation and both development-log updates together, and complete the Git commit after final verification.

## 2026-09-17 - Poultry Health Records API Endpoints

### Objective

Implement protected API endpoints for recording and listing poultry health records while using the existing poultry responsibility, permission, and project-scope authorization rules.

### Work Completed

- Added a protected `POST /poultry-health-records/create/` endpoint for recording poultry health records.
- Added a protected `GET /poultry-health-records/` endpoint for listing poultry health records.
- Required the existing `ADD` permission when creating health records.
- Required the existing `VIEW` permission when listing health records.
- Used the existing `poultry_health_records` resource authorization and poultry project-scope rules.
- Added poultry group lookup before creating a health record.
- Added project-scope validation to ensure the selected poultry group belongs to a project within the user's authorized scope.
- Added validation for required `poultry_group_id`, `record_date`, `condition_type`, and `number_affected` fields.
- Added validation to ensure `number_affected` is an integer and cannot be negative.
- Added support for optional `description`, `action_taken`, and `outcome` fields.
- Recorded the user responsible for entering the health record.
- Added `404` handling when the requested poultry group does not exist.
- Added `400` handling for missing, invalid, or negative health record data.
- Added API regression tests covering authorization, project scope, validation, creation, listing, and HTTP methods.
- No database schema or migration changes were required because the existing poultry health records table and Django model already support the implementation.

### Validation

Local verification completed:

- Poultry Health Records API tests: **12/12 passed**
- Full Django `core` test suite: **377/377 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Poultry health record operations continue to use the existing authorization architecture.

The `poultry_health_records` resource uses the existing `POULTRY_OPERATIONS` responsibility, and health records inherit project scope through their related poultry group.

### Database Decision

No database schema changes or migrations were required.

The existing `poultry_health_records` table remains authoritative, including its relationship to `poultry_groups` and `users`.

### Implementation Status

**Complete.**

### Next Step

Stage the Poultry Health Records API implementation and both development-log updates together, review the staged changes, and complete the Git commit after final verification.

## 2026-09-17 - Poultry Sales API Endpoints

### Objective

Implement protected API endpoints for recording and listing poultry sales while using the existing poultry responsibility, permission, and project-scope authorization rules.

### Work Completed

- Added a protected `POST /poultry-sales/create/` endpoint for recording poultry sales.
- Added a protected `GET /poultry-sales/` endpoint for listing poultry sales.
- Required the existing `ADD` permission when creating poultry sales.
- Required the existing `VIEW` permission when listing poultry sales.
- Used the existing `poultry_sales` resource authorization and poultry project-scope rules.
- Added poultry group lookup before creating a poultry sale.
- Added project-scope validation to ensure the selected poultry group belongs to a project within the user's authorized scope.
- Added validation for required `poultry_group_id`, `sale_date`, and `quantity` fields.
- Added validation to ensure quantity is an integer and cannot be negative.
- Added validation for optional `unit_price` and `total_amount` values.
- Added validation to prevent negative unit prices and total amounts.
- Added `404` handling when the requested poultry group does not exist.
- Added `400` handling for missing or invalid poultry sale data.
- Recorded the user responsible for entering the poultry sale.
- Added API regression tests covering authorization, project scope, validation, creation, listing, and HTTP methods.
- No database schema or migration changes were required because the existing poultry sales table and Django model already support the implementation.
- Did not automatically calculate `total_amount` because the existing schema allows `unit_price` and `total_amount` to be stored independently and no existing business rule requires automatic calculation.

### Validation

Local verification completed:

- Poultry Sales API tests: **14/14 passed**
- Full Django `core` test suite: **391/391 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Poultry sale operations continue to use the existing authorization architecture.

The `poultry_sales` resource uses the existing `POULTRY_OPERATIONS` responsibility, and sales inherit project scope through their related poultry group.

### Database Decision

No database schema changes or migrations were required.

The existing `poultry_sales` table remains authoritative, including its relationship to `poultry_groups` and `users`.

### Implementation Status

**Complete.**

### Next Step

Stage the Poultry Sales API implementation and both development-log updates together, review the staged changes, and complete the Git commit after final verification.

## 2026-09-18 - Farm Crops API Endpoints

### Objective

Implement protected API endpoints for recording and listing farm crops while using the existing permission, project-scope, and authorization rules.

### Work Completed

- Added a protected `POST /farm-crops/create/` endpoint for recording farm crops.
- Added a protected `GET /farm-crops/` endpoint for listing farm crops.
- Required the existing `ADD` permission when creating farm crops.
- Required the existing `VIEW` permission when listing farm crops.
- Used the existing `farm_crops` resource authorization and project-scope rules.
- Added project lookup before creating a farm crop.
- Added project-scope validation to ensure the selected project is within the user's authorized scope.
- Added validation for required `project_id` and `crop_name` fields.
- Added validation to prevent an empty crop name.
- Added validation for the optional `planting_date` field using `YYYY-MM-DD` format.
- Added handling for invalid JSON requests.
- Recorded the user responsible for entering the farm crop.
- Added URL routes for farm crop creation and listing.
- Added API regression tests covering authentication, permissions, project scope, validation, creation, listing, and HTTP methods.
- No database schema or migration changes were required because the existing `farm_crops` table and Django model already support the implementation.

### Validation

Local verification completed:

- Farm Crops API tests: **13/13 passed**
- Full Django `core` test suite: **404/404 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Farm crop operations use the existing authorization architecture.

The `farm_crops` resource uses the existing project-scoped authorization rules, and farm crops are accessible only within projects available to the user.

### Database Decision

No database schema changes or migrations were required.

The existing `farm_crops` table remains authoritative, including its relationship to `projects` and `users`.

### Implementation Status

**Complete.**

### Next Step

Stage the Farm Crops API implementation, its regression tests, and the development-log update together, review the staged changes, and complete the Git commit after final verification.

## 2026-09-19 - Farm Activities API Endpoints

### Objective

Implement protected API endpoints for recording and listing farm activities while using the existing permission, crop scope, project scope, and authorization rules.

### Work Completed

- Added a protected `POST /farm-activities/create/` endpoint for recording farm activities.
- Added a protected `GET /farm-activities/` endpoint for listing farm activities.
- Required the existing `ADD` permission when creating farm activities.
- Required the existing `VIEW` permission when listing farm activities.
- Used the existing `farm_activities` authorization and project-scope rules.
- Added crop lookup before creating a farm activity.
- Added project-scope validation through the selected farm crop.
- Added validation for required `crop_id`, `activity_date`, and `activity_type` fields.
- Added validation to prevent an empty activity type.
- Added validation for `activity_date` using `YYYY-MM-DD` format.
- Added handling for invalid JSON requests.
- Recorded the current user as the user responsible for entering the farm activity.
- Added URL routes for farm activity creation and listing.
- Added 13 API regression tests covering authentication, permissions, crop and project scope, validation, creation, listing, and HTTP methods.
- No database schema or migration changes were required because the existing `farm_activities` table and Django model already support the implementation.

### Validation

Local verification completed:

- Farm Activities API tests: **13/13 passed**
- Full Django `core` test suite: **417/417 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Farm activity operations use the existing authorization architecture.

The `farm_activities` resource uses the existing farm operations responsibility, and farm activities inherit project scope through their related farm crop.

### Database Decision

No database schema changes or migrations were required.

The existing `farm_activities` table remains authoritative, including its relationships to `farm_crops` and `users`.

### Implementation Status

**Complete.**

### Next Step

Stage the Farm Activities API implementation, its regression tests, and the development-log update together, review the staged changes, and complete the Git commit after final verification.

## 2026-09-19 - Farm Poultry Transfers API Endpoints

### Objective

Implement protected API endpoints for recording and listing transfers of farm harvests to poultry groups while using the existing permission, project scope, and authorization rules.

### Work Completed

- Added a protected `POST /farm-poultry-transfers/create/` endpoint for recording farm poultry transfers.
- Added a protected `GET /farm-poultry-transfers/` endpoint for listing farm poultry transfers.
- Required the existing `ADD` permission when creating farm poultry transfers.
- Required the existing `VIEW` permission when listing farm poultry transfers.
- Used the existing `farm_poultry_transfers` authorization and project-scope rules.
- Added harvest and poultry group lookups before creating a transfer.
- Added validation to ensure the harvest and poultry group belong to the same project.
- Added project-scope validation for the related farm project.
- Added validation for required `harvest_id`, `poultry_group_id`, `transfer_date`, and `quantity` fields.
- Added validation to ensure quantity is a valid positive number.
- Added validation for `transfer_date` using `YYYY-MM-DD` format.
- Added handling for invalid JSON requests.
- Recorded the current user as the user responsible for entering the transfer.
- Added URL routes for farm poultry transfer creation and listing.
- Added 14 API regression tests covering authentication, permissions, project matching, project scope, validation, creation, listing, and missing related records.
- No database schema or migration changes were required because the existing `farm_poultry_transfers` table and Django model already support the implementation.

### Validation

Local verification completed:

- Farm Poultry Transfers API tests: **14/14 passed**
- Full Django `core` test suite: **431/431 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Farm poultry transfer operations use the existing authorization architecture.

The `farm_poultry_transfers` resource uses the existing farm operations responsibility. A transfer is accessible only when the related harvest and poultry group belong to the same project and that project is within the user's active project scope.

### Database Decision

No database schema changes or migrations were required.

The existing `farm_poultry_transfers` table remains authoritative, including its relationships to `harvests`, `poultry_groups`, and `users`.

### Implementation Status

**Complete.**

### Next Step

Stage the Farm Poultry Transfers API implementation, its regression tests, and the development-log update together, review the staged changes, and complete the Git commit after final verification.

## 2026-09-19 - Harvest API Endpoints

### Objective

Implement protected API endpoints for recording and listing farm harvest records while using the existing permission, project scope, and authorization rules.

### Work Completed

- Added a protected `POST /harvests/create/` endpoint for recording harvests.
- Added a protected `GET /harvests/` endpoint for listing harvests.
- Required the existing `ADD` permission when creating harvests.
- Required the existing `VIEW` permission when listing harvests.
- Used the existing `harvests` authorization and farm project scope rules.
- Added crop lookup before creating a harvest.
- Added project-scope validation through the selected crop's project.
- Added validation for required `crop_id`, `harvest_date`, and `quantity` fields.
- Added validation to ensure quantity is a valid positive number.
- Added validation for `harvest_date` using `YYYY-MM-DD` format.
- Added handling for invalid JSON requests.
- Allowed optional `unit`, `usage_type`, and `notes` values.
- Recorded the current user as the user responsible for entering the harvest.
- Added URL routes for harvest creation and listing.
- Added 13 API regression tests covering authentication, permissions, validation, project scope, creation, listing, and missing related records.
- No database schema or migration changes were required because the existing `harvests` table and Django model already support the implementation.

### Validation

Local verification completed:

- Harvest API tests: **13/13 passed**
- Full Django `core` test suite: **444/444 passed**
- Django system check: **clean**
- `git diff --check`: **clean**

### Authorization Decision

Harvest operations use the existing authorization architecture.

The `harvests` resource uses the existing farm operations responsibility. A harvest is accessible only when its related crop belongs to a project within the user's active project scope.

### Database Decision

No database schema changes or migrations were required.

The existing `harvests` table remains authoritative, including its relationship to `farm_crops` and `users`.

### Implementation Status

**Complete.**

### Next Step

Stage the Harvest API implementation, its regression tests, and the development-log update together, review the staged changes, and complete the Git commit after final verification.
