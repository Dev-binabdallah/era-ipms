from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.farm_views import (
    farm_activity_update,
    farm_crop_update,
    farm_poultry_transfer_update,
    harvest_update,
)


class FarmLifecycleUpdateApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True)
        self.unauthenticated_user = SimpleNamespace(is_authenticated=False)

    def make_patch_request(self, user, path, body):
        request = self.factory.patch(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def test_crop_update_unauthenticated_returns_401(self):
        response = farm_crop_update(
            self.make_patch_request(
                self.unauthenticated_user,
                "/farm-crops/1/",
                b'{"crop_name":"Updated"}',
            ),
            1,
        )
        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"authorized": False})

    @patch("core.farm_views.FarmCrops.objects.get")
    @patch("core.farm_views.authorization_service")
    def test_crop_update_unauthorized_returns_403(
        self,
        service,
        crop_get,
    ):
        crop_get.return_value = SimpleNamespace()
        service.can_edit.return_value = False

        response = farm_crop_update(
            self.make_patch_request(
                self.user,
                "/farm-crops/1/",
                b'{"crop_name":"Updated"}',
            ),
            1,
        )
        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {"authorized": False})

    @patch("core.farm_views.FarmCrops.objects.get")
    @patch("core.farm_views.authorization_service")
    @patch("django.utils.timezone.now")
    def test_crop_update_success(self, timezone_now, service, crop_get):
        crop = SimpleNamespace(
            crop_id=1,
            project_id=10,
            crop_name="Maize",
            description="Old",
            planting_date=date(2026, 1, 1),
            status="active",
            recorded_by_id=5,
            created_at="created",
            updated_at="old-updated",
        )
        crop_get.return_value = crop
        service.can_edit.return_value = True
        timezone_now.return_value = "new-updated"
        crop.save = lambda **kwargs: None

        response = farm_crop_update(
            self.make_patch_request(
                self.user,
                "/farm-crops/1/",
                b'{"crop_name":"Beans","status":"completed"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(crop.crop_name, "Beans")
        self.assertEqual(crop.status, "completed")
        self.assertEqual(crop.updated_at, "new-updated")

    @patch("core.farm_views.FarmActivities.objects.get")
    @patch("core.farm_views.authorization_service")
    def test_activity_update_success(self, service, record_get):
        record = SimpleNamespace(
            farm_activity_id=1,
            crop_id=2,
            activity_date=date(2026, 2, 1),
            activity_type="Weeding",
            description="Old",
            recorded_by_id=5,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = farm_activity_update(
            self.make_patch_request(
                self.user,
                "/farm-activities/1/",
                b'{"activity_type":"Fertilizing"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(record.activity_type, "Fertilizing")

    @patch("core.farm_views.Harvests.objects.get")
    @patch("core.farm_views.authorization_service")
    def test_harvest_update_success(self, service, record_get):
        record = SimpleNamespace(
            harvest_id=1,
            crop_id=2,
            harvest_date=date(2026, 8, 1),
            quantity=Decimal("20.00"),
            unit="kg",
            usage_type="sale",
            notes="Old",
            recorded_by_id=5,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = harvest_update(
            self.make_patch_request(
                self.user,
                "/harvests/1/",
                b'{"quantity":"25.50","usage_type":"poultry"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(record.quantity, Decimal("25.50"))
        self.assertEqual(record.usage_type, "poultry")

    @patch("core.farm_views.FarmPoultryTransfers.objects.get")
    @patch("core.farm_views.authorization_service")
    def test_transfer_update_success(self, service, record_get):
        record = SimpleNamespace(
            transfer_id=1,
            harvest_id=2,
            poultry_group_id=3,
            transfer_date=date(2026, 8, 1),
            quantity=Decimal("10.00"),
            unit="kg",
            notes="Old",
            recorded_by_id=5,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = farm_poultry_transfer_update(
            self.make_patch_request(
                self.user,
                "/farm-poultry-transfers/1/",
                b'{"quantity":"12.50","notes":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(record.quantity, Decimal("12.50"))
        self.assertEqual(record.notes, "Updated")

    @patch("core.farm_views.FarmCrops.objects.get")
    def test_crop_update_missing_returns_404(self, crop_get):
        from core.models import FarmCrops

        crop_get.side_effect = FarmCrops.DoesNotExist

        response = farm_crop_update(
            self.make_patch_request(
                self.user,
                "/farm-crops/1/",
                b'{"crop_name":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(response.content, {"error": "Farm crop not found"})

    @patch("core.farm_views.Harvests.objects.get")
    @patch("core.farm_views.authorization_service")
    def test_harvest_update_rejects_non_positive_quantity(
        self,
        service,
        record_get,
    ):
        record_get.return_value = SimpleNamespace()
        service.can_edit.return_value = True

        response = harvest_update(
            self.make_patch_request(
                self.user,
                "/harvests/1/",
                b'{"quantity":"0"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "quantity must be greater than 0"},
        )

    @patch("core.farm_views.FarmPoultryTransfers.objects.get")
    @patch("core.farm_views.authorization_service")
    def test_transfer_update_protects_links(
        self,
        service,
        record_get,
    ):
        record_get.return_value = SimpleNamespace()
        service.can_edit.return_value = True

        response = farm_poultry_transfer_update(
            self.make_patch_request(
                self.user,
                "/farm-poultry-transfers/1/",
                b'{"poultry_group_id":99}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Protected fields cannot be modified",
                "fields": ["poultry_group_id"],
            },
        )

    def test_all_update_endpoints_reject_get(self):
        endpoints = [
            (farm_crop_update, 1, "/farm-crops/1/"),
            (farm_activity_update, 1, "/farm-activities/1/"),
            (harvest_update, 1, "/harvests/1/"),
            (farm_poultry_transfer_update, 1, "/farm-poultry-transfers/1/"),
        ]

        for view, record_id, path in endpoints:
            request = self.factory.get(path)
            request.user = self.user
            response = view(request, record_id)

            self.assertEqual(response.status_code, 405)
            self.assertJSONEqual(
                response.content,
                {"error": "Method not allowed"},
            )
