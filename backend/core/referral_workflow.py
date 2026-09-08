from django.http import JsonResponse
from django.utils import timezone

from core.authorization.constants import PERMISSION_APPROVE
from core.authorization.decorators import require_permission
from core.models import Referrals


def get_referral(request, referral_id):
    try:
        referral_id = int(referral_id)
    except (TypeError, ValueError):
        return None

    if referral_id <= 0:
        return None

    try:
        return Referrals.objects.get(referral_id=referral_id)
    except Referrals.DoesNotExist:
        return None


@require_permission(
    permission=PERMISSION_APPROVE,
    resource="referrals",
    record_getter=get_referral,
)
def referral_approve(request, referral_id):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        referral_id = int(referral_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "referral_id must be an integer"},
            status=400,
        )

    if referral_id <= 0:
        return JsonResponse(
            {"error": "referral_id must be a positive integer"},
            status=400,
        )

    try:
        referral = Referrals.objects.get(referral_id=referral_id)
    except Referrals.DoesNotExist:
        return JsonResponse(
            {"error": "Referral not found"},
            status=404,
        )

    if referral.status == "approved":
        return JsonResponse(
            {"error": "Referral is already approved"},
            status=409,
        )

    if referral.status != "submitted":
        return JsonResponse(
            {
                "error": (
                    "Referral cannot be approved from status "
                    f"'{referral.status}'"
                )
            },
            status=409,
        )

    now = timezone.now()

    referral.status = "approved"
    referral.approved_by_id = request.user.user_id
    referral.approved_at = now
    referral.updated_at = now
    referral.save(
        update_fields=(
            "status",
            "approved_by",
            "approved_at",
            "updated_at",
        )
    )

    return JsonResponse(
        {
            "referral": {
                "referral_id": referral.referral_id,
                "beneficiary_id": referral.beneficiary_id,
                "referral_date": referral.referral_date,
                "destination": referral.destination,
                "reason": referral.reason,
                "referred_by_id": referral.referred_by_id,
                "status": referral.status,
                "approved_by_id": referral.approved_by_id,
                "approved_at": referral.approved_at,
                "created_at": referral.created_at,
                "updated_at": referral.updated_at,
            }
        }
    )
