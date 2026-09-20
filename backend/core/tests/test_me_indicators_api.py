import json
from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.models import Projects
from core.views import me_indicator_create


@override_settings(ROOT_URLCONF="config.urls")
class MeIndicatorsApiTests(SimpleTestCase):
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
            indicator_name="Percentage of beneficiaries receiving services",
            description="Measures beneficiaries who receive the planned service.",
            target_value=Decimal("80.00"),
            unit="percent",
            start_date=date(2026, 9, 1),
            end_date=date(2026, 12, 31),
            status="active",
            created_by_id=1,
            created_at=datetime(2026, 9, 19, 10, 0, 0),
            updated_at=datetime(2026, 9, 19, 10, 0, 0),
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_authentication(self, decorator_service):
        decorator_service.can_add.return_value = False

        request = self.factory.post(
            "/me-indicators/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "indicator_name": "Beneficiaries receiving services",
                }
            ),
            content_type="application/json",
        )

        request.user = SimpleNamespace(
            is_authenticated=False,
        )

        response = me_indicator_create(request)

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_add_permission(self, decorator_service):
        decorator_service.can_add.return_value = False

        request = self.factory.post(
            "/me-indicators/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "indicator_name": "Beneficiaries receiving services",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_get_request_returns_405(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.get(
            "/me-indicators/create/"
        )
        request.user = self.user

        response = me_indicator_create(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_json_returns_400(self, decorator_service):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/me-indicators/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_indicator_name_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/me-indicators/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "indicator_name is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_project_id_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        request = self.factory.post(
            "/me-indicators/create/",
            data=json.dumps(
                {
                    "indicator_name": "Beneficiaries receiving services",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "project_id is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_project_not_found_returns_404(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        with patch(
            "core.views.Projects.objects.get"
        ) as project_get:
            project_get.side_effect = Projects.DoesNotExist

            request = self.factory.post(
                "/me-indicators/create/",
                data=json.dumps(
                    {
                        "project_id": 10,
                        "indicator_name": (
                            "Beneficiaries receiving services"
                        ),
                    }
                ),
                content_type="application/json",
            )
            request.user = self.user

            response = me_indicator_create(request)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Project not found"},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_project_outside_scope_returns_403(
        self,
        decorator_service,
        service,
        project_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = False
        project_get.return_value = self.project

        request = self.factory.post(
            "/me-indicators/create/",
            data=json.dumps(
                {
                    "project_id": 10,
                    "indicator_name": (
                        "Beneficiaries receiving services"
                    ),
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_create(request)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to use this project"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_target_value_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        with patch(
            "core.views.Projects.objects.get"
        ) as project_get:
            project_get.return_value = self.project

            with patch(
                "core.views.authorization_service"
            ) as service:
                service.has_project_scope.return_value = True

                request = self.factory.post(
                    "/me-indicators/create/",
                    data=json.dumps(
                        {
                            "project_id": 10,
                            "indicator_name": (
                                "Beneficiaries receiving services"
                            ),
                            "target_value": "abc",
                        }
                    ),
                    content_type="application/json",
                )
                request.user = self.user

                response = me_indicator_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "target_value must be a valid number"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_start_date_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        with patch(
            "core.views.Projects.objects.get"
        ) as project_get:
            project_get.return_value = self.project

            with patch(
                "core.views.authorization_service"
            ) as service:
                service.has_project_scope.return_value = True

                request = self.factory.post(
                    "/me-indicators/create/",
                    data=json.dumps(
                        {
                            "project_id": 10,
                            "indicator_name": (
                                "Beneficiaries receiving services"
                            ),
                            "start_date": "19-09-2026",
                        }
                    ),
                    content_type="application/json",
                )
                request.user = self.user

                response = me_indicator_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "start_date must be in YYYY-MM-DD format"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_end_date_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        with patch(
            "core.views.Projects.objects.get"
        ) as project_get:
            project_get.return_value = self.project

            with patch(
                "core.views.authorization_service"
            ) as service:
                service.has_project_scope.return_value = True

                request = self.factory.post(
                    "/me-indicators/create/",
                    data=json.dumps(
                        {
                            "project_id": 10,
                            "indicator_name": (
                                "Beneficiaries receiving services"
                            ),
                            "end_date": "31-12-2026",
                        }
                    ),
                    content_type="application/json",
                )
                request.user = self.user

                response = me_indicator_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "end_date must be in YYYY-MM-DD format"
                )
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_start_date_after_end_date_returns_400(
        self,
        decorator_service,
    ):
        decorator_service.can_add.return_value = True

        with patch(
            "core.views.Projects.objects.get"
        ) as project_get:
            project_get.return_value = self.project

            with patch(
                "core.views.authorization_service"
            ) as service:
                service.has_project_scope.return_value = True

                request = self.factory.post(
                    "/me-indicators/create/",
                    data=json.dumps(
                        {
                            "project_id": 10,
                            "indicator_name": (
                                "Beneficiaries receiving services"
                            ),
                            "start_date": "2026-12-31",
                            "end_date": "2026-09-01",
                        }
                    ),
                    content_type="application/json",
                )
                request.user = self.user

                response = me_indicator_create(request)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "start_date cannot be after end_date"
                )
            },
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_project_indicator_authorized(
        self,
        decorator_service,
        service,
        project_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        project_get.return_value = self.project

        with patch(
            "core.views.MeIndicators.objects.create"
        ) as indicator_create:
            indicator_create.return_value = self.indicator

            with patch(
                "core.views.timezone.now"
            ) as now:
                now.return_value = datetime(
                    2026,
                    9,
                    19,
                    10,
                    0,
                    0,
                )

                request = self.factory.post(
                    "/me-indicators/create/",
                    data=json.dumps(
                        {
                            "project_id": 10,
                            "indicator_name": (
                                "Percentage of beneficiaries "
                                "receiving services"
                            ),
                            "description": (
                                "Measures beneficiaries who "
                                "receive the planned service."
                            ),
                            "target_value": "80.00",
                            "unit": "percent",
                            "start_date": "2026-09-01",
                            "end_date": "2026-12-31",
                            "status": "active",
                        }
                    ),
                    content_type="application/json",
                )
                request.user = self.user

                response = me_indicator_create(request)

        self.assertEqual(response.status_code, 201)

        indicator_create.assert_called_once_with(
            project=self.project,
            indicator_name=(
                "Percentage of beneficiaries receiving services"
            ),
            description=(
                "Measures beneficiaries who receive the planned service."
            ),
            target_value=Decimal("80.00"),
            unit="percent",
            start_date=date(2026, 9, 1),
            end_date=date(2026, 12, 31),
            status="active",
            created_by=self.user,
            created_at=now.return_value,
            updated_at=now.return_value,
        )

        self.assertJSONEqual(
            response.content,
            {
                "me_indicator": {
                    "indicator_id": 1,
                    "project_id": 10,
                    "indicator_name": (
                        "Percentage of beneficiaries "
                        "receiving services"
                    ),
                    "description": (
                        "Measures beneficiaries who receive "
                        "the planned service."
                    ),
                    "target_value": "80.00",
                    "unit": "percent",
                    "start_date": "2026-09-01",
                    "end_date": "2026-12-31",
                    "status": "active",
                    "created_by_id": 1,
                    "created_at": "2026-09-19T10:00:00",
                    "updated_at": "2026-09-19T10:00:00",
                }
            },
        )


    @patch("core.authorization.decorators.authorization_service")
    def test_list_requires_authentication(self, decorator_service):
        decorator_service.has_permission.return_value = False

        request = self.factory.get("/me-indicators/")
        request.user = SimpleNamespace(
            is_authenticated=False,
            is_active=True,
        )

        from core.views import me_indicators_list

        response = me_indicators_list(request)

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service")
    def test_list_requires_view_permission(self, decorator_service):
        decorator_service.can_view.return_value = False

        request = self.factory.get("/me-indicators/")
        request.user = self.user

        from core.views import me_indicators_list

        response = me_indicators_list(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_list_post_request_returns_405(self, decorator_service):
        decorator_service.can_view.return_value = True

        request = self.factory.post("/me-indicators/")
        request.user = self.user

        from core.views import me_indicators_list

        response = me_indicators_list(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_returns_authorized_indicators(
        self,
        decorator_service,
        authorized_queryset,
    ):
        decorator_service.can_view.return_value = True

        authorized_queryset.return_value.values.return_value = [
            {
                "indicator_id": 1,
                "project_id": 10,
                "indicator_name": (
                    "Percentage of beneficiaries receiving services"
                ),
                "description": (
                    "Measures beneficiaries who receive the planned service."
                ),
                "target_value": Decimal("80.00"),
                "unit": "percent",
                "start_date": date(2026, 9, 1),
                "end_date": date(2026, 12, 31),
                "status": "active",
                "created_by_id": 1,
                "created_at": datetime(2026, 9, 19, 10, 0, 0),
                "updated_at": datetime(2026, 9, 19, 10, 0, 0),
            }
        ]

        request = self.factory.get("/me-indicators/")
        request.user = self.user

        from core.views import me_indicators_list

        response = me_indicators_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "me_indicators": [
                    {
                        "indicator_id": 1,
                        "project_id": 10,
                        "indicator_name": (
                            "Percentage of beneficiaries receiving services"
                        ),
                        "description": (
                            "Measures beneficiaries who receive the planned service."
                        ),
                        "target_value": "80.00",
                        "unit": "percent",
                        "start_date": "2026-09-01",
                        "end_date": "2026-12-31",
                        "status": "active",
                        "created_by_id": 1,
                        "created_at": "2026-09-19T10:00:00",
                        "updated_at": "2026-09-19T10:00:00",
                    }
                ]
            },
        )

        authorized_queryset.assert_called_once()

    @patch("core.authorization.decorators.authorization_service")
    def test_record_list_requires_authentication(self, decorator_service):
        decorator_service.has_permission.return_value = False

        request = self.factory.get("/me-indicator-records/")
        request.user = SimpleNamespace(
            is_authenticated=False,
            is_active=True,
        )

        from core.views import me_indicator_records_list

        response = me_indicator_records_list(request)

        self.assertEqual(response.status_code, 401)

    @patch("core.authorization.decorators.authorization_service")
    def test_record_list_requires_view_permission(self, decorator_service):
        decorator_service.can_view.return_value = False

        request = self.factory.get("/me-indicator-records/")
        request.user = self.user

        from core.views import me_indicator_records_list

        response = me_indicator_records_list(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.authorization.decorators.authorization_service")
    def test_record_list_post_request_returns_405(self, decorator_service):
        decorator_service.can_view.return_value = True

        request = self.factory.post("/me-indicator-records/")
        request.user = self.user

        from core.views import me_indicator_records_list

        response = me_indicator_records_list(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_record_list_returns_authorized_records(
        self,
        decorator_service,
        authorized_queryset,
    ):
        decorator_service.can_view.return_value = True

        authorized_queryset.return_value.values.return_value = [
            {
                "indicator_record_id": 1,
                "indicator_id": 10,
                "record_date": date(2026, 9, 19),
                "recorded_value": Decimal("75.00"),
                "notes": "September progress recorded.",
                "recorded_by_id": 1,
                "created_at": datetime(2026, 9, 19, 11, 0, 0),
            }
        ]

        request = self.factory.get("/me-indicator-records/")
        request.user = self.user

        from core.views import me_indicator_records_list

        response = me_indicator_records_list(request)

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "me_indicator_records": [
                    {
                        "indicator_record_id": 1,
                        "indicator_id": 10,
                        "record_date": "2026-09-19",
                        "recorded_value": "75.00",
                        "notes": "September progress recorded.",
                        "recorded_by_id": 1,
                        "created_at": "2026-09-19T11:00:00",
                    }
                ]
            },
        )

        authorized_queryset.assert_called_once()
