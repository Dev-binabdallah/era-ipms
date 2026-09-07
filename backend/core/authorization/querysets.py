from django.db.models import F, Q

from core.authorization.constants import PERMISSION_VIEW
from core.authorization.policy import RESOURCE_RESPONSIBILITY_MAP
from core.authorization.service import authorization_service


PROJECT_RESOURCES = {
    "project",
    "projects",
    "poultry_group",
    "poultry_groups",
    "farm",
    "farms",
    "farm_crop",
    "farm_crops",
    "financial_transaction",
    "financial_transactions",
    "me_indicator",
    "me_indicators",
}

ACTIVITY_RESOURCES = {
    "activity",
    "activities",
}

ACTIVITY_PARTICIPANT_RESOURCES = {
    "activity_participant",
    "activity_participants",
}

POULTRY_RECORD_RESOURCES = {
    "poultry_stock_movement",
    "poultry_stock_movements",
    "egg_production",
    "feed_record",
    "feed_records",
    "poultry_health_record",
    "poultry_health_records",
    "poultry_sale",
    "poultry_sales",
}

FARM_CROP_CHILD_RESOURCES = {
    "farm_activity",
    "farm_activities",
    "harvest",
    "harvests",
}

FARM_POULTRY_TRANSFER_RESOURCES = {
    "farm_poultry_transfer",
    "farm_poultry_transfers",
}

ME_INDICATOR_RECORD_RESOURCES = {
    "me_indicator_record",
    "me_indicator_records",
}

UNSCOPED_RESOURCES = {
    "disability_assessment",
    "disability_assessments",
    "home_visit",
    "home_visits",
    "referral",
    "referrals",
    "follow_up",
    "follow_ups",
    "referral_follow_up",
    "referral_follow_ups",
    "disability_service",
    "disability_services",
    "community_awareness",
}


def authorized_queryset(user, resource, queryset):
    """
    Return the subset of a queryset authorized for the user.

    The queryset boundary applies:

        authentication
            -> VIEW permission
            -> resource responsibility
            -> record-level project/activity scope

    Filtering is performed at the database-query level rather than by
    loading records into Python.

    Resources without an approved project/activity relationship are
    returned unchanged after permission and responsibility checks.

    Unknown resources are denied with queryset.none().
    """

    if not getattr(user, "is_authenticated", False):
        return queryset.none()

    if not getattr(user, "is_active", False):
        return queryset.none()

    resource_name = str(resource).strip().lower() if resource else ""

    if not resource_name:
        return queryset.none()

    if resource_name not in RESOURCE_RESPONSIBILITY_MAP:
        return queryset.none()

    if not authorization_service.has_permission(
        user,
        PERMISSION_VIEW,
    ):
        return queryset.none()

    required_responsibility = (
        authorization_service.get_required_responsibility(
            resource_name,
        )
    )

    if required_responsibility is None:
        return queryset.none()

    if not authorization_service.has_responsibility(
        user,
        required_responsibility,
    ):
        return queryset.none()

    if resource_name in PROJECT_RESOURCES:
        if resource_name in {"project", "projects"}:
            return queryset.filter(
                user_assignments__user=user,
                user_assignments__is_active=True,
            ).distinct()

        return queryset.filter(
            project__user_assignments__user=user,
            project__user_assignments__is_active=True,
        ).distinct()

    if resource_name in ACTIVITY_RESOURCES:
        return queryset.filter(
            project__user_assignments__user=user,
            project__user_assignments__is_active=True,
            assignments__user=user,
            assignments__status="assigned",
        ).distinct()

    if resource_name in ACTIVITY_PARTICIPANT_RESOURCES:
        return queryset.filter(
            activity__project__user_assignments__user=user,
            activity__project__user_assignments__is_active=True,
        ).distinct()

    if resource_name in POULTRY_RECORD_RESOURCES:
        return queryset.filter(
            poultry_group__project__user_assignments__user=user,
            poultry_group__project__user_assignments__is_active=True,
        ).distinct()

    if resource_name in FARM_CROP_CHILD_RESOURCES:
        return queryset.filter(
            crop__project__user_assignments__user=user,
            crop__project__user_assignments__is_active=True,
        ).distinct()

    if resource_name in FARM_POULTRY_TRANSFER_RESOURCES:
        return queryset.filter(
            harvest__crop__project__user_assignments__user=user,
            harvest__crop__project__user_assignments__is_active=True,
            poultry_group__project__user_assignments__user=user,
            poultry_group__project__user_assignments__is_active=True,
            harvest__crop__project_id=F(
                "poultry_group__project_id"
            ),
        ).distinct()

    if resource_name in ME_INDICATOR_RECORD_RESOURCES:
        return queryset.filter(
            indicator__project__user_assignments__user=user,
            indicator__project__user_assignments__is_active=True,
        ).distinct()

    if resource_name in {"beneficiary", "beneficiaries"}:
        title_name = getattr(
            getattr(user, "title", None),
            "title_name",
            "",
        )

        if title_name in {
            "Director",
            "Programme Coordinator",
        }:
            return queryset

        return queryset.filter(
            Q(created_by=user)
            | Q(disability_assessments__assessed_by=user)
            | Q(home_visits__conducted_by=user)
        ).distinct()

    if resource_name in UNSCOPED_RESOURCES:
        return queryset

    return queryset.none()
