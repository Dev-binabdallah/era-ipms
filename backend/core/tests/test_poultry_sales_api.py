import json
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import RequestFactory, SimpleTestCase

from core.views import poultry_sale_create, poultry_sales_list


class PoultrySalesCreateApiTests(SimpleTestCase):
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

        self.poultry_group = SimpleNamespace(
            poultry_group_id=20,
            project=self.project,
        )

    def make_request(self, payload, method="post"):
        request = getattr(self.factory, method)(
            "/poultry-sales/create/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        request.user = self.user
        return request

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_requires_add_permission(self, mock_can_add):
        mock_can_add.return_value = False

        request = self.make_request(
            {
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": 5,
            }
        )

        response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_json(
        self,
        mock_can_add,
        mock_select_related,
    ):
        mock_can_add.return_value = True

        request = self.factory.post(
            "/poultry-sales/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(json.loads(response.content)["error"], "Invalid JSON")
        mock_select_related.assert_not_called()

    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_requires_fields(self, mock_can_add):
        mock_can_add.return_value = True

        request = self.make_request(
            {
                "poultry_group_id": 20,
            }
        )

        response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn("required", json.loads(response.content)["error"])

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_group_not_found(
        self,
        mock_can_add,
        mock_select_related,
    ):
        mock_can_add.return_value = True

        mock_manager = Mock()
        mock_manager.get.side_effect = Exception("group not found")
        mock_select_related.return_value = mock_manager

        request = self.make_request(
            {
                "poultry_group_id": 999,
                "sale_date": "2026-09-17",
                "quantity": 5,
            }
        )

        with patch(
            "core.views.PoultryGroups.DoesNotExist",
            Exception,
        ):
            response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 404)

    @patch("core.views.authorization_service.has_project_scope")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_out_of_scope_group(
        self,
        mock_can_add,
        mock_select_related,
        mock_has_project_scope,
    ):
        mock_can_add.return_value = True
        mock_has_project_scope.return_value = False

        mock_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        request = self.make_request(
            {
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": 5,
            }
        )

        response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_quantity(
        self,
        mock_can_add,
        mock_select_related,
    ):
        mock_can_add.return_value = True

        mock_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        request = self.make_request(
            {
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": "abc",
            }
        )

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "quantity must be an integer",
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_negative_quantity(
        self,
        mock_can_add,
        mock_select_related,
    ):
        mock_can_add.return_value = True

        mock_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        request = self.make_request(
            {
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": -1,
            }
        )

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "quantity cannot be negative",
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_invalid_price(
        self,
        mock_can_add,
        mock_select_related,
    ):
        mock_can_add.return_value = True

        mock_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        request = self.make_request(
            {
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": 5,
                "unit_price": "abc",
            }
        )

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertIn(
            "valid numbers",
            json.loads(response.content)["error"],
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_negative_unit_price(
        self,
        mock_can_add,
        mock_select_related,
    ):
        mock_can_add.return_value = True

        mock_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        request = self.make_request(
            {
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": 5,
                "unit_price": "-10.00",
            }
        )

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "unit_price cannot be negative",
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_negative_total_amount(
        self,
        mock_can_add,
        mock_select_related,
    ):
        mock_can_add.return_value = True

        mock_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        request = self.make_request(
            {
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": 5,
                "total_amount": "-100.00",
            }
        )

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json.loads(response.content)["error"],
            "total_amount cannot be negative",
        )

    @patch("core.views.PoultrySales.objects.create")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service.can_add")
    def test_create_success(
        self,
        mock_can_add,
        mock_select_related,
        mock_create,
    ):
        mock_can_add.return_value = True

        mock_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        sale = SimpleNamespace(
            poultry_sale_id=50,
            poultry_group_id=20,
            sale_date="2026-09-17",
            quantity=5,
            unit_price=Decimal("1500.00"),
            total_amount=Decimal("7500.00"),
            buyer_description="Local buyer",
            notes="Five birds sold",
            recorded_by_id=1,
            created_at="2026-09-17T10:00:00Z",
        )

        mock_create.return_value = sale

        request = self.make_request(
            {
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": 5,
                "unit_price": "1500.00",
                "total_amount": "7500.00",
                "buyer_description": "Local buyer",
                "notes": "Five birds sold",
            }
        )

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            response = poultry_sale_create(request)

        self.assertEqual(response.status_code, 201)

        data = json.loads(response.content)["poultry_sale"]

        self.assertEqual(data["poultry_sale_id"], 50)
        self.assertEqual(data["poultry_group_id"], 20)
        self.assertEqual(data["quantity"], 5)
        self.assertEqual(data["unit_price"], "1500.00")
        self.assertEqual(data["total_amount"], "7500.00")

        mock_create.assert_called_once()


class PoultrySalesListApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = SimpleNamespace(
            is_authenticated=True,
            is_active=True,
            user_id=1,
            username="testuser",
        )

    @patch("core.authorization.decorators.authorization_service.can_view")
    def test_list_requires_view_permission(self, mock_can_view):
        mock_can_view.return_value = False

        request = self.factory.get("/poultry-sales/")
        request.user = self.user

        response = poultry_sales_list(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service.can_view")
    def test_list_success(
        self,
        mock_can_view,
        mock_authorized_queryset,
    ):
        mock_can_view.return_value = True

        values_result = [
            {
                "poultry_sale_id": 50,
                "poultry_group_id": 20,
                "sale_date": "2026-09-17",
                "quantity": 5,
                "unit_price": "1500.00",
                "total_amount": "7500.00",
                "buyer_description": "Local buyer",
                "notes": "Five birds sold",
                "recorded_by_id": 1,
                "created_at": "2026-09-17T10:00:00Z",
            }
        ]

        mock_queryset = Mock()
        mock_queryset.values.return_value = values_result
        mock_authorized_queryset.return_value = mock_queryset

        request = self.factory.get("/poultry-sales/")
        request.user = self.user

        response = poultry_sales_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content)["poultry_sales"],
            values_result,
        )

        mock_authorized_queryset.assert_called_once()
        call_args = mock_authorized_queryset.call_args.args

        self.assertEqual(call_args[0], self.user)
        self.assertEqual(call_args[1], "poultry_sales")

    def test_list_rejects_post(self):
        request = self.factory.post("/poultry-sales/")
        request.user = self.user

        with patch(
            "core.authorization.decorators.authorization_service.can_view",
            return_value=True,
        ):
            response = poultry_sales_list(request)

        self.assertEqual(response.status_code, 405)
