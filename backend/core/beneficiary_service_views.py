import json
from datetime import date

from django.http import JsonResponse

from core.authorization.service import authorization_service
from core.models import DisabilityAssessments, HomeVisits


def _parse_json_object(request):
    try:
        payload = json.loads(request.body or "{}")
    except (TypeError, ValueError):
        return None, JsonResponse({"error": "Invalid JSON"}, status=400)

    if not isinstance(payload, dict):
        return None, JsonResponse(
            {"error": "JSON body must be an object"},
            status=400,
        )

    return payload, None


def _get_authorized_record(
    request,
    model,
    lookup,
    resource,
    not_found_message,
):
    if not getattr(
        getattr(request, "user", None),
        "is_authenticated",
        False,
    ):
        return None, JsonResponse(
            {"authorized": False},
            status=401,
        )

    try:
        record = model.objects.get(**lookup)
    except model.DoesNotExist:
        return None, JsonResponse(
            {"error": not_found_message},
            status=404,
        )

    if not authorization_service.can_edit(
        request.user,
        record,
        resource=resource,
        context=None,
    ):
        return None, JsonResponse(
            {"authorized": False},
            status=403,
        )

    return record, None


def disability_assessment_update(request, assessment_id):
    """Update an authorized disability assessment."""
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    assessment, access_error = _get_authorized_record(
        request,
        DisabilityAssessments,
        {"assessment_id": assessment_id},
        "disability_assessments",
        "Assessment not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "assessment_date",
        "assessment_type",
        "disability_type",
        "needs",
        "assessment_notes",
    }
    protected_fields = {
        "assessment_id",
        "beneficiary",
        "beneficiary_id",
        "assessed_by",
        "assessed_by_id",
        "created_at",
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

    if "assessment_date" in payload:
        try:
            value = date.fromisoformat(
                str(payload["assessment_date"])
            )
        except (TypeError, ValueError):
            return JsonResponse(
                {
                    "error": (
                        "assessment_date must use YYYY-MM-DD format"
                    )
                },
                status=400,
            )
        assessment.assessment_date = value
        update_fields.append("assessment_date")

    for field_name in (
        "assessment_type",
        "disability_type",
        "needs",
        "assessment_notes",
    ):
        if field_name in payload:
            value = payload[field_name]
            if value is not None and not isinstance(value, str):
                return JsonResponse(
                    {"error": f"{field_name} must be text"},
                    status=400,
                )
            setattr(assessment, field_name, value)
            update_fields.append(field_name)

    assessment.save(update_fields=update_fields)

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
        }
    )


def home_visit_update(request, home_visit_id):
    """Update an authorized home visit."""
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    visit, access_error = _get_authorized_record(
        request,
        HomeVisits,
        {"home_visit_id": home_visit_id},
        "home_visits",
        "Home visit not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "visit_date",
        "purpose",
        "observations",
        "support_provided",
        "follow_up_required",
        "next_action",
    }
    protected_fields = {
        "home_visit_id",
        "beneficiary",
        "beneficiary_id",
        "conducted_by",
        "conducted_by_id",
        "created_at",
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

    if "visit_date" in payload:
        try:
            value = date.fromisoformat(
                str(payload["visit_date"])
            )
        except (TypeError, ValueError):
            return JsonResponse(
                {
                    "error": (
                        "visit_date must use YYYY-MM-DD format"
                    )
                },
                status=400,
            )
        visit.visit_date = value
        update_fields.append("visit_date")

    for field_name in (
        "purpose",
        "observations",
        "support_provided",
        "next_action",
    ):
        if field_name in payload:
            value = payload[field_name]
            if value is not None and not isinstance(value, str):
                return JsonResponse(
                    {"error": f"{field_name} must be text"},
                    status=400,
                )
            setattr(visit, field_name, value)
            update_fields.append(field_name)

    if "follow_up_required" in payload:
        value = payload["follow_up_required"]
        if not isinstance(value, bool):
            return JsonResponse(
                {"error": "follow_up_required must be true or false"},
                status=400,
            )
        visit.follow_up_required = value
        update_fields.append("follow_up_required")

    visit.save(update_fields=update_fields)

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
        }
    )
