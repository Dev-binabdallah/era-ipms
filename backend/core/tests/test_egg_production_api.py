from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.views import (
    egg_production_create,
    egg_production_list,
)


class EggProductionApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_get_request(
        self,
        user,
        path="/egg-production/",
    ):
        request = self.factory.get(path)
        request.user = user
        return request

    def make_post_request(
        self,
        user,
        path="/egg-production/create/",
        body=b"{}",
    ):
        request = self.factory.post(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def test_list_unauthenticated_request_returns_401(self):
        response = egg_production_list(
            self.make_get_request(self.unauthenticated_user),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    def test_create_unauthenticated_request_returns_401(self):
        response = egg_production_create(
            self.make_post_request(self.unauthenticated_user),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_list_unauthorized_request_returns_403(self, service):
        service.can_view.return_value = False

        response = egg_production_list(
            self.make_get_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_unauthorized_request_returns_403(self, service):
        service.can_add.return_value = False

        response = egg_production_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"production_date":"2026-09-17",'
                    b'"eggs_produced":100,'
                    b'"eggs_used":20,'
                    b'"eggs_sold":30}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.views.EggProduction.objects.create")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    @patch("django.utils.timezone.now")
    def test_create_authorized_egg_production(
        self,
        timezone_now,
        decorator_service,
        service,
        group_get,
        production_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True

        project = SimpleNamespace(project_id=1)

        poultry_group = SimpleNamespace(
            poultry_group_id=10,
            project=project,
        )

        production = SimpleNamespace(
            egg_production_id=30,
            poultry_group_id=10,
            production_date="2026-09-17",
            eggs_produced=100,
            eggs_used=20,
            eggs_sold=30,
            eggs_remaining=50,
            recorded_by_id=5,
            created_at="2026-09-17T10:00:00Z",
        )

        group_get.return_value.get.return_value = poultry_group
        production_create.return_value = production
        timezone_now.return_value = "2026-09-17T10:00:00Z"

        response = egg_production_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"production_date":"2026-09-17",'
                    b'"eggs_produced":100,'
                    b'"eggs_used":20,'
                    b'"eggs_sold":30}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "egg_production": {
                    "egg_production_id": 30,
                    "poultry_group_id": 10,
                    "production_date": "2026-09-17",
                    "eggs_produced": 100,
                    "eggs_used": 20,
                    "eggs_sold": 30,
                    "eggs_remaining": 50,
                    "recorded_by": 5,
                    "created_at": "2026-09-17T10:00:00Z",
                }
            },
        )

        service.has_project_scope.assert_called_once_with(
            self.authenticated_user,
            project,
        )

        production_create.assert_called_once_with(
            poultry_group=poultry_group,
            production_date="2026-09-17",
            eggs_produced=100,
            eggs_used=20,
            eggs_sold=30,
            eggs_remaining=50,
            recorded_by=self.authenticated_user,
            created_at="2026-09-17T10:00:00Z",
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_group_returns_404(
        self,
        decorator_service,
        group_get,
    ):
        decorator_service.can_add.return_value = True

        from core.models import PoultryGroups

        group_get.side_effect = PoultryGroups.DoesNotExist

        response = egg_production_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":999,'
                    b'"production_date":"2026-09-17",'
                    b'"eggs_produced":100,'
                    b'"eggs_used":20,'
                    b'"eggs_sold":30}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Poultry group not found"},
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_outside_project_scope_returns_403(
        self,
        decorator_service,
        service,
        group_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = False

        project = SimpleNamespace(project_id=1)

        poultry_group = SimpleNamespace(
            poultry_group_id=10,
            project=project,
        )

        group_get.return_value.get.return_value = poultry_group

        response = egg_production_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"production_date":"2026-09-17",'
                    b'"eggs_produced":100,'
                    b'"eggs_used":20,'
                    b'"eggs_sold":30}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "You are not authorized to use this poultry group"
                ),
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_required_data_returns_400(self, decorator_service):
        decorator_service.can_add.return_value = True

        response = egg_production_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"poultry_group_id":10}',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "poultry_group_id, production_date, eggs_produced, "
                    "eggs_used, and eggs_sold are required"
                ),
            },
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_negative_egg_values_returns_400(
        self,
        decorator_service,
        service,
        group_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        group_get.return_value.get.return_value = SimpleNamespace(
            poultry_group_id=10,
            project=SimpleNamespace(project_id=1),
        )

        response = egg_production_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"production_date":"2026-09-17",'
                    b'"eggs_produced":-10,'
                    b'"eggs_used":0,'
                    b'"eggs_sold":0}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "eggs_produced, eggs_used, and eggs_sold "
                    "cannot be negative"
                ),
            },
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_used_and_sold_greater_than_produced_returns_400(
        self,
        decorator_service,
        service,
        group_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        group_get.return_value.get.return_value = SimpleNamespace(
            poultry_group_id=10,
            project=SimpleNamespace(project_id=1),
        )

        response = egg_production_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"production_date":"2026-09-17",'
                    b'"eggs_produced":50,'
                    b'"eggs_used":30,'
                    b'"eggs_sold":30}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "eggs_used and eggs_sold cannot be greater "
                    "than eggs_produced"
                ),
            },
        )

    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_non_integer_egg_values_returns_400(
        self,
        decorator_service,
        service,
        group_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True
        group_get.return_value.get.return_value = SimpleNamespace(
            poultry_group_id=10,
            project=SimpleNamespace(project_id=1),
        )

        response = egg_production_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"production_date":"2026-09-17",'
                    b'"eggs_produced":"many",'
                    b'"eggs_used":20,'
                    b'"eggs_sold":30}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "eggs_produced, eggs_used, and eggs_sold "
                    "must be integers"
                ),
            },
        )

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_authorized_egg_production(
        self,
        service,
        queryset,
    ):
        service.can_view.return_value = True

        values = queryset.return_value.values
        values.return_value = [
            {
                "egg_production_id": 30,
                "poultry_group_id": 10,
                "production_date": "2026-09-17",
                "eggs_produced": 100,
                "eggs_used": 20,
                "eggs_sold": 30,
                "eggs_remaining": 50,
                "recorded_by_id": 5,
                "created_at": "2026-09-17T10:00:00Z",
            }
        ]

        response = egg_production_list(
            self.make_get_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "egg_production": [
                    {
                        "egg_production_id": 30,
                        "poultry_group_id": 10,
                        "production_date": "2026-09-17",
                        "eggs_produced": 100,
                        "eggs_used": 20,
                        "eggs_sold": 30,
                        "eggs_remaining": 50,
                        "recorded_by_id": 5,
                        "created_at": "2026-09-17T10:00:00Z",
                    }
                ]
            },
        )
