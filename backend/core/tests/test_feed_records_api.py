import json
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase, override_settings

from core.views import feed_record_create, feed_records_list


@override_settings(ROOT_URLCONF="config.urls")
class FeedRecordApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.user = SimpleNamespace(
            is_authenticated=True,
            is_active=True,
            user_id=1,
        )

        self.project = SimpleNamespace(
            project_id=10,
        )

        self.poultry_group = SimpleNamespace(
            poultry_group_id=100,
            project=self.project,
        )

        self.feed_record = SimpleNamespace(
            feed_record_id=1,
            poultry_group_id=100,
            record_date="2026-09-17",
            feed_source="Local supplier",
            feed_description="Chicken feed",
            quantity=Decimal("25.50"),
            unit="kg",
            cost=Decimal("1500.00"),
            recorded_by_id=1,
            created_at="2026-09-17T10:00:00Z",
        )

    def test_list_requires_authentication(self):
        response = self.client.get("/feed-records/")

        self.assertEqual(response.status_code, 401)

    def test_create_requires_authentication(self):
        response = self.client.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 100,
                    "record_date": "2026-09-17",
                    "quantity": "25.50",
                }
            ),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)

    @patch("core.views.authorization_service")
    @patch("core.views.authorized_queryset")
    def test_list_requires_permission(
        self,
        authorized_queryset,
        service,
    ):
        service.has_permission.return_value = False

        request = self.factory.get("/feed-records/")
        request.user = self.user

        response = feed_records_list(request)

        self.assertEqual(response.status_code, 403)
        authorized_queryset.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    def test_create_requires_permission(self, service):
        service.can_add.return_value = False

        request = self.factory.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 100,
                    "record_date": "2026-09-17",
                    "quantity": "25.50",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.FeedRecords.objects.create")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_create(
        self,
        decorator_service,
        service,
        select_related,
        create,
    ):
        decorator_service.can_add.return_value = True
        service.can_add.return_value = True
        service.has_project_scope.return_value = True
        select_related.return_value.get.return_value = self.poultry_group
        create.return_value = self.feed_record

        request = self.factory.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 100,
                    "record_date": "2026-09-17",
                    "feed_source": "Local supplier",
                    "feed_description": "Chicken feed",
                    "quantity": "25.50",
                    "unit": "kg",
                    "cost": "1500.00",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 201)

        create.assert_called_once()
        call_kwargs = create.call_args.kwargs

        self.assertEqual(call_kwargs["poultry_group"], self.poultry_group)
        self.assertEqual(call_kwargs["record_date"], "2026-09-17")
        self.assertEqual(call_kwargs["feed_source"], "Local supplier")
        self.assertEqual(call_kwargs["feed_description"], "Chicken feed")
        self.assertEqual(call_kwargs["quantity"], Decimal("25.50"))
        self.assertEqual(call_kwargs["unit"], "kg")
        self.assertEqual(call_kwargs["cost"], Decimal("1500.00"))
        self.assertEqual(call_kwargs["recorded_by"], self.user)

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_outside_project_scope(
        self,
        decorator_service,
        service,
        select_related,
    ):
        decorator_service.can_add.return_value = True
        service.can_add.return_value = True
        service.has_project_scope.return_value = False
        select_related.return_value.get.return_value = self.poultry_group

        request = self.factory.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 100,
                    "record_date": "2026-09-17",
                    "quantity": "25.50",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 403)

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_poultry_group(
        self,
        decorator_service,
        service,
        select_related,
    ):
        decorator_service.can_add.return_value = True
        service.can_add.return_value = True
        service.has_project_scope.return_value = True
        select_related.return_value.get.side_effect = (
            __import__("core.models", fromlist=["PoultryGroups"])
            .PoultryGroups.DoesNotExist
        )

        request = self.factory.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 999,
                    "record_date": "2026-09-17",
                    "quantity": "25.50",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 404)

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_required_data(
        self,
        decorator_service,
        service,
        select_related,
    ):
        decorator_service.can_add.return_value = True
        service.can_add.return_value = True
        service.has_project_scope.return_value = True

        request = self.factory.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 100,
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 400)
        select_related.assert_not_called()

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_json(
        self,
        decorator_service,
        service,
        select_related,
    ):
        decorator_service.can_add.return_value = True
        service.can_add.return_value = True

        request = self.factory.post(
            "/feed-records/create/",
            data="{invalid json",
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 400)
        select_related.assert_not_called()

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_quantity(
        self,
        decorator_service,
        service,
        select_related,
    ):
        decorator_service.can_add.return_value = True
        service.can_add.return_value = True
        service.has_project_scope.return_value = True
        select_related.return_value.get.return_value = self.poultry_group

        request = self.factory.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 100,
                    "record_date": "2026-09-17",
                    "quantity": "not-a-number",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 400)

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_cost(
        self,
        decorator_service,
        service,
        select_related,
    ):
        decorator_service.can_add.return_value = True
        service.can_add.return_value = True
        service.has_project_scope.return_value = True
        select_related.return_value.get.return_value = self.poultry_group

        request = self.factory.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 100,
                    "record_date": "2026-09-17",
                    "quantity": "25.50",
                    "cost": "not-a-number",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 400)

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_negative_values(
        self,
        decorator_service,
        service,
        select_related,
    ):
        decorator_service.can_add.return_value = True
        service.can_add.return_value = True
        service.has_project_scope.return_value = True
        select_related.return_value.get.return_value = self.poultry_group

        request = self.factory.post(
            "/feed-records/create/",
            data=json.dumps(
                {
                    "poultry_group_id": 100,
                    "record_date": "2026-09-17",
                    "quantity": "-5.00",
                    "cost": "100.00",
                }
            ),
            content_type="application/json",
        )
        request.user = self.user

        response = feed_record_create(request)

        self.assertEqual(response.status_code, 400)

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_list(
        self,
        service,
        authorized_queryset,
    ):
        service.can_view.return_value = True

        values = [
            {
                "feed_record_id": 1,
                "poultry_group_id": 100,
                "record_date": "2026-09-17",
                "feed_source": "Local supplier",
                "feed_description": "Chicken feed",
                "quantity": Decimal("25.50"),
                "unit": "kg",
                "cost": Decimal("1500.00"),
                "recorded_by_id": 1,
                "created_at": "2026-09-17T10:00:00Z",
            }
        ]

        queryset = authorized_queryset.return_value
        queryset.values.return_value = values

        request = self.factory.get("/feed-records/")
        request.user = self.user

        response = feed_records_list(request)

        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.content)

        self.assertEqual(
            response_data["feed_records"],
            [
                {
                    **values[0],
                    "quantity": "25.50",
                    "cost": "1500.00",
                }
            ],
        )

        authorized_queryset.assert_called_once()

        args = authorized_queryset.call_args.args
        self.assertEqual(args[0], self.user)
        self.assertEqual(args[1], "feed_records")
