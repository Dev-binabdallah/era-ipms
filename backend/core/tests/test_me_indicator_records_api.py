import json
from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.models import MeIndicators
from core.views import me_indicator_record_create


@override_settings(ROOT_URLCONF="config.urls")
class MeIndicatorRecordsApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = SimpleNamespace(
            user_id=1,
            is_authenticated=True,
        )

        self.project = SimpleNamespace(
            project_id=10,
        )

        self.indicator = SimpleNamespace(
            indicator_id=1,
            project_id=10,
            project=self.project,
        )

        self.record = SimpleNamespace(
            indicator_record_id=1,
            indicator_id=1,
            record_date=date(2026, 9, 19),
            recorded_value=Decimal("25.00"),
            notes="Monthly monitoring record.",
            recorded_by_id=1,
            created_at=datetime(2026, 9, 19, 10, 0, 0),
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_authentication(self, decorator_service):
        decorator_service.can_add.return_value = False

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "record_date": "2026-09-19",
                    "recorded_value": 25,
                }
            ),
            content_type="application/json",
        )

        request.user = SimpleNamespace(
            is_authenticated=False,
        )

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_add_permission(self, decorator_service):
        decorator_service.can_add.return_value = False

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "record_date": "2026-09-19",
                    "recorded_value": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_get_request_returns_405(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.get(
            "/me-indicator-records/create/"
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_json_returns_400(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/me-indicator-records/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_indicator_id_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "record_date": "2026-09-19",
                    "recorded_value": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "indicator_id is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_indicator_not_found_returns_404(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        with patch(
            "core.views.MeIndicators.objects.select_related"
        ) as indicator_query:
            indicator_query.return_value.get.side_effect = (
                MeIndicators.DoesNotExist
            )

            request = self.factory.post(
                "/me-indicator-records/create/",
                data=json.dumps(
                    {
                        "indicator_id": 1,
                        "record_date": "2026-09-19",
                        "recorded_value": 25,
                    }
                ),
                content_type="application/json",
            )
            request.user = self.user

            response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Indicator not found"},
        )

    @patch("core.views.MeIndicators.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_indicator_outside_scope_returns_403(
        self,
        decorator_service,
        service,
        indicator_query,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = False
        indicator_query.return_value.get.return_value = self.indicator

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "record_date": "2026-09-19",
                    "recorded_value": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to use this indicator"
                )
            },
        )

    @patch("core.views.MeIndicators.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_record_date_returns_400(
        self,
        decorator_service,
        service,
        indicator_query,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        indicator_query.return_value.get.return_value = self.indicator

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "recorded_value": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "record_date is required"},
        )

    @patch("core.views.MeIndicators.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_record_date_returns_400(
        self,
        decorator_service,
        service,
        indicator_query,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        indicator_query.return_value.get.return_value = self.indicator

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "record_date": "19-09-2026",
                    "recorded_value": 25,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "record_date must be in YYYY-MM-DD format"},
        )

    @patch("core.views.MeIndicators.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_recorded_value_returns_400(
        self,
        decorator_service,
        service,
        indicator_query,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        indicator_query.return_value.get.return_value = self.indicator

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "record_date": "2026-09-19",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "recorded_value is required"},
        )

    @patch("core.views.MeIndicators.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_recorded_value_returns_400(
        self,
        decorator_service,
        service,
        indicator_query,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        indicator_query.return_value.get.return_value = self.indicator

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "record_date": "2026-09-19",
                    "recorded_value": "not-a-number",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "recorded_value must be a valid number"},
        )

    @patch("core.views.MeIndicators.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_notes_returns_400(
        self,
        decorator_service,
        service,
        indicator_query,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        indicator_query.return_value.get.return_value = self.indicator

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "record_date": "2026-09-19",
                    "recorded_value": 25,
                    "notes": 123,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "notes must be text"},
        )

    @patch("core.views.MeIndicatorRecords.objects.create")
    @patch("core.views.MeIndicators.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_authorized_indicator_creates_record(
        self,
        decorator_service,
        service,
        indicator_query,
        record_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        indicator_query.return_value.get.return_value = self.indicator
        record_create.return_value = self.record

        request = self.factory.post(
            "/me-indicator-records/create/",
            data=json.dumps(
                {
                    "indicator_id": 1,
                    "record_date": "2026-09-19",
                    "recorded_value": "25.00",
                    "notes": "Monthly monitoring record.",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        with patch(
            "core.views.timezone.now",
            return_value=self.record.created_at,
        ):
            response = me_indicator_record_create(request)

        self.assertEqual(response.status_code, 201)

        record_create.assert_called_once_with(
            indicator=self.indicator,
            record_date=date(2026, 9, 19),
            recorded_value=Decimal("25.00"),
            notes="Monthly monitoring record.",
            recorded_by=self.user,
            created_at=self.record.created_at,
        )

        self.assertJSONEqual(
            response.content,
            {
                "me_indicator_record": {
                    "indicator_record_id": 1,
                    "indicator_id": 1,
                    "record_date": "2026-09-19",
                    "recorded_value": "25.00",
                    "notes": "Monthly monitoring record.",
                    "recorded_by_id": 1,
                    "created_at": "2026-09-19T10:00:00",
                }
            },
        )
