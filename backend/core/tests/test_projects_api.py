from types import SimpleNamespace
from unittest.mock import call, patch

from django.test import RequestFactory, SimpleTestCase

from core.models import Projects
from core.views import projects_detail, projects_list


class ProjectsApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_request(self, user, path="/projects/"):
        request = self.factory.get(path)
        request.user = user
        return request

    def test_unauthenticated_request_returns_401(self):
        response = projects_list(
            self.make_request(self.unauthenticated_user),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unauthorized_request_returns_403(self, service):
        service.can_view.return_value = False

        response = projects_list(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            None,
            resource="projects",
            context=None,
        )

    @patch("core.views.Projects.objects.all")
    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_request_uses_authorized_queryset(
        self,
        service,
        authorized_queryset,
        objects_all,
    ):
        service.can_view.return_value = True

        values_queryset = [
            {
                "project_id": 1,
                "project_name": "Test Project",
            },
        ]

        queryset = SimpleNamespace(
            values=lambda *args: values_queryset,
        )

        authorized_queryset.return_value = queryset
        objects_all.return_value = SimpleNamespace()

        response = projects_list(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "projects": values_queryset,
            },
        )

        objects_all.assert_called_once_with()
        authorized_queryset.assert_called_once_with(
            self.authenticated_user,
            "projects",
            objects_all.return_value,
        )

    def test_detail_unauthenticated_request_returns_401(self):
        response = projects_detail(
            self.make_request(
                self.unauthenticated_user,
                "/projects/1/",
            ),
            1,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_detail_unauthorized_request_returns_403(
        self,
        service,
        project_get,
    ):
        service.can_view.return_value = False

        project = SimpleNamespace(
            project_id=1,
        )
        project_get.return_value = project

        request = self.make_request(
            self.authenticated_user,
            "/projects/1/",
        )

        response = projects_detail(
            request,
            1,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        project_get.assert_called_once_with(
            project_id=1,
        )

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            project,
            resource="projects",
            context=None,
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_detail_authorized_request_returns_project(
        self,
        service,
        project_get,
    ):
        service.can_view.return_value = True

        project = SimpleNamespace(
            project_id=1,
            project_name="Test Project",
            description="Test description",
            start_date=None,
            end_date=None,
            objectives="Test objectives",
            status="active",
            created_by_id=10,
            created_at=None,
            updated_at=None,
        )

        project_get.return_value = project

        request = self.make_request(
            self.authenticated_user,
            "/projects/1/",
        )

        response = projects_detail(
            request,
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "project": {
                    "project_id": 1,
                    "project_name": "Test Project",
                    "description": "Test description",
                    "start_date": None,
                    "end_date": None,
                    "objectives": "Test objectives",
                    "status": "active",
                    "created_by_id": 10,
                    "created_at": None,
                    "updated_at": None,
                }
            },
        )

        project_get.assert_has_calls(
            [
                call(project_id=1),
                call(project_id=1),
            ]
        )
        self.assertEqual(project_get.call_count, 2)

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            project,
            resource="projects",
            context=None,
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_detail_nonexistent_project_returns_404(
        self,
        service,
        project_get,
    ):
        project_get.side_effect = Projects.DoesNotExist

        request = self.make_request(
            self.authenticated_user,
            "/projects/999/",
        )

        response = projects_detail(
            request,
            999,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Project not found",
            },
        )

        project_get.assert_has_calls(
            [
                call(project_id=999),
                call(project_id=999),
            ]
        )
        self.assertEqual(project_get.call_count, 2)

        service.can_view.assert_called_once_with(
           self.authenticated_user,
           None,
           resource="projects",
           context=None,
        )
