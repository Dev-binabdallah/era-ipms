from datetime import date
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.finance_views import financial_transaction_update


class FinancialTransactionUpdateApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True)
        self.unauthenticated_user = SimpleNamespace(is_authenticated=False)

    def make_patch_request(self, user, body):
        request = self.factory.patch(
            "/financial-transactions/1/",
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def test_update_requires_authentication(self):
        response = financial_transaction_update(
            self.make_patch_request(
                self.unauthenticated_user,
                b'{"amount":"1200.00"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"authorized": False})

    @patch("core.finance_views.FinancialTransactions.objects.get")
    @patch("core.finance_views.authorization_service")
    def test_update_requires_authorization(self, service, transaction_get):
        transaction_get.return_value = SimpleNamespace()
        service.can_edit.return_value = False

        response = financial_transaction_update(
            self.make_patch_request(
                self.user,
                b'{"amount":"1200.00"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {"authorized": False})

    @patch("core.finance_views.FinancialTransactions.objects.get")
    @patch("core.finance_views.authorization_service")
    @patch("django.utils.timezone.now")
    def test_update_success(
        self,
        timezone_now,
        service,
        transaction_get,
    ):
        transaction = SimpleNamespace(
            transaction_id=1,
            project_id=10,
            transaction_date=date(2026, 9, 1),
            transaction_type="expense",
            category="Feed",
            amount=Decimal("1000.00"),
            description="Old",
            payment_method="Cash",
            reference_number="REF-001",
            recorded_by_id=5,
            approved_by_id=None,
            approved_at=None,
            status="recorded",
            created_at="created",
            updated_at="old-updated",
        )
        transaction_get.return_value = transaction
        service.can_edit.return_value = True
        timezone_now.return_value = "new-updated"
        transaction.save = lambda **kwargs: None

        response = financial_transaction_update(
            self.make_patch_request(
                self.user,
                b'{"amount":"1200.50","description":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(transaction.amount, Decimal("1200.50"))
        self.assertEqual(transaction.description, "Updated")
        self.assertEqual(transaction.updated_at, "new-updated")

    @patch("core.finance_views.FinancialTransactions.objects.get")
    @patch("core.finance_views.authorization_service")
    def test_update_rejects_approval_fields(
        self,
        service,
        transaction_get,
    ):
        transaction_get.return_value = SimpleNamespace()
        service.can_edit.return_value = True

        response = financial_transaction_update(
            self.make_patch_request(
                self.user,
                b'{"status":"approved","approved_by_id":4}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Protected fields cannot be modified",
                "fields": ["approved_by_id", "status"],
            },
        )

    @patch("core.finance_views.FinancialTransactions.objects.get")
    @patch("core.finance_views.authorization_service")
    def test_update_invalid_amount_returns_400(
        self,
        service,
        transaction_get,
    ):
        transaction_get.return_value = SimpleNamespace()
        service.can_edit.return_value = True

        response = financial_transaction_update(
            self.make_patch_request(
                self.user,
                b'{"amount":"not-a-number"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "amount must be a valid number"},
        )

    @patch("core.finance_views.FinancialTransactions.objects.get")
    def test_update_missing_transaction_returns_404(self, transaction_get):
        from core.models import FinancialTransactions

        transaction_get.side_effect = FinancialTransactions.DoesNotExist

        response = financial_transaction_update(
            self.make_patch_request(
                self.user,
                b'{"amount":"1200.00"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Financial transaction not found"},
        )

    def test_update_get_returns_405(self):
        request = self.factory.get("/financial-transactions/1/")
        request.user = self.user

        response = financial_transaction_update(request, 1)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )
