import json
from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import JsonResponse
from django.utils import timezone

from core.authorization.constants import (
    PERMISSION_ADD,
    PERMISSION_EDIT,
    PERMISSION_VIEW,
)
from core.authorization.decorators import (
    require_activity_creation,
    require_activity_assignment_management,
    require_activity_edit,
    require_permission,
    require_project_assignment_management,
)
from core.authorization.querysets import authorized_queryset
from core.authorization.service import authorization_service
from core.models import (
    Activities,
    ActivityAssignments,
    Beneficiaries,
    DisabilityAssessments,
    HomeVisits,
    Referrals,
    ReferralFollowUps,
    Projects,
    PoultryGroups,
    PoultryStockMovements,
    EggProduction,
    FeedRecords,
    PoultryHealthRecords,
    PoultrySales,
    UserProjectAssignments,
    Users,
)


def get_referral_beneficiary_context(request, **kwargs):
    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return {}

    if not isinstance(payload, dict):
        return {}

    beneficiary_id = payload.get("beneficiary_id")

    try:
        beneficiary_id = int(beneficiary_id)
    except (TypeError, ValueError):
        return {}

    if beneficiary_id <= 0:
        return {}

    return {"beneficiary_id": beneficiary_id}


def get_referral(request, referral_id, **kwargs):
    try:
        referral_id = int(referral_id)
    except (TypeError, ValueError):
        return None

    if referral_id <= 0:
        return None

    try:
        return Referrals.objects.get(
            referral_id=referral_id,
        )
    except Referrals.DoesNotExist:
        return None


def auth_login(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    identifier = request.POST.get("identifier", "").strip()
    password = request.POST.get("password", "")

    if not identifier or not password:
        return JsonResponse(
            {
                "authenticated": False,
                "error": "Identifier and password are required",
            },
            status=400,
        )

    user = authenticate(
        request,
        username=identifier,
        password=password,
    )

    if user is None:
        return JsonResponse(
            {
                "authenticated": False,
                "error": "Invalid credentials",
            },
            status=401,
        )

    login(request, user)

    return JsonResponse({
        "authenticated": True,
        "user_id": user.user_id,
        "username": user.username,
        "title": user.title.title_name,
    })


def auth_me(request):
    if not request.user.is_authenticated:
        return JsonResponse(
            {
                "authenticated": False,
            },
            status=401,
        )

    return JsonResponse({
        "authenticated": True,
        "user_id": request.user.user_id,
        "username": request.user.username,
        "title": request.user.title.title_name,
    })


def auth_logout(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    logout(request)

    return JsonResponse({
        "authenticated": False,
        "message": "Logged out successfully",
    })


@require_permission(
    permission=PERMISSION_ADD,
    resource="projects",
)
def projects_create(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    project_name = str(payload.get("project_name", "")).strip()

    if not project_name:
        return JsonResponse(
            {"error": "project_name is required"},
            status=400,
        )

    date_values = {}

    for field in ("start_date", "end_date"):
        value = payload.get(field)

        if value in (None, ""):
            date_values[field] = None
            continue

        try:
            date_values[field] = date.fromisoformat(str(value))
        except ValueError:
            return JsonResponse(
                {
                    "error": f"{field} must use YYYY-MM-DD format",
                },
                status=400,
            )

    now = timezone.now()

    project = Projects.objects.create(
        project_name=project_name,
        description=payload.get("description"),
        start_date=date_values["start_date"],
        end_date=date_values["end_date"],
        objectives=payload.get("objectives"),
        status=payload.get("status"),
        created_by_id=request.user.user_id,
        created_at=now,
        updated_at=now,
    )

    return JsonResponse(
        {
            "project": {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "description": project.description,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "objectives": project.objectives,
                "status": project.status,
                "created_by_id": project.created_by_id,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
        },
        status=201,
    )


@require_permission(
    permission=PERMISSION_ADD,
    resource="beneficiaries",
)
def beneficiary_create(request):
    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    required_fields = (
        "beneficiary_code",
        "first_name",
        "last_name",
    )

    for field in required_fields:
        value = str(payload.get(field, "")).strip()

        if not value:
            return JsonResponse(
                {"error": f"{field} is required"},
                status=400,
            )

        payload[field] = value

    date_values = {}

    for field in ("date_of_birth", "registration_date"):
        value = payload.get(field)

        if value in (None, ""):
            date_values[field] = None
            continue

        try:
            date_values[field] = date.fromisoformat(str(value))
        except ValueError:
            return JsonResponse(
                {
                    "error": f"{field} must use YYYY-MM-DD format",
                },
                status=400,
            )

    now = timezone.now()

    beneficiary = Beneficiaries.objects.create(
        beneficiary_code=payload["beneficiary_code"],
        first_name=payload["first_name"],
        last_name=payload["last_name"],
        date_of_birth=date_values["date_of_birth"],
        sex=payload.get("sex"),
        location=payload.get("location"),
        phone=payload.get("phone"),
        registration_date=date_values["registration_date"],
        status=payload.get("status") or "active",
        created_by_id=request.user.user_id,
        created_at=now,
        updated_at=now,
    )

    return JsonResponse(
        {
            "beneficiary": {
                "beneficiary_id": beneficiary.beneficiary_id,
                "beneficiary_code": beneficiary.beneficiary_code,
                "first_name": beneficiary.first_name,
                "last_name": beneficiary.last_name,
                "date_of_birth": beneficiary.date_of_birth,
                "sex": beneficiary.sex,
                "location": beneficiary.location,
                "phone": beneficiary.phone,
                "registration_date": beneficiary.registration_date,
                "status": beneficiary.status,
                "created_by_id": beneficiary.created_by_id,
                "created_at": beneficiary.created_at,
                "updated_at": beneficiary.updated_at,
            }
        },
        status=201,
    )


@require_permission(
    permission=PERMISSION_ADD,
    resource="disability_assessments",
)
def disability_assessment_create(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    required_fields = (
        "beneficiary_id",
        "assessment_date",
    )

    for field in required_fields:
        value = payload.get(field)

        if value in (None, ""):
            return JsonResponse(
                {"error": f"{field} is required"},
                status=400,
            )

    try:
        beneficiary_id = int(payload["beneficiary_id"])
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "beneficiary_id must be an integer"},
            status=400,
        )

    if beneficiary_id <= 0:
        return JsonResponse(
            {"error": "beneficiary_id must be a positive integer"},
            status=400,
        )

    try:
        assessment_date = date.fromisoformat(
            str(payload["assessment_date"])
        )
    except ValueError:
        return JsonResponse(
            {
                "error": "assessment_date must use YYYY-MM-DD format",
            },
            status=400,
        )

    try:
        beneficiary = Beneficiaries.objects.get(
            beneficiary_id=beneficiary_id,
        )
    except Beneficiaries.DoesNotExist:
        return JsonResponse(
            {"error": "Beneficiary not found"},
            status=404,
        )

    now = timezone.now()

    assessment = DisabilityAssessments.objects.create(
        beneficiary=beneficiary,
        assessment_date=assessment_date,
        assessment_type=payload.get("assessment_type"),
        disability_type=payload.get("disability_type"),
        needs=payload.get("needs"),
        assessment_notes=payload.get("assessment_notes"),
        assessed_by_id=request.user.user_id,
        created_at=now,
    )

    return JsonResponse(
        {
            "assessment": {
                "assessment_id": assessment.assessment_id,
                "beneficiary_id": assessment.beneficiary_id,
                "assessment_date": assessment.assessment_date,
                "assessment_type": assessment.assessment_type,
                "disability_type": assessment.disability_type,
                "needs": assessment.needs,
                "assessment_notes": assessment.assessment_notes,
                "assessed_by_id": assessment.assessed_by_id,
                "created_at": assessment.created_at,
            }
        },
        status=201,
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="disability_assessments",
)
def disability_assessments_list(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    queryset = authorized_queryset(
        request.user,
        "disability_assessments",
        DisabilityAssessments.objects.all(),
    )

    assessments = list(
        queryset.values(
            "assessment_id",
            "beneficiary_id",
            "assessment_date",
            "assessment_type",
            "disability_type",
            "needs",
            "assessment_notes",
            "assessed_by_id",
            "created_at",
        )
    )

    return JsonResponse(
        {
            "assessments": assessments,
        }
    )



@require_permission(
    permission=PERMISSION_ADD,
    resource="home_visits",
)
def home_visit_create(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    required_fields = (
        "beneficiary_id",
        "visit_date",
    )

    for field in required_fields:
        value = payload.get(field)

        if value in (None, ""):
            return JsonResponse(
                {"error": f"{field} is required"},
                status=400,
            )

    try:
        beneficiary_id = int(payload["beneficiary_id"])
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "beneficiary_id must be an integer"},
            status=400,
        )

    if beneficiary_id <= 0:
        return JsonResponse(
            {"error": "beneficiary_id must be a positive integer"},
            status=400,
        )

    try:
        visit_date = date.fromisoformat(
            str(payload["visit_date"])
        )
    except ValueError:
        return JsonResponse(
            {
                "error": "visit_date must use YYYY-MM-DD format",
            },
            status=400,
        )

    try:
        beneficiary = Beneficiaries.objects.get(
            beneficiary_id=beneficiary_id,
        )
    except Beneficiaries.DoesNotExist:
        return JsonResponse(
            {"error": "Beneficiary not found"},
            status=404,
        )

    now = timezone.now()

    visit = HomeVisits.objects.create(
        beneficiary=beneficiary,
        visit_date=visit_date,
        conducted_by_id=request.user.user_id,
        purpose=payload.get("purpose"),
        observations=payload.get("observations"),
        support_provided=payload.get("support_provided"),
        follow_up_required=payload.get("follow_up_required", False),
        next_action=payload.get("next_action"),
        created_at=now,
    )

    return JsonResponse(
        {
            "home_visit": {
                "home_visit_id": visit.home_visit_id,
                "beneficiary_id": visit.beneficiary_id,
                "visit_date": visit.visit_date,
                "conducted_by_id": visit.conducted_by_id,
                "purpose": visit.purpose,
                "observations": visit.observations,
                "support_provided": visit.support_provided,
                "follow_up_required": visit.follow_up_required,
                "next_action": visit.next_action,
                "created_at": visit.created_at,
            }
        },
        status=201,
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="home_visits",
)
def home_visits_list(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    queryset = authorized_queryset(
        request.user,
        "home_visits",
        HomeVisits.objects.all(),
    )

    visits = list(
        queryset.values(
            "home_visit_id",
            "beneficiary_id",
            "visit_date",
            "conducted_by_id",
            "purpose",
            "observations",
            "support_provided",
            "follow_up_required",
            "next_action",
            "created_at",
        )
    )

    return JsonResponse(
        {
            "home_visits": visits,
        }
    )


@require_permission(
    permission=PERMISSION_ADD,
    resource="referrals",
    context_getter=get_referral_beneficiary_context,
)
def referral_create(request):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    required_fields = (
        "beneficiary_id",
        "referral_date",
        "destination",
    )

    for field in required_fields:
        value = payload.get(field)
        if value in (None, ""):
            return JsonResponse(
                {"error": f"{field} is required"},
                status=400,
            )

    try:
        beneficiary_id = int(payload["beneficiary_id"])
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "beneficiary_id must be an integer"},
            status=400,
        )

    if beneficiary_id <= 0:
        return JsonResponse(
            {
                "error": (
                    "beneficiary_id must be a positive integer"
                )
            },
            status=400,
        )

    try:
        referral_date = date.fromisoformat(
            str(payload["referral_date"])
        )
    except ValueError:
        return JsonResponse(
            {
                "error": (
                    "referral_date must use YYYY-MM-DD format"
                )
            },
            status=400,
        )

    try:
        beneficiary = Beneficiaries.objects.get(
            beneficiary_id=beneficiary_id,
        )
    except Beneficiaries.DoesNotExist:
        return JsonResponse(
            {"error": "Beneficiary not found"},
            status=404,
        )

    now = timezone.now()

    referral = Referrals.objects.create(
        beneficiary=beneficiary,
        referral_date=referral_date,
        destination=payload["destination"],
        reason=payload.get("reason"),
        referred_by_id=request.user.user_id,
        status="pending",
        approved_by_id=None,
        approved_at=None,
        created_at=now,
        updated_at=now,
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
        },
        status=201,
    )


@require_permission(
    permission=PERMISSION_EDIT,
    resource="referrals",
    record_getter=get_referral,
)
def referral_submit(request, referral_id):
    referral = get_referral(
        request,
        referral_id,
    )

    if referral is None:
        return JsonResponse(
            {"error": "Referral not found"},
            status=404,
        )

    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    if referral.status == "submitted":
        return JsonResponse(
            {"error": "Referral is already submitted"},
            status=409,
        )

    if referral.status != "pending":
        return JsonResponse(
            {
                "error": (
                    "Referral cannot be submitted from status "
                    f"'{referral.status}'"
                )
            },
            status=409,
        )

    now = timezone.now()

    referral.status = "submitted"
    referral.updated_at = now

    referral.save(
        update_fields=[
            "status",
            "updated_at",
        ],
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


@require_permission(
    permission=PERMISSION_VIEW,
    resource="referrals",
)
def referrals_list(request):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    queryset = authorized_queryset(
        request.user,
        "referrals",
        Referrals.objects.all(),
    )

    referrals = list(
        queryset.values(
            "referral_id",
            "beneficiary_id",
            "referral_date",
            "destination",
            "reason",
            "referred_by_id",
            "status",
            "approved_by_id",
            "approved_at",
            "created_at",
            "updated_at",
        )
    )

    return JsonResponse(
        {"referrals": referrals}
    )


def referrals_collection(request):
    if request.method == "POST":
        return referral_create(request)

    if request.method == "GET":
        return referrals_list(request)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


@require_permission(
    permission=PERMISSION_ADD,
    resource="follow_ups",
    context_getter=lambda request, referral_id: {
        "referral": get_referral(
            request,
            referral_id,
        )
    },
)
def referral_follow_up_create(request, referral_id):
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
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    required_fields = (
        "follow_up_date",
    )

    for field in required_fields:
        value = payload.get(field)

        if value in (None, ""):
            return JsonResponse(
                {"error": f"{field} is required"},
                status=400,
            )

    try:
        follow_up_date = date.fromisoformat(
            str(payload["follow_up_date"])
        )
    except ValueError:
        return JsonResponse(
            {
                "error": (
                    "follow_up_date must use YYYY-MM-DD format"
                )
            },
            status=400,
        )

    try:
        referral = Referrals.objects.get(
            referral_id=referral_id,
        )
    except Referrals.DoesNotExist:
        return JsonResponse(
            {"error": "Referral not found"},
            status=404,
        )

    now = timezone.now()

    follow_up = ReferralFollowUps.objects.create(
        referral=referral,
        follow_up_date=follow_up_date,
        conducted_by_id=request.user.user_id,
        outcome=payload.get("outcome"),
        service_received=payload.get(
            "service_received",
            False,
        ),
        remaining_needs=payload.get("remaining_needs"),
        next_action=payload.get("next_action"),
        created_at=now,
    )

    return JsonResponse(
        {
            "follow_up": {
                "follow_up_id": follow_up.follow_up_id,
                "referral_id": follow_up.referral_id,
                "follow_up_date": follow_up.follow_up_date,
                "conducted_by_id": follow_up.conducted_by_id,
                "outcome": follow_up.outcome,
                "service_received": follow_up.service_received,
                "remaining_needs": follow_up.remaining_needs,
                "next_action": follow_up.next_action,
                "created_at": follow_up.created_at,
            }
        },
        status=201,
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="follow_ups",
    record_getter=get_referral,
)
def referral_follow_ups_list(request, referral_id):
    if request.method != "GET":
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
        Referrals.objects.get(
            referral_id=referral_id,
        )
    except Referrals.DoesNotExist:
        return JsonResponse(
            {"error": "Referral not found"},
            status=404,
        )

    follow_ups = list(
        ReferralFollowUps.objects.filter(
            referral_id=referral_id,
        ).values(
            "follow_up_id",
            "referral_id",
            "follow_up_date",
            "conducted_by_id",
            "outcome",
            "service_received",
            "remaining_needs",
            "next_action",
            "created_at",
        )
    )

    return JsonResponse(
        {"follow_ups": follow_ups}
    )


def referral_follow_ups_collection(request, referral_id):
    if request.method == "POST":
        return referral_follow_up_create(
            request,
            referral_id,
        )

    if request.method == "GET":
        return referral_follow_ups_list(
            request,
            referral_id,
        )

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


def home_visits_collection(request):
    if request.method == "POST":
        return home_visit_create(request)

    if request.method == "GET":
        return home_visits_list(request)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


def disability_assessments_collection(request):
    if request.method == "POST":
        return disability_assessment_create(request)

    if request.method == "GET":
        return disability_assessments_list(request)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


def beneficiaries_collection(request):
    if request.method == "POST":
        return beneficiary_create(request)

    if request.method == "GET":
        return beneficiaries_list(request)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="beneficiaries",
)
def beneficiaries_list(request):
    queryset = authorized_queryset(
        request.user,
        "beneficiaries",
        Beneficiaries.objects.all(),
    )

    beneficiaries = list(
        queryset.values(
            "beneficiary_id",
            "beneficiary_code",
            "first_name",
            "last_name",
            "date_of_birth",
            "sex",
            "location",
            "phone",
            "registration_date",
            "status",
            "created_by_id",
            "created_at",
            "updated_at",
        )
    )

    return JsonResponse(
        {
            "beneficiaries": beneficiaries,
        }
    )

@require_activity_edit
def activity_update(request, activity):
    """
    Update an existing activity.

    Authorization is enforced by require_activity_edit.
    Only activity fields owned by this endpoint may be modified.
    The parent project and audit timestamps are protected.
    """

    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    protected_fields = {
        "activity_id",
        "project",
        "project_id",
        "created_at",
        "updated_at",
        "responsible_user",
    }

    attempted_protected = sorted(
        protected_fields.intersection(payload.keys())
    )

    if attempted_protected:
        return JsonResponse(
            {
                "error": "Protected fields cannot be modified",
                "fields": attempted_protected,
            },
            status=400,
        )

    editable_fields = {
        "activity_name",
        "activity_date",
        "location",
        "responsible_user_id",
        "description",
        "status",
        "results",
    }

    unknown_fields = sorted(
        set(payload.keys()) - editable_fields
    )

    if unknown_fields:
        return JsonResponse(
            {
                "error": "Unknown fields",
                "fields": unknown_fields,
            },
            status=400,
        )

    if not payload:
        return JsonResponse(
            {"error": "At least one editable field is required"},
            status=400,
        )

    update_fields = []

    if "activity_name" in payload:
        activity_name = str(
            payload.get("activity_name", "")
        ).strip()

        if not activity_name:
            return JsonResponse(
                {"error": "activity_name is required"},
                status=400,
            )

        activity.activity_name = activity_name
        update_fields.append("activity_name")

    if "activity_date" in payload:
        activity_date = payload.get("activity_date")

        if activity_date in (None, ""):
            activity_date = None
        else:
            try:
                activity_date = date.fromisoformat(
                    str(activity_date)
                )
            except ValueError:
                return JsonResponse(
                    {
                        "error": (
                            "activity_date must use "
                            "YYYY-MM-DD format"
                        )
                    },
                    status=400,
                )

        activity.activity_date = activity_date
        update_fields.append("activity_date")

    if "location" in payload:
        activity.location = payload.get("location")
        update_fields.append("location")

    if "responsible_user_id" in payload:
        responsible_user_id = payload.get(
            "responsible_user_id"
        )

        if responsible_user_id in (None, ""):
            return JsonResponse(
                {
                    "error": (
                        "responsible_user_id is required"
                    )
                },
                status=400,
            )

        try:
            responsible_user_id = int(
                responsible_user_id
            )
        except (TypeError, ValueError):
            return JsonResponse(
                {
                    "error": (
                        "responsible_user_id must be "
                        "an integer"
                    )
                },
                status=400,
            )

        if responsible_user_id <= 0:
            return JsonResponse(
                {
                    "error": (
                        "responsible_user_id must be "
                        "a positive integer"
                    )
                },
                status=400,
            )

        try:
            responsible_user = Users.objects.get(
                user_id=responsible_user_id,
            )
        except Users.DoesNotExist:
            return JsonResponse(
                {"error": "Responsible user not found"},
                status=404,
            )

        if not responsible_user.is_active:
            return JsonResponse(
                {
                    "error": (
                        "Responsible user is inactive"
                    )
                },
                status=400,
            )

        activity.responsible_user = responsible_user
        update_fields.append("responsible_user")

    if "description" in payload:
        activity.description = payload.get("description")
        update_fields.append("description")

    if "status" in payload:
        activity_status = payload.get("status")

        allowed_statuses = {
            "Planned",
            "Ongoing",
            "Pending",
            "Completed",
            "Cancelled",
        }

        if activity_status is not None and (
            activity_status not in allowed_statuses
        ):
            return JsonResponse(
                {
                    "error": (
                        "status must be one of: "
                        "Planned, Ongoing, Pending, "
                        "Completed, Cancelled"
                    )
                },
                status=400,
            )

        activity.status = activity_status
        update_fields.append("status")

    if "results" in payload:
        activity.results = payload.get("results")
        update_fields.append("results")

    activity.updated_at = timezone.now()
    update_fields.append("updated_at")

    activity.save(update_fields=update_fields)

    return JsonResponse(
        {
            "activity": {
                "activity_id": activity.activity_id,
                "project_id": activity.project_id,
                "activity_name": activity.activity_name,
                "activity_date": activity.activity_date,
                "location": activity.location,
                "responsible_user_id": (
                    activity.responsible_user_id
                ),
                "description": activity.description,
                "status": activity.status,
                "results": activity.results,
                "created_at": activity.created_at,
                "updated_at": activity.updated_at,
            }
        },
        status=200,
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="activities",
)
def activities_list(request):
    queryset = authorized_queryset(
        request.user,
        "activities",
        Activities.objects.all(),
    )

    activities = list(
        queryset.values(
            "activity_id",
            "project_id",
            "activity_name",
            "activity_date",
            "location",
            "responsible_user_id",
            "description",
            "status",
            "results",
            "created_at",
            "updated_at",
        )
    )

    return JsonResponse(
        {
            "activities": activities,
        }
    )


@require_activity_creation
def activities_create(request, project):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    activity_name = str(payload.get("activity_name", "")).strip()

    if not activity_name:
        return JsonResponse(
            {"error": "activity_name is required"},
            status=400,
        )

    responsible_user_id = payload.get("responsible_user_id")

    if responsible_user_id in (None, ""):
        return JsonResponse(
            {"error": "responsible_user_id is required"},
            status=400,
        )

    try:
        responsible_user_id = int(responsible_user_id)
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "responsible_user_id must be an integer"},
            status=400,
        )

    if responsible_user_id <= 0:
        return JsonResponse(
            {"error": "responsible_user_id must be a positive integer"},
            status=400,
        )

    activity_date = payload.get("activity_date")

    if activity_date in (None, ""):
        activity_date = None
    else:
        try:
            activity_date = date.fromisoformat(str(activity_date))
        except ValueError:
            return JsonResponse(
                {
                    "error": (
                        "activity_date must use YYYY-MM-DD format"
                    )
                },
                status=400,
            )

    try:
        responsible_user = Users.objects.get(
            user_id=responsible_user_id,
        )
    except Users.DoesNotExist:
        return JsonResponse(
            {"error": "Responsible user not found"},
            status=404,
        )

    if not responsible_user.is_active:
        return JsonResponse(
            {"error": "Responsible user is inactive"},
            status=400,
        )

    activity_status = payload.get("status")

    if activity_status is not None:
        allowed_statuses = {
            "Planned",
            "Ongoing",
            "Pending",
            "Completed",
            "Cancelled",
        }

        if activity_status not in allowed_statuses:
            return JsonResponse(
                {
                    "error": (
                        "status must be one of: "
                        "Planned, Ongoing, Pending, Completed, Cancelled"
                    )
                },
                status=400,
            )

    now = timezone.now()

    activity = Activities.objects.create(
        project=project,
        activity_name=activity_name,
        activity_date=activity_date,
        location=payload.get("location"),
        responsible_user=responsible_user,
        description=payload.get("description"),
        status=activity_status,
        results=payload.get("results"),
        created_at=now,
        updated_at=now,
    )

    return JsonResponse(
        {
            "activity": {
                "activity_id": activity.activity_id,
                "project_id": activity.project_id,
                "activity_name": activity.activity_name,
                "activity_date": activity.activity_date,
                "location": activity.location,
                "responsible_user_id": activity.responsible_user_id,
                "description": activity.description,
                "status": activity.status,
                "results": activity.results,
                "created_at": activity.created_at,
                "updated_at": activity.updated_at,
            }
        },
        status=201,
    )


def activities_collection(request):
    if request.method == "POST":
        return activities_create(request)

    if request.method == "GET":
        return activities_list(request)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


def projects_collection(request):
    if request.method == "POST":
        return projects_create(request)

    if request.method == "GET":
        return projects_list(request)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="projects",
)
def projects_list(request):
    queryset = authorized_queryset(
        request.user,
        "projects",
        Projects.objects.all(),
    )

    projects = list(
        queryset.values(
            "project_id",
            "project_name",
            "description",
            "start_date",
            "end_date",
            "objectives",
            "status",
            "created_by_id",
            "created_at",
            "updated_at",
        )
    )

    return JsonResponse(
        {
            "projects": projects,
        }
    )


def get_project(request, project_id):
    try:
        return Projects.objects.get(
            project_id=project_id,
        )
    except Projects.DoesNotExist:
        return None


@require_permission(
    permission=PERMISSION_EDIT,
    resource="projects",
    record_getter=get_project,
)
def projects_update(request, project_id):
    project = get_project(
        request,
        project_id,
    )

    if project is None:
        return JsonResponse(
            {"error": "Project not found"},
            status=404,
        )

    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    protected_fields = {
        "project_id",
        "created_by",
        "created_by_id",
        "created_at",
        "updated_at",
    }

    attempted_protected_fields = protected_fields.intersection(payload)

    if attempted_protected_fields:
        return JsonResponse(
            {
                "error": "Protected fields cannot be modified",
                "fields": sorted(attempted_protected_fields),
            },
            status=400,
        )

    editable_fields = {
        "project_name",
        "description",
        "start_date",
        "end_date",
        "objectives",
        "status",
    }

    unknown_fields = set(payload) - editable_fields

    if unknown_fields:
        return JsonResponse(
            {
                "error": "Unknown fields",
                "fields": sorted(unknown_fields),
            },
            status=400,
        )

    if not payload:
        return JsonResponse(
            {"error": "At least one editable field is required"},
            status=400,
        )

    if "project_name" in payload:
        project_name = str(payload["project_name"]).strip()

        if not project_name:
            return JsonResponse(
                {"error": "project_name cannot be empty"},
                status=400,
            )

        project.project_name = project_name

    for field in ("description", "objectives", "status"):
        if field in payload:
            setattr(project, field, payload[field])

    for field in ("start_date", "end_date"):
        if field not in payload:
            continue

        value = payload[field]

        if value in (None, ""):
            setattr(project, field, None)
            continue

        try:
            parsed_date = date.fromisoformat(str(value))
        except ValueError:
            return JsonResponse(
                {
                    "error": f"{field} must use YYYY-MM-DD format",
                },
                status=400,
            )

        setattr(project, field, parsed_date)

    project.updated_at = timezone.now()

    project.save(
        update_fields=[
            "project_name",
            "description",
            "start_date",
            "end_date",
            "objectives",
            "status",
            "updated_at",
        ],
    )

    return JsonResponse(
        {
            "project": {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "description": project.description,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "objectives": project.objectives,
                "status": project.status,
                "created_by_id": project.created_by_id,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
        }
    )


def projects_detail_collection(request, project_id):
    if request.method == "PATCH":
        return projects_update(request, project_id)

    if request.method == "GET":
        return projects_detail(request, project_id)

    return JsonResponse(
        {"error": "Method not allowed"},
        status=405,
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="projects",
    record_getter=get_project,
)
def projects_detail(request, project_id):
    project = get_project(
        request,
        project_id,
    )

    if project is None:
        return JsonResponse(
            {
                "error": "Project not found",
            },
            status=404,
        )

    return JsonResponse(
        {
            "project": {
                "project_id": project.project_id,
                "project_name": project.project_name,
                "description": project.description,
                "start_date": project.start_date,
                "end_date": project.end_date,
                "objectives": project.objectives,
                "status": project.status,
                "created_by_id": project.created_by_id,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
            }
        }
    )


def _assignment_payload(assignment):
    return {
        "assignment_id": assignment.assignment_id,
        "user_id": assignment.user_id,
        "project_id": assignment.project_id,
        "assigned_at": assignment.assigned_at,
        "assigned_by_id": assignment.assigned_by_id,
        "is_active": assignment.is_active,
    }


def _activity_assignment_payload(assignment):
    return {
        "activity_assignment_id": assignment.activity_assignment_id,
        "activity_id": assignment.activity_id,
        "user_id": assignment.user_id,
        "assigned_at": assignment.assigned_at,
        "assigned_by_id": assignment.assigned_by_id,
        "status": assignment.status,
    }


@require_activity_assignment_management
def activity_assignments(request, activity):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    assignments = ActivityAssignments.objects.filter(
        activity=activity,
    )

    return JsonResponse(
        {
            "assignments": [
                _activity_assignment_payload(assignment)
                for assignment in assignments
            ]
        }
    )


@require_activity_assignment_management
def activity_assignment_create(request, activity):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    if "user_id" not in payload:
        return JsonResponse(
            {"error": "user_id is required"},
            status=400,
        )

    try:
        user_id = int(payload["user_id"])
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "user_id must be an integer"},
            status=400,
        )

    if user_id <= 0:
        return JsonResponse(
            {"error": "user_id must be a positive integer"},
            status=400,
        )

    try:
        target_user = Users.objects.get(
            user_id=user_id,
        )
    except Users.DoesNotExist:
        return JsonResponse(
            {"error": "Target user not found"},
            status=404,
        )

    if not target_user.is_active:
        return JsonResponse(
            {"error": "Target user is inactive"},
            status=400,
        )

    assignment = ActivityAssignments.objects.filter(
        user=target_user,
        activity=activity,
    ).first()

    now = timezone.now()

    if assignment is not None:
        assignment.status = "assigned"
        assignment.assigned_at = now
        assignment.assigned_by = request.user
        assignment.save(
            update_fields=[
                "status",
                "assigned_at",
                "assigned_by",
            ],
        )

        return JsonResponse(
            {
                "assignment": _activity_assignment_payload(
                    assignment,
                )
            }
        )

    assignment = ActivityAssignments.objects.create(
        activity=activity,
        user=target_user,
        assigned_at=now,
        assigned_by=request.user,
        status="assigned",
    )

    return JsonResponse(
        {
            "assignment": _activity_assignment_payload(
                assignment,
            )
        },
        status=201,
    )


@require_activity_assignment_management
def activity_assignment_update(
    request,
    activity,
    assignment_id,
):
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        assignment = ActivityAssignments.objects.get(
            activity_assignment_id=assignment_id,
            activity=activity,
        )
    except ActivityAssignments.DoesNotExist:
        return JsonResponse(
            {"error": "Activity assignment not found"},
            status=404,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    if not payload:
        return JsonResponse(
            {"error": "Request body is required"},
            status=400,
        )

    unexpected_keys = set(payload) - {"status"}

    if unexpected_keys:
        return JsonResponse(
            {"error": "Only status can be modified"},
            status=400,
        )

    if "status" not in payload:
        return JsonResponse(
            {"error": "status is required"},
            status=400,
        )

    status_value = payload["status"]

    if not isinstance(status_value, str) or not status_value.strip():
        return JsonResponse(
            {"error": "status must be a non-empty string"},
            status=400,
        )

    status_value = status_value.strip()
    allowed_statuses = {
        "assigned",
        "completed",
        "cancelled",
    }

    if status_value not in allowed_statuses:
        return JsonResponse(
            {
                "error": (
                    "status must be one of: "
                    "assigned, completed, cancelled"
                )
            },
            status=400,
        )

    assignment.status = status_value

    assignment.save(
        update_fields=["status"],
    )

    return JsonResponse(
        {
            "assignment": _activity_assignment_payload(
                assignment,
            )
        }
    )


@require_project_assignment_management
def project_assignments(request, project):
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    assignments = UserProjectAssignments.objects.filter(
        project=project,
    )

    return JsonResponse(
        {
            "assignments": [
                _assignment_payload(assignment)
                for assignment in assignments
            ]
        }
    )


@require_project_assignment_management
def project_assignment_create(request, project):
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    if "user_id" not in payload:
        return JsonResponse(
            {"error": "user_id is required"},
            status=400,
        )

    try:
        user_id = int(payload["user_id"])
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "user_id must be an integer"},
            status=400,
        )

    try:
        target_user = Users.objects.get(
            user_id=user_id,
        )
    except Users.DoesNotExist:
        return JsonResponse(
            {"error": "Target user not found"},
            status=404,
        )

    if not target_user.is_active:
        return JsonResponse(
            {"error": "Target user is inactive"},
            status=400,
        )

    assignment = UserProjectAssignments.objects.filter(
        user=target_user,
        project=project,
    ).first()

    now = timezone.now()

    if assignment is not None:
        assignment.is_active = True
        assignment.assigned_at = now
        assignment.assigned_by = request.user
        assignment.save(
            update_fields=[
                "assigned_at",
                "assigned_by",
                "is_active",
            ],
        )

        return JsonResponse(
            {
                "assignment": _assignment_payload(assignment),
            }
        )

    assignment = UserProjectAssignments.objects.create(
        user=target_user,
        project=project,
        assigned_at=now,
        assigned_by=request.user,
        is_active=True,
    )

    return JsonResponse(
        {
            "assignment": _assignment_payload(assignment),
        },
        status=201,
    )


@require_project_assignment_management
def project_assignment_update(
    request,
    project,
    assignment_id,
):
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        assignment = UserProjectAssignments.objects.get(
            assignment_id=assignment_id,
            project=project,
        )
    except UserProjectAssignments.DoesNotExist:
        return JsonResponse(
            {"error": "Assignment not found"},
            status=404,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    if not isinstance(payload, dict):
        return JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    if set(payload) - {"is_active"}:
        return JsonResponse(
            {
                "error": "Only is_active can be modified",
            },
            status=400,
        )

    if not payload:
        return JsonResponse(
            {"error": "is_active is required"},
            status=400,
        )

    if not isinstance(payload["is_active"], bool):
        return JsonResponse(
            {"error": "is_active must be a boolean"},
            status=400,
        )

    assignment.is_active = payload["is_active"]
    assignment.save(
        update_fields=["is_active"],
    )

    return JsonResponse(
        {
            "assignment": _assignment_payload(assignment),
        }
    )


@require_permission(permission=PERMISSION_ADD, resource="poultry_groups")
def poultry_group_create(request):
    """Create a poultry group inside a project the user can access."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    project_id = payload.get("project_id")
    group_name = payload.get("group_name")

    if not project_id or not group_name:
        return JsonResponse(
            {"error": "project_id and group_name are required"},
            status=400,
        )

    try:
        project = Projects.objects.get(project_id=project_id)
    except Projects.DoesNotExist:
        return JsonResponse({"error": "Project not found"}, status=404)

    if not authorization_service.has_project_scope(request.user, project):
        return JsonResponse(
            {"error": "You are not authorized to use this project"},
            status=403,
        )

    try:
        group = PoultryGroups.objects.create(
            project=project,
            group_name=group_name,
            poultry_category=payload.get("poultry_category"),
            breed_or_type=payload.get("breed_or_type"),
            start_date=payload.get("start_date"),
            status=payload.get("status", "active"),
            description=payload.get("description"),
            created_at=timezone.now(),
            updated_at=timezone.now(),
        )
    except IntegrityError:
        return JsonResponse(
            {
                "error": (
                    "A poultry group with this name already exists "
                    "in this project"
                )
            },
            status=409,
        )

    return JsonResponse(
        {
            "poultry_group": {
                "poultry_group_id": group.poultry_group_id,
                "project_id": group.project_id,
                "group_name": group.group_name,
                "poultry_category": group.poultry_category,
                "breed_or_type": group.breed_or_type,
                "start_date": group.start_date,
                "status": group.status,
                "description": group.description,
            }
        },
        status=201,
    )


@require_permission(permission=PERMISSION_VIEW, resource="poultry_groups")
def poultry_groups_list(request):
    """List poultry groups within the user's authorized project scope."""
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    groups = authorized_queryset(
        request.user,
        "poultry_groups",
        PoultryGroups.objects.all(),
    ).values(
        "poultry_group_id",
        "project_id",
        "group_name",
        "poultry_category",
        "breed_or_type",
        "start_date",
        "status",
        "description",
    )

    return JsonResponse({"poultry_groups": list(groups)})


@require_permission(
    permission=PERMISSION_ADD,
    resource="poultry_stock_movements",
)
def poultry_stock_movement_create(request):
    """Create a stock movement for a poultry group the user can access."""
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    poultry_group_id = payload.get("poultry_group_id")
    movement_date = payload.get("movement_date")
    movement_type = payload.get("movement_type")
    quantity = payload.get("quantity")

    if (
        poultry_group_id is None
        or movement_date in (None, "")
        or movement_type in (None, "")
        or quantity is None
    ):
        return JsonResponse(
            {
                "error": (
                    "poultry_group_id, movement_date, movement_type, "
                    "and quantity are required"
                )
            },
            status=400,
        )

    try:
        poultry_group = PoultryGroups.objects.select_related(
            "project"
        ).get(poultry_group_id=poultry_group_id)
    except PoultryGroups.DoesNotExist:
        return JsonResponse({"error": "Poultry group not found"}, status=404)

    if not authorization_service.has_project_scope(
        request.user,
        poultry_group.project,
    ):
        return JsonResponse(
            {"error": "You are not authorized to use this poultry group"},
            status=403,
        )

    movement = PoultryStockMovements.objects.create(
        poultry_group=poultry_group,
        movement_date=movement_date,
        movement_type=movement_type,
        quantity=quantity,
        description=payload.get("description"),
        recorded_by=request.user,
        created_at=timezone.now(),
    )

    return JsonResponse(
        {
            "poultry_stock_movement": {
                "movement_id": movement.movement_id,
                "poultry_group_id": movement.poultry_group_id,
                "movement_date": movement.movement_date,
                "movement_type": movement.movement_type,
                "quantity": movement.quantity,
                "description": movement.description,
                "recorded_by": movement.recorded_by_id,
                "created_at": movement.created_at,
            }
        },
        status=201,
    )


@require_permission(
    permission=PERMISSION_ADD,
    resource="egg_production",
)
def egg_production_create(request):
    """Record egg production for a poultry group the user can access."""
    if request.method != "POST":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return JsonResponse(
            {"error": "Invalid JSON"},
            status=400,
        )

    poultry_group_id = payload.get("poultry_group_id")
    production_date = payload.get("production_date")
    eggs_produced = payload.get("eggs_produced")
    eggs_used = payload.get("eggs_used")
    eggs_sold = payload.get("eggs_sold")

    if (
        poultry_group_id is None
        or production_date in (None, "")
        or eggs_produced is None
        or eggs_used is None
        or eggs_sold is None
    ):
        return JsonResponse(
            {
                "error": (
                    "poultry_group_id, production_date, eggs_produced, "
                    "eggs_used, and eggs_sold are required"
                )
            },
            status=400,
        )

    try:
        poultry_group = PoultryGroups.objects.select_related(
            "project"
        ).get(
            poultry_group_id=poultry_group_id,
        )
    except PoultryGroups.DoesNotExist:
        return JsonResponse(
            {"error": "Poultry group not found"},
            status=404,
        )

    if not authorization_service.has_project_scope(
        request.user,
        poultry_group.project,
    ):
        return JsonResponse(
            {"error": "You are not authorized to use this poultry group"},
            status=403,
        )

    try:
        eggs_produced = int(eggs_produced)
        eggs_used = int(eggs_used)
        eggs_sold = int(eggs_sold)
    except (TypeError, ValueError):
        return JsonResponse(
            {
                "error": (
                    "eggs_produced, eggs_used, and eggs_sold "
                    "must be integers"
                )
            },
            status=400,
        )

    if eggs_produced < 0 or eggs_used < 0 or eggs_sold < 0:
        return JsonResponse(
            {
                "error": (
                    "eggs_produced, eggs_used, and eggs_sold "
                    "cannot be negative"
                )
            },
            status=400,
        )

    eggs_remaining = eggs_produced - eggs_used - eggs_sold

    if eggs_remaining < 0:
        return JsonResponse(
            {
                "error": (
                    "eggs_used and eggs_sold cannot be greater "
                    "than eggs_produced"
                )
            },
            status=400,
        )

    production = EggProduction.objects.create(
        poultry_group=poultry_group,
        production_date=production_date,
        eggs_produced=eggs_produced,
        eggs_used=eggs_used,
        eggs_sold=eggs_sold,
        eggs_remaining=eggs_remaining,
        recorded_by=request.user,
        created_at=timezone.now(),
    )

    return JsonResponse(
        {
            "egg_production": {
                "egg_production_id": production.egg_production_id,
                "poultry_group_id": production.poultry_group_id,
                "production_date": production.production_date,
                "eggs_produced": production.eggs_produced,
                "eggs_used": production.eggs_used,
                "eggs_sold": production.eggs_sold,
                "eggs_remaining": production.eggs_remaining,
                "recorded_by": production.recorded_by_id,
                "created_at": production.created_at,
            }
        },
        status=201,
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="egg_production",
)
def egg_production_list(request):
    """List egg production records within the user's authorized poultry scope."""
    if request.method != "GET":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    production_records = authorized_queryset(
        request.user,
        "egg_production",
        EggProduction.objects.all(),
    ).values(
        "egg_production_id",
        "poultry_group_id",
        "production_date",
        "eggs_produced",
        "eggs_used",
        "eggs_sold",
        "eggs_remaining",
        "recorded_by_id",
        "created_at",
    )

    return JsonResponse(
        {"egg_production": list(production_records)}
    )


@require_permission(
    permission=PERMISSION_VIEW,
    resource="poultry_stock_movements",
)
def poultry_stock_movements_list(request):
    """List stock movements within the user's authorized poultry scope."""
    if request.method != "GET":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    movements = authorized_queryset(
        request.user,
        "poultry_stock_movements",
        PoultryStockMovements.objects.all(),
    ).values(
        "movement_id",
        "poultry_group_id",
        "movement_date",
        "movement_type",
        "quantity",
        "description",
        "recorded_by_id",
        "created_at",
    )

    return JsonResponse(
        {"poultry_stock_movements": list(movements)}
    )
