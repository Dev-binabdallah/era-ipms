import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.views import beneficiaries_collection, beneficiaries_list


class BeneficiariesApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_request(self, user, method="get"):
        request = getattr(self.factory, method)(
            "/beneficiaries/",
        )
        request.user = user
        return request

    def test_unauthenticated_request_returns_401(self):
        response = beneficiaries_list(
            self.make_request(self.unauthenticated_user),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unauthorized_request_returns_403(self, service):
        service.can_view.return_value = False

        response = beneficiaries_list(
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
            resource="beneficiaries",
            context=None,
        )

    @patch("core.views.Beneficiaries.objects.all")
    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_request_uses_authorized_queryset(
        self,
        service,
        authorized_queryset,
        objects_all,
    ):
        service.can_view.return_value = True

        values_queryset = [
            {
                "beneficiary_id": 1,
                "beneficiary_code": "BEN-001",
                "first_name": "Test",
                "last_name": "Beneficiary",
            },
        ]

        queryset = SimpleNamespace(
            values=lambda *args: values_queryset,
        )

        authorized_queryset.return_value = queryset
        objects_all.return_value = SimpleNamespace()

        response = beneficiaries_list(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "beneficiaries": values_queryset,
            },
        )

        objects_all.assert_called_once_with()
        authorized_queryset.assert_called_once_with(
            self.authenticated_user,
            "beneficiaries",
            objects_all.return_value,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unsupported_method_returns_405(self, service):
        service.can_view.return_value = True

        response = beneficiaries_collection(
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


    @patch("core.views.Beneficiaries.objects.create")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_post_creates_beneficiary(
        self,
        service,
        objects_create,
    ):
        service.can_add.return_value = True

        beneficiary = SimpleNamespace(
            beneficiary_id=10,
            beneficiary_code="BEN-010",
            first_name="Amina",
            last_name="Hassan",
            date_of_birth=date(1995, 5, 10),
            sex="Female",
            location="Mombasa",
            phone="0700000000",
            registration_date=date(2026, 9, 7),
            status="active",
            created_by_id=42,
            created_at="2026-09-07T00:00:00Z",
            updated_at="2026-09-07T00:00:00Z",
        )

        objects_create.return_value = beneficiary

        payload = {
            "beneficiary_code": "BEN-010",
            "first_name": "Amina",
            "last_name": "Hassan",
            "date_of_birth": "1995-05-10",
            "sex": "Female",
            "location": "Mombasa",
            "phone": "0700000000",
            "registration_date": "2026-09-07",
        }

        request = self.factory.post(
            "/beneficiaries/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        request.user = SimpleNamespace(
            is_authenticated=True,
            user_id=42,
        )

        response = beneficiaries_collection(request)

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "beneficiary": {
                    "beneficiary_id": 10,
                    "beneficiary_code": "BEN-010",
                    "first_name": "Amina",
                    "last_name": "Hassan",
                    "date_of_birth": "1995-05-10",
                    "sex": "Female",
                    "location": "Mombasa",
                    "phone": "0700000000",
                    "registration_date": "2026-09-07",
                    "status": "active",
                    "created_by_id": 42,
                    "created_at": "2026-09-07T00:00:00Z",
                    "updated_at": "2026-09-07T00:00:00Z",
                }
            },
        )

        objects_create.assert_called_once()
        create_kwargs = objects_create.call_args.kwargs

        self.assertEqual(
            create_kwargs["beneficiary_code"],
            "BEN-010",
        )
        self.assertEqual(
            create_kwargs["first_name"],
            "Amina",
        )
        self.assertEqual(
            create_kwargs["last_name"],
            "Hassan",
        )
        self.assertEqual(
            create_kwargs["created_by_id"],
            42,
        )
        self.assertEqual(
            create_kwargs["status"],
            "active",
        )

        service.can_add.assert_called_once_with(
            request.user,
            "beneficiaries",
            context=None,
        )


    @patch("core.authorization.decorators.authorization_service")
    def test_post_without_registration_permission_returns_403(
        self,
        service,
    ):
        service.can_add.return_value = False

        request = self.factory.post(
            "/beneficiaries/",
            data=json.dumps({
                "beneficiary_code": "BEN-011",
                "first_name": "Test",
                "last_name": "User",
            }),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = beneficiaries_collection(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "beneficiaries",
            context=None,
        )


    @patch("core.authorization.decorators.authorization_service")
    def test_post_invalid_json_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/beneficiaries/",
            data="{invalid-json",
            content_type="application/json",
        )
        request.user = SimpleNamespace(
            is_authenticated=True,
            user_id=42,
        )

        response = beneficiaries_collection(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )


    @patch("core.authorization.decorators.authorization_service")
    def test_post_missing_required_field_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/beneficiaries/",
            data=json.dumps({
                "beneficiary_code": "BEN-012",
                "first_name": "Test",
            }),
            content_type="application/json",
        )
        request.user = SimpleNamespace(
            is_authenticated=True,
            user_id=42,
        )

        response = beneficiaries_collection(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "last_name is required"},
        )


    @patch("core.authorization.decorators.authorization_service")
    def test_post_invalid_date_returns_400(self, service):
        service.can_add.return_value = True

        request = self.factory.post(
            "/beneficiaries/",
            data=json.dumps({
                "beneficiary_code": "BEN-013",
                "first_name": "Test",
                "last_name": "User",
                "date_of_birth": "13-05-1995",
            }),
            content_type="application/json",
        )
        request.user = SimpleNamespace(
            is_authenticated=True,
            user_id=42,
        )

        response = beneficiaries_collection(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "date_of_birth must use YYYY-MM-DD format",
            },
        )
