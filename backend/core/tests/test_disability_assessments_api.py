import json
from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.models import Beneficiaries
from core.views import disability_assessments_collection


class DisabilityAssessmentsApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
            user_id=42,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_post_request(self, user, body):
        request = self.factory.post(
            "/disability-assessments/",
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def make_get_request(self, user):
        request = self.factory.get(
            "/disability-assessments/",
        )
        request.user = user
        return request

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.DisabilityAssessments.objects.create")
    @patch("core.views.Beneficiaries.objects.get")
    @patch("django.utils.timezone.now")
    def test_post_authorized_creates_assessment(
        self,
        timezone_now,
        beneficiary_get,
        assessment_create,
        service,
    ):
        service.can_add.return_value = True
        timezone_now.return_value = "created-at"

        beneficiary = SimpleNamespace(
            beneficiary_id=10,
        )
        beneficiary_get.return_value = beneficiary

        assessment = SimpleNamespace(
            assessment_id=1,
            beneficiary_id=10,
            assessment_date=date(2026, 9, 7),
            assessment_type="Initial",
            disability_type="Physical",
            needs="Mobility support",
            assessment_notes="Assessment completed",
            assessed_by_id=42,
            created_at="created-at",
        )
        assessment_create.return_value = assessment

        request = self.make_post_request(
            self.authenticated_user,
            json.dumps({
                "beneficiary_id": 10,
                "assessment_date": "2026-09-07",
                "assessment_type": "Initial",
                "disability_type": "Physical",
                "needs": "Mobility support",
                "assessment_notes": "Assessment completed",
            }),
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "assessment": {
                    "assessment_id": 1,
                    "beneficiary_id": 10,
                    "assessment_date": "2026-09-07",
                    "assessment_type": "Initial",
                    "disability_type": "Physical",
                    "needs": "Mobility support",
                    "assessment_notes": "Assessment completed",
                    "assessed_by_id": 42,
                    "created_at": "created-at",
                }
            },
        )

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "disability_assessments",
            context=None,
        )

        beneficiary_get.assert_called_once_with(
            beneficiary_id=10,
        )

        assessment_create.assert_called_once_with(
            beneficiary=beneficiary,
            assessment_date=date(2026, 9, 7),
            assessment_type="Initial",
            disability_type="Physical",
            needs="Mobility support",
            assessment_notes="Assessment completed",
            assessed_by_id=42,
            created_at="created-at",
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_post_unauthenticated_returns_401(self, service):
        request = self.make_post_request(
            self.unauthenticated_user,
            json.dumps({
                "beneficiary_id": 10,
                "assessment_date": "2026-09-07",
            }),
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    def test_post_without_assessment_permission_returns_403(
        self,
        service,
    ):
        service.can_add.return_value = False

        request = self.make_post_request(
            self.authenticated_user,
            json.dumps({
                "beneficiary_id": 10,
                "assessment_date": "2026-09-07",
            }),
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "disability_assessments",
            context=None,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_post_invalid_json_returns_400(self, service):
        service.can_add.return_value = True

        request = self.make_post_request(
            self.authenticated_user,
            "{invalid-json",
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_post_missing_beneficiary_id_returns_400(self, service):
        service.can_add.return_value = True

        request = self.make_post_request(
            self.authenticated_user,
            json.dumps({
                "assessment_date": "2026-09-07",
            }),
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "beneficiary_id is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_post_missing_assessment_date_returns_400(self, service):
        service.can_add.return_value = True

        request = self.make_post_request(
            self.authenticated_user,
            json.dumps({
                "beneficiary_id": 10,
            }),
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "assessment_date is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_post_invalid_beneficiary_id_returns_400(self, service):
        service.can_add.return_value = True

        request = self.make_post_request(
            self.authenticated_user,
            json.dumps({
                "beneficiary_id": "invalid",
                "assessment_date": "2026-09-07",
            }),
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "beneficiary_id must be an integer"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_post_invalid_assessment_date_returns_400(self, service):
        service.can_add.return_value = True

        request = self.make_post_request(
            self.authenticated_user,
            json.dumps({
                "beneficiary_id": 10,
                "assessment_date": "07-09-2026",
            }),
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "assessment_date must use YYYY-MM-DD format",
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.DisabilityAssessments.objects.create")
    @patch("core.views.Beneficiaries.objects.get")
    def test_post_missing_beneficiary_returns_404(
        self,
        beneficiary_get,
        assessment_create,
        service,
    ):
        service.can_add.return_value = True
        beneficiary_get.side_effect = Beneficiaries.DoesNotExist

        request = self.make_post_request(
            self.authenticated_user,
            json.dumps({
                "beneficiary_id": 999,
                "assessment_date": "2026-09-07",
            }),
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Beneficiary not found"},
        )

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "disability_assessments",
            context=None,
        )

        beneficiary_get.assert_called_once_with(
            beneficiary_id=999,
        )

        assessment_create.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.authorized_queryset")
    @patch("core.views.DisabilityAssessments.objects.all")
    def test_get_authorized_returns_assessments(
        self,
        objects_all,
        authorized_queryset_mock,
        service,
    ):
        service.can_view.return_value = True

        queryset = SimpleNamespace(
            values=lambda *fields: [
                {
                    "assessment_id": 1,
                    "beneficiary_id": 10,
                    "assessment_date": date(2026, 9, 7),
                    "assessment_type": "Initial",
                    "disability_type": "Physical",
                    "needs": "Mobility support",
                    "assessment_notes": "Assessment completed",
                    "assessed_by_id": 42,
                    "created_at": "created-at",
                }
            ]
        )

        objects_all.return_value = "base-queryset"
        authorized_queryset_mock.return_value = queryset

        request = self.make_get_request(
            self.authenticated_user,
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "assessments": [
                    {
                        "assessment_id": 1,
                        "beneficiary_id": 10,
                        "assessment_date": "2026-09-07",
                        "assessment_type": "Initial",
                        "disability_type": "Physical",
                        "needs": "Mobility support",
                        "assessment_notes": "Assessment completed",
                        "assessed_by_id": 42,
                        "created_at": "created-at",
                    }
                ]
            },
        )

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            None,
            resource="disability_assessments",
            context=None,
        )

        objects_all.assert_called_once_with()

        authorized_queryset_mock.assert_called_once_with(
            self.authenticated_user,
            "disability_assessments",
            "base-queryset",
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_get_without_view_permission_returns_403(
        self,
        service,
    ):
        service.can_view.return_value = False

        request = self.make_get_request(
            self.authenticated_user,
        )

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    def test_unsupported_method_returns_405(self):
        request = self.factory.put(
            "/disability-assessments/",
            data=json.dumps({}),
            content_type="application/json",
        )
        request.user = self.authenticated_user

        response = disability_assessments_collection(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )
