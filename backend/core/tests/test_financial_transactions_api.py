import json
from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.models import Projects
from core.views import (
    financial_transaction_create,
    financial_transactions_list,
)


@override_settings(ROOT_URLCONF="config.urls")
class FinancialTransactionsApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = SimpleNamespace(
            user_id=1,
            is_authenticated=True,
        )

        self.project = SimpleNamespace(
            project_id=10,
        )

        self.transaction = SimpleNamespace(
            transaction_id=1,
            project_id=10,
            transaction_date=date(2026, 9, 18),
            transaction_type="expense",
            category="Transport",
            amount=Decimal("1500.00"),
            description="Transport for field activity",
            payment_method="Cash",
            reference_number="REF-001",
            recorded_by_id=1,
            status="recorded",
            created_at=datetime(2026, 9, 18, 10, 0, 0),
            updated_at=datetime(2026, 9, 18, 10, 0, 0),
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_authentication(self, decorator_service):
        decorator_service.can_add.return_value = False

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Transport",
                    "amount": "1500.00",
                }
            ),
            content_type="application/json",
        )

        request.user = SimpleNamespace(
            is_authenticated=False,
        )

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_add_permission(self, decorator_service):
        decorator_service.can_add.return_value = False

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Transport",
                    "amount": "1500.00",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_get_request_returns_405(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.get(
            "/financial-transactions/create/"
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_json_returns_400(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/financial-transactions/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_required_data_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "transaction_date": "2026-09-18",
                    "category": "Transport",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "transaction_date, transaction_type, "
                    "category, and amount are required"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_date_returns_400(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "transaction_date": "18-09-2026",
                    "transaction_type": "expense",
                    "category": "Transport",
                    "amount": "1500.00",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "transaction_date must be in YYYY-MM-DD format"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_amount_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Transport",
                    "amount": "abc",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "amount must be a valid number"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_non_positive_amount_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Transport",
                    "amount": "0",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "amount must be greater than 0"},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_project_transaction_authorized(
        self,
        decorator_service,
        service,
        project_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        project_get.return_value = self.project

        with patch(
            "core.views.FinancialTransactions.objects.create"
        ) as transaction_create:
            transaction_create.return_value = self.transaction

            with patch(
                "core.views.timezone.now"
            ) as now:
                now.return_value = datetime(
                    2026,
                    9,
                    18,
                    10,
                    0,
                    0,
                )

                request = self.factory.post(
                    "/financial-transactions/create/",
                    data=json.dumps(
                        {
                            "project_id": 10,
                            "transaction_date": "2026-09-18",
                            "transaction_type": "expense",
                            "category": "Transport",
                            "amount": "1500.00",
                            "description": "Transport for field activity",
                            "payment_method": "Cash",
                            "reference_number": "REF-001",
                        }
                    ),
                    content_type="application/json",
                )
                request.user = self.user

                response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 201)

        transaction_create.assert_called_once_with(
            project=self.project,
            transaction_date=date(2026, 9, 18),
            transaction_type="expense",
            category="Transport",
            amount=Decimal("1500.00"),
            description="Transport for field activity",
            payment_method="Cash",
            reference_number="REF-001",
            recorded_by=self.user,
            status="recorded",
            created_at=now.return_value,
            updated_at=now.return_value,
        )

        self.assertJSONEqual(
            response.content,
            {
                "financial_transaction": {
                    "transaction_id": 1,
                    "project_id": 10,
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Transport",
                    "amount": "1500.00",
                    "description": "Transport for field activity",
                    "payment_method": "Cash",
                    "reference_number": "REF-001",
                    "recorded_by": 1,
                    "status": "recorded",
                    "created_at": "2026-09-18T10:00:00",
                    "updated_at": "2026-09-18T10:00:00",
                }
            },
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_project_not_found_returns_404(
        self,
        decorator_service,
        project_get,
    ):
        decorator_service.can_add.return_value = True
        project_get.side_effect = Projects.DoesNotExist

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Transport",
                    "amount": "1500.00",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Project not found"},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_project_transaction_outside_scope_returns_403(
        self,
        decorator_service,
        service,
        project_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = False
        project_get.return_value = self.project

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Transport",
                    "amount": "1500.00",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to use this project"
                )
            },
        )

    @patch("core.views.FinancialTransactions.objects.create")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_organization_transaction_authorized(
        self,
        decorator_service,
        service,
        transaction_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_organization_financial_scope.return_value = True
        transaction_create.return_value = SimpleNamespace(
            transaction_id=2,
            project_id=None,
            transaction_date=date(2026, 9, 18),
            transaction_type="expense",
            category="Office expenses",
            amount=Decimal("2500.00"),
            description="Office supplies",
            payment_method="Cash",
            reference_number="OFF-001",
            recorded_by_id=1,
            status="recorded",
            created_at=datetime(2026, 9, 18, 11, 0, 0),
            updated_at=datetime(2026, 9, 18, 11, 0, 0),
        )

        with patch(
            "core.views.timezone.now"
        ) as now:
            now.return_value = datetime(
                2026,
                9,
                18,
                11,
                0,
                0,
            )

            request = self.factory.post(
                "/financial-transactions/create/",
                data=json.dumps(
                    {
                        "transaction_date": "2026-09-18",
                        "transaction_type": "expense",
                        "category": "Office expenses",
                        "amount": "2500.00",
                        "description": "Office supplies",
                        "payment_method": "Cash",
                        "reference_number": "OFF-001",
                    }
                ),
                content_type="application/json",
            )
            request.user = self.user

            response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 201)

        transaction_create.assert_called_once_with(
            project=None,
            transaction_date=date(2026, 9, 18),
            transaction_type="expense",
            category="Office expenses",
            amount=Decimal("2500.00"),
            description="Office supplies",
            payment_method="Cash",
            reference_number="OFF-001",
            recorded_by=self.user,
            status="recorded",
            created_at=now.return_value,
            updated_at=now.return_value,
        )

        self.assertJSONEqual(
            response.content,
            {
                "financial_transaction": {
                    "transaction_id": 2,
                    "project_id": None,
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Office expenses",
                    "amount": "2500.00",
                    "description": "Office supplies",
                    "payment_method": "Cash",
                    "reference_number": "OFF-001",
                    "recorded_by": 1,
                    "status": "recorded",
                    "created_at": "2026-09-18T11:00:00",
                    "updated_at": "2026-09-18T11:00:00",
                }
            },
        )

    @patch("core.views.FinancialTransactions.objects.create")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_organization_transaction_without_financial_scope_returns_403(
        self,
        decorator_service,
        service,
        transaction_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_organization_financial_scope.return_value = False

        request = self.factory.post(
            "/financial-transactions/create/",
            data=json.dumps(
                {
                    "transaction_date": "2026-09-18",
                    "transaction_type": "expense",
                    "category": "Office expenses",
                    "amount": "2500.00",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = financial_transaction_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to record "
                    "organization-level financial transactions"
                )
            },
        )

        transaction_create.assert_not_called()

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_returns_authorized_transactions(
        self,
        decorator_service,
        authorized_queryset,
    ):
        decorator_service.can_view.return_value = True

        transaction = SimpleNamespace(
            transaction_id=1,
            project_id=10,
            transaction_date=date(2026, 9, 18),
            transaction_type="expense",
            category="Transport",
            amount=Decimal("1500.00"),
            description="Transport support",
            payment_method="Cash",
            reference_number="TR-001",
            recorded_by_id=1,
            approved_by_id=None,
            approved_at=None,
            status="recorded",
            created_at=datetime(2026, 9, 18, 10, 0, 0),
            updated_at=datetime(2026, 9, 18, 10, 0, 0),
        )

        authorized_queryset.return_value = [transaction]

        request = self.factory.get(
            "/financial-transactions/"
        )
        request.user = self.user

        response = financial_transactions_list(request)

        self.assertEqual(response.status_code, 200)

        authorized_queryset.assert_called_once()

        self.assertJSONEqual(
            response.content,
            {
                "financial_transactions": [
                    {
                        "transaction_id": 1,
                        "project_id": 10,
                        "transaction_date": "2026-09-18",
                        "transaction_type": "expense",
                        "category": "Transport",
                        "amount": "1500.00",
                        "description": "Transport support",
                        "payment_method": "Cash",
                        "reference_number": "TR-001",
                        "recorded_by_id": 1,
                        "approved_by_id": None,
                        "approved_at": None,
                        "status": "recorded",
                        "created_at": "2026-09-18T10:00:00",
                        "updated_at": "2026-09-18T10:00:00",
                    }
                ]
            },
        )

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_returns_empty_when_no_authorized_transactions(
        self,
        decorator_service,
        authorized_queryset,
    ):
        decorator_service.can_view.return_value = True
        authorized_queryset.return_value = []

        request = self.factory.get(
            "/financial-transactions/"
        )
        request.user = self.user

        response = financial_transactions_list(request)

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            response.content,
            {"financial_transactions": []},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_list_requires_view_permission(
        self,
        decorator_service,
    ):
        decorator_service.can_view.return_value = False

        request = self.factory.get(
            "/financial-transactions/"
        )
        request.user = self.user

        response = financial_transactions_list(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_list_requires_get_request(
        self,
        decorator_service,
    ):
        decorator_service.can_view.return_value = True

        request = self.factory.post(
            "/financial-transactions/"
        )
        request.user = self.user

        response = financial_transactions_list(request)

        self.assertEqual(response.status_code, 405)
