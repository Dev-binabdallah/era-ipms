from types import SimpleNamespace
from unittest.mock import patch

from django.test import RequestFactory, SimpleTestCase

from core.views import (
    poultry_stock_movement_create,
    poultry_stock_movements_list,
)


class PoultryStockMovementApiTests(SimpleTestCase):
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
        path="/poultry-stock-movements/",
    ):
        request = self.factory.get(path)
        request.user = user
        return request

    def make_post_request(
        self,
        user,
        path="/poultry-stock-movements/create/",
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
        response = poultry_stock_movements_list(
            self.make_get_request(self.unauthenticated_user),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    def test_create_unauthenticated_request_returns_401(self):
        response = poultry_stock_movement_create(
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

        response = poultry_stock_movements_list(
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

        response = poultry_stock_movement_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"movement_date":"2026-09-14",'
                    b'"movement_type":"Added",'
                    b'"quantity":20}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.views.PoultryStockMovements.objects.create")
    @patch("core.views.PoultryGroups.objects.select_related")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    @patch("django.utils.timezone.now")
    def test_create_authorized_stock_movement(
        self,
        timezone_now,
        decorator_service,
        service,
        group_get,
        movement_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True

        project = SimpleNamespace(project_id=1)
        poultry_group = SimpleNamespace(
            poultry_group_id=10,
            project=project,
        )

        movement = SimpleNamespace(
            movement_id=20,
            poultry_group_id=10,
            movement_date="2026-09-14",
            movement_type="Added",
            quantity=20,
            description="New chicks added",
            recorded_by_id=5,
            created_at="2026-09-14T10:00:00Z",
        )

        group_get.return_value.get.return_value = poultry_group
        movement_create.return_value = movement
        timezone_now.return_value = "2026-09-14T10:00:00Z"

        response = poultry_stock_movement_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"movement_date":"2026-09-14",'
                    b'"movement_type":"Added",'
                    b'"quantity":20,'
                    b'"description":"New chicks added"}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "poultry_stock_movement": {
                    "movement_id": 20,
                    "poultry_group_id": 10,
                    "movement_date": "2026-09-14",
                    "movement_type": "Added",
                    "quantity": 20,
                    "description": "New chicks added",
                    "recorded_by": 5,
                    "created_at": "2026-09-14T10:00:00Z",
                }
            },
        )

        service.has_project_scope.assert_called_once_with(
            self.authenticated_user,
            project,
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

        response = poultry_stock_movement_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":10,'
                    b'"movement_date":"2026-09-14",'
                    b'"movement_type":"Added",'
                    b'"quantity":20}'
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

        response = poultry_stock_movement_create(
            self.make_post_request(
                self.authenticated_user,
                body=(
                    b'{"poultry_group_id":999,'
                    b'"movement_date":"2026-09-14",'
                    b'"movement_type":"Added",'
                    b'"quantity":20}'
                ),
            ),
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {"error": "Poultry group not found"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_required_data_returns_400(self, decorator_service):
        decorator_service.can_add.return_value = True

        response = poultry_stock_movement_create(
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
                    "poultry_group_id, movement_date, movement_type, "
                    "and quantity are required"
                ),
            },
        )

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_authorized_stock_movements(
        self,
        service,
        queryset,
    ):
        service.can_view.return_value = True

        values = queryset.return_value.values
        values.return_value = [
            {
                "movement_id": 20,
                "poultry_group_id": 10,
                "movement_date": "2026-09-14",
                "movement_type": "Added",
                "quantity": 20,
                "description": "New chicks added",
                "recorded_by_id": 5,
                "created_at": "2026-09-14T10:00:00Z",
            }
        ]

        response = poultry_stock_movements_list(
            self.make_get_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "poultry_stock_movements": [
                    {
                        "movement_id": 20,
                        "poultry_group_id": 10,
                        "movement_date": "2026-09-14",
                        "movement_type": "Added",
                        "quantity": 20,
                        "description": "New chicks added",
                        "recorded_by_id": 5,
                        "created_at": "2026-09-14T10:00:00Z",
                    }
                ]
            },
        )
