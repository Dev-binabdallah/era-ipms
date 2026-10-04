from datetime import date
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.beneficiary_service_views import (
    disability_assessment_update,
    home_visit_update,
)


class BeneficiaryServiceLifecycleUpdateApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True)
        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False
        )

    def make_patch_request(self, user, path, body):
        request = self.factory.patch(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def test_assessment_update_unauthenticated_returns_401(self):
        response = disability_assessment_update(
            self.make_patch_request(
                self.unauthenticated_user,
                "/disability-assessments/1/",
                b'{"needs":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(response.content, {"authorized": False})

    @patch("core.beneficiary_service_views.DisabilityAssessments.objects.get")
    @patch("core.beneficiary_service_views.authorization_service")
    def test_assessment_update_unauthorized_returns_403(
        self,
        service,
        record_get,
    ):
        record_get.return_value = SimpleNamespace()
        service.can_edit.return_value = False

        response = disability_assessment_update(
            self.make_patch_request(
                self.user,
                "/disability-assessments/1/",
                b'{"needs":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(response.content, {"authorized": False})

    @patch("core.beneficiary_service_views.DisabilityAssessments.objects.get")
    @patch("core.beneficiary_service_views.authorization_service")
    def test_assessment_update_success(self, service, record_get):
        record = SimpleNamespace(
            assessment_id=1,
            beneficiary_id=2,
            assessment_date=date(2026, 9, 1),
            assessment_type="Initial",
            disability_type="Physical",
            needs="Old needs",
            assessment_notes="Old notes",
            assessed_by_id=5,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = disability_assessment_update(
            self.make_patch_request(
                self.user,
                "/disability-assessments/1/",
                b'{"needs":"Updated needs","assessment_notes":"Updated notes"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(record.needs, "Updated needs")
        self.assertEqual(record.assessment_notes, "Updated notes")

    @patch("core.beneficiary_service_views.HomeVisits.objects.get")
    @patch("core.beneficiary_service_views.authorization_service")
    def test_home_visit_update_success(self, service, record_get):
        record = SimpleNamespace(
            home_visit_id=1,
            beneficiary_id=2,
            visit_date=date(2026, 9, 1),
            conducted_by_id=5,
            purpose="Assessment",
            observations="Old observations",
            support_provided="Old support",
            follow_up_required=False,
            next_action=None,
            created_at="created",
        )
        record_get.return_value = record
        service.can_edit.return_value = True
        record.save = lambda **kwargs: None

        response = home_visit_update(
            self.make_patch_request(
                self.user,
                "/home-visits/1/",
                b'{"follow_up_required":true,"next_action":"Call partner"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(record.follow_up_required)
        self.assertEqual(record.next_action, "Call partner")

    @patch("core.beneficiary_service_views.HomeVisits.objects.get")
    @patch("core.beneficiary_service_views.authorization_service")
    def test_home_visit_update_rejects_non_boolean_follow_up(
        self,
        service,
        record_get,
    ):
        record_get.return_value = SimpleNamespace()
        service.can_edit.return_value = True

        response = home_visit_update(
            self.make_patch_request(
                self.user,
                "/home-visits/1/",
                b'{"follow_up_required":"yes"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "follow_up_required must be true or false"},
        )

    @patch("core.beneficiary_service_views.DisabilityAssessments.objects.get")
    @patch("core.beneficiary_service_views.authorization_service")
    def test_assessment_update_protects_relationships(
        self,
        service,
        record_get,
    ):
        record_get.return_value = SimpleNamespace()
        service.can_edit.return_value = True

        response = disability_assessment_update(
            self.make_patch_request(
                self.user,
                "/disability-assessments/1/",
                b'{"beneficiary_id":99}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Protected fields cannot be modified",
                "fields": ["beneficiary_id"],
            },
        )

    @patch("core.beneficiary_service_views.HomeVisits.objects.get")
    def test_home_visit_missing_returns_404(self, record_get):
        from core.models import HomeVisits

        record_get.side_effect = HomeVisits.DoesNotExist

        response = home_visit_update(
            self.make_patch_request(
                self.user,
                "/home-visits/1/",
                b'{"purpose":"Updated"}',
            ),
            1,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Home visit not found"},
        )

    def test_all_update_endpoints_reject_get(self):
        endpoints = [
            (
                disability_assessment_update,
                1,
                "/disability-assessments/1/",
            ),
            (home_visit_update, 1, "/home-visits/1/"),
        ]

        for view, record_id, path in endpoints:
            request = self.factory.get(path)
            request.user = self.user
            response = view(request, record_id)

            self.assertEqual(response.status_code, 405)
            self.assertJSONEqual(
                response.content,
                {"error": "Method not allowed"},
            )
