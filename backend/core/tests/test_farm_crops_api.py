import json
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.views import (
    farm_crop_create,
    farm_crops_list,
)


@override_settings(ROOT_URLCONF="config.urls")
class FarmCropApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = SimpleNamespace(
            is_authenticated=True,
            is_active=True,
            user_id=1,
        )

        self.project = SimpleNamespace(
            project_id=10,
        )

        self.farm_crop = SimpleNamespace(
            crop_id=1,
            project_id=10,
            crop_name="Maize",
            description="Maize production",
            planting_date="2026-09-17",
            status="active",
            recorded_by_id=1,
            created_at="2026-09-17T10:00:00Z",
            updated_at="2026-09-17T10:00:00Z",
        )

    def test_list_requires_authentication(self):
        response = self.client.get("/farm-crops/")

        self.assertEqual(response.status_code, 401)

    def test_create_requires_authentication(self):
        response = self.client.post(
            "/farm-crops/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "crop_name": "Maize",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service")
    def test_list_requires_permission(self, service):
        service.can_view.return_value = False

        request = self.factory.get("/farm-crops/")
        request.user = self.user

        response = farm_crops_list(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_permission(self, service):
        service.can_add.return_value = False

        request = self.factory.post(
            "/farm-crops/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "crop_name": "Maize",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_crop_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.FarmCrops.objects.create")
    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    @patch("django.utils.timezone.now")
    def test_authorized_create(
        self,
        timezone_now,
        decorator_service,
        service,
        project_get,
        crop_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True

        project_get.return_value = self.project
        crop_create.return_value = self.farm_crop
        timezone_now.return_value = "2026-09-17T10:00:00Z"

        request = self.factory.post(
            "/farm-crops/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "crop_name": "Maize",
                    "description": "Maize production",
                    "planting_date": "2026-09-17",
                    "status": "active",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_crop_create(request)

        self.assertEqual(response.status_code, 201)

        self.assertJSONEqual(
            response.content,
            {
                "farm_crop": {
                    "crop_id": 1,
                    "project_id": 10,
                    "crop_name": "Maize",
                    "description": "Maize production",
                    "planting_date": "2026-09-17",
                    "status": "active",
                    "recorded_by": 1,
                    "created_at": "2026-09-17T10:00:00Z",
                    "updated_at": "2026-09-17T10:00:00Z",
                }
            },
        )

        service.has_project_scope.assert_called_once_with(
            self.user,
            self.project,
        )

        crop_create.assert_called_once()

        call_kwargs = crop_create.call_args.kwargs

        self.assertEqual(call_kwargs["project"], self.project)
        self.assertEqual(call_kwargs["crop_name"], "Maize")
        self.assertEqual(
            call_kwargs["description"],
            "Maize production",
        )
        self.assertEqual(
            str(call_kwargs["planting_date"]),
            "2026-09-17",
        )
        self.assertEqual(call_kwargs["status"], "active")
        self.assertEqual(call_kwargs["recorded_by"], self.user)
        self.assertEqual(
            call_kwargs["created_at"],
            "2026-09-17T10:00:00Z",
        )
        self.assertEqual(
            call_kwargs["updated_at"],
            "2026-09-17T10:00:00Z",
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_project_returns_404(
        self,
        decorator_service,
        project_get,
    ):
        decorator_service.can_add.return_value = True

        from core.models import Projects

        project_get.side_effect = Projects.DoesNotExist

        request = self.factory.post(
            "/farm-crops/create/",
            data=json.dumps(
                {
                    "project_id": 999,
                    "crop_name": "Maize",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_crop_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Project not found"},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_outside_project_scope_returns_403(
        self,
        decorator_service,
        service,
        project_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = False
        project_get.return_value = self.project

        request = self.factory.post(
            "/farm-crops/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "crop_name": "Maize",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_crop_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to use this project"
                )
            },
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_required_data_returns_400(
        self,
        decorator_service,
        project_get,
    ):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/farm-crops/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_crop_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "project_id and crop_name are required"
            },
        )

        project_get.assert_not_called()

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_planting_date_returns_400(
        self,
        decorator_service,
        project_get,
    ):
        decorator_service.can_add.return_value = True
        project_get.return_value = self.project

        with patch(
            "core.views.authorization_service"
        ) as service:
            service.has_project_scope.return_value = True

            request = self.factory.post(
                "/farm-crops/create/",
                data=json.dumps(
                    {
                        "project_id": 10,
                        "crop_name": "Maize",
                        "planting_date": "17-09-2026",
                    }
                ),
                content_type="application/json",
            )
            request.user = self.user

            response = farm_crop_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "planting_date must be in YYYY-MM-DD format"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_json_returns_400(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/farm-crops/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = farm_crop_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_get_request_returns_405(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.get("/farm-crops/create/")
        request.user = self.user

        response = farm_crop_create(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.views.FarmCrops.objects.all")
    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_authorized_crops(
        self,
        decorator_service,
        authorized_queryset,
        crop_all,
    ):
        decorator_service.can_view.return_value = True

        crop_values = [
            {
                "crop_id": 1,
                "project_id": 10,
                "crop_name": "Maize",
                "description": "Maize production",
                "planting_date": "2026-09-17",
                "status": "active",
                "recorded_by_id": 1,
                "created_at": "2026-09-17T10:00:00Z",
                "updated_at": "2026-09-17T10:00:00Z",
            }
        ]

        queryset = SimpleNamespace(
            values=lambda *fields: crop_values,
        )

        crop_all.return_value = SimpleNamespace()
        authorized_queryset.return_value = queryset

        request = self.factory.get("/farm-crops/")
        request.user = self.user

        response = farm_crops_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"farm_crops": crop_values},
        )

        authorized_queryset.assert_called_once_with(
            self.user,
            "farm_crops",
            crop_all.return_value,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_list_post_request_returns_405(self, decorator_service):
        decorator_service.can_view.return_value = True

        request = self.factory.post("/farm-crops/")
        request.user = self.user

        response = farm_crops_list(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )
