from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.referral_workflow import referral_approve


class ReferralApprovalApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
            user_id=42,
        )
        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_request(self, user, method="post", referral_id=7):
        request = getattr(
            self.factory,
            method,
        )(
            f"/referrals/{referral_id}/approve/",
        )
        request.user = user
        return request

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.referral_workflow.Referrals.objects.get")
    def test_unauthenticated_returns_401(self, referral_get, service):
        response = referral_approve(
            self.make_request(self.unauthenticated_user),
            7,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"authorized": False})
        referral_get.assert_not_called()
        service.can_approve.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.referral_workflow.Referrals.objects.get")
    def test_unauthorized_returns_403(self, referral_get, service):
        referral = SimpleNamespace(referral_id=7, status="submitted")
        referral_get.return_value = referral
        service.can_approve.return_value = False

        response = referral_approve(
            self.make_request(self.authenticated_user),
            7,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {"authorized": False})
        service.can_approve.assert_called_once_with(
            self.authenticated_user,
            referral,
            resource="referrals",
            context=None,
        )

    @patch("core.referral_workflow.timezone.now")
    @patch("core.authorization.decorators.authorization_service")
    @patch("core.referral_workflow.Referrals.objects.get")
    def test_submitted_referral_is_approved(
        self,
        referral_get,
        service,
        now_mock,
    ):
        now = "2026-09-08T12:00:00Z"
        referral = SimpleNamespace(
            referral_id=7,
            beneficiary_id=25,
            referral_date=date(2026, 9, 8),
            destination="Health Centre",
            reason="Medical assessment",
            referred_by_id=11,
            status="submitted",
            approved_by_id=None,
            approved_at=None,
            created_at="2026-09-08T09:00:00Z",
            updated_at="2026-09-08T09:00:00Z",
        )
        referral_get.return_value = referral
        service.can_approve.return_value = True
        now_mock.return_value = now

        response = referral_approve(
            self.make_request(self.authenticated_user),
            7,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(referral.status, "approved")
        self.assertEqual(referral.approved_by_id, 42)
        self.assertEqual(referral.approved_at, now)
        self.assertEqual(referral.updated_at, now)
        referral.save.assert_not_called() if hasattr(referral, "assert_not_called") else None

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.referral_workflow.Referrals.objects.get")
    def test_already_approved_returns_409(self, referral_get, service):
        referral = SimpleNamespace(
            referral_id=7,
            status="approved",
        )
        referral_get.return_value = referral
        service.can_approve.return_value = True

        response = referral_approve(
            self.make_request(self.authenticated_user),
            7,
        )

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(
            response.content,
            {"error": "Referral is already approved"},
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.referral_workflow.Referrals.objects.get")
    def test_non_submitted_status_returns_409(self, referral_get, service):
        referral = SimpleNamespace(
            referral_id=7,
            status="completed",
        )
        referral_get.return_value = referral
        service.can_approve.return_value = True

        response = referral_approve(
            self.make_request(self.authenticated_user),
            7,
        )

        self.assertEqual(response.status_code, 409)
        self.assertIn(
            "cannot be approved",
            response.content.decode(),
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.referral_workflow.Referrals.objects.get")
    def test_missing_referral_returns_404(self, referral_get, service):
        from core.models import Referrals

        referral_get.side_effect = Referrals.DoesNotExist
        service.can_approve.return_value = True

        response = referral_approve(
            self.make_request(self.authenticated_user),
            7,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Referral not found"},
        )
