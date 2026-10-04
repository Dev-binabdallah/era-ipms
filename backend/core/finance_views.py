import json
from datetime import date
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.utils import timezone

from core.authorization.service import authorization_service
from core.models import FinancialTransactions


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


def financial_transaction_update(request, transaction_id):
    """Update editable fields on an authorized financial transaction."""
    if request.method != "PATCH":
        return JsonResponse(
            {"error": "Method not allowed"},
            status=405,
        )

    if not getattr(
        getattr(request, "user", None),
        "is_authenticated",
        False,
    ):
        return JsonResponse(
            {"authorized": False},
            status=401,
        )

    try:
        transaction = FinancialTransactions.objects.get(
            transaction_id=transaction_id,
        )
    except FinancialTransactions.DoesNotExist:
        return JsonResponse(
            {"error": "Financial transaction not found"},
            status=404,
        )

    if not authorization_service.can_edit(
        request.user,
        transaction,
        resource="financial_transactions",
        context=None,
    ):
        return JsonResponse(
            {"authorized": False},
            status=403,
        )

    payload, payload_error = _parse_json_object(request)
    if payload_error is not None:
        return payload_error

    protected_fields = {
        "transaction_id",
        "project",
        "project_id",
        "recorded_by",
        "recorded_by_id",
        "approved_by",
        "approved_by_id",
        "approved_at",
        "status",
        "created_at",
        "updated_at",
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
        "transaction_date",
        "transaction_type",
        "category",
        "amount",
        "description",
        "payment_method",
        "reference_number",
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

    if "transaction_date" in payload:
        try:
            transaction_date = date.fromisoformat(
                str(payload["transaction_date"])
            )
        except (TypeError, ValueError):
            return JsonResponse(
                {
                    "error": (
                        "transaction_date must be in "
                        "YYYY-MM-DD format"
                    )
                },
                status=400,
            )

        transaction.transaction_date = transaction_date
        update_fields.append("transaction_date")

    if "transaction_type" in payload:
        transaction_type = payload["transaction_type"]

        if (
            not isinstance(transaction_type, str)
            or not transaction_type.strip()
        ):
            return JsonResponse(
                {"error": "transaction_type is required"},
                status=400,
            )

        transaction_type = transaction_type.strip()

        if len(transaction_type) > 30:
            return JsonResponse(
                {
                    "error": (
                        "transaction_type must not exceed "
                        "30 characters"
                    )
                },
                status=400,
            )

        transaction.transaction_type = transaction_type
        update_fields.append("transaction_type")

    if "category" in payload:
        category = payload["category"]

        if not isinstance(category, str) or not category.strip():
            return JsonResponse(
                {"error": "category is required"},
                status=400,
            )

        category = category.strip()

        if len(category) > 100:
            return JsonResponse(
                {
                    "error": (
                        "category must not exceed 100 characters"
                    )
                },
                status=400,
            )

        transaction.category = category
        update_fields.append("category")

    if "amount" in payload:
        try:
            amount = Decimal(str(payload["amount"]))
        except (TypeError, ValueError, InvalidOperation):
            return JsonResponse(
                {"error": "amount must be a valid number"},
                status=400,
            )

        if amount <= 0:
            return JsonResponse(
                {"error": "amount must be greater than 0"},
                status=400,
            )

        transaction.amount = amount
        update_fields.append("amount")

    for field_name in (
        "description",
        "payment_method",
        "reference_number",
    ):
        if field_name in payload:
            value = payload[field_name]

            if value is not None and not isinstance(value, str):
                return JsonResponse(
                    {"error": f"{field_name} must be text"},
                    status=400,
                )

            setattr(
                transaction,
                field_name,
                value.strip() if isinstance(value, str) else value,
            )
            update_fields.append(field_name)

    transaction.updated_at = timezone.now()
    update_fields.append("updated_at")
    transaction.save(update_fields=update_fields)

    return JsonResponse(
        {
            "financial_transaction": {
                "transaction_id": transaction.transaction_id,
                "project_id": transaction.project_id,
                "transaction_date": transaction.transaction_date,
                "transaction_type": transaction.transaction_type,
                "category": transaction.category,
                "amount": transaction.amount,
                "description": transaction.description,
                "payment_method": transaction.payment_method,
                "reference_number": transaction.reference_number,
                "recorded_by_id": transaction.recorded_by_id,
                "approved_by_id": transaction.approved_by_id,
                "approved_at": transaction.approved_at,
                "status": transaction.status,
                "created_at": transaction.created_at,
                "updated_at": transaction.updated_at,
            }
        },
        status=200,
    )
