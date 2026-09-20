import json
from datetime import date, datetime
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.models import MeIndicatorRecords, MeIndicators, Projects
from core.views import (
    me_indicator_create,
    me_indicator_update,
)


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
            project=self.project,
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
    def test_update_requires_authentication(self, decorator_service):
        decorator_service.can_edit.return_value = False

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps(
                {
                    "indicator_name": "Updated indicator",
                }
            ),
            content_type="application/json",
        )

        request.user = SimpleNamespace(
            is_authenticated=False,
        )

        response = me_indicator_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 401)

    @patch("core.models.MeIndicators.objects")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_requires_edit_permission(
        self,
        decorator_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = False
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps(
                {
                    "indicator_name": "Updated indicator",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 403)

    @patch("core.models.MeIndicators.objects")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_get_request_returns_405(
        self,
        decorator_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.get(
            "/me-indicators/1/update/"
        )
        request.user = self.user

        response = me_indicator_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_json_returns_400(
        self,
        decorator_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_indicator_success(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True

        indicator = SimpleNamespace(
            indicator_id=1,
            project=self.project,
            project_id=10,
            indicator_name="Old indicator",
            description="Old description",
            target_value=Decimal("50.00"),
            unit="percent",
            start_date=date(2026, 9, 1),
            end_date=date(2026, 12, 31),
            status="active",
            created_by_id=1,
            created_at=datetime(2026, 9, 19, 10, 0, 0),
            updated_at=datetime(2026, 9, 19, 10, 0, 0),
        )
        indicator.save = lambda **kwargs: None

        indicator_objects.select_related.return_value.get.return_value = (
            indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps(
                {
                    "indicator_name": "Updated indicator",
                    "description": "Updated description",
                    "target_value": 80,
                    "unit": "beneficiaries",
                    "start_date": "2026-09-10",
                    "end_date": "2026-12-20",
                    "status": "ongoing",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 200)

        response_data = json.loads(response.content)
        updated_at = response_data["me_indicator"].pop("updated_at", None)

        self.assertTrue(updated_at)

        response_data_without_timestamp = json.dumps(response_data)

        self.assertJSONEqual(
            response_data_without_timestamp,
            {
                "me_indicator": {
                    "indicator_id": 1,
                    "project_id": 10,
                    "indicator_name": "Updated indicator",
                    "description": "Updated description",
                    "target_value": "80",
                    "unit": "beneficiaries",
                    "start_date": "2026-09-10",
                    "end_date": "2026-12-20",
                    "status": "ongoing",
                    "created_by_id": 1,
                    "created_at": "2026-09-19T10:00:00",
                }
            },
        )

        self.assertEqual(indicator.indicator_name, "Updated indicator")
        self.assertEqual(indicator.description, "Updated description")
        self.assertEqual(indicator.target_value, Decimal("80"))
        self.assertEqual(indicator.unit, "beneficiaries")
        self.assertEqual(indicator.start_date, date(2026, 9, 10))
        self.assertEqual(indicator.end_date, date(2026, 12, 20))
        self.assertEqual(indicator.status, "ongoing")
        self.assertTrue(indicator.updated_at)

    @patch("core.models.MeIndicators.objects")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_indicator_not_found_returns_404(
        self,
        decorator_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        indicator_objects.select_related.return_value.get.side_effect = (
            MeIndicators.DoesNotExist
        )

        request = self.factory.patch(
            "/me-indicators/999/update/",
            data=json.dumps({"indicator_name": "Updated indicator"}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 999)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Indicator not found"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_outside_project_scope_returns_403(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = False
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"indicator_name": "Updated indicator"}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to update this indicator"
                )
            },
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_protected_field_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"created_by_id": 99}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Protected fields cannot be modified",
                "fields": ["created_by_id"],
            },
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_unknown_field_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"unexpected_field": "value"}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Unknown fields",
                "fields": ["unexpected_field"],
            },
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_empty_payload_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "At least one editable field is required"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_negative_target_value_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"target_value": -10}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "target_value cannot be negative"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_target_value_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"target_value": "not-a-number"}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "target_value must be a valid number"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_start_date_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"start_date": "not-a-date"}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "start_date must be in "
                    "YYYY-MM-DD format"
                )
            },
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_end_date_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"end_date": "not-a-date"}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "end_date must be in "
                    "YYYY-MM-DD format"
                )
            },
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_start_date_after_end_date_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps(
                {
                    "start_date": "2027-01-01",
                    "end_date": "2026-12-31",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "start_date cannot be after end_date"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_description_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"description": 123}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "description must be text"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_unit_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"unit": 123}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "unit must be text"},
        )

    @patch("core.models.MeIndicators.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_status_returns_400(
        self,
        decorator_service,
        view_service,
        indicator_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        indicator_objects.select_related.return_value.get.return_value = (
            self.indicator
        )

        request = self.factory.patch(
            "/me-indicators/1/update/",
            data=json.dumps({"status": 123}),
            content_type="application/json",
        )
        request.user = self.user

        response = me_indicator_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "status must be text"},
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


class MeIndicatorRecordUpdateApiTests(SimpleTestCase):
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
            indicator_id=10,
            project=self.project,
            project_id=10,
        )

        self.record = SimpleNamespace(
            indicator_record_id=1,
            indicator=self.indicator,
            indicator_id=10,
            record_date=date(2026, 9, 19),
            recorded_value=Decimal("75.00"),
            notes="Original notes.",
            recorded_by_id=1,
            created_at=datetime(2026, 9, 19, 11, 0, 0),
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_update_requires_authentication(self, decorator_service):
        decorator_service.can_edit.return_value = False

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps(
                {
                    "recorded_value": 80,
                }
            ),
            content_type="application/json",
        )

        request.user = SimpleNamespace(
            is_authenticated=False,
        )

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 401)

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_requires_edit_permission(
        self,
        decorator_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = False
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps(
                {
                    "recorded_value": 80,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 403)

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_get_request_returns_405(
        self,
        decorator_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.get(
            "/me-indicator-records/1/update/"
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_json_returns_400(
        self,
        decorator_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_record_success(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True

        self.record.save = lambda **kwargs: None

        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps(
                {
                    "record_date": "2026-09-20",
                    "recorded_value": 80,
                    "notes": "Updated progress.",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 200)

        self.assertJSONEqual(
            response.content,
            {
                "me_indicator_record": {
                    "indicator_record_id": 1,
                    "indicator_id": 10,
                    "record_date": "2026-09-20",
                    "recorded_value": "80",
                    "notes": "Updated progress.",
                    "recorded_by_id": 1,
                    "created_at": "2026-09-19T11:00:00",
                }
            },
        )

        self.assertEqual(
            self.record.record_date,
            date(2026, 9, 20),
        )
        self.assertEqual(
            self.record.recorded_value,
            Decimal("80"),
        )
        self.assertEqual(
            self.record.notes,
            "Updated progress.",
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_record_not_found_returns_404(
        self,
        decorator_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        record_objects.select_related.return_value.get.side_effect = (
            MeIndicatorRecords.DoesNotExist
        )

        request = self.factory.patch(
            "/me-indicator-records/999/update/",
            data=json.dumps({"recorded_value": 80}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 999)

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Indicator record not found"},
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_outside_project_scope_returns_403(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = False
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({"recorded_value": 80}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to update this "
                    "indicator record"
                )
            },
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_protected_field_returns_400(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({"indicator_id": 99}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Protected fields cannot be modified",
                "fields": ["indicator_id"],
            },
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_unknown_field_returns_400(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({"unexpected_field": "value"}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Unknown fields",
                "fields": ["unexpected_field"],
            },
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_empty_payload_returns_400(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "At least one editable field is required"},
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_record_date_returns_400(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({"record_date": "not-a-date"}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "record_date must be in "
                    "YYYY-MM-DD format"
                )
            },
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_missing_record_date_returns_400(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({"record_date": None}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "record_date is required"},
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_recorded_value_returns_400(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({"recorded_value": "not-a-number"}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "recorded_value must be a valid number"},
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_missing_recorded_value_returns_400(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({"recorded_value": None}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "recorded_value is required"},
        )

    @patch("core.models.MeIndicatorRecords.objects")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_notes_returns_400(
        self,
        decorator_service,
        view_service,
        record_objects,
    ):
        decorator_service.can_edit.return_value = True
        view_service.has_project_scope.return_value = True
        record_objects.select_related.return_value.get.return_value = (
            self.record
        )

        request = self.factory.patch(
            "/me-indicator-records/1/update/",
            data=json.dumps({"notes": 123}),
            content_type="application/json",
        )
        request.user = self.user

        from core.views import me_indicator_record_update

        response = me_indicator_record_update(request, 1)

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "notes must be text"},
        )
