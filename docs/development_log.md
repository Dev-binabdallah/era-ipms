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