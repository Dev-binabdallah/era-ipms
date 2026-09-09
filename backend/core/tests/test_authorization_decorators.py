import json
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.authorization.decorators import require_activity_creation


class ActivityCreationDecoratorTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

        self.view = require_activity_creation(
            self.decorated_view,
        )

    def test_unauthenticated_request_returns_401(self):
        request = self.factory.post(
            "/activities/",
            data=json.dumps({"project_id": 1}),
            content_type="application/json",
        )
        request.user = self.unauthenticated_user

        response = self.view(request)

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.models.Projects.objects.get")
    def test_missing_project_id_returns_400(
        self,
        project_get,
        service,
    ):
        request = self.factory.post(
            "/activities/",
            data=json.dumps({}),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = self.view(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "project_id is required"},
        )

        project_get.assert_not_called()
        service.can_add_activity.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.models.Projects.objects.get")
    def test_invalid_project_id_returns_400(
        self,
        project_get,
        service,
    ):
        request = self.factory.post(
            "/activities/",
            data=json.dumps({"project_id": "abc"}),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = self.view(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "project_id must be an integer"},
        )

        project_get.assert_not_called()
        service.can_add_activity.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.models.Projects.objects.get")
    def test_missing_project_returns_404(
        self,
        project_get,
        service,
    ):
        from core.models import Projects

        project_get.side_effect = Projects.DoesNotExist

        request = self.factory.post(
            "/activities/",
            data=json.dumps({"project_id": 999}),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = self.view(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Project not found"},
        )

        service.can_add_activity.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.models.Projects.objects.get")
    def test_unauthorized_request_returns_403(
        self,
        project_get,
        service,
    ):
        project = SimpleNamespace(
            project_id=1,
        )
        project_get.return_value = project
        service.can_add_activity.return_value = False

        request = self.factory.post(
            "/activities/",
            data=json.dumps({"project_id": 1}),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = self.view(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add_activity.assert_called_once_with(
            self.authenticated_user,
            project,
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.models.Projects.objects.get")
    def test_authorized_request_passes_project_to_view(
        self,
        project_get,
        service,
    ):
        project = SimpleNamespace(
            project_id=1,
        )
        project_get.return_value = project
        service.can_add_activity.return_value = True

        request = self.factory.post(
            "/activities/",
            data=json.dumps({"project_id": 1}),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"project_id": 1},
        )

        service.can_add_activity.assert_called_once_with(
            self.authenticated_user,
            project,
        )

    def test_view_receives_resolved_project(self):
        project = SimpleNamespace(
            project_id=42,
        )

        with patch(
            "core.models.Projects.objects.get",
            return_value=project,
        ), patch(
            "core.authorization.decorators.authorization_service"
        ) as service:
            service.can_add_activity.return_value = True

            request = self.factory.post(
                "/activities/",
                data=json.dumps({"project_id": 42}),
                content_type="application/json",
            )
            request.user = self.authenticated_user

            response = self.view(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"project_id": 42},
        )

    @staticmethod
    def decorated_view(request, project):
        return __import__("django.http").http.JsonResponse(
            {"project_id": project.project_id},
        )
