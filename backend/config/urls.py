from django.contrib import admin
from django.urls import path
from core.views import (
    auth_login,
    auth_me,
    auth_logout,
    projects_collection,
    projects_detail_collection,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/", auth_login),
    path("auth/me/", auth_me),
    path("auth/logout/", auth_logout),
    path("projects/", projects_collection),
    path("projects/<int:project_id>/", projects_detail_collection),
]
