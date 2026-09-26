import json
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.views import me_indicators_summary


class MeIndicatorSummaryApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = SimpleNamespace(is_authenticated=True)

    def test_me_indicator_summary_requires_authorization(self):
        request = self.factory.get("/me-indicators/summary/")
        request.user = self.user

        response = me_indicators_summary(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_me_indicator_summary_rejects_non_get_requests_after_authorization(
        self,
        mock_authorization_service,
    ):
        request = self.factory.post("/me-indicators/summary/")
        request.user = self.user

        mock_authorization_service.can_view.return_value = True

        response = me_indicators_summary(request)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json.loads(response.content),
            {"error": "Method not allowed"},
        )

        mock_authorization_service.can_view.assert_called_once_with(
            self.user,
            None,
            resource="me_indicators",
            context=None,
        )

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.authorized_queryset")
    def test_me_indicator_summary_returns_authorized_summary(
        self,
        mock_authorized_queryset,
        mock_authorization_service,
    ):
        request = self.factory.get("/me-indicators/summary/")
        request.user = self.user

        mock_authorization_service.can_view.return_value = True

        summary_rows = [
            {
                "indicator_id": 1,
                "project_id": 10,
                "indicator_name": "Persons receiving rehabilitation support",
                "target_value": 100,
                "unit": "persons",
                "latest_recorded_value": 75,
                "record_count": 3,
                "status": "Active",
            },
            {
                "indicator_id": 2,
                "project_id": 10,
                "indicator_name": "Referrals completed",
                "target_value": 50,
                "unit": "referrals",
                "latest_recorded_value": 32,
                "record_count": 2,
                "status": "Active",
            },
        ]

        mock_queryset = SimpleNamespace(
            annotate=lambda **kwargs: SimpleNamespace(
                values=lambda *args: summary_rows
            )
        )
        mock_authorized_queryset.return_value = mock_queryset

        response = me_indicators_summary(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json.loads(response.content),
            {"me_indicators_summary": summary_rows},
        )

        self.assertEqual(
            json.loads(response.content)["me_indicators_summary"][0],
            {
                "indicator_id": 1,
                "project_id": 10,
                "indicator_name": "Persons receiving rehabilitation support",
                "target_value": 100,
                "unit": "persons",
                "latest_recorded_value": 75,
                "record_count": 3,
                "status": "Active",
            },
        )

        mock_authorization_service.can_view.assert_called_once_with(
            self.user,
            None,
            resource="me_indicators",
            context=None,
        )

        mock_authorized_queryset.assert_called_once()
        self.assertEqual(
            mock_authorized_queryset.call_args.args[0],
            self.user,
        )
        self.assertEqual(
            mock_authorized_queryset.call_args.args[1],
            "me_indicators",
        )
