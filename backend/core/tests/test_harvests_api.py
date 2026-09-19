import json
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.models import FarmCrops, Harvests
from core.views import harvest_create, harvests_list


@override_settings(ROOT_URLCONF="config.urls")
class HarvestApiTests(SimpleTestCase):
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

        self.harvest = SimpleNamespace(
            harvest_id=1,
            crop_id=5,
            harvest_date="2026-09-19",
            quantity="25.50",
            unit="kg",
            usage_type="Sale",
            notes="Harvested maize.",
            recorded_by_id=1,
            created_at="2026-09-19T10:00:00Z",
        )

    def test_create_requires_authentication(self):
        response = self.client.post(
            "/harvests/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "harvest_date": "2026-09-19",
                    "quantity": 25,
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_requires_add_permission(
        self,
        mock_can_add,
    ):
        mock_can_add.return_value = False

        request = self.factory.post(
            "/harvests/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "harvest_date": "2026-09-19",
                    "quantity": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = harvest_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_json(
        self,
        mock_can_add,
    ):
        mock_can_add.return_value = True

        request = self.factory.post(
            "/harvests/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = harvest_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_requires_fields(
        self,
        mock_can_add,
    ):
        mock_can_add.return_value = True

        request = self.factory.post(
            "/harvests/create/",
            data=json.dumps({}),
            content_type="application/json",
        )
        request.user = self.user

        response = harvest_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "crop_id, harvest_date, and quantity are required"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_quantity(
        self,
        mock_can_add,
    ):
        mock_can_add.return_value = True

        request = self.factory.post(
            "/harvests/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "harvest_date": "2026-09-19",
                    "quantity": "abc",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = harvest_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "quantity must be a valid number"},
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_non_positive_quantity(
        self,
        mock_can_add,
    ):
        mock_can_add.return_value = True

        request = self.factory.post(
            "/harvests/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "harvest_date": "2026-09-19",
                    "quantity": 0,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = harvest_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "quantity must be greater than 0"},
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_date(
        self,
        mock_can_add,
    ):
        mock_can_add.return_value = True

        request = self.factory.post(
            "/harvests/create/",
            data=json.dumps(
                {
                    "crop_id": 5,
                    "harvest_date": "19-09-2026",
                    "quantity": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = harvest_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "harvest_date must be in YYYY-MM-DD format"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    @patch("core.views.FarmCrops.objects")
    def test_create_crop_not_found(
        self,
        mock_crop_objects,
        mock_can_add,
    ):
        mock_can_add.return_value = True
        mock_crop_objects.select_related.return_value.get.side_effect = (
            FarmCrops.DoesNotExist
        )

        request = self.factory.post(
            "/harvests/create/",
            data=json.dumps(
                {
                    "crop_id": 999,
                    "harvest_date": "2026-09-19",
                    "quantity": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = harvest_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Crop not found"},
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    @patch("core.views.FarmCrops.objects")
    def test_create_out_of_scope(
        self,
        mock_crop_objects,
        mock_can_add,
    ):
        mock_can_add.return_value = True
        mock_crop_objects.select_related.return_value.get.return_value = (
            self.crop
        )

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=False,
        ):
            request = self.factory.post(
                "/harvests/create/",
                data=json.dumps(
                    {
                        "crop_id": 5,
                        "harvest_date": "2026-09-19",
                        "quantity": 25,
                    }
                ),
                content_type="application/json",
            )
            request.user = self.user

            response = harvest_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"error": "You are not authorized to use this crop"},
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    @patch("core.views.timezone.now")
    @patch("core.views.Harvests.objects.create")
    @patch("core.views.FarmCrops.objects")
    def test_create_authorized(
        self,
        mock_crop_objects,
        mock_harvest_create,
        mock_now,
        mock_can_add,
    ):
        mock_can_add.return_value = True
        mock_crop_objects.select_related.return_value.get.return_value = (
            self.crop
        )
        mock_harvest_create.return_value = self.harvest
        mock_now.return_value = "2026-09-19T10:00:00Z"

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            request = self.factory.post(
                "/harvests/create/",
                data=json.dumps(
                    {
                        "crop_id": 5,
                        "harvest_date": "2026-09-19",
                        "quantity": 25.50,
                        "unit": "kg",
                        "usage_type": "Sale",
                        "notes": "Harvested maize.",
                    }
                ),
                content_type="application/json",
            )
            request.user = self.user

            response = harvest_create(request)

        self.assertEqual(response.status_code, 201)

        mock_harvest_create.assert_called_once()

        create_kwargs = mock_harvest_create.call_args.kwargs
        self.assertEqual(create_kwargs["crop"], self.crop)
        self.assertEqual(
            str(create_kwargs["harvest_date"]),
            "2026-09-19",
        )
        self.assertEqual(create_kwargs["quantity"], Decimal("25.50"))
        self.assertEqual(create_kwargs["unit"], "kg")
        self.assertEqual(create_kwargs["usage_type"], "Sale")
        self.assertEqual(create_kwargs["notes"], "Harvested maize.")
        self.assertEqual(create_kwargs["recorded_by"], self.user)

    def test_list_requires_authentication(self):
        response = self.client.get("/harvests/")

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service.can_view")
    def test_list_requires_view_permission(
        self,
        mock_can_view,
    ):
        mock_can_view.return_value = False

        request = self.factory.get("/harvests/")
        request.user = self.user

        response = harvests_list(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service.can_view")
    @patch("core.views.authorized_queryset")
    def test_list_authorized(
        self,
        mock_authorized_queryset,
        mock_can_view,
    ):
        mock_can_view.return_value = True

        class ValuesResult:
            def values(self, *args):
                return [
                    {
                        "harvest_id": 1,
                        "crop_id": 5,
                        "harvest_date": "2026-09-19",
                        "quantity": "25.50",
                        "unit": "kg",
                        "usage_type": "Sale",
                        "notes": "Harvested maize.",
                        "recorded_by_id": 1,
                        "created_at": "2026-09-19T10:00:00Z",
                    }
                ]

        mock_authorized_queryset.return_value = ValuesResult()

        request = self.factory.get("/harvests/")
        request.user = self.user

        response = harvests_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "harvests": [
                    {
                        "harvest_id": 1,
                        "crop_id": 5,
                        "harvest_date": "2026-09-19",
                        "quantity": "25.50",
                        "unit": "kg",
                        "usage_type": "Sale",
                        "notes": "Harvested maize.",
                        "recorded_by_id": 1,
                        "created_at": "2026-09-19T10:00:00Z",
                    }
                ]
            },
        )

        mock_authorized_queryset.assert_called_once()

        queryset_args = mock_authorized_queryset.call_args.args
        self.assertEqual(queryset_args[0], self.user)
        self.assertEqual(queryset_args[1], "harvests")
