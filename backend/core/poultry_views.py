import json
from datetime import date
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.utils import timezone

from core.authorization.service import authorization_service
from core.models import (
    EggProduction,
    FeedRecords,
    PoultryGroups,
    PoultryHealthRecords,
    PoultrySales,
    PoultryStockMovements,
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


def _validate_non_negative_integer(value, field_name):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return None, JsonResponse(
            {"error": f"{field_name} must be an integer"},
            status=400,
        )

    if value < 0:
        return None, JsonResponse(
            {"error": f"{field_name} cannot be negative"},
            status=400,
        )

    return value, None


def _validate_non_negative_decimal(value, field_name):
    try:
        value = Decimal(str(value))
    except (TypeError, ValueError, InvalidOperation):
        return None, JsonResponse(
            {"error": f"{field_name} must be a valid number"},
            status=400,
        )

    if value < 0:
        return None, JsonResponse(
            {"error": f"{field_name} cannot be negative"},
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


def poultry_group_update(request, group_id):
    """Update editable fields on an authorized poultry group."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    group, access_error = _require_edit_access(
        request,
        PoultryGroups,
        {"poultry_group_id": group_id},
        "poultry_groups",
        "Poultry group not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "group_name",
        "poultry_category",
        "breed_or_type",
        "start_date",
        "status",
        "description",
    }
    protected_fields = {
        "poultry_group_id",
        "project",
        "project_id",
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

    if "group_name" in payload:
        value, error = _validate_text(
            payload["group_name"],
            "group_name",
            required=True,
            max_length=150,
        )
        if error is not None:
            return error
        group.group_name = value
        update_fields.append("group_name")

    if "poultry_category" in payload:
        value, error = _validate_text(
            payload["poultry_category"],
            "poultry_category",
            max_length=100,
        )
        if error is not None:
            return error
        group.poultry_category = value or None
        update_fields.append("poultry_category")

    if "breed_or_type" in payload:
        value, error = _validate_text(
            payload["breed_or_type"],
            "breed_or_type",
            max_length=100,
        )
        if error is not None:
            return error
        group.breed_or_type = value or None
        update_fields.append("breed_or_type")

    if "start_date" in payload:
        value, error = _validate_date(
            payload["start_date"],
            "start_date",
        )
        if error is not None:
            return error
        group.start_date = value
        update_fields.append("start_date")

    if "status" in payload:
        value, error = _validate_text(
            payload["status"],
            "status",
            required=True,
            max_length=50,
        )
        if error is not None:
            return error
        group.status = value
        update_fields.append("status")

    if "description" in payload:
        value = payload["description"]
        if value is not None and not isinstance(value, str):
            return JsonResponse(
                {"error": "description must be text"},
                status=400,
            )
        group.description = value
        update_fields.append("description")

    group.updated_at = timezone.now()
    update_fields.append("updated_at")
    group.save(update_fields=update_fields)

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
        }
    )


def poultry_stock_movement_update(request, movement_id):
    """Update an authorized poultry stock movement."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    movement, access_error = _require_edit_access(
        request,
        PoultryStockMovements,
        {"movement_id": movement_id},
        "poultry_stock_movements",
        "Poultry stock movement not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "movement_date",
        "movement_type",
        "quantity",
        "description",
    }
    protected_fields = {
        "movement_id",
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

    if "movement_date" in payload:
        value, error = _validate_date(
            payload["movement_date"],
            "movement_date",
            allow_null=False,
        )
        if error is not None:
            return error
        movement.movement_date = value
        update_fields.append("movement_date")

    if "movement_type" in payload:
        value, error = _validate_text(
            payload["movement_type"],
            "movement_type",
            required=True,
            max_length=50,
        )
        if error is not None:
            return error
        movement.movement_type = value
        update_fields.append("movement_type")

    if "quantity" in payload:
        value, error = _validate_non_negative_integer(
            payload["quantity"],
            "quantity",
        )
        if error is not None:
            return error
        movement.quantity = value
        update_fields.append("quantity")

    if "description" in payload:
        value = payload["description"]
        if value is not None and not isinstance(value, str):
            return JsonResponse(
                {"error": "description must be text"},
                status=400,
            )
        movement.description = value
        update_fields.append("description")

    movement.save(update_fields=update_fields)

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
        }
    )


def egg_production_update(request, egg_production_id):
    """Update an authorized egg production record."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    record, access_error = _require_edit_access(
        request,
        EggProduction,
        {"egg_production_id": egg_production_id},
        "egg_production",
        "Egg production record not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "production_date",
        "eggs_produced",
        "eggs_used",
        "eggs_sold",
    }
    protected_fields = {
        "egg_production_id",
        "poultry_group",
        "poultry_group_id",
        "eggs_remaining",
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

    if "production_date" in payload:
        value, error = _validate_date(
            payload["production_date"],
            "production_date",
            allow_null=False,
        )
        if error is not None:
            return error
        record.production_date = value
        update_fields.append("production_date")

    for field_name in (
        "eggs_produced",
        "eggs_used",
        "eggs_sold",
    ):
        if field_name in payload:
            value, error = _validate_non_negative_integer(
                payload[field_name],
                field_name,
            )
            if error is not None:
                return error
            setattr(record, field_name, value)
            update_fields.append(field_name)

    eggs_remaining = (
        record.eggs_produced
        - record.eggs_used
        - record.eggs_sold
    )

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

    record.eggs_remaining = eggs_remaining
    update_fields.append("eggs_remaining")
    record.save(update_fields=update_fields)

    return JsonResponse(
        {
            "egg_production": {
                "egg_production_id": record.egg_production_id,
                "poultry_group_id": record.poultry_group_id,
                "production_date": record.production_date,
                "eggs_produced": record.eggs_produced,
                "eggs_used": record.eggs_used,
                "eggs_sold": record.eggs_sold,
                "eggs_remaining": record.eggs_remaining,
                "recorded_by": record.recorded_by_id,
                "created_at": record.created_at,
            }
        }
    )


def feed_record_update(request, feed_record_id):
    """Update an authorized feed record."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    record, access_error = _require_edit_access(
        request,
        FeedRecords,
        {"feed_record_id": feed_record_id},
        "feed_records",
        "Feed record not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "record_date",
        "feed_source",
        "feed_description",
        "quantity",
        "unit",
        "cost",
    }
    protected_fields = {
        "feed_record_id",
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

    if "record_date" in payload:
        value, error = _validate_date(
            payload["record_date"],
            "record_date",
            allow_null=False,
        )
        if error is not None:
            return error
        record.record_date = value
        update_fields.append("record_date")

    if "feed_source" in payload:
        value, error = _validate_text(
            payload["feed_source"],
            "feed_source",
            max_length=200,
        )
        if error is not None:
            return error
        record.feed_source = value or None
        update_fields.append("feed_source")

    if "feed_description" in payload:
        value = payload["feed_description"]
        if value is not None and not isinstance(value, str):
            return JsonResponse(
                {"error": "feed_description must be text"},
                status=400,
            )
        record.feed_description = value
        update_fields.append("feed_description")

    if "quantity" in payload:
        value, error = _validate_non_negative_decimal(
            payload["quantity"],
            "quantity",
        )
        if error is not None:
            return error
        record.quantity = value
        update_fields.append("quantity")

    if "unit" in payload:
        value, error = _validate_text(
            payload["unit"],
            "unit",
            max_length=50,
        )
        if error is not None:
            return error
        record.unit = value or None
        update_fields.append("unit")

    if "cost" in payload:
        value, error = _validate_non_negative_decimal(
            payload["cost"],
            "cost",
        )
        if error is not None:
            return error
        record.cost = value
        update_fields.append("cost")

    record.save(update_fields=update_fields)

    return JsonResponse(
        {
            "feed_record": {
                "feed_record_id": record.feed_record_id,
                "poultry_group_id": record.poultry_group_id,
                "record_date": record.record_date,
                "feed_source": record.feed_source,
                "feed_description": record.feed_description,
                "quantity": record.quantity,
                "unit": record.unit,
                "cost": record.cost,
                "recorded_by": record.recorded_by_id,
                "created_at": record.created_at,
            }
        }
    )


def poultry_health_record_update(request, health_record_id):
    """Update an authorized poultry health record."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    record, access_error = _require_edit_access(
        request,
        PoultryHealthRecords,
        {"health_record_id": health_record_id},
        "poultry_health_records",
        "Poultry health record not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "record_date",
        "condition_type",
        "number_affected",
        "description",
        "action_taken",
        "outcome",
    }
    protected_fields = {
        "health_record_id",
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

    if "record_date" in payload:
        value, error = _validate_date(
            payload["record_date"],
            "record_date",
            allow_null=False,
        )
        if error is not None:
            return error
        record.record_date = value
        update_fields.append("record_date")

    if "condition_type" in payload:
        value, error = _validate_text(
            payload["condition_type"],
            "condition_type",
            required=True,
            max_length=100,
        )
        if error is not None:
            return error
        record.condition_type = value
        update_fields.append("condition_type")

    if "number_affected" in payload:
        value, error = _validate_non_negative_integer(
            payload["number_affected"],
            "number_affected",
        )
        if error is not None:
            return error
        record.number_affected = value
        update_fields.append("number_affected")

    for field_name in (
        "description",
        "action_taken",
        "outcome",
    ):
        if field_name in payload:
            value = payload[field_name]
            if value is not None and not isinstance(value, str):
                return JsonResponse(
                    {"error": f"{field_name} must be text"},
                    status=400,
                )
            setattr(record, field_name, value)
            update_fields.append(field_name)

    record.save(update_fields=update_fields)

    return JsonResponse(
        {
            "poultry_health_record": {
                "health_record_id": record.health_record_id,
                "poultry_group_id": record.poultry_group_id,
                "record_date": record.record_date,
                "condition_type": record.condition_type,
                "number_affected": record.number_affected,
                "description": record.description,
                "action_taken": record.action_taken,
                "outcome": record.outcome,
                "recorded_by": record.recorded_by_id,
                "created_at": record.created_at,
            }
        }
    )


def poultry_sale_update(request, poultry_sale_id):
    """Update an authorized poultry sale."""
    method_error = _check_patch_method(request)
    if method_error is not None:
        return method_error

    sale, access_error = _require_edit_access(
        request,
        PoultrySales,
        {"poultry_sale_id": poultry_sale_id},
        "poultry_sales",
        "Poultry sale not found",
    )
    if access_error is not None:
        return access_error

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    editable_fields = {
        "sale_date",
        "quantity",
        "unit_price",
        "total_amount",
        "buyer_description",
        "notes",
    }
    protected_fields = {
        "poultry_sale_id",
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

    if "sale_date" in payload:
        value, error = _validate_date(
            payload["sale_date"],
            "sale_date",
            allow_null=False,
        )
        if error is not None:
            return error
        sale.sale_date = value
        update_fields.append("sale_date")

    if "quantity" in payload:
        value, error = _validate_non_negative_integer(
            payload["quantity"],
            "quantity",
        )
        if error is not None:
            return error
        sale.quantity = value
        update_fields.append("quantity")

    for field_name in ("unit_price", "total_amount"):
        if field_name in payload:
            raw_value = payload[field_name]
            if raw_value in (None, ""):
                value = None
            else:
                value, error = _validate_non_negative_decimal(
                    raw_value,
                    field_name,
                )
                if error is not None:
                    return error
            setattr(sale, field_name, value)
            update_fields.append(field_name)

    for field_name in ("buyer_description", "notes"):
        if field_name in payload:
            value = payload[field_name]
            if value is not None and not isinstance(value, str):
                return JsonResponse(
                    {"error": f"{field_name} must be text"},
                    status=400,
                )
            setattr(sale, field_name, value)
            update_fields.append(field_name)

    sale.save(update_fields=update_fields)

    return JsonResponse(
        {
            "poultry_sale": {
                "poultry_sale_id": sale.poultry_sale_id,
                "poultry_group_id": sale.poultry_group_id,
                "sale_date": sale.sale_date,
                "quantity": sale.quantity,
                "unit_price": sale.unit_price,
                "total_amount": sale.total_amount,
                "buyer_description": sale.buyer_description,
                "notes": sale.notes,
                "recorded_by": sale.recorded_by_id,
                "created_at": sale.created_at,
            }
        }
    )
