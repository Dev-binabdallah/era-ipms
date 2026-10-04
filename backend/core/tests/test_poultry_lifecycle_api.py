from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.poultry_views import (
    egg_production_update,
    feed_record_update,
    poultry_group_update,
    poultry_health_record_update,
    poultry_sale_update,
    poultry_stock_movement_update,
)


class PoultryLifecycleUpdateApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
        )
        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_patch_request(self, user, path, body):
        request = self.factory.patch(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def test_group_update_unauthenticated_returns_401(self):
        response = poultry_group_update(
            self.make_patch_request(
                self.unauthenticated_user,
                "/poultry-groups/1/",
                b'{"group_name":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.poultry_views.PoultryGroups.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_group_update_unauthorized_returns_403(
        self,
        service,
        group_get,
    ):
        group_get.return_value = SimpleNamespace()
        service.can_edit.return_value = False

        response = poultry_group_update(
            self.make_patch_request(
                self.authenticated_user,
                "/poultry-groups/1/",
                b'{"group_name":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.poultry_views.PoultryGroups.objects.get")
    def test_group_update_missing_returns_404(self, group_get):
        from core.models import PoultryGroups

        group_get.side_effect = PoultryGroups.DoesNotExist

        response = poultry_group_update(
            self.make_patch_request(
                self.authenticated_user,
                "/poultry-groups/1/",
                b'{"group_name":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Poultry group not found"},
        )

    @patch("core.poultry_views.PoultryGroups.objects.get")
    @patch("core.poultry_views.authorization_service")
    @patch("django.utils.timezone.now")
    def test_group_update_success(
        self,
        timezone_now,
        service,
        group_get,
    ):
        group = SimpleNamespace(
            poultry_group_id=1,
            project_id=10,
            group_name="Old",
            poultry_category="Layers",
            breed_or_type="Kienyeji",
            start_date=date(2026, 1, 1),
            status="active",
            description="Old description",
            updated_at="old-updated-at",
        )
        group_get.return_value = group
        service.can_edit.return_value = True
        timezone_now.return_value = "new-updated-at"
        group.save = lambda **kwargs: None

        response = poultry_group_update(
            self.make_patch_request(
                self.authenticated_user,
                "/poultry-groups/1/",
                b'{"group_name":"Updated","status":"completed"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(group.group_name, "Updated")
        self.assertEqual(group.status, "completed")
        self.assertEqual(group.updated_at, "new-updated-at")
        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            group,
            resource="poultry_groups",
            context=None,
        )

    @patch("core.poultry_views.PoultryGroups.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_group_update_invalid_json_returns_400(
        self,
        service,
        group_get,
    ):
        group_get.return_value = SimpleNamespace()
        service.can_edit.return_value = True

        response = poultry_group_update(
            self.make_patch_request(
                self.authenticated_user,
                "/poultry-groups/1/",
                b'{"group_name":',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.poultry_views.PoultryGroups.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_group_update_protected_fields_returns_400(
        self,
        service,
        group_get,
    ):
        group_get.return_value = SimpleNamespace()
        service.can_edit.return_value = True

        response = poultry_group_update(
            self.make_patch_request(
                self.authenticated_user,
                "/poultry-groups/1/",
                b'{"project_id":99}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Protected fields cannot be modified",
                "fields": ["project_id"],
            },
        )

    @patch("core.poultry_views.PoultryStockMovements.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_stock_movement_update_success(self, service, record_get):
        record = SimpleNamespace(
            movement_id=1,
            poultry_group_id=2,
            movement_date=date(2026, 9, 1),
            movement_type="purchase",
            quantity=10,
            description="Old",
            recorded_by_id=5,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = poultry_stock_movement_update(
            self.make_patch_request(
                self.authenticated_user,
                "/poultry-stock-movements/1/",
                b'{"quantity":15,"movement_type":"transfer"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(record.quantity, 15)
        self.assertEqual(record.movement_type, "transfer")

    @patch("core.poultry_views.EggProduction.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_egg_production_update_recalculates_remaining(
        self,
        service,
        record_get,
    ):
        record = SimpleNamespace(
            egg_production_id=1,
            poultry_group_id=2,
            production_date=date(2026, 9, 1),
            eggs_produced=100,
            eggs_used=10,
            eggs_sold=20,
            eggs_remaining=70,
            recorded_by_id=5,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = egg_production_update(
            self.make_patch_request(
                self.authenticated_user,
                "/egg-production/1/",
                b'{"eggs_produced":120,"eggs_sold":30}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(record.eggs_produced, 120)
        self.assertEqual(record.eggs_sold, 30)
        self.assertEqual(record.eggs_remaining, 80)

    @patch("core.poultry_views.EggProduction.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_egg_production_update_rejects_negative_remaining(
        self,
        service,
        record_get,
    ):
        record = SimpleNamespace(
            egg_production_id=1,
            poultry_group_id=2,
            eggs_produced=50,
            eggs_used=20,
            eggs_sold=20,
        )
        record_get.return_value = record
        service.can_edit.return_value = True

        response = egg_production_update(
            self.make_patch_request(
                self.authenticated_user,
                "/egg-production/1/",
                b'{"eggs_used":40}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "eggs_used and eggs_sold cannot be greater "
                    "than eggs_produced"
                )
            },
        )

    @patch("core.poultry_views.FeedRecords.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_feed_record_update_success(self, service, record_get):
        record = SimpleNamespace(
            feed_record_id=1,
            poultry_group_id=2,
            record_date=date(2026, 9, 1),
            feed_source="Store",
            feed_description="Old",
            quantity=Decimal("10.00"),
            unit="kg",
            cost=Decimal("100.00"),
            recorded_by_id=5,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = feed_record_update(
            self.make_patch_request(
                self.authenticated_user,
                "/feed-records/1/",
                b'{"quantity":"15.50","cost":"155.00"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(record.quantity, Decimal("15.50"))
        self.assertEqual(record.cost, Decimal("155.00"))

    @patch("core.poultry_views.PoultryHealthRecords.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_health_record_update_success(self, service, record_get):
        record = SimpleNamespace(
            health_record_id=1,
            poultry_group_id=2,
            record_date=date(2026, 9, 1),
            condition_type="Disease",
            number_affected=2,
            description="Old",
            action_taken="Old action",
            outcome="Old outcome",
            recorded_by_id=5,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = poultry_health_record_update(
            self.make_patch_request(
                self.authenticated_user,
                "/poultry-health-records/1/",
                b'{"number_affected":3,"outcome":"Recovered"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(record.number_affected, 3)
        self.assertEqual(record.outcome, "Recovered")

    @patch("core.poultry_views.PoultrySales.objects.get")
    @patch("core.poultry_views.authorization_service")
    def test_sale_update_success(self, service, record_get):
        sale = SimpleNamespace(
            poultry_sale_id=1,
            poultry_group_id=2,
            sale_date=date(2026, 9, 1),
            quantity=5,
            unit_price=Decimal("100.00"),
            total_amount=Decimal("500.00"),
            buyer_description="Old buyer",
            notes="Old notes",
            recorded_by_id=5,
            created_at="created",
        )
        record_get.return_value = sale
        service.can_edit.return_value = True
        sale.save = lambda **kwargs: None

        response = poultry_sale_update(
            self.make_patch_request(
                self.authenticated_user,
                "/poultry-sales/1/",
                b'{"quantity":7,"total_amount":"700.00"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(sale.quantity, 7)
        self.assertEqual(sale.total_amount, Decimal("700.00"))

    def test_all_update_endpoints_reject_get(self):
        endpoints = [
            (poultry_group_update, 1, "/poultry-groups/1/"),
            (poultry_stock_movement_update, 1, "/poultry-stock-movements/1/"),
            (egg_production_update, 1, "/egg-production/1/"),
            (feed_record_update, 1, "/feed-records/1/"),
            (poultry_health_record_update, 1, "/poultry-health-records/1/"),
            (poultry_sale_update, 1, "/poultry-sales/1/"),
        ]

        for view, record_id, path in endpoints:
            request = self.factory.get(path)
            request.user = self.authenticated_user
            response = view(request, record_id)

            self.assertEqual(response.status_code, 405)
            self.assertJSONEqual(
                response.content,
                {"error": "Method not allowed"},
            )
