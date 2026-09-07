from functools import wraps

from django.http import JsonResponse

from core.authorization.constants import (
    PERMISSION_ADD,
    PERMISSION_ADMINISTER,
    PERMISSION_APPROVE,
    PERMISSION_DELETE,
    PERMISSION_EDIT,
    PERMISSION_EXPORT,
    PERMISSION_MANAGE,
    PERMISSION_VIEW,
)
from core.authorization.service import authorization_service


PERMISSION_METHODS = {
    PERMISSION_VIEW: "can_view",
    PERMISSION_ADD: "can_add",
    PERMISSION_EDIT: "can_edit",
    PERMISSION_DELETE: "can_delete",
    PERMISSION_APPROVE: "can_approve",
    PERMISSION_EXPORT: "can_export",
    PERMISSION_MANAGE: "can_manage",
    PERMISSION_ADMINISTER: "can_administer",
}


def require_permission(
    permission,
    resource=None,
    record_getter=None,
    context_getter=None,
):
    """
    Enforce an authorization decision before executing a Django view.

    Authentication failures return HTTP 401.
    Authorization failures return HTTP 403.

    Resource-aware authorization is delegated entirely to
    AuthorizationService so permission, responsibility, and
    record-level scope remain centralized.
    """

    if permission not in PERMISSION_METHODS:
        raise ValueError(f"Unsupported permission: {permission}")

    if permission != PERMISSION_ADMINISTER and not resource:
        raise ValueError(
            "A resource is required for non-administration permissions."
        )

    if record_getter is not None and not callable(record_getter):
        raise TypeError("record_getter must be callable.")

    if context_getter is not None and not callable(context_getter):
        raise TypeError("context_getter must be callable.")

    method_name = PERMISSION_METHODS[permission]

    def decorator(view_func):
        @wraps(view_func)
        def wrapped_view(request, *args, **kwargs):
            user = getattr(request, "user", None)

            if not getattr(user, "is_authenticated", False):
                return JsonResponse(
                    {"authorized": False},
                    status=401,
                )

            record = None
            context = None

            if record_getter is not None:
                record = record_getter(request, *args, **kwargs)

            if context_getter is not None:
                context = context_getter(request, *args, **kwargs)

            authorization_method = getattr(
                authorization_service,
                method_name,
            )

            if permission == PERMISSION_ADMINISTER:
                authorized = authorization_method(user)
            elif permission == PERMISSION_ADD:
                authorized = authorization_method(
                    user,
                    resource,
                    context=context,
                )
            elif permission in {
                PERMISSION_EXPORT,
                PERMISSION_MANAGE,
            }:
                authorized = authorization_method(
                    user,
                    resource,
                    context=context,
                )
            else:
                authorized = authorization_method(
                    user,
                    record,
                    resource=resource,
                    context=context,
                )

            if not authorized:
                return JsonResponse(
                    {"authorized": False},
                    status=403,
                )

            return view_func(request, *args, **kwargs)

        return wrapped_view

    return decorator
