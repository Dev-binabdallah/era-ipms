import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.views import (
    referral_create,
    referrals_collection,
    referrals_list,
)


class ReferralsApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
            user_id=42,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_request(self, user, method="get"):
        request = getattr(self.factory, method)(
            "/referrals/",
        )
        request.user = user
        return request

    @patch("core.authorization.decorators.authorization_service")
    def test_unauthenticated_request_returns_401(self, service):
        response = referrals_list(
            self.make_request(self.unauthenticated_user),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unauthorized_get_returns_403(self, service):
        service.can_view.return_value = False

        response = referrals_list(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            None,
            resource="referrals",
            context=None,
        )

    @patch("core.views.Referrals.objects.all")
    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_get_uses_authorized_queryset(
        self,
        service,
        authorized_queryset,
        objects_all,
    ):
        service.can_view.return_value = True

        values_queryset = [
            {
                "referral_id": 1,
                "beneficiary_id": 10,
                "referral_date": "2026-09-07",
                "destination": "Health Centre",
                "reason": "Medical assessment required.",
                "referred_by_id": 42,
                "status": "submitted",
                "approved_by_id": None,
                "approved_at": None,
                "created_at": "2026-09-07T00:00:00Z",
                "updated_at": "2026-09-07T00:00:00Z",
            },
        ]

        queryset = SimpleNamespace(
            values=lambda *args: values_queryset,
        )

        authorized_queryset.return_value = queryset
        objects_all.return_value = SimpleNamespace()

        response = referrals_list(
            self.make_request(
                self.authenticated_user,
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "referrals": values_queryset,
            },
        )

        objects_all.assert_called_once_with()
        authorized_queryset.assert_called_once_with(
            self.authenticated_user,
            "referrals",
            objects_all.return_value,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unauthorized_post_returns_403(self, service):
        service.can_add.return_value = False

        payload = {
            "beneficiary_id": 10,
            "referral_date": "2026-09-07",
            "destination": "Health Centre",
        }

        request = self.factory.post(
            "/referrals/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "referrals",
            context=None,
        )

    @patch("core.views.Referrals.objects.create")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_post_creates_referral(
        self,
        service,
        objects_create,
    ):
        service.can_add.return_value = True

        referral = SimpleNamespace(
            referral_id=10,
            beneficiary_id=25,
            referral_date=date(2026, 9, 7),
            destination="Health Centre",
            reason="Medical assessment required.",
            referred_by_id=42,
            status="submitted",
            approved_by_id=None,
            approved_at=None,
            created_at="2026-09-07T00:00:00Z",
            updated_at="2026-09-07T00:00:00Z",
        )

        objects_create.return_value = referral

        payload = {
            "beneficiary_id": 25,
            "referral_date": "2026-09-07",
            "destination": "Health Centre",
            "reason": "Medical assessment required.",
        }

        request = self.factory.post(
            "/referrals/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "referral": {
                    "referral_id": 10,
                    "beneficiary_id": 25,
                    "referral_date": "2026-09-07",
                    "destination": "Health Centre",
                    "reason": "Medical assessment required.",
                    "referred_by_id": 42,
                    "status": "submitted",
                    "approved_by_id": None,
                    "approved_at": None,
                    "created_at": "2026-09-07T00:00:00Z",
                    "updated_at": "2026-09-07T00:00:00Z",
                }
            },
        )

        objects_create.assert_called_once_with(
            beneficiary_id=25,
            referral_date=date(2026, 9, 7),
            destination="Health Centre",
            reason="Medical assessment required.",
            referred_by_id=42,
            status="submitted",
            approved_by_id=None,
            approved_at=None,
            created_at=objects_create.call_args.kwargs["created_at"],
            updated_at=objects_create.call_args.kwargs["updated_at"],
        )

    @patch("core.views.Referrals.objects.create")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_post_ignores_client_supplied_status(
        self,
        service,
        objects_create,
    ):
        service.can_add.return_value = True

        referral = SimpleNamespace(
            referral_id=11,
            beneficiary_id=25,
            referral_date=date(2026, 9, 7),
            destination="Health Centre",
            reason="Status override test",
            referred_by_id=42,
            status="submitted",
            approved_by_id=None,
            approved_at=None,
            created_at="2026-09-07T00:00:00Z",
            updated_at="2026-09-07T00:00:00Z",
        )

        objects_create.return_value = referral

        payload = {
            "beneficiary_id": 25,
            "referral_date": "2026-09-07",
            "destination": "Health Centre",
            "reason": "Status override test",
            "status": "approved",
        }

        request = self.factory.post(
            "/referrals/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.content)

        self.assertEqual(
            response_data["referral"]["status"],
            "submitted",
        )

        self.assertEqual(
            objects_create.call_args.kwargs["status"],
            "submitted",
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_invalid_json_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/referrals/",
            data="{invalid-json",
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_missing_beneficiary_id_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/referrals/",
            data=json.dumps(
                {
                    "referral_date": "2026-09-07",
                    "destination": "Health Centre",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "beneficiary_id is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_missing_referral_date_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/referrals/",
            data=json.dumps(
                {
                    "beneficiary_id": 25,
                    "destination": "Health Centre",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "referral_date is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_missing_destination_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/referrals/",
            data=json.dumps(
                {
                    "beneficiary_id": 25,
                    "referral_date": "2026-09-07",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "destination is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_invalid_beneficiary_id_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/referrals/",
            data=json.dumps(
                {
                    "beneficiary_id": "invalid",
                    "referral_date": "2026-09-07",
                    "destination": "Health Centre",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "beneficiary_id must be an integer"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_invalid_referral_date_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/referrals/",
            data=json.dumps(
                {
                    "beneficiary_id": 25,
                    "referral_date": "07-09-2026",
                    "destination": "Health Centre",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "referral_date must use YYYY-MM-DD format",
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unsupported_method_returns_405(self, service):
        service.can_view.return_value = True

        response = referrals_collection(
            self.make_request(
                self.authenticated_user,
                method="put",
            ),
        )

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )
