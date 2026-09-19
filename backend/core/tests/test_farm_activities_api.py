import json
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.views import (
    farm_activities_list,
    farm_activity_create,
)


@override_settings(ROOT_URLCONF="config.urls")
class FarmActivityApiTests(SimpleTestCase):
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

        self.crop = SimpleNamespace(
            crop_id=5,
            project=self.project,
        )

        self.farm_activity = SimpleNamespace(
            farm_activity_id=1,
            crop_id=5,
            activity_date="2026-09-19",
            activity_type="Weeding",
            description="Removed weeds from the farm.",
            recorded_by_id=1,
            created_at="2026-09-19T10:00:00Z",
        )

    def test_list_requires_authentication(self):
        response = self.client.get("/farm-activities/")

        self.assertEqual(response.status_code, 401)

    def test_create_requires_authentication(self):
        response = self.client.post(
            "/farm-activities/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "activity_date": "2026-09-19",
                    "activity_type": "Weeding",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service")
    def test_list_requires_permission(self, service):
        service.can_view.return_value = False

        request = self.factory.get("/farm-activities/")
        request.user = self.user

        response = farm_activities_list(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_permission(self, service):
        service.can_add.return_value = False

        request = self.factory.post(
            "/farm-activities/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "activity_date": "2026-09-19",
                    "activity_type": "Weeding",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_activity_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.FarmActivities.objects.create")
    @patch("core.views.FarmCrops.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    @patch("django.utils.timezone.now")
    def test_authorized_create(
        self,
        timezone_now,
        decorator_service,
        service,
        crop_select_related,
        activity_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True

        crop_manager = SimpleNamespace(
            get=lambda **kwargs: self.crop,
        )
        crop_select_related.return_value = crop_manager

        activity_create.return_value = self.farm_activity
        timezone_now.return_value = "2026-09-19T10:00:00Z"

        request = self.factory.post(
            "/farm-activities/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "activity_date": "2026-09-19",
                    "activity_type": "Weeding",
                    "description": "Removed weeds from the farm.",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_activity_create(request)

        self.assertEqual(response.status_code, 201)

        self.assertJSONEqual(
            response.content,
            {
                "farm_activity": {
                    "farm_activity_id": 1,
                    "crop_id": 5,
                    "activity_date": "2026-09-19",
                    "activity_type": "Weeding",
                    "description": "Removed weeds from the farm.",
                    "recorded_by": 1,
                    "created_at": "2026-09-19T10:00:00Z",
                }
            },
        )

        service.has_project_scope.assert_called_once_with(
            self.user,
            self.project,
        )

        activity_create.assert_called_once()

    @patch("core.views.FarmCrops.objects.select_related")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_crop_returns_404(
        self,
        decorator_service,
        crop_select_related,
    ):
        decorator_service.can_add.return_value = True

        from core.models import FarmCrops

        crop_manager = SimpleNamespace(
            get=lambda **kwargs: (_ for _ in ()).throw(
                FarmCrops.DoesNotExist
            ),
        )
        crop_select_related.return_value = crop_manager

        request = self.factory.post(
            "/farm-activities/create/",
            data=json.dumps(
                {
                    "crop_id": 999,
                    "activity_date": "2026-09-19",
                    "activity_type": "Weeding",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_activity_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Farm crop not found"},
        )

    @patch("core.views.FarmCrops.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_outside_crop_scope_returns_403(
        self,
        decorator_service,
        service,
        crop_select_related,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = False

        crop_manager = SimpleNamespace(
            get=lambda **kwargs: self.crop,
        )
        crop_select_related.return_value = crop_manager

        request = self.factory.post(
            "/farm-activities/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "activity_date": "2026-09-19",
                    "activity_type": "Weeding",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_activity_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to use this farm crop"
                )
            },
        )

    @patch("core.views.FarmCrops.objects.select_related")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_required_data_returns_400(
        self,
        decorator_service,
        crop_select_related,
    ):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/farm-activities/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_activity_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "crop_id, activity_date, and activity_type "
                    "are required"
                )
            },
        )

        crop_select_related.assert_not_called()

    @patch("core.views.FarmCrops.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_date_returns_400(
        self,
        decorator_service,
        service,
        crop_select_related,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True

        crop_manager = SimpleNamespace(
            get=lambda **kwargs: self.crop,
        )
        crop_select_related.return_value = crop_manager

        request = self.factory.post(
            "/farm-activities/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "activity_date": "19-09-2026",
                    "activity_type": "Weeding",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = farm_activity_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "activity_date must be in YYYY-MM-DD format"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_json_returns_400(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/farm-activities/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = farm_activity_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_get_request_returns_405(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.get("/farm-activities/create/")
        request.user = self.user

        response = farm_activity_create(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.views.FarmActivities.objects.all")
    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_authorized_activities(
        self,
        decorator_service,
        authorized_queryset,
        activity_all,
    ):
        decorator_service.can_view.return_value = True

        activity_values = [
            {
                "farm_activity_id": 1,
                "crop_id": 5,
                "activity_date": "2026-09-19",
                "activity_type": "Weeding",
                "description": "Removed weeds from the farm.",
                "recorded_by_id": 1,
                "created_at": "2026-09-19T10:00:00Z",
            }
        ]

        queryset = SimpleNamespace(
            values=lambda *fields: activity_values,
        )

        activity_all.return_value = SimpleNamespace()
        authorized_queryset.return_value = queryset

        request = self.factory.get("/farm-activities/")
        request.user = self.user

        response = farm_activities_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"farm_activities": activity_values},
        )

        authorized_queryset.assert_called_once_with(
            self.user,
            "farm_activities",
            activity_all.return_value,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_list_post_request_returns_405(self, decorator_service):
        decorator_service.can_view.return_value = True

        request = self.factory.post("/farm-activities/")
        request.user = self.user

        response = farm_activities_list(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )
