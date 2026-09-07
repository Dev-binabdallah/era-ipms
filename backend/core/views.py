from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse

from core.authorization.constants import PERMISSION_VIEW
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