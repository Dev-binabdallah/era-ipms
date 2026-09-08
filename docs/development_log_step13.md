# Step 13 — Referral Approval Workflow

**Date:** September 2026  
**Status:** Implemented; local test execution required

## Objective

Implement the first explicit referral approval workflow while preserving the
ERA-IPMS separation between permissions, responsibilities, and record-level
access.

## Existing Baseline

The approved database design already provides referral approval fields:

- `status`
- `approved_by`
- `approved_at`

The referral API creates every new referral with `status="submitted"` and does
not trust a client-supplied status value.

## Work Completed

### Approval Endpoint

Added:

`POST /referrals/<referral_id>/approve/`

The endpoint:

1. Requires authentication.
2. Requires the `APPROVE` permission for the `referrals` resource.
3. Uses the existing referral record as the authorization record context.
4. Accepts approval only when the current status is `submitted`.
5. Changes the status to `approved`.
6. Records the approving user in `approved_by`.
7. Records the approval timestamp in `approved_at`.
8. Updates `updated_at`.
9. Rejects repeated approval with HTTP `409`.
10. Rejects approval from any non-`submitted` status with HTTP `409`.
11. Returns HTTP `404` when the referral does not exist.

### Authorization

The implementation uses the existing centralized authorization service and
`PERMISSION_APPROVE`. No new hard-coded title is introduced for approval.

This means approval authority remains assignable through the existing title,
permission, responsibility, and record-scope model rather than being silently
assigned to a particular job title in application code.

## Status Transition

Current implemented transition:

```text
submitted  ->  approved
```

No other referral status is changed by this endpoint.

The broader referral lifecycle remains:

```text
submitted
    |
    +--> approved
           |
           +--> follow-up required
           |
           +--> completed
           |
           +--> not completed
           |
           +--> cancelled
```

The downstream transitions require separate validation before implementation.

## Tests Added

Added `backend/core/tests/test_referral_approval_api.py` covering:

- Unauthenticated request → `401`.
- Unauthorized request → `403`.
- Successful submitted → approved transition.
- Approval metadata recording.
- Already approved referral → `409`.
- Invalid source status → `409`.
- Missing referral → `404`.

## Important Validation Decision

The existing requirements documentation identifies the exact referral approval
authority as a validation item. Therefore this implementation deliberately
checks the `APPROVE` permission and referral responsibility through the
central authorization system instead of hard-coding `Director` or `Programme
Coordinator` as the sole approver.

The exact organisational assignment of `APPROVE` for referrals should be
confirmed before production permissions are seeded.

## Database Impact

No schema change is introduced by this step. The existing `referrals` table
already contains `status`, `approved_by`, and `approved_at`.

## Next Step

Run the focused referral approval tests and then the complete Django test
suite locally. After all tests pass, review the referral status lifecycle and
implement the validated follow-up/completion transitions as the next workflow
increment.
