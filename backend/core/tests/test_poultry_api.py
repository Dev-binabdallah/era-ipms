from types import SimpleNamespace
from unittest.mock import patch

from django.db import IntegrityError
from django.test import RequestFactory, SimpleTestCase

from core.views import poultry_group_create, poultry_groups_list


class PoultryApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_get_request(self, user, path="/poultry-groups/"):
        request = self.factory.get(path)
        request.user = user
        return request

    def make_post_request(
        self,
        user,
        path="/poultry-groups/create/",
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
        response = poultry_groups_list(
            self.make_get_request(self.unauthenticated_user),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    def test_create_unauthenticated_request_returns_401(self):
        response = poultry_group_create(
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

        response = poultry_groups_list(
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

        response = poultry_group_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"project_id":1,"group_name":"Test Group"}',
            ),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )


    @patch("core.views.PoultryGroups.objects.create")
    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    @patch("django.utils.timezone.now")
    def test_create_authorized_group(
        self,
        timezone_now,
        decorator_service,
        service,
        project_get,
        group_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True

        project = SimpleNamespace(project_id=1)
        group = SimpleNamespace(
            poultry_group_id=10,
            project_id=1,
            group_name="Layer Chickens",
            poultry_category="Layers",
            breed_or_type="Kienyeji",
            start_date=None,
            status="active",
            description="Test poultry group",
        )

        project_get.return_value = project
        group_create.return_value = group
        timezone_now.return_value = "2026-09-14T10:00:00Z"

        response = poultry_group_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"project_id":1,"group_name":"Layer Chickens","poultry_category":"Layers","breed_or_type":"Kienyeji","description":"Test poultry group"}',
            ),
        )

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "poultry_group": {
                    "poultry_group_id": 10,
                    "project_id": 1,
                    "group_name": "Layer Chickens",
                    "poultry_category": "Layers",
                    "breed_or_type": "Kienyeji",
                    "start_date": None,
                    "status": "active",
                    "description": "Test poultry group",
                }
            },
        )

        service.has_project_scope.assert_called_once_with(
            self.authenticated_user,
            project,
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_outside_project_scope_returns_403(
        self,
        decorator_service,
        service,
        project_get,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = False

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        response = poultry_group_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"project_id":1,"group_name":"Unauthorized Group"}',
            ),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {
                "error": "You are not authorized to use this project",
            },
        )

    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_authorized_groups(
        self,
        service,
        queryset,
    ):
        service.can_view.return_value = True

        values = queryset.return_value.values
        values.return_value = [
            {
                "poultry_group_id": 10,
                "project_id": 1,
                "group_name": "Layer Chickens",
                "poultry_category": "Layers",
                "breed_or_type": "Kienyeji",
                "start_date": None,
                "status": "active",
                "description": "Test poultry group",
            }
        ]

        response = poultry_groups_list(
            self.make_get_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "poultry_groups": [
                    {
                        "poultry_group_id": 10,
                        "project_id": 1,
                        "group_name": "Layer Chickens",
                        "poultry_category": "Layers",
                        "breed_or_type": "Kienyeji",
                        "start_date": None,
                        "status": "active",
                        "description": "Test poultry group",
                    }
                ]
            },
        )

    @patch("core.views.PoultryGroups.objects.create")
    @patch("core.views.Projects.objects.get")
    @patch("core.views.authorization_service")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_duplicate_group_returns_409(
        self,
        decorator_service,
        service,
        project_get,
        group_create,
    ):
        decorator_service.can_add.return_value = True
        service.has_project_scope.return_value = True

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        group_create.side_effect = IntegrityError()

        response = poultry_group_create(
            self.make_post_request(
                self.authenticated_user,
                body=b'{"project_id":1,"group_name":"Layer Chickens"}',
            ),
        )

        self.assertEqual(response.status_code, 409)
        self.assertJSONEqual(
            response.content,
            {
                "error": (
                    "A poultry group with this name already exists "
                    "in this project"
                ),
            },
        )
