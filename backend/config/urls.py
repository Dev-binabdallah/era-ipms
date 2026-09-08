from django.contrib import admin
from django.urls import path
from core.views import (
    auth_login,
    auth_me,
    auth_logout,
    beneficiaries_collection,
    disability_assessments_collection,
    home_visits_collection,
    referrals_collection,
    referral_follow_ups_collection,
    projects_collection,
    projects_detail_collection,
    project_assignments,
    project_assignment_create,
    project_assignment_update,
)
from core.referral_workflow import referral_approve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/login/", auth_login),
    path("auth/me/", auth_me),
    path("auth/logout/", auth_logout),
    path("projects/", projects_collection),
    path("beneficiaries/", beneficiaries_collection),
    path(
        "disability-assessments/",
        disability_assessments_collection,
    ),
    path(
        "home-visits/",
        home_visits_collection,
    ),
    path(
        "referrals/",
        referrals_collection,
    ),
    path(
        "referrals/<int:referral_id>/follow-ups/",
        referral_follow_ups_collection,
    ),
    path(
        "referrals/<int:referral_id>/approve/",
        referral_approve,
    ),
    path("projects/<int:project_id>/", projects_detail_collection),
    path(
        "projects/<int:project_id>/assignments/",
        project_assignments,
    ),
    path(
        "projects/<int:project_id>/assignments/create/",
        project_assignment_create,
    ),
    path(
        "projects/<int:project_id>/assignments/<int:assignment_id>/",
        project_assignment_update,
    ),
]
