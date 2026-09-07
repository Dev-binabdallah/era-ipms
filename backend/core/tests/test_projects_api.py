from datetime import date
from types import SimpleNamespace
from unittest.mock import Mock, call, patch

from django.test import RequestFactory, SimpleTestCase

from core.models import Projects, UserProjectAssignments
from core.views import (
    projects_create,
    projects_detail,
    projects_list,
    projects_update,
    project_assignments,
    project_assignment_create,
    project_assignment_update,
)


class ProjectsApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
        )

    def make_request(self, user, path="/projects/"):
        request = self.factory.get(path)
        request.user = user
        return request

    def make_patch_request(self, user, path="/projects/1/", body=b"{}"):
        request = self.factory.patch(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def test_update_unauthenticated_request_returns_401(self):
        response = projects_update(
            self.make_patch_request(self.unauthenticated_user),
            1,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_unauthorized_request_returns_403(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = False

        project = SimpleNamespace(
            project_id=1,
        )
        project_get.return_value = project

        request = self.make_patch_request(
            self.authenticated_user,
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        project_get.assert_called_once_with(
            project_id=1,
        )

        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            project,
            resource="projects",
            context=None,
        )

    @patch("django.utils.timezone.now")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_authorized_request_updates_project(
        self,
        service,
        project_get,
        timezone_now,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(
            project_id=1,
            project_name="Original Project",
            description="Original description",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            objectives="Original objectives",
            status="active",
            created_by_id=10,
            created_at="original-created-at",
            updated_at="original-updated-at",
        )

        project_get.return_value = project
        timezone_now.return_value = "new-updated-at"

        project.save = lambda **kwargs: None

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"project_name":"Updated Project","status":"completed"}',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "project": {
                    "project_id": 1,
                    "project_name": "Updated Project",
                    "description": "Original description",
                    "start_date": "2026-01-01",
                    "end_date": "2026-12-31",
                    "objectives": "Original objectives",
                    "status": "completed",
                    "created_by_id": 10,
                    "created_at": "original-created-at",
                    "updated_at": "new-updated-at",
                }
            },
        )

        self.assertEqual(project.project_name, "Updated Project")
        self.assertEqual(project.status, "completed")
        self.assertEqual(project.created_by_id, 10)
        self.assertEqual(project.created_at, "original-created-at")
        self.assertEqual(project.updated_at, "new-updated-at")

        service.can_edit.assert_called_once_with(
            self.authenticated_user,
            project,
            resource="projects",
            context=None,
        )

        project_get.assert_has_calls(
            [
                call(project_id=1),
                call(project_id=1),
            ]
        )
        self.assertEqual(project_get.call_count, 2)

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_protected_fields_returns_400(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"project_id":999,"created_by_id":999}',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Protected fields cannot be modified",
                "fields": ["created_by_id", "project_id"],
            },
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_unknown_fields_returns_400(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"project_name":"Updated","unknown_field":"value"}',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Unknown fields",
                "fields": ["unknown_field"],
            },
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_empty_payload_returns_400(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        request = self.make_patch_request(
            self.authenticated_user,
            body=b"{}",
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "At least one editable field is required",
            },
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_blank_project_name_returns_400(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"project_name":"   "}',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "project_name cannot be empty",
            },
        )

    @patch("django.utils.timezone.now")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_valid_dates(
        self,
        service,
        project_get,
        timezone_now,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(
            project_id=1,
            project_name="Test Project",
            description="Description",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 6, 30),
            objectives="Objectives",
            status="active",
            created_by_id=10,
            created_at="created-at",
            updated_at="old-updated-at",
        )

        project_get.return_value = project
        timezone_now.return_value = "new-updated-at"
        project.save = lambda **kwargs: None

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"start_date":"2026-02-01","end_date":"2026-11-30"}',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.start_date, date(2026, 2, 1))
        self.assertEqual(project.end_date, date(2026, 11, 30))
        self.assertEqual(project.updated_at, "new-updated-at")

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_invalid_date_returns_400(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"start_date":"01-02-2026"}',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "start_date must use YYYY-MM-DD format",
            },
        )

    @patch("django.utils.timezone.now")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_null_date_clears_date(
        self,
        service,
        project_get,
        timezone_now,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(
            project_id=1,
            project_name="Test Project",
            description="Description",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            objectives="Objectives",
            status="active",
            created_by_id=10,
            created_at="created-at",
            updated_at="old-updated-at",
        )

        project_get.return_value = project
        timezone_now.return_value = "new-updated-at"
        project.save = lambda **kwargs: None

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"start_date":null}',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(project.start_date)
        self.assertEqual(project.end_date, date(2026, 12, 31))

    @patch("django.utils.timezone.now")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_empty_date_clears_date(
        self,
        service,
        project_get,
        timezone_now,
    ):
        service.can_edit.return_value = True

        project = SimpleNamespace(
            project_id=1,
            project_name="Test Project",
            description="Description",
            start_date=date(2026, 1, 1),
            end_date=date(2026, 12, 31),
            objectives="Objectives",
            status="active",
            created_by_id=10,
            created_at="created-at",
            updated_at="old-updated-at",
        )

        project_get.return_value = project
        timezone_now.return_value = "new-updated-at"
        project.save = lambda **kwargs: None

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"end_date":""}',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(project.start_date, date(2026, 1, 1))
        self.assertIsNone(project.end_date)

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_malformed_json_returns_400(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True
        project_get.return_value = SimpleNamespace(project_id=1)

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"project_name":',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_non_object_json_returns_400(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True
        project_get.return_value = SimpleNamespace(project_id=1)

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'["project_name","Updated"]',
        )

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "JSON body must be an object"},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_non_patch_request_returns_405(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True
        project_get.return_value = SimpleNamespace(project_id=1)

        request = self.factory.get("/projects/1/")
        request.user = self.authenticated_user

        response = projects_update(
            request,
            1,
        )

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_nonexistent_project_returns_404(
        self,
        service,
        project_get,
    ):
        service.can_edit.return_value = True
        project_get.side_effect = Projects.DoesNotExist

        request = self.make_patch_request(
            self.authenticated_user,
            "/projects/999/",
        )

        response = projects_update(
            request,
            999,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Project not found",
            },
        )

        project_get.assert_has_calls(
            [
                call(project_id=999),
                call(project_id=999),
            ]
        )
        self.assertEqual(project_get.call_count, 2)

    def test_unauthenticated_request_returns_401(self):
        response = projects_list(
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

        response = projects_list(
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

    @patch("core.views.Projects.objects.all")
    @patch("core.views.authorized_queryset")
    @patch("core.authorization.decorators.authorization_service")
    def test_authorized_request_uses_authorized_queryset(
        self,
        service,
        authorized_queryset,
        objects_all,
    ):
        service.can_view.return_value = True

        values_queryset = [
            {
                "project_id": 1,
                "project_name": "Test Project",
            },
        ]

        queryset = SimpleNamespace(
            values=lambda *args: values_queryset,
        )

        authorized_queryset.return_value = queryset
        objects_all.return_value = SimpleNamespace()

        response = projects_list(
            self.make_request(self.authenticated_user),
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "projects": values_queryset,
            },
        )

        objects_all.assert_called_once_with()
        authorized_queryset.assert_called_once_with(
            self.authenticated_user,
            "projects",
            objects_all.return_value,
        )

    def test_detail_unauthenticated_request_returns_401(self):
        response = projects_detail(
            self.make_request(
                self.unauthenticated_user,
                "/projects/1/",
            ),
            1,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_detail_unauthorized_request_returns_403(
        self,
        service,
        project_get,
    ):
        service.can_view.return_value = False

        project = SimpleNamespace(
            project_id=1,
        )
        project_get.return_value = project

        request = self.make_request(
            self.authenticated_user,
            "/projects/1/",
        )

        response = projects_detail(
            request,
            1,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        project_get.assert_called_once_with(
            project_id=1,
        )

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            project,
            resource="projects",
            context=None,
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_detail_authorized_request_returns_project(
        self,
        service,
        project_get,
    ):
        service.can_view.return_value = True

        project = SimpleNamespace(
            project_id=1,
            project_name="Test Project",
            description="Test description",
            start_date=None,
            end_date=None,
            objectives="Test objectives",
            status="active",
            created_by_id=10,
            created_at=None,
            updated_at=None,
        )

        project_get.return_value = project

        request = self.make_request(
            self.authenticated_user,
            "/projects/1/",
        )

        response = projects_detail(
            request,
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "project": {
                    "project_id": 1,
                    "project_name": "Test Project",
                    "description": "Test description",
                    "start_date": None,
                    "end_date": None,
                    "objectives": "Test objectives",
                    "status": "active",
                    "created_by_id": 10,
                    "created_at": None,
                    "updated_at": None,
                }
            },
        )

        project_get.assert_has_calls(
            [
                call(project_id=1),
                call(project_id=1),
            ]
        )
        self.assertEqual(project_get.call_count, 2)

        service.can_view.assert_called_once_with(
            self.authenticated_user,
            project,
            resource="projects",
            context=None,
        )

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_detail_nonexistent_project_returns_404(
        self,
        service,
        project_get,
    ):
        project_get.side_effect = Projects.DoesNotExist

        request = self.make_request(
            self.authenticated_user,
            "/projects/999/",
        )

        response = projects_detail(
            request,
            999,
        )

        self.assertEqual(response.status_code, 404)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Project not found",
            },
        )

        project_get.assert_has_calls(
            [
                call(project_id=999),
                call(project_id=999),
            ]
        )
        self.assertEqual(project_get.call_count, 2)

        service.can_view.assert_called_once_with(
           self.authenticated_user,
           None,
           resource="projects",
           context=None,
        )

    def make_post_request(
        self,
        user,
        body,
        path="/projects/",
    ):
        request = self.factory.post(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    @patch("core.authorization.decorators.authorization_service")
    def test_create_unauthenticated_request_returns_401(self, service):
        response = projects_create(
            self.make_post_request(
                self.unauthenticated_user,
                '{"project_name": "Test Project"}',
            ),
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )
        service.can_add.assert_not_called()

    @patch("core.authorization.decorators.authorization_service")
    def test_create_unauthorized_request_returns_403(self, service):
        service.can_add.return_value = False

        user = SimpleNamespace(
            is_authenticated=True,
            user_id=10,
        )

        response = projects_create(
            self.make_post_request(
                user,
                '{"project_name": "Test Project"}',
            ),
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_add.assert_called_once_with(
            user,
            "projects",
            context=None,
        )

    @patch("core.views.timezone.now")
    @patch("core.views.Projects.objects.create")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_authorized_request_creates_project(
        self,
        service,
        objects_create,
        timezone_now,
    ):
        service.can_add.return_value = True

        user = SimpleNamespace(
            is_authenticated=True,
            user_id=10,
        )

        timestamp = "2026-09-07T10:00:00Z"
        timezone_now.return_value = timestamp

        project = SimpleNamespace(
            project_id=25,
            project_name="New Project",
            description="Project description",
            start_date="2026-09-10",
            end_date="2026-12-31",
            objectives="Project objectives",
            status="active",
            created_by_id=10,
            created_at=timestamp,
            updated_at=timestamp,
        )

        objects_create.return_value = project

        response = projects_create(
            self.make_post_request(
                user,
                '{"project_name": "New Project", '
                '"description": "Project description", '
                '"start_date": "2026-09-10", '
                '"end_date": "2026-12-31", '
                '"objectives": "Project objectives", '
                '"status": "active", '
                '"created_by_id": 999, '
                '"project_id": 999}',
            ),
        )

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "project": {
                    "project_id": 25,
                    "project_name": "New Project",
                    "description": "Project description",
                    "start_date": "2026-09-10",
                    "end_date": "2026-12-31",
                    "objectives": "Project objectives",
                    "status": "active",
                    "created_by_id": 10,
                    "created_at": timestamp,
                    "updated_at": timestamp,
                }
            },
        )

        objects_create.assert_called_once_with(
            project_name="New Project",
            description="Project description",
            start_date=date(2026, 9, 10),
            end_date=date(2026, 12, 31),
            objectives="Project objectives",
            status="active",
            created_by_id=10,
            created_at=timestamp,
            updated_at=timestamp,
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_malformed_json_returns_400(self, service):
        service.can_add.return_value = True

        response = projects_create(
            self.make_post_request(
                self.authenticated_user,
                '{"project_name": ',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Invalid JSON"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_non_object_json_returns_400(self, service):
        service.can_add.return_value = True

        response = projects_create(
            self.make_post_request(
                self.authenticated_user,
                '["Test Project"]',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "JSON body must be an object"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_missing_project_name_returns_400(self, service):
        service.can_add.return_value = True

        response = projects_create(
            self.make_post_request(
                self.authenticated_user,
                '{"description": "Missing name"}',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "project_name is required"},
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_invalid_date_returns_400(self, service):
        service.can_add.return_value = True

        response = projects_create(
            self.make_post_request(
                self.authenticated_user,
                '{"project_name": "Test Project", '
                '"start_date": "10/09/2026"}',
            ),
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "start_date must use YYYY-MM-DD format",
            },
        )

    @patch("core.authorization.decorators.authorization_service")
    def test_create_non_post_request_returns_405(self, service):
        service.can_add.return_value = True

        request = self.factory.get("/projects/")
        request.user = self.authenticated_user

        response = projects_create(request)

        self.assertEqual(response.status_code, 405)
        self.assertJSONEqual(
            response.content,
            {"error": "Method not allowed"},
        )


class ProjectAssignmentsApiTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

        self.authenticated_user = SimpleNamespace(
            is_authenticated=True,
            user_id=10,
        )

        self.unauthenticated_user = SimpleNamespace(
            is_authenticated=False,
            user_id=10,
        )

    def make_get_request(self, user, path="/projects/1/assignments/"):
        request = self.factory.get(path)
        request.user = user
        return request

    def make_post_request(
        self,
        user,
        path="/projects/1/assignments/",
        body=b"{}",
    ):
        request = self.factory.post(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    def make_patch_request(
        self,
        user,
        path="/projects/1/assignments/5/",
        body=b"{}",
    ):
        request = self.factory.patch(
            path,
            data=body,
            content_type="application/json",
        )
        request.user = user
        return request

    @patch("core.authorization.decorators.authorization_service")
    def test_list_unauthenticated_returns_401(self, service):
        response = project_assignments(
            self.make_get_request(self.unauthenticated_user),
            1,
        )

        self.assertEqual(response.status_code, 401)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_manage_project_assignments.assert_not_called()

    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_unauthorized_returns_403(
        self,
        service,
        project_get,
    ):
        service.can_manage_project_assignments.return_value = False

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        response = project_assignments(
            self.make_get_request(self.authenticated_user),
            1,
        )

        self.assertEqual(response.status_code, 403)
        self.assertJSONEqual(
            response.content,
            {"authorized": False},
        )

        service.can_manage_project_assignments.assert_called_once_with(
            self.authenticated_user,
            project,
        )

    @patch("core.views.UserProjectAssignments.objects.filter")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_list_authorized_returns_assignments(
        self,
        service,
        project_get,
        assignments_filter,
    ):
        service.can_manage_project_assignments.return_value = True

        project = SimpleNamespace(project_id=1)
        project_get.return_value = project

        assignment = SimpleNamespace(
            assignment_id=5,
            user_id=20,
            project_id=1,
            assigned_at="2026-09-07T10:00:00Z",
            assigned_by_id=10,
            is_active=True,
        )

        assignments_filter.return_value = [assignment]

        response = project_assignments(
            self.make_get_request(self.authenticated_user),
            1,
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "assignments": [
                    {
                        "assignment_id": 5,
                        "user_id": 20,
                        "project_id": 1,
                        "assigned_at": "2026-09-07T10:00:00Z",
                        "assigned_by_id": 10,
                        "is_active": True,
                    }
                ]
            },
        )

        assignments_filter.assert_called_once_with(
            project=project,
        )

    @patch("core.views.UserProjectAssignments.objects.filter")
    @patch("core.views.Users.objects.get")
    @patch("core.views.UserProjectAssignments.objects.create")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_authorized_creates_assignment(
        self,
        service,
        project_get,
        assignment_create,
        user_get,
        assignments_filter,
    ):
        service.can_manage_project_assignments.return_value = True

        project = SimpleNamespace(project_id=1)
        target_user = SimpleNamespace(
            user_id=20,
            is_active=True,
        )
        assignment = SimpleNamespace(
            assignment_id=5,
            user_id=20,
            project_id=1,
            assigned_at="2026-09-07T10:00:00Z",
            assigned_by_id=10,
            is_active=True,
        )

        project_get.return_value = project
        user_get.return_value = target_user
        assignment_create.return_value = assignment
        assignments_filter.return_value.first.return_value = None

        request = self.make_post_request(
            self.authenticated_user,
            body=b'{"user_id":20}',
        )

        response = project_assignment_create(
            request,
            1,
        )

        self.assertEqual(response.status_code, 201)
        self.assertJSONEqual(
            response.content,
            {
                "assignment": {
                    "assignment_id": 5,
                    "user_id": 20,
                    "project_id": 1,
                    "assigned_at": "2026-09-07T10:00:00Z",
                    "assigned_by_id": 10,
                    "is_active": True,
                }
            },
        )

        assignment_create.assert_called_once()
        create_kwargs = assignment_create.call_args.kwargs
        self.assertEqual(create_kwargs["user"], target_user)
        self.assertEqual(create_kwargs["project"], project)
        self.assertEqual(
            create_kwargs["assigned_by"],
            self.authenticated_user,
        )
        self.assertTrue(create_kwargs["is_active"])

    @patch("core.views.UserProjectAssignments.objects.filter")
    @patch("core.views.Users.objects.get")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_reactivates_existing_assignment(
        self,
        service,
        project_get,
        user_get,
        assignments_filter,
    ):
        service.can_manage_project_assignments.return_value = True

        project = SimpleNamespace(project_id=1)
        target_user = SimpleNamespace(
            user_id=20,
            is_active=True,
        )
        assignment = SimpleNamespace(
            assignment_id=5,
            user=target_user,
            user_id=20,
            project=project,
            project_id=1,
            assigned_at="old-time",
            assigned_by_id=10,
            is_active=False,
            save=Mock(),
        )

        project_get.return_value = project
        user_get.return_value = target_user
        assignments_filter.return_value.first.return_value = assignment

        request = self.make_post_request(
            self.authenticated_user,
            body=b'{"user_id":20}',
        )

        with patch("django.utils.timezone.now") as timezone_now:
            timezone_now.return_value = "2026-09-07T11:00:00Z"

            response = project_assignment_create(
                request,
                1,
            )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "assignment": {
                    "assignment_id": 5,
                    "user_id": 20,
                    "project_id": 1,
                    "assigned_at": "2026-09-07T11:00:00Z",
                    "assigned_by_id": 10,
                    "is_active": True,
                }
            },
        )

        self.assertTrue(assignment.is_active)
        self.assertEqual(
            assignment.assigned_at,
            "2026-09-07T11:00:00Z",
        )
        self.assertEqual(
            assignment.assigned_by_id,
            10,
        )
        assignment.save.assert_called_once()

        assignments_filter.assert_called_once_with(
            user=target_user,
            project=project,
        )

    @patch("core.views.Users.objects.get")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_create_inactive_target_user_returns_400(
        self,
        service,
        project_get,
        user_get,
    ):
        service.can_manage_project_assignments.return_value = True

        project_get.return_value = SimpleNamespace(project_id=1)
        user_get.return_value = SimpleNamespace(
            user_id=20,
            is_active=False,
        )

        request = self.make_post_request(
            self.authenticated_user,
            body=b'{"user_id":20}',
        )

        response = project_assignment_create(
            request,
            1,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {"error": "Target user is inactive"},
        )

    @patch("core.views.UserProjectAssignments.objects.get")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_deactivates_assignment(
        self,
        service,
        project_get,
        assignment_get,
    ):
        service.can_manage_project_assignments.return_value = True

        project = SimpleNamespace(project_id=1)
        assignment = SimpleNamespace(
            assignment_id=5,
            user_id=20,
            project_id=1,
            assigned_at="2026-09-07T10:00:00Z",
            assigned_by_id=10,
            is_active=True,
            project=project,
            save=Mock(),
        )

        project_get.return_value = project
        assignment_get.return_value = assignment

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"is_active":false}',
        )

        response = project_assignment_update(
            request,
            1,
            5,
        )

        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {
                "assignment": {
                    "assignment_id": 5,
                    "user_id": 20,
                    "project_id": 1,
                    "assigned_at": "2026-09-07T10:00:00Z",
                    "assigned_by_id": 10,
                    "is_active": False,
                }
            },
        )

        self.assertFalse(assignment.is_active)
        assignment.save.assert_called_once_with(
            update_fields=["is_active"],
        )

    @patch("core.views.UserProjectAssignments.objects.get")
    @patch("core.views.Projects.objects.get")
    @patch("core.authorization.decorators.authorization_service")
    def test_update_rejects_user_id_change(
        self,
        service,
        project_get,
        assignment_get,
    ):
        service.can_manage_project_assignments.return_value = True

        project = SimpleNamespace(project_id=1)
        assignment = SimpleNamespace(
            assignment_id=5,
            user_id=20,
            project_id=1,
            project=project,
        )

        project_get.return_value = project
        assignment_get.return_value = assignment

        request = self.make_patch_request(
            self.authenticated_user,
            body=b'{"user_id":30}',
        )

        response = project_assignment_update(
            request,
            1,
            5,
        )

        self.assertEqual(response.status_code, 400)
        self.assertJSONEqual(
            response.content,
            {
                "error": "Only is_active can be modified",
            },
        )
