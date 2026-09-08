import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.views import (
    referral_create,
    referral_submit,
    referrals_collection,
    referrals_list,
    referral_follow_up_create,
    referral_follow_ups_list,
)


class ReferralsApiTests(SimpleTestCase):

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Referrals.objects.get")
    def test_submit_unauthenticated_request_returns_401(
        self,
        referral_get,
        service,
    ):
        response = referral_submit(
            self.make_request(
                self.unauthenticated_user,
                "post",
            ),
            7,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        referral_get.assert_not_called()
        service.can_edit.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Referrals.objects.get")
    def test_submit_unauthorized_request_returns_403(
        self,
        referral_get,
        service,
    ):
        referral = SimpleNamespace(
            referral_id=7,
            status="pending",
        )

        referral_get.return_value = referral
        service.can_edit.return_value = False

        response = referral_submit(
            self.make_request(
                self.authenticated_user,
                "post",
            ),
            7,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        referral_get.assert_called_once_with(
            referral_id=7,
        )

        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            referral,
            resource="referrals",
            context=None,
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Referrals.objects.get")
    def test_submit_missing_referral_returns_404(
        self,
        referral_get,
        service,
    ):
        service.can_edit.return_value = True

        from core.models import Referrals

        referral_get.side_effect = Referrals.DoesNotExist

        response = referral_submit(
            self.make_request(
                self.authenticated_user,
                "post",
            ),
            999,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Referral not found"},
        )

        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            None,
            resource="referrals",
            context=None,
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Referrals.objects.get")
    def test_submit_already_submitted_returns_409(
        self,
        referral_get,
        service,
    ):
        referral = SimpleNamespace(
            referral_id=7,
            status="submitted",
        )

        referral_get.return_value = referral
        service.can_edit.return_value = True

        response = referral_submit(
            self.make_request(
                self.authenticated_user,
                "post",
            ),
            7,
        )

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(
            response.content,
            {"error": "Referral is already submitted"},
        )

        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            referral,
            resource="referrals",
            context=None,
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Referrals.objects.get")
    def test_submit_non_pending_referral_returns_409(
        self,
        referral_get,
        service,
    ):
        referral = SimpleNamespace(
            referral_id=7,
            status="approved",
        )

        referral_get.return_value = referral
        service.can_edit.return_value = True

        response = referral_submit(
            self.make_request(
                self.authenticated_user,
                "post",
            ),
            7,
        )

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "Referral cannot be submitted from status "
                    "'approved'"
                )
            },
        )

        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            referral,
            resource="referrals",
            context=None,
        )

    @patch("django.utils.timezone.now")
    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Referrals.objects.get")
    def test_submit_pending_referral_updates_status(
        self,
        referral_get,
        service,
        timezone_now,
    ):
        referral = SimpleNamespace(
            referral_id=7,
            beneficiary_id=10,
            referral_date=date(2026, 9, 7),
            destination="Health Centre",
            reason="Medical assessment required.",
            referred_by_id=42,
            status="pending",
            approved_by_id=None,
            approved_at=None,
            created_at="original-created-at",
            updated_at="original-updated-at",
        )

        referral_get.return_value = referral
        service.can_edit.return_value = True
        timezone_now.return_value = "new-updated-at"

        def save(**kwargs):
            referral.save_kwargs = kwargs

        referral.save = save

        response = referral_submit(
            self.make_request(
                self.authenticated_user,
                "post",
            ),
            7,
        )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(
            referral.status,
            "submitted",
        )
        self.assertEqual(
            referral.updated_at,
            "new-updated-at",
        )

        self.assertIsNone(
            referral.approved_by_id,
        )
        self.assertIsNone(
            referral.approved_at,
        )

        self.assertEqual(
            referral.save_kwargs["update_fields"],
            [
                "status",
                "updated_at",
            ],
        )

        self.assertJSONEqual(
            response.content,
            {
                "referral": {
                    "referral_id": 7,
                    "beneficiary_id": 10,
                    "referral_date": "2026-09-07",
                    "destination": "Health Centre",
                    "reason": "Medical assessment required.",
                    "referred_by_id": 42,
                    "status": "submitted",
                    "approved_by_id": None,
                    "approved_at": None,
                    "created_at": "original-created-at",
                    "updated_at": "new-updated-at",
                }
            },
        )

        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            referral,
            resource="referrals",
            context=None,
        )


    @patch("core.views.ReferralFollowUps.objects.create")
    @patch("core.views.Referrals.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_follow_up_create_allows_authorized_user(
        self,
        service,
        referral_get,
        follow_up_create,
    ):
        referral = SimpleNamespace(
            referral_id=7,
        )

        follow_up = SimpleNamespace(
            follow_up_id=1,
            referral_id=7,
            follow_up_date=date(2026, 9, 8),
            conducted_by_id=42,
            outcome="Service received",
            service_received=True,
            remaining_needs=None,
            next_action="Monitor",
            created_at="2026-09-08T10:00:00Z",
        )

        referral_get.return_value = referral
        service.can_add.return_value = True
        follow_up_create.return_value = follow_up

        request = self.factory.post(
            "/referrals/7/follow-ups/",
            data=json.dumps(
                {
                    "follow_up_date": "2026-09-08",
                    "outcome": "Service received",
                    "service_received": True,
                    "next_action": "Monitor",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_follow_up_create(
            request,
            7,
        )

        self.assertEqual(response.status_code, 201)

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "follow_ups",
            context={"referral": referral},
        )

        follow_up_create.assert_called_once()

        create_kwargs = follow_up_create.call_args.kwargs

        self.assertIs(
            create_kwargs["referral"],
            referral,
        )
        self.assertEqual(
            create_kwargs["follow_up_date"],
            date(2026, 9, 8),
        )
        self.assertEqual(
            create_kwargs["conducted_by_id"],
            42,
        )
        self.assertEqual(
            create_kwargs["outcome"],
            "Service received",
        )
        self.assertTrue(
            create_kwargs["service_received"],
        )
        self.assertIsNone(
            create_kwargs["remaining_needs"],
        )
        self.assertEqual(
            create_kwargs["next_action"],
            "Monitor",
        )
        self.assertIsNotNone(
            create_kwargs["created_at"],
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Referrals.objects.get")
    def test_follow_up_create_denies_unauthorized_user(
        self,
        referral_get,
        service,
    ):
        referral = SimpleNamespace(
            referral_id=7,
        )

        referral_get.return_value = referral
        service.can_add.return_value = False

        request = self.factory.post(
            "/referrals/7/follow-ups/",
            data=json.dumps(
                {
                    "follow_up_date": "2026-09-08",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = referral_follow_up_create(
            request,
            7,
        )

        self.assertEqual(response.status_code, 403)

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "follow_ups",
            context={"referral": referral},
        )

    @patch("core.views.ReferralFollowUps.objects.filter")
    @patch("core.views.Referrals.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_follow_ups_list_allows_authorized_user(
        self,
        service,
        referral_get,
        follow_ups_filter,
    ):
        referral = SimpleNamespace(
            referral_id=7,
        )

        referral_get.return_value = referral
        service.can_view.return_value = True

        follow_ups_filter.return_value.values.return_value = [
            {
                "follow_up_id": 1,
                "referral_id": 7,
                "follow_up_date": date(2026, 9, 8),
                "conducted_by_id": 42,
                "outcome": "Service received",
                "service_received": True,
                "remaining_needs": None,
                "next_action": "Monitor",
                "created_at": "2026-09-08T10:00:00Z",
            }
        ]

        request = self.make_request(
            self.authenticated_user,
            "get",
        )

        response = referral_follow_ups_list(
            request,
            7,
        )

        self.assertEqual(response.status_code, 200)

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            referral,
            resource="follow_ups",
            context=None,
        )

        follow_ups_filter.assert_called_once_with(
            referral_id=7,
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.Referrals.objects.get")
    def test_follow_ups_list_denies_unauthorized_user(
        self,
        referral_get,
        service,
    ):
        referral = SimpleNamespace(
            referral_id=7,
        )

        referral_get.return_value = referral
        service.can_view.return_value = False

        request = self.make_request(
            self.authenticated_user,
            "get",
        )

        response = referral_follow_ups_list(
            request,
            7,
        )

        self.assertEqual(response.status_code, 403)

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            referral,
            resource="follow_ups",
            context=None,
        )


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
            context={"beneficiary_id": 10},
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
            status="pending",
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
                    "status": "pending",
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
            status="pending",
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
            status="pending",
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
            "pending",
        )

        self.assertEqual(
            objects_create.call_args.kwargs["status"],
            "pending",
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
