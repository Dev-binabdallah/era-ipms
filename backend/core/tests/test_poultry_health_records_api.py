import json
from datetime import date
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.models import Projects, PoultryGroups, PoultryHealthRecords, Users
from core.views import (
    poultry_health_record_create,
    poultry_health_records_list,
)


class PoultryHealthRecordsApiTests(SimpleTestCase):

    def setUp(self):
        self.factory = RequestFactory()

        self.user = Users(
            user_id=1,
        )

        self.project = Projects(
            project_id=1,
        )

        self.poultry_group = PoultryGroups(
            poultry_group_id=1,
            project=self.project,
        )

    def make_request(self, method, path, data=None):
        body = json.dumps(data) if data is not None else b""

        request = getattr(self.factory, method.lower())(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = self.user
        return request

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_add_permission(
        self,
        mock_authorization,
        mock_select_related,
    ):
        mock_authorization.can_add.return_value = False

        mock_select_related.return_value.get.return_value = (
            self.poultry_group
        )

        request = self.make_request(
            "POST",
            "/poultry-health-records/create/",
            {
                "poultry_group_id": 1,
                "record_date": "2026-09-17",
                "condition_type": "Disease",
                "number_affected": 3,
            },
        )

        response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_requires_view_permission(
        self,
        mock_authorization,
        mock_authorized_queryset,
    ):
        mock_authorization.can_view.return_value = False

        request = self.make_request(
            "GET",
            "/poultry-health-records/",
        )

        response = poultry_health_records_list(request)

        self.assertEqual(response.status_code, 403)
        mock_authorized_queryset.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    def test_create_rejects_invalid_json(self, mock_authorization):
        mock_authorization.has_permission.return_value = True

        request = self.factory.post(
            "/poultry-health-records/create/",
            data="{invalid",
            content_type="application/json",
        )
        request.user = self.user

        response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 400)

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_fields(self, mock_authorization):
        mock_authorization.has_permission.return_value = True

        request = self.make_request(
            "POST",
            "/poultry-health-records/create/",
            {
                "poultry_group_id": 1,
            },
        )

        response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 400)

    @patch("core.authorization.decorators.authorization_service")
    @patch("core.views.PoultryGroups.objects.select_related")
    def test_create_returns_404_when_group_not_found(
        self,
        mock_select_related,
        mock_authorization,
    ):
        mock_authorization.has_permission.return_value = True

        mock_select_related.return_value.get.side_effect = (
            __import__("core.models", fromlist=["PoultryGroups"])
            .PoultryGroups.DoesNotExist
        )

        request = self.make_request(
            "POST",
            "/poultry-health-records/create/",
            {
                "poultry_group_id": 999,
                "record_date": "2026-09-17",
                "condition_type": "Disease",
                "number_affected": 3,
            },
        )

        response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 404)

    @patch("core.views.PoultryHealthRecords.objects.create")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_rejects_out_of_scope_group(
        self,
        mock_authorization,
        mock_select_related,
        mock_create,
    ):
        mock_authorization.has_permission.return_value = True
        mock_select_related.return_value.get.return_value = self.poultry_group

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=False,
        ):
            request = self.make_request(
                "POST",
                "/poultry-health-records/create/",
                {
                    "poultry_group_id": 1,
                    "record_date": "2026-09-17",
                    "condition_type": "Disease",
                    "number_affected": 3,
                },
            )

            response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 403)
        mock_create.assert_not_called()

    @patch("core.views.PoultryHealthRecords.objects.create")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_rejects_invalid_number_affected(
        self,
        mock_authorization,
        mock_select_related,
        mock_create,
    ):
        mock_authorization.has_permission.return_value = True
        mock_select_related.return_value.get.return_value = self.poultry_group

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            request = self.make_request(
                "POST",
                "/poultry-health-records/create/",
                {
                    "poultry_group_id": 1,
                    "record_date": "2026-09-17",
                    "condition_type": "Disease",
                    "number_affected": "abc",
                },
            )

            response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 400)
        mock_create.assert_not_called()

    @patch("core.views.PoultryHealthRecords.objects.create")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_rejects_negative_number_affected(
        self,
        mock_authorization,
        mock_select_related,
        mock_create,
    ):
        mock_authorization.has_permission.return_value = True
        mock_select_related.return_value.get.return_value = self.poultry_group

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            request = self.make_request(
                "POST",
                "/poultry-health-records/create/",
                {
                    "poultry_group_id": 1,
                    "record_date": "2026-09-17",
                    "condition_type": "Disease",
                    "number_affected": -1,
                },
            )

            response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 400)
        mock_create.assert_not_called()

    @patch("core.views.PoultryHealthRecords.objects.create")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_health_record_success(
        self,
        mock_authorization,
        mock_select_related,
        mock_create,
    ):
        mock_authorization.has_permission.return_value = True
        mock_select_related.return_value.get.return_value = self.poultry_group

        created_record = PoultryHealthRecords(
            health_record_id=10,
            poultry_group=self.poultry_group,
            record_date=date(2026, 9, 17),
            condition_type="Disease",
            number_affected=3,
            description="Three birds showed signs of illness.",
            action_taken="Separated affected birds.",
            outcome="Under observation.",
            recorded_by=self.user,
        )

        mock_create.return_value = created_record

        with patch(
            "core.views.authorization_service.has_project_scope",
            return_value=True,
        ):
            request = self.make_request(
                "POST",
                "/poultry-health-records/create/",
                {
                    "poultry_group_id": 1,
                    "record_date": "2026-09-17",
                    "condition_type": "Disease",
                    "number_affected": 3,
                    "description": "Three birds showed signs of illness.",
                    "action_taken": "Separated affected birds.",
                    "outcome": "Under observation.",
                },
            )

            response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 201)
        mock_create.assert_called_once()

        payload = json.loads(response.content)
        self.assertEqual(
            payload["poultry_health_record"]["health_record_id"],
            10,
        )
        self.assertEqual(
            payload["poultry_health_record"]["number_affected"],
            3,
        )

    @patch("core.views.PoultryHealthRecords.objects.all")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_returns_authorized_health_records(
        self,
        mock_authorization,
        mock_all,
    ):
        mock_authorization.has_permission.return_value = True

        records = [
            {
                "health_record_id": 10,
                "poultry_group_id": 1,
                "record_date": date(2026, 9, 17),
                "condition_type": "Disease",
                "number_affected": 3,
                "description": "Illness observed.",
                "action_taken": "Treatment started.",
                "outcome": "Under observation.",
                "recorded_by_id": 1,
                "created_at": None,
            }
        ]

        mock_queryset = mock_all.return_value
        mock_authorized_queryset = mock_queryset

        with patch(
            "core.views.authorized_queryset",
            return_value=mock_authorized_queryset,
        ):
            mock_authorized_queryset.values.return_value = records

            request = self.make_request(
                "GET",
                "/poultry-health-records/",
            )

            response = poultry_health_records_list(request)

        self.assertEqual(response.status_code, 200)

        payload = json.loads(response.content)
        self.assertEqual(len(payload["poultry_health_records"]), 1)
        self.assertEqual(
            payload["poultry_health_records"][0]["health_record_id"],
            10,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_rejects_get_method(self, mock_authorization):
        mock_authorization.has_permission.return_value = True

        request = self.make_request(
            "GET",
            "/poultry-health-records/create/",
        )

        response = poultry_health_record_create(request)

        self.assertEqual(response.status_code, 405)

    @patch("core.authorization.decorators.authorization_service")
    def test_list_rejects_post_method(self, mock_authorization):
        mock_authorization.has_permission.return_value = True

        request = self.make_request(
            "POST",
            "/poultry-health-records/",
        )

        response = poultry_health_records_list(request)

        self.assertEqual(response.status_code, 405)
