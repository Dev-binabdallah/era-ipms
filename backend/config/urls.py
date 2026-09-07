from django.contrib import admin
from django.urls import path
from core.views import auth_test, auth_logout, projects_list


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/test/", auth_test),
    path("auth/logout/", auth_logout),
    path("projects/", projects_list),
]
