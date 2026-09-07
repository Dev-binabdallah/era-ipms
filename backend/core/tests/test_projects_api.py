from datetime import date
from types import SimpleNamespace
from unittest.mock import call, patch

from django.test import RequestFactory, SimpleTestCase

from core.models import Projects
from core.views import projects_create, projects_detail, projects_list


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

    def make_post_request(
        self,
        user,
        body,
        path="/projects/",
    ):
        request = self.factory.post(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    @patch("core.authorization.decorators.authorization_service")
    def test_create_unauthenticated_request_returns_401(self, service):
        response = projects_create(
            self.make_post_request(
                self.unauthenticated_user,
                '{"project_name": "Test Project"}',
            ),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )
        service.can_add.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    def test_create_unauthorized_request_returns_403(self, service):
        service.can_add.return_value = False

        user = SimpleNamespace(
            is_authenticated=True,
            user_id=10,
        )

        response = projects_create(
            self.make_post_request(
                user,
                '{"project_name": "Test Project"}',
            ),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add.assert_called_once_with(
            user,
            "projects",
            context=None,
        )

    @patch("core.views.timezone.now")
    @patch("core.views.Projects.objects.create")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_authorized_request_creates_project(
        self,
        service,
        objects_create,
        timezone_now,
    ):
        service.can_add.return_value = True

        user = SimpleNamespace(
            is_authenticated=True,
            user_id=10,
        )

        timestamp = "2026-09-07T10:00:00Z"
        timezone_now.return_value = timestamp

        project = SimpleNamespace(
            project_id=25,
            project_name="New Project",
            description="Project description",
            start_date="2026-09-10",
            end_date="2026-12-31",
            objectives="Project objectives",
            status="active",
            created_by_id=10,
            created_at=timestamp,
            updated_at=timestamp,
        )

        objects_create.return_value = project

        response = projects_create(
            self.make_post_request(
                user,
                '{"project_name": "New Project", '
                '"description": "Project description", '
                '"start_date": "2026-09-10", '
                '"end_date": "2026-12-31", '
                '"objectives": "Project objectives", '
                '"status": "active", '
                '"created_by_id": 999, '
                '"project_id": 999}',
            ),
        )

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "project": {
                    "project_id": 25,
                    "project_name": "New Project",
                    "description": "Project description",
                    "start_date": "2026-09-10",
                    "end_date": "2026-12-31",
                    "objectives": "Project objectives",
                    "status": "active",
                    "created_by_id": 10,
                    "created_at": timestamp,
                    "updated_at": timestamp,
                }
            },
        )

        objects_create.assert_called_once_with(
            project_name="New Project",
            description="Project description",
            start_date=date(2026, 9, 10),
            end_date=date(2026, 12, 31),
            objectives="Project objectives",
            status="active",
            created_by_id=10,
            created_at=timestamp,
            updated_at=timestamp,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_malformed_json_returns_400(self, service):
        service.can_add.return_value = True

        response = projects_create(
            self.make_post_request(
                self.authenticated_user,
                '{"project_name": ',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_non_object_json_returns_400(self, service):
        service.can_add.return_value = True

        response = projects_create(
            self.make_post_request(
                self.authenticated_user,
                '["Test Project"]',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "JSON body must be an object"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_project_name_returns_400(self, service):
        service.can_add.return_value = True

        response = projects_create(
            self.make_post_request(
                self.authenticated_user,
                '{"description": "Missing name"}',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "project_name is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_date_returns_400(self, service):
        service.can_add.return_value = True

        response = projects_create(
            self.make_post_request(
                self.authenticated_user,
                '{"project_name": "Test Project", '
                '"start_date": "10/09/2026"}',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "start_date must use YYYY-MM-DD format",
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_non_post_request_returns_405(self, service):
        service.can_add.return_value = True

        request = self.factory.get("/projects/")
        request.user = self.authenticated_user

        response = projects_create(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )
