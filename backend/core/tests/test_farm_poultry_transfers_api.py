import json
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase

from core.views import (
    farm_poultry_transfer_create,
    farm_poultry_transfers_list,
)


class FarmPoultryTransfersApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = SimpleNamespace(
            is_authenticated=True,
            is_active=True,
            user_id=1,
            username="testuser",
        )

        self.project = SimpleNamespace(
            project_id=10,
        )

        self.other_project = SimpleNamespace(
            project_id=20,
        )

        self.crop = SimpleNamespace(
            crop_id=5,
            project=self.project,
        )

        self.harvest = SimpleNamespace(
            harvest_id=15,
            crop=self.crop,
        )

        self.poultry_group = SimpleNamespace(
            poultry_group_id=20,
            project=self.project,
        )

        self.other_poultry_group = SimpleNamespace(
            poultry_group_id=30,
            project=self.other_project,
        )

        self.transfer = SimpleNamespace(
            transfer_id=1,
            harvest_id=15,
            poultry_group_id=20,
            transfer_date="2026-09-19",
            quantity=Decimal("10.00"),
            unit="kg",
            notes="Transferred for poultry use.",
            recorded_by_id=1,
            created_at="2026-09-19T10:00:00Z",
        )

    def make_request(self, payload, method="post"):
        request = getattr(self.factory, method)(
            "/farm-poultry-transfers/create/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        request.user = self.user
        return request

    def test_create_requires_authentication(self):
        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 20,
                "transfer_date": "2026-09-19",
                "quantity": 10,
            }
        )
        request.user = SimpleNamespace(is_authenticated=False)

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_requires_add_permission(self, mock_can_add):
        mock_can_add.return_value = False

        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 20,
                "transfer_date": "2026-09-19",
                "quantity": 10,
            }
        )

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_json(self, mock_can_add):
        mock_can_add.return_value = True

        request = self.factory.post(
            "/farm-poultry-transfers/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "Invalid JSON",
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_requires_fields(self, mock_can_add):
        mock_can_add.return_value = True

        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 20,
            }
        )

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "required",
            json.loads(response.content)["error"],
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_quantity(self, mock_can_add):
        mock_can_add.return_value = True

        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 20,
                "transfer_date": "2026-09-19",
                "quantity": "abc",
            }
        )

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "quantity must be a valid number",
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_non_positive_quantity(self, mock_can_add):
        mock_can_add.return_value = True

        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 20,
                "transfer_date": "2026-09-19",
                "quantity": 0,
            }
        )

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "quantity must be greater than 0",
        )

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_date(self, mock_can_add):
        mock_can_add.return_value = True

        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 20,
                "transfer_date": "19-09-2026",
                "quantity": 10,
            }
        )

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "transfer_date must be in YYYY-MM-DD format",
        )

    @patch("core.views.Harvests.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_harvest_not_found(
        self,
        mock_can_add,
        mock_select_related,
    ):
        mock_can_add.return_value = True

        mock_manager = Mock()
        mock_manager.get.side_effect = Exception("harvest not found")
        mock_select_related.return_value = mock_manager

        from core.models import Harvests

        with patch(
            "core.views.Harvests.DoesNotExist",
            Exception,
        ):
            request = self.make_request(
                {
                    "harvest_id": 999,
                    "poultry_group_id": 20,
                    "transfer_date": "2026-09-19",
                    "quantity": 10,
                }
            )

            response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content)["error"],
            "Harvest not found",
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.Harvests.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_poultry_group_not_found(
        self,
        mock_can_add,
        mock_harvest_select_related,
        mock_group_select_related,
    ):
        mock_can_add.return_value = True

        mock_harvest_select_related.return_value.get.return_value = (
            self.harvest
        )

        mock_manager = Mock()
        mock_manager.get.side_effect = Exception("group not found")
        mock_group_select_related.return_value = mock_manager

        with patch(
            "core.views.PoultryGroups.DoesNotExist",
            Exception,
        ):
            request = self.make_request(
                {
                    "harvest_id": 15,
                    "poultry_group_id": 999,
                    "transfer_date": "2026-09-19",
                    "quantity": 10,
                }
            )

            response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json.loads(response.content)["error"],
            "Poultry group not found",
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.Harvests.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_requires_same_project(
        self,
        mock_can_add,
        mock_harvest_select_related,
        mock_group_select_related,
    ):
        mock_can_add.return_value = True

        mock_harvest_select_related.return_value.get.return_value = (
            self.harvest
        )

        mock_group_select_related.return_value.get.return_value = (
            self.other_poultry_group
        )

        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 30,
                "transfer_date": "2026-09-19",
                "quantity": 10,
            }
        )

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "Harvest and poultry group must belong to the same project",
        )

    @patch("core.views.authorization_service.has_project_scope")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.Harvests.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_out_of_scope(
        self,
        mock_can_add,
        mock_harvest_select_related,
        mock_group_select_related,
        mock_has_project_scope,
    ):
        mock_can_add.return_value = True
        mock_has_project_scope.return_value = False

        mock_harvest_select_related.return_value.get.return_value = (
            self.harvest
        )

        mock_group_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 20,
                "transfer_date": "2026-09-19",
                "quantity": 10,
            }
        )

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.timezone.now")
    @patch("core.views.FarmPoultryTransfers.objects.create")
    @patch("core.views.authorization_service.has_project_scope")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.Harvests.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_authorized(
        self,
        mock_can_add,
        mock_harvest_select_related,
        mock_group_select_related,
        mock_has_project_scope,
        mock_transfer_create,
        mock_timezone_now,
    ):
        mock_can_add.return_value = True
        mock_has_project_scope.return_value = True
        mock_timezone_now.return_value = "2026-09-19T10:00:00Z"

        mock_harvest_select_related.return_value.get.return_value = (
            self.harvest
        )

        mock_group_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        mock_transfer_create.return_value = self.transfer

        request = self.make_request(
            {
                "harvest_id": 15,
                "poultry_group_id": 20,
                "transfer_date": "2026-09-19",
                "quantity": 10,
                "unit": "kg",
                "notes": "Transferred for poultry use.",
            }
        )

        response = farm_poultry_transfer_create(request)

        self.assertEqual(response.status_code, 201)

        self.assertJSONEqual(
            response.content,
            {
                "farm_poultry_transfer": {
                    "transfer_id": 1,
                    "harvest_id": 15,
                    "poultry_group_id": 20,
                    "transfer_date": "2026-09-19",
                    "quantity": "10.00",
                    "unit": "kg",
                    "notes": "Transferred for poultry use.",
                    "recorded_by": 1,
                    "created_at": "2026-09-19T10:00:00Z",
                }
            },
        )

        mock_has_project_scope.assert_called_once_with(
            self.user,
            self.project,
        )

        mock_transfer_create.assert_called_once()

    @patch("core.authorization.decorators.authorization_service.can_view")
    def test_list_requires_view_permission(self, mock_can_view):
        mock_can_view.return_value = False

        request = self.factory.get("/farm-poultry-transfers/")
        request.user = self.user

        response = farm_poultry_transfers_list(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.FarmPoultryTransfers.objects.all")
    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service.can_view")
    def test_list_authorized(
        self,
        mock_can_view,
        mock_authorized_queryset,
        mock_all,
    ):
        mock_can_view.return_value = True

        mock_queryset = Mock()
        mock_queryset.values.return_value = [
            {
                "transfer_id": 1,
                "harvest_id": 15,
                "poultry_group_id": 20,
                "transfer_date": "2026-09-19",
                "quantity": Decimal("10.00"),
                "unit": "kg",
                "notes": "Transferred for poultry use.",
                "recorded_by_id": 1,
                "created_at": "2026-09-19T10:00:00Z",
            }
        ]

        mock_all.return_value = Mock()
        mock_authorized_queryset.return_value = mock_queryset

        request = self.factory.get("/farm-poultry-transfers/")
        request.user = self.user

        response = farm_poultry_transfers_list(request)

        self.assertEqual(response.status_code, 200)

        data = json.loads(response.content)

        self.assertEqual(
            data["farm_poultry_transfers"][0]["transfer_id"],
            1,
        )

        mock_authorized_queryset.assert_called_once_with(
            self.user,
            "farm_poultry_transfers",
            mock_all.return_value,
        )
