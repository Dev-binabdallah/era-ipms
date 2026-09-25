import json
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.views import dashboard_summary


class DashboardSummaryApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_dashboard_summary_requires_authentication(self):
        request = self.factory.get("/dashboard/summary/")
        request.user = SimpleNamespace(is_authenticated=False)

        response = dashboard_summary(request)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(json.loads(response.content), {"authorized": False})

    def test_dashboard_summary_allows_get_for_authenticated_user(self):
        request = self.factory.get("/dashboard/summary/")
        request.user = SimpleNamespace(is_authenticated=True)

        authorized_queryset_mock = patch(
            "core.views.authorized_queryset"
        )

        with authorized_queryset_mock as mock_authorized_queryset:
            mock_queryset = SimpleNamespace(count=lambda: 0)
            mock_authorized_queryset.return_value = mock_queryset

            response = dashboard_summary(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {
                "summary": {
                    "projects": 0,
                    "activities": 0,
                    "beneficiaries": 0,
                    "referrals": 0,
                    "poultry_groups": 0,
                    "farm_crops": 0,
                    "financial_transactions": 0,
                    "me_indicators": 0,
                }
            },
        )

        self.assertEqual(mock_authorized_queryset.call_count, 8)

    def test_dashboard_summary_rejects_non_get_requests(self):
        request = self.factory.post("/dashboard/summary/")
        request.user = SimpleNamespace(is_authenticated=True)

        response = dashboard_summary(request)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json.loads(response.content),
            {"error": "Method not allowed"},
        )
