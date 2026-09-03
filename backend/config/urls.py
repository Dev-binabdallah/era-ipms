from django.contrib import admin
from django.urls import path
from core.views import auth_test, auth_logout


urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/test/", auth_test),
    path("auth/logout/", auth_logout),
]