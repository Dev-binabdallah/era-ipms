import json
from datetime import date

from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.utils import timezone

from core.authorization.constants import PERMISSION_ADD, PERMISSION_EDIT, PERMISSION_VIEW
from core.authorization.decorators import require_permission
from core.authorization.querysets import authorized_queryset
from core.models import Projects


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