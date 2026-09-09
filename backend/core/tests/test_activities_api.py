import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.views import activities_create


class ActivitiesApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
            user_id=10,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_post_request(
        self,
        user,
        path="/activities/",
        body=b"{}",
    ):
        request = self.factory.post(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def test_create_unauthenticated_request_returns_401(self):
        response = activities_create(
            self.make_post_request(
                self.unauthenticated_user,
            )
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Projects.objects.get")
    def test_create_unauthorized_request_returns_403(
        self,
        project_get,
        service,
    ):
        service.can_add_activity.return_value = False

        project = SimpleNamespace(
            project_id=1,
        )
        project_get.return_value = project

        request = self.make_post_request(
            self.authenticated_user,
            body=b'{"project_id":1,"activity_name":"Training","responsible_user_id":20}',
        )

        response = activities_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add_activity.assert_called_once_with(
            self.authenticated_user,
            project,
        )

    def test_create_missing_project_id_returns_400(self):
        response = activities_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"activity_name":"Training","responsible_user_id":20}',
            )
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "project_id is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.models.Projects.objects.get")
    def test_create_missing_activity_name_returns_400(
        self,
        project_get,
        service,
    ):
        project_get.return_value = SimpleNamespace(project_id=1)
        service.can_add_activity.return_value = True

        response = activities_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"project_id":1,"responsible_user_id":20}',
            )
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "activity_name is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.models.Projects.objects.get")
    def test_create_missing_responsible_user_id_returns_400(
        self,
        project_get,
        service,
    ):
        project_get.return_value = SimpleNamespace(project_id=1)
        service.can_add_activity.return_value = True

        response = activities_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"project_id":1,"activity_name":"Training"}',
            )
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "responsible_user_id is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Projects.objects.get")
    def test_create_missing_project_returns_404(
        self,
        project_get,
        service,
    ):
        from core.models import Projects

        project_get.side_effect = Projects.DoesNotExist

        request = self.make_post_request(
            self.authenticated_user,
            body=b'{"project_id":999,"activity_name":"Training","responsible_user_id":20}',
        )

        response = activities_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Project not found"},
        )

        service.can_add_activity.assert_not_called()

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_responsible_user_returns_404(
        self,
        service,
        project_get,
    ):
        from core.models import Users

        project = SimpleNamespace(
            project_id=1,
        )
        project_get.return_value = project

        with patch(
            "core.views.Users.objects.get",
            side_effect=Users.DoesNotExist,
        ):
            service.can_add_activity.return_value = True

            request = self.make_post_request(
                self.authenticated_user,
                body=b'{"project_id":1,"activity_name":"Training","responsible_user_id":999}',
            )

            response = activities_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Responsible user not found"},
        )

    @patch("core.views.Users.objects.get")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_inactive_responsible_user_returns_400(
        self,
        service,
        project_get,
        user_get,
    ):
        service.can_add_activity.return_value = True

        project_get.return_value = SimpleNamespace(
            project_id=1,
        )
        user_get.return_value = SimpleNamespace(
            user_id=20,
            is_active=False,
        )

        request = self.make_post_request(
            self.authenticated_user,
            body=b'{"project_id":1,"activity_name":"Training","responsible_user_id":20}',
        )

        response = activities_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Responsible user is inactive"},
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.models.Projects.objects.get")
    def test_create_invalid_date_returns_400(
        self,
        project_get,
        service,
    ):
        project_get.return_value = SimpleNamespace(project_id=1)
        service.can_add_activity.return_value = True

        response = activities_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"project_id":1,"activity_name":"Training","responsible_user_id":20,"activity_date":"2026-99-99"}',
            )
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "activity_date must use YYYY-MM-DD format",
            },
        )

    @patch("django.utils.timezone.now")
    @patch("core.views.Activities.objects.create")
    @patch("core.views.Users.objects.get")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_authorized_creates_activity(
        self,
        service,
        project_get,
        user_get,
        activity_create,
        timezone_now,
    ):
        service.can_add_activity.return_value = True

        project = SimpleNamespace(
            project_id=1,
        )
        responsible_user = SimpleNamespace(
            user_id=20,
            is_active=True,
        )
        activity = SimpleNamespace(
            activity_id=5,
            project_id=1,
            activity_name="Community Training",
            activity_date=date(2026, 9, 8),
            location="Mombasa",
            responsible_user_id=20,
            description="Training session",
            status="Planned",
            results=None,
            created_at="2026-09-08T10:00:00Z",
            updated_at="2026-09-08T10:00:00Z",
        )

        project_get.return_value = project
        user_get.return_value = responsible_user
        activity_create.return_value = activity
        timezone_now.return_value = "2026-09-08T10:00:00Z"

        request = self.make_post_request(
            self.authenticated_user,
            body=json.dumps(
                {
                    "project_id": 1,
                    "activity_name": "Community Training",
                    "activity_date": "2026-09-08",
                    "location": "Mombasa",
                    "responsible_user_id": 20,
                    "description": "Training session",
                    "status": "Planned",
                    "results": None,
                }
            ).encode(),
        )

        response = activities_create(request)

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "activity": {
                    "activity_id": 5,
                    "project_id": 1,
                    "activity_name": "Community Training",
                    "activity_date": "2026-09-08",
                    "location": "Mombasa",
                    "responsible_user_id": 20,
                    "description": "Training session",
                    "status": "Planned",
                    "results": None,
                    "created_at": "2026-09-08T10:00:00Z",
                    "updated_at": "2026-09-08T10:00:00Z",
                }
            },
        )

        service.can_add_activity.assert_called_once_with(
            self.authenticated_user,
            project,
        )

        activity_create.assert_called_once()

        create_kwargs = activity_create.call_args.kwargs

        self.assertEqual(
            create_kwargs["project"],
            project,
        )
        self.assertEqual(
            create_kwargs["activity_name"],
            "Community Training",
        )
        self.assertEqual(
            create_kwargs["activity_date"],
            date(2026, 9, 8),
        )
        self.assertEqual(
            create_kwargs["location"],
            "Mombasa",
        )
        self.assertEqual(
            create_kwargs["responsible_user"],
            responsible_user,
        )
        self.assertEqual(
            create_kwargs["description"],
            "Training session",
        )
        self.assertEqual(
            create_kwargs["status"],
            "Planned",
        )
        self.assertIsNone(
            create_kwargs["results"],
        )
        self.assertEqual(
            create_kwargs["created_at"],
            "2026-09-08T10:00:00Z",
        )
        self.assertEqual(
            create_kwargs["updated_at"],
            "2026-09-08T10:00:00Z",
        )
