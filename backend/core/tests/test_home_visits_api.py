import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.models import Beneficiaries
from core.views import (
    home_visit_create,
    home_visits_collection,
    home_visits_list,
)


class HomeVisitsApiTests(SimpleTestCase):
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
            "/home-visits/",
        )
        request.user = user
        return request

    @patch("core.authorization.decorators.authorization_service")
    def test_unauthenticated_request_returns_401(self, service):
        response = home_visits_list(
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

        response = home_visits_list(
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
            resource="home_visits",
            context=None,
        )

    @patch("core.views.HomeVisits.objects.all")
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
                "home_visit_id": 1,
                "beneficiary_id": 10,
                "visit_date": "2026-09-07",
                "conducted_by_id": 42,
                "purpose": "Household assessment",
                "observations": "Assessment completed.",
                "support_provided": "Information provided.",
                "follow_up_required": True,
                "next_action": "Follow up next month.",
                "created_at": "2026-09-07T00:00:00Z",
            },
        ]

        queryset = SimpleNamespace(
            values=lambda *args: values_queryset,
        )

        authorized_queryset.return_value = queryset
        objects_all.return_value = SimpleNamespace()

        response = home_visits_list(
            self.make_request(
                self.authenticated_user,
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "home_visits": values_queryset,
            },
        )

        objects_all.assert_called_once_with()
        authorized_queryset.assert_called_once_with(
            self.authenticated_user,
            "home_visits",
            objects_all.return_value,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unauthorized_post_returns_403(self, service):
        service.can_add.return_value = False

        payload = {
            "beneficiary_id": 10,
            "visit_date": "2026-09-07",
        }

        request = self.factory.post(
            "/home-visits/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = home_visit_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "home_visits",
            context=None,
        )

    @patch("core.views.HomeVisits.objects.create")
    @patch("core.views.Beneficiaries.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_post_creates_home_visit(
        self,
        service,
        beneficiary_get,
        objects_create,
    ):
        service.can_add.return_value = True

        beneficiary = SimpleNamespace(
            beneficiary_id=25,
        )
        beneficiary_get.return_value = beneficiary

        home_visit = SimpleNamespace(
            home_visit_id=10,
            beneficiary_id=25,
            visit_date=date(2026, 9, 7),
            conducted_by_id=42,
            purpose="Household assessment",
            observations="Beneficiary requires follow-up support.",
            support_provided="Provided information on available services.",
            follow_up_required=True,
            next_action="Schedule follow-up visit.",
            created_at="2026-09-07T00:00:00Z",
        )

        objects_create.return_value = home_visit

        payload = {
            "beneficiary_id": 25,
            "visit_date": "2026-09-07",
            "purpose": "Household assessment",
            "observations": "Beneficiary requires follow-up support.",
            "support_provided": "Provided information on available services.",
            "follow_up_required": True,
            "next_action": "Schedule follow-up visit.",
        }

        request = self.factory.post(
            "/home-visits/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = home_visit_create(request)

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "home_visit": {
                    "home_visit_id": 10,
                    "beneficiary_id": 25,
                    "visit_date": "2026-09-07",
                    "conducted_by_id": 42,
                    "purpose": "Household assessment",
                    "observations": "Beneficiary requires follow-up support.",
                    "support_provided": "Provided information on available services.",
                    "follow_up_required": True,
                    "next_action": "Schedule follow-up visit.",
                    "created_at": "2026-09-07T00:00:00Z",
                }
            },
        )

        beneficiary_get.assert_called_once_with(
            beneficiary_id=25,
        )

        objects_create.assert_called_once_with(
            beneficiary=beneficiary,
            visit_date=date(2026, 9, 7),
            conducted_by_id=42,
            purpose="Household assessment",
            observations="Beneficiary requires follow-up support.",
            support_provided="Provided information on available services.",
            follow_up_required=True,
            next_action="Schedule follow-up visit.",
            created_at=objects_create.call_args.kwargs["created_at"],
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.HomeVisits.objects.create")
    @patch("core.views.Beneficiaries.objects.get")
    def test_post_missing_beneficiary_returns_404(
        self,
        beneficiary_get,
        objects_create,
        service,
    ):
        service.can_add.return_value = True
        beneficiary_get.side_effect = Beneficiaries.DoesNotExist

        request = self.factory.post(
            "/home-visits/",
            data=json.dumps(
                {
                    "beneficiary_id": 999,
                    "visit_date": "2026-09-07",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = home_visit_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Beneficiary not found"},
        )

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "home_visits",
            context=None,
        )

        beneficiary_get.assert_called_once_with(
            beneficiary_id=999,
        )

        objects_create.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    def test_invalid_json_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/home-visits/",
            data="{invalid-json",
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = home_visit_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_missing_beneficiary_id_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/home-visits/",
            data=json.dumps(
                {
                    "visit_date": "2026-09-07",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = home_visit_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "beneficiary_id is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_missing_visit_date_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/home-visits/",
            data=json.dumps(
                {
                    "beneficiary_id": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = home_visit_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "visit_date is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_invalid_beneficiary_id_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/home-visits/",
            data=json.dumps(
                {
                    "beneficiary_id": "invalid",
                    "visit_date": "2026-09-07",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = home_visit_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "beneficiary_id must be an integer"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_invalid_visit_date_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/home-visits/",
            data=json.dumps(
                {
                    "beneficiary_id": 25,
                    "visit_date": "07-09-2026",
                }
            ),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = home_visit_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "visit_date must use YYYY-MM-DD format",
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unsupported_method_returns_405(self, service):
        service.can_view.return_value = True

        response = home_visits_collection(
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
