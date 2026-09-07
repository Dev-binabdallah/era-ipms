from types import SimpleNamespace
from unittest.mock import patch

from django.http import JsonResponse
from django.test import RequestFactory, SimpleTestCase

from core.authorization.constants import (
    PERMISSION_ADMINISTER,
    PERMISSION_EDIT,
    PERMISSION_VIEW,
)
from core.authorization.decorators import require_permission


class AuthorizationBoundaryTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_request(self, user):
        request = self.factory.get("/test/")
        request.user = user
        return request

    def test_unauthenticated_request_returns_401(self):
        @require_permission(
            permission=PERMISSION_VIEW,
            resource="projects",
        )
        def view(request):
            return JsonResponse({"success": True})

        response = view(
            self.make_request(self.unauthenticated_user),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_unauthorized_request_returns_403(self, service):
        service.can_view.return_value = False

        @require_permission(
            permission=PERMISSION_VIEW,
            resource="projects",
        )
        def view(request):
            return JsonResponse({"success": True})

        response = view(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            None,
            resource="projects",
            context=None,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_request_executes_view(self, service):
        service.can_view.return_value = True

        @require_permission(
            permission=PERMISSION_VIEW,
            resource="projects",
        )
        def view(request):
            return JsonResponse({"success": True})

        response = view(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"success": True},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_record_getter_is_passed_to_authorization_service(
        self,
        service,
    ):
        service.can_edit.return_value = True

        record = SimpleNamespace(project_id=10)

        def get_record(request, project_id):
            self.assertEqual(project_id, 10)
            return record

        @require_permission(
            permission=PERMISSION_EDIT,
            resource="projects",
            record_getter=get_record,
        )
        def view(request, project_id):
            return JsonResponse({"success": True})

        response = view(
            self.make_request(self.authenticated_user),
            10,
        )

        self.assertEqual(response.status_code, 200)

        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            record,
            resource="projects",
            context=None,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_context_getter_is_passed_to_authorization_service(
        self,
        service,
    ):
        service.can_view.return_value = True

        record = SimpleNamespace(project_id=10)
        context = {"project": record}

        @require_permission(
            permission=PERMISSION_VIEW,
            resource="projects",
            record_getter=lambda request: record,
            context_getter=lambda request: context,
        )
        def view(request):
            return JsonResponse({"success": True})

        response = view(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            record,
            resource="projects",
            context=context,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_add_permission_uses_resource_without_record(
        self,
        service,
    ):
        service.can_add.return_value = True

        @require_permission(
            permission="ADD",
            resource="projects",
        )
        def view(request):
            return JsonResponse({"success": True})

        response = view(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)

        service.can_add.assert_called_once_with(
            self.authenticated_user,
            "projects",
            context=None,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_administer_permission_uses_dedicated_check(
        self,
        service,
    ):
        service.can_administer.return_value = True

        @require_permission(
            permission=PERMISSION_ADMINISTER,
        )
        def view(request):
            return JsonResponse({"success": True})

        response = view(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)

        service.can_administer.assert_called_once_with(
            self.authenticated_user,
        )

    def test_non_admin_permission_requires_resource(self):
        with self.assertRaises(ValueError):
            require_permission(
                permission=PERMISSION_VIEW,
            )

    def test_unknown_permission_is_rejected(self):
        with self.assertRaises(ValueError):
            require_permission(
                permission="NOT_A_PERMISSION",
                resource="projects",
            )

    def test_non_callable_record_getter_is_rejected(self):
        with self.assertRaises(TypeError):
            require_permission(
                permission=PERMISSION_VIEW,
                resource="projects",
                record_getter="not-callable",
            )

    def test_non_callable_context_getter_is_rejected(self):
        with self.assertRaises(TypeError):
            require_permission(
                permission=PERMISSION_VIEW,
                resource="projects",
                context_getter="not-callable",
            )
