import json
from datetime import date
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.utils import timezone

from core.authorization.service import authorization_service
from core.models import (
    FarmActivities,
    FarmCrops,
    FarmPoultryTransfers,
    Harvests,
)


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


def _require_edit_access(
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


def _check_patch_method(request):
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )
    return None


def _validate_date(value, field_name, allow_null=True):
    if allow_null and value in (None, ""):
        return None, None

    try:
        parsed = date.fromisoformat(str(value))
    except (TypeError, ValueError):
        return None, JsonResponse(
            {
                "error": (
                    f"{field_name} must be in YYYY-MM-DD format"
                )
            },
            status=400,
        )

    return parsed, None


def _validate_text(
    value,
    field_name,
    *,
    required=False,
    max_length=None,
):
    if value is None:
        if required:
            return None, JsonResponse(
                {"error": f"{field_name} is required"},
                status=400,
            )
        return None, None

    if not isinstance(value, str):
        return None, JsonResponse(
            {"error": f"{field_name} must be text"},
            status=400,
        )

    value = value.strip()

    if required and not value:
        return None, JsonResponse(
            {"error": f"{field_name} is required"},
            status=400,
        )

    if max_length is not None and len(value) > max_length:
        return None, JsonResponse(
            {
                "error": (
                    f"{field_name} must not exceed "
                    f"{max_length} characters"
                )
            },
            status=400,
        )

    return value, None


def _validate_positive_decimal(value, field_name):
    try:
        value = Decimal(str(value))
    except (TypeError, ValueError, InvalidOperation):
        return None, JsonResponse(
            {"error": f"{field_name} must be a valid number"},
            status=400,
        )

    if value <= 0:
        return None, JsonResponse(
            {"error": f"{field_name} must be greater than 0"},
            status=400,
        )

    return value, None


def _validate_fields(payload, editable_fields, protected_fields):
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

    return None


def farm_crop_update(request, crop_id):
    """Update editable fields on an authorized farm crop."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    crop, access_error = _require_edit_access(
        request,
        FarmCrops,
        {"crop_id": crop_id},
        "farm_crops",
        "Farm crop not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "crop_name",
        "description",
        "planting_date",
        "status",
    }
    protected_fields = {
        "crop_id",
        "project",
        "project_id",
        "recorded_by",
        "recorded_by_id",
        "created_at",
        "updated_at",
    }

    field_error = _validate_fields(
        payload,
        editable_fields,
        protected_fields,
    )
    if field_error is not None:
        return field_error

    update_fields = []

    if "crop_name" in payload:
        value, error = _validate_text(
            payload["crop_name"],
            "crop_name",
            required=True,
            max_length=200,
        )
        if error is not None:
            return error
        crop.crop_name = value
        update_fields.append("crop_name")

    if "description" in payload:
        value = payload["description"]
        if value is not None and not isinstance(value, str):
            return JsonResponse(
                {"error": "description must be text"},
                status=400,
            )
        crop.description = value
        update_fields.append("description")

    if "planting_date" in payload:
        value, error = _validate_date(
            payload["planting_date"],
            "planting_date",
        )
        if error is not None:
            return error
        crop.planting_date = value
        update_fields.append("planting_date")

    if "status" in payload:
        value, error = _validate_text(
            payload["status"],
            "status",
            required=True,
            max_length=50,
        )
        if error is not None:
            return error
        crop.status = value
        update_fields.append("status")

    crop.updated_at = timezone.now()
    update_fields.append("updated_at")
    crop.save(update_fields=update_fields)

    return JsonResponse(
        {
            "farm_crop": {
                "crop_id": crop.crop_id,
                "project_id": crop.project_id,
                "crop_name": crop.crop_name,
                "description": crop.description,
                "planting_date": crop.planting_date,
                "status": crop.status,
                "recorded_by": crop.recorded_by_id,
                "created_at": crop.created_at,
                "updated_at": crop.updated_at,
            }
        }
    )


def farm_activity_update(request, farm_activity_id):
    """Update an authorized farm activity."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    activity, access_error = _require_edit_access(
        request,
        FarmActivities,
        {"farm_activity_id": farm_activity_id},
        "farm_activities",
        "Farm activity not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "activity_date",
        "activity_type",
        "description",
    }
    protected_fields = {
        "farm_activity_id",
        "crop",
        "crop_id",
        "recorded_by",
        "recorded_by_id",
        "created_at",
    }

    field_error = _validate_fields(
        payload,
        editable_fields,
        protected_fields,
    )
    if field_error is not None:
        return field_error

    update_fields = []

    if "activity_date" in payload:
        value, error = _validate_date(
            payload["activity_date"],
            "activity_date",
            allow_null=False,
        )
        if error is not None:
            return error
        activity.activity_date = value
        update_fields.append("activity_date")

    if "activity_type" in payload:
        value, error = _validate_text(
            payload["activity_type"],
            "activity_type",
            required=True,
            max_length=100,
        )
        if error is not None:
            return error
        activity.activity_type = value
        update_fields.append("activity_type")

    if "description" in payload:
        value = payload["description"]
        if value is not None and not isinstance(value, str):
            return JsonResponse(
                {"error": "description must be text"},
                status=400,
            )
        activity.description = value
        update_fields.append("description")

    activity.save(update_fields=update_fields)

    return JsonResponse(
        {
            "farm_activity": {
                "farm_activity_id": activity.farm_activity_id,
                "crop_id": activity.crop_id,
                "activity_date": activity.activity_date,
                "activity_type": activity.activity_type,
                "description": activity.description,
                "recorded_by": activity.recorded_by_id,
                "created_at": activity.created_at,
            }
        }
    )


def harvest_update(request, harvest_id):
    """Update an authorized harvest record."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    harvest, access_error = _require_edit_access(
        request,
        Harvests,
        {"harvest_id": harvest_id},
        "harvests",
        "Harvest not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "harvest_date",
        "quantity",
        "unit",
        "usage_type",
        "notes",
    }
    protected_fields = {
        "harvest_id",
        "crop",
        "crop_id",
        "recorded_by",
        "recorded_by_id",
        "created_at",
    }

    field_error = _validate_fields(
        payload,
        editable_fields,
        protected_fields,
    )
    if field_error is not None:
        return field_error

    update_fields = []

    if "harvest_date" in payload:
        value, error = _validate_date(
            payload["harvest_date"],
            "harvest_date",
            allow_null=False,
        )
        if error is not None:
            return error
        harvest.harvest_date = value
        update_fields.append("harvest_date")

    if "quantity" in payload:
        value, error = _validate_positive_decimal(
            payload["quantity"],
            "quantity",
        )
        if error is not None:
            return error
        harvest.quantity = value
        update_fields.append("quantity")

    if "unit" in payload:
        value, error = _validate_text(
            payload["unit"],
            "unit",
            max_length=50,
        )
        if error is not None:
            return error
        harvest.unit = value or None
        update_fields.append("unit")

    if "usage_type" in payload:
        value, error = _validate_text(
            payload["usage_type"],
            "usage_type",
            max_length=100,
        )
        if error is not None:
            return error
        harvest.usage_type = value or None
        update_fields.append("usage_type")

    if "notes" in payload:
        value = payload["notes"]
        if value is not None and not isinstance(value, str):
            return JsonResponse(
                {"error": "notes must be text"},
                status=400,
            )
        harvest.notes = value
        update_fields.append("notes")

    harvest.save(update_fields=update_fields)

    return JsonResponse(
        {
            "harvest": {
                "harvest_id": harvest.harvest_id,
                "crop_id": harvest.crop_id,
                "harvest_date": harvest.harvest_date,
                "quantity": harvest.quantity,
                "unit": harvest.unit,
                "usage_type": harvest.usage_type,
                "notes": harvest.notes,
                "recorded_by": harvest.recorded_by_id,
                "created_at": harvest.created_at,
            }
        }
    )


def farm_poultry_transfer_update(request, transfer_id):
    """Update an authorized farm-to-poultry transfer."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    transfer, access_error = _require_edit_access(
        request,
        FarmPoultryTransfers,
        {"transfer_id": transfer_id},
        "farm_poultry_transfers",
        "Farm poultry transfer not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "transfer_date",
        "quantity",
        "unit",
        "notes",
    }
    protected_fields = {
        "transfer_id",
        "harvest",
        "harvest_id",
        "poultry_group",
        "poultry_group_id",
        "recorded_by",
        "recorded_by_id",
        "created_at",
    }

    field_error = _validate_fields(
        payload,
        editable_fields,
        protected_fields,
    )
    if field_error is not None:
        return field_error

    update_fields = []

    if "transfer_date" in payload:
        value, error = _validate_date(
            payload["transfer_date"],
            "transfer_date",
            allow_null=False,
        )
        if error is not None:
            return error
        transfer.transfer_date = value
        update_fields.append("transfer_date")

    if "quantity" in payload:
        value, error = _validate_positive_decimal(
            payload["quantity"],
            "quantity",
        )
        if error is not None:
            return error
        transfer.quantity = value
        update_fields.append("quantity")

    if "unit" in payload:
        value, error = _validate_text(
            payload["unit"],
            "unit",
            max_length=50,
        )
        if error is not None:
            return error
        transfer.unit = value or None
        update_fields.append("unit")

    if "notes" in payload:
        value = payload["notes"]
        if value is not None and not isinstance(value, str):
            return JsonResponse(
                {"error": "notes must be text"},
                status=400,
            )
        transfer.notes = value
        update_fields.append("notes")

    transfer.save(update_fields=update_fields)

    return JsonResponse(
        {
            "farm_poultry_transfer": {
                "transfer_id": transfer.transfer_id,
                "harvest_id": transfer.harvest_id,
                "poultry_group_id": transfer.poultry_group_id,
                "transfer_date": transfer.transfer_date,
                "quantity": transfer.quantity,
                "unit": transfer.unit,
                "notes": transfer.notes,
                "recorded_by": transfer.recorded_by_id,
                "created_at": transfer.created_at,
            }
        }
    )
