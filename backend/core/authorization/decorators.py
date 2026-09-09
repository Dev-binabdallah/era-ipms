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


def require_activity_creation(view_func):
    """
    Enforce authorization for creating an activity under a project.

    Authentication failures return HTTP 401.
    Invalid project input returns HTTP 400.
    Missing projects return HTTP 404.
    Authorization failures return HTTP 403.

    Activity creation uses the dedicated AuthorizationService decision
    because the activity does not exist yet and authorization must be
    evaluated against its parent project.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        user = getattr(request, "user", None)

        if not getattr(user, "is_authenticated", False):
            return JsonResponse(
                {"authorized": False},
                status=401,
            )

        import json

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

        project_id = payload.get("project_id")

        if project_id in (None, ""):
            return JsonResponse(
                {"error": "project_id is required"},
                status=400,
            )

        try:
            project_id = int(project_id)
        except (TypeError, ValueError):
            return JsonResponse(
                {"error": "project_id must be an integer"},
                status=400,
            )

        if project_id <= 0:
            return JsonResponse(
                {"error": "project_id must be a positive integer"},
                status=400,
            )

        from core.models import Projects

        try:
            project = Projects.objects.get(
                project_id=project_id,
            )
        except Projects.DoesNotExist:
            return JsonResponse(
                {"error": "Project not found"},
                status=404,
            )

        if not authorization_service.can_add_activity(
            user,
            project,
        ):
            return JsonResponse(
                {"authorized": False},
                status=403,
            )

        return view_func(
            request,
            project,
            *args,
            **kwargs,
        )

    return wrapped_view


def require_project_assignment_management(view_func):
    """
    Enforce authorization for project assignment management.

    Authentication failures return HTTP 401.
    Authorization failures return HTTP 403.
    Missing projects return HTTP 404.

    Project assignment management uses the dedicated
    AuthorizationService decision because the operation creates or
    changes project membership and therefore cannot require
    pre-existing project membership.
    """

    @wraps(view_func)
    def wrapped_view(request, project_id, *args, **kwargs):
        user = getattr(request, "user", None)

        if not getattr(user, "is_authenticated", False):
            return JsonResponse(
                {"authorized": False},
                status=401,
            )

        from core.models import Projects

        try:
            project = Projects.objects.get(
                project_id=project_id,
            )
        except Projects.DoesNotExist:
            return JsonResponse(
                {"error": "Project not found"},
                status=404,
            )

        if not authorization_service.can_manage_project_assignments(
            user,
            project,
        ):
            return JsonResponse(
                {"authorized": False},
                status=403,
            )

        return view_func(
            request,
            project,
            *args,
            **kwargs,
        )

    return wrapped_view
