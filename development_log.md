
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
